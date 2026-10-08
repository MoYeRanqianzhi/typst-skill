#!/usr/bin/env python3
"""Build a compact locator catalog from live, official Typst documentation."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import re
import sys
import tempfile
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from html.parser import HTMLParser
from http.client import HTTPException
from pathlib import Path
from urllib.parse import urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener

SEARCH_URL = "https://typst.app/assets/search.json"
API_ROOT = "https://api.github.com/repos/typst/typst"
DOCS_ROOT = "https://typst.app/docs/"
ARRAY_URL = DOCS_ROOT + "reference/foundations/array/"
TYPED_HTML_URL = DOCS_ROOT + "reference/html/typed/"
SYMBOL_URLS = {
    "sym": DOCS_ROOT + "reference/symbols/sym/",
    "emoji": DOCS_ROOT + "reference/symbols/emoji/",
}
CONSTANT_URLS = {
    "sys": DOCS_ROOT + "reference/foundations/sys/",
    "int": DOCS_ROOT + "reference/foundations/int/",
    "direction": DOCS_ROOT + "reference/layout/direction/",
    "alignment": DOCS_ROOT + "reference/layout/alignment/",
    "math": DOCS_ROOT + "reference/layout/h/",
}
DEFAULT_OUTPUT = Path(__file__).resolve().parent.parent / "references" / "catalog.json"
STABLE_VERSION = re.compile(r"(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)")
IDENTIFIER = re.compile(r"[A-Za-z_][A-Za-z0-9_-]*(?:\.[A-Za-z_][A-Za-z0-9_-]*)*")
COMMIT = re.compile(r"[0-9a-f]{40}")
KINDS = {"function", "type", "group", "category", "chapter", "parameter", "symbol", "constant"}
SCOPED_CATEGORIES = {"math", "html", "pdf"}
MAX_DOWNLOAD = 16 * 1024 * 1024


class NoRedirects(HTTPRedirectHandler):
    def redirect_request(self, request, response, code, message, headers, new_url):
        raise ValueError(f"Refusing redirect from {request.full_url} to {new_url}")


def required_text(value: object, label: str, limit: int = 2048) -> str:
    if not isinstance(value, str) or not value.strip() or len(value) > limit:
        raise ValueError(f"Invalid {label}: expected nonempty text up to {limit} characters")
    if any(ord(character) < 32 or ord(character) == 127 for character in value):
        raise ValueError(f"Invalid control character in {label}")
    value.encode("utf-8")
    return value


def documentation_url(route: str) -> str:
    """Accept only the site's canonical, unencoded documentation routes."""
    required_text(route, "documentation route")
    url = "https://typst.app" + route if route.startswith("/docs/") else route
    parsed = urlsplit(url)
    if (
        parsed.scheme != "https"
        or parsed.netloc != "typst.app"
        or not parsed.path.startswith("/docs/")
        or parsed.query
        or not re.fullmatch(r"/docs/(?:[A-Za-z0-9_.-]+/)*", parsed.path)
        or any(part in {".", ".."} for part in parsed.path.split("/"))
        or (parsed.fragment and not re.fullmatch(r"[A-Za-z0-9_.-]+", parsed.fragment))
    ):
        raise ValueError(f"Not a canonical official documentation URL: {route}")
    return url


def fetch(url: str, timeout: float, content_type: str) -> bytes:
    """Bound downloads and reject redirects before contacting another endpoint."""
    parsed = urlsplit(url)
    if url != SEARCH_URL:
        if parsed.netloc == "typst.app":
            documentation_url(url)
        elif not (
            url.startswith(API_ROOT + "/")
            and parsed.scheme == "https"
            and parsed.netloc == "api.github.com"
            and not parsed.query
            and not parsed.fragment
        ):
            raise ValueError(f"Refusing non-official download: {url}")
    request = Request(url, headers={
        "User-Agent": "Mozilla/5.0 (compatible; typst-skill-catalog/1)",
        "Accept": content_type,
    })
    try:
        with build_opener(NoRedirects()).open(request, timeout=timeout) as response:
            if response.status != 200 or response.url != url:
                raise ValueError(f"Unexpected response from {url}")
            if response.headers.get_content_type() != content_type:
                raise ValueError(f"Unexpected content type from {url}")
            body = response.read(MAX_DOWNLOAD + 1)
    except (OSError, HTTPException) as error:
        raise OSError(f"Download failed for {url}: {error}") from error
    if not body or len(body) > MAX_DOWNLOAD:
        raise ValueError(f"Empty or oversized response from {url}")
    return body


def fetch_object(url: str, timeout: float) -> dict:
    value = json.loads(fetch(url, timeout, "application/json").decode("utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"Expected a JSON object from {url}")
    return value


def resolve_release(version: str | None, timeout: float) -> dict:
    """Resolve the actual tag object, not the release's mutable target_commitish."""
    endpoint = "/releases/latest" if version is None else f"/releases/tags/v{version}"
    release = fetch_object(API_ROOT + endpoint, timeout)
    tag = required_text(release.get("tag_name"), "release tag")
    if not tag.startswith("v") or not STABLE_VERSION.fullmatch(tag[1:]):
        raise ValueError(f"Not a stable Typst release tag: {tag}")
    if release.get("draft") is not False or release.get("prerelease") is not False:
        raise ValueError(f"Release {tag} is a draft or prerelease")
    if version is not None and tag != f"v{version}":
        raise ValueError(f"Requested v{version}, but the release API returned {tag}")
    release_url = f"https://github.com/typst/typst/releases/tag/{tag}"
    if release.get("html_url") != release_url:
        raise ValueError("Release API returned an unexpected release URL")

    reference = fetch_object(f"{API_ROOT}/git/ref/tags/{tag}", timeout)
    if reference.get("ref") != f"refs/tags/{tag}":
        raise ValueError("Release tag reference does not match the requested tag")
    target = reference.get("object")
    visited = set()
    while True:
        if not isinstance(target, dict):
            raise ValueError("Malformed release tag target")
        commit = required_text(target.get("sha"), "release commit")
        if not COMMIT.fullmatch(commit) or commit in visited or len(visited) >= 8:
            raise ValueError("Invalid or cyclic release tag target")
        if target.get("type") == "commit":
            break
        if target.get("type") != "tag":
            raise ValueError("Release tag does not resolve to a commit")
        visited.add(commit)
        annotated = fetch_object(f"{API_ROOT}/git/tags/{commit}", timeout)
        if annotated.get("sha") != commit:
            raise ValueError("Annotated tag SHA does not match its URL")
        target = annotated.get("object")
    return {"version": tag[1:], "release_url": release_url, "release_commit": commit}


def read_items(body: bytes) -> list[dict]:
    """Validate every authoritative location; the full-text words/hits stay upstream."""
    source = json.loads(body.decode("utf-8"))
    if not isinstance(source, dict) or not isinstance(source.get("items"), list):
        raise ValueError("Search data must contain an items array")
    if not source["items"]:
        raise ValueError("Search items array is empty")
    items = []
    seen = set()
    for raw in source["items"]:
        if not isinstance(raw, dict):
            raise ValueError("Search item must be an object")
        source_kind = required_text(raw.get("kind"), "item kind")
        kind = source_kind.lower()
        if kind.startswith("parameter of "):
            kind = "parameter"
        elif kind == "symbols":
            kind = "group"
        if kind not in KINDS - {"symbol"}:
            raise ValueError(f"Unrecognized search item kind: {source_kind}")
        url = documentation_url(required_text(raw.get("route"), "item route"))
        if url in seen:
            raise ValueError(f"Duplicate search item URL: {url}")
        seen.add(url)
        keywords = raw.get("keywords", [])
        if not isinstance(keywords, list):
            raise ValueError(f"Keywords must be an array: {url}")
        items.append({
            "kind": kind,
            "title": required_text(raw.get("title"), "item title"),
            "url": url,
            "keywords": [required_text(keyword, "keyword") for keyword in keywords],
            "owner": source_kind.removeprefix("Parameter of ") if kind == "parameter" else "",
        })
    return items


def verify_documentation_version(items: list[dict], version: str) -> None:
    versions = set()
    for item in items:
        parsed = urlsplit(item["url"])
        match = re.fullmatch(r"/docs/changelog/([0-9]+\.[0-9]+\.[0-9]+)/", parsed.path)
        if match and not parsed.fragment and STABLE_VERSION.fullmatch(match[1]):
            versions.add(match[1])
    if not versions:
        raise ValueError("No stable changelog version in the official search index")
    newest = max(versions, key=lambda value: tuple(map(int, value.split("."))))
    if newest != version:
        raise ValueError(
            f"Documentation version mismatch: newest stable changelog is {newest}, "
            f"requested release is {version}; output was not replaced"
        )


class DocumentationHTML(HTMLParser):
    """Read structured anchors and metadata; never execute or retain page markup."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.symbols = []
        self.headings = []
        self.source_commits = set()
        self.sections = defaultdict(list)
        self.section = ""
        self.versions = set()
        self.has_main = False
        self.closed_html = False
        self.in_main = False
        self.heading = ""
        self.blocks = []
        self.open_blocks = []
        self.code_parts = None

    def handle_starttag(self, tag: str, attributes: list[tuple[str, str | None]]) -> None:
        attrs = dict(attributes)
        anchor = attrs.get("id", "") or ""
        if tag == "main":
            self.has_main = True
            self.in_main = True
        if self.in_main:
            if tag in {"h1", "h2", "h3", "h4", "h5", "h6"}:
                self.heading = anchor
            if tag in {"p", "li"}:
                self.open_blocks.append({
                    "tag": tag, "heading": self.heading, "text": [], "codes": [],
                })
            if tag == "code":
                self.code_parts = []
        if tag == "li" and (anchor.startswith("symbol-") or "data-codex-name" in attrs):
            self.symbols.append(attrs)
        if tag in {"h1", "h2", "h3", "h4"}:
            if anchor:
                self.headings.append((tag, anchor))
            if tag != "h4":
                self.section = anchor if tag == "h3" else ""
        if tag == "a":
            href = attrs.get("href", "") or ""
            match = re.match(
                r"https://github\.com/typst/typst/blob/([0-9a-f]{40})/",
                href,
            )
            if match:
                self.source_commits.add(match[1])
            version = re.fullmatch(
                r"(?:https://typst\.app)?/docs/changelog/([0-9]+\.[0-9]+\.[0-9]+)/", href
            )
            if version and STABLE_VERSION.fullmatch(version[1]):
                self.versions.add(version[1])

    def handle_endtag(self, tag: str) -> None:
        if tag == "code" and self.code_parts is not None:
            code = "".join(self.code_parts)
            for block in self.open_blocks:
                block["codes"].append(code)
            self.code_parts = None
        if tag in {"p", "li"} and self.open_blocks and self.open_blocks[-1]["tag"] == tag:
            block = self.open_blocks.pop()
            block["text"] = " ".join("".join(block["text"]).split())
            self.blocks.append(block)
        if tag == "main":
            self.in_main = False
        if tag == "html":
            self.closed_html = True

    def handle_data(self, data: str) -> None:
        if self.in_main:
            for block in self.open_blocks:
                block["text"].append(data)
            if self.code_parts is not None:
                self.code_parts.append(data)
        if self.section:
            self.sections[self.section].append(data)


def read_html(body: bytes) -> DocumentationHTML:
    parser = DocumentationHTML()
    parser.feed(body.decode("utf-8"))
    parser.close()
    if not parser.has_main or not parser.closed_html:
        raise ValueError("Incomplete official HTML page: missing main content or closing html tag")
    return parser


def typed_html_items(page: DocumentationHTML) -> list[dict]:
    """Supplement the search index's group with its explicit H3/H4 API anchors."""
    items = []
    for tag, anchor in page.headings:
        if tag not in {"h3", "h4"} or not anchor.startswith("functions-"):
            continue
        items.append({
            "kind": "function" if tag == "h3" else "parameter",
            "title": anchor.removeprefix("functions-"),
            "url": documentation_url(TYPED_HTML_URL + "#" + anchor),
            "keywords": [],
            "owner": "",
        })
    if not any(item["kind"] == "function" for item in items) or not any(
        item["kind"] == "parameter" for item in items
    ):
        raise ValueError("Typed HTML page is missing function or parameter headings")
    return items


def page_name(item: dict) -> str:
    parts = urlsplit(item["url"]).path.strip("/").split("/")[1:]
    if item["kind"] in {"chapter", "category"}:
        return ".".join(parts) or "overview"
    if len(parts) != 3 or parts[0] != "reference":
        raise ValueError(f"Unexpected API page route: {item['url']}")
    category, slug = parts[1:]
    return f"{category}.{slug}" if category in SCOPED_CATEGORIES else slug


def entry(name: str, kind: str, url: str, title: str, aliases=()) -> dict:
    result = {"name": name, "kind": kind, "url": documentation_url(url), "title": title}
    alternatives = sorted(set(aliases) - {name})
    if alternatives:
        result["aliases"] = alternatives
    return result


def build_entries(items: list[dict], global_aliases: dict[str, str]) -> list[dict]:
    """Derive scope from official routes, never from display titles or Rust names.

    Categories retain the reference namespace. A group's name gains a group:
    prefix only if it would shadow an actual callable, such as math.attach.
    Unqualified aliases aid lookup but do not establish a global binding.
    The literal types auto and none have no corresponding std module binding.
    Parameter ownership uses the longest known callable anchor so hyphenated
    names survive intact; nested constructors also use the index's owner hint.
    """
    pages = {item["url"]: item for item in items if not urlsplit(item["url"]).fragment}
    anchors = defaultdict(dict)
    entries = []
    lookup_names = {}

    for item in sorted(items, key=lambda value: len(urlsplit(value["url"]).fragment)):
        if item["kind"] == "parameter":
            continue
        parsed = urlsplit(item["url"])
        page_url = item["url"].split("#", 1)[0]
        if page_url not in pages:
            raise ValueError(f"Missing page entry for {item['url']}")
        base = page_name(pages[page_url])
        name = base
        if parsed.fragment:
            prefix, separator, member = parsed.fragment.partition("-")
            if prefix not in {"functions", "definitions"} or not separator:
                raise ValueError(f"Unknown API anchor: {item['url']}")
            if prefix == "functions" and base.split(".", 1)[0] in SCOPED_CATEGORIES:
                base = base.split(".", 1)[0]
            name = base + "." + ".".join(member.split("-definitions-"))
        aliases = []
        if item["kind"] in {"function", "type"}:
            if not IDENTIFIER.fullmatch(name):
                raise ValueError(f"Invalid API name derived from {item['url']}")
            if name not in {"auto", "none"}:
                aliases.append("std." + name)
            if item["kind"] == "function" and pages[page_url]["kind"] != "type":
                aliases.append(name.rsplit(".", 1)[-1])
            if name in global_aliases:
                aliases.extend([global_aliases[name], "std." + global_aliases[name]])
            anchors[page_url][parsed.fragment] = name
        elif item["kind"] == "category":
            aliases.append(name.rsplit(".", 1)[-1])
        lookup_names[name] = sorted(set(aliases) - {name})
        entries.append(entry(name, item["kind"], item["url"], item["title"], aliases + item["keywords"]))

    for item in items:
        if item["kind"] != "parameter":
            continue
        parsed = urlsplit(item["url"])
        page_url = item["url"].split("#", 1)[0]
        candidates = anchors[page_url]
        matching = [
            anchor for anchor in candidates
            if anchor and parsed.fragment.startswith(anchor + "-")
        ]
        if matching:
            prefix = max(matching, key=len)
            owner = candidates[prefix]
            parameter = parsed.fragment[len(prefix) + 1:]
        elif parsed.fragment.startswith("constructor-"):
            owners = [
                name for name in candidates.values()
                if name.rsplit(".", 1)[-1] == item["owner"]
            ]
            if len(owners) != 1:
                raise ValueError(f"Ambiguous constructor owner: {item['url']}")
            owner = owners[0]
            parameter = parsed.fragment.removeprefix("constructor-")
        elif parsed.fragment.startswith("parameters-") and "" in candidates:
            owner = candidates[""]
            parameter = parsed.fragment.removeprefix("parameters-")
        else:
            raise ValueError(f"No function anchor owns parameter {item['url']}")
        if not IDENTIFIER.fullmatch(parameter) or "." in parameter:
            raise ValueError(f"Invalid parameter anchor: {item['url']}")
        aliases = [f"{alias}:{parameter}" for alias in lookup_names[owner]]
        title = parameter if page_url == TYPED_HTML_URL else item["title"]
        entries.append(entry(
            f"{owner}:{parameter}", "parameter", item["url"], title, aliases + item["keywords"]
        ))

    callable_names = {item["name"] for item in entries if item["kind"] in {"function", "type"}}
    for item in entries:
        if item["kind"] == "group" and item["name"] in callable_names:
            item.setdefault("aliases", []).append(item["name"])
            item["name"] = "group:" + item["name"]
    return entries


def symbol_entries(namespace: str, page: DocumentationHTML) -> list[dict]:
    """Preserve symbol case and exact Unicode values, including whitespace symbols."""
    result = []
    for attributes in page.symbols:
        name = required_text(attributes.get("data-codex-name"), "symbol name")
        anchor = required_text(attributes.get("id"), "symbol anchor")
        value = attributes.get("data-value")
        if not isinstance(value, str) or not value or len(value) > 2048:
            raise ValueError(f"Invalid symbol value for {namespace}.{name}")
        value.encode("utf-8")
        title = required_text(attributes.get("data-unic-name") or name, "symbol title")
        if not IDENTIFIER.fullmatch(name) or anchor != "symbol-" + name:
            raise ValueError(f"Malformed symbol metadata in {SYMBOL_URLS[namespace]}")
        qualified = f"{namespace}.{name}"
        symbol = entry(
            qualified, "symbol", SYMBOL_URLS[namespace] + "#" + anchor, title,
            [name, "std." + qualified],
        )
        symbol["value"] = value
        result.append(symbol)
    if not result:
        raise ValueError(f"No symbol metadata found in {SYMBOL_URLS[namespace]}")
    return result


def constant_entries(namespace: str, page: DocumentationHTML) -> list[dict]:
    """Index declarations in explicit prose lists, not arbitrary code examples.

    Current docs do not give most constants individual headings. Their real
    summary or parent-page URL is retained; multiple bindings can share it.
    Lists establish global direction/alignment aliases, while math spacing
    aliases are only lookup shorthand for the math namespace. Runtime values
    such as sys.inputs and sys.version are never snapshotted into the catalog.
    """
    heading = {"sys": "", "math": "math-spacing"}.get(namespace, "summary")
    blocks = [block for block in page.blocks if block["heading"] == heading]
    text = " ".join(block["text"] for block in blocks)
    if namespace == "sys":
        evidence = "This module defines the following items:" in text
        codes = [block["codes"][0] for block in blocks if block["tag"] == "li" and block["codes"]]
        names = [code for code in codes if code.startswith("sys.") and code.count(".") == 1]
    elif namespace == "int":
        declarations = [block for block in blocks if "These values are accessible as" in block["text"]]
        evidence = bool(declarations)
        names = [code for block in declarations for code in block["codes"] if code.startswith("int.")]
    elif namespace in {"direction", "alignment"}:
        evidence = (
            "Possible values are:" in text
            and f"available globally and also in the {namespace} type" in text
        )
        names = [
            f"{namespace}.{block['codes'][0]}" for block in blocks
            if block["tag"] == "li" and block["codes"]
            and block["text"].startswith(block["codes"][0] + ":")
        ]
    else:
        declarations = [block for block in blocks if "use these constants" in block["text"]]
        evidence = "In mathematical formulas" in text and bool(declarations)
        names = [f"math.{code}" for block in declarations for code in block["codes"]]
    if not evidence or not names:
        raise ValueError(f"No explicit constant declarations found at {CONSTANT_URLS[namespace]}")
    if heading and heading not in {anchor for _, anchor in page.headings}:
        raise ValueError(f"Missing constant section #{heading} at {CONSTANT_URLS[namespace]}")

    result = []
    for name in names:
        if not IDENTIFIER.fullmatch(name) or name.count(".") != 1:
            raise ValueError(f"Invalid constant declaration: {name}")
        aliases = ["std." + name]
        if namespace in {"direction", "alignment", "math"}:
            unqualified = name.split(".", 1)[1]
            aliases.append(unqualified)
            if namespace != "math":
                aliases.append("std." + unqualified)
        url = CONSTANT_URLS[namespace] + ("#" + heading if heading else "")
        result.append(entry(name, "constant", url, name, aliases))
    return result


def build_catalog(version: str | None, timeout: float) -> dict:
    release = resolve_release(version, timeout)
    source = fetch(SEARCH_URL, timeout, "application/json")
    items = read_items(source)
    verify_documentation_version(items, release["version"])
    supplemental_urls = [*SYMBOL_URLS.values(), TYPED_HTML_URL, ARRAY_URL, *CONSTANT_URLS.values()]
    item_urls = {item["url"] for item in items}
    if not set(supplemental_urls) <= item_urls:
        raise ValueError("Official search index is missing a required supplemental page")
    with ThreadPoolExecutor(max_workers=4) as executor:
        bodies = list(executor.map(lambda url: fetch(url, timeout, "text/html"), supplemental_urls))
    pages = {url: read_html(body) for url, body in zip(supplemental_urls, bodies)}
    for url, page in pages.items():
        newest = max(
            page.versions, key=lambda value: tuple(map(int, value.split("."))), default=None
        )
        if newest != release["version"]:
            raise ValueError(f"Supplemental page version mismatch at {url}: {newest}")

    range_text = " ".join(" ".join(pages[ARRAY_URL].sections["definitions-range"]).split())
    if "available both in the array function" not in range_text or "scope and globally" not in range_text:
        raise ValueError("Official array.range documentation no longer confirms the global range alias")
    combined_items = list(items)
    for item in typed_html_items(pages[TYPED_HTML_URL]):
        if item["url"] not in item_urls:
            combined_items.append(item)
    entries = build_entries(combined_items, {"array.range": "range"})
    for namespace, url in SYMBOL_URLS.items():
        entries.extend(symbol_entries(namespace, pages[url]))
    for namespace, url in CONSTANT_URLS.items():
        entries.extend(constant_entries(namespace, pages[url]))

    names = set()
    urls = set()
    for item in entries:
        if item["name"] in names:
            raise ValueError(f"Duplicate catalog name: {item['name']} ({item['url']})")
        names.add(item["name"])
        urls.add(item["url"])
    if not item_urls <= urls:
        raise ValueError("Catalog omitted an official search item")
    observed_commits = sorted(set().union(*(page.source_commits for page in pages.values())))
    if not observed_commits:
        raise ValueError("Official documentation no longer exposes source commit links")
    return {
        "schema": 1,
        **release,
        "retrieved_at": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "documentation_source": SEARCH_URL,
        "source_sha256": hashlib.sha256(source).hexdigest(),
        "source_items": len(items),
        "documentation_version": release["version"],
        "documentation_snapshot": "live",
        "documentation_source_commits": observed_commits,
        "provenance_note": (
            "Live official docs, not a release-tag checkout. Documentation commits are observed "
            "HTML source links; version is checked against the newest stable changelog. "
            "A matching changelog does not certify that every live entry exists in the release compiler."
        ),
        "constant_coverage": (
            "Selected explicit system, integer-limit, direction, alignment, and math-spacing "
            "declarations, not an exhaustive constant inventory. Constants can share a parent "
            "page or section URL; their runtime values are not stored."
        ),
        "supplemental_sources": [
            {"url": url, "sha256": hashlib.sha256(body).hexdigest()}
            for url, body in zip(supplemental_urls, bodies)
        ],
        "entries": sorted(entries, key=lambda item: (item["name"], item["kind"], item["url"])),
    }


def write_catalog(output: Path, catalog: dict) -> None:
    """Replace only a fully built snapshot; failures preserve the previous file."""
    serialized = (json.dumps(catalog, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="wb", dir=output.parent, prefix=f".{output.name}.", suffix=".tmp", delete=False
        ) as stream:
            temporary = Path(stream.name)
            stream.write(serialized)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, output)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def stable_version(value: str) -> str:
    if not STABLE_VERSION.fullmatch(value):
        raise argparse.ArgumentTypeError("use a stable version such as 0.15.1")
    return value


def positive_timeout(value: str) -> float:
    try:
        timeout = float(value)
    except ValueError as error:
        raise argparse.ArgumentTypeError("timeout must be a positive number") from error
    if not math.isfinite(timeout) or timeout <= 0:
        raise argparse.ArgumentTypeError("timeout must be finite and positive")
    return timeout


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    selection = parser.add_mutually_exclusive_group(required=True)
    selection.add_argument("--version", type=stable_version, help="required stable documentation version, e.g. 0.15.1")
    selection.add_argument("--latest", action="store_true", help="explicitly select GitHub's latest stable release")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="catalog path (default: skill references/catalog.json)")
    parser.add_argument("--timeout", type=positive_timeout, default=45.0, help="per-request timeout in seconds (default: 45)")
    args = parser.parse_args(argv)
    try:
        catalog = build_catalog(args.version, args.timeout)
        output = args.output.expanduser().resolve()
        write_catalog(output, catalog)
    except (OSError, ValueError, HTTPException) as error:
        print(f"Catalog refresh failed: {error}", file=sys.stderr)
        return 1
    counts = Counter(item["kind"] for item in catalog["entries"])
    print(f"Catalog: {output}")
    print(f"Entries: {len(catalog['entries'])}; " + ", ".join(f"{kind}={count}" for kind, count in sorted(counts.items())))
    print(f"Release: {catalog['version']} ({catalog['release_commit']})")
    print(f"Release URL: {catalog['release_url']}")
    print(f"Search snapshot: {catalog['documentation_source']} ({catalog['source_items']} items)")
    print(f"Search SHA-256: {catalog['source_sha256']}")
    print(f"Retrieved: {catalog['retrieved_at']}")
    print("Observed live-doc source commits: " + ", ".join(catalog["documentation_source_commits"]))
    print("Live documentation is not an exact release-tag checkout.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

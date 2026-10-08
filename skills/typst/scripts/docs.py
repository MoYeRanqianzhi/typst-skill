#!/usr/bin/env python3
"""Find official Typst documentation and read a version-checked API section."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import tempfile
from collections import Counter
from datetime import datetime, timezone
from html.parser import HTMLParser
from http.client import HTTPException
from pathlib import Path
from urllib.parse import unquote, urldefrag, urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener


SKILL_ROOT = Path(__file__).resolve().parent.parent
RELEASE_API = "https://api.github.com/repos/typst/typst/releases/latest"


class LookupFailure(Exception):
    """A lookup cannot supply a trustworthy result within the requested mode."""


def check_url(url: str) -> None:
    """Keep both requested URLs and HTTP redirects on the official services."""
    parsed = urlsplit(url)
    allowed = (
        parsed.hostname == "typst.app" and parsed.path.startswith("/docs/")
    ) or url == RELEASE_API
    if (
        parsed.scheme != "https"
        or parsed.port not in (None, 443)
        or parsed.username
        or parsed.password
        or not allowed
    ):
        raise LookupFailure(f"Not an allowed official documentation URL: {url}")


class OfficialRedirects(HTTPRedirectHandler):
    def redirect_request(self, request, response, code, message, headers, newurl):
        check_url(newurl)
        return super().redirect_request(request, response, code, message, headers, newurl)


def fetch(url: str) -> bytes:
    check_url(url)
    request = Request(url, headers={"User-Agent": "typst-skill-docs/1.0"})
    with build_opener(OfficialRedirects).open(request, timeout=30) as response:
        check_url(response.url)
        declared_length = response.headers.get("Content-Length")
        if declared_length is not None:
            declared_length = int(declared_length)
            if declared_length < 0 or declared_length > 12 * 1024 * 1024:
                raise LookupFailure("Invalid or oversized documentation Content-Length.")
        data = response.read(12 * 1024 * 1024 + 1)
        # A bounded HTTPResponse.read does not raise for every short fixed-length body.
        if declared_length is not None and len(data) != declared_length:
            raise LookupFailure("Incomplete documentation response; nothing was cached. Retry the lookup.")
    if len(data) > 12 * 1024 * 1024:
        raise LookupFailure("Documentation response exceeds the 12 MiB limit.")
    return data


class Documentation(HTMLParser):
    """Extract main content while retaining heading offsets and literal code.

    Offsets refer to the unnormalized output. Normalizing before slicing would
    shift anchors, potentially returning a neighboring function's parameters.
    """

    VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}
    BLOCK = {"p", "div", "section", "li", "ul", "ol", "table", "tr", "details", "summary", "blockquote"}
    SKIP = {"script", "style", "svg", "button", "nav"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.parts = []
        self.length = 0
        self.main_depth = None
        self.suppressed = 0
        self.pre_depth = 0
        self.pre_parts = []
        self.headings = []
        self.versions = set()
        self.source_commits = set()
        self.has_main = False
        self.closed_main = False
        self.closed_html = False

    def append(self, text: str) -> None:
        if not self.pre_depth and text and not text.strip("\n"):
            trailing = "".join(self.parts[-3:])
            existing = len(trailing) - len(trailing.rstrip("\n"))
            text = "\n" * max(0, min(2 - existing, len(text)))
        if not text:
            return
        self.parts.append(text)
        self.length += len(text)

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        href = attrs.get("href") or ""
        version = re.search(r"/docs/changelog/(\d+\.\d+\.\d+)/", href)
        if version:
            self.versions.add(version.group(1))
        source = re.search(r"https://github.com/typst/typst/blob/([0-9a-f]{40})/", href)
        if source:
            self.source_commits.add(source.group(1))

        if tag == "main":
            self.main_depth = len(self.stack)
            self.has_main = True
        active = self.main_depth is not None
        skip = active and (tag in self.SKIP or attrs.get("role") == "tooltip" or "nav-button" in (attrs.get("class") or "").split())
        if tag not in self.VOID:
            self.stack.append((tag, skip, attrs))
        if skip:
            self.suppressed += 1
        if not active or self.suppressed:
            return
        if tag == "pre":
            self.pre_depth += 1
            if self.pre_depth == 1:
                self.pre_parts = []
        elif self.pre_depth:
            if tag == "br":
                self.pre_parts.append("\n")
        elif re.fullmatch(r"h[1-6]", tag):
            self.append("\n\n")
            self.headings.append((attrs.get("id"), int(tag[1]), self.length))
            self.append("#" * int(tag[1]) + " ")
        elif tag == "code" and not self.pre_depth:
            self.append("`")
        elif tag == "small":
            self.append(" ")
        elif tag in self.BLOCK or tag in {"br", "hr"}:
            self.append("\n")
        elif tag == "img" and attrs.get("alt"):
            self.append(f" [Image: {attrs['alt']}] ")

    def handle_startendtag(self, tag, attributes):
        self.handle_starttag(tag, attributes)
        if tag not in self.VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        if tag in self.VOID:
            return
        index = next((position for position in range(len(self.stack) - 1, -1, -1) if self.stack[position][0] == tag), None)
        if index is None:
            return
        attrs = self.stack[index][2]
        if self.main_depth is not None and not self.suppressed:
            if tag == "pre":
                self.pre_depth -= 1
                if self.pre_depth == 0:
                    code = "".join(self.pre_parts)
                    longest_run = max((len(run) for run in re.findall(r"`+", code)), default=0)
                    fence = "`" * max(3, longest_run + 1)
                    ending = "" if code.endswith("\n") else "\n"
                    self.append(f"\n\n{fence}\n{code}{ending}{fence}\n\n")
            elif self.pre_depth:
                pass
            elif tag == "code" and not self.pre_depth:
                self.append("`")
            elif tag in self.BLOCK or re.fullmatch(r"h[1-6]", tag):
                self.append("\n")
            elif tag == "a" and "pill" in (attrs.get("class") or "").split():
                self.append(" ")
            elif tag == "span" and "overview-param" in (attrs.get("class") or "").split():
                self.append(" ")
            elif tag == "small":
                self.append(" ")
            elif tag in {"td", "th"}:
                self.append(" | ")
        self.suppressed -= sum(int(frame[1]) for frame in self.stack[index:])
        del self.stack[index:]
        if tag == "main":
            self.main_depth = None
            self.closed_main = True
        elif tag == "html":
            self.closed_html = True

    def handle_data(self, text):
        if self.main_depth is not None and not self.suppressed:
            if self.pre_depth:
                self.pre_parts.append(text)
            else:
                self.append(re.sub(r"\s+", " ", text))

    def validate_complete(self) -> None:
        self.close()
        if not self.has_main or not self.closed_main or not self.closed_html:
            raise LookupFailure("Incomplete official HTML page; retry with --refresh or inspect its URL directly.")

    def version(self) -> str | None:
        return max(self.versions, key=lambda value: tuple(map(int, value.split(".")))) if self.versions else None

    def section(self, anchor: str) -> str:
        self.validate_complete()
        text = "".join(self.parts)
        if anchor:
            for position, (identifier, level, start) in enumerate(self.headings):
                if identifier == anchor:
                    end = next((offset for _, next_level, offset in self.headings[position + 1:] if next_level <= level), len(text))
                    return text[start:end].strip()
            raise LookupFailure(f"The official page no longer contains section #{anchor}; refresh the catalog or inspect the URL.")
        return text.strip()


def load_catalog(path: Path) -> dict:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict) or payload.get("schema") != 1 or not isinstance(payload.get("entries"), list) or not isinstance(payload.get("version"), str):
        raise LookupFailure("Unsupported catalog. Install the complete skill or rebuild its catalog.")
    if not re.fullmatch(r"\d+\.\d+\.\d+", payload["version"]):
        raise LookupFailure("Invalid catalog version. Rebuild its catalog.")
    for entry in payload["entries"]:
        if not isinstance(entry, dict) or any(not isinstance(entry.get(key), str) or not entry[key] for key in ("name", "kind", "title", "url")):
            raise LookupFailure("Invalid catalog entry: name, kind, title, and URL must be nonempty strings.")
        aliases = entry.get("aliases", [])
        if not isinstance(aliases, list) or any(not isinstance(alias, str) or not alias for alias in aliases):
            raise LookupFailure(f"Invalid aliases for {entry['name']}.")
        if entry["kind"] == "symbol" and (not isinstance(entry.get("value"), str) or not entry["value"]):
            raise LookupFailure(f"Invalid symbol value for {entry['name']}.")
        check_url(entry["url"])
    return payload


def relevance(entry: dict, query: str) -> int:
    # Unicode case folding also merges mathematical symbol variants, not just letter case.
    if query == entry.get("value"):
        return 1300
    if query == entry["name"]:
        return 1200
    if query in entry.get("aliases", []):
        return 1100
    query = query.casefold()
    name = entry["name"].casefold()
    aliases = [alias.casefold() for alias in entry.get("aliases", [])]
    title = entry["title"].casefold()
    if query == name:
        return 1000
    if query in aliases:
        return 900
    if query == title:
        return 800
    if name.startswith(query):
        return 600
    if name.rsplit(".", 1)[-1] == query:
        return 550
    words = query.split()
    haystack = " ".join([name, title, *aliases])
    if all(word in haystack for word in words):
        return 300 if query in name else 200
    return 0


def search(entries: list[dict], query: str, kind: str | None = None) -> list[dict]:
    # Spaces are legitimate Typst symbols; recognize their exact values before trimming names.
    if query and not query.strip():
        symbols = [entry for entry in entries if entry.get("value") == query and (not kind or entry["kind"] == kind)]
        if symbols:
            return sorted(symbols, key=lambda entry: entry["name"])
    query = query.strip()
    if not query:
        raise LookupFailure("The search term must not be empty.")
    hits = [(relevance(entry, query), entry) for entry in entries if not kind or entry["kind"] == kind]
    hits = [hit for hit in hits if hit[0]]
    hits.sort(key=lambda hit: (-hit[0], hit[1]["name"], hit[1]["kind"], hit[1]["url"]))
    return [entry for _, entry in hits]


def resolve(entries: list[dict], query: str, kind: str | None) -> dict:
    candidates = [entry for entry in entries if not kind or entry["kind"] == kind]
    query = query.strip()
    normalized = query.casefold()
    exact = [entry for entry in candidates if entry["name"] == query or entry["url"] == query]
    if not exact:
        exact = [entry for entry in candidates if query in entry.get("aliases", [])]
    if not exact:
        exact = [entry for entry in candidates if entry["name"].casefold() == normalized]
    if not exact:
        exact = [entry for entry in candidates if normalized in [alias.casefold() for alias in entry.get("aliases", [])]]
    if not exact:
        exact = [entry for entry in candidates if entry["title"].casefold() == normalized]
    unique = {entry["url"]: entry for entry in exact}
    if len(unique) == 1:
        return next(iter(unique.values()))
    suggestions = list(unique.values()) or search(candidates, query)[:6]
    reason = "Ambiguous name" if unique else "No exact documentation entry"
    choices = "\n".join(f"  {entry['name']} [{entry['kind']}] {entry['url']}" for entry in suggestions)
    raise LookupFailure(f"{reason}: {query}. Choose a qualified name or an exact URL.\n{choices}")


def default_cache() -> Path:
    base = os.environ.get("LOCALAPPDATA") if os.name == "nt" else os.environ.get("XDG_CACHE_HOME")
    return (Path(base) if base else Path.home() / ".cache") / "typst-skill" / "docs"


def read_page(url: str, cache_dir: Path, offline: bool, refresh: bool) -> tuple[dict, bool]:
    check_url(url)
    cache_path = cache_dir / (hashlib.sha256(url.encode()).hexdigest() + ".json")
    if cache_path.is_file() and not refresh:
        record = json.loads(cache_path.read_text(encoding="utf-8"))
        if not isinstance(record, dict) or record.get("url") != url or not isinstance(record.get("html"), str) or not isinstance(record.get("fetched_at"), str) or not record["fetched_at"]:
            raise LookupFailure(f"Invalid page cache: {cache_path}. Retry with --refresh.")
        return record, True
    if offline:
        raise LookupFailure(f"No cached page for {url}. Offline search still works; omit --offline once to fetch this page.")
    body = fetch(url).decode("utf-8")
    document = Documentation()
    document.feed(body)
    document.validate_complete()
    record = {"url": url, "fetched_at": datetime.now(timezone.utc).isoformat(), "html": body}
    cache_dir.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=cache_dir, suffix=".tmp", delete=False) as temporary:
        json.dump(record, temporary, ensure_ascii=False)
        temporary_path = Path(temporary.name)
    try:
        temporary_path.replace(cache_path)
    finally:
        temporary_path.unlink(missing_ok=True)
    return record, False


def positive_int(value: str) -> int:
    number = int(value)
    if number < 1:
        raise argparse.ArgumentTypeError("must be positive")
    return number


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog", type=Path, default=SKILL_ROOT / "references" / "catalog.json")
    commands = parser.add_subparsers(dest="command", required=True)
    find = commands.add_parser("search", help="Search the bundled official location catalog without network access")
    find.add_argument("query")
    find.add_argument("--kind")
    find.add_argument("--limit", type=positive_int, default=8)
    find.add_argument("--json", action="store_true")
    show = commands.add_parser("show", help="Read an exact official API entry, keeping its version and URL visible")
    show.add_argument("query")
    show.add_argument("--kind")
    show.add_argument("--section", help="Override the URL fragment with an exact heading ID")
    show.add_argument("--cache-dir", type=Path, default=default_cache())
    mode = show.add_mutually_exclusive_group()
    mode.add_argument("--offline", action="store_true", help="Read only an already cached page")
    mode.add_argument("--refresh", action="store_true", help="Fetch again instead of reading an existing cache")
    show.add_argument("--max-chars", type=positive_int, default=16000)
    show.add_argument("--offset", type=int, default=0, help="Continue a truncated section at this character offset")
    show.add_argument("--json", action="store_true")
    status = commands.add_parser("status", help="Show catalog provenance and optionally check the latest stable release")
    status.add_argument("--check-latest", action="store_true", help="Explicitly query GitHub; does not update any files")
    status.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    if getattr(args, "offset", 0) < 0:
        parser.error("--offset must not be negative")
    return args


def run(args) -> int:
    catalog = load_catalog(args.catalog)
    if args.command == "status":
        result = {key: value for key, value in catalog.items() if key != "entries"}
        result["entry_count"] = len(catalog["entries"])
        result["kinds"] = dict(sorted(Counter(entry["kind"] for entry in catalog["entries"]).items()))
        if args.check_latest:
            latest = json.loads(fetch(RELEASE_API))
            if not isinstance(latest, dict) or not isinstance(latest.get("tag_name"), str) or not re.fullmatch(r"v\d+\.\d+\.\d+", latest["tag_name"]):
                raise LookupFailure("Latest-release service returned an invalid stable release tag.")
            result["latest_stable"] = latest["tag_name"].removeprefix("v")
            result["catalog_is_latest"] = result["latest_stable"] == catalog["version"]
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0

    if args.command == "search":
        matches = search(catalog["entries"], args.query, args.kind)
        result = {"catalog_version": catalog["version"], "total": len(matches), "results": matches[:args.limit]}
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"Typst {catalog['version']} catalog: {len(matches)} matches")
            for entry in matches[:args.limit]:
                print(f"{entry['name']} [{entry['kind']}] — {entry['title']}\n  {entry['url']}")
            if not matches:
                print("No match. Try the official API name or an English topic; do not infer a signature from a missing result.")
        return 0 if matches else 1

    entry = resolve(catalog["entries"], args.query, args.kind)
    if entry["kind"] == "symbol":
        result = {"catalog_version": catalog["version"], "source": "bundled official symbol metadata", **entry}
    else:
        page_url, fragment = urldefrag(entry["url"])
        record, cached = read_page(page_url, args.cache_dir, args.offline, args.refresh)
        document = Documentation()
        document.feed(record["html"])
        version = document.version()
        if version != catalog["version"]:
            raise LookupFailure(f"Documentation version {version or 'unknown'} differs from catalog {catalog['version']}. Do not use this page as version-pinned evidence; inspect {entry['url']} and update the catalog deliberately.")
        anchor = args.section if args.section is not None else unquote(fragment)
        text = document.section(anchor)
        if args.offset >= len(text) and args.offset:
            raise LookupFailure(f"Offset exceeds the section length ({len(text)} characters).")
        end = min(args.offset + args.max_chars, len(text))
        result = {
            "name": entry["name"], "kind": entry["kind"], "url": page_url + ("#" + anchor if anchor else ""),
            "catalog_version": catalog["version"], "documentation_version": version,
            "documentation_source_commits": sorted(document.source_commits),
            "source": "cached official page" if cached else "live official page", "fetched_at": record["fetched_at"],
            "offset": args.offset, "total_chars": len(text), "next_offset": end if end < len(text) else None,
            "text": text[args.offset:end],
        }
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"{result['name']} — Typst {catalog['version']}\n{result['url']}\nSource: {result['source']}")
        if "text" in result:
            print(f"Fetched: {result['fetched_at']}\n\n{result['text']}")
            if result["next_offset"] is not None:
                print(f"\n[Truncated; continue with --offset {result['next_offset']} or increase --max-chars.]")
        else:
            print(f"{result.get('value', '')} — {result['title']}")
    return 0


def main(argv=None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    args = parse_args(argv)
    try:
        return run(args)
    except (LookupFailure, OSError, ValueError, KeyError, HTTPException) as error:
        print(f"docs: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

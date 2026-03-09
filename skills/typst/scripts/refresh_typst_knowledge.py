#!/usr/bin/env python3
"""Refresh bundled Typst reference artifacts from local source snapshots."""

from __future__ import annotations

import json
import re
import subprocess
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

import yaml

CATEGORY_MAP = {
    "foundations": "foundations",
    "model": "model",
    "text": "text",
    "math": "math",
    "layout": "layout",
    "visualize": "visualize",
    "introspection": "introspection",
    "loading": "data-loading",
    "pdf": "export",
    "html": "export",
}

MACRO_RE = re.compile(r"#\[(func|elem|ty|scope)(?:\((.*?)\))?\]")
NAME_RE = re.compile(r'name\s*=\s*"([^"]+)"')
TITLE_RE = re.compile(r'title\s*=\s*"([^"]+)"')
PUB_FN_RE = re.compile(r"pub\s+(?:const\s+)?fn\s+([A-Za-z_][A-Za-z0-9_]*)")
PUB_STRUCT_RE = re.compile(r"pub\s+struct\s+([A-Za-z_][A-Za-z0-9_]*)")
PUB_ENUM_RE = re.compile(r"pub\s+enum\s+([A-Za-z_][A-Za-z0-9_]*)")
PUB_CONST_RE = re.compile(r"pub\s+const\s+([A-Za-z_][A-Za-z0-9_]*)")
IMPL_RE = re.compile(r"impl\s+([A-Za-z_][A-Za-z0-9_]*)\s*\{")
TYPE_DECL_RE = re.compile(r"\btype\s+([A-Za-z_][A-Za-z0-9_]*)\s*;")


@dataclass
class ScopeFrame:
    canonical: str
    target_depth: int


def repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def skill_root() -> Path:
    return Path(__file__).resolve().parents[1]


def camel_to_kebab(name: str) -> str:
    name = name.rstrip("_")
    if name.endswith("Elem"):
        name = name[:-4]
    chunks = re.sub(r"([a-z0-9])([A-Z])", r"\1-\2", name).replace("_", "-")
    return chunks.lower()


def parse_attr_payload(payload: str | None) -> dict[str, object]:
    payload = payload or ""
    name_match = NAME_RE.search(payload)
    title_match = TITLE_RE.search(payload)
    return {
        "scope": "scope" in payload,
        "name": name_match.group(1) if name_match else None,
        "title": title_match.group(1) if title_match else None,
    }


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def git_info(path: Path) -> dict[str, str | None]:
    info: dict[str, str | None] = {"branch": None, "commit": None}
    try:
        info["branch"] = subprocess.check_output(
            ["git", "-C", str(path), "branch", "--show-current"],
            text=True,
            encoding="utf-8",
        ).strip() or None
        info["commit"] = subprocess.check_output(
            ["git", "-C", str(path), "rev-parse", "--short", "HEAD"],
            text=True,
            encoding="utf-8",
        ).strip() or None
    except Exception:
        pass
    return info


def typst_version(typst_root: Path) -> str:
    cargo = read_text(typst_root / "Cargo.toml")
    match = re.search(r'^version\s*=\s*"([^"]+)"', cargo, re.MULTILINE)
    if not match:
        raise RuntimeError("Failed to determine Typst version from Cargo.toml")
    return match.group(1)


def changelog_date(typst_root: Path, version: str) -> str | None:
    changelog = typst_root / "docs" / "changelog" / f"{version}.md"
    if not changelog.exists():
        return None
    text = read_text(changelog)
    match = re.search(r"Version .*?\(([A-Za-z]+ \d{1,2}, \d{4})\)", text)
    return match.group(1) if match else None


def collect_reference_pages(typst_root: Path) -> dict[str, list[dict[str, str]]]:
    docs_root = typst_root / "docs" / "reference"
    page_groups = {
        "language": sorted((docs_root / "language").glob("*.md")),
        "library": sorted((docs_root / "library").glob("*.md")),
        "export": sorted((docs_root / "export").glob("*.md")),
    }
    result: dict[str, list[dict[str, str]]] = {}
    for section, paths in page_groups.items():
        items = []
        for path in paths:
            body = read_text(path).strip().splitlines()
            if section == "library":
                title = path.stem.replace("-", " ").title()
            else:
                title = next((line[2:].strip() for line in body if line.startswith("# ")), path.stem.replace("-", " ").title())
            items.append(
                {
                    "slug": path.stem,
                    "title": title,
                    "path": path.relative_to(typst_root).as_posix(),
                }
            )
        result[section] = items
    return result


def collect_groups(typst_root: Path) -> list[dict[str, object]]:
    groups_path = typst_root / "docs" / "reference" / "groups.yml"
    groups = yaml.safe_load(read_text(groups_path))
    return [
        {
            "name": item["name"],
            "title": item["title"],
            "category": item["category"],
            "path": item.get("path", []),
        }
        for item in groups
    ]


def dedupe(entries: Iterable[dict[str, object]]) -> list[dict[str, object]]:
    seen: set[tuple[str, str, str]] = set()
    result = []
    for entry in entries:
        key = (str(entry["name"]), str(entry["kind"]), str(entry["source"]))
        if key in seen:
            continue
        seen.add(key)
        result.append(entry)
    return result


def collect_rust_metadata(source_root: Path) -> tuple[dict[str, str], set[str]]:
    rust_to_typst: dict[str, str] = {}
    scope_types: set[str] = set()

    for path in sorted(source_root.rglob("*.rs")):
        pending_attrs: list[tuple[str, dict[str, object]]] = []
        for raw_line in read_text(path).splitlines():
            line = raw_line.strip()

            if line.startswith("#["):
                macro_match = MACRO_RE.fullmatch(line)
                if macro_match:
                    pending_attrs.append((macro_match.group(1), parse_attr_payload(macro_match.group(2))))
                else:
                    pending_attrs.append(("other", {}))
                continue

            impl_match = IMPL_RE.search(line)
            if impl_match and any(kind == "scope" for kind, _ in pending_attrs):
                scope_types.add(impl_match.group(1))

            fn_match = PUB_FN_RE.search(line)
            struct_match = PUB_STRUCT_RE.search(line)
            enum_match = PUB_ENUM_RE.search(line)

            if fn_match:
                rust_name = fn_match.group(1)
                func_attr = next((attrs for kind, attrs in pending_attrs if kind == "func"), None)
                if func_attr:
                    rust_to_typst.setdefault(rust_name, str(func_attr["name"] or camel_to_kebab(rust_name)))
                    if func_attr["scope"]:
                        scope_types.add(rust_name)

            elif struct_match or enum_match:
                rust_name = (struct_match or enum_match).group(1)
                macro_kind, attrs = next(
                    ((kind, attrs) for kind, attrs in pending_attrs if kind in {"elem", "ty"}),
                    (None, None),
                )
                if macro_kind and attrs:
                    rust_to_typst.setdefault(rust_name, str(attrs["name"] or camel_to_kebab(rust_name)))
                    if attrs["scope"]:
                        scope_types.add(rust_name)

            if line and not line.startswith("///"):
                pending_attrs.clear()

    return rust_to_typst, scope_types


def scan_library(typst_root: Path) -> list[dict[str, object]]:
    source_root = typst_root / "crates" / "typst-library" / "src"
    rust_to_typst, scope_types = collect_rust_metadata(source_root)
    scoped_members: dict[str, str] = {}
    entries: list[dict[str, object]] = []

    for path in sorted(source_root.rglob("*.rs")):
        rel = path.relative_to(typst_root).as_posix()
        category_key = path.relative_to(source_root).parts[0]
        category = CATEGORY_MAP.get(category_key, category_key)
        pending_attrs: list[tuple[str, dict[str, object]]] = []
        scopes: list[ScopeFrame] = []
        depth = 0

        for lineno, raw_line in enumerate(read_text(path).splitlines(), start=1):
            line = raw_line.strip()

            while scopes and depth < scopes[-1].target_depth:
                scopes.pop()

            if line.startswith("#["):
                macro_match = MACRO_RE.fullmatch(line)
                if macro_match:
                    pending_attrs.append((macro_match.group(1), parse_attr_payload(macro_match.group(2))))
                else:
                    pending_attrs.append(("other", {}))
                depth += raw_line.count("{") - raw_line.count("}")
                continue

            current_scope = scopes[-1].canonical if scopes else None
            impl_match = IMPL_RE.search(line)
            if impl_match and (any(kind == "scope" for kind, _ in pending_attrs) or impl_match.group(1) in scope_types):
                rust_name = impl_match.group(1)
                scope_name = rust_to_typst.get(rust_name, camel_to_kebab(rust_name))
                target_depth = depth + raw_line.count("{") - raw_line.count("}")
                scopes.append(ScopeFrame(scope_name, target_depth))
                pending_attrs.clear()
                depth = target_depth
                continue

            fn_match = PUB_FN_RE.search(line)
            struct_match = PUB_STRUCT_RE.search(line)
            enum_match = PUB_ENUM_RE.search(line)
            const_match = PUB_CONST_RE.search(line) if current_scope else None
            scoped_type_match = TYPE_DECL_RE.search(line)

            if scoped_type_match and current_scope and any(kind in {"elem", "ty"} for kind, _ in pending_attrs):
                scoped_members[scoped_type_match.group(1)] = current_scope
                pending_attrs.clear()
                depth += raw_line.count("{") - raw_line.count("}")
                continue

            if fn_match:
                rust_name = fn_match.group(1)
                func_attr = next((attrs for kind, attrs in pending_attrs if kind == "func"), None)
                if func_attr:
                    typst_name = str(func_attr["name"] or camel_to_kebab(rust_name))
                    full_name = f"{current_scope}.{typst_name}" if current_scope else typst_name
                    rust_to_typst.setdefault(rust_name, typst_name)
                    entries.append(
                        {
                            "name": full_name,
                            "kind": "function",
                            "title": func_attr["title"] or typst_name,
                            "category": category,
                            "source": f"{rel}:{lineno}",
                            "scope": current_scope,
                        }
                    )

            elif struct_match or enum_match:
                rust_name = (struct_match or enum_match).group(1)
                macro_kind, attrs = next(
                    ((kind, attrs) for kind, attrs in pending_attrs if kind in {"elem", "ty"}),
                    (None, None),
                )
                if attrs:
                    typst_name = str(attrs["name"] or camel_to_kebab(rust_name))
                    rust_to_typst.setdefault(rust_name, typst_name)
                    member_scope = current_scope or scoped_members.get(rust_name)
                    full_name = f"{member_scope}.{typst_name}" if member_scope else typst_name
                    entries.append(
                        {
                            "name": full_name,
                            "kind": "element" if macro_kind == "elem" else "type",
                            "title": attrs["title"] or typst_name,
                            "category": category,
                            "source": f"{rel}:{lineno}",
                            "scope": member_scope,
                        }
                    )

            elif const_match:
                const_name = const_match.group(1)
                if const_name != "Self":
                    entries.append(
                        {
                            "name": f"{current_scope}.{const_name.lower().replace('_', '-')}",
                            "kind": "member",
                            "title": const_name,
                            "category": category,
                            "source": f"{rel}:{lineno}",
                            "scope": current_scope,
                        }
                    )

            if line and not line.startswith("///"):
                pending_attrs.clear()

            depth += raw_line.count("{") - raw_line.count("}")

    entries = sorted(entries, key=lambda item: (str(item["category"]), str(item["name"]), str(item["source"])))
    return dedupe(entries)


def blue_book_summary(blue_book_root: Path) -> dict[str, object]:
    readme = blue_book_root / "README.md"
    cargo = blue_book_root / "Cargo.toml"
    summary = {
        "has_readme": readme.exists(),
        "has_cargo": cargo.exists(),
        "topic_roots": [],
        "typst_dependency": None,
    }
    for section in ["tutorial", "topics", "template", "science", "graph", "misc"]:
        path = blue_book_root / "src" / section
        if path.exists():
            summary["topic_roots"].append(path.relative_to(blue_book_root).as_posix())
    if cargo.exists():
        content = read_text(cargo)
        match = re.search(r'typst\s*=\s*"([^"]+)"', content)
        if match:
            summary["typst_dependency"] = match.group(1)
    return summary


def render_markdown(snapshot: dict[str, object], pages: dict[str, list[dict[str, str]]], groups: list[dict[str, object]], entries: list[dict[str, object]]) -> str:
    by_category: dict[str, list[dict[str, object]]] = defaultdict(list)
    for entry in entries:
        by_category[str(entry["category"])].append(entry)

    counts = Counter(str(entry["kind"]) for entry in entries)
    lines = [
        "# Typst API Summary",
        "",
        f"- Generated at: `{snapshot['generated_at']}`",
        f"- Typst version: `{snapshot['typst']['version']}`",
        f"- Typst commit: `{snapshot['typst'].get('commit') or 'unknown'}`",
        f"- Blue-book Typst dependency: `{snapshot['blue_book'].get('typst_dependency') or 'unknown'}`",
        f"- Entries: `{len(entries)}` primary API records",
        f"- Kinds: `function={counts.get('function', 0)}`, `element={counts.get('element', 0)}`, `type={counts.get('type', 0)}`, `member={counts.get('member', 0)}`",
        f"- Official page sets: `language={len(pages.get('language', []))}`, `library={len(pages.get('library', []))}`, `export={len(pages.get('export', []))}`",
        f"- Official group pages: `{len(groups)}`",
        "",
        "Use `typst-api-index.json` plus `query_api_index.py` for a fast official inventory of library/category entries.",
        "Use `query_reference.py` for broader symbol, HTML-attribute, and blue-book-backed lookup.",
        "",
        "## Category Counts",
        "",
    ]

    for category in sorted(by_category):
        lines.append(f"- `{category}`: `{len(by_category[category])}`")

    lines.extend(["", "## Sample Entries", ""])
    for category in sorted(by_category):
        lines.append(f"### {category}")
        for entry in sorted(by_category[category], key=lambda item: str(item['name']))[:8]:
            lines.append(f"- `{entry['name']}` - `{entry['source']}`")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    root = repo_root()
    skill = skill_root()
    typst_root = root / "typst"
    blue_book_root = root / "The Raindrop-Blue Book"
    generated_root = skill / "reference" / "08-generated"
    generated_root.mkdir(parents=True, exist_ok=True)

    version = typst_version(typst_root)
    pages = collect_reference_pages(typst_root)
    groups = collect_groups(typst_root)
    entries = scan_library(typst_root)

    snapshot = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "typst": {
            "version": version,
            "changelog_date": changelog_date(typst_root, version),
            **git_info(typst_root),
        },
        "blue_book": {
            **git_info(blue_book_root),
            **blue_book_summary(blue_book_root),
        },
        "reference_pages": pages,
        "groups": groups,
        "entry_count": len(entries),
        "coverage_notes": [
            "This inventory focuses on official library/category entries extracted from typst-library source.",
            "Use the broader query_reference pipeline for symbols, HTML attributes, and blue-book-backed lookups.",
        ],
    }

    (generated_root / "source-snapshot.json").write_text(
        json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (generated_root / "typst-api-index.json").write_text(
        json.dumps(entries, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (generated_root / "typst-api-index.md").write_text(
        render_markdown(snapshot, pages, groups, entries),
        encoding="utf-8",
    )
    print(f"Refreshed Typst knowledge under {generated_root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

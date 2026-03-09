#!/usr/bin/env python3
"""Query the generated Typst API index."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path


def parse_args() -> argparse.Namespace:
    script_dir = Path(__file__).resolve().parent
    default_index = script_dir.parent / "reference" / "08-generated" / "typst-api-index.json"
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--index", type=Path, default=default_index)
    parser.add_argument("--name", default="")
    parser.add_argument("--category", default="")
    parser.add_argument("--kind", default="")
    parser.add_argument("--scope", default="")
    parser.add_argument("--source", default="")
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--json", action="store_true")
    return parser.parse_args()


def score_name(entry: dict[str, object], query: str) -> int:
    if not query:
        return 1

    name = str(entry.get("name", "")).casefold()
    title = str(entry.get("title", "")).casefold()
    query = query.casefold()
    score = 0
    name_parts = [part for part in re.split(r"[._-]", name) if part]
    title_parts = [part for part in re.split(r"[\s._-]", title) if part]

    if name == query:
        score += 400
    if any(part == query for part in name_parts):
        score += 220
    if name.endswith(f".{query}") or name.startswith(f"{query}.") or f".{query}." in name:
        score += 180
    if name.startswith(query):
        score += 120
    if query in name:
        score += 80
    if title == query:
        score += 60
    if any(part == query for part in title_parts):
        score += 40

    return score


def main() -> int:
    args = parse_args()
    if args.limit <= 0:
        print("--limit must be positive.", file=sys.stderr)
        return 2
    if not args.index.exists():
        print(f"Index file not found: {args.index}", file=sys.stderr)
        return 2

    data = json.loads(args.index.read_text(encoding="utf-8"))

    name_query = args.name.casefold()
    category_query = args.category.casefold()
    kind_query = args.kind.casefold()
    scope_query = args.scope.casefold()
    source_query = args.source.casefold()

    matches: list[tuple[int, dict[str, object]]] = []
    for entry in data:
        name_score = score_name(entry, name_query)
        if name_query and name_score <= 0:
            continue
        if category_query and category_query != str(entry.get("category", "")).casefold():
            continue
        if kind_query and kind_query != str(entry.get("kind", "")).casefold():
            continue
        if scope_query and scope_query != str(entry.get("scope", "")).casefold():
            continue
        if source_query and source_query not in str(entry.get("source", "")).casefold():
            continue
        matches.append((name_score, entry))

    matches.sort(key=lambda item: (-item[0], str(item[1].get("name", "")), str(item[1].get("source", ""))))
    ordered = [entry for _, entry in matches]

    if args.json:
        print(json.dumps(ordered[: args.limit], ensure_ascii=False, indent=2))
        return 0

    counts = Counter(str(entry.get("kind", "unknown")) for entry in ordered)
    print(f"Index: {args.index}")
    print(f"Matches: {len(ordered)}")
    if ordered:
        print("Kinds: " + ", ".join(f"{kind}={count}" for kind, count in sorted(counts.items())))
    for entry in ordered[: args.limit]:
        title = f" ({entry['title']})" if entry.get("title") and entry["title"] != entry.get("name") else ""
        scope = f" scope={entry['scope']}" if entry.get("scope") else ""
        print(f"- {entry['name']} [{entry['kind']}] {entry['category']}{title}{scope} -> {entry['source']}")
    if len(ordered) > args.limit:
        print(f"... {len(ordered) - args.limit} more")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

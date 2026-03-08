#!/usr/bin/env python3
"""Query the generated Typst API index."""

from __future__ import annotations

import argparse
import json
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
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--json", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    data = json.loads(args.index.read_text(encoding="utf-8"))

    name_query = args.name.casefold()
    category_query = args.category.casefold()
    kind_query = args.kind.casefold()

    matches = []
    for entry in data:
        if name_query and name_query not in str(entry["name"]).casefold():
            continue
        if category_query and category_query != str(entry["category"]).casefold():
            continue
        if kind_query and kind_query != str(entry["kind"]).casefold():
            continue
        matches.append(entry)

    if args.json:
        print(json.dumps(matches[: args.limit], ensure_ascii=False, indent=2))
        return 0

    counts = Counter(entry["kind"] for entry in matches)
    print(f"Index: {args.index}")
    print(f"Matches: {len(matches)}")
    if matches:
        print("Kinds: " + ", ".join(f"{kind}={count}" for kind, count in sorted(counts.items())))
    for entry in matches[: args.limit]:
        title = f" ({entry['title']})" if entry.get("title") and entry["title"] != entry["name"] else ""
        print(f"- {entry['name']} [{entry['kind']}] {entry['category']}{title} -> {entry['source']}")
    if len(matches) > args.limit:
        print(f"... {len(matches) - args.limit} more")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def score(item: dict[str, object], query: str) -> int:
    query = query.lower().strip()
    name = str(item.get("name", "")).lower()
    qualified = str(item.get("qualified_name", "")).lower()
    summary = str(item.get("summary", "")).lower()
    docs = str(item.get("docs", "")).lower()
    ident = str(item.get("source_ident", "")).lower()
    module = str(item.get("module", "")).lower()
    keywords = " ".join(item.get("keywords", [])) if isinstance(item.get("keywords"), list) else ""
    keywords = keywords.lower()

    value = 0
    if qualified == query:
        value += 220
    if name == query:
        value += 180
    if module and f"{module}.{name}" == query:
        value += 200
    if qualified.startswith(query):
        value += 120
    if name.startswith(query):
        value += 110
    if query in qualified:
        value += 90
    if query in name:
        value += 80
    if query in ident:
        value += 70
    if query in module:
        value += 60
    if query in keywords:
        value += 50
    if query in summary:
        value += 35
    if query in docs:
        value += 20
    return value


def find(items: list[dict[str, object]], query: str, kind: str | None, category: str | None, module: str | None, limit: int):
    hits = []
    for item in items:
        if kind and item.get("kind") != kind:
            continue
        if category and item.get("category") != category:
            continue
        if module and str(item.get("module", "")).lower() != module.lower():
            continue
        value = score(item, query)
        if value > 0:
            hits.append((value, item))
    hits.sort(key=lambda pair: (-pair[0], str(pair[1].get("qualified_name", pair[1].get("name", "")))))
    return [pair[1] for pair in hits[:limit]]


def find_docs(items: list[dict[str, object]], query: str, limit: int):
    query = query.lower().strip()
    hits = []
    for item in items:
        title = str(item.get("title", "")).lower()
        summary = str(item.get("summary", "")).lower()
        path = str(item.get("path", "")).lower()
        headings = item.get("headings", []) if isinstance(item.get("headings"), list) else []
        headings_blob = " ".join(headings).lower()
        value = 0
        if title == query:
            value += 120
        if query in title:
            value += 80
        if query in headings_blob:
            value += 60
        if query in path:
            value += 45
        if query in summary:
            value += 25
        if value > 0:
            hits.append((value, item))
    hits.sort(key=lambda pair: (-pair[0], str(pair[1].get("path", ""))))
    return [pair[1] for pair in hits[:limit]]


def infer_root(reference_file: Path, payload: dict[str, object]) -> Path:
    raw = Path(str(payload.get("project_root") or "."))
    if raw != Path(".") and raw.exists():
        return raw
    parents = reference_file.resolve().parents
    return parents[4] if len(parents) > 4 else reference_file.resolve().parent


def grep(root: Path, query: str, limit: int):
    query = query.lower().strip()
    variants = [query]
    if query.startswith("global."):
        suffix = query.split(".", 1)[1].strip()
        if suffix and suffix not in variants:
            variants.append(suffix)
    out = []
    for base in (root / "typst", root / "The Raindrop-Blue Book"):
        if not base.exists():
            continue
        for path in base.rglob("*"):
            if not path.is_file() or path.suffix.lower() not in {".rs", ".md", ".typ", ".toml", ".txt", ".yml", ".yaml"}:
                continue
            try:
                lines = path.read_text(encoding="utf-8").splitlines()
            except Exception:
                continue
            for index, line in enumerate(lines, 1):
                haystack = line.lower()
                if any(variant in haystack for variant in variants):
                    out.append({"path": path.relative_to(root).as_posix(), "line": index, "text": line.strip()})
                    if len(out) >= limit:
                        return out
    return out


def rit(item: dict[str, object]) -> str:
    label = item.get("qualified_name", item.get("name"))
    lines = [f"- `{label}` [{item.get('kind')}] - {item.get('summary', '')}"]
    source_file = item.get("source_file")
    source_line = item.get("source_line")
    if source_file:
        lines.append(f"  Source: `{source_file}:{source_line}`" if source_line else f"  Source: `{source_file}`")
    if item.get("module"):
        lines.append(f"  Module: `{item['module']}`")
    if item.get("signature"):
        lines.append(f"  Signature: `{str(item['signature']).splitlines()[0].strip()}`")
    if item.get("member_of") and not item.get("constructor"):
        lines.append(f"  Scope: `{item['member_of']}`")
    if item.get("deprecated_message"):
        lines.append(f"  Deprecated: `{item['deprecated_message']}`")
    return "\n".join(lines)


def rdoc(item: dict[str, object]) -> str:
    return f"- `{item.get('path')}` - {item.get('title')}"


def rgrep(item: dict[str, object]) -> str:
    return f"- `{item['path']}:{item['line']}` - {item['text']}"


def join_tokens(value):
    if not value:
        return ""
    return " ".join(value) if isinstance(value, list) else str(value)


def main() -> int:
    me = Path(__file__).resolve()
    skill = me.parent.parent
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", nargs="+")
    parser.add_argument("--name", nargs="+")
    parser.add_argument("--kind")
    parser.add_argument("--category")
    parser.add_argument("--module")
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--rebuild", action="store_true")
    parser.add_argument("--reference-file", type=Path, default=skill / "reference" / "generated" / "typst-reference.json")
    args = parser.parse_args()

    query = join_tokens(args.name) or join_tokens(args.query)
    if not query:
        print("Provide --name or --query.", file=sys.stderr)
        return 2
    if args.limit <= 0:
        print("--limit must be positive.", file=sys.stderr)
        return 2
    if args.rebuild:
        subprocess.run([sys.executable, str(me.parent / "build_reference.py")], check=True)

    payload = load(args.reference_file)
    root = infer_root(args.reference_file, payload)
    items = list(payload.get("items", [])) + list(payload.get("symbols", [])) + list(payload.get("bindings", [])) + list(payload.get("html_attributes", []))
    matches = find(items, query, args.kind, args.category, args.module, args.limit)
    docs = find_docs(list(payload.get("official_docs", [])), query, min(args.limit, 6))
    blue = find_docs(list(payload.get("bluebook", [])), query, min(args.limit, 6))
    raw = grep(root, query, min(args.limit, 8))

    if args.json:
        print(json.dumps({"matches": matches, "docs": docs, "bluebook": blue, "grep": raw}, ensure_ascii=False, indent=2))
        return 0

    lines = [f"# Query: {query}", "", "## API Matches", ""]
    lines.extend([rit(item) for item in matches] or ["- No indexed API match."])
    lines.extend(["", "## Official Docs", ""])
    lines.extend([rdoc(item) for item in docs] or ["- No official docs match."])
    lines.extend(["", "## Blue Book", ""])
    lines.extend([rdoc(item) for item in blue] or ["- No Blue Book match."])
    lines.extend(["", "## Raw Grep", ""])
    lines.extend([rgrep(item) for item in raw] or ["- No raw source match."])
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

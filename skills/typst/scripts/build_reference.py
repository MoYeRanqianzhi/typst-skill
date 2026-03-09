from __future__ import annotations

import argparse
import json
import re
import subprocess
import tomllib
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

CT = {
    "foundations": "Foundations",
    "data-loading": "Data Loading",
    "introspection": "Introspection",
    "layout": "Layout",
    "math": "Math",
    "model": "Model",
    "symbols": "Symbols",
    "text": "Text",
    "visualize": "Visualize",
    "pdf": "PDF",
    "html": "HTML",
}


def rt(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def rel(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except Exception:
        home = Path.home()
        cargo_git = home / ".cargo" / "git" / "checkouts"
        cargo_registry = home / ".cargo" / "registry" / "src"
        try:
            return f"external/cargo-git/{path.relative_to(cargo_git).as_posix()}"
        except Exception:
            pass
        try:
            return f"external/cargo-registry/{path.relative_to(cargo_registry).as_posix()}"
        except Exception:
            pass
        return path.name


def run(args: list[str]) -> str | None:
    try:
        result = subprocess.run(args, check=True, capture_output=True, text=True, encoding="utf-8")
        return result.stdout.strip() or None
    except Exception:
        return None


def gitinfo(path: Path) -> dict[str, str | None]:
    return {
        "commit": run(["git", "-C", str(path), "rev-parse", "HEAD"]),
        "remote": run(["git", "-C", str(path), "remote", "get-url", "origin"]),
        "tag": run(["git", "-C", str(path), "tag", "--points-at", "HEAD"]),
    }


def kebab(value: str) -> str:
    return re.sub(r"(?<!^)(?=[A-Z])", "-", value).replace("_", "-").lower()


def strip_generics(value: str) -> str:
    out = []
    depth = 0
    for char in value:
        if char == "<":
            depth += 1
            continue
        if char == ">":
            depth = max(depth - 1, 0)
            continue
        if depth == 0:
            out.append(char)
    return "".join(out)


def rust_base(value: str) -> str:
    return strip_generics(value).strip().rsplit("::", 1)[-1].strip()


def binding_name(value: str, known_names: dict[str, str]) -> str:
    base = rust_base(value).rstrip("_")
    if base in known_names:
        return known_names[base]
    if base.endswith("Elem"):
        return kebab(base.removesuffix("Elem")).rstrip("-")
    return kebab(base).rstrip("-")


def title(value: str) -> str:
    return value.replace("-", " ").title()


def summary(value: str) -> str:
    value = value.strip()
    return re.sub(r"\s+", " ", value.split("\n\n", 1)[0]).strip()


def m1(text: str, pattern: str):
    match = re.search(pattern, text, re.S)
    return match.group(1) if match else None


def ameta(attrs: list[str]) -> dict[str, object]:
    text = " ".join(attrs)
    keywords_match = m1(text, r"keywords\s*=\s*\[(.*?)\]")
    return {
        "name": m1(text, r"name\s*=\s*\"([^\"]+)\""),
        "title": m1(text, r"title\s*=\s*\"([^\"]+)\""),
        "scope": "scope" in text,
        "contextual": "contextual" in text,
        "constructor": "constructor" in text,
        "keywords": re.findall(r"\"([^\"]+)\"", keywords_match or ""),
        "deprecated_message": m1(text, r"message\s*=\s*\"([^\"]+)\""),
        "deprecated_until": m1(text, r"until\s*=\s*\"([^\"]+)\""),
    }


def cattr(lines: list[str], index: int):
    out = []
    depth = 0
    while index < len(lines):
        line = lines[index].rstrip("\n")
        out.append(line.strip())
        depth += line.count("[") - line.count("]")
        if depth <= 0:
            return " ".join(out), index
        index += 1
    return " ".join(out), index


def cfn(lines: list[str], index: int):
    out = []
    depth = 0
    seen = False
    while index < len(lines):
        line = lines[index].rstrip("\n")
        out.append(line)
        depth += line.count("(") - line.count(")")
        seen = seen or "(" in line
        if seen and depth <= 0 and "{" in line:
            return out, index
        index += 1
    return out, index


def cblock(lines: list[str], index: int):
    out = []
    depth = 0
    seen = False
    while index < len(lines):
        line = lines[index].rstrip("\n")
        out.append(line)
        seen = seen or "{" in line
        depth += line.count("{") - line.count("}")
        if seen and depth <= 0:
            return out, index
        index += 1
    return out, index


def bdelta(block: list[str]) -> int:
    return sum(line.count("{") - line.count("}") for line in block)


def cat(path: Path, lib: Path, html: Path) -> str | None:
    if path.is_relative_to(lib):
        relative = path.relative_to(lib)
        if relative.name == "symbols.rs":
            return "symbols"
        head = relative.parts[0]
        if head == "loading":
            return "data-loading"
        if head in {"foundations", "introspection", "layout", "math", "model", "pdf", "text", "visualize"}:
            return head
        return None
    if path.is_relative_to(html):
        return "html"
    return None


def parse_items(project: Path, typst: Path) -> list[dict[str, object]]:
    lib = typst / "crates" / "typst-library" / "src"
    html = typst / "crates" / "typst-html" / "src"
    files = sorted(lib.rglob("*.rs")) + sorted(html.rglob("*.rs"))
    known: dict[str, str] = {}
    scoped_members: dict[str, str] = {}
    items: list[dict[str, object]] = []

    for path in files:
        category = cat(path, lib, html)
        if not category:
            continue
        lines = rt(path).splitlines()
        docs: list[str] = []
        attrs: list[str] = []
        scopes: list[dict[str, object]] = []
        index = 0

        while index < len(lines):
            raw = lines[index]
            stripped = raw.strip()
            block = [raw]
            pushed = False

            if stripped.startswith("///"):
                docs.append(stripped[3:].lstrip())
                index += 1
                continue
            if stripped.startswith("#"):
                attr, index2 = cattr(lines, index)
                attrs.append(attr)
                index = index2 + 1
                continue

            impl_match = re.match(r"impl\s+([A-Za-z_][A-Za-z0-9_]*)\s*\{", stripped)
            if impl_match and any(attr.strip() == "#[scope]" for attr in attrs):
                rust_ident = impl_match.group(1)
                scopes.append({
                    "name": known.get(rust_ident, kebab(rust_ident.rstrip("_"))),
                    "depth": raw.count("{") - raw.count("}"),
                })
                docs = []
                attrs = []
                index += 1
                pushed = True
                continue

            fn_match = re.match(r"pub\s+fn\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(", stripped)
            struct_match = re.match(r"pub\s+struct\s+([A-Za-z_][A-Za-z0-9_]*)", stripped)
            enum_match = re.match(r"pub\s+enum\s+([A-Za-z_][A-Za-z0-9_]*)", stripped)
            type_match = re.match(r"pub\s+type\s+([A-Za-z_][A-Za-z0-9_]*)", stripped)
            scoped_type_match = re.match(r"type\s+([A-Za-z_][A-Za-z0-9_]*)\s*;", stripped)

            if scoped_type_match and scopes and any(
                attr.startswith("#[elem") or attr.startswith("#[ty") for attr in attrs
            ):
                scoped_members[scoped_type_match.group(1)] = str(scopes[-1]["name"])
                docs = []
                attrs = []
                index += 1
                continue

            if fn_match and any(attr.startswith("#[func") for attr in attrs):
                header, index2 = cfn(lines, index)
                meta = ameta(attrs)
                rust_ident = fn_match.group(1)
                scope = scopes[-1]["name"] if scopes else None
                name = meta["name"] or rust_ident.rstrip("_")
                qualified = scope if meta["constructor"] and scope else f"{scope}.{name}" if scope else str(name)
                items.append(
                    {
                        "kind": "function",
                        "category": category,
                        "name": name,
                        "qualified_name": qualified,
                        "title": meta["title"] or title(str(name)),
                        "summary": summary("\n".join(docs)),
                        "docs": "\n".join(docs).strip(),
                        "keywords": meta["keywords"],
                        "source_ident": rust_ident,
                        "source_file": rel(path, project),
                        "source_line": index + 1,
                        "signature": "\n".join(header).strip(),
                        "member_of": scope,
                        "scope": bool(meta["scope"]),
                        "contextual": bool(meta["contextual"]),
                        "constructor": bool(meta["constructor"]),
                        "deprecated_message": meta["deprecated_message"],
                        "deprecated_until": meta["deprecated_until"],
                    }
                )
                if meta["scope"]:
                    known[rust_ident] = str(name)
                docs = []
                attrs = []
                block = header
                index = index2 + 1
            elif (struct_match or enum_match or type_match) and (
                any(attr.startswith("#[ty") for attr in attrs) or any(attr.startswith("#[elem") for attr in attrs)
            ):
                rust_ident = (struct_match or enum_match or type_match).group(1)
                meta = ameta(attrs)
                is_element = any(attr.startswith("#[elem") for attr in attrs)
                name = str(meta["name"] or (kebab(rust_ident.removesuffix("Elem")) if is_element else kebab(rust_ident)))
                known[rust_ident] = name
                member_of = scopes[-1]["name"] if scopes else scoped_members.get(rust_ident)
                if "{" in raw:
                    parsed_block, index2 = cblock(lines, index)
                    block = parsed_block
                    index = index2 + 1
                else:
                    index += 1
                items.append(
                    {
                        "kind": "element" if is_element else "type",
                        "category": category,
                        "name": name,
                        "qualified_name": f"{member_of}.{name}" if member_of else name,
                        "title": meta["title"] or title(name),
                        "summary": summary("\n".join(docs)),
                        "docs": "\n".join(docs).strip(),
                        "keywords": meta["keywords"],
                        "source_ident": rust_ident,
                        "source_file": rel(path, project),
                        "source_line": index - len(block) + 1,
                        "member_of": member_of,
                        "scope": bool(meta["scope"]),
                        "deprecated_message": meta["deprecated_message"],
                        "deprecated_until": meta["deprecated_until"],
                    }
                )
                docs = []
                attrs = []
            else:
                if stripped:
                    docs = []
                    if stripped != "#[scope]":
                        attrs = []
                index += 1

            if scopes and not pushed:
                scopes[-1]["depth"] += bdelta(block)
                while scopes and scopes[-1]["depth"] <= 0:
                    scopes.pop()

    return items


def parse_bindings(project: Path, typst: Path, known_names: dict[str, str] | None = None) -> list[dict[str, object]]:
    known_names = known_names or {}
    out = []
    seen = set()
    module_re = re.compile(r'Module::new\(\"([^\"]+)\",\s*([A-Za-z_][A-Za-z0-9_]*)\)')
    global_re = re.compile(r'(?:pub(?:\([^)]*\))?\s+)?fn\s+define\s*\(\s*([A-Za-z_][A-Za-z0-9_]*)\s*:\s*&mut\s+Scope\b')
    define_re = re.compile(r'\b([A-Za-z_][A-Za-z0-9_]*)\.define\(\"([^\"]+)\"\s*,')
    elem_re = re.compile(r'\b([A-Za-z_][A-Za-z0-9_]*)\.define_elem::<([A-Za-z_][A-Za-z0-9_]*)>\(\)')
    func_re = re.compile(r'\b([A-Za-z_][A-Za-z0-9_]*)\.define_func::<([A-Za-z_][A-Za-z0-9_:]*)>\(\)')
    type_re = re.compile(r'\b([A-Za-z_][A-Za-z0-9_]*)\.define_type::<([^>]+)>\(\)')

    def emit(module: str, name: str, path: Path, offset: int, rust: str | None = None):
        key = (module, name, rel(path, project), offset)
        if key in seen:
            return
        seen.add(key)
        entry = {
            "kind": "binding",
            "module": module,
            "name": name,
            "qualified_name": f"{module}.{name}",
            "source_file": rel(path, project),
            "source_line": text[: offset].count("\n") + 1,
        }
        if rust:
            entry["source_ident"] = rust
        out.append(entry)

    for path in sorted((typst / "crates" / "typst-library" / "src").rglob("*.rs")):
        text = rt(path)
        module_vars = [(m.group(1), m.group(2)) for m in module_re.finditer(text)]
        module_vars.extend(("global", m.group(1)) for m in global_re.finditer(text))
        module_vars = list(dict.fromkeys(module_vars))
        for module, var in module_vars:
            for match in define_re.finditer(text):
                if match.group(1) == var:
                    emit(module, match.group(2), path, match.start())
            for match in elem_re.finditer(text):
                if match.group(1) == var:
                    rust = match.group(2)
                    emit(module, binding_name(rust, known_names), path, match.start(), rust)
            for match in func_re.finditer(text):
                if match.group(1) == var:
                    rust = match.group(2)
                    emit(module, binding_name(rust, known_names), path, match.start(), rust)
            for match in type_re.finditer(text):
                if match.group(1) == var:
                    rust = match.group(2)
                    emit(module, binding_name(rust, known_names), path, match.start(), rust)

        for match in define_re.finditer(text):
            if match.group(1) == "global":
                emit("global", match.group(2), path, match.start())
        for match in elem_re.finditer(text):
            if match.group(1) == "global":
                rust = match.group(2)
                emit("global", binding_name(rust, known_names), path, match.start(), rust)
        for match in func_re.finditer(text):
            if match.group(1) == "global":
                rust = match.group(2)
                emit("global", binding_name(rust, known_names), path, match.start(), rust)
        for match in type_re.finditer(text):
            if match.group(1) == "global":
                rust = match.group(2)
                emit("global", binding_name(rust, known_names), path, match.start(), rust)
    return out
def parse_html(project: Path):
    base = Path.home() / ".cargo" / "git" / "checkouts"
    data_files = sorted(base.glob("typst-assets-*/**/files/html/data.rs"))
    info_files = sorted(base.glob("typst-assets-*/**/src/html.rs"))
    if not data_files or not info_files:
        return [], [], None
    data = data_files[0]
    text = rt(data)
    attrs = []
    for index, match in enumerate(
        re.finditer(r"AttrInfo::new\(\s*\"([^\"]+)\",\s*\"((?:[^\"\\]|\\.)*)\",", text, re.S)
    ):
        docs = match.group(2).replace("\\n", "\n").replace('\\\"', '"')
        attrs.append(
            {
                "index": index,
                "kind": "html-attribute",
                "category": "html",
                "name": match.group(1),
                "qualified_name": f"html.attr.{match.group(1)}",
                "title": title(match.group(1)),
                "summary": docs,
                "docs": docs,
                "source_file": rel(data, project),
            }
        )
    attr_map = {item["index"]: item for item in attrs}
    elems = []
    for match in re.finditer(
        r"ElemInfo::new\(\s*\"([^\"]+)\",\s*\"((?:[^\"\\]|\\.)*)\",\s*&\[(.*?)\],\s*\)", text, re.S
    ):
        indices = [int(value) for value in re.findall(r"\d+", match.group(3))]
        docs = match.group(2).replace("\\n", "\n").replace('\\\"', '"')
        elems.append(
            {
                "kind": "html-element",
                "category": "html",
                "name": match.group(1),
                "qualified_name": f"html.{match.group(1)}",
                "title": title(match.group(1)),
                "summary": docs,
                "docs": docs,
                "source_file": rel(data, project),
                "attributes": [attr_map[idx] for idx in indices if idx in attr_map],
            }
        )
    return elems, attrs, {"data_file": rel(data, project), "info_file": rel(info_files[0], project)}


def parse_symbols(project: Path) -> list[dict[str, object]]:
    roots = sorted((Path.home() / ".cargo" / "registry" / "src").glob("index.crates.io-*/codex-*/src/modules"))
    if not roots:
        return []
    out = []
    seen = set()
    child_re = re.compile(r"(?<!\S)(\.[A-Za-z0-9_-]+(?:\.[A-Za-z0-9_-]+)*)")
    for module in ("sym", "emoji"):
        path = roots[0] / f"{module}.txt"
        current = None
        for lineno, raw in enumerate(rt(path).splitlines(), start=1):
            if not raw.strip() or raw.strip().startswith("//"):
                continue
            if raw.startswith(" ") or raw.startswith("\t"):
                if current is None:
                    continue
                for suffix in child_re.findall(raw.strip()):
                    name = f"{current['name']}{suffix}"
                    key = (module, name)
                    if key in seen:
                        continue
                    seen.add(key)
                    out.append(
                        {
                            "kind": "symbol-module-entry",
                            "category": "symbols",
                            "module": module,
                            "name": name,
                            "qualified_name": f"{module}.{name}",
                            "title": title(name.replace(".", " ")),
                            "summary": raw.strip(),
                            "raw": raw.rstrip(),
                            "source_file": rel(path, project),
                            "source_line": lineno,
                        }
                    )
                continue
            name = raw.split(maxsplit=1)[0]
            key = (module, name)
            if key in seen:
                continue
            seen.add(key)
            current = {
                "kind": "symbol-module-entry",
                "category": "symbols",
                "module": module,
                "name": name,
                "qualified_name": f"{module}.{name}",
                "title": title(name),
                "summary": raw.strip(),
                "raw": raw.rstrip(),
                "source_file": rel(path, project),
                "source_line": lineno,
            }
            out.append(current)
    return out


def docs_index(project: Path, typst: Path) -> list[dict[str, object]]:
    out = []
    root = typst / "docs"
    for path in sorted(root.rglob("*.md")):
        text = rt(path)
        relative = path.relative_to(root)
        if relative.parts[:2] == ("reference", "library"):
            title_line = title(path.stem)
        else:
            title_line = next((line.strip()[2:].strip() for line in text.splitlines() if line.strip().startswith("# ")), title(path.stem))
        out.append(
            {
                "kind": "official-doc",
                "path": rel(path, project),
                "section": relative.parts[0],
                "title": title_line,
                "summary": summary(text),
            }
        )
    return out


def blue_index(project: Path, blue: Path) -> list[dict[str, object]]:
    out = []
    root = blue / "src"
    for path in sorted(root.rglob("*.typ")):
        text = rt(path)
        headings = [line.strip()[2:].strip() for line in text.splitlines() if line.strip().startswith("= ")][:6]
        label = headings[0] if headings else path.stem.replace("-", " ")
        out.append(
            {
                "kind": "bluebook",
                "path": rel(path, project),
                "section": path.relative_to(root).parts[0],
                "title": label,
                "summary": label,
                "headings": headings,
            }
        )
    return out


def render_summary(payload: dict[str, object]) -> str:
    stats = payload["stats"]
    typst = payload["sources"]["typst"]
    bluebook = payload["sources"]["bluebook"]
    lines = [
        "# Typst Reference Summary",
        "",
        f"- Generated at: `{payload['generated_at']}`",
        f"- Typst version: `{typst['version']}`",
        f"- Typst commit: `{typst['commit']}`",
        f"- Blue Book commit: `{bluebook['commit']}`",
        f"- Rust API items: `{stats['rust_items']}`",
        f"- HTML typed elements: `{stats['html_elements']}`",
        f"- HTML attributes: `{stats['html_attributes']}`",
        f"- Symbol blocks: `{stats['symbol_blocks']}`",
        f"- Bindings indexed: `{stats['bindings']}`",
        f"- Official docs indexed: `{stats['official_docs']}`",
        f"- Blue Book files indexed: `{stats['bluebook_entries']}`",
        "",
        "## Category Counts",
        "",
    ]
    for key, value in sorted(stats["category_counts"].items()):
        lines.append(f"- `{key}`: `{value}`")
    return "\n".join(lines) + "\n"


def build(project: Path, typst: Path, blue: Path, out: Path):
    version = tomllib.loads(rt(typst / "Cargo.toml"))["workspace"]["package"]["version"]
    items = parse_items(project, typst)
    known_names = {}
    for item in items:
        ident = item.get("source_ident")
        name = item.get("name")
        if ident and name:
            known_names.setdefault(str(ident), str(name))
    bindings = parse_bindings(project, typst, known_names)
    html_items, html_attrs, html_meta = parse_html(project)
    symbols = parse_symbols(project)
    docs = docs_index(project, typst)
    bluebook = blue_index(project, blue)
    counted = items + html_items + html_attrs + symbols
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "project_root": ".",
        "sources": {
            "typst": {"path": rel(typst, project), "version": version, **gitinfo(typst)},
            "bluebook": {"path": rel(blue, project), **gitinfo(blue)},
            "html_assets": html_meta,
        },
        "stats": {
            "rust_items": len(items),
            "html_elements": len(html_items),
            "html_attributes": len(html_attrs),
            "symbol_blocks": len(symbols),
            "bindings": len(bindings),
            "official_docs": len(docs),
            "bluebook_entries": len(bluebook),
            "kind_counts": dict(Counter(item["kind"] for item in counted)),
            "category_counts": dict(Counter(item["category"] for item in counted if item.get("category"))),
        },
        "categories": [{"name": key, "title": value} for key, value in CT.items()],
        "items": items + html_items,
        "bindings": bindings,
        "html_attributes": html_attrs,
        "symbols": symbols,
        "official_docs": docs,
        "bluebook": bluebook,
    }
    out.mkdir(parents=True, exist_ok=True)
    (out / "typst-reference.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    (out / "summary.md").write_text(render_summary(payload), encoding="utf-8")
    return payload


def main() -> int:
    script = Path(__file__).resolve()
    skill = script.parent.parent
    project = skill.parent.parent
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", type=Path, default=project)
    parser.add_argument("--typst-root", type=Path, default=project / "typst")
    parser.add_argument("--bluebook-root", type=Path, default=project / "The Raindrop-Blue Book")
    parser.add_argument("--out-dir", type=Path, default=skill / "reference" / "generated")
    args = parser.parse_args()
    payload = build(args.project_root.resolve(), args.typst_root.resolve(), args.bluebook_root.resolve(), args.out_dir.resolve())
    print(json.dumps({"output": str((args.out_dir / "typst-reference.json").resolve()), "stats": payload["stats"]}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

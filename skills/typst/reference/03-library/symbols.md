# Symbols

## Use

- Handle named symbols, emoji, shorthand-like symbol lookup, and symbol-heavy Typst authoring tasks.

## Authoritative Sources

- `typst/docs/reference/library/symbols.md`
- `typst/docs/reference/groups.yml`
- `typst/crates/typst-library/src/symbols.rs`
- `skills/typst/reference/generated/typst-reference.json`

## Key Guidance

- Treat `symbols` as an official library category, not just a side topic under modules.
- Distinguish between `sym`, `emoji`, and math-specific symbol usage.
- For exact symbol block or variant lookup, prefer `query_reference.py` because the comprehensive index covers far more symbol metadata than the lightweight inventory.

## Typical Tasks

- Find a named symbol or emoji.
- Explain whether a symbol is better written through `sym`, `emoji`, or math syntax.
- Diagnose portability issues when symbol-heavy content renders differently across contexts.

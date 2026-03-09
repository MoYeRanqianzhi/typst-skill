# Symbols

## Use

- Handle named symbols, emoji, symbol categories, and symbol lookup strategy.

## Authoritative Sources

- `typst/docs/reference/library/symbols.md`
- `typst/docs/reference/groups.yml`
- `typst/crates/typst-library/src/symbols.rs`
- `The Raindrop-Blue Book/src/tutorial/reference-math-symbols.typ`

## What Lives Here

- General named symbols under `sym`.
- Emoji under `emoji`.
- Math-specific symbol usage that overlaps with formulas but should still be checked against the math library.
- Group-page metadata in `groups.yml` for `sym` and `emoji`.

## Lookup Rules

- Use `sym` for general named symbols.
- Use `emoji` for named emoji.
- Use formula constructs from the math library when the symbol participates in equation semantics rather than simple glyph insertion.
- For exact symbol discovery, prefer `python scripts/query_reference.py --query <symbol-name>` because the comprehensive index covers far more symbol entries than the lightweight official inventory.

## Common Pitfalls

- Confusing a general symbol with a math-specific operator or delimiter API.
- Assuming a blue-book symbol example reflects the newest official naming without checking the current index.
- Treating symbol lookup as a pure text search when many names are grouped or namespaced.

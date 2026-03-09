# Foundations

## Use

- Handle core value types, utility functions, module-level helpers, and the broad base layer of the Typst standard library.

## Authoritative Sources

- `typst/docs/reference/library/foundations.md`
- `typst/crates/typst-library/src/foundations/**`
- `typst/docs/reference/groups.yml`

## What Lives Here

- primitive and container types such as `array`, `dictionary`, `str`, `bytes`, `version`, and `datetime`
- content-facing helpers such as `content`, `repr`, and conversion-related utilities
- globally visible helper modules and scopes such as `std`, `calc`, and `sys`
- many exact APIs that other categories build on top of

## Guidance

- Treat `foundations` as the broad base layer, not as a single narrow feature page.
- When answering exact API questions here, query the generated indexes instead of relying on memory.
- Distinguish between `calc` helpers, `sys` environment values, and category-specific library functions.
- If a task mixes data conversion, formatting, and generic computation, this category is often involved even when the user did not name it.

## Exact Lookup

- Start with `python skills/typst/scripts/query_reference.py --query <name>`.
- Use `query_api_index.py` when you want a quick official source anchor by name or category.

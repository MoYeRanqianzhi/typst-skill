# Introspection

## Use

- Handle `counter`, `state`, `locate`, `location`, `query`, and `metadata` work.

## Authoritative Sources

- `typst/docs/reference/library/introspection.md`
- `typst/crates/typst-library/src/introspection/**`
- `typst/docs/reference/language/context.md`
- `typst/docs/changelog/0.14.0.md`

## Key APIs

- stateful tracking: `counter`, `state`
- location-aware lookup: `locate`, `location`, `query`
- explicit document metadata: `metadata`

## Rules of Thumb

- These APIs are layout-aware and may require multiple compilation passes to stabilize.
- Query only locatable and semantically stable structures.
- Keep show rules, labels, and query selectors aligned so you are querying the structure that actually exists after realization.
- Avoid self-referential logic that changes the very structure it later queries.

## Version Notes

- `0.14.0` changed some locatable-element behavior and expanded accessibility-sensitive document structure, so old recipes may drift.

## Also See

- `../05-recipes/state-counter-query-locator.md`

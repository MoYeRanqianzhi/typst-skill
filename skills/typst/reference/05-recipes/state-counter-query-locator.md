# State, Counter, Query, Locator

## Use

- Handle the most error-prone location-aware and multi-pass Typst logic.

## Authoritative Sources

- `typst/docs/reference/language/context.md`
- `typst/docs/reference/library/introspection.md`
- `The Raindrop-Blue Book/src/tutorial/doc-stateful.typ`
- `The Raindrop-Blue Book/src/tutorial/reference-counter-state.typ`

## Debug Framework

1. Decide whether the issue depends on page position, numbering, or query results.
2. Confirm whether the target element is locatable or queryable.
3. Check whether a show rule or template changes the structure being queried.
4. Explain multi-pass layout instead of treating it as a random bug.

## Common Pitfalls

- Treating `query` like an ordinary collection lookup.
- Writing self-affecting show rules that change the same structure later queried.

# State, Counter, Query, Locator

## Use

- Handle the most error-prone location-aware and multi-pass Typst logic.

## Authoritative Sources

- `typst/docs/reference/language/context.md`
- `typst/docs/reference/library/introspection.md`
- `typst/docs/changelog/0.14.0.md`
- `typst/docs/changelog/0.14.1.md`
- `The Raindrop-Blue Book/src/tutorial/doc-stateful.typ`
- `The Raindrop-Blue Book/src/tutorial/reference-counter-state.typ`

## Debug Framework

1. Decide whether the issue depends on page position, numbering, or query results.
2. Confirm whether the target element is locatable or queryable.
3. Check whether a show rule or template changes the structure being queried.
4. Explain multi-pass layout instead of treating it as a random bug.
5. Reduce to one counter or one query target before making broader changes.

## High-Value `0.14.x` Notes

- `0.14.0` made many more elements locatable without explicit labels.
- `0.14.1` fixed a first-iteration heading counter regression that could surface in numbering functions.
- `typst query` gained `--target` in `0.14.0`, which matters for backend-aware diagnostics.

## Common Pitfalls

- Treating `query` like an ordinary collection lookup.
- Writing self-affecting show rules that change the same structure later queried.
- Assuming first-iteration counter or state values are already final.
- Reinserting queried elements without checking for structural feedback.

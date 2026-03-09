# std, calc, sys, sym, emoji, and Group Pages

## Use

- Handle official `groups.yml` pages and grouped helper namespaces that should not be mixed blindly into category summaries.

## Authoritative Sources

- `typst/docs/reference/groups.yml`
- `typst/docs/src/lib.rs`
- `typst/crates/typst-library/src/foundations/**`
- `typst/crates/typst-library/src/math/**`
- `typst/crates/typst-library/src/symbols.rs`

## Main Groups

- `std`: globally accessible definitions and a safe escape hatch when a name is shadowed.
- `calc`: numeric and computational helpers plus constants such as `pi`, `tau`, `e`, and `inf`.
- `sys`: runtime-facing values such as `sys.version` and `sys.inputs`.
- `sym` and `emoji`: named symbols and emoji.
- Math group pages: Variants, Styles, Sizes, Under/Over, Roots, Attach, and Left/Right.
- Typed HTML group page: the `html` typed layer is documented as a grouped page rather than a plain library category.

## Guidance

- Open grouped pages when an API is exposed through a namespace or grouped documentation page rather than the plain category document.
- Do not assume every grouped item is imported by default.
- Query exact module members with `query_reference.py` or `query_api_index.py` before answering exact API questions.
- Distinguish grouped pages from library categories, especially in math-heavy tasks and system-input tasks.

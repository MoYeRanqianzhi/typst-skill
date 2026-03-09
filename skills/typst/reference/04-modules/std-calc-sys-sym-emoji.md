# std, calc, sys, sym, emoji, and Group Pages

## Use

- Handle official `groups.yml` module pages and grouped helper functions that should not be mixed into category docs blindly.

## Authoritative Sources

- `typst/docs/reference/groups.yml`
- `typst/docs/src/lib.rs`
- `typst/crates/typst-library/src/foundations/**`
- `typst/crates/typst-library/src/math/**`

## Key Modules and Groups

- `std` for access to globally visible definitions and shadowed names.
- `calc` for computation and numeric helpers.
- `sys` for version, inputs, and system-facing values.
- `sym` and `emoji` for named symbols and emoji.
- Math group pages such as variants, styles, sizes, roots, attach, and `lr`.

## Guidance

- Query exact module members with `query_reference.py` or `query_api_index.py` first.
- Distinguish category pages from group pages, especially in math-heavy tasks.

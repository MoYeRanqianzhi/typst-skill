# Styling, Layout, and Show Rules

## Use

- Handle `set` and `show` rules, selectors, page setup, layout elements, and style propagation.

## Authoritative Sources

- `typst/docs/reference/language/styling.md`
- `typst/docs/guides/page-setup.md`
- `The Raindrop-Blue Book/src/tutorial/scripting-style.typ`
- `The Raindrop-Blue Book/src/tutorial/scripting-layout.typ`

## Core Concepts

- `set` configures defaults; `show` overrides presentation logic.
- Page-level configuration is safest near the start of a document or in a template.
- For layout issues, inspect `page`, `block`, `box`, `align`, `place`, `stack`, and `grid` before adding hacks.
- Keep `show` selectors as narrow as possible to reduce side effects.

## Common Pitfalls

- Changing `set page(...)` mid-document and triggering unexpected page breaks.
- Using absolute placement to hide a structural problem.
- Writing highly global `show` rules with position-sensitive logic.

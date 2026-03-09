# Styling, Layout, and Show Rules

## Use

- Handle `set` and `show` rules, selectors, style propagation, page setup, and layout-aware styling.

## Authoritative Sources

- `typst/docs/reference/language/styling.md`
- `typst/docs/guides/page-setup.md`
- `typst/docs/reference/library/layout.md`
- `The Raindrop-Blue Book/src/tutorial/scripting-style.typ`
- `The Raindrop-Blue Book/src/tutorial/scripting-layout.typ`

## Core Concepts

- `set` configures defaults; `show` transforms or replaces presentation behavior.
- Keep selectors narrow to avoid surprising global side effects.
- Put page configuration near the start of the document or inside a template.
- Prefer solving structural problems structurally before reaching for absolute placement.

## High-Value Topics

- `set page(...)` and page-level margins, numbering, and headers
- `show heading`, `show link`, and other semantic element selectors
- `block`, `box`, `align`, `place`, `stack`, `grid`, `columns`
- backend-aware styling with `target()`

## Common Mistakes

- changing `set page(...)` mid-document without considering page breaks
- using global `show` rules where a local selector or wrapper would do
- relying on paged layout tricks for HTML output

## Also See

- `../03-library/layout.md`
- `../05-recipes/plugins-html-pdf-svg-png.md`

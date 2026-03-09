# Layout

## Use

- Handle page geometry, page breaks, regions, alignment, placement, and layout composition.

## Authoritative Sources

- `typst/docs/reference/library/layout.md`
- `typst/docs/guides/page-setup.md`
- `typst/crates/typst-library/src/layout/**`

## Key APIs

- page-level control: `page`, `pagebreak`, `columns`
- region and box composition: `block`, `box`, `grid`, `stack`, `align`
- measurement and placement: `measure`, `place`

## Guidance

- Prefer stable page and region rules over manual spacing hacks.
- Put major page setup decisions in templates or near the document start.
- Use `place` intentionally; it is powerful but can hide structural problems when overused.
- Re-check layout-heavy patterns when targeting HTML because paged assumptions do not automatically carry over.

## Also See

- `../02-language/styling-layout-and-show-rules.md`
- `export-and-platform.md`

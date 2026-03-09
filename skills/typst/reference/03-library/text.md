# Text

## Use

- Handle text styling, inline semantics, casing helpers, raw text, and text-adjacent export semantics.

## Authoritative Sources

- `typst/docs/reference/library/text.md`
- `typst/crates/typst-library/src/text/**`
- `typst/docs/changelog/0.14.0.md`

## Coverage Map

- Core text: `text`, `linebreak`, `space`, `smartquote`, `raw`, `lorem`.
- Emphasis and decoration: `highlight`, `underline`, `overline`, `strike`, `smallcaps`.
- Vertical shifts and case transforms: `sub`, `super`, `lower`, `upper`.
- Font/language behavior through text settings and language helpers.

## Guidance

- Separate text-element questions from structure (`model`) and layout (`layout`) questions.
- Inline emphasis should stay semantic when possible because export backends and accessibility care about meaning, not only appearance.
- Use `raw` for literal text or code-like content, not as a workaround for ordinary styling.
- In `0.14.x`, many inline semantics also affect locatability and export tagging.

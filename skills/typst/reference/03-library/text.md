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

## `text` Parameter Quick Reference

```typst
// Signature (most-used parameters)
#text(
  size: 12pt,        // font size (length)
  font: "New Computer Modern", // font family (string or array)
  fill: black,       // text color (color | gradient | pattern)
  weight: "regular", // "thin" | "light" | "regular" | "medium" | "bold" | int 100-900
  style: "normal",   // "normal" | "italic" | "oblique"
  tracking: 0pt,     // letter spacing
  spacing: 100%,     // word spacing as percentage of space width
  lang: "en",        // language for hyphenation and smart quotes
)[Content here]

// Set rule — applies to all subsequent text
#set text(font: "Libertinus Serif", size: 11pt, fill: luma(30))
```

## Emphasis and Decoration

```typst
// highlight — background marker
#highlight(fill: yellow)[Important text]
#highlight(fill: rgb("#cce5ff"), extent: 2pt)[With padding]

// underline — with customizable stroke
#underline[Basic underline]
#underline(stroke: 1.5pt + red, offset: 3pt)[Styled underline]
#underline(evade: false)[Underline through descenders]

// strike — strikethrough
#strike[Deleted text]
#strike(stroke: 2pt + red)[Bold deletion]

// overline
#overline[Overlined text]
```

## Subscript and Superscript

```typst
// sub and super for inline shifts
H#sub[2]O is water.

E = mc#super[2]

// Nested or styled
#text(fill: blue)[x#sub[#text(fill: red)[i]]]
```

## Case Transforms

```typst
#upper[hello world]   // → HELLO WORLD
#lower[HELLO WORLD]   // → hello world
#smallcaps[Small Caps Text]
```

## Raw Text and Code Blocks

```typst
// Inline code
This is `inline code` in a sentence.

// Block code with language highlighting
#raw(lang: "python", block: true)[
def greet(name):
    return f"Hello, {name}!"
]

// Raw block via markup sugar
```python
def greet(name):
    return f"Hello, {name}!"
`` `

// Customizing raw text appearance via set rule
#show raw: set text(font: "JetBrains Mono", size: 9pt)
```

## Placeholder Text

```typst
// Generate lorem ipsum placeholder text
#lorem(50)

// Useful for layout testing
#rect(width: 200pt)[#lorem(30)]
```

## Common Combination Patterns

```typst
// Bold colored heading-like text
#text(size: 18pt, weight: "bold", fill: navy)[Section Title]

// Small gray annotation
#text(size: 8pt, fill: luma(120))[Last updated: 2025-01-01]

// Highlighted code keyword
#highlight(fill: rgb("#f0f0f0"))[`async`] keyword

// Decorated label
#underline(stroke: 0.5pt + gray)[#text(tracking: 1pt)[CHAPTER ONE]]
```

## Guidance

- Separate text-element questions from structure (`model`) and layout (`layout`) questions.
- Inline emphasis should stay semantic when possible because export backends and accessibility care about meaning, not only appearance.
- Use `raw` for literal text or code-like content, not as a workaround for ordinary styling.
- In `0.14.x`, many inline semantics also affect locatability and export tagging.

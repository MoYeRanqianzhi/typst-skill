# Tables, Figures, Bibliography, and Outline

## Use

- Handle common report, paper, and book composition tasks that rely on Typst model semantics.

## Authoritative Sources

- `typst/docs/reference/library/model.md`
- `typst/docs/guides/tables.md`
- `typst/docs/guides/accessibility.md`
- `typst/docs/changelog/0.14.0.md`
- `The Raindrop-Blue Book/src/tutorial/reference-bibliography.typ`
- `The Raindrop-Blue Book/src/tutorial/reference-layout.typ`

## Pattern Checklist

- Tables: stabilize columns, headers, footers, and line logic before styling.
- Figures: prefer `figure`; add `figure.alt` when the figure's meaning needs a textual representation.
- Bibliography: centralize style and source configuration in the template or document preamble.
- Outline: stabilize heading levels and numbering before generating outlines or page references.

## Tricky Spots

- Complex tables may need PDF-specific accessibility extras or at least explicit summaries and careful header structure.
- Bibliography locators and citation behavior are style-dependent; keep them semantic and avoid formatting them manually.
- Show rules that restyle headings or figure captions can change outline or query behavior indirectly.
- HTML and PDF may render the same semantic structure differently; keep semantics stable and let backends diverge where appropriate.

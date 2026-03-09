# Accessibility and HTML

## Use

- Handle accessibility-sensitive Typst work and HTML-specific output decisions.
- Use this recipe when the task involves tagged PDF, PDF/UA, PDF/A, alt text, artifacts, or HTML-targeted templates and show rules.

## Authoritative Sources

- `typst/docs/guides/accessibility.md`
- `typst/docs/reference/export/pdf.md`
- `typst/docs/reference/export/html.md`
- `typst/docs/reference/library/model.md`
- `typst/docs/reference/library/math.md`
- `typst/docs/changelog/0.14.0.md`

## Core Rules

- Prefer semantic Typst markup over visual imitation. Real `heading`, `figure`, `table`, `quote`, and list structure help both PDF and HTML.
- `figure.alt` and `math.equation.alt` are semantic tools, not compliance stickers. Add them when they improve comprehension for Assistive Technology.
- Use `pdf.artifact` only for purely decorative or layout-only content.
- Current official docs state that PDF/A and PDF/UA cannot be chosen simultaneously in one export setting.
- For HTML-specific structure, prefer typed HTML helpers such as `html.div` over ad hoc raw strings when possible.

## Practical Workflow

1. Decide whether the target is PDF, HTML, or both.
2. If PDF accessibility matters, first review semantic structure, then alt text, then artifacts.
3. If exact PDF conformance matters, open `typst/docs/reference/export/pdf.md` and choose the standard intentionally.
4. If HTML is first-class, inspect `target()` branching and typed HTML elements/attributes.
5. Re-check figures, equations, tables, decorative elements, and reading order.

## Common Pitfalls

- Adding alternative text mechanically without considering whether it hides useful surrounding structure.
- Wrapping meaningful content in `pdf.artifact`.
- Assuming a visually pleasing PDF automatically becomes meaningful HTML.
- Assuming all HTML behavior can be inferred from PDF-oriented show rules.

## Precise Lookup

- `python skills/typst/scripts/query_reference.py --query figure.alt`
- `python skills/typst/scripts/query_reference.py --query math.equation.alt`
- `python skills/typst/scripts/query_reference.py --query pdf.artifact`
- `python skills/typst/scripts/query_reference.py --query html.div`
- `python skills/typst/scripts/query_reference.py --query aria-`

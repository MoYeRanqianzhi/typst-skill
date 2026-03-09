# Model

## Use

- Handle the document model: headings, lists, quotes, figures, tables, bibliography, references, links, and other semantic block structures.

## Authoritative Sources

- `typst/docs/reference/library/model.md`
- `typst/crates/typst-library/src/model/**`
- `typst/docs/changelog/0.14.0.md`

## Key Areas

- document structure: `document`, `title`, `heading`, `outline`
- block and list structures: `par`, `quote`, `list`, `enum`, `terms`
- scholarly and cross-reference elements: `figure`, `table`, `bibliography`, `cite`, `ref`
- inline semantic links and notes: `link`, `footnote`

## Version Notes

- `0.14.0` added `title`.
- `0.14.0` added `figure.alt` and expanded accessibility-sensitive output.
- `0.14.0` added multiple table headers and subheaders.

## Guidance

- Prefer semantic model elements over purely visual styling.
- Solve outline, caption, bibliography, and reference logic structurally, not with manual text hacks.
- When output accessibility matters, this category is central.

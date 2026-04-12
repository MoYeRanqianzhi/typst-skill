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

## Headings

```typst
// Markup sugar
= Level 1 Heading
== Level 2 Heading
=== Level 3 Heading

// Function form with explicit depth
#heading(level: 2)[Custom Heading]

// Numbering — applied via set rule
#set heading(numbering: "1.1")

= Introduction        // → 1 Introduction
== Background          // → 1.1 Background
== Motivation          // → 1.2 Motivation
= Methods              // → 2 Methods

// Supplement text for references
#set heading(numbering: "1.", supplement: [Section])
```

## Outline (Table of Contents)

```typst
// Basic table of contents
#outline()

// Customized outline
#outline(
  title: [Table of Contents],
  indent: auto,
  depth: 3,           // only include levels 1-3
)
```

## Lists and Enumerations

```typst
// Unordered list (markup)
- Item A
- Item B
  - Nested item

// Ordered list (markup)
+ First
+ Second
+ Third

// Custom list markers
#set list(marker: ([◆], [▸], [--]))
- Level 1
  - Level 2
    - Level 3

// Custom enum numbering
#set enum(numbering: "(a)")
+ Alpha
+ Beta
+ Gamma

// Term list (definition list)
/ Term: Description of the term
/ Another: Its description
```

## Figures and Captions

```typst
// Basic figure with caption
#figure(
  image("chart.png", width: 80%),
  caption: [Monthly revenue growth in 2025.],
) <fig-revenue>

// Reference a figure
See @fig-revenue for details.

// Figure with table content
#figure(
  table(
    columns: 3,
    [Name], [Age], [City],
    [Alice], [30], [Zurich],
    [Bob], [25], [Berlin],
  ),
  caption: [Participant demographics.],
) <tbl-demo>

// Alt text for accessibility (0.14.0+)
#figure(
  image("photo.jpg"),
  caption: [A sunset over the mountains.],
  alt: [Orange and purple sunset behind snow-capped peaks],
)
```

## Tables

```typst
// Basic table
#table(
  columns: (1fr, 2fr, 1fr),
  align: (center, left, right),
  // Header row
  table.header(
    [*ID*], [*Description*], [*Price*],
  ),
  [001], [Widget A], [\$9.99],
  [002], [Widget B], [\$14.50],
  [003], [Widget C], [\$7.25],
)

// Styled table with stroke and fill
#table(
  columns: 3,
  stroke: 0.5pt + gray,
  fill: (x, y) => if y == 0 { luma(230) },
  table.header([*Name*], [*Score*], [*Grade*]),
  [Alice], [95], [A],
  [Bob],   [82], [B],
  [Carol], [78], [C],
)

// Cell spanning
#table(
  columns: 3,
  table.cell(colspan: 3)[#align(center)[*Full Report*]],
  [A], [B], [C],
)
```

## Bibliography and Citations

```typst
// Load a bibliography file
#bibliography("refs.bib")

// Set citation style
#set bibliography(style: "ieee")

// Cite in text
As shown by @einstein1905 and @turing1950.

// Explicit cite forms
#cite(<einstein1905>, form: "prose")  // Einstein (1905)
```

## Links and Footnotes

```typst
// Hyperlink
#link("https://typst.app")[Typst website]

// Footnote
This claim needs support.#footnote[See appendix A for derivation.]
```

## Version Notes

- `0.14.0` added `title`.
- `0.14.0` added `figure.alt` and expanded accessibility-sensitive output.
- `0.14.0` added multiple table headers and subheaders.

## Guidance

- Prefer semantic model elements over purely visual styling.
- Solve outline, caption, bibliography, and reference logic structurally, not with manual text hacks.
- When output accessibility matters, this category is central.

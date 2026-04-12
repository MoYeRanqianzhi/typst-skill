# Layout

## Use

- Handle page geometry, page breaks, regions, alignment, placement, and layout composition.

## Authoritative Sources

- `typst/docs/reference/library/layout.md`
- `typst/docs/guides/page-setup.md`
- `typst/crates/typst-library/src/layout/**`

---

## Page Setup

### Basic Page Configuration

```typst
// A4 page with custom margins
#set page(
  paper: "a4",
  margin: (top: 2.5cm, bottom: 2cm, left: 2.5cm, right: 2cm),
)

// US Letter with symmetric margins
#set page(paper: "us-letter", margin: 1in)
```

### Page with Header, Footer, and Columns

```typst
#set page(
  paper: "a4",
  margin: (top: 3cm, bottom: 2.5cm, x: 2cm),
  header: align(right)[_Draft_],
  footer: context align(center)[#counter(page).display("1 / 1", both: true)],
  columns: 2,
)
```

### Key `page` Parameters

| Parameter  | Type / Example                       | Description                    |
|-----------|--------------------------------------|--------------------------------|
| `paper`   | `"a4"`, `"us-letter"`, `"a5"`       | Predefined paper size          |
| `width`   | `21cm`                               | Custom width (overrides paper) |
| `height`  | `29.7cm`                             | Custom height                  |
| `margin`  | `1cm`, `(x: 2cm, y: 1.5cm)`         | Uniform or per-side margins    |
| `columns` | `2`                                  | Number of columns              |
| `header`  | content                              | Repeated header content        |
| `footer`  | content                              | Repeated footer content        |
| `fill`    | `luma(95%)`                          | Page background color          |

---

## Grid Layout

`grid` is the primary tool for multi-column / multi-row layouts.

```typst
// Two-column layout: 1/3 + 2/3
#grid(
  columns: (1fr, 2fr),
  gutter: 12pt,
  [Left column content.],
  [Right column content with more text.],
)
```

```typst
// Three equal columns with row gap
#grid(
  columns: (1fr, 1fr, 1fr),
  column-gutter: 10pt,
  row-gutter: 16pt,
  [Cell 1], [Cell 2], [Cell 3],
  [Cell 4], [Cell 5], [Cell 6],
)
```

```typst
// Fixed + flexible columns
#grid(
  columns: (120pt, 1fr),
  gutter: 8pt,
  image("photo.png", width: 100%), [Description text next to the image.],
)
```

### Key `grid` Parameters

| Parameter       | Type / Example           | Description                  |
|----------------|--------------------------|------------------------------|
| `columns`      | `(1fr, 2fr)`, `3`       | Column track sizes or count  |
| `rows`         | `(auto, 1fr)`           | Row track sizes              |
| `gutter`       | `12pt`                  | Uniform gap                  |
| `column-gutter`| `10pt`                  | Horizontal gap only          |
| `row-gutter`   | `16pt`                  | Vertical gap only            |
| `align`        | `center + horizon`      | Cell alignment               |
| `inset`        | `8pt`                   | Cell inner padding           |

---

## Stack

`stack` arranges children along a single axis without wrapping.

```typst
// Horizontal stack (left to right)
#stack(dir: ltr, spacing: 12pt,
  rect(width: 40pt, height: 40pt, fill: red),
  rect(width: 40pt, height: 40pt, fill: blue),
  rect(width: 40pt, height: 40pt, fill: green),
)
```

```typst
// Vertical stack (default direction)
#stack(spacing: 8pt,
  [First item],
  [Second item],
  [Third item],
)
```

---

## Columns

`columns` splits content into flowing newspaper-style columns.

```typst
#columns(2, gutter: 12pt)[
  This text flows from the first column into the second column
  automatically. Useful for article-style layouts where content
  should reflow naturally.

  #colbreak() // Force column break

  This starts in the next column.
]
```

---

## Align and Place

### `align` — Position within parent

```typst
// Center content horizontally and vertically
#align(center + horizon)[Centered content]

// Right-align a block
#align(right)[
  — Author Name
]
```

### `place` — Absolute / floating placement

```typst
// Watermark in page center
#place(center + horizon, float: false,
  text(size: 60pt, fill: luma(90%))[DRAFT]
)

// Float a figure to the top of the page
#place(top + end, float: true, scope: "parent",
  rect(width: 150pt, height: 100pt, fill: luma(90%))[Sidebar],
)
```

### `block` and `box`

```typst
// block — block-level container (can break across pages)
#block(width: 100%, inset: 12pt, fill: luma(95%), radius: 4pt)[
  A highlighted block paragraph.
]

// box — inline container (never breaks)
This is #box(fill: yellow, inset: 2pt)[highlighted] inline text.
```

---

## Common Layout Patterns

```typst
// Title page with vertical centering
#page(margin: 2cm)[
  #align(center + horizon)[
    #text(size: 28pt, weight: "bold")[Document Title]
    #v(1em)
    #text(size: 14pt)[Author Name]
    #v(0.5em)
    #text(size: 12pt, fill: gray)[April 2026]
  ]
]
```

```typst
// Sidebar layout
#grid(
  columns: (180pt, 1fr),
  gutter: 16pt,
  // Sidebar
  block(fill: luma(95%), inset: 12pt, radius: 4pt)[
    *Navigation*
    - Section 1
    - Section 2
  ],
  // Main content
  [Main content area.],
)
```

---

## Guidance

- Prefer stable page and region rules over manual spacing hacks.
- Put major page setup decisions in templates or near the document start.
- Use `place` intentionally; it is powerful but can hide structural problems when overused.
- Re-check layout-heavy patterns when targeting HTML because paged assumptions do not automatically carry over.

## Also See

- `../02-language/styling-layout-and-show-rules.md`
- `export-and-platform.md`

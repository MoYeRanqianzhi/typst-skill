# Visualize

## Use

- Handle color, stroke, gradients, tilings, geometric shapes, images, and decorative graphics.

## Authoritative Sources

- `typst/docs/reference/library/visualize.md`
- `typst/crates/typst-library/src/visualize/**`
- `typst/docs/changelog/0.14.0.md`
- `typst/docs/guides/accessibility.md`

---

## Rectangles and Squares

### `rect` Parameter Quick Reference

| Parameter | Type / Example              | Description                     |
|----------|-----------------------------|---------------------------------|
| `width`  | `100pt`, `100%`, `auto`     | Box width                       |
| `height` | `60pt`, `auto`              | Box height                      |
| `fill`   | `blue`, `luma(90%)`         | Background color                |
| `stroke` | `1pt + black`, `none`       | Border stroke                   |
| `radius` | `4pt`, `(top: 8pt)`         | Corner radius                   |
| `inset`  | `12pt`, `(x: 16pt, y: 8pt)`| Inner padding                   |

```typst
// Basic styled rectangle
#rect(
  width: 200pt,
  height: 80pt,
  fill: rgb("#f0f4ff"),
  stroke: 1pt + rgb("#4a7ce8"),
  radius: 6pt,
  inset: 12pt,
)[Content inside the rectangle]
```

```typst
// Square shorthand
#square(size: 60pt, fill: eastern, radius: 4pt)
```

---

## Circle and Ellipse

```typst
// Circle with content
#circle(radius: 30pt, fill: rgb("#e8f5e9"), stroke: 1pt + green)[
  #align(center + horizon)[✓]
]

// Circle without explicit radius — sizes to fit content
#circle(fill: luma(90%), inset: 8pt)[Hello]
```

```typst
// Ellipse
#ellipse(width: 120pt, height: 60pt, fill: rgb("#fff3e0"), stroke: orange)
```

---

## Line

```typst
// Simple horizontal line
#line(length: 100%)

// Diagonal line with custom stroke
#line(
  start: (0pt, 0pt),
  end: (100pt, 50pt),
  stroke: 2pt + red,
)

// Dashed line
#line(length: 100%, stroke: (paint: gray, dash: "dashed"))
```

---

## Polygon

```typst
// Triangle
#polygon(
  fill: rgb("#e3f2fd"),
  stroke: 1pt + blue,
  (0pt, 60pt),
  (40pt, 0pt),
  (80pt, 60pt),
)
```

```typst
// Pentagon
#polygon(
  fill: rgb("#f3e5f5"),
  stroke: 1pt + purple,
  (40pt, 0pt),
  (80pt, 30pt),
  (65pt, 70pt),
  (15pt, 70pt),
  (0pt, 30pt),
)
```

---

## Gradients

```typst
// Linear gradient background
#rect(
  width: 100%,
  height: 60pt,
  fill: gradient.linear(rgb("#667eea"), rgb("#764ba2"), angle: 135deg),
  radius: 4pt,
)
```

```typst
// Radial gradient
#circle(
  radius: 40pt,
  fill: gradient.radial(white, rgb("#1a237e"), focal-center: (30%, 30%)),
)
```

```typst
// Conic gradient
#square(
  size: 80pt,
  fill: gradient.conic(red, yellow, green, blue, red),
)
```

---

## Images

```typst
// Basic image with width constraint
#image("logo.png", width: 80%)

// Image with alt text (for accessibility)
#image("chart.png", width: 100%, alt: "Sales chart for Q1 2026")

// Fit modes
#image("photo.jpg", width: 200pt, height: 150pt, fit: "cover")
#image("diagram.svg", width: 100%, fit: "contain")
```

### `image` Key Parameters

| Parameter | Type / Example             | Description                          |
|----------|----------------------------|--------------------------------------|
| `width`  | `80%`, `200pt`             | Display width                        |
| `height` | `150pt`, `auto`            | Display height                       |
| `fit`    | `"cover"`, `"contain"`     | How to fit image in the bounding box |
| `alt`    | `"description"`            | Alt text for accessibility           |

```typst
// Decode inline SVG or base64 image
#image.decode(
  read("icon.svg"),
  format: "svg",
  width: 24pt,
)
```

---

## Color and Stroke

```typst
// Named colors and custom colors
#text(fill: red)[Red text]
#text(fill: rgb("#2196F3"))[Blue text]
#text(fill: rgb(33, 150, 243))[Also blue]
#text(fill: luma(60%))[Gray text]
```

```typst
// Stroke styles
#line(length: 100%, stroke: 2pt + black)
#line(length: 100%, stroke: (paint: blue, thickness: 1pt, dash: "dotted"))
#line(length: 100%, stroke: (paint: red, thickness: 3pt, cap: "round"))
```

---

## Common Composition Patterns

### Card Component

```typst
// Card = rect + inset + radius + fill + shadow-like border
#let card(body) = rect(
  width: 100%,
  fill: white,
  stroke: 0.5pt + luma(85%),
  radius: 8pt,
  inset: 16pt,
  body,
)

#card[
  *Card Title*
  #v(4pt)
  #text(fill: gray)[This is a card component built from a styled rect.]
]
```

### Badge / Tag

```typst
#let badge(label, color: blue) = box(
  fill: color.lighten(80%),
  stroke: 0.5pt + color,
  radius: 3pt,
  inset: (x: 6pt, y: 2pt),
  text(size: 9pt, fill: color.darken(20%))[#label],
)

#badge[Typst] #badge(color: green)[New] #badge(color: orange)[WIP]
```

### Decorative Divider

```typst
#let divider = {
  v(8pt)
  line(length: 100%, stroke: 0.5pt + luma(80%))
  v(8pt)
}

Section one content.
#divider
Section two content.
```

### Image with Caption (Semantic)

```typst
#figure(
  image("screenshot.png", width: 80%),
  caption: [Application screenshot showing the main dashboard.],
)
```

---

## High-Value `0.14.x` Notes

- `0.14.0` added support for using PDFs as images.
- `0.14.0` added WebP support.
- Decorative graphics should often be artifacts in PDF or paired with textual support when they carry meaning.

## Design Rules

- Keep meaningful graphics semantic when possible, for example by wrapping them in `figure` and providing captions or alt text.
- Treat purely decorative layers as artifacts in accessibility-sensitive PDF work.
- Prefer stable geometry and styling primitives over backend-specific image hacks.
- External drawing packages may be useful, but they are not part of the core library contract.

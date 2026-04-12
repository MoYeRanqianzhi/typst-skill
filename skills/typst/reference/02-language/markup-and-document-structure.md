# Markup and Document Structure

## Use

- Answer questions about markup mode, block structure, labels and references, imports, and semantic document organization.

## Authoritative Sources

- `typst/docs/reference/language/syntax.md`
- `typst/docs/tutorial/1-writing.md`
- `typst/docs/tutorial/2-formatting.md`
- `The Raindrop-Blue Book/src/tutorial/writing-markup.typ`

## Core Concepts

Typst fuses markup, content, and code into one language via three modes:

```typst
// Markup mode (default at top level) — write prose directly
This is *bold* and _italic_ text.

// Code mode — entered with #, { }, or function bodies
#let x = 1 + 2

// Content mode — entered with [ ] inside code
#let greeting = [Hello, _world_!]
```

### Headings

```typst
= Level 1 Heading
== Level 2 Heading
=== Level 3 Heading

// Headings generate outline entries automatically
#outline()
```

### Lists

```typst
// Unordered list
- Item A
- Item B
  - Nested item

// Ordered list
+ First
+ Second
+ Third

// Term list (definition list)
/ Term: Description of the term
/ Typst: A modern typesetting system
```

### Emphasis and Inline Markup

```typst
*strong emphasis* and _emphasis_
`inline raw code`
"smart quotes" and 'single quotes'
A line break: \
A non-breaking space: ~
An em dash: ---
An en dash: --
An ellipsis: ...
```

### Labels and References

```typst
= Introduction <intro>

See @intro for details.          // reference a heading
See @fig-chart for the figure.   // reference a figure

#figure(
  image("chart.png", width: 80%),
  caption: [Monthly revenue],
) <fig-chart>

// Supplement text can be customized
@fig-chart shows the trend.
```

### Figures and Tables

```typst
#figure(
  table(
    columns: (auto, 1fr, 1fr),
    [*Name*], [*Score*], [*Grade*],
    [Alice],  [92],      [A],
    [Bob],    [78],      [B],
  ),
  caption: [Student grades],
) <tbl-grades>

// Image figure
#figure(
  image("photo.png", width: 60%),
  caption: [A sample photo],
)
```

### Import vs Include

```typst
// import — bring code definitions (functions, variables) into scope
#import "utils.typ": my-func, my-var
#import "@preview/cetz:0.3.4": canvas, draw

// include — insert another document's rendered content inline
#include "chapter1.typ"
```

Key difference: `import` gives access to names; `include` splices content.

## Common Mistakes

```typst
// ❌ # expression extends too far — the comma becomes part of the call
#text(fill: red)[Hello], world   // "world" is NOT red, but ", world" may cause errors

// ✅ Terminate the expression explicitly
#text(fill: red)[Hello], world

// ❌ Faking structure with raw spacing
#h(2em) My pseudo-heading

// ✅ Use semantic headings
== My Real Heading

// ❌ Mixing up import and include
#import "chapter1.typ"   // imports names, doesn't render content
#include "utils.typ"     // renders content, can't access definitions

// ✅ Correct usage
#include "chapter1.typ"  // render the chapter
#import "utils.typ": helper  // import specific function

// ❌ Using a label without the < > syntax
= Introduction intro     // "intro" is body text, not a label

// ✅ Labels use angle brackets
= Introduction <intro>
```

## Structural Hotspots

- heading hierarchy and outline generation
- labels, `ref`, and `link` targets
- list and term semantics
- figure and table wrappers instead of ad hoc captions
- document-level metadata such as `title`

## Exact Lookup

- For exact element or function questions, run `python skills/typst/scripts/query_reference.py --query <keyword>`.

# Styling, Layout, and Show Rules

## Use

- Handle `set` rules, `show` rules, selectors, style propagation, page setup, and layout-aware styling.

## Authoritative Sources

- `typst/docs/reference/language/styling.md`
- `typst/docs/guides/page-setup.md`
- `typst/docs/reference/library/layout.md`
- `The Raindrop-Blue Book/src/tutorial/scripting-style.typ`
- `The Raindrop-Blue Book/src/tutorial/scripting-layout.typ`

## Core Concepts

`set` configures defaults; `show` transforms or replaces presentation behavior. Both cascade and can be scoped.

### Set Rules — Configure Defaults

```typst
// Set text font and size globally
#set text(font: "New Computer Modern", size: 11pt)
#set text(lang: "zh", region: "cn")  // for Chinese documents

// Page configuration — put near the top or in a template
#set page(
  paper: "a4",
  margin: (top: 2.5cm, bottom: 2.5cm, left: 2cm, right: 2cm),
  numbering: "1",
  header: align(right)[My Document],
)

// Paragraph and list defaults
#set par(justify: true, leading: 0.8em)
#set heading(numbering: "1.1")
#set list(marker: ([--], [•]))
```

### Show Rules — Transform Presentation

```typst
// Full show rule with access to the element
#show heading: it => {
  set text(font: "Noto Sans", fill: navy)
  block(below: 0.8em)[
    #if it.level == 1 {
      text(size: 18pt, weight: "bold", it.body)
    } else {
      text(size: 14pt, it.body)
    }
  ]
}

// Shorthand show-set rule — no function needed
#show link: set text(fill: blue)
#show raw: set text(font: "Fira Code", size: 9pt)

// Show rule that wraps content
#show heading.where(level: 1): it => {
  pagebreak(weak: true)
  it
}
```

### Selectors

```typst
// Element selector — matches all instances of a type
#show heading: set text(fill: eastern)

// Where filter — narrow by field values
#show heading.where(level: 2): set text(style: "italic")

// Label selector — matches elements with a specific label
#show <important>: set text(fill: red, weight: "bold")

// Combined in practice
#show figure.where(kind: table): set figure(supplement: [Table])
```

### Scoping and Cascade

```typst
// Set/show rules apply to everything AFTER them in the same scope
#set text(fill: black)

This is black.

#[
  // Inner scope — overrides parent
  #set text(fill: red)
  This is red.
]

This is black again.  // parent scope restored

// Order matters — later rules override earlier ones
#set text(size: 12pt)
#set text(size: 10pt)  // this wins
```

### Page Configuration Notes

```typst
// ⚠ Changing set page() mid-document forces a page break
#set page(paper: "a4")

// ... content ...

#set page(paper: "us-letter")  // triggers a new page here

// Use page() function call for one-off pages (e.g., landscape)
#page(flipped: true)[
  #table(columns: 6, ..data)
]
```

## Common Mistakes

```typst
// ❌ Forgetting that show rules need a function or set rule
#show heading: text(fill: red)  // error — bare function call

// ✅ Use set shorthand or a closure
#show heading: set text(fill: red)
#show heading: it => text(fill: red, it.body)

// ❌ Applying set page() in a nested scope — has no effect
#block[
  #set page(margin: 1cm)  // ⚠ ignored — page is top-level only
]

// ✅ Set page at the top level or in a template
#set page(margin: 1cm)

// ❌ Overly broad show rule causes unexpected global changes
#show: columns.with(2)  // everything after this is two-column

// ✅ Scope the columns to a specific section
#columns(2)[
  Only this block is two-column.
]

// ❌ show rule returning nothing — content disappears
#show heading: it => {
  // forgot to use `it`
}

// ✅ Always include the element or replacement content
#show heading: it => {
  underline(it.body)
}
```

## High-Value Topics

- `set page(...)` and page-level margins, numbering, and headers
- `show heading`, `show link`, and other semantic element selectors
- `block`, `box`, `align`, `place`, `stack`, `grid`, `columns`
- backend-aware styling with `target()`

## Also See

- `../03-library/layout.md`
- `../05-recipes/plugins-html-pdf-svg-png.md`

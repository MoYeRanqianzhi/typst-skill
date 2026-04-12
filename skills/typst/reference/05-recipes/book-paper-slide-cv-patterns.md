# Book, Paper, Slide, and CV Patterns

## Use

- Provide reusable high-level document patterns grounded in the local blue-book templates and official template workflow.

## Authoritative Sources

- `typst/docs/tutorial/4-template.md`
- `The Raindrop-Blue Book/src/template/book.typ`
- `The Raindrop-Blue Book/src/template/paper.typ`
- `The Raindrop-Blue Book/src/template/slides.typ`
- `The Raindrop-Blue Book/src/topics/template-book.typ`
- `The Raindrop-Blue Book/src/topics/template-paper.typ`
- `The Raindrop-Blue Book/src/topics/template-cv.typ`

## Design Rules

- Put document-wide defaults in a template function instead of scattering `set` and `show` rules through the body.
- Keep content parameters semantic: `title`, `authors`, `date`, `abstract`, `lang`, `theme`, and so on.
- Avoid hard-coding one user's local fonts or package paths into a template.
- If a design must work for both PDF and HTML, isolate backend-specific behavior early.

---

## Minimal Paper Template

A reusable template function that accepts metadata and yields a formatted paper.

```typst
#let paper(
  title: "Untitled",
  authors: (),
  abstract: none,
  date: datetime.today().display("[year]-[month]-[day]"),
  body,
) = {
  set document(title: title, author: authors)
  set page(paper: "a4", margin: (x: 2.5cm, y: 2.8cm))
  set text(size: 11pt, lang: "en")
  set par(justify: true, first-line-indent: 1.5em)
  set heading(numbering: "1.1")

  // --- Title block ---
  align(center)[
    #text(size: 16pt, weight: "bold", title)
    #v(0.6em)
    #text(size: 11pt, authors.join(", ", last: " and "))
    #v(0.4em)
    #text(size: 10pt, fill: gray, date)
  ]

  // --- Abstract ---
  if abstract != none {
    v(1em)
    block(width: 90%, inset: (x: 1em))[
      #text(weight: "bold", "Abstract. ")
      #abstract
    ]
  }

  v(1.5em)
  body
}

// --- Usage ---
#show: paper.with(
  title: "My Research Paper",
  authors: ("Alice", "Bob"),
  abstract: [This paper explores ...],
)

= Introduction
Content goes here.
```

## Minimal CV Template

A compact CV with reusable `section` and `entry` helper functions.

```typst
#let cv-section(title) = {
  v(0.8em)
  text(size: 12pt, weight: "bold", fill: eastern, title)
  v(-0.4em)
  line(length: 100%, stroke: 0.5pt + eastern)
  v(0.3em)
}

#let cv-entry(
  what: "",
  when: "",
  where: "",
  details: none,
) = {
  grid(
    columns: (1fr, auto),
    align: (left, right),
    text(weight: "bold", what),
    text(style: "italic", when),
  )
  if where != "" {
    text(size: 9pt, fill: gray, where)
  }
  if details != none {
    v(0.2em)
    details
  }
  v(0.4em)
}

// --- Usage ---
#set page(paper: "a4", margin: (x: 2cm, y: 2cm))
#set text(size: 10pt, lang: "en")

#align(center, text(size: 18pt, weight: "bold", "Jane Doe"))
#align(center, text(size: 9pt, "jane@example.com | github.com/jane"))

#cv-section("Experience")
#cv-entry(
  what: "Software Engineer",
  when: "2023 – Present",
  where: "Acme Corp",
  details: list(
    [Built distributed data pipeline],
    [Reduced latency by 40%],
  ),
)

#cv-section("Education")
#cv-entry(
  what: "M.Sc. Computer Science",
  when: "2021 – 2023",
  where: "University of Typst",
)
```

## Minimal Slide / Presentation Setup

Typst doesn't have a built-in slide package, but page-based slides work well. Each `pagebreak()` creates a new slide.

```typst
#set page(
  width: 25.4cm,    // 10 in — widescreen 16:9
  height: 14.29cm,  // 5.625 in
  margin: (x: 2cm, y: 1.5cm),
  fill: white,
)
#set text(size: 20pt, lang: "en")

// --- Slide 1: Title ---
#align(center + horizon)[
  #text(size: 36pt, weight: "bold", "Talk Title") \
  #text(size: 18pt, fill: gray, "Author — Conference 2026")
]

#pagebreak()

// --- Slide 2: Content ---
== Key Points

- First point
- Second point
- Third point

#pagebreak()

// --- Slide 3: Thanks ---
#align(center + horizon, text(size: 28pt, "Thank you!"))
```

## Pattern Matrix

| Pattern | Key Elements |
|---------|-------------|
| **Book** | Stable page setup, chapter headings, `outline()`, running headers via `context`, bibliography |
| **Paper** | Title metadata, author block, abstract, figures/tables, `bibliography()`, compact template function |
| **Slides** | Explicit 16:9 page size, `pagebreak()` per slide, large text, `align(center + horizon)` |
| **CV** | Reusable section/entry functions, grid layout for dates, compact spacing, font control |

## Validation Checklist

1. Render a minimal sample document for the pattern.
2. Verify headings, references, figures, and bibliography still behave under the template.
3. Re-test fonts and page setup on the target machine.
4. For slide or HTML-adjacent workflows, verify backend-specific assumptions explicitly.

# Authoring documents and reusable components

Baseline: **Typst 0.15.1**, [stable source at 9dfd3a08](https://github.com/typst/typst/tree/9dfd3a08500b7896045f907433cf7b4b02434fad).
Use the [0.15.0 changes](https://typst.app/docs/changelog/0.15.0/) and [0.15.1 fixes](https://typst.app/docs/changelog/0.15.1/) when checking version-sensitive behavior; online reference pages can move beyond this baseline.
Examples need no packages. Each example is independent except the explicitly paired module files.

## Keep markup, code, and math separate

- Use `[...]` for content, `{...}` for computation, and `$...$` for mathematical notation. A string is not parsed as markup when inserted into content.
- Enter code with `#` from markup or math. Inside a code block, do not add another `#` until re-entering markup or math.
- A code block **joins the output of its expressions**; it does not simply return the last expression. Bind intermediate results with `let` so a diagnostic value does not accidentally become document content.
- Pass content to components rather than building source strings. Use numeric code for calculations: math notation such as `$2 + 3$` typesets a formula, whereas `#(2 + 3)` evaluates it.

```typst
#let count = 3
#let note(body, copies: 1) = {
  let doubled = copies * 2
  block(inset: 6pt)[
    #body \
    Computed: #doubled; formula: $2 x$.
  ]
}

#note(copies: count)[*Measurement*]
```

Sources: [syntax and escapes](https://typst.app/docs/reference/syntax/), [blocks and scripting](https://typst.app/docs/reference/scripting/#blocks). For formulas and safe data insertion, see [math-data.md](math-data.md).

## Export functions, not ambient configuration

Choose `import` to access definitions; choose `include` to insert a file's evaluated content. Neither makes the imported/included file see the caller's local variables. A module's top-level styling is not a configuration export: expose a function that applies rules to its `body`.

Prefer named imports or a module namespace over `import ...: *` when names could collide. Keep dependencies explicit through parameters or imports in the module that needs them. In particular, including a chapter is not textual macro expansion; the chapter must import its own helpers.

For whole-document styling, a body-taking function plus `#show: report.with(...)` avoids wrapping the manuscript manually.

**`components.typ`**

```typst
#let report(body, title: "Report") = {
  set document(title: title)
  set text(lang: "en")
  set heading(numbering: "1.")
  heading(numbering: none, outlined: false)[#title]
  body
}

#let callout(body) = block(
  inset: 8pt,
  fill: luma(245),
  [*Note:* #body],
)
```

**`main.typ`**, beside `components.typ`:

```typst
#import "components.typ": report, callout
#show: report.with(title: "Field notes")

= Method
#callout[Keep the raw observations with the report.]
```

Path strings resolve relative to the file containing the load/import call, not necessarily the entrypoint. Pass `path("data.csv")` from the caller when a helper in another module must load a caller-relative file. A leading `/` refers to the Typst project root, not the operating system root.

Sources: [modules](https://typst.app/docs/reference/scripting/#modules), [functions](https://typst.app/docs/reference/foundations/function/), [paths](https://typst.app/docs/reference/foundations/path/).

## Prefer set rules before transformations

1. Use `set` for an element's configurable parameters, such as heading numbering.
2. Use a **show-set** rule for styling selected elements, such as text color only within level-one headings.
3. Use a transformational `show` only when the rendered structure must change.

Rules apply to subsequent content through the end of their enclosing block/file. Narrow a selector or use a content block to limit a rule's reach.

```typst
#set heading(numbering: "1.")
#show heading.where(level: 1): set text(fill: navy)
#show heading.where(level: 1): element => block(
  inset: (bottom: 4pt),
  stroke: (bottom: 0.5pt + gray),
  element,
)

= Results <sec:results>
The heading remains numbered and referenceable: @sec:results.
```

Transformation traps:

- **Wrap the supplied element when keeping its default rendering.** Returning the original element is supported without reapplying the same rule to it. Constructing a fresh matching element inside the transformation can recurse indefinitely.
- **Using only `element.body` replaces the default rendering.** For a heading, that also omits its visible default number unless you render it yourself. The original element can remain discoverable through introspection and retain PDF semantics, while HTML may lose its heading tag; inspect the requested export's structure.
- **Keep overridable styling in show-set rules.** A `set` buried inside a transformation cannot be overridden by later outer show-set rules in the same way.
- **Do not treat arbitrary functions as element constructors.** A helper like `callout` above is configured by parameters or `.with(...)`, not by inventing `set callout(...)`.
- A show rule supplies style context, but location context is only implicit for locatable elements. Do not assume a text/regex transformation has a document location.
- When customizing `ref`, guard its `element` field against `none` before inspecting the destination: references can be unresolved during early layout iterations.

Sources: [styling](https://typst.app/docs/reference/styling/), [context](https://typst.app/docs/reference/context/), [reference customization](https://typst.app/docs/reference/model/ref/#customization).

## Choose ordinary values, counters, or state

| Need | Use |
| --- | --- |
| Compute from known input data | Ordinary variables, arrays, functions; no context needed |
| Number headings, figures, equations | Their built-in numbering and counters |
| Count custom items in layout order | `counter("distinct-key")` |
| Accumulate another value in layout order | `state("distinct-key", initial)` |
| Read styles, counters, state, or document positions | `context` at the intended insertion point |

`context` produces opaque **content**, not an immediately available number or array. Keep arithmetic, branching, and formatting that depend on a contextual value inside that context. A reused context resolves separately at each insertion point.

```typst
#let item-counter = counter("review/items")
#let points-total = state("review/points", 0)
#let scored-item(body, points) = block[
  #item-counter.step()
  #points-total.update(previous => previous + points)
  *Item #context item-counter.display("1"):* #body (#points points)
]

Final points: #context points-total.final()

#scored-item([Method explained], 3)
#scored-item([Results reproduced], 4)

#context [
  Items here: #item-counter.get().first().
  Points here: #points-total.get().
]
```

Updates return content: they take effect only where that content is inserted. Merely assigning `points-total.update(...)` to a variable does not apply it. Step a custom counter before displaying it; counter reads return arrays because counters can have multiple levels. Distinct components should not accidentally reuse a state/counter key.

Prefer `update(previous => ...)` to reading then updating inside a context. Avoid updates derived from the same state's `final()`, or layout decisions that repeatedly change their own inputs. If inserting an update inside an existing context, a later read in that same context still observes its original location; place a new inner context after the update to observe the new position.

Sources: [context and compiler iterations](https://typst.app/docs/reference/context/#compiler-iterations), [counters](https://typst.app/docs/reference/introspection/counter/), [state and convergence](https://typst.app/docs/reference/introspection/state/#caution).

## Query structure without changing what you query

Use `outline()` for a normal contents list. Reach for `query` when a different selection or derived summary is actually required. Queries inspect the laid-out document, including elements later in the source, rather than parsing source text.

This custom list uses the 0.15 `counter.display(at: ...)` parameter to format page numbers at each heading's location:

```typst
#set page(numbering: "1")
#set heading(numbering: "1.")

#context {
  for section in query(heading.where(level: 1, outlined: true)) {
    link(section.location(), section.body)
    h(1fr)
    counter(page).display(at: section.location())
    linebreak()
  }
}

= Method
Describe the procedure.

= Results
Report the observations.
```

Do not generate new matching headings from a query over those same headings. Render links/text, or exclude the generated elements from the selector. A convergence warning means the layout-dependent result is not settled, even if a PDF was produced; diagnose the feedback loop instead of treating the output as reliable.

Sources: [query](https://typst.app/docs/reference/introspection/query/), [outline](https://typst.app/docs/reference/model/outline/).

## Preserve semantic structure

Use real headings with logical levels, lists for lists, and tables for related data; use layout containers for visual arrangement. Style those elements instead of replacing the document model with large bold text or manually typed numbering. Introspection and PDF tagging can preserve original semantic roles through custom show rules, but HTML tags follow the emitted markup: replacing a heading or strong element with only its body can remove the corresponding HTML tag. Check usable text, structure, and reading order in the actual target.

Set document metadata with `document` and language with `text(lang: ...)`. Attach unique labels to meaningful elements and let references/captions follow their counters; see [math-data.md](math-data.md). When accessibility matters, verify the exported structure as well as appearance; compilation alone is not an accessibility audit.

Sources: [maintaining semantics](https://typst.app/docs/guides/accessibility/#maintaining-semantics), [heading levels](https://typst.app/docs/reference/model/heading/#accessibility), [document metadata](https://typst.app/docs/reference/model/document/).

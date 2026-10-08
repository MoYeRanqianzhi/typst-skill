# Export targets and semantics

Scope: Typst **0.15.1**, tag `v0.15.1`, commit `9dfd3a0`. Check another compiler's help before transferring version-sensitive flags. The [release-pinned CLI source](https://github.com/typst/typst/blob/v0.15.1/crates/typst-cli/src/args.rs) defines the options below.

## Choose the requested target

| Need | Choose | Important boundary |
| --- | --- | --- |
| Fixed pages, selectable text, document exchange | PDF | Tagged by default; tags alone do not establish accessibility. |
| Raster images | PNG | Resolution-dependent; no semantic text or reading order. |
| Scalable page graphics | SVG | Text becomes glyph outlines, not selectable/accessible text. |
| Semantic web content | HTML | Experimental, incomplete, feature-gated; not production-ready in 0.15.1. Not a faithful paged-layout conversion. |
| Several documents/assets from one source | Bundle | Experimental directory output, not an archive; documents can mix formats. |

For an existing `main.typ`, run only the needed export:

```sh
typst compile main.typ main.pdf
typst compile --ppi 300 main.typ "page-{0p}.png"
typst compile main.typ "page-{0p}.svg"
typst compile --features html main.typ main.html
```

PDF is the default; otherwise the output extension selects the format, or use `--format pdf|png|svg|html`. Multi-page PNG/SVG needs a page-number output pattern: `{p}` or zero-padded `{0p}`; `{t}` adds the total page count. `--ppi` affects only PNG and defaults to 144. `--pages 2,4-6` selects physical, one-based pages, not displayed page-counter numbers. For transparent PNG/SVG, use `#set page(fill: none)`; their default background is white. See [PNG](https://typst.app/docs/reference/png/) and [SVG](https://typst.app/docs/reference/svg/).

## Preserve meaning, not just appearance

Use actual `heading`, list, table, figure, and link elements rather than visually similar text/shapes. Set the document title and the actual text language. This small `main.typ` works for paged output and experimental HTML:

```typst
#set document(title: [Triangle relation])
#set text(lang: "en")

= Relation
#math.equation(
  block: true,
  alt: "a squared plus b squared equals c squared",
  $ a^2 + b^2 = c^2 $,
)
```

- Describe an informative image with `image("chart.svg", alt: "...")`; its caption is not a substitute. Use `figure(alt: ...)` for a composition that should be one semantic unit, not automatically in addition to image alt. Write a meaningful description for the actual image.
- Keep text as text. Rasterizing a page, outlining it in SVG, or importing a PDF as an image does not retain the original document's text structure.
- For PDF, mark genuinely decorative content with `pdf.artifact[...]`. It removes that content from the accessible structure; do not use it to silence errors about meaningful content. It is not a cross-format HTML hiding API.
- **HTML math is native MathML in 0.15.1**, with no separate math feature flag or MathJax requirement. Remove legacy blanket `show math.equation: html.frame` rules when semantic math is wanted. `math.equation(alt: ...)` supplies the natural-language description needed for PDF/UA-1; HTML's native equation rule emits MathML rather than turning that alt into an HTML label. Test the target browser/assistive technology, not just the source alt string.

Sources: [image alt](https://typst.app/docs/reference/visualize/image/#parameters-alt), [accessibility guide](https://typst.app/docs/guides/accessibility/), [0.15 MathML change](https://typst.app/docs/changelog/0.15.0/#html-export), and [release-pinned HTML rules](https://github.com/typst/typst/blob/v0.15.1/crates/typst-html/src/rules.rs).

## PDF standards: request the profile, keep its limits

```sh
typst compile --pdf-standard ua-1 main.typ accessible.pdf
typst compile --pdf-standard a-2a,ua-1 main.typ archived-accessible.pdf
```

- Default output is PDF 1.7. Accepted base versions are `1.4`, `1.5`, `1.6`, `1.7`, and `2.0`; PDF/A profiles are `a-1b`, `a-1a`, `a-2b`, `a-2u`, `a-2a`, `a-3b`, `a-3u`, `a-3a`, `a-4`, `a-4f`, and `a-4e`. Choose the recipient's requirement, not a supposedly universal best profile.
- Only **PDF/UA-1** is supported, not PDF/UA-2. UA-1 is incompatible with PDF 2.0 and PDF/A-4. Compatible standards can be comma-combined, as above.
- PDF/A is for archiving, not automatically accessibility: `b`/`u` profiles are not equivalent to UA-1. PDF/A-1 forbids transparency; arbitrary attachments require PDF/A-3 or PDF/A-4f/4e. Profile checks can reject otherwise valid documents.
- Keep tagging for accessibility. In this CLI, **`--pages` implies `--no-pdf-tags`**, even for a range covering every page. Either option conflicts with UA-1 and PDF/A `a-1a`, `a-2a`, `a-3a`; build the intended document rather than silently stripping tags to extract pages.
- UA-1 adds checks such as a document title and descriptions for informative images/equations. Compilation cannot establish that descriptions are useful, language is correct, contrast is sufficient, or reading order makes sense. Experimental table helpers behind `--features a11y-extras` are separate from ordinary tagged export; enable only when their specific API is needed.

See [PDF standards](https://typst.app/docs/reference/pdf/#pdf-standards) and the [release-pinned tagging/selection checks](https://github.com/typst/typst/blob/v0.15.1/crates/typst-cli/src/compile.rs).

## Experimental HTML and bundles

Both targets are CLI-only experiments in this release; neither is available in the web app. HTML emits a standalone document, not an embeddable fragment. Do not expect page geometry or all set rules to become equivalent CSS. Put target-specific markup in templates/show rules: contextual `target()` returns `"html"`, `"bundle"`, or `"paged"` (PDF/PNG/SVG and inside `html.frame`), never `"pdf"`. `html.frame` is a deliberate inline-SVG escape hatch for a graphic, not the default treatment of text or math; provide an accessible text equivalent if needed.

For an actual multi-file request, `site.typ` can contain:

```typst
#document("index.html", title: [Home])[
  = Home
  #link(<print>)[Printable notes]
]
#document("notes.pdf", title: [Notes])[Hello.] <print>
#asset("data.txt", "One bundle, several files.")
```

```sh
typst compile --features bundle,html --format bundle site.typ site-output
```

The output is a directory. `document` compiles content into the format inferred from its output path; `asset` writes a string/bytes unchanged. For binary assets use `asset("logo.png", read("logo.png", encoding: none))`. Non-HTML bundles need only `--features bundle`. Labels, queries, counters, and states span the entire bundle; the page counter is per document. Do not assume independent heading numbering or label namespaces for each file. Bundle export writes named files but does not clean obsolete outputs; inspect a fresh output directory when checking the deliverable.

See [HTML status](https://typst.app/docs/reference/html/), [bundle semantics](https://typst.app/docs/reference/bundle/), and [document](https://typst.app/docs/reference/model/document/).

## Validate the delivered format

Validate only the formats requested; a successful PDF build does not validate HTML.

| Target | Evidence that matters |
| --- | --- |
| PDF | Inspect rendered pages, text extraction, links, and metadata. For an accessibility/archival requirement, inspect tags/reading order and use an appropriate PDF/UA or PDF/A validator such as veraPDF; supplement automatic checks with human/assistive-technology review. |
| PNG | Check actual pixel dimensions against page size and PPI, page count/names, clipping, and alpha/background. Do not claim text accessibility from a good screenshot. |
| SVG | Open in the destination renderer; check page size, clipping, background, and links if needed. Glyph outlines are expected, not proof of missing fonts. |
| HTML | Review warnings and the DOM for headings, language, alt attributes, links, and native `<math>`; render in the target browser and check math, navigation, and any required assistive-technology behavior. |
| Bundle | Check emitted paths, assets, and cross-document links, then validate each requested constituent format. A directory existing is not sufficient evidence. |

State separately what compiled, what was visually/structurally inspected, and which conformance or assistive-technology checks were not run.

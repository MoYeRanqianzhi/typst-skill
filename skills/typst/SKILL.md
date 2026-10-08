---
name: typst
description: >-
  Create, edit, debug, and migrate Typst documents, reusable templates, and packages.
  Use for .typ source, Typst API or symbol questions, mathematical and Chinese
  typesetting, and PDF/HTML export. Includes version-aware official API lookup.
metadata:
  typst-version: "0.15.1"
---

# Typst

Produce working Typst that respects the user's document, compiler, and intended output. The verified stable baseline is **0.15.1**, checked on **2026-10-09**. Treat this as a dated baseline, not a promise that it remains the latest release.

## Start with the document

For an existing project, find the entry file, project root, package versions, and the smallest change that achieves the request. Preserve its design and template conventions. For a new document, use the requested content and visual direction; a small local component is often enough without a published template.

When executing Typst, check `typst --version`. A compiler mismatch is a compatibility decision, not permission to upgrade the user's environment. If there is no compiler, provide source and the exact compile command, and state that compilation was not verified.

## Choose only the guidance needed

| Work | Read when relevant |
| --- | --- |
| Write or refactor `.typ`; set/show; context, state, counters | [Authoring](references/authoring.md) |
| Equations, symbols, data-driven tables, citations | [Math and data](references/math-data.md) |
| Page composition, long content, typography, Chinese text | [Layout and CJK](references/layout-cjk.md) |
| Compilation errors, unexpected output, diagnostics | [Debugging](references/debugging.md) |
| PDF/PNG/SVG, HTML, multi-file bundle, accessibility | [Exports](references/exports.md) |
| Modules, packages, templates, inputs, Wasm | [Packages](references/packages.md) |
| Exact API details, offline use, source investigation | [Documentation and versions](references/docs-and-versions.md) |
| Move an older project to 0.15 | [Migration](references/migration.md) |

Do ordinary edits directly. Consult a reference or look up an API when it resolves a real uncertainty; do not load this entire library for a short snippet.

## Resolve API uncertainty

The bundled catalog locates official functions, types, parameters, symbols, selected constants, and chapters. It is not a replacement for their signatures and behavior. `<skill-dir>` below is the directory containing this file, regardless of the current working directory.

```sh
python "<skill-dir>/scripts/docs.py" search "table.cell"
python "<skill-dir>/scripts/docs.py" show "table.cell"
python "<skill-dir>/scripts/docs.py" show "text:font"
python "<skill-dir>/scripts/docs.py" search "sym.arrow.r"
```

Search is offline. `show` reads a cached or live official section with provenance and checks its advertised documentation version. Names such as `text:font` denote a catalog parameter, **not Typst syntax**. A scoped definition such as `figure.caption` is different from the parameter `figure:caption`.

For new APIs or migration questions, check the user's compiler against the release notes. Official documentation for that version and executable probes outrank remembered signatures or older tutorial recipes. The Chinese blue book is useful for explanations; its older examples do not establish current API behavior. See [version boundaries](references/docs-and-versions.md) when offline or when documentation has moved ahead.

## Verify the result that matters

- For a runnable change, compile the actual entry file with its root, fonts, inputs, and target. Report errors and relevant warnings; do not substitute a mental walkthrough for execution.
- For layout changes, render the affected pages and inspect them, including long-content/page-break cases. Successful compilation alone does not verify typography or prevent clipping.
- For contextual logic, inspect concrete values with `typst eval --in main.typ 'query(heading)'` on 0.15+. A `context` expression produces content, not an ordinary value available outside its context.
- Test the requested export. PDF success says nothing about HTML semantics, and selecting a PDF standard is not independent conformance certification.

Deliver the changed source or requested explanation, the output location where applicable, and a concise account of what actually ran. Mention only compatibility or validation gaps that affect the result.

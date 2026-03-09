# Plugins and Output Backends

## Use

- Handle plugins, WASM-related work, and cross-backend compatibility planning.

## Authoritative Sources

- `The Raindrop-Blue Book/src/topics/writing-plugin-lib.typ`
- `The Raindrop-Blue Book/src/topics/call-externals.typ`
- `The Raindrop-Blue Book/src/tutorial/reference-wasm-plugin.typ`
- `typst/docs/reference/export/pdf.md`
- `typst/docs/reference/export/html.md`
- `typst/docs/reference/export/svg.md`
- `typst/docs/reference/export/png.md`
- `typst/docs/changelog/0.14.1.md`
- `typst/docs/changelog/0.14.2.md`

## Core Guidance

- Prefer `Typst 0.14.2` for plugin-related work.
- `0.14.1` upgraded the WASM runtime for a plugin bug, but `0.14.2` is the security baseline because `0.14.0` and `0.14.1` used a vulnerable runtime.
- Explain backend differences separately for PDF, HTML, SVG, and PNG; do not assume identical behavior.
- If the same design must target multiple backends, reduce paged-only assumptions early.

## Plugin and External-Call Boundaries

- The blue book is the main local source for external-call and plugin recipes in this repository snapshot.
- Treat such recipes as workflow guidance, not as proof that the surrounding Typst API is unchanged in `0.14.2`.
- Re-check current CLI, export, and package behavior against official docs before locking in an integration pattern.

## Backend Checklist

- PDF: accessibility, archival, attachments, and artifact handling.
- HTML: semantics, typed HTML, and backend-aware templates.
- SVG and PNG: page-image outputs and multi-page filename-template constraints.
- Mixed backend output: isolate backend-aware logic rather than branching ad hoc throughout the document.

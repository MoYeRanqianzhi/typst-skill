# Plugins and Output Backends

## Use

- Handle plugins, WASM-related work, and cross-backend compatibility planning.

## Authoritative Sources

- `The Raindrop-Blue Book/src/topics/writing-plugin-lib.typ`
- `The Raindrop-Blue Book/src/topics/call-externals.typ`
- `The Raindrop-Blue Book/src/tutorial/reference-wasm-plugin.typ`
- `typst/docs/reference/export/**`
- `typst/docs/changelog/0.14.2.md`

## Core Guidance

- For plugin-related work, prefer `Typst 0.14.2`.
- Explain backend differences separately for PDF, HTML, SVG, and PNG; do not assume identical behavior.
- If the same design must target multiple backends, reduce paged-only assumptions early.

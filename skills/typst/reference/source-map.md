> Support note: This file supports the generated-index pipeline. Prefer the numbered reference tree for normal task routing.

# Source Map

## Purpose

- Provide a compact map of upstream locations used by the generated indexes.
- Help maintainers jump to the right source tree when a query result needs manual verification.

## Main Upstream Roots

- Official library source: `typst/crates/typst-library/src/`
- Official HTML source: `typst/crates/typst-html/src/`
- Official docs source: `typst/docs/`
- Blue-book source: `The Raindrop-Blue Book/src/`

## Generated Outputs

- Comprehensive index: `skills/typst/reference/generated/typst-reference.json`
- Comprehensive summary: `skills/typst/reference/generated/summary.md`
- Lightweight official inventory: `skills/typst/reference/08-generated/typst-api-index.json`
- Lightweight official summary: `skills/typst/reference/08-generated/typst-api-index.md`

## Cached Inputs Used By The Comprehensive Builder

- Typed HTML metadata from local `typst-assets` Cargo checkout
- Symbol and emoji metadata from local `codex` Cargo registry sources

## Open This File When

- You are maintaining the generated-index scripts.
- You need to verify where a generated field ultimately comes from.
- You need a quick upstream path map without reopening the numbered docs tree.

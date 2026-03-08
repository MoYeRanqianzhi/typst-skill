# Typst Reference Index

## Baseline

- Official baseline: `Typst 0.14.2`
- Primary authority: `typst/docs/reference/**`, `typst/docs/tutorial/**`, `typst/docs/guides/**`, `typst/docs/changelog/**`
- Default cross-source index: `reference/generated/typst-reference.json`
- Fast-path official inventory: `reference/08-generated/typst-api-index.json`
- Chinese practice layer: `The Raindrop-Blue Book/src/**`

## Index Comparison

- `generated/typst-reference.json`
  - default entry point
  - broadest coverage
  - query with `python scripts/query_reference.py --query <keyword>`
  - best for symbols, typed HTML, blue-book examples, and mixed-source lookup
- `08-generated/typst-api-index.json`
  - official-only inventory
  - query with `python scripts/query_api_index.py --name <keyword>`
  - best for quick source anchoring by API/category/kind

## Task Routing

- Compile, export, debug: `01-workflows/compile-debug-publish.md`
- Project structure, templates, packages: `01-workflows/project-templates-and-packages.md`
- Language layer: `02-language/`
- Official library categories: `03-library/`
- Module/group pages: `04-modules/std-calc-sys-sym-emoji.md`
- Chinese recipes: `05-recipes/`
- CLI and source maps: `06-dev/`
- Versioning and blue-book drift: `07-versioning/`
- Support docs: `overview.md`, `source-map.md`, `workflows.md`

## Support Docs

- `overview.md`, `source-map.md`, and `workflows.md` are support/compatibility notes for the comprehensive index pipeline.
- Prefer the numbered tree for normal task routing; open the support docs when you need generated-index context or a quick source overview.

## Refresh

- Run `python scripts/build_reference.py` after updating local upstream snapshots.
- Run `python scripts/refresh_typst_knowledge.py` to refresh the lightweight official inventory.
- Update `07-versioning/` whenever the Typst version changes.

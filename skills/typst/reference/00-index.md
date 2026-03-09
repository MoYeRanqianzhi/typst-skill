# Typst Reference Index

## Baseline

- Official baseline: `Typst 0.14.2`
- Primary authority: `typst/docs/reference/**`, `typst/docs/tutorial/**`, `typst/docs/guides/**`, `typst/docs/changelog/**`, and the corresponding Rust source under `typst/crates/**`
- Default cross-source index: `reference/generated/typst-reference.json`
- Fast official inventory: `reference/08-generated/typst-api-index.json`
- Chinese practice layer: `The Raindrop-Blue Book/src/**`

## Route the Task

- Compile, export, debug: `01-workflows/compile-debug-publish.md`
- Project structure, templates, packages: `01-workflows/project-templates-and-packages.md`
- Language layer: `02-language/`
- Library categories: `03-library/`
- Official group pages and named modules: `04-modules/std-calc-sys-sym-emoji.md`
- Recipes and authoring patterns: `05-recipes/`
- Source-level development and maintenance: `06-dev/`
- Version drift and release baselines: `07-versioning/`

## Index Strategy

- Use `query_reference.py` first for broad cross-source lookup, symbols, HTML attributes, and mixed official / blue-book discovery.
- Use `query_api_index.py` for fast official name, kind, category, scope, and source filtering.
- If an index disagrees with raw upstream source, raw upstream source wins.

## Support Docs

- `overview.md` is the shortest route map.
- `workflows.md` is an operational checklist.
- Prefer the numbered tree for actual reference reading.

## Refresh

- Run `python skills/typst/scripts/build_reference.py` after upstream snapshot changes.
- Run `python skills/typst/scripts/refresh_typst_knowledge.py` after official inventory changes.
- Update `07-versioning/` whenever the Typst release baseline changes.

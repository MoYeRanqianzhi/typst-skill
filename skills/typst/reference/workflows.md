# Typst Workflows

## API Lookup

- Exact API: `python skills/typst/scripts/query_reference.py --name dictionary.at`
- Category/topic: `python skills/typst/scripts/query_reference.py --query layout grid`
- HTML typed element: `python skills/typst/scripts/query_reference.py --query html video`
- Chinese example: `python skills/typst/scripts/query_reference.py --query wasm plugin`

## Answering Questions

1. Anchor the Typst version first.
2. Search the generated index.
3. Open the returned local source files for verification.
4. Add Blue Book examples when the user wants a tutorial or Chinese explanation.
5. Check the latest changelog if behavior may have changed across versions.

## Migration Guidance

- Search the generated index for deprecation messages.
- Read `typst/docs/changelog/0.14.2.md`, `typst/docs/changelog/0.14.1.md`, and `typst/docs/changelog/0.14.0.md`.
- Recommend feature detection via `"name" in std` or `sys.version` when back-compat matters.

## Packages, Templates, And Plugins

- Packages and imports: Blue Book tutorial files around modulization and packages.
- Templates: Blue Book `src/template/` and official tutorial/template docs.
- Plugins/WASM: Blue Book tutorial/reference files mentioning WASM plugin usage.
- HTML export: official `typst/docs/reference/export/html.md`, `typst/crates/typst-html/src/`, and cached typed HTML metadata.

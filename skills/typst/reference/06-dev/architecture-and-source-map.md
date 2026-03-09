# Architecture and Source Map

## Use

- Support source-level Typst maintenance by mapping features, docs, macros, and compiler phases to the right crates and files.

## Authoritative Sources

- `typst/docs/dev/architecture.md`
- `typst/docs/src/lib.rs`
- `typst/docs/reference/groups.yml`
- `typst/crates/typst-library/src/lib.rs`
- `typst/crates/typst-macros/src/elem.rs`
- `typst/crates/typst-macros/src/scope.rs`

## Crate Map

- `crates/typst`: main compiler crate and high-level language integration.
- `crates/typst-syntax`: parser and syntax tree.
- `crates/typst-eval`: evaluator / interpreter.
- `crates/typst-realize`: show-rule realization path.
- `crates/typst-layout`: layout engine.
- `crates/typst-library`: standard library categories and public APIs.
- `crates/typst-pdf`, `crates/typst-html`, `crates/typst-svg`, `crates/typst-render`: export and rendering backends.
- `crates/typst-ide`: IDE-facing semantic tooling.
- `crates/typst-cli`: command-line interface and environment wiring.
- `docs`: official documentation source tree.
- `tests`: integration tests and reference outputs.

## Compilation Pipeline

1. parsing in `typst-syntax`
2. evaluation in `typst-eval`
3. realization and layout in `typst-realize` and `typst-layout`
4. export in backend crates such as `typst-pdf` and `typst-html`

## How Public APIs Surface

- `typst-library/src/**` holds the public library implementation.
- `docs/reference/**` provides the narrative reference pages.
- `docs/reference/groups.yml` defines grouped pages and math helper groupings.
- `typst-macros` powers attributes such as `#[func]`, `#[elem]`, `#[ty]`, and `#[scope]`, which are key to extracting the public API surface.

## Maintenance Workflow

- Start from the official docs page or changelog note.
- Map the feature to the category or group page.
- Trace the implementation into the corresponding crate or library module.
- Refresh the generated indexes after structural or version updates.

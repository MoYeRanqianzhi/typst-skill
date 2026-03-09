# Compile, Debug, Publish

## Use

- Handle `typst` CLI execution, backend selection, environment setup, debugging, and release-ready output decisions.

## Authoritative Sources

- `typst/crates/typst-cli/src/args.rs`
- `typst/docs/tutorial/1-writing.md`
- `typst/docs/tutorial/3-advanced.md`
- `typst/docs/guides/page-setup.md`
- `typst/docs/guides/accessibility.md`
- `typst/docs/reference/export/pdf.md`
- `typst/docs/reference/export/html.md`

## Command Matrix

- `typst compile`: compile one input to `pdf`, `png`, `svg`, or `html`.
- `typst watch`: recompile on change; same compile arguments, plus optional HTML server behavior when that feature is enabled.
- `typst eval`: evaluate Typst code, optionally with `--in <file>` for document-aware introspection.
- `typst query`: still exists in `0.14.2` but is hidden and deprecated in favor of `eval`.
- `typst fonts`: inspect discovered font families and variants.
- `typst info`: print environment and build facts; supports human-readable and machine-readable formats.
- `typst completions`: generate shell completions.

## Output and Target Controls

- `--target` selects the compilation target, especially `paged` versus `html`.
- `--format` controls the output format when it should not be inferred from the output extension.
- `--deps` and `--deps-format` control dependency reporting for build-system integration.
- `--open` can open the produced output in a viewer after compilation.
- `--timings` emits a JSON timing trace suitable for tools such as Perfetto.
- For `png` and `svg`, multi-page output needs a page-number template in the output path such as `page-{0p}.png`.

## World and Environment Inputs

- `--root` / `TYPST_ROOT`: define the project root for absolute paths.
- `--input key=value`: expose runtime inputs through `sys.inputs`.
- `--package-path` / `TYPST_PACKAGE_PATH`: add a local package search root.
- `--package-cache-path` / `TYPST_PACKAGE_CACHE_PATH`: control package cache storage.
- `--font-path` / `TYPST_FONT_PATHS`: add custom font search directories.
- `TYPST_IGNORE_SYSTEM_FONTS`: ignore system fonts unless explicitly added.
- `TYPST_CERT`: use a custom CA certificate for network requests.
- `SOURCE_DATE_EPOCH`: set the creation timestamp for reproducible builds.

## Debug Workflow

1. Reproduce the issue with the smallest possible `.typ` file.
2. Lock `--root`, `--font-path`, and package paths so the environment is stable.
3. Decide whether the problem is syntax, evaluation, layout, export, or environment.
4. Use `typst eval` for expression-level investigation and `typst info` for environment facts.
5. If the issue is backend-specific, test the relevant `--target` / `--format` combination explicitly.
6. If the issue involves accessibility or HTML semantics, open the relevant export docs before proposing a fix.

## Publish Checklist

- Pin fonts and package inputs for reproducibility.
- Select the backend intentionally instead of relying on a PDF-only assumption.
- For accessible PDF work, verify semantic structure, `figure.alt`, `math.equation.alt`, and `pdf.artifact` usage.
- For HTML work, verify that the document does not depend on paged-only layout tricks.
- Preserve build metadata requirements such as `SOURCE_DATE_EPOCH` when reproducibility matters.

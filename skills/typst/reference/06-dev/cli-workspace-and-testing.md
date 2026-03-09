# CLI, Workspace, and Testing

## Use

- Support source-level maintenance, scripted workflows, and environment diagnostics.

## Authoritative Sources

- `typst/crates/typst-cli/src/args.rs`
- `typst/tests/**`
- `typst/docs/tutorial/**`

## Current CLI Focus

- `typst compile`
- `typst watch`
- `typst init`
- `typst eval`
- `typst fonts`
- `typst info`
- `typst completions`

## Environment and Parameters

- `TYPST_ROOT` / `--root`
- `--input` mapped to `sys.inputs`
- `TYPST_PACKAGE_PATH` / `--package-path`
- `--package-cache-path`
- `--font-path`

## Debug Strategy

- Minimize to a small `.typ` reproduction.
- Keep root, font-path, and package-path stable to avoid environment drift.
- Use `typst info` when environment facts matter.

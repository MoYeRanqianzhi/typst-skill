# CLI, Workspace, and Testing

## Use

- Support source-level maintenance, scripted workflows, and environment diagnostics.

## Authoritative Sources

- `typst/crates/typst-cli/src/args.rs`
- `typst/tests/**`
- `typst/docs/tutorial/**`
- `typst/docs/changelog/0.14.0.md`

## Current CLI Surface

- `typst compile`
- `typst watch`
- `typst init`
- `typst query`
- `typst eval`
- `typst fonts`
- `typst info`
- `typst completions`

## Argument Families

- `CompileArgs` for shared compile and watch behavior.
- `WorldArgs` for root and input handling.
- `PackageArgs` for package path and cache control.
- `FontArgs` for font discovery and overrides.
- `ProcessArgs` and related CLI plumbing for diagnostics and server-facing behavior.

## Debug Strategy

- Minimize to a small `.typ` reproduction.
- Keep root, font path, and package path stable to avoid environment drift.
- Use `typst info` when environment facts matter.
- Use `typst query` or the skill's own query scripts when checking whether a bug is structural or backend-specific.
- Check `typst/tests/**` for nearby regression coverage before changing scripts or assumptions.

## Maintenance Notes

- `0.14.0` added `typst info`, `typst completions`, and `typst query --target`.
- If CLI behavior in the skill becomes stale, `args.rs` is the authoritative local source.

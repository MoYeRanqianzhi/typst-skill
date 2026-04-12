# Known Issues

## Upstream Drift

- The Chinese blue book still contains traces of older Typst baselines such as `0.11`, `0.12.x`, and `0.13.1`.
- The blue book is weaker than the official docs on CLI behavior, package ecosystem details, and `0.14.x` export and accessibility changes.

## Provenance Limits

- In this repo, `typst/` and `The Raindrop-Blue Book/` are vendored local directories without their own checked-in `.git` metadata.
- Because of that, upstream commit provenance for those snapshots is not machine-verifiable from this workspace alone.
- Any exact upstream commit claims must be treated as external notes unless backed by a checked-in manifest.

## Environment Blockers

- In the current Windows environment, direct `cargo run -p typst-docs` has been blocked by linker / PDB issues.
- Earlier `cargo run --release -p typst-docs` attempts were also limited by disk pressure.
- Because of this, the current skill relies on source parsing plus generated indexes instead of a direct `typst-docs` artifact.

## Chinese Typesetting Traps

- Typst string literals interpret Chinese full-width quotes `""` `''` as string delimiters, causing compilation errors. Use `「」` `『』` instead. Documented in `chinese-typesetting.md`.
- Cross-platform CJK font availability varies: `Microsoft YaHei` absent on Linux/macOS, `SimSun` absent on macOS. Reference docs now recommend fallback chains.

## Version Mismatch

- SKILL.md targets Typst 0.14.2 but local CLI is 0.13.1. Reference docs should note minimum version for 0.14.x-specific features.

## Reference Documentation Gaps (Partially Addressed)

- v0.4.0 expanded all 2/5-scored files with code examples. Remaining gaps:
  - `data-loading.md`, `introspection.md`, `symbols.md` still at 3/5 (no code examples).
  - `plugins-html-pdf-svg-png.md`, `state-counter-query-locator.md` at 3/5.
  - No reference for: font management, custom numbering, PDF metadata, multi-file projects, Typst vs LaTeX migration.

## Scripts Quality Notes

- `query_reference.py`: function names (`rit`/`rdoc`/`rgrep`) are terse; `infer_root()` uses hardcoded `parents[4]`.
- `refresh_typst_knowledge.py`: no argparse, `--help` triggers full refresh; depends on `yaml` without install check.
- Two parallel index systems (`generated/` vs `08-generated/`) add maintenance cost.

## Current Acceptance Blockers

- No confirmed active blocker remains in the three previously failing index classes: helper-driven `global.*`, scoped sub-elements, and nested symbol exact lookups were repaired on 2026-03-09 and revalidated locally.
- Keep watching for future upstream syntax changes in Typst source macros or `sym.txt` layout that could require parser updates.

## Index Strategy Limits

- The skill keeps both `reference/generated/` and `reference/08-generated/`.
- `query_reference.py` is the default entry point because it also covers symbols, HTML attributes, and blue-book material.
- `query_api_index.py` is a fast official inventory, not a replacement for the comprehensive index.
- If generated data and raw source disagree, always verify against `typst/` and trust the raw upstream source.

> Support note: This file is a generated-index support document. Prefer the numbered reference tree for normal task routing.

﻿# Typst Skill Overview

- Purpose: provide a source-backed Typst skill rooted in the local `typst` compiler source tree and the local Chinese Blue Book repository.
- Primary version anchor: Typst `0.14.2` from `typst/Cargo.toml`.
- Primary upstream source tree: `typst/`.
- Chinese example source tree: `The Raindrop-Blue Book/`.
- Generated index: `reference/generated/typst-reference.json`.

## Source Priority

1. Local Typst source code and official docs source under `typst/`
2. Generated index under `reference/generated/`
3. Chinese Blue Book examples under `The Raindrop-Blue Book/`
4. Raw grep fallback through `scripts/query_reference.py`

## What Is Covered

- Standard library functions, types, elements, scope methods, and deprecation markers extracted from Rust source.
- Typed HTML element metadata extracted from the local `typst-assets` checkout in Cargo cache.
- Symbol and emoji block entries extracted from the local `codex` crate source in Cargo cache.
- Official docs source pages from `typst/docs/`.
- Blue Book `.typ` tutorial/example files from `The Raindrop-Blue Book/src/`.

## Rebuild

Run `python skills/typst/scripts/build_reference.py`.

This regenerates:

- `skills/typst/reference/generated/typst-reference.json`
- `skills/typst/reference/generated/summary.md`

## Known Limitation

- Full `typst-docs` JSON generation was attempted but blocked locally by Windows linker/PDB limits in debug mode and disk-space exhaustion in release mode.
- Because of that, the current skill uses a source parser plus local cached data sources (`typst-assets`, `codex`) instead of the compiled `typst-docs` binary output.
- When the parser and raw source disagree, trust the raw source and note the discrepancy.

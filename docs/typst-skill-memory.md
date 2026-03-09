# Typst Skill Shared Memory

## Role

- This file is the append-only implementation and verification log.
- Do not store the canonical current state here; `docs/project-memory.md` owns that role.

## 2026-03-09 Initial Snapshot

- Confirmed the local official Typst baseline as `0.14.2` from `typst/Cargo.toml`.
- Observed the blue-book dependency baseline as `0.13.1` from `The Raindrop-Blue Book/Cargo.toml`.
- Created `skills/typst/` and `docs/`.
- Added `SKILL.md`, `agents/openai.yaml`, the layered reference tree, and the generated index scripts.

## 2026-03-09 Verification Snapshot

- Ran the first 16-way concurrent completeness review across SOP, docs, reference pages, scripts, generated artifacts, and versioning notes.
- Found multiple corrupted reference pages and repaired workflow, language, library, recipe, dev, and versioning references.
- Improved cross-source queryability, including HTML attributes and official inventory filters.
- Launched a second 15-way concurrent final acceptance review.
- Second final acceptance review still found blockers in docs memory quality, changelog / known-issues traceability, and broad index generator consistency.

## 2026-03-09 Index Repair Snapshot

- Repaired `build_reference.py` so scoped sub-elements declared through `#[scope] impl ... { #[elem] type ...; }` are emitted with exact qualified names instead of flattened top-level names.
- Repaired `refresh_typst_knowledge.py` with the same scoped-member recovery logic, fixing official inventory records such as `figure.caption`, `table.cell`, `curve.move`, and `place.flush`.
- Expanded `build_reference.py` binding extraction to scan helper `global.define_*` calls outside the single `Module::new("global", ...)` file, restoring exact `global.*` coverage.
- Expanded symbol parsing so nested `sym.txt` members become first-class lookup keys like `sym.arrow.r` and `sym.arrow.r.squiggly`.
- Rebuilt both generated index layers and revalidated the repaired queries through `query_reference.py` and `query_api_index.py`.

## Historical Decisions

- The skill uses two index layers: a broad cross-source index and a fast official inventory.
- Official source and docs are authoritative; the blue book is secondary and recipe-oriented.
- Because direct `typst-docs` generation is blocked in this environment, committed generated artifacts are produced by local source-grounded scripts.

## Follow-up Candidates

- Replace local vendored snapshot provenance with a checked-in manifest if verifiable upstream commit tracking becomes required.
- Add a stable acceptance checklist for representative queries such as `pdf.artifact`, `math.thin`, `figure.caption`, and HTML attribute lookups.
- Add a lightweight automated smoke-test script for representative query samples if future acceptance needs to be repeatable in one command.

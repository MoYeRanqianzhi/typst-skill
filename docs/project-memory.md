# Project Memory

## Role

- This file is the canonical current-state memory for the `typst` skill.
- Keep it concise, readable, and authoritative.
- Historical detail belongs in `docs/typst-skill-memory.md`.

## Project Summary

- Project name: `Typst Skill`
- Skill name: `typst`
- Goal: provide a source-grounded Typst skill for authoring, debugging, templating, package work, source-level maintenance, and API lookup.

## Current Baseline

- Official local snapshot: `./typst`
- Chinese blue-book snapshot: `./The Raindrop-Blue Book`
- Official Typst baseline used by the skill: `0.14.2`
- Blue-book dependency baseline observed locally: `0.13.1`
- Vendored snapshots are local directories without their own checked-in `.git` metadata in this repo, so upstream commit provenance is not machine-verifiable here.

## Source Priority

1. Raw official source under `typst/`
2. Official docs under `typst/docs/`
3. Generated indexes under `skills/typst/reference/generated/` and `skills/typst/reference/08-generated/`
4. Blue-book explanations, templates, and recipes under `The Raindrop-Blue Book/`

## Current Architecture

- `skills/typst/SKILL.md` provides routing and the standard operating procedure.
- `skills/typst/reference/` stores the layered workflow, language, library, recipe, dev, and versioning references.
- `skills/typst/scripts/build_reference.py` builds the broad cross-source index.
- `skills/typst/scripts/query_reference.py` is the default broad lookup entry point.
- `skills/typst/scripts/refresh_typst_knowledge.py` builds the lightweight official inventory.
- `skills/typst/scripts/query_api_index.py` is the fast official inventory query tool.

## Maintenance Workflow

1. Refresh local `typst/` and `The Raindrop-Blue Book/` snapshots when needed.
2. Run `python skills/typst/scripts/build_reference.py`.
3. Run `python skills/typst/scripts/refresh_typst_knowledge.py`.
4. Verify representative lookups: `global.assert`, `global.pagebreak`, `sym.arrow.r`, `figure.caption`, `table.cell`, `curve.move`, and `place.flush`.
5. Review `skills/typst/reference/generated/summary.md` and `skills/typst/reference/08-generated/typst-api-index.md`.
6. Update `skills/typst/reference/07-versioning/` if the Typst baseline changes.
7. Run `python C:/Users/MoYeR/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/typst`.

## Verified Index Coverage

- Broad index now resolves `global.*` aliases emitted through helper `define(&mut global)` paths, including `global.assert`, `global.pagebreak`, `global.target`, and `global.length`.
- Broad index now preserves scoped element names declared through `#[scope] impl ... { #[elem] type ...; }`, including `figure.caption`, `table.cell`, `curve.move`, and `place.flush`.
- Symbol inventory now expands nested symbol families from `sym.txt`, including exact names such as `sym.arrow.r` and `sym.arrow.r.squiggly`.
- Fast official inventory under `reference/08-generated/` now emits scoped names for figure, table, curve, and place sub-elements instead of flattening them to top-level names.

## Documentation Rules

- Keep current rules here.
- Move dated implementation history to `docs/typst-skill-memory.md`.
- Track active blockers in `docs/known-issues.md`.
- Track milestone-style project updates in `docs/changelog.md`.

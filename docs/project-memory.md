# Project Memory

## Role

- This is the canonical current-state memory for the `typst` skill.
- Keep this file concise, current, and authoritative.
- Put detailed historical notes into `docs/typst-skill-memory.md`.

## Project Summary

- Project name: `Typst Skill`
- Skill name: `typst`
- Goal: provide a complete Typst Agent Skill for `Typst 0.14.2`, covering official workflows, language guidance, library reference, API lookup, debugging guidance, blue-book recipes, and version-risk notes.

## Current Baseline

- Official source snapshot: `./typst`
- Chinese blue-book snapshot: `./The Raindrop-Blue Book`
- Official stable version: `Typst 0.14.2`
- Blue-book version traces: mixed `0.11`, `0.12.0`, and `0.13.1`, so version documents are mandatory.

## Important Paths

- `skills/typst/SKILL.md` - SOP and routing logic
- `skills/typst/scripts/build_reference.py` - comprehensive cross-source index builder
- `skills/typst/scripts/query_reference.py` - default cross-source query entry point
- `skills/typst/scripts/refresh_typst_knowledge.py` - lightweight official inventory builder
- `skills/typst/scripts/query_api_index.py` - lightweight official inventory query entry point
- `skills/typst/reference/generated/` - comprehensive generated artifacts
- `skills/typst/reference/08-generated/` - lightweight official inventory artifacts

## Maintenance Workflow

1. Update local `typst` or blue-book snapshots.
2. Run `python skills/typst/scripts/build_reference.py`.
3. Run `python skills/typst/scripts/refresh_typst_knowledge.py`.
4. Check `skills/typst/reference/generated/` and `skills/typst/reference/08-generated/`.
5. If the Typst version changes, update `skills/typst/reference/07-versioning/`.
6. Run `python C:/Users/MoYeR/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/typst`.

## Design Decisions

- `SKILL.md` handles routing; `reference/` handles detailed knowledge.
- Official Typst docs/source take precedence over the blue book.
- Keep two index layers: a broad default index and a fast official-only inventory.
- Prefer concise references and progressive disclosure over large monolithic docs.

## Encoding

- Store all Skill and docs files as UTF-8 without BOM when possible.

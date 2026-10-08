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

- Official local checkout: `./typst`
- Chinese blue-book checkout: `./The Raindrop-Blue Book`
- Official source manifest version: `0.15.1`; the skill and committed indexes still target `0.14.2`.
- Blue-book dependency baseline observed locally: `0.13.1`.
- Both source directories are independent shallow Git clones, ignored by the skill repository. Their upstream commits are verifiable locally; cloning the skill repository alone does not include them.

Upstream default branches retrieved on `2026-10-08`:

| Source | Upstream | Branch | Commit |
| --- | --- | --- | --- |
| Official source and docs | [typst/typst](https://github.com/typst/typst) | `main` | `e58a63af09032a486b12241d08ebd04131483221` |
| Chinese blue book | [typst-doc-cn/tutorial](https://github.com/typst-doc-cn/tutorial) | `main` | `b2e19b6c9ddcec580c9f5b2741bd3b323b2eaf8c` |

- The blue book's three submodules are checked out at the revisions pinned by its parent repository.
- These are default-branch checkouts, not release-tag checkouts. Downloading them does not establish skill compatibility with their newer content.

## Source Priority

1. Raw official source under `typst/`
2. Official docs under `typst/docs/`
3. Generated indexes under `skills/typst/reference/generated/` and `skills/typst/reference/08-generated/`
4. Blue-book explanations, templates, and recipes under `The Raindrop-Blue Book/`

## Current Architecture

- `skills/typst/SKILL.md` (97 lines, v0.4.0) provides routing and the standard operating procedure.
  - L1 description: ~30 words, "Use when..." format.
  - Routing: Quick intent check → Error triage → Subsystem routes → Creating from scratch.
  - Workflow: 7 steps including Verify + If-stuck fallback.
- `skills/typst/reference/` stores the layered references, now with code examples in all core files.
  - `02-language/`: 4 files, all expanded to 140-173 lines with runnable Typst code.
  - `03-library/`: 6 files, key files expanded to 80-197 lines with API examples.
  - `05-recipes/`: 5 files, patterns and chinese-typesetting expanded with templates.
- `skills/typst/scripts/build_reference.py` builds the broad cross-source index.
- `skills/typst/scripts/query_reference.py` is the default broad lookup entry point.
- `skills/typst/scripts/refresh_typst_knowledge.py` builds the lightweight official inventory.
- `skills/typst/scripts/query_api_index.py` is the fast official inventory query tool.

## Maintenance Workflow

1. Update the local clones with `git -C typst pull --ff-only` and `git -C "The Raindrop-Blue Book" pull --ff-only`, followed by `git -C "The Raindrop-Blue Book" submodule update --init --recursive`. Before rebuilding against the current source, adapt the index generators to `docs/content/**/*.typ` and the replacement for the former `docs/reference/groups.yml`; they still expect the older Markdown/YAML layout.
2. Run `python skills/typst/scripts/build_reference.py`.
3. Run `python skills/typst/scripts/refresh_typst_knowledge.py`.
4. Verify representative lookups: `global.assert`, `global.pagebreak`, `sym.arrow.r`, `figure.caption`, `table.cell`, `curve.move`, and `place.flush`.
5. Review `skills/typst/reference/generated/summary.md` and `skills/typst/reference/08-generated/typst-api-index.md`.
6. Update `skills/typst/reference/07-versioning/` if the Typst baseline changes.
7. Validate with `<skill-creator-path>/scripts/quick_validate.py skills/typst`.

## Verified Index Coverage

- Broad index now resolves `global.*` aliases emitted through helper `define(&mut global)` paths, including `global.assert`, `global.pagebreak`, `global.target`, and `global.length`.
- Broad index now preserves scoped element names declared through `#[scope] impl ... { #[elem] type ...; }`, including `figure.caption`, `table.cell`, `curve.move`, and `place.flush`.
- Symbol inventory now expands nested symbol families from `sym.txt`, including exact names such as `sym.arrow.r` and `sym.arrow.r.squiggly`.
- Fast official inventory under `reference/08-generated/` now emits scoped names for figure, table, curve, and place sub-elements instead of flattening them to top-level names.

## Documentation Rules

- Keep recursive Python cache ignore rules in root `.gitignore` (`**/__pycache__/`, `*.py[cod]`) so local bytecode never blocks rebase or branch switching again.
- Keep current rules here.
- Move dated implementation history to `docs/typst-skill-memory.md`.
- Track active blockers in `docs/known-issues.md`.
- Track milestone-style project updates in `docs/changelog.md`.

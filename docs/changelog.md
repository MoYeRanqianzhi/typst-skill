# Changelog

## 2026-03-09

- Initialized the root repository and created `skills/typst/` and `docs/`.
- Added `SKILL.md`, `agents/openai.yaml`, layered references, and version notes for Typst `0.14.2`.
- Added the broad index pipeline: `build_reference.py` and `query_reference.py`.
- Added the lightweight official inventory pipeline: `refresh_typst_knowledge.py` and `query_api_index.py`.
- Generated `reference/generated/` and `reference/08-generated/` artifacts from the local snapshots.
- Completed a first 16-way concurrent completeness review.
- Rewrote corrupted or underspecified workflow, language, library, recipe, dev, and versioning reference pages.
- Tightened index portability, HTML-attribute queryability, official inventory naming, and inventory filtering.
- Clarified long-term memory roles in `docs/`.
- Current local `HEAD`: `369ddd3` (`agent(claude): ??Skill????`).
- Existing local tags observed during verification: `typst-skill-v0.1.0`, `typst-skill-v0.1.1`, `typst-skill-v0.1.1-text`, `typst-skill-v0.2.0`, `typst-skill-v0.3.0`, `typst-skill-docs`.
- Completed a second 15-way concurrent final acceptance review and identified remaining blocking issues in docs memory quality and broad index generator consistency.
- Repaired broad-index extraction for helper-driven `global.*` aliases, including `global.assert` and `global.pagebreak`.
- Repaired scoped-name extraction for both index layers so `figure.caption`, `table.cell`, `curve.move`, and `place.flush` resolve exactly.
- Repaired nested symbol expansion from `sym.txt`, including exact lookups such as `sym.arrow.r` and `sym.arrow.r.squiggly`.
- Rebuilt `skills/typst/reference/generated/typst-reference.json` and `skills/typst/reference/08-generated/typst-api-index.json` after the parser fixes.
- Re-ran targeted regression checks for the repaired index classes and confirmed the previously blocking lookup samples now pass.

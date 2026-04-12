# Changelog

## 2026-04-12 — v0.4.0: Reference Expansion & SKILL.md Rewrite

### SKILL.md Rewrite (Phase 1)
- Rewrote description to ~30 words, "Use when..." format per CSO standards.
- Added Quick intent check table (create / explain / fix / modify).
- Added Error triage routing (syntax, type, font, context, layout, version).
- Added Creating from scratch quick-start path.
- Separated Chinese typesetting as independent route entry.
- Enhanced standard workflow: multi-file selection guidance, Verify step, If-stuck fallback.
- Fixed hardcoded user path to placeholder.
- Total: 97 lines (within 120-line L2 budget).

### Core Language References (Phase 2, P0)
- `markup-and-document-structure.md`: 40→162 lines. Added #expr/[content]/{code} modes, headings, lists, labels/refs, figure/table, import/include, 5 error pairs.
- `styling-layout-and-show-rules.md`: 37→167 lines. Added set/show rules, selectors, scope/cascade, page config, 4 error pairs.
- `scripting-and-context.md`: 37→173 lines. Added let/closures/loops/context/state/counter examples, error table.
- `math-and-symbols.md`: 38→144 lines. Added inline/block equations, frac/sqrt/mat/vec/cases, symbols, alignment.
- `book-paper-slide-cv-patterns.md`: 37→186 lines. Added 3 minimal runnable templates (paper, CV, slides).

### Library & Recipe References (Phase 3, P1)
- `chinese-typesetting.md`: 26→expanded. Added font config, quote trap ⚠️, lang/region, minimal template.
- `layout.md`: 30→expanded. Added page/grid/stack/columns/align examples, parameter quick-ref.
- `visualize.md`: 33→expanded. Added rect/circle/line/gradient/image examples, card combo pattern.
- `text.md`: 26→132 lines. Added text params, highlight/underline/strike, raw, lorem, sub/super.
- `model.md`: 31→189 lines. Added heading/outline, figure/caption, table, bibliography, list/enum.
- `foundations.md`: 31→197 lines. Added array/dict/str methods, calc module, type conversion, datetime.

### Process
- Conducted 4 parallel review audits (SOP, reference, scripts, cat-resume test).
- Reference docs average score: 2.85/5 → targeted all 2/5 files for expansion.
- Used 5-agent parallel team for implementation.

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
- Hardened root `.gitignore` with recursive Python cache rules so `__pycache__` artifacts no longer block rebase or branch switching.

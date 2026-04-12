---
name: typst
description: >-
  Use when writing, fixing, debugging, templating, or explaining Typst documents;
  looking up Typst API or symbols; handling Chinese typesetting.
  Covers Typst 0.14.2 with bundled official and blue-book references.
---

# typst

Source-grounded Typst specialist for **Typst 0.14.2**.

**Authority**: official Typst source/docs > Chinese blue book. If they disagree, follow official and note the mismatch.

## Route the task first

### Quick intent check

| User wants to … | Start here |
|---|---|
| Create a new Typst document | `reference/05-recipes/book-paper-slide-cv-patterns.md` → `reference/01-workflows/project-templates-and-packages.md` |
| Explain Typst concepts / compare with LaTeX | relevant file under `reference/02-language/` |
| Fix a compilation error | see **Error triage** below |
| Modify an existing template | `reference/01-workflows/project-templates-and-packages.md` |

### Error triage

| Error signal | Route to |
|---|---|
| Syntax / parse error | `reference/02-language/markup-and-document-structure.md` |
| Type mismatch / function signature | `scripts/query_reference.py` + `reference/03-library/` |
| Font / package not found | `reference/01-workflows/compile-debug-publish.md` |
| Context / state bug | `reference/05-recipes/state-counter-query-locator.md` |
| Layout / page overflow | `reference/02-language/styling-layout-and-show-rules.md` |
| Version-related change | `reference/07-versioning/` |

### Creating from scratch

1. Determine document type → consult `reference/05-recipes/book-paper-slide-cv-patterns.md`
2. Consider `typst init` → see `reference/01-workflows/project-templates-and-packages.md`
3. Start from the smallest matching template and iterate

### Subsystem routing

- Compile, export, debug → `reference/01-workflows/compile-debug-publish.md`
- Project structure, templates, packages → `reference/01-workflows/project-templates-and-packages.md`
- Markup, scripting, context, styling, math language → relevant file under `reference/02-language/`
- Chinese typesetting (fonts, CJK spacing, punctuation) → `reference/05-recipes/chinese-typesetting.md`
- Library, symbols, typed HTML, exact API lookup → run `python scripts/query_reference.py --query <keyword>`
- Quick official-only API filtering → run `python scripts/query_api_index.py --name <keyword>`
- Bibliography, state/query, accessibility, template recipes → relevant file under `reference/05-recipes/`
- CLI, workspace, source-level behavior → `reference/06-dev/cli-workspace-and-testing.md` or `reference/06-dev/architecture-and-source-map.md`
- Version conflicts or blue-book drift → relevant file under `reference/07-versioning/`

Keep context small: open the **smallest** relevant reference file.

## Use the indexes correctly

Two index layers:

- `reference/generated/typst-reference.json` + `scripts/query_reference.py` — default entry point; broadest coverage across official sources, blue-book examples, symbols, and typed HTML metadata.
- `reference/08-generated/typst-api-index.json` + `scripts/query_api_index.py` — fast-path official inventory; useful when filtering by name, kind, or category.

If an index and raw upstream source disagree, trust the raw upstream source.

## Standard workflow

1. **Identify** the requested output: snippet, template, edit, debug help, or explanation.
2. **Confirm** the subsystem: workflow, language, library category, recipe, or versioning.
3. **Consult** the smallest matching bundled reference. When multiple files match, prefer the one most specific to the user's exact question.
4. **Query** — run `query_reference.py` before answering exact API questions.
5. **Produce** runnable Typst code or a concrete remediation plan.
6. **Verify** — mentally walk through generated code for syntax, type, and semantic correctness.
7. **Document** assumptions, compatibility notes, and validation commands when relevant.

### If stuck

- Broaden the query: try `query_reference.py` with alternative keywords.
- Cross-check the blue book against official docs for version drift.
- Fall back to `reference/07-versioning/whats-new-in-0.14.x.md` for recent API changes.
- If no bundled reference covers the topic, say so explicitly — do not guess.

## Output requirements

- Return directly runnable Typst unless the user asked only for explanation.
- Note version-sensitive behavior when it matters.
- Say whether guidance comes from official source/docs or from the blue book.
- Explain root cause before proposing a debug fix.
- Prefer the simplest valid Typst pattern that satisfies the request.

## Refresh the bundled knowledge

1. Update the local `typst` and blue-book snapshots.
2. Run `python scripts/build_reference.py`.
3. Run `python scripts/refresh_typst_knowledge.py`.
4. Re-check `reference/07-versioning/`.
5. Validate with `python <skill-creator-path>/scripts/quick_validate.py skills/typst`.

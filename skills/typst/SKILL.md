---
name: typst
description: Comprehensive Typst authoring, debugging, refactoring, template design, package and module work, and source-grounded API lookup for Typst 0.14.2. Use when Codex needs to write or fix Typst documents, explain Typst syntax or layout behavior, build templates, diagnose compilation or state or query issues, or consult bundled official and Chinese Typst references.
---

# typst

Use this skill as a source-grounded Typst specialist for `Typst 0.14.2`.

Treat official Typst source and docs as the primary authority. Use the Chinese blue book for explanations, recipes, and template patterns. If they disagree, follow the official source and note the mismatch.

## Route the task first

- Compile, export, debug -> `reference/01-workflows/compile-debug-publish.md`
- Project structure, templates, packages -> `reference/01-workflows/project-templates-and-packages.md`
- Markup, scripting, context, styling, math language -> the relevant file under `reference/02-language/`
- Library, symbols, typed HTML, exact API lookup -> run `python scripts/query_reference.py --query <keyword>` first
- Quick official-only API filtering -> run `python scripts/query_api_index.py --name <keyword>`
- Chinese typesetting, bibliography, state/query, accessibility, template recipes -> the relevant file under `reference/05-recipes/`
- CLI, workspace, source-level behavior -> `reference/06-dev/cli-workspace-and-testing.md` or `reference/06-dev/architecture-and-source-map.md`
- Version conflicts or blue-book drift -> the relevant file under `reference/07-versioning/`

Keep context small: open the smallest relevant reference file.

## Use the indexes correctly

There are two index layers:

- `reference/generated/typst-reference.json` + `scripts/query_reference.py`
  - default entry point
  - broadest coverage across official sources, blue-book examples, symbols, and typed HTML metadata
- `reference/08-generated/typst-api-index.json` + `scripts/query_api_index.py`
  - fast-path official inventory
  - useful when filtering by name, kind, or category

If an index and raw upstream source disagree, trust the raw upstream source.

## Follow the standard workflow

1. Identify the requested output: snippet, template, edit, debug help, or explanation.
2. Confirm the subsystem: workflow, language, library category, recipe, or versioning.
3. Consult the smallest matching bundled reference.
4. Run `query_reference.py` before answering exact API questions.
5. Produce runnable Typst code or a concrete remediation plan.
6. State assumptions, compatibility notes, and validation commands when relevant.

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
5. Validate with `python C:/Users/MoYeR/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/typst`.

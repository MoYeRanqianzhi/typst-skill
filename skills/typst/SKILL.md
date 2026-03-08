---
name: typst
description: Comprehensive Typst authoring, debugging, refactoring, template design, package/module work, and source-grounded API lookup for Typst 0.14.2. Use when Codex needs to write or fix Typst documents, explain Typst syntax or layout behavior, build templates, diagnose compilation or state/query issues, or consult bundled official and Chinese Typst references.
---

# typst

Use this skill as a source-grounded Typst specialist.

Default to the bundled knowledge base, which is grounded in:

- the official `typst` source snapshot at `0.14.2`
- the official `docs/reference`, `docs/tutorial`, `docs/guides`, and `docs/changelog`
- the local Chinese blue book snapshot in `The Raindrop-Blue Book`
- the bundled generated indexes under `reference/generated/` and `reference/08-generated/`

Treat official Typst sources as the primary authority. Use the blue book to add Chinese explanations, recipes, and template patterns. If they disagree, follow the official source and note the mismatch.

## Route the task first

Classify the request before opening more files:

- **Compile / debug / publish workflow** → open `reference/01-workflows/compile-debug-publish.md`
- **Project layout / templates / packages** → open `reference/01-workflows/project-templates-and-packages.md`
- **Markup / scripting / show-set / context / math language questions** → open the relevant file under `reference/02-language/`
- **Standard-library / symbols / HTML typed API lookup** → first run `python scripts/query_reference.py --query <keyword>`; use `python scripts/query_api_index.py --name <keyword>` when you need a fast official-only inventory filter
- **Chinese typesetting / bibliography / figures / state / query / template recipes** → open the relevant file under `reference/05-recipes/`
- **CLI / workspace / source-level behavior** → open `reference/06-dev/cli-workspace-and-testing.md` or `reference/06-dev/architecture-and-source-map.md`
- **Version conflicts / migration / blue-book drift** → open the relevant file under `reference/07-versioning/`

Keep context small: load only the minimal reference file that matches the current task.

## Follow the standard workflow

1. Identify the requested output type: document snippet, full template, package/module edit, debugging help, or explanation.
2. Confirm the relevant Typst subsystem: language, library category, workflow, recipe, or versioning.
3. Consult the smallest bundled reference that answers the question.
4. If the request depends on exact API names, locations, or availability, run `scripts/query_reference.py` first.
5. Use `scripts/query_api_index.py` if you need a quick official-only filter by name, kind, or category.
6. Produce runnable Typst code or a concrete remediation plan.
7. State assumptions, compatibility notes, and the command needed to validate the result when relevant.

## Use the bundled indexes correctly

The skill ships with two complementary indexes:

- `reference/generated/typst-reference.json` + `scripts/query_reference.py`:
  - broader cross-source index
  - includes official API items, docs pages, blue-book files, and extra generated metadata
  - best default search path for most questions
- `reference/08-generated/typst-api-index.json` + `scripts/query_api_index.py`:
  - lightweight official-source inventory
  - good for quick category/kind filtering and source anchoring

When a generated index and raw upstream source disagree, trust the raw upstream source and mention the discrepancy.

## Prefer this source order

Use sources in this order unless the task explicitly asks otherwise:

1. `reference/07-versioning/whats-new-in-0.14.x.md`
2. `reference/generated/typst-reference.json`
3. `reference/08-generated/typst-api-index.json` and `reference/08-generated/typst-api-index.md`
4. the relevant `reference/02-language/`, `reference/03-library/`, `reference/04-modules/`, or `reference/06-dev/` file
5. the official upstream file path referenced inside that document
6. the blue-book recipe or Chinese explanation in `reference/05-recipes/`

## Produce answers with these guarantees

- Return code that is directly runnable in Typst unless the user asked only for explanation.
- Explicitly note version-sensitive behavior when it matters.
- Call out whether a recommendation comes from official docs/source or from the blue book.
- When debugging, explain the likely root cause before proposing a fix.
- When multiple valid Typst patterns exist, prefer the simplest one that matches the requested output.

## Refresh the bundled knowledge

When maintaining this skill itself:

1. Update the local `typst` and blue-book snapshots.
2. Run `python scripts/build_reference.py` to rebuild the comprehensive cross-source index.
3. Run `python scripts/refresh_typst_knowledge.py` to rebuild the lightweight official inventory.
4. Re-read the changed `reference/07-versioning/` notes.
5. Validate with `python C:/Users/MoYeR/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/typst`.

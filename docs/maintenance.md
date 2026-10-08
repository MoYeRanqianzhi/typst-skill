# Design and maintenance

## Runtime design

`skills/typst/SKILL.md` is the entrypoint. Eight focused guides under `references/` cover authoring, math/data, layout/CJK, debugging, exports, packages, documentation/version boundaries, and migration. They explain decisions and non-obvious constraints; they do not duplicate the entire standard-library manual.

`scripts/docs.py` is the single runtime lookup entrypoint:

- `search`: offline ranked discovery in `references/catalog.json`.
- `show`: exact-name/URL resolution, official page fetch or cache, advertised version check, anchored text extraction; symbols use bundled metadata.
- `status`: catalog provenance, with an explicit optional latest-release check.

`scripts/refresh_catalog.py` is a maintainer operation, not a prerequisite for using the skill. It fetches official search metadata and supplemental symbol, typed-HTML, and selected constant locations, checks version identity, and replaces the catalog atomically only after validation. Both scripts use Python's standard library and locate resources relative to their own files.

The former `reference/` hierarchy, dual generated indexes, Rust regex signature extraction, and four legacy scripts are retired. There are no compatibility wrappers: use the documented new commands.

## Evidence and boundaries

The verified baseline is **0.15.1**, latest stable on **2026-10-09**. Release tag commit: `9dfd3a08500b7896045f907433cf7b4b02434fad`. The original `typst/` development checkout can legitimately have another commit with the same manifest version; it must not silently define stable behavior.

The catalog stores the release URL/commit, retrieval timestamp, official index hash, supplemental source hashes, and observed live-doc source commits. The official website and release tag are distinct provenance sources. Exact functions are located through official metadata, not inferred from Rust return types or arbitrary neighboring filenames.

Typst and blue-book checkouts remain optional research inputs outside the installed skill. The blue book's older dependency baseline means its examples need current compiler checks. Neither source checkout is silently required by a query.

## Updating a baseline

1. Check the latest stable release and the project's intended target:

   ```sh
   python skills/typst/scripts/docs.py status --check-latest
   ```

2. Read that release's changelog/migration notes and inspect the tag, not just `main`. Run a compiler reporting that version; verify downloaded release assets against their published checksums when supplied.
3. Generate a candidate catalog explicitly:

   ```sh
   python skills/typst/scripts/refresh_catalog.py --version 0.15.1
   ```

   `--latest` is an explicit alternative. A refresh updates only the catalog; it does not upgrade guidance, examples, or user environments. Use `--output <candidate.json>` for review without replacing the bundled file. The live website must advertise the requested version; this command is not a historical documentation archive downloader.
4. Review the provenance and coverage diff, especially scoped definitions, parameters, symbols, and typed HTML. Resolve changed locations or removed APIs without inventing aliases.
5. Update affected guides, `SKILL.md` metadata/baseline, and README claims. Re-run the checks in [validation](validation.md), including a standalone installation and realistic independent tasks.

## Development hygiene

Do not put fetched pages, compiler binaries, personal paths, evaluation outputs, or source worktrees in the distributed skill. Use ignored local directories for these artifacts. Worktree roots and `.agents/` records with a `.local` segment stay untracked. Ignore rules prevent ordinary untracked bytecode additions; they do not override files already tracked in historical commits.

User-facing documentation belongs here and in the READMEs. Durable agent design decisions belong in `.agents/memory/`, linked from `.agents/MEMORY.md`; unfinished work belongs in ignored local plans when it contains machine-specific setup.

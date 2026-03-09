> Support note: This file supports the generated-index pipeline. Prefer the numbered reference tree for normal task routing.

# Workflows

## Purpose

- Document the maintenance workflow for the generated indexes.
- Keep query and rebuild commands in one small support note.

## Default Query Flow

1. Use `python skills/typst/scripts/query_reference.py --query <keyword>` for broad cross-source lookup.
2. Use `python skills/typst/scripts/query_api_index.py --name <keyword>` for quick official-only filtering.
3. Open the returned upstream source path to verify final behavior.

## Rebuild Flow

1. Update local upstream snapshots under `typst/` and `The Raindrop-Blue Book/`.
2. Run `python skills/typst/scripts/build_reference.py`.
3. Run `python skills/typst/scripts/refresh_typst_knowledge.py`.
4. Re-check `reference/07-versioning/` if the Typst version changed.

## Open This File When

- You are rebuilding indexes after upstream updates.
- You need the canonical query commands.
- You are debugging differences between the broad index and the lightweight official inventory.

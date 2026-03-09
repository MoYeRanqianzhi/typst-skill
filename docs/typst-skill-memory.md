# Typst Skill Shared Memory

## Role

- This file is the append-only shared implementation log for the `typst` skill.
- Keep current-state guidance in `docs/project-memory.md`.
- Put detailed historical facts, decisions, and implementation notes here.

## Confirmed Upstream Facts

- Typst version: `0.14.2`
- Typst commit used during implementation: `364ece3cb37975f509a779fc3ddc929285971d73`
- Typst remote: `https://github.com/typst/typst`
- Blue-book commit used during implementation: `f8d51ad0cb99a886dbe347f0d71c4f3a49c1f59f`
- Blue-book remote: `https://github.com/typst-doc-cn/tutorial`

## Key Technical Decisions

- Do not rely on conversational context as the only memory.
- Prefer local upstream source and docs over recollection.
- Use `build_reference.py` and `query_reference.py` as the default cross-source search layer.
- Keep `refresh_typst_knowledge.py` and `query_api_index.py` as a lighter official inventory path.
- Keep blue-book content as a secondary source for explanation, templates, and Chinese recipes.

## Environment Notes

- `cargo run -p typst-docs` debug builds were blocked on this machine by Windows linker or PDB issues.
- `cargo run --release -p typst-docs` was previously blocked by disk pressure.
- Because of this, the current skill relies on a source-parsing index pipeline instead of a direct `typst-docs` JSON artifact.

## Historical Milestones

- 2026-03-09: initialized the root repo and created `skills/typst/` and `docs/`.
- 2026-03-09: confirmed local Typst baseline as `0.14.2`.
- 2026-03-09: added SOP, layered references, index builders, and query scripts.
- 2026-03-09: added dual-index routing and version-risk notes.
- 2026-03-09: aligned `data-loading` naming with official docs and added a `symbols` reference page.

## Future Follow-Up

- If the environment allows, compare the custom index output against a true `typst-docs` artifact.
- Refine `query_reference.py` ranking based on real usage feedback.
- Expand typed HTML and accessibility recipes if future usage shows they need more depth.

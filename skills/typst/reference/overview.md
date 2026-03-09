> Support note: This file supports the generated-index pipeline. Prefer the numbered reference tree for normal task routing.

# Overview

## Purpose

- Explain what the generated cross-source index is for.
- Clarify why the skill keeps both a broad index and a lightweight official inventory.

## Open This File When

- You need to understand the role of `reference/generated/typst-reference.json`.
- You are maintaining `build_reference.py` or `query_reference.py`.
- You need a quick reminder of the source-priority rules behind the generated index.

## Key Points

- The default search layer is `reference/generated/typst-reference.json`.
- It combines official Typst source/docs, blue-book material, and cached metadata used by the builder.
- The lightweight official inventory lives under `reference/08-generated/` and is a fast-path, not the default broad search layer.
- When generated data and raw upstream source disagree, trust the raw upstream source.

## Rebuild

- Run `python skills/typst/scripts/build_reference.py` to refresh the comprehensive generated index.
- Run `python skills/typst/scripts/refresh_typst_knowledge.py` to refresh the lightweight official inventory.

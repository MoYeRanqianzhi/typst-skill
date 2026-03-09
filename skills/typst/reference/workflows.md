# Workflows

## Standard Procedure

1. Identify whether the task is workflow, language, library, recipe, dev, or versioning.
2. Open the smallest matching reference page.
3. For exact API questions, run the query scripts before answering.
4. If the answer is version-sensitive, verify against the local official changelog or source snapshot.
5. If blue-book guidance differs from official Typst, state the drift and prefer the official source.

## Query Shortcuts

- broad cross-source lookup: `python skills/typst/scripts/query_reference.py --query <keyword>`
- fast official inventory lookup: `python skills/typst/scripts/query_api_index.py --name <keyword>`

## When to Escalate to Raw Source

- the query indexes disagree
- a behavior is target-specific or version-sensitive
- a recipe appears older than `0.14.2`
- the task needs exact CLI or backend semantics

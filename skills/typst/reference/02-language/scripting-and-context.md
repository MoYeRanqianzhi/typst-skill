# Scripting and Context

## Use

- Handle expressions, bindings, functions, loops, modules, context, state, counters, and query-like behavior.

## Authoritative Sources

- `typst/docs/reference/language/scripting.md`
- `typst/docs/reference/language/context.md`
- `The Raindrop-Blue Book/src/tutorial/writing-scripting.typ`
- `The Raindrop-Blue Book/src/tutorial/scripting-*.typ`
- `The Raindrop-Blue Book/src/tutorial/doc-stateful.typ`

## Core Concepts

- `let`, functions, closures, destructuring, conditionals, and loops are the scripting foundation.
- `context`, `state`, `counter`, `locate`, and `query` depend on layout-aware execution.
- The same code can yield different results at different positions or layout stages.
- Prefer modularization over repeated inline logic.

## Debug Focus

- First decide whether the problem is pure computation or layout-aware context behavior.
- If `query`, `counter`, or `state` is involved, consider multi-pass layout effects.
- If output depends on position, inspect `context` and locatable elements first.

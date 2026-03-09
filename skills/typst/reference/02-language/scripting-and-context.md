# Scripting and Context

## Use

- Handle expressions, bindings, functions, modules, loops, context-dependent evaluation, and layout-aware introspection behavior.

## Authoritative Sources

- `typst/docs/reference/language/scripting.md`
- `typst/docs/reference/language/context.md`
- `typst/docs/reference/library/introspection.md`
- `The Raindrop-Blue Book/src/tutorial/writing-scripting.typ`
- `The Raindrop-Blue Book/src/tutorial/doc-stateful.typ`

## Core Concepts

- `let`, closures, loops, conditionals, destructuring, and module imports form the scripting foundation.
- `context`, `state`, `counter`, `locate`, and `query` are layout-aware and may change across compilation passes.
- A result can depend on position, target, and surrounding structure, not just on local code.
- Prefer reusable helpers and modules over repeating inline logic.

## Debug Split

- Pure scripting issue: evaluate expressions, bindings, and data flow.
- Layout-aware issue: inspect `context`, locatable elements, and introspection loops.
- Export-aware issue: also inspect `target()` and backend-specific branches.

## Common Mistakes

- treating `query` like a static collection lookup
- writing self-affecting state or show-rule logic
- debugging context-sensitive behavior without a stable minimal reproduction

## Also See

- `../05-recipes/state-counter-query-locator.md`
- `../03-library/introspection.md`

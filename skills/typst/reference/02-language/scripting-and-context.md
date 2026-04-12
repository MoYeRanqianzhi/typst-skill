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

---

## `let` Bindings and Functions

```typst
// Simple binding
#let name = "Typst"

// Function definition (short form)
#let greet(name) = [Hello, #name!]

// Function with default parameter
#let badge(label, color: blue) = box(
  fill: color.lighten(80%),
  inset: 4pt,
  radius: 3pt,
  text(fill: color, weight: "bold", label),
)

#greet("World")          // → Hello, World!
#badge("NEW")            // → blue badge
#badge("WARN", color: red) // → red badge
```

## Closures

```typst
// Anonymous function (closure)
#let double = (x) => x * 2
#double(4) // → 8

// Passing closures to built-in functions
#let nums = (3, 1, 4, 1, 5)
#nums.sorted()                     // → (1, 1, 3, 4, 5)
#nums.map((n) => n * 10)           // → (30, 10, 40, 10, 50)
#nums.filter((n) => calc.rem(n, 2) == 1) // → (3, 1, 1, 5)
```

## Conditionals (`if` / `else`)

```typst
#let score = 85

#if score >= 90 [
  Excellent
] else if score >= 60 [
  Pass
] else [
  Fail
]

// Inline ternary-style (expression returns value)
#let label = if score >= 60 { "pass" } else { "fail" }
```

## Loops

```typst
// for loop — iterate arrays, ranges, dictionaries
#for i in range(1, 4) [
  Item #i \
]

#let data = ("Alice": 90, "Bob": 78)
#for (name, score) in data [
  #name scored #score \
]

// while loop
#{
  let i = 1
  let total = 0
  while i <= 100 {
    total += i
    i += 1
  }
  [Sum 1–100 = #total]
}
```

## `context` — Layout-Aware Evaluation

`context` creates an expression that is resolved **after layout**. Required for any introspection.

```typst
// Get current page number
#context counter(page).get().first()

// Get current heading
#context {
  let elems = query(selector(heading).before(here()))
  if elems.len() > 0 {
    elems.last().body
  }
}
```

> ⚠ `context` blocks cannot be stored into variables evaluated at scripting time; they produce *content*, not plain values.

## `state` — Mutable Document State

```typst
#let answer = state("answer", 0)

// Update state
#answer.update(42)
#answer.update((old) => old + 1)

// Read state (must be inside context)
The answer is #context answer.get().
```

## `counter` — Built-in Counters

```typst
// Page counter (built-in)
Page #context counter(page).get().first() of
#context counter(page).final().first()

// Heading counter
#set heading(numbering: "1.1")
= Introduction
Section #context counter(heading).get().first()
```

## Destructuring

```typst
#let (a, b) = (1, 2)        // array destructuring
#let (name: n, age: a) = (name: "Jo", age: 30) // dict destructuring
#let (first, ..rest) = (1, 2, 3, 4) // spread
```

## Common Errors

| Symptom | Cause | Fix |
|---------|-------|-----|
| "cannot access `get` on state" | Missing `context` wrapper | Wrap in `#context { ... }` |
| Loop produces no output | Using `{ }` code block without joining content | Use `[ ]` markup blocks or explicit `+` to join content |
| "expected content, found integer" | Bare expression in markup | Prefix with `#` or wrap in `[#value]` |
| Infinite recompilation | State update depends on state read at same position | Separate read/write locations; avoid self-affecting logic |

## Debug Split

- Pure scripting issue: evaluate expressions, bindings, and data flow.
- Layout-aware issue: inspect `context`, locatable elements, and introspection loops.
- Export-aware issue: also inspect `target()` and backend-specific branches.

## Also See

- `../05-recipes/state-counter-query-locator.md`
- `../03-library/introspection.md`

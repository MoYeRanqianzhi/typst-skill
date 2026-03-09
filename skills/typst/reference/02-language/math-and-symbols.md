# Math and Symbols

## Use

- Handle math mode, text-versus-math boundaries, symbol lookup, and formula structure questions.

## Authoritative Sources

- `typst/docs/reference/language/syntax.md`
- `typst/docs/reference/library/math.md`
- `typst/docs/reference/library/symbols.md`
- `The Raindrop-Blue Book/src/tutorial/writing-math.typ`

## Core Concepts

- Math mode and text mode follow different spacing and parsing rules.
- Prefer built-in math functions and structures over manual glyph composition.
- `sym`, `emoji`, and math syntax solve different classes of symbol problems.
- For non-trivial formulas, check matrix, delimiter, attachment, and variant APIs explicitly.

## High-Value Topics

- inline versus block equations
- `mat`, `vec`, `cases`, `frac`, `root`, `sqrt`
- attachments, scripts, fences, and delimiters
- shorthand-like symbols versus named symbol access
- accessibility-sensitive math such as `math.equation.alt`

## Common Mistakes

- applying text styling assumptions directly inside math
- guessing symbol names instead of querying them
- forgetting that delimiter and attachment behavior is semantic, not just visual

## Exact Lookup

- Use `query_reference.py` for symbol-heavy lookups because the broad index covers far more symbol data than the lightweight inventory.

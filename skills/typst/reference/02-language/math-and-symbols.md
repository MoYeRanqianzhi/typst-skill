# Math and Symbols

## Use

- Handle math mode, symbols, formula structure, and text-versus-math boundary questions.

## Authoritative Sources

- `typst/docs/reference/language/syntax.md`
- `typst/docs/reference/library/math.md`
- `typst/docs/reference/library/symbols.md`
- `The Raindrop-Blue Book/src/tutorial/writing-math.typ`
- `The Raindrop-Blue Book/src/tutorial/reference-math-*.typ`

## Core Concepts

- Math mode and text mode have different spacing, binding, and semantic rules.
- Prefer built-in math API over manual glyph composition.
- `sym`, `emoji`, and `math` serve different symbol roles.
- For complex formulas, check matrix, root, attachment, delimiter, and math-class APIs explicitly.

## Common Pitfalls

- Applying text styling assumptions directly to math content.
- Ignoring default attachment and delimiter behavior.
- Remembering syntax but not checking the actual math element or API that controls it.

# Markup and Document Structure

## Use

- Answer questions about Typst markup mode, structural elements, references, content blocks, and document organization.

## Authoritative Sources

- `typst/docs/reference/language/syntax.md`
- `typst/docs/tutorial/1-writing.md`
- `The Raindrop-Blue Book/src/tutorial/writing-markup.typ`

## Core Concepts

- Typst fuses markup, code, and content into one language.
- `#expr` embeds expressions, `[...]` creates content blocks, and `{...}` creates code blocks.
- Prefer semantic elements such as headings, lists, figures, tables, labels, and references over manual visual imitation.
- Keep stable labels separate from presentation text so references remain maintainable.

## Common Pitfalls

- Letting a `#` expression run longer than intended because the expression boundary is unclear.
- Mixing content blocks and code blocks without remembering how values join.
- Solving structure problems with manual spacing instead of semantic elements and styles.

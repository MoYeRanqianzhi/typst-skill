# Markup and Document Structure

## Use

- Answer questions about markup mode, block structure, labels and references, imports, and semantic document organization.

## Authoritative Sources

- `typst/docs/reference/language/syntax.md`
- `typst/docs/tutorial/1-writing.md`
- `typst/docs/tutorial/2-formatting.md`
- `The Raindrop-Blue Book/src/tutorial/writing-markup.typ`

## Core Concepts

- Typst fuses markup, content, and code into one language.
- `#expr` embeds code into markup, `[...]` builds content, and `{...}` creates code blocks.
- Use semantic elements such as headings, lists, figures, tables, quotes, terms, and references instead of manual visual imitation.
- Keep labels stable and presentation-independent so references survive refactoring.
- Use `import` for code and reusable definitions, and `include` for pulling another Typst document's content into the current flow.

## Structural Hotspots

- heading hierarchy and outline generation
- labels, `ref`, and `link` targets
- list and term semantics
- figure and table wrappers instead of ad hoc captions
- document-level metadata such as `title`

## Common Mistakes

- letting a `#` expression continue longer than intended
- using raw spacing to fake structure
- styling plain text to look like a semantic element instead of using the real element
- mixing `include` and `import` responsibilities

## Exact Lookup

- For exact element or function questions, run `python skills/typst/scripts/query_reference.py --query <keyword>`.

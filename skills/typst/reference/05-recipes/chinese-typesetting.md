# Chinese Typesetting

## Use

- Provide Chinese typography, font setup, mixed-language layout, and local best-practice guidance.

## Authoritative Sources

- `The Raindrop-Blue Book/src/tutorial/writing-chinese.typ`
- `The Raindrop-Blue Book/src/tutorial/scripting-style.typ`
- `typst/crates/typst-cli/src/args.rs`
- `typst/docs/guides/page-setup.md`

## Practice Notes

- Lock fonts with `--font-path` or a stable project font directory for reproducibility.
- Solve Chinese and mixed-language spacing with fonts, language settings, and paragraph rules instead of manual spaces.
- Put typography decisions such as margins, emphasis, heading style, and punctuation strategy into templates when possible.
- Re-check emoji, icon, and fallback font behavior on the actual target machine.

## Validation

- confirm the chosen fonts really contain the required Han glyph coverage
- verify punctuation, quotation, and line-break behavior in realistic paragraphs
- check exact API usage against the official `0.14.2` baseline before repeating older blue-book examples verbatim

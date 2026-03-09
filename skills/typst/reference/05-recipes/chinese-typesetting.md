# Chinese Typesetting

## Use

- Provide Chinese typography, font setup, mixed-language layout, and local best-practice guidance.

## Authoritative Sources

- `The Raindrop-Blue Book/src/tutorial/writing-chinese.typ`
- `The Raindrop-Blue Book/src/tutorial/scripting-style.typ`
- `typst/crates/typst-cli/src/args.rs`

## Practice Notes

- Lock fonts with `--font-path` or a stable project font directory for reproducibility.
- Solve Chinese and mixed-language spacing with fonts and paragraph rules, not ad hoc manual spaces.
- Move typography decisions such as margins, emphasis, and heading style into templates when possible.
- Use the blue book for practical Chinese examples, but always verify API availability against the official 0.14.2 baseline.

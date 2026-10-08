# Migrating to Typst 0.15

Use this when a version upgrade is part of the request, or a symptom plausibly comes from a version mismatch. Record the current compiler and package pins first. Compare rendered pages before and after changing them: some 0.15 changes alter layout without producing errors.

## Changes that affect implementation choices

| Need | 0.15 behavior and consequence |
| --- | --- |
| Pass an asset path into a package | The new `path` type preserves the file where it was constructed; a plain string resolves where it is consumed |
| Windows-authored imports/assets | Typst file paths require `/`; backslashes are no longer accepted |
| Document introspection from CLI | `typst eval --in main.typ 'query(heading)'` supersedes `typst query`; inspect the expression's result and exit status |
| Nested document selection | `selector(...).within(...)` avoids manually filtering a global query by ancestry |
| Separate bibliographies | `bibliography(target: ..., group: ...)` controls citation routing and numbering groups; read the exact API before combining them |
| Variable fonts | Use the family name and `text(variations: ...)`; the `Variable`, `Var`, and `VF` family-name suffixes are stripped |
| HTML equations | Native MathML is available; test the consuming browser and styling |
| Multiple output files | Experimental bundle export can contain `document` and `asset` outputs; do not apply its flags to ordinary PDF builds |
| Thematic break | `divider` provides semantic content that a template can style |
| Printing | `color.spot` and combined PDF standards are available; check the actual print/output requirements |

## Changes that can break or silently shift output

- Baselines now propagate through more boxes, blocks, list items, and equations. Revisit compensating offsets if alignment changes; do not automatically reintroduce the old workaround.
- Glyph stretching in 0.15 starts from the base glyph rather than a display-sized variant, so explicit `math.stretch` settings may need retuning. This is distinct from `math.lr(size: ...)`, whose ratio scales against the height of the enclosed content; do not use one formula for both APIs. Check the [release implementation of `lr`](https://github.com/typst/typst/blob/v0.15.1/crates/typst-library/src/math/lr.rs) when the changelog's broad wording is insufficient.
- Math classes no longer apply recursively to every descendant. Default calligraphic letterforms also changed; the former forms can be selected through stylistic set 6 of the matching New Computer Modern Math font.
- HTML paragraph grouping distinguishes neutral elements; typed HTML no longer necessarily produces the old implicit paragraphs. `box`/`block` wrappers may be omitted or expressed through CSS. Inspect actual HTML before updating selectors.
- `html.script` and `html.style` take strings; use a raw block's `.text` when embedding code. Content blocks accepted by older versions may now fail.
- Exported SVGs no longer contain the former `typst-frame`, `typst-doc`, `typst-group`, `typst-shape`, and `typst-text` classes. Update downstream styling based on the actual output structure.
- Some functions reject inputs they previously tolerated, including a slice with both `end` and `count`. Follow renamed symbol/citation-style diagnostics. Review the release notes' removals when migrating from 0.13 or earlier.

## Patch release

0.15.1 fixes math alignment regressions, multi-page list gaps, and the CLI evaluation exit code, and updates embedded New Computer Modern fonts to 8.1.1. A newer system-installed font can still change output, so compiler pinning alone does not make typography reproducible.

These are migration decision points, not a replacement for the complete [0.15.0 release notes and migration guide](https://typst.app/docs/changelog/0.15.0/) and [0.15.1 fixes](https://typst.app/docs/changelog/0.15.1/). For exact historical behavior use the [release-tag changelog source](https://github.com/typst/typst/tree/v0.15.1/docs/content/changelog).

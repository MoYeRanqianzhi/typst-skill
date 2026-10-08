# Layout and Chinese typography

Use for paged layout, mixed Chinese/Latin text, font problems, and content that
must survive changes in length. Behavior below targets **Typst 0.15.1**, release
commit `9dfd3a08500b7896045f907433cf7b4b02434fad`. The tagged source links are the
authority; live documentation can describe a different revision. The Raindrop
Blue Book's Chinese examples are secondary reading, not a compatibility promise:
its embedded compiler dependency is 0.13.1.

## Discover fonts before choosing typography

Run discovery with the same compiler and font paths used for the final render:

```sh
typst --version
typst fonts --variants
typst fonts --font-path ./fonts --ignore-system-fonts --variants
```

Use the reported **family name**, not a font filename or an assumed operating
system alias. Check the requested weights/styles and representative Han glyphs.
A family being listed does not establish coverage of every character. Do not
install a long platform-specific fallback chain and hope one entry matches.

For mixed fonts, order matters: Typst tries the specified families in order.
Putting a Latin family first can also select its curly quotes, dashes, and
ellipsis. A descriptor with `covers: "latin-in-cjk"` excludes selected shared
punctuation from that family, allowing the following CJK family to supply it.
This is **not** a general "Latin characters only" filter.

The probe below takes discovered names as inputs rather than embedding a font
policy. Set the shell variable `CJK_FONT` to the chosen family; `LATIN_FONT` is
optional and otherwise the probe uses the CJK family for both. Its small page
is a test surface, not a recommended document format.

```typst
#let cjk-font = sys.inputs.at("cjk-font")
#let latin-font = sys.inputs.at("latin-font", default: cjk-font)
#set text(
  font: ((name: latin-font, covers: "latin-in-cjk"), cjk-font),
  lang: "zh", region: "CN",
)
#set page(width: 110mm, height: auto, margin: 8mm)
#let title = "他说：“你好”。"
#title

中文English与API2026混排；《书名》（说明），标点：“引号”。

*粗体 Bold*，以及#text(lang: "en")[an English passage].
```

```sh
typst compile --input "cjk-font=$CJK_FONT" probe.typ "probe-{p}.png"
typst compile --input "cjk-font=$CJK_FONT" --input "latin-font=$LATIN_FONT" probe.typ "mixed-{p}.png"
```

If fonts live in a project directory, pass its `--font-path` to both discovery
and compilation. **`--font-path` adds fonts; it does not isolate them.** For a
controlled font inventory, also use `--ignore-system-fonts`; add
`--ignore-embedded-fonts` only when supplying all required families yourself.
Ship font files only when their license permits it. Record the actual files and
compiler version when matching output across machines matters.

Last-resort fallback searches other available fonts and can conceal a missing
glyph in the intended family. `text(fallback: false)` can help isolate a probe,
but 0.15.1 does not warn about missing glyphs when fallback is disabled: inspect
the rendered text, not just the exit status.

Sources: [font selection and fallback, tagged source](https://github.com/typst/typst/blob/v0.15.1/crates/typst-library/src/text/mod.rs#L90),
[CLI font options, tagged source](https://github.com/typst/typst/blob/v0.15.1/crates/typst-cli/src/args.rs),
[text documentation](https://typst.app/docs/reference/text/text/).

## Separate language, punctuation, and string syntax

- **Language:** use `lang: "zh"` and a separate `region`, such as `"CN"` or
  `"TW"`, for the intended text. These codes are case-insensitive. Mark genuine
  English passages locally with `text(lang: "en")`; language affects text
  processing and accessibility, not just appearance. In 0.15.1, Chinese/Japanese
  paragraphs use a line-break segmenter that treats curly double quotes as
  opening/closing punctuation. This is not a switch that creates Han coverage.
- **Region:** for Chinese, `TW` and `HK` select the engine's CNS punctuation
  behavior; `CN`, `SG`, and `MY` use its GB behavior. In particular, the CNS path
  skips the additional consecutive-punctuation compression pass. Region does
  not convert simplified/traditional text or guarantee a particular glyph form:
  choose suitable characters and fonts, and inspect the result.
- **Mixed spacing:** `cjk-latin-spacing: auto` is the default, independently of
  `lang: "zh"`. The implementation adds spacing at eligible Han/kana-to-letter
  or digit boundaries, normally `0.25em`, shrinkable to `0.125em`. Use `none` to
  disable it when the required typography calls for that. Do not layer manual
  spaces or `h(0.25em)` onto every boundary, or assume the same rule spans inline
  math, boxes, and all scripts. Compare the actual boundary that looks wrong.
- **Punctuation metrics:** curly quotes share Unicode codepoints with Latin
  typography. Compression depends on the selected glyph's width and shaping
  context, not just the character. Prefer the font coverage descriptor above
  over per-character show rules, which can split runs and disrupt punctuation
  adjustment or Latin kerning. Check `。”`, `《书名》（说明）`, `！？`, and line
  starts/ends in the intended font and region.

**Chinese quotation marks are valid text.** The probe's `#let title = "他说：“你好”。"`
and literal markup such as `他说：“你好”。` compile in 0.15.1. No escaping or
replacement with corner quotes is necessary. Code string literals, however,
use ASCII double quotes: `#let title = “中文”` and `#let title = '中文'` both fail.
ASCII apostrophes are not Typst string delimiters.

Straight quotes in markup invoke `smartquote`. In the 0.15.1 implementation,
both Chinese `CN` and `TW` fall through to curly quotation marks; do not promise
that changing region produces corner quotes. If the user wants corner quotes,
write them literally or configure them explicitly:

```typst
#set text(font: sys.inputs.at("cjk-font"), lang: "zh", region: "TW")
#set smartquote(quotes: (double: "「」", single: "『』"))
"外层 '内层' 文字"
```

Sources: [spacing implementation](https://github.com/typst/typst/blob/v0.15.1/crates/typst-layout/src/inline/prepare.rs#L123),
[regional punctuation and glyph metrics](https://github.com/typst/typst/blob/v0.15.1/crates/typst-layout/src/inline/shaping.rs#L1299),
[Chinese/Japanese line breaking](https://github.com/typst/typst/blob/v0.15.1/crates/typst-layout/src/inline/linebreak.rs#L41),
[smartquote selection](https://github.com/typst/typst/blob/v0.15.1/crates/typst-library/src/text/smartquote.rs).

## Choose layout by what must move together

| Need | Use | Consequence to check |
| --- | --- | --- |
| Running prose | Ordinary paragraphs, optionally `block` | Normal flow accounts for height and page breaks. Blocks are breakable by default. |
| A small item within a sentence | `box` | Participates inline, but is an unbreakable unit; do not box a long paragraph or table. |
| Aligned layout regions | `grid` | Tracks share dimensions; use it for presentation, not to disguise data tables. |
| Related data with headers | `table` | Supplies table semantics and repeating headers, unlike a layout grid. |
| A sequence along one axis | `stack` | Useful for small groups; a horizontal stack does not wrap like a paragraph or a CSS flex-wrap container. |
| An overlay or fixed annotation | `place` | Default placement reserves no space; later content can overlap it. |

Content brackets `[...]` group content; they do not by themselves create a
sized, unbreakable box. Keep long text in flow. Use an unbreakable block only
for a group that really must remain together and can fit on a page. A vertical
stack is not inherently a single-page object, but ordinary flow remains simpler
for headings, paragraphs, and page-breaking prose.

Set `page` dimensions and margins to the requested medium. Keep recurring
furniture in `page`'s header/footer or foreground/background rather than nudging
body text into position. A page set rule can start a new page; do not change
page geometry as a substitute for sizing a component. `height: auto` is useful
for cropped probes, but hides the page-break problems of a finite-height report.

In a grid/table, `auto` sizes tracks from content, whereas `1fr` receives a
share of the space remaining after other tracks and gutters. `columns: 2`
means two `auto` tracks, **not** two equal fractional tracks. Two `50%` tracks
plus a nonzero gutter oversubscribe the available width; use `(1fr, 1fr)` when
equal shares are intended. Let text rows grow instead of assigning fixed heights.

This fixture renders the same content at two widths. The label stays intrinsic;
the description reflows and changes the block height without positional offsets:

```typst
#let description = [A longer description wraps within the available column
  instead of moving a manually positioned object below it.]
#for available in (90mm, 55mm) {
  block(width: available, inset: 5pt, stroke: 0.5pt)[
    #grid(
      columns: (auto, 1fr),
      column-gutter: 1em, row-gutter: 0.4em,
      [*Date*], [2026-10-08],
      [*Scope*], description,
    )
  ]
}
```

Relative widths adapt to the available **typesetting** area; they are not
browser-responsive CSS. A grid will not automatically reduce its column count.
If the narrow form needs a different structure, select it deliberately using
`layout(size => ...)`, and test both structures with the longest real content.

Use `place` when overlap or a fixed anchor is intentional. At top level its
coordinates refer to the page's text area; inside `page.foreground` or
`page.background` they can address the full page. `float: true` instead reserves
space at the top/bottom; `dx`/`dy` still only move the drawing, not its reserved
space. Neither mode is general text wrapping around arbitrary shapes.

Sources: [page setup, tagged guide](https://github.com/typst/typst/blob/v0.15.1/docs/content/guides/page-setup.typ),
[box/block](https://github.com/typst/typst/blob/v0.15.1/crates/typst-library/src/layout/container.rs),
[grid sizing](https://github.com/typst/typst/blob/v0.15.1/crates/typst-library/src/layout/grid/mod.rs#L25),
[stack layout](https://github.com/typst/typst/blob/v0.15.1/crates/typst-layout/src/stack.rs),
[placement](https://github.com/typst/typst/blob/v0.15.1/crates/typst-library/src/layout/place.rs).

## Preserve long-table and paragraph flow

A bare table can span pages. `table.header` and `table.footer` repeat by default;
use `repeat: false` only when that is the desired meaning. Cells spanning an
`auto` row are breakable by default, whereas cells spanning only fixed-size rows
are not. For records that must stay intact, set `table.cell(breakable: false)`
on the relevant cells and verify the whole record fits. Oversized text should
split rather than disappear behind clipping or spill out of a fixed-height box.

A table inside a `figure` inherits an unbreakable block by default. When the
captioned table must span pages, make that figure block breakable and leave it
in flow rather than floating it. This finite-page fixture tests that behavior,
including repeated headers and the paragraph after the table. Its explicit cell
alignment keeps descriptive text start-aligned instead of inheriting the figure's
centering; choose alignment to suit the actual data.

```typst
#set page(width: 100mm, height: 80mm, margin: 8mm)
#show figure.where(kind: table): set block(breakable: true)
#figure(
  table(
    columns: (auto, 1fr),
    align: start,
    table.header([*ID*], [*Observation*]),
    ..range(1, 13).map(record => (
      str(record),
      [A record with enough text to wrap when the page becomes narrower.],
    )).flatten(),
  ),
  caption: [Observations across pages.],
)
This paragraph follows the complete table.
```

For Chinese paragraphs, choose indentation and justification from the user's
style, not from a universal template. `first-line-indent: 2em` applies to
consecutive paragraphs, not the first paragraph or one after a block such as a
heading. If **all** first lines must indent, use
`#set par(first-line-indent: (amount: 2em, all: true))`. `par.leading` is the gap
between line edges, not a baseline-to-baseline multiplier; changing font metrics
or `text.top-edge`/`bottom-edge` changes the resulting line rhythm. `par.spacing`
is the gap between paragraphs. Inspect both before trying to fix either with
blank lines or manual `v` calls.

Sources: [multi-page tables, tagged guide](https://github.com/typst/typst/blob/v0.15.1/docs/content/guides/tables.typ#L834),
[table cells and headers](https://github.com/typst/typst/blob/v0.15.1/crates/typst-library/src/model/table.rs),
[paragraph parameters](https://github.com/typst/typst/blob/v0.15.1/crates/typst-library/src/model/par.rs).

## Iterate on the rendered result

Compile to numbered PNGs so additional pages are visible, not accidentally
omitted. Carry over the final font paths and `--input` values where applicable:

```sh
typst compile layout.typ "layout-{p}.png" --ppi 144
```

Open the output images. Check the whole page for balance/flow, then inspect the
actual glyphs and punctuation at readable scale. Compilation alone does not
detect tofu, unintended fallback, overlap, awkward line breaks, or cropped text.

Use a short feedback loop tied to the defect:

- Missing or mismatched glyphs: confirm the discovered family, coverage, and
  weight before altering spacing. Re-render the same mixed-text probe.
- Excessive mixed-text gaps: compare `cjk-latin-spacing: auto` with `none`, and
  inspect source whitespace and run boundaries before adding manual spacing.
- Content colliding after edits: remove accidental unbreakable wrappers or
  fixed positions, then test a narrower width and a longer real paragraph.
- Multi-page tables: inspect the first page, every continuation boundary, and
  the final caption/following paragraph; also test one unusually tall cell.
- Dense Chinese paragraphs: inspect line starts/ends, punctuation clusters,
  first paragraphs after headings, and mixed bold/Latin runs using final fonts.

Change the responsible constraint, recompile, and reopen the affected pages.
Report the compiler and fonts actually tested, the variants visually inspected,
and remaining portability gaps. A successful render with local fonts is not
evidence that those fonts exist on another machine.

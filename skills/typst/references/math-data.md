# Math, references, bibliographies, and data

Baseline: **Typst 0.15.1**, [stable source at 9dfd3a08](https://github.com/typst/typst/tree/9dfd3a08500b7896045f907433cf7b4b02434fad).
The [0.15.0 changelog](https://typst.app/docs/changelog/0.15.0/) introduces multiple bibliographies; [0.15.1](https://typst.app/docs/changelog/0.15.1/) fixes math alignment within matched delimiters and operator positioning.
Online reference pages can describe newer versions. Examples below are independent and use only built-ins.

## Translate mathematical intent, not LaTeX syntax

- Use `$x^2$` inline and `$ x^2 $` for a displayed equation: whitespace at **both** ends determines block mode. Neither `$$...$$` nor LaTeX environments are needed.
- Use `alpha`, `sum`, `sqrt(...)`, `frac(...)` or `(numerator)/(denominator)`, not backslash commands. A single `\` is a line break, and `&` marks alignment points.
- Single letters in math are literal mathematical symbols; multi-letter identifiers resolve names. Separate products (`x y`), quote words (`"otherwise"`), and use `op("rank")` for a named operator with operator spacing.
- Use `#` to insert a computed code value into math. Compute numeric products before insertion or separate factors with `dot`: adjacent interpolated digits can visually merge. Math calls parse their arguments as math; code-valued options need forms such as `limits: #true`. Outside math, address math functions through `math.`.
- Use parentheses for grouping, `mat(1, 2; 3, 4)` for matrix rows, and `cases(...)` for branches instead of reproducing LaTeX array syntax.

```typst
#let amplitude = 3

Inline notation: $x_i^2$.

$ f(x) &= #amplitude x^2 + alpha \
  f'(x) &= #(2 * amplitude) x $

$ mat(1, 2; 3, 4) vec(alpha, beta) $

$ abs(x) = cases(
  x & "if" x >= 0,
  -x & "otherwise",
) $
```

Use a font with OpenType math support; a normal prose font is not automatically suitable. For an accessible equation, supply a natural-language `alt` description through `math.equation` and verify the requested export target rather than assuming visual math is sufficient.

Sources: [math syntax and functions](https://typst.app/docs/reference/math/), [LaTeX migration](https://typst.app/docs/guides/for-latex-users/), [equations and alternative text](https://typst.app/docs/reference/math/equation/).

## Let semantic elements own numbering

A label attaches to the nearest preceding non-space element **in the same content scope**. Put it immediately after the intended heading, equation, or figure. A label alone does not make arbitrary content referenceable: ordinary `@label` references need a referenceable numbered element. Use `link(<label>)[text]` when only a link is needed.

Use separate names such as `sec:method`, `eq:model`, and `tab:results`; avoid collisions with bibliography keys. A dynamically generated heading label should follow the constructed heading in markup, not be inserted into its title text.

```typst
#set heading(numbering: "1.")
#set math.equation(numbering: "(1)", supplement: [Eq.])
#show figure.where(kind: table): set figure.caption(position: top)
#show figure.where(kind: table): set block(breakable: true)

= Calibration <sec:calibration>

$ y = 2 x + 1 $ <eq:model>

#figure(
  table(
    columns: (1fr, auto),
    inset: 6pt,
    table.header([Input], [Output]),
    [0], [1],
    [1], [3],
  ),
  caption: [Model values.],
) <tab:model>

See @sec:calibration, @eq:model, and @tab:model.
#link(<sec:calibration>)[Jump to calibration.]
```

- **Equations:** numbering applies to block equations, not inline math. One aligned multi-line equation gets one number; use separate equation elements if each needs its own label/number.
- **Tables:** use `table` for data and `grid` for visual arrangement. Supply cells in row-major order; spread a flattened array with `..cells.flatten()` when generating cells. Mark header rows with `table.header`, which repeats by default for multipage tables.
- **Captions/references:** wrap a table in `figure` when it needs a caption and reference number. A table-containing figure normally infers `kind: table` and has a counter separate from image figures; set `kind` explicitly when inference is ambiguous.
- **Long tables:** figures are unbreakable by default. The example enables breaking only for table figures. Their bodies must also be breakable; avoid forcing a long table into a fixed-height or unbreakable container.
- **Images/floats:** use `figure`'s `placement` option when floating is wanted, and keep its source near the discussion for reading order. Put image alternative text on `image(alt: ...)`. Do not add a figure-level `alt` to an already accessible table, as it replaces access to the table body.
- **Reference customization:** change the supplement or numbering instead of typing numbers manually. Page references use `ref(<label>, form: "page")` and require page numbering to be configured.

Sources: [labels](https://typst.app/docs/reference/foundations/label/), [references](https://typst.app/docs/reference/model/ref/), [tables](https://typst.app/docs/reference/model/table/), [table headers](https://typst.app/docs/reference/model/table/#definitions-header), [figures](https://typst.app/docs/reference/model/figure/).

## Bibliography routing is distinct from numbering

Accept BibLaTeX `.bib` or Hayagriva `.yaml`/`.yml`. Cite with `@key` or `cite(<key>)`; use an explicit `cite` call for citation-specific options such as `form`. A bibliography normally lists only cited works. Use `full: true` for all entries, or `cite(<key>, form: none)` to include a selected work without printing the citation.

For one combined list, pass multiple source files to **one** bibliography. Do not create multiple bibliography elements just to merge files; duplicate keys within a combined source set are errors.

For chapter-specific or thematic lists, Typst **0.15 supports multiple bibliographies**:

- With `target: auto`, a citation goes to the closest following bibliography containing its key; if none follows, the closest preceding eligible bibliography is used.
- An explicit `target` selector takes priority over automatic assignment; the first bibliography whose selector matches gets the citation. Use this when placement alone cannot express a thematic/sidebar split.
- `group` controls numbering, **not citation selection**: default `auto` shares consecutive numbering; `none` numbers each bibliography independently; matching string groups share a sequence.

This self-contained example uses synthetic BibLaTeX entries. Each chapter cites a different work; `group: none` resets the second list's citation number to 1.

```typst
#let sources = bytes(
  "@book{north,title={Field Methods},author={Mira North},year={2024}}\n"
  + "@book{west,title={Data Practice},author={Ari West},year={2025}}"
)
#set bibliography(style: "ieee", group: none)

= Method
We follow this illustrative method. @north
#bibliography(sources, title: [Method references])

= Data
We use this illustrative data procedure. @west
#bibliography(sources, title: [Data references])
```

For real projects, replace `sources` with a checked-in bibliography path (or array of paths). Select a built-in CSL style requested by the user, or provide a local CSL file; do not rewrite citations through string substitution.

Sources: [bibliography, target, and group](https://typst.app/docs/reference/model/bibliography/), [citation options](https://typst.app/docs/reference/model/cite/), [0.15 bibliography changes](https://typst.app/docs/changelog/0.15.0/#model).

## Load data as values, then format it

- `csv("data.csv")` returns arrays of **strings** and retains the header row. With `row-type: dictionary`, the first row supplies keys and is not returned as data. Convert numeric fields with `int`/`float` before arithmetic.
- `json("data.json")` preserves structured types: objects become dictionaries, arrays remain arrays, numbers become numeric values, and `null` becomes `none`. Large integer identifiers outside signed 64-bit range can lose precision; encode identifiers as strings when exact digits matter.
- Validate the input shape/required fields at the data boundary when accepting outside data. Do not silently replace malformed measurements with zero or flatten nested objects indiscriminately.
- These loaders accept local paths or bytes, not arbitrary HTTP fetches. Resolve paths relative to the file with the loading call; use `path(...)` when passing a caller-relative location across modules.

Here bytes keep the example self-contained. Replace them with local file paths for production input; no separate decode helper is required.

```typst
#let rows = csv(
  bytes("sample,value\nA,12.5\nB,9.0\n"),
  row-type: dictionary,
)
#let config = json(bytes(
  "{\"scale\":2,\"unit\":\"mg\",\"title\":\"Batch #1\"}"
))

#heading(config.title)
#table(
  columns: (1fr, auto),
  table.header([Sample], [Scaled value]),
  ..rows.map(row => (
    row.sample,
    [#(float(row.value) * config.scale) #config.unit],
  )).flatten(),
)
```

This distinguishes numeric conversion from display: the two scaled values are 25 mg and 18 mg, while `Batch #1` remains ordinary text.

Sources: [CSV and row types](https://typst.app/docs/reference/data-loading/csv/), [JSON conversion](https://typst.app/docs/reference/data-loading/json/#conversion), [path resolution](https://typst.app/docs/reference/foundations/path/).

## Escape the source layer, not loaded data

Imported strings are not executed as Typst source. Insert them directly or pass them to `text`; use `raw` when verbatim/code presentation is intended. Do not run CSV/JSON/user text through `eval` to render it.

```typst
#let literal = "#literal *not bold* $x$ @missing [brackets]"
#literal

#raw(literal, block: true)
#raw("C:\\reports\\draft.typ")

Literal markup characters: \$5, \#, \*, \_.
```

When generating Typst source, escape markup-special characters in markup and escape `"`/`\` in string literals. JSON embedded inside a Typst string has **two encoding layers**; a separate JSON file avoids that extra layer. Do not pre-escape strings already returned by `csv`/`json` as if they were source: that prints unnecessary backslashes. `raw` is for presentation, not an input parser or a reason to evaluate data.

Sources: [escape sequences](https://typst.app/docs/reference/syntax/#escapes), [strings](https://typst.app/docs/reference/foundations/str/), [raw text](https://typst.app/docs/reference/text/raw/).

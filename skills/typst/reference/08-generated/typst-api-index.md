# Typst API Summary

- Generated at: `2026-03-09T05:12:16.721816+00:00`
- Typst version: `0.14.2`
- Typst commit: `364ece3`
- Blue-book Typst dependency: `0.13.1`
- Entries: `493` primary API records
- Kinds: `function=296`, `element=132`, `type=34`, `member=31`
- Official page sets: `language=4`, `library=9`, `export=4`
- Official group pages: `13`

Use `typst-api-index.json` plus `query_api_index.py` for the exhaustive inventory.

## Category Counts

- `export`: `6`
- `foundations`: `204`
- `introspection`: `26`
- `layout`: `64`
- `loading`: `11`
- `math`: `49`
- `model`: `44`
- `text`: `15`
- `visualize`: `74`

## Sample Entries

### export
- `artifact` - `crates/typst-library/src/pdf/accessibility.rs:37`
- `attach` - `crates/typst-library/src/pdf/attach.rs:33`
- `data-cell` - `crates/typst-library/src/pdf/accessibility.rs:236`
- `header-cell` - `crates/typst-library/src/pdf/accessibility.rs:175`
- `pdf-marker-tag` - `crates/typst-library/src/pdf/accessibility.rs:285`
- `table-summary` - `crates/typst-library/src/pdf/accessibility.rs:109`

### foundations
- `abs` - `crates/typst-library/src/foundations/calc.rs:73`
- `acos` - `crates/typst-library/src/foundations/calc.rs:322`
- `acosh` - `crates/typst-library/src/foundations/calc.rs:428`
- `arguments` - `crates/typst-library/src/foundations/args.rs:48`
- `arguments.at` - `crates/typst-library/src/foundations/args.rs:339`
- `arguments.construct` - `crates/typst-library/src/foundations/args.rs:315`
- `arguments.filter` - `crates/typst-library/src/foundations/args.rs:382`
- `arguments.len` - `crates/typst-library/src/foundations/args.rs:327`

### introspection
- `counter` - `crates/typst-library/src/introspection/counter.rs:210`
- `counter-display` - `crates/typst-library/src/introspection/counter.rs:664`
- `counter-update` - `crates/typst-library/src/introspection/counter.rs:639`
- `counter.at` - `crates/typst-library/src/introspection/counter.rs:435`
- `counter.construct` - `crates/typst-library/src/introspection/counter.rs:321`
- `counter.display` - `crates/typst-library/src/introspection/counter.rs:361`
- `counter.final-` - `crates/typst-library/src/introspection/counter.rs:450`
- `counter.get` - `crates/typst-library/src/introspection/counter.rs:343`

### layout
- `align` - `crates/typst-library/src/layout/align.rs:76`
- `alignment` - `crates/typst-library/src/layout/align.rs:142`
- `alignment.axis` - `crates/typst-library/src/layout/align.rs:195`
- `alignment.bottom` - `crates/typst-library/src/layout/align.rs:183`
- `alignment.center` - `crates/typst-library/src/layout/align.rs:178`
- `alignment.end` - `crates/typst-library/src/layout/align.rs:180`
- `alignment.horizon` - `crates/typst-library/src/layout/align.rs:182`
- `alignment.inv` - `crates/typst-library/src/layout/align.rs:212`

### loading
- `cbor` - `crates/typst-library/src/loading/cbor.rs:49`
- `cbor.encode` - `crates/typst-library/src/loading/cbor.rs:78`
- `csv` - `crates/typst-library/src/loading/csv.rs:27`
- `json` - `crates/typst-library/src/loading/json.rs:78`
- `json.encode` - `crates/typst-library/src/loading/json.rs:125`
- `read` - `crates/typst-library/src/loading/read.rs:24`
- `toml` - `crates/typst-library/src/loading/toml.rs:65`
- `toml.encode` - `crates/typst-library/src/loading/toml.rs:93`

### math
- `abs` - `crates/typst-library/src/math/lr.rs:112`
- `accent` - `crates/typst-library/src/math/accent.rs:31`
- `align-point` - `crates/typst-library/src/math/mod.rs:115`
- `attach` - `crates/typst-library/src/math/attach.rs:20`
- `bb` - `crates/typst-library/src/math/style.rs:156`
- `binom` - `crates/typst-library/src/math/frac.rs:107`
- `bold` - `crates/typst-library/src/math/style.rs:15`
- `cal` - `crates/typst-library/src/math/style.rs:79`

### model
- `bibliography` - `crates/typst-library/src/model/bibliography.rs:87`
- `caption` - `crates/typst-library/src/model/figure.rs:495`
- `cell` - `crates/typst-library/src/model/table.rs:735`
- `cite` - `crates/typst-library/src/model/cite.rs:46`
- `cite-group` - `crates/typst-library/src/model/cite.rs:155`
- `csl-indent` - `crates/typst-library/src/model/bibliography.rs:1184`
- `csl-light` - `crates/typst-library/src/model/bibliography.rs:1172`
- `direct-link` - `crates/typst-library/src/model/link.rs:377`

### text
- `highlight` - `crates/typst-library/src/text/deco.rs:215`
- `line` - `crates/typst-library/src/text/raw.rs:677`
- `linebreak` - `crates/typst-library/src/text/linebreak.rs:23`
- `lorem` - `crates/typst-library/src/text/lorem.rs:19`
- `lower` - `crates/typst-library/src/text/case.rs:13`
- `overline` - `crates/typst-library/src/text/deco.rs:82`
- `smallcaps` - `crates/typst-library/src/text/smallcaps.rs:44`
- `smartquote` - `crates/typst-library/src/text/smartquote.rs:33`

### visualize
- `circle` - `crates/typst-library/src/visualize/shape.rs:271`
- `close` - `crates/typst-library/src/visualize/curve.rs:365`
- `color` - `crates/typst-library/src/visualize/color.rs:194`
- `color.aqua` - `crates/typst-library/src/visualize/color.rs:224`
- `color.black` - `crates/typst-library/src/visualize/color.rs:218`
- `color.blue` - `crates/typst-library/src/visualize/color.rs:223`
- `color.cmyk` - `crates/typst-library/src/visualize/color.rs:548`
- `color.components` - `crates/typst-library/src/visualize/color.rs:726`

# Validation

## Reproduce the core checks

Run from the repository with Python 3.11+:

```sh
python -m py_compile skills/typst/scripts/docs.py skills/typst/scripts/refresh_catalog.py
python skills/typst/scripts/docs.py --help
python skills/typst/scripts/refresh_catalog.py --help
python skills/typst/scripts/docs.py status --check-latest
python skills/typst/scripts/docs.py search "selector.within" --json
python skills/typst/scripts/docs.py search "array.range:inclusive" --json
python skills/typst/scripts/docs.py show "table.cell:colspan"
python skills/typst/scripts/docs.py show "html.a:href"
python skills/typst/scripts/docs.py show "sym.alpha" --offline
python skills/typst/scripts/docs.py show "sym.Alpha" --offline
```

When the skill-creator validator is available, run `python <skill-creator>/scripts/quick_validate.py skills/typst`. It validates packaging/frontmatter, not behavior. Copy the complete skill to a different directory and repeat lookups from an unrelated working directory to test installation portability.

Use a fresh `--cache-dir` to exercise both the first network read and a repeated `show --offline`. A nonexistent API should fail explicitly; a bare ambiguous method name should request qualification rather than return the wrong member. Preserve case-sensitive symbols. A cached page advertising another release must be rejected. A missing section must not return its neighboring function.

For catalog maintenance, compare the official search item URLs with generated URLs, check unique names, inspect added constant/symbol/typed-HTML entries, and confirm that a failed refresh leaves the old output unchanged. `--help` must not fetch data or mutate output. See [maintenance](maintenance.md) for the release-update workflow.

## Verified on 2026-10-08–09

The compiler was the official **Typst 0.15.1 (9dfd3a08)** Windows release binary, verified against its published archive SHA-256. Tests used isolated local fixtures; no packages were downloaded or published.

| Area | Observed evidence |
| --- | --- |
| Authoring and math/data guides | 10 runnable entrypoints and 6 instrumented fixtures compiled without diagnostics; 20 semantic assertions passed; 5 representative renders inspected |
| Layout/CJK guide | 4 guide examples compiled; mixed-font punctuation, responsive grid widths, repeated table headers, 3-/5-page flows, and an oversized cell were rendered and inspected |
| Export/package guides | 24 compiler probes passed, including expected errors for unsupported flags, missing alternatives, PDF-profile conflicts, and project/package root escapes |
| Export artifacts | PDF text/metadata/tags/alt, PNG dimensions/transparency, SVG glyph outlines, native HTML MathML, and bundle files/cross-document links checked |
| Runtime lookup | Exact scoped/parameter names, case-sensitive Greek symbols, ambiguity, CLI error exits, offline misses, version mismatch, URL restrictions, and heading/code-block extraction checked |
| Symbol values | All 2,592 symbol values return an exact-value result, including 13 whitespace-valued symbols; named lookups preserve case |
| Independent debugging task | A two-page document with recursive heading styling and invalid contextual counter reads was repaired; headings, cross-references, and `Page N of 2` footers verified in the actual PDF |
| Independent Chinese report | A 52-record CSV became a two-page PDF; all 156 fields matched the source, headers repeated, page counters and equation numbering were verified, and the final render was inspected |

The independent debugging task exposed an invalid guide command: CLI `eval --in` does not supply an insertion location for `counter(page).final()`. The guide now uses queries over explicitly located headings and explains the boundary; the replacement command ran successfully.

Independent source/output review also corrected delimiter-sizing advice and qualified semantic preservation for HTML show rules. Runtime regressions cover truncated fixed-length and chunked HTTP responses, old partial caches, malformed JSON, case-sensitive glyph values, exact aliases, and code examples containing their own Markdown fences.

## What these checks do not establish

They do not prove all future Typst inputs work, every live-document entry exists in the release compiler, or every font/backend behaves identically on other machines. No external PDF/A or PDF/UA conformance validator or assistive-technology review was run. HTML DOM/math checks are not a full browser/accessibility review. `typst init` was source-reviewed; no registry template was installed to validate it. Evaluation-generated documents and machine-specific tools stay ignored and are not part of the installed skill.

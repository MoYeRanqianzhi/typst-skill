# Documentation and version boundaries

## Lookup without a source checkout

Only Python 3.11+ and this skill directory are needed for lookup; no third-party Python packages or sibling repositories are required. Resolve the script relative to `SKILL.md`, not the document's working directory.

```sh
python "<skill-dir>/scripts/docs.py" status
python "<skill-dir>/scripts/docs.py" status --check-latest
python "<skill-dir>/scripts/docs.py" search "selector.within" --json
python "<skill-dir>/scripts/docs.py" search "bibliography" --kind parameter
python "<skill-dir>/scripts/docs.py" show "figure.caption"
python "<skill-dir>/scripts/docs.py" show "table.cell:colspan"
python "<skill-dir>/scripts/docs.py" show "html.a:href"
python "<skill-dir>/scripts/docs.py" show "sym.arrow.r.squiggly" --offline
python "<skill-dir>/scripts/docs.py" search "sys.inputs"
python "<skill-dir>/scripts/docs.py" show "math.thin"
```

`search` returns names, kinds, and official URLs from the bundled location catalog. The snapshot contains 4,482 entries, including all 1,411 official search items, symbols, typed HTML, and 21 explicitly documented system/integer-limit/direction/alignment/math-spacing constants. Constant coverage is selective; several constants share a parent page and their runtime values are not stored. It does not extract Rust signatures, generate fictional signatures, or promise every compiler-internal definition is a public API. A missing result is not proof that an API does not exist: follow the corresponding official category or use the site's search.

Parameters use `callable:parameter`, scoped callables use `scope.member`, and nested parameters use `scope.member:parameter`. For example, `figure:caption` and `figure.caption` are different entries. Preserve symbol case: `sym.alpha` and `sym.Alpha` are different characters. Ambiguous names require an exact qualified name or one of the returned URLs; `show` does not silently select a similarly named function.

`show` extracts the requested section, including parameter descriptions, defaults, constraints, and code examples. It labels the URL, retrieval time, cache/live origin, and document version. JSON output additionally includes the source commits linked by the official page. Long sections announce truncation and a `--offset` for continuing; do not answer from a truncated signature or parameter discussion.

```sh
python "<skill-dir>/scripts/docs.py" show "text" --section parameters-font
python "<skill-dir>/scripts/docs.py" show "array" --max-chars 24000 --json
python "<skill-dir>/scripts/docs.py" show "array" --offset 24000 --json
```

## Offline and cache behavior

Search and symbol metadata work offline immediately. Full API descriptions require an initial HTTPS fetch, or a previously populated cache. Page caches live outside the skill and the user's document: `%LOCALAPPDATA%/typst-skill/docs` on Windows, otherwise `$XDG_CACHE_HOME/typst-skill/docs` or `~/.cache/typst-skill/docs`. Use `--cache-dir` for a project-controlled cache.

```sh
python "<skill-dir>/scripts/docs.py" show "table.cell" --cache-dir .cache/typst-docs
python "<skill-dir>/scripts/docs.py" show "table.cell" --cache-dir .cache/typst-docs --offline
python "<skill-dir>/scripts/docs.py" show "table.cell" --refresh
```

If no cached page exists, offline `show` fails explicitly; it does not invent the missing documentation. If the live page advertises a different release from the catalog, it fails before replacing the existing cache, so a previously fetched version-matched page remains usable offline. Read an available version-matched source or explain what cannot be confirmed. No command updates the user's compiler or installs packages.

## Stable release, live docs, development source

The baseline is **Typst 0.15.1**, latest stable when checked on **2026-10-09**, release commit `9dfd3a08500b7896045f907433cf7b4b02434fad`. The catalog records its retrieval date, release identity, and official-index hash. The official website is live and its linked source commit can differ even while advertising the same release. Its page version check is not a cryptographic guarantee of release-tag identity.

For release-critical behavior, reproduce it with that compiler or inspect the [v0.15.1 source](https://github.com/typst/typst/tree/v0.15.1). Do not infer a stable feature from an upstream `main` checkout merely because its manifest has the same version. For older projects, preserve their chosen compiler/package pins and consult the intervening changelogs; see [migration](migration.md).

The [Chinese blue book](https://github.com/typst-doc-cn/tutorial) supplies useful explanations and examples. Its observed dependency is 0.13.1; verify current syntax, arguments, and behavior against the target compiler. It is not bundled or needed at skill runtime.

## Source-level investigation

Use a release-matched checkout only when docs and a minimal compiler probe do not settle the issue, or when the task explicitly changes Typst itself:

| Area | Source location |
| --- | --- |
| Language syntax and evaluation | `crates/typst-syntax`, `crates/typst-eval` |
| Public definitions and API documentation | `crates/typst-library/src` |
| Macro expansion | `crates/typst-macros` |
| Styling/realization and paged layout | `crates/typst-realize`, `crates/typst-layout` |
| PDF, HTML, SVG, raster, bundle | The matching `crates/typst-*` exporter |
| CLI and host services | `crates/typst-cli`, `crates/typst-kit` |
| Official guide content and API reflection | `docs/content/**/*.typ`, `docs/src/reflect.rs` |
| Compiler regression tests | `tests/suite`, `cargo testit --help` |

The 0.15 docs generator is `cargo docit`, with website/PDF output; the former Markdown plus `groups.yml` structure no longer applies. Follow that checkout's `CONTRIBUTING.md` and `docs/README.md` for source work.

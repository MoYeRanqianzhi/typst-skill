# Debugging Typst

## Reproduce the actual build

Use the project's entry file and flags rather than compiling an included chapter by itself. Record the first error and its span; later errors may be consequences. Check the CLI version, root, font paths, `sys.inputs`, package pins, and chosen output target before changing document logic.

```sh
typst --version
typst compile --root . main.typ result.pdf --diagnostic-format short
typst fonts
typst eval 'range(0, 3, inclusive: true)'
typst eval --in main.typ 'query(heading).map(entry => (level: entry.level, body: entry.body))'
typst eval --in main.typ 'query(heading).map(entry => (body: entry.body, page: entry.location().page()))'
```

`eval` is a CLI subcommand in 0.15, distinct from the Typst language's `eval` function. `--in` makes the compiled document available for queries, but does not supply an insertion location for every contextual API: `counter(page).final()` still needs an in-document `context`. Query located elements as above, or emit labelled `metadata` from a context in a temporary diagnostic document and retrieve its value. For a legacy compiler, inspect `typst help query` instead of passing new CLI flags blindly. Typst 0.15.1 fixes the exit status for failing CLI evaluation; use exit codes and diagnostics together when validating earlier 0.15.0 installations.

## Choose the cause before the edit

| Symptom | What to inspect |
| --- | --- |
| Unexpected token or missing delimiter | Markup/code/math boundary; an extra `#` inside code; unmatched `[]`, `{}`, `()`; accidental markup in data |
| Unknown variable | Import scope, spelling, `.typ` entry point, package/compiler version; use `std.name` for a shadowed global |
| Unexpected argument or wrong type | The exact callable's official parameter section; named vs positional; content `[]` vs string vs array |
| Cannot access context | Move the read to where the value is consumed in `context`; do not wrap a top-level assignment and expect a number |
| State update has no visible effect | Ensure the update's returned content is inserted into the document; distinguish `get`, `at`, and `final` |
| Layout does not converge | Break a dependency where queried/generated content changes the same state, counter, or selection that controls its own existence |
| File not found / access denied | Paths relative to the source file, explicit project root, casing, forward slashes, package boundaries; see `path` in 0.15 |
| Font warning or missing glyph | Check the actual family name with `typst fonts`; supply a suitable fallback or font path; compare machines |
| Unexpected page count / overlap | Fixed heights, non-breakable blocks, placement outside flow, table row constraints, page header/footer space |
| Only HTML fails | Feature flags and export support; paged layout functions are not a browser layout model |

## Shrink without changing the failure

Keep the failing style rule, contextual read, or import boundary in a minimal reproduction. Replace unrelated data/assets with a small local fixture; retain the data shape and enough content to preserve pagination. Then fix that reproduction and apply the change back to the actual entry point.

For a context error:

```typst
#set heading(numbering: "1.")
= Introduction
#context [Current heading: #counter(heading).display()]
```

For delayed state, emit the update and read at a location:

```typst
#let total = state("total", 0)
#total.update(previous => previous + 3)
#context [Total here: #total.get()]
```

Do not repair pagination with arbitrary spacers until the flow constraint is understood. Recompile after the structural change and inspect the affected pages. Treat warnings about unsupported output features and non-convergence as unresolved behavior, even if an output file exists.

Sources: [context](https://typst.app/docs/reference/context/), [state](https://typst.app/docs/reference/introspection/state/), [CLI arguments at v0.15.1](https://github.com/typst/typst/blob/v0.15.1/crates/typst-cli/src/args.rs), [0.15.1 fixes](https://typst.app/docs/changelog/0.15.1/).

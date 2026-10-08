# Reusable modules, packages, and templates

Scope: Typst **0.15.1**, tag `v0.15.1`, commit `9dfd3a0`. Prefer the smallest reuse boundary that fits the task; packaging, downloading dependencies, and publishing are separate decisions.

## Choose the boundary

- **Within a project:** use local `.typ` modules. `import` exposes definitions; `include` inserts a file's evaluated content. No manifest, registry, or installation is needed.
- **Across projects:** a package adds a `typst.toml` manifest and a namespace/name/version identity. Published community imports use an exact version, for example `#import "@preview/cetz:0.4.1" as cetz`; that is a pin, not a claim that this version is newest. Follow the selected version's API and preserve existing pins unless an upgrade is requested.
- **A starter project:** a template package has both an importable library entrypoint and a `[template]` directory copied by `typst init`. A template function used through `show` does not by itself require a template package.

Uncached `@preview` imports and `typst init @preview/...` can download packages. Do not use them as an offline probe or treat a guide lookup as permission to install/publish. For local work, per-command `--package-path` avoids changing global configuration. See [modules and packages](https://typst.app/docs/reference/scripting/#modules) and the [official package repository](https://github.com/typst/packages#readme).

## Start with an ordinary module

`lib.typ`:

```typst
#let report(title: [Report], body) = {
  set text(lang: "en")
  heading(level: 1, title)
  body
}

#let load-note(source) = read(source).trim()
```

`main.typ`, with a UTF-8 `note.txt` beside it:

```typst
#import "lib.typ": report, load-note
#show: report.with(title: [Notes])

#load-note(path("note.txt"))
```

Keep document-wide styling inside the template function rather than expecting an imported module's top-level set rules to style its caller. Prefer explicit imports and parameters at the public boundary; do not make callers depend on private file layouts.

## Paths belong to their originating root

- A relative string resolves at the file-reading/importing call site, not the shell working directory and not necessarily the caller that originally supplied the string. Inside `load-note`, a plain string would resolve beside `lib.typ`.
- `/assets/logo.svg` means the current project/package root, not an OS filesystem root. The default project root is the main file's parent; `--root` changes it and must contain the main file. Keep it as narrow as the project requires.
- A package has its **own** root; its `/` does not refer to the consuming project. Package-owned assets should resolve inside the package.
- **The 0.15 `path` type carries its resolved root and location.** Construct `path("note.txt")` in the consumer and pass it to the package, as above. It continues to identify the consumer's file when `read`, `image`, or another loader uses it inside the package. Passing loaded data or `image(...)` content is another option when the package need not perform the loading itself.
- Neither strings nor constructed paths may escape their originating root with `..`. The new type does not add file-existence checks or directory enumeration; do not invent methods for those operations.

For a nested entrypoint, a typical invocation is `typst compile --root project project/chapters/main.typ result.pdf`. See the [path API](https://typst.app/docs/reference/foundations/path/) and its [release-pinned implementation](https://github.com/typst/typst/blob/v0.15.1/crates/typst-library/src/foundations/path.rs).

## Add a manifest only for a package

Minimal `typst.toml` for the library above:

```toml
[package]
name = "report-kit"
version = "0.1.0"
entrypoint = "lib.typ"
compiler = "0.15.1"
```

The compiler requires `name`, `version`, and `entrypoint`. `compiler` is an optional **minimum** compiler version, not a compiler lock. Match the imported name/version exactly; use a full `major.minor.patch` version without a `v` prefix. Paths in the library resolve within the package. Publication additionally requires metadata such as authors, a valid license expression, and description; do not invent a license or publish just to test reuse.

For a starter-project request, append:

```toml
[template]
path = "template"
entrypoint = "main.typ"
```

Here `[package].entrypoint` is relative to the package root; `[template].entrypoint` is relative to `template/`. The latter directory contains the files copied into the new project. Its `main.typ` normally imports the package by its pinned identity, not `../lib.typ`, which would stop working after copying. A template thumbnail, if supplied, is relative to the package root.

See the [manifest specification](https://github.com/typst/packages/blob/main/docs/manifest.md), [0.15.1 manifest parser](https://github.com/typst/typst/blob/v0.15.1/crates/typst-syntax/src/package.rs), and [template initialization implementation](https://github.com/typst/typst/blob/v0.15.1/crates/typst-cli/src/init.rs).

## External inputs are strings

Use `sys.inputs` for build-time values, not as a hidden file-root override. Parse and validate values at the consuming document's boundary, then pass ordinary parameters into reusable functions:

```typst
#let draft = sys.inputs.at("draft", default: "false") == "true"
#if draft [Draft]
```

```sh
typst compile --input draft=true main.typ report.pdf
```

Even `--input count=3` yields a string; convert with `int(...)` when a number is required. Here the draft switch is true only for the literal `"true"`. See [system inputs](https://typst.app/docs/reference/foundations/sys/).

## Test the public package boundary

For package work, direct `import "../lib.typ"` alone is insufficient: it misses the manifest and package-root isolation. An isolated fixture can use:

```text
packages/local/report-kit/0.1.0/typst.toml
packages/local/report-kit/0.1.0/lib.typ
consumer/main.typ
consumer/note.txt
```

Use the earlier consumer example with its import replaced by `#import "@local/report-kit:0.1.0": report, load-note`, then run from the fixture directory:

```sh
typst compile --package-path packages --root consumer consumer/main.typ result.pdf
```

`--package-path` points to the directory **containing namespaces**, not directly to the package. The local namespace does not trigger registry downloads. This is a command-local test fixture, not a global installation.

Check the public function's result, consumer-owned `path(...)` resources, package-owned resources, and any claimed export targets. For a template, compile its copied starter as a separate project. If distributing a package with `exclude` rules, test the intended distributed contents too: a loose local directory does not prove excluded runtime assets will survive publication. Use expected failures for root escapes or manifest mismatches when those boundaries are being changed; do not widen `--root` to hide a broken package design.

## Escalate beyond Typst only when needed

Prefer functions, content, and set/show rules for formatting. A Wasm plugin is useful for computation or existing non-Typst algorithms that justify the added build/runtime boundary, not ordinary templates. `plugin("engine.wasm")` loads a module whose exported functions accept byte buffers and return one byte buffer; wrap conversions in a Typst API. Plugins must follow Typst's protocol and behave purely. They do not gain filesystem/network access or a general WASI runtime; pass needed data explicitly. See the [plugin protocol and limitations](https://typst.app/docs/reference/foundations/plugin/).

Only for host/compiler integration, inspect [`World` and `Library`](https://github.com/typst/typst/blob/v0.15.1/crates/typst-library/src/lib.rs) and [`typst::compile<T>`](https://github.com/typst/typst/blob/v0.15.1/crates/typst/src/lib.rs): the host supplies sources/files/fonts and the library, then selects an output type and exporter. These are Rust integration entry points, not APIs a `.typ` package can call. Keep such work separate from an ordinary package/template request.

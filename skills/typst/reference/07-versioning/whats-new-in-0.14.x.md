# What's New in 0.14.x

## Baseline

- The current official local baseline is `Typst 0.14.2`.
- For plugin-related or security-sensitive work, recommend `0.14.2` rather than `0.14.0` or `0.14.1`.

## Release Dates

- `0.14.0` - October 24, 2025
- `0.14.1` - December 3, 2025
- `0.14.2` - December 12, 2025

## 0.14.2

- Security: updates the WebAssembly runtime used for plugins and fixes the `0.14.0` / `0.14.1` WASM memory-handling vulnerability.
- Diagnostics: adds a hint when `array.sorted` fails because elements are not comparable.

## 0.14.1

- Fixes a wide range of regressions across PDF, HTML, SVG, math, model, and text behavior.
- Fixes `array.sorted` overflow and invariant issues and updates the WASM runtime used by plugins.
- Adjusts command-line dependency-output edge cases.

## 0.14.0 Highlights

- tagged and accessible PDF by default
- PDF/UA-1 support and full PDF/A family support
- `pdf.artifact`
- typed HTML API such as `html.div`
- broader HTML export coverage
- `title`
- multiple table headers and subheaders
- `figure.alt`
- `math.equation.alt`
- `frac.style`
- `typst info`
- `typst completions`

## Upgrade Rules

- If a recipe, template, or answer was written against `0.11` to `0.13`, re-check it against the `0.14.x` changelog before reusing it.
- If the task touches accessibility, HTML, PDF standards, plugins, or CLI behavior, explicitly call out the `0.14.x` baseline.
- When version ambiguity exists, cite the relevant `0.14.0`, `0.14.1`, or `0.14.2` changelog file directly.

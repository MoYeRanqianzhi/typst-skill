# Export and Platform

## Use

- Summarize PDF, HTML, SVG, and PNG backend behavior, output constraints, and platform-sensitive decisions.

## Authoritative Sources

- `typst/docs/reference/export/pdf.md`
- `typst/docs/reference/export/html.md`
- `typst/docs/reference/export/svg.md`
- `typst/docs/reference/export/png.md`
- `typst/docs/guides/accessibility.md`
- `typst/docs/changelog/0.14.0.md`
- `typst/docs/changelog/0.14.1.md`
- `typst/docs/changelog/0.14.2.md`

## Backend Baselines

- PDF is the most feature-complete publication backend and, in `0.14.x`, emits tagged PDFs by default.
- HTML is semantic and backend-specific; it should not be treated as a paged PDF clone.
- SVG and PNG are page-image exports and have multi-page filename-template requirements.
- Plugin-sensitive work should prefer `Typst 0.14.2` because `0.14.0` and `0.14.1` carried a WASM runtime vulnerability fixed in `0.14.2`.

## PDF Notes

- `0.14.0` added broad PDF/A support.
- `0.14.0` added `pdf.artifact` and experimental table accessibility extras under `a11y-extras`.
- PDF/UA and PDF/A solve different problems; choose them intentionally.

## HTML Notes

- `0.14.0` greatly expanded built-in element coverage and added the typed HTML API.
- `0.14.1` changed a `page` set rule in HTML export from a hard error to a warning.
- Keep HTML-specific structure behind backend-aware templates or `target()` checks.

## Platform and Reproducibility Rules

- Fonts, package paths, and root configuration are part of the platform contract.
- Backend-specific work should be validated with the exact target backend, not only with one default PDF run.
- If a document must target multiple backends, reduce page-only assumptions early.

## Related Recipe

- Accessibility and HTML-specific guidance lives in `../05-recipes/accessibility-and-html.md`.

# Export and Platform

## Use

- Summarize PDF, HTML, SVG, and PNG backend behavior, constraints, and decision points.

## Authoritative Sources

- `typst/docs/reference/export/pdf.md`
- `typst/docs/reference/export/html.md`
- `typst/docs/reference/export/svg.md`
- `typst/docs/reference/export/png.md`
- `typst/docs/guides/accessibility.md`
- `typst/docs/changelog/0.14.0.md`
- `typst/docs/changelog/0.14.2.md`

## Key Takeaways

- `0.14.0` significantly expanded PDF export and made tagged PDF part of the baseline.
- `0.14.0` added broad PDF/A support and `pdf.artifact`.
- `0.14.0` greatly expanded HTML export and introduced the typed HTML API.
- `0.14.2` is the recommended 0.14.x baseline for plugin-related work because it fixes the 0.14.0 and 0.14.1 WASM runtime security issue.

## Design Rules

- Accessibility-sensitive PDF work should be checked against the Accessibility Guide and the PDF export reference.
- HTML should be treated as a semantic backend, not as a guaranteed page-faithful clone of paged PDF output.
- Backend-specific behavior belongs in backend-aware templates, rules, or recipes rather than scattered ad hoc patches.

## Also See

- Accessibility and HTML recipe: `../05-recipes/accessibility-and-html.md`

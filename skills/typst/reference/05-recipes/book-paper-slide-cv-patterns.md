# Book, Paper, Slide, and CV Patterns

## Use

- Provide reusable high-level document patterns grounded in the local blue-book templates and official template workflow.

## Authoritative Sources

- `typst/docs/tutorial/4-template.md`
- `The Raindrop-Blue Book/src/template/book.typ`
- `The Raindrop-Blue Book/src/template/paper.typ`
- `The Raindrop-Blue Book/src/template/slides.typ`
- `The Raindrop-Blue Book/src/topics/template-book.typ`
- `The Raindrop-Blue Book/src/topics/template-paper.typ`
- `The Raindrop-Blue Book/src/topics/template-cv.typ`

## Pattern Matrix

- Book: stable page setup, chapter-level heading structure, outline, running heads, and bibliography strategy.
- Paper: title metadata, author block, abstract, figures/tables, bibliography, and compact template-scoped styling.
- Slides: explicit aspect ratio and page style, minimal paged assumptions, and strong separation between content and theme.
- CV: compact reusable section blocks, predictable spacing, font locking, and graceful fallback when iconography or external assets are unavailable.

## Design Rules

- Put document-wide defaults in a template function instead of scattering `set` and `show` rules through the body.
- Keep content parameters semantic: `title`, `authors`, `date`, `abstract`, `lang`, `theme`, and so on.
- Avoid hard-coding one user's local fonts or package paths into a template.
- If a design must work for both PDF and HTML, isolate backend-specific behavior early.

## Validation Checklist

1. Render a minimal sample document for the pattern.
2. Verify headings, references, figures, and bibliography still behave under the template.
3. Re-test fonts and page setup on the target machine.
4. For slide or HTML-adjacent workflows, verify backend-specific assumptions explicitly.

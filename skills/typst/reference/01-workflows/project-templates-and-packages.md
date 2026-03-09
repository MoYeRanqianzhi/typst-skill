# Project, Templates, and Packages

## Use

- Handle project structure, reusable templates, package imports, and template-based project bootstrap.

## Authoritative Sources

- `typst/crates/typst-cli/src/args.rs`
- `typst/docs/tutorial/4-template.md`
- `typst/docs/tutorial/3-advanced.md`
- `typst/docs/guides/guide-for-latex-users.md`
- `The Raindrop-Blue Book/src/template/*.typ`
- `The Raindrop-Blue Book/src/topics/template-*.typ`

## Recommended Project Layout

- Keep one explicit entry file such as `main.typ` or `paper.typ`.
- Put reusable theme or template logic in separate files and import them.
- Keep static assets and data files inside the project root or a clearly chosen root passed through `--root`.
- Add a stable local font directory when typography reproducibility matters.

## Template Design Rules

- In Typst, a template is usually a function that accepts `doc` and optional metadata parameters.
- Apply document-wide `set` and `show` rules inside the template, then pass the body through once.
- Keep content parameters semantic, such as `title`, `authors`, `abstract`, or `lang`, instead of overfitting to one document.
- Split visual theme logic from content structure so the same template can serve multiple outputs.

## Package and Import Guidance

- Use file imports for project-local reusable code.
- Use package imports when the dependency should be versioned and reused across projects.
- Pin package versions explicitly when reproducibility matters.
- Keep local package mirrors or package-path overrides stable in CI or offline environments.

## `typst init`

- `typst init <template>` bootstraps a new project from a local or published template.
- Published templates can be referenced like `@preview/charged-ieee` and optionally version-pinned as `@preview/charged-ieee:0.1.0`.
- The output directory defaults to the template name if no explicit directory is supplied.

## Validation Workflow

1. Render a minimal sample document with the template.
2. Confirm imports, fonts, and package resolution under the intended root.
3. Check that heading, bibliography, figure, and table behavior still works under the template.
4. If the template must support HTML too, validate backend-aware behavior before publishing it.

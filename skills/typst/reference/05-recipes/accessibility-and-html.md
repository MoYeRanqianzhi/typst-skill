# Accessibility and HTML

## Use

- Handle accessibility-sensitive Typst work and HTML-specific output decisions.
- Use this recipe when the task involves tagged PDF, PDF/UA, PDF/A, alt text, artifacts, or HTML-targeted templates and show rules.

## Authoritative Sources

- `typst/docs/guides/accessibility.md`
- `typst/docs/reference/export/pdf.md`
- `typst/docs/reference/export/html.md`
- `typst/docs/reference/library/model.md`
- `typst/docs/reference/library/math.md`
- `typst/docs/changelog/0.14.0.md`

## Core Rules

- Prefer semantic Typst markup over purely visual styling. A real `heading`, `figure`, `table`, or `equation` is more accessible than text manually styled to look similar.
- In `Typst 0.14.x`, PDF output is tagged by default. Treat this as a baseline, not as a guarantee that the document is fully accessible without author work.
- HTML and PDF have different goals. Do not assume a paged PDF-oriented layout automatically turns into good semantic HTML.
- If content is meaningful, give it a textual representation. If it is purely decorative, mark it as an artifact or keep it out of the semantic layer.

## Tagged PDF, PDF/UA, and PDF/A

- Tagged PDF is the default accessibility baseline in modern Typst PDF export.
- Choose **PDF/UA-1** when the task explicitly prioritizes accessibility compliance and stronger automatic checks.
- Choose a **PDF/A** profile when archival constraints matter. If accessibility also matters, prefer an accessible `a` conformance level where possible.
- Do not conflate PDF/A with PDF/UA:
  - PDF/UA focuses on accessibility.
  - PDF/A focuses on archival constraints.
  - Some profiles can be used together conceptually, but the exact choice depends on the delivery requirement.
- If the user asks for an exact archival/accessibility target, consult `typst/docs/reference/export/pdf.md` before deciding the profile.

## Alternative Text

- Use `figure.alt` when the figure's full meaning needs to be announced as text by Assistive Technology.
- Do not add `figure.alt` mechanically to every figure. If the body is already accessible and should still be read, an unnecessary alt can hide useful structure.
- Use `math.equation.alt` for equations whose meaning would otherwise be unclear or lossy to AT users.
- For both figure and equation alt text:
  - describe meaning, not just appearance
  - be concise but sufficient
  - avoid duplicating nearby caption text unless the caption alone is enough

## `pdf.artifact`

- Use `pdf.artifact` for purely decorative or layout-only content.
- Typical candidates:
  - decorative backgrounds
  - ornaments
  - purely cosmetic overlays
  - manual visual embellishments that should not be announced
- Once content is inside an artifact, it cannot become semantic again. If you need decorative and semantic layers together, separate them structurally and stack them with layout tools such as `place`.
- Shapes and paths are often treated as artifacts automatically, but their inner content may still be meaningful. Wrap semantically meaningful graphics in `figure` and provide textual support when needed.

## Typed HTML API

- `Typst 0.14.x` adds a typed HTML API, for example `html.div`, on top of raw `html.elem`.
- Prefer typed HTML helpers when generating HTML-specific structure because they encode attributes more explicitly and are easier to reason about than raw element strings.
- Use HTML-specific logic behind `target()` checks, templates, or show rules so that document content can stay largely backend-agnostic.
- Keep HTML-specific structure focused on semantics first. Styling can be handled separately by downstream CSS.

## HTML Backend Notes

- The local official docs still describe HTML export as experimental and feature-gated. Do not present it as a mature, production-safe replacement for PDF without checking the exact requirement.
- HTML export aims for semantic structure, not a perfect reproduction of paged layout.
- Good candidates for HTML-specific handling:
  - navigation structure
  - semantic wrappers
  - metadata
  - media elements and typed HTML nodes
- Common pitfalls:
  - assuming page headers/footers make sense in HTML
  - assuming absolute placement survives meaningfully
  - assuming every PDF-oriented spacing trick should be preserved in HTML

## Practical Workflow

1. Identify the target: PDF, HTML, or both.
2. If PDF accessibility matters, review semantic structure first, then alt text, then artifacts.
3. If exact compliance is requested, open `typst/docs/reference/export/pdf.md` and choose the profile intentionally.
4. If HTML is a first-class target, review `typst/docs/reference/export/html.md` and decide where `target()` or typed HTML helpers are needed.
5. Re-check figures, equations, tables, and decorative layout elements before finalizing output.

## When to Open Official Export Docs

Open `typst/docs/reference/export/pdf.md` when you need:

- an exact PDF/UA or PDF/A recommendation
- PDF version constraints
- attachment and archival behavior
- backend-specific accessibility details

Open `typst/docs/reference/export/html.md` when you need:

- feature-flag and CLI export details
- current HTML backend limitations
- typed HTML behavior and HTML-specific output design
- guidance on using `target()` and backend-aware document generation

# Visualize

## Use

- Handle color, stroke, gradients, tilings, geometric shapes, images, and decorative graphics.

## Authoritative Sources

- `typst/docs/reference/library/visualize.md`
- `typst/crates/typst-library/src/visualize/**`
- `typst/docs/changelog/0.14.0.md`
- `typst/docs/guides/accessibility.md`

## Main API Families

- Color and paint: `color`, `stroke`, `gradient`, `tiling`.
- Shapes and paths: `rect`, `square`, `ellipse`, `circle`, `polygon`, `curve`, `line`.
- Images: `image`, `image.decode`.
- Color transforms: `lighten`, `darken`, `saturate`, `desaturate`, `mix`, `transparentize`, `opacify`, `rotate`.

## High-Value `0.14.x` Notes

- `0.14.0` added support for using PDFs as images.
- `0.14.0` added WebP support.
- Decorative graphics should often be artifacts in PDF or paired with textual support when they carry meaning.

## Design Rules

- Keep meaningful graphics semantic when possible, for example by wrapping them in `figure` and providing captions or alt text.
- Treat purely decorative layers as artifacts in accessibility-sensitive PDF work.
- Prefer stable geometry and styling primitives over backend-specific image hacks.
- External drawing packages may be useful, but they are not part of the core library contract.

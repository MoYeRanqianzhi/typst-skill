# Blue Book Gaps and Staleness

## Use

- Explain why the blue book is a secondary source and how to use it safely against the official `0.14.2` baseline.

## Evidence in the Local Snapshot

- `The Raindrop-Blue Book/README.md` still points to `typst-docs-v0.11.0.json`.
- `The Raindrop-Blue Book/Cargo.toml` still declares `typst = "0.13.1"`.
- `The Raindrop-Blue Book/src/tutorial/stateful-v0.12.0/` preserves historical `0.12.0` stateful material.

## Practical Consequences

- Do not treat blue-book API claims as authoritative without checking the official Typst source or docs.
- Expect drift in CLI behavior, package workflow, HTML export, accessibility features, and newer `0.14.x` additions.
- Continue using the blue book for Chinese explanations, recipes, and template patterns where those remain useful.

## Safe Usage Rules

- Verify exact API names and signatures against the generated indexes or raw official source.
- Verify version-sensitive workflows against `typst/docs/changelog/0.14.0.md`, `0.14.1.md`, and `0.14.2.md`.
- If the blue book and official docs disagree, follow the official docs and explicitly note the drift.

## Typical Drift Areas

- CLI subcommands and arguments
- package and template ecosystem guidance
- typed HTML API and export details
- accessibility features such as tagged PDF, `figure.alt`, `math.equation.alt`, and `pdf.artifact`

# Typst Skill

[中文说明](README.zh-CN.md)

A Typst skill for agents that write, improve, debug, and migrate real documents. Verified against **Typst 0.15.1**, the latest stable release checked on **2026-10-09**.

The skill starts with the user's document and output requirements. It provides a short entrypoint, focused task guides, and one official-documentation lookup tool. It asks for actual compilation and relevant visual/output checks, not an assertion that code looks correct.

## What it supports

- Document authoring, reusable components, context/state/counters, and debugging.
- Mathematics, data-driven tables, citations, Chinese typography, and long-page layouts.
- Packages and templates, PDF/PNG/SVG, experimental HTML and bundle export, and migration to 0.15.
- Offline discovery of official API pages, parameters, scoped members, symbols, and typed HTML; full official sections fetched on demand and cached with provenance.

The catalog is a location index, not a copied manual or a guessed signature database. Full API text needs network access on first use; cached sections and symbol metadata can be read offline. The tool detects advertised documentation-version drift. Release-critical details still need the matching compiler or release-tag source.

## Install

```sh
npx skills add MoYeRanqianzhi/typst-skill@typst -g -y
```

Or copy the complete `skills/typst/` directory into your agent's skill directory. Installing only `SKILL.md` leaves its references and tools missing. See [installation](docs/INSTALL.md).

For example, ask:

> Use $typst to turn this CSV into a Chinese report with a repeated table header, a numbered equation, and a PDF. Preserve the existing project styling and verify the result.

## Documentation lookup

From this repository:

```sh
python skills/typst/scripts/docs.py search "table.cell"
python skills/typst/scripts/docs.py show "table.cell:colspan"
python skills/typst/scripts/docs.py show "sym.arrow.r.squiggly" --offline
python skills/typst/scripts/docs.py status --check-latest
```

The same scripts work from another directory or a standalone skill installation. `figure.caption` identifies a scoped function; `figure:caption` identifies a parameter. The colon is catalog notation, not Typst syntax. See [lookup and version boundaries](skills/typst/references/docs-and-versions.md).

## Requirements

- Python **3.11+**, standard library only, for lookup and catalog maintenance.
- Typst CLI for compilation; guides and examples target **0.15.1**. Existing projects may stay on their chosen version.
- Suitable fonts for the document's scripts; fonts and the compiler are not installed by the skill.

No Typst source checkout, blue-book checkout, Cargo toolchain, or PyYAML is required to use the skill. Contributors can consult [design and maintenance](docs/maintenance.md), [validation](docs/validation.md), and [known limitations](docs/known-issues.md).

## License

Project code and original guidance: MIT. The catalog records names, symbols, and locations from official Typst documentation with source provenance; linked or fetched upstream documentation retains its upstream licensing.

# Data Loading

## Use

- Handle external file reads, structured data parsing, encoding helpers, and CLI input bridging.

## Authoritative Sources

- `typst/docs/reference/library/data-loading.md`
- `typst/crates/typst-library/src/loading/**`
- `typst/crates/typst-cli/src/args.rs`

## Coverage Map

- File reads: `read`
- Structured formats: `json`, `csv`, `yaml`, `xml`, `toml`, `cbor`
- Encoding helpers: `json.encode`, `toml.encode`, `yaml.encode`, `cbor.encode`
- CLI bridge: `sys.inputs`

## Guidance

- Small configuration knobs fit well in `sys.inputs` because they are easy to override from the CLI.
- Reusable structured data belongs in external JSON, YAML, CSV, XML, or TOML files under a stable root.
- `cbor.encode` and related helpers are mainly useful when bridging structured data to plugins.
- Round trips across Typst values and external encodings can be lossy; confirm format-specific behavior before assuming full fidelity.
- When a build becomes non-reproducible, verify root, relative paths, and input wiring before changing document code.

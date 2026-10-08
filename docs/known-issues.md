# Known limitations

- The bundled catalog is an official-documentation **locator**, not a complete offline manual. Full API descriptions need network access once per page or a pre-populated cache; offline failures are explicit.
- Official web documentation can change independently of a compiler release. The catalog records the observed source commit(s) separately from the release commit. The reader checks the advertised document version, but only release-tag source and compiler probes settle exact release behavior.
- HTML structure and official search metadata are upstream interfaces. A missing heading or version mismatch causes a lookup/refresh failure rather than silent fallback. See [maintenance](maintenance.md) when upstream changes these interfaces.
- Natural-language lookup uses names, titles, and aliases, not semantic embeddings or translation. For Chinese questions, use the relevant guide and the corresponding Typst identifier/English term. A search miss does not prove an API is absent.
- The guide baseline is 0.15.1; earlier projects need version-specific checks. Experimental HTML, bundle, and accessibility extras can change separately from ordinary PDF workflows.
- Compiling does not prove page layout, accessible reading order, PDF conformance, or equivalent HTML presentation. Font availability also affects rendering. Verify what the requested deliverable actually needs.

See [validation](validation.md) for concrete evidence and the checks not performed.

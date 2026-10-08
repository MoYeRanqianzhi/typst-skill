---
name: reference-provenance
description: Recall when refreshing the Typst baseline, changing API lookup, or evaluating coverage claims.
metadata:
  type: project
  scope: Typst skill documentation and catalog maintenance
  status: active
  last_verified: 2026-10-09
---

The compiler release and live official documentation are separate sources of evidence. Their commits can differ even when they advertise the same version. The catalog is a portable location index; it is not a release-exact API implementation or an offline copy of the manual.

**Why:** The previous source parsers depended on a local checkout, inferred incomplete API names, and failed when upstream documentation moved from Markdown/YAML to Typst. A source checkout without its own Git metadata also caused the old generators to report the parent project's commit as upstream provenance.

**How to apply:** Keep official location discovery separate from reading full API text and from proving compiler behavior. Use the release compiler or release-tag source for version-critical claims. Preserve explicit offline misses, ambiguity, and version mismatches. Prefer one portable official locator over parallel inferred indexes unless new upstream evidence justifies another design.

**Evidence:** [Maintenance design](../../docs/maintenance.md), [catalog provenance](../../skills/typst/references/catalog.json), and [validation evidence](../../docs/validation.md). On 2026-10-08, the v0.15.1 compiler/tag resolved to `9dfd3a08500b7896045f907433cf7b4b02434fad`, while official HTML linked source commit `d101c2f507acd2e680a187735c5c201094e00077`.

**Recheck when:** A new release, official search/HTML schema change, or a move to a release-pinned documentation artifact changes these boundaries.

# Typst Skill

> **Typst version covered: `0.14.2`**

A source-grounded [Typst](https://typst.app) expert skill for AI agents, providing layered reference docs, API query tools, and a standard routing workflow.

## Features

- **Smart Routing** — Automatically navigates to the most relevant reference doc based on task type (create / debug / explain / template)
- **33 Layered Reference Docs** — Covering workflows, language core, standard library, recipes, and versioning — all with runnable code examples
- **Dual Index Query System** — `query_reference.py` (broad: API + docs + blue-book + grep) and `query_api_index.py` (fast official index)
- **Chinese Typesetting Support** — Font configuration, CJK mixed-script, quote-trap warnings, punctuation rules, powered by the Raindrop Blue Book
- **Progressive Disclosure** — L1 description (~30 words) → L2 SKILL.md (97 lines) → L3 on-demand reference docs and scripts

## Quick Start

### Install

```bash
npx skills add MoYeRanqianzhi/typst-skill@typst -g -y
```

> For more installation methods (manual install, no-npx environments, etc.), see [docs/INSTALL.md](docs/INSTALL.md)

### Give This to Any AI Agent

Copy the following line and send it to your AI agent to install automatically:

```
Install the Typst skill by following the instructions at: https://raw.githubusercontent.com/MoYeRanqianzhi/typst-skill/main/docs/INSTALL.md
```

### Verify

After installation, ask your agent:

```
Write a minimal Typst document with a title and paragraph.
```

If the skill is loaded correctly, the agent will route through SKILL.md, reference the appropriate docs, and produce compilable Typst code.

## Directory Structure

```
skills/typst/
├── SKILL.md                       # Core SOP — routing, workflow, authority
├── scripts/                       # Deterministic query tools
│   ├── query_reference.py         # Broad cross-source lookup (API + docs + blue-book + grep)
│   ├── query_api_index.py         # Fast official API index query
│   ├── build_reference.py         # Build comprehensive reference DB
│   └── refresh_typst_knowledge.py # Refresh API index from source
└── reference/                     # 33 layered reference docs
    ├── 01-workflows/              # Compile, debug, publish, templates
    ├── 02-language/               # Markup, styling, scripting, math
    ├── 03-library/                # Layout, text, model, visualize, etc.
    ├── 05-recipes/                # CV, paper, slides, Chinese typesetting
    ├── 07-versioning/             # What's new, blue-book gaps
    └── 08-generated/              # Auto-generated API index
```

## How It Works

```
User request → SKILL.md route table → smallest matching reference → query_reference.py → runnable code
```

**Authority hierarchy**: Official source > Generated indexes > Blue Book

**Routing flow**:
1. Quick intent check — create / explain / fix / modify
2. Error triage — syntax / type / font / state / layout / version
3. Subsystem routes — precise per-subsystem navigation
4. Creating from scratch — quick-start path

## Test Results

End-to-end test using a "Cute Cat Resume":

| Dimension | v0.3.0 | v0.4.0 | Delta |
|-----------|:------:|:------:|:-----:|
| Routing | 4/5 | 5/5 | +1 |
| Reference Docs | 3/5 | 4.7/5 | +1.7 |
| Query Tools | 4/5 | 4/5 | — |
| Writing Experience | 4/5 | 4.8/5 | +0.8 |
| **Overall** | **3.75** | **4.6** | **+0.85** |

## Dependencies

- **Python 3.10+** — Required for query scripts
- **Typst CLI** — Required for compiling `.typ` files ([install](https://github.com/typst/typst/releases))
- **PyYAML** — Required by `refresh_typst_knowledge.py` (`pip install pyyaml`)

## License

MIT

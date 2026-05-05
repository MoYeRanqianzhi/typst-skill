# Installing the Typst Skill

This document describes how to install the `typst` skill for AI agents. Follow the section that matches your environment.

## Skill Source

- **Repository**: `https://github.com/MoYeRanqianzhi/typst-skill.git`
- **Skill path inside repo**: `skills/typst/`
- **Spec**: [agentskills.io/specification](https://agentskills.io/specification)

---

## Option A: Install via `npx skills` (Recommended)

If you have Node.js (v18+) installed:

```bash
npx skills add MoYeRanqianzhi/typst-skill@typst -g -y
```

This installs the skill globally. To verify:

```bash
npx skills list
```

You should see `typst` in the output.

### Update

```bash
npx skills update
```

---

## Option B: Install via `npx skills` (Non-Global)

To install into the current project only (not globally):

```bash
npx skills add MoYeRanqianzhi/typst-skill@typst
```

The skill will be available only in the current working directory.

---

## Option C: Manual Install (No npx / No Node.js)

### For Claude Code

1. Clone the repository:
   ```bash
   git clone https://github.com/MoYeRanqianzhi/typst-skill.git
   ```

2. Copy the skill directory to your Claude Code skills path:
   ```bash
   # Linux / macOS
   cp -r typst-skill/skills/typst ~/.claude/skills/typst

   # Windows (PowerShell)
   Copy-Item -Recurse typst-skill\skills\typst $env:USERPROFILE\.claude\skills\typst
   ```

3. Verify the skill is loaded by starting Claude Code and checking the skill list.

### For Codex / Other Agents

1. Clone the repository (same as above).

2. Copy the skill directory to your agent's skills path:
   ```bash
   # Codex default path
   cp -r typst-skill/skills/typst ~/.agents/skills/typst
   ```

3. Alternatively, symlink the skill:
   ```bash
   ln -s /absolute/path/to/typst-skill/skills/typst ~/.agents/skills/typst
   ```

---

## Option D: Manual Install (Minimal — SKILL.md Only)

If you only want the core skill without scripts or reference data:

1. Download `SKILL.md`:
   ```bash
   curl -o SKILL.md https://raw.githubusercontent.com/MoYeRanqianzhi/typst-skill/main/skills/typst/SKILL.md
   ```

2. Place it in your agent's skills directory:
   ```bash
   mkdir -p ~/.claude/skills/typst
   mv SKILL.md ~/.claude/skills/typst/
   ```

> **Note**: Without the `reference/` and `scripts/` directories, the skill will have limited functionality — no bundled API index, no query tools, and no code examples in references.

---

## Dependencies

- **Python 3.10+** — Required for query scripts (`query_reference.py`, `query_api_index.py`)
- **PyYAML** — Required by `refresh_typst_knowledge.py` (`pip install pyyaml`)
- **Typst CLI** — Required for compiling `.typ` files (`typst compile`)
  - Install: https://github.com/typst/typst/releases
  - The skill targets Typst **0.14.2** but is backward-compatible with **0.13.x**

---

## Verify Installation

After installation, ask your agent:

```
Write a minimal Typst document with a title and paragraph.
```

If the skill is loaded correctly, the agent should:
1. Route through SKILL.md's Quick intent check
2. Reference `book-paper-slide-cv-patterns.md` or `markup-and-document-structure.md`
3. Produce runnable Typst code

---

## Directory Structure

```
skills/typst/
├── SKILL.md                          # Core SOP — routing, workflow, authority
├── scripts/
│   ├── query_reference.py            # Broad cross-source API lookup
│   ├── query_api_index.py            # Fast official API index query
│   ├── build_reference.py            # Build comprehensive reference DB
│   └── refresh_typst_knowledge.py    # Refresh API index from source
└── reference/
    ├── 00-index.md                   # Master routing index
    ├── 01-workflows/                 # Compile, debug, publish, templates
    ├── 02-language/                  # Markup, styling, scripting, math
    ├── 03-library/                   # Layout, text, model, visualize, etc.
    ├── 04-modules/                   # std, calc, sys, sym, emoji
    ├── 05-recipes/                   # CV, paper, slides, Chinese typesetting
    ├── 06-dev/                       # Architecture, CLI, testing
    ├── 07-versioning/                # What's new, blue-book gaps
    ├── 08-generated/                 # Auto-generated API index + snapshot
    └── generated/                    # Broad cross-source reference DB
```

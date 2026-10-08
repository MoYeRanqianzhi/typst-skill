# Installing the Typst skill

Install the **complete** `skills/typst/` directory from [MoYeRanqianzhi/typst-skill](https://github.com/MoYeRanqianzhi/typst-skill). It contains the entrypoint, references, bundled catalog, and scripts. Sibling source checkouts and repository maintenance records are not runtime dependencies.

## Skill manager

```sh
npx skills add MoYeRanqianzhi/typst-skill@typst -g -y
```

Omit `-g` for a project-local installation supported by the manager. Choose the agent targets and installation scope you intend to change.

## Manual installation

Clone the repository and copy `skills/typst/` into the skill directory configured for your agent. For example, if your agent uses `~/.agents/skills`:

```sh
git clone https://github.com/MoYeRanqianzhi/typst-skill.git
mkdir -p ~/.agents/skills
cp -R typst-skill/skills/typst ~/.agents/skills/typst
```

PowerShell equivalent, with the target chosen for your agent:

```powershell
$skillTarget = Join-Path $env:USERPROFILE '.agents/skills'
New-Item -ItemType Directory -Path $skillTarget -Force
Copy-Item -Recurse -LiteralPath 'typst-skill/skills/typst' -Destination $skillTarget
```

If that destination already contains a customized skill, review it before replacing it. During updates, replace the old skill as a directory instead of merging obsolete `reference/` files and retired scripts into the new installation. Keep personal backups outside the installed skill directory so agents do not discover stale instructions.

## Dependencies

Python **3.11+** runs both scripts without third-party packages. A Typst CLI is needed only for compilation and evaluation, not for offline catalog search. Obtain the compiler from the [official releases](https://github.com/typst/typst/releases) using the installation method appropriate to your environment.

This skill's verified baseline is **Typst 0.15.1**. Check `typst --version`; no blanket compatibility with 0.13/0.14 is implied. Keep an existing project's compiler version unless a change is intended. Provide suitable fonts for CJK or other scripts.

## Verify the installed copy

Replace `<installed-typst>` with the copied skill directory:

```sh
python "<installed-typst>/scripts/docs.py" status
python "<installed-typst>/scripts/docs.py" search "selector.within"
python "<installed-typst>/scripts/docs.py" show "sym.arrow.r.squiggly" --offline
python "<installed-typst>/scripts/docs.py" show "table.cell:colspan"
```

The first three commands need no network. The last retrieves an official page if it is not cached, then checks its version and extracts the exact parameter. The cache is outside the skill; see [cache behavior](../skills/typst/references/docs-and-versions.md#offline-and-cache-behavior).

Then ask the agent to use `$typst` for a small document. Confirm it follows the relevant guide, compiles when a CLI is available, and states any unavailable verification rather than claiming success. Automatic invocation is enabled; the skill can also be requested explicitly.

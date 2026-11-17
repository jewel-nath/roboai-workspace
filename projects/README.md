# Projects

Your own robots live here. **Each project is its own git repo**; the workspace ignores everything
in this folder except this file.

```
projects/
├── README.md            ← this file (tracked by the workspace)
├── orbibot/             ← its own repo
│   ├── PROJECT.md       ← the card: goal, stage, stack, wiki pages and skills used, open questions
│   ├── CLAUDE.md        ← project rules; points at ../../AGENTS.md
│   ├── .claude/skills/  ← skills only this project needs
│   └── docs/ cad/ pcb/ firmware/ ros2_ws/ sim/ videos/
└── nexbot/              ← same shape, its own repo
```

## Start a project

In Claude Code, run `/new-project <name> [what it is for]`. By hand, or in another agent:

1. Copy [templates/project/](../templates/project/) to `projects/<name>/`.
2. Fill in `PROJECT.md`.
3. Run `git init` inside `projects/<name>/`, and add its remote.

## Bring in an existing repo

Push everything in the old folder, then clone it fresh into `projects/<name>/` and check it works
before archiving the old folder. Moving the folder instead breaks paths stored by git worktrees.

## Where a change is committed

| Change | Repo |
|---|---|
| The project's CAD, BOM, plans, firmware, decisions, video sources | the project's repo |
| A general lesson: a tool trap, a part finding, robot research, a new MCP server | the workspace |
| Machine-specific config | nowhere (gitignored) |

Before committing, check which repo each changed file belongs to. A general lesson found in a
project is promoted to the wiki with the project's names removed (`/promote`).

Open the **workspace root** to work: workspace skills, wiki and MCP servers are then all loaded, and
the project's own `CLAUDE.md` loads when you work on its files.

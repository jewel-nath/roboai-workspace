# RoboAI Workspace

> **The open-source LLM Wiki for robotics.**

Every robotics developer re-researches the same things: which open robot to copy, what it costs,
which motor, which MCU, which simulator. RoboAI Workspace does that research once, carefully, in a
form AI agents can read, and pairs it with the skills and tool setups that let an agent help you
build your own robot: planning, mechanical design, electronics, firmware, ROS 2, simulation, robot
learning, and the videos that explain it.

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)

## Status

**Being redesigned (November 2026).** The structure, templates, source registry, scripts and
commands are done (Phases 0 and 1). The [Robot Atlas](wiki/robots/README.md) has its first 17
profiles (Phase 3, in progress). Content arrives phase by phase; the
[roadmap](docs/plan.md#12-roadmap) says in what order. The previous skill library is kept in
[legacy/](legacy/) until it is re-filed.

## What it will hold

| Part | What | Where |
|---|---|---|
| Robot Atlas | A researched profile of every notable open-source robot: specs, how it works, uses, cost, build effort, what to reuse | [wiki/robots/](wiki/robots/) |
| Parts and tools | Actuators, MCUs, drivers, sensors, compute, power; CAD, EDA, simulators, ROS 2 | [wiki/](wiki/) |
| Knowledge | Software, robot learning, concepts, decision guides | [wiki/](wiki/) |
| Skills and MCP | How an agent does the work, and the MCP servers that let it drive the tools | [skills/](skills/), [mcp/](mcp/) |
| Playbooks | Idea → requirements → design → build → simulation → bringup → learning | [playbooks/](playbooks/) |
| Video studio | Turning robots, concepts, CAD and tutorials into narrated videos | [docs/plan.md](docs/plan.md#10-video-track) |

Everything taken from outside is recorded in the [source registry](sources/README.md), with its
version and condition.

## Use it

```bash
git clone https://github.com/jewel-nath/roboai-workspace.git
```

```bash
cd roboai-workspace
```

Open the folder in Claude Code (or any agent that reads `AGENTS.md`) and brainstorm. Start your
own robot as a project in [projects/](projects/README.md): each project is its own git repo, so
your work stays yours while the workspace stays the shared brain.

## For agents and contributors

- [AGENTS.md](AGENTS.md) — how the repo works and where everything goes
- [docs/plan.md](docs/plan.md) — the design and roadmap
- [docs/frontmatter.md](docs/frontmatter.md) — page fields
- [templates/](templates/) — page, skill and project templates
- [CONTRIBUTING.md](CONTRIBUTING.md)

## License

[Apache License 2.0](LICENSE). Credits for adapted material are in [NOTICE](NOTICE).

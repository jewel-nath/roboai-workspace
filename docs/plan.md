# RoboAI Workspace — Plan

Status: **Phases 0 and 1 done, 2026-11-17; Phase 2 deferred; Phase 3 done, 2026-11-18.** This
plan replaces the old "Agentic Robotics" layout. Phase 0 built the structure, templates,
frontmatter and source registry; Phase 1 built the scripts and commands that keep them consistent;
Phase 3 wrote the Robot Atlas's 79 pages (17 profiles, 62 cards). The [roadmap](#12-roadmap) says
what comes next.

## Contents

1. [Vision](#1-vision)
2. [Principles](#2-principles)
3. [The six parts](#3-the-six-parts)
4. [Repository layout](#4-repository-layout)
5. [Projects](#5-projects)
6. [Robot Atlas](#6-robot-atlas)
7. [Tool support tiers](#7-tool-support-tiers)
8. [Curation rules](#8-curation-rules)
9. [Source registry](#9-source-registry)
10. [Video track](#10-video-track)
11. [Migration](#11-migration)
12. [Roadmap](#12-roadmap)
13. [Decisions](#13-decisions)
14. [Open questions](#14-open-questions)

---

## 1. Vision

**RoboAI Workspace is the open-source LLM Wiki for robotics.**

Every robotics developer re-researches the same things: which open robot to copy, what it costs, which
motor, which MCU, which simulator. RoboAI Workspace does that research once, carefully, in a form AI
agents can read, and pairs it with the skills and tools that let an agent help you build your own
robot: planning, mechanical design (skeleton, CAD, 3D printing), electronics (schematic, PCB),
firmware, ROS 2, simulation, robot learning, and the videos that explain it all.

Clone it, open it in Claude Code (or any agent that reads Markdown), and brainstorm. Your robot lives
in its own project folder. **Shared knowledge stays in the workspace; project-specific work stays in
the project.**

## 2. Principles

- **Curate, don't mirror.** Sources such as the awesome lists are raw material. Only what helps a
  builder gets in; everything else is one line in the index or a Rejected entry.
- **Accuracy beats volume.** An agent trusts what it reads. Every claim has a source, an evidence
  label and a date.
- **Write our own words, link the files.** Profiles summarise facts in our words; other people's CAD,
  meshes and firmware stay at their source, under their licence.
- **Agents work best in code.** Prefer tools an agent can drive by script (FreeCAD Python, KiCad with
  an MCP server, MuJoCo) over GUI-only or cloud tools.
- **Everything is traceable.** Every outside skill, tool or resource we take is registered with its
  version, so we can see its present condition and measure whether a new version is better.
- **Generated, not hand-kept.** Index tables, comparison tables, the toolkit page and NOTICE credits
  are generated from frontmatter and the registry, so they cannot drift.

## 3. The six parts

| Part | What it holds | Lives in |
|---|---|---|
| **Robot Atlas** | A research profile of every notable open-source robot: specs, how it works, uses, cost, build effort, what to reuse. Commercial robots as reference benchmarks | `wiki/robots/` |
| **Parts and tools** | Profiles of actuators, MCUs, drivers, sensors, compute, power, materials; the engineering tools. Linked both ways: a motor page lists every robot that uses it | `wiki/parts/`, `wiki/tools/` |
| **Knowledge** | Software and libraries, learning (policies, foundation models, datasets), concepts, decision guides | `wiki/software/`, `wiki/learning/`, `wiki/concepts/`, `wiki/guides/` |
| **Skills and MCP** | How the agent does the work, and the MCP servers that let it drive the tools | `skills/`, `mcp/` |
| **Playbooks** | Idea → requirements → mechanical → electronics → firmware → software → simulation → bringup → learning, with a checklist per stage | `playbooks/` |
| **Video studio** | Skills and tools that turn Atlas profiles, concepts, CAD and tutorials into narrated videos | `skills/video-*`, `wiki/tools/video/` |

Your own robots sit beside these in `projects/` (see [Projects](#5-projects)). What they learn flows
back into the Atlas, and once a project is public it gets its own profile with `evidence: built`.

## 4. Repository layout

```
roboai-workspace/
├── CLAUDE.md                ← agent entry: how to navigate, ingest, query, lint, commit
├── AGENTS.md                ← the same for Cursor, Codex and other agents
├── README.md
├── .mcp.example.json        ← copied to .mcp.json (gitignored, machine-specific paths)
├── wiki/
│   ├── robots/              ← Robot Atlas: one profile per robot + generated index
│   ├── parts/               ← actuators, mcu, drivers, sensors, compute, power, materials
│   ├── tools/               ← freecad, kicad, mujoco, ros2, video/ … (fusion360, easyeda: documented)
│   ├── software/            ← ROS 2 packages, SLAM, planners, libraries, mjlab
│   ├── learning/            ← policies, foundation models, datasets
│   ├── concepts/            ← kinematics, PID, power budget, design-for-print
│   └── guides/              ← choose-an-actuator, choose-an-MCU, robot cost ranges
├── sources/                 ← source registry, triage notes, benchmarks, check reports
├── skills/                  ← flat, prefixed: cad-freecad, pcb-kicad, fw-esp32, sim-mujoco, video-…
├── mcp/                     ← one setup guide per MCP server
├── playbooks/               ← the robot lifecycle and its stage checklists
├── templates/               ← page templates (robot, part, tool, source) and the project scaffold
├── tools/                   ← runnable scripts: calculators, index generator, lint, source checks
├── .claude/                 ← commands, agents, rules for this workspace
├── docs/                    ← this plan and other docs about the workspace itself
├── legacy/                  ← the old layout, until Phases 4–5 re-file it
└── projects/                ← gitignored; each project is its own git repo
```

Notes:

- **Skills are flat with a category prefix.** That is the layout Claude Code discovers reliably;
  nested category folders are not.
- **The repo ships as a Claude Code plugin** (Phase 7), so its skills load in the workspace and in any
  project, and can be installed without cloning.
- **MCP config is per machine.** `.mcp.json` holds local paths (for example a `konnect.exe` location),
  so only `.mcp.example.json` and the setup guides in `mcp/` are committed.

## 5. Projects

Each project is its own git repo inside `projects/`, which the workspace ignores.

```
projects/
├── README.md                ← tracked: how projects work
├── orbibot/                 ← gitignored; its own repo (private now, public later)
│   ├── PROJECT.md           ← the card: goal, stage, stack, wiki pages and skills used, open questions
│   ├── CLAUDE.md            ← project rules; points at ../../wiki and ../../skills
│   ├── .claude/skills/      ← skills only this project needs (its paths, params, versions)
│   └── docs/ cad/ pcb/ firmware/ ros2_ws/ sim/ videos/
└── nexbot/                  ← same shape, its own repo
```

- **One ignore rule:** `projects/*` with an exception for `projects/README.md`.
- **The card lives inside the project repo** (`PROJECT.md`), so it is versioned and travels with the
  project. The workspace agent finds all projects by reading `projects/*/PROJECT.md`.
- **No git submodules:** they would put private repo URLs into the public workspace.
- **Open the workspace root** to work. Workspace skills, wiki and MCP servers are then all loaded.
- `/new-project <name>` scaffolds a project from `templates/project/` and runs `git init`.

**Where a change is committed:**

| Change | Repo |
|---|---|
| A project's CAD, BOM, plans, firmware, decisions, video sources | that project's repo |
| A general lesson: a FreeCAD trap, a motor finding, a new MCP server, robot research | workspace |
| Machine-specific tool config | nowhere (gitignored) |

Before any commit, the agent checks which repo each changed file belongs to. `/promote` lifts a
general lesson from a project into the wiki, with the project's names removed and the project cited
as evidence.

## 6. Robot Atlas

### Profile frontmatter

Machine-readable, so comparison tables are generated, never hand-edited.

```yaml
type: robot
name:
category: arm            # arm | mobile-base | mobile-manipulator | humanoid | legged | social | gripper
openness: full           # full | partial | software-only | closed-reference
license: {hardware: , software: , docs: }
links: {repo: , docs: , cad: , paper: }
specs: {dof: , payload_kg: , reach_mm: , mass_kg: , size_mm: , speed: , runtime_h: }
stack: {actuators: , mcu: , compute: , sensors: [], sim_models: [], ros2: }
cost: {type: bom, usd: , as_of: , source: }   # type: bom | kit | retail
build: {difficulty: , hours: , print_hours: }  # difficulty 1–5
maturity: {last_commit: , stars: , active: }
use_cases: []            # teleop, imitation-learning, education, research …
evidence: researched     # built | researched | vendor-claim
last_verified:
sources: []
```

### Profile body

1. Summary — what it is, who made it, why it matters
2. Specs
3. How it works — mechanics, actuation, electronics, firmware, software, simulation
4. What it is used for — use cases, projects and papers that used it
5. Cost and BOM
6. Building it — difficulty, printing, tools, time, common failures
7. What is open — CAD format, PCB, firmware, URDF/MJCF, datasets
8. Strengths and limits
9. What to reuse — design ideas worth copying
10. Related robots
11. Sources

### Rules

- Every number has a source and an evidence label: `built`, `researched` or `vendor-claim`.
- Every cost is dated and typed (BOM, kit or retail, in USD). Prices drift fast.
- Robots seen only through datasheets share one note per group, as vendor claims.
- `/compare` answers questions such as "SO-101 vs Koch on cost and payload" from the frontmatter.

### Depth tiers

| Tier | Which robots | Depth |
|---|---|---|
| A | Open hardware with files and a BOM, still active | Full profile |
| B | Partly open, older but important, or commercial references | Short card |
| C | Everything else from the sources | One index row, or a Rejected entry with the reason |

## 7. Tool support tiers

| Tier | Meaning | Tools |
|---|---|---|
| **First-class** | Skills, tested setup, MCP where one exists | FreeCAD Python (headless `freecadcmd` build scripts; FreeCAD MCP for live GUI work), KiCad with the Konnect MCP, MuJoCo, ROS 2 |
| **Documented** | A wiki page only | Fusion 360, EasyEDA, build123d, CadQuery, OpenSCAD, Isaac Sim |
| **Video** | See [Video track](#10-video-track) | explainroo and video-director (core), huashu-motion (trial), earshot (later) |

The FreeCAD standard is the pattern OrbiBot already uses: FreeCAD 1.1 Python scripts run headless,
shared geometry in `params.py`, one module per part, explicit layout versions, guards and a build
recorder, STEP/STL/DXF export with a read-back, and CalculiX for FEA.

**MuJoCo** gets a skill (the old `skills/mujoco` merged with the general parts of OrbiBot's
`mujoco-sim`), wiki pages (versions and install on Windows and WSL, mjlab, MuJoCo MCP servers and how
they were judged) and a **CAD-to-sim pipeline**: FreeCAD `params.py` → meshes and inertia from mass
properties → generated MJCF → MuJoCo checks for tip-over, reach and stability.

## 8. Curation rules

An entry gets into the wiki only if it is:

- useful to someone building a robot;
- maintained, or historically important;
- under a usable licence;
- written with why it matters and where the facts come from.

Everything else gets a one-line **Rejected** entry with its reason and date, so nobody researches it
again. Awesome lists are cited from their upstream GitHub repos, not from mirror sites.

## 9. Source registry

Every outside source we take a skill, tool or resource from is recorded, so we can see its present
condition and measure whether a new version is better. It generalises what OrbiBot keeps by hand in
`docs/ai-toolkit.md` and `diagram-design/upstream.md`.

```
sources/
├── registry.yaml            ← one entry per outside source; the single source of truth
├── README.md                ← generated: in use · trial · planned · watching · rejected
├── <list>.md                ← one triage note per awesome list or other research source
├── benchmarks/<id>/         ← a fixed test per adopted source, with results per version
└── reports/<date>.md        ← output of each check
skills/<name>/upstream.md    ← for copied or adapted skills: kept · changed · added · left out · how to update
tools/check_sources.py       ← compares each source today against what we recorded
```

### Entry

```yaml
- id: explainroo
  url: https://github.com/vincentsch/explainroo
  kind: skill            # skill | mcp | tool | research-source | dataset | model
  area: video
  relation: installed    # installed | distilled | copied | referenced
  status: planned        # planned | trial | in-use | watching | rejected | retired
  license: MIT
  pinned: {version: 0.6.0, commit: }
  baseline: {stars: 1245, last_push: 2026-11-10}
  used_in: [skills/video-robot-explainer]
  install: /plugin install explainroo@explainroo
  benchmark: benchmarks/explainroo/
  last_checked: 2026-11-12
  history:
    - {date: 2026-11-12, event: planned, note: core video tool}
```

### How each relation is updated

| Relation | Meaning | Examples | Updating means |
|---|---|---|---|
| installed | Used as-is at a pinned version | explainroo, huashu-motion, earshot, freecad-mcp, Konnect | Move the pin, re-run the benchmark, compare |
| distilled | We wrote our own skill from it | `freecad-scripting-reference`, the legacy ROS 2 skills | Diff upstream since our commit, carry over improvements |
| copied | Files kept as-is under their licence | diagram-design's reference files | Diff, re-copy, re-run the checks |
| referenced | Only summarised and linked | awesome lists | Health check only |

### Present condition

`tools/check_sources.py` reports for each source: new releases or commits since our pin; archived,
moved or deleted repos; licence changes; no activity for more than 6 months; the star trend. With
`--pages` it checks each Robot Atlas page against its `links.repo` the same way. It reads a GitHub
token from an environment variable, which is never committed.

### Is it better?

Every source in `trial` or `in-use` has a fixed benchmark, re-run on each version bump. Results are
kept as numbers per version (never as MP4s or other large outputs), so "v0.6 vs v0.7" is a
measurement. Example: explainroo and video-director render the same 60-second PID brief each time,
recording video-director's and `explainroo check`'s QA numbers (text size, black frames, loudness,
misheard words), render time and a 1–10 human score.

### Review

`/review-sources`, weekly (OrbiBot's `toolkit-review`, generalised): run the check; for each flag,
read the changelog and decide — update and re-benchmark, carry over, keep watching, or retire. The
registry records the decision with the date. Nothing updates on its own.

### Two-way links

Every skill's frontmatter lists `sources: [ids]`; every registry entry lists `used_in`. The lint
checks both sides agree. `NOTICE` is generated from the copied and distilled entries, so Apache-2.0
credits stay correct.

### First entries

- **Video tools** (2026-11-12): explainroo, video-director, huashu-motion, earshot as `planned`;
  take-one and reanimate as `rejected` (reasons in [Video track](#10-video-track)).
- **MCP servers in `.mcp.example.json`** (2026-11-12): freecad-mcp and Konnect, as used by OrbiBot.
- **Sources of the legacy skills**, from `NOTICE`: `arpitg1304/robotics-agent-skills` and
  `harunkurtdev/ros2-claude-code-template`, both Apache-2.0. No commit was recorded when they were
  taken, so their baseline starts at registration.
- **OrbiBot's toolkit page**: 6 sources taken, 8 watched, 10 rejected — moved when OrbiBot moves
  in (deferred).
- **The 14 awesome lists** as `referenced`, each added when it is researched.

## 10. Video track

Videos planned: explanations of open-source robots, control concepts such as PID, OrbiBot part by
part in exploded views, ROS 2 tutorials, and a way for builders to make videos of their own projects.

### Tools

| Tool | Role | Status | Notes |
|---|---|---|---|
| [explainroo](https://github.com/vincentsch/explainroo) | Narrated explainers and tutorials: local voice (Kokoro), word timing (Whisper), charts, math, code steps, screen recordings, `cut` by words, subtitles and chapters | planned, core | MIT; Node 20.11+, ffmpeg, Chrome; tested on Windows in CI; no 3D of its own |
| [video-director](https://github.com/win4r/video-director) | Directing method and QA scripts (timeline check, render QA) for any renderer | planned, core | MIT; Python with numpy and Pillow, ffmpeg |
| [huashu-motion](https://github.com/alchaincyf/huashu-motion) | Promo and launch films as one HTML file (GSAP, Three.js), local music, point-at-frame editor, 12 templates | planned, trial | MIT (+ GSAP licence); Node 22+; tested on macOS only |
| [earshot](https://github.com/Leonxlnx/earshot) | Sound critique, sync checks, 252 code-made sound effects, MCP server | planned, later | MIT; uv, ~1.1 GB models; check torch on Python 3.14 |
| [take-one](https://github.com/talsiach/take-one) | One-line ad and music-video studio | rejected 2026-11-12 | Overlaps huashu-motion; product-ad focus; 1–2 h per 30 s; pushes paid services; macOS only |
| [reanimate](https://github.com/NiazMorshed2007/reanimate) | Clones web UI animations into code | rejected 2026-11-12 | Not a video maker; needs Bun; Windows untested |

This machine already has Node 22.23, ffmpeg 8.1, Chrome, uv and Python (checked 2026-11-12).

### Video type → tool chain

| Video | Chain |
|---|---|
| Open-source robot explainer | Atlas profile → script → explainroo (spec cards, how-it-works diagram, cost chart) → video-director QA |
| Control concepts (PID, kinematics, filters) | explainroo with the math computed in `scenes.js`, so plots are real step responses |
| OrbiBot exploded view | FreeCAD → one GLB per part → Three.js explode/assemble animation → clip inside an explainroo narration |
| ROS 2 tutorial | Screen recording (`explainroo record` or OBS) → `explainroo cut` → narration with code steps |
| A builder's project video | `/make-video` playbook reading `PROJECT.md`, CAD and photos; huashu-motion for promos |

### Skills we build

- `video-robot-explainer` — Atlas profile → a standard video structure, so every robot gets a
  consistent video.
- `video-cad-exploded` — FreeCAD → GLB → exploded or assembly animation → clip.
- `video-control-explainer` — PID, kinematics and filters with simulated plots.
- `video-ros2-tutorial` — record, cut, narrate.
- A **RoboAI look**: one explainroo look file (colours, fonts) so every video reads as one channel.

### Where things live

- Third-party video tools are installed from upstream at user level, pinned, and recorded in the
  registry and `wiki/tools/video/`. They are not copied in; they release almost daily.
- Our video skills: `skills/video-*`.
- The videos: `projects/roboai-videos/`, its own repo. Sources (`script.md`, `scenes.js`,
  `video.json`) are committed; MP4s go to YouTube or GitHub Releases, never into git.

### Caveats

- All four tools are weeks old and change fast — pin versions and benchmark each bump.
- explainroo adds an "explainroo.com" corner mark (`"watermark": false` turns it off; its author asks
  to keep it). huashu-motion ends films with "Made with huashu-motion" (can be turned off).
- Kokoro has no Bangla voice. Bangla narration needs a recorded voice (Whisper still times the words)
  or a paid voice service that supports it — not yet checked.

## 11. Migration

### Legacy content of this repo

In Phase 0 the old layout (skills, guides, rules, commands, scripts, README, CONTRIBUTING) was moved
into `legacy/` with `git mv` and audited. [legacy-audit.md](legacy-audit.md) records the findings
and maps every file to its destination. Re-filing was part of Phase 2; with Phase 2 deferred, it
moves into the phases that cover the same topics: ROS 2, simulation, perception, navigation,
manipulation, learning and operations skills in Phase 4, firmware and control skills in Phase 5.

### OrbiBot

**Deferred on 2026-11-17:** OrbiBot stays in its own folder for now. When it moves, this is how.

OrbiBot moves into `projects/orbibot/`: push everything, fresh-clone it there, verify, then archive
the old folder (moving it directly would break its `.claude/worktrees` paths). Renaming the GitHub
repo from `orbibot-workspace` to `orbibot` is optional.

| From OrbiBot | To |
|---|---|
| `freecad-scripting-reference` (tested recipes and traps) | `skills/cad-freecad-scripting` |
| `freecad-build-scripts` | `skills/cad-freecad-build` (the pattern); OrbiBot paths and versions stay in the project |
| `freecad-mcp-bridge` | `skills/cad-freecad-mcp` |
| `kicad-project-rules` | `skills/pcb-kicad` + `mcp/konnect.md`; where OrbiBot's board lives stays in the project |
| `mujoco-sim` | merged into `skills/sim-mujoco` + `wiki/tools/mujoco.md`; the twin stays in the project |
| `diagram-design` | `skills/diagram-design` with colours as a theme |
| `toolkit-review` + `docs/ai-toolkit.md` | `/review-sources` + the source registry |
| `.mcp.json` (Konnect, freecad-mcp) | `mcp/` guides + `.mcp.example.json` |
| Robot studies in `research/` and `references/robots/*` | first Atlas profiles (linking to the original repos, not copying them) |
| `research/motor-research.md`, `base-drive-options.md` | `wiki/parts/`, `wiki/guides/` |
| `research/*-power.py`, `*-battery.py`, `*-estop.py` | `tools/calc/`, made general |
| OrbiBot plans, model-specific research, private material | stay in the OrbiBot repo |

## 12. Roadmap

| Phase | Goal | Done when |
|---|---|---|
| **0. Redesign** ✅ 2026-11-12 | Skeleton; templates (robot, part, tool, concept, guide, source, skill, project); frontmatter schema; CLAUDE.md and AGENTS.md; projects setup; registry schema and first entries; legacy audit; new README | An agent opening the repo knows where everything goes |
| **1. Tooling** ✅ 2026-11-17 | `/ingest`, `/new-project`, `/promote`, `/compare`, `/review-sources`; `check_sources.py`; benchmark setup; index generator; lint and CI | Research and reviews produce consistent, checked output |
| **2. OrbiBot** — deferred 2026-11-17 | Move it into `projects/`; general skills, calculators, Atlas profiles; its registry entries. Legacy re-filing moved to Phases 4–5 | OrbiBot works from `projects/orbibot` and its general knowledge is in the wiki |
| **3. Robot Atlas** ✅ 2026-11-18 | The robot entries of awesome-robot-descriptions, robotics-projects, ros-mobile-robot and social-robots | Every robot entry triaged; tier A/B profiles with generated comparison tables |
| **4. Software and learning** | robotics-libraries, robotic-tooling, robot-learning, foundation models, datasets, robotics-3D, mobile-robotics, manipulation, the general awesome-robotics list, and the non-robot sections of the Phase 3 lists; ROS 2 from its official docs; re-file the 21 legacy ROS 2, simulation, perception, navigation, manipulation, learning and operations skills ([Phase 4 plan](#phase-4-plan)) | Every Phase 4 list triaged; software and learning pages with a decision guide per topic; those legacy skills re-filed |
| **5. Gaps** | Parts catalog, PCB, firmware and MCU, FreeCAD and KiCad skills, CAD-to-MuJoCo, known-good combinations; re-file the legacy firmware and control skills | The areas the awesome lists miss are covered; `legacy/` is empty |
| **6. Playbooks** | The idea-to-robot lifecycle with a checklist per stage | A new project can follow it end to end |
| **7. Distribution** | Claude Code plugin, docs site, contributor guide | Others can install and contribute |
| **Video track** | V1 PID pilot (explainroo + video-director) → V2 huashu-motion trial with an OrbiBot teaser → V3 `video-cad-exploded` (after the FreeCAD skills, Phase 5) → V4 robot explainers (after Phase 3) → V5 earshot | Starts after Phase 1, so its first benchmark lands in the registry |

### Phase 4 plan

Planned 2026-11-18. Sizes are rough counts of linked lines in each README on that day.

| List | Upstream | Last commit | Size | Holds |
|---|---|---|---|---|
| awesome-robotic-tooling | Ly0n/awesome-robotic-tooling | 2023-04-30 | ~940 | Development tools, ROS, simulation, perception, ops |
| awesome-mobile-robotics | mathiasmantelli/awesome-mobile-robotics | 2026-08-03 | ~530 | Courses, software, papers, datasets |
| Awesome-Robotics-Manipulation | BaiShuanghao/Awesome-Robotics-Manipulation | 2026-10-29 | ~4,100 papers | Manipulation papers with code links, in the README and five `contents/` files |
| awesome-robotics-libraries | jslee02/awesome-robotics-libraries | 2026-10-26 | ~230 | Simulators, kinematics, planning, math libraries |
| awesome-robotics | kiloreux/awesome-robotics | 2024-09-22 | ~150 | General: courses, books, software, competitions |
| Awesome-Robotics-Foundation-Models | robotics-survey/Awesome-Robotics-Foundation-Models | 2024-10-07 | ~110 papers | Foundation-model papers |
| Awesome-Robotics-3D | zubair-irshad/Awesome-Robotics-3D | 2025-12-17 | ~95 papers | 3D vision for robotics |
| awesome-robotics-datasets | mint-lab/awesome-robotics-datasets | 2021-08-27 | ~80 | Datasets |
| Awesome-Robot-Learning | RayYoh/Awesome-Robot-Learning | 2026-08-20 | ~75 | Surveys, policies, benchmarks |

Plus the sections each Phase 3 triage note left for Phase 4. ROS 2 pages come from docs.ros.org
and ROS Index instead of a list (see Decisions).

**Steps.**

1. **Triage every list** with `/ingest`, in parallel by list, before writing any page. Sections
   that hold only papers get one index row each, with the paper count; models, policies, datasets,
   benchmarks, tools and code repos get their own rows. Each "Waiting for a page" row names its
   topic batch.
2. **Write by topic.** Each batch writes its pages (tools and libraries in `wiki/tools/` and
   `wiki/software/`, policies, models and datasets in `wiki/learning/`, ideas in
   `wiki/concepts/`), one decision guide in `wiki/guides/`, and re-files its legacy skills:

   | Batch | Legacy skills re-filed |
   |---|---|
   | ROS 2 core and tooling | `ros2-core`, `ros2-control`, `ros2-web-bridge`, `ros2-robot-description`, `ops-docker-ci` |
   | Simulation | `sim-gazebo`, `sim-to-real`; Isaac Sim to `wiki/tools/` |
   | Perception and SLAM | `perception-camera`, `perception-lidar`, `perception-slam` |
   | Navigation | `nav-nav2`, `nav-planning` |
   | Manipulation | `manip-moveit2`, `manip-grasping` |
   | Learning: policies, foundation models, datasets | `learn-robot-learning`, `learn-edge-deployment` |
   | Operations and architecture | `ops-bringup`, `ops-fleet`, `arch-robot-architecture`, `arch-safety` |

3. **Each batch** ends with the index generator, the lint and one commit. The MuJoCo, control and
   firmware skills stay in `legacy/` for Phase 5.

## 13. Decisions

All dated 2026-11-12.

- The repo is **RoboAI Workspace** (formerly agentic-robotics): the open-source LLM Wiki for robotics.
- **Full redesign.** The old layout is legacy material, audited and re-filed.
- **Projects** live in `projects/`, gitignored, each its own git repo with a `PROJECT.md` card.
- **OrbiBot** is private now and public later. Its general research and skills move to the
  workspace; private material does not.
- **CAD:** FreeCAD Python is first-class. **Fusion 360 and EasyEDA are documented only.**
- **MuJoCo** is a first-class simulator, with a skill and a CAD-to-sim pipeline.
- **No garbage:** curation rules plus a Rejected log.
- **Robot Atlas** is the centrepiece: one researched profile per robot, with dated costs.
- **Video:** explainroo and video-director are core, huashu-motion is a trial, earshot comes later;
  take-one and reanimate are rejected. Plan only — nothing is installed yet.
- **Every outside source** goes into the source registry with its version, condition and benchmark.
- **The old layout moved into `legacy/`** in Phase 0, so the new structure starts clean and nothing
  is lost; Phases 4–5 re-file it.
- **AGENTS.md is the agent guide** for every tool; CLAUDE.md imports it and adds Claude Code notes.
- **2026-11-17: Phase 2 is deferred.** OrbiBot is not brought into `projects/` for now. The FreeCAD,
  KiCad and MuJoCo skills are written in Phase 5 instead of being taken from OrbiBot first.
- **2026-11-17: scripts run with `uv run`.** Each declares its dependencies inline (PEP 723), so
  there is nothing to install beyond uv. Allowed frontmatter values live in `tools/schema.yaml`.
- **2026-11-17: NOTICE is generated** from the registry's `notice` fields.
- **2026-11-17: Phase 3 covers robots only.** awesome-mobile-robotics and
  Awesome-Robotics-Manipulation hold courses, software, papers and datasets but no robots, so they
  move to Phase 4, as do the software sections of the Phase 3 lists. Their triage notes say which
  sections are still open. Registry sources that feed the Atlas use the area `robots`.
- **2026-11-17: Atlas robots are not registry entries.** A robot page's own frontmatter (`links`,
  `license`, `maturity`) is its baseline, so a registry entry per robot would only repeat it. The
  registry keeps the lists they came from. `tools/check_sources.py --pages` is the page health
  check (repo moved, archived, licence changed, stale `maturity`), run by `/review-sources`.
- **2026-11-18: awesome-ros2 is dropped.** Its upstream, fkromer/awesome-ros2, returned 404 on
  2026-11-18, and the live fork (floesche) has had no commit since 2021. ROS 2 pages are written
  from docs.ros.org, ROS Index and the ROS sections of awesome-ros-mobile-robot.
- **2026-11-18: paper sections are triaged by section.** A section that holds only papers is one
  index row with its paper count. Entries with a model, policy, dataset, benchmark, tool or code
  repo are still triaged one by one.
- **2026-11-18: re-filed skills default to ROS 2 Jazzy** (LTS to May 2029) and note where Lyrical
  (the May 2026 LTS) differs.
- **2026-11-18: the architecture and safety skills join Phase 4's operations batch;** the legacy
  audit gave them no phase.

## 14. Open questions

- **Video language:** English, Bangla, or both?
- **Review day** for `/review-sources` (OrbiBot uses Friday).
- **Gazebo's tier:** first-class with ROS 2, or documented beside MuJoCo?
- **Legacy skills that fall to the documented tier** (such as `isaac-sim`): keep the long text as a
  wiki page, or trim it?
- **GitHub token** for the source checks: which account, kept in an environment variable.

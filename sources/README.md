# Sources

Every outside source we take a skill, tool or resource from is recorded here, so we can see its
present condition and measure whether a new version is better. [registry.yaml](registry.yaml) is
the single source of truth; this page explains it and shows the generated summary.

```
sources/
├── registry.yaml          ← one entry per outside source
├── README.md              ← this page; the summary below is generated
├── <source>.md            ← one triage note per research source (template: templates/source.md)
├── benchmarks/<id>/       ← a fixed test per adopted source, with results per version
└── reports/<date>.md      ← output of each check
```

## Entry fields

| Field | Meaning |
|---|---|
| `id` | Short kebab-case name, used by skills and wiki pages to refer to it |
| `url` | Upstream repo or site (never a mirror) |
| `kind` | `skill`, `mcp`, `tool`, `research-source`, `dataset`, `model` |
| `area` | As for tools in [docs/frontmatter.md](../docs/frontmatter.md), plus `robots` for sources that feed the Robot Atlas |
| `relation` | How we use it — see below |
| `status` | `planned`, `trial`, `in-use`, `watching`, `rejected`, `retired` |
| `license` | SPDX id, as upstream states it |
| `pinned` | `{version, commit}` we use or took from; empty until adopted |
| `baseline` | `{as_of, commit, commit_date, release, stars, archived}` read when last recorded |
| `used_in` | Paths in this repo that depend on it |
| `benchmark` | `{path, status}` of its fixed test, for sources in `trial` or `in-use` |
| `install` | How to install it, when we install it |
| `last_checked` | Date of the last check |
| `notes` | Why it is here, and anything a reviewer must know |
| `history` | `{date, event, note}`, appended on every change |
| `notice` | For `distilled` and `copied` sources: who made it and what we took, for `NOTICE` |

Commit ids are quoted (`commit: "0272906"`), so YAML never reads one as a number.

## How each relation is updated

| Relation | Meaning | Updating means |
|---|---|---|
| `installed` | Used as-is at a pinned version | Move the pin, re-run the benchmark, compare |
| `distilled` | We wrote our own skill or page from it | Diff upstream since our commit; carry over what is better |
| `copied` | Files kept as-is under their licence | Diff, re-copy, re-run the checks; record in the skill's `upstream.md` |
| `referenced` | Only summarised and linked | Health check only |

## Rules

- **Nothing outside comes in unregistered.** Taking a skill, installing a tool, or copying a file
  means adding an entry first.
- **Rejected entries stay**, with the reason and date, so nobody reviews the same thing twice.
- **Skills and registry agree:** a skill's `metadata.sources` lists the ids it uses, and those
  entries list the skill in `used_in`. `tools/lint.py` checks both sides.
- **Nothing updates on its own.** `/review-sources` runs `tools/check_sources.py`; a person decides.
- **`NOTICE` is generated** by `tools/build_index.py` from the `notice` of each `copied` and
  `distilled` entry. Edit the registry, never `NOTICE`.

## Checking sources

```bash
uv run tools/check_sources.py --report --record
```

```bash
uv run tools/check_sources.py --pages --report
```

The first compares each GitHub source with its baseline (new commits and releases, archived,
moved, licence changes, no push for 180 days), writes `reports/<date>.md`, and sets
`last_checked`. `--rebaseline <id>` records today's upstream state once a change is accepted.

Robot Atlas pages are not registry entries: a page's own frontmatter is its baseline. The second
command checks each page in `wiki/robots/` against its `links.repo`: moved or deleted, archived, a
GitHub licence that is neither the page's `license.software` nor `license.hardware` (`NOASSERTION`
is ignored), commits newer than `maturity.last_commit`, and `maturity.active` against the last
push. It adds its own section to the same report and changes no page unless given
`--record-pages`, which writes today's `maturity.last_commit`, `stars` and `active`;
`last_verified` stays for a person to set once the page's facts are re-checked.

Set `GITHUB_TOKEN` for more than 60 API requests an hour. Without it the page check stops near the
limit and lists the pages it skipped.

## Summary

<!-- index:start -->
### In use (17)

| Source | Kind | Area | Relation | Licence | Pinned | Checked | Notes |
|---|---|---|---|---|---|---|---|
| [freecad-mcp](https://github.com/neka-nat/freecad-mcp) | mcp | cad | installed | MIT | 0.1.28 | 2026-11-17 | Version pinned in OrbiBot since 2026-11-03. |
| [awesome-robotics-libraries](https://github.com/jslee02/awesome-robotics-libraries) | research-source | control | referenced | CC0-1.0 | — | 2026-11-18 | Robotics libraries and software - simulators, dynamics, kinematics, motion planning, optimisation, SLAM and vision. |
| [awesome-robotics](https://github.com/kiloreux/awesome-robotics) | research-source | docs | referenced | custom | — | 2026-11-18 | General robotics list - courses, books, software, competitions and companies. |
| [awesome-robot-learning](https://github.com/RayYoh/Awesome-Robot-Learning) | research-source | learning | referenced | MIT | — | 2026-11-18 | Robot learning resources, mainly for manipulation - surveys, policies, benchmarks and datasets. |
| [awesome-robotics-datasets](https://github.com/mint-lab/awesome-robotics-datasets) | research-source | learning | referenced | none | — | 2026-11-18 | Robotics datasets, mostly navigation, driving and SLAM. |
| [awesome-robotics-foundation-models](https://github.com/robotics-survey/Awesome-Robotics-Foundation-Models) | research-source | learning | referenced | MIT | — | 2026-11-18 | Papers on foundation models in robotics, the list behind the survey "Foundation Models in Robotics" (2023). |
| [awesome-robotics-manipulation](https://github.com/BaiShuanghao/Awesome-Robotics-Manipulation) | research-source | manip | referenced | MIT | — | 2026-11-18 | Robot manipulation papers with code and project links, grouped by method. |
| [awesome-mobile-robotics](https://github.com/mathiasmantelli/awesome-mobile-robotics) | research-source | nav | referenced | none | — | 2026-11-18 | Mobile robotics courses, books, software, papers and datasets. |
| [konnect](https://github.com/mixelpixx/Konnect) | mcp | pcb | installed | AGPL-3.0 | v0.13.0 | 2026-11-17 | Upstream archived on 2026-11-02, so v0.13.0 is final. |
| [awesome-robotics-3d](https://github.com/zubair-irshad/Awesome-Robotics-3D) | research-source | perception | referenced | none | — | 2026-11-18 | Papers on 3D vision for robotics - policies, representations, pretraining and simulation. |
| [awesome-robot-descriptions](https://github.com/robot-descriptions/awesome-robot-descriptions) | research-source | robots | referenced | CC0-1.0 | — | 2026-11-17 | URDF, MJCF and Xacro models of about 160 robots, by type, with each model's licence. |
| [awesome-robotics-projects](https://github.com/mjyc/awesome-robotics-projects) | research-source | robots | referenced | CC0-1.0 | — | 2026-11-17 | Open-source and affordable robot projects, plus robotics software and companies. |
| [awesome-ros-mobile-robot](https://github.com/shannon112/awesome-ros-mobile-robot) | research-source | robots | referenced | CC0-1.0 | — | 2026-11-17 | ROS mobile robot resources; CC0 stated in its README only. |
| [awesome-social-robots](https://github.com/jcarolinares/awesome-social-robots) | research-source | robots | referenced | GPL-3.0 | — | 2026-11-17 | Open and closed social and companion robots, virtual pets, and learning material. |
| [awesome-robotic-tooling](https://github.com/Ly0n/awesome-robotic-tooling) | research-source | ros2 | referenced | CC0-1.0 | — | 2026-11-18 | Development tooling for robotics in C++ and Python, with ROS, simulation, perception, autonomous driving and operations sections. |
| [robotics-agent-skills](https://github.com/arpitg1304/robotics-agent-skills) | skill | ros2 | distilled | Apache-2.0 | — | 2026-11-17 | The commit the old skills were adapted from was never recorded; this baseline is the upstream head at registration. |
| [ros2-claude-code-template](https://github.com/harunkurtdev/ros2-claude-code-template) | skill | ros2 | distilled | Apache-2.0 | — | 2026-11-17 | Licence stated in its README only; the repo has no licence file GitHub recognises. |

### Planned (4)

| Source | Kind | Area | Relation | Licence | Pinned | Checked | Notes |
|---|---|---|---|---|---|---|---|
| [earshot](https://github.com/Leonxlnx/earshot) | tool | video | installed | MIT | — | 2026-11-17 | Later, for sound checks and code-made sound effects; has an MCP server. |
| [explainroo](https://github.com/vincentsch/explainroo) | tool | video | installed | MIT | — | 2026-11-17 | Core video tool for narrated explainers and tutorials. |
| [huashu-motion](https://github.com/alchaincyf/huashu-motion) | tool | video | installed | MIT | — | 2026-11-17 | Trial for promo and 3D showcase films. |
| [video-director](https://github.com/win4r/video-director) | skill | video | installed | MIT | — | 2026-11-17 | Core directing method and QA scripts (check_timeline.py, qa_video.py), for any renderer. |

### Rejected (2)

| Source | Kind | Area | Relation | Licence | Pinned | Checked | Notes |
|---|---|---|---|---|---|---|---|
| [reanimate](https://github.com/NiazMorshed2007/reanimate) | skill | video | referenced | MIT | — | 2026-11-17 | Clones web UI animations into code; it does not make videos. |
| [take-one](https://github.com/talsiach/take-one) | skill | video | referenced | MIT | — | 2026-11-17 | Overlaps huashu-motion; aimed at product ads; 1-2 hours and 0.4-0.7M tokens per 30 s film; suggests paid services through affiliate links;… |

### Triage notes

| Source | Read on | Entries | Pages | Waiting | Index only | Deferred | Rejected |
|---|---|---|---|---|---|---|---|
| [Awesome Mobile Robotics](awesome-mobile-robotics.md) | 2026-11-18 | 533 | 6 | 17 | 438 | 4 | 68 |
| [Awesome Robot Descriptions](awesome-robot-descriptions.md) | 2026-11-17 | 161 | 54 | 0 | 54 | 0 | 4 |
| [Awesome Robot Learning](awesome-robot-learning.md) | 2026-11-18 | 56 | 2 | 10 | 35 | 0 | 9 |
| [awesome-robotic-tooling](awesome-robotic-tooling.md) | 2026-11-18 | 938 | 13 | 27 | 577 | 71 | 250 |
| [Awesome Robotics 3D](awesome-robotics-3d.md) | 2026-11-18 | 32 | 1 | 4 | 25 | 0 | 2 |
| [Awesome Robotics Datasets](awesome-robotics-datasets.md) | 2026-11-18 | 77 | 0 | 2 | 52 | 0 | 23 |
| [Awesome Robotics Foundation Models](awesome-robotics-foundation-models.md) | 2026-11-18 | 42 | 1 | 7 | 33 | 0 | 1 |
| [Awesome Robotics Libraries](awesome-robotics-libraries.md) | 2026-11-18 | 229 | 12 | 19 | 124 | 33 | 41 |
| [Awesome-Robotics-Manipulation](awesome-robotics-manipulation.md) | 2026-11-18 | 109 | 1 | 27 | 77 | 0 | 4 |
| [Awesome Robotics Projects](awesome-robotics-projects.md) | 2026-11-17 | 195 | 25 | 9 | 127 | 1 | 33 |
| [Awesome Robotics](awesome-robotics.md) | 2026-11-18 | 147 | 4 | 3 | 106 | 1 | 33 |
| [awesome-ros-mobile-robot](awesome-ros-mobile-robot.md) | 2026-11-17 | 185 | 14 | 16 | 119 | 11 | 25 |
| [Awesome Social Robots](awesome-social-robots.md) | 2026-11-17 | 92 | 11 | 0 | 45 | 0 | 36 |
<!-- index:end -->

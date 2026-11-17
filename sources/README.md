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
| `area` | As in [docs/frontmatter.md](../docs/frontmatter.md) |
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

It compares each GitHub source with its baseline (new commits and releases, archived, moved,
licence changes, no push for 180 days), writes `reports/<date>.md`, and sets `last_checked`.
`--rebaseline <id>` records today's upstream state once a change is accepted. Set `GITHUB_TOKEN`
for more than 60 API requests an hour.

## Summary

<!-- index:start -->
### In use (4)

| Source | Kind | Area | Relation | Licence | Pinned | Checked | Notes |
|---|---|---|---|---|---|---|---|
| [freecad-mcp](https://github.com/neka-nat/freecad-mcp) | mcp | cad | installed | MIT | 0.1.28 | 2026-11-17 | Version pinned in OrbiBot since 2026-11-03. |
| [konnect](https://github.com/mixelpixx/Konnect) | mcp | pcb | installed | AGPL-3.0 | v0.13.0 | 2026-11-17 | Upstream archived on 2026-11-02, so v0.13.0 is final. |
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

_None yet._
<!-- index:end -->

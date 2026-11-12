# Frontmatter

Every wiki page, triage note, skill and project card starts with YAML frontmatter. It is what makes
pages comparable and indexes generatable, so its fields and words are fixed here. The templates in
[templates/](../templates/) carry these fields; the Phase 1 lint checks them.

## Conventions

- Dates are `YYYY-MM-DD`.
- Money is USD, always with `as_of` and `source`.
- Units go in the key name: `mass_kg`, `reach_mm`, `stall_torque_kgcm`, `voltage_v`.
- Unknown values stay empty; never guess to fill a field.
- The file name is the slug (kebab-case); there is no `slug` field to drift from it.
- A value that names something with its own page uses that page's slug.

## Fields on every wiki page

| Field | Values | Meaning |
|---|---|---|
| `type` | `robot`, `part`, `tool`, `concept`, `guide` | Which template the page follows |
| `name` | text | Display name |
| `summary` | one line | What it is and why it matters |
| `tags` | list | Free search words |
| `evidence` | `built`, `researched`, `vendor-claim` | `built`: we built or ran it. `researched`: read from its repo, docs or paper. `vendor-claim`: only the maker's word |
| `last_verified` | date | When the facts were last checked against the sources |
| `sources` | list of `{url, title, accessed}` | Where the facts come from |

## `type: robot`

| Field | Values |
|---|---|
| `category` | `arm`, `mobile-base`, `mobile-manipulator`, `humanoid`, `legged`, `social`, `gripper`, `other` |
| `tier` | `A` (full profile), `B` (short card) |
| `openness` | `full`, `partial`, `software-only`, `closed-reference` |
| `maker`, `year` | who made it, first public year |
| `license` | `{hardware, software, docs}`, SPDX ids where they exist |
| `links` | `{repo, docs, cad, paper, site}` |
| `specs` | `{dof, payload_kg, reach_mm, mass_kg, size_mm, speed_mps, runtime_h}` |
| `stack` | `{actuators, mcu, compute, sensors, sim_models, ros2}`; part slugs where pages exist |
| `cost` | `{type: bom \| kit \| retail, usd, as_of, source}` |
| `build` | `{difficulty: 1–5, hours, print_hours}` |
| `maturity` | `{last_commit, stars, active: true \| false}` |
| `use_cases` | list, for example `teleop`, `imitation-learning`, `education`, `research` |

## `type: part`

| Field | Values |
|---|---|
| `category` | `actuator`, `mcu`, `driver`, `sensor`, `compute`, `power`, `material` |
| `subcategory` | text, for example `serial-bus-servo`, `2d-lidar` |
| `maker`, `model` | text |
| `specs` | category-specific keys with units |
| `interfaces` | list, for example `uart`, `ttl-bus`, `i2c`, `spi`, `can`, `usb`, `ethernet` |
| `cost` | `{usd, qty, as_of, source}` |
| `where_to_buy` | list of `{seller, url, as_of}` |
| `datasheet` | URL |
| `alternatives` | list of part slugs |
| `used_in` | generated from robot pages; leave empty |

## `type: tool`

Used for tools, libraries, frameworks, policies, models and datasets.

| Field | Values |
|---|---|
| `kind` | `tool`, `library`, `framework`, `policy`, `model`, `dataset` |
| `area` | `cad`, `pcb`, `sim`, `ros2`, `firmware`, `perception`, `nav`, `manip`, `control`, `learning`, `video`, `docs` |
| `support` | `first-class`, `documented` (tools only; see plan §7) |
| `license` | SPDX id |
| `links` | `{repo, docs, site}` |
| `version` | `{tested, latest, as_of}` |
| `platforms` | list: `windows`, `linux`, `macos` |
| `agent_access` | `script`, `mcp`, `cli`, `api`, `gui-only` |
| `registry` | source registry id, when we install or take from it |

## `type: concept`

| Field | Values |
|---|---|
| `area` | as for tools |
| `prerequisites` | list of concept slugs |
| `related` | list of slugs: concepts, skills, parts |

## `type: guide`

| Field | Values |
|---|---|
| `question` | the decision, as a question |
| `options` | list of slugs compared |
| `recommendation` | one line, with its condition |

## Triage notes (`type: source`)

One per research source in [sources/](../sources/), such as an awesome list.

| Field | Values |
|---|---|
| `registry` | its source registry id |
| `url` | upstream URL (the GitHub repo, not a mirror) |
| `commit` | the commit read |
| `read_on` | date |
| `counts` | `{entries, pages, index_only, rejected}` |

## Skills

Skills follow the [Agent Skills](https://agentskills.io) format: `name` and `description` at the
top level, our own fields under `metadata`.

| Field | Values |
|---|---|
| `name` | the folder name, with its category prefix |
| `description` | what it does and when to use it; agents match on this text |
| `license` | `Apache-2.0` unless upstream files keep their own |
| `metadata.sources` | registry ids it was taken or distilled from; `[]` if written here |
| `metadata.evidence` | `built` (its recipes were run) or `researched` |
| `metadata.last_verified` | date |

## Project cards (`PROJECT.md`)

| Field | Values |
|---|---|
| `type` | `project` |
| `name`, `summary` | text |
| `category` | as for robots |
| `stage` | `idea`, `requirements`, `design`, `build`, `bringup`, `learning`, `deployed`, `paused` |
| `visibility` | `private`, `public` |
| `repo` | remote URL |
| `stack` | as for robots, plus `{cad, sim}` |
| `uses` | `{wiki: [slugs], skills: [names]}` |

## Source registry entries

Defined in [sources/README.md](../sources/README.md).

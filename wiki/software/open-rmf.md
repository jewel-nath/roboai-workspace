---
type: tool
name: Open-RMF
summary: The ROS 2 framework that lets robot fleets share a building - one traffic schedule, task bidding, doors and lifts, a web dashboard; Apache-2.0, governed by the OSRA. Full binaries for Humble, Jazzy and Kilted; Lyrical has the core packages but no metapackage.
tags: [open-rmf, rmf, fleet-management, multi-robot, multi-fleet, traffic-schedule, doors, lifts, fleet-adapter, easyfullcontrol, free-fleet, rmf-web, dashboard, osra, rmf-core]
kind: framework
area: nav
support:
license: Apache-2.0
links: {repo: "https://github.com/open-rmf/rmf", docs: "https://osrf.github.io/ros2multirobotbook/", site: "https://www.open-rmf.org"}
version: {tested: , latest: 2.15.0, as_of: 2026-11-25}
platforms: [linux]
agent_access: script
registry:
evidence: researched
last_verified: 2026-11-25
sources:
  - {url: "https://github.com/open-rmf/rmf", title: "Open-RMF rmf repository: README, LICENSE, docs/Project-Roles.md, docs/Development-and-Release.md, branches and tags", accessed: 2026-11-25}
  - {url: "https://github.com/open-rmf/rmf_ros2", title: "rmf_ros2 repository: README, LICENSE.md, package.xml files, CHANGELOGs, EasyFullControl.hpp, StandardNames.hpp, tags, issues", accessed: 2026-11-25}
  - {url: "https://github.com/open-rmf/fleet_adapter_template", title: "fleet_adapter_template repository: full-control and traffic-light templates, READMEs, LICENSE", accessed: 2026-11-25}
  - {url: "https://github.com/open-rmf/free_fleet", title: "free_fleet repository: README, LICENSE, tags", accessed: 2026-11-25}
  - {url: "https://github.com/open-rmf/rmf-web", title: "rmf-web repository: README, LICENSE.md, api-server README, default_config.py and routes", accessed: 2026-11-25}
  - {url: "https://github.com/osrf/rmf_core", title: "rmf_core repository (archived 2021-07-22): README", accessed: 2026-11-25}
  - {url: "https://discourse.openrobotics.org/t/next-generation-open-rmf-roadmap/53820", title: "Open Robotics Discourse: Next Generation Open-RMF Roadmap (2026-04-06)", accessed: 2026-11-25}
  - {url: "https://github.com/ros/rosdistro", title: "rosdistro distribution files: humble, jazzy, kilted, lyrical, rolling", accessed: 2026-11-25}
---

# Open-RMF

Open-RMF lets robot fleets share a building: a traffic schedule keeps planned paths apart, a
dispatcher gives each task to the fleet that bids best, and adapters work doors and lifts [1][2].
All Apache-2.0, governed since 2024 by the OSRA's Open-RMF committee [1][7]. Newest core release:
rmf_ros2 2.15.0 (2026-11-13); last commit 2026-11-20; 85 open issues [2]. It continues the archived
`osrf/rmf_core` [6]. A staged rewrite is planned; its v2 adapter should run today's adapters [7].

## When to use it

- **Several fleets, or robots that ride lifts and pass automatic doors:** its purpose [1].
- **One fleet of your own:** you still write an adapter and draw a nav graph [3], and get task
  bidding, charging, doors, lifts and a dashboard [2][5]. On one floor with no doors,
  [Nav2](nav2.md) alone is lighter (our judgement). Nav2 robots on Jazzy can use free_fleet [4].

## Setup

```bash
sudo apt install ros-jazzy-rmf-dev     # all but the demos
```

`rmf_dev` exists for Humble, Jazzy (rmf_ros2 2.7.3) and Kilted; Lyrical has the core packages
(rmf_ros2 2.13.0) but no `rmf_dev` [8]. Debs and some RPMs, amd64 and aarch64 [1]. Demos: none for
Humble, no `rmf_demos_gz` for Jazzy; build tag `2.4.1` or run the nightly `rmf_demos` image [1][8].

## How an agent works with it

- **Fleet adapter:** copy the template; fill `RobotClientAPI.py` (`navigate`, `stop`, `position`,
  `battery_soc`) for the robot's API and `config.yaml` (four or more points matched between maps);
  run `ros2 run fleet_adapter_template fleet_adapter -c config.yaml -n nav_graph.yaml -s <uri>`.
  It wraps EasyFullControl; self-navigating robots use the traffic-light template [2][3]. Door
  and lift adapters publish `door_states`, `lift_states`; they act on `*_requests` topics [2].
- **Dashboard:** run rmf-web's `api-server` and `demo-dashboard` images with `--network host` and
  the fleet's `ROS_DOMAIN_ID` and RMW; give adapters `-s ws://localhost:8000/_internal`. Check:
  the robots show on `localhost:3000` [5].

## Traps

- **Versions drift.** The meta repo's `jazzy-release` branch still pins rmf_ros2 2.7.2 (June 2024)
  [1]: take versions from rosdistro [8]. Nightly images follow `main` and break; pin a digest [1].
- **Source over binaries:** purge `ros-<distro>-rmf*` first, or old headers clash; the first build
  downloads up to an hour of models unless `-DNO_DOWNLOAD_MODELS=On` [1].
- **Demo-grade API server.** It binds 127.0.0.1, keeps an in-memory database, makes `admin` an
  admin and checks tokens with a published default `jwt_secret`. Set `jwt_public_key` from an
  OpenID Connect provider and clear the secret before exposing it [5].
- **free_fleet is narrow:** Jazzy and source only, tested mostly with Cyclone DDS, Zenoh bridges
  at 1.5.0, pip with `--break-system-packages`; robots' Nav2 un-namespaced, bridges namespaced [4].

## Alternatives

[Nav2](nav2.md) alone, or a vendor's fleet manager. For the robot-to-server network see
[rmw_zenoh](rmw-zenoh.md); for operations, the [ops-fleet skill](../../skills/ops-fleet/SKILL.md).

## Sources

1. [Open-RMF rmf repository: README, LICENSE, docs/Project-Roles.md, docs/Development-and-Release.md, branches and tags](https://github.com/open-rmf/rmf), accessed 2026-11-25
2. [rmf_ros2 repository: README, LICENSE.md, package.xml files, CHANGELOGs, EasyFullControl.hpp, StandardNames.hpp, tags, issues](https://github.com/open-rmf/rmf_ros2), accessed 2026-11-25
3. [fleet_adapter_template repository: full-control and traffic-light templates, READMEs, LICENSE](https://github.com/open-rmf/fleet_adapter_template), accessed 2026-11-25
4. [free_fleet repository: README, LICENSE, tags](https://github.com/open-rmf/free_fleet), accessed 2026-11-25
5. [rmf-web repository: README, LICENSE.md, api-server README, default_config.py and routes](https://github.com/open-rmf/rmf-web), accessed 2026-11-25
6. [rmf_core repository (archived 2021-07-22): README](https://github.com/osrf/rmf_core), accessed 2026-11-25
7. [Open Robotics Discourse: Next Generation Open-RMF Roadmap (2026-04-06)](https://discourse.openrobotics.org/t/next-generation-open-rmf-roadmap/53820), accessed 2026-11-25
8. [rosdistro distribution files: humble, jazzy, kilted, lyrical, rolling](https://github.com/ros/rosdistro), accessed 2026-11-25

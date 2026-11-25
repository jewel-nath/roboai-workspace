# Legacy audit

Audited 2026-11-12, in Phase 0 of the [plan](plan.md). The old "Agentic Robotics" layout now sits in
[`legacy/`](../legacy/), moved with `git mv` so its history follows it. This page records what is
there, what is wrong with it today, and where each piece goes. The re-filing itself happens in
Phases 4 and 5, and the old guides become playbooks in Phase 6 (Phase 2, which first held it, is
deferred); nothing new is added to `legacy/`.

## How it was audited

- Every file was inventoried by size, category and the ROS 2 distros, simulators and RTOSes it
  names (precise patterns such as `/opt/ros/<distro>` and `ros-<distro>-`, so words like
  "environment" do not count as "Iron").
- Sources come from [`NOTICE`](../NOTICE).
- Content was **not** re-reviewed line by line. Each skill gets that review when it is re-filed.

## Findings

1. **OrbiBot is the worked example in 11 skills and 2 guides.** Most mentions are in
   `deployment-fleet` (74), `production-deployment` (66) and `testing-strategy` (41). Workspace skills
   must be general, so on re-filing the examples become neutral, and any OrbiBot-specific part moves
   to `projects/orbibot`.
2. **Mixed ROS 2 distros.** Humble appears in 14 skills and 3 guides, Jazzy in 8 skills and 2
   guides, sometimes both in one file. No skill names Iron or Kilted. Re-filed skills pick one
   default distro and say where others differ.
3. **Gazebo Classic** is still covered beside Gazebo Sim in `gazebo`. Gazebo Classic reached end of
   life in January 2025; it becomes a migration note.
4. **Overlaps to merge:**
   - PID appears in `control-systems`, `realtime-motor-control` and `sensor-actuator-drivers`.
   - `robot-bringup` (skill) and `guides/robot-bringup.md` cover the same ground.
   - `sim-to-real` (skill) and `guides/sim-to-real-pipeline.md` cover the same ground.
   - `guides/testing-strategy.md` and `rules/robotics-testing.md` overlap.
5. **No source version was recorded** for the adapted material. Both sources are now in the
   [source registry](../sources/registry.yaml), baselined at registration.
6. **Format:** skills use the old frontmatter (`category`, `tags`, `version`) and no `sources` field.
   Re-filed skills follow [templates/skill/SKILL.md](../templates/skill/SKILL.md).

## Skills

Lines and distros as found. "Source" is the outside project a skill was partly adapted from, per
`NOTICE`. Destinations follow [plan §11](plan.md#11-migration) and may change during review.
A row marked "re-filed" gives the date; the old file then leaves `legacy/`, and git history keeps
it.

| Old skill | Lines | Distros named | Source | Destination | Action |
|---|---|---|---|---|---|
| `ros2` | 704 | Humble | robotics-agent-skills | `skills/ros2-core` | re-filed 2026-11-18 |
| `ros2-control` | 621 | Humble | — | `skills/ros2-control` | re-filed 2026-11-18 |
| `ros2-web-bridge` | 1072 | — | robotics-agent-skills | `skills/ros2-web-bridge` | re-filed 2026-11-18 |
| `robot-modeling` | 594 | — | — | `skills/ros2-robot-description` | re-filed 2026-11-18 |
| `gazebo` | 599 | Humble | — | `skills/sim-gazebo` | re-filed 2026-11-19; Classic → migration note |
| `mujoco` | 988 | — | — | `skills/sim-mujoco` | re-file in Phase 5 from upstream; OrbiBot's `mujoco-sim` adds its lessons through `/promote` later |
| `isaac-sim` | 676 | Humble | — | `wiki/tools/isaac-sim.md` | re-filed 2026-11-19 to the wiki (documented tier) |
| `sim-to-real` | 550 | Humble, Jazzy | — | `skills/sim-to-real` | re-filed 2026-11-19, merged with `guides/sim-to-real-pipeline.md` |
| `camera-vision` | 557 | Humble | robotics-agent-skills | `skills/perception-camera` | re-filed 2026-11-23 |
| `lidar-pointcloud` | 687 | — | robotics-agent-skills | `skills/perception-lidar` | re-filed 2026-11-23 |
| `sensor-fusion-slam` | 779 | — | — | `skills/perception-slam` | re-filed 2026-11-23 |
| `nav2` | 845 | — | — | `skills/nav-nav2` | re-filed 2026-11-24 |
| `path-planning` | 833 | — | — | `skills/nav-planning` | re-filed 2026-11-24 |
| `moveit2` | 947 | Humble | — | `skills/manip-moveit2` | re-filed 2026-11-25 |
| `grasping-force-control` | 953 | Humble | — | `skills/manip-grasping` | re-filed 2026-11-25 |
| `control-systems` | 788 | — | — | `skills/control-systems` + `wiki/concepts/` | re-file; owns PID |
| `realtime-motor-control` | 909 | Humble | — | `skills/fw-motor-control` | re-file; PID → link to `control-systems` |
| `microcontrollers` | 886 | — | — | `skills/fw-mcu` | re-file |
| `gpio-i2c-spi` | 1265 | — | — | `skills/fw-peripherals` | re-file, neutral example |
| `serial-can-protocols` | 1141 | Humble | — | `skills/fw-serial-can` | re-file |
| `rtos-micro-ros` | 1140 | Jazzy | — | `skills/fw-rtos-micro-ros` | re-file, neutral example |
| `sensor-actuator-drivers` | 1267 | Jazzy | — | `skills/fw-drivers` | re-file; PID → link |
| `learning-robotics` | 1131 | — | — | `skills/learn-robot-learning` | re-filed 2026-11-25 |
| `edge-ml-deployment` | 1080 | Jazzy | — | `skills/learn-edge-deployment` | re-filed 2026-11-25 |
| `robot-architecture` | 1316 | Humble, Jazzy | robotics-agent-skills | `skills/arch-robot-architecture` | re-filed 2026-11-25 |
| `safety-systems` | 1124 | Humble | robotics-agent-skills | `skills/arch-safety` | re-filed 2026-11-25 |
| `robot-bringup` | 1190 | Humble, Jazzy | robotics-agent-skills | `skills/ops-bringup` | re-filed 2026-11-25, with the agent steps of `guides/robot-bringup.md` |
| `deployment-fleet` | 1417 | Jazzy | — | `skills/ops-fleet` | re-filed 2026-11-25 |
| `docker-ros2-ci` | 948 | Humble, Jazzy | robotics-agent-skills | `skills/ops-docker-ci` | re-filed 2026-11-18 |

## Guides, rules, commands, scripts

| Old file | Lines | Destination | Action |
|---|---|---|---|
| `guides/robot-bringup.md` | 390 | `playbooks/` + `skills/ops-bringup` | agent steps merged into `skills/ops-bringup` 2026-11-25; the checklist waits for Phase 6 |
| `guides/hardware-integration.md` | 675 | `playbooks/` | re-file in Phase 6 |
| `guides/sensor-calibration.md` | 424 | `playbooks/` | re-file in Phase 6 |
| `guides/sim-to-real-pipeline.md` | 311 | `skills/sim-to-real` | re-filed 2026-11-19 (merged) |
| `guides/production-deployment.md` | 692 | `playbooks/` | re-file in Phase 6; neutral example |
| `guides/testing-strategy.md` | 965 | `playbooks/` | re-file in Phase 6; absorb `rules/robotics-testing.md`; neutral example |
| `rules/ros2-general.md`, `ros2-nodes.md`, `ros2-communication.md` | 188 | `.claude/rules/` | re-file in the Phase 5 cleanup |
| `rules/robotics-testing.md` | 54 | `playbooks/` testing | merge in Phase 6 |
| `rules/clean-architecture.md`, `robot-specific.md` | 69 | `.claude/rules/` or drop | decide on review in the Phase 5 cleanup |
| `commands/ros2.md` | 74 | `wiki/tools/ros2.md` (CLI reference) | re-filed 2026-11-18 |
| `scripts/validate-skills.py` | 184 | `tools/lint.py` | replaced by `tools/lint.py` (Phase 1); delete in the Phase 5 cleanup |
| `README.md`, `CONTRIBUTING.md` | — | — | superseded by the new README, AGENTS.md and CONTRIBUTING.md; delete in the Phase 5 cleanup |

All `rules/` files and `commands/ros2.md` were adapted from ros2-claude-code-template.

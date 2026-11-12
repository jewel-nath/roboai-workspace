# Legacy audit

Audited 2026-11-12, in Phase 0 of the [plan](plan.md). The old "Agentic Robotics" layout now sits in
[`legacy/`](../legacy/), moved with `git mv` so its history follows it. This page records what is
there, what is wrong with it today, and where each piece goes. The re-filing itself happens in
Phase 2; nothing new is added to `legacy/`.

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

| Old skill | Lines | Distros named | Source | Destination | Action |
|---|---|---|---|---|---|
| `ros2` | 704 | Humble | robotics-agent-skills | `skills/ros2-core` | re-file |
| `ros2-control` | 621 | Humble | — | `skills/ros2-control` | re-file |
| `ros2-web-bridge` | 1072 | — | robotics-agent-skills | `skills/ros2-web-bridge` | re-file, neutral example |
| `robot-modeling` | 594 | — | — | `skills/ros2-robot-description` | re-file |
| `gazebo` | 599 | Humble | — | `skills/sim-gazebo` | re-file; Classic → migration note |
| `mujoco` | 988 | — | — | `skills/sim-mujoco` | merge with OrbiBot's `mujoco-sim` |
| `isaac-sim` | 676 | Humble | — | `wiki/tools/isaac-sim.md` | to wiki (documented tier) |
| `sim-to-real` | 550 | Humble, Jazzy | — | `skills/sim-to-real` | merge with `guides/sim-to-real-pipeline.md`, neutral example |
| `camera-vision` | 557 | Humble | robotics-agent-skills | `skills/perception-camera` | re-file |
| `lidar-pointcloud` | 687 | — | robotics-agent-skills | `skills/perception-lidar` | re-file |
| `sensor-fusion-slam` | 779 | — | — | `skills/perception-slam` | re-file |
| `nav2` | 845 | — | — | `skills/nav-nav2` | re-file |
| `path-planning` | 833 | — | — | `skills/nav-planning` | re-file |
| `moveit2` | 947 | Humble | — | `skills/manip-moveit2` | re-file |
| `grasping-force-control` | 953 | Humble | — | `skills/manip-grasping` | re-file |
| `control-systems` | 788 | — | — | `skills/control-systems` + `wiki/concepts/` | re-file; owns PID |
| `realtime-motor-control` | 909 | Humble | — | `skills/fw-motor-control` | re-file; PID → link to `control-systems` |
| `microcontrollers` | 886 | — | — | `skills/fw-mcu` | re-file |
| `gpio-i2c-spi` | 1265 | — | — | `skills/fw-peripherals` | re-file, neutral example |
| `serial-can-protocols` | 1141 | Humble | — | `skills/fw-serial-can` | re-file |
| `rtos-micro-ros` | 1140 | Jazzy | — | `skills/fw-rtos-micro-ros` | re-file, neutral example |
| `sensor-actuator-drivers` | 1267 | Jazzy | — | `skills/fw-drivers` | re-file; PID → link |
| `learning-robotics` | 1131 | — | — | `skills/learn-robot-learning` | re-file, neutral example |
| `edge-ml-deployment` | 1080 | Jazzy | — | `skills/learn-edge-deployment` | re-file, neutral example |
| `robot-architecture` | 1316 | Humble, Jazzy | robotics-agent-skills | `skills/arch-robot-architecture` | re-file, neutral example |
| `safety-systems` | 1124 | Humble | robotics-agent-skills | `skills/arch-safety` | re-file, neutral example |
| `robot-bringup` | 1190 | Humble, Jazzy | robotics-agent-skills | `skills/ops-bringup` | merge with `guides/robot-bringup.md`, neutral example |
| `deployment-fleet` | 1417 | Jazzy | — | `skills/ops-fleet` | re-file; most OrbiBot examples |
| `docker-ros2-ci` | 948 | Humble, Jazzy | robotics-agent-skills | `skills/ops-docker-ci` | re-file, neutral example |

## Guides, rules, commands, scripts

| Old file | Lines | Destination | Action |
|---|---|---|---|
| `guides/robot-bringup.md` | 390 | `playbooks/` + `skills/ops-bringup` | merge |
| `guides/hardware-integration.md` | 675 | `playbooks/` | re-file |
| `guides/sensor-calibration.md` | 424 | `playbooks/` | re-file |
| `guides/sim-to-real-pipeline.md` | 311 | `skills/sim-to-real` | merge |
| `guides/production-deployment.md` | 692 | `playbooks/` | re-file; neutral example |
| `guides/testing-strategy.md` | 965 | `playbooks/` | re-file; absorb `rules/robotics-testing.md`; neutral example |
| `rules/ros2-general.md`, `ros2-nodes.md`, `ros2-communication.md` | 188 | `.claude/rules/` | re-file |
| `rules/robotics-testing.md` | 54 | `playbooks/` testing | merge |
| `rules/clean-architecture.md`, `robot-specific.md` | 69 | `.claude/rules/` or drop | decide on review |

All `rules/` files and `commands/ros2.md` were adapted from ros2-claude-code-template.
| `commands/ros2.md` | 74 | `wiki/tools/ros2.md` (CLI reference) | re-file |
| `scripts/validate-skills.py` | 184 | `tools/lint/` | replaced by the Phase 1 lint |
| `README.md`, `CONTRIBUTING.md` | — | — | superseded by the new README, AGENTS.md and CONTRIBUTING.md |

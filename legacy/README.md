> **Legacy.** This is the README of the old "Agentic Robotics" layout, kept with its content while
> RoboAI Workspace is redesigned. Each item here is re-filed, merged or dropped in Phases 4–5, as
> [docs/legacy-audit.md](../docs/legacy-audit.md) records. Do not add to this folder.

# 🤖 Agentic Robotics

> A curated skill library for AI assistants helping robotics engineers.
> Works with Claude Code, Cursor, or any AI tool that can read Markdown files.

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

## Quick Start

```bash
# Clone the repository
git clone https://github.com/jewel-nath/agentic-robotics.git
cd agentic-robotics

# Use with Cursor: list skill paths in a rule, .cursor/rules/robotics.mdc
# /path/to/agentic-robotics/skills/ros2/SKILL.md
# /path/to/agentic-robotics/skills/nav2/SKILL.md

# Use with Claude Code
# Reference in your project's CLAUDE.md:
# When working on ROS2, read /path/to/agentic-robotics/skills/ros2/SKILL.md
```

## What is This?

A skill library covering the robotics stack, from ROS 2 and simulation to embedded and deployment:

- **29 consolidated skills** — Each skill is substantial (500-3000 lines), covering a complete domain
- **Tool-agnostic** — Plain markdown with YAML frontmatter, consumable by any AI tool
- **Real-world focus** — Anti-patterns and failure modes alongside example code
- **Progressive disclosure** — Quick start at top, deep reference below

## Project Status

Status as of March 2026, when the skills were last updated:

### ✅ Completed (Phase 1-5)
- **Phase 1** (Foundation): ros2, robot-modeling, gazebo, camera-vision, ros2-control ✓
- **Phase 2** (Navigation): nav2, sensor-fusion-slam, path-planning, lidar-pointcloud, control-systems ✓
- **Phase 3** (Manipulation & Hardware): moveit2, grasping-force-control, serial-can-protocols, microcontrollers, realtime-motor-control ✓
- **Phase 4** (AI & Advanced): isaac-sim, mujoco, sim-to-real, learning-robotics, edge-ml-deployment, robot-architecture, safety-systems ✓
- **Phase 5** (Embedded, DevOps & Production): gpio-i2c-spi, sensor-actuator-drivers, rtos-micro-ros, deployment-fleet, robot-bringup, ros2-web-bridge, docker-ros2-ci ✓
- **Phase 5 Guides**: production-deployment.md, testing-strategy.md ✓

### 🚧 Remaining
- **Templates**: Starter templates for ROS2 packages, URDF, Docker

## Skill Catalog

### Core Middleware
| Skill | Description | Status |
|-------|-------------|--------|
| [ros2](../skills/ros2-core/SKILL.md) (re-filed as `ros2-core`) | ROS2 development: nodes, topics, services, actions, launch files, QoS, lifecycle, DDS | ✅ |
| [ros2-control](../skills/ros2-control/SKILL.md) (re-filed) | ros2_control framework: hardware interfaces, controllers, transmissions | ✅ |
| [ros2-web-bridge](../skills/ros2-web-bridge/SKILL.md) (re-filed) | Web integration: rosbridge, FastAPI, WebSocket streaming, REST APIs | ✅ |
| [robot-modeling](../skills/ros2-robot-description/SKILL.md) (re-filed as `ros2-robot-description`) | URDF, Xacro, TF2 transforms, robot state publisher | ✅ |

### Simulation
| Skill | Description | Status |
|-------|-------------|--------|
| [gazebo](../skills/sim-gazebo/SKILL.md) (re-filed as `sim-gazebo`) | Gazebo Classic & Sim: SDF worlds, plugins, physics, sensor models | ✅ |
| [isaac-sim](../wiki/tools/isaac-sim.md) (re-filed as a wiki page) | NVIDIA Isaac Sim: USD format, photorealistic rendering, synthetic data | ✅ |
| [mujoco](skills/mujoco/SKILL.md) | MuJoCo physics: contact modeling, MJCF, optimal control | ✅ |
| [sim-to-real](../skills/sim-to-real/SKILL.md) (re-filed) | Domain transfer: reality gap, domain adaptation, validation | ✅ |

### Perception
| Skill | Description | Status |
|-------|-------------|--------|
| [camera-vision](../skills/perception-camera/SKILL.md) (re-filed as `perception-camera`) | Camera calibration, OpenCV, detection, tracking, depth pipelines | ✅ |
| [lidar-pointcloud](../skills/perception-lidar/SKILL.md) (re-filed as `perception-lidar`) | PCL, Open3D, filtering, registration, ICP, segmentation | ✅ |
| [sensor-fusion-slam](../skills/perception-slam/SKILL.md) (re-filed as `perception-slam`) | Multi-sensor fusion, EKF, ORB-SLAM3, RTAB-Map, Cartographer | ✅ |

### Navigation
| Skill | Description | Status |
|-------|-------------|--------|
| [nav2](../skills/nav-nav2/SKILL.md) (re-filed as `nav-nav2`) | Nav2 stack: behavior trees, planners, controllers, recovery | ✅ |
| [path-planning](../skills/nav-planning/SKILL.md) (re-filed as `nav-planning`) | A*, RRT, costmaps, waypoint following, coverage planning | ✅ |

### Manipulation
| Skill | Description | Status |
|-------|-------------|--------|
| [moveit2](../skills/manip-moveit2/SKILL.md) (re-filed as `manip-moveit2`) | Motion planning, collision checking, trajectory execution | ✅ |
| [grasping-force-control](../skills/manip-grasping/SKILL.md) (re-filed as `manip-grasping`) | Grasp synthesis, F/T sensing, impedance control, pick-and-place | ✅ |

### Control
| Skill | Description | Status |
|-------|-------------|--------|
| [control-systems](skills/control-systems/SKILL.md) | PID, LQR, MPC, state-space, system identification, trajectories | ✅ |
| [realtime-motor-control](skills/realtime-motor-control/SKILL.md) | Motor types, PID tuning, FOC, encoders, PREEMPT_RT, deterministic loops | ✅ |

### Hardware Interfaces
| Skill | Description | Status |
|-------|-------------|--------|
| [serial-can-protocols](../skills/fw-serial-can/SKILL.md) (re-filed as `fw-serial-can`) | UART, RS485, CAN 2.0, CANopen, J1939, EtherCAT | ✅ |
| [gpio-i2c-spi](skills/gpio-i2c-spi/SKILL.md) | GPIO, PWM, interrupts, I2C, SPI protocols on Linux/RPi | ✅ |
| [sensor-actuator-drivers](skills/sensor-actuator-drivers/SKILL.md) | Custom ROS2 driver development: IMU, encoder, motor, servo | ✅ |

### Embedded Systems
| Skill | Description | Status |
|-------|-------------|--------|
| [microcontrollers](../skills/fw-mcu/SKILL.md) (re-filed as `fw-mcu`) | STM32, ESP32, nRF52, HAL patterns, DMA, interrupts, bootloaders | ✅ |
| [rtos-micro-ros](../skills/fw-rtos-micro-ros/SKILL.md) (re-filed as `fw-rtos-micro-ros`) | FreeRTOS task scheduling, micro-ROS on STM32/ESP32, real-time patterns | ✅ |

### AI & Learning
| Skill | Description | Status |
|-------|-------------|--------|
| [learning-robotics](../skills/learn-robot-learning/SKILL.md) (re-filed as `learn-robot-learning`) | Imitation learning, RL for robotics, VLA models | ✅ |
| [edge-ml-deployment](../skills/learn-edge-deployment/SKILL.md) (re-filed as `learn-edge-deployment`) | TensorRT, ONNX, quantization, Jetson, data pipelines | ✅ |

### Architecture & Safety
| Skill | Description | Status |
|-------|-------------|--------|
| [robot-architecture](../skills/arch-robot-architecture/SKILL.md) (re-filed as `arch-robot-architecture`) | Design patterns, BT/FSM, state estimation, multi-robot | ✅ |
| [safety-systems](../skills/arch-safety/SKILL.md) (re-filed as `arch-safety`) | Watchdogs, E-stops, SROS2, ISO 10218 risk assessment, IEC 60204 stop categories and ISO 13849 levels | ✅ |

### DevOps & Production
| Skill | Description | Status |
|-------|-------------|--------|
| [robot-bringup](../skills/ops-bringup/SKILL.md) (re-filed as `ops-bringup`) | systemd, layered launch, udev, watchdog, production bringup | ✅ |
| [docker-ros2-ci](../skills/ops-docker-ci/SKILL.md) (re-filed as `ops-docker-ci`) | Docker builds, docker-compose, DDS in containers, CI with colcon | ✅ |
| [deployment-fleet](../skills/ops-fleet/SKILL.md) (re-filed as `ops-fleet`) | OTA updates, fleet management, centralized logging, diagnostics | ✅ |

## Commands

Quick CLI reference for daily use and AI-assisted workflows:

| File | Description |
|------|-------------|
| [commands/ros2.md](../wiki/tools/ros2.md) (re-filed into the ROS 2 page) | colcon build/test, `ros2 node/topic/service/action/param`, rqt, tf2_tools, ros2 doctor |

## Rules

Project-wide conventions and always-on rules for ROS2 and robotics projects. Use in Cursor rules, Claude project instructions, or as team standards:

| File | Description |
|------|-------------|
| [rules/ros2-general.md](rules/ros2-general.md) | Package naming, file structure, launch, params, logging |
| [rules/ros2-nodes.md](rules/ros2-nodes.md) | Node design: parameters first, pub/sub order, QoS, lifecycle |
| [rules/ros2-communication.md](rules/ros2-communication.md) | Topic naming, QoS selection, message/service packages, TF2 |
| [rules/robotics-testing.md](rules/robotics-testing.md) | Unit, integration, launch tests; pytest, launch_testing |
| [rules/clean-architecture.md](rules/clean-architecture.md) | Optional: domain / application / infrastructure layers |
| [rules/robot-specific.md](rules/robot-specific.md) | Optional: URDF, TF tree, Nav2, sensor/motor patterns |

## Usage

### With Cursor IDE

Create a rule, `.cursor/rules/robotics.mdc`, in your project (Cursor reads `.mdc` rules only):

```markdown
---
description: ROS 2 and Nav2 work
alwaysApply: false
---
When working on ROS 2 navigation, read:
- /path/to/agentic-robotics/skills/ros2/SKILL.md
- /path/to/agentic-robotics/skills/nav2/SKILL.md
```

### With Claude Code

Reference skills in your project's `CLAUDE.md`:

```markdown
## ROS2 Development Guidelines

When the user asks about ROS2, read and follow:
- /path/to/agentic-robotics/skills/ros2/SKILL.md

When working on robot perception:
- /path/to/agentic-robotics/skills/camera-vision/SKILL.md
- /path/to/agentic-robotics/skills/sensor-fusion-slam/SKILL.md
```

### With Any AI Tool

Skills are plain markdown. Copy the content into your context, or configure your tool to read the file when relevant topics come up.

### Manual Reference

Skills are well-structured documentation. Engineers can read them directly.

## Guides

Multi-skill workflow guides:

| Guide | Description | Status |
|-------|-------------|--------|
| [Robot Bringup](guides/robot-bringup.md) | First power-on checklist | ✅ |
| [Sensor Calibration](guides/sensor-calibration.md) | End-to-end calibration workflow | ✅ |
| [Hardware Integration](guides/hardware-integration.md) | Wiring to first ROS2 topic | ✅ |
| [Sim-to-Real Pipeline](../skills/sim-to-real/SKILL.md) (merged into `sim-to-real`) | Full sim-to-real transfer | ✅ |
| [Production Deployment](guides/production-deployment.md) | Pre-deployment checklist, staging, rollback | ✅ |
| [Testing Strategy](guides/testing-strategy.md) | Unit → integration → sim → HIL → field testing | ✅ |

## Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for:
- Skill format specification
- How to add a new skill
- Code review process
- Style guide

## Design Principles

1. **Flat and discoverable** — Two-level hierarchy (`skills/<name>/SKILL.md`)
2. **Consolidated skills** — Substantial references (~500-3000 lines), no thin stubs
3. **Tool-agnostic** — Plain markdown with YAML frontmatter
4. **Real-world focus** — Anti-patterns and failure modes documented
5. **Progressive disclosure** — Quick start at top, deep reference below

## Credits

Parts of this library are adapted from two Apache 2.0 projects:

- [robotics-agent-skills](https://github.com/arpitg1304/robotics-agent-skills),
  by arpitg1304 and its contributors: material in the `ros2`,
  `camera-vision`, `lidar-pointcloud`, `safety-systems`,
  `robot-architecture`, `robot-bringup`, `ros2-web-bridge` and
  `docker-ros2-ci` skills.
- [ros2-claude-code-template](https://github.com/harunkurtdev/ros2-claude-code-template),
  by harunkurtdev: `commands/ros2.md` and the files in `rules/`.

The material was renamed, merged into larger skills and rewritten in
places. [NOTICE](../NOTICE) lists what came from where. Many of the worked
examples use my robot, OrbiBot V1.

## License

Apache 2.0: see [LICENSE](../LICENSE) and [NOTICE](../NOTICE).

## References

- [ROS2](https://github.com/ros2)
- [MoveIt 2](https://moveit.ai)
- [Nav2](https://docs.nav2.org)
- [OpenCV](https://opencv.org)
- [PCL](https://pointclouds.org)
- [Gazebo](https://gazebosim.org)
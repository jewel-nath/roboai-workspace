---
type: tool
name: Webots
summary: Apache-2.0 desktop robot simulator from Cyberbotics, with ready robot models, controllers in Python or C/C++, and official ROS 2 packages (webots_ros2) released from Humble to Lyrical.
tags: [simulator, webots, cyberbotics, webots-ros2, wbt, proto, controllers, education, ros2, headless]
kind: tool
area: sim
support: documented
license: Apache-2.0
links: {repo: "https://github.com/cyberbotics/webots", docs: "https://cyberbotics.com/doc/guide/index", site: "https://cyberbotics.com"}
version: {tested: , latest: R2025a, as_of: 2026-11-19}
platforms: [linux, windows, macos]
agent_access: script
registry:
evidence: researched
last_verified: 2026-11-19
sources:
  - {url: "https://github.com/cyberbotics/webots", title: "Webots repository: README, LICENSE, releases, develop history and docs/reference", accessed: 2026-11-19}
  - {url: "https://cyberbotics.com/doc/guide/system-requirements", title: "Webots User Guide: System requirements", accessed: 2026-11-19}
  - {url: "https://cyberbotics.com/doc/guide/installation-procedure", title: "Webots User Guide: Installation procedure", accessed: 2026-11-19}
  - {url: "https://cyberbotics.com/doc/guide/running-extern-robot-controllers", title: "Webots User Guide: Running extern robot controllers", accessed: 2026-11-19}
  - {url: "https://cyberbotics.com/doc/guide/using-python", title: "Webots User Guide: Using Python", accessed: 2026-11-19}
  - {url: "https://github.com/cyberbotics/webots_ros2", title: "webots_ros2 repository: README, package.xml files, driver utils.py and importer", accessed: 2026-11-19}
  - {url: "https://github.com/ros/rosdistro", title: "rosdistro: humble, jazzy, kilted and lyrical distribution.yaml (webots_ros2)", accessed: 2026-11-19}
---

# Webots

An Apache-2.0 desktop simulator for robots and vehicles, maintained by Cyberbotics [1]. A world
(`.wbt`) holds robots built from PROTO models, each run by a controller in Python, C/C++, Java or
MATLAB [4]. Builders use it to teach and to try a robot before hardware, often through ROS 2.

## When to use it

For teaching, and for robots with `webots_ros2` examples: TurtleBot3 Burger, TIAGo, UR arms,
e-puck, Husarion ROSbots, Mavic, Crazyflie [6]. Otherwise: [Gazebo](gazebo.md) for ROS 2 work,
[MuJoCo](mujoco.md) for contact-rich learning, Isaac Lab on [Isaac Sim](isaac-sim.md) for GPU RL.

## Setup

Newest stable release **R2025a**, 2025-02-04; nightly builds continue [1]. On Ubuntu 24.04 [3]:

```bash
sudo mkdir -p /etc/apt/keyrings && sudo wget -q -P /etc/apt/keyrings https://cyberbotics.com/Cyberbotics.asc
echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/Cyberbotics.asc] https://cyberbotics.com/debian binary-amd64/" | sudo tee /etc/apt/sources.list.d/Cyberbotics.list
sudo apt update && sudo apt install webots ros-jazzy-webots-ros2
```

Linux x86-64 (Ubuntu 22.04+), Windows 10/11 `.exe`, macOS 12–14 `.dmg` (Apple silicon, Intel),
Docker `cyberbotics/webots` [1][2][3]. Advised GPU: OpenGL 3.3, NVIDIA or AMD (Linux: NVIDIA only),
not Intel [2]. Python 3.8+ [5]. `webots_ros2` 2025.0.x is out for Humble–Lyrical [7], needs R2025a+;
try `ros2 launch webots_ros2_universal_robot multirobot_launch.py` [6].

## How an agent works with it

A Python controller does `from controller import Robot` and loops on `robot.step(timestep)`,
which returns -1 when Webots ends it; a `Supervisor` can reset the world and end the run with
`simulationQuit(status)`, a CI exit code [1][5]. Headless: `xvfb-run --auto-servernum webots
--mode=fast --no-rendering --batch --stdout --stderr --minimize world.wbt` [3]. An `<extern>`
robot takes commands from your own process, run by `$WEBOTS_HOME/webots-controller ctrl.py` [4].
`webots_ros2_importer` turns URDF or xacro into PROTO [6]; see [URDF](../software/urdf.md).

## Traps

- **It needs a display.** Even with `--no-rendering`, run it under `xvfb-run` on servers and in
  CI; `--batch` stops pop-ups that would block a scripted run [3].
- **`webots_ros2` may stop to ask.** If it finds no R2025a+, it asks on the terminal to download
  Webots and an unattended launch hangs; set `WEBOTS_HOME`, which skips the version check [6].
- **The snap is sealed.** Its controllers cannot use your pip packages: run them as extern
  controllers, or install the `.deb` [3].
- **A frozen world may be waiting.** An `<extern>` robot with `synchronization` TRUE waits for its
  controller; with several Webots instances, pass `--port` to reach the right one [4].
- **Old release.** Commits land weekly (to November 2026), but R2025a is still the newest stable;
  its guide lists Ubuntu 22.04 and 24.04, and only the `master` guide adds 26.04 for Lyrical [1][2].

## Alternatives

[Gazebo](gazebo.md), [MuJoCo](mujoco.md), [Isaac Sim](isaac-sim.md), [CoppeliaSim](coppeliasim.md),
[PyBullet](pybullet.md), [Genesis](genesis.md), [CARLA](carla.md) for cars; see
[Choose a simulator](../guides/choose-a-simulator.md).

## Sources

1. [Webots repository: README, LICENSE, releases, develop history and docs/reference](https://github.com/cyberbotics/webots), accessed 2026-11-19
2. [Webots User Guide: System requirements](https://cyberbotics.com/doc/guide/system-requirements), accessed 2026-11-19
3. [Webots User Guide: Installation procedure](https://cyberbotics.com/doc/guide/installation-procedure), accessed 2026-11-19
4. [Webots User Guide: Running extern robot controllers](https://cyberbotics.com/doc/guide/running-extern-robot-controllers), accessed 2026-11-19
5. [Webots User Guide: Using Python](https://cyberbotics.com/doc/guide/using-python), accessed 2026-11-19
6. [webots_ros2 repository: README, package.xml files, driver utils.py and importer](https://github.com/cyberbotics/webots_ros2), accessed 2026-11-19
7. [rosdistro: humble, jazzy, kilted and lyrical distribution.yaml (webots_ros2)](https://github.com/ros/rosdistro), accessed 2026-11-19

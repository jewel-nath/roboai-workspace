---
type: tool
name: CARLA
summary: Open-source self-driving simulator on Unreal Engine with a Python client API, ROS 2 output from the server, traffic and ScenarioRunner; 1.0 (UE 5.8, November 2026) replaces the 0.9.x (UE 4.26) line.
tags: [simulator, carla, autonomous-driving, unreal-engine, python-api, ros2, scenario-runner, autoware, lidar, traffic]
kind: tool
area: sim
support: documented
license: MIT
links: {repo: "https://github.com/carla-simulator/carla", docs: "https://carla-ue5.readthedocs.io/en/latest/", site: "https://carla.org"}
version: {tested: , latest: "1.0", as_of: 2026-11-19}
platforms: [linux, windows]
agent_access: script
registry:
evidence: researched
last_verified: 2026-11-19
sources:
  - {url: "https://github.com/carla-simulator/carla", title: "CARLA repository: README, LICENSE, releases (1.0 notes), Docs, AGENTS.md and Skills/", accessed: 2026-11-19}
  - {url: "https://carla-ue5.readthedocs.io/en/latest/start_quickstart/", title: "CARLA 1.0 docs: Quick start", accessed: 2026-11-19}
  - {url: "https://carla-ue5.readthedocs.io/en/latest/ros2_native/", title: "CARLA 1.0 docs: ROS 2 native interface", accessed: 2026-11-19}
  - {url: "https://carla-ue5.readthedocs.io/en/latest/core_synchrony/", title: "CARLA 1.0 docs: Synchrony and time-step", accessed: 2026-11-19}
  - {url: "https://carla-ue5.readthedocs.io/en/latest/scenario_runner/", title: "CARLA 1.0 docs: ScenarioRunner", accessed: 2026-11-19}
  - {url: "https://carla.readthedocs.io/en/latest/start_quickstart/", title: "CARLA 0.9.x docs: Quick start", accessed: 2026-11-19}
  - {url: "https://pypi.org/project/carla/", title: "PyPI: carla release history", accessed: 2026-11-19}
  - {url: "https://github.com/carla-simulator/ros-bridge", title: "carla-ros-bridge repository: commit history", accessed: 2026-11-19}
---

# CARLA

An open self-driving simulator on Unreal Engine from the CVC at UAB: code MIT, CARLA's assets CC-BY,
Unreal Engine under its own terms [1]. Python clients spawn vehicles and sensors (camera, lidar,
radar, GNSS, IMU) in its towns and drive them; Autoware users test full stacks in it [1][3].

## When to use it

For cars on roads: driving stacks, traffic scenarios, perception data; for small robots use
[Gazebo](gazebo.md), [Isaac Sim](isaac-sim.md) or [MuJoCo](mujoco.md). Start on **1.0** (UE 5.8,
2026-11-17, replacing UE5's 0.10.0); the 0.9.x line (last 0.9.16, UE 4.26) is obsolete [1].

## Setup

1.0: Ubuntu 22.04/24.04 or Windows 11; NVIDIA RTX 3000+ with 16 GB VRAM and driver 550+ (Linux),
560+ (Windows) or 570+ (RTX 50); 32 GB RAM; 225 GB disk; ports 2000–2002 [1][2]. 0.9.x: 8 GB VRAM,
~20 GB, Ubuntu 20.04/22.04, Windows 10/11, Python 3.7–3.12 [6]. Ubuntu 24.04 [2]:

```bash
tar -xzf CARLA_1.0.tar.gz && cd Carla-*-Linux-Shipping   # from the 1.0 release page
python3 -m venv ~/carla-env && . ~/carla-env/bin/activate
pip install PythonAPI/carla/dist/carla-*-cp312-*.whl       # wheel tag must match your Python
./CarlaUnreal.sh -RenderOffScreen                            # add -ros2 for ROS 2 topics
```

Wheels: Python 3.10–3.15. Docker image: `carlasim/carla:1.0`. `-nullrhi` runs with no GPU [2].

## How an agent works with it

`carla.Client('localhost', 2000)`; for repeatable runs set `synchronous_mode = True` and
`fixed_delta_seconds = 0.05` in the world settings, then call `world.tick()` each step [4]. With
`-ros2` the server publishes sensors, `/clock` and `/tf` for any ROS 2 distro (Linux only; `--rmw=`
picks Fast DDS, Cyclone DDS or Zenoh); a `hero` car takes `/carla/<ros_name>/vehicle_control_cmd`
[3]. ScenarioRunner is a separate client: branch `ue58-dev` for 1.0, `master` for 0.9.x [5]. CARLA
ships 64 agent skills, `AGENTS.md` and an MCP server (`.mcp.json`) [1]; review before enabling.

## Traps

- **`pip install carla` gets 0.9.16.** That UE4 client cannot reach a 1.0 server, though the 1.0
  quick start says PyPI has 1.0 [2][7]. Install the package's wheel; versions must match [2].
- **A dead sync client freezes the world.** The server waits for ticks; `PythonAPI/util/config.py
  --no-sync` frees it. Put the Traffic Manager in sync mode too [4].
- **Topics listed, no data.** Shared memory fails silently across users, containers or Humble, so
  1.0 sends UDP only; big camera and lidar samples then overflow default socket buffers (2 Hz, not
  10): raise `net.core.rmem_max` to 16 MB, use the `PythonAPI/examples/ros2/config/` profiles [3].
- **Lines do not mix.** Towns, blueprints and scenarios differ between 0.9.x and 1.0 [5];
  carla-ros-bridge targets 0.9.13 and was last changed in July 2022 [8].
- **Windows fails without a word** if the x64 Visual C++ Redistributable is missing [2].

## Alternatives

[Gazebo](gazebo.md), [Isaac Sim](isaac-sim.md), [Webots](webots.md), [MuJoCo](mujoco.md); AirSim.

## Sources

1. [CARLA repository: README, LICENSE, releases (1.0 notes), Docs, AGENTS.md and Skills/](https://github.com/carla-simulator/carla), accessed 2026-11-19
2. [CARLA 1.0 docs: Quick start](https://carla-ue5.readthedocs.io/en/latest/start_quickstart/), accessed 2026-11-19
3. [CARLA 1.0 docs: ROS 2 native interface](https://carla-ue5.readthedocs.io/en/latest/ros2_native/), accessed 2026-11-19
4. [CARLA 1.0 docs: Synchrony and time-step](https://carla-ue5.readthedocs.io/en/latest/core_synchrony/), accessed 2026-11-19
5. [CARLA 1.0 docs: ScenarioRunner](https://carla-ue5.readthedocs.io/en/latest/scenario_runner/), accessed 2026-11-19
6. [CARLA 0.9.x docs: Quick start](https://carla.readthedocs.io/en/latest/start_quickstart/), accessed 2026-11-19
7. [PyPI: carla release history](https://pypi.org/project/carla/), accessed 2026-11-19
8. [carla-ros-bridge repository: commit history](https://github.com/carla-simulator/ros-bridge), accessed 2026-11-19

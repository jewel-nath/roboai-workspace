---
type: tool
name: CoppeliaSim
summary: Long-standing robot simulator from Coppelia Robotics (formerly V-REP) with five physics engines, Lua and Python scene scripts, a ZeroMQ remote API and a ROS 2 plugin; the free Edu build is for schools and universities only.
tags: [simulator, coppeliasim, v-rep, zeromq, remote-api, simros2, lua, python, education, urdf, sdf]
kind: tool
area: sim
support: documented
license: GPL-3.0-or-later
links: {repo: "https://github.com/CoppeliaRobotics/CoppeliaSimLib", docs: "https://manual.coppeliarobotics.com", site: "https://www.coppeliarobotics.com"}
version: {tested: , latest: 4.10.0 rev0, as_of: 2026-11-19}
platforms: [linux, windows, macos]
agent_access: script
registry:
evidence: researched
last_verified: 2026-11-19
sources:
  - {url: "https://www.coppeliarobotics.com", title: "CoppeliaSim website: editions, Edu terms and downloads", accessed: 2026-11-19}
  - {url: "https://manual.coppeliarobotics.com/en/versionInfo.htm", title: "CoppeliaSim manual: Version history", accessed: 2026-11-19}
  - {url: "https://github.com/CoppeliaRobotics/CoppeliaSimLib", title: "CoppeliaSimLib repository: license.txt, tags and commit history", accessed: 2026-11-19}
  - {url: "https://github.com/CoppeliaRobotics/zmqRemoteApi", title: "zmqRemoteApi repository: licence, Python client README and pyproject, PROTOCOL.md", accessed: 2026-11-19}
  - {url: "https://manual.coppeliarobotics.com/en/commandLine.htm", title: "CoppeliaSim manual: Commands and settings", accessed: 2026-11-19}
  - {url: "https://manual.coppeliarobotics.com/en/ros2Tutorial.htm", title: "CoppeliaSim manual: ROS 2 tutorial", accessed: 2026-11-19}
  - {url: "https://github.com/CoppeliaRobotics/simROS2", title: "simROS2 repository: README and licence", accessed: 2026-11-19}
  - {url: "https://manual.coppeliarobotics.com/en/importExport.htm", title: "CoppeliaSim manual: Import/export", accessed: 2026-11-19}
---

# CoppeliaSim

A general robot simulator from Coppelia Robotics, formerly V-REP [1]. Scenes carry Lua or Python
scripts, physics runs on MuJoCo, Bullet, ODE, Vortex or Newton, and programs drive it over a ZeroMQ
remote API or ROS 2 [1][4][6]. Builders use it in courses and to try arm and mobile-robot ideas.

**Licence.** The core, CoppeliaSimLib, is GPL-3.0-or-later on GitHub, and scripts and plugins may
use any licence [3]; the remote API and ROS 2 plugin are BSD-3-Clause [4][7]. Downloads have their
own terms [1]: **Edu** is free only for students, teachers and professors of schools and
universities, not for companies, research institutes or non-profits, and never commercially;
**Pro** is paid; **Lite**, on request, is commercial with less editing. The site lists no Player.

## When to use it

Use it when the Edu terms fit or you hold Pro, and want one tool with scene scripting, IK and a
choice of physics engines. Otherwise: [Gazebo](gazebo.md) for open ROS 2 work, [Webots](webots.md)
to teach outside a university, [MuJoCo](mujoco.md) for learning.

## Setup

Newest release **4.10.0 rev0**, 2025-05-14; 4.11 is in development, with core commits to November
2026 [2][3]. Downloads only: Ubuntu 22.04 and 24.04 (x86-64), Windows, macOS 13+ Intel, macOS 15+
Apple silicon; on Ubuntu, extract the `.tar.xz` and run `./coppeliaSim.sh` [1][5]. No GPU need is
stated. Client: `python3 -m pip install coppeliasim-zmqremoteapi-client` (Python 3.8+) [4].

## How an agent works with it

`sim = RemoteAPIClient().require('sim')` (port 23000) reaches the whole `sim.*` API and plugin APIs;
`sim.setStepping(True)`, `sim.startSimulation()`, then `sim.step()` per step [4]. Clients exist for
C++, Java, MATLAB and Octave too [4]. Batch run: `./coppeliaSim.sh -h -s5000 -q scene.ttt` hides
the GUI, simulates 5 s and quits [5]. Scenes are `.ttt`, models `.ttm`, or XML; add-ons import
URDF and SDF and export URDF [5][8]. ROS 2: copy `compiledROSPlugins/libsimROS2.so` into the
CoppeliaSim folder, source ROS 2, start it; `ros2 node list` should show `/sim_ros2_interface` [6].

## Traps

- **Old tutorials, old client.** Client 2.x speaks protocol 2 (CoppeliaSim 4.6+); 4.5.1 and older
  use protocol 1. Old code imports `zmqRemoteApi` and calls `client.getObject('sim')`; new code
  uses `coppeliasim_zmqremoteapi_client` and `client.require('sim')` [4].
- **It runs free unless you step it.** By default the simulation runs asynchronously to your
  client; for lock-step control, set stepping and call `sim.step()` [4].
- **simROS2 may not load.** The prebuilt plugin's distro is not stated and the README lists only
  Humble. If it fails, or you need more message types (`meta/interfaces.txt`), rebuild it with
  colcon for your distro with `ulimit -s unlimited`; if gcc fails on many types, use clang [6][7].
- **True headless loses cameras.** `-H` drops the GUI libraries but still needs a display server,
  and vision sensors then work only with POV-Ray rendering; `-h` just hides the GUI [5]. Keep a
  robot's meshes near 10,000–20,000 triangles in total, or the simulation slows down [8].

## Alternatives

[Webots](webots.md), [Gazebo](gazebo.md), [MuJoCo](mujoco.md), [Isaac Sim](isaac-sim.md),
[PyBullet](pybullet.md), [Genesis](genesis.md) ([how to choose](../guides/choose-a-simulator.md)).

## Sources

1. [CoppeliaSim website: editions, Edu terms and downloads](https://www.coppeliarobotics.com), accessed 2026-11-19
2. [CoppeliaSim manual: Version history](https://manual.coppeliarobotics.com/en/versionInfo.htm), accessed 2026-11-19
3. [CoppeliaSimLib repository: license.txt, tags and commit history](https://github.com/CoppeliaRobotics/CoppeliaSimLib), accessed 2026-11-19
4. [zmqRemoteApi repository: licence, Python client README and pyproject, PROTOCOL.md](https://github.com/CoppeliaRobotics/zmqRemoteApi), accessed 2026-11-19
5. [CoppeliaSim manual: Commands and settings](https://manual.coppeliarobotics.com/en/commandLine.htm), accessed 2026-11-19
6. [CoppeliaSim manual: ROS 2 tutorial](https://manual.coppeliarobotics.com/en/ros2Tutorial.htm), accessed 2026-11-19
7. [simROS2 repository: README and licence](https://github.com/CoppeliaRobotics/simROS2), accessed 2026-11-19
8. [CoppeliaSim manual: Import/export](https://manual.coppeliarobotics.com/en/importExport.htm), accessed 2026-11-19

---
type: tool
name: PyBullet
summary: Python bindings for the Bullet physics SDK; a CPU rigid-body simulator that loads URDF, SDF and MJCF and still runs many older learning repos and tutorials, but gets few updates and no new wheels.
tags: [simulator, physics, bullet, python, urdf, sdf, mjcf, reinforcement-learning, cpu, headless, egl]
kind: library
area: sim
support: documented
license: Zlib
links: {repo: "https://github.com/bulletphysics/bullet3", docs: "https://docs.google.com/document/d/10sXEhzFRSnvFcl3XxNGhnD4N2SedqwdAvK3dsihxVUA/edit", site: "https://pybullet.org"}
version: {tested: , latest: 3.2.7, as_of: 2026-11-19}
platforms: [linux, windows, macos]
agent_access: script
registry:
evidence: researched
last_verified: 2026-11-19
sources:
  - {url: "https://github.com/bulletphysics/bullet3", title: "Bullet repository: README, LICENSE.txt, setup.py, examples, commits, tags and releases", accessed: 2026-11-19}
  - {url: "https://pypi.org/project/pybullet/#files", title: "pybullet on PyPI: release history and wheel files", accessed: 2026-11-19}
  - {url: "https://anaconda.org/conda-forge/pybullet", title: "pybullet on conda-forge", accessed: 2026-11-19}
  - {url: "https://docs.google.com/document/d/10sXEhzFRSnvFcl3XxNGhnD4N2SedqwdAvK3dsihxVUA/edit", title: PyBullet Quickstart Guide, accessed: 2026-11-19}
  - {url: "https://www.ros.org/reps/rep-2000.html", title: "REP 2000: ROS 2 releases and target platforms", accessed: 2026-11-19}
  - {url: "https://gymnasium.farama.org/environments/mujoco/", title: "Gymnasium docs: MuJoCo environments", accessed: 2026-11-19}
---

# PyBullet

Python bindings for the Bullet physics SDK: CPU rigid-body simulation with inverse kinematics,
collision queries and camera images, loading URDF, SDF and MJCF [1][4]. Builders meet it in older RL
and manipulation repos and tutorials. Licence zlib (except `Extras/` and third-party folders); newest
`pybullet` on PyPI 3.2.7, 2025-01-30; the last GitHub release, PyBullet 3.2.5, is from April 2022 [1][2].

## When to use it

To run an existing PyBullet project (panda-gym, gym-pybullet-drones and many papers), or for a quick
CPU check that a URDF loads and moves. For a new project pick [MuJoCo](mujoco.md): open source since
2022 and the engine of Gymnasium's robot environments [6], while PyBullet's issue tracker is closed,
its last physics-code changes were merged in April 2024 [1], and PyPI has no wheels for Windows,
macOS or Python 3.12+ [2]. For GPU-batched RL see [Genesis](genesis.md); for ROS 2, [Gazebo](gazebo.md).

## Setup

- **Ubuntu 24.04:** `pip install pybullet` in a venv. PyPI 3.2.7 has wheels only for Linux x86_64 and
  CPython 3.6–3.11 [2]; on Python 3.12 (Ubuntu 24.04 and ROS 2 Jazzy [5]) pip compiles the source
  package, which needs a C++ compiler (`sudo apt install build-essential`) [1][2].
- **Windows and macOS:** the last PyPI wheels were 2.6.9 and 2.7.1 in March 2020, so pip compiles there
  too [2]. Easier: `conda install -c conda-forge pybullet` has binaries (Bullet 3.25) for Linux x86_64
  and aarch64, Intel and Apple-silicon macOS and Windows, Python 3.8–3.14 [3].
- **Check:** `python -c "import pybullet as p; print(p.isNumpyEnabled())"`. `False` means it was built
  without NumPy and camera images copy slowly [4]. The source build lists only setuptools as a build
  need [1], so install NumPy first and use `pip install --no-build-isolation pybullet`.

## How an agent works with it

`p.connect(p.DIRECT)` runs headless in the same process; `p.GUI` opens the OpenGL window [4]. Add the
bundled models with `p.setAdditionalSearchPath(pybullet_data.getDataPath())`, then `p.loadURDF`,
`p.loadSDF` or `p.loadMJCF`, `p.setJointMotorControl2`, `p.stepSimulation()` (1/240 s by default) and
`p.getJointState` [4]. In DIRECT mode `getCameraImage` uses the CPU TinyRenderer; on Linux the bundled
EGL plugin renders on the GPU without X11: `p.loadPlugin(pkgutil.get_loader("eglRenderer").get_filename(),
"_eglRendererPlugin")` [1][4]. A model is fine when its id is non-negative, `p.getNumJoints` matches the
URDF and joint states change after steps. The repo has no ROS 2 bridge; wrap it in an rclpy node [1].

## Traps

- **Joints start motorised.** Revolute and prismatic joints get a velocity motor by default, so the
  robot looks stuck; for torque control first set `VELOCITY_CONTROL` with `force=0` [4].
- **Self-collision is off and inertia is recomputed.** Pass
  `flags=p.URDF_USE_SELF_COLLISION | p.URDF_USE_INERTIA_FROM_FILE`, or links pass through each other
  and Bullet derives inertia from the collision shapes instead of your URDF [4].
- **SDF and MJCF import is partial.** `loadSDF` reads only models and geometry, not cameras or lights;
  `loadMJCF` is a basic importer for Gym-era files [4]. Prefer URDF, and MuJoCo for MJCF models.
- **Old Gym inside.** `pybullet_envs` imports the old `gym` package, not Gymnasium [1]; current RL
  libraries need a wrapper or a maintained fork.
- **No support channel.** GitHub issues are closed and the forum is a historical archive [1]. Pin the
  version and expect to debug problems yourself.

## Alternatives

[MuJoCo](mujoco.md), [Genesis](genesis.md), [Gazebo](gazebo.md), [Webots](webots.md),
[CoppeliaSim](coppeliasim.md), [Isaac Sim](isaac-sim.md); Gymnasium, ManiSkill, robosuite. See
[Choose a simulator](../guides/choose-a-simulator.md).

## Sources

1. [Bullet repository: README, LICENSE.txt, setup.py, examples, commits, tags and releases](https://github.com/bulletphysics/bullet3), accessed 2026-11-19
2. [pybullet on PyPI: release history and wheel files](https://pypi.org/project/pybullet/#files), accessed 2026-11-19
3. [pybullet on conda-forge](https://anaconda.org/conda-forge/pybullet), accessed 2026-11-19
4. [PyBullet Quickstart Guide](https://docs.google.com/document/d/10sXEhzFRSnvFcl3XxNGhnD4N2SedqwdAvK3dsihxVUA/edit), accessed 2026-11-19
5. [REP 2000: ROS 2 releases and target platforms](https://www.ros.org/reps/rep-2000.html), accessed 2026-11-19
6. [Gymnasium docs: MuJoCo environments](https://gymnasium.farama.org/environments/mujoco/), accessed 2026-11-19

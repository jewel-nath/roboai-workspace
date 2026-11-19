---
type: guide
name: Choose a robot simulator
summary: Which simulator to run a robot in (Gazebo, MuJoCo, Isaac Sim, Webots, CoppeliaSim, CARLA, Genesis, PyBullet or Habitat), decided by ROS 2 support, contact physics, sensors, GPU-parallel learning, hardware, licence and maintenance.
tags: [simulation, simulator, gazebo, mujoco, isaac-sim, webots, coppeliasim, carla, genesis, pybullet, habitat, ros2, reinforcement-learning, synthetic-data, sim-to-real]
question: Which simulator should I use for my robot?
options: [gazebo, mujoco, isaac-sim, webots, coppeliasim, carla, genesis, pybullet, habitat]
recommendation: "Gazebo (Harmonic on Jazzy, Jetty on Lyrical) for a ROS 2 robot; MuJoCo for contact-rich control and learning; Isaac Sim only for photoreal sensors on an RTX GPU; CARLA for cars, Webots for teaching, Habitat only for embodied-AI navigation benchmarks."
evidence: researched
last_verified: 2026-11-19
sources:
  - {url: "https://gazebosim.org/docs/latest/ros_installation/", title: Installing Gazebo with ROS, accessed: 2026-11-19}
  - {url: "https://github.com/gazebosim/gz-sim", title: "gz-sim repository: LICENSE, release tags, gz sim and gz model help, SimulationRunner (gz-sim8)", accessed: 2026-11-19}
  - {url: "https://github.com/google-deepmind/mujoco", title: "MuJoCo repository: README, LICENSE, release tags and Python rendering backends", accessed: 2026-11-19}
  - {url: "https://github.com/ros-controls/mujoco_ros2_control", title: "mujoco_ros2_control repository: README, docs and CHANGELOG", accessed: 2026-11-19}
  - {url: "https://github.com/isaac-sim/IsaacSim", title: "IsaacSim repository at v6.2.0: README, LICENSE, releases, extension docs and examples", accessed: 2026-11-19}
  - {url: "https://github.com/cyberbotics/webots", title: "Webots repository: README, LICENSE, releases, develop history and docs/reference", accessed: 2026-11-19}
  - {url: "https://www.coppeliarobotics.com", title: "CoppeliaSim website: editions, Edu terms and downloads", accessed: 2026-11-19}
  - {url: "https://github.com/carla-simulator/carla", title: "CARLA repository: README, LICENSE, releases (1.0 notes), Docs, AGENTS.md and Skills/", accessed: 2026-11-19}
  - {url: "https://pypi.org/project/carla/", title: "PyPI: carla release history", accessed: 2026-11-19}
  - {url: "https://github.com/Genesis-Embodied-AI/genesis-world", title: "Genesis World repository: README, LICENSE, pyproject.toml, RELEASE.md, solver options, examples", accessed: 2026-11-19}
  - {url: "https://stoneztao.substack.com/p/the-new-hyped-genesis-simulator-is", title: "Stone Tao: How fast is the new hyped Genesis simulator? (December 2024)", accessed: 2026-11-19}
  - {url: "https://github.com/bulletphysics/bullet3", title: "Bullet repository: README, LICENSE.txt, setup.py, examples, commits, tags and releases", accessed: 2026-11-19}
  - {url: "https://pypi.org/project/pybullet/#files", title: "pybullet on PyPI: release history and wheel files", accessed: 2026-11-19}
  - {url: "https://github.com/facebookresearch/habitat-lab", title: "habitat-lab repository: README, LICENSE, requirements, rearrange grasp manager, kinematic humanoid", accessed: 2026-11-19}
---

# Choose a robot simulator

Which simulator should your robot run in, before and beside the hardware? For builders of a
[ROS 2](../tools/ros2.md) robot (Jazzy by default, Lyrical noted), of control and learning, synthetic
data, teaching, cars and indoor navigation. First-class here: [Gazebo](../tools/gazebo.md) and
[MuJoCo](../tools/mujoco.md); documented: [Isaac Sim](../tools/isaac-sim.md), [Webots](../tools/webots.md),
[CoppeliaSim](../tools/coppeliasim.md), [CARLA](../tools/carla.md), [Genesis](../tools/genesis.md),
[PyBullet](../tools/pybullet.md), [Habitat](../tools/habitat.md).

## Short answer

- **A ROS 2 robot:** Gazebo, Harmonic on Jazzy (its only pairing) and Jetty on Lyrical [1];
  `sudo apt install ros-jazzy-ros-gz` installs it [1]. Steps: [sim-gazebo](../../skills/sim-gazebo/SKILL.md).
- **Control and robot learning:** MuJoCo, on the CPU, with MJX or MuJoCo Warp for GPU batches [3];
  its [ros2_control](../software/ros2-control.md) plugin runs your ROS 2 controllers on it [4].
- **Photoreal cameras, lidar and synthetic data:** Isaac Sim, if you have an RTX 4080-class GPU on
  Ubuntu or Windows 11 [5]. Without one, stay with Gazebo or MuJoCo.
- **Teaching:** Webots: Apache-2.0, ready robot models, Linux, Windows and macOS on a modest GPU
  [6], though no stable release since R2025a [6]. CoppeliaSim Edu if you teach or study at a school
  or university [7]. For a ROS 2 course, Gazebo.
- **Self-driving cars:** CARLA. Start on 1.0 (released 2026-11-17) [8]: install the Python wheel
  that comes with it, because `pip install carla` still gives the 0.9.16 client [9].
- **Indoor navigation research:** Habitat for embodied-AI benchmarks, frozen at v0.3.4 [14]. To test
  a real robot's Nav2 stack, use Gazebo.
- **Not for new work:** PyBullet; keep it for running old projects [12][13].

## What decides it

- **ROS 2 integration.** Gazebo is released with each ROS 2 distro and bridged by `ros_gz` [1].
  Isaac Sim's bridge bundles Humble and Jazzy, and 6.2 has no Lyrical support [5]. CARLA 1.0
  publishes ROS 2 topics from the server itself, over Fast DDS, Cyclone DDS or Zenoh [8]. MuJoCo
  connects through `mujoco_ros2_control`, a ros2_control system interface released for Humble to
  Lyrical [4]: it runs controllers, not a whole ROS world. Webots has its `webots_ros2` packages and
  CoppeliaSim a ROS interface [7]. Genesis and PyBullet have no ROS 2 bridge [10][12]; Habitat has
  only a third-party one [14].
- **Physics and contact.** MuJoCo is built for articulated bodies in contact: arms, hands and legged
  robots [3]. Gazebo runs DART by default [2], enough for mobile bases and arms under controllers.
  Isaac Sim runs GPU PhysX [5]. CoppeliaSim offers five engines: MuJoCo, Bullet, ODE, Newton and
  Vortex [7]. Genesis adds soft-body, cloth and fluid solvers to rigid bodies [10]. Habitat
  simplifies: grasped objects snap to the gripper, and humanoids are animated, not simulated [14].
- **Sensors and rendering.** Isaac Sim ray-traces cameras and lidars with RTX and writes labelled
  images with Replicator [5]. CARLA renders roads in Unreal Engine 5.8 with car sensors [8]. Habitat
  renders scanned homes fast [14]. Gazebo's lidar, camera and IMU plugins are made for testing a
  ROS 2 stack; MuJoCo renders RGB, depth and segmentation for learning, not photorealism [3].
- **GPU-parallel learning.** Training over thousands of environments needs an engine that batches on
  a GPU: MJX or MuJoCo Warp [3], Isaac Sim with Isaac Lab [5], or Genesis [10]; ManiSkill, robosuite
  and mjlab are other frameworks, with no pages yet. Gazebo, Webots and CoppeliaSim run one world per
  process. Speed figures are makers' claims: a ManiSkill author re-ran Genesis' launch numbers with
  realistic settings and disputed them [11].
- **Platform and GPU.** MuJoCo needs no GPU and ships for Linux, Windows and macOS [3]. Webots
  wants an NVIDIA or AMD card with OpenGL 3.3 [6]. Gazebo for ROS 2 targets Ubuntu; on another OS,
  run Ubuntu in a VM [1]. Isaac Sim needs an RTX 4080 or better (an A40 in a data centre) on Ubuntu
  22.04/24.04 or Windows 11 [5]; CARLA needs 16 GB of VRAM on the same systems [8]. Genesis runs on
  NVIDIA (CUDA), AMD (ROCm), Apple (Metal) or the CPU [10]. PyBullet's PyPI wheels stop at Linux
  x86-64 and Python 3.11, so on Ubuntu 24.04's Python 3.12 pip compiles it from source [13].
- **Licence and cost.** Gazebo [2], MuJoCo [3], Webots [6] and Genesis [10] are Apache-2.0; CARLA's
  code is MIT and its assets CC-BY [8]; PyBullet is zlib [12]. Isaac Sim's code is Apache-2.0, but
  it builds and runs only with NVIDIA-licensed parts: the Kit SDK, models and textures [5].
  CoppeliaSim Edu is free only to students and teachers of schools and universities, never to
  companies or research institutes; Pro is paid [7]. Habitat's code is MIT, but its MP3D and Gibson
  task data are non-commercial [14].
- **Maintenance.** Active: Gazebo (Jetty, gz-sim 10.7.0 [2]), MuJoCo (4.0.1, aiming at a release
  a month [3]), Isaac Sim (6.2.0, October 2026 [5]). Webots has had only nightly builds since R2025a,
  February 2025 [6]; CoppeliaSim's newest release is 4.10.0 rev0 [7]. CARLA 1.0 came out on
  2026-11-17 [8]. Genesis breaks its API often; read its release notes before upgrading [10].
  PyBullet's issue tracker is closed [12]; its last PyPI release is 3.2.7, January 2025 [13]. Meta
  no longer develops or maintains Habitat beyond v0.3.4 [14].

## Options compared

| Option | Cost and licence | Strengths | Limits | Best when |
|---|---|---|---|---|
| Gazebo | Free, Apache-2.0 [2] | Paired with each ROS 2 distro, one apt package [1]; `ros_gz`; lidar, camera and IMU plugins; DART physics [2] | Ubuntu for ROS 2 work [1]; one world per process, no GPU batching | A ROS 2 robot with Nav2 or ros2_control; several robots in one world |
| MuJoCo | Free, Apache-2.0 [3] | Contact dynamics for arms, hands and legs; Python and C; no GPU needed; MJX and MuJoCo Warp for GPU batches [3]; ros2_control plugin [4] | Plain rendering; no world, sensor and plugin ecosystem like Gazebo's | Control, MPC, reinforcement learning, system identification |
| Isaac Sim | Code Apache-2.0; needs NVIDIA-licensed Kit SDK, models and textures [5] | RTX cameras and lidars, Replicator data, GPU PhysX, USD scenes, URDF and MJCF import, ROS 2 bridge, Isaac Lab [5] | RTX 4080-class GPU; Ubuntu or Windows 11, no macOS; no Lyrical bridge in 6.2 [5] | Photoreal sensors, synthetic data, digital twins |
| Webots | Free, Apache-2.0 [6] | Ready robot models; Linux, Windows and macOS; modest OpenGL 3.3 GPU [6]; `webots_ros2` | No stable release since R2025a (February 2025) [6] | Teaching; quick tries on any desktop OS |
| CoppeliaSim | Edu free only for schools and universities; Pro paid [7] | Five physics engines; Python and Lua scripts; ZeroMQ remote API; ROS interface [7] | Edu not for companies or research institutes [7] | A university course; comparing engines in one tool |
| CARLA | Free; code MIT, assets CC-BY [8] | Towns, traffic and car sensors on Unreal Engine 5.8; ROS 2 from the server [8] | 16 GB VRAM [8]; 1.0 is new and PyPI still has 0.9.16 [9]; cars only | Driving stacks, traffic scenarios, perception data |
| Genesis | Free, Apache-2.0 [10] | Python; batched environments on CUDA, ROCm, Metal or CPU; soft bodies, cloth and fluids [10] | Frequent breaking changes; no ROS 2 bridge [10]; disputed speed claims [11] | GPU-batched RL with soft bodies, or on AMD or Apple GPUs, version pinned |
| PyBullet | Free, zlib [12] | Small CPU Python API; used by many older RL repos and tutorials | Issue tracker closed [12]; PyPI wheels only for Linux x86-64 up to Python 3.11 [13] | Running an existing PyBullet project |
| Habitat | Code MIT; MP3D and Gibson task data non-commercial [14] | Fast indoor scenes; navigation and rearrangement tasks; Habitat 3.0 humanoids; RL baselines [14] | Not maintained beyond v0.3.4; grasps snap, humanoids kinematic; no official ROS bridge [14] | Embodied-AI navigation and rearrangement benchmarks |

## Combining simulators

- **One robot description.** Generate every simulator's model from one URDF
  ([ros2-robot-description](../../skills/ros2-robot-description/SKILL.md)); Isaac Sim imports URDF and MJCF [5].
- **Split by job.** The ROS 2 stack (Nav2, ros2_control, sensors) in Gazebo; policy training in
  MuJoCo or Isaac Lab; synthetic images in Isaac Sim.
- **Sim-to-sim check.** Train in one engine, then run the policy or controller in a second before
  the hardware, such as a MuJoCo policy in Isaac Sim, or in Gazebo through ros2_control. If it works
  in only one, it learned that engine, not your robot: [sim-to-real](../../skills/sim-to-real/SKILL.md).

## When the answer changes

- **Jazzy to Lyrical:** Gazebo moves to Jetty, the pairing it now recommends to new users [1], and
  `mujoco_ros2_control` is already released for Lyrical [4]. Isaac Sim 6.2's bridge has no Lyrical
  support [5], and Webots R2025a's guide lists Ubuntu 22.04 and 24.04; only the unreleased master
  guide adds Lyrical's 26.04 [6].
- **No NVIDIA RTX card:** Isaac Sim [5] and CARLA [8] are out. MuJoCo, Gazebo and Webots run on
  ordinary hardware, and Genesis on AMD or Apple GPUs [10].
- **A commercial product:** CoppeliaSim Edu is out [7]; check Habitat's dataset terms [14] and
  NVIDIA's terms for Isaac Sim's parts [5].
- **Grasping or legged dynamics in a navigation project:** Habitat's physics will not transfer [14];
  move that part to MuJoCo or Isaac Sim.
- **Status to watch:** a new stable Webots, a CARLA 1.0 client on PyPI, a maintained Habitat fork, a
  stable Genesis API. Any of these reopens the choice.

## Sources

1. [Installing Gazebo with ROS](https://gazebosim.org/docs/latest/ros_installation/), accessed 2026-11-19
2. [gz-sim repository: LICENSE, release tags, gz sim and gz model help, SimulationRunner (gz-sim8)](https://github.com/gazebosim/gz-sim), accessed 2026-11-19
3. [MuJoCo repository: README, LICENSE, release tags and Python rendering backends](https://github.com/google-deepmind/mujoco), accessed 2026-11-19
4. [mujoco_ros2_control repository: README, docs and CHANGELOG](https://github.com/ros-controls/mujoco_ros2_control), accessed 2026-11-19
5. [IsaacSim repository at v6.2.0: README, LICENSE, releases, extension docs and examples](https://github.com/isaac-sim/IsaacSim), accessed 2026-11-19
6. [Webots repository: README, LICENSE, releases, develop history and docs/reference](https://github.com/cyberbotics/webots), accessed 2026-11-19
7. [CoppeliaSim website: editions, Edu terms and downloads](https://www.coppeliarobotics.com), accessed 2026-11-19
8. [CARLA repository: README, LICENSE, releases (1.0 notes), Docs, AGENTS.md and Skills/](https://github.com/carla-simulator/carla), accessed 2026-11-19
9. [PyPI: carla release history](https://pypi.org/project/carla/), accessed 2026-11-19
10. [Genesis World repository: README, LICENSE, pyproject.toml, RELEASE.md, solver options, examples](https://github.com/Genesis-Embodied-AI/genesis-world), accessed 2026-11-19
11. [Stone Tao: How fast is the new hyped Genesis simulator? (December 2024)](https://stoneztao.substack.com/p/the-new-hyped-genesis-simulator-is), accessed 2026-11-19
12. [Bullet repository: README, LICENSE.txt, setup.py, examples, commits, tags and releases](https://github.com/bulletphysics/bullet3), accessed 2026-11-19
13. [pybullet on PyPI: release history and wheel files](https://pypi.org/project/pybullet/#files), accessed 2026-11-19
14. [habitat-lab repository: README, LICENSE, requirements, rearrange grasp manager, kinematic humanoid](https://github.com/facebookresearch/habitat-lab), accessed 2026-11-19

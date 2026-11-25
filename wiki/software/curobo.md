---
type: tool
name: cuRobo
summary: NVIDIA Research's CUDA library for robot motion generation - batched IK, sphere-based collision checking, graph planning and trajectory optimisation in milliseconds on a GPU; Apache-2.0 since the cuRoboV2 rewrite (April 2026), non-commercial before. Python on Linux, no ROS release.
tags: [curobo, nvidia, gpu, cuda, motion-generation, inverse-kinematics, collision-checking, trajectory-optimization, mpc, esdf, pytorch, warp, cumotion, isaac-ros, moveit]
kind: library
area: manip
support:
license: Apache-2.0
links: {repo: "https://github.com/NVlabs/curobo", docs: "https://nvlabs.github.io/curobo/latest/", site: }
version: {tested: , latest: 0.9.0, as_of: 2026-11-25}
platforms: [linux]
agent_access: script
registry:
evidence: researched
last_verified: 2026-11-25
sources:
  - {url: "https://github.com/NVlabs/curobo", title: "cuRobo repository: README, LICENSE and its history, LICENSE_ASSETS, CHANGELOG, pyproject.toml, examples, tags, issues", accessed: 2026-11-25}
  - {url: "https://nvlabs.github.io/curobo/latest/getting-started/installation.html", title: "cuRobo docs: Installation", accessed: 2026-11-25}
  - {url: "https://nvlabs.github.io/curobo/latest/reference/benchmarks.html", title: "cuRobo docs: Benchmarks & Profiling", accessed: 2026-11-25}
  - {url: "https://github.com/NVIDIA-ISAAC-ROS/isaac_ros_cumotion", title: "isaac_ros_cumotion repository: README, LICENSE, package.xml files, release branches", accessed: 2026-11-25}
  - {url: "https://nvidia-isaac-ros.github.io/repositories_and_packages/isaac_ros_cumotion/index.html", title: "Isaac ROS docs: Isaac ROS cuMotion", accessed: 2026-11-25}
  - {url: "https://github.com/nvidia-isaac/cumotion", title: "NVIDIA cuMotion repository: README, LICENSE", accessed: 2026-11-25}
  - {url: "https://github.com/ros/rosdistro", title: "rosdistro distribution files: humble, jazzy, kilted, lyrical, rolling", accessed: 2026-11-25}
---

# cuRobo

cuRobo runs motion generation on an NVIDIA GPU: batched kinematics and IK, sphere-based collision
checking (cuboids, meshes, voxel grids, ESDFs from depth), graph planning, trajectory optimisation
and MPC, on PyTorch, CUDA and Warp [1]. Builders use it for arm motions in milliseconds or many IK
problems at once. From NVIDIA Research; **Apache-2.0 since cuRoboV2 (2026-04-18)**; up to v0.7.8
the NVIDIA License allowed only non-commercial research or evaluation [1]. Newest tag v0.9.0
(2026-11-04); last commit 2026-11-20 [1]. **No ROS 2 release in any distro** [7].

## When to use it

- **Use it** when speed or batch size matters: many goals or grasps, fast replanning, MPC,
  humanoids [1]. NVIDIA reports 3.8 ms mean planning and 99.73% success on 2,590 Franka problems
  on an RTX 5090 (25.7 ms on Jetson AGX Orin), warmed C++ with CUDA graphs [3].
- **Use something else** without an NVIDIA GPU: [MoveIt 2](moveit2.md) with [OMPL](ompl.md),
  [Drake](drake.md) or [Pinocchio](pinocchio.md).

## Setup

```bash
git clone https://github.com/NVlabs/curobo && cd curobo
uv venv --python 3.11 && source .venv/bin/activate
uv pip install ".[cu12-torch]"       # or ".[cu13-torch]"; check: nvidia-smi | grep CUDA
```

Needs Linux (Ubuntu 20.04+), an NVIDIA GPU newer than Turing with 4 GB of VRAM, driver
580.65.06+, and Python 3.10 to 3.13 [2]; the extras pull PyTorch 2.5+ (CUDA 12) or 2.9+ (CUDA
13) [1]. The docs install from a clone, not PyPI [2].

## How an agent works with it

Run `python -m curobo.examples.getting_started.motion_planning` first. In code,
`MotionPlanner(MotionPlannerCfg.create(robot="franka.yml", scene_model=...))`, `warmup()` once,
then `plan_pose(goal, start)`; check `result.success` and take `result.get_interpolated_plan()`,
a timed joint trajectory for a `joint_trajectory_controller` ([ros2_control](ros2-control.md))
[1]. For your own arm, the `build_robot_model` example fits collision spheres to the URDF meshes
and writes a YAML or XRDF config; `--visualize` shows them in a browser [1].

## Traps

- **Old licence on old code.** The v1 API, kept at tag v0.7.8, is still under the non-commercial
  NVIDIA License; only cuRoboV2 (v0.8.0+) is Apache-2.0, and its API changed [1]. Bundled robot
  assets keep their own licences (Franka Apache-2.0, UR and G1 BSD-3-Clause) [1].
- **cuMotion is not cuRobo.** NVIDIA's MoveIt plugin, Isaac ROS cuMotion, wrapped cuRobo v0.7.7
  in releases 4.0 to 4.3; from 4.4 (2026-04-30) it links NVIDIA's separate cuMotion library, and
  5.0 (September 2026) moved to Lyrical [4][5]. `isaac_ros_cumotion` is under the NVIDIA Isaac
  ROS Software License (NVIDIA GPUs only); the Apache-2.0 plugin depends on it [4][6].
- **Spheres decide collisions.** Checks use the fitted spheres, not meshes; inspect and refit [1].
- **Slow first call.** `warmup()` compiles CUDA graphs; warm up once and reuse the planner [1].

## Alternatives

[MoveIt 2](moveit2.md) with [OMPL](ompl.md), [Drake](drake.md), [Pinocchio](pinocchio.md), NVIDIA
cuMotion; see [Choose an arm motion planner](../guides/choose-an-arm-motion-planner.md).

## Sources

1. [cuRobo repository: README, LICENSE and its history, LICENSE_ASSETS, CHANGELOG, pyproject.toml, examples, tags, issues](https://github.com/NVlabs/curobo), accessed 2026-11-25
2. [cuRobo docs: Installation](https://nvlabs.github.io/curobo/latest/getting-started/installation.html), accessed 2026-11-25
3. [cuRobo docs: Benchmarks & Profiling](https://nvlabs.github.io/curobo/latest/reference/benchmarks.html), accessed 2026-11-25
4. [isaac_ros_cumotion repository: README, LICENSE, package.xml files, release branches](https://github.com/NVIDIA-ISAAC-ROS/isaac_ros_cumotion), accessed 2026-11-25
5. [Isaac ROS docs: Isaac ROS cuMotion](https://nvidia-isaac-ros.github.io/repositories_and_packages/isaac_ros_cumotion/index.html), accessed 2026-11-25
6. [NVIDIA cuMotion repository: README, LICENSE](https://github.com/nvidia-isaac/cumotion), accessed 2026-11-25
7. [rosdistro distribution files: humble, jazzy, kilted, lyrical, rolling](https://github.com/ros/rosdistro), accessed 2026-11-25

---
type: tool
name: Habitat
summary: Meta's embodied-AI platform (habitat-sim plus habitat-lab) for fast, photorealistic indoor navigation and rearrangement research; MIT code, but Meta stopped active development after v0.3.4 and most scene datasets are non-commercial.
tags: [simulator, embodied-ai, navigation, rearrangement, habitat-sim, habitat-lab, hm3d, humanoids, python, conda]
kind: library
area: sim
support: documented
license: MIT
links: {repo: "https://github.com/facebookresearch/habitat-sim", docs: "https://aihabitat.org/docs/habitat-sim/", site: "https://aihabitat.org"}
version: {tested: , latest: 0.3.3, as_of: 2026-11-19}
platforms: [linux, macos]
agent_access: script
registry:
evidence: researched
last_verified: 2026-11-19
sources:
  - {url: "https://github.com/facebookresearch/habitat-sim", title: "habitat-sim repository: README, LICENSE, BUILD_FROM_SOURCE.md, DATASETS.md, examples, tags", accessed: 2026-11-19}
  - {url: "https://github.com/facebookresearch/habitat-lab", title: "habitat-lab repository: README, LICENSE, requirements, rearrange grasp manager, kinematic humanoid", accessed: 2026-11-19}
  - {url: "https://anaconda.org/aihabitat/habitat-sim", title: "habitat-sim on the aihabitat conda channel", accessed: 2026-11-19}
  - {url: "https://arxiv.org/abs/2310.13724", title: "Habitat 3.0: A Co-Habitat for Humans, Avatars and Robots", accessed: 2026-11-19}
  - {url: "https://aihabitat.org/datasets/hm3d/", title: "Habitat-Matterport 3D Research Dataset (HM3D)", accessed: 2026-11-19}
  - {url: "https://aihabitat.org/datasets/replica_cad/", title: ReplicaCAD dataset, accessed: 2026-11-19}
  - {url: "https://huggingface.co/datasets/hssd/hssd-hab", title: "HSSD-hab dataset card", accessed: 2026-11-19}
---

# Habitat

Meta AI's embodied-AI platform: habitat-sim renders 3D scans and CAD scenes very fast, with Bullet for
rigid and articulated physics; habitat-lab adds tasks, robots, humanoids and RL baselines [1][2].
Builders use it to train and benchmark navigation and mobile-manipulation policies in houses. MIT code;
newest release 0.3.3, 2025-01-27; Meta stopped developing it after v0.3.4 [1][3].

## When to use it

For indoor navigation (point, object and image goals, instructions) or rearrangement research, to
reproduce Habitat Challenge work, or for Habitat 3.0's humanoids, human-in-the-loop tools and social
navigation and rearrangement tasks [2][4]. Meta's README claims over 8,000 steps per second for a
Fetch in ReplicaCAD, each step a 128×128 RGB-D frame and 1/30 s of physics, hardware not stated [1].
For manipulation, legged robots or ROS 2 work use [MuJoCo](mujoco.md), [Isaac Sim](isaac-sim.md) or
[Gazebo](gazebo.md).

## Setup

Conda is the official route, with builds for Linux and Apple-silicon macOS, none for Windows [1][3]:
`conda create -n habitat python=3.9 cmake=3.14.0`, `conda install habitat-sim withbullet headless -c
conda-forge -c aihabitat`, then `pip install -e habitat-lab` in a clone of its `stable` branch [2].

- **Python 3.9:** stable 0.3.3 is built only for it [3], though the habitat-sim README now says 3.12
  [1]. habitat-lab pins `gym>=0.22,<0.23.1` and `numpy==1.26.4` [2], so keep it in its own env.
- **Flags:** `withbullet` adds physics, needed for robots; `headless` uses EGL for servers without a
  display and does not work on macOS [1]. Source builds enable CUDA with `HABITAT_WITH_CUDA=ON` [1].
- **Check:** fetch `habitat_test_scenes` with `python -m habitat_sim.utils.datasets_download`, then run
  habitat-lab's `examples/example.py` [2]. Docker images are updated about yearly, for the Challenge [2].

## How an agent works with it

habitat-lab: `habitat.get_config("benchmark/rearrange/skills/pick.yaml", overrides=[...])` (Hydra),
`habitat.gym.make_gym_from_config(config)`, then `reset` and `step` [2]. habitat-sim alone:
`habitat_sim.Simulator(cfg)`, then `sim.step("move_forward")` returns sensor observations [1]. Robots
load from URDF; scenes are `.glb` or `*.scene_dataset_config.json` [1]. Set `HABITAT_ENV_DEBUG=1` when
vectorised envs hang silently [2]. No official ROS bridge; ROS-X-Habitat from UBC is third-party [2].

## Traps

- **Unmaintained after v0.3.4.** Both READMEs say Meta no longer develops or maintains it beyond
  v0.3.4, a tag of 2026-05-07 whose code still says 0.3.3 [1][2]. Pin it, and fix breakages yourself.
- **The datasets are not MIT.** HM3D is for academic, non-commercial research [5] and needs a Matterport
  API token [1]; HSSD-hab is CC BY-NC 4.0 [7]; MP3D and Gibson task data are CC BY-NC-SA 3.0 under
  their own terms [2]; ReplicaCAD is CC BY 4.0 [6]. Check before shipping a trained model.
- **Physics is simplified.** Rearrangement grasps snap the object to the gripper with a rigid
  constraint, and humanoids are kinematic, animated rather than simulated [2]. Contact-rich grasping and
  legged dynamics do not transfer; use MuJoCo or Isaac Sim for them.
- **Display errors on servers.** `Could not initialize GLFW` on a remote machine: `unset DISPLAY` and
  use the `headless` build [1].

## Alternatives

[Isaac Sim](isaac-sim.md), [MuJoCo](mujoco.md), [Gazebo](gazebo.md), [Genesis](genesis.md),
[PyBullet](pybullet.md); AI2-THOR, OmniGibson; [Choose a simulator](../guides/choose-a-simulator.md).

## Sources

1. [habitat-sim repository: README, LICENSE, BUILD_FROM_SOURCE.md, DATASETS.md, examples, tags](https://github.com/facebookresearch/habitat-sim), accessed 2026-11-19
2. [habitat-lab repository: README, LICENSE, requirements, rearrange grasp manager, kinematic humanoid](https://github.com/facebookresearch/habitat-lab), accessed 2026-11-19
3. [habitat-sim on the aihabitat conda channel](https://anaconda.org/aihabitat/habitat-sim), accessed 2026-11-19
4. [Habitat 3.0: A Co-Habitat for Humans, Avatars and Robots](https://arxiv.org/abs/2310.13724), accessed 2026-11-19
5. [Habitat-Matterport 3D Research Dataset (HM3D)](https://aihabitat.org/datasets/hm3d/), accessed 2026-11-19
6. [ReplicaCAD dataset](https://aihabitat.org/datasets/replica_cad/), accessed 2026-11-19
7. [HSSD-hab dataset card](https://huggingface.co/datasets/hssd/hssd-hab), accessed 2026-11-19

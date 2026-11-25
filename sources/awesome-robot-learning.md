---
type: source
name: Awesome Robot Learning
registry: awesome-robot-learning
url: https://github.com/RayYoh/Awesome-Robot-Learning
commit: "41eb274"
read_on: 2026-11-18
counts: {entries: 56, pages: 12, waiting: 0, index_only: 35, deferred: 0, rejected: 9}
---

# Awesome Robot Learning: what it gives RoboAI

A short list for robot-learning researchers, mostly about manipulation: surveys, related awesome
lists, labs and researchers, and then its real content, the simulation benchmarks (grouped by
physics engine) and a few datasets. That benchmark section is a good shortlist of what a learning
setup is built on today: Isaac Lab, ManiSkill, robosuite and RoboCasa, MuJoCo Menagerie, Genesis,
RLBench, CALVIN, LeRobot and Open X-Embodiment. Around them sit many older or one-off environments,
and four 2026 additions that promote their authors' own projects.

## How it was read

- Read at commit `41eb274` (last commit 2026-08-20) on 2026-11-18: the README, `how-to-RP.md` and
  the licence. The README links no list files of its own, only ten other awesome lists; those are
  index rows here, and five of them are registry sources with their own triage notes.
- **Grouped rows:** the Surveys section holds only papers, so it is one index row. Laboratories and
  Active Researchers are grouped the same way, one row each, since labs and people get no pages.
- **2026 additions:** the list was dormant from August 2024 until four outside pull requests in
  July and August 2026 added so101-nexus, ActionShift and Physical AI Atlas, each by its own author,
  and the RoboSkin.ai directory, from a branch named `codex/...`, which suggests a generated pull
  request. so101-nexus is index only; the other three are rejected. so101-nexus ships an agent
  skill file (`skills/reward-engineering/SKILL.md`); it was not read or followed.
- Page candidates were checked with a blobless shallow clone (last commit, licence file):
  Isaac Lab, which the Orbit link now resolves to (`isaac-sim/IsaacLab`; 2026-11-18, BSD-3-Clause,
  its mimic part Apache-2.0); OmniGibson, which now resolves to `StanfordVL/BEHAVIOR-1K`
  (2026-11-18, MIT); robosuite (2026-07-11, MIT); RoboCasa (2026-11-12, MIT); MuJoCo Menagerie
  (2026-11-10, a licence per model, mostly Apache-2.0); ManiSkill (2026-08-01, Apache-2.0); CALVIN
  (2025-09-08, MIT); Genesis (2026-11-18, Apache-2.0); RLBench (2025-01-25, an Imperial College
  licence for non-commercial research only); LeRobot (2026-11-18, Apache-2.0); Open X-Embodiment
  (`google-deepmind/open_x_embodiment`, 2025-11-05, code Apache-2.0 and data CC-BY-4.0).
- The rejected repos were cloned too, to date them. Other index rows were not checked; their Last
  commit and Licence are `—`.
- `unitree_mujoco` is filed under Isaac-based by mistake. Several entries link a project site
  instead of a repo (robosuite, Meta-World, RoboPianist, CALVIN, RLBench, Open X-Embodiment, D4RL).

## Pages made

| Entry | Page | Tier |
|---|---|---|
| mujoco_menagerie | [MuJoCo](../wiki/tools/mujoco.md) | A |
| Genesis | [Genesis](../wiki/tools/genesis.md) | B |
| Omniverse Isaac Orbit | [Isaac Lab](../wiki/learning/frameworks/isaac-lab.md) | A |
| OmniGibson | [BEHAVIOR-1K (with OmniGibson)](../wiki/learning/benchmarks/behavior-1k.md) | B |
| robosuite | [robosuite](../wiki/learning/frameworks/robosuite.md) | A |
| RoboCasa | [RoboCasa (RoboCasa365)](../wiki/learning/benchmarks/robocasa.md) | B |
| ManiSkill3 | [ManiSkill](../wiki/learning/frameworks/maniskill.md) | A |
| Calvin | [CALVIN](../wiki/learning/benchmarks/calvin.md) | B |
| RLBench | [RLBench](../wiki/learning/benchmarks/rlbench.md) | B |
| LeRobot | [LeRobot](../wiki/learning/frameworks/lerobot.md) | A |
| Open X-Embodiment | [Open X-Embodiment](../wiki/learning/datasets/open-x-embodiment.md) | A |
| SimplerEnv | [SimplerEnv (SIMPLER)](../wiki/learning/benchmarks/simpler-env.md) | B |

## Waiting for a page

| Entry | Page | Tier | Batch | Why it matters |
|---|---|---|---|---|

## Index only

| Entry | What it is | Last commit | Licence |
|---|---|---|---|
| Section: Surveys (8 papers) | Surveys of embodied AI, VLAs and robot foundation models | — | — |
| Awesome Robotics (Kiloreux) | Awesome list; registry source `awesome-robotics` | — | — |
| Awesome Robotics (ahundt) | General robotics awesome list; not a registry source | — | — |
| Awesome Robotic Tooling | Awesome list; registry source `awesome-robotic-tooling` | — | — |
| Awesome Robotics Libraries | Awesome list; registry source `awesome-robotics-libraries` | — | — |
| Awesome Reinforcement Learning | Reinforcement-learning awesome list; not a registry source | — | — |
| Awesome Robot Descriptions | Awesome list; registry source `awesome-robot-descriptions` | — | — |
| Awesome NVIDIA Isaac Gym | List of Isaac Gym projects; Isaac Gym is retired | — | — |
| Awesome RL Envs | List of reinforcement-learning environments | — | — |
| Awesome-Robotics-3D | Awesome list; registry source `awesome-robotics-3d` | — | — |
| Awesome-Video-Robotic-Papers | Papers on robot learning from video | — | — |
| Section: Laboratories (7 labs) | Seven robot-learning labs, from Berkeley to ETH Zurich | — | — |
| Section: Active Researchers (21 people) | Robot-learning researchers with links to their pages | — | — |
| Omniverse Isaac Gym Reinforcement Learning Environments for Isaac Sim | Retired Isaac Sim RL environments; merged into Isaac Lab | — | — |
| ARNOLD | Language-grounded manipulation benchmark on Isaac Sim | — | — |
| Unitree Go2 Omniverse | Community Isaac Sim setup for the [Unitree Go2](../wiki/robots/unitree-go2.md) | — | — |
| unitree_mujoco | Unitree's MuJoCo simulator for its own robots | — | — |
| dm_control | DeepMind's MuJoCo control suite and model tools; a classic RL benchmark | — | — |
| dm_robotics | DeepMind's robotics task and agent libraries on MuJoCo | — | — |
| DMControl Generalization Benchmark 2 | Visual generalization benchmark on DeepMind Control tasks | — | — |
| Meta-World | Multi-task and meta-RL benchmark of simulated Sawyer tasks | — | — |
| Gymnasium-Robotics | Farama's robot environments: Fetch, Shadow Hand and mazes | — | — |
| RoboPianist | Bimanual robot-hand piano-playing benchmark in MuJoCo | — | — |
| IKEA Furniture Assembly Environment | Furniture-assembly simulation for long-horizon manipulation | — | — |
| RoboHive | Meta's unified framework of MuJoCo robot-learning environments | — | — |
| so101-nexus | [SO-101](../wiki/robots/so-101.md) simulation, teleoperation and learning stack; added by its author | — | — |
| panda-gym | Franka Panda reach, push and pick tasks in PyBullet | — | — |
| MiniTouch benchmark | ServiceNow's small visuo-tactile manipulation benchmark | — | — |
| Toolkit for Vision-Guided Quadrupedal Locomotion Research | Vision-guided quadruped locomotion RL toolkit in PyBullet | — | — |
| SoftGym | Cloth, rope and fluid manipulation benchmark | — | — |
| VIMA-Bench | Multimodal-prompt manipulation benchmark from VIMA | — | — |
| Colosseum | RLBench-based benchmark testing generalization under perturbations | — | — |
| HumanoidBench | Simulated humanoid locomotion and manipulation benchmark | — | — |
| D4RL | Offline-RL datasets; succeeded by Farama's Minari | — | — |
| RH20T | Multi-robot manipulation dataset with paired human demonstrations | — | — |

## Deferred

| Entry | What it is | Phase |
|---|---|---|

## Rejected

| Entry | Why | Date |
|---|---|---|
| RoboSkin.ai Tactile Robotics Datasets | Promotion: an independent website's directory, added by an outside pull request in August 2026; not a dataset | 2026-11-18 |
| Isaac-ManipulaRL | Abandoned: its author paused development, with no commit since April 2022 | 2026-11-18 |
| Divide-and-Conquer Reinforcement Learning | Code for a 2018 paper, untouched since September 2018 and with no licence | 2026-11-18 |
| DoorGym | Abandoned since June 2020 and limited to one door-opening task | 2026-11-18 |
| ActionShift | Too thin to help a builder: a one-author 2026 research benchmark, added to the list by its author | 2026-11-18 |
| PyBullet Gymperium | Abandoned since March 2021; Gymnasium's own MuJoCo environments replace it | 2026-11-18 |
| Pybullet-implementation of the multi-goal robotics environment originally from Open AI Gym | Its author stopped development in 2022 once MuJoCo became free; Gymnasium-Robotics covers the tasks | 2026-11-18 |
| Thrower and Goalie Robot Arms | A 2020 student project run in a lab's own simulator, with no licence | 2026-11-18 |
| Physical AI Atlas | Promotion: a French directory site's data, added by its author; not a robot-learning dataset | 2026-11-18 |

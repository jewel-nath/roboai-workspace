---
type: tool
name: Isaac Lab
summary: NVIDIA's open-source framework (formerly Orbit) for training robot policies in thousands of GPU-parallel environments - manager-based and direct RL tasks trained with RSL-RL, rl_games, skrl or Stable-Baselines3, Mimic demonstration generation, and policy export to the robot; BSD-3-Clause (Mimic Apache-2.0). Since 3.0 it runs on Newton without Isaac Sim; Isaac Sim 6.2 is an optional extra under NVIDIA's terms.
tags: [isaac-lab, orbit, nvidia, reinforcement-learning, imitation-learning, gpu-simulation, newton, warp, physx, isaac-sim, rsl-rl, rl-games, skrl, stable-baselines3, mimic, skillgen, leapp, sim-to-real, locomotion, humanoid, quadruped]
kind: framework
area: learning
support:
license: BSD-3-Clause
links: {repo: "https://github.com/isaac-sim/IsaacLab", docs: "https://isaac-sim.github.io/IsaacLab/main/", site: }
version: {tested: , latest: 3.0.0, as_of: 2026-11-25}
platforms: [linux, windows]
agent_access: cli
registry:
evidence: researched
last_verified: 2026-11-25
sources:
  - {url: "https://github.com/isaac-sim/IsaacLab", title: "IsaacLab repository: README, LICENSE, LICENSE-mimic, pyproject.toml, docs/licenses, task configs, CHANGELOG, tags, issues", accessed: 2026-11-25}
  - {url: "https://github.com/isaac-sim/IsaacLab/releases/tag/v3.0.0", title: "Isaac Lab v3.0.0 release notes", accessed: 2026-11-25}
  - {url: "https://isaac-sim.github.io/IsaacLab/main/source/isaaclab/installation.html", title: "Isaac Lab docs: Installation (main, and its source at the v3.0.0 tag)", accessed: 2026-11-25}
  - {url: "https://isaac-sim.github.io/IsaacLab/main/source/isaaclab/migrating.html", title: "Isaac Lab docs: Migrating to 3.0", accessed: 2026-11-25}
  - {url: "https://isaac-sim.github.io/IsaacLab/main/source/concepts/task_workflows.html", title: "Isaac Lab docs: Direct and Manager MDP", accessed: 2026-11-25}
  - {url: "https://isaac-sim.github.io/IsaacLab/main/source/concepts/reinforcement_learning.html", title: "Isaac Lab docs: Reinforcement Learning", accessed: 2026-11-25}
  - {url: "https://isaac-sim.github.io/IsaacLab/main/source/concepts/backends_and_presets.html", title: "Isaac Lab docs: Backends and Presets", accessed: 2026-11-25}
  - {url: "https://isaac-sim.github.io/IsaacLab/main/source/features/imitation-learning/teleop_imitation.html", title: "Isaac Lab docs: Isaac Lab Mimic, SkillGen and humanoid imitation", accessed: 2026-11-25}
  - {url: "https://isaac-sim.github.io/IsaacLab/main/source/policy_deployment/index.html", title: "Isaac Lab docs: Sim2Real deployment (LEAPP export, SO-101 typing, G1 visual locomotion, policy inference)", accessed: 2026-11-25}
  - {url: "https://isaac-sim.github.io/IsaacLab/main/source/concepts/actuators.html", title: "Isaac Lab docs: Actuators", accessed: 2026-11-25}
  - {url: "https://isaac-sim.github.io/IsaacLab/main/source/how-to/transfer_policies_between_physx_and_newton.html", title: "Isaac Lab docs: Transfer policies between PhysX and Newton", accessed: 2026-11-25}
  - {url: "https://nvidia-isaac-ros.github.io/repositories_and_packages/isaac_ros_deploy/index.html", title: "Isaac ROS docs: Isaac ROS Deploy", accessed: 2026-11-25}
  - {url: "https://github.com/NVlabs/curobo/tree/ebb71702f3f70e767f40fd8e050674af0288abe8", title: "cuRobo at commit ebb71702 (the one SkillGen pins): LICENSE", accessed: 2026-11-25}
  - {url: "https://pypi.org/project/isaaclab/", title: "PyPI: isaaclab, rsl-rl-lib, skrl and rl-games release histories", accessed: 2026-11-25}
---

# Isaac Lab

Isaac Lab is NVIDIA's framework for training robot policies in thousands of simulated environments
at once on a GPU; it grew out of Orbit [1]. Builders use it for reinforcement learning of legged
and humanoid locomotion and of manipulation, to generate demonstrations for imitation learning,
and to export the trained policy to a real robot [6][8][9]. **Licence:** the framework is
BSD-3-Clause and `isaaclab_mimic` is Apache-2.0 [1]. Workflows that launch Isaac Sim pull in
NVIDIA's proprietary Isaac Sim terms, and so do assets not listed in `docs/licenses`; Newton-only
("kit-less") runs do not need Isaac Sim [1]. **Newest release: v3.0.0 (2026-10-20)** [2]; `main`
(3.1.0, unreleased) had commits on 2026-11-25; 156 issues were open [1]. NVIDIA maintains it.

## When to use it

- **Use it** for RL on a quadruped or humanoid with an NVIDIA GPU. Velocity-tracking tasks ship for
  ANYmal, Unitree Go2, H1 and [G1](../../robots/unitree-g1.md), Spot and Cassie, among others,
  with domain randomisation of friction, mass, centre of mass and pushes [1]. The docs start new
  projects on RSL-RL [6].
- **Manipulation RL** (reach, lift, cabinet, assembly) and **demonstration generation** for
  imitation learning with Mimic [1][8]. For an [SO-101](../../robots/so-101.md), NVIDIA's
  so101-typing-task trains with RSL-RL on Newton and runs the policy on a CPU through LeRobot; it
  pins a patched 3.0.0 runtime in a 32.6 GB Docker image [9].
- **Use something else** without an NVIDIA GPU or for a lighter manipulation setup
  ([ManiSkill](maniskill.md), [robosuite](robosuite.md)), for imitation from real demonstrations
  ([LeRobot](lerobot.md)) or for photoreal sensors ([Isaac Sim](../../tools/isaac-sim.md)); see
  [Choose a simulator](../../guides/choose-a-simulator.md).

## Setup

| Isaac Lab | Isaac Sim | Notes [1][2][7] |
|---|---|---|
| **v3.0.0** (2026-10-20) | 6.2, optional | Newton is the default install; `--extra isaacsim` adds PhysX and RTX |
| `main` (3.1.0) | 6.2, optional | Deprecates Mimic and the Isaac Sim (Kit) path, which 3.2 removes |
| v3.0.0-EA, beta2 | 6.1, 6.0 | Pre-releases |
| v2.3.x | 4.5, 5.0, 5.1 | Last 2.x line; `isaaclab.sh` and conda installs |

**Ubuntu 24.04** with uv, which 3.0 makes the only supported installer [3][4]:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
git clone --branch v3.0.0 https://github.com/isaac-sim/IsaacLab.git && cd IsaacLab
uv run isaaclab train --rl_library rsl_rl --task Isaac-Cartpole-Direct physics=newton_mjwarp
uv run --extra isaacsim isaaclab train --rl_library rsl_rl --task Isaac-Cartpole-Direct \
  physics=isaacsim_physx          # only when a task needs Isaac Sim PhysX or RTX
```

As a package: `uv pip install isaaclab==3.0.0 --index https://pypi.nvidia.com --torch-backend
cu130` (the wheel is also on PyPI [14]). Docker: `./docker/container.py start` builds a `base`
(Isaac Sim) or `kitless` image; `nvcr.io/nvidia/isaac-lab:3.0.0-kitless` is prebuilt [3].

**Needs (v3.0.0 docs)** [3]: Python 3.12 only; Ubuntu 22.04+ on x86_64, Linux aarch64 (DGX
Spark) or Windows 11 with long paths on; no macOS. PyTorch 2.11 with CUDA 13 needs a Turing or
newer NVIDIA GPU and driver 580.65.06+ (Linux) or 580.88+ (Windows); `main` asks for 595.58.03
and 595.97. Headless Newton needs no RTX card, and upstream gives **no RAM or VRAM figure** for
it (task, environment count and cameras decide). With Isaac Sim: 32 GB of RAM, 16 GB of VRAM and
an RTX GPU at least. Training on a Jetson is not documented; deployment on one is (below) [12].

## How an agent works with it

**Tasks** come in two styles [5]. *Manager-based* (`ManagerBasedRLEnv`, `ManagerBasedRLEnvCfg`)
assembles observation, action, reward, termination, event and curriculum terms from config, so a
change is a config edit; the docs suggest it for new single-agent tasks. *Direct* (`DirectRLEnv`)
puts the logic in methods (`_get_observations()`, `_get_rewards()`, `_get_dones()`,
`_reset_idx()`), for tightly coupled logic, multi-agent tasks or IsaacGymEnvs ports. Tasks
register with [Gymnasium](gymnasium.md) but return batched torch tensors on the GPU [1].

**Backends** are command-line presets [7]: `physics=newton_mjwarp`, `newton_kamino`, `ovphysx` or
`isaacsim_physx`; `renderer=newton_warp`, `ovrtx` or `isaacsim_rtx`; `--viz newton` or `kit`.
`uv run isaaclab list_envs --show_presets` lists what each task accepts.

**RL libraries** share one `train` and `play` command [6]:

| `--rl_library` | Install | What it adds |
|---|---|---|
| `rsl_rl` | default | PPO, teacher-student distillation, symmetry augmentation, RND; the docs' default |
| `rl_games` | `--extra rl-games` | PPO, SAC, A2C, population-based training; Isaac Lab pins its own fork [1] |
| `skrl` | `--extra skrl`, `skrl-jax` | PyTorch, JAX or Warp; AMP, IPPO and MAPPO |
| `sb3` | `--extra sb3` | [Stable-Baselines3](stable-baselines3.md) PPO; "best suited to smaller experiments" |
| `torchrl`, RLinf | `--extra torchrl`; separate setup | TorchRL PPO; RL post-training of GR00T and OpenVLA |

```bash
uv run isaaclab random_agent --task Isaac-Velocity-Rough-AnymalD --num_envs 16  # steps, no RL
uv run isaaclab train --rl_library rsl_rl --task Isaac-Velocity-Rough-AnymalD \
  --num_envs 64 --max_iterations 10                       # smoke test, then drop the overrides
uv run isaaclab play --rl_library rsl_rl --task Isaac-Velocity-Rough-AnymalD \
  --checkpoint latest --viz newton
```

Runs log to `logs/<library>/`; `play` exports TorchScript and ONNX into the run's `exported/`
folder [6][9]. Check mean reward and episode length in TensorBoard, then watch playback.

**Imitation learning with Mimic** [8]: teleoperate a few demonstrations (keyboard, SpaceMouse or
XR headset) into HDF5, mark subtask ends with `annotate_demos.py`, multiply them with
`generate_dataset.py` across many environments, and train BC-RNN with [robomimic](robomimic.md)
v0.4.0. Mimic needs Isaac Sim, Linux and task-space actions. SkillGen joins segments with cuRobo
plans; humanoid data converts to the LeRobot format to fine-tune [GR00T](../models/gr00t.md) N1.5.

**Sim-to-real for locomotion** [9][10][11]: train a teacher with privileged observations (height
scan, base velocity), distil a student that sees only what the robot measures, export, deploy.
Actuator models include DC-motor limits, randomly delayed PD and learned actuator networks
(`ActuatorNetMLP`, `ActuatorNetLSTM`). LEAPP exports the policy with its observation and action
processing as a YAML pipeline plus ONNX. **Isaac ROS Deploy** runs these bundles through Triton
on ROS 2 **Lyrical** (4.6: Jazzy), to topics or [ros2_control](../../software/ros2-control.md),
on x86 with an Ampere or newer GPU or on Jetson Thor or Orin (JetPack 7.2) [12]. Try the policy in
the other physics engine first; see the [sim-to-real](../../../skills/sim-to-real/SKILL.md) skill.

## Traps

- **2.x code breaks on 3.0.** Quaternions went from (w, x, y, z) to (x, y, z, w); `.data.*`
  returns `ProxyArray` (use `.torch`); `AppLauncher` is only partly compatible; per-library
  `train.py` and `play.py` are gone [2]; task IDs lost `-v0` (`Isaac-Velocity-Rough-AnymalD`) [1].
  Tell: `ProxyArray` errors, rotated robots. Fix: the migration guide [4], and the same quaternion
  order in the robot's observations.
- **A pinned stack.** Python 3.12, torch 2.11.0 and Warp 1.17.0 are exact pins [1][14]; another
  torch breaks it. Use a fresh uv environment per release, never an upgraded 2.x one [4].
- **Joint order is not the robot's.** PhysX and MuJoCo-Warp may order joints and bodies
  differently; set `joint_ordering` and `body_ordering`, and map the policy's joints to your
  driver's by name [11].
- **Sim-to-real gaps.** Simulated torque limits are set apart from the hardware's (20 N·m at the
  G1 ankles) [9]; an ideal PD actuator hides real latency and friction. Fit the actuator model,
  randomise what stays uncertain, and dry-run with torque limits on.
- **Licences beyond BSD.** NVIDIA robot assets fall under the Isaac Sim licence [1]. SkillGen pins
  cuRobo commit `ebb71702` (2025-08), whose LICENSE allows only non-commercial research or
  evaluation; Isaac Lab's bundled cuRobo licence limits it to use with Isaac Lab [1][13].
- **Mimic is on its way out.** `main` deprecates Mimic for NVIDIA's AutoData, and the Isaac Sim
  (Kit) path for removal in 3.2; the docs point new work to `newton_mjwarp` or `ovphysx` [7][8].

## Alternatives

[ManiSkill](maniskill.md), [robosuite](robosuite.md), [robomimic](robomimic.md),
[LeRobot](lerobot.md), [Genesis](../../tools/genesis.md), MuJoCo Playground, mjlab.

## Sources

1. [IsaacLab repository: README, LICENSE, LICENSE-mimic, pyproject.toml, docs/licenses, task configs, CHANGELOG, tags, issues](https://github.com/isaac-sim/IsaacLab), accessed 2026-11-25
2. [Isaac Lab v3.0.0 release notes](https://github.com/isaac-sim/IsaacLab/releases/tag/v3.0.0), accessed 2026-11-25
3. [Isaac Lab docs: Installation (main, and its source at the v3.0.0 tag)](https://isaac-sim.github.io/IsaacLab/main/source/isaaclab/installation.html), accessed 2026-11-25
4. [Isaac Lab docs: Migrating to 3.0](https://isaac-sim.github.io/IsaacLab/main/source/isaaclab/migrating.html), accessed 2026-11-25
5. [Isaac Lab docs: Direct and Manager MDP](https://isaac-sim.github.io/IsaacLab/main/source/concepts/task_workflows.html), accessed 2026-11-25
6. [Isaac Lab docs: Reinforcement Learning](https://isaac-sim.github.io/IsaacLab/main/source/concepts/reinforcement_learning.html), accessed 2026-11-25
7. [Isaac Lab docs: Backends and Presets](https://isaac-sim.github.io/IsaacLab/main/source/concepts/backends_and_presets.html), accessed 2026-11-25
8. [Isaac Lab docs: Isaac Lab Mimic, SkillGen and humanoid imitation](https://isaac-sim.github.io/IsaacLab/main/source/features/imitation-learning/teleop_imitation.html), accessed 2026-11-25
9. [Isaac Lab docs: Sim2Real deployment (LEAPP export, SO-101 typing, G1 visual locomotion, policy inference)](https://isaac-sim.github.io/IsaacLab/main/source/policy_deployment/index.html), accessed 2026-11-25
10. [Isaac Lab docs: Actuators](https://isaac-sim.github.io/IsaacLab/main/source/concepts/actuators.html), accessed 2026-11-25
11. [Isaac Lab docs: Transfer policies between PhysX and Newton](https://isaac-sim.github.io/IsaacLab/main/source/how-to/transfer_policies_between_physx_and_newton.html), accessed 2026-11-25
12. [Isaac ROS docs: Isaac ROS Deploy](https://nvidia-isaac-ros.github.io/repositories_and_packages/isaac_ros_deploy/index.html), accessed 2026-11-25
13. [cuRobo at commit ebb71702 (the one SkillGen pins): LICENSE](https://github.com/NVlabs/curobo/tree/ebb71702f3f70e767f40fd8e050674af0288abe8), accessed 2026-11-25
14. [PyPI: isaaclab, rsl-rl-lib, skrl and rl-games release histories](https://pypi.org/project/isaaclab/), accessed 2026-11-25

---
type: tool
name: ManiSkill
summary: GPU-parallel robot simulator and benchmark for manipulation learning, built on SAPIEN (ManiSkill3); about 70 Gymnasium tasks, some 35 robots including SO100 and Koch v1.1, HDF5 demonstrations, PPO, SAC, BC, Diffusion Policy and ACT baselines, and sim-to-real tooling. Code Apache-2.0, assets CC BY-NC 4.0; GPU simulation only on Linux with an NVIDIA GPU. Last commit 2026-08-01.
tags: [maniskill, maniskill3, maniskill2, sapien, physx, gpu-simulation, manipulation, reinforcement-learning, imitation-learning, benchmark, gymnasium, demonstrations, hdf5, lerobot, sim-to-real, real2sim, so100, koch, panda, widowx]
kind: framework
area: learning
support:
license: Apache-2.0
links: {repo: "https://github.com/mani-skill/ManiSkill", docs: "https://maniskill.readthedocs.io/en/latest/", site: }
version: {tested: , latest: 3.0.1, as_of: 2026-11-25}
platforms: [linux, windows, macos]
agent_access: script
registry:
evidence: researched
last_verified: 2026-11-25
sources:
  - {url: "https://github.com/mani-skill/ManiSkill", title: "ManiSkill repository: README, LICENSE, setup.py, PPO baseline README, task and robot code, docs sources, tags", accessed: 2026-11-25}
  - {url: "https://maniskill.readthedocs.io/en/latest/user_guide/getting_started/installation.html", title: "ManiSkill docs: Installation", accessed: 2026-11-25}
  - {url: "https://maniskill.readthedocs.io/en/latest/user_guide/reinforcement_learning/setup.html", title: "ManiSkill docs: Reinforcement learning setup", accessed: 2026-11-25}
  - {url: "https://maniskill.readthedocs.io/en/latest/user_guide/reinforcement_learning/baselines.html", title: "ManiSkill docs: Reinforcement learning baselines", accessed: 2026-11-25}
  - {url: "https://maniskill.readthedocs.io/en/latest/user_guide/learning_from_demos/setup.html", title: "ManiSkill docs: Learning from demonstrations, setup and baselines", accessed: 2026-11-25}
  - {url: "https://maniskill.readthedocs.io/en/latest/user_guide/datasets/demos.html", title: "ManiSkill docs: Demonstrations", accessed: 2026-11-25}
  - {url: "https://maniskill.readthedocs.io/en/latest/user_guide/datasets/replay.html", title: "ManiSkill docs: Replaying and converting trajectories", accessed: 2026-11-25}
  - {url: "https://maniskill.readthedocs.io/en/latest/robots/index.html", title: "ManiSkill docs: Robots", accessed: 2026-11-25}
  - {url: "https://maniskill.readthedocs.io/en/latest/tasks/index.html", title: "ManiSkill docs: Tasks", accessed: 2026-11-25}
  - {url: "https://maniskill.readthedocs.io/en/latest/user_guide/tutorials/sim2real/index.html", title: "ManiSkill docs: Sim2Real", accessed: 2026-11-25}
  - {url: "https://maniskill.readthedocs.io/en/latest/user_guide/additional_resources/performance_benchmarking.html", title: "ManiSkill docs: Performance benchmarking", accessed: 2026-11-25}
  - {url: "https://huggingface.co/datasets/haosulab/ManiSkill_Demonstrations", title: "Hugging Face dataset card: haosulab/ManiSkill_Demonstrations", accessed: 2026-11-25}
  - {url: "https://pypi.org/project/mani-skill/", title: "PyPI: mani-skill, mani-skill-nightly and sapien release histories and wheels", accessed: 2026-11-25}
  - {url: "https://github.com/mani-skill/ManiSkill/issues", title: "ManiSkill issues, including 1489 (asset server unreachable)", accessed: 2026-11-25}
---

# ManiSkill

ManiSkill is a robot simulator and benchmark for manipulation learning, built on the SAPIEN engine
(PhysX). Version 3 steps and renders many environments at once on a GPU, and each parallel
environment may hold different objects [1]. Builders use it to train RL and imitation policies on
simulated arms, hands, mobile manipulators and humanoids, to evaluate policies in real-to-sim
scenes, and to try sim-to-real on a low-cost arm [1][10]. **Licence:** the code is Apache-2.0,
but the README puts the assets under **CC BY-NC 4.0** (non-commercial) [1]; the demonstration
dataset card says Apache-2.0 [12]. SAPIEN is MIT [13]. From Hao Su's lab (UC San Diego); the
repo moved from `haosulab` to the `mani-skill` organisation [1].

**Maintenance:** 3.0.1 (2026-04-21) is the first stable ManiSkill3 release on PyPI, after betas
from 3.0.0b1 (May 2024) to b22 (December 2025) [13]. The last commit to `main` was 2026-08-01
and the last nightly 2026-08-02; 131 issues are open, and the asset-server and SAPIEN reports of
September and November 2026 have no maintainer reply [1][14]. Treat it as slowing down.

## When to use it

- **Use it** for manipulation RL or imitation learning with a GPU budget, or for a benchmark with
  ready demonstrations: about 70 registered environments (control, table-top pick, push, stack
  and peg insertion, dexterous hands, drawing, mobile manipulation, quadrupeds, humanoids) [1][9].
- **Robots:** about 35 models graded A to C, among them Panda, xArm6 and 7, UR10e, WidowX 250S
  and WidowX AI, Unitree G1, H1 and Go2, ANYmal C, Allegro, and the low-cost
  [Koch v1.1](../../robots/koch-v1-1.md) and SO100 (both grade A) [8]. There is no SO-101 model;
  the SO-ARM100 repo ships a separate SO-101 URDF ([SO-101](../../robots/so-101.md)).
- **VLA evaluation:** real-to-sim "digital twin" tasks back the ManiSkill3 branch of
  [SimplerEnv](../benchmarks/simpler-env.md) for [Octo](../models/octo.md) and
  [RT-1](../models/rt-1.md); [RDT](../models/rdt.md) pretrained on some ManiSkill demos [1].
- **Use something else** for legged and humanoid locomotion or USD scenes
  ([Isaac Lab](isaac-lab.md)), for MuJoCo-based manipulation benchmarks ([robosuite](robosuite.md),
  [LIBERO](../benchmarks/libero.md)), or for training on real-robot data ([LeRobot](lerobot.md)).
  The authors report ManiSkill faster and leaner in GPU memory than Isaac Lab on most of their
  RTX 4090 tests, and say the comparison is not like for like [11].

## Setup

```bash
python3 -m venv ~/venvs/maniskill && . ~/venvs/maniskill/bin/activate
pip install --upgrade mani_skill torch                 # 3.0.1; pick a torch that fits your CUDA
sudo apt-get install libvulkan1 vulkan-tools && vulkaninfo   # rendering needs Vulkan
python -m mani_skill.examples.demo_random_action       # PickCube-v1, 50 random steps
```

| System | CPU sim | GPU sim | Rendering [2] |
|---|---|---|---|
| Linux, NVIDIA GPU | yes | yes | yes |
| Windows (NVIDIA or AMD) | yes | no | yes |
| macOS | yes | no | yes, after extra Vulkan setup |
| WSL | yes | no | no |

SAPIEN 3.0.3 has wheels for Python 3.10 to 3.14 on x86_64 Linux, Windows and macOS; there is no
Linux aarch64 wheel, so no Jetson [13]. Upstream gives no CUDA or driver minimum: GPU simulation
needs an NVIDIA GPU, rendering a working Vulkan driver (`nvidia-driver-xxx`, not the server
variant or the runfile) [2]. A `maniskill/base` Docker image exists [2]. Assets download on first
use to `~/.maniskill/data` (`MS_ASSET_DIR`) [2]. **GPU memory:** the RGB PPO examples stay under
15 GB with 256 environments; lower `num_envs` on smaller cards [1]. No other figures are given.

## How an agent works with it

**Environments** are Gymnasium IDs [3]:

```python
import gymnasium as gym, mani_skill.envs
env = gym.make("PickCube-v1", num_envs=512, obs_mode="rgb",
               control_mode="pd_ee_delta_pose", robot_uids="panda")   # num_envs > 1: GPU sim
obs, info = env.reset(seed=0)
obs, rew, terminated, truncated, info = env.step(env.action_space.sample())
```

- With `num_envs > 1` the backend switches to `physx_cuda` and every output is a batched torch
  tensor on the GPU, not NumPy [1][3]. `ManiSkillVectorEnv(env, auto_reset=True,
  ignore_terminations=False)` gives the Gymnasium vector interface; `CPUGymWrapper` makes a
  single NumPy env for CPU libraries such as [Stable-Baselines3](stable-baselines3.md) [3].
- **Observations:** `state`, `state_dict`, `rgb`, `depth`, `segmentation`, `rgbd`, `pointcloud`
  and combinations; PickCube's camera is 128 x 128 [1]. **Actions:** controllers such as
  `pd_joint_pos`, `pd_joint_delta_pos`, `pd_ee_delta_pos` and `pd_ee_delta_pose`. Physics runs
  at 100 Hz and control at 20 Hz by default [1].
- **RL baselines** [4]: PPO (tested, adapted from CleanRL), SAC (results pending), TD-MPC2 (in
  progress). From the repo's `examples/baselines/ppo`: `python ppo.py --env_id=PushCube-v1
  --num_envs=2048 ...` for state, `ppo_rgb.py` for images; the authors report PushCube in under a
  minute (state) and PickCube in 15 to 45 minutes (RGB), GPU unnamed [1].
- **Demonstrations** [6][12]: `python -m mani_skill.utils.download_demo PickCube-v1` fetches
  `trajectory.h5` plus `trajectory.json` from the `haosulab/ManiSkill_Demonstrations` dataset,
  sorted by source (motion planning, RL, teleoperation). The HDF5 holds actions, env states and
  usually success flags, but no observations; `env_info` in the JSON rebuilds the environment.
- **Replay** adds observations or converts the controller [7]:
  `python -m mani_skill.trajectory.replay_trajectory --traj-path PickCube-v1/.../trajectory.h5
  --use-first-env-state -b physx_cuda -c pd_joint_delta_pos -o rgb --save-traj`.
  `python -m mani_skill.trajectory.convert_to_lerobot` writes a LeRobot v3.0 dataset [7].
- **Imitation baselines** [5]: Diffusion Policy and ACT under `examples/baselines`, plus RFCL and
  RLPD that mix demonstrations with RL; standard BC is still marked in progress. Use the repo's
  `replay_for_il_baselines.sh` so your data matches the published runs [5].
- **Own data:** click-and-drag teleoperation with motion planning
  (`mani_skill.examples.teleoperation.interactive_panda`) and scripted Panda motion-planning
  solutions through mplib (Linux) [1].
- **Check the result** with `ManiSkillVectorEnv(..., ignore_terminations=True,
  record_metrics=True)`, `reconfiguration_freq=1`, and read `success_once` or `success_at_end`
  from `info["final_info"]["episode"]` [3][5].
- **Sim-to-real:** `Sim2RealEnv` wraps a real robot behind the simulated task's interface; the
  worked example trains an RGB policy to pick a cube in simulation and runs it zero-shot on an
  SO100 through LeRobot (`lerobot-sim2real` repo) [10]. The code is specific to that setup [10].

## Traps

- **Same pip name, different library.** ManiSkill2 is `mani_skill` 0.5.3 and lower (`v0.5.3`
  tag); ManiSkill3 is `mani_skill>=3` with new task IDs and APIs [1]. SimplerEnv keeps a separate
  `maniskill3` branch [1]. Pin the version your code was written for.
- **Non-commercial assets.** Object and scene assets are CC BY-NC 4.0 [1]; a product or paid
  service built on them needs other assets, even though the code and demo files are permissive.
- **CPU demos on the GPU.** CPU and GPU PhysX differ slightly for the same actions, and action
  replay of precise tasks (PushT, PickSingleYCB) can fail. Replay with `--use-first-env-state -b
  physx_cuda`, or `--use-env-states`; controller conversion does not run on the GPU backend, and
  works best for the Panda [7]. Evaluate on the backend the data came from [5].
- **Success rates that do not compare.** Numbers change with reset and metric settings. Evaluate
  as the docs prescribe (`ignore_terminations=True`, `reconfiguration_freq=1`) and name the
  metric you report, `success_once` or `success_at_end` [3][5].
- **Missing assets.** Since 2026-09, PartNet-Mobility objects and some YCB clutter files fail to
  download from `storage1.ucsd.edu`, with no maintainer reply (issue 1489) [14]. Check that a
  task's assets download before you build on it.
- **Duplicated demos.** A user reports 312 duplicate trajectories in the PegInsertionSide-v1
  motion-planning set (issue 1525) [14]; de-duplicate before splitting a dataset.

## Alternatives

[Isaac Lab](isaac-lab.md), [robosuite](robosuite.md) and [RoboCasa](../benchmarks/robocasa.md),
[LIBERO](../benchmarks/libero.md), [RLBench](../benchmarks/rlbench.md),
[BEHAVIOR-1K](../benchmarks/behavior-1k.md), [Genesis](../../tools/genesis.md),
[MuJoCo](../../tools/mujoco.md) with MuJoCo Playground.

## Sources

1. [ManiSkill repository: README, LICENSE, setup.py, PPO baseline README, task and robot code, docs sources, tags](https://github.com/mani-skill/ManiSkill), accessed 2026-11-25
2. [ManiSkill docs: Installation](https://maniskill.readthedocs.io/en/latest/user_guide/getting_started/installation.html), accessed 2026-11-25
3. [ManiSkill docs: Reinforcement learning setup](https://maniskill.readthedocs.io/en/latest/user_guide/reinforcement_learning/setup.html), accessed 2026-11-25
4. [ManiSkill docs: Reinforcement learning baselines](https://maniskill.readthedocs.io/en/latest/user_guide/reinforcement_learning/baselines.html), accessed 2026-11-25
5. [ManiSkill docs: Learning from demonstrations, setup and baselines](https://maniskill.readthedocs.io/en/latest/user_guide/learning_from_demos/setup.html), accessed 2026-11-25
6. [ManiSkill docs: Demonstrations](https://maniskill.readthedocs.io/en/latest/user_guide/datasets/demos.html), accessed 2026-11-25
7. [ManiSkill docs: Replaying and converting trajectories](https://maniskill.readthedocs.io/en/latest/user_guide/datasets/replay.html), accessed 2026-11-25
8. [ManiSkill docs: Robots](https://maniskill.readthedocs.io/en/latest/robots/index.html), accessed 2026-11-25
9. [ManiSkill docs: Tasks](https://maniskill.readthedocs.io/en/latest/tasks/index.html), accessed 2026-11-25
10. [ManiSkill docs: Sim2Real](https://maniskill.readthedocs.io/en/latest/user_guide/tutorials/sim2real/index.html), accessed 2026-11-25
11. [ManiSkill docs: Performance benchmarking](https://maniskill.readthedocs.io/en/latest/user_guide/additional_resources/performance_benchmarking.html), accessed 2026-11-25
12. [Hugging Face dataset card: haosulab/ManiSkill_Demonstrations](https://huggingface.co/datasets/haosulab/ManiSkill_Demonstrations), accessed 2026-11-25
13. [PyPI: mani-skill, mani-skill-nightly and sapien release histories and wheels](https://pypi.org/project/mani-skill/), accessed 2026-11-25
14. [ManiSkill issues, including 1489 (asset server unreachable)](https://github.com/mani-skill/ManiSkill/issues), accessed 2026-11-25

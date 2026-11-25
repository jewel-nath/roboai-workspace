---
type: tool
name: Stable-Baselines3
summary: Reliable PyTorch implementations of model-free RL algorithms (PPO, SAC, TD3, DQN, A2C, DDPG, HER) behind a Gymnasium interface, with SB3-Contrib (TQC, CrossQ, RecurrentPPO, TRPO) and the RL Zoo for tuned hyperparameters; MIT, maintained by DLR-RM. Best for single-machine CPU or few-environment training; GPU-parallel simulators use RSL-RL or rl_games instead.
tags: [stable-baselines3, sb3, reinforcement-learning, ppo, sac, td3, tqc, crossq, sb3-contrib, rl-zoo, sbx, gymnasium, pytorch, dlr]
kind: library
area: learning
support:
license: MIT
links: {repo: "https://github.com/DLR-RM/stable-baselines3", docs: "https://stable-baselines3.readthedocs.io/en/master/", site: }
version: {tested: , latest: 2.9.2, as_of: 2026-11-25}
platforms: [linux, windows, macos]
agent_access: script
registry:
evidence: researched
last_verified: 2026-11-25
sources:
  - {url: "https://github.com/DLR-RM/stable-baselines3", title: "stable-baselines3 repository: README, LICENSE, NOTICE, docs sources (install, algos, rl_tips, examples, export, imitation, RL Zoo, SB3-Contrib), on_policy_algorithm.py, tags, issues", accessed: 2026-11-25}
  - {url: "https://stable-baselines3.readthedocs.io/en/master/modules/ppo.html", title: "SB3 docs: PPO", accessed: 2026-11-25}
  - {url: "https://stable-baselines3.readthedocs.io/en/master/guide/vec_envs.html", title: "SB3 docs: Vectorized Environments", accessed: 2026-11-25}
  - {url: "https://pypi.org/project/stable-baselines3/", title: "PyPI: stable-baselines3, sb3-contrib, rl-zoo3, rsl-rl-lib and rl-games release histories", accessed: 2026-11-25}
  - {url: "https://isaac-sim.github.io/IsaacLab/main/source/concepts/reinforcement_learning.html", title: "Isaac Lab docs: Reinforcement Learning (choosing an RL library)", accessed: 2026-11-25}
  - {url: "https://github.com/isaac-sim/IsaacLab/blob/main/source/isaaclab_rl/isaaclab_rl/sb3.py", title: "Isaac Lab Stable-Baselines3 wrapper source", accessed: 2026-11-25}
---

# Stable-Baselines3

Stable-Baselines3 (SB3) is a PyTorch library of tested model-free RL algorithms behind one
interface, `PPO("MlpPolicy", env).learn(...)`, for [Gymnasium](gymnasium.md) environments: a
MuJoCo task, your simulator, or a real robot wrapped as an `Env` [1]. MIT [1]. **2.9.2**
(2026-10-26) [4]; DLR-RM maintains it, and new algorithms go to SB3-Contrib [1].

## When to use it

- **Use it** with one to a few dozen CPU environments, a custom or real-robot `Env`, or for
  sample-efficient off-policy learning: SAC, TD3, and TQC or CrossQ from SB3-Contrib are the docs'
  picks for continuous control in one process [1].
- **Use RSL-RL or rl_games** with thousands of GPU environments ([Isaac Lab](isaac-lab.md)). Isaac
  Lab's docs default to RSL-RL (BSD-3-Clause, 6.0.0 on 2026-11-20) and find SB3 best for smaller
  experiments [4][5]; its SB3 wrapper copies GPU tensors to NumPy every step and builds per-env
  infos in a Python loop [6]. On [ManiSkill](maniskill.md)'s GPU backend, use its own baselines.

## Setup

```bash
pip install "stable-baselines3[extra]" sb3-contrib rl_zoo3   # 2.9.2; Python 3.10+, PyTorch 2.8+
python -m rl_zoo3.train --algo sac --env Pendulum-v1           # tuned hyperparameters from the Zoo
```

Pure Python with `gymnasium>=0.29.1,<2.0`; no GPU needed [1][4]. Algorithms: A2C, DDPG, DQN, HER,
PPO, SAC, TD3; SB3-Contrib adds ARS, CrossQ, MaskablePPO, QR-DQN, RecurrentPPO, TQC, TRPO [1].

## How an agent works with it

```python
from stable_baselines3 import SAC
from stable_baselines3.common.env_checker import check_env
check_env(env)                                  # your Gymnasium Env
model = SAC("MlpPolicy", env, device="cpu", verbose=1).learn(200_000)
model.save("sac_reach")                         # a zip; SAC.load("sac_reach") restores it
action, _ = model.predict(obs, deterministic=True)
```

Watch the episode reward in TensorBoard, then test with `evaluate_policy` on new seeds. The RL
Zoo adds Optuna tuning, plots and videos; the `imitation` library adds BC, DAgger and GAIL [1].

## Traps

- **PPO on the GPU is slower.** `device="auto"` picks CUDA, but "PPO is meant to be run primarily
  on the CPU" without a CNN [2]; SB3 warns and trains slowly. Pass `device="cpu"` [1].
- **Unnormalised spaces.** Scale actions to [-1, 1], normalise observations (`VecNormalize`),
  and load its saved statistics with `training = False` at inference, or inputs drift [1].
- **SB3's VecEnv is not Gymnasium's.** `step` returns `obs, rewards, dones, infos` and `reset`
  only `obs`; done envs reset at once (last obs: `infos[i]["terminal_observation"]`) [3].
- **Exported actions are raw.** ONNX export of `model.policy` skips the clip or unscale step for
  continuous actions; add it in the robot's runtime [1].
- **Not reproducible across devices.** CPU, GPU and PyTorch versions differ with one seed [1].

## Alternatives

RSL-RL, rl_games, skrl, CleanRL, TorchRL, SBX (SB3 in JAX); see [Isaac Lab](isaac-lab.md).

## Sources

1. [stable-baselines3 repository: README, LICENSE, NOTICE, docs sources (install, algos, rl_tips, examples, export, imitation, RL Zoo, SB3-Contrib), on_policy_algorithm.py, tags, issues](https://github.com/DLR-RM/stable-baselines3), accessed 2026-11-25
2. [SB3 docs: PPO](https://stable-baselines3.readthedocs.io/en/master/modules/ppo.html), accessed 2026-11-25
3. [SB3 docs: Vectorized Environments](https://stable-baselines3.readthedocs.io/en/master/guide/vec_envs.html), accessed 2026-11-25
4. [PyPI: stable-baselines3, sb3-contrib, rl-zoo3, rsl-rl-lib and rl-games release histories](https://pypi.org/project/stable-baselines3/), accessed 2026-11-25
5. [Isaac Lab docs: Reinforcement Learning (choosing an RL library)](https://isaac-sim.github.io/IsaacLab/main/source/concepts/reinforcement_learning.html), accessed 2026-11-25
6. [Isaac Lab Stable-Baselines3 wrapper source](https://github.com/isaac-sim/IsaacLab/blob/main/source/isaaclab_rl/isaaclab_rl/sb3.py), accessed 2026-11-25

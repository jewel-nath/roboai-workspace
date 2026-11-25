---
type: tool
name: Gymnasium
summary: The Farama Foundation's maintained successor to OpenAI Gym - the standard Python API between RL environments and learning code, plus reference tasks such as the MuJoCo set (v5); MIT. Its 0.26/1.x API (reset returning info, step returning terminated and truncated, next-step vector autoreset) breaks old Gym code.
tags: [gymnasium, gym, openai-gym, farama, reinforcement-learning, environment-api, mujoco, vector-env, shimmy, gymnasium-robotics]
kind: library
area: learning
support:
license: MIT
links: {repo: "https://github.com/Farama-Foundation/Gymnasium", docs: "https://gymnasium.farama.org", site: "https://farama.org"}
version: {tested: , latest: 1.4.0, as_of: 2026-11-25}
platforms: [linux, windows, macos]
agent_access: script
registry:
evidence: researched
last_verified: 2026-11-25
sources:
  - {url: "https://github.com/Farama-Foundation/Gymnasium", title: "Gymnasium repository: README, LICENSE, pyproject.toml, vector and registration source, tags, issues", accessed: 2026-11-25}
  - {url: "https://github.com/Farama-Foundation/Gymnasium/releases", title: "Gymnasium releases v1.0.0 to v1.4.0", accessed: 2026-11-25}
  - {url: "https://gymnasium.farama.org/introduction/migration_guide/", title: "Gymnasium docs: Migration guide (Gym v0.21 to v0.26+)", accessed: 2026-11-25}
  - {url: "https://gymnasium.farama.org/environments/mujoco/", title: "Gymnasium docs: MuJoCo environments", accessed: 2026-11-25}
  - {url: "https://farama.org/Vector-Autoreset-Mode", title: "Farama: Vector autoreset modes (2025-02-20)", accessed: 2026-11-25}
  - {url: "https://pypi.org/project/gymnasium/", title: "PyPI: gymnasium, gym, shimmy and gymnasium-robotics release histories", accessed: 2026-11-25}
---

# Gymnasium

Gymnasium is the standard Python interface between an RL algorithm and an environment (`reset()`,
`step()`, typed spaces): the Farama Foundation's fork of OpenAI Gym, where Gym's maintainers went;
Gym stopped at 0.26.2 (2022-10-04) [1][6]. Builders wrap a robot or simulator in it for RL.
MIT. **1.4.0** (2026-10-05); last commit 2026-11-25, 65 issues open [1][6].

## When to use it

- **Use it** so any RL library ([Stable-Baselines3](stable-baselines3.md)) can train on your
  robot, simulator or task, and for the MuJoCo reference tasks (Ant, Hopper, Humanoid) [4].
  Fetch, Shadow hand and Franka Kitchen tasks are in Gymnasium-Robotics (MIT, 1.4.2) [6].

## Setup

```bash
pip install "gymnasium[mujoco]"   # 1.4.0, Python 3.10+ (main: 3.11+); pure Python, no GPU [1][6]
python -c "import gymnasium as gym; print(gym.make('Ant-v5').reset(seed=0)[0].shape)"
```

## How an agent works with it

```python
import gymnasium as gym, numpy as np
class ReachEnv(gym.Env):
    observation_space = gym.spaces.Box(-np.inf, np.inf, (12,), np.float32)
    action_space = gym.spaces.Box(-1.0, 1.0, (6,), np.float32)   # scale to the joints yourself
    def reset(self, seed=None, options=None):
        super().reset(seed=seed)                                 # seeds self.np_random
        return self._obs(), {}
    def step(self, action):                                      # act, wait one control period
        return self._obs(), self._reward(), self._reached(), False, {}
gym.register("Reach-v0", entry_point=ReachEnv, max_episode_steps=200)   # TimeLimit truncates
```

Check it with `gymnasium.utils.env_checker.check_env(env)`; batch it with `gym.make_vec` [1].

## Traps

- **Old Gym code.** `obs, info = env.reset(seed=...)` replaces `env.reset()` and `env.seed()`;
  `step` returns `terminated, truncated` instead of `done`; `render_mode` goes to `make` [3].
  Wrap old envs with Shimmy: `gym.make("shimmy:GymV26Environment-v0", env_id=...)` [1].
- **`truncated` is not `terminated`.** A time limit truncates: bootstrap the value there, not at
  a real end. Merging both into one `done` biases learning [3].
- **Next-step autoreset (1.0+).** A finished sub-environment resets on the *next* `step()`, which
  ignores the action and returns zero reward [1][2]; loops written for 0.29 store a bogus
  transition. Mask it, or set `autoreset_mode="SameStep"` (final obs in `info["final_obs"]`) [5].
- **Versions.** MuJoCo v5 (`mujoco>=2.3.3`) is recommended, v4 kept, v2/v3 moved to
  Gymnasium-Robotics in 1.2; scores across versions do not compare [4]. Since 1.0, `import` an
  env's package (or call `gym.register_envs`) before `make` [2].
- **Batched simulators.** [ManiSkill](maniskill.md) and [Isaac Lab](isaac-lab.md) register
  Gymnasium IDs but return batched torch tensors on the GPU; see their pages first.

## Alternatives

PettingZoo (multi-agent, Farama), dm_env (DeepMind), the batched APIs of ManiSkill and Isaac Lab.

## Sources

1. [Gymnasium repository: README, LICENSE, pyproject.toml, vector and registration source, tags, issues](https://github.com/Farama-Foundation/Gymnasium), accessed 2026-11-25
2. [Gymnasium releases v1.0.0 to v1.4.0](https://github.com/Farama-Foundation/Gymnasium/releases), accessed 2026-11-25
3. [Gymnasium docs: Migration guide (Gym v0.21 to v0.26+)](https://gymnasium.farama.org/introduction/migration_guide/), accessed 2026-11-25
4. [Gymnasium docs: MuJoCo environments](https://gymnasium.farama.org/environments/mujoco/), accessed 2026-11-25
5. [Farama: Vector autoreset modes (2025-02-20)](https://farama.org/Vector-Autoreset-Mode), accessed 2026-11-25
6. [PyPI: gymnasium, gym, shimmy and gymnasium-robotics release histories](https://pypi.org/project/gymnasium/), accessed 2026-11-25

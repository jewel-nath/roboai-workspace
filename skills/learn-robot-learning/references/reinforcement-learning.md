# Reinforcement learning: Isaac Lab, ManiSkill, Stable-Baselines3

Part of [learn-robot-learning](../SKILL.md). Checked against Isaac Lab v3.0.0 (2026-10-19:
`docs/source/concepts/reinforcement_learning.rst`, `isaaclab/quickstart.rst`, `installation.rst`, task
registrations), ManiSkill 3.0.1 (`main` 62ff3a5: RL setup and baselines docs, `examples/baselines/ppo`),
Stable-Baselines3 2.9.2 (`docs/guide/rl_tips.md`, `custom_env.md`, `export.md`, source) and Gymnasium 1.4.0
(`docs/introduction/create_custom_env.md`). Nothing here was run.

Transfer to hardware (randomisation, identification, observation design, staged tests) is the job of
[sim-to-real](../../sim-to-real/SKILL.md); Isaac Lab randomisation terms and policy export are in its
[isaac-lab.md](../../sim-to-real/references/isaac-lab.md).

## Choose a stack

| Stack | Good at | Needs | Licence |
|---|---|---|---|
| Isaac Lab 3.0 | Thousands of GPU-parallel environments; legged and humanoid locomotion (Go2, G1, H1, ANYmal-D, Cassie), arms and hands; RSL-RL, skrl, RL-Games, SB3, TorchRL | NVIDIA GPU, Python 3.12, Ubuntu 22.04+ or Windows 11; Newton physics by default, Isaac Sim 6.2 optional | BSD-3-Clause; Isaac Sim parts under NVIDIA terms |
| ManiSkill 3.0.1 | GPU-parallel SAPIEN manipulation, visual RL, standard PPO baselines, an SO-100 twin | NVIDIA GPU for GPU simulation; Vulkan for rendering; Linux best supported | Environments Apache-2.0; **assets CC BY-NC 4.0** |
| SB3 2.9.2 on Gymnasium 1.4 | Tested PPO, SAC, TD3 and others on any Gymnasium environment, CPU is fine for state-based tasks | Python 3.10+ (2.9.2 is the last release for 3.10) | MIT |

Pick Isaac Lab for locomotion and anything needing massive parallelism, ManiSkill for tabletop manipulation
with GPU sim, SB3 for a small environment you wrote yourself (MuJoCo, PyBullet, a kinematic model).

## Isaac Lab 3.0

```bash
git clone https://github.com/isaac-sim/IsaacLab.git && cd IsaacLab && git checkout v3.0.0
uv run isaaclab list_envs
uv run isaaclab random_agent --task Isaac-Velocity-Flat-UnitreeGo2 --num_envs 16        # env resets and steps
uv run isaaclab train --rl_library rsl_rl --task Isaac-Velocity-Flat-UnitreeGo2 \
  --num_envs 64 --max_iterations 10                                                    # smoke test
uv run isaaclab train --rl_library rsl_rl --task Isaac-Velocity-Rough-UnitreeGo2         # full run, headless
uv run python -m tensorboard.main --logdir logs/rsl_rl
uv run isaaclab play --rl_library rsl_rl --task Isaac-Velocity-Rough-UnitreeGo2 \
  --checkpoint latest --num_envs 32 --viz newton_gl
```

- Task ids in 3.0 have no `-v0` suffix (`Isaac-Velocity-Rough-G1`, `Isaac-Lift-Franka`, `Isaac-Reach-UR10`).
- Other libraries: `uv run --extra sb3 isaaclab train --rl_library sb3 ...`; likewise `skrl`, `rl-games`,
  `torchrl`. Isaac Lab recommends RSL-RL for new robotics projects.
- Physics backends are presets: `physics=newton_mjwarp` (the default), `physics=ovphysx` with
  `--extra ovphysx`; Isaac Sim with the `isaacsim` extra (16 GB VRAM and an RTX GPU on Linux).
- `play --checkpoint` takes `latest`, `best`, `pretrained` (published checkpoints for some core tasks) or a
  path; `--video --video_length 200` records a clip (`--extra video`).
- Watch mean reward and episode length trends, throughput, and for PPO the entropy, KL and action standard
  deviation; absolute reward values are task-specific.
- Your own robot: copy a velocity task config, swap the articulation (URDF or USD), joint names, default pose,
  actuator gains and observation scales; keep the deploy spec of [sim-to-real](../../sim-to-real/SKILL.md).

## ManiSkill 3

```bash
pip install --upgrade mani_skill torch
python -m mani_skill.examples.demo_random_action -e PickCube-v1
git clone https://github.com/haosulab/ManiSkill && cd ManiSkill/examples/baselines/ppo
python ppo.py --env_id="PushCube-v1" --num_envs=2048 --update_epochs=8 --num_minibatches=32 \
  --total_timesteps=2_000_000 --eval_freq=10 --num-steps=20
python ppo.py --env_id="PushCube-v1" --evaluate --checkpoint=path/to/model.pt --num_eval_envs=1
python ppo_rgb.py --env_id="PickCube-v1" --num_envs=256 --update_epochs=8 --num_minibatches=8 \
  --total_timesteps=10_000_000                 # from camera images; keep it under your GPU memory
```

- `gym.make("PickCube-v1", num_envs=N)` returns batched torch tensors on the GPU, not the plain Gymnasium API.
  Wrap with `CPUGymWrapper` (single env, numpy) or `ManiSkillVectorEnv` (vector API) for other libraries.
- Fair evaluation, per the ManiSkill docs: `ignore_terminations=True` (no partial resets), and
  `reconfiguration_freq=1` so object geometry is re-randomised each reset; report success-at-end and
  success-once separately.
- The small benchmark set: `PushCube-v1`, `PickCube-v1`, `PegInsertionSide-v1`, `PushT-v1`,
  `HumanoidPlaceAppleInBowl-v1`, `AnymalC-Reach-v1`, `OpenCabinetDrawer-v1`, all with dense rewards.
- `SO100GraspCube-v1` and the `lerobot-sim2real` repository train an RGB grasping policy for an SO-100 in
  simulation; the arm model is rated "values realistic, not identified".
- The asset licence (CC BY-NC 4.0) rules out commercial use of models trained on those assets without other
  arrangements.

## Stable-Baselines3 on a Gymnasium environment

### The environment

```python
"""reach_env.py - minimal Gymnasium 1.x environment: move a point to a goal in a 2D workspace."""
import gymnasium as gym
import numpy as np
from gymnasium import spaces


class ReachEnv(gym.Env):
    metadata = {"render_modes": []}

    def __init__(self, max_step_m: float = 0.02, success_m: float = 0.02):
        self.max_step_m = max_step_m
        self.success_m = success_m
        # actions in [-1, 1]; scaled to metres inside step()
        self.action_space = spaces.Box(-1.0, 1.0, shape=(2,), dtype=np.float32)
        # position and goal, both within a 0.6 m square
        self.observation_space = spaces.Box(-0.3, 0.3, shape=(4,), dtype=np.float32)

    def _obs(self) -> np.ndarray:
        return np.concatenate([self.pos, self.goal]).astype(np.float32)

    def reset(self, *, seed=None, options=None):
        super().reset(seed=seed)  # seeds self.np_random
        self.pos = self.np_random.uniform(-0.25, 0.25, size=2)
        self.goal = self.np_random.uniform(-0.25, 0.25, size=2)
        self.prev_dist = float(np.linalg.norm(self.goal - self.pos))
        return self._obs(), {}

    def step(self, action):
        action = np.clip(action, -1.0, 1.0)
        self.pos = np.clip(self.pos + action * self.max_step_m, -0.3, 0.3)
        dist = float(np.linalg.norm(self.goal - self.pos))
        # potential-based shaping: progress towards the goal, plus a success bonus and a small action cost
        reward = (self.prev_dist - dist) * 10.0 - 0.01 * float(np.square(action).sum())
        self.prev_dist = dist
        terminated = dist < self.success_m
        if terminated:
            reward += 1.0
        return self._obs(), reward, terminated, False, {"is_success": terminated}


gym.register(id="Reach2D-v0", entry_point=ReachEnv, max_episode_steps=200)  # TimeLimit sets truncated
```

Rules the example follows (SB3 RL tips, Gymnasium docs):

- Continuous actions in a symmetric `[-1, 1]` box, scaled to physical units inside `step()`.
- Observations bounded and normalised (or wrapped in `VecNormalize`); include the goal, relative where possible.
- `reset()` calls `super().reset(seed=seed)` and draws randomness from `self.np_random` only.
- `terminated` for task end (success or failure), `truncated` for the time limit; never fold a time limit into
  `terminated`, or values are learned for a terminal state that does not exist.
- Shaping as a potential difference (`gamma * phi(s') - phi(s)`, Ng et al. 1999, here with gamma about 1) keeps the
  optimal policy; ad hoc bonuses can create loops the agent exploits. Check the reward on random rollouts first.
- `info["is_success"]` lets `EvalCallback` and `evaluate_policy` report a success rate.

### Train, evaluate, save

```python
"""train_reach.py - PPO on Reach2D-v0 with normalisation, evaluation and checkpoints."""
import gymnasium as gym
from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import CheckpointCallback, EvalCallback
from stable_baselines3.common.env_checker import check_env
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.common.vec_env import SubprocVecEnv, VecNormalize

import reach_env  # noqa: F401  registers Reach2D-v0

if __name__ == "__main__":
    check_env(gym.make("Reach2D-v0").unwrapped)

    venv = VecNormalize(make_vec_env("Reach2D-v0", n_envs=8, seed=0, vec_env_cls=SubprocVecEnv))
    eval_env = VecNormalize(make_vec_env("Reach2D-v0", n_envs=1, seed=1000), training=False, norm_reward=False)

    model = PPO("MlpPolicy", venv, seed=0, verbose=1, tensorboard_log="runs/reach")
    callbacks = [
        EvalCallback(eval_env, n_eval_episodes=50, eval_freq=10_000, deterministic=True,
                     best_model_save_path="models/reach", log_path="models/reach"),
        CheckpointCallback(save_freq=50_000, save_path="models/reach/ckpt", save_vecnormalize=True),
    ]
    model.learn(total_timesteps=500_000, callback=callbacks)
    model.save("models/reach/final")
    venv.save("models/reach/vecnormalize.pkl")            # the policy is useless without these statistics

    # reload exactly as a deployment would
    test_env = VecNormalize.load("models/reach/vecnormalize.pkl", make_vec_env("Reach2D-v0", n_envs=1, seed=2000))
    test_env.training, test_env.norm_reward = False, False
    model = PPO.load("models/reach/final", env=test_env)
    mean, std = evaluate_policy(model, test_env, n_eval_episodes=100, deterministic=True)
    print(f"return {mean:.2f} +/- {std:.2f}")
```

- `EvalCallback` copies the training `VecNormalize` statistics into the evaluation env before each evaluation.
- Evaluate with `deterministic=True` over many seeds; report success rate, not only return.
- SAC or TD3 for sample efficiency on continuous control; PPO when simulation is cheap and parallel.
- For deployment, SB3's ONNX export recipe wraps `model.policy` in a module and returns actions before
  SB3's clipping and rescaling, so apply those, and the `VecNormalize` observation statistics, on the robot. The
  export and the on-robot node are in [learn-edge-deployment](../../learn-edge-deployment/SKILL.md).
- Imitation algorithms on top of SB3 (behaviour cloning, DAgger, GAIL) live in the separate `imitation` package;
  SB3 itself has no `BC` class.

## Before calling an RL policy done

- The environment passes `check_env` and a random-action rollout gives sensible rewards and terminations.
- Training curves for at least two seeds; the result does not depend on one lucky seed.
- Deterministic evaluation over 100+ episodes with randomisation and noise on, success rate with an interval
  ([evaluation.md](evaluation.md#3-report-numbers-with-an-interval)).
- Normalisation statistics, observation and action scaling, control rate and joint order saved with the
  checkpoint (the deploy spec in [sim-to-real](../../sim-to-real/SKILL.md)).
- Licences of simulator assets checked (ManiSkill assets are non-commercial).

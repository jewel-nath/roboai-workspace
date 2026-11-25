---
type: tool
name: Diffusion Policy
summary: Chi et al.'s visuomotor imitation policy that denoises a short chunk of future actions from camera frames and robot state; the reference repo (MIT) is unreleased and quiet since 2023, and the method is maintained in LeRobot (Apache-2.0, U-Net variant) and robomimic 0.5. Needs a CUDA GPU to train (about 8 to 14 GB in LeRobot's guide); inference latency claims range from 0.1 s to 0.37 s per chunk.
tags: [diffusion-policy, imitation-learning, behavior-cloning, visuomotor, action-chunking, ddpm, ddim, unet, transformer, lerobot, robomimic, push-t, so-101, manipulation]
kind: policy
area: learning
support:
license: MIT
links: {repo: "https://github.com/real-stanford/diffusion_policy", docs: , site: "https://diffusion-policy.cs.columbia.edu/"}
version: {tested: , latest: , as_of: 2026-11-25}
platforms: [linux]
agent_access: script
registry:
evidence: researched
last_verified: 2026-11-25
sources:
  - {url: "https://github.com/real-stanford/diffusion_policy", title: "diffusion_policy repository: README, LICENSE, conda_environment.yaml, configs, eval_real_robot.py, Push-T env and runner, history", accessed: 2026-11-25}
  - {url: "https://arxiv.org/abs/2303.04137", title: "Chi et al.: Diffusion Policy: Visuomotor Policy Learning via Action Diffusion (arXiv v5, extended RSS 2023 paper)", accessed: 2026-11-25}
  - {url: "https://diffusion-policy.cs.columbia.edu/", title: "Diffusion Policy project site: training data and experiment checkpoints", accessed: 2026-11-25}
  - {url: "https://github.com/real-stanford/diffusion_policy/issues", title: "diffusion_policy issues, including 167 (cached_download import error)", accessed: 2026-11-25}
  - {url: "https://github.com/huggingface/lerobot/tree/v0.7.0/src/lerobot/policies/diffusion", title: "LeRobot v0.7.0 diffusion policy: configuration, model, README; config defaults compared at v0.3.3 to v0.7.0; train config; pyproject.toml", accessed: 2026-11-25}
  - {url: "https://huggingface.co/docs/lerobot/installation", title: "LeRobot docs: Installation", accessed: 2026-11-25}
  - {url: "https://pypi.org/project/lerobot/", title: "PyPI: lerobot release history and extras", accessed: 2026-11-25}
  - {url: "https://huggingface.co/docs/lerobot/main/hardware_guide", title: "LeRobot docs: Compute HW Guide for LeRobot Training", accessed: 2026-11-25}
  - {url: "https://arxiv.org/abs/2602.22818", title: "Cadene et al.: LeRobot: An Open-Source Library for End-to-End Robot Learning (inference latency table)", accessed: 2026-11-25}
  - {url: "https://huggingface.co/lerobot/diffusion_pusht", title: "Hugging Face: lerobot/diffusion_pusht model card and config, with the lerobot/pusht dataset card", accessed: 2026-11-25}
  - {url: "https://robomimic.github.io/docs/tutorials/training_diffusion_policy.html", title: "robomimic docs: Training Diffusion Policy, with diffusion_policy_config.py", accessed: 2026-11-25}
  - {url: "https://huggingface.co/docs/lerobot/multi_task_dit", title: "LeRobot docs: Multitask DiT Policy", accessed: 2026-11-25}
---

# Diffusion Policy

Diffusion Policy (Chi et al., Columbia, TRI and MIT; RSS 2023, extended for a journal) learns a
policy from demonstrations by denoising: it refines random noise, step by step, into a short
sequence of future actions, conditioned on the last few camera frames and robot states [1][2].
Builders use it as a strong single-task imitation baseline for an arm. **Licences:** reference
code MIT [1]; LeRobot's port Apache-2.0 [5]; the reference data and checkpoints on the project
site state no licence of their own [1][3]; LeRobot's PushT weights Apache-2.0, data MIT [10].

**Maintenance.** The reference repo (moved from `columbia-ai-robotics` to `real-stanford`) has no
releases or tags; its last commit (2024-12-24) only added a dataset adapter, the one before is
from 2023-10, and the newest of its 94 open issues had no maintainer reply [1][4]. Maintained:
[LeRobot](../frameworks/lerobot.md) 0.7.0 [5][7], [robomimic](../frameworks/robomimic.md) 0.5 [11].

## The method in builder terms

- **Horizons** [1][2]: the policy sees `To` observation steps (`n_obs_steps`, default 2),
  predicts `Tp` actions (`horizon`, 16) and executes the first `Ta` (`n_action_steps`, 8)
  before it predicts again. The paper found an action horizon of 8 best for most tasks.
- **Two networks** [1][2]: a 1D temporal U-Net with FiLM conditioning (CNN) and a minGPT-style
  transformer. Start with the CNN; the transformer is more sensitive to hyperparameters but copes
  better with fast, sharp action changes. Images go through a ResNet-18 encoder [1][5].
- **Denoising steps** [1][2]: training adds noise over 100 DDPM steps. Sampling all 100 is slow;
  DDIM samples in fewer. The paper reports 0.1 s inference with 10 DDIM steps on an RTX 3080;
  the real-robot configs use a DDIM scheduler, and `eval_real_robot.py` samples 16 steps.
- **Position control** [2]: absolute position targets beat velocity commands for this policy,
  and velocity control suffers more from latency.
- **Data** [2]: the authors' real tasks used 90 to 284 demos each (Push-T on a UR5: 136 demos,
  10 Hz actions interpolated to 125 Hz; sauce pouring and spreading on a Franka Panda: 90 each).

## When to use it

- **Use it** for one task with demos that solve it in more than one way, where a regression
  policy would average the modes. The paper reports a 46.9% average improvement over prior
  methods on 12 tasks from 4 benchmarks; that is the authors' claim [2].
- **On a low-cost arm** such as the [SO-101](../../robots/so-101.md), train it in LeRobot;
  [ACT](act.md) is lighter (5 ms against about 370 ms per forward pass on an RTX 4090, LeRobot's
  measurement [9]). The [UMI gripper](../../robots/umi-gripper.md) trains it from hand-held demos.
- **Use something else** for point clouds ([3D Diffusion Policy](3d-diffusion-policy.md)), or
  for many tasks with language: LeRobot's Multitask DiT, a CLIP-conditioned diffusion transformer
  [12], or a VLA such as [pi0](../models/pi0.md) or [SmolVLA](../models/smolvla.md). See
  [Choose a robot learning policy](../../guides/choose-a-robot-learning-policy.md).

## Setup

**LeRobot** (the maintained path) [5][6][7]:

```bash
conda create -y -n lerobot python=3.12 && conda activate lerobot
pip install 'lerobot[diffusion,pusht]'     # 0.7.0; PyTorch 2.7 to 2.15; pusht adds the sim
```

Linux, macOS (Apple Silicon, macOS 14+) and Windows; Linux wheels need NVIDIA driver 580.65+
[6]. LeRobot implements only the CNN (U-Net) variant [5].

**Reference repo** [1]: Linux with an NVIDIA GPU, tested on Ubuntu 20.04: the README's MuJoCo apt
packages, then `mamba env create -f conda_environment.yaml`; training logs to Weights & Biases.
A macOS environment exists for development only.

| Need | Figure | Whose |
|---|---|---|
| Training memory | about 8 to 14 GB peak at batch 8 with AdamW; RTX 4070 or better, L4, A10G | LeRobot guide, "indicative" [8] |
| Training time | about 2 to 4 h for 5 epochs of about 45,000 frames on one RTX 4090 or 3090 | LeRobot guide [8] |
| Inference | 0.1 s, 10 DDIM steps, RTX 3080 | paper [2] |
| Inference | about 370 ms on RTX 4090, 614 ms on A100, over 5 s on CPU; 263 M parameters, 10 steps | LeRobot paper [9] |
| Jetson | no upstream figure | none |

The reference repo gives no memory figure [1]. The latency claims differ threefold: measure yours.

## How an agent works with it

**LeRobot** [5][10]. Train on a LeRobotDataset and evaluate in simulation:

```bash
lerobot-train --policy.type=diffusion --dataset.repo_id=<user>/<dataset> \
  --policy.horizon=16 --policy.n_action_steps=8 --ema.type=warmup \
  --policy.repo_id=<user>/dp_<task> --output_dir=outputs/train/dp_<task>
lerobot-eval --policy.path=lerobot/diffusion_pusht --env.type=pusht \
  --eval.n_episodes=50 --policy.device=cuda
```

- **Inputs:** `observation.images.<camera>` (every camera the same shape), `observation.state`
  and `action` from the dataset. Defaults: images mean-std normalised; state and action min-max
  scaled to [-1, 1]; ResNet-18 with ImageNet weights [5].
- **Running:** `DiffusionPolicy.from_pretrained(path)`, `policy.reset()` at each episode start,
  then `policy.select_action(batch)` each control step. It predicts a whole chunk, queues
  `n_action_steps` actions and returns one per call [5].

**Reference repo** [1]: Hydra configs per task and method; `python train.py
--config-name=<workspace>.yaml task=<task>` evaluates every 50 epochs as `test/mean_score`, and
`eval.py --checkpoint <ckpt>` re-scores one. Data is a Zarr `ReplayBuffer` (all episodes
concatenated per field, plus `meta/episode_ends`). On a [UR5](../../robots/universal-robots.md),
`demo_real_robot.py` records SpaceMouse demos and `eval_real_robot.py` runs at 10 Hz by default.

**Check:** loss falls and simulated success rises; then a slow first run on the robot, hand on the
e-stop, with speed or torque limits. See
[skills/learn-robot-learning/SKILL.md](../../../skills/learn-robot-learning/SKILL.md).

## Traps

- **LeRobot's defaults changed.** From 0.6.0 `horizon` is 64 and `n_action_steps` 32 (16 and 8
  before, as in the paper and the PushT checkpoint); `drop_n_last_frames` stayed 7, though its
  comment says `horizon - n_action_steps - n_obs_steps + 1` [5][10]. Set all three explicitly.
- **No EMA by default.** The reference code evaluates an exponential moving average of the
  weights; LeRobot does so only with `--ema.type=warmup`, then loads `pretrained_model_ema` [5].
- **100 steps per action chunk.** With `num_inference_steps` unset, LeRobot samples every one of
  the 100 training steps. For a real robot, train with `--policy.noise_scheduler_type=DDIM` and
  set `--policy.num_inference_steps` near 10 [1][5].
- **Actions stay inside the demos.** Min-max scaling plus `clip_sample` (on by default) keeps
  outputs inside the range seen in training, and one outlier squashes the rest. The README calls
  normalisation a common source of bugs; print the scale and offset per key [1][5].
- **Record positions, not velocities** [2]. robomimic's robosuite data uses delta actions; the
  reference repo converts it to absolute poses with a 6D rotation (`image_abs.hdf5`) [1].
- **Horizon counts dataset steps.** 16 steps last 1.6 s at the paper's 10 Hz but 0.53 s at 30
  fps; tune horizons in seconds. The paper held peak performance with up to 4 steps of latency;
  the real-robot code offsets actions by `n_latency_steps` [1][2].
- **Camera mismatch.** Camera names, order and image size at run time must match training;
  LeRobot rejects cameras of different shapes and crops larger than the image [5].
- **The reference environment has rotted.** It pins Python 3.9, PyTorch 1.12.1 with CUDA 11.6,
  diffusers 0.11.1, gym 0.21, mujoco-py, a robosuite fork and robomimic 0.2.0 [1]. A newer
  `huggingface_hub` fails on `cached_download`; the reporter pinned 0.10.1 [4]. robosuite envs in
  forked subprocesses can segfault on their OpenGL context [1].
- **Checkpoints are pickles.** Reference `.ckpt` files load with `torch.load` and `dill`, which
  can run code: load only your own or trusted files. LeRobot stores safetensors [1][10].
- **Push-T scores do not compare.** The reference logs `test/mean_score`, a mean best coverage
  reward [1]; LeRobot counts success at 95% overlap and reports 65.4% for its checkpoint and
  64.2% for one from the reference code, over 500 episodes in its own evaluation [10].

## Alternatives

[ACT](act.md), [3D Diffusion Policy](3d-diffusion-policy.md), Multitask DiT [12],
[pi0](../models/pi0.md), [SmolVLA](../models/smolvla.md); benchmarks:
[LIBERO](../benchmarks/libero.md), [RoboCasa](../benchmarks/robocasa.md).

## Sources

1. [diffusion_policy repository: README, LICENSE, conda_environment.yaml, configs, eval_real_robot.py, Push-T env and runner, history](https://github.com/real-stanford/diffusion_policy), accessed 2026-11-25
2. [Chi et al.: Diffusion Policy: Visuomotor Policy Learning via Action Diffusion (arXiv v5, extended RSS 2023 paper)](https://arxiv.org/abs/2303.04137), accessed 2026-11-25
3. [Diffusion Policy project site: training data and experiment checkpoints](https://diffusion-policy.cs.columbia.edu/), accessed 2026-11-25
4. [diffusion_policy issues, including 167 (cached_download import error)](https://github.com/real-stanford/diffusion_policy/issues), accessed 2026-11-25
5. [LeRobot v0.7.0 diffusion policy: configuration, model, README; config defaults compared at v0.3.3 to v0.7.0; train config; pyproject.toml](https://github.com/huggingface/lerobot/tree/v0.7.0/src/lerobot/policies/diffusion), accessed 2026-11-25
6. [LeRobot docs: Installation](https://huggingface.co/docs/lerobot/installation), accessed 2026-11-25
7. [PyPI: lerobot release history and extras](https://pypi.org/project/lerobot/), accessed 2026-11-25
8. [LeRobot docs: Compute HW Guide for LeRobot Training](https://huggingface.co/docs/lerobot/main/hardware_guide), accessed 2026-11-25
9. [Cadene et al.: LeRobot: An Open-Source Library for End-to-End Robot Learning (inference latency table)](https://arxiv.org/abs/2602.22818), accessed 2026-11-25
10. [Hugging Face: lerobot/diffusion_pusht model card and config, with the lerobot/pusht dataset card](https://huggingface.co/lerobot/diffusion_pusht), accessed 2026-11-25
11. [robomimic docs: Training Diffusion Policy, with diffusion_policy_config.py](https://robomimic.github.io/docs/tutorials/training_diffusion_policy.html), accessed 2026-11-25
12. [LeRobot docs: Multitask DiT Policy](https://huggingface.co/docs/lerobot/multi_task_dit), accessed 2026-11-25

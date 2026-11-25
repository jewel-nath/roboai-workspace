---
type: tool
name: ACT (Action Chunking with Transformers)
summary: The imitation-learning policy from the ALOHA paper - a small transformer that predicts the next chunk of joint targets from camera images and joint positions, trained from about 50 demonstrations on one GPU; the usual first policy for low-cost arms, run today through LeRobot because the original MIT repo has had no commit since January 2024.
tags: [act, action-chunking, aloha, imitation-learning, behaviour-cloning, transformer, cvae, temporal-ensembling, lerobot, so-101, koch, bimanual, low-cost-arm]
kind: policy
area: learning
support:
license: MIT
links: {repo: "https://github.com/tonyzhaozh/act", docs: "https://huggingface.co/docs/lerobot/act", site: "https://tonyzhaozh.github.io/aloha/"}
version: {tested: , latest: , as_of: 2026-11-25}
platforms: [linux, macos, windows]
agent_access: script
registry:
evidence: researched
last_verified: 2026-11-25
sources:
  - {url: "https://github.com/tonyzhaozh/act", title: "ACT repository: README, LICENSE, conda_env.yaml, imitate_episodes.py, constants.py, utils.py, history", accessed: 2026-11-25}
  - {url: "https://arxiv.org/abs/2304.13705", title: "Zhao, Kumar, Levine, Finn: Learning Fine-Grained Bimanual Manipulation with Low-Cost Hardware (arXiv 2304.13705, read in the ar5iv HTML render)", accessed: 2026-11-25}
  - {url: "https://docs.google.com/document/d/1FVIZfoALXg_ZkYKaYVh-qOlaXveq5CtvJHXkY25eYhs/edit", title: "ACT tuning tips (Google Doc linked from the ACT README)", accessed: 2026-11-25}
  - {url: "https://github.com/tonyzhaozh/act/issues", title: "ACT repository issues", accessed: 2026-11-25}
  - {url: "https://github.com/MarkFzp/act-plus-plus", title: "act-plus-plus (Mobile ALOHA) repository: README, LICENSE, history", accessed: 2026-11-25}
  - {url: "https://huggingface.co/docs/lerobot/act", title: "LeRobot docs: ACT (Action Chunking with Transformers)", accessed: 2026-11-25}
  - {url: "https://github.com/huggingface/lerobot/tree/main/src/lerobot", title: "LeRobot source: policies/act (configuration_act.py, modeling_act.py), configs (train.py, dataset.py), robots/so_follower config", accessed: 2026-11-25}
  - {url: "https://huggingface.co/docs/lerobot/hardware_guide", title: "LeRobot docs: Compute Hardware Guide", accessed: 2026-11-25}
  - {url: "https://huggingface.co/docs/lerobot/il_robots", title: "LeRobot docs: Imitation Learning on Real-World Robots", accessed: 2026-11-25}
  - {url: "https://huggingface.co/docs/lerobot/remote_inference", title: "LeRobot docs: Remote Inference", accessed: 2026-11-25}
  - {url: "https://github.com/haosulab/ManiSkill", title: "ManiSkill repository: examples/baselines (act, diffusion_policy)", accessed: 2026-11-25}
  - {url: "https://huggingface.co/datasets/lerobot/aloha_sim_transfer_cube_human", title: "Hugging Face dataset card: lerobot/aloha_sim_transfer_cube_human (licence field)", accessed: 2026-11-25}
---

# ACT (Action Chunking with Transformers)

ACT is the imitation-learning policy of the ALOHA paper (Zhao, Kumar, Levine and Finn, 2023)
[2]. Given camera images and the current joint positions, it predicts the next *k* joint targets
at once (a chunk) instead of one action per step, which the authors show cuts compounding errors
on imprecise low-cost hardware with human demonstrations [2]. Builders train it per task from
about 50 demonstrations, as the first policy on a leader-follower arm; LeRobot recommends it first
[6]. **Code: MIT** in the original repo [1], Apache-2.0 in LeRobot's port [7]. There are no
pretrained policy weights: you train your own, starting from torchvision's ImageNet ResNet-18 [7].
**The original repo is unmaintained** (last commit 2024-01-28, no releases) [1]; use LeRobot.

## When to use it

- **Use it** for one task in a fixed scene on a low-cost arm such as the
  [SO-101](../../robots/so-101.md) or [Koch v1.1](../../robots/koch-v1-1.md), with 50 or more
  teleoperated demonstrations and a small GPU (see Setup). ALOHA itself used two ViperX
  followers and two WidowX leaders
  ([Interbotix X-series arms](../../robots/interbotix-x-series-arms.md)) [2].
- **Use something else** when one policy must follow language over many tasks
  ([SmolVLA](../models/smolvla.md), [pi0](../models/pi0.md)); when ACT plateaus, try
  [Diffusion Policy](diffusion-policy.md) (about 8 to 14 GB to train [8]); for point clouds,
  [DP3](3d-diffusion-policy.md). See
  [Choose a robot learning policy](../../guides/choose-a-robot-learning-policy.md).

## Setup

Through [LeRobot](../frameworks/lerobot.md), which ships ACT in its base install [6]:

```bash
pip install 'lerobot[core_scripts,training,feetech]'      # Python 3.12+; see the LeRobot page
lerobot-train --dataset.repo_id=$HF_USER/my_task --policy.type=act --policy.device=cuda \
  --policy.repo_id=$HF_USER/act_my_task --steps=20000
```

**GPU.** LeRobot's guide puts ACT at about 2 to 6 GB of VRAM at batch 8 (its starter GPUs include
a laptop RTX 3060); 5 epochs over a 50-episode dataset take about 30 to 60 minutes on an RTX 4090,
1 to 2 hours on an L4 or A10G, and 6 to 14 hours on an Apple M-series Max through MPS [8]. The
paper trained in about 5 hours on an 11 GB RTX 2080 Ti, with about 80 M parameters and about
0.01 s per inference [2]. Upstream gives no Jetson figures. CPU training is not advised [8].

**Original repo** (for reproducing the paper only): a conda env with Python 3.8.10, unpinned
`torch`, `mujoco==2.3.7` and `dm_control==1.0.14`, then `pip install -e detr` [1]. Its training and
evaluation code calls `.cuda()` directly, so it needs an NVIDIA GPU [1]. Mobile ALOHA's fork
`act-plus-plus` (MIT) adds Diffusion Policy and VINN; its last commit is 2024-01-10 [5].

## How an agent works with it

**The model** [2][7]: a ResNet-18 encodes each camera; a transformer encoder mixes the image
features, the joint state and a style latent *z*; a decoder outputs `chunk_size` future actions.
Training adds a CVAE encoder that sees the true action chunk and produces *z*; inference sets
*z* to zero. The loss is L1 on the actions plus `kl_weight` times the KL term [2][7]. Actions are
absolute joint targets (14 numbers on ALOHA: 7 per arm, gripper included); the paper found delta
joint actions worse [2].

**Inputs and outputs in LeRobot** [7][9]: one or more `observation.images.<name>` (all the same
shape), `observation.state`, and `action`, normalised by mean and standard deviation from the
dataset's `meta/stats.json`. The control rate is the dataset's fps (30 on an SO-101 by default;
ALOHA recorded at 50 Hz [2]). Record at least 50 episodes, about 10 per object position, with
cameras fixed [9].

**Hyperparameters that matter** (LeRobot defaults from `configuration_act.py` [7]; advice from the
authors' tuning tips [3]):

| Parameter | LeRobot default | What to know |
|---|---|---|
| `chunk_size` | 100 | The most important one to tune. Aim for about 1 s of motion per chunk [3]: 100 was 2 s at ALOHA's 50 Hz, but 3.3 s at 30 fps |
| `n_action_steps` | 100 | Actions executed before the next query; the tips suggest running each chunk fully [3] |
| `temporal_ensemble_coeff` | None (off) | The paper's ensembling, weights exp(-m i) with m = 0.01 in the original code [1][2]; needs `n_action_steps=1`, so the policy runs every tick [7] |
| `kl_weight` | 10 | Keep it high (10 or 100), or drop the CVAE with `use_vae=false` [3] |
| `use_vae` | true | On human demos the paper's success fell from 35.3% to 2% without it [2] |
| batch size, `optimizer_lr` | 8, 1e-5 | Larger batches with a higher rate train better: 64 with 5e-5 rather than 8 with 1e-5 [3][7] |
| `n_decoder_layers` | 1 | Matches the original, whose 7-layer decoder used only its first layer (a bug) [7] |

**Check the result.** In simulation, LeRobot's `aloha` environment runs the paper's Transfer Cube
and Insertion tasks; `lerobot-eval` reports a success rate (the authors expect about 90% and 50%
with scripted data) [1][7]. On the robot, run `lerobot-rollout --strategy.type=base
--policy.path=$HF_USER/act_my_task ... --duration=60`, first with `--robot.max_relative_target`
set small (it caps each step's joint change; off by default) [6][7]. Compare several checkpoints:
success and smoothness keep improving after the loss flattens [1][3].

## Traps

- **Chunks too long for your rate.** With the defaults the arm runs 100 steps, 3.3 s at 30 fps,
  between observations. Try a chunk of about 30 at 30 fps, or keep 100 and set `n_action_steps`
  lower so it re-plans sooner [3][7].
- **Jerky motion or pauses mid-episode.** The authors' answer is to train longer, well past the
  loss plateau, and to try several checkpoints [1][3]. LeRobot's guide says imitation learning
  usually converges in 5 to 10 epochs [8]; judge on the robot, not by the loss.
- **Temporal ensembling costs compute and is incompatible with remote inference.** It forces a
  forward pass every control tick; disable it for LeRobot's remote policy server [7][10]. If the
  robot moves slowly because inference lags, the tips say to switch ensembling off [3].
- **Camera set is fixed at training time.** Names, count, order and resolution must match at
  rollout, and every camera must share one shape [7][9]. LeRobot shares one ResNet-18 across all
  cameras; the authors found separate backbones per camera better, which needs a code change
  [3][7].
- **Paper numbers are the authors', on ALOHA.** 50 demonstrations per task (100 for Thread
  Velcro), 10 to 20 minutes of data per task, gave 84 to 96% on four tasks, 64% on Prep Tape and
  20% on Thread Velcro, with four cameras at 50 Hz [2]. They say nothing about a 5-DOF arm with
  one camera; measure your own success rate over fixed trials.
- **The original repo is frozen.** 26 issues are open, including a Mujoco 3 request and a
  decoder bug report from December 2025 [4]. Its HDF5 layout (`/observations/qpos`,
  `/observations/images/<cam>`, `/action` per episode) differs from LeRobotDataset; convert or
  use LeRobot's `lerobot/aloha_sim_*` copies (the transfer-cube card says MIT) [1][12].

## Alternatives

[Diffusion Policy](diffusion-policy.md), [3D Diffusion Policy](3d-diffusion-policy.md),
[SmolVLA](../models/smolvla.md), [pi0](../models/pi0.md). ManiSkill keeps maintained ACT and
Diffusion Policy baselines for its simulator [11]; see [ManiSkill](../frameworks/maniskill.md).
Skill: [skills/learn-robot-learning/SKILL.md](../../../skills/learn-robot-learning/SKILL.md).

## Sources

1. [ACT repository: README, LICENSE, conda_env.yaml, imitate_episodes.py, constants.py, utils.py, history](https://github.com/tonyzhaozh/act), accessed 2026-11-25
2. [Zhao, Kumar, Levine, Finn: Learning Fine-Grained Bimanual Manipulation with Low-Cost Hardware (arXiv 2304.13705, read in the ar5iv HTML render)](https://arxiv.org/abs/2304.13705), accessed 2026-11-25
3. [ACT tuning tips (Google Doc linked from the ACT README)](https://docs.google.com/document/d/1FVIZfoALXg_ZkYKaYVh-qOlaXveq5CtvJHXkY25eYhs/edit), accessed 2026-11-25
4. [ACT repository issues](https://github.com/tonyzhaozh/act/issues), accessed 2026-11-25
5. [act-plus-plus (Mobile ALOHA) repository: README, LICENSE, history](https://github.com/MarkFzp/act-plus-plus), accessed 2026-11-25
6. [LeRobot docs: ACT (Action Chunking with Transformers)](https://huggingface.co/docs/lerobot/act), accessed 2026-11-25
7. [LeRobot source: policies/act (configuration_act.py, modeling_act.py), configs (train.py, dataset.py), robots/so_follower config](https://github.com/huggingface/lerobot/tree/main/src/lerobot), accessed 2026-11-25
8. [LeRobot docs: Compute Hardware Guide](https://huggingface.co/docs/lerobot/hardware_guide), accessed 2026-11-25
9. [LeRobot docs: Imitation Learning on Real-World Robots](https://huggingface.co/docs/lerobot/il_robots), accessed 2026-11-25
10. [LeRobot docs: Remote Inference](https://huggingface.co/docs/lerobot/remote_inference), accessed 2026-11-25
11. [ManiSkill repository: examples/baselines (act, diffusion_policy)](https://github.com/haosulab/ManiSkill), accessed 2026-11-25
12. [Hugging Face dataset card: lerobot/aloha_sim_transfer_cube_human (licence field)](https://huggingface.co/datasets/lerobot/aloha_sim_transfer_cube_human), accessed 2026-11-25

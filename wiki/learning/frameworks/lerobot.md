---
type: tool
name: LeRobot
summary: Hugging Face's PyTorch library for learning on real robots - drivers and teleoperation from the SO-101 and Koch arms to the Unitree G1, the LeRobotDataset v3.0 format on the Hub, and about 30 policies from ACT and Diffusion Policy to pi0.5, SmolVLA and GR00T, trained and deployed with the lerobot-* commands; Apache-2.0 code, weights and datasets under their own licences.
tags: [lerobot, hugging-face, imitation-learning, teleoperation, lerobotdataset, act, diffusion-policy, smolvla, pi0, pi05, groot, vla, so-101, koch, lekiwi, unitree-g1, remote-inference, rtc, hil-serl, libero, metaworld, pytorch]
kind: framework
area: learning
support:
license: Apache-2.0
links: {repo: "https://github.com/huggingface/lerobot", docs: "https://huggingface.co/docs/lerobot/index", site: "https://huggingface.co/lerobot"}
version: {tested: , latest: 0.7.0, as_of: 2026-11-25}
platforms: [linux, macos, windows]
agent_access: cli
registry:
evidence: researched
last_verified: 2026-11-25
sources:
  - {url: "https://github.com/huggingface/lerobot", title: "LeRobot repository: README, LICENSE, pyproject.toml, docs/source (cheat sheet, ACT, SmolVLA, GR00T, pi0 pages), docker/README, source tree at v0.7.0 and main, history, issues", accessed: 2026-11-25}
  - {url: "https://pypi.org/project/lerobot/", title: "PyPI: lerobot release history", accessed: 2026-11-25}
  - {url: "https://huggingface.co/docs/lerobot/installation", title: "LeRobot docs: Installation", accessed: 2026-11-25}
  - {url: "https://huggingface.co/docs/lerobot/il_robots", title: "LeRobot docs: Imitation Learning on Real-World Robots", accessed: 2026-11-25}
  - {url: "https://huggingface.co/docs/lerobot/lerobot-dataset-v3", title: "LeRobot docs: LeRobotDataset v3.0", accessed: 2026-11-25}
  - {url: "https://huggingface.co/docs/lerobot/hardware_guide", title: "LeRobot docs: Compute Hardware Guide", accessed: 2026-11-25}
  - {url: "https://huggingface.co/docs/lerobot/inference", title: "LeRobot docs: Policy Deployment (lerobot-rollout)", accessed: 2026-11-25}
  - {url: "https://huggingface.co/docs/lerobot/remote_inference", title: "LeRobot docs: Remote Inference", accessed: 2026-11-25}
  - {url: "https://huggingface.co/docs/lerobot/backwardcomp", title: "LeRobot docs: Backward compatibility (PR #777 calibration, PR #1452 normalisation)", accessed: 2026-11-25}
  - {url: "https://huggingface.co/docs/lerobot/main/third_party_robots", title: "LeRobot docs: Third-Party Robots & Teleoperators, including ROS 2 bridges", accessed: 2026-11-25}
  - {url: "https://huggingface.co/docs/lerobot/pi05", title: "LeRobot docs: pi0.5 (Pi05), with the gated PaliGemma tokenizer note", accessed: 2026-11-25}
  - {url: "https://huggingface.co/lerobot/pi05_base", title: "Hugging Face cards: lerobot/pi05_base, lerobot/pi0_base, lerobot/smolvla_base, nvidia/GR00T-N1.7-3B, lerobot/svla_so101_pickplace (licence fields)", accessed: 2026-11-25}
  - {url: "https://github.com/iblnkn/rosetta", title: "Rosetta repository: README status, LICENSE, pixi.toml", accessed: 2026-11-25}
  - {url: "https://github.com/ngres/leros2", title: "leros2 repository: README, LICENSE, pyproject.toml", accessed: 2026-11-25}
---

# LeRobot

Hugging Face's PyTorch library for learning on real robots. It drives the arm and cameras,
records teleoperated demonstrations as a LeRobotDataset on the Hugging Face Hub, trains a policy
and runs it back on the robot, all through `lerobot-*` commands [1]. Builders with a low-cost arm
use it as their whole imitation-learning stack. **Code: Apache-2.0** [1]; pretrained weights and
Hub datasets carry their own licences (see Traps). **Latest release 0.7.0 (2026-11-05)**, after
0.6.0 (July) and 0.6.1 (August); releases come every one to three months [2]. Very active: 112
commits in the month to 2026-11-24, 302 open issues and 726 open pull requests [1].

## When to use it

- **Use it** with a supported robot to teleoperate, record, train and deploy. Built in for 0.7.0
  [1]: SO-100 and [SO-101](../../robots/so-101.md) (`so101_follower`, the flagship arm),
  [Koch v1.1](../../robots/koch-v1-1.md) (`koch_follower`), LeKiwi (a wheeled base with an SO
  arm), HopeJR, [Reachy 2](../../robots/reachy.md), [Unitree G1](../../robots/unitree-g1.md), OMX,
  OpenArm, reBot B601, I2RT YAM, EarthRover Mini Plus; most arms have bimanual types.
- Teleoperation: leader arms, keyboard, gamepad, phone, HopeJR glove [1]. Plugins (packages named
  `lerobot_robot_*`, `lerobot_teleoperator_*`, `lerobot_camera_*`) add xArm, UR5e, Franka, AgileX
  Piper, WidowX, GELLO, SpaceMouse and Meta Quest [1][10].
- **Use something else** for massively parallel RL in simulation ([Isaac Lab](isaac-lab.md),
  [ManiSkill](maniskill.md)), for classic offline IL benchmarks ([robomimic](robomimic.md),
  [robosuite](robosuite.md)), or for point-cloud policies such as
  [DP3](../policies/3d-diffusion-policy.md), which LeRobot does not ship. To pick a policy, see
  [Choose a robot learning policy](../../guides/choose-a-robot-learning-policy.md).

## Setup

```bash
conda create -y -n lerobot python=3.12 && conda activate lerobot
conda install ffmpeg -c conda-forge                       # video decoding through TorchCodec
pip install 'lerobot[core_scripts,training,feetech]'      # record and train with an SO-101
```

Python 3.12+ [2][3]. Other extras: `dynamixel`, `pi`, `smolvla`, `diffusion`, and the simulators
`aloha`, `pusht`, `libero` (Linux only), `metaworld` [3]. Linux PyTorch wheels are CUDA 13 builds
needing driver 580.65+; older drivers take torch (at most 2.14) from the `cu126` index first [3].
macOS 14+ (MPS 15+) and Windows work [3]. Docker: `huggingface/lerobot-gpu`, nightly [1].
**Jetson:** a community `docker/Dockerfile.jetson` builds torch for Orin on JetPack 6.2, taking
hours the first time; video decodes on the CPU [1][3].

**GPU for training**, from the hardware guide (batch 8, AdamW; indicative only) [6]:

| Policies | Peak VRAM | Example: 5 epochs over about 50 episodes at 640 x 480 |
|---|---|---|
| ACT, VQ-BeT, TD-MPC | about 2 to 6 GB | ACT: 30 to 60 min on an RTX 4090 or 3090; 6 to 14 h on an M-series Max |
| Diffusion, Multitask DiT | about 8 to 14 GB | Diffusion: 2 to 4 h on an RTX 4090 |
| SmolVLA | about 10 to 16 GB | 3 to 6 h on an L4 or A10G (batch 4) |
| pi0, pi0-FAST, pi0.5, X-VLA, WALL-X | about 24 to 40 GB | pi0 or pi0.5: 4 to 8 h on an A100 40 GB (batch 4) |
| GR00T, EO-1 | about 24 to 40 GB | none given |

No CPU training: rent a GPU or add `--job.target=a10g-small` for Hugging Face Jobs [6]. No
inference memory figures per policy; check that the device keeps up with the control rate [7].

## How an agent works with it

**Record, train, deploy** on an SO-101 (flags from [1][4]; ports from `lerobot-find-port`):

```bash
lerobot-calibrate --robot.type=so101_follower --robot.port=/dev/ttyACM0 --robot.id=follower
CAMS="{ top: {type: opencv, index_or_path: 1, width: 640, height: 480, fps: 30},
        wrist: {type: opencv, index_or_path: 0, width: 640, height: 480, fps: 30} }"
lerobot-record --robot.type=so101_follower --robot.port=/dev/ttyACM0 --robot.id=follower \
  --robot.cameras="$CAMS" --teleop.type=so101_leader --teleop.port=/dev/ttyACM1 \
  --teleop.id=leader --dataset.repo_id=$HF_USER/pick_cube --dataset.num_episodes=50 \
  --dataset.single_task="Put the cube in the bowl"
lerobot-train --dataset.repo_id=$HF_USER/pick_cube_YYYYMMDD_HHMMSS --policy.type=act \
  --policy.device=cuda --policy.repo_id=$HF_USER/act_pick_cube --steps=20000
lerobot-rollout --strategy.type=base --policy.path=$HF_USER/act_pick_cube \
  --robot.type=so101_follower --robot.port=/dev/ttyACM0 --robot.id=follower \
  --robot.cameras="$CAMS" --task="Put the cube in the bowl" --duration=60
```

- **Data: LeRobotDataset v3.0**, the format since lerobot 0.4.0 [5]: state, action and
  timestamps in Parquet shards, each camera in MP4 shards; `meta/info.json` (features, fps, path
  templates), `meta/stats.json` (normalisation statistics), `meta/tasks.parquet` (language tasks)
  and `meta/episodes/`. Camera names become `observation.images.<name>` [4][5].
  `LeRobotDataset("<repo_id>")` decodes video on access; `StreamingLeRobotDataset` streams [5].
- **Policies in 0.7.0** [1]: imitation learning with [ACT](../policies/act.md) (the docs' first
  pick), [Diffusion Policy](../policies/diffusion-policy.md), VQ-BeT and Multitask DiT; RL with
  HIL-SERL and TD-MPC; VLAs including [pi0](../models/pi0.md), pi0-FAST, pi0.5,
  [SmolVLA](../models/smolvla.md), [GR00T](../models/gr00t.md) N1.7, X-VLA, EO-1, MolmoAct2,
  WALL-OSS and six more; seven world-model policies; three reward models. `--policy.type` trains
  from scratch; `--policy.path` fine-tunes a checkpoint [1].
- **Evaluate** in simulation with `lerobot-eval --policy.path=lerobot/pi0_libero_finetuned
  --env.type=libero --env.task=libero_object --eval.n_episodes=10` (a success rate); environments
  include [LIBERO](../benchmarks/libero.md), Meta-World, RoboTwin 2.0, RoboCasa365 [1]. Loss goes
  to Trackio (`--trackio.enable=true`) [3]. `lerobot-rollout` strategies: `base`, `sentry`
  (records, uploads), `highlight`, `dagger` (human corrections), `episodic` [7].
- **Async and remote inference.** `--inference.type=rtc` (Real-Time Chunking) computes the next
  chunk in a background thread for pi0, pi0.5 and SmolVLA [7]. For a GPU on another machine, run
  `lerobot-policy-server --config_path=server.yaml` there and `lerobot-rollout
  --inference.type=remote --inference.endpoint=tcp/<ip>:7447` on the robot computer (Zenoh); the
  robot keeps executing buffered actions while the server predicts. ACT, SmolVLA, X-VLA, EVO1 and
  LaWAM have run on real robots this way [8].
- **ROS 2: no bridge in LeRobot itself.** Community plugins [10]: leros2 (Apache-2.0; Jazzy via
  RoboStack; pins `lerobot>=0.6.0,<0.7.0`) [14], Rosetta (Apache-2.0; tested only on Lyrical;
  needs `lerobot<0.6.2` for the removed async inference) [13], and ROBOTIS'
  `lerobot_robot_ros2_zenoh`. Neither pinned plugin accepts 0.7.0 yet [13][14].

## Traps

- **Camera names and sizes are part of the policy.** Reuse the same `--robot.cameras` at
  rollout, or map names with `--rename_map` [4]. ACT needs every camera at the same shape [1].
- **The dataset's frame rate can lie.** Timestamps come from the frame index, so a loop that ran
  at 25 Hz still claims 30 Hz and replays too fast. Read the cadence report `lerobot-record`
  prints; drop resolution or a camera if ticks run over [4].
- **Calibration belongs to `--robot.id`;** use the same id everywhere [1]. Since PR #777 joints
  are normalised to -100 to 100 (gripper 0 to 100), so older datasets replay wrongly [9].
- **Old checkpoints, datasets and guides.** Checkpoints from before PR #1452 hold normalisation in
  the weights; run `migrate_policy_normalization.py` [9]. Convert v2.1 datasets with `python -m
  lerobot.scripts.convert_dataset_v21_to_v30 --repo-id=<id>` [5]. Guides for 0.5.x and older
  deploy with `lerobot-record` [1]; `lerobot.async_inference` is gone [8]. Pin the version.
- **Stamped names, too many steps.** `lerobot-record` appends `_YYYYMMDD_HHMMSS` to the repo id
  and pushes to the Hub unless `--dataset.push_to_hub=false` [4]. Training defaults to 100,000
  steps, but 5 to 10 epochs usually suffice; cut `--policy.scheduler_decay_steps` too [4][6].
- **Weights licences differ from the code.** Hub cards tag `lerobot/pi0_base` and
  `lerobot/pi05_base` as `gemma`, though LeRobot's docs say Apache-2.0; pi0, pi0.5 and pi0-FAST
  load the gated `google/paligemma-3b-pt-224` tokenizer (accept, then log in) [1][11][12].
  GR00T N1.7: NVIDIA Open Model License; SmolVLA base: Apache-2.0 [1][12]. Each Hub dataset has
  its own licence tag [12].
- **Remote code and public logs.** PI0-FAST, FineART and WALL-X tokenizers run custom code; review
  it before `trust_remote_code: true` [8]. Trackio runs synced to a Space are public unless
  `--trackio.private=true`, console output included [3].

## Alternatives

[Isaac Lab](isaac-lab.md), [ManiSkill](maniskill.md), [robomimic](robomimic.md),
[robosuite](robosuite.md), [Stable-Baselines3](stable-baselines3.md); openpi for pi0 itself. Skill:
[skills/learn-robot-learning/SKILL.md](../../../skills/learn-robot-learning/SKILL.md).

## Sources

1. [LeRobot repository: README, LICENSE, pyproject.toml, docs/source (cheat sheet, ACT, SmolVLA, GR00T, pi0 pages), docker/README, source tree at v0.7.0 and main, history, issues](https://github.com/huggingface/lerobot), accessed 2026-11-25
2. [PyPI: lerobot release history](https://pypi.org/project/lerobot/), accessed 2026-11-25
3. [LeRobot docs: Installation](https://huggingface.co/docs/lerobot/installation), accessed 2026-11-25
4. [LeRobot docs: Imitation Learning on Real-World Robots](https://huggingface.co/docs/lerobot/il_robots), accessed 2026-11-25
5. [LeRobot docs: LeRobotDataset v3.0](https://huggingface.co/docs/lerobot/lerobot-dataset-v3), accessed 2026-11-25
6. [LeRobot docs: Compute Hardware Guide](https://huggingface.co/docs/lerobot/hardware_guide), accessed 2026-11-25
7. [LeRobot docs: Policy Deployment (lerobot-rollout)](https://huggingface.co/docs/lerobot/inference), accessed 2026-11-25
8. [LeRobot docs: Remote Inference](https://huggingface.co/docs/lerobot/remote_inference), accessed 2026-11-25
9. [LeRobot docs: Backward compatibility (PR #777 calibration, PR #1452 normalisation)](https://huggingface.co/docs/lerobot/backwardcomp), accessed 2026-11-25
10. [LeRobot docs: Third-Party Robots & Teleoperators, including ROS 2 bridges](https://huggingface.co/docs/lerobot/main/third_party_robots), accessed 2026-11-25
11. [LeRobot docs: pi0.5 (Pi05), with the gated PaliGemma tokenizer note](https://huggingface.co/docs/lerobot/pi05), accessed 2026-11-25
12. [Hugging Face cards: lerobot/pi05_base, lerobot/pi0_base, lerobot/smolvla_base, nvidia/GR00T-N1.7-3B, lerobot/svla_so101_pickplace (licence fields)](https://huggingface.co/lerobot/pi05_base), accessed 2026-11-25
13. [Rosetta repository: README status, LICENSE, pixi.toml](https://github.com/iblnkn/rosetta), accessed 2026-11-25
14. [leros2 repository: README, LICENSE, pyproject.toml](https://github.com/ngres/leros2), accessed 2026-11-25

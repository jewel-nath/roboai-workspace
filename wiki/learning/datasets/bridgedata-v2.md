---
type: tool
name: BridgeData V2
summary: UC Berkeley's WidowX 250 dataset, 60,096 trajectories (50,365 teleoperated, 9,731 scripted) in 24 environments, mostly toy kitchens, 13 skills, language labels, 5 Hz; raw and RLDS copies under CC BY 4.0. Part of Open X-Embodiment and the source of SimplerEnv's WidowX scenes; the data has not changed since 2023.
tags: [bridgedata-v2, bridge, dataset, widowx, interbotix, toy-kitchen, teleoperation, rlds, language-conditioned, goal-conditioned, open-x-embodiment, simpler-env, octo]
kind: dataset
area: learning
support:
license: CC-BY-4.0
links: {repo: "https://github.com/rail-berkeley/bridge_data_v2", docs: , site: "https://rail-berkeley.github.io/bridgedata/"}
version: {tested: , latest: "1.0.0", as_of: 2026-11-25}
platforms: []
agent_access: script
registry:
evidence: researched
last_verified: 2026-11-25
sources:
  - {url: "https://rail-berkeley.github.io/bridgedata/", title: "BridgeData V2 project page: contents, cameras, control rate, licence", accessed: 2026-11-25}
  - {url: "https://github.com/rail-berkeley/bridge_data_v2", title: "bridge_data_v2 repository: README, LICENSE, commit history and issues", accessed: 2026-11-25}
  - {url: "https://rail.eecs.berkeley.edu/datasets/bridge_release/data/", title: "BridgeData release directory: raw archives, TFDS bridge_dataset 1.0.0 and its dataset_info.json", accessed: 2026-11-25}
  - {url: "https://www.tensorflow.org/datasets/catalog/bridge", title: "TensorFlow Datasets catalog: bridge (the Open X-Embodiment copy)", accessed: 2026-11-25}
  - {url: "https://github.com/rail-berkeley/bridge_data_robot", title: "bridge_data_robot repository: README, Dockerfile, LICENSE", accessed: 2026-11-25}
  - {url: "https://github.com/octo-models/octo/blob/main/octo/data/oxe/oxe_standardization_transforms.py", title: "Octo: OXE standardisation transforms (Bridge) and data utilities", accessed: 2026-11-25}
  - {url: "https://huggingface.co/datasets/IPEC-COMMUNITY/bridge_orig_lerobot", title: "Hugging Face IPEC-COMMUNITY/bridge_orig_lerobot: card and meta/info.json", accessed: 2026-11-25}
  - {url: "https://github.com/simpler-env/SimplerEnv", title: "SimplerEnv repository: README (WidowX Bridge tasks)", accessed: 2026-11-25}
---

# BridgeData V2

UC Berkeley RAIL's WidowX 250 data: 60,096 trajectories (50,365 VR-teleoperated, 9,731 scripted)
in 24 environments, mostly 7 toy kitchens, over 13 skills from pushing to cloth folding, each with
a language instruction [1]. Builders use it to pretrain or test WidowX-class policies; it is in
[Open X-Embodiment](open-x-embodiment.md). **Licences:** data CC BY 4.0 [1]; code MIT [2][5].
**Maintenance:** files from 2023 [3], last commit 2024-03-16, 31 open issues [2]; it is finished.

## When to use it

- **Use it** for a WidowX or similar small arm on table-top tasks with language or goal images:
  the repo trains goal- and language-conditioned BC, diffusion BC, IQL and contrastive RL, with
  checkpoints [2]. [SimplerEnv](../benchmarks/simpler-env.md)'s four WidowX tasks rebuild its
  scenes at 5 Hz [8].
- **Use something else** for a Franka in real rooms ([DROID](droid.md)) or many robots
  ([Open X-Embodiment](open-x-embodiment.md)); it has no [SO-101](../../robots/so-101.md) data.

## Setup

Cameras: a fixed over-the-shoulder RGB-D, two RGB moved every 50 trajectories, a wide-angle
wrist RGB, all 640 x 480; most data has only the fixed view. 5 Hz, 38 steps on average [1].

| Copy | Episodes | Size | Where |
|---|---|---|---|
| Raw JPEG, PNG, pkl | 50,365 + 9,731 | 411 + 30 GB | `demos_8_17.zip`, `scripted_6_18.zip` [1][3] |
| RLDS `bridge_dataset` 1.0.0, 256 x 256 | 53,192 train, 6,872 val | 132 GB | `data/tfds/bridge_dataset/` [3] |
| OXE `bridge` 0.1.0 | 25,460 train, 3,475 test | 387 GiB | `gs://gresearch/robotics/bridge` [4] |
| LeRobot v2.0, community | 53,192 | | `IPEC-COMMUNITY/bridge_orig_lerobot` [7] |

Fetch the RLDS copy with `wget -r -np` from the release directory [3]; reading needs no GPU.
Training: Python 3.10, JAX 0.4.13 on CUDA 11 or TPU, no GPU memory figure given; for RLDS the
README recommends Octo's loader [2]. Fields (OXE copy): `image_0` to `image_3`, 7-D `state` and
`action`, `language_instruction` [4]. The arm runs `bridge_data_robot` (Docker, ROS 1 Noetic,
Interbotix drivers, Meta Quest teleop); `experiments/eval.py` drives a checkpoint [2][5].

## Traps

- **OXE's copy is the older one** (25,460 training episodes [4]); Octo's loader uses Berkeley's
  newer copy [6]. Download `bridge_dataset` 1.0.0.
- **Process actions like the model did.** Octo binarises the gripper and relabels the movement
  numbers from consecutive states, dropping the last step [6].
- **Missing views.** Most episodes have only the fixed camera [1]; the OXE copy flags
  `has_image_0` to `has_image_3` and `has_language` per episode [4]. Pick keys from the flags.
- **Old hardware, ROS 1.** The WidowX 250 S reached end of life in 2025
  ([Interbotix X-Series](../../robots/interbotix-x-series-arms.md)); the controller is Noetic [5].
- **The LeRobot port is unofficial:** a community v2.0 conversion tagged Apache-2.0, unlike the
  CC BY 4.0 source [1][7]; LeRobot 0.4+ reads v3.0, so convert it first.

## Alternatives

[DROID](droid.md), [Open X-Embodiment](open-x-embodiment.md), [LeRobot](../frameworks/lerobot.md)
formats; pretrained on it: [Octo](../models/octo.md), [OpenVLA](../models/openvla.md).

## Sources

1. [BridgeData V2 project page: contents, cameras, control rate, licence](https://rail-berkeley.github.io/bridgedata/), accessed 2026-11-25
2. [bridge_data_v2 repository: README, LICENSE, commit history and issues](https://github.com/rail-berkeley/bridge_data_v2), accessed 2026-11-25
3. [BridgeData release directory: raw archives, TFDS bridge_dataset 1.0.0 and its dataset_info.json](https://rail.eecs.berkeley.edu/datasets/bridge_release/data/), accessed 2026-11-25
4. [TensorFlow Datasets catalog: bridge (the Open X-Embodiment copy)](https://www.tensorflow.org/datasets/catalog/bridge), accessed 2026-11-25
5. [bridge_data_robot repository: README, Dockerfile, LICENSE](https://github.com/rail-berkeley/bridge_data_robot), accessed 2026-11-25
6. [Octo: OXE standardisation transforms (Bridge) and data utilities](https://github.com/octo-models/octo/blob/main/octo/data/oxe/oxe_standardization_transforms.py), accessed 2026-11-25
7. [Hugging Face IPEC-COMMUNITY/bridge_orig_lerobot: card and meta/info.json](https://huggingface.co/datasets/IPEC-COMMUNITY/bridge_orig_lerobot), accessed 2026-11-25
8. [SimplerEnv repository: README (WidowX Bridge tasks)](https://github.com/simpler-env/SimplerEnv), accessed 2026-11-25

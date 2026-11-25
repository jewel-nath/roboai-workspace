---
type: tool
name: DROID
summary: Large in-the-wild Franka teleoperation dataset, 76k successful demonstrations (350 h) in 564 scenes and 52 buildings from 13 institutions, plus about 16k failures, three stereo cameras at 15 Hz; RLDS 1.0.1 (1.87 TB) and a LeRobot v3.0 copy; data CC BY 4.0. It trained openpi's DROID checkpoints and comes with a reproducible collection rig of about $46,000.
tags: [droid, dataset, franka, panda, fr3, robotiq, teleoperation, in-the-wild, rlds, lerobot, zed, stereo, imitation-learning, co-training, openpi, polymetis]
kind: dataset
area: learning
support:
license: CC-BY-4.0
links: {repo: "https://github.com/droid-dataset/droid", docs: "https://droid-dataset.github.io/droid/", site: "https://droid-dataset.github.io/"}
version: {tested: , latest: "1.0.1", as_of: 2026-11-25}
platforms: []
agent_access: script
registry:
evidence: researched
last_verified: 2026-11-25
sources:
  - {url: "https://droid-dataset.github.io/", title: "DROID home page: dataset summary, loading snippet and updates", accessed: 2026-11-25}
  - {url: "https://arxiv.org/abs/2403.12945", title: "DROID: A Large-Scale In-The-Wild Robot Manipulation Dataset (arXiv 2403.12945, v2)", accessed: 2026-11-25}
  - {url: "https://droid-dataset.github.io/droid/the-droid-dataset", title: "DROID docs: The DROID Dataset (downloads, RLDS schema, raw format)", accessed: 2026-11-25}
  - {url: "https://github.com/droid-dataset/droid", title: "DROID platform repository: README, docs sources, Dockerfiles, commit history and issues", accessed: 2026-11-25}
  - {url: "https://github.com/droid-dataset/droid/blob/main/docs/hardware-setup/shopping-list.md", title: "DROID docs: hardware shopping list (updated September 2025)", accessed: 2026-11-25}
  - {url: "https://github.com/droid-dataset/droid_policy_learning", title: "droid_policy_learning repository: README and LICENSE", accessed: 2026-11-25}
  - {url: "https://huggingface.co/KarlP/droid", title: "Hugging Face KarlP/droid: language annotations, camera calibrations and idle filter", accessed: 2026-11-25}
  - {url: "https://storage.googleapis.com/gresearch/robotics/droid/1.0.1/dataset_info.json", title: "Google Cloud Storage: DROID dataset_info.json for 1.0.0 and 1.0.1, and bucket listings", accessed: 2026-11-25}
  - {url: "https://huggingface.co/datasets/lerobot/droid_1.0.1", title: "Hugging Face lerobot/droid_1.0.1: card, meta/info.json and discussions", accessed: 2026-11-25}
  - {url: "https://huggingface.co/docs/lerobot/porting_datasets_v3", title: "LeRobot docs: porting large datasets to LeRobotDataset v3.0 (DROID)", accessed: 2026-11-25}
  - {url: "https://github.com/Physical-Intelligence/openpi", title: "openpi repository: README (DROID checkpoints, GPU requirements)", accessed: 2026-11-25}
  - {url: "https://github.com/Physical-Intelligence/openpi/blob/main/examples/droid/README_train.md", title: "openpi: training on the full DROID dataset", accessed: 2026-11-25}
  - {url: "https://arxiv.org/abs/2406.09246", title: "OpenVLA: An Open-Source Vision-Language-Action Model (arXiv 2406.09246)", accessed: 2026-11-25}
  - {url: "https://huggingface.co/datasets/lerobot/droid_100", title: "Hugging Face lerobot/droid_100: card and meta/info.json", accessed: 2026-11-25}
---

# DROID

DROID (Distributed Robot Interaction Dataset) is teleoperated Franka Panda data collected outside
the lab: 76k successful demonstrations, 350 hours, in 564 scenes and 52 buildings, by 50
collectors at 13 institutions over 12 months, on one platform built 18 times [2]. The release also
keeps about 16k episodes marked unsuccessful [2]. Builders use it to pretrain or co-train
manipulation policies, through openpi's DROID checkpoints [11], and as a recipe for a collection
rig. **Licences:** data CC BY 4.0 [2]; the Hugging Face annotations CC BY 4.0 [7]; the training
code MIT [6]; the platform repo has no licence file [4]. **Maintenance:** platform code last
changed 2024-10-01 and its docs 2025-09-15; 49 issues are open, the newest (2026-09-15) with no
reply; annotations were updated in December 2024 and April 2025 [4][6][7].

## When to use it

- **Pretraining or co-training** a policy for a 7-DoF arm with a parallel gripper that must cope
  with new rooms, objects and camera placements. The authors report co-training with DROID beat
  no co-training and OXE co-training by 22 points in distribution and 17 out of distribution, on
  their 6 tasks in 4 locations with a DROID Franka [2].
- **Zero-shot on a DROID-like rig** with openpi's checkpoints: pi0-FAST-DROID and pi0.5-DROID for
  inference, pi0-DROID for fine-tuning [11]. See [pi0](../models/pi0.md).
- **Use something else** for many embodiments ([Open X-Embodiment](open-x-embodiment.md), which
  lists DROID in its v1.1), a WidowX ([BridgeData V2](bridgedata-v2.md)) or a low-cost arm such
  as [SO-101](../../robots/so-101.md): record your own with [LeRobot](../frameworks/lerobot.md).
  DROID holds one robot type, a Franka with a Robotiq 2F-85 [2][5].

## Setup

| Copy | Episodes | Size | Where |
|---|---|---|---|
| RLDS 1.0.1 | 95,658 | 1.87 TB | `gs://gresearch/robotics/droid/1.0.1` [8] |
| RLDS 1.0.0 | 92,233 | 1.83 TB | `gs://gresearch/robotics/droid/1.0.0` [8] |
| RLDS sample | 100 | 2 GB | `gs://gresearch/robotics/droid_100` [3] |
| Raw (stereo HD MP4, SVO, HDF5) | | 8.7 TB; 5.6 TB without stereo and SVO | `gs://gresearch/robotics/droid_raw` [3] |
| LeRobot v3.0 | 95,658 | 415 GB | `lerobot/droid_1.0.1` [9] |

```bash
gsutil -m cp -r gs://gresearch/robotics/droid_100 ~/data/            # try the loader first
gsutil -m cp -r gs://gresearch/robotics/droid/1.0.1 ~/data/droid/    # then the full set
```

Reading needs no GPU. Porting the RLDS copy to LeRobot is CPU work: over 7 days on one machine
and about 400 GB of output, or a SLURM job over its 2,048 shards [10]. **Training compute:**
`droid_policy_learning` (a robomimic fork with diffusion policy) trained every paper policy on one
A100 [6]. openpi's full pi0.5 recipe takes about 2 days on 8 H100s (100k steps, batch 256) from
pi0, or 5 days from PaliGemma; its RLDS loader needs Python 3.11, and LoRA runs did not
perform well [12]. openpi's general table:
inference over 8 GB of GPU memory, LoRA fine-tuning over 22.5 GB, full over 70 GB [11]. OpenVLA
mixed DROID in at 10% but removed it for the last third of training, as its action-token
accuracy stayed low [13].

## How an agent works with it

**What was recorded** [2][3]: 15 Hz; three stereo cameras at 1280 x 720 (two exterior ZED 2 on
adjustable tripods, a ZED Mini on the wrist); joint positions and velocities, end-effector pose
and velocity, gripper; actions in joint and Cartesian space; depth, calibration and language.
Raw episodes hold a metadata JSON (building, collector), `trajectory.h5`, MP4s and SVO files.

**RLDS fields** [3]: left images `wrist_image_left`, `exterior_image_1_left` and
`exterior_image_2_left` at 180 x 320; state `joint_position` (7), `cartesian_position` (6),
`gripper_position` (1); `action_dict` with joint, Cartesian and gripper positions and velocities;
`language_instruction` plus two alternatives; `recording_folderpath` and `file_path` per episode.

```python
import tensorflow_datasets as tfds
b = tfds.builder_from_directory("gs://gresearch/robotics/droid_100/1.0.0")
for ep in b.as_dataset(split="train").take(1):
    for step in ep["steps"].take(3):
        print(step["language_instruction"], step["action_dict"]["joint_position"])
```

**LeRobot** (`lerobot` 0.4.0 or newer): `LeRobotDataset("lerobot/droid_1.0.1")` gives 27.6M
frames of AV1 video at 320 x 180 and 15 fps, with an 8-D `observation.state` and `action` (seven
joints and the gripper) plus the separate joint, Cartesian and gripper fields [9].

**Annotations** in `KarlP/droid` [7]: three instructions each for over 95% of the 75k successful
episodes; camera-to-base extrinsics for about 36k episodes, camera-to-camera poses and
intrinsics; and `keep_ranges_1_0_1.json`, which drops idle stretches. openpi's RLDS loader
applies the idle filter for you [12]. robomimic-style training: set `DATA_PATH`, the mix and its
weights in `droid_runs_language_conditioned_rlds.py`, then run the command it prints [6].

**Check** with the dataset visualiser [3], a falling loss on held-out episodes, and a run on a DROID
rig with `scripts/evaluation/evaluate_policy.py` from the platform repo, at low speed first [6].

## The platform

The shopping list's approximate total is **$46,000 (retail parts, updated about September
2025)**, up from $20,000: a Franka Panda or Franka Research 3 (now about $35,000 in the US), a
Robotiq 2F-85 (about $6,000), two ZED 2 and one ZED Mini cameras, a Meta Quest 2 for teleop, an
Intel NUC, a Linux laptop or tower (an NVIDIA GPU advised), a standing desk, a breadboard, a
ChArUco board and printed camera mounts [5]. **Software, not ROS** [4]: the NUC runs Polymetis
on Ubuntu 18.04 with a real-time kernel and libfranka 0.9.0 (Panda) or 0.10.0 (FR3); the laptop
runs a Docker image with CUDA 12.1, Ubuntu 22.04 and the ZED SDK 4.0. The Panda is end of life;
see [Franka Panda and FR3](../../robots/franka-panda.md).

## Traps

- **The docs' download takes both versions.** `gsutil -m cp -r gs://gresearch/robotics/droid`
  [3] copies `1.0.0` and `1.0.1`, 3.7 TB together [8]. Copy `droid/1.0.1` only.
- **Use 1.0.1.** It carries full language labels (about 75k episodes; 1.0.0 has 30k), and
  openpi's idle-filter indices fit only 1.0.1 [12].
- **Idle frames teach idling.** Many episodes start with a pause; trained on them, a policy sits
  at home. Keep non-idle runs of at least 16 frames, about 1 s [7][12].
- **Failures are in the data.** About 16k episodes are unsuccessful [2]. Raw episodes sit under
  `success/` or `failure/` folders [12], and `recording_folderpath` points to that folder [3].
- **Which action?** The top-level `action` is 7 numbers that the schema calls "[6x joint
  velocities, 1x gripper position]", which cannot cover seven joints [3]; take the field you
  want from `action_dict`. LeRobot's `action` is joint positions plus gripper [9].
  pi0.5-DROID used joint velocities; openpi now recommends joint positions [12].
- **Camera keys change between copies.** RLDS says `exterior_image_1_left`, `lerobot/droid_1.0.1`
  says `observation.images.exterior_1_left`, and `lerobot/droid_100` says
  `observation.images.exterior_image_1_left`, with a 7-D state and action [9][14]. Exterior
  cameras move between scenes [2], so "1" and "2" are not fixed views. RLDS has left images
  only; depth and stereo need the raw copy [3].
- **Noisy calibration.** The original extrinsics are noisy; better ones cover about 36k
  episodes [7].
- **The LeRobot copy has open bugs.** 70 parquet shards that `meta/episodes` does not reference
  add rows when you filter episodes, hitting a CUDA assert with `success_only=True` (open);
  `episode_index` does not follow the RLDS order; a merged fix re-encoded 16 corrupt videos [9].
- **Licence tags disagree.** `lerobot/droid_1.0.1` is tagged Apache-2.0 and `lerobot/droid_100`
  MIT [9][14]; the paper releases the data under CC BY 4.0 [2], so credit DROID. The platform
  repo has no licence, so reusing its code needs the authors' permission [4].
- **Hardware drift.** The NUC stack pins Ubuntu 18.04 and libfranka versions [4]; a newer FR3
  system image may need a newer libfranka, so check Franka's compatibility table first.

## Alternatives

[Open X-Embodiment](open-x-embodiment.md), [BridgeData V2](bridgedata-v2.md); models trained on
DROID: [pi0](../models/pi0.md); see [Choose a robot learning
policy](../../guides/choose-a-robot-learning-policy.md).

## Sources

1. [DROID home page: dataset summary, loading snippet and updates](https://droid-dataset.github.io/), accessed 2026-11-25
2. [DROID: A Large-Scale In-The-Wild Robot Manipulation Dataset (arXiv 2403.12945, v2)](https://arxiv.org/abs/2403.12945), accessed 2026-11-25
3. [DROID docs: The DROID Dataset (downloads, RLDS schema, raw format)](https://droid-dataset.github.io/droid/the-droid-dataset), accessed 2026-11-25
4. [DROID platform repository: README, docs sources, Dockerfiles, commit history and issues](https://github.com/droid-dataset/droid), accessed 2026-11-25
5. [DROID docs: hardware shopping list (updated September 2025)](https://github.com/droid-dataset/droid/blob/main/docs/hardware-setup/shopping-list.md), accessed 2026-11-25
6. [droid_policy_learning repository: README and LICENSE](https://github.com/droid-dataset/droid_policy_learning), accessed 2026-11-25
7. [Hugging Face KarlP/droid: language annotations, camera calibrations and idle filter](https://huggingface.co/KarlP/droid), accessed 2026-11-25
8. [Google Cloud Storage: DROID dataset_info.json for 1.0.0 and 1.0.1, and bucket listings](https://storage.googleapis.com/gresearch/robotics/droid/1.0.1/dataset_info.json), accessed 2026-11-25
9. [Hugging Face lerobot/droid_1.0.1: card, meta/info.json and discussions](https://huggingface.co/datasets/lerobot/droid_1.0.1), accessed 2026-11-25
10. [LeRobot docs: porting large datasets to LeRobotDataset v3.0 (DROID)](https://huggingface.co/docs/lerobot/porting_datasets_v3), accessed 2026-11-25
11. [openpi repository: README (DROID checkpoints, GPU requirements)](https://github.com/Physical-Intelligence/openpi), accessed 2026-11-25
12. [openpi: training on the full DROID dataset](https://github.com/Physical-Intelligence/openpi/blob/main/examples/droid/README_train.md), accessed 2026-11-25
13. [OpenVLA: An Open-Source Vision-Language-Action Model (arXiv 2406.09246)](https://arxiv.org/abs/2406.09246), accessed 2026-11-25
14. [Hugging Face lerobot/droid_100: card and meta/info.json](https://huggingface.co/datasets/lerobot/droid_100), accessed 2026-11-25

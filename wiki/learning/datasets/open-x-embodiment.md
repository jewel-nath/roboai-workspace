---
type: tool
name: Open X-Embodiment
summary: Google DeepMind's pooled robot-learning dataset, 60 lab datasets from 22 embodiments (72 listed today, 2.4M episodes, about 9 TB) in one RLDS format, released with the RT-X models; the pretraining mix behind Octo and OpenVLA. The collection is CC BY 4.0, but each dataset keeps its own lab's terms, and the repo only gets colab fixes.
tags: [open-x-embodiment, oxe, rt-x, rt-1-x, rt-2-x, dataset, rlds, tfds, cross-embodiment, pretraining, co-training, imitation-learning, lerobot, octo, openvla]
kind: dataset
area: learning
support:
license: CC-BY-4.0
links: {repo: "https://github.com/google-deepmind/open_x_embodiment", docs: "https://docs.google.com/spreadsheets/d/1rPBD77tk60AEIGZrGSODwyyzs5FgCU9Uz3h-3_t2A9g", site: "https://robotics-transformer-x.github.io/"}
version: {tested: , latest: "1.1", as_of: 2026-11-25}
platforms: []
agent_access: script
registry:
evidence: researched
last_verified: 2026-11-25
sources:
  - {url: "https://github.com/google-deepmind/open_x_embodiment", title: "open_x_embodiment repository: README, LICENSE, colabs, models, commit history and issues", accessed: 2026-11-25}
  - {url: "https://robotics-transformer-x.github.io/", title: "Open X-Embodiment project page: dataset and RT-X models", accessed: 2026-11-25}
  - {url: "https://arxiv.org/abs/2310.08864", title: "Open X-Embodiment: Robotic Learning Datasets and RT-X Models (arXiv 2310.08864, v9)", accessed: 2026-11-25}
  - {url: "https://docs.google.com/spreadsheets/d/1rPBD77tk60AEIGZrGSODwyyzs5FgCU9Uz3h-3_t2A9g", title: "Open X-Embodiment dataset spreadsheet: per-dataset robot, episodes, size, cameras, action space, control rate", accessed: 2026-11-25}
  - {url: "https://github.com/google-deepmind/open_x_embodiment/issues/104", title: "open_x_embodiment issue 104: only 27 of 55 datasets available", accessed: 2026-11-25}
  - {url: "https://storage.googleapis.com/storage/v1/b/gresearch/o?prefix=robotics/&delimiter=/", title: "Google Cloud Storage listings and dataset_info.json files: gs://gresearch/robotics and gs://gdm-robotics-open-x-embodiment", accessed: 2026-11-25}
  - {url: "https://huggingface.co/collections/lerobot/open-x-embodiment", title: "Hugging Face: LeRobot Open X-Embodiment collection", accessed: 2026-11-25}
  - {url: "https://huggingface.co/lerobot", title: "Hugging Face: lerobot dataset cards and meta/info.json files (licence tags, format version, cameras)", accessed: 2026-11-25}
  - {url: "https://huggingface.co/docs/lerobot/lerobot-dataset-v3", title: "LeRobot docs: LeRobotDataset v3.0", accessed: 2026-11-25}
  - {url: "https://github.com/kpertsch/rlds_dataset_mod", title: "rlds_dataset_mod repository: README and prepare_open_x.sh", accessed: 2026-11-25}
  - {url: "https://github.com/octo-models/octo", title: "Octo repository: README and OXE standardisation transforms", accessed: 2026-11-25}
  - {url: "https://github.com/openvla/openvla", title: "OpenVLA repository: README (data mixtures, fine-tuning on RLDS datasets)", accessed: 2026-11-25}
  - {url: "https://arxiv.org/abs/2406.09246", title: "OpenVLA: An Open-Source Vision-Language-Action Model (arXiv 2406.09246)", accessed: 2026-11-25}
  - {url: "https://github.com/SudeepDasari/RoboNet", title: "RoboNet repository: README data licence and LICENSE", accessed: 2026-11-25}
---

# Open X-Embodiment

Open X-Embodiment (OXE) pools other labs' robot demonstration datasets into one format, RLDS
episodes read with TensorFlow Datasets [1]. The 2023 paper pooled 60 datasets from 34 labs: over
1M real trajectories from 22 embodiments, single arms to bimanual robots and quadrupeds [3]. Its
spreadsheet now lists 72 datasets, 60 as v1.0 and 12 as v1.1 (DROID among them), with 2,419,193
episodes and 8,964.94 GB in total [4]. Builders use it to pretrain or co-train generalist
policies, or to fetch one lab's data in a standard shape. **Licences:** the repo puts software
under Apache-2.0 and "other materials" under CC BY 4.0 [1]; each dataset also carries its own
lab's terms (see Traps). **Maintenance:** the last commit (2025-11-05) merged colab fixes; 55
issues are open, the newest (2026-11-20, a missing shard) with no reply [1].

## When to use it

- **Pretraining or co-training** across robots. Most builders use it second-hand: Octo trained
  on 800k trajectories from 25 OXE datasets [10][11], OpenVLA on 970k [12][13]. Fine-tuning
  [Octo](../models/octo.md) or [OpenVLA](../models/openvla.md) on your own demonstrations is
  far cheaper: OpenVLA's full fine-tunes took 8 A100s for 5 to 15 hours per task [13].
- **One lab's data** in a common format, such as Language Table (xArm, 442,226 episodes) [4].
- **Choosing a subset.** The sheet's filter views select by robot, morphology, gripper, action
  space, RGB, depth and wrist cameras, language, collection method and control rate, then print
  the dataset list and BibTeX to paste into the colab [4].
- **Use something else** for one robot in many real scenes ([DROID](droid.md)), WidowX data
  ([BridgeData V2](bridgedata-v2.md): use Berkeley's copy, not OXE's), or a low-cost arm: no
  SO-100 or [SO-101](../../robots/so-101.md) data is listed; WidowX, xArm, Franka, UR5, Kuka,
  [Google Robot](../../robots/google-robot.md), Stretch and ViperX are [4]. Record your own with
  [LeRobot](../frameworks/lerobot.md).

## Setup

Reading needs no GPU. Disk is the cost: Kuka (QT-Opt) 778 GB, Language Table 399 GB, Bridge
387 GB, DROID 1,670 GB, many others under 10 GB [4]. Sizes and versions are in each
`dataset_info.json`; most datasets are `0.1.0`, `robo_net` is `1.0.0`, `language_table` is
`0.0.1` [1][6].

```bash
pip install tensorflow tensorflow-datasets      # plus the Google Cloud SDK for gsutil
gsutil ls gs://gresearch/robotics/taco_play/      # versions; the bucket holds other sets too
gsutil -m cp -r gs://gresearch/robotics/taco_play/0.1.0 ~/tensorflow_datasets/taco_play/
```

**LeRobot route.** The `lerobot` org hosts 56 ports, from 14-episode NYU ROT to
`droid_1.0.1` [7]. Those checked are LeRobotDataset v3.0, which needs `lerobot` 0.4.0 or newer
[8][9]; each keeps its source's frame rate (5 Hz UR5, 15 Hz TACO Play, 30 Hz TOTO) [8].

```python
from lerobot.datasets import LeRobotDataset
ds = LeRobotDataset("lerobot/taco_play")      # streams: StreamingLeRobotDataset(...)
```

## How an agent works with it

**Episode shape.** Each episode holds `steps`; each step has `observation`, `action`,
`is_first`, `is_last`, `is_terminal`, `reward`, `discount` and usually a language instruction
[1]. Everything inside differs per dataset: Bridge has four 256 x 256 images `image_0` to
`image_3` and a 7-D state [4]; RT-1 data (`fractal20220817_data`) splits its action into
`world_vector`, `rotation_delta` and `gripper_closedness_action` [1]. Print one step first:

```python
import tensorflow_datasets as tfds
b = tfds.builder_from_directory("gs://gresearch/robotics/fractal20220817_data/0.1.0")
ep = next(iter(b.as_dataset(split="train[:1]")))
for k, v in next(iter(ep["steps"])).items():
    print(k, v)                     # keys, shapes and dtypes of this dataset only
```

**Mixing datasets.** Reuse a maintained loader with per-dataset configs (image keys, state,
action encoding) and standardisation transforms: Octo's `oxe_magic_soup` mix [11] or OpenVLA's
`prismatic/vla/datasets/rlds/oxe` (mixtures, configs, transforms) [12]. To add your robot,
convert it to RLDS with `kpertsch/rlds_dataset_builder` and register a config, a transform and a
mixture [12]. `prepare_open_x.sh` downloads Octo's 25 datasets one at a time and re-encodes images
to 256 x 256 JPEG to save disk [10].

**Compute** belongs to the model: OpenVLA's final run took 64 A100s for 14 days [13]; Octo-S
pretrained in 8 hours and Octo-B in 14 on a TPU v4-128 pod [11]. **Check** a pipeline before a
long run: plot a few episodes per dataset and compare per-dimension action statistics across the
mix. Score the policy in [SimplerEnv](../benchmarks/simpler-env.md) (Google Robot and WidowX
scenes) or on your robot with torque limits.

**RT-X models** [1][3]. RT-1-X is RT-1 (35M parameters, see [RT-1](../models/rt-1.md)) trained on
a mix from 9 manipulators: RT-1, QT-Opt, Bridge, Task Agnostic Robot Play, Jaco Play, Cable
Routing, RoboTurk, NYU VINN, Austin VIOLA, Berkeley Autolab UR5, TOTO and Language Table. It
takes one workspace RGB image and a task string at about 3 Hz, no wrist or depth camera, and
outputs x, y, z, roll, pitch, yaw and gripper. Checkpoints sit in
`gs://gdm-robotics-open-x-embodiment/open_x_embodiment_and_rt_x_oss/`: a TensorFlow zip (775 MB,
2023-10-10) and a JAX checkpoint (2024-02-15) that `models/rt1_inference_example.py` loads
[1][6]. RT-2-X (55B) weights were not released; the README offers only RT-1-X [1][2]. The
authors report RT-1-X 50% above each lab's original method on small datasets, and RT-2-X three
times RT-2 on emergent skills; they also report RT-1-X underfitting the large Bridge and RT-1
sets [3]. See [RT-2](../models/rt-2.md).

## Traps

- **The README's bucket is half empty.** Its FAQ says to copy from
  `gs://gdm-robotics-open-x-embodiment/<name>`, but only 27 of 55 folders there hold data
  (issue 104, no maintainer reply) [5]. On 2026-11-25 `bridge` and `fractal20220817_data` had no
  `dataset_info.json` there, while `gs://gresearch/robotics/<name>/<version>` served both [6].
  Use the `gresearch` paths, as the colab and Octo's script do [1][10].
- **`tfds.load` fails.** "Dataset not found" is the README's FAQ; the colab warns that
  `tfds.load` hits a `RecursionError` on Python 3.11 and works on 3.10 [1]. Load by path with
  `tfds.builder_from_directory`, as above.
- **Gripper conventions differ.** Octo's transforms invert the gripper action for 15 datasets,
  turn relative gripper commands into absolute ones, and binarise others [11]. Action spaces
  (end-effector position, delta or velocity, joints) and control rates (1 Hz RoboNet, 3 Hz
  RT-1, 5 Hz Bridge, 66.6 Hz ETH Agent Affordances) differ too [4]. Use per-dataset
  normalisation; OpenVLA un-normalises with a per-dataset `unnorm_key` [12].
- **Some images are BGR.** Octo's script flips colour channels for Stanford HYDRA, Austin Mutex
  and Berkeley Fanuc, and the wrist camera of Berkeley Autolab UR5 [10]. Unflipped, red objects
  turn blue.
- **OXE's `bridge` is old.** It is 25,460 training episodes [6]; Octo and OpenVLA train on
  Berkeley's newer `bridge_dataset` instead [11][12]. See [BridgeData V2](bridgedata-v2.md).
- **The sheet and the files disagree.** The sheet says 73,499 RT-1 episodes; the build's
  training split has 87,212 [4][6]. ALOHA, QUT Dynamic Grasping and MPI Muscular Proprioception
  are listed with no dataset name to download [4]; LeRobot hosts ALOHA separately [7]. Open
  issues report a missing shard (`agent_aware_affordances`) and missing camera images
  (`berkeley_rpt`) [1]. Count episodes from `dataset_info.json`.
- **Licences are per dataset.** The sheet has no licence column, and the README asks you to cite
  each dataset [1][4]. RoboNet's data is CC BY 4.0 while its code is MIT [14]. LeRobot's ports
  are tagged MIT (TOTO, Austin Mutex), Apache-2.0 (RoboTurk, `droid_1.0.1`) or CC BY 4.0
  (TACO Play, Jaco Play) [8]; DROID's own paper says CC BY 4.0 (see [DROID](droid.md)). Check
  each source before commercial use.
- **No common camera.** Datasets have 0 to 6 RGB cameras, some with a wrist view [4]; a policy
  that needs a wrist camera can use only those.

## Alternatives

[DROID](droid.md), [BridgeData V2](bridgedata-v2.md); simulated demonstrations in
[LIBERO](../benchmarks/libero.md) and [RoboCasa](../benchmarks/robocasa.md); data recorded with
[LeRobot](../frameworks/lerobot.md); RoboNet (2019) is inside OXE as `robo_net` [4]. See
[Choose a robot learning policy](../../guides/choose-a-robot-learning-policy.md).

## Sources

1. [open_x_embodiment repository: README, LICENSE, colabs, models, commit history and issues](https://github.com/google-deepmind/open_x_embodiment), accessed 2026-11-25
2. [Open X-Embodiment project page: dataset and RT-X models](https://robotics-transformer-x.github.io/), accessed 2026-11-25
3. [Open X-Embodiment: Robotic Learning Datasets and RT-X Models (arXiv 2310.08864, v9)](https://arxiv.org/abs/2310.08864), accessed 2026-11-25
4. [Open X-Embodiment dataset spreadsheet: per-dataset robot, episodes, size, cameras, action space, control rate](https://docs.google.com/spreadsheets/d/1rPBD77tk60AEIGZrGSODwyyzs5FgCU9Uz3h-3_t2A9g), accessed 2026-11-25
5. [open_x_embodiment issue 104: only 27 of 55 datasets available](https://github.com/google-deepmind/open_x_embodiment/issues/104), accessed 2026-11-25
6. [Google Cloud Storage listings and dataset_info.json files: gs://gresearch/robotics and gs://gdm-robotics-open-x-embodiment](https://storage.googleapis.com/storage/v1/b/gresearch/o?prefix=robotics/&delimiter=/), accessed 2026-11-25
7. [Hugging Face: LeRobot Open X-Embodiment collection](https://huggingface.co/collections/lerobot/open-x-embodiment), accessed 2026-11-25
8. [Hugging Face: lerobot dataset cards and meta/info.json files (licence tags, format version, cameras)](https://huggingface.co/lerobot), accessed 2026-11-25
9. [LeRobot docs: LeRobotDataset v3.0](https://huggingface.co/docs/lerobot/lerobot-dataset-v3), accessed 2026-11-25
10. [rlds_dataset_mod repository: README and prepare_open_x.sh](https://github.com/kpertsch/rlds_dataset_mod), accessed 2026-11-25
11. [Octo repository: README and OXE standardisation transforms](https://github.com/octo-models/octo), accessed 2026-11-25
12. [OpenVLA repository: README (data mixtures, fine-tuning on RLDS datasets)](https://github.com/openvla/openvla), accessed 2026-11-25
13. [OpenVLA: An Open-Source Vision-Language-Action Model (arXiv 2406.09246)](https://arxiv.org/abs/2406.09246), accessed 2026-11-25
14. [RoboNet repository: README data licence and LICENSE](https://github.com/SudeepDasari/RoboNet), accessed 2026-11-25

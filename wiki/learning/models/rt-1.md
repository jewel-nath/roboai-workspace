---
type: tool
name: RT-1 (Robotics Transformer 1)
summary: Google's 2022 Robotics Transformer, a 35M-parameter TensorFlow policy trained on 130k demonstrations from the Everyday Robots fleet that set the large-scale imitation baseline; the Apache-2.0 repo is archived (last commit 2023-02-10), but RT-1 and RT-1-X checkpoints remain downloadable and serve as baselines in SimplerEnv. Use Octo, OpenVLA, pi0 or SmolVLA for new work.
tags: [rt-1, rt-1-x, robotics-transformer, google, deepmind, everyday-robots, imitation-learning, transformer, tensorflow, efficientnet, film, tokenlearner, open-x-embodiment, simplerenv, baseline, archived]
kind: model
area: learning
support:
license: Apache-2.0
links: {repo: "https://github.com/google-research/robotics_transformer", docs: , site: "https://robotics-transformer1.github.io/"}
version: {tested: , latest: RT-1-X, as_of: 2026-11-25}
platforms: []
agent_access: script
registry:
evidence: researched
last_verified: 2026-11-25
sources:
  - {url: "https://github.com/google-research/robotics_transformer", title: "robotics_transformer repository: README, LICENSE, requirements.txt, .gitattributes, archive banner, issues", accessed: 2026-11-25}
  - {url: "https://arxiv.org/abs/2212.06817", title: "Brohan et al., RT-1: Robotics Transformer for Real-World Control at Scale (arXiv, v2 2023-08-11)", accessed: 2026-11-25}
  - {url: "https://robotics-transformer1.github.io/", title: "RT-1 project page", accessed: 2026-11-25}
  - {url: "https://github.com/google-deepmind/open_x_embodiment", title: "Open X-Embodiment repository: README (RT-1-X checkpoints, licences), colabs, models/rt1.py", accessed: 2026-11-25}
  - {url: "https://github.com/simpler-env/SimplerEnv", title: "SimplerEnv repository: README (RT-1 and RT-1-X checkpoints, TensorFlow 2.15)", accessed: 2026-11-25}
  - {url: "https://www.tensorflow.org/datasets/catalog/fractal20220817_data", title: "TensorFlow Datasets: fractal20220817_data (the RT-1 dataset)", accessed: 2026-11-25}
  - {url: "https://github.com/huggingface/lerobot/tree/main/src/lerobot/policies", title: "LeRobot policies folder (no RT-1 policy)", accessed: 2026-11-25}
---

# RT-1 (Robotics Transformer 1)

**Unmaintained.** RT-1 is Google's 2022 Robotics Transformer: a 35M-parameter TensorFlow model
mapping six 300 x 300 frames and an instruction to discretised arm and base actions at 3 Hz [2].
Trained on about 130,000 demonstrations of 744 tasks from 13 Everyday Robots manipulators
([Google Robot](../../robots/google-robot.md)), it set the large-scale imitation baseline
[2][3]; RT-1-X retrained it on Open X-Embodiment [4]. Code Apache-2.0; repo archived 2025-04-07,
last commit 2023-02-10 [1]. Open X-Embodiment, which hosts the data, licenses non-software
materials CC-BY-4.0 [4][6]. **Use instead:** [Octo](octo.md), [OpenVLA](openvla.md),
[pi0](pi0.md), [SmolVLA](smolvla.md) [7].

## When to use it

- **As a baseline.** [SimplerEnv](../benchmarks/simpler-env.md) scores RT-1 Converged, RT-1 15%,
  RT-1 Begin and RT-1-X on simulated Google Robot and WidowX tasks [5].
- **To study the data:** `fractal20220817_data` in
  [Open X-Embodiment](../datasets/open-x-embodiment.md): 87,212 RLDS episodes, 111 GiB, 256 x 320
  images, a 512-value instruction embedding per step [6].
- **Not for your robot:** no maintained training code, no PyTorch or LeRobot port [1][7].

## Setup

The repo lists TensorFlow, `tf-agents`, `gin-config` and `tensor2robot` with no versions or OS
[1]. What works today is SimplerEnv's environment (`tensorflow[and-cuda]==2.15.1`) and the
bucket checkpoints [5]. No GPU memory figures from upstream.

```bash
B=gs://gdm-robotics-open-x-embodiment/open_x_embodiment_and_rt_x_oss
gsutil -m cp -r $B/rt_1_tf_trained_for_000400120 $B/rt_1_x_tf_trained_for_002272480_step.zip .
```

## How an agent works with it

- **RT-1** outputs 11 dimensions in 256 bins each: arm x, y, z, roll, pitch, yaw, gripper; base
  x, y, yaw; a mode switch [2].
- **RT-1-X** takes one workspace RGB image and the task string about every 333 ms and returns 7
  end-effector values; no wrist or depth camera [4]. The OXE colab overlays predicted on recorded
  actions; a JAX checkpoint loads with `models/rt1_inference_example.py` [4].

## Traps

- **Old TensorFlow stack.** Unpinned TF, `tf-agents` and `tensor2robot`; open issues report
  `tensorflow.contrib` errors and checkpoint loading failures; use SimplerEnv's pins [1][5].
- **Pointer files, not weights.** The repo's three SavedModels (`rt1main`, `rt1multirobot`,
  `rt1simreal`) are Git LFS objects; install `git-lfs` or use the bucket [1].
- **Missing text encoder.** New instructions need Universal Sentence Encoder embeddings (512
  values), which the repo does not ship; an open issue asks for it [1][2][6].
- **Action conventions.** RT-1-X values may be absolute, delta or velocity per source dataset; RT-1
  assumes the Everyday Robot's base and 3 Hz. Map units and rates to your robot first [2][4].
- **Results are Google's:** 97% seen, 76% unseen instructions, on their own robots and rooms [2][3].

## Alternatives

[RT-2](rt-2.md) (closed), [Octo](octo.md), [OpenVLA](openvla.md), [pi0](pi0.md), [GR00T](gr00t.md).

## Sources

1. [robotics_transformer repository: README, LICENSE, requirements.txt, .gitattributes, archive banner, issues](https://github.com/google-research/robotics_transformer), accessed 2026-11-25
2. [Brohan et al., RT-1: Robotics Transformer for Real-World Control at Scale (arXiv, v2 2023-08-11)](https://arxiv.org/abs/2212.06817), accessed 2026-11-25
3. [RT-1 project page](https://robotics-transformer1.github.io/), accessed 2026-11-25
4. [Open X-Embodiment repository: README (RT-1-X checkpoints, licences), colabs, models/rt1.py](https://github.com/google-deepmind/open_x_embodiment), accessed 2026-11-25
5. [SimplerEnv repository: README (RT-1 and RT-1-X checkpoints, TensorFlow 2.15)](https://github.com/simpler-env/SimplerEnv), accessed 2026-11-25
6. [TensorFlow Datasets: fractal20220817_data (the RT-1 dataset)](https://www.tensorflow.org/datasets/catalog/fractal20220817_data), accessed 2026-11-25
7. [LeRobot policies folder (no RT-1 policy)](https://github.com/huggingface/lerobot/tree/main/src/lerobot/policies), accessed 2026-11-25

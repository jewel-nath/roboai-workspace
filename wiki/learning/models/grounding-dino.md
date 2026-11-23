---
type: tool
name: Grounding DINO
summary: IDEA Research's open-vocabulary detector that returns boxes for whatever a text prompt names; the open release (Swin-T and Swin-B weights) is Apache-2.0 but idle since August 2024, Grounding DINO 1.5 and 1.6 are cloud-API only, and paired with SAM it turns a word into a mask (Grounded SAM).
tags: [grounding-dino, open-vocabulary, zero-shot-detection, text-prompt, grounded-sam, grounded-sam-2, sam, idea-research, transformers, isaac-ros, labelling]
kind: model
area: perception
support:
license: Apache-2.0
links: {repo: "https://github.com/IDEA-Research/GroundingDINO", docs: "https://github.com/IDEA-Research/GroundingDINO#readme", site: }
version: {tested: , latest: , as_of: 2026-11-23}
platforms: [linux]
agent_access: script
registry:
evidence: researched
last_verified: 2026-11-23
sources:
  - {url: "https://github.com/IDEA-Research/GroundingDINO", title: "GroundingDINO repository: README, LICENSE, setup.py, util/inference.py, config, tags", accessed: 2026-11-23}
  - {url: "https://github.com/IDEA-Research/Grounding-DINO-1.5-API", title: "Grounding DINO 1.5 API repository: README (1.5 Pro, 1.5 Edge, 1.6 Pro, API tokens)", accessed: 2026-11-23}
  - {url: "https://github.com/IDEA-Research/Grounded-SAM-2", title: "Grounded SAM 2 repository: README and LICENSE", accessed: 2026-11-23}
  - {url: "https://github.com/IDEA-Research/Grounded-Segment-Anything", title: "Grounded-Segment-Anything repository: README, LICENSE, history", accessed: 2026-11-23}
  - {url: "https://huggingface.co/IDEA-Research/grounding-dino-tiny", title: "Hugging Face model card: IDEA-Research/grounding-dino-tiny", accessed: 2026-11-23}
  - {url: "https://github.com/NVIDIA-ISAAC-ROS/isaac_ros_object_detection", title: "Isaac ROS Object Detection repository: packages and Grounding DINO model install script, release-4.6 and main", accessed: 2026-11-23}
  - {url: "https://catalog.ngc.nvidia.com/orgs/nvidia/teams/tao/models/grounding_dino", title: "NVIDIA NGC: TAO Grounding DINO model card", accessed: 2026-11-23}
  - {url: "https://nvidia-isaac-ros.github.io/v/release-4.6/getting_started/index.html", title: "Isaac ROS 4.6 getting started: ROS 2 Jazzy and platform requirements", accessed: 2026-11-23}
---

# Grounding DINO

An open-set detector from IDEA Research: given an image and a prompt such as `"mug . drill ."`,
it returns a box, score and phrase per match [1]; builders use it to find untrained objects,
label data and prompt [SAM](segment-anything.md) (Grounded SAM) [3]. Code and Swin-T/Swin-B
weights are Apache-2.0; last commit 2024-08-12, only `v0.1.0-alpha` pre-release tags, so `latest`
is empty [1]. **Grounding DINO 1.5 Pro, 1.5 Edge and 1.6 Pro** have no public weights: they run
only on DeepDataSpace's cloud API with a token, and extra calls are paid [2].

## When to use it

- Grasp "the blue box" without a trained detector, or bootstrap a labelled dataset. With masks:
  Grounded SAM 2 (Apache-2.0, last commit 2025-11-11) chains it with SAM 2 for images and video;
  the first Grounded-Segment-Anything stopped in September 2024 [3][4].
- Known classes at camera rate: train YOLO. Text to mask in one model: SAM 3 (SAM License).

## Setup

```bash
export CUDA_HOME=/usr/local/cuda     # if unset, the custom ops build for CPU only [1]
git clone https://github.com/IDEA-Research/GroundingDINO.git && cd GroundingDINO && pip install -e .
R=https://github.com/IDEA-Research/GroundingDINO/releases/download/v0.1.0-alpha
mkdir weights && wget -q -P weights $R/groundingdino_swint_ogc.pth
```

The `transformers` port needs no CUDA build: `IDEA-Research/grounding-dino-tiny` (Apache-2.0)
loads with `AutoModelForZeroShotObjectDetection` [5]. IDEA reports 48.4 COCO AP zero-shot for
Swin-T [1]; no repo gives a GPU memory figure.

## How an agent works with it

- `predict(model, image, caption, box_threshold=0.35, text_threshold=0.25)` keeps boxes (of 900
  queries) above `box_threshold` and words above `text_threshold` as labels [1]. Boxes are
  normalised centre x, y, width, height: convert to pixel `xyxy`, as `annotate` does [1].
- ROS 2: no rosdistro package. Isaac ROS `isaac_ros_grounding_dino` runs NVIDIA's Swin-T model,
  retrained on commercially licensed images, from NGC under the NVIDIA Open Model License [6][7].
  Isaac ROS 4.6 is for Jazzy and Ampere+ 8 GB GPUs [8]; see [FoundationPose](foundationpose.md).

## Traps

- **Prompt format.** Lower-case, each phrase ending in a period (`"a cat. a remote control."`)
  [5]; prompts stop at 256 tokens, and one word may be several tokens [1].
- **`NameError: name '_C' is not defined`:** the CUDA ops did not build, usually because
  `CUDA_HOME` was unset; re-clone and reinstall [1].
- **Unmaintained upstream.** No commit since 2024: pin PyTorch and `transformers` [1][5].
- **1.5 and 1.6 need the internet** and a token, so not for an offline robot; Grounded SAM 2
  moved to API V2 in April 2025 [2][3].
- **Other weights, other licence:** the NGC model is under NVIDIA's Open Model License [7].

## Alternatives

[YOLO](yolo.md), [SAM 3](segment-anything.md); Florence-2 and DINO-X (API) in Grounded SAM 2 [3].

## Sources

1. [GroundingDINO repository: README, LICENSE, setup.py, util/inference.py, config, tags](https://github.com/IDEA-Research/GroundingDINO), accessed 2026-11-23
2. [Grounding DINO 1.5 API repository: README (1.5 Pro, 1.5 Edge, 1.6 Pro, API tokens)](https://github.com/IDEA-Research/Grounding-DINO-1.5-API), accessed 2026-11-23
3. [Grounded SAM 2 repository: README and LICENSE](https://github.com/IDEA-Research/Grounded-SAM-2), accessed 2026-11-23
4. [Grounded-Segment-Anything repository: README, LICENSE, history](https://github.com/IDEA-Research/Grounded-Segment-Anything), accessed 2026-11-23
5. [Hugging Face model card: IDEA-Research/grounding-dino-tiny](https://huggingface.co/IDEA-Research/grounding-dino-tiny), accessed 2026-11-23
6. [Isaac ROS Object Detection repository: packages and Grounding DINO model install script, release-4.6 and main](https://github.com/NVIDIA-ISAAC-ROS/isaac_ros_object_detection), accessed 2026-11-23
7. [NVIDIA NGC: TAO Grounding DINO model card](https://catalog.ngc.nvidia.com/orgs/nvidia/teams/tao/models/grounding_dino), accessed 2026-11-23
8. [Isaac ROS 4.6 getting started: ROS 2 Jazzy and platform requirements](https://nvidia-isaac-ros.github.io/v/release-4.6/getting_started/index.html), accessed 2026-11-23

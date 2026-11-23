---
type: tool
name: Segment Anything (SAM, SAM 2, SAM 3)
summary: Meta's promptable segmentation models; SAM and SAM 2 (Apache-2.0 code and weights) turn a point or box into a mask and SAM 2 tracks it through video, while SAM 3 (Meta's own SAM License, gated weights) also returns every instance of a text concept; robot builders use the masks for grasping, pose estimation and labelling.
tags: [sam, sam2, sam3, segment-anything, segmentation, masks, video-tracking, open-vocabulary, meta, edgetam, mobilesam, isaac-ros, labelling]
kind: model
area: perception
support:
license: LicenseRef-SAM-License
links: {repo: "https://github.com/facebookresearch/sam3", docs: "https://github.com/facebookresearch/sam3#readme", site: "https://ai.meta.com/sam3"}
version: {tested: , latest: 0.1.4, as_of: 2026-11-23}
platforms: [linux]
agent_access: script
registry:
evidence: researched
last_verified: 2026-11-23
sources:
  - {url: "https://github.com/facebookresearch/segment-anything", title: "segment-anything (SAM) repository: README, LICENSE, history", accessed: 2026-11-23}
  - {url: "https://github.com/facebookresearch/sam2", title: "sam2 repository: README, LICENSE, image predictor, history", accessed: 2026-11-23}
  - {url: "https://github.com/facebookresearch/sam3", title: "sam3 repository: README, LICENSE (SAM License), RELEASE_SAM3p1.md, history", accessed: 2026-11-23}
  - {url: "https://arxiv.org/abs/2511.16719", title: "SAM 3: Segment Anything with Concepts (arXiv 2511.16719, v2)", accessed: 2026-11-23}
  - {url: "https://pypi.org/project/sam3/", title: "PyPI: sam3 release history", accessed: 2026-11-23}
  - {url: "https://github.com/NVIDIA-ISAAC-ROS/isaac_ros_image_segmentation", title: "Isaac ROS Image Segmentation repository: README and package list", accessed: 2026-11-23}
  - {url: "https://github.com/facebookresearch/EdgeTAM", title: "EdgeTAM repository: README and LICENSE", accessed: 2026-11-23}
  - {url: "https://github.com/ChaoningZhang/MobileSAM", title: "MobileSAM repository: README and LICENSE", accessed: 2026-11-23}
---

# Segment Anything

Meta's promptable segmentation models: SAM and SAM 2 turn a point, box or rough mask into a pixel
mask, SAM 2 carries it through video, and SAM 3 also returns every match for a short noun phrase
[1][2][3]: masks for grasping, labelling, and depth crops for [FoundationPose](foundationpose.md).

| Model | Checkpoints | Code and weights | Last commit |
|---|---|---|---|
| SAM | ViT-B, ViT-L, ViT-H | Apache-2.0 | 2024-09-18 [1] |
| SAM 2.1 | Hiera tiny, small, base+, large | Apache-2.0 | 2024-12-15 [2] |
| SAM 3, SAM 3.1 (2026-03-27) | gated on Hugging Face | Meta's SAM License | 2026-11-17 [3] |

## When to use it

- Click or box to mask, no training: SAM 2.1; its tiny model (38.9 M parameters) ran at 91 FPS
  on an A100 [2]. Masks through video: SAM 2's video predictor.
- Objects by name: SAM 3, or [Grounding DINO](grounding-dino.md) plus SAM 2 for Apache-2.0 only.
  Fixed classes at camera rate on a small computer: a [YOLO](yolo.md) segmentation model.

## Setup

```bash
git clone https://github.com/facebookresearch/sam2.git && cd sam2 && pip install -e .
cd checkpoints && ./download_ckpts.sh && cd ..     # SAM 2: Python 3.10+, PyTorch 2.5.1+
```

SAM 2 on Windows: use WSL [2]. SAM 3 installs from a clone and needs Python 3.12+, PyTorch 2.7+
and a CUDA 12.6+ GPU [3]; PyPI `sam3` 0.1.4 is from 2026-05-26 [5]. About 850 M parameters, 30 ms
per image with 100+ objects on an H200 [4]; no repo gives GPU memory figures.

## How an agent works with it

- SAM 2: `SAM2ImagePredictor.from_pretrained("facebook/sam2-hiera-large")`; `set_image(rgb)`,
  then `predict(point_coords=, point_labels=, box=)` returns masks, scores and logits [2].
- SAM 3: `Sam3Processor(build_sam3_image_model())`, `set_image`, then
  `set_text_prompt(state=, prompt="red mug")` gives masks, boxes and scores [3].
- ROS 2: no rosdistro package; on NVIDIA GPUs, Isaac ROS `isaac_ros_segment_anything` (SAM or
  MobileSAM) and `isaac_ros_segment_anything2` (video) segment the object a prompt names [6].

## Traps

- **SAM 3's licence travels.** Royalty-free and commercial use allowed, but redistribution must
  carry it, it bars military, ITAR, nuclear and espionage uses, and Meta may change it [3].
- **Gated weights:** SAM 3 needs an accepted Hugging Face request and `hf auth login`; cache it [3].
- **The image encoder is the cost.** SAM's ONNX export covers only the mask decoder [1];
  `set_image` computes the embedding every `predict` reuses, so call it once per frame [2].
- **Video slows per object** in SAM 3; SAM 3.1 groups them, about 7x faster for 128 objects [3].
- **Wrappers add licences:** Ultralytics' SAM support is AGPL-3.0 code ([YOLO](yolo.md)).

## Alternatives

EdgeTAM (Apache-2.0, 16 FPS on an iPhone 15 Pro Max, by Meta) [7], MobileSAM (Apache-2.0) [8].

## Sources

1. [segment-anything (SAM) repository: README, LICENSE, history](https://github.com/facebookresearch/segment-anything), accessed 2026-11-23
2. [sam2 repository: README, LICENSE, image predictor, history](https://github.com/facebookresearch/sam2), accessed 2026-11-23
3. [sam3 repository: README, LICENSE (SAM License), RELEASE_SAM3p1.md, history](https://github.com/facebookresearch/sam3), accessed 2026-11-23
4. [SAM 3: Segment Anything with Concepts (arXiv 2511.16719, v2)](https://arxiv.org/abs/2511.16719), accessed 2026-11-23
5. [PyPI: sam3 release history](https://pypi.org/project/sam3/), accessed 2026-11-23
6. [Isaac ROS Image Segmentation repository: README and package list](https://github.com/NVIDIA-ISAAC-ROS/isaac_ros_image_segmentation), accessed 2026-11-23
7. [EdgeTAM repository: README and LICENSE](https://github.com/facebookresearch/EdgeTAM), accessed 2026-11-23
8. [MobileSAM repository: README and LICENSE](https://github.com/ChaoningZhang/MobileSAM), accessed 2026-11-23

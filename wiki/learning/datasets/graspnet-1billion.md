---
type: tool
name: GraspNet-1Billion
summary: SJTU's benchmark for 6-DoF parallel-jaw grasping in clutter, 190 scenes and 97,280 RGB-D images from a RealSense D435 and an Azure Kinect with over 1.1 billion grasp labels, scored by the graspnetAPI toolkit; data, labels and baseline are for non-commercial use only.
tags: [graspnet-1billion, graspnet, dataset, benchmark, grasping, 6-dof-grasp, rgbd, realsense, azure-kinect, graspnetapi, force-closure, non-commercial]
kind: dataset
area: manip
support:
license: CC-BY-NC-SA-4.0
links: {repo: "https://github.com/graspnet/graspnetAPI", docs: "https://graspnetapi.readthedocs.io/en/latest/", site: "https://graspnet.net/"}
version: {tested: , latest: , as_of: 2026-11-25}
platforms: []
agent_access: script
registry:
evidence: researched
last_verified: 2026-11-25
sources:
  - {url: "https://graspnet.net/", title: "GraspNet home: GraspNet-1Billion overview, related datasets, news", accessed: 2026-11-25}
  - {url: "https://graspnet.net/datasets.html", title: "GraspNet: dataset downloads, sizes, object list and file layout", accessed: 2026-11-25}
  - {url: "https://graspnet.net/evaluation.html", title: "GraspNet: dataset split and evaluation metric", accessed: 2026-11-25}
  - {url: "https://graspnet.net/about", title: "GraspNet: about and licence", accessed: 2026-11-25}
  - {url: "https://github.com/graspnet/graspnetAPI", title: "graspnetAPI repository: README, LICENSE, setup.py history, evaluation code, docs source, bundled Dex-Net licence headers", accessed: 2026-11-25}
  - {url: "https://pypi.org/project/graspnetAPI/", title: "PyPI: graspnetAPI releases", accessed: 2026-11-25}
  - {url: "https://github.com/graspnet/graspnet-baseline", title: "graspnet-baseline repository: README, LICENSE, data loader, history", accessed: 2026-11-25}
  - {url: "https://github.com/graspnet/anygrasp_sdk", title: "AnyGrasp SDK repository: README and licence registration", accessed: 2026-11-25}
---

# GraspNet-1Billion

MVIG's (Shanghai Jiao Tong University) 6-DoF grasp benchmark: 190 cluttered tabletop scenes,
each seen from 256 views by a RealSense D435 and an Azure Kinect (97,280 RGB-D images), 88 objects
with 6D poses and masks, over 1.1 billion grasp labels [1][2]. Builders use it to score or train a
parallel-jaw grasp model on real sensor data. **Licence:** CC BY-NC 4.0 ("BY-NC-SA" in brackets)
for data, labels, code and models; commercial use needs the team's consent [4].

## When to use it

- **Use it** to compare a grasp detector, such as [Contact-GraspNet](../models/contact-graspnet.md),
  with published numbers on seen, similar and novel objects, or to test 6D pose estimation [3].
- **Use something else** for suction (SuctionNet-1Billion) or transparent objects (TransCG) [1].

## How an agent works with it

- **Splits** [3][5]: scenes 0 to 99 train; tests 100 to 129 seen, 130 to 159 similar, 160 to 189
  novel. Objects: YCB items, printed Dex-Net adversarial shapes and shop products, with links [2].
- **Files** [2]: per scene and camera, 256 RGB, depth and mask PNGs, 6D poses (XML and YCB-Video
  MAT), `camK.npy`, `camera_poses.npy`; depth scales by each frame's `factor_depth` [7]. Raw grasp
  labels (`NNN_labels.npz`) store the minimum friction coefficient; the API scores 1.1 minus it [5].
- **Download** [2] (Google Drive, Baidu, SJTU Jbox): train images 66.3 GB, test images 59 GB
  (`test_seen`, `test_similar`, `test_novel`), labels 2.3 GB, models 4.3 GB; optional `dex_models`
  8.9 GB and planar `rect_labels` 12.5 GB. Scoring reads the test archives and models [5].

Dump one `GraspGroup` per frame: each row is score, width, height, depth, rotation (9),
translation (3) and object id, in that frame's camera frame [5]. The scorer applies pose NMS
(3 cm, 30 degrees, 10 per object), checks collision and force closure, and averages precision
over the top 1 to 50 grasps at friction 0.2 to 1.2; `ap` is AP for all, seen, similar, novel [3][5].
```python
from graspnetAPI import GraspGroup, GraspNetEval   # pip install . from the GitHub source
GraspGroup(preds).save_npy(f"dump/scene_{s:04d}/realsense/{a:04d}.npy")  # N x 17, each frame
res, ap = GraspNetEval(root, camera="realsense", split="test").eval_all("dump", proc=8)
```

## Traps

- **Licences differ by part.** graspnetAPI's LICENSE (2025-06-16) is MIT, but its docs still say
  non-commercial CC 4.0 and the scorer imports Dex-Net files under a UC Berkeley not-for-profit
  licence [5]. graspnet-baseline is an SJTU research-only agreement whose text names AlphaPose [7].
- **Old pip release.** PyPI's 1.2.11 (2023-12-31) pins numpy 1.20.3 [5][6], and the README warns
  the pip version may be old. Install from source: setup.py (2026-06-29) relaxes the pins [5].
- **Approach is x.** GraspNet grasps approach along x [5]; most grasp nets and hand frames use z,
  so rotate before dumping. Widths over 0.1 m are clipped when scored [5].
- **Camera matters.** Score per camera; the authors say RealSense weights may transfer better [7].
- **Slow scoring.** Without `dex_models` the scorer rebuilds Dex-Net models from meshes [5].

## Alternatives

graspnet-baseline (PyTorch, CUDA ops, last commit 2025-02-17) reports AP 47.47, 42.27 and 16.61
(seen, similar, novel, RealSense) [7]. AnyGrasp, the team's closed SDK, needs a per-machine
licence applied for by form [8].

## Sources

1. [GraspNet home: GraspNet-1Billion overview, related datasets, news](https://graspnet.net/), accessed 2026-11-25
2. [GraspNet: dataset downloads, sizes, object list and file layout](https://graspnet.net/datasets.html), accessed 2026-11-25
3. [GraspNet: dataset split and evaluation metric](https://graspnet.net/evaluation.html), accessed 2026-11-25
4. [GraspNet: about and licence](https://graspnet.net/about), accessed 2026-11-25
5. [graspnetAPI repository: README, LICENSE, setup.py history, evaluation code, docs source, bundled Dex-Net licence headers](https://github.com/graspnet/graspnetAPI), accessed 2026-11-25
6. [PyPI: graspnetAPI releases](https://pypi.org/project/graspnetAPI/), accessed 2026-11-25
7. [graspnet-baseline repository: README, LICENSE, data loader, history](https://github.com/graspnet/graspnet-baseline), accessed 2026-11-25
8. [AnyGrasp SDK repository: README and licence registration](https://github.com/graspnet/anygrasp_sdk), accessed 2026-11-25

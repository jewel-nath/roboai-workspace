---
type: tool
name: 3D Diffusion Policy (DP3)
summary: Ze et al.'s RSS 2024 imitation-learning policy that runs a diffusion action head on a small cropped point cloud from one depth camera; the authors report most of 72 simulated tasks learned from 10 demonstrations and 85% on four real tasks from 40. MIT research code with no releases and no code change since May 2025; no maintained port in LeRobot or ManiSkill.
tags: [dp3, 3d-diffusion-policy, point-cloud, diffusion-policy, imitation-learning, depth-camera, dexterous-manipulation, idp3, metaworld, adroit, dexart, zarr, research-code]
kind: policy
area: learning
support:
license: MIT
links: {repo: "https://github.com/YanjieZe/3D-Diffusion-Policy", docs: , site: "https://3d-diffusion-policy.github.io"}
version: {tested: , latest: , as_of: 2026-11-25}
platforms: [linux]
agent_access: script
registry:
evidence: researched
last_verified: 2026-11-25
sources:
  - {url: "https://arxiv.org/abs/2403.03954", title: "Ze et al.: 3D Diffusion Policy: Generalizable Visuomotor Policy Learning via Simple 3D Representations (arXiv 2403.03954, RSS 2024)", accessed: 2026-11-25}
  - {url: "https://github.com/YanjieZe/3D-Diffusion-Policy", title: "DP3 repository: README, INSTALL.md, LICENSE, dp3.yaml, simple_dp3.yaml, task configs, scripts, history, issues", accessed: 2026-11-25}
  - {url: "https://github.com/YanjieZe/Improved-3D-Diffusion-Policy", title: "iDP3 repository: README, LICENSE, history", accessed: 2026-11-25}
  - {url: "https://www.therobotreport.com/intel-issues-end-of-life-notice-realsense-lidar/", title: "The Robot Report: Intel issues end-of-life notice for RealSense LiDAR (2021-09-01)", accessed: 2026-11-25}
  - {url: "https://github.com/RoboTwin-Platform/RoboTwin", title: "RoboTwin repository: README news and XPolicyLab submodule", accessed: 2026-11-25}
  - {url: "https://github.com/XPolicyLab/XPolicyLab", title: "XPolicyLab repository: policy folder", accessed: 2026-11-25}
  - {url: "https://github.com/huggingface/lerobot", title: "LeRobot repository: policy list and source tree (no point-cloud policy)", accessed: 2026-11-25}
  - {url: "https://github.com/haosulab/ManiSkill", title: "ManiSkill repository: examples/baselines", accessed: 2026-11-25}
---

# 3D Diffusion Policy (DP3)

DP3 (Ze et al., RSS 2024) feeds a diffusion action head with a compact feature of a sparse point
cloud, cropped to the workspace and downsampled, plus the robot state [1][2]. It is the common 3D
imitation baseline; its README lists 18 later works built on it [2]. **Code: MIT**; no pretrained
weights; its demonstration data (OneDrive, Google Drive) states no licence [2]. **Idle research
code:** no releases; last commit 2025-10-16 (README), last code change 2025-05-14 [2].

## When to use it

- **Use it** with a good depth camera, a fixed workspace and few demonstrations, or a dexterous
  hand. The authors report most of 72 simulated tasks learned from 10 demonstrations (24.2%
  relative gain over baselines) and 85% on four real Franka plus Allegro hand tasks from 40
  demonstrations each [1]. We found no independent rerun.
- **Use something else** with RGB cameras only: [Diffusion Policy](diffusion-policy.md) or
  [ACT](act.md) in [LeRobot](../frameworks/lerobot.md), which has no point-cloud policy [7]. On a
  humanoid with a head camera, the authors' iDP3 (MIT, last commit 2025-06-16) needs no camera
  calibration or point-cloud segmentation [3].

## Setup

Linux only (MuJoCo 2.1.0 and `mujoco-py`); tested with CUDA 11.7 on RTX 3090, A40, A800 and A100.
Follow `INSTALL.md` exactly: conda Python 3.8, torch from the `cu121` index, `pip install -e`
the package, then MuJoCo 2.1.0, its bundled gym 0.21, Metaworld and DexArt. Generate demos with
`bash scripts/gen_demonstration_adroit.sh hammer`, then train with
`bash scripts/train_policy.sh dp3 adroit_hammer 0112 0 0` (algorithm, task, tag, seed, GPU) [2].

**GPU (authors' figures):** about 10 GB and 3 hours on an A40; Simple DP3 trains in 1 to 2 hours
and infers at 25 FPS [2]. iDP3 trained on an RTX 4090 and ran on the robot's onboard CPU [3]. No
Jetson figures. **Inputs** [2]: 512 (simulation) or 1024 (real) XYZ points plus `agent_pos`, in
Zarr; 2 observation steps, horizon 16, 8 executed actions, 10 DDIM steps. Bundled benchmarks:
Adroit, DexArt and MetaWorld, 57 tasks.

## Traps

- **Point-cloud quality decides it.** The authors used a RealSense L515 and warn that a D435 may
  fail from poor point clouds [2][3]; Intel discontinued the L515 in 2021 [4]. Crop away the
  table and background [2].
- **Action space.** The real setup used relative end-effector and joint actions, but the README
  now advises absolute positions and horizons of 8 to 32 [2]. Pick one and keep it.
- **Results vary by seed.** Open issues report large swings across training seeds and a weak
  `metaworld_disassemble`; a May 2026 question has no reply. Benchmark several seeds from the
  training logs, as the authors advise, not from `eval_policy.sh` [2].
- **Old stack.** Python 3.8, MuJoCo 2.1.0, gym 0.21 and online `wandb`; see `ERROR_CATCH.md` [2].
- **No maintained port.** RoboTwin 2.0 fixed its DP3 evaluation in July 2025 [5], but its
  policies now come from XPolicyLab, which has no DP3 [6]; neither do ManiSkill's baselines [8].
  For real-robot code, the README points to iDP3 [2][3].

## Alternatives

[Diffusion Policy](diffusion-policy.md), [ACT](act.md), iDP3 [3], [pi0](../models/pi0.md); see
[Choose a robot learning policy](../../guides/choose-a-robot-learning-policy.md).

## Sources

1. [Ze et al.: 3D Diffusion Policy: Generalizable Visuomotor Policy Learning via Simple 3D Representations (arXiv 2403.03954, RSS 2024)](https://arxiv.org/abs/2403.03954), accessed 2026-11-25
2. [DP3 repository: README, INSTALL.md, LICENSE, dp3.yaml, simple_dp3.yaml, task configs, scripts, history, issues](https://github.com/YanjieZe/3D-Diffusion-Policy), accessed 2026-11-25
3. [iDP3 repository: README, LICENSE, history](https://github.com/YanjieZe/Improved-3D-Diffusion-Policy), accessed 2026-11-25
4. [The Robot Report: Intel issues end-of-life notice for RealSense LiDAR (2021-09-01)](https://www.therobotreport.com/intel-issues-end-of-life-notice-realsense-lidar/), accessed 2026-11-25
5. [RoboTwin repository: README news and XPolicyLab submodule](https://github.com/RoboTwin-Platform/RoboTwin), accessed 2026-11-25
6. [XPolicyLab repository: policy folder](https://github.com/XPolicyLab/XPolicyLab), accessed 2026-11-25
7. [LeRobot repository: policy list and source tree (no point-cloud policy)](https://github.com/huggingface/lerobot), accessed 2026-11-25
8. [ManiSkill repository: examples/baselines](https://github.com/haosulab/ManiSkill), accessed 2026-11-25

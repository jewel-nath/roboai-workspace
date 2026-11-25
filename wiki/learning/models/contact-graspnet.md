---
type: tool
name: Contact-GraspNet
summary: NVIDIA's 2021 network that proposes 6-DoF grasps for a Franka Panda-style parallel-jaw gripper from one depth view of a cluttered scene; research-and-evaluation-only licence, TensorFlow 2.2 code unchanged since 2021, unofficial PyTorch ports, no ROS 2 package.
tags: [contact-graspnet, grasping, 6-dof-grasp, grasp-generation, depth, point-cloud, parallel-jaw, franka-panda, tensorflow, pytorch, nvidia, moveit2, non-commercial]
kind: model
area: manip
support:
license: LicenseRef-NVIDIA-Source-Code-License
links: {repo: "https://github.com/NVlabs/contact_graspnet", docs: "https://github.com/NVlabs/contact_graspnet/blob/main/README.md", site: "https://research.nvidia.com/publication/2021-03_contact-graspnet-efficient-6-dof-grasp-generation-cluttered-scenes"}
version: {tested: , latest: , as_of: 2026-11-25}
platforms: [linux]
agent_access: script
registry:
evidence: researched
last_verified: 2026-11-25
sources:
  - {url: "https://github.com/NVlabs/contact_graspnet", title: "Contact-GraspNet repository: README, License.pdf, conda file, inference and estimator code, config, history, issues (issue 19)", accessed: 2026-11-25}
  - {url: "https://github.com/elchun/contact_graspnet_pytorch", title: "contact_graspnet_pytorch (unofficial PyTorch port): README, License.pdf, conda file, history", accessed: 2026-11-25}
  - {url: "https://pypi.org/project/cgn-pytorch/", title: "PyPI: cgn-pytorch releases and metadata, with its sebbyjp/cgn_pytorch repository", accessed: 2026-11-25}
  - {url: "https://github.com/frankaemika/franka_ros/blob/develop/franka_description/robots/common/franka_hand.xacro", title: "franka_description: franka_hand.xacro finger joint axes", accessed: 2026-11-25}
  - {url: "https://github.com/moveit/moveit2_tutorials", title: "moveit2_tutorials (main): MTC pick-and-place tutorial and Deep Grasps page", accessed: 2026-11-25}
  - {url: "https://github.com/NVlabs/GraspGenX", title: "GraspGenX repository: README, LICENSE, Hugging Face checkpoint licence", accessed: 2026-11-25}
  - {url: "https://nvidia-isaac-ros.github.io/releases/index.html", title: "Isaac ROS release notes (5.0.0 and 5.1.0)", accessed: 2026-11-25}
---

# Contact-GraspNet

NVIDIA's ICRA 2021 network that turns one depth view of a cluttered table into many 6-DoF grasps
for a two-finger gripper, each with a score and an opening width [1]. Builders use it to pick
unknown objects with MoveIt 2. **Unmaintained:** no code change since 2021-08-30, no releases,
no replies to issues since mid-2023, no ROS code [1]. **Licence:** research or evaluation only
(NVIDIA Source Code License); the Google Drive checkpoints carry no licence of their own [1].

## When to use it

- **Use it** as a baseline or lab demo with a Panda-like gripper; mask objects first, as the README
  advises [1], with [SAM](segment-anything.md) or [Grounding DINO](grounding-dino.md).
- **Use something else** for a product or another gripper: GraspGenX (see Alternatives).

## Setup

Linux, an NVIDIA GPU with 8 GB to run (24 GB and 64 GB RAM to train). The README says Python 3.7,
TF 2.2, CUDA 11.1; the conda file pins `tensorflow-gpu` 2.2.0, `cudatoolkit` 10.1, cuDNN 7.6 [1].
Unofficial PyTorch ports: `elchun/contact_graspnet_pytorch` (PyTorch 2.0.1, CUDA 11.7, weights
included, core features only, last commit 2025-02-20) [2]; `pip install cgn-pytorch` (0.4.3) [3].
```bash
conda env create -f contact_graspnet_env.yml && conda activate contact_graspnet_env
sh compile_pointnet_tfops.sh && python contact_graspnet/inference.py --np_path="test_data/*.npy"
```

## How an agent works with it

- **Input** [1]: `.npz` with `depth` (metres), `K`, optional `segmap` and `rgb`; or `xyz` (N x 3).
  ROS 2 `16UC1` depth is millimetres ([image_pipeline](../../software/image-pipeline.md)); `K` is
  `camera_info.k`. Default `z_range`: 0.2 to 1.8 m. GraspNet-1Billion PNGs load directly.
- **Output** [1]: `predict_scene_grasps_from_depth_K_and_2d_seg()` returns per mask id N x 4 x 4
  grasps in the camera's OpenCV frame (a ROS optical frame), scores, contacts, openings (max
  0.08 m). Grasp frame: Panda hand, approach z, fingers close along x, contacts 0.1034 m out.
- **To [MoveIt 2](../../software/moveit2.md)** [5]: [tf2](../../software/tf2.md) to the planning
  frame; each grasp into an MTC `GeneratePose` in `ComputeIK` (`setIKFrame` at the TCP), then
  `MoveRelative` to approach and lift, as the MTC pick-and-place tutorial does; `ComputeIK` must
  solve and the fingers must close on the object in sim. MoveIt's Deep Grasps demo is MoveIt 1.

## Traps

- **New GPUs.** On an RTX 3080 Ti inference was slow; users later ran Python 3.8, TF 2.5, CUDA
  11.2 or 11.3, cuDNN 8.2 on RTX 3090 and A5000; no official file came (issue 19) [1].
- **Frame turned 90 degrees.** Franka's ROS hand closes along y [4], this model along x [1]: turn
  each grasp about z, even for a Panda; for other grippers, offset to the TCP and check the stroke.
- **README typo:** point clouds use the key `xyz`, not `xzy` [1].
- **Width not saved:** `inference.py` drops the openings from `results/*.npz`; use the API [1].
- **Licence drift.** The elchun port keeps NVIDIA's licence [2]; `cgn-pytorch` says MIT on PyPI,
  has no LICENSE file and loads weights it calls based on NVIDIA's [3].

## Alternatives

GraspGenX: Apache-2.0 code, NVIDIA Open Model License weights, one model for any gripper from its
URDF (GraspGen needs one per gripper) [6]; Isaac ROS 5.1.0 wraps it as `isaac_ros_grasping`, for
Lyrical only [7]. Benchmark, AnyGrasp: [GraspNet-1Billion](../datasets/graspnet-1billion.md).

## Sources

1. [Contact-GraspNet repository: README, License.pdf, conda file, inference and estimator code, config, history, issues (issue 19)](https://github.com/NVlabs/contact_graspnet), accessed 2026-11-25
2. [contact_graspnet_pytorch (unofficial PyTorch port): README, License.pdf, conda file, history](https://github.com/elchun/contact_graspnet_pytorch), accessed 2026-11-25
3. [PyPI: cgn-pytorch releases and metadata, with its sebbyjp/cgn_pytorch repository](https://pypi.org/project/cgn-pytorch/), accessed 2026-11-25
4. [franka_description: franka_hand.xacro finger joint axes](https://github.com/frankaemika/franka_ros/blob/develop/franka_description/robots/common/franka_hand.xacro), accessed 2026-11-25
5. [moveit2_tutorials (main): MTC pick-and-place tutorial and Deep Grasps page](https://github.com/moveit/moveit2_tutorials), accessed 2026-11-25
6. [GraspGenX repository: README, LICENSE, Hugging Face checkpoint licence](https://github.com/NVlabs/GraspGenX), accessed 2026-11-25
7. [Isaac ROS release notes (5.0.0 and 5.1.0)](https://nvidia-isaac-ros.github.io/releases/index.html), accessed 2026-11-25

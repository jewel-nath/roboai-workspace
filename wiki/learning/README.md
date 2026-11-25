# Learning

Robot learning: policies, foundation models and datasets. Template:
[templates/tool.md](../../templates/tool.md) with `kind: policy`, `kind: model` or `kind: dataset`.

| Folder | Holds |
|---|---|
| `policies/` | Imitation and reinforcement learning methods: ACT, Diffusion Policy |
| `models/` | Foundation and vision-language-action models |
| `datasets/` | Robot datasets: what robots, tasks, size, format, licence |
| `frameworks/` | Libraries and simulators you install to train or run policies: LeRobot, Isaac Lab |
| `benchmarks/` | Simulated task suites that score policies: LIBERO, SimplerEnv |

- This area changes monthly. Set `last_verified` honestly and re-check before relying on a page.
- Say what hardware a model or policy needs to train and to run.

## Index

<!-- index:start -->
| Name | Kind | Area | Support | Licence | Tested | Agent access | Verified |
|---|---|---|---|---|---|---|---|
| [3D Diffusion Policy (DP3)](policies/3d-diffusion-policy.md) | policy | learning | — | MIT | — | script | 2026-11-25 |
| [ACT (Action Chunking with Transformers)](policies/act.md) | policy | learning | — | MIT | — | script | 2026-11-25 |
| [BEHAVIOR-1K (with OmniGibson)](benchmarks/behavior-1k.md) | framework | learning | — | MIT | — | script | 2026-11-25 |
| [BridgeData V2](datasets/bridgedata-v2.md) | dataset | learning | — | CC-BY-4.0 | — | script | 2026-11-25 |
| [CALVIN](benchmarks/calvin.md) | framework | learning | — | MIT | — | script | 2026-11-25 |
| [Diffusion Policy](policies/diffusion-policy.md) | policy | learning | — | MIT | — | script | 2026-11-25 |
| [DROID](datasets/droid.md) | dataset | learning | — | CC-BY-4.0 | — | script | 2026-11-25 |
| [Gymnasium](frameworks/gymnasium.md) | library | learning | — | MIT | — | script | 2026-11-25 |
| [Isaac GR00T](models/gr00t.md) | model | learning | — | Apache-2.0 | — | script | 2026-11-25 |
| [Isaac Lab](frameworks/isaac-lab.md) | framework | learning | — | BSD-3-Clause | — | cli | 2026-11-25 |
| [LeRobot](frameworks/lerobot.md) | framework | learning | — | Apache-2.0 | — | cli | 2026-11-25 |
| [LIBERO](benchmarks/libero.md) | framework | learning | — | MIT | — | script | 2026-11-25 |
| [ManiSkill](frameworks/maniskill.md) | framework | learning | — | Apache-2.0 | — | script | 2026-11-25 |
| [Octo](models/octo.md) | model | learning | — | MIT | — | script | 2026-11-25 |
| [Open X-Embodiment](datasets/open-x-embodiment.md) | dataset | learning | — | CC-BY-4.0 | — | script | 2026-11-25 |
| [OpenVLA (and OpenVLA-OFT)](models/openvla.md) | model | learning | — | MIT | — | script | 2026-11-25 |
| [RDT (RDT-1B and RDT2)](models/rdt.md) | model | learning | — | MIT | — | script | 2026-11-25 |
| [RLBench](benchmarks/rlbench.md) | framework | learning | — | LicenseRef-RLBench-Imperial-Non-Commercial | — | script | 2026-11-25 |
| [RoboCasa (RoboCasa365)](benchmarks/robocasa.md) | framework | learning | — | MIT | — | script | 2026-11-25 |
| [robomimic](frameworks/robomimic.md) | framework | learning | — | MIT | — | script | 2026-11-25 |
| [robosuite](frameworks/robosuite.md) | framework | learning | — | MIT | — | script | 2026-11-25 |
| [RT-1 (Robotics Transformer 1)](models/rt-1.md) | model | learning | — | Apache-2.0 | — | script | 2026-11-25 |
| [RT-2 (Robotics Transformer 2)](models/rt-2.md) | model | learning | — | — | — | — | 2026-11-25 |
| [SimplerEnv (SIMPLER)](benchmarks/simpler-env.md) | framework | learning | — | MIT | — | script | 2026-11-25 |
| [SmolVLA](models/smolvla.md) | model | learning | — | Apache-2.0 | — | script | 2026-11-25 |
| [Stable-Baselines3](frameworks/stable-baselines3.md) | library | learning | — | MIT | — | script | 2026-11-25 |
| [π0 family (openpi - π0, π0-FAST, π0.5)](models/pi0.md) | model | learning | — | Apache-2.0 | — | script | 2026-11-25 |
| [Contact-GraspNet](models/contact-graspnet.md) | model | manip | — | LicenseRef-NVIDIA-Source-Code-License | — | script | 2026-11-25 |
| [GraspNet-1Billion](datasets/graspnet-1billion.md) | dataset | manip | — | CC-BY-NC-SA-4.0 | — | script | 2026-11-25 |
| [FoundationPose](models/foundationpose.md) | model | perception | — | LicenseRef-NVIDIA-Source-Code-License | — | script | 2026-11-23 |
| [Grounding DINO](models/grounding-dino.md) | model | perception | — | Apache-2.0 | — | script | 2026-11-23 |
| [KITTI and KITTI-360](datasets/kitti.md) | dataset | perception | — | CC-BY-NC-SA-3.0 | — | cli | 2026-11-23 |
| [Segment Anything (SAM, SAM 2, SAM 3)](models/segment-anything.md) | model | perception | — | LicenseRef-SAM-License | — | script | 2026-11-23 |
| [TUM RGB-D](datasets/tum-rgbd.md) | dataset | perception | — | CC-BY-4.0 | — | cli | 2026-11-23 |
| [YOLO](models/yolo.md) | model | perception | — | AGPL-3.0-or-later | — | cli | 2026-11-23 |
<!-- index:end -->

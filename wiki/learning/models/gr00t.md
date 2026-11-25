---
type: tool
name: Isaac GR00T
summary: NVIDIA's open vision-language-action model for humanoids and arms; N1.7 (3B, Cosmos-Reason2 backbone, flow-matching action head) has Apache-2.0 code and weights under the NVIDIA Open Model License, which allows commercial use, while N1.5 and N1.6 weights are non-commercial. Fine-tunes on 40 GB GPUs, runs on 16 GB GPUs and Jetson AGX Thor or Orin with TensorRT; also in LeRobot.
tags: [gr00t, groot, isaac-gr00t, nvidia, vla, vision-language-action, foundation-model, humanoid, cross-embodiment, flow-matching, cosmos-reason, lerobot, tensorrt, jetson-thor, jetson-orin, unitree-g1, so-101, fine-tuning]
kind: model
area: learning
support:
license: Apache-2.0
links: {repo: "https://github.com/NVIDIA/Isaac-GR00T", docs: "https://github.com/NVIDIA/Isaac-GR00T/tree/main/getting_started", site: "https://developer.nvidia.com/isaac/gr00t"}
version: {tested: , latest: N1.7, as_of: 2026-11-25}
platforms: [linux]
agent_access: script
registry:
evidence: researched
last_verified: 2026-11-25
sources:
  - {url: "https://github.com/NVIDIA/Isaac-GR00T", title: "Isaac-GR00T repository: README, LICENSE, FAQ, CLAUDE.md, pyproject.toml, tags, branches and issues", accessed: 2026-11-25}
  - {url: "https://github.com/NVIDIA/Isaac-GR00T/blob/main/getting_started/hardware_recommendation.md", title: "Isaac-GR00T: Hardware Recommendations (N1.7)", accessed: 2026-11-25}
  - {url: "https://github.com/NVIDIA/Isaac-GR00T/blob/main/scripts/deployment/README.md", title: "Isaac-GR00T: Deployment and Inference Guide (TensorRT, Jetson Thor and Orin, DGX Spark)", accessed: 2026-11-25}
  - {url: "https://github.com/NVIDIA/Isaac-GR00T/tree/main/getting_started", title: "Isaac-GR00T getting-started guides: policy API, data config, fine-tuning a new embodiment", accessed: 2026-11-25}
  - {url: "https://huggingface.co/nvidia/GR00T-N1.7-3B", title: "Hugging Face: nvidia/GR00T-N1.7-3B model card and LICENSE", accessed: 2026-11-25}
  - {url: "https://huggingface.co/nvidia/GR00T-N1.6-3B", title: "Hugging Face: nvidia/GR00T-N1.6-3B model card and LICENSE (NVIDIA License, non-commercial)", accessed: 2026-11-25}
  - {url: "https://www.nvidia.com/en-us/agreements/enterprise-software/nvidia-open-model-license/", title: "NVIDIA Open Model License Agreement (version of 2025-10-24)", accessed: 2026-11-25}
  - {url: "https://huggingface.co/nvidia/Cosmos-Reason2-2B", title: "Hugging Face: nvidia/Cosmos-Reason2-2B model card (gated)", accessed: 2026-11-25}
  - {url: "https://developer.nvidia.com/isaac/gr00t/llm-info.md", title: "NVIDIA: LLM Info - NVIDIA Isaac GR00T (version history, licences, N2 status)", accessed: 2026-11-25}
  - {url: "https://huggingface.co/blog/nvidia/nvidia-isaac-teleop-and-gr00t17-in-lerobot", title: "Hugging Face blog: NVIDIA Isaac Teleop and GR00T 1.7 open VLA model available in LeRobot (2026-07-07)", accessed: 2026-11-25}
  - {url: "https://nvidia-isaac-ros.github.io/releases/index.html", title: "Isaac ROS release notes (4.4 to 5.1): GR00T workflows for Unitree G1", accessed: 2026-11-25}
  - {url: "https://research.nvidia.com/labs/gear/gr00t-2/", title: "NVIDIA GEAR: GR00T 2 world-action model page", accessed: 2026-11-25}
  - {url: "https://huggingface.co/datasets/nvidia/PhysicalAI-Robotics-GR00T-X-Embodiment-Sim", title: "Hugging Face: nvidia/PhysicalAI-Robotics-GR00T-X-Embodiment-Sim dataset card (CC-BY-4.0)", accessed: 2026-11-25}
  - {url: "https://huggingface.co/datasets/nvidia/PhysicalAI-Robotics-GR00T-Teleop-Sim", title: "Hugging Face: nvidia/PhysicalAI-Robotics-GR00T-Teleop-Sim dataset card (CC-BY-NC-4.0)", accessed: 2026-11-25}
---

# Isaac GR00T

GR00T is NVIDIA's open vision-language-action (VLA) model. N1.7 (3B parameters) pairs the
Cosmos-Reason2-2B vision-language model with a flow-matching diffusion transformer that outputs
action chunks; it takes camera images, a language instruction and the robot state [1][5].
Builders fine-tune it on their own demonstrations for an arm or humanoid, then serve it from a
GPU or a Jetson. **Licences:** code Apache-2.0 [1]; **N1.7 weights** NVIDIA Open Model License,
which allows commercial use [5][7]; **N1.5 and N1.6 weights** non-commercial research or
evaluation only [6][9]. NVIDIA's datasets differ: GR00T-X-Embodiment-Sim is CC-BY-4.0 [13],
GR00T-Teleop-Sim CC-BY-NC-4.0 [14]. Very active: last commit 2026-11-17, 217 open issues [1].

## When to use it

- **Use it** for a humanoid or a bimanual or single arm when you can collect about 100
  demonstrations per simple task (NVIDIA's guide; 500+ for multi-step, 2,000+ for humanoid
  tasks) and have a 40 GB GPU to fine-tune [1][2]. It runs zero-shot only on its pretraining
  embodiments (DROID Franka, Unitree G1, R1 Pro Sharpa, generic X-DOF) [4].
- **Use N1.7:** the only version with commercially usable weights, and the one LeRobot ships
  (it dropped N1.5) [9][10]. GR00T N2 was previewed at GTC 2026 but is not released [9]; the
  GR00T 2 research page (November 2026) promises code in December [12].
- **Use something else** on an 8 to 12 GB GPU: [SmolVLA](smolvla.md), [ACT](../policies/act.md),
  [Diffusion Policy](../policies/diffusion-policy.md); [pi0](pi0.md) for Gemma-based weights. See
  [Choose a robot learning policy](../../guides/choose-a-robot-learning-policy.md).

## Setup

Ubuntu 22.04+ on x86-64 with an NVIDIA GPU, Python 3.12, CUDA 12.8 [1][2]:

```bash
sudo apt-get install -y git-lfs ffmpeg && git lfs install  # FFmpeg 4-7; 8 breaks torchcodec
git clone --recurse-submodules https://github.com/NVIDIA/Isaac-GR00T && cd Isaac-GR00T
uv sync --python 3.12          # pins torch 2.9.0, transformers 4.57.3, flash-attn, TensorRT
uv run huggingface-cli login   # after accepting the terms of nvidia/Cosmos-Reason2-2B
```

Jetson AGX Thor and Orin need JetPack 7.2 (CUDA 13.2, PyTorch 2.13); JetPack 6 is no longer
supported. Run `bash scripts/deployment/thor/install_deps.sh` (or `orin/`), then
`source .venv/bin/activate && source scripts/activate_thor.sh`; Dockerfiles exist per platform
[1][3]. Linux only. The base checkpoint downloads about 6 GB on first use [1].

| Need | NVIDIA's figure [2] |
|---|---|
| Inference | 1 GPU with 16 GB+ (RTX 4090, L40, H100, AGX Thor, AGX Orin, DGX Spark) |
| Fine-tuning (default: projector + action head) | 40 GB+ per GPU; peak under ~35 GB |
| Fine-tuning with `--tune-llm` or `--tune-visual` | 80 GB+ per GPU |

NVIDIA's replanning rates, PyTorch then TensorRT [2]: H100 11.7 and 35.9 Hz; AGX Thor 8.9 and
12.4 Hz (35.6 ms with mixed-NVFP4 engines [3]); Orin (64 GB) 2.9 and 6.6 Hz. Action chunks let
10 Hz replanning drive a 30 Hz robot [2].

## How an agent works with it

**Data.** GR00T reads a LeRobot v2 dataset plus `meta/modality.json`, which splits the state
and action arrays into named fields and lists the video keys [1]. Convert LeRobot v3 datasets
with `scripts/lerobot_conversion/convert_v3_to_v2.py`, and AV1 videos to H.264 [1]. Statistics:
`python gr00t/data/stats.py --dataset-path <ds> --embodiment-tag <tag>` [4].

**Embodiment tag.** Every command takes `--embodiment-tag`. Pretrain tags work with the base
model; post-train tags (`LIBERO_PANDA`, `SIMPLER_ENV_WIDOWX` and others) need their fine-tuned
checkpoint; your robot is `NEW_EMBODIMENT` plus a modality config such as
`examples/SO100/so100_config.py` (SO-100, the [SO-101](../../robots/so-101.md)'s forerunner) [1][4].

**Fine-tune** (one GPU; `torchrun --nproc_per_node=8` for eight) [1]:

```bash
CUDA_VISIBLE_DEVICES=0 uv run python gr00t/experiment/launch_finetune.py \
  --base-model-path nvidia/GR00T-N1.7-3B --dataset-path <your_dataset> \
  --embodiment-tag NEW_EMBODIMENT --modality-config-path examples/SO100/so100_config.py \
  --num-gpus 1 --output-dir ./ckpt --max-steps 2000 --global-batch-size 32
```

**Inputs and outputs** [4]: `video` holds one uint8 array (B, T, H, W, 3) per camera, `state`
float32 arrays (B, T, D), `language` the task string. The model returns an action chunk; the
base checkpoint predicts 40 steps and `--execution-horizon` (8 to 16 typical) sets how many run
before replanning. N1.7 uses relative end-effector and joint actions; the SO100 example keeps
the gripper absolute [4].

**Serve and check** [1]:

- `uv run python gr00t/eval/run_gr00t_server.py --model-path ./ckpt --embodiment-tag
  NEW_EMBODIMENT` serves over ZeroMQ on port 5555; the robot side calls
  `PolicyClient(host, port).get_action(obs)`. There is no ROS 2 node in the repo; wrap the
  client yourself. Isaac ROS 4.5 and 4.6 (Jazzy) ship a GR00T workflow for the
  [Unitree G1](../../robots/unitree-g1.md) (`isaac_ros_physical_ai`); on Lyrical from 5.1 [11].
- `gr00t/eval/open_loop_eval.py` plots predicted against recorded actions with MSE and MAE;
  the error should fall as training steps rise [1][4]. Starting the server with
  `--dataset-path` and no model replays recorded actions, to test the robot wiring first [1].
- Closed loop: [LIBERO](../benchmarks/libero.md) and [SimplerEnv](../benchmarks/simpler-env.md)
  examples, then the real robot with torque limits [1].

**TensorRT** ([TensorRT](../../software/tensorrt.md)):
`python scripts/deployment/build_trt_pipeline.py` exports ONNX, builds engines (2 to 5 minutes),
checks them against PyTorch (cosine similarity 0.999+ passes) and benchmarks; run inference with
`--inference-mode trt_full_pipeline` [3].

**LeRobot** ([LeRobot](../frameworks/lerobot.md)): install the `groot` extra and train with
`--policy.type=groot --policy.base_model_path=nvidia/GR00T-N1.7-3B`; LeRobot needs a v3.0
dataset [10].

## Traps

- **Licence depends on the version.** A fine-tune of N1.5 or N1.6 stays non-commercial [6][9].
  N1.7 terms require an NVIDIA attribution notice and a "Built on NVIDIA Cosmos" credit
  when you share the model, end your rights if you strip a guardrail without a
  replacement, and NVIDIA may update them [7]. NVIDIA's own LLM-info page still says N1.7's HF
  LICENSE is non-commercial [9]; the file switched to the Open Model License on 2026-11-10 [5].
- **`GatedRepoError` or 401 on load.** Every checkpoint loads the gated Cosmos-Reason2-2B;
  accept its terms on Hugging Face and log in [1][8].
- **Tag and data mismatch.** A post-train tag on the base model, or a tag whose state keys do not
  match the dataset, fails; only one `NEW_EMBODIMENT` config may be imported per process [4].
- **Statistics and defaults.** Changing the action `delta_indices` without re-running `stats.py`
  gives an `IndexError`; NaN loss points to normalisation [4]. `--state_dropout_prob` is 0.8 in
  the model config but 0.2 in the fine-tune CLI; lower it if the task leans on joint state [1].
- **Jetson environments break.** On aarch64, `uv run` re-syncs to the x86 lock file and destroys
  the platform environment; use plain `python` after activating [1]. Orin with TensorRT stays
  under 10 Hz, enough only for slow tasks; an 8 GB Orin is below the 16 GB minimum [2].
- **Engines do not travel.** TensorRT engines are tied to the GPU architecture, have a static
  batch size, and must be rebuilt when the padding-mask settings change; evaluate TensorRT with
  `--n-envs 1` [1][3].
- **N1.6 checkpoints need N1.6 code.** N1.7 moved the package to `gr00t_n1d7`, the backbone to
  Qwen3-VL and transformers to 4.57.3; use the `n1d6` branch for older checkpoints [1].
- **Results are NVIDIA's.** LIBERO 96.5% average for N1.7 is NVIDIA's own LeRobot run [10]; runs
  vary 5 to 6% from image augmentation [1].

## Alternatives

[pi0](pi0.md), [SmolVLA](smolvla.md), [OpenVLA](openvla.md), [Octo](octo.md), [RDT](rdt.md),
[ACT](../policies/act.md), [Diffusion Policy](../policies/diffusion-policy.md). Skills:
[learn-robot-learning](../../../skills/learn-robot-learning/SKILL.md),
[learn-edge-deployment](../../../skills/learn-edge-deployment/SKILL.md).

## Sources

1. [Isaac-GR00T repository: README, LICENSE, FAQ, CLAUDE.md, pyproject.toml, tags, branches and issues](https://github.com/NVIDIA/Isaac-GR00T), accessed 2026-11-25
2. [Isaac-GR00T: Hardware Recommendations (N1.7)](https://github.com/NVIDIA/Isaac-GR00T/blob/main/getting_started/hardware_recommendation.md), accessed 2026-11-25
3. [Isaac-GR00T: Deployment and Inference Guide (TensorRT, Jetson Thor and Orin, DGX Spark)](https://github.com/NVIDIA/Isaac-GR00T/blob/main/scripts/deployment/README.md), accessed 2026-11-25
4. [Isaac-GR00T getting-started guides: policy API, data config, fine-tuning a new embodiment](https://github.com/NVIDIA/Isaac-GR00T/tree/main/getting_started), accessed 2026-11-25
5. [Hugging Face: nvidia/GR00T-N1.7-3B model card and LICENSE](https://huggingface.co/nvidia/GR00T-N1.7-3B), accessed 2026-11-25
6. [Hugging Face: nvidia/GR00T-N1.6-3B model card and LICENSE (NVIDIA License, non-commercial)](https://huggingface.co/nvidia/GR00T-N1.6-3B), accessed 2026-11-25
7. [NVIDIA Open Model License Agreement (version of 2025-10-24)](https://www.nvidia.com/en-us/agreements/enterprise-software/nvidia-open-model-license/), accessed 2026-11-25
8. [Hugging Face: nvidia/Cosmos-Reason2-2B model card (gated)](https://huggingface.co/nvidia/Cosmos-Reason2-2B), accessed 2026-11-25
9. [NVIDIA: LLM Info - NVIDIA Isaac GR00T (version history, licences, N2 status)](https://developer.nvidia.com/isaac/gr00t/llm-info.md), accessed 2026-11-25
10. [Hugging Face blog: NVIDIA Isaac Teleop and GR00T 1.7 open VLA model available in LeRobot (2026-07-07)](https://huggingface.co/blog/nvidia/nvidia-isaac-teleop-and-gr00t17-in-lerobot), accessed 2026-11-25
11. [Isaac ROS release notes (4.4 to 5.1): GR00T workflows for Unitree G1](https://nvidia-isaac-ros.github.io/releases/index.html), accessed 2026-11-25
12. [NVIDIA GEAR: GR00T 2 world-action model page](https://research.nvidia.com/labs/gear/gr00t-2/), accessed 2026-11-25
13. [Hugging Face: nvidia/PhysicalAI-Robotics-GR00T-X-Embodiment-Sim dataset card (CC-BY-4.0)](https://huggingface.co/datasets/nvidia/PhysicalAI-Robotics-GR00T-X-Embodiment-Sim), accessed 2026-11-25
14. [Hugging Face: nvidia/PhysicalAI-Robotics-GR00T-Teleop-Sim dataset card (CC-BY-NC-4.0)](https://huggingface.co/datasets/nvidia/PhysicalAI-Robotics-GR00T-Teleop-Sim), accessed 2026-11-25

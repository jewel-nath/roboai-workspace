---
type: tool
name: RDT (RDT-1B and RDT2)
summary: Tsinghua's Robotics Diffusion Transformer family for bimanual manipulation; RDT-1B (2024, MIT code, weights and data) is a 1B diffusion policy fine-tuned per robot, and RDT2 (2025, Apache-2.0) is a Qwen2.5-VL-7B VLA trained on UMI data that runs zero-shot only on matching UMI hardware. Research code, no releases, issues mostly unanswered.
tags: [rdt, rdt-1b, rdt-170m, rdt2, robotics-diffusion-transformer, diffusion-policy, flow-matching, vla, bimanual, aloha, umi, qwen2.5-vl, siglip, t5, tsinghua]
kind: model
area: learning
support:
license: MIT
links: {repo: "https://github.com/thu-ml/RoboticsDiffusionTransformer", docs: , site: "https://rdt-robotics.github.io/rdt-robotics/"}
version: {tested: , latest: RDT2, as_of: 2026-11-25}
platforms: [linux]
agent_access: script
registry:
evidence: researched
last_verified: 2026-11-25
sources:
  - {url: "https://github.com/thu-ml/RoboticsDiffusionTransformer", title: "RDT-1B repository: README, LICENSE, configs/base.yaml, requirements.txt, history and issues", accessed: 2026-11-25}
  - {url: "https://huggingface.co/robotics-diffusion-transformer/rdt-1b", title: "Hugging Face: robotics-diffusion-transformer/rdt-1b model card", accessed: 2026-11-25}
  - {url: "https://arxiv.org/abs/2410.07864", title: "Liu et al., RDT-1B: a Diffusion Foundation Model for Bimanual Manipulation (ICLR 2025)", accessed: 2026-11-25}
  - {url: "https://github.com/thu-ml/RDT2", title: "RDT2 repository: README, LICENSE, requirements.txt, deploy and examples, history and issues", accessed: 2026-11-25}
  - {url: "https://huggingface.co/robotics-diffusion-transformer/RDT2-FM", title: "Hugging Face: RDT2-FM model card (and RDT2-VQ, RVQActionTokenizer licence fields)", accessed: 2026-11-25}
  - {url: "https://github.com/huggingface/lerobot/tree/main/src/lerobot/policies", title: "LeRobot policies folder (no RDT policy)", accessed: 2026-11-25}
---

# RDT (RDT-1B and RDT2)

Robotics Diffusion Transformers from Tsinghua's TSAIL group, for bimanual arms. **RDT-1B** (ICLR
2025) is a 1B diffusion transformer pre-trained on 1M+ episodes from 46 datasets; from an
instruction, up to three cameras and the robot state it predicts the next 64 actions [1][2][3].
**RDT2** (September 2025) is a Qwen2.5-VL-7B VLA trained on 10,000+ hours of UMI gripper data,
plus a flow-matching action expert, RDT2-FM [4]. **Licences:** RDT-1B code, weights and
fine-tuning data are MIT [1][2]; RDT2 code and weights Apache-2.0 [4][5]. **Quiet:** no releases;
last commits 2026-01-21 and 2026-02-07; most 2026 issues unanswered; no LeRobot port [1][4][6].

## When to use it

- **RDT-1B** to fine-tune for a dual-arm robot, given a large GPU and time: the authors used
  6,000+ own episodes for ALOHA and advise 150K+ steps [1]. RDT-170M (MIT) needs less VRAM [1].
- **RDT2** for zero-shot pick, place and wipe on a bimanual UR5e or Franka FR3 with the authors'
  [UMI](../../robots/umi-gripper.md)-style gripper and camera; other robots need fine-tuning [4].
- **Use something else** for one low-cost arm or a maintained stack: [ACT](../policies/act.md) or
  [SmolVLA](smolvla.md) in [LeRobot](../frameworks/lerobot.md), [pi0](pi0.md), [GR00T](gr00t.md).

## Setup

RDT2 needs Ubuntu 24.04 and a Python 3.10 conda env; RDT-1B pins PyTorch 2.1.0 (CUDA 12.1) [1][4]:

```bash
pip install torch==2.7.1 torchvision==0.22.1 --index-url https://download.pytorch.org/whl/cu128
pip install flash-attn --no-build-isolation && pip install -r requirements.txt   # in RDT2/
```

GPU memory [1][4]: RDT2 inference and RDT2-FM fine-tuning about 16 GB (RTX 4090), 32 GB+ RAM;
RDT2-VQ LoRA 32 GB+ (A100 40 GB), full 80 GB+. None for RDT-1B, whose T5-XXL text encoder may
not fit a 24 GB card. No Jetson figures.

## How an agent works with it

- **RDT-1B:** re-implement `HDF5VLADataset`, add the control rate to `configs/`, run
  `python -m data.compute_dataset_stat_hdf5` and `source finetune.sh` (DeepSpeed, bf16) until
  `overall_avg_sample_mse` converges; deploy via `scripts/agilex_model.py`'s `step()` [1].
- **RDT2:** `RDTInferencer(...).step()` takes two 384 x 384 wrist images and an instruction and
  returns a (24, 20) relative chunk: per arm, position (m), 6D rotation and gripper width, 0.8 s
  at 30 fps [4]. Fine-tuning reads WebDataset shards [4].

## Traps

- **RDT-1B's unified vector.** State and actions fill 128 fixed slots: a single arm goes in the
  right-arm slots, rotations in 6D form, values unnormalised in SI units except gripper width [1].
- **Camera order.** `step()` wants exterior, right wrist, left wrist; previous frame first [1].
- **T5-XXL memory.** Precompute instruction embeddings (`scripts/encode_lang.py`, CPU offload
  under 24 GB) and pass `--precomp_lang_embed` [1].
- **RDT2 zero-shot is hardware-bound:** the designated gripper, a HikRobot camera, printed mounts,
  a tracker-to-TCP calibration; state input is zeros; rescale gripper width 0.088 to 0.1 [4][5].
- **Results are the authors'.** RDT-1B's ManiSkill mean of 53.6% (OpenVLA 4.8%, Octo 0%) comes
  from their own fine-tunes of each baseline on 5,000 trajectories [1].

## Alternatives

[GR00T](gr00t.md), [pi0](pi0.md), [OpenVLA](openvla.md), [Octo](octo.md), [ACT](../policies/act.md).

## Sources

1. [RDT-1B repository: README, LICENSE, configs/base.yaml, requirements.txt, history and issues](https://github.com/thu-ml/RoboticsDiffusionTransformer), accessed 2026-11-25
2. [Hugging Face: robotics-diffusion-transformer/rdt-1b model card](https://huggingface.co/robotics-diffusion-transformer/rdt-1b), accessed 2026-11-25
3. [Liu et al., RDT-1B: a Diffusion Foundation Model for Bimanual Manipulation (ICLR 2025)](https://arxiv.org/abs/2410.07864), accessed 2026-11-25
4. [RDT2 repository: README, LICENSE, requirements.txt, deploy and examples, history and issues](https://github.com/thu-ml/RDT2), accessed 2026-11-25
5. [Hugging Face: RDT2-FM model card (and RDT2-VQ, RVQActionTokenizer licence fields)](https://huggingface.co/robotics-diffusion-transformer/RDT2-FM), accessed 2026-11-25
6. [LeRobot policies folder (no RDT policy)](https://github.com/huggingface/lerobot/tree/main/src/lerobot/policies), accessed 2026-11-25

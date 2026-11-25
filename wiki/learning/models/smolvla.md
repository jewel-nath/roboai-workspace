---
type: tool
name: SmolVLA
summary: Hugging Face's 450M vision-language-action model in LeRobot (SmolVLM2 plus a flow-matching action expert), pretrained on community SO-100 datasets and fine-tuned on about 50 demonstrations; Apache-2.0 code and weights; one GPU trains it (about 4 hours for 20k steps on an A100) and LeRobot's remote inference server runs it off the robot.
tags: [smolvla, lerobot, hugging-face, vla, vision-language-action, smolvlm2, flow-matching, so-100, so-101, lekiwi, low-cost-arm, remote-inference, rtc, apache-2.0]
kind: model
area: learning
support:
license: Apache-2.0
links: {repo: "https://github.com/huggingface/lerobot", docs: "https://huggingface.co/docs/lerobot/smolvla", site: "https://huggingface.co/lerobot/smolvla_base"}
version: {tested: , latest: smolvla_base, as_of: 2026-11-25}
platforms: [linux, macos, windows]
agent_access: script
registry:
evidence: researched
last_verified: 2026-11-25
sources:
  - {url: "https://github.com/huggingface/lerobot", title: "LeRobot repository: LICENSE, docs (smolvla, installation, bring_your_own_policies, simulation), configuration_smolvla.py, tags, history", accessed: 2026-11-25}
  - {url: "https://huggingface.co/lerobot/smolvla_base", title: "Hugging Face model card: lerobot/smolvla_base", accessed: 2026-11-25}
  - {url: "https://arxiv.org/abs/2506.01844", title: "Shukor et al., SmolVLA: A Vision-Language-Action Model for Affordable and Efficient Robotics (arXiv 2506.01844)", accessed: 2026-11-25}
  - {url: "https://huggingface.co/blog/smolvla", title: "Hugging Face blog: SmolVLA, efficient VLA trained on LeRobot community data (2025-06-03)", accessed: 2026-11-25}
  - {url: "https://huggingface.co/datasets/HuggingFaceVLA/community_dataset_v1", title: "Hugging Face dataset card: HuggingFaceVLA/community_dataset_v1", accessed: 2026-11-25}
  - {url: "https://github.com/huggingface/lerobot/blob/main/docs/source/remote_inference.mdx", title: "LeRobot docs: Remote Inference, with the policy support table in src/lerobot/remote_inference/README.md", accessed: 2026-11-25}
---

# SmolVLA

Hugging Face's 450M vision-language-action (VLA) model in [LeRobot](../frameworks/lerobot.md):
SmolVLM2-500M (half its layers) plus a 100M flow-matching action expert [1][4]. From up to three
cameras, the state and an instruction it outputs 50-step action chunks; builders fine-tune
`smolvla_base` on about 50 demonstrations from an arm such as the [SO-101](../../robots/so-101.md)
[1]. HF reports pretraining on 487 community datasets (about 10M frames, mostly SO-100) [4]; the
released `community_dataset_v1` (128 datasets) is Apache-2.0 behind a Hub login [5]. **Code and
weights: Apache-2.0** [1][2]. Maintained: LeRobot 0.7.0 on 2026-11-05, last commit 2026-11-24 [1].

## When to use it

- **Use it** for a language-conditioned policy on a hobby arm (SO-100, SO-101, LeKiwi) with one
  consumer GPU [3][4]. For one task with little data, [ACT](../policies/act.md) from scratch; for
  harder tasks and a large GPU, [π0.5](pi0.md); for humanoids, [GR00T](gr00t.md).

## Setup

```bash
pip install 'lerobot[smolvla]'          # LeRobot 0.7.0, Python 3.12+
lerobot-train --policy.path=lerobot/smolvla_base --dataset.repo_id=$HF_USER/my_dataset \
  --rename_map='{"observation.images.top": "observation.images.camera1",
                 "observation.images.wrist": "observation.images.camera2"}' \
  --policy.repo_id=$HF_USER/my_smolvla --batch_size=64 --steps=20000 --policy.device=cuda
```

20k steps take about 4 hours on one A100 [1]; LeRobot's hardware guide puts training at about 10 to
16 GB (indicative) [1]. Upstream gives no Jetson figure [3][4].
Linux PyTorch wheels are CUDA 13 builds (NVIDIA driver 580.65+); Apple Silicon needs macOS 14 [1].

## How an agent works with it

- **Data:** a LeRobotDataset v3.0 (convert v2.1 with `convert_dataset_v21_to_v30`); about 10
  episodes per variation (25 in all were too few in HF's test). Defaults: images padded to 512 x
  512, state and action to 32 dims, chunks of 50, vision encoder frozen [1].
- **Check, then run:** training loss, `lerobot-eval` in simulation (`lerobot/smolvla_libero`),
  then `lerobot-rollout --policy.path=... --robot.type=so101_follower --rename_map=... --task=...`
  at low speed; `--inference.type=rtc` helps slow GPUs [1].
- **Off-robot GPU:** `lerobot-policy-server` on the GPU machine, `lerobot-rollout
  --inference.type=remote` on the robot, which must hold position while waiting (SO, Koch, OMX do;
  mobile bases do not) [6]. HF claims asynchronous runs finish about 30% faster [4].

## Traps

- **Camera names.** `smolvla_base` expects `camera1` to `camera3`; without `--rename_map` training
  stops on a feature mismatch. Reuse the map, camera resolution and `--task` text at rollout [1].
- **Retired async stack.** The paper's `lerobot[async]` and `lerobot.async_inference` are gone;
  use `lerobot[remote]` and `lerobot-policy-server`, and retune: old thresholds do not carry [6].
- **Silent normalisation errors.** Modes or statistics that differ from training run without
  error but wreck results; keep the checkpoint's processors [1].
- **Authors' results.** HF reports SO-100 success rising from 51.7% to 78.3% with community
  pretraining, in its own tests [4]; other arms and frame rates may gain less.

## Alternatives

[π0](pi0.md), [GR00T](gr00t.md), [OpenVLA](openvla.md), [Octo](octo.md), [ACT](../policies/act.md).

## Sources

1. [LeRobot repository: LICENSE, docs (smolvla, installation, bring_your_own_policies, simulation), configuration_smolvla.py, tags, history](https://github.com/huggingface/lerobot), accessed 2026-11-25
2. [Hugging Face model card: lerobot/smolvla_base](https://huggingface.co/lerobot/smolvla_base), accessed 2026-11-25
3. [Shukor et al., SmolVLA: A Vision-Language-Action Model for Affordable and Efficient Robotics (arXiv 2506.01844)](https://arxiv.org/abs/2506.01844), accessed 2026-11-25
4. [Hugging Face blog: SmolVLA, efficient VLA trained on LeRobot community data (2025-06-03)](https://huggingface.co/blog/smolvla), accessed 2026-11-25
5. [Hugging Face dataset card: HuggingFaceVLA/community_dataset_v1](https://huggingface.co/datasets/HuggingFaceVLA/community_dataset_v1), accessed 2026-11-25
6. [LeRobot docs: Remote Inference, with the policy support table in src/lerobot/remote_inference/README.md](https://github.com/huggingface/lerobot/blob/main/docs/source/remote_inference.mdx), accessed 2026-11-25

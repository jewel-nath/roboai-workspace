---
type: tool
name: π0 family (openpi - π0, π0-FAST, π0.5)
summary: Physical Intelligence's vision-language-action models on a PaliGemma backbone, released in openpi with base and fine-tuned checkpoints plus JAX and PyTorch training; code Apache-2.0, weights under the Gemma Terms of Use; inference needs a GPU with more than 8 GB, LoRA fine-tuning more than 22.5 GB, full fine-tuning more than 70 GB; LeRobot carries a port.
tags: [pi0, pi0-fast, pi05, openpi, physical-intelligence, vla, vision-language-action, flow-matching, fast-tokenizer, paligemma, gemma, lerobot, jax, pytorch, droid, aloha, libero, lora, remote-inference, jetson-thor]
kind: model
area: learning
support:
license: Apache-2.0
links: {repo: "https://github.com/Physical-Intelligence/openpi", docs: "https://github.com/Physical-Intelligence/openpi/tree/main/docs", site: "https://www.pi.website/blog/openpi"}
version: {tested: , latest: pi0.5, as_of: 2026-11-25}
platforms: [linux]
agent_access: script
registry:
evidence: researched
last_verified: 2026-11-25
sources:
  - {url: "https://github.com/Physical-Intelligence/openpi", title: "openpi repository: README, LICENSE, LICENSE_GEMMA.txt, pyproject.toml, docs (norm_stats, remote_inference, docker), model, policy and serving code, history", accessed: 2026-11-25}
  - {url: "https://github.com/Physical-Intelligence/openpi/issues", title: "openpi issues and merged pull requests", accessed: 2026-11-25}
  - {url: "https://arxiv.org/abs/2410.24164", title: "Black et al., π0: A Vision-Language-Action Flow Model for General Robot Control (arXiv 2410.24164)", accessed: 2026-11-25}
  - {url: "https://arxiv.org/abs/2504.16054", title: "Physical Intelligence et al., π0.5: a Vision-Language-Action Model with Open-World Generalization (arXiv 2504.16054)", accessed: 2026-11-25}
  - {url: "https://www.pi.website/blog/pi07", title: "Physical Intelligence: π0.7, a Steerable Model with Emergent Capabilities (blog listing)", accessed: 2026-11-25}
  - {url: "https://huggingface.co/lerobot/pi0_base", title: "Hugging Face model card: lerobot/pi0_base", accessed: 2026-11-25}
  - {url: "https://huggingface.co/lerobot/pi05_base", title: "Hugging Face model card: lerobot/pi05_base", accessed: 2026-11-25}
  - {url: "https://huggingface.co/google/paligemma-3b-pt-224", title: "Hugging Face model card: google/paligemma-3b-pt-224 (gated)", accessed: 2026-11-25}
  - {url: "https://github.com/huggingface/lerobot/tree/main/docs/source", title: "LeRobot repository: docs pi0.mdx, pi0fast.mdx, pi05.mdx, installation.mdx, pyproject.toml, dataset format code, tags", accessed: 2026-11-25}
  - {url: "https://www.jetson-ai-lab.com/tutorials/openpi_on_thor", title: "NVIDIA Jetson AI Lab: OpenPi π0.5 on Jetson Thor", accessed: 2026-11-25}
  - {url: "https://github.com/huggingface/lerobot/blob/main/src/lerobot/remote_inference/README.md", title: "LeRobot remote inference: design notes and policy support table", accessed: 2026-11-25}
  - {url: "https://pypi.org/project/openpi-client/", title: "PyPI: openpi-client", accessed: 2026-11-25}
---

# π0 family (openpi)

Physical Intelligence's vision-language-action (VLA) models: a PaliGemma vision-language model
(`gemma_2b` with SigLIP) plus a 300M action expert that turns camera images, robot state and a
prompt into a 50-step action chunk [1]. π0 and π0.5 generate actions by flow matching; π0-FAST
is autoregressive over FAST action tokens [1][3]. Base checkpoints were pretrained on 10k+ hours
of robot data, π0.5 also on web data and subtask labels [1][4]. Builders fine-tune a base model
on their own demonstrations, or run the DROID and ALOHA checkpoints as they are [1].

**Licences.** The openpi code is Apache-2.0 [1]. The weights are not: the Hub copies are tagged
`gemma` [6][7], openpi ships the Gemma Terms of Use beside its licence [1], and the PaliGemma
tokenizer is a gated download [8]. Those terms allow commercial use, but bind you to Google's
prohibited-use policy and require that anyone you give fine-tuned weights to gets the terms and a
notice file [1]. PI's pretraining data is not in openpi; its examples use LIBERO, DROID, ALOHA [1].
**Status:** no releases; last commit 2026-08-24; 255 open issues, few recent replies [1][2]. Only
π0, π0-FAST and π0.5 are open; PI's π0.7 (blog dated 2026-04-16) has no open release [1][5].

## When to use it

- **Use it** to fine-tune a strong generalist base with a large GPU, best on robots like PI's
  mix (ALOHA, Franka, UR5e, ARX); π0-FAST follows language better than π0 but infers slower [1].
- **Without fine-tuning,** run a checkpoint only on its own robot, the DROID
  [Franka](../../robots/franka-panda.md) setup or ALOHA [1].
- **openpi or LeRobot?** openpi is PI's reference (JAX with LoRA and FSDP, plus PyTorch); the
  [LeRobot](../frameworks/lerobot.md) port (`pi0`, `pi0_fast`, `pi05`) suits current LeRobot
  datasets and arms such as the [SO-101](../../robots/so-101.md) [9].
- **Use something else** for small GPUs ([SmolVLA](smolvla.md), [ACT](../policies/act.md)) or NVIDIA
  humanoids ([GR00T](gr00t.md)); see [the guide](../../guides/choose-a-robot-learning-policy.md).

## Setup

| Mode [1] | GPU memory | Example GPU |
|---|---|---|
| Inference | more than 8 GB | RTX 4090 |
| LoRA fine-tuning | more than 22.5 GB | RTX 4090 |
| Full fine-tuning | more than 70 GB | A100 80 GB, H100 |

Figures are per NVIDIA GPU; `--fsdp-devices` splits memory over GPUs; JAX training is single-node.
Tested on Ubuntu 22.04 only; Docker is upstream's fallback for host problems [1]:

```bash
git clone --recurse-submodules https://github.com/Physical-Intelligence/openpi && cd openpi
GIT_LFS_SKIP_SMUDGE=1 uv sync          # Python 3.11, JAX 0.5.3 (CUDA 12), PyTorch 2.7.1
GIT_LFS_SKIP_SMUDGE=1 uv pip install -e .
uv run scripts/serve_policy.py --env=LIBERO     # serves pi05_libero on port 8000
# or: docker compose -f scripts/docker/compose.yml up --build
```

uv brings the CUDA libraries; system CUDA can conflict. Docker must be rootless with the NVIDIA
Container Toolkit; snap Docker and Docker Desktop cannot reach the GPU. Checkpoints come from
`gs://openpi-assets` into `~/.cache/openpi` [1].

**LeRobot port:** `pip install 'lerobot[pi]'` (LeRobot 0.7.0, Python 3.12+); accept the
PaliGemma licence on the Hub and `hf auth login` [9][8]. Checkpoints: `lerobot/pi0_base`,
`lerobot/pi05_base`, `lerobot/pi0_libero`, `lerobot/pi05_libero_base`. Its π0.5 LIBERO fine-tune
is sized for one 80 GB GPU; `train_expert_only=true` freezes the VLM to save memory (no figure) [9].

**Jetson:** not covered by openpi. NVIDIA's Jetson AI Lab runs π0.5 on Jetson AGX Thor (JetPack
7.2) with its own patches: about 132 ms per call in PyTorch BF16, about 49 ms with TensorRT FP8
plus NVFP4, on `pi05_libero` with a 10-step horizon (NVIDIA's figures) [10].

## How an agent works with it

**Data.** openpi reads LeRobot datasets (see `examples/libero/convert_libero_data_*.py`). Per robot,
write input and output transforms (see `libero_policy.py`) and a `TrainConfig` in `config.py` [1].

**Inputs** [1]: up to three 224 x 224 RGB images in the slots `base_0_rgb`, `left_wrist_0_rgb`
and `right_wrist_0_rgb` (missing ones masked), the state and a prompt. State and actions are
padded to 32 dimensions; π0.5 reads the state as discretised prompt tokens, π0 as a vector [1][9].

**Base-model actions** [1]: joints in radians, grippers 0.0 (open) to 1.0 (closed); dims 0-5 left
arm, 6 its gripper, 7-13 right arm and gripper, 14-15 base velocity (a 7-DoF arm: 0-6, gripper 7).
UR5e and Franka ran at 20 Hz, ARX and ALOHA at 50 Hz; DROID uses joint velocities at 15 Hz.

**Fine-tune and serve** (JAX; logs to Weights & Biases) [1]:

```bash
uv run scripts/compute_norm_stats.py --config-name pi05_libero
XLA_PYTHON_CLIENT_MEM_FRACTION=0.9 uv run scripts/train.py pi05_libero --exp-name=run1 --overwrite
uv run scripts/serve_policy.py policy:checkpoint --policy.config=pi05_libero \
  --policy.dir=checkpoints/pi05_libero/run1/20000
# PyTorch: examples/convert_jax_model_to_pytorch.py, then scripts/train_pytorch.py (or torchrun)
```

**Robot side.** Install `packages/openpi-client` in the robot's environment;
`WebsocketClientPolicy(host, port=8000).infer(obs)["actions"]` returns a (horizon, dims) chunk.
Resize images on the client (`image_tools.resize_with_pad(img, 224, 224)`, uint8) and send the
raw state; the server normalises. Run several steps of each chunk before the next query [1].

**LeRobot:** `lerobot-train --policy.type=pi05 --policy.pretrained_path=lerobot/pi05_base ...`,
then `lerobot-rollout --policy.path=<checkpoint> --robot.type=so101_follower ...` [9]. Its remote
inference server lists π0 and π0.5 as candidates with no hardware acceptance yet [11].

**Check:** the loss falls; [LIBERO](../benchmarks/libero.md) success per LeRobot: 96.85% for PI's
π0.5, 97.5% for its port (its runs) [9]. Then try `examples/simple_client`, then the robot slowly.

## Traps

- **Licence labels disagree.** LeRobot's docs call the models Apache-2.0 [9]; the Hub cards say
  `gemma` [6][7]. Treat weights and fine-tunes as Gemma model derivatives [1].
- **Normalisation.** Training needs `compute_norm_stats` first. A diverging loss often means tiny
  `q01`, `q99` or `std` on a rarely used dimension in `norm_stats.json`; edit them. PI's own
  statistics (`AssetsConfig`, ids such as `trossen`, `franka`, `ur5e`) help only if your data
  follows PI's conventions; try both [1]. In LeRobot, π0.5 needs `q01` and `q99`: run
  `lerobot-edit-dataset --operation.type recompute_stats` or use `MEAN_STD` [9].
- **Two dataset formats.** openpi pins a LeRobot commit of 2025-05-28 that reads format v2.1;
  LeRobot 0.7 records v3.0 and documents conversion only from v2.1 to v3.0 [1][9]. Record with a
  matching LeRobot for openpi, or train with LeRobot's port.
- **Silent convention errors.** An inverted gripper, joints in degrees, a camera in the wrong slot
  or another control rate move the arm wrongly with no error; the ALOHA example remaps joints and
  gripper (`adapt_to_pi`) [1]. Replay a recorded episode through your transforms first.
- **Weights only.** LeRobot's `--policy.pretrained_path` skips the config, so `n_action_steps` and
  `empty_cameras` fall back to 50 and 0; `--policy.path` loads both [9].
- **Separate environments.** openpi pins Python 3.11 and transformers 4.53.2; LeRobot 0.7 needs
  Python 3.12+ and transformers 5.22 [1][9]. openpi's PyTorch path patches files inside
  transformers, which with uv's hardlinks alters the uv cache until `uv cache clean transformers`;
  it lacks π0-FAST, LoRA, FSDP, mixed precision and EMA [1].
- **Out of memory.** JAX takes 75% of GPU memory unless `XLA_PYTHON_CLIENT_MEM_FRACTION` is set [1].
- **An open server.** `serve_policy.py` binds all interfaces with no authentication and no message
  size limit [1]; firewall it. PyPI's `openpi-client` 0.1.2 names no author or project link [12];
  upstream installs the client from the repo [1].
- **Gated and remote code.** LeRobot's π0, π0.5 and π0-FAST read the gated PaliGemma tokenizer;
  π0-FAST also needs `--policy.trust_remote_code=true` for its tokenizer; review and pin it [9][8].
- **No promise for your robot.** PI calls the release an experiment that may not work on other
  robots [1]. Judge it after fine-tuning on your own demonstrations.

## Alternatives

[SmolVLA](smolvla.md), [GR00T](gr00t.md), [OpenVLA](openvla.md), [Octo](octo.md), [RDT](rdt.md);
from scratch, [ACT](../policies/act.md), [Diffusion Policy](../policies/diffusion-policy.md).
Data: [DROID](../datasets/droid.md). Skills:
[learn-robot-learning](../../../skills/learn-robot-learning/SKILL.md),
[learn-edge-deployment](../../../skills/learn-edge-deployment/SKILL.md).

## Sources

1. [openpi repository: README, LICENSE, LICENSE_GEMMA.txt, pyproject.toml, docs (norm_stats, remote_inference, docker), model, policy and serving code, history](https://github.com/Physical-Intelligence/openpi), accessed 2026-11-25
2. [openpi issues and merged pull requests](https://github.com/Physical-Intelligence/openpi/issues), accessed 2026-11-25
3. [Black et al., π0: A Vision-Language-Action Flow Model for General Robot Control (arXiv 2410.24164)](https://arxiv.org/abs/2410.24164), accessed 2026-11-25
4. [Physical Intelligence et al., π0.5: a Vision-Language-Action Model with Open-World Generalization (arXiv 2504.16054)](https://arxiv.org/abs/2504.16054), accessed 2026-11-25
5. [Physical Intelligence: π0.7, a Steerable Model with Emergent Capabilities (blog listing)](https://www.pi.website/blog/pi07), accessed 2026-11-25
6. [Hugging Face model card: lerobot/pi0_base](https://huggingface.co/lerobot/pi0_base), accessed 2026-11-25
7. [Hugging Face model card: lerobot/pi05_base](https://huggingface.co/lerobot/pi05_base), accessed 2026-11-25
8. [Hugging Face model card: google/paligemma-3b-pt-224 (gated)](https://huggingface.co/google/paligemma-3b-pt-224), accessed 2026-11-25
9. [LeRobot repository: docs pi0.mdx, pi0fast.mdx, pi05.mdx, installation.mdx, pyproject.toml, dataset format code, tags](https://github.com/huggingface/lerobot/tree/main/docs/source), accessed 2026-11-25
10. [NVIDIA Jetson AI Lab: OpenPi π0.5 on Jetson Thor](https://www.jetson-ai-lab.com/tutorials/openpi_on_thor), accessed 2026-11-25
11. [LeRobot remote inference: design notes and policy support table](https://github.com/huggingface/lerobot/blob/main/src/lerobot/remote_inference/README.md), accessed 2026-11-25
12. [PyPI: openpi-client](https://pypi.org/project/openpi-client/), accessed 2026-11-25

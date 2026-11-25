---
type: tool
name: OpenVLA (and OpenVLA-OFT)
summary: A 7B open vision-language-action model (Prismatic - DINOv2 and SigLIP with Llama 2) trained on 970k Open X-Embodiment episodes, plus OFT, its faster fine-tuning recipe; MIT code, weights tagged MIT but bound by the Llama 2 Community License; about 15 to 17 GB to run in bf16 (7 GB at 4-bit), 27 GB or more to fine-tune with LoRA; both repos quiet since 2025.
tags: [openvla, openvla-oft, vla, vision-language-action, prismatic, llama-2, dinov2, siglip, open-x-embodiment, rlds, lora, libero, bridgedata, widowx, aloha, baseline]
kind: model
area: learning
support:
license: MIT
links: {repo: "https://github.com/openvla/openvla", docs: "https://github.com/moojink/openvla-oft", site: "https://openvla.github.io/"}
version: {tested: , latest: openvla-7b, as_of: 2026-11-25}
platforms: []
agent_access: script
registry:
evidence: researched
last_verified: 2026-11-25
sources:
  - {url: "https://github.com/openvla/openvla", title: "OpenVLA repository: README, LICENSE, pyproject.toml, vla-scripts, experiments, history", accessed: 2026-11-25}
  - {url: "https://github.com/openvla/openvla/issues", title: "OpenVLA issues", accessed: 2026-11-25}
  - {url: "https://github.com/openvla/openvla/issues/346", title: "OpenVLA issue 346: OpenVLA-7B silently ignores the image on transformers 4.50 and later", accessed: 2026-11-25}
  - {url: "https://huggingface.co/openvla/openvla-7b", title: "Hugging Face model card: openvla/openvla-7b", accessed: 2026-11-25}
  - {url: "https://arxiv.org/abs/2406.09246", title: "Kim et al., OpenVLA: An Open-Source Vision-Language-Action Model (arXiv 2406.09246, v3 HTML)", accessed: 2026-11-25}
  - {url: "https://ai.meta.com/llama/license/", title: "Meta: Llama 2 Community License Agreement", accessed: 2026-11-25}
  - {url: "https://github.com/moojink/openvla-oft", title: "OpenVLA-OFT repository: README, SETUP.md, LIBERO.md, ALOHA.md, LICENSE, prismatic/vla/constants.py, history", accessed: 2026-11-25}
---

# OpenVLA

A 7B vision-language-action (VLA) model on the Prismatic VLM (DINOv2 and SigLIP vision, Llama 2),
trained on 970k Open X-Embodiment episodes; from one 224 x 224 image and an instruction it outputs
a 7-DoF end-effector delta as 256-bin tokens [1][4][5]. It is the common open VLA baseline.
**OpenVLA-OFT**, the authors' later recipe, adds action chunks, continuous actions, wrist images
and state; they claim 25 to 50 times faster inference and higher success [1][7]. **Licences:**
code MIT [1][7]; the Hub tags the weights MIT [4], but the README says they inherit the Llama 2
Community License [1]: a notice file, Meta's use policy, a separate licence above 700 million
monthly users, no improving other LLMs [6]. **Status:** last commit 2025-03-23 (OFT 2025-09-08),
no tags, 101 open issues [1][2][7].

## When to use it

- **Use it** to compare with published VLA results (LIBERO; BridgeData V2 on a WidowX,
  [Interbotix arms](../../robots/interbotix-x-series-arms.md)) or with RLDS data; for a new robot
  use OFT, as the README advises [1][7]. Maintained instead: [π0.5](pi0.md), [SmolVLA](smolvla.md).

## Setup

Inference: `pip install -r requirements-min.txt`, then `transformers`. Full: conda, Python 3.10,
PyTorch 2.2, `pip install -e .`, `flash-attn==2.5.5` (OFT alike) [1][7]. No Jetson figure upstream.

| Task | GPU memory (authors' figures) |
|---|---|
| Inference, bf16 | about 15 GB, 6 Hz on an RTX 4090; 16.8 GB in the quantisation table [5] |
| Inference, int8 / int4 | 10.2 GB / 7.0 GB; int4 matched bf16's success in their tests [5] |
| LoRA / full fine-tuning | about 72 GB at batch 16, about 27 GB with a smaller batch / 8 A100s [1] |
| OFT inference / training | about 16 GB (LIBERO), 18 GB (ALOHA) / 1 to 8 GPUs of 27 to 80 GB [7] |

## How an agent works with it

Load `openvla/openvla-7b` with `AutoModelForVision2Seq` (`trust_remote_code=True`, bf16), give it
the README's `In: What action should the robot take to ...? Out:` prompt and an image, then call
`vla.predict_action(**inputs, unnorm_key="bridge_orig")`. Fine-tune: convert demonstrations to
RLDS, register them in `configs.py` and `transforms.py`, run `vla-scripts/finetune.py` (LoRA rank
32) with `torchrun`; `deploy.py` serves over REST; `run_libero_eval.py` checks it in LIBERO [1].

## Traps

- **Llama 2 terms despite the MIT tag** cover the weights and your fine-tunes [1][6].
- **Image silently ignored** on `transformers` 4.50+: the same action for any image (issue 346) [3].
  Keep the README pins (`transformers` 4.40.1, `timm` 0.9.10); test black vs white frames [1][3].
- **No zero-shot on a new robot.** Actions are normalised per dataset; choose the right
  `unnorm_key` and fine-tune for your arm and cameras [4].
- **Test on the training GPU.** OFT warns success may drop sharply on another GPU; merge the LoRA
  weights on the test machine (`merge_lora_weights_and_save.py`) [7].
- **OFT guesses the robot from the command line:** `libero`, `aloha` or `bridge` in the arguments
  sets chunk and action sizes (default LIBERO: 8 steps, 7 dims); add yours in `constants.py` [7].

## Alternatives

[π0](pi0.md), [SmolVLA](smolvla.md), [Octo](octo.md), [RT-2](rt-2.md), [GR00T](gr00t.md);
[Open X-Embodiment](../datasets/open-x-embodiment.md); [LIBERO](../benchmarks/libero.md).

## Sources

1. [OpenVLA repository: README, LICENSE, pyproject.toml, vla-scripts, experiments, history](https://github.com/openvla/openvla), accessed 2026-11-25
2. [OpenVLA issues](https://github.com/openvla/openvla/issues), accessed 2026-11-25
3. [OpenVLA issue 346: OpenVLA-7B silently ignores the image on transformers 4.50 and later](https://github.com/openvla/openvla/issues/346), accessed 2026-11-25
4. [Hugging Face model card: openvla/openvla-7b](https://huggingface.co/openvla/openvla-7b), accessed 2026-11-25
5. [Kim et al., OpenVLA: An Open-Source Vision-Language-Action Model (arXiv 2406.09246, v3 HTML)](https://arxiv.org/abs/2406.09246), accessed 2026-11-25
6. [Meta: Llama 2 Community License Agreement](https://ai.meta.com/llama/license/), accessed 2026-11-25
7. [OpenVLA-OFT repository: README, SETUP.md, LIBERO.md, ALOHA.md, LICENSE, prismatic/vla/constants.py, history](https://github.com/moojink/openvla-oft), accessed 2026-11-25

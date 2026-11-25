---
type: tool
name: Octo
summary: An open generalist robot policy (transformer with a diffusion action head; Octo-Small 27M and Octo-Base 93M, version 1.5) pretrained on 800k Open X-Embodiment trajectories and fine-tuned in JAX in about 5 hours on one 24 GB GPU; MIT code and weights; unmaintained since July 2024 and its README install now breaks, so it is a historical baseline - use SmolVLA, π0.5 or OpenVLA-OFT for new work.
tags: [octo, generalist-robot-policy, diffusion-policy, transformer, open-x-embodiment, rlds, jax, flax, goal-image, language-conditioned, widowx, baseline, unmaintained]
kind: model
area: learning
support:
license: MIT
links: {repo: "https://github.com/octo-models/octo", docs: "https://github.com/octo-models/octo/tree/main/examples", site: "https://octo-models.github.io/"}
version: {tested: , latest: v1.5, as_of: 2026-11-25}
platforms: []
agent_access: script
registry:
evidence: researched
last_verified: 2026-11-25
sources:
  - {url: "https://github.com/octo-models/octo", title: "Octo repository: README, LICENSE, requirements.txt, examples, octo_model.py, gym_wrappers.py, finetune config, tags, history", accessed: 2026-11-25}
  - {url: "https://github.com/octo-models/octo/issues", title: "Octo issues", accessed: 2026-11-25}
  - {url: "https://github.com/octo-models/octo/issues/174", title: "Octo issue 174: scipy.linalg has no attribute tril after installation", accessed: 2026-11-25}
  - {url: "https://github.com/octo-models/octo/issues/176", title: "Octo issue 176: arbitrary callables loaded from a checkpoint config", accessed: 2026-11-25}
  - {url: "https://docs.scipy.org/doc/scipy/release/1.13.0-notes.html", title: "SciPy 1.13.0 release notes (scipy.linalg.tri, triu, tril removed)", accessed: 2026-11-25}
  - {url: "https://huggingface.co/rail-berkeley/octo-base-1.5", title: "Hugging Face model card: rail-berkeley/octo-base-1.5", accessed: 2026-11-25}
  - {url: "https://arxiv.org/abs/2405.12213", title: "Octo Model Team, Octo: An Open-Source Generalist Robot Policy (arXiv 2405.12213, v2 HTML)", accessed: 2026-11-25}
---

# Octo

An open generalist robot policy: a transformer over image and language tokens with a diffusion
action head, pretrained on 800k trajectories from 25 Open X-Embodiment datasets [7][6]. It takes a
primary (256 x 256) and a wrist (128 x 128) image over a 2-step history, plus a language
instruction or a goal image, and predicts 4 future 7-dimensional actions [6][1]. Sizes: Octo-Small
(27M) and Octo-Base (93M), version 1.5 on the Hub; **code and weights MIT** [1][6].
**Unmaintained.** Last commit 2024-07-30 (tags v0.1.0, v1.5); 89 issues are open, the newest
without replies; the README install now fails on import [1][2][3]. It stays here as a much-cited
baseline and an early open generalist policy. For new work use [SmolVLA](smolvla.md) or
[π0.5](pi0.md) in [LeRobot](../frameworks/lerobot.md), or [OpenVLA](openvla.md) with OFT.

## When to use it

- **Use it** to reproduce papers that report Octo (its own tests used 9 robot setups), or to study
  its modular heads, which take new observations and action spaces by fine-tuning [1][7]. For a
  robot you want working, fine-tune one of the maintained models above.

## Setup

```bash
conda create -n octo python=3.10 && conda activate octo
pip install -e . && pip install -r requirements.txt
pip install --upgrade "jax[cuda11_pip]==0.4.20" \
  -f https://storage.googleapis.com/jax-releases/jax_cuda_releases.html
python scripts/finetune.py --config.pretrained_path=hf://rail-berkeley/octo-small-1.5 --debug
```

An old stack: JAX 0.4.20 (CUDA 11 wheels), Flax 0.7.5, TensorFlow 2.15 [1]. Fine-tuning took about
5 hours on one 24 GB A5000 (50k steps, about 100 demonstrations) [7]; inference runs 13 (Base) and
17 (Small) times a second on an RTX 4090; no memory or Jetson figure upstream [1][6].

## How an agent works with it

`OctoModel.load_pretrained(...)`, `model.create_tasks(texts=[...])`, then `model.sample_actions(obs,
task, unnormalization_statistics=..., rng=...)`. Fine-tune on RLDS data with `scripts/finetune.py`
(`head_only`, `head_mlp_only` or `full`). Wrap the robot as a Gym env with `HistoryWrapper` plus
`RHCWrapper` or `TemporalEnsembleWrapper`; `examples/03_eval_finetuned.py` runs a rollout [1].

## Traps

- **Install breaks** on `scipy.linalg.tril`: SciPy has no upper pin, and 1.13 removed the function
  JAX 0.4.20 calls [1][3][5]. Pinning SciPy below 1.13 should help (untested here).
- **Checkpoints run code.** `load_pretrained` imports and calls whatever a checkpoint's
  `config.json` names (open report); load trusted checkpoints only, after reading that file [4].
- **Wrong action scale.** Pretrained models key statistics by dataset
  (`dataset_statistics["bridge_dataset"]["action"]`), fine-tuned ones at the top level [1].
- **History mask.** On the first step of the 2-step window set `timestep_pad_mask` False for the
  missing frame; `HistoryWrapper` does it [1].

## Alternatives

[SmolVLA](smolvla.md), [π0](pi0.md), [OpenVLA](openvla.md), [RDT](rdt.md),
[Diffusion Policy](../policies/diffusion-policy.md); data: [OXE](../datasets/open-x-embodiment.md).

## Sources

1. [Octo repository: README, LICENSE, requirements.txt, examples, octo_model.py, gym_wrappers.py, finetune config, tags, history](https://github.com/octo-models/octo), accessed 2026-11-25
2. [Octo issues](https://github.com/octo-models/octo/issues), accessed 2026-11-25
3. [Octo issue 174: scipy.linalg has no attribute tril after installation](https://github.com/octo-models/octo/issues/174), accessed 2026-11-25
4. [Octo issue 176: arbitrary callables loaded from a checkpoint config](https://github.com/octo-models/octo/issues/176), accessed 2026-11-25
5. [SciPy 1.13.0 release notes (scipy.linalg.tri, triu, tril removed)](https://docs.scipy.org/doc/scipy/release/1.13.0-notes.html), accessed 2026-11-25
6. [Hugging Face model card: rail-berkeley/octo-base-1.5](https://huggingface.co/rail-berkeley/octo-base-1.5), accessed 2026-11-25
7. [Octo Model Team, Octo: An Open-Source Generalist Robot Policy (arXiv 2405.12213, v2 HTML)](https://arxiv.org/abs/2405.12213), accessed 2026-11-25

---
type: tool
name: RT-2 (Robotics Transformer 2)
summary: Google DeepMind's 2023 model that named the vision-language-action (VLA) idea - a web-scale vision-language model co-fine-tuned to emit robot actions as text tokens; code and weights were never released and it ran as a cloud TPU service at 1 to 5 Hz, so builders use open VLAs that follow the recipe, such as OpenVLA, pi0, SmolVLA or GR00T.
tags: [rt-2, rt-2-x, robotics-transformer, vla, vision-language-action, google, deepmind, pali-x, palm-e, action-tokens, closed, historical, gemini-robotics]
kind: model
area: learning
support:
license:
links: {repo: , docs: , site: "https://robotics-transformer2.github.io/"}
version: {tested: , latest: , as_of: 2026-11-25}
platforms: []
agent_access:
registry:
evidence: researched
last_verified: 2026-11-25
sources:
  - {url: "https://robotics-transformer2.github.io/", title: "RT-2 project page", accessed: 2026-11-25}
  - {url: "https://arxiv.org/abs/2307.15818", title: "Brohan et al., RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control (arXiv, 2023-07-28)", accessed: 2026-11-25}
  - {url: "https://deepmind.google/discover/blog/rt-2-new-model-translates-vision-and-language-into-action/", title: "Google DeepMind blog: RT-2, new model translates vision and language into action (2023-07-28)", accessed: 2026-11-25}
  - {url: "https://arxiv.org/abs/2406.09246", title: "Kim et al., OpenVLA: An Open-Source Vision-Language-Action Model (arXiv, 2024)", accessed: 2026-11-25}
  - {url: "https://github.com/google-deepmind/open_x_embodiment", title: "Open X-Embodiment repository: README (only RT-1-X checkpoints released)", accessed: 2026-11-25}
  - {url: "https://deepmind.google/models/gemini-robotics/", title: "Google DeepMind: Gemini Robotics models and access", accessed: 2026-11-25}
---

# RT-2 (Robotics Transformer 2)

**Never released.** RT-2 (July 2023) is the Google DeepMind model that introduced the term
vision-language-action (VLA) model: a large vision-language model, co-fine-tuned on robot
trajectories and web vision-language data, that writes robot actions as text tokens [2]. It ran
only inside Google, on the RT-1 data and robots [2]. No code or weights were published; the
project page makes no release statement, the Open X-Embodiment release holds only RT-1-X
checkpoints, and the OpenVLA authors call its successor RT-2-X closed-source [1][4][5]. It earns a
card because most open VLAs follow its recipe. **Use instead:** [OpenVLA](openvla.md) for the same
recipe in the open, or [pi0](pi0.md), [SmolVLA](smolvla.md) or [GR00T](gr00t.md).

## When to use it

- **To understand VLAs and read their papers.** RT-2 is the reference point most VLA papers
  compare against or build on; nothing here can be run.
- **Not for a robot.** There are no weights, and the models were far too large for a robot: the
  55B version ran as a multi-TPU cloud service at about 1 to 3 Hz, the 5B version at about 5 Hz [2].

## Setup

None: no code, no weights, no package [1][4][5].

## How an agent works with it

The idea, which open models reuse [2][4]:

- **Backbones:** PaLI-X (55B) and PaLM-E (12B), both Google vision-language models [1][2].
- **Actions as tokens:** each action is 8 integers: a 6-DoF end-effector displacement, gripper
  extension and a terminate flag. Continuous values fall into 256 uniform bins. PaLI-X reuses its
  number tokens; PaLM-E overwrites its 256 least-used tokens [2].
- **Co-fine-tuning:** robot data is about half the training mix for PaLI-X and two thirds for
  PaLM-E; the rest is web captioning and question answering, which keeps the model's web
  knowledge [2].
- **Open follower:** OpenVLA (7B, Llama 2 with DINOv2 and SigLIP) uses the same 256-bin
  tokenisation, with quantile bin edges instead of min-max, and its authors report 16.5 points
  higher success than RT-2-X across 29 tasks [4]. Later models such as [pi0](pi0.md),
  [SmolVLA](smolvla.md) and [GR00T](gr00t.md) keep the VLM backbone but predict continuous
  actions with a separate action head; see their pages.

## Traps

- **Results are Google's.** The 62% against RT-1's 32% on unseen scenarios, and about 3x on
  emergent skills, come from the authors' own 6,000 trials on their own robots [1][2][3].
- **RT-2-X is closed too.** The 55B Open X-Embodiment version has no public weights either, so
  no one outside Google can rerun a comparison against it [4][5].
- **Google's current robot models are not open either.** The Gemini Robotics page offers no
  weights: access is a trusted-tester waitlist, and only Gemini Robotics ER 2, a reasoning model
  rather than a VLA, is a preview in Google AI Studio [6].

## Alternatives

[OpenVLA](openvla.md), [Octo](octo.md), [pi0](pi0.md), [SmolVLA](smolvla.md), [GR00T](gr00t.md),
[RT-1](rt-1.md) (released, archived).

## Sources

1. [RT-2 project page](https://robotics-transformer2.github.io/), accessed 2026-11-25
2. [Brohan et al., RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control (arXiv, 2023-07-28)](https://arxiv.org/abs/2307.15818), accessed 2026-11-25
3. [Google DeepMind blog: RT-2, new model translates vision and language into action (2023-07-28)](https://deepmind.google/discover/blog/rt-2-new-model-translates-vision-and-language-into-action/), accessed 2026-11-25
4. [Kim et al., OpenVLA: An Open-Source Vision-Language-Action Model (arXiv, 2024)](https://arxiv.org/abs/2406.09246), accessed 2026-11-25
5. [Open X-Embodiment repository: README (only RT-1-X checkpoints released)](https://github.com/google-deepmind/open_x_embodiment), accessed 2026-11-25
6. [Google DeepMind: Gemini Robotics models and access](https://deepmind.google/models/gemini-robotics/), accessed 2026-11-25

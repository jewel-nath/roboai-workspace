---
type: tool
name: CALVIN
summary: Freiburg's PyBullet benchmark for language-conditioned, long-horizon manipulation - a Franka Panda at a desk in four environment variants, 24 hours of play data and chains of five instructions scored by average length; MIT code, but no code changes since early 2024 and datasets of 166 to 656 GB on one HTTP server.
tags: [calvin, benchmark, simulation, language-conditioned, long-horizon, imitation-learning, play-data, pybullet, franka, vla, hulc, multi-task]
kind: framework
area: learning
support:
license: MIT
links: {repo: "https://github.com/mees/calvin", docs: , site: "http://calvin.cs.uni-freiburg.de/"}
version: {tested: , latest: , as_of: 2026-11-25}
platforms: [linux]
agent_access: script
registry:
evidence: researched
last_verified: 2026-11-25
sources:
  - {url: "https://github.com/mees/calvin", title: "CALVIN repository: README, LICENSE, install.sh, dataset/README.md, evaluate_policy.py, requirements, history, issues", accessed: 2026-11-25}
  - {url: "https://github.com/mees/calvin_env", title: "calvin_env repository: LICENSE, requirements.txt, history", accessed: 2026-11-25}
  - {url: "https://ar5iv.labs.arxiv.org/html/2112.03227", title: "CALVIN: A Benchmark for Language-Conditioned Policy Learning for Long-Horizon Robot Manipulation Tasks (paper)", accessed: 2026-11-25}
  - {url: "http://calvin.cs.uni-freiburg.de/", title: "CALVIN website: leaderboard and code licence note", accessed: 2026-11-25}
---

# CALVIN

CALVIN is a [PyBullet](../../tools/pybullet.md) benchmark from the University of Freiburg: a
7-DoF [Franka Panda](../../robots/franka-panda.md) at a desk with a drawer, sliding door, button,
switch and blocks, in four variants (A to D) that differ in textures and furniture positions [3].
It ships 24 hours of teleoperated "play" data, 1% of it labelled with language, and 34 tasks [3].
Builders use it to test policies that follow several text instructions in a row. Code is MIT
(both repos), and the site calls it "for academic usage"; no separate data licence is stated
[1][2][4]. **Unmaintained:** the last code change was 2024-02-08, later commits only list papers,
`calvin_env` stopped in December 2022, and recent issues get no reply [1][2].

## When to use it

- **Use it** to compare a language-conditioned policy with the many published on its leaderboard,
  and to test a new environment zero-shot (train on A, B, C, test on D) [1][4].
- **Use something else** for VLA fine-tuning comparisons ([LIBERO](libero.md)), real-robot-matched
  scores ([SimplerEnv](simpler-env.md)) or a maintained simulator ([RoboCasa](robocasa.md)).

## Setup

```bash
git clone --recurse-submodules https://github.com/mees/calvin.git && cd calvin
conda create -n calvin_venv python=3.8 && conda activate calvin_venv
sh install.sh
cd dataset && sh download_data.sh debug     # 1.3 GB; D is 166 GB, ABC 517 GB, ABCD 656 GB
```

The training code pins PyTorch 1.13.1 and PyTorch Lightning 1.8.6 [1]. Rendering uses EGL on the
GPU so rollouts can run during training [1]; no GPU memory figure is given.

## How an agent works with it

- **In and out** [1]: static RGB 200 x 200 and gripper RGB 84 x 84 (each with depth), tactile and
  15-D proprioception; actions are absolute or relative pose (7-D) or joints (8-D) at 30 Hz.
- **Data:** one NumPy file per step; language in `lang_annotations/auto_lang_ann.npy` with
  precomputed MiniLM embeddings [1].
- **Evaluate:** implement `CustomModel` (`reset()`, `step(obs, goal)`) in
  `evaluation/evaluate_policy.py` and run it with `--custom_model` [1]. It plays 1,000 chains of
  five instructions, with up to 360 steps per instruction [1][3].
- **Score:** success rates for 1 to 5 instructions in a row and the average chain length (0 to 5)
  [4]. Leaderboard figures are the authors' own: on ABC to D, FLOWER reports 4.53, UniVLA 4.41 [4].

## Traps

- **GPU and CPU renders differ.** EGL changes textures slightly, so a model trained on one may
  drop on the other [1]. Old PyBullet cannot choose the EGL GPU, which piles rollouts onto one
  card and runs out of memory; `calvin_env` maps CUDA to EGL device ids [1].
- **Old dataset bugs.** ABC and ABCD downloads before 2022-09-16 had wrong language annotations
  and `scene_info.npy`; D's `scene_info.npy` was replaced on 2023-02-24 [1]. Check the checksums.
- **One slow server.** Data and weights come over plain HTTP from Freiburg (HTTPS was refused on
  2026-11-25); issues report slow and refused downloads [1][4]. Start with the debug set.
- **Compare like with like.** Report the split (D, ABC or ABCD to D), the cameras used and the
  average length on the long-horizon protocol; single-task (MTLC) rates are another number [1][4].
- **Ageing stack.** Python 3.8; `pyhash` fails with setuptools 58 or newer, so downgrade it [1].

## Alternatives

[LIBERO](libero.md), [RLBench](rlbench.md), [SimplerEnv](simpler-env.md), [RoboCasa](robocasa.md);
[Choose a robot learning policy](../../guides/choose-a-robot-learning-policy.md).

## Sources

1. [CALVIN repository: README, LICENSE, install.sh, dataset/README.md, evaluate_policy.py, requirements, history, issues](https://github.com/mees/calvin), accessed 2026-11-25
2. [calvin_env repository: LICENSE, requirements.txt, history](https://github.com/mees/calvin_env), accessed 2026-11-25
3. [CALVIN: A Benchmark for Language-Conditioned Policy Learning for Long-Horizon Robot Manipulation Tasks (paper)](https://ar5iv.labs.arxiv.org/html/2112.03227), accessed 2026-11-25
4. [CALVIN website: leaderboard and code licence note](http://calvin.cs.uni-freiburg.de/), accessed 2026-11-25

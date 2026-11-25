---
type: tool
name: LIBERO
summary: UT Austin's 130-task simulated manipulation benchmark for a Franka Panda in robosuite and MuJoCo, with language instructions and human demonstrations; the usual place to fine-tune and compare VLAs. Code MIT, data CC BY 4.0 (the Hugging Face card says Apache-2.0); the original repo is quiet since March 2025 and Hugging Face's hf-libero fork is the maintained install.
tags: [libero, benchmark, simulation, manipulation, vla, imitation-learning, lifelong-learning, robosuite, mujoco, franka, language-conditioned, lerobot, libero-plus]
kind: framework
area: learning
support:
license: MIT
links: {repo: "https://github.com/Lifelong-Robot-Learning/LIBERO", docs: "https://lifelong-robot-learning.github.io/LIBERO/", site: "https://libero-project.github.io"}
version: {tested: , latest: , as_of: 2026-11-25}
platforms: [linux]
agent_access: script
registry:
evidence: researched
last_verified: 2026-11-25
sources:
  - {url: "https://github.com/Lifelong-Robot-Learning/LIBERO", title: "LIBERO repository: README, LICENSE, setup.py, requirements.txt, env_wrapper.py, eval config, history, issues", accessed: 2026-11-25}
  - {url: "https://huggingface.co/datasets/yifengzhu-hf/LIBERO-datasets", title: "Hugging Face dataset card: yifengzhu-hf/LIBERO-datasets", accessed: 2026-11-25}
  - {url: "https://huggingface.co/docs/lerobot/libero", title: "LeRobot docs: LIBERO", accessed: 2026-11-25}
  - {url: "https://github.com/huggingface/LIBERO", title: "Hugging Face LIBERO fork (hf-libero): README, pyproject.toml, history, tag v0.1.5", accessed: 2026-11-25}
  - {url: "https://github.com/openvla/openvla", title: "OpenVLA repository: README LIBERO section, run_libero_eval.py, libero_utils.py, regenerate_libero_dataset.py", accessed: 2026-11-25}
  - {url: "https://huggingface.co/docs/lerobot/libero_plus", title: "LeRobot docs: LIBERO-plus", accessed: 2026-11-25}
---

# LIBERO

LIBERO gives a simulated [Franka Panda](../../robots/franka-panda.md) in
[robosuite](../frameworks/robosuite.md) and MuJoCo 130 language-specified tasks in kitchen,
living-room and study scenes, with human teleoperated demonstrations [1]. Builders use it to
fine-tune and compare VLAs before using a real arm. **Licences:** code MIT; datasets CC BY 4.0
per the README [1]. The original repo's last commit was 2025-03-15, with no tags; LeRobot
installs Hugging Face's fork, `hf-libero` 0.1.5 (2026-11-16) [1][3][4].

## When to use it

- **Use it** to compare with published numbers: OpenVLA's authors report
  [OpenVLA](../models/openvla.md), Octo and [Diffusion Policy](../policies/diffusion-policy.md);
  LeRobot re-ran [pi0.5](../models/pi0.md) [3][5]. LIBERO-plus perturbs camera, light, layout,
  language and noise into about 10,000 variants [6].
- **Use something else** for other robots or scenes: [SimplerEnv](simpler-env.md) (Google Robot,
  WidowX), [RoboCasa](robocasa.md) (mobile kitchen), [CALVIN](calvin.md) (chained instructions).

## Setup

```bash
pip install -e ".[libero]"   # in a LeRobot clone, Linux only; pulls hf-libero and robosuite 1.4.0
export MUJOCO_GL=egl         # headless rendering
lerobot-eval --policy.path=<policy> --env.type=libero \
  --env.task=libero_spatial,libero_object,libero_goal,libero_10 --eval.n_episodes=10
```

The original README wants Python 3.8.13 and PyTorch 1.11 (CUDA 11.3); its HDF5 demos are about
100 GB [1][2]. No GPU figure upstream: the sim needs only EGL, and training cost is the policy's
(LeRobot's pi0.5 fine-tune used 8 H100s) [3].

## How an agent works with it

- **Suites:** `libero_spatial`, `libero_object`, `libero_goal` and `libero_10` (Long), 10 tasks
  each, plus `libero_90` for pretraining; each task has fixed initial states [1][3].
- **Interface:** agent-view and wrist images, 8-D state, and a 7-D action (end-effector delta,
  gripper) in [-1, 1] at 20 Hz; 128 x 128 renders by default, 256 x 256 in LeRobot's data [1][3].
- **Score:** the success rate, +1 when the goal holds [1]; `lerobot-eval` adds a 95% interval [3].

## Traps

- **Upside-down images.** OpenVLA rotates frames 180 degrees in its data and at eval
  (`img[::-1, ::-1]`) [5]. Training and evaluation must match; look at one frame of each.
- **Different protocols.** OpenVLA runs 50 rollouts per task over 3 seeds, LeRobot 10 [3][5];
  step limits, `relative` or `absolute` control and dataset revision also move scores. Report all.
- **Saturated scores.** pi0.5 scores 96.85% (OpenPI) and 97.5% (LeRobot's re-run); at 10
  episodes, 9/10 spans 60 to 98% [3]. A few points mean little, and none of it predicts a real arm.
- **Pinned stack.** robosuite 1.4.0 and MuJoCo below 3.9 [4]; RoboCasa needs robosuite's master,
  and LIBERO-plus replaces the `libero` package [6]. Use separate environments.
- **Data licence and variants.** HF card Apache-2.0 against README CC BY 4.0, unanswered in issue
  150 [1][2]. OpenVLA's `modified_libero_rlds` drops no-ops and failed demos [5]; name your data.

## Alternatives

[RLBench](rlbench.md), [BEHAVIOR-1K](behavior-1k.md), [LeRobot](../frameworks/lerobot.md);
[Choose a robot learning policy](../../guides/choose-a-robot-learning-policy.md).

## Sources

1. [LIBERO repository: README, LICENSE, setup.py, requirements.txt, env_wrapper.py, eval config, history, issues](https://github.com/Lifelong-Robot-Learning/LIBERO), accessed 2026-11-25
2. [Hugging Face dataset card: yifengzhu-hf/LIBERO-datasets](https://huggingface.co/datasets/yifengzhu-hf/LIBERO-datasets), accessed 2026-11-25
3. [LeRobot docs: LIBERO](https://huggingface.co/docs/lerobot/libero), accessed 2026-11-25
4. [Hugging Face LIBERO fork (hf-libero): README, pyproject.toml, history, tag v0.1.5](https://github.com/huggingface/LIBERO), accessed 2026-11-25
5. [OpenVLA repository: README LIBERO section, run_libero_eval.py, libero_utils.py, regenerate_libero_dataset.py](https://github.com/openvla/openvla), accessed 2026-11-25
6. [LeRobot docs: LIBERO-plus](https://huggingface.co/docs/lerobot/libero_plus), accessed 2026-11-25

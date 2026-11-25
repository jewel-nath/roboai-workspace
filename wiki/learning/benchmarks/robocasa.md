---
type: tool
name: RoboCasa (RoboCasa365)
summary: UT Austin's kitchen simulation on robosuite and MuJoCo - 365 tasks, 2,500+ kitchens, 3,200+ objects and over 2,000 hours of demonstrations for a Franka arm on a mobile base - to train and benchmark generalist policies; code MIT, assets and datasets CC BY 4.0, actively maintained, with a public leaderboard.
tags: [robocasa, robocasa365, benchmark, simulation, kitchen, mobile-manipulation, robosuite, mujoco, mimicgen, lerobot, gr00t, pi0, leaderboard, generalist-policy]
kind: framework
area: learning
support:
license: MIT
links: {repo: "https://github.com/robocasa/robocasa", docs: "https://robocasa.ai/docs/build/html/introduction/overview.html", site: "https://robocasa.ai"}
version: {tested: , latest: 1.0.1, as_of: 2026-11-25}
platforms: [linux, macos, windows]
agent_access: script
registry:
evidence: researched
last_verified: 2026-11-25
sources:
  - {url: "https://github.com/robocasa/robocasa", title: "RoboCasa repository: README, LICENSE, setup.py, kitchen.py, env_utils.py, download scripts, tags, history", accessed: 2026-11-25}
  - {url: "https://robocasa.ai/docs/build/html/benchmarking/benchmarking_overview.html", title: "RoboCasa docs: Benchmarking overview", accessed: 2026-11-25}
  - {url: "https://robocasa.ai/docs/build/html/datasets/datasets_overview.html", title: "RoboCasa docs: Datasets overview", accessed: 2026-11-25}
  - {url: "https://robocasa.ai/docs/build/html/datasets/using_datasets.html", title: "RoboCasa docs: Using datasets", accessed: 2026-11-25}
  - {url: "https://robocasa.ai/leaderboard.html", title: "RoboCasa365 leaderboard", accessed: 2026-11-25}
  - {url: "https://huggingface.co/docs/lerobot/robocasa", title: "LeRobot docs: RoboCasa365", accessed: 2026-11-25}
---

# RoboCasa (RoboCasa365)

RoboCasa is UT Austin's kitchen simulation on [robosuite](../frameworks/robosuite.md) and
[MuJoCo](../../tools/mujoco.md). RoboCasa365 (v1.0, 2026-02-18) has 365 tasks, 2,500+ kitchens,
3,200+ objects, 600+ hours of human and 1,600+ hours of generated demonstrations [1]. Its default
robot, PandaOmron, is a [Franka](../../robots/franka-panda.md) arm on a holonomic base [6].
Builders use it to train generalist mobile-manipulation policies. **Licences:** code MIT; assets
and datasets CC BY 4.0 [1]. Active: last commit 2026-11-18; tags v0.2 and v1.0, plus v1.0.1
(2026-05-12) in the README and `setup.py` [1].

## When to use it

- **Use it** to train multi-task or foundation models on a mobile arm and test unseen tasks [3].
- **Use something else** for published VLA numbers on a fixed arm ([LIBERO](libero.md)) or for
  multi-room tasks ([BEHAVIOR-1K](behavior-1k.md)).

## Setup

```bash
conda create -c conda-forge -n robocasa python=3.11 && conda activate robocasa
git clone https://github.com/ARISE-Initiative/robosuite && pip install -e robosuite  # master
git clone https://github.com/robocasa/robocasa && pip install -e robocasa
python -m robocasa.scripts.setup_macros
python -m robocasa.scripts.download_kitchen_assets    # about 10 GB
```

The README claims all major platforms (macOS uses `mjpython`) and gives no GPU or memory figure
[1]. `robocasa.scripts.download_datasets` fetches LeRobot-format data from UT Austin's Box [1][4]:
482 h human and 1,615 h MimicGen pretraining data, 193 h target data, no size in GB given [3].

## How an agent works with it

- `gym.make("robocasa/PickPlaceCounterToCabinet", split="target", seed=0)`, at 20 Hz [1]. Cameras
  `robot0_agentview_left`, `robot0_agentview_right`, `robot0_eye_in_hand` [4]; LeRobot gives
  256 x 256 images, a 16-D state and a 12-D action (base 4, mode 1, end effector 6, gripper 1) [6].
- **Score:** average binary success over 50 rollouts per task [2], in 10 held-out kitchens with
  Atomic-Seen (18 tasks), Composite-Seen (16) and Composite-Unseen (16) [3].
- **Leaderboard** (reviewed pull requests, pretraining kitchens) [5]: pi0 14.8, pi0.5 16.9,
  GR00T N1.5 23.9; the top entry, an agentic harness, 85.6 on 2026-11-25.

## Traps

- **`lerobot==0.3.3` pin.** RoboCasa's `setup.py` pins it, breaking a newer
  [LeRobot](../frameworks/lerobot.md), which installs RoboCasa with `--no-deps` instead [1][6].
- **robosuite from master**, unpinned [1]; [LIBERO](libero.md) needs 1.4.0. Use separate envs.
- **Longer horizons since v1.0.1.** All horizons grew 1.5 times on 2026-05-12; older scores are
  not comparable [1][2].
- **Protocols differ.** Upstream runs 50 rollouts per task [2], LeRobot recommends 20 [6], and the
  leaderboard uses pretraining kitchens [5]. State which.
- **Silent camera swaps, missing assets.** Swapped camera keys pass unnoticed (same shapes);
  without the Objaverse pack, sample only `lightwheel` objects or env creation fails on NaNs [6].

## Alternatives

[LIBERO](libero.md), [BEHAVIOR-1K](behavior-1k.md), [SimplerEnv](simpler-env.md),
[robomimic](../frameworks/robomimic.md), [GR00T](../models/gr00t.md).

## Sources

1. [RoboCasa repository: README, LICENSE, setup.py, kitchen.py, env_utils.py, download scripts, tags, history](https://github.com/robocasa/robocasa), accessed 2026-11-25
2. [RoboCasa docs: Benchmarking overview](https://robocasa.ai/docs/build/html/benchmarking/benchmarking_overview.html), accessed 2026-11-25
3. [RoboCasa docs: Datasets overview](https://robocasa.ai/docs/build/html/datasets/datasets_overview.html), accessed 2026-11-25
4. [RoboCasa docs: Using datasets](https://robocasa.ai/docs/build/html/datasets/using_datasets.html), accessed 2026-11-25
5. [RoboCasa365 leaderboard](https://robocasa.ai/leaderboard.html), accessed 2026-11-25
6. [LeRobot docs: RoboCasa365](https://huggingface.co/docs/lerobot/robocasa), accessed 2026-11-25

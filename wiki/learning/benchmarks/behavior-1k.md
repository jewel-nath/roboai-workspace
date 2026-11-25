---
type: tool
name: BEHAVIOR-1K (with OmniGibson)
summary: Stanford's benchmark of 1,000 household activities in 50 house-scale scenes, simulated in its own OmniGibson on NVIDIA Isaac Sim, with a yearly challenge on 100 long tasks for a bimanual mobile robot; code MIT, but the scene and object bundle is encrypted and for non-commercial academic research only. Needs an RTX GPU with 8 GB or more.
tags: [behavior-1k, omnigibson, benchmark, simulation, household, mobile-manipulation, bimanual, isaac-sim, omniverse, bddl, long-horizon, challenge, lerobot, non-commercial-data]
kind: framework
area: learning
support:
license: MIT
links: {repo: "https://github.com/StanfordVL/BEHAVIOR-1K", docs: "https://behavior.stanford.edu/getting_started/installation.html", site: "https://behavior.stanford.edu/"}
version: {tested: , latest: 3.9.4, as_of: 2026-11-25}
platforms: [linux, windows]
agent_access: script
registry:
evidence: researched
last_verified: 2026-11-25
sources:
  - {url: "https://github.com/StanfordVL/BEHAVIOR-1K", title: "BEHAVIOR-1K repository: README, LICENSE, setup.sh (data licence, Isaac Sim pin), OmniGibson/setup.py, docs/challenge (evaluation, dataset, baselines, updates), tags, history", accessed: 2026-11-25}
  - {url: "https://behavior.stanford.edu/getting_started/installation.html", title: "BEHAVIOR docs: Installation", accessed: 2026-11-25}
  - {url: "https://arxiv.org/abs/2403.09227", title: "BEHAVIOR-1K: A Human-Centered, Embodied AI Benchmark with 1,000 Everyday Activities and Realistic Simulation (arXiv)", accessed: 2026-11-25}
  - {url: "https://behavior.stanford.edu/challenge/index.html", title: "BEHAVIOR docs: 2026 BEHAVIOR Challenge", accessed: 2026-11-25}
  - {url: "https://huggingface.co/datasets/behavior-1k/2026-challenge-demos", title: "Hugging Face dataset card: behavior-1k/2026-challenge-demos", accessed: 2026-11-25}
---

# BEHAVIOR-1K (with OmniGibson)

BEHAVIOR-1K defines 1,000 household activities in BDDL, in 50 scenes with over 9,000 annotated
objects, simulated in OmniGibson on NVIDIA [Isaac Sim](../../tools/isaac-sim.md) with rigid and
deformable bodies and liquids [3]; one Stanford repo holds it all, with the JoyLo teleop kit [1].
Builders use it for multi-room mobile manipulation. **Licences:** code MIT; the scene and object
bundle is encrypted, usable only inside OmniGibson and only for non-commercial academic research;
Isaac Sim is under NVIDIA's EULA [1]; the 2026 challenge demos are marked MIT [5]. Active: last
commit 2026-11-24, tag v3.9.4 [1].

## When to use it

- **Use it** to test a policy on house-scale tasks mixing navigation, two arms and object states
  (cooking, wiping, slicing), given an RTX workstation [2][4].
- **Use something else** for commercial use of the scenes, a small GPU or a tabletop arm:
  [RoboCasa](robocasa.md) (CC BY 4.0 assets) or [LIBERO](libero.md).

## Setup

```bash
git clone -b v3.9.4 https://github.com/StanfordVL/BEHAVIOR-1K.git && cd BEHAVIOR-1K
./setup.sh --new-env --omnigibson --bddl --dataset   # prompts for Conda, NVIDIA and data terms
conda activate behavior
python -m omnigibson.examples.robots.robot_control_example --quickstart
```

Needs Ubuntu 22.04+ or Windows 10+, 32 GB of RAM and an RTX 2070 or better with 8 GB of VRAM;
the first import takes up to 5 minutes; Docker is paused [2]. v3.9.4 installs Isaac Sim 5.1.0 on
Python 3.11; `main` moved to Isaac Sim 6.2.0 and Python 3.12 on 2026-11-24 [1]. Baselines:
[pi0.5](../models/pi0.md) on one or more GPUs, [GR00T](../models/gr00t.md) N1.7 on 8 GPUs for
150,000 steps; no memory figure is given [1].

## How an agent works with it

- **2026 challenge** [1][4]: 100 long tasks in 7 scenes; the policy sees only RGB, depth and
  proprioception, on the bimanual mobile R1Pro or another OmniGibson robot (`--robot-config`).
  The evaluator calls your policy server over a websocket and writes `q_score` per rollout.
- **Data** [1][5]: 20,000 teleoperated demos (1,950 h) as LeRobot v3 (3.27 TB) plus raw HDF5 for
  replay (1.44 TB); head camera 720 x 720, wrists 480 x 480.
- **Status:** entries closed 2026-10-16; winners, due 2026-11-04, were not on the page by 11-25 [4].

## Traps

- **MIT code, restricted data.** `--accept-dataset-tos` accepts a licence for non-commercial
  academic research only that forbids extracting assets [1]. Read it before a company does.
- **Moving versions.** The install page says `-b v3.9.3`, but only `v3.9.3-post1`, `-post2` and
  `v3.9.4` are tags; hidden tests were set for `v3.9.3-post1` [1][2]. Pin a tag, re-check after
  the Isaac Sim 6.2 move, and avoid tiled rendering, whose artefacts can confuse a policy [1].
- **Partial credit is not success.** `q_score` gives credit per BDDL goal condition met [1];
  compare it only with `q_score` on the same instances (report 0 to 9) [1].
- **Slow, large runs.** A rollout may take `max_steps` seconds, about 10.85 hours for the longest
  task, and the demos run to terabytes [1]. Start with a few tasks.
- **Wrong GPU.** On `HydraEngine rtx failed creating scene renderer`, set `OMNIGIBSON_GPU_ID` [2].

## Alternatives

[RoboCasa](robocasa.md), [LIBERO](libero.md), [Isaac Lab](../frameworks/isaac-lab.md);
[Choose a simulator](../../guides/choose-a-simulator.md).

## Sources

1. [BEHAVIOR-1K repository: README, LICENSE, setup.sh (data licence, Isaac Sim pin), OmniGibson/setup.py, docs/challenge (evaluation, dataset, baselines, updates), tags, history](https://github.com/StanfordVL/BEHAVIOR-1K), accessed 2026-11-25
2. [BEHAVIOR docs: Installation](https://behavior.stanford.edu/getting_started/installation.html), accessed 2026-11-25
3. [BEHAVIOR-1K: A Human-Centered, Embodied AI Benchmark with 1,000 Everyday Activities and Realistic Simulation (arXiv)](https://arxiv.org/abs/2403.09227), accessed 2026-11-25
4. [BEHAVIOR docs: 2026 BEHAVIOR Challenge](https://behavior.stanford.edu/challenge/index.html), accessed 2026-11-25
5. [Hugging Face dataset card: behavior-1k/2026-challenge-demos](https://huggingface.co/datasets/behavior-1k/2026-challenge-demos), accessed 2026-11-25

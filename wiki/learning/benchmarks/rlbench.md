---
type: tool
name: RLBench
summary: Imperial College's 100-task manipulation benchmark for a simulated Franka Panda in CoppeliaSim 4.1 through PyRep, with unlimited motion-planned demonstrations; the base of PerAct, RVT and most 3D keyframe policies. Its own licence allows non-commercial research only, CoppeliaSim Edu is limited to schools and universities, and the code has been quiet since mid-2024.
tags: [rlbench, benchmark, simulation, manipulation, coppeliasim, pyrep, franka, imitation-learning, reinforcement-learning, few-shot, multi-task, peract, rvt, non-commercial]
kind: framework
area: learning
support:
license: LicenseRef-RLBench-Imperial-Non-Commercial
links: {repo: "https://github.com/stepjam/RLBench", docs: , site: "https://sites.google.com/corp/view/rlbench"}
version: {tested: , latest: 1.2.0, as_of: 2026-11-25}
platforms: [linux]
agent_access: script
registry:
evidence: researched
last_verified: 2026-11-25
sources:
  - {url: "https://github.com/stepjam/RLBench", title: "RLBench repository: README, LICENSE, setup.py, rlbench/__init__.py, tasks, tags, history, issues", accessed: 2026-11-25}
  - {url: "https://arxiv.org/abs/1909.12271", title: "RLBench: The Robot Learning Benchmark & Learning Environment (arXiv)", accessed: 2026-11-25}
  - {url: "https://github.com/stepjam/PyRep", title: "PyRep repository: README, LICENSE, history", accessed: 2026-11-25}
  - {url: "https://www.coppeliarobotics.com", title: "CoppeliaSim website: editions and Edu terms", accessed: 2026-11-25}
  - {url: "https://github.com/peract/peract", title: "PerAct repository: README (RLBench setup, data, 18-task protocol)", accessed: 2026-11-25}
  - {url: "https://github.com/NVlabs/RVT", title: "RVT and RVT-2 repository: README (CoppeliaSim, PerAct data)", accessed: 2026-11-25}
---

# RLBench

RLBench gives a simulated [Franka Panda](../../robots/franka-panda.md) 100 hand-designed tasks in
[CoppeliaSim](../../tools/coppeliasim.md) 4.1 through PyRep, with unlimited motion-planned
demonstrations and RGB, depth and masks from shoulder and wrist cameras [1][2]. It underlies
PerAct, RVT and other 3D keyframe policies [5][6]. **Licence: non-commercial.** Imperial College's
licence allows only non-commercial, internal or academic research; PyRep is MIT [1][3]. Version
1.2.0 (2022; newest tag 1.1.0); last code change 2024-07-03; 93 open issues, few answered [1].

## When to use it

- **Use it** to compare with PerAct-style 3D policies on their 18-task split, or for few-shot and
  multi-task sets such as `FS10_V1` and `MT15_V1` [1][5].
- **Use something else** commercially or on Ubuntu 24.04: [ManiSkill](../frameworks/maniskill.md),
  [LIBERO](libero.md) or [RoboCasa](robocasa.md).

## Setup

```bash
export COPPELIASIM_ROOT=$HOME/CoppeliaSim
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$COPPELIASIM_ROOT
export QT_QPA_PLATFORM_PLUGIN_PATH=$COPPELIASIM_ROOT
F=CoppeliaSim_Edu_V4_1_0_Ubuntu20_04.tar.xz
wget https://downloads.coppeliarobotics.com/V4_1_0/$F
mkdir -p $COPPELIASIM_ROOT && tar -xf $F -C $COPPELIASIM_ROOT --strip-components 1
pip install git+https://github.com/stepjam/RLBench.git    # pulls PyRep from git
```

PyRep needs CoppeliaSim 4.1 and talks to it only on Linux; 4.1 builds stop at Ubuntu 20.04 [3].
Headless runs need an X server on an NVIDIA GPU or VirtualGL [1][3]. No GPU figure upstream;
PerAct trained on 8 P100s (16 GB each) and needs one GPU for inference [5].

## How an agent works with it

- `Environment(MoveArmThenGripper(JointVelocity(), Discrete()))`, `launch()`, `get_task(...)`,
  then `reset()`, `step(action)`, `get_demos(n)`; Gymnasium ids like `reach_target-vision-v0` [1].
- Images are 128 x 128 by default; arm actions: joint velocity, position, torque or pose [1].
- **Score:** the share of episodes meeting the task's success conditions. PerAct uses 18 tasks,
  100 demos and 25 test episodes each, pre-generated (about 116 GB), and so does RVT [5][6].

## Traps

- **Two licences stack.** RLBench is non-commercial [1]; the Edu build the README downloads is
  "exclusively available for use by students, teachers and professors" [4]. RVT points to the 4.1
  Player build [6]; read its licence too.
- **Ubuntu 24.04.** No CoppeliaSim 4.1 build exists for it [3], and PerAct's Docker guide is
  still unwritten [5]; an Ubuntu 20.04 machine or container is the documented path.
- **Image size and saved demos.** Changing from 128 x 128 resizes stored demos but renders live
  frames natively, so they differ; re-collect demos at the size you train on [1].
- **Comparable runs.** PerAct's numbers come from its own fork (`peract` branch) and pre-generated
  sets; `dataset_generator.py` samples scenes at random [5]. Use both to compare.

## Alternatives

[CALVIN](calvin.md), [LIBERO](libero.md), [RoboCasa](robocasa.md),
[ManiSkill](../frameworks/maniskill.md), [3D Diffusion Policy](../policies/3d-diffusion-policy.md).

## Sources

1. [RLBench repository: README, LICENSE, setup.py, rlbench/__init__.py, tasks, tags, history, issues](https://github.com/stepjam/RLBench), accessed 2026-11-25
2. [RLBench: The Robot Learning Benchmark & Learning Environment (arXiv)](https://arxiv.org/abs/1909.12271), accessed 2026-11-25
3. [PyRep repository: README, LICENSE, history](https://github.com/stepjam/PyRep), accessed 2026-11-25
4. [CoppeliaSim website: editions and Edu terms](https://www.coppeliarobotics.com), accessed 2026-11-25
5. [PerAct repository: README (RLBench setup, data, 18-task protocol)](https://github.com/peract/peract), accessed 2026-11-25
6. [RVT and RVT-2 repository: README (CoppeliaSim, PerAct data)](https://github.com/NVlabs/RVT), accessed 2026-11-25

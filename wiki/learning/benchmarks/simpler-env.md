---
type: tool
name: SimplerEnv (SIMPLER)
summary: Simulated copies of two real evaluation setups, Google's RT-1 robot and the BridgeData V2 WidowX, built to rank VLA checkpoints without a real robot; MIT code on SAPIEN 2.2.2 and a ManiSkill2 fork (Apache-2.0), with GPU-parallel WidowX tasks in ManiSkill 3. Maintenance only since 2024, no releases.
tags: [simplerenv, simpler, benchmark, real-to-sim, evaluation, vla, rt-1, octo, google-robot, widowx, bridgedata, sapien, maniskill, open-x-embodiment]
kind: framework
area: learning
support:
license: MIT
links: {repo: "https://github.com/simpler-env/SimplerEnv", docs: , site: "https://simpler-env.github.io/"}
version: {tested: , latest: , as_of: 2026-11-25}
platforms: [linux]
agent_access: script
registry:
evidence: researched
last_verified: 2026-11-25
sources:
  - {url: "https://github.com/simpler-env/SimplerEnv", title: "SimplerEnv repository (main): README, LICENSE, setup.py, requirements_full_install.txt, history, issues 129 and 131", accessed: 2026-11-25}
  - {url: "https://github.com/simpler-env/SimplerEnv/tree/maniskill3", title: "SimplerEnv repository: maniskill3 branch README", accessed: 2026-11-25}
  - {url: "https://github.com/simpler-env/ManiSkill2_real2sim", title: "ManiSkill2_real2sim repository: README, LICENSE, setup.py, requirements.txt, data folder", accessed: 2026-11-25}
  - {url: "https://arxiv.org/abs/2405.05941", title: "Evaluating Real-World Robot Manipulation Policies in Simulation (arXiv)", accessed: 2026-11-25}
  - {url: "https://pypi.org/project/sapien/2.2.2/#files", title: "PyPI: sapien 2.2.2 files", accessed: 2026-11-25}
---

# SimplerEnv (SIMPLER)

SimplerEnv recreates two real evaluation setups in simulation: Google's RT-1 mobile manipulator
([Google Robot](../../robots/google-robot.md)) and the BridgeData V2
[WidowX 250](../../robots/interbotix-x-series-arms.md), overlaying real background photos ("visual
matching") or averaging over scene variants ("variant aggregation") [1]. Builders use it to rank
VLA checkpoints without a real robot. Code MIT; its ManiSkill2 fork is Apache-2.0, with no
separate asset licence [1][3]. No tags; the last commit (2026-09-30) pinned `transformers<5` [1].

## When to use it

- **Use it** for a policy trained on [Open X-Embodiment](../datasets/open-x-embodiment.md)
  fractal or [BridgeData V2](../datasets/bridgedata-v2.md) data, such as [RT-1](../models/rt-1.md),
  [Octo](../models/octo.md) or [OpenVLA](../models/openvla.md), to choose checkpoints [1][4].
- **Use something else** for your own arm: a new robot needs assets and system identification
  (`ADDING_NEW_ENVS_ROBOTS.md`) [1]. For fine-tuning comparisons use [LIBERO](libero.md).

## Setup

```bash
conda create -n simpler_env python=3.10 && conda activate simpler_env
git clone https://github.com/simpler-env/SimplerEnv --recurse-submodules && cd SimplerEnv
pip install numpy==1.24.4
pip install -e ./ManiSkill2_real2sim && pip install -e .
```

Needs an NVIDIA GPU, ideally RTX, since SAPIEN renders on it [1]; SAPIEN 2.2.2 wheels cover only
Python 3.7 to 3.11 on x86-64 Linux, so not Ubuntu 24.04's Python 3.12 or a Jetson [5]. The bundled
RT-1 and Octo add TensorFlow 2.15, JAX 0.4.20 and CUDA 11.8 to 12.x; no GPU memory figure is given
[1]. The `maniskill3` branch only adds inference setup; the WidowX tasks moved into ManiSkill 3 [2].

## How an agent works with it

- `simpler_env.make("widowx_carrot_on_plate")`; `env.get_language_instruction()` names the task [1].
- **Tasks** [1]: Google Robot pick coke can, pick object, move near, open or close drawer, apple
  into closed drawer; WidowX spoon on towel, carrot on plate, stack cube, eggplant in basket.
- **Actions:** 7-D, delta xyz, delta axis-angle rotation and gripper; control at 3 Hz (Google
  Robot) or 5 Hz (Bridge), physics near 500 Hz [1].
- **Score:** success rate per task from `info["episode_stats"]`. The paper rates the sim by rank
  violation (MMRV) and Pearson correlation with real results for RT-1, RT-1-X and Octo [1][4].

## Traps

- **Gripper sign.** Whether the gripper value opens or closes depends on the URDF [1]. If it looks
  wrong, the `*_inference_real_video.py` debug scripts feed real eval frames to the policy [1].
- **Control rate.** The envs step at 3 or 5 Hz [1]; a policy trained at another rate, or with
  other action scaling, scores low for reasons unrelated to skill.
- **Lenient success.** Issue 129 reports WidowX episodes counted as successes too early; a
  collaborator points to `success_require_src_completely_on_target` [1]. Inspect the videos.
- **Two code paths.** Paper numbers need `main` (SAPIEN 2.2, ManiSkill2); the ManiSkill 3 twins
  are 10 to 15 times faster but a different simulator [1][2]. Say which you used.
- **Old pins.** numpy below 2.0 and gymnasium below 1.0 [1][3]; TensorFlow 2.15 lacks kernels for
  RTX 50-series GPUs, so RT-1 and Octo inference fails there (issue 131, open) [1].

## Alternatives

[LIBERO](libero.md), [RoboCasa](robocasa.md), [CALVIN](calvin.md),
[ManiSkill](../frameworks/maniskill.md).

## Sources

1. [SimplerEnv repository (main): README, LICENSE, setup.py, requirements_full_install.txt, history, issues 129 and 131](https://github.com/simpler-env/SimplerEnv), accessed 2026-11-25
2. [SimplerEnv repository: maniskill3 branch README](https://github.com/simpler-env/SimplerEnv/tree/maniskill3), accessed 2026-11-25
3. [ManiSkill2_real2sim repository: README, LICENSE, setup.py, requirements.txt, data folder](https://github.com/simpler-env/ManiSkill2_real2sim), accessed 2026-11-25
4. [Evaluating Real-World Robot Manipulation Policies in Simulation (arXiv)](https://arxiv.org/abs/2405.05941), accessed 2026-11-25
5. [PyPI: sapien 2.2.2 files](https://pypi.org/project/sapien/2.2.2/#files), accessed 2026-11-25

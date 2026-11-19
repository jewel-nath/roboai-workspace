---
type: tool
name: Genesis
summary: GPU-parallel multi-physics simulator with a Python API for robot learning (now called Genesis World); loads URDF, MJCF and USD and steps thousands of environments on CUDA, ROCm, Metal or CPU.
tags: [simulator, gpu, physics, reinforcement-learning, parallel-environments, multi-physics, urdf, mjcf, usd, python]
kind: library
area: sim
support: documented
license: Apache-2.0
links: {repo: "https://github.com/Genesis-Embodied-AI/genesis-world", docs: "https://genesis-world.readthedocs.io/en/latest/", site: }
version: {tested: , latest: 1.4.7, as_of: 2026-11-19}
platforms: [linux, windows, macos]
agent_access: script
registry:
evidence: researched
last_verified: 2026-11-19
sources:
  - {url: "https://github.com/Genesis-Embodied-AI/genesis-world", title: "Genesis World repository: README, LICENSE, pyproject.toml, RELEASE.md, solver options, examples", accessed: 2026-11-19}
  - {url: "https://pypi.org/project/genesis-world/#history", title: "genesis-world on PyPI: release history", accessed: 2026-11-19}
  - {url: "https://genesis-world.readthedocs.io/en/latest/user_guide/overview/installation.html", title: "Genesis docs: Installation", accessed: 2026-11-19}
  - {url: "https://genesis-world.readthedocs.io/en/latest/user_guide/getting_started/hello_genesis.html", title: "Genesis docs: Hello, Genesis", accessed: 2026-11-19}
  - {url: "https://github.com/Genesis-Embodied-AI/genesis-world/blob/v0.2.1/README.md", title: "Genesis v0.2.1 README: launch speed claim", accessed: 2026-11-19}
  - {url: "https://placid-walkover-0cc.notion.site/genesis-performance-benchmarking", title: "Genesis team: A Detailed Performance Benchmarking Report on Genesis (January 2025)", accessed: 2026-11-19}
  - {url: "https://stoneztao.substack.com/p/the-new-hyped-genesis-simulator-is", title: "Stone Tao: How fast is the new hyped Genesis simulator? (December 2024)", accessed: 2026-11-19}
  - {url: "https://arxiv.org/abs/2607.13059", title: "GPUSimBench: Towards Scalable and Reliable GPU-Accelerated Simulators in Embodied AI (IROS 2026)", accessed: 2026-11-19}
---

# Genesis

A Python physics platform with rigid, FEM, MPM, SPH and PBD solvers in one scene, compiled to GPU kernels
by Quadrants, its Taichi fork [1]. Builders train locomotion and manipulation policies on it over thousands
of parallel environments. Renamed Genesis World, backed by Genesis AI; Apache-2.0; 1.4.7, 2026-11-17 [1][2].

## When to use it

For GPU-batched reinforcement learning or data generation in Python, above all when robots touch soft
bodies, cloth or fluids, or your GPU is AMD or Apple silicon [1][3]. Its rigid solver follows MuJoCo's
[6]; for one robot, contact studies or code that must last, use [MuJoCo](mujoco.md). It has no ROS 2
bridge [1]: for ROS 2 use [Gazebo](gazebo.md) or [Isaac Sim](isaac-sim.md).

## Setup

On Ubuntu 24.04, in a venv: `pip install torch` (the CUDA, ROCm or CPU build from pytorch.org), then
`pip install "genesis-world==1.4.7"`. It needs Python 3.12–3.14 [1]; the install page still says
3.10–3.13 [3], and Ubuntu 22.04's Python 3.10 cannot install current releases.

- **Backends:** CUDA and ROCm on Linux and Windows, Metal on Apple silicon, CPU everywhere; Intel GPUs
  run physics on the CPU [3]. CUDA needs a matching NVIDIA driver [3].
- **Headless Linux** renders through EGL, or falls back to slow Mesa without NVIDIA's EGL library.
  Docker: `--gpus all`, `PYOPENGL_PLATFORM=egl`. WSL2: add `/usr/lib/wsl/lib` to `LD_LIBRARY_PATH` [3].

## How an agent works with it

All Python: `gs.init(backend=gs.gpu)`, `gs.Scene()`, `scene.add_entity(gs.morphs.URDF(file=...))` (also
`MJCF`, `USD`, meshes; `.urdf.xacro` is expanded), headless by default [4]. `scene.build(n_envs=4096)`
batches it, `scene.step()` steps it, `control_dofs_position` and `get_dofs_position` drive and read
joints [1]. Healthy run: `build()` parses the model and joints follow commands. Templates: the Franka
and Go2 (rsl-rl) scripts in `examples/` [1].

## Traps

- **Speed numbers depend on settings.** Launch claim: 43 million FPS, a Franka on one RTX 4090,
  "430,000 times faster than real-time" [5]. Stone Tao, of ManiSkill's lab, added substeps, motion and
  self-collision: about 0.29M, and 3–10x slower than ManiSkill at cube picking [7]. The Genesis reply
  (v0.2.1, 32,768 envs): 47.7M static with self-collision, 27M with random actions, 16.4M with floor
  contact too [6]. GPUSimBench (0.3.11, 12 GB RTX 5070): top throughput on a random-action Franka
  (11.1M), at most 2,048 envs on falling cubes, fifth of seven on sim-to-real error [8].
- **The API breaks often.** 31 releases in 2026; 8 of the 18 since 1.0.0 (2026-05-27) list breaking
  changes [1][2]. Pin the version; read `RELEASE.md` before upgrading. Self-collision was off by default
  at launch [6] and is on in 1.4.7 [1], so old benchmarks and configs do not carry over.
- **The first build is slow.** `build()` compiles and caches kernels; `performance_mode=True` is ~30%
  faster but recompiles for minutes per scene change. Stop with Ctrl-C, not Ctrl-\, to keep the cache [4].
- **The launch demos showed more than ships.** The generative text-to-scene framework announced at
  launch was not open-sourced; only the physics engine and simulation platform are [5][7].

## Alternatives

[MuJoCo](mujoco.md), [Isaac Sim](isaac-sim.md), [PyBullet](pybullet.md), [Gazebo](gazebo.md),
[Habitat](habitat.md), Isaac Lab, ManiSkill, MJX; [Choose a simulator](../guides/choose-a-simulator.md).

## Sources

1. [Genesis World repository: README, LICENSE, pyproject.toml, RELEASE.md, solver options, examples](https://github.com/Genesis-Embodied-AI/genesis-world), accessed 2026-11-19
2. [genesis-world on PyPI: release history](https://pypi.org/project/genesis-world/#history), accessed 2026-11-19
3. [Genesis docs: Installation](https://genesis-world.readthedocs.io/en/latest/user_guide/overview/installation.html), accessed 2026-11-19
4. [Genesis docs: Hello, Genesis](https://genesis-world.readthedocs.io/en/latest/user_guide/getting_started/hello_genesis.html), accessed 2026-11-19
5. [Genesis v0.2.1 README: launch speed claim](https://github.com/Genesis-Embodied-AI/genesis-world/blob/v0.2.1/README.md), accessed 2026-11-19
6. [Genesis team: A Detailed Performance Benchmarking Report on Genesis (January 2025)](https://placid-walkover-0cc.notion.site/genesis-performance-benchmarking), accessed 2026-11-19
7. [Stone Tao: How fast is the new hyped Genesis simulator? (December 2024)](https://stoneztao.substack.com/p/the-new-hyped-genesis-simulator-is), accessed 2026-11-19
8. [GPUSimBench: Towards Scalable and Reliable GPU-Accelerated Simulators in Embodied AI (IROS 2026)](https://arxiv.org/abs/2607.13059), accessed 2026-11-19

---
type: tool
name: robomimic
summary: Stanford's MIT-licensed framework for learning manipulation from demonstrations - BC, BC-RNN, BC-Transformer, Diffusion Policy, HBC and offline RL (IRIS, BCQ, CQL, IQL, TD3-BC) - with the robomimic HDF5 format and MIT datasets on robosuite tasks; v0.5.0 is only on GitHub (PyPI stops at 0.3.0), and it needs robosuite v1.5.1 from source.
tags: [robomimic, imitation-learning, behavior-cloning, bc-rnn, bc-transformer, diffusion-policy, offline-rl, iql, cql, hdf5, robosuite, datasets, arise]
kind: framework
area: learning
support:
license: MIT
links: {repo: "https://github.com/ARISE-Initiative/robomimic", docs: "https://robomimic.github.io/docs/introduction/overview.html", site: "https://robomimic.github.io/"}
version: {tested: , latest: 0.5.0, as_of: 2026-11-25}
platforms: [linux, macos]
agent_access: script
registry:
evidence: researched
last_verified: 2026-11-25
sources:
  - {url: "https://github.com/ARISE-Initiative/robomimic", title: "robomimic repository: README, LICENSE, setup.py, Dockerfile, algo and config modules, scripts, docs sources (algorithms, dataset structure), tags and history", accessed: 2026-11-25}
  - {url: "https://robomimic.github.io/docs/introduction/installation.html", title: "robomimic docs: Installation", accessed: 2026-11-25}
  - {url: "https://robomimic.github.io/docs/datasets/robomimic_v0.1.html", title: "robomimic docs: robomimic v0.1 datasets", accessed: 2026-11-25}
  - {url: "https://huggingface.co/datasets/robomimic/robomimic_datasets", title: "Hugging Face: robomimic datasets card", accessed: 2026-11-25}
  - {url: "https://pypi.org/project/robomimic/", title: "PyPI: robomimic release history; mink and mujoco Python requirements", accessed: 2026-11-25}
  - {url: "https://github.com/ARISE-Initiative/robomimic/issues", title: "robomimic issues, including 322 (eval on checkpoint config) and 323 (egl_probe and CMake 4)", accessed: 2026-11-25}
---

# robomimic

Stanford SVL's framework (ARISE Initiative) for learning manipulation from demonstrations:
offline imitation and RL algorithms, datasets, and scripts that train policies and score them in
[robosuite](robosuite.md) [1]. Code MIT [1]; datasets MIT, not gated [4]. v0.5.0 (tagged
2025-06-26) is not on PyPI; last commit 2026-08-09; the two newest issues had no reply [1][5][6].

## When to use it

- **Algorithms** [1]: BC (GMM, VAE heads), BC-RNN, BC-Transformer, HBC, U-Net
  [Diffusion Policy](../policies/diffusion-policy.md); offline RL: IRIS, BCQ, CQL, IQL, TD3-BC.
- **Use it** to compare policies on robosuite or MimicGen HDF5 data; on a real low-cost arm,
  use [LeRobot](lerobot.md), which records, trains and runs on the robot.

## Setup

```bash
conda create -n robomimic_venv python=3.9 && conda activate robomimic_venv
git clone https://github.com/ARISE-Initiative/robomimic && pip install -e robomimic
git clone -b v1.5.1 https://github.com/ARISE-Initiative/robosuite
pip install -e robosuite "mink==0.0.5" "mujoco<3.10"     # see Traps
```

Docs: Python 3.8, PyTorch 2.0.0, robosuite `v1.5.1` from source for the released data (v1.2+
otherwise); Linux, macOS [2]. No GPU or memory figures upstream; Docker uses CUDA 11.8 [1][2].

## How an agent works with it

```bash
cd robomimic/robomimic/scripts
python download_datasets.py --tasks lift --dataset_types ph --hdf5_types low_dim
python train.py --config ../exps/templates/diffusion_policy.json --dataset <file.hdf5>
python run_trained_agent.py --agent <model.pth> --n_rollouts 50 --horizon 400
```

- **Datasets** [3]: Lift, Can, Square, Transport, Tool Hang; 200 Proficient-Human and 300
  Multi-Human demos per task, plus machine-generated and real-robot sets.
- **HDF5** [1]: `data` holds `env_args` (JSON) and one `demo_N` group per episode with
  `states` (flat MuJoCo state), `actions`, `rewards`, `dones`, `obs/<key>` and `next_obs/<key>`;
  `mask/train` and `mask/valid` hold the split. `get_dataset_info.py` prints it.
- **Check:** 50 simulated rollouts every 50 epochs log a success rate; the best are saved [1].

## Traps

- **Stale PyPI, old pins.** `pip install robomimic` gives 0.3.0 without Diffusion Policy [5];
  v0.5.0 pins `diffusers==0.11.1` and `transformers==4.41.2` [1]. Give it its own venv.
- **Python 3.8 fails.** robosuite v1.5.1 needs mink, which needs Python 3.9+ [5], and its open
  MuJoCo pin breaks on 3.10+; pin both (see [robosuite](robosuite.md)).
- **CMake 4** fails the `egl_probe` build; set `CMAKE_POLICY_VERSION_MINIMUM=3.5` first [6].
- **Data follows robosuite.** Today's files are built for robosuite v1.5.1 and may not match
  CoRL 2021 numbers; simulated image files are not hosted, so render them from raw states [1][3].
- **Checkpoints can run code** (`torch.load`, `weights_only=False`): load trusted ones [1][6].

## Alternatives

[LeRobot](lerobot.md), [LIBERO](../benchmarks/libero.md), [RoboCasa](../benchmarks/robocasa.md).

## Sources

1. [robomimic repository: README, LICENSE, setup.py, Dockerfile, algo and config modules, scripts, docs sources (algorithms, dataset structure), tags and history](https://github.com/ARISE-Initiative/robomimic), accessed 2026-11-25
2. [robomimic docs: Installation](https://robomimic.github.io/docs/introduction/installation.html), accessed 2026-11-25
3. [robomimic docs: robomimic v0.1 datasets](https://robomimic.github.io/docs/datasets/robomimic_v0.1.html), accessed 2026-11-25
4. [Hugging Face: robomimic datasets card](https://huggingface.co/datasets/robomimic/robomimic_datasets), accessed 2026-11-25
5. [PyPI: robomimic release history; mink and mujoco Python requirements](https://pypi.org/project/robomimic/), accessed 2026-11-25
6. [robomimic issues, including 322 (eval on checkpoint config) and 323 (egl_probe and CMake 4)](https://github.com/ARISE-Initiative/robomimic/issues), accessed 2026-11-25

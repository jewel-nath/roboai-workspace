---
type: tool
name: robosuite
summary: MIT-licensed MuJoCo framework for robot-learning research, with standard tabletop manipulation tasks, research arms, mobile manipulators and a humanoid, operational-space and whole-body controllers, teleoperation and HDF5 demo recording; the simulator under robomimic, LIBERO and RoboCasa. Release 1.5.2 (2025-12) breaks on current MuJoCo unless you pin it; slow maintenance since mid-2026.
tags: [robosuite, mujoco, simulation, manipulation, imitation-learning, reinforcement-learning, benchmark, osc, operational-space-control, whole-body-ik, teleoperation, hdf5, robomimic, libero, robocasa, arise]
kind: framework
area: learning
support:
license: MIT
links: {repo: "https://github.com/ARISE-Initiative/robosuite", docs: "https://robosuite.ai/docs/overview.html", site: "https://robosuite.ai"}
version: {tested: , latest: 1.5.2, as_of: 2026-11-25}
platforms: [linux, macos, windows]
agent_access: script
registry:
evidence: researched
last_verified: 2026-11-25
sources:
  - {url: "https://github.com/ARISE-Initiative/robosuite", title: "robosuite repository: README, LICENSE, setup.py, docs/changelog.md, macros, controller configs, environments, robots, renderers, tags and history", accessed: 2026-11-25}
  - {url: "https://pypi.org/project/robosuite/", title: "PyPI: robosuite release history and 1.5.2 requirements", accessed: 2026-11-25}
  - {url: "https://robosuite.ai/docs/installation.html", title: "robosuite docs: Installation", accessed: 2026-11-25}
  - {url: "https://robosuite.ai/docs/overview.html", title: "robosuite docs: Overview (v1.5)", accessed: 2026-11-25}
  - {url: "https://robosuite.ai/docs/modules/controllers.html", title: "robosuite docs: Controllers", accessed: 2026-11-25}
  - {url: "https://robosuite.ai/docs/modules/renderers.html", title: "robosuite docs: Renderers", accessed: 2026-11-25}
  - {url: "https://github.com/ARISE-Initiative/robosuite/issues/831", title: "robosuite issue 831: 1.5.2 from PyPI fails with current MuJoCo", accessed: 2026-11-25}
  - {url: "https://github.com/ARISE-Initiative/robosuite/issues", title: "robosuite issues: open issue list", accessed: 2026-11-25}
  - {url: "https://pypi.org/project/mujoco/", title: "PyPI: mujoco release history", accessed: 2026-11-25}
  - {url: "https://robomimic.github.io/docs/introduction/installation.html", title: "robomimic docs: Installation (robosuite v1.5.1 for released datasets)", accessed: 2026-11-25}
  - {url: "https://github.com/Lifelong-Robot-Learning/LIBERO", title: "LIBERO repository: requirements.txt", accessed: 2026-11-25}
  - {url: "https://github.com/robocasa/robocasa", title: "RoboCasa repository: README and setup.py", accessed: 2026-11-25}
---

# robosuite

robosuite is a simulation framework for robot learning on the [MuJoCo](../../tools/mujoco.md)
physics engine, with a set of standard manipulation tasks for reproducible benchmarks [1][4].
Builders use it to train and score imitation and reinforcement-learning policies on simulated
arms, to record teleoperated demos, and as the simulator behind
[robomimic](robomimic.md), [LIBERO](../benchmarks/libero.md) and
[RoboCasa](../benchmarks/robocasa.md). MIT [1]. Started at Stanford's Vision and Learning Lab in
2017, it is maintained in the ARISE Initiative by Stanford SVL, UT Austin's RPL and NVIDIA's GEAR
group [1][4].

**State:** release 1.5.2 (2025-12-24) on PyPI [2]; the last commit on `master` is 2026-07-11 [1].
82 issues are open; an October 2026 request for a 1.5.3 release that fixes installs on current
MuJoCo had no visible maintainer reply [7][8]. Not a ROS package; we found no maintained ROS 2
bridge.

## When to use it

- **Use it** for tabletop manipulation research: one-arm Lift, Stack, NutAssembly, PickPlace,
  Door, Wipe and ToolHang, and two-arm Lift, PegInHole, Handover and Transport [1]. Also to
  reproduce robomimic, LIBERO or RoboCasa results, which need robosuite underneath [10][11][12].
- **Robots** [1]: Panda (also with dexterous hands), Sawyer, IIWA, Jaco, Kinova3, UR5e, xArm7,
  Baxter; mobile PandaOmron, Tiago and Spot with arm; the GR1 humanoid. Grippers include Panda,
  Rethink, Robotiq 2F-85, 2F-140 and 3-finger, and Inspire and Fourier hands; the separate
  `robosuite_models` package adds more robots [1]. The demo robot is the
  [Franka Panda](../../robots/franka-panda.md).
- **Use something else** for thousands of parallel environments on a GPU
  ([ManiSkill](maniskill.md), [Isaac Lab](isaac-lab.md)), for your own robot in a ROS 2 stack
  ([Gazebo](../../tools/gazebo.md), [Isaac Sim](../../tools/isaac-sim.md)), or for a low-cost
  arm trained with [LeRobot](lerobot.md). See
  [Choose a simulator](../../guides/choose-a-simulator.md).

## Setup

```bash
conda create -n robosuite python=3.10 && conda activate robosuite
pip install robosuite "mujoco==3.9.0"   # 1.5.2; newer MuJoCo breaks it, see Traps
python -m robosuite.demos.demo_random_action
```

- **From source** [1][3]: `git clone https://github.com/ARISE-Initiative/robosuite`, then
  `pip install -r requirements.txt` (an editable install; `master` pins `mujoco>=3.3.0,<3.10`)
  and optionally `pip install -r requirements-extra.txt` (Gymnasium, h5py,
  `robosuite-models` 1.0.0, `usd-core`).
- **Platforms** [3]: Linux and macOS; on macOS the default viewer needs
  `mjpython -m robosuite.demos.demo_random_action`. Windows works with fixes from the docs: create
  `C:\tmp` for the log file, and copy `mujoco.dll` into robosuite's `utils` folder if it is
  not found.
- **GPU:** physics runs on the CPU; no GPU is needed [3]. Camera observations render offscreen
  through EGL on an NVIDIA GPU or OSMesa on the CPU, chosen by `MUJOCO_GL`; on Linux robosuite
  picks EGL unless `MUJOCO_GL` is `osmesa` or `glx` [1]. The docs estimate about 3,500 FPS
  rendering Lift with MuJoCo on an RTX 4090 [6].
- **Photoreal rendering** [6]: `robosuite/scripts/render_dataset_with_omniverse.py` re-renders
  recorded demos in [Isaac Sim](../../tools/isaac-sim.md) (Isaac Sim and Isaac Lab, Linux or
  Windows): about 58 FPS ray-traced, about 2.8 FPS path-traced at 64 samples per pixel, by the
  docs' estimate. The NVISII renderer of 1.4 is gone in 1.5 [1].

## How an agent works with it

```python
import numpy as np
import robosuite as suite
from robosuite import load_composite_controller_config

env = suite.make(
    "Lift", robots="Panda",
    controller_configs=load_composite_controller_config(controller="BASIC"),
    has_renderer=False, has_offscreen_renderer=True, use_camera_obs=True,
    camera_names=["agentview", "robot0_eye_in_hand"], camera_heights=84, camera_widths=84,
    control_freq=20, horizon=400,
)
obs = env.reset()                      # dict: robot0_eef_pos, robot0_eef_quat,
low, high = env.action_spec            # robot0_gripper_qpos, object-state, <camera>_image
obs, reward, done, info = env.step(np.zeros_like(low))
```

- **Defaults** (Lift) [1]: 20 Hz control on a 0.002 s physics step, `horizon=1000`, one
  `agentview` camera at 256 x 256, the `mjviewer` renderer, `lite_physics=True`. With sparse
  rewards (the default) Lift returns 1.0 once the cube is lifted.
- **Controllers** [1][5]: a composite controller drives the body parts. `BASIC` gives each part
  its own controller; `WHOLE_BODY_IK`, `WHOLE_BODY_MINK_IK` and `HYBRID_MOBILE_BASE` serve
  humanoids and mobile manipulators. Part controllers: `OSC_POSE`, `OSC_POSITION`, `IK_POSE`,
  `JOINT_POSITION`, `JOINT_VELOCITY`, `JOINT_TORQUE`.
- **The Panda default** [1][5]: `BASIC` with `OSC_POSE`, delta input in the base frame. Each
  action is 6 numbers in [-1, 1], scaled to at most 0.05 m and 0.5 rad per step, plus one for
  the gripper; stiffness 150, critically damped. Variable-impedance modes add stiffness (12
  numbers) or stiffness and damping (18).
- **Demos** [1]: `robosuite/scripts/collect_human_demonstrations.py --device keyboard` (or
  `spacemouse`, `dualsense`, `mjgui`) records teleoperation to a `demo.hdf5` of MuJoCo states
  and actions; `playback_demonstrations_from_hdf5.py` replays it. [robomimic](robomimic.md)
  converts such files to its format and renders camera observations from the states.
- **Gymnasium:** `GymWrapper(env)` flattens chosen observation keys into one vector; image keys
  are added when cameras are on [1]. See [Gymnasium](gymnasium.md) and
  [Stable-Baselines3](stable-baselines3.md).
- **Check:** run `demo_random_action`, then replay one demo with
  `playback_demonstrations_from_hdf5.py`; a policy is scored by its success rate over rollouts.

## Traps

- **`pip install robosuite` breaks on current MuJoCo.** 1.5.2 asks for `mujoco>=3.3.0` with no
  upper bound [2]. MuJoCo 3.10 (2026-06-22) changed `mj_fullM`, which the controllers call [1][9]:
  on 3.11 the first `step` fails on a missing `qM`, and on 3.12 and later `reset` fails with an
  `AssertionError`; 3.9.0 works [7]. `master` pins `<3.10`, but no release carries the fix [1].
  Tag 1.5.1, which robomimic asks for, has the same unbounded pin [10].
- **Version islands.** LIBERO pins `robosuite==1.4.0` [11]; RoboCasa wants robosuite `master`
  and `mujoco==3.3.1` [12]; robomimic's released datasets want the `v1.5.1` source tag [10].
  They cannot share one environment: use one venv each.
- **Old datasets replay differently.** 1.5 turned on `lite_physics`, which skips redundant
  simulation calls; set `lite_physics=False` for datasets recorded with robosuite 1.4.1 or
  older [1]. 1.5 also moved controller configs into composite controllers; migrate pre-1.5
  JSON files using the changelog's example [1].
- **Upside-down images.** Rendered frames follow OpenGL, so they are vertically flipped against
  OpenCV. `IMAGE_CONVENTION` in `macros.py` (set it in `macros_private.py`, written by
  `python robosuite/scripts/setup_macros.py`) switches to `"opencv"`; train and deploy with the
  same setting [1].
- **Quaternions are (x, y, z, w)** in robosuite's own utilities; MuJoCo uses (w, x, y, z).
  Convert with `robosuite.utils.transform_utils.convert_quat` [1].
- **Delta actions and frames.** OSC actions are deltas in the robot base frame by default.
  For absolute poses set `"input_type": "absolute"` (and `input_ref_frame`) in the part config;
  the docs' `control_delta` flag now applies only to the IK controller in the code [1][5]. A
  question on which frame LIBERO's deltas use is open [8].
- **Mink pin.** 1.5.2 requires `mink==0.0.5` for the whole-body IK controller; `master` made it
  optional [1][2].

## Alternatives

[MuJoCo](../../tools/mujoco.md) alone, [ManiSkill](maniskill.md), [Isaac Lab](isaac-lab.md),
[Genesis](../../tools/genesis.md), [PyBullet](../../tools/pybullet.md); task suites built on it:
[LIBERO](../benchmarks/libero.md), [RoboCasa](../benchmarks/robocasa.md); learning on it:
[robomimic](robomimic.md), [Diffusion Policy](../policies/diffusion-policy.md).

## Sources

1. [robosuite repository: README, LICENSE, setup.py, docs/changelog.md, macros, controller configs, environments, robots, renderers, tags and history](https://github.com/ARISE-Initiative/robosuite), accessed 2026-11-25
2. [PyPI: robosuite release history and 1.5.2 requirements](https://pypi.org/project/robosuite/), accessed 2026-11-25
3. [robosuite docs: Installation](https://robosuite.ai/docs/installation.html), accessed 2026-11-25
4. [robosuite docs: Overview (v1.5)](https://robosuite.ai/docs/overview.html), accessed 2026-11-25
5. [robosuite docs: Controllers](https://robosuite.ai/docs/modules/controllers.html), accessed 2026-11-25
6. [robosuite docs: Renderers](https://robosuite.ai/docs/modules/renderers.html), accessed 2026-11-25
7. [robosuite issue 831: 1.5.2 from PyPI fails with current MuJoCo](https://github.com/ARISE-Initiative/robosuite/issues/831), accessed 2026-11-25
8. [robosuite issues: open issue list](https://github.com/ARISE-Initiative/robosuite/issues), accessed 2026-11-25
9. [PyPI: mujoco release history](https://pypi.org/project/mujoco/), accessed 2026-11-25
10. [robomimic docs: Installation (robosuite v1.5.1 for released datasets)](https://robomimic.github.io/docs/introduction/installation.html), accessed 2026-11-25
11. [LIBERO repository: requirements.txt](https://github.com/Lifelong-Robot-Learning/LIBERO), accessed 2026-11-25
12. [RoboCasa repository: README and setup.py](https://github.com/robocasa/robocasa), accessed 2026-11-25

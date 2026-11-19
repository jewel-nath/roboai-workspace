---
type: tool
name: MuJoCo
summary: Google DeepMind's open-source physics engine for articulated robots in contact, driven from Python or C; the default simulator for robot learning and control research, with MuJoCo Menagerie as the first place to look for a robot's model.
tags: [simulation, physics, contact, mjcf, urdf, python, mjspec, mjx, jax, mujoco-warp, gpu, menagerie, reinforcement-learning, ros2-control, headless]
kind: library
area: sim
support: first-class
license: Apache-2.0
links: {repo: "https://github.com/google-deepmind/mujoco", docs: "https://mujoco.readthedocs.io", site: "https://mujoco.org"}
version: {tested: , latest: 4.0.1, as_of: 2026-11-19}
platforms: [linux, windows, macos]
agent_access: script
registry:
evidence: researched
last_verified: 2026-11-19
sources:
  - {url: "https://github.com/google-deepmind/mujoco", title: "MuJoCo repository: README, LICENSE, release tags and Python rendering backends", accessed: 2026-11-19}
  - {url: "https://mujoco.readthedocs.io/en/stable/changelog.html", title: MuJoCo changelog, accessed: 2026-11-19}
  - {url: "https://mujoco.readthedocs.io/en/stable/python.html", title: "MuJoCo docs: Python bindings", accessed: 2026-11-19}
  - {url: "https://pypi.org/project/mujoco-core/", title: "PyPI: mujoco-core 4.0.1 wheels", accessed: 2026-11-19}
  - {url: "https://mujoco.readthedocs.io/en/stable/modeling.html", title: "MuJoCo docs: Modeling (URDF extensions, model tuning)", accessed: 2026-11-19}
  - {url: "https://mujoco.readthedocs.io/en/stable/XMLreference.html", title: "MuJoCo docs: XML reference", accessed: 2026-11-19}
  - {url: "https://mujoco.readthedocs.io/en/stable/computation/index.html", title: "MuJoCo docs: Computation (collision detection)", accessed: 2026-11-19}
  - {url: "https://mujoco.readthedocs.io/en/stable/mjx.html", title: "MuJoCo docs: MuJoCo XLA (MJX)", accessed: 2026-11-19}
  - {url: "https://mujoco.readthedocs.io/en/stable/mjwarp/index.html", title: "MuJoCo docs: MuJoCo Warp", accessed: 2026-11-19}
  - {url: "https://pypi.org/project/mujoco-warp/", title: "PyPI: mujoco-warp 4.0.1", accessed: 2026-11-19}
  - {url: "https://github.com/google-deepmind/mujoco_menagerie", title: "MuJoCo Menagerie repository: README, model list and CHANGELOG", accessed: 2026-11-19}
  - {url: "https://github.com/ros-controls/mujoco_ros2_control", title: "mujoco_ros2_control repository: README, docs and CHANGELOG", accessed: 2026-11-19}
  - {url: "https://index.ros.org/p/mujoco_ros2_control/", title: "ROS Index: mujoco_ros2_control", accessed: 2026-11-19}
  - {url: "https://github.com/pal-robotics/mujoco_vendor", title: "mujoco_vendor repository: CMakeLists.txt and package.xml", accessed: 2026-11-19}
---

# MuJoCo

MuJoCo (Multi-Joint dynamics with Contact) is a physics engine for articulated bodies in contact,
with a C API and Python bindings [1]. Builders use it to check a robot model, tune controllers, and
train or test learned policies before the hardware exists. Licence Apache-2.0; newest release
4.0.1, 2026-11-11 [1][2]. It is a first-class tool in this workspace.

## When to use it

Use it when contact matters and code drives the simulation: arms and grippers, hands, legged
robots, model-predictive control, reinforcement learning, system identification [1][5]. One scene
steps fastest on the CPU; thousands of parallel scenes go to MJX or MuJoCo Warp on a GPU [8][9].
Look in MuJoCo Menagerie first: a tuned model of your robot may already exist [11]. For a whole
ROS 2 robot in a world full of sensor plugins use [Gazebo](gazebo.md); for photoreal cameras and
large USD scenes, [Isaac Sim](isaac-sim.md). MuJoCo's ROS 2 link is a ros2_control plugin, not a
full bridge [12]. See [Choose a simulator](../guides/choose-a-simulator.md).

## Setup

**Python, Ubuntu 24.04 first.** `pip install mujoco` brings the bindings and the C library; nothing
else to download [3]. 4.0.1 needs Python 3.11 to 3.15, with wheels for Linux x86-64 and aarch64
(glibc 2.28+), Windows x86-64 and Apple-silicon macOS 11+; none for Intel Macs [4]. No GPU needed.

```bash
sudo apt install python3-venv
python3 -m venv ~/venvs/mujoco && source ~/venvs/mujoco/bin/activate
pip install "mujoco==4.0.1"
python -m mujoco.viewer --mjcf=scene.xml   # interactive viewer; without --mjcf, drop a file in
```

- **Packages (4.0+):** `mujoco` is a metapackage of `mujoco-core` (bindings, NumPy only),
  `mujoco-studio` (MuJoCo Studio viewer, Filament renderer), `glfw` and `pyopengl` [2][3]. On a
  training server, `mujoco-core[rendering]` keeps offscreen rendering and `mujoco.viewer` [3].
- **macOS:** a script that opens `viewer.launch_passive` must run under `mjpython`, not `python` [3].
- **C and C++:** release archives for Linux (x86-64, AArch64), Windows (x86-64) and macOS
  (universal) on GitHub Releases, with MuJoCo Studio and the classic `simulate` viewer [1].
- **GPU batches:** `pip install mujoco-mjx` (JAX: NVIDIA or AMD GPUs, Apple silicon, TPUs) or
  `pip install mujoco-warp` (NVIDIA GPUs; CPU only for development and debugging) [8][10].

## How an agent works with it

The `sim-mujoco` skill (a later batch) will hold full recipes. The core loop [3]:

```python
import mujoco
m = mujoco.MjModel.from_xml_path("scene.xml")   # MJCF; a URDF loads too
d = mujoco.MjData(m)                            # state: qpos, qvel, ctrl, sensordata
mujoco.mj_step(m, d, nstep=1000)                # 1000 steps of m.opt.timestep
print(d.time, d.qpos)                           # fields are views: .copy() what you keep
```

- **Files.** MJCF is the native, schema-checked XML [5][6]. Build or edit models in code with
  `mujoco.MjSpec` (`from_file`, add elements, `compile()`, `to_xml()`), not string templates [3].
- **URDF.** Only a subset maps. URDF has no actuators, so a joint's `effort` limit becomes its
  `actuatorfrcrange`; for URDF the compiler discards visuals, fuses links on fixed joints and reads
  radians; mistyped attributes are silently ignored [5][6]. Load it once with a
  `<mujoco><compiler meshdir="..." discardvisual="false"/></mujoco>` block, save as MJCF, add
  actuators and sensors there, and edit the MJCF from then on [5]. Writing the URDF:
  [ros2-robot-description](../../skills/ros2-robot-description/SKILL.md), [URDF](../software/urdf.md).
- **Headless rendering.** Set `MUJOCO_GL` before `import mujoco`: `egl` (GPU, no display), `osmesa`
  (CPU software) or the default `glfw`, which needs a display; `MUJOCO_EGL_DEVICE_ID` picks the GPU.
  `mujoco.Renderer` returns RGB, depth or segmentation arrays [1]; Filament is a second renderer [3].
- **Check the result.** The model compiles; after `nstep=1000`, `d.time` is about
  `1000 * m.opt.timestep` (less means it diverged and auto-reset); `d.warning` counts no
  `mjWARN_BADQACC` [5][6]. The modeling guide lists viewer toggles that expose model bugs (contacts,
  convex hulls, inertia boxes, joint axes) and `testspeed` for headless timing [5].
- **Parallel and GPU.** `mujoco.rollout` spreads CPU rollouts over threads [9]. MJX has two
  backends: MJX-JAX (pure JAX, differentiable; small scenes, TPUs, AMD, Apple) and MJX-Warp
  (`impl='warp'`, not differentiable) [8]. MuJoCo Warp, by Google DeepMind and NVIDIA, is
  Apache-2.0, 4.0.1 and marked Alpha on PyPI; it scales better than MJX on most workloads and
  works with PyTorch [9][10]. Both trade single-scene speed for throughput [8][9].
- **Menagerie.** About 70 curated models (arms, hands, legged robots, humanoids, drones), each with
  `scene.xml`, its own `LICENSE` (all Apache-2.0, BSD or MIT on 2026-11-19), a README with the
  minimum MuJoCo version and how it was made, sometimes an MJX variant [11]. Clone it, or
  `pip install mujoco-menagerie` (2026.11.3), which downloads models on first use and pins them to
  the package version [11]. Example: `robotstudio_so101` for the [SO-101](../robots/so-101.md).
- **ROS 2.** [mujoco_ros2_control](https://github.com/ros-controls/mujoco_ros2_control) is a
  [ros2_control](../software/ros2-control.md) plugin (`mujoco_ros2_control/MujocoSystemInterface`)
  that runs the MJCF in its `mujoco_model` parameter, maps MJCF actuators to position, velocity and
  effort interfaces, and has force-torque, IMU, camera and lidar sensors and a `headless` option
  [12]. 0.1.4 (2026-10-29) is released for Humble, Jazzy, Kilted, Lyrical and Rolling [12][13]:
  `sudo apt install ros-jazzy-mujoco-ros2-control`, then
  `ros2 launch mujoco_ros2_control_demos demo.launch.py` [12]. Its URDF-to-MJCF script is marked
  highly experimental [12]. Controllers: [ros2-control](../../skills/ros2-control/SKILL.md) skill.
- **Upstream agent material.** The repo's `doc/skills/` folder (MuJoCo Agent Skills) holds eight
  guides for coding agents, from Python and model editing to rendering and MJX; since 4.0 the
  Python package ships them with the manual in `mujoco/doc/` [1][2]. Treat them as reference.

## Traps

- **The simulation explodes, jitters or snaps back to the start.** `mjWARN_BADQACC` means it
  diverged, and MuJoCo resets by default [5][6]. Causes: a timestep too large for the stiffness, or
  bodies that start interpenetrating [5]. Defaults are `integrator="Euler"`, `timestep="0.002"` [6].
  Fix model bugs first, then use `implicitfast`, give joints `armature` and light `damping`, and
  pick the timestep: 0.5 to 2 ms for contact-rich grasping, 5 to 15 ms can suit locomotion [5].
- **Grasps slip, feet creep, objects sink.** Defaults are pyramidal friction cones, `impratio` 1
  and `solref` 0.02 s. Start with `cone="elliptic"`, `impratio="10"`, `solref` 0.004 to 0.01 and
  `condim` 4 or 6 on grasp pads; `solref` is clamped to at least twice the timestep, so a longer
  timestep also softens contacts [5]. Stiffening contacts to hide model bugs causes chatter [5].
- **A mesh collides as a solid blob.** Collision uses each mesh's convex hull, so a cup cannot hold
  a ball [6]; show convex hulls in the viewer to see it [5]. Split concave parts into convex pieces
  (CoACD is one tool) or primitives, and keep detailed meshes in a visual-only
  `contype`/`conaffinity` class [5][7]. For MJX-JAX, set `maxhullvert` to 64 or less [8].
- **Rendering fails on a server or in a container** (`glfw` cannot open a window, or "Failed to
  import OpenGL backend"): the default backend needs a display, and `mujoco-core` alone lacks
  `glfw` and `pyopengl` [1][3]. Set `MUJOCO_GL=egl` (NVIDIA) or `osmesa` before the import, install
  `mujoco-core[rendering]`, and give a Docker container GPU graphics access
  ([ops-docker-ci](../../skills/ops-docker-ci/SKILL.md)).
- **The robot is limp or slams into its limits.** A `position` actuator's `kp` defaults to 1, with
  no damping and unlimited force [5][6]. `gear` scales the actuator's length, velocity and force;
  `forcerange` clamps the actuator output before the transmission, `actuatorfrcrange` the total at
  the joint [5][6]. MJCF angles default to degrees; millimetre meshes need `scale` [5]. Set `kp`
  and `forcerange` from the real servo, keep `ctrlrange` inside the joint range, check total mass.
- **A model breaks after an upgrade, or behaves differently in ROS.** Each Menagerie model states
  its minimum MuJoCo version [11]. 4.0.0 removed `composite` and the `cable` plugin, rejects
  duplicate includes, and changed RK4, tendon routing and flex stiffness [2]. mujoco_ros2_control
  runs MuJoCo 3.12.0 from mujoco_vendor 0.1.2, not your pip version [14]. Pin `mujoco` with a
  Menagerie tag (`v2026.11.3`) or `mujoco-menagerie` version, and test on the MuJoCo that runs it.
- **pip installs break around 4.0.** Upgrading a 3.x install in place leaves files missing: run
  `pip uninstall -y mujoco` first [2]. 4.0 dropped Python 3.10 [2], so on Python 3.10 (Ubuntu
  22.04's default) pip quietly installs a 3.x release; check `mujoco.__version__`.

## Alternatives

- [Gazebo](gazebo.md) for whole ROS 2 robots with sensors and worlds; [Isaac Sim](isaac-sim.md),
  NVIDIA's GPU simulator on USD, under Isaac Lab, whose Newton backend can run MuJoCo Warp [10].
- [Genesis](genesis.md), a newer GPU-parallel Python simulator (compare its speed claims on your own
  scene), and [PyBullet](pybullet.md), the Bullet engine's Python simulator.
- Pages to come: mjlab (Isaac Lab's manager-based API on MuJoCo Warp [10]), Drake, MuJoCo MCP
  servers and a CAD-to-MJCF pipeline.

## Sources

1. [MuJoCo repository: README, LICENSE, release tags and Python rendering backends](https://github.com/google-deepmind/mujoco), accessed 2026-11-19
2. [MuJoCo changelog](https://mujoco.readthedocs.io/en/stable/changelog.html), accessed 2026-11-19
3. [MuJoCo docs: Python bindings](https://mujoco.readthedocs.io/en/stable/python.html), accessed 2026-11-19
4. [PyPI: mujoco-core 4.0.1 wheels](https://pypi.org/project/mujoco-core/), accessed 2026-11-19
5. [MuJoCo docs: Modeling (URDF extensions, model tuning)](https://mujoco.readthedocs.io/en/stable/modeling.html), accessed 2026-11-19
6. [MuJoCo docs: XML reference](https://mujoco.readthedocs.io/en/stable/XMLreference.html), accessed 2026-11-19
7. [MuJoCo docs: Computation (collision detection)](https://mujoco.readthedocs.io/en/stable/computation/index.html), accessed 2026-11-19
8. [MuJoCo docs: MuJoCo XLA (MJX)](https://mujoco.readthedocs.io/en/stable/mjx.html), accessed 2026-11-19
9. [MuJoCo docs: MuJoCo Warp](https://mujoco.readthedocs.io/en/stable/mjwarp/index.html), accessed 2026-11-19
10. [PyPI: mujoco-warp 4.0.1](https://pypi.org/project/mujoco-warp/), accessed 2026-11-19
11. [MuJoCo Menagerie repository: README, model list and CHANGELOG](https://github.com/google-deepmind/mujoco_menagerie), accessed 2026-11-19
12. [mujoco_ros2_control repository: README, docs and CHANGELOG](https://github.com/ros-controls/mujoco_ros2_control), accessed 2026-11-19
13. [ROS Index: mujoco_ros2_control](https://index.ros.org/p/mujoco_ros2_control/), accessed 2026-11-19
14. [mujoco_vendor repository: CMakeLists.txt and package.xml](https://github.com/pal-robotics/mujoco_vendor), accessed 2026-11-19

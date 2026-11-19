---
type: tool
name: Isaac Sim
summary: NVIDIA's GPU robot simulator on Omniverse and OpenUSD, with PhysX, RTX-rendered cameras and lidars, Replicator synthetic data and a ROS 2 bridge; the base of Isaac Lab. Its code is Apache-2.0, but it runs only with NVIDIA-licensed components on an RTX GPU.
tags: [simulation, nvidia, omniverse, openusd, usd, physx, newton, rtx, sensors, synthetic-data, replicator, ros2, urdf, mjcf, isaac-lab, sim-to-real]
kind: tool
area: sim
support: documented
license: Apache-2.0
links: {repo: "https://github.com/isaac-sim/IsaacSim", docs: "https://docs.isaacsim.omniverse.nvidia.com/latest/", site: "https://developer.nvidia.com/isaac/sim"}
version: {tested: , latest: 6.2.0, as_of: 2026-11-19}
platforms: [linux, windows]
agent_access: script
registry:
evidence: researched
last_verified: 2026-11-19
sources:
  - {url: "https://github.com/isaac-sim/IsaacSim", title: "IsaacSim repository at v6.2.0: README, LICENSE, releases, extension docs and examples", accessed: 2026-11-19}
  - {url: "https://docs.isaacsim.omniverse.nvidia.com/6.2.0/installation/requirements.html", title: "Isaac Sim 6.2.0: Isaac Sim requirements", accessed: 2026-11-19}
  - {url: "https://docs.isaacsim.omniverse.nvidia.com/6.2.0/installation/install_python.html", title: "Isaac Sim 6.2.0: Python environment installation", accessed: 2026-11-19}
  - {url: "https://docs.isaacsim.omniverse.nvidia.com/6.2.0/installation/install_workstation.html", title: "Isaac Sim 6.2.0: Workstation installation", accessed: 2026-11-19}
  - {url: "https://docs.isaacsim.omniverse.nvidia.com/6.2.0/installation/install_container.html", title: "Isaac Sim 6.2.0: Container installation", accessed: 2026-11-19}
  - {url: "https://docs.isaacsim.omniverse.nvidia.com/6.2.0/installation/install_ros.html", title: "Isaac Sim 6.2.0: ROS 2 installation", accessed: 2026-11-19}
  - {url: "https://docs.isaacsim.omniverse.nvidia.com/6.2.0/installation/accessing_assets.html", title: "Isaac Sim 6.2.0: Accessing assets", accessed: 2026-11-19}
  - {url: "https://docs.isaacsim.omniverse.nvidia.com/6.2.0/common/license-faq.html", title: "Isaac Sim 6.2.0: License FAQ", accessed: 2026-11-19}
  - {url: "https://www.nvidia.com/en-us/agreements/enterprise-software/isaac-sim-additional-software-and-materials-license/", title: NVIDIA Isaac Sim Additional Software and Materials License, accessed: 2026-11-19}
  - {url: "https://docs.omniverse.nvidia.com/dev-guide/latest/common/technical-requirements.html", title: Omniverse technical requirements, accessed: 2026-11-19}
  - {url: "https://docs.isaacsim.omniverse.nvidia.com/6.0.0/overview/release_notes.html", title: "Isaac Sim 6.0.0: Release notes", accessed: 2026-11-19}
  - {url: "https://docs.isaacsim.omniverse.nvidia.com/6.2.0/migration_guides/isaac_sim_6_0/urdf_mjcf_importer_exporter_pipeline.html", title: "Isaac Sim 6.0 migration: URDF, MJCF and robot asset pipeline changes", accessed: 2026-11-19}
  - {url: "https://docs.isaacsim.omniverse.nvidia.com/6.2.0/overview/release_notes.html", title: "Isaac Sim 6.2.0: Release notes", accessed: 2026-11-19}
  - {url: "https://isaac-sim.github.io/IsaacLab/main/source/isaaclab/installation.html", title: Isaac Lab installation, accessed: 2026-11-19}
---

# Isaac Sim

NVIDIA's robot simulator, an Omniverse Kit app whose scenes and robots are OpenUSD files. It runs
GPU PhysX (the default; Newton is experimental since 6.0 [11][13]), renders cameras and lidars with
RTX ray tracing, writes labelled data with Replicator and talks to ROS 2 [1]. Builders use it for
realistic sensors, synthetic images, digital twins, and as the engine under Isaac Lab.

**Licence.** The GitHub code is Apache-2.0, but building or running it needs the Omniverse Kit SDK
and NVIDIA's models and textures, under the Isaac Sim Additional Software and Materials License
[1][9]: NVIDIA GPUs only, Kit only inside Isaac Sim or Isaac Lab, no redistribution [9]. Internal
R&D use is free; NVIDIA AI Enterprise is needed only to ship it with Kit to third parties or run it
as a service for them [8]. pip, container and source installs need a EULA "yes" but no login [1][3][5].

**Newest release:** 6.2.0, 2026-10-14, on Kit SDK 110.4.0; 7.0.0 Alpha 1 is a pre-release [1][13].

| 6.2.0 needs [2] | |
|---|---|
| OS | Ubuntu 24.04 or 22.04 (deprecated), x86_64; Windows 11; aarch64 only on DGX Spark (DGX OS 7) |
| GPU | RTX with RT cores: GeForce RTX 4080 minimum, RTX 5080 good; A40 minimum in a data centre [1] |
| Memory | 16 GB VRAM, 32 GB RAM, 50 GB SSD at minimum |
| Driver, Python | Tested on 595.58.03 (Linux) and 595.97 (Windows); Python 3.12, glibc 2.35+ [3] |
| Not supported | macOS, Windows 10, GPUs without RT cores (A100, H100). No WSL route: the container needs a Linux host, and WSL is only a deprecated home for external ROS 2 nodes [5][6] |

## When to use it

Use it when camera, depth or lidar realism matters, for synthetic data, for training with Isaac
Lab, or for a USD digital twin, and only with a 16 GB RTX card. Otherwise use [MuJoCo](mujoco.md)
for fast contact dynamics on any laptop, or [Gazebo](gazebo.md) for a ROS 2 Jazzy robot with Nav2
or [ros2_control](../software/ros2-control.md). Isaac Lab 3.0 runs without Isaac Sim on Newton
[14]. See [Choose a simulator](../guides/choose-a-simulator.md).

## Setup

**Ubuntu 24.04 with pip**, the best route for scripts and agents [3]:

```bash
python3.12 -m venv ~/isaacsim-env && source ~/isaacsim-env/bin/activate && pip install -U pip
pip install "isaacsim[all,extscache]==6.2.0.0" --extra-index-url https://pypi.nvidia.com
export OMNI_KIT_ACCEPT_EULA=YES             # or answer the prompt on first import
isaacsim isaacsim.exp.compatibility_check   # GPU, driver and memory check; then `isaacsim`
```

Optional: `torch==2.11.0` from the PyTorch `cu128` index. Windows 11: the same, with long paths on [3].

- **Workstation zip** [4]: download `isaac-sim-standalone-6.2.0-linux-x86_64.zip` (or the
  Windows zip) from the docs, unzip to `~/isaacsim`, run `./post_install.sh` and `./isaac-sim.sh`.
  `./python.sh script.py` runs scripts; `isaac-sim.streaming.sh` runs without a window [1].
- **Container** [5]: Linux, Docker and the NVIDIA Container Toolkit. Run
  `nvcr.io/nvidia/isaac-sim:6.2.0` with `--gpus all --network=host -e "ACCEPT_EULA=Y" -u 1234:1234`
  and the page's cache mounts, then `./runheadless.sh -v` for a WebRTC stream. `PRIVACY_CONSENT=Y`
  opts in to data collection; omit it. CI: the [ops-docker-ci](../../skills/ops-docker-ci/SKILL.md) skill.
- **From source** [1]: clone, `git lfs pull`, `./build.sh`; the app lands in `_build/<platform>/release/`.
  Linux needs GCC 11 (12+ unsupported, also on 24.04); Windows needs Visual Studio 2022.
- **Assets** [7]: loaded from NVIDIA's hosted service over HTTPS [2]; Nucleus is not needed [4].
  Offline, download the Assets Complete Pack and set `ISAACSIM_ASSET_ROOT` to its versioned root;
  `isaacsim.storage.native.get_assets_root_path()` gives the root in code.

## How an agent works with it

A standalone Python script is the interface: `python script.py` in the venv, or `./python.sh` in
the zip. Create `SimulationApp` before any other `isaacsim` or `omni` import [1]:

```python
from isaacsim import SimulationApp
app = SimulationApp({"headless": True})   # first: other modules load once Kit runs
import omni.timeline
import isaacsim.core.experimental.utils.stage as stage_utils
from isaacsim.core.experimental.prims import Articulation
stage_utils.create_new_stage()
stage_utils.add_reference_to_stage(usd_path="/abs/robot.usd", path="/World/robot")
robot = Articulation("/World/robot")
omni.timeline.get_timeline_interface().play()
for _ in range(120):
    app.update()                          # one physics and render step
print(robot.get_dof_positions().numpy())  # Warp array to NumPy
app.close()
```

- **API generation.** 6.0 removed the `omni.isaac.*` shims and deprecated `isaacsim.core.api`
  (`World`), `isaacsim.core.prims`, `.utils` and `isaacsim.sensors.*` [11]; use the batched
  `isaacsim.core.experimental.*`, `.simulation_manager` and `isaacsim.sensors.experimental.*` [1].
- **USD and importers** [1][12]: edit scenes with `pxr` and reference robot files into them.
  `URDFImporter(URDFImporterConfig(urdf_path=..., usd_path=..., fix_base=True)).import_urdf()`
  from `isaacsim.asset.importer.urdf` (on `urdf-usd-converter`) returns the USD path;
  `ros_package_paths` resolves `package://`. `fix_base` is tri-state (`None` keeps the file's
  choice), so set it. MJCF: `MJCFImporter(...).import_mjcf()` from `isaacsim.asset.importer.mjcf`.
  Prepare the [URDF](../software/urdf.md) with the
  [ros2-robot-description](../../skills/ros2-robot-description/SKILL.md) skill.
- **ROS 2 bridge** [1][6]: `isaacsim.ros2.bridge` works through OmniGraph nodes (Publish Clock,
  Image, LaserScan, PointCloud, JointState, TF; Subscribe Twist, JointState). Bundled Humble and
  Jazzy libraries, built for Python 3.12, load when no ROS is sourced. Jazzy on 24.04 is
  recommended; Humble on 24.04 is unsupported; Windows 11 uses Jazzy through Pixi. **No Lyrical or
  Kilted** in 6.2 or the 7.0 alpha: an unknown sourced distro falls back to the Jazzy backend as
  experimental, and Lyrical's Ubuntu 26.04 is not supported [1][2]. `isaacsim.ros2.control` runs a
  ros2_control `controller_manager` inside; `isaacsim.ros2.sim_control` serves `simulation_interfaces` [1].
- **Replicator** [1]: a render product, `rep.writers.get("BasicWriter")` with a `DiskBackend`, and
  `rep.orchestrator.step()` per capture; randomise lights, poses and materials ([sim-to-real](../../skills/sim-to-real/SKILL.md)).

**Check the result:** the compatibility check reports "System checking result: PASSED" [5]; the
imported USD opens in `pxr` with the expected joints; with a Publish Clock graph playing,
`ros2 topic echo --once /clock` prints a time [6]; Replicator's output folder fills per capture.

## Traps

- **Driver.** 6.2 was tested on R595 [2]; Omniverse also validates R580 and R620 [10]. Tell: the
  compatibility check fails. Fix: a listed branch, via the `.run` installer on Linux with a new GPU
  [2]; Windows 11 with update KB5074109 needs 582.41+ (R580) or 595.97 for Vulkan [10].
- **First launch looks frozen.** Shader warm-up takes 5 to 10 minutes [4], later starts 10 to 30 s
  [1]. Run `warmup.sh` after installing [1]; in Docker, mount the cache folders or each container
  rebuilds it [5]. For broken settings or caches: `--reset-user`, `clear_caches.sh` [4].
- **VRAM.** 16 GB cards may struggle above 16 megapixels of sensor output per frame [2]. Tell:
  out-of-memory errors or a crash on Play. Fix: fewer or smaller render products, simpler scenes.
- **Python 3.12 only.** Other interpreters find no wheel [3]. Never source Humble's Python 3.10
  setup into the simulator's terminal; build custom ROS messages for Python 3.12 [6].
- **ROS 2 sees no topics.** Match `ROS_DOMAIN_ID` and `RMW_IMPLEMENTATION` on both sides. The Linux
  bundle has [Fast DDS](../software/fast-dds.md) (default) and [Cyclone DDS](../software/cyclone-dds.md),
  not [Zenoh](../software/rmw-zenoh.md) [6]. Containers and remote hosts need `--network=host` and
  a UDP-only Fast DDS profile [5][6]. `use_sim_time` nodes wait for a Publish Clock graph [1].
- **Assets missing.** Tell: empty references, or `get_assets_root_path()` raises `RuntimeError` [1].
  Cause: no internet, a firewall, or a stale `ISAACSIM_ASSET_ROOT`, which overrides all else [7].
  Paths move between releases: 6.2 loads Franka from `/Isaac/Robots_Multiphysics/` [1].
- **Asset licence.** NVIDIA's models and textures may not be redistributed [8][9]: reference them
  from the asset root and never commit them to a public repo. Your own USD files are yours.

## Alternatives

[MuJoCo](mujoco.md) for contact physics without an NVIDIA GPU; [Gazebo](gazebo.md), the ROS 2
simulator (Harmonic with Jazzy); [Genesis](genesis.md), a newer GPU-parallel simulator. Isaac Lab
(on Newton, Isaac Sim optional) and ManiSkill for GPU-parallel robot learning.

## Sources

1. [IsaacSim repository at v6.2.0: README, LICENSE, releases, extension docs and examples](https://github.com/isaac-sim/IsaacSim), accessed 2026-11-19
2. [Isaac Sim 6.2.0: Isaac Sim requirements](https://docs.isaacsim.omniverse.nvidia.com/6.2.0/installation/requirements.html), accessed 2026-11-19
3. [Isaac Sim 6.2.0: Python environment installation](https://docs.isaacsim.omniverse.nvidia.com/6.2.0/installation/install_python.html), accessed 2026-11-19
4. [Isaac Sim 6.2.0: Workstation installation](https://docs.isaacsim.omniverse.nvidia.com/6.2.0/installation/install_workstation.html), accessed 2026-11-19
5. [Isaac Sim 6.2.0: Container installation](https://docs.isaacsim.omniverse.nvidia.com/6.2.0/installation/install_container.html), accessed 2026-11-19
6. [Isaac Sim 6.2.0: ROS 2 installation](https://docs.isaacsim.omniverse.nvidia.com/6.2.0/installation/install_ros.html), accessed 2026-11-19
7. [Isaac Sim 6.2.0: Accessing assets](https://docs.isaacsim.omniverse.nvidia.com/6.2.0/installation/accessing_assets.html), accessed 2026-11-19
8. [Isaac Sim 6.2.0: License FAQ](https://docs.isaacsim.omniverse.nvidia.com/6.2.0/common/license-faq.html), accessed 2026-11-19
9. [NVIDIA Isaac Sim Additional Software and Materials License](https://www.nvidia.com/en-us/agreements/enterprise-software/isaac-sim-additional-software-and-materials-license/), accessed 2026-11-19
10. [Omniverse technical requirements](https://docs.omniverse.nvidia.com/dev-guide/latest/common/technical-requirements.html), accessed 2026-11-19
11. [Isaac Sim 6.0.0: Release notes](https://docs.isaacsim.omniverse.nvidia.com/6.0.0/overview/release_notes.html), accessed 2026-11-19
12. [Isaac Sim 6.0 migration: URDF, MJCF and robot asset pipeline changes](https://docs.isaacsim.omniverse.nvidia.com/6.2.0/migration_guides/isaac_sim_6_0/urdf_mjcf_importer_exporter_pipeline.html), accessed 2026-11-19
13. [Isaac Sim 6.2.0: Release notes](https://docs.isaacsim.omniverse.nvidia.com/6.2.0/overview/release_notes.html), accessed 2026-11-19
14. [Isaac Lab installation](https://isaac-sim.github.io/IsaacLab/main/source/isaaclab/installation.html), accessed 2026-11-19

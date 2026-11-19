---
type: tool
name: Gazebo
summary: The open-source robot simulator paired with ROS 2 (formerly Ignition, not Gazebo Classic); SDF worlds, physics and sensors driven from the gz CLI and ros_gz, with Harmonic as this wiki's Jazzy pairing.
tags: [gazebo, gz-sim, ignition, harmonic, jetty, fortress, ionic, sdf, ros-gz, gz-ros2-control, fuel, simulation, ros2]
kind: tool
area: sim
support: first-class
license: Apache-2.0
links: {repo: "https://github.com/gazebosim/gz-sim", docs: "https://gazebosim.org/docs/latest/", site: "https://gazebosim.org"}
version: {tested: , latest: "Jetty (gz-sim 10.7.0)", as_of: 2026-11-19}
platforms: [linux, windows, macos]
agent_access: cli
registry:
evidence: researched
last_verified: 2026-11-19
sources:
  - {url: "https://gazebosim.org/docs/latest/releases/", title: Gazebo Releases, accessed: 2026-11-19}
  - {url: "https://gazebosim.org/docs/latest/ros_installation/", title: Installing Gazebo with ROS, accessed: 2026-11-19}
  - {url: "https://gazebosim.org/docs/latest/getstarted/", title: Getting Started with Gazebo, accessed: 2026-11-19}
  - {url: "https://gazebosim.org/docs/jetty/install/", title: "Gazebo Jetty installation: overview, Ubuntu, Windows and macOS pages", accessed: 2026-11-19}
  - {url: "https://gazebosim.org/docs/harmonic/install/", title: "Gazebo Harmonic installation: overview, Windows and macOS pages", accessed: 2026-11-19}
  - {url: "https://gazebosim.org/docs/harmonic/troubleshooting/", title: "Gazebo Harmonic: Troubleshooting", accessed: 2026-11-19}
  - {url: "https://gazebosim.org/docs/latest/install_gz11_side_by_side/", title: Installing Gazebo11 side by side with new Gazebo, accessed: 2026-11-19}
  - {url: "https://gazebosim.org/docs/latest/migrating_gazebo_classic_ros2_packages/", title: Migrating ROS 2 packages that use Gazebo Classic, accessed: 2026-11-19}
  - {url: "https://gazebosim.org/docs/harmonic/migration_from_ignition/", title: "Gazebo Harmonic: Migration from Ignition", accessed: 2026-11-19}
  - {url: "https://gazebosim.org/docs/latest/ros2_gz_vendor_pkgs/", title: ROS 2 Gazebo vendor packages, accessed: 2026-11-19}
  - {url: "https://github.com/gazebosim/gz-sim", title: "gz-sim repository: LICENSE, release tags, gz sim and gz model help, SimulationRunner (gz-sim8)", accessed: 2026-11-19}
  - {url: "https://github.com/gazebosim/gz-transport", title: "gz-transport repository: gz topic and gz service CLI, environment variables (gz-transport13)", accessed: 2026-11-19}
  - {url: "https://github.com/gazebosim/sdformat", title: "sdformat repository: gz sdf CLI (sdf14)", accessed: 2026-11-19}
  - {url: "https://github.com/gazebosim/ros_gz", title: "ros_gz repository: README, ros_gz_bridge and ros_gz_sim (jazzy branch)", accessed: 2026-11-19}
---

# Gazebo

Gazebo simulates robots in 3D: physics, sensors (lidar, cameras, IMU, contact) and plugins, with
worlds and models written in SDF. Builders use it to run the same ROS 2 launch files, topics and
controllers they will run on the robot, before the hardware exists. It is Apache-2.0 [11]. Its
Ignition name was dropped in 2022 (announced in April) [9]; the old Gazebo 9 and 11 line is now
called **Gazebo Classic** [8]. The simulator app is Gazebo Sim, run as `gz sim`.

## Releases

| Release | gz-sim | Released | End of life | LTS | ROS 2 pairing | Ubuntu |
|---|---|---|---|---|---|---|
| Fortress | 6 (`ign gazebo`) | Sep 2021 | May 2027 | yes | Humble | 22.04 |
| **Harmonic** | 8 | Sep 2023 | May 2029 | yes | **Jazzy** | 22.04, 24.04 |
| Ionic | 9 | Sep 2024 | Dec 2026 | no | Kilted | 24.04 |
| Jetty | 10 | Sep 2025 | May 2031 | yes | Lyrical | 24.04, 26.04 |

Dates [1], pairings [2], Ubuntu [3], gz-sim majors [4][5][11]. Official support is Ubuntu on
amd64; arm, Windows and macOS are best-effort [4][5]. Use the release paired with your ROS distro:
other pairs (Harmonic on Humble, Kilted or Lyrical) take extra work and block the official ROS
packages that depend on Gazebo [2]. Gazebo suggests Lyrical and Jetty on Ubuntu 26.04 for new
users, else Jazzy and Harmonic on 24.04 [2]. **Newest:** Jetty at gz-sim 10.7.0 (tagged
November 2026); Harmonic is at 8.15.0 (August 2026) [11]. Next is "M" (March 2027 to December 2028);
Rotary is the nightly rolling stream that ROS 2 Rolling tracks [1][2].

**Gazebo Classic** (`gazebo11`, `gzserver`, `gazebo_ros_pkgs`) reached end of life in January
2025; Ubuntu 22.04 was its last platform [7]. Both lines ship a `gz` tool, so installing
`gz-harmonic` removes Classic [7]. To migrate: swap `gazebo_ros_pkgs` for `ros_gz_sim`,
`ros_gz_bridge` and `ros_gz_image`; load the Physics, UserCommands, SceneBroadcaster and Sensors
systems in each world; replace `libgazebo_ros_*.so` plugins with Gazebo systems (DiffDrive,
JointStatePublisher) and bridged topics [8], and `gazebo_ros2_control` with `gz_ros2_control`.
Steps: the [sim-gazebo](../../skills/sim-gazebo/SKILL.md) skill.

## When to use it

Use it when the robot runs ROS 2 and the sim must exercise the real stack: mobile bases with
lidar, cameras and IMU, arms through `gz_ros2_control`, several robots in one world;
[TurtleBot3](../robots/turtlebot3.md) and [TurtleBot 4](../robots/turtlebot.md) ship Gazebo twins.
Choose [MuJoCo](mujoco.md) for contact-rich manipulation and learning loops, [Isaac Sim](isaac-sim.md)
for photoreal cameras, [Webots](webots.md) for teaching or Windows and macOS.

## Setup

**Ubuntu 24.04, Jazzy (the official path):** since Jazzy, Gazebo comes from packages.ros.org as
ROS vendor packages, so the [ROS 2](ros2.md) apt source is all you need [2][10]:

```bash
sudo apt install ros-jazzy-ros-gz            # ros_gz plus Gazebo Harmonic
sudo apt install ros-jazzy-gz-ros2-control   # only with ros2_control
source /opt/ros/jazzy/setup.bash             # puts gz on PATH
gz sim -v 4 shapes.sdf                       # GUI smoke test
```

- **packages.osrfoundation.org** (`gz-harmonic`, `gz-jetty`) gets patches first; it may sit beside
  the ROS source, or serve alone without ROS [2][4]. Jetty's `gz-sim10-server` has no Qt or X11,
  for CI; run `/usr/libexec/gz/sim10/gz-sim-server world.sdf`, not `gz sim -s` [4].
- **GPU:** the GUI, cameras and GPU lidars render with Ogre 2, which needs OpenGL above 3.3,
  preferably 4.3+; check with `glxinfo | grep "OpenGL version"` [6].
- **Windows** (experimental [4][5]; runtime issues [3]): Pixi from conda-forge, `gz-sim = "8.*"`
  for Harmonic (Windows 10/11; server and GUI in two shells) or `"10.*"` for Jetty (Windows 11;
  always pass a world file) [4][5]. For ROS 2, use Ubuntu, in a VM if needed [2].
- **macOS:** `brew tap osrf/simulation`, then `brew install gz-harmonic` or `gz-jetty`; bottles
  only for Sequoia on Apple silicon, else a long source build [4][5]. Run `gz sim -s` and
  `gz sim -g` in two terminals; the GUI is "currently known to be unstable" [3].

## How an agent works with it

Procedures: [sim-gazebo](../../skills/sim-gazebo/SKILL.md); URDF preparation (inertials, `<gazebo>`
tags, sensors): [ros2-robot-description](../../skills/ros2-robot-description/SKILL.md). Worlds and
models are SDF; a URDF is converted by sdformat on spawn [13][14]. Gazebo searches
`GZ_SIM_RESOURCE_PATH` for worlds, models, meshes, `GZ_SIM_SYSTEM_PLUGIN_PATH` for plugins; DART is the
default physics [11]. Fuel (app.gazebosim.org/fuel) models go in as `<include>` snippets [3].

| To | Command |
|---|---|
| Run with GUI, headless | `gz sim -v 4 world.sdf`; `gz sim -s -r -v 4 world.sdf` |
| Bounded CI run | `gz sim -s -r --iterations 5000 world.sdf` exits after 5000 steps; add `--headless-rendering` for sensors without a display [11] |
| Validate SDF, see a URDF's conversion | `gz sdf -k world.sdf`; `gz sdf -p robot.urdf`; `gz sdf --inertial-stats model.sdf` [13] |
| Topics, services | `gz topic -l`; `gz topic -e -t /clock -n 1`; `gz topic -f -t /scan` (rate); `gz topic -t /cmd_vel -m gz.msgs.Twist -p "linear: {x: 0.2}"`; `gz service -l` [12] |
| Models | `gz model --list`; `gz model -m my_robot -p` (pose); `-j` joints, `-l` links [11] |

**ROS 2 (`ros_gz`)** branches: `humble` (Fortress), `jazzy` (Harmonic), `kilted` (Ionic), `lyrical`
(Jetty) and `ros2` (Rolling), all on packages.ros.org [14].

```bash
ros2 launch ros_gz_sim gz_sim.launch.py gz_args:="-r -s -v 3 my_world.sdf" on_exit_shutdown:=true
ros2 run ros_gz_sim create -topic robot_description -name my_robot -z 0.1
ros2 run ros_gz_bridge parameter_bridge /clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock \
  /scan@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan /cmd_vel@geometry_msgs/msg/Twist]gz.msgs.Twist
```

- Without `on_exit_shutdown:=true`, launch keeps running after Gazebo closes. `create` also takes
  `-file`, `-param`, `-string`, `-x -y -z -R -P -Y`. Bridge: `[` Gazebo to ROS, `]` ROS to Gazebo,
  `@` both; many topics go in a YAML `config_file` (`direction`, `lazy`, `qos_profile`); only the
  type pairs in its README bridge [14]. `gz_ros2_control`: the [ros2-control](../../skills/ros2-control/SKILL.md) skill.
- **Time:** Gazebo owns the clock. Bridge `/clock` one way; `use_sim_time: true` on every node [14].
- **Checks:** `gz sdf -k` passes; a bounded run exits 0 without `[Err]` lines; `gz model -m my_robot
  -p` gives a sane pose; sensor rates match their `update_rate`; `/clock` advances.

## Traps

- **Invisible robot, "Unable to find file":** meshes are off `GZ_SIM_RESOURCE_PATH`. Export
  `<gazebo_ros gazebo_model_path="${prefix}/../"/>` in `package.xml`; `gz_sim.launch.py` applies it
  only to its own Gazebo, so a hand-run `gz sim` needs `$(ros2 pkg prefix <pkg>)/share` added [14].
- **"Unable to create the rendering window", black window:** read `~/.gz/rendering/ogre2.log`;
  update drivers; dual-GPU laptops `sudo prime-select nvidia`; Wayland `QT_QPA_PLATFORM=xcb`; VMs
  `LIBGL_ALWAYS_SOFTWARE=1` (slow) or `--render-engine ogre` [6]. WSL 2 is not an official
  platform [4][5]. In containers, pass the GPU through ([ops-docker-ci](../../skills/ops-docker-ci/SKILL.md)).
- **Robot never moves, TF stale, "extrapolation into the future":** no clock. Bridge `/clock`
  with `[`, not `@`: a two-way bridge up first is a second `/clock` publisher, so Gazebo publishes
  only `/world/<name>/clock` [14]. Set `use_sim_time` on every node.
- **Real-time factor below 1** (GUI, or the world's `stats` topic): lower sensor rates and
  resolutions; run server-only. For batch CI, `<real_time_factor>0</real_time_factor>` in the world
  runs unthrottled; setting 0 at runtime is ignored [11]. Wall-clock timers in nodes misbehave.
- **`ign` vs `gz`:** Fortress uses `ign gazebo`, `IGN_GAZEBO_RESOURCE_PATH` and `ignition.msgs.*`
  [3][9]. Harmonic and Jetty install no `ign`; Harmonic accepts most `ign` names with deprecation
  warnings [9]; `gz_args` replaces `ign_args` [14]. Translate 2021-2022 tutorials.
- **Mixed apt sources or pairings:** apt offers to remove packages, or `gz sim --versions` lists
  two. `ros-humble-ros-gzharmonic` conflicts with `ros-humble-ros-gz*` [2]; `gz-harmonic` removes
  Classic [7]. Keep one pairing per machine, or one container per distro. **`gz: command not
  found`:** source `/opt/ros/jazzy/setup.bash`, home of the vendored `gz` [10].
- **Parallel runs share topics:** the default partition is `<hostname>:<username>`; set a distinct
  `GZ_PARTITION` per run (and `ROS_DOMAIN_ID`); `GZ_IP` picks the interface [12]. A GUI that waits
  forever for the world list needs multicast [6].

## Alternatives

[MuJoCo](mujoco.md), [Isaac Sim](isaac-sim.md), [Webots](webots.md), [CoppeliaSim](coppeliasim.md),
[PyBullet](pybullet.md), [Genesis](genesis.md), [CARLA](carla.md) (driving) and [Habitat](habitat.md)
(embodied AI); compared in [Choose a simulator](../guides/choose-a-simulator.md).

## Sources

1. [Gazebo Releases](https://gazebosim.org/docs/latest/releases/), accessed 2026-11-19
2. [Installing Gazebo with ROS](https://gazebosim.org/docs/latest/ros_installation/), accessed 2026-11-19
3. [Getting Started with Gazebo](https://gazebosim.org/docs/latest/getstarted/), accessed 2026-11-19
4. [Gazebo Jetty installation: overview, Ubuntu, Windows and macOS pages](https://gazebosim.org/docs/jetty/install/), accessed 2026-11-19
5. [Gazebo Harmonic installation: overview, Windows and macOS pages](https://gazebosim.org/docs/harmonic/install/), accessed 2026-11-19
6. [Gazebo Harmonic: Troubleshooting](https://gazebosim.org/docs/harmonic/troubleshooting/), accessed 2026-11-19
7. [Installing Gazebo11 side by side with new Gazebo](https://gazebosim.org/docs/latest/install_gz11_side_by_side/), accessed 2026-11-19
8. [Migrating ROS 2 packages that use Gazebo Classic](https://gazebosim.org/docs/latest/migrating_gazebo_classic_ros2_packages/), accessed 2026-11-19
9. [Gazebo Harmonic: Migration from Ignition](https://gazebosim.org/docs/harmonic/migration_from_ignition/), accessed 2026-11-19
10. [ROS 2 Gazebo vendor packages](https://gazebosim.org/docs/latest/ros2_gz_vendor_pkgs/), accessed 2026-11-19
11. [gz-sim repository: LICENSE, release tags, gz sim and gz model help, SimulationRunner (gz-sim8)](https://github.com/gazebosim/gz-sim), accessed 2026-11-19
12. [gz-transport repository: gz topic and gz service CLI, environment variables (gz-transport13)](https://github.com/gazebosim/gz-transport), accessed 2026-11-19
13. [sdformat repository: gz sdf CLI (sdf14)](https://github.com/gazebosim/sdformat), accessed 2026-11-19
14. [ros_gz repository: README, ros_gz_bridge and ros_gz_sim (jazzy branch)](https://github.com/gazebosim/ros_gz), accessed 2026-11-19

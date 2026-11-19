---
type: tool
name: ROS 2
summary: The Robot Operating System 2, the open framework of middleware, tools and libraries that runs a robot as communicating nodes; this wiki defaults to the Jazzy Jalisco LTS on Ubuntu 24.04.
tags: [ros2, jazzy, lyrical, humble, middleware, rmw, dds, qos, rclcpp, rclpy, rosbag2, mcap, rviz, cli]
kind: framework
area: ros2
support: first-class
license: Apache-2.0
links: {repo: "https://github.com/ros2/ros2", docs: "https://docs.ros.org/en/jazzy/", site: "https://www.ros.org"}
version: {tested: , latest: Lyrical Luth, as_of: 2026-11-18}
platforms: [linux, windows, macos]
agent_access: cli
registry:
evidence: researched
last_verified: 2026-11-18
sources:
  - {url: "https://docs.ros.org/en/rolling/Releases.html", title: ROS 2 Distributions, accessed: 2026-11-18}
  - {url: "https://reps.openrobotics.org/rep-2000/", title: "REP 2000: ROS 2 Releases and Target Platforms", accessed: 2026-11-18}
  - {url: "https://docs.ros.org/en/lyrical/Releases/lyrical/supported-platforms.html", title: Lyrical Luth Supported Platforms, accessed: 2026-11-18}
  - {url: "https://docs.ros.org/en/rolling/Get-Started/Installation.html", title: ROS 2 Rolling installation overview, accessed: 2026-11-18}
  - {url: "https://docs.ros.org/en/jazzy/Installation/Ubuntu-Install-Debs.html", title: "Jazzy: Ubuntu (deb packages)", accessed: 2026-11-18}
  - {url: "https://docs.ros.org/en/jazzy/Installation/Windows-Install-Binary.html", title: "Jazzy: Windows (binary)", accessed: 2026-11-18}
  - {url: "https://robostack.github.io/GettingStarted.html", title: RoboStack Getting Started, accessed: 2026-11-18}
  - {url: "https://docs.ros.org/en/rolling/Releases/Release-Iron-Irwini.html", title: Iron Irwini release notes, accessed: 2026-11-18}
  - {url: "https://github.com/ros2/rosbag2/blob/jazzy/README.md", title: rosbag2 README (jazzy branch), accessed: 2026-11-18}
  - {url: "https://docs.ros.org/en/rolling/Releases/Release-Lyrical-Luth.html", title: Lyrical Luth release notes, accessed: 2026-11-18}
  - {url: "https://docs.ros.org/en/jazzy/Concepts/Intermediate/About-Quality-of-Service-Settings.html", title: "Jazzy: Quality of Service settings", accessed: 2026-11-18}
  - {url: "https://docs.ros.org/en/jazzy/Concepts/Basic/About-Command-Line-Tools.html", title: "Jazzy: Introspection with command line tools", accessed: 2026-11-18}
  - {url: "https://docs.ros.org/en/jazzy/How-To-Guides/Installation-Troubleshooting.html", title: "Jazzy: Installation troubleshooting", accessed: 2026-11-18}
  - {url: "https://github.com/ros2/rclcpp/blob/rolling/LICENSE", title: rclcpp LICENSE, accessed: 2026-11-18}
---

# ROS 2

ROS 2 runs a robot as a set of nodes (programs) that exchange typed messages, plus the build tool,
CLI, recorder and visualiser around them. Builders use it to wire drivers, control, perception,
navigation and manipulation together and to reuse maintained packages. This wiki defaults to
**Jazzy Jalisco**, the LTS release for Ubuntu 24.04 [1][2].

*Topics* stream messages from publishers to subscribers, *services* are request-reply calls,
*actions* are long goals with feedback and cancel, *parameters* are per-node settings, and *launch*
files start many nodes at once. Each publisher and subscription has a *QoS* profile (reliability,
durability, history depth); only compatible profiles connect [11]. The *RMW* layer maps ROS onto a
middleware: Fast DDS by default; Cyclone DDS, Connext and, from Kilted, Zenoh are Tier 1 too [2][3]
(see [Choose a ROS 2 middleware](../guides/choose-a-ros2-middleware.md)). Core packages such as
rclcpp are Apache-2.0 [14]; others use BSD and other licences, so check each `package.xml`.

## Distributions

| Distro | Released | End of life | Ubuntu | Tier 1 platforms |
|---|---|---|---|---|
| Humble Hawksbill (LTS) | 2022-05-23 | May 2027 | 22.04 | Ubuntu 22.04 amd64 and arm64; Windows 10 amd64 |
| **Jazzy Jalisco (LTS)** | 2024-05-23 | May 2029 | 24.04 | Ubuntu 24.04 amd64 and arm64; Windows 10 (VS 2019) amd64 |
| Kilted Kaiju | 2025-05-23 | December 2026 (REP 2000: November) | 24.04 | Same as Jazzy |
| Lyrical Luth (LTS) | 2026-05-22 | May 2031 | 26.04 | Ubuntu 26.04 amd64 and arm64; Windows 11 (VS 2022) amd64 |
| Rolling Ridley | Continuous since June 2020 | None | 26.04 | Binaries for Ubuntu 26.04, RHEL 10 and Windows 11 |

Dates from [1], platforms from [2][3][4]. Tier 1: binaries and full CI; Tier 3: source builds [2].

- **Jazzy:** RHEL 9 is Tier 2; Ubuntu 22.04, macOS and Debian 12 are Tier 3 [2].
- **Lyrical differs:** Ubuntu 24.04 is only Tier 3, so Lyrical means Ubuntu 26.04 or a source
  build; it needs C++20 and Python 3.12 to 3.14 [3]. Its CLI gets or sets several parameters in one
  call and adds `ros2 service info --verbose` [10].
- **Humble** only when a driver you need has no Jazzy release; it ends in May 2027. **Kilted** ends
  within weeks: do not start on it. **Rolling** breaks in place and is for package maintainers [1].
- Nodes from different distros are not guaranteed to talk: keep robot and base station on one [1].

## When to use it

Use it when the robot has several sensors and actuators, or needs navigation (Nav2), manipulation
(MoveIt 2), [ros2_control](../software/ros2-control.md) hardware interfaces, a robot model
([URDF](../software/urdf.md), [tf2](../software/tf2.md)) or recording and replay of every signal.
Use something else for a single-microcontroller project, a hard real-time loop (keep it in firmware
and bridge it), or an arm that LeRobot drives without ROS, like the [SO-101](../robots/so-101.md).

## Setup

**Ubuntu 24.04, Jazzy** [5]: enable Universe and install `ros2-apt-source` with the commands on the
install page. Check that `/etc/apt/sources.list.d/ubuntu.sources` lists
`noble noble-updates noble-backports`: some 24.04 installs have only `noble`, which breaks the
`ros-dev-tools` install. On a Raspberry Pi, use 64-bit Ubuntu (arm64 is Tier 1 [2]).
`desktop` adds RViz, demos and tutorials; `ros-base` is libraries, messages and CLI tools [5].

```bash
sudo apt update && sudo apt install ros-dev-tools
sudo apt install ros-jazzy-desktop     # ros-jazzy-ros-base on a robot without a screen
source /opt/ros/jazzy/setup.bash       # in every new shell, or in ~/.bashrc
ros2 run demo_nodes_cpp talker         # second shell: ros2 run demo_nodes_py listener
```

**Windows 10** (Jazzy): unzip `ros2-jazzy-*-windows-release-amd64.zip` from the ros2/ros2
releases, install dependencies with [Pixi](pixi.md) from the docs' `pixi.toml` into `C:\pixi_ws`
(the binaries are not relocatable), then run `pixi shell` and
`call C:\pixi_ws\ros2-windows\local_setup.bat` in each prompt. It holds ros-base and part of
desktop; build your C++ packages as Release or RelWithDebInfo to match [6].

**macOS** is Tier 3, source build only [2]. **RoboStack** ships ROS on conda-forge for Pixi, on
Linux (x86-64, aarch64), Windows (with VS 2022) and macOS 14 or newer, one channel per distro from
`robostack-humble` to `robostack-rolling`; on macOS, set the platform as the page shows [7]. Docker
and CI: see the [ops-docker-ci](../../skills/ops-docker-ci/SKILL.md) skill. RoboStack on Jazzy:

```bash
pixi init ros_ws -c https://prefix.dev/robostack-jazzy -c https://prefix.dev/conda-forge
cd ros_ws && pixi add ros-jazzy-desktop && pixi run rviz2
```

**Recording:** `ros2 bag` writes MCAP by default since Iron; sqlite3 is still available [8][9]. It
compresses with zstd, splits by size (`-b`) or duration (`-d`), and `--snapshot-mode` keeps a ring
buffer in memory until its `~/snapshot` service is called [9]. Open bags in [Foxglove](foxglove.md)
or [PlotJuggler](plotjuggler.md). **Viewing:** RViz (`rviz2`, in the desktop variant [5]) shows the
robot model, TF frames, sensor data and markers in 3D.

## How an agent works with it

Recipes are in the [ros2-core](../../skills/ros2-core/SKILL.md) skill. Ground rules:

- Agent shells often start fresh: prefix commands with `source /opt/ros/jazzy/setup.bash &&`, plus
  `source install/setup.bash &&` inside a workspace.
- Check the setup first: `printenv | grep -E '^(ROS|RMW)_'` and `ros2 doctor --report`.
- `topic echo`, `hz`, `bw` and `pub` run until stopped: add `--once` or wrap them in `timeout 10`.
- Publishing to command topics (`/cmd_vel`, joint commands) moves real hardware: confirm it is safe.

| To | Command |
|---|---|
| Inspect nodes | `ros2 node list`; `ros2 node info /driver` |
| Topics, types, QoS | `ros2 topic list -t`; `ros2 topic info -v /scan` |
| Read, rate, bandwidth | `ros2 topic echo --once /odom`; `timeout 10 ros2 topic hz /scan` (or `bw`) |
| Publish a test message | `ros2 topic pub --once /cmd_vel geometry_msgs/msg/Twist "{linear: {x: 0.1}}"` |
| Services | `ros2 service list -t`; `ros2 service call /reset std_srvs/srv/Empty` |
| Actions | `ros2 action list -t`; `ros2 action send_goal --feedback /move <type> "<goal yaml>"` |
| Parameters | `ros2 param list /driver`; `ros2 param get /driver port`; `ros2 param set /driver rate 50`; `ros2 param dump /driver > driver.yaml` |
| Interfaces, packages | `ros2 interface show sensor_msgs/msg/LaserScan`; `ros2 pkg executables my_robot`; `ros2 pkg prefix my_robot` |
| Run, launch | `ros2 run my_robot driver --ros-args -p port:=/dev/ttyUSB0 -r cmd_vel:=/base/cmd_vel`; `ros2 launch my_robot bringup.launch.py --show-args` |
| Record, inspect, replay | `ros2 bag record -o run1 /scan /odom /tf`; `ros2 bag info run1`; `ros2 bag play run1` |
| Test multicast | `ros2 multicast receive` on one machine, `ros2 multicast send` on the other [13] |
| Build and test | `colcon build --symlink-install --packages-up-to my_robot`; `colcon test`; `colcon test-result --verbose` ([colcon](colcon.md)) |

## Traps

- **"Package not found", or the wrong version runs:** the shell is unsourced or has two distros
  sourced. Open a clean shell; source one `/opt/ros/<distro>/setup.bash`, then the overlay.
- **A subscriber gets nothing and no error shows:** QoS mismatch. Defaults are keep-last 10,
  reliable, volatile; the sensor-data profile is best effort, and a reliable subscription does not
  connect to a best-effort publisher [11]. Compare both sides with `ros2 topic info -v`.
- **Two machines do not see each other:** set the same `ROS_DOMAIN_ID` and RMW on both (mixed
  vendors are not guaranteed [1]); test with `ros2 multicast`; open the firewall for multicast [13].
- **`ROS_LOCALHOST_ONLY` is deprecated** since Iron: use `ROS_AUTOMATIC_DISCOVERY_RANGE` (`SUBNET`
  default, `LOCALHOST`, `OFF`, `SYSTEM_DEFAULT`) and `ROS_STATIC_PEERS` [8].
- **`ros2 topic list` shows dead topics or misses new ones:** the CLI daemon caches the graph. Run
  `ros2 daemon stop` with the same `ROS_DOMAIN_ID` set; each domain has its own daemon [12].
- **RoboStack and apt ROS in one shell:** never source an apt-installed ROS inside a Pixi or conda
  environment; they interfere [7].

## Alternatives

- **ROS 1:** only to maintain old robots. **No framework:** a Python script over serial, or
  LeRobot for learning-first arms; simpler, but you write drivers, logging and viewers yourself.
- **micro-ROS** puts ROS 2 nodes on microcontrollers; **dora-rs** is a Rust dataflow framework.
- Choices inside ROS 2: middleware ([Fast DDS](../software/fast-dds.md),
  [Cyclone DDS](../software/cyclone-dds.md), [Zenoh](../software/rmw-zenoh.md)), web bridge
  ([rosbridge_suite](../software/rosbridge-suite.md)), viewers ([Foxglove](foxglove.md),
  [Rerun](rerun.md), [PlotJuggler](plotjuggler.md)).

## Sources

1. [ROS 2 Distributions](https://docs.ros.org/en/rolling/Releases.html), accessed 2026-11-18
2. [REP 2000: ROS 2 Releases and Target Platforms](https://reps.openrobotics.org/rep-2000/), accessed 2026-11-18
3. [Lyrical Luth Supported Platforms](https://docs.ros.org/en/lyrical/Releases/lyrical/supported-platforms.html), accessed 2026-11-18
4. [ROS 2 Rolling installation overview](https://docs.ros.org/en/rolling/Get-Started/Installation.html), accessed 2026-11-18
5. [Jazzy: Ubuntu (deb packages)](https://docs.ros.org/en/jazzy/Installation/Ubuntu-Install-Debs.html), accessed 2026-11-18
6. [Jazzy: Windows (binary)](https://docs.ros.org/en/jazzy/Installation/Windows-Install-Binary.html), accessed 2026-11-18
7. [RoboStack Getting Started](https://robostack.github.io/GettingStarted.html), accessed 2026-11-18
8. [Iron Irwini release notes](https://docs.ros.org/en/rolling/Releases/Release-Iron-Irwini.html), accessed 2026-11-18
9. [rosbag2 README (jazzy branch)](https://github.com/ros2/rosbag2/blob/jazzy/README.md), accessed 2026-11-18
10. [Lyrical Luth release notes](https://docs.ros.org/en/rolling/Releases/Release-Lyrical-Luth.html), accessed 2026-11-18
11. [Jazzy: Quality of Service settings](https://docs.ros.org/en/jazzy/Concepts/Intermediate/About-Quality-of-Service-Settings.html), accessed 2026-11-18
12. [Jazzy: Introspection with command line tools](https://docs.ros.org/en/jazzy/Concepts/Basic/About-Command-Line-Tools.html), accessed 2026-11-18
13. [Jazzy: Installation troubleshooting](https://docs.ros.org/en/jazzy/How-To-Guides/Installation-Troubleshooting.html), accessed 2026-11-18
14. [rclcpp LICENSE](https://github.com/ros2/rclcpp/blob/rolling/LICENSE), accessed 2026-11-18

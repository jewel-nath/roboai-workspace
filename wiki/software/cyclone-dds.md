---
type: tool
name: Cyclone DDS
summary: Eclipse's open-source DDS implementation and, as rmw_cyclonedds_cpp, a Tier 1 alternative ROS 2 middleware in every current distro; one CYCLONEDDS_URI setting picks the network interface, and robot SDKs such as Unitree's speak it.
tags: [ros2, middleware, rmw, dds, rtps, rmw-cyclonedds, eclipse, cyclonedds-uri, multi-machine, unitree]
kind: library
area: ros2
support:
license: EPL-2.0 OR BSD-3-Clause
links: {repo: "https://github.com/eclipse-cyclonedds/cyclonedds", docs: "https://cyclonedds.io/docs/", site: "https://projects.eclipse.org/projects/iot.cyclonedds"}
version: {tested: , latest: 11.1.0, as_of: 2026-11-18}
platforms: [linux, windows, macos]
agent_access: cli
registry:
evidence: researched
last_verified: 2026-11-18
sources:
  - {url: "https://github.com/eclipse-cyclonedds/cyclonedds", title: "Cyclone DDS repository: README, LICENSE, package.xml and release notes", accessed: 2026-11-18}
  - {url: "https://cyclonedds.io/docs/cyclonedds/latest/config/index.html", title: "Cyclone DDS manual: configuration (network interfaces, multicasting, discovery)", accessed: 2026-11-18}
  - {url: "https://github.com/ros2/rmw_cyclonedds", title: "rmw_cyclonedds README and rmw_node.cpp (jazzy branch)", accessed: 2026-11-18}
  - {url: "https://docs.ros.org/en/jazzy/How-To-Guides/DDS-tuning.html", title: "ROS 2 docs: Addressing common DDS tuning issues", accessed: 2026-11-18}
  - {url: "https://reps.openrobotics.org/rep-2000/", title: "REP 2000: ROS 2 Releases and Target Platforms", accessed: 2026-11-18}
  - {url: "https://docs.ros.org/en/lyrical/Releases/lyrical/supported-platforms.html", title: Lyrical Luth supported platforms and middleware, accessed: 2026-11-18}
  - {url: "https://github.com/ros/rosdistro", title: "rosdistro distribution files: humble, jazzy, kilted, lyrical", accessed: 2026-11-18}
  - {url: "https://github.com/unitreerobotics/unitree_ros2", title: unitree_ros2 README, accessed: 2026-11-18}
---

# Cyclone DDS

Eclipse's open-source DDS implementation, plugged into [ROS 2](../tools/ros2.md) by
`rmw_cyclonedds_cpp`. It is Tier 1 in Humble, Jazzy, Kilted and Lyrical but not the default;
Galactic was the one distro that shipped it as default [5][6]. Builders pick it to match a robot
SDK that speaks it, or for its single-file configuration.

## When to use it

- The robot's SDK runs on it: Unitree's SDK2 talks Cyclone DDS, and unitree_ros2 asks for
  `rmw_cyclonedds_cpp` with the robot-facing interface named in `CYCLONEDDS_URI` [8]
  ([Unitree Go2](../robots/unitree-go2.md)).
- You want one XML file to set the network interface, unicast peers and buffers [2].
- Otherwise the default [Fast DDS](fast-dds.md) is fine; for Wi-Fi or several networks read
  [Choose a ROS 2 middleware](../guides/choose-a-ros2-middleware.md).

## Setup

```bash
sudo apt install ros-jazzy-rmw-cyclonedds-cpp
export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
ros2 doctor --report      # confirms the RMW in use
# Optional: pin the interface; CYCLONEDDS_URI also takes file:///path/to/cyclonedds.xml
export CYCLONEDDS_URI='<CycloneDDS><Domain><General><Interfaces><NetworkInterface name="eth0"/></Interfaces></General></Domain></CycloneDDS>'
```

Jazzy ships Cyclone DDS 0.10.5 with rmw_cyclonedds 2.2.4, Lyrical 11.0.1 with 4.1.6 [7]. Upstream
jumped from 0.10 to 11.0.0 in February 2026 and released 11.1.0 in November 2026 [1]. Unitree pins
0.10.2 [8]; we did not test it against Lyrical's 11.0, so check before you upgrade. Cyclone is
EPL-2.0 or EDL-1.0 (BSD-3-Clause); rmw_cyclonedds is Apache-2.0 [1][3].

## Traps

- **Remote nodes invisible.** Cyclone uses a single network interface by default, ranked by
  address type, which may not be the one your other machines are on. Name it as in Setup [2].
- **Large messages drop or lag, even on a wired network.** The kernel receive buffer fills. Raise
  it (`sudo sysctl -w net.core.rmem_max=8388608 net.core.rmem_default=8388608`) and set
  `<Internal><SocketReceiveBufferSize min="10MB"/></Internal>` [3][4].
- **No discovery where multicast is blocked.** List the hosts with `ROS_STATIC_PEERS` or
  `<Discovery><Peers>` [3][2]. If multicast only misbehaves for data,
  `<AllowMulticast>spdp</AllowMulticast>` keeps it for discovery alone [2].
- **Peers miss some processes.** With unicast peers each host is probed for a fixed range of
  participant indices, about one per ROS process; rmw_cyclonedds allows 32. In your own
  `<Peers>` config, set `<ParticipantIndex>auto` and raise `<MaxAutoParticipantIndex>` [3][2].
- **Still stuck.** Run `ddsperf sanity` on both machines (a mean above 100000 µs means network
  trouble), or trace with `CYCLONEDDS_URI='<Tracing><Verbosity>trace</><Out>stderr</></>'` [3].

## Alternatives

- [Fast DDS](fast-dds.md), the default, and [rmw_zenoh](rmw-zenoh.md) are Tier 1 in Lyrical; so is
  RTI Connext DDS, except on arm64 [6].

## Sources

1. [Cyclone DDS repository: README, LICENSE, package.xml and release notes](https://github.com/eclipse-cyclonedds/cyclonedds), accessed 2026-11-18
2. [Cyclone DDS manual: configuration (network interfaces, multicasting, discovery)](https://cyclonedds.io/docs/cyclonedds/latest/config/index.html), accessed 2026-11-18
3. [rmw_cyclonedds README and rmw_node.cpp (jazzy branch)](https://github.com/ros2/rmw_cyclonedds), accessed 2026-11-18
4. [ROS 2 docs: Addressing common DDS tuning issues](https://docs.ros.org/en/jazzy/How-To-Guides/DDS-tuning.html), accessed 2026-11-18
5. [REP 2000: ROS 2 Releases and Target Platforms](https://reps.openrobotics.org/rep-2000/), accessed 2026-11-18
6. [Lyrical Luth supported platforms and middleware](https://docs.ros.org/en/lyrical/Releases/lyrical/supported-platforms.html), accessed 2026-11-18
7. [rosdistro distribution files: humble, jazzy, kilted, lyrical](https://github.com/ros/rosdistro), accessed 2026-11-18
8. [unitree_ros2 README](https://github.com/unitreerobotics/unitree_ros2), accessed 2026-11-18

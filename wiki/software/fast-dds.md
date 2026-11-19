---
type: tool
name: Fast DDS
summary: eProsima's open-source DDS library (formerly Fast-RTPS) and, as rmw_fastrtps_cpp, the default ROS 2 middleware in Jazzy and Lyrical; works untouched on one machine, needs tuning for Docker, Wi-Fi and large data.
tags: [ros2, middleware, rmw, dds, rtps, fast-rtps, rmw-fastrtps, discovery-server, shared-memory, eprosima]
kind: library
area: ros2
support:
license: Apache-2.0
links: {repo: "https://github.com/eProsima/Fast-DDS", docs: "https://fast-dds.docs.eprosima.com", site: "https://www.eprosima.com/index.php/products-all/eprosima-fast-dds"}
version: {tested: , latest: 3.6.2, as_of: 2026-11-18}
platforms: [linux, windows, macos]
agent_access: cli
registry:
evidence: researched
last_verified: 2026-11-18
sources:
  - {url: "https://github.com/eProsima/Fast-DDS", title: "Fast DDS repository: README, LICENSE, RELEASE_SUPPORT.md, PLATFORM_SUPPORT.md, source", accessed: 2026-11-18}
  - {url: "https://github.com/eProsima/Fast-DDS/blob/master/versions.md", title: Fast DDS changelog (versions.md), accessed: 2026-11-18}
  - {url: "https://github.com/ros2/rmw_fastrtps", title: "rmw_fastrtps README, jazzy and rolling branches", accessed: 2026-11-18}
  - {url: "https://reps.openrobotics.org/rep-2000/", title: "REP 2000: ROS 2 Releases and Target Platforms", accessed: 2026-11-18}
  - {url: "https://docs.ros.org/en/lyrical/Releases/lyrical/supported-platforms.html", title: Lyrical Luth supported platforms and middleware, accessed: 2026-11-18}
  - {url: "https://github.com/ros/rosdistro", title: "rosdistro distribution files: humble, jazzy, kilted, lyrical", accessed: 2026-11-18}
  - {url: "https://docs.ros.org/en/jazzy/Tutorials/Advanced/Discovery-Server/Discovery-Server.html", title: "ROS 2 docs: Using Fast DDS Discovery Server as discovery protocol", accessed: 2026-11-18}
  - {url: "https://fast-dds.docs.eprosima.com/en/latest/docker/shm_docker.html", title: "Fast DDS docs: Leveraging Fast DDS SHM in Docker deployments", accessed: 2026-11-18}
---

# Fast DDS

eProsima's open-source DDS library, the publish-subscribe layer under [ROS 2](../tools/ros2.md),
plugged in by `rmw_fastrtps_cpp`. It is the default middleware in Humble, Jazzy and Lyrical, so a
stock install already runs on it [4][5].

## When to use it

- One computer or a wired LAN: no setup, and shared memory between local processes by default [3].
- Many nodes on a busy or wireless network: keep it, but swap multicast discovery for the Discovery
  Server, a central process that cuts discovery traffic [7]. Kilted and Lyrical add Easy Mode
  (`ROS2_EASY_MODE=<ip>`), new in Fast DDS 3.2 and absent from Jazzy's 2.14 [2][6].
- Otherwise read [Choose a ROS 2 middleware](../guides/choose-a-ros2-middleware.md).

## Setup

```bash
sudo apt install ros-jazzy-rmw-fastrtps-cpp
export RMW_IMPLEMENTATION=rmw_fastrtps_cpp      # only if you changed the default
ros2 doctor --report                             # check the RMW MIDDLEWARE section
fastdds discovery --server-id 0                  # optional discovery server on port 11811
export ROS_DISCOVERY_SERVER=<server-ip>:11811    # on each node that should use it
```

| Distro | Fast DDS | rmw_fastrtps | Fast DDS branch end of life |
|---|---|---|---|
| Jazzy | 2.14.7 | 8.4.5 | May 2029 |
| Lyrical | 3.6.2 | 9.4.11 | May 2031 |

Versions: released ROS packages [6]; end of life: eProsima's LTS plan [1]. Fast DDS 3.0 broke the
API and renamed settings, so recheck Jazzy configs on Kilted or Lyrical [2]. Fast DDS is Tier 1 on
Ubuntu, Windows and macOS [1]; ROS 2 on macOS is Tier 3, a source build [4].

## Traps

- **Docker: nodes are listed but no data arrives.** Fast DDS takes containers on the host network
  for one host and uses shared memory, which fails without a shared IPC namespace. Run each with
  `--network=host --ipc=host`, or force UDP: `FASTDDS_BUILTIN_TRANSPORTS=UDPv4` [8][1].
- **Images or point clouds stall over Wi-Fi.** Large samples suffer on lossy UDP links. Set
  `FASTDDS_BUILTIN_TRANSPORTS=LARGE_DATA` on both ends: discovery stays on UDP, data uses TCP [3].
- **XML profile ignored.** Jazzy (2.14) reads `FASTRTPS_DEFAULT_PROFILES_FILE`, Kilted and Lyrical
  (3.x) `FASTDDS_DEFAULT_PROFILES_FILE` [3][2]. QoS set in code always beats the XML, and publish
  mode comes from XML only with `RMW_FASTRTPS_USE_QOS_FROM_XML=1` [3].
- **Discovery Server hides the graph from the CLI**, so `ros2 topic list` comes back short. Set
  `ROS_SUPER_CLIENT=TRUE` (or the XML profile in [7]) for the CLI, then `ros2 daemon stop` [7][1].
- **`publish()` can block.** The default mode is synchronous: data goes out in your thread [3].
  `RMW_FASTRTPS_PUBLICATION_MODE=ASYNCHRONOUS` moves sending to a background thread.

## Alternatives

- [Cyclone DDS](cyclone-dds.md) and [rmw_zenoh](rmw-zenoh.md) are Tier 1 in Lyrical; so is RTI
  Connext DDS, except on arm64 [5]. `rmw_fastrtps_dynamic_cpp` is this RMW's Tier 2 variant [5].

## Sources

1. [Fast DDS repository: README, LICENSE, RELEASE_SUPPORT.md, PLATFORM_SUPPORT.md, source](https://github.com/eProsima/Fast-DDS), accessed 2026-11-18
2. [Fast DDS changelog (versions.md)](https://github.com/eProsima/Fast-DDS/blob/master/versions.md), accessed 2026-11-18
3. [rmw_fastrtps README, jazzy and rolling branches](https://github.com/ros2/rmw_fastrtps), accessed 2026-11-18
4. [REP 2000: ROS 2 Releases and Target Platforms](https://reps.openrobotics.org/rep-2000/), accessed 2026-11-18
5. [Lyrical Luth supported platforms and middleware](https://docs.ros.org/en/lyrical/Releases/lyrical/supported-platforms.html), accessed 2026-11-18
6. [rosdistro distribution files: humble, jazzy, kilted, lyrical](https://github.com/ros/rosdistro), accessed 2026-11-18
7. [ROS 2 docs: Using Fast DDS Discovery Server as discovery protocol](https://docs.ros.org/en/jazzy/Tutorials/Advanced/Discovery-Server/Discovery-Server.html), accessed 2026-11-18
8. [Fast DDS docs: Leveraging Fast DDS SHM in Docker deployments](https://fast-dds.docs.eprosima.com/en/latest/docker/shm_docker.html), accessed 2026-11-18

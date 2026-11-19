---
type: tool
name: rmw_zenoh
summary: The ROS 2 middleware built on Eclipse Zenoh instead of DDS; Tier 1 since Kilted and in Lyrical, released but untiered for Jazzy; a per-host router replaces multicast discovery, which helps over Wi-Fi and across networks.
tags: [ros2, middleware, rmw, zenoh, rmw-zenoh-cpp, rmw-zenohd, router, wifi, multi-machine, eclipse]
kind: library
area: ros2
support:
license: Apache-2.0
links: {repo: "https://github.com/ros2/rmw_zenoh", docs: "https://docs.ros.org/en/jazzy/Installation/RMW-Implementations/Non-DDS-Implementations/Working-with-Zenoh.html", site: "https://zenoh.io"}
version: {tested: , latest: 0.2.13, as_of: 2026-11-18}
platforms: [linux, windows]
agent_access: cli
registry:
evidence: researched
last_verified: 2026-11-18
sources:
  - {url: "https://github.com/ros2/rmw_zenoh", title: "rmw_zenoh README, LICENSE and package files, rolling and jazzy branches", accessed: 2026-11-18}
  - {url: "https://github.com/ros2/rmw_zenoh/blob/rolling/docs/design.md", title: rmw_zenoh design document, accessed: 2026-11-18}
  - {url: "https://docs.ros.org/en/jazzy/Installation/RMW-Implementations/Non-DDS-Implementations/Working-with-Zenoh.html", title: "ROS 2 docs: Working with Zenoh", accessed: 2026-11-18}
  - {url: "https://docs.ros.org/en/kilted/Releases/Release-Kilted-Kaiju.html", title: "ROS 2 docs: Kilted Kaiju release notes", accessed: 2026-11-18}
  - {url: "https://docs.ros.org/en/lyrical/Releases/lyrical/supported-platforms.html", title: Lyrical Luth supported platforms and middleware, accessed: 2026-11-18}
  - {url: "https://docs.ros.org/en/lyrical/ROS-Framework/middleware/About-Different-Middleware-Vendors.html", title: "ROS 2 docs: Different ROS 2 middleware vendors (Lyrical)", accessed: 2026-11-18}
  - {url: "https://docs.ros.org/en/jazzy/Tutorials/Advanced/Improved-Dynamic-Discovery.html", title: "ROS 2 docs: Improved Dynamic Discovery", accessed: 2026-11-18}
  - {url: "https://github.com/ros/rosdistro", title: "rosdistro distribution files: humble, jazzy, kilted, lyrical, rolling", accessed: 2026-11-18}
---

# rmw_zenoh

A [ROS 2](../tools/ros2.md) middleware that swaps DDS for Zenoh, Eclipse's publish-subscribe and
query protocol [6]. Nodes on a host find each other through a small router, then talk directly
over TCP; traffic between hosts goes through the routers, and UDP multicast is off by default [2].

## When to use it

- Kilted or Lyrical, robot on Wi-Fi or across networks: Tier 1 in both [4][5]; routers link over
  TCP endpoints you list [1]. ROS docs credit its lean, routed design for hard networks [6].
- Jazzy: binaries exist [8] but no tier, as Kilted was the first Tier 1 distro [4]; test first.
- Not when the robot's SDK speaks DDS: rmw_zenoh never talks to DDS nodes, not even through
  zenoh-bridge-ros2dds [1]. See [Choose a ROS 2 middleware](../guides/choose-a-ros2-middleware.md).

## Setup

```bash
sudo apt install ros-jazzy-rmw-zenoh-cpp
ros2 run rmw_zenoh_cpp rmw_zenohd           # terminal 1: the router, one per host
export RMW_IMPLEMENTATION=rmw_zenoh_cpp     # every other terminal, then run nodes as usual
```

Released: Humble 0.1.11, Jazzy 0.2.13, Kilted 0.6.10, Lyrical 0.10.8 (Zenoh 1.8.0) [8][5], with
binaries for each distro's Tier 1 platforms [1][3]. Stop any `ros2` daemon left from another RMW.

## How an agent works with it

- Configs are JSON5 files named by `ZENOH_ROUTER_CONFIG_URI` and `ZENOH_SESSION_CONFIG_URI`;
  `ZENOH_CONFIG_OVERRIDE='key=value;key=value'` patches either [1].
- Link hosts: start one router with `ZENOH_CONFIG_OVERRIDE='connect/endpoints=["tcp/<ip>:7447"]'`.
  A laptop can join a robot's router directly with `mode="client"` and that endpoint [1].
- `ROS_AUTOMATIC_DISCOVERY_RANGE` and `ROS_STATIC_PEERS` are ignored [7]; `ROS_DOMAIN_ID` still
  separates systems [2]. `RUST_LOG=zenoh=info` logs what Zenoh connects to [1].

## Traps

- **Nodes start but see nothing.** Without a router there is no discovery; nodes start anyway and
  connect once one appears. Start `rmw_zenohd` first, or for a one-host test without it set
  `ZENOH_ROUTER_CHECK_ATTEMPTS=-1` and `ZENOH_CONFIG_OVERRIDE='scouting/multicast/enabled=true'` [1].
- **Router dies on a host without IPv6.** It listens on `tcp/[::]:7447` by default; replace that
  entry with `tcp/0.0.0.0:7447` in the router config, do not just add one [1].
- **Humble and newer distros drop each other's messages silently**, though they discover each
  other: since Iron the keys carry type hashes [1].
- **Shared memory is off by default.** Enable `transport/shared_memory/enabled=true` on every
  session; each node may take 48 MiB of `/dev/shm`, and containers need `--ipc=host`. With it on,
  heavy CPU load at launch can silently drop some service calls (known issue 978) [1].
- **Panic at exit** about thread-local storage: call `rclcpp::shutdown()` before the program ends,
  except in composable nodes [1].

## Alternatives

- [Fast DDS](fast-dds.md), [Cyclone DDS](cyclone-dds.md) and RTI Connext DDS: Tier 1 in Lyrical [5].

## Sources

1. [rmw_zenoh README, LICENSE and package files, rolling and jazzy branches](https://github.com/ros2/rmw_zenoh), accessed 2026-11-18
2. [rmw_zenoh design document](https://github.com/ros2/rmw_zenoh/blob/rolling/docs/design.md), accessed 2026-11-18
3. [ROS 2 docs: Working with Zenoh](https://docs.ros.org/en/jazzy/Installation/RMW-Implementations/Non-DDS-Implementations/Working-with-Zenoh.html), accessed 2026-11-18
4. [ROS 2 docs: Kilted Kaiju release notes](https://docs.ros.org/en/kilted/Releases/Release-Kilted-Kaiju.html), accessed 2026-11-18
5. [Lyrical Luth supported platforms and middleware](https://docs.ros.org/en/lyrical/Releases/lyrical/supported-platforms.html), accessed 2026-11-18
6. [ROS 2 docs: Different ROS 2 middleware vendors (Lyrical)](https://docs.ros.org/en/lyrical/ROS-Framework/middleware/About-Different-Middleware-Vendors.html), accessed 2026-11-18
7. [ROS 2 docs: Improved Dynamic Discovery](https://docs.ros.org/en/jazzy/Tutorials/Advanced/Improved-Dynamic-Discovery.html), accessed 2026-11-18
8. [rosdistro distribution files: humble, jazzy, kilted, lyrical, rolling](https://github.com/ros/rosdistro), accessed 2026-11-18

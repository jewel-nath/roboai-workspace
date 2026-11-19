---
type: tool
name: Foxglove
summary: Closed-source robotics visualiser for live ROS 2 (through the open foxglove_bridge) and MCAP or bag files, with plots, 3D, images and shared layouts; free tier and paid plans. Lichtblick is the open fork.
tags: [visualization, mcap, foxglove-bridge, websocket, rosbag2, 3d, layouts, lichtblick, closed-source]
kind: tool
area: ros2
support: documented
license:
links: {repo: "https://github.com/foxglove/foxglove-sdk", docs: "https://docs.foxglove.dev", site: "https://foxglove.dev"}
version: {tested: , latest: 3.6.0, as_of: 2026-11-18}
platforms: [linux, windows, macos]
agent_access: mcp
registry:
evidence: researched
last_verified: 2026-11-18
sources:
  - {url: "https://foxglove.dev/pricing", title: Foxglove pricing, accessed: 2026-11-18}
  - {url: "https://foxglove.dev/blog/foxglove-vs-foxglove-studio-two-years-on", title: "Foxglove blog: Foxglove vs Foxglove Studio, two years on", accessed: 2026-11-18}
  - {url: "https://docs.foxglove.dev/docs/getting-started/frameworks/ros2", title: "Foxglove docs: ROS 2", accessed: 2026-11-18}
  - {url: "https://github.com/foxglove/foxglove-sdk", title: "Foxglove SDK repository: README, LICENSE, foxglove_bridge README and changelog", accessed: 2026-11-18}
  - {url: "https://foxglove.dev/download", title: Foxglove download page, accessed: 2026-11-18}
  - {url: "https://docs.foxglove.dev/changelog/tags/foxglove", title: Foxglove app changelog, accessed: 2026-11-18}
  - {url: "https://github.com/lichtblick-suite/lichtblick", title: Lichtblick repository README and LICENSE, accessed: 2026-11-18}
  - {url: "https://lichtblick-suite.github.io/docs/docs/connecting-to-data/frameworks/ros2", title: "Lichtblick docs: ROS 2", accessed: 2026-11-18}
---

# Foxglove

A visualiser for robotics data: plots, 3D scenes, images, maps and logs side by side, from live
ROS 2 topics or MCAP and bag files [3]; teams also store and share recordings in its cloud [1].
**The app is closed source**, so `license` is empty: Foxglove Studio's last open release was v1.87.0
(MPL-2.0) in February 2024 [2]. Still open: MCAP [2], and the Foxglove SDK repo with foxglove_bridge,
the message schemas and SDKs for Python, C++ and Rust, all MIT [4]. Newest app: 3.6.0, 2026-11-13 [6].

## When to use it

For one window with plots, TF, robot models, point clouds, images and shared layouts [1][3]. Use
[PlotJuggler](plotjuggler.md) for time series, [Rerun](rerun.md) for an open SDK and file format,
and Lichtblick (below) or RViz 2 for open source with no account.

## Setup

The app runs on Linux (`.deb`, x64 and arm64, Ubuntu or Debian only), Windows and macOS, and syncs
with a Foxglove account [5]. Plans on 2026-11-18; Basic seats are view-only [1]:

| Plan | Price | Main limits |
|---|---|---|
| Free | $0 | 3 users, 5 devices, 1 project, 10 GB; no local MCP server |
| Pro | $20 a month plus usage | 1 TB, 3 developer seats then $42 per seat a month, free Basic seats, $20 per device after 5 |
| Academic | $0 (.edu or .ac email) | 1 TB, unlimited users, 10 devices, 3 projects |
| Enterprise | Custom | Self-hosted data, on-premises, SSO, audit logs |

Live ROS 2 goes through foxglove_bridge, a C++ WebSocket node [4]: `sudo apt install
ros-jazzy-foxglove-bridge`, then `ros2 launch foxglove_bridge foxglove_bridge_launch.xml`, and in
the app Open connection → Foxglove WebSocket → `ws://ROBOT_IP:8765` [3]. The bridge is packaged for
Humble, Jazzy, Kilted, Lyrical and Rolling; newest release 3.6.3 (2026-10-21); apt lags the repo
[4]. [rosbridge](../software/rosbridge-suite.md) also works; Foxglove prefers its bridge [3].

## How an agent works with it

Since 3.0.0 the desktop app can run a local MCP server (Settings → Personal → Agents & MCP) that
builds layouts, writes user scripts and runs queries [6]. It needs Pro, Enterprise or Academic
[1][6]; on Free the app is GUI only. Agents can also write MCAP with the Foxglove SDK [4].

## Traps

- **Bridge open to the network.** It binds `0.0.0.0` and lets clients publish, call services and
  set parameters [4]. Set `address:=127.0.0.1` and tunnel in, trim `capabilities`, or use TLS [4].
- **Custom messages in `.db3` bags.** `.db3` (the default before Iron) stores no message definitions:
  record MCAP, or run `mcap convert in.db3 out.mcap` with your workspace sourced [3].
- **Bridge defaults.** It queues 1024 messages per client and drops the oldest, so limit topics with
  `topic_whitelist`; `use_sim_time` is false, so set it in simulation or bag replay [4].

## Alternatives

**Lichtblick**, the MPL-2.0 fork of Foxglove Studio's open code (copyright BMW AG and Foxglove),
v1.31.0, runs in a browser, on desktop or from Docker (`ghcr.io/lichtblick-suite/lichtblick`) [7].
It opens MCAP with ROS 2 data and connects live through rosbridge or foxglove_bridge [8].

## Sources

1. [Foxglove pricing](https://foxglove.dev/pricing), accessed 2026-11-18
2. [Foxglove blog: Foxglove vs Foxglove Studio, two years on](https://foxglove.dev/blog/foxglove-vs-foxglove-studio-two-years-on), accessed 2026-11-18
3. [Foxglove docs: ROS 2](https://docs.foxglove.dev/docs/getting-started/frameworks/ros2), accessed 2026-11-18
4. [Foxglove SDK repository: README, LICENSE, foxglove_bridge README and changelog](https://github.com/foxglove/foxglove-sdk), accessed 2026-11-18
5. [Foxglove download page](https://foxglove.dev/download), accessed 2026-11-18
6. [Foxglove app changelog](https://docs.foxglove.dev/changelog/tags/foxglove), accessed 2026-11-18
7. [Lichtblick repository README and LICENSE](https://github.com/lichtblick-suite/lichtblick), accessed 2026-11-18
8. [Lichtblick docs: ROS 2](https://lichtblick-suite.github.io/docs/docs/connecting-to-data/frameworks/ros2), accessed 2026-11-18

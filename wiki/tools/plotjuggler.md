---
type: tool
name: PlotJuggler
summary: Desktop time-series plotter for ROS 2 topics, rosbag2 and MCAP files and PX4 logs; drag fields into synced plots to tune controllers and check sensors. Jazzy's apt repo ships the 3.x line; 4.x is a separate rewrite.
tags: [plotting, time-series, rosbag2, mcap, ulog, px4, lua, debugging, live-topics]
kind: tool
area: ros2
support: documented
license: MPL-2.0
links: {repo: "https://github.com/PlotJuggler/PlotJuggler", docs: "https://github.com/PlotJuggler/PlotJuggler#how-to-get-started", site: "https://plotjuggler.io"}
version: {tested: , latest: 3.17.2, as_of: 2026-11-18}
platforms: [linux, windows, macos]
agent_access: gui-only
registry:
evidence: researched
last_verified: 2026-11-18
sources:
  - {url: "https://github.com/PlotJuggler/PlotJuggler", title: PlotJuggler README (main branch, PlotJuggler 4), accessed: 2026-11-18}
  - {url: "https://github.com/PlotJuggler/PlotJuggler/tree/main-3.x", title: "PlotJuggler 3 branch (main-3.x): README, app and plugin source", accessed: 2026-11-18}
  - {url: "https://github.com/PlotJuggler/PlotJuggler/releases", title: PlotJuggler releases, accessed: 2026-11-18}
  - {url: "https://github.com/PlotJuggler/plotjuggler-ros-plugins", title: plotjuggler-ros-plugins README and LICENSE, accessed: 2026-11-18}
  - {url: "https://github.com/PlotJuggler/plotjuggler-ros-plugins/tree/main/src", title: "plotjuggler-ros-plugins source: rosbag2 loader and parser settings", accessed: 2026-11-18}
  - {url: "https://github.com/ros/rosdistro", title: "rosdistro distribution files (Humble, Jazzy, Kilted, Lyrical, Rolling)", accessed: 2026-11-18}
  - {url: "http://packages.ros.org/ros2/ubuntu/dists/noble/main/", title: ROS 2 apt repository package index for Ubuntu 24.04 (amd64 and arm64), accessed: 2026-11-18}
  - {url: "https://github.com/PlotJuggler/PlotJuggler/blob/main/docs/BUILDING.md", title: PlotJuggler 4 building from source and PJ3 migration notes, accessed: 2026-11-18}
  - {url: "https://github.com/PlotJuggler/pj-official-plugins/tree/main/data_stream_ros2", title: "pj-official-plugins: ROS 2 Topic Subscriber", accessed: 2026-11-18}
  - {url: "https://github.com/PlotJuggler/PlotJuggler/tree/main/pj_app/src", title: "PlotJuggler 4 app source: command line and layout files", accessed: 2026-11-18}
  - {url: "https://github.com/PlotJuggler/PlotJuggler/blob/main/docs/MCP_SERVER.md", title: "PlotJuggler 4 design doc: AI agents and the MCP server", accessed: 2026-11-18}
  - {url: "https://github.com/PlotJuggler/plotjuggler-agent", title: PlotJuggler agent plugin README, accessed: 2026-11-18}
  - {url: "https://apt.plotjuggler.io/pj4_install.sh", title: PlotJuggler 4 apt install script, accessed: 2026-11-18}
  - {url: "https://github.com/PlotJuggler/PlotJuggler/blob/main/docs/TELEMETRY.md", title: PlotJuggler 4 anonymous usage statistics, accessed: 2026-11-18}
---

# PlotJuggler

A desktop app for numbers that change over time. Open a ROS 2 bag, an MCAP file or a PX4 ULog, or
subscribe to live topics, then drag message fields into plots that share one time cursor [1][2].
Builders use it to tune controllers, check sensor rates and noise, and compare test runs.

There are two lines. **PlotJuggler 3** (3.17.2) is what the ROS 2 apt repo installs, and is the
`latest` above [6]. **PlotJuggler 4** is a rewrite with 3D scenes, video, a plugin marketplace and
Lua and Python transforms; 4.0.0 shipped on 21 September 2026 and 4.1.0 on 5 November 2026,
outside the ROS repos [1][3].

## When to use it

- **Use it** for joint states, odometry, IMU, motor currents, controller error and PX4 flight logs,
  after a run or live while you tune gains. The project says it handles thousands of series and
  millions of points [2].
- **Use something else** for 3D data (point clouds, TF, robot models) in PlotJuggler 3: RViz 2,
  [Foxglove](foxglove.md) or [Rerun](rerun.md). PlotJuggler 4 adds point clouds, URDF models and
  video [1], but is new and not in the ROS repos.
- **Use something else** for team dashboards and cloud data ([Foxglove](foxglove.md)), or for
  logging from your own Python or C++ code into datasets ([Rerun](rerun.md)).

## Setup

### Jazzy, from the ROS apt repo (PlotJuggler 3)

```bash
sudo apt install ros-jazzy-plotjuggler-ros
source /opt/ros/jazzy/setup.bash
ros2 run plotjuggler plotjuggler
```

This installs `plotjuggler` 3.17.2 and the ROS plugins `plotjuggler_ros` 2.3.1, on amd64 and arm64
[6][7]. Humble, Kilted and Lyrical carry the same versions; Rolling no longer lists either package
[6]. The plugins add the rosbag2 loader and the live topic subscriber; the republisher and rosout
viewer are ROS 1 only [4]. PlotJuggler is MPL-2.0 [1][2], but `plotjuggler_ros` is AGPL-3.0 by its
LICENSE file [4]: check that before you ship it in a product. The PlotJuggler 3 README also offers
a snap that works with ROS 2 only with limits it does not list, plus AppImage, macOS and Windows
installers [2]; on a ROS machine use apt.

### PlotJuggler 4 (Ubuntu 22.04+, Windows, macOS)

- **Ubuntu and Debian, amd64 only:** a script adds the project's apt repo and installs
  `plotjuggler4`; later releases come with `apt upgrade` [1][13]. Read it before running it as root:
  `curl -fsSLO https://apt.plotjuggler.io/pj4_install.sh`, then `sudo sh pj4_install.sh`.
- **Any Linux:** an x86_64 AppImage, which needs glibc 2.35 or newer [1].
- **Windows:** an installer or a portable zip [1].
- **Pixi or conda** (Linux x86_64, macOS arm64 on macOS 14+), aimed at RoboStack users on Jazzy and
  Kilted [1][3]; see [Pixi](pixi.md):
  `pixi global install -c conda-forge -c https://prefix.dev/plotjuggler plotjuggler4`
- **ROS 2:** install the ROS 2 Topic Subscriber from File → Marketplace. It is Linux only (x86_64,
  arm64), MIT licensed, and loads a build for Humble, Jazzy, Kilted, Lyrical or Rolling, picked
  from `ROS_DISTRO`, the RoboStack environment or `/opt/ros` [9].

Packaged PlotJuggler 4 builds send an anonymous launch ping and daily feature counters; turn them
off under Preferences → Appearance, or set `PJ_DISABLE_TELEMETRY` for scripted runs [14].

## What it reads

| Source | PlotJuggler 3 (apt) | PlotJuggler 4 |
|---|---|---|
| rosbag2 folder (`.db3` or `.mcap`) via `metadata.yaml` | Yes; needs the message packages sourced [5] | No `.db3` loader; convert to MCAP [1] |
| `.mcap` file opened directly | Yes; decodes from the schemas in the file [2] | Yes [1] |
| Live ROS 2 topics | Yes [4] | Marketplace plugin, Linux only [9] |
| CSV, PX4 ULog, Parquet; MQTT, ZeroMQ, UDP, WebSocket | Yes [2] | Yes [1] |
| LeRobot datasets, MP4, PCD, PLY | No | Yes [1] |

## How an agent works with it

In both released lines a person drives the GUI. An agent's useful work is writing the files
PlotJuggler opens and starting it with them.

- **Layouts are XML.** PlotJuggler 3 layouts are `.xml`: a `<root>` with tabs (`<tabbed_widget>`),
  plots (`<plot>`) and curves (`<curve name="/odom/twist/twist/linear/x"/>`). Lua series sit under
  `<customMathEquations>`, and the file names the data files and streamer last used [2].
  PlotJuggler 4 layouts end in `.pj4.xml` [10]. Save one layout in the GUI, then let the agent add
  plots and rename curves; do not write one from nothing.
- **Start with data and layout.** PlotJuggler 3:
  `ros2 run plotjuggler plotjuggler -n -d run.mcap -l layout.xml` (`-n` skips the splash;
  `--start_streamer` starts a streaming plugin) [2]. PlotJuggler 4:
  `plotjuggler4 -d run.mcap -l layout.pj4.xml` [10].
- **Check the result.** PlotJuggler 4 can run unattended: `--exit-after-layout` exits 0 when the
  layout loads, 1 when it fails and 2 on timeout; `--dump-diagnostics out.json` writes every
  warning; `--screenshot out.png` grabs the first 3D view and exits [10]. PlotJuggler 3 has no
  headless check.
- **Derived series.** PlotJuggler 3 has a Custom Function Editor (Lua over one or more inputs, one
  output series) and a Reactive Script Editor (Lua run on each time update that can create series)
  [2]; Python scripting arrived in 3.17.0 [3]. PlotJuggler 4 uses Lua and Python transforms under a
  different contract [1][8].
- **MCP is coming.** The main branch, 4.2.0 in development, adds an MCP server:
  `plotjuggler4 --mcp-bridge` speaks MCP over stdio to a running window, with tools such as
  `open_file`, `read_series`, `create_derived_series`, `plot_tab`, `export_series` and `screenshot`
  [11]. The PlotJuggler agent plugin wraps it for Claude Code and Codex and needs 4.2, not yet
  released [12]. When 4.2 ships, `agent_access` here should become `mcp`.

## Traps

- **"Can not recognize the following message types".** PlotJuggler 3's rosbag2 loader and live
  subscriber look types up in the installed ROS packages, so topics with your own messages are
  dropped and the dialog asks if you forgot to source your workspace [5]. Start PlotJuggler from a
  terminal with your overlay's `install/setup.bash` sourced, or open the `.mcap` file directly,
  which carries its definitions [2]. PlotJuggler 4's ROS 2 plugin picks the distro once per
  process: source first, then restart it [9].
- **Arrays silently missing.** The ROS parser drops arrays longer than 100 elements by default, so
  `LaserScan.ranges` or a long `Float64MultiArray` shows nothing [5]. Raise the maximum array size
  in the topic dialog, or clamp instead of discard; the MCAP loader has the same options [2].
- **Time axis is not the sensor's clock.** Samples sit at receive or log time unless you enable the
  `header.stamp` option in the topic dialog [5]. The Time Offset button starts the axis at zero; turn it off
  or use the date-time view to match plots to log lines [2].
- **Big bags fill RAM.** The loader reads every selected topic into memory: pick only the topics
  you need and leave out images and point clouds [5]. Live streams keep only the last 60 s by
  default; raise it with `--buffer_size` or in the GUI [2].
- **Mixing the two lines.** PlotJuggler 3 plugins (Qt 5) do not load in PlotJuggler 4, Lua
  functions need porting, and the project advises keeping the PlotJuggler 3 layouts while you check
  a migrated analysis [8]. PlotJuggler 4's ROS 2 streaming is Linux only [8][9].
- **No PlotJuggler 4 build for Linux arm64.** The apt repo is amd64 only, and the AppImage and Linux
  conda build are x86_64 [1][13]. On a Jetson or Raspberry Pi use the ROS apt package, or record a
  bag on the robot and plot it on a laptop.
- **Fake website.** The PlotJuggler 3 README warns that plotjuggler.com impersonates the project;
  the project's own domain is plotjuggler.io [1][2].

## Alternatives

- [Foxglove](foxglove.md): plots, 3D, images and maps in one app, with team layouts and cloud data;
  closed source with a free tier. Lichtblick is the open fork of its last open code.
- [Rerun](rerun.md): open SDK and viewer for multimodal data and datasets; better when you log from
  your own code.
- rqt_plot, from the rqt tools, for a quick live plot of one or two fields; PX4 Flight Review for
  PX4 log reports; pandas and matplotlib for plots that must be scripted.

## Sources

1. [PlotJuggler README (main branch, PlotJuggler 4)](https://github.com/PlotJuggler/PlotJuggler), accessed 2026-11-18
2. [PlotJuggler 3 branch (main-3.x): README, app and plugin source](https://github.com/PlotJuggler/PlotJuggler/tree/main-3.x), accessed 2026-11-18
3. [PlotJuggler releases](https://github.com/PlotJuggler/PlotJuggler/releases), accessed 2026-11-18
4. [plotjuggler-ros-plugins README and LICENSE](https://github.com/PlotJuggler/plotjuggler-ros-plugins), accessed 2026-11-18
5. [plotjuggler-ros-plugins source: rosbag2 loader and parser settings](https://github.com/PlotJuggler/plotjuggler-ros-plugins/tree/main/src), accessed 2026-11-18
6. [rosdistro distribution files (Humble, Jazzy, Kilted, Lyrical, Rolling)](https://github.com/ros/rosdistro), accessed 2026-11-18
7. [ROS 2 apt repository package index for Ubuntu 24.04 (amd64 and arm64)](http://packages.ros.org/ros2/ubuntu/dists/noble/main/), accessed 2026-11-18
8. [PlotJuggler 4 building from source and PJ3 migration notes](https://github.com/PlotJuggler/PlotJuggler/blob/main/docs/BUILDING.md), accessed 2026-11-18
9. [pj-official-plugins: ROS 2 Topic Subscriber](https://github.com/PlotJuggler/pj-official-plugins/tree/main/data_stream_ros2), accessed 2026-11-18
10. [PlotJuggler 4 app source: command line and layout files](https://github.com/PlotJuggler/PlotJuggler/tree/main/pj_app/src), accessed 2026-11-18
11. [PlotJuggler 4 design doc: AI agents and the MCP server](https://github.com/PlotJuggler/PlotJuggler/blob/main/docs/MCP_SERVER.md), accessed 2026-11-18
12. [PlotJuggler agent plugin README](https://github.com/PlotJuggler/plotjuggler-agent), accessed 2026-11-18
13. [PlotJuggler 4 apt install script](https://apt.plotjuggler.io/pj4_install.sh), accessed 2026-11-18
14. [PlotJuggler 4 anonymous usage statistics](https://github.com/PlotJuggler/PlotJuggler/blob/main/docs/TELEMETRY.md), accessed 2026-11-18

---
type: tool
name: Rerun
summary: Open-source SDK and viewer for multimodal robot data; log images, point clouds, transforms and time series from Python, Rust or C++, save .rrd recordings, and browse MCAP bags and LeRobot datasets.
tags: [visualization, logging, sdk, rrd, mcap, lerobot, multimodal, datasets, python, rust, cpp]
kind: tool
area: ros2
support: documented
license: MIT OR Apache-2.0
links: {repo: "https://github.com/rerun-io/rerun", docs: "https://rerun.io/docs", site: "https://rerun.io"}
version: {tested: , latest: 0.43.2, as_of: 2026-11-18}
platforms: [linux, windows, macos]
agent_access: api
registry:
evidence: researched
last_verified: 2026-11-18
sources:
  - {url: "https://github.com/rerun-io/rerun", title: "Rerun repository: README, LICENSE files, changelog and release tags", accessed: 2026-11-18}
  - {url: "https://rerun.io/docs/reference/cli", title: Rerun CLI reference, accessed: 2026-11-18}
  - {url: "https://rerun.io/docs/getting-started/install-rerun/python", title: "Rerun docs: Python SDK install and requirements", accessed: 2026-11-18}
  - {url: "https://rerun.io/docs/howto/visualization/limit-ram", title: "Rerun docs: Limit the viewer's memory usage", accessed: 2026-11-18}
  - {url: "https://rerun.io/docs/howto/logging-and-ingestion/mcap", title: "Rerun docs: Working with MCAP", accessed: 2026-11-18}
  - {url: "https://rerun.io/docs/howto/integrations/ros2-nav-turtlebot", title: "Rerun docs: Use Rerun with ROS 2", accessed: 2026-11-18}
  - {url: "https://github.com/huggingface/lerobot", title: "LeRobot repository: pyproject.toml and lerobot_dataset_viz.py", accessed: 2026-11-18}
  - {url: "https://www.ros.org/reps/rep-2000.html", title: "REP 2000: ROS 2 releases and target platforms", accessed: 2026-11-18}
---

# Rerun

An SDK and viewer for time-stamped, multimodal data: log images, point clouds, transforms, joint
states and scalars from Python, Rust or C++, then scrub them live or from `.rrd` files; the viewer
also opens MCAP files and LeRobot datasets [1]. Builders use it to debug perception and learning
code and to browse datasets. Licence MIT OR Apache-2.0; newest release 0.43.2, 2026-11-13 [1].

## When to use it

Use it when your own code makes the data, or to open MCAP bags and LeRobot datasets without ROS
[1][5]. It has no native ROS 2 subscriber [6]: for a live ROS 2 graph without code use RViz 2 or
[Foxglove](foxglove.md); for many numeric fields, [PlotJuggler](plotjuggler.md).

## Setup

`pip install "rerun-sdk==0.43.2"` installs the Python SDK and the `rerun` viewer. It needs Python
3.11+ and NumPy 2+, with wheels for Linux x86_64 and aarch64 (glibc 2.28+), Windows x86_64 and
Apple-silicon macOS, not Intel Macs; conda-forge has it too [3]. Rust and C++ users install the
viewer separately [1]. On a ROS 2 machine use a venv or [Pixi](pixi.md) env (see Traps).

- **ROS 2 bags:** `rerun my_bag.mcap`, or `rerun mcap convert my_bag.mcap -o my_bag.rrd`; common
  ROS 2 messages become Rerun types, others are decoded by reflection [5].
- **Live ROS 2:** write a small rclpy node that subscribes and calls `rr.log`, as the official guide
  does [6]. The experimental `rosbag2_storage_rrd` plugin records with `ros2 bag record -s rrd` [5].
- **LeRobot:** after `pip install "lerobot[viz]"`, `lerobot-dataset-viz --repo-id lerobot/pusht
  --episode-index 0` opens an episode in Rerun, for example from an [SO-101](../robots/so-101.md) [7].

## How an agent works with it

The SDK is the interface: `rr.init("app")`, then `rr.save("run.rrd")` or `rr.spawn()`,
`rr.set_time(...)` and `rr.log("world/points", rr.Points3D(xyz))` [1]. Check files headless with
`rerun rrd verify` and `rerun rrd stats` [2]. In 0.43, `rerun viewer-mcp` is an MCP server for a
running viewer [2]; the main branch renames it `rerun mcp` [1].

## Traps

- **SDK and viewer must match.** No stable API yet, so pin one version [1]; an older viewer may not
  show a newer SDK's data, and the `rerun` on `PATH` must come from your env [3]. LeRobot pins
  `rerun-sdk>=0.24.0,<0.34.0` [7], far behind 0.43. Old `.rrd` files: `rerun rrd migrate` [2].
- **Clash with the ROS 2 Python.** Jazzy (Ubuntu 24.04) ships Python 3.12.3 with NumPy 1.26.4;
  Humble (22.04) ships Python 3.10.4 [8], below Rerun's minimum [3]. Keep Rerun in its own env and
  test any node that imports both ROS packages and `rerun`.
- **Memory.** The viewer's default cap is 75% of RAM (2.5 GB in a browser); past it, it drops data;
  `rr.spawn` reuses a viewer already on port 9876 and ignores a new limit; `static=True` data is
  never dropped; the gRPC server keeps its own 1 GiB [4]. Set `--memory-limit` for long runs [4].
  Many entities or multi-million-point clouds also slow the viewer: downsample [1].
- **`.db3` bags do not open.** Convert with `ros2 bag convert -i my_bag -o convert.yaml`, with
  `storage_id: mcap` and a topic selection in the YAML, or the output is empty [5].

## Alternatives

[Foxglove](foxglove.md), [PlotJuggler](plotjuggler.md), and RViz 2 for live 3D on the ROS machine.

## Sources

1. [Rerun repository: README, LICENSE files, changelog and release tags](https://github.com/rerun-io/rerun), accessed 2026-11-18
2. [Rerun CLI reference](https://rerun.io/docs/reference/cli), accessed 2026-11-18
3. [Rerun docs: Python SDK install and requirements](https://rerun.io/docs/getting-started/install-rerun/python), accessed 2026-11-18
4. [Rerun docs: Limit the viewer's memory usage](https://rerun.io/docs/howto/visualization/limit-ram), accessed 2026-11-18
5. [Rerun docs: Working with MCAP](https://rerun.io/docs/howto/logging-and-ingestion/mcap), accessed 2026-11-18
6. [Rerun docs: Use Rerun with ROS 2](https://rerun.io/docs/howto/integrations/ros2-nav-turtlebot), accessed 2026-11-18
7. [LeRobot repository: pyproject.toml and lerobot_dataset_viz.py](https://github.com/huggingface/lerobot), accessed 2026-11-18
8. [REP 2000: ROS 2 releases and target platforms](https://www.ros.org/reps/rep-2000.html), accessed 2026-11-18

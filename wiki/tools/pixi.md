---
type: tool
name: Pixi (with RoboStack)
summary: prefix.dev's conda-based environment manager; with RoboStack's channels it installs ROS 2 Jazzy, Humble, Lyrical or Rolling on Linux, macOS and Windows from one lock file, without apt or root.
tags: [pixi, robostack, conda, conda-forge, windows, macos, lock-file, reproducible, prefix-dev]
kind: tool
area: ros2
support: documented
license: BSD-3-Clause
links: {repo: "https://github.com/prefix-dev/pixi", docs: "https://pixi.prefix.dev/latest/", site: "https://pixi.sh"}
version: {tested: , latest: "0.84.2", as_of: 2026-11-18}
platforms: [linux, macos, windows]
agent_access: cli
registry:
evidence: researched
last_verified: 2026-11-18
sources:
  - {url: "https://pixi.prefix.dev/latest/installation/", title: Pixi installation guide, accessed: 2026-11-18}
  - {url: "https://github.com/prefix-dev/pixi/blob/main/CHANGELOG.md", title: Pixi changelog, accessed: 2026-11-18}
  - {url: "https://pixi.prefix.dev/latest/tutorials/ros2/", title: "Pixi tutorial: develop a ROS 2 package", accessed: 2026-11-18}
  - {url: "https://pixi.prefix.dev/latest/reference/cli/pixi/install/", title: pixi install command reference, accessed: 2026-11-18}
  - {url: "https://robostack.github.io/GettingStarted.html", title: RoboStack Getting Started, accessed: 2026-11-18}
  - {url: "https://robostack.github.io/FAQ.html", title: RoboStack FAQ, accessed: 2026-11-18}
  - {url: "https://robostack.github.io/Monorepo.html", title: The RoboStack monorepo, accessed: 2026-11-18}
  - {url: "https://github.com/RoboStack/robostack/blob/main/shared/vinca.yaml", title: "RoboStack package list for all distributions (shared/vinca.yaml)", accessed: 2026-11-18}
---

# Pixi (with RoboStack)

Pixi is a single Rust binary that manages per-project conda environments [1]; the latest release is
0.84.2 (2026-11-10) [2]. RoboStack rebuilds ROS as conda packages, so the pair gives you ROS 2 on
Linux, macOS and Windows from a `pixi.toml` and a `pixi.lock`, with no system ROS and no root [5][6].

## When to use it

Use it on Windows or macOS, on a Linux that is not the distro's Ubuntu (no system libraries are
used), or to put ROS beside PyTorch in one pinned environment; RoboStack ships Linux x86-64 and ARM,
macOS Intel and Apple Silicon, and Windows builds [6]. It builds **Humble, Jazzy, Lyrical and
Rolling**; Noetic and Kilted are deprecated there [7]. Its package list includes rosbridge_suite,
mavros and foxglove_bridge, with a few left out on Windows [8]. On an Ubuntu 24.04 robot whose
packages are all in apt, the plain [ROS 2](ros2.md) install is simpler.

## Setup

```bash
curl -fsSL https://pixi.sh/install.sh | sh      # Linux, macOS
winget install prefix-dev.pixi                  # Windows (also MSI, scoop, PowerShell script)
pixi init ros_ws -c https://prefix.dev/robostack-jazzy -c https://prefix.dev/conda-forge
cd ros_ws && pixi add ros-jazzy-desktop
pixi run ros2 run demo_nodes_cpp talker
```

The installer sends one anonymous ping; `PIXI_NO_TELEMETRY=1` opts out [1]. `pixi add` writes a
version range to `pixi.toml` and exact builds to `pixi.lock`: commit both; `pixi shell` opens an
activated shell [5]. Windows needs Visual Studio 2022 with C++ [5]. Packages are now named
`ros2-<pkg>`, the channel setting the distro; `ros-jazzy-<pkg>` names still resolve [7]. For
**Lyrical**, use the `robostack-lyrical` channel and `ros-lyrical-` prefix; RoboStack's guide now
starts there [5]. Agents drive it as plain CLI: keep commands in `[tasks]`, and in CI run
`pixi install --locked`, which aborts when the lock file no longer matches the manifest [4].

## Traps

- **Apt ROS in the same shell.** A `source /opt/ros/jazzy/setup.bash` in `.bashrc` leaks its
  `PYTHONPATH` into the environment and imports break [5]. Remove it; open a fresh terminal.
- **No rosdep** in Pixi [3][6]. Add each dependency by its conda name, dashes for underscores
  (`pixi add ros-jazzy-nav2-bringup`); if absent, file a package request on RoboStack/robostack [7].
- **Builds pick up system tools.** Add `compilers cmake ninja pkg-config` and pass
  `-DPython_FIND_VIRTUALENV=ONLY -DPython3_FIND_VIRTUALENV=ONLY` to colcon [5]; on Linux add `libgl-devel` [6].
- **colcon inside Pixi.** `pixi add ros-dev-tools`, `pixi run colcon build`, and list
  `install/setup.bash` (`setup.bat` on Windows) as an activation script so `pixi run` finds your nodes [5].
- **Old or unsolvable builds.** On macOS, Pixi assumes macOS 13 and quietly installs older builds:
  run `pixi workspace platform add osx-latest=osx-arm64 --osx 14`, then
  `pixi workspace platform rm osx-arm64` [5][6]. A `__glibc` error: declare your oldest target's glibc [6].

## Alternatives

Apt packages on Ubuntu 24.04 ([ROS 2](ros2.md), [colcon](colcon.md)); Docker images (see the
[ops-docker-ci skill](../../skills/ops-docker-ci/SKILL.md)); micromamba or conda with the same
RoboStack channels [5]; rospypi for a plain Python virtualenv [6].

## Sources

1. [Pixi installation guide](https://pixi.prefix.dev/latest/installation/), accessed 2026-11-18
2. [Pixi changelog](https://github.com/prefix-dev/pixi/blob/main/CHANGELOG.md), accessed 2026-11-18
3. [Pixi tutorial: develop a ROS 2 package](https://pixi.prefix.dev/latest/tutorials/ros2/), accessed 2026-11-18
4. [pixi install command reference](https://pixi.prefix.dev/latest/reference/cli/pixi/install/), accessed 2026-11-18
5. [RoboStack Getting Started](https://robostack.github.io/GettingStarted.html), accessed 2026-11-18
6. [RoboStack FAQ](https://robostack.github.io/FAQ.html), accessed 2026-11-18
7. [The RoboStack monorepo](https://robostack.github.io/Monorepo.html), accessed 2026-11-18
8. [RoboStack package list for all distributions (shared/vinca.yaml)](https://github.com/RoboStack/robostack/blob/main/shared/vinca.yaml), accessed 2026-11-18

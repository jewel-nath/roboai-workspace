---
type: tool
name: colcon
summary: The command-line build tool for ROS 2 workspaces; it finds the packages under src/, builds and tests them in dependency order, and writes the setup scripts you source to use them.
tags: [ros2, colcon, build, workspace, overlay, ament, cmake, rosdep, mixins, testing]
kind: tool
area: ros2
support: documented
license: Apache-2.0
links: {repo: "https://github.com/colcon/colcon-core", docs: "https://colcon.readthedocs.io", site: }
version: {tested: , latest: 0.21.3, as_of: 2026-11-18}
platforms: [linux, windows, macos]
agent_access: cli
registry:
evidence: researched
last_verified: 2026-11-18
sources:
  - {url: "https://github.com/colcon/colcon-core", title: colcon-core repository, accessed: 2026-11-18}
  - {url: "https://colcon.readthedocs.io/en/released/reference/verb/build.html", title: "colcon docs: build verb", accessed: 2026-11-18}
  - {url: "https://colcon.readthedocs.io/en/released/reference/package-selection-arguments.html", title: "colcon docs: package selection arguments", accessed: 2026-11-18}
  - {url: "https://colcon.readthedocs.io/en/released/reference/executor-arguments.html", title: "colcon docs: executor arguments", accessed: 2026-11-18}
  - {url: "https://colcon.readthedocs.io/en/released/user/log-files.html", title: "colcon docs: log files", accessed: 2026-11-18}
  - {url: "https://colcon.readthedocs.io/en/released/reference/verb/test-result.html", title: "colcon docs: test-result verb", accessed: 2026-11-18}
  - {url: "https://colcon.readthedocs.io/en/released/user/configuration.html", title: "colcon docs: configuration", accessed: 2026-11-18}
  - {url: "https://github.com/colcon/colcon-override-check", title: colcon-override-check repository, accessed: 2026-11-18}
  - {url: "https://github.com/colcon/colcon-cmake/blob/master/colcon_cmake/task/cmake/build.py", title: colcon-cmake CMake build task, accessed: 2026-11-18}
  - {url: "https://docs.ros.org/en/jazzy/Tutorials/Beginner-Client-Libraries/Colcon-Tutorial.html", title: "Jazzy: Using colcon to build packages", accessed: 2026-11-18}
  - {url: "https://docs.ros.org/en/jazzy/Tutorials/Beginner-Client-Libraries/Creating-A-Workspace/Creating-A-Workspace.html", title: "Jazzy: Creating a workspace", accessed: 2026-11-18}
  - {url: "https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Rosdep.html", title: "Jazzy: Managing dependencies with rosdep", accessed: 2026-11-18}
  - {url: "https://docs.ros.org/en/jazzy/How-To-Guides/Using-Python-Packages.html", title: "Jazzy: Using Python packages with ROS 2", accessed: 2026-11-18}
  - {url: "https://discourse.openrobotics.org/t/uv-on-ros-2-a-field-report-on-workspace-level-virtual-environments-five-failure-modes-and-minimal-colcon-ament-proposals/57111", title: "ROS Discourse: uv on ROS 2, a field report on workspace-level virtual environments", accessed: 2026-11-18}
---

# colcon

colcon is the build tool of ROS 2. It finds every package under a workspace's `src/`, orders them
by their declared dependencies, builds, tests and installs each one with its own build system
(CMake, `ament_cmake`, `ament_python`), and writes the setup scripts you source to use the result
[10]. It is a Python program: `colcon-core` plus extension packages such as `colcon-cmake` [1].

## When to use it

- Whenever you build ROS 2 packages from source: your own robot packages, a driver that has no
  binary release, or a patched copy of a released package. It is the tool the ROS 2 docs use [10].
- Not needed if you only run binary packages from apt or RoboStack ([ROS 2](ros2.md)).

## Setup

colcon is released on its own schedule, not per ROS distro: the apt package name carries no
distro, unlike `ros-jazzy-*` packages [10], and the newest colcon-core tag is 0.21.3, from
2026-09-17 [1]. On Ubuntu with the ROS apt repository added, install it and rosdep with
`sudo apt install python3-colcon-common-extensions python3-rosdep`; elsewhere use
`pip install -U colcon-common-extensions` [10][12].

**Workspace layout** [10][5]:

```text
ros2_ws/
  src/       packages, usually git clones
  build/     intermediate files, one folder per package
  install/   installed packages plus setup.bash and local_setup.bash
  log/       one folder per run; latest_build links to the newest build
```

**First build** of a workspace on Jazzy [11][12]:

```bash
source /opt/ros/jazzy/setup.bash                     # the underlay
cd ~/ros2_ws
sudo rosdep init && rosdep update                    # init once per machine
rosdep install --from-paths src --ignore-src -y      # system dependencies from package.xml
colcon build --symlink-install
# in a NEW terminal, to use the result:
source /opt/ros/jazzy/setup.bash && source ~/ros2_ws/install/local_setup.bash
```

**Build flags that matter:**

| Flag | Effect |
|---|---|
| `--symlink-install` | Link installed files back to the source, so edits to Python files and other non-compiled resources apply without a rebuild [10] |
| `--packages-select a b` | Build only these packages [3] |
| `--packages-up-to a` | `a` and everything it depends on [3] |
| `--packages-above a` | `a` and everything that depends on it; use after changing a shared package [3] |
| `--packages-select-build-failed` | Retry only the packages that failed last time [3] |
| `--cmake-args -DCMAKE_BUILD_TYPE=Release` | Pass arguments to every CMake package [2] |
| `--cmake-clean-cache` | Delete `CMakeCache.txt` first, which forces a fresh configure [2] |
| `--continue-on-error` | Keep building; packages that depend on the failed one are skipped [2] |
| `--parallel-workers N`, `--executor sequential` | At most N packages at once (default: logical CPU count), or one at a time [4] |
| `--event-handlers console_direct+` | Stream all build output to the console as it happens [5] |
| `--merge-install` | One shared install prefix: shorter environment variables, but less isolation between packages [2] |

**Tests:** `colcon test` runs each package's tests; `colcon test-result --verbose` shows the
failures in detail, and `--all` lists every result file [6]. To run one CMake test, pass
`--packages-select my_pkg --ctest-args -R my_test` [10].

**Mixins and defaults.** Mixins are named sets of arguments. Add the shared ones once with
`colcon mixin add default https://raw.githubusercontent.com/colcon/colcon-mixin-repository/master/index.yaml`
and `colcon mixin update default`, then use them as `colcon build --mixin debug` [10]. Defaults
that apply to every run go in `~/.colcon/defaults.yaml` (or the file named by
`COLCON_DEFAULTS_FILE`), and per workspace in `colcon_defaults.yaml` at its root, which wins over
the global file [7]. A mixin given on the command line overrides a defaults file; per-package
settings go in a `colcon.pkg` or `colcon.meta` file [7].

```yaml
# colcon_defaults.yaml at the workspace root
build:
  symlink-install: true
  cmake-args: ["-DCMAKE_BUILD_TYPE=RelWithDebInfo"]
```

## How an agent works with it

The [ros2-core](../../skills/ros2-core/SKILL.md) skill holds the edit-build-test loop;
[ops-docker-ci](../../skills/ops-docker-ci/SKILL.md) covers builds in CI.

- Build from the workspace root, in a shell that has sourced only the underlay [11].
- Build the smallest set: `colcon build --symlink-install --packages-up-to my_pkg`.
- On failure, the console shows only a summary. Read `log/latest_build/<pkg>/stdout_stderr.log`;
  the first line of `log/latest_build/logger_all.log` is the exact command that ran [5].
- `colcon test` exits 0 even when tests fail. Gate on
  `colcon test --packages-select my_pkg --return-code-on-test-failure` [1], then read
  `colcon test-result --verbose` [6].
- After a build, run the result in a new shell that sources `install/local_setup.bash` [11].

## Traps

- **Built in a shell where the overlay was sourced, or sourced it in the build shell.** The docs
  warn this may cause complex issues [11]: build in one terminal, use in another.
  `setup.bash` sources the overlay and its underlays; `local_setup.bash` only the overlay [11].
- **Out of memory or a frozen board.** colcon builds up to one package per logical CPU at once [4],
  and colcon-cmake gives each CMake package's `make` one job per CPU unless `MAKEFLAGS` sets
  `-j` [9]: on a 4-core Pi that is up to 16 compilers. Use
  `MAKEFLAGS=-j1 colcon build --executor sequential` (or `--parallel-workers 1`) [4][9][10].
- **Slow C++ nodes.** colcon picks a Release configuration only for multi-config generators such as
  Visual Studio [9]; on Linux it sets no build type. Pass `-DCMAKE_BUILD_TYPE=Release` or
  `RelWithDebInfo` in `--cmake-args` or the defaults file.
- **Stale output.** Switching `--merge-install` on or off fails until you delete `install/`; colcon
  records the layout in `install/.colcon_install_layout` [1]. After renaming or deleting a
  package, delete its `build/` and `install/` folders too.
- **Python edits do not show up.** `--symlink-install` covers edits to installed files; new entry
  points, launch or config files and `setup.py`, `setup.cfg` or `package.xml` changes need a
  rebuild. If setuptools lacks `develop --editable`, colcon quietly falls back to a copied install
  [1]. On Windows, symlinks need an administrator shell or Developer Mode [10].
- **"Some selected packages are already built in one or more underlay workspaces".** You are
  overriding a package from `/opt/ros` that other underlay packages use. The overlay copy must stay
  API and ABI compatible; pass `--allow-overriding <pkg>` if you mean it. This warning may become an
  error in a later release [8].
- **pip packages on Ubuntu 24.04.** Prefer rosdep keys or apt `python3-*` packages [13]. For
  pip-only packages, make a venv from the system Python (ROS binaries need that interpreter) and put
  a `COLCON_IGNORE` file in it so colcon does not scan it [13]. A Jazzy field report adds: PEP 668
  blocks system-wide `pip install`; `ros2 run` still starts `ament_python` nodes with the system
  interpreter; and numpy 2 in the venv breaks apt-built extensions such as cv_bridge, so pin
  `numpy<2` [14].
- **rosdep fails or installs the wrong thing.** Remove `python3-rosdep2` if it is installed [12];
  rerun `rosdep update` now and then to refresh the index [12]. rosdep runs on Linux only [11].

## Alternatives

- **Plain CMake or `pip`** for one package outside a ROS workspace.
- **catkin_tools** and `catkin_make`, which colcon grew out of, only for ROS 1 workspaces [10].
- **[Pixi](pixi.md)** manages the environment around colcon; it does not replace it.

## Sources

1. [colcon-core repository](https://github.com/colcon/colcon-core), accessed 2026-11-18
2. [colcon docs: build verb](https://colcon.readthedocs.io/en/released/reference/verb/build.html), accessed 2026-11-18
3. [colcon docs: package selection arguments](https://colcon.readthedocs.io/en/released/reference/package-selection-arguments.html), accessed 2026-11-18
4. [colcon docs: executor arguments](https://colcon.readthedocs.io/en/released/reference/executor-arguments.html), accessed 2026-11-18
5. [colcon docs: log files](https://colcon.readthedocs.io/en/released/user/log-files.html), accessed 2026-11-18
6. [colcon docs: test-result verb](https://colcon.readthedocs.io/en/released/reference/verb/test-result.html), accessed 2026-11-18
7. [colcon docs: configuration](https://colcon.readthedocs.io/en/released/user/configuration.html), accessed 2026-11-18
8. [colcon-override-check repository](https://github.com/colcon/colcon-override-check), accessed 2026-11-18
9. [colcon-cmake CMake build task](https://github.com/colcon/colcon-cmake/blob/master/colcon_cmake/task/cmake/build.py), accessed 2026-11-18
10. [Jazzy: Using colcon to build packages](https://docs.ros.org/en/jazzy/Tutorials/Beginner-Client-Libraries/Colcon-Tutorial.html), accessed 2026-11-18
11. [Jazzy: Creating a workspace](https://docs.ros.org/en/jazzy/Tutorials/Beginner-Client-Libraries/Creating-A-Workspace/Creating-A-Workspace.html), accessed 2026-11-18
12. [Jazzy: Managing dependencies with rosdep](https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Rosdep.html), accessed 2026-11-18
13. [Jazzy: Using Python packages with ROS 2](https://docs.ros.org/en/jazzy/How-To-Guides/Using-Python-Packages.html), accessed 2026-11-18
14. [ROS Discourse: uv on ROS 2, a field report on workspace-level virtual environments](https://discourse.openrobotics.org/t/uv-on-ros-2-a-field-report-on-workspace-level-virtual-environments-five-failure-modes-and-minimal-colcon-ament-proposals/57111), accessed 2026-11-18

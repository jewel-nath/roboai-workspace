---
type: tool
name: PythonRobotics
summary: MIT-licensed collection of short, readable Python scripts with an online textbook covering localization, mapping, SLAM, path planning and path tracking; for learning an algorithm and prototyping it, not for running a robot. Not a pip package and has no ROS interface.
tags: [python, path-planning, path-tracking, localization, slam, a-star, rrt, kalman-filter, mpc, education, textbook, prototyping]
kind: library
area: nav
support:
license: MIT
links: {repo: "https://github.com/AtsushiSakai/PythonRobotics", docs: "https://atsushisakai.github.io/PythonRobotics/index.html", site: }
version: {tested: , latest: v1.0, as_of: 2026-11-24}
platforms: [linux, macos, windows]
agent_access: script
registry:
evidence: researched
last_verified: 2026-11-24
sources:
  - {url: "https://github.com/AtsushiSakai/PythonRobotics", title: "PythonRobotics repository: README, LICENSE, requirements, CI workflows, tests, sample code, history and tags", accessed: 2026-11-24}
  - {url: "https://github.com/AtsushiSakai/PythonRobotics/issues", title: PythonRobotics issue tracker, accessed: 2026-11-24}
  - {url: "https://atsushisakai.github.io/PythonRobotics/index.html", title: "PythonRobotics textbook (documentation site)", accessed: 2026-11-24}
  - {url: "https://atsushisakai.github.io/PythonRobotics/modules/0_getting_started/1_what_is_python_robotics.html", title: "PythonRobotics textbook: What is PythonRobotics?", accessed: 2026-11-24}
  - {url: "https://atsushisakai.github.io/PythonRobotics/modules/0_getting_started/2_how_to_run_sample_codes.html", title: "PythonRobotics textbook: How to run sample codes", accessed: 2026-11-24}
  - {url: "https://arxiv.org/abs/1808.10703", title: "Sakai et al., PythonRobotics: a Python code collection of robotics algorithms (arXiv 1808.10703)", accessed: 2026-11-24}
  - {url: "https://pypi.org/project/numpy/2.5.4/", title: "PyPI metadata of the pinned requirements: numpy 2.5.4 and scipy 1.18.1 (Python 3.12 or later)", accessed: 2026-11-24}
---

# PythonRobotics

Atsushi Sakai's PythonRobotics has one short Python script per algorithm, animated with Matplotlib,
and an online textbook [1][3][6]: localization (Kalman, particle, histogram filters), mapping, SLAM
(EKF SLAM, FastSLAM, graph SLAM, ICP), planning (A*, D* Lite, hybrid A*, RRT*, Frenet), tracking
(pure pursuit, Stanley, LQR, MPC) and more [1]. MIT; last commit 2026-11-10, 22 open issues [1][2].

## When to use it

- **Learn or prototype:** run a sample, change a parameter, watch the animation; readable code is
  its stated aim [4]. Try an unusual planner (car-like paths, MPC) before writing a Nav2 plugin.
- **Not to run a robot:** it is sample code with no ROS interface. Use [Nav2](nav2.md) and
  [Choose a Nav2 planner and controller](../guides/choose-a-nav2-planner-and-controller.md),
  [robot_localization](robot-localization.md), [SLAM Toolbox](slam-toolbox.md) and
  [skills/nav-planning/SKILL.md](../../skills/nav-planning/SKILL.md).

## Setup

Not a package (no `setup.py` or `pyproject.toml`): clone it and install NumPy, SciPy, Matplotlib
and cvxpy from the requirements [1][5]. CPU only; CI tests Python 3.14 on Linux, macOS, Windows [1].

```bash
git clone https://github.com/AtsushiSakai/PythonRobotics && cd PythonRobotics
python3 -m venv .venv && .venv/bin/pip install -r requirements/requirements.txt
.venv/bin/python PathPlanning/AStar/a_star.py    # opens a Matplotlib animation
```

From code, import from the repo root as the tests do, with the animation off [1]:

```python
import sys; sys.path.insert(0, "/path/to/PythonRobotics")
from PathPlanning.AStar import a_star
a_star.show_animation = False
rx, ry = a_star.AStarPlanner(ox, oy, 2.0, 1.0).planning(sx, sy, gx, gy)  # grid 2 m, radius 1 m
```

The path runs goal to start; the grid spans only the obstacles' bounding box, so enclose it [1].

## Traps

- **Python version.** The pins need Python 3.12+ (numpy 2.5.4, scipy 1.18.1), so pip fails on
  Ubuntu 22.04's 3.10; use `requirements/environment.yml` (conda, Python 3.13) [1][7]. The docs
  say 3.12, the README 3.13, CI 3.14 [1][4].
- **Run it as the tests do.** Scripts extend `sys.path` and import `utils` or other samples, so a
  copied file breaks; and they open animation windows unless `show_animation` is `False` [1].
- **Edge cases unhandled.** Open issues from November 2026: A* returns a one-point path to an
  unreachable goal, BFS, DFS and bidirectional A* raise errors there, and pure pursuit fails at
  the last waypoint [2]. Test unreachable goals before you port one.
- **No versions.** The only tag is v1.0 (2019-04-04); pin a commit [1]. The textbook's run
  example says `localization/`; the folder is `Localization/`, and Linux is case-sensitive [1][5].

## Alternatives

[Nav2](nav2.md) on a robot; for learning, Peter Corke's Robotics Toolbox for Python and OMPL.

## Sources

1. [PythonRobotics repository: README, LICENSE, requirements, CI workflows, tests, sample code, history and tags](https://github.com/AtsushiSakai/PythonRobotics), accessed 2026-11-24
2. [PythonRobotics issue tracker](https://github.com/AtsushiSakai/PythonRobotics/issues), accessed 2026-11-24
3. [PythonRobotics textbook (documentation site)](https://atsushisakai.github.io/PythonRobotics/index.html), accessed 2026-11-24
4. [PythonRobotics textbook: What is PythonRobotics?](https://atsushisakai.github.io/PythonRobotics/modules/0_getting_started/1_what_is_python_robotics.html), accessed 2026-11-24
5. [PythonRobotics textbook: How to run sample codes](https://atsushisakai.github.io/PythonRobotics/modules/0_getting_started/2_how_to_run_sample_codes.html), accessed 2026-11-24
6. [Sakai et al., PythonRobotics: a Python code collection of robotics algorithms (arXiv 1808.10703)](https://arxiv.org/abs/1808.10703), accessed 2026-11-24
7. [PyPI metadata of the pinned requirements: numpy 2.5.4 and scipy 1.18.1 (Python 3.12 or later)](https://pypi.org/project/numpy/2.5.4/), accessed 2026-11-24

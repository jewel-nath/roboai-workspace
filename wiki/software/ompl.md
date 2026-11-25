---
type: tool
name: OMPL
summary: The Open Motion Planning Library from Rice University's Kavraki Lab; BSD-licensed C++ sampling-based planners (RRT-Connect, PRM, RRT*, KPIECE and many more) with nanobind Python wheels since 2.0, and MoveIt 2's default planner. Jazzy ships 1.7.0, Lyrical 2.0.2.
tags: [ompl, motion-planning, sampling-based-planning, rrt, rrt-connect, prm, rrt-star, kinodynamic, constrained-planning, vamp, python, pip, moveit, kavraki-lab]
kind: library
area: manip
support:
license: BSD-3-Clause
links: {repo: "https://github.com/ompl/ompl", docs: "https://ompl.kavrakilab.org", site: "https://ompl.kavrakilab.org"}
version: {tested: , latest: 2.0.2, as_of: 2026-11-25}
platforms: [linux, macos, windows]
agent_access: script
registry:
evidence: researched
last_verified: 2026-11-25
sources:
  - {url: "https://github.com/ompl/ompl", title: "OMPL repository: README, LICENSE, package.xml, CMakeLists.txt, py-bindings, demos, CI workflows, tags and history", accessed: 2026-11-25}
  - {url: "https://github.com/ompl/ompl/blob/main/doc/markdown/releaseNotes.md", title: "OMPL release notes (1.7.0 to 2.0.2)", accessed: 2026-11-25}
  - {url: "https://github.com/ompl/ompl/blob/main/doc/markdown/installation.md", title: "OMPL installation page source (main branch)", accessed: 2026-11-25}
  - {url: "https://ompl.kavrakilab.org/core/installation.html", title: "OMPL website: Installation", accessed: 2026-11-25}
  - {url: "https://github.com/ompl/ompl/blob/main/doc/markdown/planners.md", title: "OMPL docs source: Available Planners", accessed: 2026-11-25}
  - {url: "https://pypi.org/project/ompl/", title: "ompl on PyPI: releases and wheels", accessed: 2026-11-25}
  - {url: "https://anaconda.org/conda-forge/ompl", title: "ompl on conda-forge", accessed: 2026-11-25}
  - {url: "https://packages.ubuntu.com/search?keywords=libompl-dev&searchon=names&suite=all&section=all", title: "Ubuntu packages: libompl-dev", accessed: 2026-11-25}
  - {url: "https://github.com/ros/rosdistro", title: "rosdistro distribution files: humble, jazzy, kilted, lyrical, rolling", accessed: 2026-11-25}
  - {url: "https://github.com/moveit/moveit2/tree/jazzy/moveit_planners/ompl", title: "moveit2 jazzy branch: moveit_planners_ompl and moveit_configs_utils default configs", accessed: 2026-11-25}
  - {url: "https://moveit.picknik.ai/main/doc/examples/ompl_interface/ompl_interface_tutorial.html", title: "MoveIt docs: OMPL Planner", accessed: 2026-11-25}
  - {url: "https://moveit.picknik.ai/main/doc/how_to_guides/using_ompl_constrained_planning/ompl_constrained_planning.html", title: "MoveIt docs: Using OMPL Constrained Planning", accessed: 2026-11-25}
  - {url: "https://github.com/KavrakiLab/vamp", title: "VAMP repository: README, LICENSE", accessed: 2026-11-25}
  - {url: "https://github.com/ompl/ompl/issues", title: "OMPL issue tracker", accessed: 2026-11-25}
---

# OMPL

OMPL is a C++ library of sampling-based motion planners: RRT-Connect, PRM, RRT\*, KPIECE, EST and
dozens more, over state spaces from R^n and SE(3) to Dubins and Reeds-Shepp cars, plus
kinodynamic planners that plan with controls [1][5]. It has no robot model and no collision
checker: you supply a state space and a validity check. Builders meet it as MoveIt 2's default
planner [10], or use it directly for custom planning problems in C++ or Python. BSD-3-Clause,
from the Kavraki Lab at Rice University [1]. Newest release 2.0.2 (2026-08-14); last commit
2026-11-06; 67 open issues [1][2][14]. ROS binaries: **Jazzy 1.7.0**, Lyrical 2.0.2 [9].

## When to use it

- **Through MoveIt** for arms: the `moveit_planners_ompl` plugin turns a planning group into an
  OMPL state space and uses MoveIt's collision checking; this is the default pipeline [10][11].
- **Directly** for non-arm problems (vehicles, drones, rigid bodies, custom spaces), research and
  benchmarking, or prototyping in Python [1][5]. The README claims over 40 planners and over 20
  state spaces [1].
- **Optimal paths:** RRT\*, PRM\*, BIT\*, AIT\*, AORRTC and others converge towards the shortest
  path with time; RRT-Connect is fast but not optimal [2][5][11].
- **Use something else** for smooth, time-optimal arm trajectories in milliseconds on a GPU
  ([cuRobo](curobo.md)), trajectory optimisation ([Drake](drake.md), or CHOMP and STOMP inside
  [MoveIt 2](moveit2.md)), or a teaching codebase ([PythonRobotics](pythonrobotics.md)).

## Setup

```bash
sudo apt install ros-jazzy-ompl                   # C++, what MoveIt on Jazzy links (1.7.0)
python3 -m venv ~/ompl && ~/ompl/bin/pip install ompl   # Python bindings (2.0.1 on PyPI)
```

| Channel | Version | Python bindings |
|---|---|---|
| ROS Humble, Jazzy, Kilted (`ros-<distro>-ompl`) | 1.7.0 | Docs say no [3][9] |
| ROS Lyrical, Rolling | 2.0.2 | Docs say no [3][9] |
| PyPI `ompl` | 2.0.1 (2026-06-23) | Yes: CPython 3.10 to 3.13, Linux x86-64 and aarch64, macOS 15 [6] |
| conda-forge `ompl` | 2.0.2 | Not stated [7] |
| Ubuntu `libompl-dev` | 1.5.2 on 24.04, 1.6.0 on 26.04 | No [3][8] |
| Homebrew, vcpkg (Windows) | not checked | No [3] |

Building from source needs Boost 1.68+, CMake 3.12+, Eigen 3.3+ and a C++17 compiler; run
`git submodule update --init --recursive` first, because the VAMP backend and nanobind are
submodules [1][3]. Python bindings build by default when Python is found (`pip install
./py-bindings` from a checkout) [1][2]. CPU only; nothing needs CUDA [1]. OMPL.app, the old GUI,
is deprecated as of 2.0.0, and Planner Arena is now `pip install plannerarena` [2].

## How an agent works with it

**Python** (2.x bindings mirror the C++ API; a plain function can be the validity check) [1]:

```python
from ompl import base as ob, geometric as og
space = ob.RealVectorStateSpace(2)
space.setBounds(0.0, 1.0)
ss = og.SimpleSetup(space)
ss.setStateValidityChecker(lambda s: (s[0] - 0.5) ** 2 + (s[1] - 0.5) ** 2 > 0.04)  # a disc
start, goal = space.allocState(), space.allocState()
start[0], start[1], goal[0], goal[1] = 0.0, 0.0, 1.0, 1.0
ss.setStartAndGoalStates(start, goal)
ss.setPlanner(og.RRTConnect(ss.getSpaceInformation()))
if ss.solve(1.0):                      # seconds
    ss.simplifySolution()
    ss.getSolutionPath().printAsMatrix()
```

The core pieces are a `StateSpace` (with bounds), a `StateValidityChecker`, a
`ProblemDefinition` (start, goal, optional `OptimizationObjective`), a `Planner` and a
termination condition; `SimpleSetup` wires them together [1][5]. Demos in `demos/` cover rigid
bodies, cars with controls, constrained planning and optimal planning [1].

**In MoveIt** the group's entry in `ompl_planning.yaml` lists `planner_configs` (for example
`RRTConnectkConfigDefault`, `RRTstarkConfigDefault`), each with a `type` such as
`geometric::RRTstar` and its parameters [10]. Per group you can set `default_planner_config`,
`projection_evaluator` (needed by KPIECE-family planners), `longest_valid_segment_fraction`,
`enforce_joint_model_state_space` and `enforce_constrained_state_space` [10][11]. Without a
`default_planner_config`, MoveIt uses `geometric::RRTConnect` [10]. A request picks one with
`planner_id` and sets `allowed_planning_time` [10]. The skill
[skills/manip-moveit2/SKILL.md](../../skills/manip-moveit2/SKILL.md) covers the MoveIt side.

**Check:** `solve()` returns an exact solution (not approximate); the simplified path passes the
validity checker at fine resolution; in MoveIt, the RViz trajectory clears obstacles and the
log names the planner and its planning time.

## Traps

- **Thin obstacles missed.** Motions are checked at steps of `longest_valid_segment_fraction`
  of the space's largest extent (0.01, OMPL's default, if unset) [10][11]. Too high misses small
  or narrow objects; too low makes planning slow. MoveIt also honours
  `maximum_waypoint_distance` and uses the stricter of the two [11].
- **Optimal planners use the whole time budget.** RRT\* and other optimising planners keep
  refining until the time limit unless you set a `termination_condition` such as
  `CostConvergence[10,.1]` or `ExactSolution` [11].
- **Approximate solutions.** `solve()` can return an approximate path that stops short of the
  goal; check the returned status before using it [1].
- **Orientation constraints are slow.** With orientation path constraints MoveIt samples through
  IK by default; `enforce_joint_model_state_space` switches to rejection sampling, which can take
  far longer [11]. `enforce_constrained_state_space: true` uses OMPL's constrained planning, which
  supports one position or orientation constraint and needs a `projection_evaluator` [12].
- **Python bindings changed in 2.0.** The bindings were rewritten with nanobind [2]. Planners
  exposed in 1.7.0 are missing in 2.0.0 (issue 1419), AORRTC returned zero-length paths from
  Python (1420), and an SST constructor is missing (1482) [14]. Old Py++ scripts may not run.
- **Python and C++ versions differ.** PyPI has 2.0.1 (no 2.0.2 wheels, no Windows wheels) [6],
  while Jazzy's MoveIt links ROS's 1.7.0 [9]. A prototype in Python may use planners that the
  Jazzy C++ build lacks, such as AORRTC from 2.0.0 [2]. Ubuntu 24.04's own `libompl-dev` is
  older still (1.5.2) [8]; in a ROS workspace link `ros-jazzy-ompl`.
- **Stale install page.** The website's installation page still offers 1.7.0 wheel downloads for
  Python 3.10 to 3.12 [4]; the source in the repo says `pip install ompl` [3].
- **VAMP speed needs a supported robot.** VAMP (Apache-2.0) accelerates collision checking and
  forward kinematics with CPU SIMD; the OMPL team claims planning at up to 25 kHz [2][13]. It
  works only for robots compiled into VAMP (demos use Panda, UR5, Fetch and Baxter); adding your
  own needs the separate cricket tool [2][13].

## Alternatives

[MoveIt 2](moveit2.md) wraps OMPL for arms; [cuRobo](curobo.md) for GPU motion generation;
[Drake](drake.md) for optimisation-based planning; [PythonRobotics](pythonrobotics.md) for
teaching implementations. See
[Choose an arm motion planner](../guides/choose-an-arm-motion-planner.md).

## Sources

1. [OMPL repository: README, LICENSE, package.xml, CMakeLists.txt, py-bindings, demos, CI workflows, tags and history](https://github.com/ompl/ompl), accessed 2026-11-25
2. [OMPL release notes (1.7.0 to 2.0.2)](https://github.com/ompl/ompl/blob/main/doc/markdown/releaseNotes.md), accessed 2026-11-25
3. [OMPL installation page source (main branch)](https://github.com/ompl/ompl/blob/main/doc/markdown/installation.md), accessed 2026-11-25
4. [OMPL website: Installation](https://ompl.kavrakilab.org/core/installation.html), accessed 2026-11-25
5. [OMPL docs source: Available Planners](https://github.com/ompl/ompl/blob/main/doc/markdown/planners.md), accessed 2026-11-25
6. [ompl on PyPI: releases and wheels](https://pypi.org/project/ompl/), accessed 2026-11-25
7. [ompl on conda-forge](https://anaconda.org/conda-forge/ompl), accessed 2026-11-25
8. [Ubuntu packages: libompl-dev](https://packages.ubuntu.com/search?keywords=libompl-dev&searchon=names&suite=all&section=all), accessed 2026-11-25
9. [rosdistro distribution files: humble, jazzy, kilted, lyrical, rolling](https://github.com/ros/rosdistro), accessed 2026-11-25
10. [moveit2 jazzy branch: moveit_planners_ompl and moveit_configs_utils default configs](https://github.com/moveit/moveit2/tree/jazzy/moveit_planners/ompl), accessed 2026-11-25
11. [MoveIt docs: OMPL Planner](https://moveit.picknik.ai/main/doc/examples/ompl_interface/ompl_interface_tutorial.html), accessed 2026-11-25
12. [MoveIt docs: Using OMPL Constrained Planning](https://moveit.picknik.ai/main/doc/how_to_guides/using_ompl_constrained_planning/ompl_constrained_planning.html), accessed 2026-11-25
13. [VAMP repository: README, LICENSE](https://github.com/KavrakiLab/vamp), accessed 2026-11-25
14. [OMPL issue tracker](https://github.com/ompl/ompl/issues), accessed 2026-11-25

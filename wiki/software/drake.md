---
type: tool
name: Drake
summary: BSD-3-Clause C++ and Python toolbox led by Toyota Research Institute for multibody dynamics, contact simulation and optimisation-based planning (IK, trajectory optimisation, graphs of convex sets); pip, .deb and tarball builds for Ubuntu 24.04/26.04 and macOS, no ROS 2 binary, and solvers whose licences differ.
tags: [drake, pydrake, multibody, contact-simulation, hydroelastic, inverse-kinematics, trajectory-optimization, gcs, iris, mathematical-program, snopt, mosek, gurobi, drake-ros, tri, manipulation]
kind: library
area: manip
support:
license: BSD-3-Clause
links: {repo: "https://github.com/RobotLocomotion/drake", docs: "https://drake.mit.edu", site: }
version: {tested: , latest: 1.59.0, as_of: 2026-11-25}
platforms: [linux, macos]
agent_access: script
registry:
evidence: researched
last_verified: 2026-11-25
sources:
  - {url: "https://github.com/RobotLocomotion/drake", title: "Drake repository: README, LICENSE.TXT, headers (planning, multibody, geometry, solvers, manipulation), release tags, issue tracker", accessed: 2026-11-25}
  - {url: "https://drake.mit.edu/installation.html", title: "Drake docs: Installation and Quickstart (supported configurations)", accessed: 2026-11-25}
  - {url: "https://drake.mit.edu/pip.html", title: "Drake docs: Installation via Pip", accessed: 2026-11-25}
  - {url: "https://drake.mit.edu/apt.html", title: "Drake docs: Installation via APT", accessed: 2026-11-25}
  - {url: "https://pypi.org/project/drake/", title: "drake on PyPI: releases, wheels and dependencies", accessed: 2026-11-25}
  - {url: "https://drake.mit.edu/release_notes/release_notes.html", title: "Drake release notes, v1.52.0 to v1.59.0, and end-of-support releases", accessed: 2026-11-25}
  - {url: "https://drake.mit.edu/doxygen_cxx/group__solvers.html", title: "Drake docs: Formulating and Solving Optimization Problems (solver table)", accessed: 2026-11-25}
  - {url: "https://drake.mit.edu/bazel.html#proprietary-solvers", title: "Drake docs: Bazel build system, proprietary solvers", accessed: 2026-11-25}
  - {url: "https://drake.mit.edu/doxygen_cxx/group__multibody__parsing.html", title: "Drake docs: Parsing models for MultibodyPlant", accessed: 2026-11-25}
  - {url: "https://drake.mit.edu/doxygen_cxx/group__geometry__file__formats.html", title: "Drake docs: Geometry file formats", accessed: 2026-11-25}
  - {url: "https://drake.mit.edu", title: "Drake documentation home", accessed: 2026-11-25}
  - {url: "https://drake.mit.edu/troubleshooting.html", title: "Drake docs: Troubleshooting", accessed: 2026-11-25}
  - {url: "https://github.com/RobotLocomotion/drake-ros", title: "drake-ros repository: README, drake_ros and drake_ros_examples packages, setup, CI, LICENSE", accessed: 2026-11-25}
  - {url: "https://github.com/ros/rosdistro", title: "rosdistro distribution files: humble, jazzy, kilted, lyrical, rolling", accessed: 2026-11-25}
---

# Drake

Drake is a C++ toolbox with Python bindings (`pydrake`) for robot dynamics, simulation and
optimisation-based planning and control [11]. An arm builder loads the robot into a
`MultibodyPlant`, simulates contact, solves inverse kinematics with collision constraints and
optimises trajectories, including over graphs of convex sets (GCS) [1]. MIT's Robot Locomotion
Group started it; Toyota Research Institute (TRI) now leads core development [11]. BSD-3-Clause,
with some portions under other permissive licences [1]; the solvers it calls carry their own
(see Setup). Releases come monthly: v1.59.0 on 2026-11-17, a commit on 2026-11-24, 587 open
issues [1][6]. **No ROS 2 binary in any distro**: the drake-ros bridge builds from source [13][14].

## When to use it

- **Plan by optimisation, not sampling:** IK with position, orientation, gaze and
  minimum-distance constraints; B-spline trajectory optimisation with velocity and acceleration
  bounds (`KinematicTrajectoryOptimization`); GCS (`GcsTrajectoryOptimization`, experimental),
  which plans only inside collision-free convex regions you compute first, with IRIS [1].
- **Simulate contact-rich manipulation** (point or hydroelastic contact) and design controllers
  in the same Python script [1][10].
- **Pick [MoveIt 2](moveit2.md) instead** for a ROS 2 arm that must move today: it reads URDF and
  SRDF, samples with [OMPL](ompl.md) and sends `JointTrajectory` goals to
  [ros2_control](ros2-control.md). Drake has no sampling planner (RRT, PRM) in its public repo,
  no SRDF parser and no ros2_control interface [1][9]. You can also plan in Drake and send the
  result as a `JointTrajectory` yourself. See
  [Choose an arm motion planner](../guides/choose-an-arm-motion-planner.md).

## Setup

Supported: Ubuntu 24.04 and 26.04 (x86-64, arm64), macOS 26 and 27 (arm64), and Amazon Linux
2023 (pip only); CPython only; no Windows; x86-64 needs at least x86-64-v2 [2]. It is not
tested with Anaconda; on macOS use Homebrew Python [3]. No GPU needed; camera rendering on
Linux needs EGL (`sudo apt install libegl1`) [12].

```bash
python3 -m venv ~/drake && ~/drake/bin/pip install drake        # Python only
~/drake/bin/python -c "import pydrake.all; print('ok')"
```

For C++ plus Python (drake-ros needs both), install the release `.deb` on Ubuntu 24.04 [4]:

```bash
U=https://github.com/RobotLocomotion/drake/releases/download/v1.59.0
wget -O drake-dev.deb $U/drake-dev_1.59.0-1_amd64-noble.deb
sudo apt-get install --no-install-recommends ./drake-dev.deb     # installs to /opt/drake
export PYTHONPATH=/opt/drake/lib/python3.12/site-packages:$PYTHONPATH
```

Also: an APT site (Ubuntu 24.04 amd64 only), tarballs, nightlies kept 56 days, Bazel or CMake
source builds [2][3][4]. PyPI still had 1.58.0; v1.59.0 shipped `.deb` and tarballs [1][5].

**Solver licences** decide what you can run [3][7][8]:

| Solver | Licence | In the binaries |
|---|---|---|
| Clarabel, SCS, OSQP, CLP, CSDP, DAQP, Ipopt, NLopt | open source | yes |
| SNOPT | commercial; Drake's private build needs no licence through `SnoptSolver` | yes |
| MOSEK | commercial; bring a licence (`MOSEKLM_LICENSE_FILE`) | pip: the `[mosek]` extra from v1.59.0 |
| Gurobi 13.0 | commercial; bring a licence (`GRB_LICENSE_FILE`) | no: build from source |

## How an agent works with it

Write Python against `pydrake`. A plant and its `SceneGraph` live in a `Diagram`; IK, trajectory
optimisation and GCS build a `MathematicalProgram`, and `Solve()` picks the solver [1][7]:

```python
from pydrake.all import (AddMultibodyPlantSceneGraph, DiagramBuilder, InverseKinematics,
                         Parser, Solve)
builder = DiagramBuilder()
plant, scene_graph = AddMultibodyPlantSceneGraph(builder, time_step=0.001)
parser = Parser(plant)
parser.package_map().AddPackageXml("share/my_arm_description/package.xml")  # for package://
parser.AddModels("my_arm.urdf")             # URDF, SDFormat, MJCF (.xml) or model directives
plant.WeldFrames(plant.world_frame(), plant.GetFrameByName("base_link"))
plant.Finalize()
diagram = builder.Build()
plant_context = plant.GetMyMutableContextFromRoot(diagram.CreateDefaultContext())
ik = InverseKinematics(plant, plant_context)  # this form accepts collision constraints
tool = plant.GetFrameByName("tool0")
ik.AddPositionConstraint(tool, [0, 0, 0], plant.world_frame(), [0.4, 0, 0.3], [0.4, 0, 0.3])
ik.AddMinimumDistanceLowerBoundConstraint(0.01)   # metres between non-adjacent geometries
result = Solve(ik.prog())
print(result.is_success(), result.get_solver_id().name(), result.GetSolution(ik.q()))
```

- **Check:** `result.is_success()`; the solution inside `plant.GetPositionLowerLimits()` and
  `GetPositionUpperLimits()`; a simulated replay in Meshcat, in the browser [1].
- **Trajectories:** `KinematicTrajectoryOptimization` returns a `BsplineTrajectory` in `q`;
  sample it at the controller's rate into `JointTrajectory` points. GCS paths are not smooth
  where regions meet; retime them with Drake's Toppra for acceleration bounds [1].
- **Hardware:** LCM translators in `manipulation/` (KUKA iiwa, Panda, Jaco, Schunk WSG) [1].
- **ROS 2: drake-ros** (Apache-2.0) adds `RosInterfaceSystem`, publisher, subscriber and clock
  systems, a TF broadcaster for `SceneGraph` frames, and `RvizVisualizer`, which publishes the
  scene as a `MarkerArray` on `/scene_markers` [13]. It targets Ubuntu 24.04 with Jazzy, builds
  with colcon or Bazel, needs Drake's C++ and Python (its docs advise against pip) and pins
  Drake 1.51.0 in its setup [13]. No tags, no rosdistro entry, last commit 2026-10-07 [13][14].
  Its README reads "Usable! But No Stability Commitment" [13].

## Traps

- **STL and DAE meshes are not read.** Drake takes `.obj` for every role, `.gltf` for visuals
  and convex hulls, and tetrahedral `.vtk` for compliant contact; unlisted formats are
  unsupported [10]. Most ROS URDFs ship STL or DAE. Convert them, for example with
  `make_drake_compatible_model` from the `manipulation` package [12].
- **The arm floats.** At `Finalize()`, any body with no joint to a parent gets a 6-DoF floating
  joint [1]. A URDF without a world joint then drifts in IK and falls in simulation. Call
  `WeldFrames` before `Finalize()`.
- **IK fails or ignores collisions.** `InverseKinematics(plant)` without a context cannot take
  minimum-distance constraints. The solve is local (SNOPT, then Ipopt, then NLopt) [1]: on a
  failure, retry from several seeds with `ik.get_mutable_prog().SetInitialGuess(ik.q(), q0)`.
- **No SRDF.** Collision filtering comes from `drake:collision_filter_group` tags in URDF or
  SDFormat, or from code [9]. MoveIt's disabled pairs do not carry over.
- **`package://` lookups.** Register each ROS 2 package with `AddPackageXml` or
  `PopulateFromFolder` (`PopulateFromRosPackagePath` reads the ROS 1 variable).
  `package://drake_models/...` downloads from GitHub on first use: offline robots fail [1].
- **Licence surprises.** Gurobi needs a source build [2]. MOSEK needs your licence; PyPI's 1.58.0
  wheel installs the `Mosek` package by default on x86-64, and v1.59.0 makes it opt-in [5][6].
  SNOPT is free only through Drake's wrapper [7].
- **Python bindings are changing.** pybind11 was deprecated in v1.57.0; wheels switched to
  nanobind in v1.58.0; the project-wide default moves around 2026-12-01; pybind11 nightly wheels
  stop on or after 2027-03-01 [3][6]. Your own pybind11 bindings of Drake types must port.
  drake-ros's CMake looks for Drake's pybind11 fork, so pin a Drake that still ships it [13].
- **Old Ubuntu and fast change.** v1.51.1 was the last release for Ubuntu 22.04 (Humble) [6].
  Releases break APIs: v1.59.0 changed `use_sampled_output_ports` and models closed kinematic
  loops by default [6]. Pin a version; read the notes before upgrading.

## Alternatives

[MoveIt 2](moveit2.md), [OMPL](ompl.md), [Pinocchio](pinocchio.md), [cuRobo](curobo.md) and
[Robotics Toolbox for Python](robotics-toolbox-python.md); for simulation alone, see
[Choose a simulator](../guides/choose-a-simulator.md).

## Sources

1. [Drake repository: README, LICENSE.TXT, headers (planning, multibody, geometry, solvers, manipulation), release tags, issue tracker](https://github.com/RobotLocomotion/drake), accessed 2026-11-25
2. [Drake docs: Installation and Quickstart (supported configurations)](https://drake.mit.edu/installation.html), accessed 2026-11-25
3. [Drake docs: Installation via Pip](https://drake.mit.edu/pip.html), accessed 2026-11-25
4. [Drake docs: Installation via APT](https://drake.mit.edu/apt.html), accessed 2026-11-25
5. [drake on PyPI: releases, wheels and dependencies](https://pypi.org/project/drake/), accessed 2026-11-25
6. [Drake release notes, v1.52.0 to v1.59.0, and end-of-support releases](https://drake.mit.edu/release_notes/release_notes.html), accessed 2026-11-25
7. [Drake docs: Formulating and Solving Optimization Problems (solver table)](https://drake.mit.edu/doxygen_cxx/group__solvers.html), accessed 2026-11-25
8. [Drake docs: Bazel build system, proprietary solvers](https://drake.mit.edu/bazel.html#proprietary-solvers), accessed 2026-11-25
9. [Drake docs: Parsing models for MultibodyPlant](https://drake.mit.edu/doxygen_cxx/group__multibody__parsing.html), accessed 2026-11-25
10. [Drake docs: Geometry file formats](https://drake.mit.edu/doxygen_cxx/group__geometry__file__formats.html), accessed 2026-11-25
11. [Drake documentation home](https://drake.mit.edu), accessed 2026-11-25
12. [Drake docs: Troubleshooting](https://drake.mit.edu/troubleshooting.html), accessed 2026-11-25
13. [drake-ros repository: README, drake_ros and drake_ros_examples packages, setup, CI, LICENSE](https://github.com/RobotLocomotion/drake-ros), accessed 2026-11-25
14. [rosdistro distribution files: humble, jazzy, kilted, lyrical, rolling](https://github.com/ros/rosdistro), accessed 2026-11-25

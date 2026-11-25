---
type: tool
name: Pinocchio
summary: BSD-2-Clause C++ library with Python bindings from Inria and LAAS-CNRS for fast rigid-body kinematics and dynamics with analytical derivatives; loads URDF, SDF, MJCF and SRDF; 4.1.0 binaries for every ROS 2 distro, plus conda-forge and pip `pin`; the base of Crocoddyl, TSID and Aligator. It is not a planner or an IK solver.
tags: [pinocchio, rigid-body-dynamics, kinematics, jacobian, rnea, aba, crba, analytical-derivatives, centroidal, urdf, mjcf, srdf, coal, crocoddyl, tsid, aligator, stack-of-tasks, inria]
kind: library
area: manip
support:
license: BSD-2-Clause
links: {repo: "https://github.com/stack-of-tasks/pinocchio", docs: "https://gepetto.github.io/doc/pinocchio/doxygen-html/", site: "https://stack-of-tasks.github.io/pinocchio/"}
version: {tested: , latest: 4.1.0, as_of: 2026-11-25}
platforms: [linux, macos, windows]
agent_access: script
registry:
evidence: researched
last_verified: 2026-11-25
sources:
  - {url: "https://github.com/stack-of-tasks/pinocchio", title: "Pinocchio repository: README, LICENSE, CHANGELOG, package.xml, examples, Python bindings, headers, porting guides, history and tags", accessed: 2026-11-25}
  - {url: "https://github.com/stack-of-tasks/pinocchio/issues", title: "Pinocchio issue tracker", accessed: 2026-11-25}
  - {url: "https://github.com/ros/rosdistro", title: "rosdistro distribution files: humble, jazzy, kilted, lyrical, rolling", accessed: 2026-11-25}
  - {url: "https://stack-of-tasks.github.io/pinocchio/download.html", title: "Pinocchio website: installation procedure", accessed: 2026-11-25}
  - {url: "https://pypi.org/project/pin/", title: "pin on PyPI: releases, wheels and dependencies", accessed: 2026-11-25}
  - {url: "https://anaconda.org/conda-forge/pinocchio", title: "pinocchio on conda-forge: versions and platforms", accessed: 2026-11-25}
  - {url: "https://pypi.org/project/pinocchio/", title: "pinocchio on PyPI (an unrelated nose plugin)", accessed: 2026-11-25}
  - {url: "https://github.com/loco-3d/crocoddyl", title: "Crocoddyl repository: README, LICENSE, package.xml, tags", accessed: 2026-11-25}
  - {url: "https://github.com/stack-of-tasks/tsid", title: "TSID repository: README, LICENSE, tags", accessed: 2026-11-25}
  - {url: "https://github.com/Simple-Robotics/aligator", title: "Aligator repository: README, LICENSE, tags", accessed: 2026-11-25}
  - {url: "https://github.com/Simple-Robotics/proxsuite", title: "ProxSuite repository: README, LICENSE, tags", accessed: 2026-11-25}
  - {url: "https://github.com/coal-library/coal", title: "Coal repository: README, LICENSE, package.xml, tags", accessed: 2026-11-25}
  - {url: "https://github.com/open-planning/roboplan", title: "RoboPlan repository: README, LICENSE, tags", accessed: 2026-11-25}
---

# Pinocchio

Pinocchio computes the kinematics and dynamics of articulated robots: forward kinematics,
Jacobians, inverse and forward dynamics (RNEA, ABA), the mass matrix (CRBA), centroidal
dynamics, regressors for identification, closed-loop mechanisms and frictional contact, with
analytical derivatives of the main algorithms [1]. Builders call it inside IK loops, gravity
compensation, whole-body controllers, MPC and trajectory optimisation, where derivatives matter.
Inria's Willow team leads it with LAAS-CNRS's Gepetto team; BSD-2-Clause [1]. Release 4.1.0 came
on 2026-07-07; `devel` had a commit on 2026-11-24 and 97 open issues [1][2]. **ROS 2 binaries:
4.1.0 for Humble, Jazzy, Kilted, Lyrical and Rolling** (`ros-jazzy-pinocchio`) [3].

## When to use it

- **Use it** when your own code needs fast rigid-body quantities: FK and Jacobians for a
  Cartesian controller, `M(q)` and gravity torques for a torque controller, or derivatives for
  a DDP or MPC solver [1].
- **It is a library, not a planner.** It has no IK solver, sampling planner or ROS node; the
  examples write their own damped least-squares IK loop [1]. For a ready pipeline use
  [MoveIt 2](moveit2.md); for optimisation-based planning with contact simulation,
  [Drake](drake.md); for GPU planning, [cuRobo](curobo.md); for teaching,
  [Robotics Toolbox for Python](robotics-toolbox-python.md).
- **Build on it:** the projects below add optimal control, whole-body QP control and planning.

## Setup

```bash
sudo apt install ros-jazzy-pinocchio        # C++ and Python, with coal for collisions [1]
source /opt/ros/jazzy/setup.bash && python3 -c "import pinocchio as pin; print(pin.__version__)"
```

| Path | Version | Platforms |
|---|---|---|
| ROS apt `ros-<distro>-pinocchio` | 4.1.0 in humble, jazzy, kilted, lyrical, rolling [3] | Ubuntu |
| conda-forge `pinocchio` | 4.1.0 [6] | linux-64, linux-aarch64, osx-64, osx-arm64, win-64 |
| PyPI `pin` (import `pinocchio`) | 4.1.0, 2026-07-08 [5] | Linux x86-64, aarch64; macOS x86-64, arm64; CPython 3.10 to 3.14 |
| robotpkg apt, Homebrew tap, Nix, AUR, Docker | per channel [1][4] | Linux, macOS |

```bash
conda install -c conda-forge pinocchio                  # also on Windows
python3 -m venv ~/pin && ~/pin/bin/pip install pin      # Linux and macOS wheels
```

CI covers ROS, Linux apt, and macOS, Linux and Windows through Pixi [1]. Nothing needs a GPU.
In a ROS 2 C++ package: `<depend>pinocchio</depend>`, `find_package(pinocchio REQUIRED)` and
link `pinocchio::pinocchio` [1].

## How an agent works with it

A `Model` holds the constant tree; a `Data` holds the workspace for each computation; every
algorithm takes `(model, data, q, ...)` and writes into `data` [1]:

```python
import numpy as np
import pinocchio as pin
model, collision_model, visual_model = pin.buildModelsFromUrdf(
    "my_arm.urdf", package_dirs=["install/my_arm_description/share"])
data = model.createData()
q, v, a = pin.neutral(model), np.zeros(model.nv), np.zeros(model.nv)   # q has model.nq values
pin.forwardKinematics(model, data, q)
pin.updateFramePlacements(model, data)        # fills data.oMf; FK alone does not
tool = model.getFrameId("tool0")
print(data.oMf[tool])                         # SE3 pose of the tool in the world
J = pin.computeFrameJacobian(model, data, q, tool, pin.LOCAL_WORLD_ALIGNED)
tau = pin.rnea(model, data, q, v, a)          # inverse dynamics; v = a = 0 gives gravity
M = pin.crba(model, data, q)                  # mass matrix; Python returns it symmetric
```

- **Model sources:** URDF (with mesh `package_dirs`), SDF, MJCF (`buildModelFromMJCF`), a URDF
  string (`buildModelFromXML`, for example from `/robot_description`), or code; see
  [URDF](urdf.md) [1].
- **Collisions:** `collision_model.addAllCollisionPairs()`, then
  `pin.removeCollisionPairs(model, collision_model, "my_arm.srdf")` drops the pairs a MoveIt SRDF
  disables; `pin.computeCollisions(model, data, collision_model, pin.GeometryData(collision_model),
  q, False)` checks a pose with coal [1].
- **IK:** iterate `q = pin.integrate(model, q, v * dt)` with a damped least-squares step from
  the Jacobian of `pin.log(...)` error, as `examples/inverse-kinematics.py` does; stop on a
  tolerance and an iteration cap, and report whether it converged [1].
- **Check:** compare `data.oMf` with `tf2_echo` on the real robot for the same joint state; a
  gravity-torque check: `pin.computeGeneralizedGravity(model, data, q)` should match the arm's
  holding torques within its model error [1].
- **Viewers:** Meshcat, Viser, Panda3D, Gepetto Viewer and RViz [1].

**Projects built on it** (checked 2026-11-25):

| Project | Does | Licence | Get it |
|---|---|---|---|
| Crocoddyl (loco-3d) | DDP optimal control and MPC with contacts | BSD-3-Clause | ROS 3.2.1 (Lyrical 3.2.0), conda, pip [3][8] |
| TSID | task-space inverse-dynamics QP control | BSD-2-Clause | ROS 1.10.0 in all five distros, conda [3][9] |
| Aligator (Simple-Robotics) | constrained trajectory optimisation | BSD-2-Clause | conda-forge, source; no rosdistro entry [3][10] |
| ProxSuite | QP solvers (ProxQP) | BSD-2-Clause | ROS 0.8.3, pip, conda [3][11] |
| Coal | collision detection, formerly HPP-FCL | BSD-3-Clause | ROS 3.0.3, conda [3][12] |
| RoboPlan | arm IK, RRT, TOPP-RA and Cartesian planning; experimental before 1.0 | MIT | ROS 0.8.0 for Jazzy onward, pip [3][13] |

All six had commits in November 2026 [8][9][10][11][12][13]. The README also lists HPP, OCS2,
PlaCo, Jiminy and CRISP controllers, a set of `ros2_control` controllers for compliant arms [1].

## Traps

- **`q` is not one value per URDF joint.** Continuous joints take two (cos, sin); a free-flyer
  root takes seven, its quaternion ordered (x, y, z, w); fixed joints become frames [1]. Size
  vectors from `model.nq` and `model.nv`, build them with `pin.neutral`, and step with
  `pin.integrate`, never `q + v`. Map joint names through `model.names`, not URDF order.
- **Stale frames.** `forwardKinematics` updates joints (`data.oMi`), not frames: call
  `updateFramePlacements` or `framesForwardKinematics` before reading `data.oMf` [1].
- **Wrong Jacobian frame.** `computeFrameJacobian` without a reference frame returns `LOCAL`
  coordinates [1]. Mixing that with a world-frame error makes IK diverge; pass
  `LOCAL_WORLD_ALIGNED` or `WORLD` to match your error.
- **Half a mass matrix in C++.** C++ `crba` fills only the upper triangle of `data.M`; the
  Python binding copies it to make it symmetric [1]. Symmetrise before using it in C++.
- **Mimic joints ignored.** `buildModelsFromUrdf` defaults `mimic=False`, so a gripper's mimic
  fingers become independent joints [1]. Pass `mimic=True`.
- **Wrong package from pip.** `pip install pinocchio` installs an unrelated nose plugin [7];
  the package is `pin`. The `pin` wheels come from the cmeel project and declare BSD-3-Clause,
  while the LICENSE file says BSD-2-Clause [1][5]. There is no Windows wheel; use conda [5][6].
- **One source per environment.** ROS apt, `pin` and conda each bring their own builds of coal,
  eigenpy and Boost [3][5][6]. Do not mix them in one Python environment.
- **Version 4 broke version 3 code.** 4.0.0 (2026-04-13) replaced HPP-FCL with coal
  (`pinocchio.hppfcl` became `pinocchio.coal`), required C++17, Eigen 3.4 and Boost 1.74, removed
  the 3.x deprecated API and pkg-config files, and dropped PyPy [1]. Every distro's apt package
  is now 4.1.0 [3]; port with `doc/_porting/porting-3-to-4.md` or pin an older build.
- **Stale install page.** The website still names HPP-FCL and Python 2.7 paths [4]; trust the
  README and CHANGELOG [1].
- **C++ build errors.** Include `pinocchio/fwd.hpp` first to avoid Boost variant size errors [1].

## Alternatives

[Drake](drake.md) for dynamics plus optimisation and contact simulation;
[Robotics Toolbox for Python](robotics-toolbox-python.md) for teaching; RBDL and Orocos KDL are
other dynamics libraries; [MoveIt 2](moveit2.md) and [cuRobo](curobo.md) for planning.

## Sources

1. [Pinocchio repository: README, LICENSE, CHANGELOG, package.xml, examples, Python bindings, headers, porting guides, history and tags](https://github.com/stack-of-tasks/pinocchio), accessed 2026-11-25
2. [Pinocchio issue tracker](https://github.com/stack-of-tasks/pinocchio/issues), accessed 2026-11-25
3. [rosdistro distribution files: humble, jazzy, kilted, lyrical, rolling](https://github.com/ros/rosdistro), accessed 2026-11-25
4. [Pinocchio website: installation procedure](https://stack-of-tasks.github.io/pinocchio/download.html), accessed 2026-11-25
5. [pin on PyPI: releases, wheels and dependencies](https://pypi.org/project/pin/), accessed 2026-11-25
6. [pinocchio on conda-forge: versions and platforms](https://anaconda.org/conda-forge/pinocchio), accessed 2026-11-25
7. [pinocchio on PyPI (an unrelated nose plugin)](https://pypi.org/project/pinocchio/), accessed 2026-11-25
8. [Crocoddyl repository: README, LICENSE, package.xml, tags](https://github.com/loco-3d/crocoddyl), accessed 2026-11-25
9. [TSID repository: README, LICENSE, tags](https://github.com/stack-of-tasks/tsid), accessed 2026-11-25
10. [Aligator repository: README, LICENSE, tags](https://github.com/Simple-Robotics/aligator), accessed 2026-11-25
11. [ProxSuite repository: README, LICENSE, tags](https://github.com/Simple-Robotics/proxsuite), accessed 2026-11-25
12. [Coal repository: README, LICENSE, package.xml, tags](https://github.com/coal-library/coal), accessed 2026-11-25
13. [RoboPlan repository: README, LICENSE, tags](https://github.com/open-planning/roboplan), accessed 2026-11-25

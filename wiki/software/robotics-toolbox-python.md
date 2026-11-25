---
type: tool
name: Robotics Toolbox for Python
summary: MIT-licensed Python library by Peter Corke and Jesse Haviland for arm kinematics, Jacobians, IK, dynamics and trajectories, plus mobile-robot planning and estimation, with about 50 bundled robot models and the Swift browser visualiser; for teaching and prototyping, with no ROS 2 interface. Active again since mid-2026 after two quiet years.
tags: [robotics-toolbox, python, kinematics, jacobian, inverse-kinematics, dynamics, rne, trajectory, dh-parameters, ets, urdf, swift, education, prototyping, peter-corke]
kind: library
area: manip
support:
license: MIT
links: {repo: "https://github.com/petercorke/robotics-toolbox-python", docs: "https://petercorke.github.io/robotics-toolbox-python/", site: }
version: {tested: , latest: 1.5.0, as_of: 2026-11-25}
platforms: [linux, macos, windows]
agent_access: script
registry:
evidence: researched
last_verified: 2026-11-25
sources:
  - {url: "https://github.com/petercorke/robotics-toolbox-python", title: "Robotics Toolbox for Python repository: README, LICENSE, CHANGELOG, pyproject.toml, models, backends, trajectory and IK sources, CI, history and tags", accessed: 2026-11-25}
  - {url: "https://github.com/petercorke/robotics-toolbox-python/issues", title: "Robotics Toolbox for Python issue tracker", accessed: 2026-11-25}
  - {url: "https://pypi.org/project/roboticstoolbox-python/", title: "roboticstoolbox-python on PyPI: release history and wheels", accessed: 2026-11-25}
  - {url: "https://github.com/jhavl/swift", title: "Swift repository: README, LICENSE, history", accessed: 2026-11-25}
---

# Robotics Toolbox for Python

The Robotics Toolbox for Python models serial arms from DH parameters, an elementary transform
sequence (ETS) or a URDF: forward kinematics, Jacobians, numerical and analytic IK, Newton-Euler
dynamics and trajectories, plus mobile-robot planning and estimation [1]. MIT, by Peter Corke
and Jesse Haviland [1]. 1.5.0 came on 2026-10-23, the last commit on 2026-11-19; 56 open issues.
Quiet from 1.1.1 (2024-05) to 1.3.0 (2026-06), it has released about monthly since [1][2][3].
**No ROS 2 interface**: its ROS backend imports ROS 1's `rospy` [1].

## When to use it

- **Teaching and prototyping:** about 50 bundled models (Panda, UR3/5/10, Kinova Gen3, LBR,
  YuMi, Puma 560, [Interbotix](../robots/interbotix-x-series-arms.md) arms), more through
  `robot_descriptions`; it accompanies Corke's *Robotics, Vision & Control* [1]. Check reach
  and IK on a model, or try resolved-rate control in the Swift browser view [1][4].
- **Not to run an arm:** no arm planner beyond joint and Cartesian interpolation, no controller
  interface [1]. Use [MoveIt 2](moveit2.md) on a ROS 2 arm, [Pinocchio](pinocchio.md) for
  dynamics in production code and [Drake](drake.md) for optimisation-based planning.

## Setup

```bash
python3 -m venv ~/rtb && ~/rtb/bin/pip install "roboticstoolbox-python[swift]"
~/rtb/bin/python -c "import roboticstoolbox as rtb; print(rtb.models.Panda())"
```

CPU only. Wheels: Linux, macOS arm64, Windows x86-64, CPython 3.10 to 3.14 [3]; `main` needs
3.11 [1]. Extras: `swift`, `qp`, `collision` (no coal on Windows), `tool`, `ik`, `all` [1].

## How an agent works with it

```python
import roboticstoolbox as rtb
from spatialmath import SE3
robot = rtb.models.Panda()                       # or URDFRobot("ur5") via robot_descriptions
Tep = SE3.Trans(0.6, -0.3, 0.1) * SE3.OA([0, 1, 0], [0, 0, -1])
sol = robot.ik_LM(Tep)                           # C++ solver; joint_limits=True by default
print(sol.success, robot.fkine(sol.q))           # sol.q is invalid when success is False
traj = rtb.jtraj(robot.qr, sol.q, [0.02 * k for k in range(100)])   # 2 s, times in seconds
robot.plot(traj.q, backend="pyplot")             # or Swift in the browser
```

## Traps

- **Default Panda has no dynamics.** The bundled URDF Panda has no inertial data; in 1.5.0
  `rne()`, `inertia()` and `gravload()` raise `ValueError` on it, while older versions (and its
  docstring) give silent zeros. Use `Panda(use_robot_descriptions=True)` [1].
- **Old versions give wrong torques.** Before 1.4.4 (2026-09-20), `rne()` was wrong for links
  with translational offsets and `robot.tool` was ignored unless passed each call [1].
- **`jtraj` time is not seconds by default.** Given a step count, time runs 0 to 1; pass a time
  vector. It never checks joint velocity limits [1].
- **Swift 2.0 changed the API.** Drive a robot through the handle `env.add()` returns
  (`handle.q`); setting `robot.q` is deprecated [1][4]. On Windows the toolbox README calls for
  a one-line Swift patch; Swift's README says Windows works [1][4].
- **Downloads on first use.** `URDFRobot("ur5")` fetches through `robot_descriptions` [1]; vendor
  the URDF for an offline robot.

## Alternatives

[PythonRobotics](pythonrobotics.md) for mobile algorithms; the original MATLAB Robotics Toolbox.

## Sources

1. [Robotics Toolbox for Python repository: README, LICENSE, CHANGELOG, pyproject.toml, models, backends, trajectory and IK sources, CI, history and tags](https://github.com/petercorke/robotics-toolbox-python), accessed 2026-11-25
2. [Robotics Toolbox for Python issue tracker](https://github.com/petercorke/robotics-toolbox-python/issues), accessed 2026-11-25
3. [roboticstoolbox-python on PyPI: release history and wheels](https://pypi.org/project/roboticstoolbox-python/), accessed 2026-11-25
4. [Swift repository: README, LICENSE, history](https://github.com/jhavl/swift), accessed 2026-11-25

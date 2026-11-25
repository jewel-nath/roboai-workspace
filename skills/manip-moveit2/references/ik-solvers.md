# IK solvers for MoveIt (Jazzy)

Part of [manip-moveit2](../SKILL.md). Release state from `ros/rosdistro` `jazzy/distribution.yaml` on 2026-11-25;
parameters from each plugin's source (`moveit_kinematics` 2.12.4, `trac_ik` `jazzy` branch 2.0.2, `pick_ik` 1.1.2).
No speed or success-rate numbers are given here: measure them on your arm (see the end).

## Choose

| Solver | Jazzy install | `kinematics_solver` value | Licence | Use it when |
|---|---|---|---|---|
| KDL | in `ros-jazzy-moveit` (`moveit_kinematics`) | `kdl_kinematics_plugin/KDLKinematicsPlugin` | BSD-3-Clause | The default. Serial chains; start here |
| TRAC-IK | `ros-jazzy-trac-ik-kinematics-plugin` | `trac_ik_kinematics_plugin/TRAC_IKKinematicsPlugin` | BSD | KDL fails near joint limits; you want the solution nearest the seed or most manipulable |
| pick_ik | `ros-jazzy-pick-ik` | `pick_ik/PickIkPlugin` | BSD-3-Clause | Custom cost terms, approximate or rotation-only IK (Servo). **Deprecated by PickNik**, basic maintenance only |
| IKFast | generated per robot (see below) | `<package>/IKFastKinematicsPlugin` | `ikfast.h` Apache-2.0, template BSD-3-Clause | 6-DOF arm with an analytic solution; you need every solution, fast and repeatable |
| Cached IK | in `moveit_kinematics` | `cached_ik_kinematics_plugin/CachedKDLKinematicsPlugin` | BSD-3-Clause | Many similar queries; seeds KDL from a cache on disk |

Not available on Jazzy: `lma_kinematics_plugin` (removed from MoveIt 2), `bio_ik` (no ROS 2 release; pick_ik
reimplements it), `CachedTRACKinematicsPlugin` (commented out of the plugin list).

Every plugin reads `kinematics_solver_timeout` (Jazzy default 0.05 s). `kinematics_solver_search_resolution`
(default 0.1) matters only for redundant joints. `kinematics_solver_attempts` is not read by MoveIt 2.

## KDL

```yaml
arm:
  kinematics_solver: kdl_kinematics_plugin/KDLKinematicsPlugin
  kinematics_solver_timeout: 0.05
  position_only_ik: false          # true for arms with fewer than 6 DOF that cannot hold an orientation
  orientation_vs_position: 1.0     # weight; position_only_ik overrides it
  max_solver_iterations: 500
  epsilon: 1.0e-5
```

Numeric, seeded from the current state, restarts with random seeds until the timeout. Obeys URDF joint limits.
For a 4- or 5-DOF hobby arm, full-pose goals usually have no solution: use `position_only_ik: true` or plan with
joint goals.

## TRAC-IK

```bash
sudo apt install ros-jazzy-trac-ik-kinematics-plugin
```

```yaml
arm:
  kinematics_solver: trac_ik_kinematics_plugin/TRAC_IKKinematicsPlugin
  kinematics_solver_timeout: 0.005
  solve_type: Speed        # Speed | Distance | Manipulation1 | Manipulation2 | Manipulation3
  epsilon: 1.0e-5
  position_only_ik: false
```

- Runs a KDL-style Newton solver and an SQP solver in parallel and returns the first answer (`Speed`), or uses the
  whole timeout to return the solution closest to the seed (`Distance`) or the most manipulable one.
- The Jazzy plugin's generated parameter file defaults `solve_type` to `Distance`, although its README says
  `Speed`; set it explicitly. With `Distance` every call uses the full timeout, so keep the timeout short.
- Mimic joints are not supported. Add `<exec_depend>trac_ik_kinematics_plugin</exec_depend>` to the config
  package. Upstream moved from Bitbucket to `github.com/traclabs/trac_ik` (branches `jazzy`, `kilted`,
  `rolling`, `master`).

## pick_ik

```bash
sudo apt install ros-jazzy-pick-ik
```

```yaml
arm:
  kinematics_solver: pick_ik/PickIkPlugin
  kinematics_solver_timeout: 0.05
  mode: global                    # local = gradient descent only (Cartesian moves, Servo); global adds the evolutionary search
  position_threshold: 0.001       # m
  orientation_threshold: 0.01     # rad
  rotation_scale: 0.5             # 0 = position-only IK
  minimal_displacement_weight: 0.0  # small non-zero value for Servo and Cartesian paths
```

Parameters can be changed live on the node that loaded the plugin, for example
`ros2 param set /move_group robot_description_kinematics.arm.mode local` (`mode` defaults to `global`). The
README on `main` (read 2026-11-25) says PickNik no longer uses or develops it and seeks a new owner: prefer KDL
or TRAC-IK for new work.

## IKFast

An analytic solver generated from the robot's kinematics by OpenRAVE. MoveIt's script needs Docker and builds an
Ubuntu 14.04 / ROS Indigo / OpenRAVE 0.9 image from the third-party `personalrobotics/ros-openrave` image; its apt
steps reach long-retired repositories, so expect to repair the Dockerfile. If it will not build, use TRAC-IK.

```bash
xacro my_robot.urdf.xacro hardware:=mock > my_robot.urdf
ros2 run moveit_kinematics auto_create_ikfast_moveit_plugin.sh --iktype Transform6D my_robot.urdf arm base_link tool0
colcon build --packages-select my_robot_arm_ikfast_plugin
```

- `Transform6D` is the full-pose type. The tutorial reports MoveIt IKFast tested on 6- and 7-DOF arms and not
  supporting more than 7 DOF; lower-DOF arms use other IK types (`Translation3D`, `TranslationDirection5D`, ...).
- The script writes the package `<robot>_<group>_ikfast_plugin` and tries to edit `kinematics.yaml`; check that
  the group now names `my_robot_arm_ikfast_plugin/IKFastKinematicsPlugin`.
- If generation hangs, round the Collada file with `ros2 run moveit_kinematics round_collada_numbers.py in.dae
  out.dae 5` (the tutorial suggests 5 decimals) and re-run the script on the `.dae`.
- Regenerate (`update_ikfast_plugin.sh` in the generated package) whenever the URDF kinematics change.

## Prove the solver

Before planning, check IK alone through `move_group`'s `/compute_ik` service:

```bash
ros2 service call /compute_ik moveit_msgs/srv/GetPositionIK "{ik_request: {group_name: arm, avoid_collisions: true,
  pose_stamped: {header: {frame_id: base_link}, pose: {position: {x: 0.3, y: 0.0, z: 0.3}, orientation: {w: 1.0}}},
  timeout: {sec: 0, nanosec: 50000000}}}"
```

`error_code.val: 1` is success, `-31` is `NO_IK_SOLUTION`. Script 50-100 poses taken from forward kinematics of
random valid joint states (so each is reachable) and record the success rate and time per solver; keep the
numbers with the config. In RViz, dragging the interactive marker should move the arm smoothly without
flips; jumps mean the solver lands in different branches, which `Distance` (TRAC-IK) or a seed near the current
state reduces.

A node that calls `RobotState::setFromIK()` itself (not through `move_group`) loads the plugin locally and needs
`robot_description_kinematics` among its own parameters, or it logs `No kinematics plugins defined`.

---
type: guide
name: Choose an arm motion planner
summary: Which motion planner a 4- to 7-DoF arm should start with on ROS 2 Jazzy (MoveIt 2's OMPL, Pilz, STOMP or CHOMP pipelines, GPU planning with cuRobo or Isaac ROS cuMotion, Drake's trajectory optimisation, or a Python toolbox), decided by the motion, where obstacles come from, CPU or GPU, cycle time, licences and ROS 2; with IK and timing pairings that work.
tags: [motion-planning, manipulation, arm, moveit, moveit2, ompl, rrt-connect, pilz, stomp, chomp, curobo, cumotion, isaac-ros, drake, gcs, trajectory-optimization, inverse-kinematics, kdl, trac-ik, pick-ik, totg, ruckig, robotics-toolbox, pinocchio, ros2]
question: Which motion planner should my robot arm use?
options: [ompl, pilz-industrial, stomp, chomp, curobo, isaac-ros-cumotion, drake, robotics-toolbox-python, pinocchio]
recommendation: "MoveIt 2 with OMPL's RRTConnect (the Jazzy default), KDL and TOTG for most ROS 2 arms, adding Pilz LIN for straight approaches; joint or position-only goals on 4- and 5-DoF hobby arms; cuRobo or Isaac ROS cuMotion only with an NVIDIA GPU and a need for millisecond or batched planning; Drake for optimisation work outside ROS."
evidence: researched
last_verified: 2026-11-25
sources:
  - {url: "https://github.com/moveit/moveit2/tree/2.12.4", title: "moveit2 tag 2.12.4: package.xml files, moveit_configs_utils default configs, Setup Assistant templates, planning pipeline, OMPL, Pilz, CHOMP, STOMP and Ruckig sources, MIGRATION.md, trajectory_cache README", accessed: 2026-11-25}
  - {url: "https://github.com/moveit/moveit2_tutorials", title: "moveit2_tutorials (main): Pilz, CHOMP, STOMP, parallel planning, time parameterization, hybrid planning and planning adapter pages", accessed: 2026-11-25}
  - {url: "https://github.com/ros/rosdistro", title: "rosdistro distribution files: humble, jazzy, kilted, lyrical, rolling", accessed: 2026-11-25}
  - {url: "https://github.com/traclabs/trac_ik/tree/jazzy", title: "trac_ik jazzy branch and tag 2.0.2: README, plugin README, generated parameter file, CHANGELOG", accessed: 2026-11-25}
  - {url: "https://github.com/PickNikRobotics/pick_ik", title: "pick_ik repository (main): README deprecation notice, package.xml", accessed: 2026-11-25}
  - {url: "https://github.com/NVIDIA-ISAAC-ROS/isaac_ros_cumotion", title: "isaac_ros_cumotion release-4.0 to release-5.1 branches: LICENSE, package.xml files, CMakeLists.txt, MoveIt plugin and its config", accessed: 2026-11-25}
  - {url: "https://nvidia-isaac-ros.github.io/releases/index.html", title: "Isaac ROS release notes (4.0.0 to 5.1.0)", accessed: 2026-11-25}
  - {url: "https://nvidia-isaac-ros.github.io/repositories_and_packages/isaac_ros_cumotion/index.html", title: "Isaac ROS docs: Isaac ROS cuMotion (release 5.1)", accessed: 2026-11-25}
  - {url: "https://github.com/nvidia-isaac/cumotion", title: "NVIDIA cuMotion library repository: README, LICENSE", accessed: 2026-11-25}
  - {url: "https://github.com/NVlabs/curobo", title: "cuRobo repository: README, LICENSE, tags, docs/reference/benchmarks.rst", accessed: 2026-11-25}
  - {url: "https://github.com/RobotLocomotion/drake", title: "Drake repository: LICENSE.TXT, planning/trajectory_optimization headers", accessed: 2026-11-25}
---

# Choose an arm motion planner

Which planner should move your arm to a goal without hitting anything? For builders of a 4- to
7-DoF arm on ROS 2 Jazzy, with later distros noted: a hobby arm such as
[SO-101](../robots/so-101.md) or [OpenManipulator-X](../robots/openmanipulator-x.md), a cobot
such as a [UR](../robots/universal-robots.md) or [Franka](../robots/franka-panda.md), or a mobile
manipulator. Bring-up is in [manip-moveit2](../../skills/manip-moveit2/SKILL.md); the pick
sequence in [manip-grasping](../../skills/manip-grasping/SKILL.md).

## Short answer

- **Most ROS 2 arms:** [MoveIt 2](../software/moveit2.md) with [OMPL](../software/ompl.md)'s
  RRTConnect, KDL IK and TOTG timing. A Jazzy config gets this without asking: the Setup
  Assistant writes no `ompl_planning.yaml`, so `MoveItConfigsBuilder` loads its default OMPL,
  Pilz, CHOMP and STOMP pipelines, makes `ompl` the default, and OMPL falls back to
  `geometric::RRTConnect` [1].
- **Straight approaches and repeatable cell moves:** add Pilz `LIN` for the last centimetres and
  `PTP` for joint moves, and keep OMPL for the transfer; Pilz draws a fixed shape and does not
  search around obstacles, so a colliding result just fails `ValidateSolution` [1][2].
- **4- and 5-DoF hobby arms:** the same stack with joint goals or position-only IK (KDL
  `position_only_ik: true`). A full 6-D pose rarely has a solution, and Pilz `LIN` and `CIRC`
  solve IK at every sample of the line [1].
- **An NVIDIA GPU on the robot and a need for milliseconds or many goals at once:**
  [cuRobo](../software/curobo.md) from Python, or Isaac ROS cuMotion as a MoveIt planner plugin.
  Read their licences first [6][10].
- **Optimisation research, offline planning or no ROS:** [Drake](../software/drake.md). To learn
  kinematics or check reach: [Robotics Toolbox for Python](../software/robotics-toolbox-python.md).

## What decides it

- **The motion.** Free-space moves among known obstacles suit OMPL; RRTConnect stops at its first
  path, while RRT\* and PRM\* refine until the time limit ([OMPL](../software/ompl.md)). Straight
  lines and arcs of the tool suit Pilz `LIN` and `CIRC`, with trapezoidal Cartesian profiles from
  `pilz_cartesian_limits.yaml` [2]. Orientation constraints (a cup kept upright) go to OMPL path
  constraints, which are slow; its constrained state space takes one position or orientation
  constraint ([OMPL](../software/ompl.md)). For smooth paths, STOMP avoids the local minima CHOMP
  falls into, and both take comparable time; non-optimising OMPL planners are usually quicker [2].
- **Many repeated queries.** MoveItCpp (and MoveItPy) can run several pipelines in parallel and
  keep one result [2]. MoveIt's trajectory cache replays plans for similar requests but ignores
  collisions, so check a fetched plan before running it [1]. cuRobo batches IK and planning [10].
- **Where obstacles come from.** A known table and walls become collision objects. A live depth
  camera feeds MoveIt's octomap updaters, which live in `moveit_ros_perception`; `ros-jazzy-moveit`
  does not install it, `ros-jazzy-moveit-ros-perception` or `ros-jazzy-moveit-runtime` does, and
  it needs a `sensors_3d.yaml` [1][3]. cuRobo checks fitted spheres against cuboids, meshes,
  voxels or an ESDF from depth [10]; cuMotion also segments the arm out of depth images [9].
- **CPU or GPU.** MoveIt's planners, Drake, the toolbox and [Pinocchio](../software/pinocchio.md)
  run on the CPU. cuRobo needs an NVIDIA GPU newer than Turing with 4 GB
  ([cuRobo](../software/curobo.md)); the cuMotion library asks for Ampere or later on x86, or a
  Jetson Orin, Thor or DGX Spark [9].
- **Cycle time.** NVIDIA reports cuRobo planning in 3.8 ms on average on an RTX 5090 (25.7 ms on
  a Jetson AGX Orin), solving 99.73% of 2,590 Franka benchmark problems, warmed up in C++ with
  CUDA graphs [10]. No figure for MoveIt on the same problems was found; time your own arm.
  TOTG and Pilz profiles are limited by `joint_limits.yaml` and the scaling factors, which the
  Setup Assistant sets to 0.1 ([MoveIt 2](../software/moveit2.md)).
- **Licences.** MoveIt's planner packages and KDL are BSD-3-Clause [1]; TRAC-IK says BSD, pick_ik
  BSD-3-Clause [4][5]. cuRobo is Apache-2.0 from v0.8.0; v0.7.8 and older stay non-commercial
  [10]. cuMotion is under the NVIDIA Isaac ROS Software License, for systems with NVIDIA GPUs
  [6][9]. Drake is BSD-3-Clause [11], but MOSEK and Gurobi need your own licence
  ([Drake](../software/drake.md)).
- **ROS 2 or not.** MoveIt, TRAC-IK, pick_ik and Pinocchio have Jazzy binaries; cuRobo, cuMotion
  and Drake are not in rosdistro [3]. cuRobo and Drake give you a trajectory to send to a
  `joint_trajectory_controller` yourself; cuMotion comes from Isaac ROS.

## Options compared

| Option | Cost | Strengths | Limits | Best when |
|---|---|---|---|---|
| OMPL in MoveIt (RRTConnect) | BSD-3-Clause; CPU; in `ros-jazzy-moveit` (OMPL 1.7.0) [1][3] | The default; finds a collision-free path quickly; many planners selectable by `planner_id` | Random, wandering paths, shortened but not optimal; orientation constraints slow | Free-space moves among known obstacles: the starting point |
| Pilz industrial (PTP, LIN, CIRC) | BSD-3-Clause; CPU; in `ros-jazzy-moveit` [1] | Predictable shapes with trapezoidal timing; sequences with blend radii through `MoveGroupSequenceAction` [2] | Does not avoid obstacles; LIN and CIRC need IK along the path and Cartesian limits; no `POLYLINE` on Jazzy [1][2] | Approach and retreat, straight tool moves, repeatable cell cycles |
| STOMP | BSD-3-Clause; CPU; Jazzy binary, none for Humble [1][3] | Smooth paths; needs no gradients; escapes local minima better than CHOMP [2] | Slower than RRTConnect; tune `num_timesteps` and rollouts; no custom-cost API in MoveIt yet [2] | Smoothness matters more than planning time |
| CHOMP | BSD-3-Clause; CPU; in `ros-jazzy-moveit` [1] | Pulls an interpolated start-to-goal guess out of collision while smoothing it [1][2] | Local minima among many obstacles; can cut through a thin obstacle [2] | Open workspaces; seldom the first choice |
| cuRobo | Apache-2.0 from v0.8.0; NVIDIA GPU; Python on Linux; no ROS release [3][10] | Batched IK and collision-aware motion generation in milliseconds; MPC; ESDF from depth images [10] | Spheres approximate the arm; you write the ROS bridge; v0.7.8 and older non-commercial [10] | A GPU on board, many goals or grasps, fast replanning |
| Isaac ROS cuMotion | MoveIt plugin Apache-2.0, but it needs `isaac_ros_cumotion` (NVIDIA Isaac ROS Software License); NVIDIA GPU; not in rosdistro [3][6] | Loads into `move_group` as `isaac_ros_cumotion_moveit/CumotionPlanner`; GPU IK and trajectory optimisation [6][8][9] | NVIDIA hardware and licence; the last Jazzy release is Isaac ROS 4.6 [6][7] | A Jetson or RTX robot already on Isaac ROS |
| Drake | BSD-3-Clause; CPU; MOSEK and Gurobi licences extra; no ROS binary [3][11] | IK with collision constraints ([page](../software/drake.md)); B-spline trajectory optimisation and graphs of convex sets (GCS) [11] | No SRDF and no sampling planner ([page](../software/drake.md)); GCS is experimental [11] | Research, offline or optimal plans, contact simulation beside planning |
| Robotics Toolbox for Python | MIT; CPU; pip ([page](../software/robotics-toolbox-python.md)) | IK, Jacobians and joint or Cartesian interpolation on about 50 bundled models; browser viewer | No collision-aware planner, no ROS 2 interface | Teaching, reach checks, trying resolved-rate control |
| Pinocchio (with your IK, or RoboPlan) | BSD-2-Clause; CPU; Jazzy binary 4.1.0 [3] | Fast FK, Jacobians and dynamics; RoboPlan (MIT, 0.8.0 on Jazzy) adds IK, RRT and TOPP-RA [3] | A library: no planner of its own; RoboPlan is experimental before 1.0 ([page](../software/pinocchio.md)) | Your own Python or C++ planner or controller without MoveIt |

## Pairings that work

Planner, IK solver and timing, inside MoveIt unless noted:

- **OMPL RRTConnect + KDL + TOTG:** the Jazzy default. TOTG runs as a response adapter in the
  OMPL, CHOMP and STOMP pipelines and needs an acceleration limit for every joint [1].
- **OMPL to a pre-pose, then Pilz `LIN` in and out:** two requests or one MoveIt Task Constructor
  task ([manip-moveit2](../../skills/manip-moveit2/references/planners.md)). Pilz times its own
  motion; its pipeline has no TOTG adapter [1].
- **OMPL + TRAC-IK + TOTG** when KDL fails near joint limits. Set `solve_type`: Jazzy's generated
  default is `Distance`, which spends the whole timeout on every call, though the plugin README
  says `Speed` [4].
- **Add Ruckig after TOTG** (`AddRuckigTrajectorySmoothing`) for jerk limits [2]. Set `max_jerk`
  per joint; otherwise it falls back to 5 rad/s, 10 rad/s² and 1000 rad/s³ [1].
- **OMPL then STOMP in one pipeline:** `planning_plugins: [ompl_interface/OMPLPlanner,
  stomp_moveit/StompPlanner]`. The pipeline runs plugins in order and hands each the last path;
  STOMP uses it as its seed [1]. No MoveIt 2 tutorial shows this (the adapter tutorial is
  MoveIt 1), and CHOMP in 2.12.4 does not read the handed path, so `fillTrajectory` finds none
  [1][2]. Read from the code, not run: test it in simulation.
- **cuRobo IK + cuRobo planner,** its timed output sent to a `joint_trajectory_controller`
  ([cuRobo](../software/curobo.md)).
- **Drake GCS, then retiming** with Toppra for acceleration bounds, since GCS paths are not smooth
  where regions meet [11].
- **Avoid:** pick_ik for new work (PickNik deprecated it in September 2026 and offers only basic
  maintenance) [5]; Pilz `LIN` through clutter; CHOMP alone among many obstacles [2].

## When the answer changes

- **Lyrical and Rolling:** MoveIt 2.15, with Pilz `POLYLINE`, and OMPL 2.0.2 with its newer
  planners [2][3]. Isaac ROS 5.0 (2026-09-18) moved cuMotion to Lyrical [7][8].
- **Humble:** MoveIt 2.5.10, no STOMP or TRAC-IK binary, and the old `planning_plugin` and
  adapter keys [1][3].
- **cuMotion on Jazzy:** use the Isaac ROS 4.x branches. 4.0 to 4.3 wrapped cuRobo v0.7.7
  (`curobo_core`); 4.4 (2026-04-30) to 4.6 (2026-08-18) link NVIDIA's separate cuMotion library,
  which builds on algorithms first shown in cuRobo [6][7][9]. In every branch from 4.0 to 5.1
  the Apache-2.0 plugin depends on the NVIDIA-licensed `isaac_ros_cumotion` [6].
- **Obstacles that move during the motion:** MoveIt's hybrid planning pairs a global planner with
  a fast local one that adapts the motion as it runs [2]; `moveit_hybrid_planning` has a Jazzy
  binary [3]. Servo jogs and corrects small moves ([MoveIt 2](../software/moveit2.md)).
- **No ROS on the arm:** an SO-101 on LeRobot has no official ROS 2 driver
  ([SO-101](../robots/so-101.md)); plan in Python with RoboPlan or the toolbox, or learn the
  motion instead of planning it.
- **Mobile manipulators:** drive the base with [Nav2](../software/nav2.md) and plan the arm. MoveIt
  can plan base and arm together through a planar joint with `motion_model: diff_drive`, but its
  tutorial uses a Stretch-specific IK plugin and advises Nav2 for pure navigation [2].
- **Before hardware:** try each planner on mock hardware or a simulated arm
  ([choose a simulator](choose-a-simulator.md), [MuJoCo](../tools/mujoco.md)).

## Sources

1. [moveit2 tag 2.12.4: package.xml files, moveit_configs_utils default configs, Setup Assistant templates, planning pipeline, OMPL, Pilz, CHOMP, STOMP and Ruckig sources, MIGRATION.md, trajectory_cache README](https://github.com/moveit/moveit2/tree/2.12.4), accessed 2026-11-25
2. [moveit2_tutorials (main): Pilz, CHOMP, STOMP, parallel planning, time parameterization, hybrid planning and planning adapter pages](https://github.com/moveit/moveit2_tutorials), accessed 2026-11-25
3. [rosdistro distribution files: humble, jazzy, kilted, lyrical, rolling](https://github.com/ros/rosdistro), accessed 2026-11-25
4. [trac_ik jazzy branch and tag 2.0.2: README, plugin README, generated parameter file, CHANGELOG](https://github.com/traclabs/trac_ik/tree/jazzy), accessed 2026-11-25
5. [pick_ik repository (main): README deprecation notice, package.xml](https://github.com/PickNikRobotics/pick_ik), accessed 2026-11-25
6. [isaac_ros_cumotion release-4.0 to release-5.1 branches: LICENSE, package.xml files, CMakeLists.txt, MoveIt plugin and its config](https://github.com/NVIDIA-ISAAC-ROS/isaac_ros_cumotion), accessed 2026-11-25
7. [Isaac ROS release notes (4.0.0 to 5.1.0)](https://nvidia-isaac-ros.github.io/releases/index.html), accessed 2026-11-25
8. [Isaac ROS docs: Isaac ROS cuMotion (release 5.1)](https://nvidia-isaac-ros.github.io/repositories_and_packages/isaac_ros_cumotion/index.html), accessed 2026-11-25
9. [NVIDIA cuMotion library repository: README, LICENSE](https://github.com/nvidia-isaac/cumotion), accessed 2026-11-25
10. [cuRobo repository: README, LICENSE, tags, docs/reference/benchmarks.rst](https://github.com/NVlabs/curobo), accessed 2026-11-25
11. [Drake repository: LICENSE.TXT, planning/trajectory_optimization headers](https://github.com/RobotLocomotion/drake), accessed 2026-11-25

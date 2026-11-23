---
type: guide
name: Choose a Nav2 planner and controller
summary: Which Nav2 global planner (NavFn, Smac 2D, Smac Hybrid-A*, Smac State Lattice, Theta*) and controller (DWB, Regulated Pure Pursuit, MPPI, Graceful, with Rotation Shim as a wrapper) a ROS 2 robot should start with, decided by drive type, footprint shape, environment, speed and CPU; with pairings that work and when Nav2 is the wrong tool.
tags: [nav2, navigation, path-planning, path-following, planner, controller, smac, hybrid-a-star, state-lattice, theta-star, navfn, mppi, dwb, regulated-pure-pursuit, graceful, rotation-shim, footprint, ackermann, omnidirectional, ros2]
question: Which Nav2 global planner and controller should my robot start with?
options: [navfn, smac-2d, smac-hybrid, smac-lattice, theta-star, dwb, regulated-pure-pursuit, mppi, graceful, rotation-shim]
recommendation: "Smac 2D (or the shipped NavFn) with MPPI for a circular differential or omni base; Smac Hybrid-A* with MPPI or Regulated Pure Pursuit for a car-like or legged robot; Smac State Lattice with a footprint polygon for a non-circular base in tight spaces; Regulated Pure Pursuit when the CPU is small."
evidence: researched
last_verified: 2026-11-24
sources:
  - {url: "https://docs.nav2.org/jazzy/configuration_and_development/tuning_guide/", title: "Nav2 docs (Jazzy): Tuning Guide", accessed: 2026-11-24}
  - {url: "https://docs.nav2.org/jazzy/configuration_and_development/navigation_plugins/", title: "Nav2 docs (Jazzy): Navigation Plugins", accessed: 2026-11-24}
  - {url: "https://docs.nav2.org/jazzy/configuration_and_development/first_time_robot_setup_guide/navigation_plugins/setup_navigation_plugins/", title: "Nav2 docs (Jazzy): Setting Up Navigation Plugins", accessed: 2026-11-24}
  - {url: "https://github.com/ros-navigation/navigation2/tree/jazzy/nav2_smac_planner", title: "nav2_smac_planner, jazzy branch: README, source and sample lattice primitives", accessed: 2026-11-24}
  - {url: "https://github.com/ros-navigation/navigation2/tree/jazzy/nav2_mppi_controller", title: "nav2_mppi_controller, jazzy branch: README, package.xml, CMakeLists.txt and critics", accessed: 2026-11-24}
  - {url: "https://docs.nav2.org/jazzy/configuration_and_development/configuration_guide/controller_plugins/mppi_controller/configuring_mppic/", title: "Nav2 docs (Jazzy): Model Predictive Path Integral Controller", accessed: 2026-11-24}
  - {url: "https://github.com/ros-navigation/navigation2/tree/jazzy/nav2_regulated_pure_pursuit_controller", title: "nav2_regulated_pure_pursuit_controller, jazzy branch: README and parameter handler", accessed: 2026-11-24}
  - {url: "https://github.com/ros-navigation/navigation2/tree/jazzy/nav2_rotation_shim_controller", title: "nav2_rotation_shim_controller, jazzy branch: README and source", accessed: 2026-11-24}
  - {url: "https://github.com/ros-navigation/navigation2/tree/jazzy/nav2_graceful_controller", title: "nav2_graceful_controller, jazzy branch: README and source", accessed: 2026-11-24}
  - {url: "https://github.com/ros-navigation/navigation2/tree/jazzy", title: "navigation2 jazzy branch: nav2_bringup params, planner and controller servers, default BT XML, DWB, NavFn, Theta* and docking packages", accessed: 2026-11-24}
  - {url: "https://docs.nav2.org/lyrical/configuration_and_development/migration_guides/jazzy/Jazzy/", title: "Nav2 docs: Jazzy to Kilted migration guide", accessed: 2026-11-24}
  - {url: "https://docs.nav2.org/lyrical/configuration_and_development/migration_guides/kilted/Kilted/", title: "Nav2 docs: Kilted to Lyrical migration guide", accessed: 2026-11-24}
  - {url: "https://github.com/ros-navigation/navigation2", title: "navigation2 repository: kilted, lyrical and main branches; tags 1.3.14, 1.4.2 and 1.5.3", accessed: 2026-11-24}
  - {url: "https://github.com/ros/rosdistro", title: "rosdistro distribution files: humble, jazzy, kilted, lyrical", accessed: 2026-11-24}
---

# Choose a Nav2 planner and controller

Which global planner should draw your robot's path, and which controller should drive along it?
For builders of a [Nav2](../software/nav2.md) robot on ROS 2 Jazzy, with later distros noted.
Bring-up is in [nav-nav2](../../skills/nav-nav2/SKILL.md); tuning in
[nav-planning](../../skills/nav-planning/SKILL.md).

## Short answer

- **Circular differential drive** (most DIY bases, [TurtleBot3](../robots/turtlebot3.md)): Smac 2D,
  or keep the shipped NavFn, with MPPI and `motion_model: DiffDrive` [1][10]. On a small CPU, use
  RPP, which turns to the path heading by itself [7]; [linorobot2](../software/linorobot2.md)
  ships NavFn with RPP inside Rotation Shim.
- **Circular omni or mecanum:** Smac 2D, NavFn or Theta\* [1]; MPPI with `motion_model: Omni`, or
  DWB, whose trajectory generators cover omni bases [5][10]. RPP ignores sideways motion [7].
- **Non-circular base in narrow aisles:** Smac State Lattice with the diff or omni control set and a
  `footprint` polygon [1][4]; MPPI with `consider_footprint: true`, or DWB with its
  `ObstacleFootprint` critic [5][10].
- **Ackermann or car-like:** Smac Hybrid-A\* (`DUBIN`, or `REEDS_SHEPP` if it reverses) with
  `minimum_turning_radius` set to the vehicle's [4]; MPPI with `motion_model: Ackermann`, or RPP
  with `use_rotate_to_heading: false` [5][7]. DWB has no Ackermann trajectory generator, and
  Rotation Shim needs a base that turns on the spot [3][8][10].
- **Legged:** Smac Hybrid-A\*, the planner Nav2's tuning guide gives legged robots [1]; RPP, DWB and
  Graceful list legged support, and MPPI does in the tuning guide only [1][2].

## What decides it

- **Drive type.** NavFn, Smac 2D and Theta\* plan for a point that can turn in place, so they suit
  differential and omni bases, not cars [1][3]. Hybrid-A\* searches Dubins or Reeds-Shepp motions
  limited by a turning radius; State Lattice uses precomputed control sets for diff, omni,
  Ackermann or your own [4].
- **Shape.** Give a round robot `robot_radius` and any other the `footprint` polygon, which
  Hybrid-A\*, State Lattice and every controller can collision-check [1]. A radius on a non-circular
  robot is fine only if it is small for its space, the CPU is tiny, or a 2D planner is used anyway
  [1]. Hybrid-A\* and State Lattice need `inflation_radius` at least the footprint's circumscribed
  radius; otherwise Smac logs an error and planning slows sharply [4].
- **Environment.** In halls and aisles, raise the inflation radius and cost scale until a gentle
  cost gradient fills the space; all planners use it to keep to the middle [1]. NavFn draws broad
  curves, Theta\* straight lines at any angle, Smac 2D a cost-aware A\* path [1]. For long plans
  across large or outdoor maps, Smac 2D and Hybrid-A\* can downsample the costmap, and Hybrid-A\*
  and State Lattice can cache their obstacle heuristic on a static map [1][4]. Rough ground needs
  elevation data that Nav2's 2D costmaps do not hold; see [grid_map](../software/grid-map.md).
- **Speed.** Hybrid-A\* and State Lattice also suit fast robots that must not skid or tip [4]. MPPI
  predicts `time_steps × model_dt` seconds ahead; at top speed that distance must fit in half the
  local costmap, or the costmap caps your speed [5]. The Jazzy params (56 × 0.05 s at 0.5 m/s,
  1.4 m, in a 3 m costmap) just fit [10].
- **Compute.** MPPI runs on the CPU only; Nav2 measured it at 50+ Hz on a 4th-gen Intel i5 (its docs
  page says 100+ Hz) and suggests 1000 samples at 50 Hz or 2000 at 30 Hz [5][6]. Footprint checks
  and `visualize` cost more; the Jazzy params ship `visualize: true` [5][10]. RPP's README reports
  well over 1 kHz on a modern Intel CPU [7]. Nav2 says the feasible planners run about as fast as
  the 2D ones [1].
- **Smoothing.** NavFn, Theta\* and Smac 2D paths are not kinematically feasible. Smac smooths its
  own output; the Simple Smoother is meant for 2D planners, the Constrained Smoother keeps a turning
  radius [2][4]. No default behaviour tree calls `SmoothPath`, so `smoother_server` does nothing
  until you add that node to your tree [10].

## Planners

| Option | Kinematics it suits | Footprint handling | Cost or compute | Jazzy default? | Best when |
|---|---|---|---|---|---|
| NavFn | Circular diff and omni; Nav2 also lists legged [1][2] | Circle, through the inflated costmap [3] | Wavefront search, Dijkstra or A\* (`use_astar`) [10] | Yes: Dijkstra in `nav2_params.yaml`, and the server's fallback [10] | A round indoor robot on the stock config |
| Smac 2D | Circular diff and omni [1] | Circle: cell cost against the inscribed cost [4] | Cost-aware 8-connected A\* with its own smoother; README says slightly slower than NavFn [4] | No | A round robot that needs cleaner paths than NavFn [4] |
| Smac Hybrid-A\* | Ackermann, car-like, legged; non-circular diff or omni needing feasible paths [1][4] | Full SE2 footprint [4] | Dubins or Reeds-Shepp search; `minimum_turning_radius` 0.4 m by default [4] | No | Cars, legged robots, fast robots |
| Smac State Lattice | Non-circular diff, omni, Ackermann, custom [1][4] | Full SE2 footprint [4] | Precomputed control sets, samples at 5 cm only; default set is Ackermann, 0.5 m radius; no downsampling [4] | No | Long or odd-shaped robots in tight spaces |
| Theta\* | Circular diff and omni [1][2] | Point on the inflated costmap [2] | A\* with line-of-sight shortcuts [10] | No | Open floors where straight lines at any angle suit |

## Controllers

| Option | Kinematics it suits | Footprint handling | Cost or compute | Jazzy default? | Best when |
|---|---|---|---|---|---|
| DWB | Diff, omni; legged in Nav2's list; no Ackermann generator [2][10] | `ObstacleFootprint` critic; `BaseObstacle` assumes a circle [10] | Samples velocities and scores them with critics; needs per-robot tuning [1] | The server's fallback when no plugin is set [10] | Omni bases; full control over each critic's weight |
| Regulated Pure Pursuit | Diff, Ackermann, legged; omni without sideways motion [2][7] | Projects the footprint ahead (`use_collision_detection`, on by default) [7] | Geometric; well over 1 kHz on a modern Intel CPU per its README [7] | No | Exact path following, small CPUs, feasible Smac paths [1][7] |
| MPPI | Diff, omni, Ackermann; legged in the tuning guide [1][5] | Point cost unless `consider_footprint: true`, which costs more CPU [5] | Sampling MPC on the CPU; 50+ Hz on a 4th-gen i5 per Nav2 [5] | Yes, in `nav2_params.yaml` [10] | People and moving obstacles, smooth motion, CPU to spare [1] |
| Graceful | Diff by design; Nav2 also lists omni and legged [2][9] | Checks the footprint along its local plan [9] | A feedback control law towards a moving target point [9] | No | Smooth arcs; the docking server uses the same law [10] |
| Rotation Shim | A wrapper; bases that rotate in place [8] | Checks the footprint over `simulate_ahead_time` [8] | A rotation command and its checks, then the primary controller's cost [8] | No | Turning in place before tracking a 2D planner's path [1][8] |

## Pairings that work

- **NavFn + MPPI:** the Jazzy default pair; start here on a round diff base, in simulation [10].
- **Smac 2D, NavFn or Theta\* + Rotation Shim around MPPI or DWB:** a clean rotation in place
  before tracking, so the primary controller can be tuned for tracking alone [1][8].
- **NavFn + Rotation Shim around RPP:** the linorobot2 setup for small boards. RPP's own
  `use_rotate_to_heading` (on by default) already rotates in place, so the shim is optional [7].
- **Smac Hybrid-A\* + RPP** for exact tracking, or **+ MPPI** (Ackermann model) to dodge obstacles
  [1]. With `REEDS_SHEPP`, set RPP's `allow_reversing: true` with `use_rotate_to_heading: false`,
  or MPPI's `enforce_path_inversion: true` to reverse at the planned cusps [5][7].
- **Smac State Lattice + MPPI** with `consider_footprint: true`, or **+ DWB** with
  `ObstacleFootprint`, for a long or rectangular robot [1][5][10].
- **Two of each:** both servers load several plugins, and the default tree's `PlannerSelector`
  and `ControllerSelector` switch between them by topic [3][10].
- **Avoid:** Rotation Shim on a car [8]; RPP on a 2D planner's path for a large or non-circular
  robot, where its README asks for a feasible planner [7]; a shim in front of Hybrid-A\* or State
  Lattice, whose paths already start at the robot's heading [1].

## When the answer changes

- **Jazzy to Kilted or Lyrical:** all ten plugins ship as binaries from Humble to Lyrical, and
  Rolling's `main` adds no planner or controller class [13][14]. Kilted rewrote MPPI on Eigen,
  which Nav2 says is faster and runs on ARM CPUs with little SIMD support; Jazzy's uses xtensor
  and xsimd [5][11]. Lyrical moves MPPI's motion model to a plugin entry, nests Rotation Shim's
  primary controller parameters under `primary_controller`, and moves RPP's `stateful` to the
  goal checker [12]. It also adds a Dynamic Window Pure Pursuit option to RPP (keep the velocity
  smoother's limits at or above RPP's) and omni analytic expansion to State Lattice [12].
- **Mecanum wheels:** MPPI's Omni Constraint and Mecanum critics are on the `jazzy` and `lyrical`
  branches but in no release yet (1.3.14, 1.4.2, 1.5.3); build from source to use them [5][13].
- **Third-party controllers:** Nav2 lists TEB (with Ackermann support, its own repo) and Vector
  Pursuit (high-speed tracking, binaries for Humble and Jazzy only) [2][14].
- **A car on roads:** Nav2 plans on costmaps; lanes, traffic and car sensors are
  [Autoware](../software/autoware.md)'s job.
- **A new algorithm:** prototype it in [PythonRobotics](../software/pythonrobotics.md) (hybrid A\*,
  pure pursuit and MPC samples), then write it as a Nav2 plugin with
  [nav-planning](../../skills/nav-planning/SKILL.md).
- **Mission logic, not motion:** recoveries and replanning live in the behaviour tree; see
  [BehaviorTree.CPP](../software/behaviortree-cpp.md).

## Sources

1. [Nav2 docs (Jazzy): Tuning Guide](https://docs.nav2.org/jazzy/configuration_and_development/tuning_guide/), accessed 2026-11-24
2. [Nav2 docs (Jazzy): Navigation Plugins](https://docs.nav2.org/jazzy/configuration_and_development/navigation_plugins/), accessed 2026-11-24
3. [Nav2 docs (Jazzy): Setting Up Navigation Plugins](https://docs.nav2.org/jazzy/configuration_and_development/first_time_robot_setup_guide/navigation_plugins/setup_navigation_plugins/), accessed 2026-11-24
4. [nav2_smac_planner, jazzy branch: README, source and sample lattice primitives](https://github.com/ros-navigation/navigation2/tree/jazzy/nav2_smac_planner), accessed 2026-11-24
5. [nav2_mppi_controller, jazzy branch: README, package.xml, CMakeLists.txt and critics](https://github.com/ros-navigation/navigation2/tree/jazzy/nav2_mppi_controller), accessed 2026-11-24
6. [Nav2 docs (Jazzy): Model Predictive Path Integral Controller](https://docs.nav2.org/jazzy/configuration_and_development/configuration_guide/controller_plugins/mppi_controller/configuring_mppic/), accessed 2026-11-24
7. [nav2_regulated_pure_pursuit_controller, jazzy branch: README and parameter handler](https://github.com/ros-navigation/navigation2/tree/jazzy/nav2_regulated_pure_pursuit_controller), accessed 2026-11-24
8. [nav2_rotation_shim_controller, jazzy branch: README and source](https://github.com/ros-navigation/navigation2/tree/jazzy/nav2_rotation_shim_controller), accessed 2026-11-24
9. [nav2_graceful_controller, jazzy branch: README and source](https://github.com/ros-navigation/navigation2/tree/jazzy/nav2_graceful_controller), accessed 2026-11-24
10. [navigation2 jazzy branch: nav2_bringup params, planner and controller servers, default BT XML, DWB, NavFn, Theta* and docking packages](https://github.com/ros-navigation/navigation2/tree/jazzy), accessed 2026-11-24
11. [Nav2 docs: Jazzy to Kilted migration guide](https://docs.nav2.org/lyrical/configuration_and_development/migration_guides/jazzy/Jazzy/), accessed 2026-11-24
12. [Nav2 docs: Kilted to Lyrical migration guide](https://docs.nav2.org/lyrical/configuration_and_development/migration_guides/kilted/Kilted/), accessed 2026-11-24
13. [navigation2 repository: kilted, lyrical and main branches; tags 1.3.14, 1.4.2 and 1.5.3](https://github.com/ros-navigation/navigation2), accessed 2026-11-24
14. [rosdistro distribution files: humble, jazzy, kilted, lyrical](https://github.com/ros/rosdistro), accessed 2026-11-24

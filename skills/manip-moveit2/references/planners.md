# Planning pipelines (Jazzy)

Part of [manip-moveit2](../SKILL.md). Checked against MoveIt 2.12.4 (`moveit_configs_utils/default_configs`,
`moveit_planners`, the planning adapters) and the moveit2_tutorials how-to guides for Pilz, STOMP, CHOMP and OMPL
constrained planning. Which planner family suits a task, beyond MoveIt, is in
[choose an arm motion planner](../../../wiki/guides/choose-an-arm-motion-planner.md).

## The four pipelines

All four ship in `ros-jazzy-moveit` (the `moveit_planners` metapackage), all BSD-3-Clause.

| Pipeline name | Plugin | Kind | Use it for | Watch out |
|---|---|---|---|---|
| `ompl` | `ompl_interface/OMPLPlanner` | Sampling (RRTConnect by default) | General collision-free moves; the default | Paths are random and wander; shortened, but not optimal unless an anytime planner runs the full time |
| `pilz_industrial_motion_planner` | `pilz_industrial_motion_planner/CommandPlanner` | Analytic: `PTP`, `LIN`, `CIRC` | Predictable joint moves, straight lines, arcs; approach and retreat | Does not avoid obstacles: a colliding result is rejected (`ValidateSolution`), not replanned |
| `stomp` | `stomp_moveit/StompPlanner` | Stochastic trajectory optimization | Smooth paths; refining another planner's path | Slower; tuned by `num_timesteps`, `num_iterations`, `num_rollouts` |
| `chomp` | `chomp_interface/CHOMPPlanner` | Gradient trajectory optimization | Smoothing near obstacles | Local minima among many obstacles; may cut through thin obstacles |

Pick per request: in RViz (MotionPlanning, Context tab); `setPlanningPipelineId("pilz_industrial_motion_planner")`
and `setPlannerId("LIN")` in `MoveGroupInterface`; `planning_pipeline` and `planner_id` in MoveItPy's
`plan_request_params`. `ros2 service call /query_planner_interface moveit_msgs/srv/QueryPlannerInterfaces {}`
lists what `move_group` actually loaded.

## Adapters (Jazzy format)

A pipeline runs request adapters, then the planner, then response adapters, in list order:

| Adapter | Does |
|---|---|
| `default_planning_request_adapters/ResolveConstraintFrames` | Resolves goal constraints given on subframes |
| `.../ValidateWorkspaceBounds` | Adds default workspace bounds if the request has none |
| `.../CheckStartStateBounds` | Fails with `START_STATE_INVALID` if a joint is outside its limits; `fix_start_state` only normalizes continuous joints |
| `.../CheckStartStateCollision` | Fails with `START_STATE_IN_COLLISION`; it no longer nudges the state free |
| `.../CheckForStackedConstraints` | Optional; warns about multiple constraints on one link |
| `default_planning_response_adapters/AddTimeOptimalParameterization` | TOTG timing from velocity and acceleration limits and the scaling factors |
| `.../AddRuckigTrajectorySmoothing` | Optional jerk-limited smoothing after TOTG |
| `.../ValidateSolution` | Re-checks the timed path for collisions and constraints |
| `.../DisplayMotionPath` | Publishes `display_planned_path` for RViz |

Humble's `planning_plugin: ...` string, the space-separated `request_adapters` and the
`default_planner_request_adapters/Fix...` names are not read by Jazzy.

**Time parameterization.** TOTG needs an acceleration limit for every joint ([config-package.md](config-package.md)).
Ruckig smoothing falls back to 5 rad/s, 10 rad/s² and 1000 rad/s³ when `joint_limits.yaml` has no value: set
`has_jerk_limits`/`max_jerk` for every joint before adding it on hardware.

## OMPL

- The default config for a group is `geometric::RRTConnect`. Named configs come from `planner_configs` (global,
  from `ompl_defaults.yaml`) and the group's own `planner_configs` list; ids are `RRTConnect`, `RRTstar`,
  `PRMstar`, ... An id the group does not list logs
  `Cannot find planning configuration for group 'arm' using planner '...'. Will use defaults instead.`
- RRTConnect stops at the first solution; asymptotically optimal planners (`RRTstar`, `PRMstar`) use the whole
  planning time, so give them a time budget and expect planning to take that long.
- `MoveGroupInterface` defaults: 5 s planning time, 1 attempt. Extra attempts run in parallel threads and, by
  default, their paths are hybridized into one shorter path; raise attempts before raising time.
- Group keys in `ompl_planning.yaml`: `longest_valid_segment_fraction` (collision-check resolution along each
  edge; lower it if thin obstacles are skipped), `projection_evaluator`, `enforce_joint_model_state_space`,
  `enforce_constrained_state_space`.
- Path constraints (keep a cup upright): with an IK solver, OMPL samples them through IK in a pose state space,
  where consecutive IK solutions can flip; `enforce_joint_model_state_space: true` forces slower rejection
  sampling in joint space instead. For exactly one position or one orientation constraint (a box, plane or
  line), `enforce_constrained_state_space: true` plus `projection_evaluator: joints(joint1,joint2)` selects OMPL's
  constrained state space. Clear path constraints after use.

## Pilz industrial motion planner

- `PTP`: joint-space trapezoid, all joints start and stop together. `LIN`: straight tool line. `CIRC`: arc
  defined by a `center` or `interim` point given in `path_constraints` (constraint name `center` or `interim`).
- Needs acceleration limits for every joint in `joint_limits.yaml` and, for LIN and CIRC, `cartesian_limits` in
  `pilz_cartesian_limits.yaml`. `max_velocity_scaling_factor` and `max_acceleration_scaling_factor` scale them.
  The pipeline has no TOTG adapter: Pilz times its own trajectories.
- **Sequences:** a `moveit_msgs/MotionSequenceRequest` chains commands with `blend_radius` (m) between them;
  blend spheres must not overlap and the last item's radius must be 0. Load the capabilities
  `pilz_industrial_motion_planner/MoveGroupSequenceAction` and `.../MoveGroupSequenceService` on `move_group`; they
  serve the `sequence_move_group` action and the `plan_sequence_path` service. If any item fails, nothing runs.
- `POLYLINE` (a path through many points) exists only from MoveIt 2.15 (Lyrical); it is not planned for Jazzy.

## STOMP

```yaml
# config/stomp_planning.yaml (copy the shipped default, then edit)
stomp_moveit:
  num_timesteps: 60            # shipped defaults; waypoints in the trajectory
  num_iterations: 40
  num_iterations_after_valid: 0
  num_rollouts: 30
  max_rollouts: 30
  exponentiated_cost_sensitivity: 0.8
  control_cost_weight: 0.1
  delta_t: 0.1
```

Not in Humble's MoveIt. Higher `exponentiated_cost_sensitivity` converges faster and less repeatably. Smooth, collision-free results with no gradient needed. Listed after
`ompl` in `planning_plugins`, it takes the OMPL path as its seed. Custom cost functions through MoveIt's plugin
API are not supported yet (the STOMP tutorial says this is being investigated).

## CHOMP

Starts from an interpolated path (`trajectory_initialization_method`: `quintic-spline` by default) and
pushes it out of collision while smoothing. In 2.12.4 CHOMP does not read a path handed on by an earlier planner,
so `fillTrajectory` in a chained `planning_plugins` list fails with "No input trajectory specified"; chain
STOMP instead. Keys sit
in `chomp_planning.yaml`. Defaults suit open space; with clutter tune `obstacle_cost_weight`,
`collision_clearance` and `ridge_factor`, or use OMPL and post-process. Like every optimizer it can trade a thin
obstacle for a shorter path: keep `ValidateSolution` in the response adapters.

## Planning several ways at once

MoveItPy (and `moveit_cpp`) can run several pipelines in parallel and keep the best result
(`MultiPipelinePlanRequestParameters`, see [moveit-py.md](moveit-py.md)). A common pairing: Pilz `LIN` for the last
centimetres of an approach, OMPL for the transfer move, both inside an MTC task ([task-constructor.md](task-constructor.md)).

## Alternatives outside MoveIt's pipelines

- [cuRobo](../../../wiki/software/curobo.md): GPU motion generation from NVIDIA. NVIDIA's **Isaac ROS cuMotion**
  is a separate MoveIt planner plugin (`isaac_ros_cumotion_moveit/CumotionPlanner`): releases 4.0 to 4.3 wrapped
  cuRobo, 4.4 to 4.6 (the Jazzy line) use NVIDIA's own cuMotion library, and 5.0 moved to Lyrical. It needs an
  NVIDIA GPU. The plugin's `package.xml` says Apache-2.0, but it depends on `isaac_ros_cumotion`, which is under
  the NVIDIA Isaac ROS Software License: read it before you ship.
- [Drake](../../../wiki/software/drake.md): optimization-based planning (trajectory optimization, graphs of convex
  sets) outside ROS; plan there and send the trajectory to the same `joint_trajectory_controller`.
- [OMPL](../../../wiki/software/ompl.md) directly, without MoveIt, for research on planners themselves.

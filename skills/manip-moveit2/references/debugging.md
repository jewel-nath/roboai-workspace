# Debugging planning and execution (Jazzy)

Part of [manip-moveit2](../SKILL.md). Messages, services and error codes checked against MoveIt 2.12.4 source and
`moveit_msgs` (`MoveItErrorCodes.msg`, `GetPositionIK.srv`, `GetStateValidity.srv`).

## Triage order

Work down this list; most failures are found in the first four steps.

1. **Is `move_group` up and does it see the robot?** It prints `You can start planning now!`. Then
   `ros2 topic echo --once /joint_states` must list every non-fixed joint, gripper and passive joints included,
   and `ros2 run tf2_ros tf2_echo base_link tool0` must return a transform.
2. **Read the error code** (table below). `MoveGroupInterface::plan()` returns it; RViz prints it in the
   MotionPlanning panel; the `move_group` log names the adapter or planner that failed.
3. **Check the start state:**
   `ros2 service call /check_state_validity moveit_msgs/srv/GetStateValidity "{group_name: arm, robot_state: {is_diff: true}}"`.
   `valid: false` lists the contacts: a link pair the self-collision matrix should have disabled, a scene object
   overlapping the robot, or an attached object without touch links.
4. **Check the goal:** solve it alone with `/compute_ik` ([ik-solvers.md](ik-solvers.md)). In RViz the goal
   state shows red links when in collision. Check the frame of a pose goal and the orientation convention of
   `tool0`.
5. **Check the planner:** `ros2 service call /query_planner_interface moveit_msgs/srv/QueryPlannerInterfaces {}`
   lists loaded pipelines and planner ids. Give hard problems more attempts and time.
6. **Check the timing step:** acceleration limits for every joint (TOTG), jerk limits if Ruckig smoothing runs.
7. **Check execution:** `ros2 control list_controllers` (all `active`), `ros2 action list` (one
   `follow_joint_trajectory` per arm controller), controller and joint names in `moveit_controllers.yaml`, the
   `trajectory_execution` tolerances, and the `joint_trajectory_controller` log.

More log detail: start `move_group` with `arguments=["--ros-args", "--log-level", "debug"]` in the launch file.

## MoveItErrorCodes

| val | Name | Usual cause | Fix |
|---|---|---|---|
| 1 | `SUCCESS` | — | — |
| -1 | `PLANNING_FAILED` | No path found in time: goal boxed in, narrow passage, over-tight constraints | More attempts/time; check the scene; relax tolerances; try another planner |
| -2 | `INVALID_MOTION_PLAN` | `ValidateSolution`: `Computed path is not valid. Invalid states at index locations: [...]` | Lower `longest_valid_segment_fraction`; with CHOMP/STOMP, retune or use OMPL |
| -4 | `CONTROL_FAILED` | The controller aborted: tolerance violated, hardware fault, no action server | Controller log; JTC `constraints`; controller state |
| -6 | `TIMED_OUT` | Execution took longer than expected x `allowed_execution_duration_scaling` + margin | Fix limits so the arm can follow; raise scaling only with a reason |
| -7 | `PREEMPTED` | Stopped by `stop()`, a new goal, or a cancel | — |
| -10 | `START_STATE_IN_COLLISION` | See step 3; Jazzy no longer nudges the start state free | Fix the ACM or scene; move the arm out by hand or with joint jog |
| -12 | `GOAL_IN_COLLISION` | Goal pose puts a link in a scene object or itself | Move the goal; check object sizes and padding |
| -15 | `INVALID_GROUP_NAME` | Group name not in the SRDF | Use the SRDF name (`arm`) |
| -21 | `FRAME_TRANSFORM_FAILURE` | Goal or object in a frame TF cannot transform | Publish the frame; use the planning frame |
| -26 | `START_STATE_INVALID` | `Joint '...' from the starting state is outside bounds` | Encoder offset or URDF limits; joint-jog back inside |
| -31 | `NO_IK_SOLUTION` | Pose unreachable, wrong orientation, short IK timeout, IK target link not the chain tip | Step 4; solver choice ([ik-solvers.md](ik-solvers.md)) |
| 99999 | `FAILURE` | Often time parameterization: `Response adapter '...' failed to generate a trajectory.` after `No acceleration limit was defined for joint ...` | Acceleration limits in `joint_limits.yaml` |

## Messages and what they mean

| Message | Meaning | Fix |
|---|---|---|
| `Didn't receive robot state (joint angles) with recent timestamp within 1.000000 seconds.` | No `/joint_states`, a joint missing from it, or clocks differ (sim time on one node only) | Broadcaster active; publish every joint; `use_sim_time` everywhere or nowhere |
| `Unable to identify any set of controllers that can actuate the specified joints` | No controller in `moveit_controllers.yaml` covers the trajectory's joints, or it is not active | Match names and joints; keep gripper joints out of the arm group |
| `Action client not connected to action server: arm_controller/follow_joint_trajectory` | Controller not spawned, inactive, or a different `action_ns`/namespace | `ros2 action list`; fix `action_ns` |
| `Invalid Trajectory: start point deviates from current robot state more than 0.01 at joint '...'` | The arm moved or sagged between planning and execution, or `/joint_states` lags | Plan from the current state just before executing; fix holding; raise `allowed_start_tolerance` slightly only if the drift is understood |
| `Controller is taking too long to execute trajectory` | Hardware slower than the limits MoveIt planned with | Lower `joint_limits.yaml` to what the arm achieves |
| `Velocity of last trajectory point of joint ... is not zero` (JTC) | A trajectory that does not end at rest | Use MoveIt-timed trajectories; `allow_nonzero_velocity_at_trajectory_end` only for streaming |
| `Cannot find planning configuration for group 'arm' using planner '...'. Will use defaults instead.` | Planner id not listed for the group | `ompl_planning.yaml` per-group `planner_configs` ([config-package.md](config-package.md)) |
| `No kinematics plugins defined. Fill and load kinematics.yaml!` | This node has no `robot_description_kinematics` parameters | Pass `moveit_config.robot_description_kinematics` to it |
| `Group 'arm' was not found.` | `MoveGroupInterface` got an SRDF without that group, or none | `move_group` publishes `/robot_description_semantic`; check the name |
| OMPL `Unable to sample any valid states for goal tree` | Every sampled goal state is invalid: IK fails or the goal is in collision | Steps 3-4 |
| `Found a contact between '...' and '...', which constitutes a collision.` | Verbose collision report naming the pair | ACM for robot-robot pairs; scene geometry for objects |

## RViz habits that find problems fast

- MotionPlanning display, Planning Request: drag the goal; red links mean collision at the goal.
- Scene Robot: "Show Robot Collision" to see the collision meshes MoveIt actually checks (often coarser or
  offset compared with the visual meshes).
- Trajectory slider: step through a plan to find where it scrapes an object.
- Add a "Motion Planning Tasks" display when debugging Task Constructor ([task-constructor.md](task-constructor.md)).

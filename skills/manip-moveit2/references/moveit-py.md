# MoveItPy (Jazzy)

Part of [manip-moveit2](../SKILL.md). Checked against the `moveit_py` bindings and `moveit_cpp` headers in MoveIt
2.12.4 and the motion-planning Python API tutorial source. The code below was written for this skill and not run.

MoveItPy wraps `moveit_cpp`: the Python process loads the robot model, the planning pipelines, its own planning
scene monitor and its own trajectory execution manager. It does **not** talk to `move_group`; you can run it
without one. `moveit_commander` (the ROS 1 Python API) has no ROS 2 port.

```bash
sudo apt install ros-jazzy-moveit-py
```

## The parameters it needs

The Setup Assistant does not write a `moveit_cpp.yaml`; add one to the config package:

```yaml
# my_robot_moveit_config/config/moveit_cpp.yaml
planning_scene_monitor_options:
  name: planning_scene_monitor
  robot_description: robot_description
  wait_for_initial_state_timeout: 10.0     # s; 0 (the default) does not wait for /joint_states
planning_pipelines:
  pipeline_names: [ompl, pilz_industrial_motion_planner]   # empty list = no planner at all
plan_request_params:                       # used by plan() without arguments
  planning_pipeline: ompl
  planner_id: RRTConnect
  planning_attempts: 1
  planning_time: 2.0
  max_velocity_scaling_factor: 0.2         # code default 1.0 = full joint limits
  max_acceleration_scaling_factor: 0.2
pilz_lin:                                  # a named parameter set, loaded with PlanRequestParameters
  plan_request_params:
    planning_pipeline: pilz_industrial_motion_planner
    planner_id: LIN
    planning_attempts: 1
    planning_time: 1.0
    max_velocity_scaling_factor: 0.1
    max_acceleration_scaling_factor: 0.1
```

Unlike `MoveGroupInterface`, MoveItPy does not start from `default_velocity_scaling_factor`: its
`plan_request_params` defaults are 1.0 for both scaling factors, 5 attempts and 1 s. Set them.

## Launch

```python
# my_robot_moveit_config/launch/moveit_py_demo.launch.py
from launch import LaunchDescription
from launch_ros.actions import Node
from moveit_configs_utils import MoveItConfigsBuilder


def generate_launch_description():
    moveit_config = (
        MoveItConfigsBuilder("my_robot", package_name="my_robot_moveit_config")
        .trajectory_execution(file_path="config/moveit_controllers.yaml")
        .planning_pipelines(pipelines=["ompl", "pilz_industrial_motion_planner"])
        .moveit_cpp(file_path="config/moveit_cpp.yaml")
        .to_moveit_configs()
    )
    return LaunchDescription([
        Node(
            package="my_robot_apps",
            executable="pick_demo.py",
            name="moveit_py",          # same name as MoveItPy(node_name=...) below
            parameters=[moveit_config.to_dict()],
            output="screen",
        ),
    ])
```

Start the robot side first (robot_state_publisher, controllers, RViz) with the bringup from [launch.md](launch.md);
`move_group` is optional. Install the script with `install(PROGRAMS scripts/pick_demo.py DESTINATION
lib/${PROJECT_NAME})` and make it executable. Outside launch, `MoveItPy(node_name=..., config_dict=moveit_config.to_dict())`
accepts the same dictionary.

## A script

```python
#!/usr/bin/env python3
"""Move to a named state, then to a pose, then straight down with Pilz LIN."""
import rclpy
from geometry_msgs.msg import Pose, PoseStamped
from moveit.planning import MoveItPy, PlanRequestParameters
from moveit_msgs.msg import CollisionObject
from rclpy.logging import get_logger
from shape_msgs.msg import SolidPrimitive


def plan_and_execute(robot, arm, logger, params=None):
    result = arm.plan(single_plan_parameters=params) if params else arm.plan()
    if not result:
        logger.error("Planning failed")
        return False
    status = robot.execute(result.trajectory, controllers=[])
    if not status:
        logger.error(f"Execution failed: {status.status}")
    return bool(status)


def add_table(robot):
    table = CollisionObject()
    table.header.frame_id = "base_link"
    table.id = "table"
    box = SolidPrimitive(type=SolidPrimitive.BOX, dimensions=[1.0, 1.2, 0.04])  # m, placeholder
    table.primitives.append(box)
    pose = Pose()
    pose.position.x, pose.position.z = 0.5, -0.021
    table.primitive_poses.append(pose)
    table.operation = CollisionObject.ADD
    with robot.get_planning_scene_monitor().read_write() as scene:
        scene.apply_collision_object(table)
        scene.current_state.update()


def main():
    rclpy.init()
    logger = get_logger("pick_demo")
    robot = MoveItPy(node_name="moveit_py")
    arm = robot.get_planning_component("arm")
    add_table(robot)

    arm.set_start_state_to_current_state()
    arm.set_goal_state(configuration_name="home")
    ok = plan_and_execute(robot, arm, logger)

    goal = PoseStamped()
    goal.header.frame_id = "base_link"
    goal.pose.position.x, goal.pose.position.z = 0.35, 0.25
    goal.pose.orientation.x, goal.pose.orientation.w = 1.0, 0.0
    if ok:
        arm.set_start_state_to_current_state()
        arm.set_goal_state(pose_stamped_msg=goal, pose_link="tool0")
        ok = plan_and_execute(robot, arm, logger)

    if ok:
        goal.pose.position.z -= 0.05
        arm.set_start_state_to_current_state()
        arm.set_goal_state(pose_stamped_msg=goal, pose_link="tool0")
        ok = plan_and_execute(robot, arm, logger, PlanRequestParameters(robot, "pilz_lin"))

    robot.shutdown()


if __name__ == "__main__":
    main()
```

## API notes (Jazzy)

| Need | Call |
|---|---|
| Goal from the SRDF, a `RobotState`, a pose, or constraints | `set_goal_state(configuration_name=...)`, `robot_state=...`, `pose_stamped_msg=..., pose_link=...`, `motion_plan_constraints=[...]` |
| Joint goal | `RobotState(robot.get_robot_model())`, set `joint_positions = {"joint1": ...}`, then `construct_joint_constraint(robot_state=..., joint_model_group=...)` from `moveit.core.kinematic_constraints` |
| Path constraints | `set_path_constraints(constraints)` |
| Several pipelines in parallel, shortest result kept | `MultiPipelinePlanRequestParameters(robot, ["ompl_rrtc", "pilz_lin"])` passed as `multi_plan_parameters=` (each name a parameter set like `pilz_lin`) |
| Scene read / write | `with robot.get_planning_scene_monitor().read_only() as scene:` / `read_write()`; `scene.is_state_colliding(...)` |
| Execute | `robot.execute(trajectory, controllers=[])`; returns an `ExecutionStatus` that is truthy on success |

- `controllers` is a required argument on Jazzy (`[]` lets MoveIt choose from `moveit_controllers.yaml`). The
  Humble binding was `execute(group_name, robot_trajectory, blocking=True)`.
- There is no `PlanningComponent.execute()` and no waypoint list in `set_goal_state`: plan each segment, or use
  Pilz sequences or Task Constructor for chained moves.
- **Scenes:** MoveItPy keeps its own planning scene. It applies diffs from `/planning_scene` and objects from
  `/collision_object`, and publishes its own updates on `/monitored_planning_scene`, the topic `move_group` also
  uses. If both run, add shared objects through those topics, or run only one of them.
- `MoveItPy` initializes rclcpp itself (separately from `rclpy`) and spins its C++ node in a background thread.
  Call `robot.shutdown()` at the end.

## Checks

- The node logs the pipelines from `pipeline_names` loading without errors.
- `plan()` with no arguments returns a trajectory whose duration matches the scaling you set (not full speed).
- The table appears in RViz (add a PlanningScene display on `/monitored_planning_scene`) and plans avoid it.

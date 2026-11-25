# MoveGroupInterface in C++ (Jazzy)

Part of [manip-moveit2](../SKILL.md). Checked against `move_group_interface.hpp` and `planning_scene_interface.hpp`
in MoveIt 2.12.4 and the "Your First C++ MoveIt Project" and "Planning Around Objects" tutorial sources. The code
below was written for this skill and not run.

`MoveGroupInterface` is a client of `move_group`: it sends goals to the `move_action` action and the
`compute_cartesian_path` service, and runs nothing heavy itself. Use it for scripted moves from C++; use MoveItPy
([moveit-py.md](moveit-py.md)) from Python and Task Constructor ([task-constructor.md](task-constructor.md)) for
multi-step tasks.

## Package

```xml
<!-- package.xml -->
<depend>rclcpp</depend>
<depend>moveit_ros_planning_interface</depend>
<depend>geometry_msgs</depend>
<depend>moveit_msgs</depend>
<depend>shape_msgs</depend>
```

```cmake
# CMakeLists.txt
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(moveit_ros_planning_interface REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(moveit_msgs REQUIRED)
find_package(shape_msgs REQUIRED)

add_executable(move_demo src/move_demo.cpp)
target_compile_features(move_demo PUBLIC cxx_std_17)
# Namespaced targets: work on Jazzy and are what MoveIt 2.15 (Lyrical) exports
target_link_libraries(move_demo
  rclcpp::rclcpp
  moveit_ros_planning_interface::moveit_move_group_interface
  moveit_ros_planning_interface::moveit_planning_scene_interface
  ${geometry_msgs_TARGETS} ${moveit_msgs_TARGETS} ${shape_msgs_TARGETS})
install(TARGETS move_demo DESTINATION lib/${PROJECT_NAME})
ament_package()
```

Headers end in `.hpp` on Jazzy; the old `.h` names still compile but print
`.h header is obsolete. Please use the .hpp header instead.`

## A node: named, pose and Cartesian moves around a table

```cpp
// my_robot_apps/src/move_demo.cpp
#include <memory>
#include <string>
#include <thread>
#include <vector>

#include <geometry_msgs/msg/pose_stamped.hpp>
#include <moveit/move_group_interface/move_group_interface.hpp>
#include <moveit/planning_scene_interface/planning_scene_interface.hpp>
#include <moveit_msgs/msg/collision_object.hpp>
#include <rclcpp/rclcpp.hpp>
#include <shape_msgs/msg/solid_primitive.hpp>

using moveit::planning_interface::MoveGroupInterface;

namespace
{
bool planAndExecute(MoveGroupInterface& group, const rclcpp::Logger& logger)
{
  MoveGroupInterface::Plan plan;
  const auto planned = group.plan(plan);
  if (!planned)
  {
    RCLCPP_ERROR(logger, "Planning failed, MoveItErrorCodes %d", planned.val);
    return false;
  }
  const auto executed = group.execute(plan);
  if (!executed)
  {
    RCLCPP_ERROR(logger, "Execution failed, MoveItErrorCodes %d", executed.val);
  }
  return static_cast<bool>(executed);
}

moveit_msgs::msg::CollisionObject makeTable(const std::string& frame)
{
  moveit_msgs::msg::CollisionObject table;
  table.header.frame_id = frame;
  table.id = "table";
  shape_msgs::msg::SolidPrimitive box;
  box.type = shape_msgs::msg::SolidPrimitive::BOX;
  box.dimensions = { 1.0, 1.2, 0.04 };  // m, placeholder: measure the real table
  geometry_msgs::msg::Pose pose;
  pose.position.x = 0.5;
  pose.position.z = -0.021;  // top surface just below base_link
  pose.orientation.w = 1.0;
  table.primitives.push_back(box);
  table.primitive_poses.push_back(pose);
  table.operation = moveit_msgs::msg::CollisionObject::ADD;
  return table;
}
}  // namespace

int main(int argc, char** argv)
{
  rclcpp::init(argc, argv);
  auto node = std::make_shared<rclcpp::Node>(
      "move_demo", rclcpp::NodeOptions().automatically_declare_parameters_from_overrides(true));
  const auto logger = node->get_logger();

  // The interface needs a spinning node for joint states and action results
  rclcpp::executors::SingleThreadedExecutor executor;
  executor.add_node(node);
  std::thread spinner([&executor] { executor.spin(); });

  MoveGroupInterface arm(node, "arm");
  arm.setEndEffectorLink("tool0");
  arm.setPlanningPipelineId("ompl");
  arm.setNumPlanningAttempts(4);
  arm.setMaxVelocityScalingFactor(0.2);
  arm.setMaxAccelerationScalingFactor(0.2);

  moveit::planning_interface::PlanningSceneInterface scene;
  scene.applyCollisionObject(makeTable(arm.getPlanningFrame()));

  arm.setNamedTarget("home");  // a group_state from the SRDF
  bool ok = planAndExecute(arm, logger);

  if (ok)
  {
    geometry_msgs::msg::PoseStamped target;
    target.header.frame_id = "base_link";
    target.pose.position.x = 0.35;
    target.pose.position.z = 0.25;
    target.pose.orientation.x = 1.0;  // 180 deg about x: tool z points down if z is the approach axis
    target.pose.orientation.w = 0.0;
    arm.setPoseTarget(target);
    ok = planAndExecute(arm, logger);
  }

  if (ok)
  {
    // Straight 5 cm descent; waypoints are in the planning frame
    std::vector<geometry_msgs::msg::Pose> waypoints{ arm.getCurrentPose().pose };
    waypoints.back().position.z -= 0.05;
    moveit_msgs::msg::RobotTrajectory trajectory;
    const double fraction = arm.computeCartesianPath(waypoints, 0.005, trajectory);
    ok = fraction > 0.999 && static_cast<bool>(arm.execute(trajectory));
    if (!ok)
    {
      RCLCPP_ERROR(logger, "Cartesian path: %.1f %% of the path found", fraction * 100.0);
    }
  }

  rclcpp::shutdown();
  spinner.join();
  return ok ? 0 : 1;
}
```

Run it after `move_group` is up. It needs no MoveIt parameters to plan and execute; pass the kinematics and joint
limits anyway so local IK calls and the default scaling work:

```python
Node(package="my_robot_apps", executable="move_demo", output="screen",
     parameters=[moveit_config.robot_description_kinematics, moveit_config.joint_limits])
```

## Other calls you will need

| Task | Call |
|---|---|
| Joint goal | `setJointValueTarget(std::vector<double>)` in the group's joint order (`getActiveJoints()`) |
| Start from a given state instead of the current one | `setStartState(robot_state)`; back with `setStartStateToCurrentState()` |
| Pilz straight line | `setPlanningPipelineId("pilz_industrial_motion_planner"); setPlannerId("LIN");` |
| Plan and execute in one call | `move()`; `asyncExecute(plan)` returns at once, `stop()` cancels |
| Tolerances | `setGoalPositionTolerance(m)`, `setGoalOrientationTolerance(rad)`, `setGoalJointTolerance(rad)` |
| Keep the tool level | `setPathConstraints(constraints)` with one `moveit_msgs::msg::OrientationConstraint` (`link_name`, `header.frame_id`, `orientation`, `absolute_x/y/z_axis_tolerance`, `weight` 1.0); raise planning time; `clearPathConstraints()` after |
| Remove objects | `scene.removeCollisionObjects({"table"})` |
| Attach a held part | add it as a collision object, then `arm.attachObject("part", "tool0", {"left_finger_link", "right_finger_link"})`; `detachObject("part")` after release |
| Read the state | `getCurrentJointValues()`, `getCurrentPose()`, `getCurrentState(wait_s)` |

- **Scaling:** without an explicit call the interface uses `robot_description_planning.default_velocity_scaling_factor`
  from its own parameters, else 0.1. Planning time defaults to 5 s, attempts to 1.
- **Frames:** `setPoseTarget` with a `PoseStamped` takes any TF frame; a bare `Pose` and Cartesian waypoints use
  the pose reference frame (`setPoseReferenceFrame`, default the planning frame). `getCurrentPose()` returns the
  pose in the robot model's root frame (`world` with a virtual joint, else `base_link`).
- **Cartesian paths:** the Jazzy signature has no `jump_threshold` (the old overload is deprecated). A fraction
  below 1.0 means IK failed or a collision was found part-way; try a smaller `eef_step`, check that waypoints are
  reachable with the current wrist configuration, or use Pilz `LIN`. The trajectory is already timed.
- **Touch links:** `attachObject` without touch links makes the part collide with the fingers holding it, and
  the next plan fails with a start-state collision.
- **Threading:** never call `plan()` or `execute()` from a callback of the same single-threaded executor that
  must deliver the result; use a separate thread, as above, or a `MultiThreadedExecutor`.

## Checks

- The node logs the planning frame and end-effector link you expect (`getPlanningFrame()`, `getEndEffectorLink()`).
- In RViz the table appears in the planning scene and the planned path avoids it.
- The Cartesian descent returns a fraction of 1.0 and the tool moves straight down by 5 cm (`tf2_echo base_link tool0`).

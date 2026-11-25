# Approach, grasp, lift and place

Part of [manip-grasping](../SKILL.md). One pick with `MoveGroupInterface`, the planning scene and
the gripper action, with a check after every stage. Checked against the Jazzy headers of MoveIt
2.12.4 (`move_group_interface.hpp`, `planning_scene_interface.hpp`) and control_msgs 5.11.0. MoveIt
setup (SRDF groups `arm` and `gripper`, `tcp` as end-effector link, controllers, planners) is in
[manip-moveit2](../../manip-moveit2/SKILL.md). Written for this skill, not compiled or run.

## The sequence

| Stage | Motion | Planning scene | Check before going on |
|---|---|---|---|
| Open | gripper to open | target in the world | `reached_goal`, position near open |
| Pre-grasp | planned, normal speed | target in the world | plan succeeded and executed |
| Approach | straight line along tcp z, slow | target **removed** | Cartesian fraction is the whole path |
| Close | gripper, force-limited | — | position between empty and open; stalled or effort |
| Attach | none | target **attached** to `tcp`, gripper links may touch it | — |
| Lift | straight up in `base_link`, slow | attached | finger position unchanged; wrench shows the weight |
| Transport, place | planned, then straight down | attached | same as lift |
| Release, retreat | open, straight back along tcp z | detached, back in the world | gripper open; object left behind |

Removing the target before the final approach lets the fingers enter its volume while the table
and everything else are still checked. MoveIt Task Constructor does the same with
`ModifyPlanningScene` stages (`allowCollisions`, `attachObject`) and plans pick and place as one
task; it is released for Jazzy as 0.1.8 (`ros-jazzy-moveit-task-constructor-core`, tutorial
"Pick and Place with MoveIt Task Constructor"). Its solution executes as a whole, so a grasp check
between close and lift needs two tasks. The old `moveit_msgs/Grasp` pick pipeline is deprecated in
favour of MTC.

## The node

```cpp
// my_robot_manipulation/src/pick.cpp: links moveit_ros_planning_interface, rclcpp_action,
// control_msgs, tf2_eigen (package layout in ros2-core)
#include <chrono>
#include <string>
#include <thread>

#include <control_msgs/action/parallel_gripper_command.hpp>
#include <geometry_msgs/msg/pose_stamped.hpp>
#include <moveit/move_group_interface/move_group_interface.hpp>
#include <moveit/planning_scene_interface/planning_scene_interface.hpp>
#include <rclcpp/rclcpp.hpp>
#include <rclcpp/wait_for_message.hpp>
#include <rclcpp_action/rclcpp_action.hpp>
#include <tf2_eigen/tf2_eigen.hpp>

using namespace std::chrono_literals;
using GripperCmd = control_msgs::action::ParallelGripperCommand;
using moveit::planning_interface::MoveGroupInterface;

struct Grip { bool done; double position; bool stalled; };

Grip move_gripper(const rclcpp_action::Client<GripperCmd>::SharedPtr& client,
                  const std::string& joint, double position, double effort)
{
  GripperCmd::Goal goal;
  goal.command.name = {joint};
  goal.command.position = {position};
  if (effort > 0.0) goal.command.effort = {effort};  // used only with max_effort_interface
  auto goal_future = client->async_send_goal(goal);
  if (goal_future.wait_for(5s) != std::future_status::ready || !goal_future.get()) return {false, 0.0, false};
  auto result_future = client->async_get_result(goal_future.get());
  if (result_future.wait_for(10s) != std::future_status::ready) return {false, 0.0, false};
  const auto wrapped = result_future.get();
  return {wrapped.code == rclcpp_action::ResultCode::SUCCEEDED, wrapped.result->state.position.at(0),
          wrapped.result->stalled};
}

bool straight_line(MoveGroupInterface& arm, const geometry_msgs::msg::Pose& target)
{
  moveit_msgs::msg::RobotTrajectory traj;
  const double fraction = arm.computeCartesianPath({target}, 0.005, traj);  // 5 mm steps
  return fraction >= 0.999 && static_cast<bool>(arm.execute(traj));
}

int main(int argc, char** argv)
{
  rclcpp::init(argc, argv);
  auto node = rclcpp::Node::make_shared("pick");
  // Gripper values are in the joint's units (m here); examples, set them from your gripper
  const auto joint = node->declare_parameter<std::string>("gripper_joint", "gripper_left_finger_joint");
  const double open = node->declare_parameter("open_position", 0.04);   // URDF upper limit
  const double closed = node->declare_parameter("close_position", 0.0);
  const double effort = node->declare_parameter("close_effort", 0.0);   // 0: hardware default
  const double tol = node->declare_parameter("position_tolerance", 0.005);
  const double empty_below = node->declare_parameter("empty_below", 0.002);  // closed on nothing
  const double approach = node->declare_parameter("approach_distance", 0.10);  // m
  const double lift = node->declare_parameter("lift_height", 0.10);            // m
  const double slip_tol = node->declare_parameter("slip_tolerance", 0.002);
  const auto object_id = node->declare_parameter<std::string>("object_id", "target");
  auto log = node->get_logger();

  // Grasp pose for tcp, in base_link, from the grasp node; read before the executor starts
  geometry_msgs::msg::PoseStamped grasp_msg;
  if (!rclcpp::wait_for_message(grasp_msg, node, "/grasp_pose", 30s) ||
      grasp_msg.header.frame_id != "base_link") {
    RCLCPP_ERROR(log, "no grasp pose in base_link");
    return 1;
  }
  rclcpp::executors::SingleThreadedExecutor exec;
  exec.add_node(node);
  std::thread spinner([&exec] { exec.spin(); });

  MoveGroupInterface arm(node, "arm");
  arm.setPoseReferenceFrame("base_link");
  arm.setEndEffectorLink("tcp");
  arm.setMaxVelocityScalingFactor(0.2);       // example; first runs slower
  arm.setMaxAccelerationScalingFactor(0.2);
  moveit::planning_interface::PlanningSceneInterface scene;
  auto gripper = rclcpp_action::create_client<GripperCmd>(node, "/gripper_controller/gripper_cmd");

  Eigen::Isometry3d grasp;
  tf2::fromMsg(grasp_msg.pose, grasp);
  const auto pre_pose = tf2::toMsg(grasp * Eigen::Translation3d(0, 0, -approach));
  const auto lift_pose = tf2::toMsg(Eigen::Translation3d(0, 0, lift) * grasp);

  auto objects = scene.getObjects({object_id});
  if (!objects.count(object_id) || !gripper->wait_for_action_server(5s)) {
    RCLCPP_ERROR(log, "target not in the planning scene or gripper action missing");
    rclcpp::shutdown(); spinner.join(); return 1;
  }
  const moveit_msgs::msg::CollisionObject target = objects.at(object_id);

  auto finish = [&](bool ok, const char* why) {
    if (!ok) RCLCPP_ERROR(log, "pick failed: %s", why);
    rclcpp::shutdown();
    spinner.join();
    return ok ? 0 : 1;
  };

  // 1. Open, 2. pre-grasp
  const Grip opened = move_gripper(gripper, joint, open, 0.0);
  if (!opened.done || opened.position < open - tol) return finish(false, "gripper did not open");
  arm.setPoseTarget(pre_pose);
  MoveGroupInterface::Plan plan;
  if (!arm.plan(plan) || !arm.execute(plan)) return finish(false, "no plan to pre-grasp");

  // 3. Approach slowly with the target out of the scene
  moveit_msgs::msg::CollisionObject remove;
  remove.id = object_id;
  remove.header.frame_id = target.header.frame_id;
  remove.operation = remove.REMOVE;
  scene.applyCollisionObject(remove);
  arm.setMaxVelocityScalingFactor(0.05);
  if (!straight_line(arm, grasp_msg.pose)) {
    scene.applyCollisionObject(target);
    return finish(false, "approach blocked");
  }

  // 4. Close and judge the grasp from the finger position
  const Grip closed_on = move_gripper(gripper, joint, closed, effort);
  const bool holding = closed_on.done && closed_on.position > empty_below &&
                       closed_on.position < open - tol;
  if (!holding) {
    move_gripper(gripper, joint, open, 0.0);
    straight_line(arm, pre_pose);
    scene.applyCollisionObject(target);
    return finish(false, "nothing between the fingers");
  }

  // 5. Attach: the gripper links may touch the object from now on
  moveit_msgs::msg::AttachedCollisionObject held;
  held.link_name = "tcp";
  held.object = target;
  held.object.operation = held.object.ADD;
  held.touch_links = arm.getRobotModel()->getJointModelGroup("gripper")
                         ->getLinkModelNamesWithCollisionGeometry();
  scene.applyAttachedCollisionObject(held);

  // 6. Lift slowly, then confirm the fingers did not close further (slip)
  if (!straight_line(arm, lift_pose)) return finish(false, "lift blocked");
  const double after = arm.getCurrentState(1.0)->getVariablePosition(joint);
  if (closed_on.position - after > slip_tol) return finish(false, "object slipping");
  arm.setMaxVelocityScalingFactor(0.2);
  RCLCPP_INFO(log, "holding %s at %.4f", object_id.c_str(), after);
  return finish(true, "");
}
```

## Placing

Mirror the pick: plan to a pose above the place pose with the object attached (collision checking
now includes the object), straight down slowly until the object is at the place height or the
wrench shows contact, open, then detach: `arm.detachObject(object_id)` keeps it as a world object
where it now is. Retreat straight back along tcp z before planning anywhere else, or the open
fingers sweep through the object.

## When a stage fails

- **No plan to pre-grasp:** try the next grasp candidate; do not raise planning time first.
- **Approach fraction below 1:** the straight line hits something or leaves the arm's reach; the
  grasp is unreachable in this orientation. Try its 180-degree twin.
- **Closed on nothing:** the object moved or the grasp pose is off. Check hand-eye calibration and
  the pose source before retrying the same grasp.
- **Slip during lift:** set the object down, open, raise the force limit (within the object's
  tolerance) or pick a grasp nearer the centre of mass; do not just squeeze harder in the air.

Sources: moveit2 `jazzy` (`move_group_interface.hpp`: `computeCartesianPath` without
`jump_threshold`, `attachObject`, `getCurrentState`; `planning_scene_interface.hpp`;
`move_group_interface.cpp`: Cartesian paths are time-parameterised with the scaling factors);
moveit2_tutorials `main` (MTC pick-and-place tutorial; `pick_place_tutorial.rst` deprecation note);
rosdistro `jazzy` (moveit_task_constructor 0.1.8).

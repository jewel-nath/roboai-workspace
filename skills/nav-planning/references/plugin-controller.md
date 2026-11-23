# Writing a controller plugin

Part of [nav-planning](../SKILL.md). Written against the Jazzy `nav2_core::Controller` header (Nav2
1.3.14); package layout, plugin XML, CMake and `package.xml` are shared with the planner in
[plugin-planner.md](plugin-planner.md). Not compiled for this skill.

## The Jazzy interface

| Method | Called | Do |
|---|---|---|
| `configure(parent, name, tf, costmap_ros)` | once | read parameters (prefixed by `name`), keep the TF buffer and costmap |
| `activate()`, `deactivate()`, `cleanup()` | lifecycle | create/destroy publishers |
| `setPlan(const nav_msgs::msg::Path &)` | each new global path | store it; the path is in the planner's frame (`map`) |
| `computeVelocityCommands(pose, velocity, goal_checker)` | every cycle at `controller_frequency` | return a `TwistStamped`; `pose` is the robot in the local costmap's global frame (`odom`), `velocity` is the thresholded odometry twist |
| `setSpeedLimit(speed_limit, percentage)` | speed filter or BT | scale the speed limit; `nav2_costmap_2d::NO_SPEED_LIMIT` (0.0) restores it |
| `cancel()`, `reset()` | optional | slow down on cancel; clear state |

In Jazzy the plugin itself must bring the plan and the robot into one frame and prune the passed part of
the path. Throw `nav2_core::ControllerTFError`, `InvalidPath`, `NoValidControl` (from
`controller_exceptions.hpp`) so the BT gets error codes 102, 103 and 106. The server checks the goal and
progress itself; the `goal_checker` pointer is there if the control law needs the tolerances.

## Header

```cpp
// include/my_robot_nav_plugins/carrot_controller.hpp
#pragma once

#include <memory>
#include <string>

#include "geometry_msgs/msg/pose_stamped.hpp"
#include "geometry_msgs/msg/twist.hpp"
#include "geometry_msgs/msg/twist_stamped.hpp"
#include "nav2_core/controller.hpp"
#include "nav2_costmap_2d/costmap_2d_ros.hpp"
#include "nav_msgs/msg/path.hpp"
#include "rclcpp/rclcpp.hpp"
#include "rclcpp_lifecycle/lifecycle_node.hpp"
#include "tf2_ros/buffer.hpp"

namespace my_robot_nav_plugins
{

class CarrotController : public nav2_core::Controller
{
public:
  void configure(
    const rclcpp_lifecycle::LifecycleNode::WeakPtr & parent, std::string name,
    std::shared_ptr<tf2_ros::Buffer> tf,
    std::shared_ptr<nav2_costmap_2d::Costmap2DROS> costmap_ros) override;
  void cleanup() override {}
  void activate() override {}
  void deactivate() override {}
  void setPlan(const nav_msgs::msg::Path & path) override {plan_ = path;}
  geometry_msgs::msg::TwistStamped computeVelocityCommands(
    const geometry_msgs::msg::PoseStamped & pose,
    const geometry_msgs::msg::Twist & velocity,
    nav2_core::GoalChecker * goal_checker) override;
  void setSpeedLimit(const double & speed_limit, const bool & percentage) override;

private:
  std::shared_ptr<tf2_ros::Buffer> tf_;
  nav_msgs::msg::Path plan_;
  double lookahead_{0.6};
  double base_linear_vel_{0.4};
  double linear_vel_{0.4};
  double max_angular_vel_{1.5};
  double transform_tolerance_{0.1};
  rclcpp::Logger logger_{rclcpp::get_logger("CarrotController")};
};

}  // namespace my_robot_nav_plugins
```

## Source

```cpp
// src/carrot_controller.cpp
#include "my_robot_nav_plugins/carrot_controller.hpp"

#include <algorithm>
#include <cmath>
#include <limits>

#include "nav2_core/controller_exceptions.hpp"
#include "nav2_costmap_2d/costmap_filters/filter_values.hpp"
#include "nav2_util/node_utils.hpp"
#include "nav2_util/robot_utils.hpp"
#include "pluginlib/class_list_macros.hpp"
#include "tf2/utils.hpp"

namespace my_robot_nav_plugins
{

void CarrotController::configure(
  const rclcpp_lifecycle::LifecycleNode::WeakPtr & parent, std::string name,
  std::shared_ptr<tf2_ros::Buffer> tf,
  std::shared_ptr<nav2_costmap_2d::Costmap2DROS> /*costmap_ros*/)
{
  auto node = parent.lock();
  if (!node) {
    throw std::runtime_error("CarrotController: controller server node is gone");
  }
  tf_ = tf;
  logger_ = node->get_logger();
  auto param = [&](const std::string & key, double value, double & out) {
      nav2_util::declare_parameter_if_not_declared(node, name + "." + key, rclcpp::ParameterValue(value));
      node->get_parameter(name + "." + key, out);
    };
  param("lookahead_dist", 0.6, lookahead_);
  param("desired_linear_vel", 0.4, base_linear_vel_);
  param("max_angular_vel", 1.5, max_angular_vel_);
  param("transform_tolerance", 0.1, transform_tolerance_);
  linear_vel_ = base_linear_vel_;
}

geometry_msgs::msg::TwistStamped CarrotController::computeVelocityCommands(
  const geometry_msgs::msg::PoseStamped & pose,
  const geometry_msgs::msg::Twist & /*velocity*/,
  nav2_core::GoalChecker * /*goal_checker*/)
{
  if (plan_.poses.empty()) {
    throw nav2_core::InvalidPath("CarrotController has no plan");
  }
  // Bring the robot pose (odom) into the plan frame (map)
  geometry_msgs::msg::PoseStamped robot;
  if (!nav2_util::transformPoseInTargetFrame(
      pose, robot, *tf_, plan_.header.frame_id, transform_tolerance_))
  {
    throw nav2_core::ControllerTFError("Cannot transform the robot pose into the plan frame");
  }
  auto dist = [&](const geometry_msgs::msg::PoseStamped & p) {
      return std::hypot(p.pose.position.x - robot.pose.position.x,
               p.pose.position.y - robot.pose.position.y);
    };
  // Closest pose, then the first pose at least lookahead_ ahead of it (bound this on long paths)
  size_t closest = 0;
  double best = std::numeric_limits<double>::max();
  for (size_t i = 0; i < plan_.poses.size(); ++i) {
    if (dist(plan_.poses[i]) < best) {best = dist(plan_.poses[i]); closest = i;}
  }
  size_t target = plan_.poses.size() - 1;
  for (size_t i = closest; i < plan_.poses.size(); ++i) {
    if (dist(plan_.poses[i]) >= lookahead_) {target = i; break;}
  }
  // Carrot in the robot frame
  const double yaw = tf2::getYaw(robot.pose.orientation);
  const double gx = plan_.poses[target].pose.position.x - robot.pose.position.x;
  const double gy = plan_.poses[target].pose.position.y - robot.pose.position.y;
  const double x = std::cos(yaw) * gx + std::sin(yaw) * gy;
  const double y = -std::sin(yaw) * gx + std::cos(yaw) * gy;

  geometry_msgs::msg::TwistStamped cmd;
  cmd.header = pose.header;
  if (x <= 0.0) {
    // Carrot behind: turn in place toward it (diff-drive only)
    cmd.twist.angular.z = std::copysign(max_angular_vel_, y);
    return cmd;
  }
  const double curvature = 2.0 * y / (x * x + y * y);  // pure pursuit
  cmd.twist.linear.x = linear_vel_;
  cmd.twist.angular.z = std::clamp(linear_vel_ * curvature, -max_angular_vel_, max_angular_vel_);
  return cmd;
}

void CarrotController::setSpeedLimit(const double & speed_limit, const bool & percentage)
{
  if (speed_limit == nav2_costmap_2d::NO_SPEED_LIMIT) {
    linear_vel_ = base_linear_vel_;
  } else {
    linear_vel_ = percentage ? base_linear_vel_ * speed_limit / 100.0 : speed_limit;
  }
}

}  // namespace my_robot_nav_plugins

PLUGINLIB_EXPORT_CLASS(my_robot_nav_plugins::CarrotController, nav2_core::Controller)
```

This shows the plumbing, not a production controller: it has no collision check, no acceleration limit
and no slow-down at the goal. For those, start from RPP's source or wrap RPP with the Rotation Shim.

## Use and check it

```yaml
controller_server:
  ros__parameters:
    controller_plugins: ["FollowPath"]
    FollowPath:
      plugin: "my_robot_nav_plugins::CarrotController"
      lookahead_dist: 0.6
      desired_linear_vel: 0.4
      max_angular_vel: 1.5
```

- The log says `Created controller : FollowPath of type my_robot_nav_plugins::CarrotController`.
- `ros2 topic echo /cmd_vel_nav` (the controller's output with the bringup launch files) stays inside
  the limits; no `Control loop missed its desired rate` warnings.
- In simulation the robot reaches a goal 5 m away around one corner; record the run as a bag.

## Distro differences

- **Lyrical** (Nav2 1.5): `configure` takes `nav2::LifecycleNode::WeakPtr` and
  `nav2::TransformBuffer::SharedPtr`; `setPlan` is replaced by `newPathReceived(const nav_msgs::msg::Path &
  raw_global_path)`, and `computeVelocityCommands` gains `const nav_msgs::msg::Path &
  transformed_global_plan` and `const geometry_msgs::msg::PoseStamped & global_goal`. The controller
  server's path handler (`nav2_controller::FeasiblePathHandler`) now transforms and prunes the plan, so
  drop that code from the plugin.
- **Humble** (Nav2 1.1): same three-argument `computeVelocityCommands` and `setPlan` as Jazzy.

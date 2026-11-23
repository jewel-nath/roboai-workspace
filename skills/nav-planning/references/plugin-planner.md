# Writing a planner plugin (and packaging any Nav2 plugin)

Part of [nav-planning](../SKILL.md). Written against the Jazzy `nav2_core` headers (Nav2 1.3.14); the
controller half is in [plugin-controller.md](plugin-controller.md). Not compiled for this skill: build it
and fix what the compiler says before relying on it.

A planner plugin derives from `nav2_core::GlobalPlanner`, is built into a shared library and registered
with pluginlib so `planner_server` loads it by its type string. One package, `my_robot_nav_plugins`,
holds both examples: `include/my_robot_nav_plugins/*.hpp`, `src/*.cpp`, one `nav2_plugins.xml`.

The server transforms start and goal into the global costmap frame before calling `createPlan`, and maps
the `nav2_core` exceptions in `planner_exceptions.hpp` to the action's error codes
(`StartOutsideMapBounds` 203, `GoalOccupied` 206, `PlannerTimedOut` 207, `NoValidPathCouldBeFound` 208,
...). An empty path also counts as failure.

## Header

```cpp
// include/my_robot_nav_plugins/straight_line_planner.hpp
#pragma once

#include <functional>
#include <memory>
#include <string>

#include "geometry_msgs/msg/pose_stamped.hpp"
#include "nav2_core/global_planner.hpp"
#include "nav2_costmap_2d/costmap_2d_ros.hpp"
#include "nav_msgs/msg/path.hpp"
#include "rclcpp/rclcpp.hpp"
#include "rclcpp_lifecycle/lifecycle_node.hpp"
#include "tf2_ros/buffer.hpp"

namespace my_robot_nav_plugins
{

class StraightLinePlanner : public nav2_core::GlobalPlanner
{
public:
  void configure(
    const rclcpp_lifecycle::LifecycleNode::WeakPtr & parent, std::string name,
    std::shared_ptr<tf2_ros::Buffer> tf,
    std::shared_ptr<nav2_costmap_2d::Costmap2DROS> costmap_ros) override;
  void cleanup() override {}
  void activate() override {}
  void deactivate() override {}
  nav_msgs::msg::Path createPlan(
    const geometry_msgs::msg::PoseStamped & start,
    const geometry_msgs::msg::PoseStamped & goal,
    std::function<bool()> cancel_checker) override;

private:
  nav2_costmap_2d::Costmap2D * costmap_{nullptr};
  std::string global_frame_;
  double resolution_{0.05};
  rclcpp::Clock::SharedPtr clock_;
  rclcpp::Logger logger_{rclcpp::get_logger("StraightLinePlanner")};
};

}  // namespace my_robot_nav_plugins
```

## Source

```cpp
// src/straight_line_planner.cpp
#include "my_robot_nav_plugins/straight_line_planner.hpp"

#include <algorithm>
#include <cmath>
#include <mutex>

#include "nav2_core/planner_exceptions.hpp"
#include "nav2_costmap_2d/cost_values.hpp"
#include "nav2_util/geometry_utils.hpp"
#include "nav2_util/node_utils.hpp"
#include "pluginlib/class_list_macros.hpp"

namespace my_robot_nav_plugins
{

void StraightLinePlanner::configure(
  const rclcpp_lifecycle::LifecycleNode::WeakPtr & parent, std::string name,
  std::shared_ptr<tf2_ros::Buffer> /*tf*/,
  std::shared_ptr<nav2_costmap_2d::Costmap2DROS> costmap_ros)
{
  auto node = parent.lock();
  if (!node) {
    throw std::runtime_error("StraightLinePlanner: planner server node is gone");
  }
  logger_ = node->get_logger();
  clock_ = node->get_clock();
  costmap_ = costmap_ros->getCostmap();
  global_frame_ = costmap_ros->getGlobalFrameID();

  // Parameters live under the plugin ID, e.g. GridBased.interpolation_resolution
  nav2_util::declare_parameter_if_not_declared(
    node, name + ".interpolation_resolution", rclcpp::ParameterValue(0.05));
  node->get_parameter(name + ".interpolation_resolution", resolution_);
}

nav_msgs::msg::Path StraightLinePlanner::createPlan(
  const geometry_msgs::msg::PoseStamped & start,
  const geometry_msgs::msg::PoseStamped & goal,
  std::function<bool()> cancel_checker)
{
  unsigned int mx, my;
  if (!costmap_->worldToMap(start.pose.position.x, start.pose.position.y, mx, my)) {
    throw nav2_core::StartOutsideMapBounds("Start is outside the costmap");
  }
  if (!costmap_->worldToMap(goal.pose.position.x, goal.pose.position.y, mx, my)) {
    throw nav2_core::GoalOutsideMapBounds("Goal is outside the costmap");
  }

  const double dx = goal.pose.position.x - start.pose.position.x;
  const double dy = goal.pose.position.y - start.pose.position.y;
  const int steps = std::max(1, static_cast<int>(std::ceil(std::hypot(dx, dy) / resolution_)));
  const auto heading = nav2_util::geometry_utils::orientationAroundZAxis(std::atan2(dy, dx));

  nav_msgs::msg::Path path;
  path.header.frame_id = global_frame_;
  path.header.stamp = clock_->now();

  // Hold the costmap lock while reading cells
  std::unique_lock<nav2_costmap_2d::Costmap2D::mutex_t> lock(*(costmap_->getMutex()));
  for (int i = 0; i <= steps; ++i) {
    if (cancel_checker()) {
      throw nav2_core::PlannerCancelled("Planning was cancelled");
    }
    geometry_msgs::msg::PoseStamped pose;
    pose.header = path.header;
    pose.pose.position.x = start.pose.position.x + dx * i / steps;
    pose.pose.position.y = start.pose.position.y + dy * i / steps;
    pose.pose.orientation = heading;
    costmap_->worldToMap(pose.pose.position.x, pose.pose.position.y, mx, my);
    // 253 inscribed, 254 lethal, 255 unknown: all treated as blocked here
    if (costmap_->getCost(mx, my) >= nav2_costmap_2d::INSCRIBED_INFLATED_OBSTACLE) {
      throw nav2_core::NoValidPathCouldBeFound("The straight line crosses an obstacle");
    }
    path.poses.push_back(pose);
  }
  path.poses.back().pose.orientation = goal.pose.orientation;
  return path;
}

}  // namespace my_robot_nav_plugins

PLUGINLIB_EXPORT_CLASS(my_robot_nav_plugins::StraightLinePlanner, nav2_core::GlobalPlanner)
```

## Register it

`nav2_plugins.xml` (the `library path` is the CMake target name):

```xml
<class_libraries>
  <library path="my_robot_nav_plugins">
    <class type="my_robot_nav_plugins::StraightLinePlanner" base_class_type="nav2_core::GlobalPlanner">
      <description>Straight line from start to goal; fails if it crosses an obstacle.</description>
    </class>
    <class type="my_robot_nav_plugins::CarrotController" base_class_type="nav2_core::Controller">
      <description>Minimal pure-pursuit path follower.</description>
    </class>
  </library>
</class_libraries>
```

`CMakeLists.txt` (Jazzy style; the Nav2 Jazzy packages export no CMake targets for `nav2_core`, so
`ament_target_dependencies` is the simple path):

```cmake
cmake_minimum_required(VERSION 3.8)
project(my_robot_nav_plugins)

set(dependencies geometry_msgs nav2_core nav2_costmap_2d nav2_util nav_msgs pluginlib
  rclcpp rclcpp_lifecycle tf2 tf2_ros)
find_package(ament_cmake REQUIRED)
foreach(dep ${dependencies})
  find_package(${dep} REQUIRED)
endforeach()

add_library(${PROJECT_NAME} SHARED src/straight_line_planner.cpp src/carrot_controller.cpp)
target_include_directories(${PROJECT_NAME} PUBLIC
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
  $<INSTALL_INTERFACE:include/${PROJECT_NAME}>)
ament_target_dependencies(${PROJECT_NAME} ${dependencies})

# Installs nav2_plugins.xml and adds it to the ament index under nav2_core
pluginlib_export_plugin_description_file(nav2_core nav2_plugins.xml)

install(TARGETS ${PROJECT_NAME} ARCHIVE DESTINATION lib LIBRARY DESTINATION lib RUNTIME DESTINATION bin)
install(DIRECTORY include/ DESTINATION include/${PROJECT_NAME})
ament_export_include_directories(include/${PROJECT_NAME})
ament_export_libraries(${PROJECT_NAME})
ament_export_dependencies(${dependencies})
ament_package()
```

`package.xml`: `<depend>` on each entry of `dependencies`, and in `<export>`:

```xml
    <build_type>ament_cmake</build_type>
    <nav2_core plugin="${prefix}/nav2_plugins.xml"/>
```

## Use and check it

```yaml
planner_server:
  ros__parameters:
    planner_plugins: ["GridBased"]
    GridBased:
      plugin: "my_robot_nav_plugins::StraightLinePlanner"
      interpolation_resolution: 0.05
```

```bash
colcon build --packages-select my_robot_nav_plugins && source install/setup.bash
sudo apt install ros-jazzy-ros2plugin                  # provides `ros2 plugin`
ros2 plugin list --package my_robot_nav_plugins        # both classes with base nav2_core::...
ros2 launch nav2_bringup tb3_loopback_simulation.launch.py params_file:=<your params file>
```

The planner server log must say `Created global planner plugin GridBased of type
my_robot_nav_plugins::StraightLinePlanner`; a goal behind a wall must end with error code 208.

## Rules for any planner plugin

- Return poses in the costmap's global frame, spaced about one cell apart, with orientations set.
- Check `cancel_checker()` inside long loops; respect a time budget parameter and throw
  `nav2_core::PlannerTimedOut` when it runs out.
- Lock the costmap mutex while reading it; never keep the lock between calls.
- Prefix every parameter with the plugin ID (`name`), so two instances can coexist.
- Throw the specific `nav2_core` exception: the BT uses the error code to choose a recovery.

## Distro differences

- **Lyrical** (Nav2 1.5): `configure` takes `const nav2::LifecycleNode::WeakPtr &` and
  `nav2::TransformBuffer::SharedPtr` (package `nav2_ros_common`); `createPlan` gains a
  `const std::vector<geometry_msgs::msg::PoseStamped> & viapoints` argument before `cancel_checker`;
  parameter helpers are `nav2::declare_parameter_if_not_declared` or `node->declare_or_get_parameter`;
  link the exported targets (`nav2_core::nav2_core`, `nav2_costmap_2d::nav2_costmap_2d_core`,
  `nav2_util::nav2_util_core`, `nav2_ros_common::nav2_ros_common`) with `target_link_libraries`.
- **Humble** (Nav2 1.1): `createPlan(start, goal)` has no `cancel_checker`; Humble's own planners register
  slash names such as `nav2_navfn_planner/NavfnPlanner`.

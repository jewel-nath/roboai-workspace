# The behavior layer: behavior trees or state machines (Jazzy)

Part of [arch-robot-architecture](../SKILL.md): which kind and library for mission logic, with one example of
each. BehaviorTree.CPP itself (ports, node types, v3 to v4, Groot2) is on its
[wiki page](../../../wiki/software/behaviortree-cpp.md); Nav2's trees are in [nav-nav2](../../nav-nav2/references/behavior-trees.md).

## Tree or state machine

| If the robot... | Lean to |
|---|---|
| must keep checking conditions while it acts (battery, a new goal) and drop the current step, or reuses steps (navigate, dock, pick) across missions edited as XML | behavior tree: `ReactiveSequence` and `ReactiveFallback` re-check on every tick |
| has a few explicit modes (manual, autonomous, docking, fault) whose transitions are reviewed and shown to an operator | state machine |
| needs an operator to approve or pick transitions while it runs | FlexBE |
| is written by a Python-only team | py_trees_ros or YASMIN |

A common shape: a mode state machine on top, a tree for the mission in the autonomous mode, Nav2's tree below.
A flat state machine holding every mode and task combination grows without end; split modes from tasks.

## Libraries on Jazzy

Versions are the Jazzy binaries on 2026-11-25 (`ros/rosdistro`); licences from each repository.

| Library | apt (`ros-jazzy-...`) | Licence | Language | Notes |
|---|---|---|---|---|
| BehaviorTree.CPP | `behaviortree-cpp` 4.11.1 | MIT | C++ | Nav2 uses it. Groot2, its editor, is closed-source; monitoring trees over 20 nodes needs the paid PRO tier. BehaviorTree.ROS2 wrappers (Apache-2.0) have no binary: build from source |
| py_trees_ros | `py-trees-ros` 2.6.0 | BSD | Python | `py_trees_ros_viewer` 0.3.0 for a live view |
| YASMIN | `yasmin` 6.1.4 | Apache-2.0 | Python, C++ | Ready states for ROS actions, services and topics; `yasmin_viewer` web view |
| SMACC2 | `smacc2` 3.1.0 | Apache-2.0 | C++ | Built on Boost.Statechart, transitions checked at compile time; no Lyrical release |
| FlexBE | `flexbe-behavior-engine` 3.0.7 | BSD-3-Clause | Python | Operator in the loop. Its editor, FlexBE WebUI (Apache-2.0), has no binary; its `jazzy` branch needs engine 4.x from source and PySide6 (LGPL-3.0) from pip in a venv |
| SMACH | `smach` 3.0.3 | BSD | Python | Small and old; fine for a short sequence |

## Rules for the layer

- Call actions and services below; never open a device or publish the base's velocity topic. One action goal
  per long step; halting the step cancels it.
- Read state (battery, mode, faults) from the node's own subscriptions; a stale value fails the condition.
- Never block a tick: `tickOnce()` from a timer. `tickWhileRunning()` in a callback stops the executor that
  delivers the feedback the tree waits for.
- Publish the mode (latched) and serve the mission as an action ([interfaces.md](interfaces.md)); the operator
  interface talks to this layer, not to Nav2. Safety never depends on it ([arch-safety](../../arch-safety/SKILL.md)).

## Example: a BehaviorTree.CPP mission node

A patrol that stops when the battery is low. `NavigateTo` sends one Nav2 goal and cancels it when halted.

```xml
<!-- my_robot_behavior/trees/patrol.xml -->
<root BTCPP_format="4" main_tree_to_execute="Patrol">
  <BehaviorTree ID="Patrol">
    <ReactiveSequence>
      <BatteryOk/>                         <!-- re-checked every tick; failing halts the patrol -->
      <Sequence>
        <NavigateTo x="2.0" y="0.0"/>
        <NavigateTo x="2.0" y="3.0"/>
        <NavigateTo x="0.0" y="0.0"/>
      </Sequence>
    </ReactiveSequence>
  </BehaviorTree>
</root>
```

```cpp
// my_robot_behavior/src/mission_node.cpp
#include <chrono>
#include <memory>
#include <string>

#include "ament_index_cpp/get_package_share_directory.hpp"
#include "behaviortree_cpp/bt_factory.h"
#include "nav2_msgs/action/navigate_to_pose.hpp"
#include "rclcpp/rclcpp.hpp"
#include "rclcpp_action/rclcpp_action.hpp"
#include "sensor_msgs/msg/battery_state.hpp"

using NavigateToPose = nav2_msgs::action::NavigateToPose;
using GoalHandle = rclcpp_action::ClientGoalHandle<NavigateToPose>;

class NavigateTo : public BT::StatefulActionNode
{
public:
  NavigateTo(const std::string & name, const BT::NodeConfig & config, rclcpp::Node::SharedPtr node)
  : BT::StatefulActionNode(name, config),
    client_(rclcpp_action::create_client<NavigateToPose>(node, "navigate_to_pose")) {}

  static BT::PortsList providedPorts() {return {BT::InputPort<double>("x"), BT::InputPort<double>("y")};}

  BT::NodeStatus onStart() override
  {
    auto x = getInput<double>("x");
    auto y = getInput<double>("y");
    if (!x || !y || !client_->action_server_is_ready()) {return BT::NodeStatus::FAILURE;}
    NavigateToPose::Goal goal;
    goal.pose.header.frame_id = "map";
    goal.pose.pose.position.x = x.value();
    goal.pose.pose.position.y = y.value();
    goal.pose.pose.orientation.w = 1.0;
    const unsigned attempt = ++attempt_;   // answers to an older goal are ignored
    status_ = BT::NodeStatus::RUNNING;
    rclcpp_action::Client<NavigateToPose>::SendGoalOptions options;
    options.goal_response_callback = [this, attempt](GoalHandle::SharedPtr handle) {
        if (attempt != attempt_) {   // halted before the server answered
          if (handle) {client_->async_cancel_goal(handle);}
          return;
        }
        goal_handle_ = handle;
        if (!handle) {status_ = BT::NodeStatus::FAILURE;}   // rejected
      };
    options.result_callback = [this, attempt](const GoalHandle::WrappedResult & result) {
        if (attempt != attempt_) {return;}
        status_ = result.code == rclcpp_action::ResultCode::SUCCEEDED ?
          BT::NodeStatus::SUCCESS : BT::NodeStatus::FAILURE;
      };
    client_->async_send_goal(goal, options);
    return BT::NodeStatus::RUNNING;
  }

  BT::NodeStatus onRunning() override {return status_;}
  void onHalted() override
  {
    if (goal_handle_ && status_ == BT::NodeStatus::RUNNING) {client_->async_cancel_goal(goal_handle_);}
    goal_handle_.reset();
    ++attempt_;
  }

private:
  rclcpp_action::Client<NavigateToPose>::SharedPtr client_;
  GoalHandle::SharedPtr goal_handle_;
  BT::NodeStatus status_{BT::NodeStatus::IDLE};
  unsigned attempt_{0};
};

class MissionNode : public rclcpp::Node
{
public:
  MissionNode() : Node("mission")
  {
    declare_parameter("tree_file",
      ament_index_cpp::get_package_share_directory("my_robot_behavior") + "/trees/patrol.xml");
    declare_parameter("min_battery", 0.25);   // fraction of full charge; an example to tune
    battery_sub_ = create_subscription<sensor_msgs::msg::BatteryState>(
      "battery_state", 10, [this](sensor_msgs::msg::BatteryState::ConstSharedPtr msg) {battery_ = msg;});
  }

  // Separate from the constructor: shared_from_this() is not available there.
  void start()
  {
    factory_.registerNodeType<NavigateTo>("NavigateTo", shared_from_this());
    factory_.registerSimpleCondition("BatteryOk", [this](BT::TreeNode &) {
        const bool ok = battery_ && battery_->percentage >= get_parameter("min_battery").as_double();
        return ok ? BT::NodeStatus::SUCCESS : BT::NodeStatus::FAILURE;
      });
    tree_ = factory_.createTreeFromFile(get_parameter("tree_file").as_string());
    timer_ = create_wall_timer(std::chrono::milliseconds(100), [this]() {   // 10 Hz, an example rate
          const auto status = tree_.tickOnce();
          if (status != BT::NodeStatus::RUNNING) {
            RCLCPP_INFO(get_logger(), "Mission ended: %s", BT::toStr(status).c_str());
            timer_->cancel();
          }
        });
  }

private:
  BT::BehaviorTreeFactory factory_;
  BT::Tree tree_;
  rclcpp::TimerBase::SharedPtr timer_;
  rclcpp::Subscription<sensor_msgs::msg::BatteryState>::SharedPtr battery_sub_;
  sensor_msgs::msg::BatteryState::ConstSharedPtr battery_;
};

int main(int argc, char ** argv)
{
  rclcpp::init(argc, argv);
  auto node = std::make_shared<MissionNode>();
  node->start();
  rclcpp::spin(node);
  rclcpp::shutdown();
}
```

```cmake
foreach(dep ament_index_cpp behaviortree_cpp nav2_msgs rclcpp rclcpp_action sensor_msgs)
  find_package(${dep} REQUIRED)
endforeach()
add_executable(mission_node src/mission_node.cpp)
target_link_libraries(mission_node PUBLIC ament_index_cpp::ament_index_cpp
  behaviortree_cpp::behaviortree_cpp rclcpp::rclcpp rclcpp_action::rclcpp_action
  ${nav2_msgs_TARGETS} ${sensor_msgs_TARGETS})
install(TARGETS mission_node DESTINATION lib/${PROJECT_NAME})
install(DIRECTORY trees launch DESTINATION share/${PROJECT_NAME})
```

A real tree adds a staleness test and a docking `Fallback`. One single-threaded executor runs it all, so the
timer and the action callbacks never overlap.

## Example: the same patrol as a YASMIN state machine (Python)

```python
# my_robot_behavior/my_robot_behavior/patrol_sm.py
import rclpy
import yasmin
from nav2_msgs.action import NavigateToPose
from yasmin import Blackboard, CbState, StateMachine
from yasmin_ros import ActionState, set_ros_loggers
from yasmin_ros.basic_outcomes import ABORT, CANCEL, SUCCEED
from yasmin_ros.yasmin_node import YasminNode
from yasmin_viewer import YasminViewerPub

NEXT, DONE = 'next', 'done'


def pick_next(blackboard: Blackboard) -> str:
    index = blackboard['index']
    if index >= len(blackboard['waypoints']):
        return DONE
    blackboard['goal'] = blackboard['waypoints'][index]
    blackboard['index'] = index + 1
    return NEXT


def main():
    rclpy.init()
    set_ros_loggers()
    sm = StateMachine(outcomes=[SUCCEED, ABORT, CANCEL], handle_sigint=True)
    sm.add_state('PICK', CbState([NEXT, DONE], pick_next),
                 transitions={NEXT: 'NAVIGATE', DONE: SUCCEED})
    # The goal handler builds the action goal from the blackboard (a PoseStamped in map)
    navigate = ActionState(NavigateToPose, 'navigate_to_pose',
                           lambda blackboard: NavigateToPose.Goal(pose=blackboard['goal']))
    sm.add_state('NAVIGATE', navigate, transitions={SUCCEED: 'PICK', ABORT: ABORT, CANCEL: CANCEL})
    viewer = YasminViewerPub(sm, 'PATROL')       # live view in yasmin_viewer
    blackboard = Blackboard()
    blackboard['waypoints'] = load_waypoints()   # your own loader: list of PoseStamped
    blackboard['index'] = 0
    try:
        yasmin.YASMIN_LOG_INFO(f'Patrol ended: {sm(blackboard)}')
    finally:
        viewer.shutdown()
        YasminNode.destroy_instance()
        if rclpy.ok():
            rclpy.shutdown()
```

## Checks

- Cancelling the mission leaves no Nav2 goal running; a low battery in simulation halts the step within one tick.
- `ros2 node info` on the behavior node shows action clients and subscriptions only: no velocity publisher.

Sources: BehaviorTree.CPP 4.11.1 headers and CMake export; `rclcpp_action` `jazzy`; YASMIN 6.1.4 tag
(`action_state.py`, `action_client_demo.py`); SMACC2 `jazzy` README and `package.xml`; FlexBE engine and WebUI
`jazzy` branches; `ros/rosdistro` `jazzy/distribution.yaml`.

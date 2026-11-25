# MoveIt Task Constructor (Jazzy)

Part of [manip-moveit2](../SKILL.md). Checked against `moveit_task_constructor` tag `ros2-0.1.8` (the Jazzy binary
release; headers, `task.cpp`, the demo package) and the MTC pick-and-place tutorial in moveit2_tutorials `main`.
The code below was written for this skill and not run. Where grasps come from, gripper behaviour and the checks
between stages are in [manip-grasping](../../manip-grasping/references/pick-place.md).

MTC plans a whole multi-step task (open, approach, grasp, lift, carry, place, retreat) as one search: stages
pass planning scenes to each other, generator stages offer several candidates (grasp poses, IK solutions), and
connecting stages plan between them. The best complete solution is executed as a whole by `move_group`.

## Install (Jazzy has binaries)

```bash
sudo apt install ros-jazzy-moveit-task-constructor-core ros-jazzy-moveit-task-constructor-capabilities \
  ros-jazzy-moveit-task-constructor-visualization ros-jazzy-moveit-task-constructor-demo
ros2 launch moveit_task_constructor_demo demo.launch.py                       # Panda, move_group, RViz
ros2 launch moveit_task_constructor_demo run.launch.py exe:=pick_place_demo   # also: cartesian, modular
```

The tutorial builds MTC from source; on Jazzy that is unnecessary. If you must build it, use the tag `ros2-0.1.8`:
the `ros2` branch follows MoveIt `main` (2.15) and is released for Lyrical as 0.2.x.

## What has to be running

- `move_group` with `{"capabilities": "move_group/ExecuteTaskSolutionCapability"}` in its parameters
  ([launch.md](launch.md)). Without it `task.execute()` logs
  `Failed to connect to the 'execute_task_solution' action server`.
- Your MTC node with `moveit_config.to_dict()` as parameters (it loads the robot model, kinematics and the
  planning pipelines itself).
- RViz with the "Motion Planning Tasks" display (from `moveit_task_constructor_visualization`) to browse every
  stage's solutions and failures. Keep the node alive after planning or the display empties.
- The object to pick, as a collision object in the planning scene before the task plans.

## Package

```cmake
find_package(rclcpp REQUIRED)
find_package(moveit_task_constructor_core REQUIRED)
add_executable(mtc_pick src/mtc_pick.cpp)
target_link_libraries(mtc_pick rclcpp::rclcpp ${moveit_task_constructor_core_TARGETS})
```

`package.xml`: `<depend>moveit_task_constructor_core</depend>`, plus `<exec_depend>` on
`moveit_task_constructor_capabilities` for the config package that starts `move_group`.

## A pick task

```cpp
// my_robot_apps/src/mtc_pick.cpp (pick half; the place half follows the same pattern, see below)
#include <cmath>
#include <memory>
#include <string>
#include <thread>

#include <geometry_msgs/msg/vector3_stamped.hpp>
#include <moveit/task_constructor/solvers.h>
#include <moveit/task_constructor/stages.h>
#include <moveit/task_constructor/task.h>
#include <rclcpp/rclcpp.hpp>

namespace mtc = moveit::task_constructor;

namespace
{
const std::string kArm = "arm";
const std::string kGripper = "gripper";
const std::string kTool = "tool0";

// A straight move of min_m..max_m metres along +z of `frame`
std::unique_ptr<mtc::stages::MoveRelative> straightMove(const std::string& name,
                                                       const mtc::solvers::PlannerInterfacePtr& planner,
                                                       const std::string& frame, double min_m, double max_m)
{
  auto stage = std::make_unique<mtc::stages::MoveRelative>(name, planner);
  stage->properties().configureInitFrom(mtc::Stage::PARENT, { "group" });
  stage->setIKFrame(kTool);
  stage->setMinMaxDistance(min_m, max_m);
  geometry_msgs::msg::Vector3Stamped direction;
  direction.header.frame_id = frame;
  direction.vector.z = 1.0;
  stage->setDirection(direction);
  return stage;
}

mtc::Task buildPickTask(const rclcpp::Node::SharedPtr& node)
{
  mtc::Task task;
  task.stages()->setName("pick");
  task.loadRobotModel(node);
  task.setProperty("group", kArm);
  task.setProperty("eef", kGripper);
  task.setProperty("ik_frame", kTool);

  auto sampling = std::make_shared<mtc::solvers::PipelinePlanner>(node);  // "ompl", default planner
  auto interpolation = std::make_shared<mtc::solvers::JointInterpolationPlanner>();
  auto cartesian = std::make_shared<mtc::solvers::CartesianPath>();
  cartesian->setMaxVelocityScalingFactor(0.1);
  cartesian->setMaxAccelerationScalingFactor(0.1);
  cartesian->setStepSize(0.005);

  auto current = std::make_unique<mtc::stages::CurrentState>("current");
  mtc::Stage* current_ptr = current.get();
  task.add(std::move(current));

  auto open = std::make_unique<mtc::stages::MoveTo>("open gripper", interpolation);
  open->setGroup(kGripper);
  open->setGoal("open");  // SRDF group_state
  task.add(std::move(open));

  auto connect = std::make_unique<mtc::stages::Connect>(
      "move to pre-grasp", mtc::stages::Connect::GroupPlannerVector{ { kArm, sampling } });
  connect->setTimeout(5.0);
  connect->properties().configureInitFrom(mtc::Stage::PARENT);
  task.add(std::move(connect));

  auto grasp = std::make_unique<mtc::SerialContainer>("grasp");
  task.properties().exposeTo(grasp->properties(), { "eef", "group", "ik_frame" });
  grasp->properties().configureInitFrom(mtc::Stage::PARENT, { "eef", "group", "ik_frame" });

  grasp->insert(straightMove("approach", cartesian, kTool, 0.05, 0.10));  // along the tool's z

  auto generator = std::make_unique<mtc::stages::GenerateGraspPose>("grasp candidates");
  generator->properties().configureInitFrom(mtc::Stage::PARENT);
  generator->setPreGraspPose("open");
  generator->setObject("object");
  generator->setAngleDelta(M_PI / 12);  // candidates every 15 deg about the object's z axis
  generator->setMonitoredStage(current_ptr);

  Eigen::Isometry3d grasp_frame = Eigen::Isometry3d::Identity();
  grasp_frame.translation().z() = 0.10;  // placeholder: point between the fingertips, in tool0
  auto ik = std::make_unique<mtc::stages::ComputeIK>("grasp IK", std::move(generator));
  ik->setMaxIKSolutions(8);
  ik->setMinSolutionDistance(1.0);
  ik->setIKFrame(grasp_frame, kTool);
  ik->properties().configureInitFrom(mtc::Stage::PARENT, { "eef", "group" });
  ik->properties().configureInitFrom(mtc::Stage::INTERFACE, { "target_pose" });
  grasp->insert(std::move(ik));

  auto allow = std::make_unique<mtc::stages::ModifyPlanningScene>("allow finger contact");
  allow->allowCollisions("object", *task.getRobotModel()->getJointModelGroup(kGripper), true);
  grasp->insert(std::move(allow));

  auto close = std::make_unique<mtc::stages::MoveTo>("close gripper", interpolation);
  close->setGroup(kGripper);
  close->setGoal("close");
  grasp->insert(std::move(close));

  auto attach = std::make_unique<mtc::stages::ModifyPlanningScene>("attach object");
  attach->attachObject("object", kTool);
  grasp->insert(std::move(attach));

  grasp->insert(straightMove("lift", cartesian, "base_link", 0.05, 0.10));
  task.add(std::move(grasp));
  return task;
}
}  // namespace

int main(int argc, char** argv)
{
  rclcpp::init(argc, argv);
  auto node = std::make_shared<rclcpp::Node>(
      "mtc_pick", rclcpp::NodeOptions().automatically_declare_parameters_from_overrides(true));
  rclcpp::executors::SingleThreadedExecutor executor;
  executor.add_node(node);
  std::thread spinner([&executor] { executor.spin(); });

  auto task = buildPickTask(node);
  try
  {
    task.init();
    if (task.plan(5))  // stop after 5 complete solutions
    {
      task.introspection().publishSolution(*task.solutions().front());
      const auto result = task.execute(*task.solutions().front());
      RCLCPP_INFO(node->get_logger(), "Execution result: %d", result.val);
    }
    else
    {
      RCLCPP_ERROR(node->get_logger(), "No solution; inspect the failing stage in RViz");
    }
  }
  catch (const mtc::InitStageException& e)
  {
    RCLCPP_ERROR_STREAM(node->get_logger(), "Task init failed: " << e);
  }
  spinner.join();  // keep the node up for RViz; stop with Ctrl-C
  return 0;
}
```

`GenerateGraspPose` only spins candidate grasps about one axis of the object: enough for an upright box or
cylinder in a demo. Real grasp poses (from a detector, FoundationPose or Contact-GraspNet) come from
[manip-grasping](../../manip-grasping/references/grasp-poses.md) and enter MTC through a `GeneratePose`-style
generator or `FixedCartesianPoses` stage feeding `ComputeIK`.

## The place half

| Stage | Type | Settings |
|---|---|---|
| move to place | `Connect` | `GroupPlannerVector{{kArm, sampling}, {kGripper, interpolation}}` |
| lower | `MoveRelative` | down 5-10 cm in `base_link` (direction z = -1) |
| place candidates | `GeneratePlacePose` in `ComputeIK` | `setObject("object")`, `setPose(target PoseStamped)`, monitored stage = the attach stage; IK frame `"object"` |
| open gripper | `MoveTo` | `"open"` |
| forbid finger contact | `ModifyPlanningScene` | `allowCollisions("object", gripper group, false)` |
| detach | `ModifyPlanningScene` | `detachObject("object", kTool)` |
| retreat | `MoveRelative` | back along the tool's -z |
| return home | `MoveTo` | group `arm`, goal `"home"`, sampling planner |

## Using other planners in stages

- Pilz for straight moves: `std::make_shared<mtc::solvers::PipelinePlanner>(node, "pilz_industrial_motion_planner", "LIN")`.
- `CartesianPath` interpolates with IK and stops at a collision; `setMinFraction` decides how much of a
  straight move must succeed (`MoveRelative`'s min distance plays the same role).
- `Alternatives` and `Fallbacks` containers try several planners for one move; see the demo's
  `fallbacks_move_to` and `alternative_path_costs`.

## When it fails

- `InitStageException`: a stage misses a property (`group`, `eef`, `ik_frame`) or a monitored stage; the
  message names the stage.
- `task.plan()` returns no solution: open the Motion Planning Tasks display; each stage lists its failures with
  a comment (IK failed, collision, path fraction). Usual causes: the object is not in the scene, `grasp_frame`
  is wrong so every IK target is out of reach, the approach distance collides with the table, or `"open"` /
  `"close"` / `"home"` are missing from the SRDF.
- The solution executes in one go: a grasp check between "close" and "lift" needs two tasks
  ([manip-grasping](../../manip-grasping/references/pick-place.md)).

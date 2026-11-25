# Gripper control

Part of [manip-grasping](../SKILL.md). Checked against ros2_controllers 4.43.1 (`jazzy` branch:
`parallel_gripper_controller` and `gripper_controllers` sources and parameter files), control_msgs
5.11.0 and MoveIt 2.12.4 (`moveit_simple_controller_manager`). Not run.

## Description: one driven joint, the other finger mimics it

```xml
<!-- my_robot_description/urdf/gripper.xacro; gripper_base_link and the finger links
     (fixed to tool0, with meshes and inertials) are not shown -->
<link name="tcp"/>  <!-- point between the fingertips; plan grasps for this link -->
<joint name="tcp_joint" type="fixed">
  <parent link="tool0"/>
  <child link="tcp"/>
  <origin xyz="0 0 0.12" rpy="0 0 0"/>  <!-- example: measure flange to fingertip centre -->
</joint>
<joint name="gripper_left_finger_joint" type="prismatic">
  <parent link="gripper_base_link"/>
  <child link="gripper_left_finger"/>
  <axis xyz="1 0 0"/>
  <limit lower="0.0" upper="0.04" effort="20" velocity="0.05"/>  <!-- example: from the datasheet -->
</joint>
<joint name="gripper_right_finger_joint" type="prismatic">
  <parent link="gripper_base_link"/>
  <child link="gripper_right_finger"/>
  <axis xyz="-1 0 0"/>
  <limit lower="0.0" upper="0.04" effort="20" velocity="0.05"/>
  <mimic joint="gripper_left_finger_joint" multiplier="1" offset="0"/>
</joint>
```

The `<ros2_control>` tag lists the driven joint with a command interface and the mimic joint with
state interfaces only. Mimic joints come from the URDF `<mimic>` element; `mock_components` and
`gz_ros2_control` copy the driven joint's state to them.

```xml
<ros2_control name="my_gripper" type="system">
  <hardware>
    <plugin>mock_components/GenericSystem</plugin>   <!-- real: your gripper's plugin -->
  </hardware>
  <joint name="gripper_left_finger_joint">
    <command_interface name="position"/>
    <state_interface name="position"><param name="initial_value">0.04</param></state_interface>
    <state_interface name="velocity"/>   <!-- required by the parallel gripper controller -->
  </joint>
  <joint name="gripper_right_finger_joint">
    <state_interface name="position"/>
    <state_interface name="velocity"/>
  </joint>
</ros2_control>
```

A real plugin can also export `effort` as a state interface (motor current or force, so grasp
checks can read it from `/joint_states`) and a `max_effort` command interface if the hardware takes
a force limit per move. Hobby servos often report only position: compute velocity in the plugin
from the position difference over the period, because the controller refuses to activate without
it.

## Controller: `parallel_gripper_action_controller`

```yaml
# my_robot_bringup/config/controllers.yaml (beside the arm controller)
gripper_controller:
  ros__parameters:
    type: parallel_gripper_action_controller/GripperActionController
    joint: gripper_left_finger_joint     # the driven joint, never the mimic
    state_interfaces: [position, velocity]   # default; velocity must be there
    goal_tolerance: 0.002          # default 0.01, in the joint's units (m here): set it to a few % of travel
    allow_stalling: true           # default false: closing on an object then aborts the goal
    stall_velocity_threshold: 0.001  # default; below this the fingers count as stopped
    stall_timeout: 0.5             # default 1.0 s stopped before "stalled"
    max_effort: 10.0               # default 10.0; written only when max_effort_interface is set
    # max_effort_interface: gripper_left_finger_joint/max_effort   # only if the plugin exports it
    max_velocity: 0.1              # default 0.1; written only when max_velocity_interface is set
    # max_velocity_interface: gripper_left_finger_joint/max_velocity
```

- Action server: `/gripper_controller/gripper_cmd`, type `control_msgs/action/ParallelGripperCommand`.
  The goal is a `sensor_msgs/JointState` with exactly one `position` (any other count is rejected);
  `velocity[0]` and `effort[0]` are used only when the matching `*_interface` parameter is set.
- Result: `state` (position, and in `effort[0]` the commanded value, not a measurement), `stalled`,
  `reached_goal`. It succeeds when the position error is under `goal_tolerance`, or when the fingers
  have been still for `stall_timeout` and `allow_stalling` is true; otherwise a stall aborts.
- After a goal ends the controller keeps commanding the last position, so a closed gripper keeps
  squeezing at whatever force the hardware applies for that position error.

The older `position_controllers/GripperActionController` (action `control_msgs/action/GripperCommand`,
goal `{position, max_effort}`, same action name) still loads on Jazzy but logs a deprecation warning
and is not released for Lyrical. The position variant writes only the position; `max_effort` in its
goal is not sent to the hardware, and the `effort` in its result is that goal value echoed back.

## MoveIt: the gripper as a controller

MoveIt sends the last point of the gripper trajectory as one action goal. In the MoveIt config
(`config/moveit_controllers.yaml`; the rest of the file is [manip-moveit2](../../manip-moveit2/SKILL.md)):

```yaml
moveit_controller_manager: moveit_simple_controller_manager/MoveItSimpleControllerManager
moveit_simple_controller_manager:
  controller_names: [arm_controller, gripper_controller]
  gripper_controller:
    type: ParallelGripperCommand     # MoveIt 2.12.2+; GripperCommand for the deprecated controller
    action_ns: gripper_cmd
    default: true
    joints: [gripper_left_finger_joint]   # one joint; extra names are ignored with a warning
    max_effort: 10.0                 # > 0 adds effort[0] to every goal
    max_velocity: 0.05               # > 0 adds velocity[0]
```

For `type: GripperCommand`: `max_effort`, `allow_failure: true` (treat an aborted close as
success), and `parallel: true` with exactly two joints for two independently modelled fingers.
MoveIt does not see `stalled`; with `ParallelGripperCommand` an aborted goal is a failed execution,
which is why `allow_stalling: true` belongs on the controller.

## Test from the command line

```bash
sudo apt install ros-jazzy-ros2-controllers   # includes parallel_gripper_controller
ros2 control list_controllers                 # gripper_controller ... active
ros2 action list -t | grep gripper_cmd
# open (upper limit of the example joint)
ros2 action send_goal /gripper_controller/gripper_cmd control_msgs/action/ParallelGripperCommand \
  "{command: {name: [gripper_left_finger_joint], position: [0.04]}}" --feedback
# close on an object, with an effort limit if the hardware takes one
ros2 action send_goal /gripper_controller/gripper_cmd control_msgs/action/ParallelGripperCommand \
  "{command: {name: [gripper_left_finger_joint], position: [0.0], effort: [5.0]}}"
ros2 topic echo --once /joint_states   # gripper position, velocity, effort if exported
```

On mock hardware the close always reaches the goal (`reached_goal: true`), because nothing blocks
the fingers. A stall only shows on real hardware or in a simulator with contact.

## From Python

```python
# my_robot_manipulation/my_robot_manipulation/gripper_client.py
import time

from rclpy.action import ActionClient
from rclpy.node import Node
from control_msgs.action import ParallelGripperCommand


class GripperClient:
    """Blocking helper: call from a thread other than the one spinning the node."""

    def __init__(self, node: Node, joint: str,
                 action: str = '/gripper_controller/gripper_cmd'):
        self._node = node
        self._joint = joint
        self._client = ActionClient(node, ParallelGripperCommand, action)

    def move(self, position: float, effort: float | None = None, timeout: float = 10.0):
        if not self._client.wait_for_server(timeout_sec=2.0):
            raise RuntimeError('gripper action server not available')
        goal = ParallelGripperCommand.Goal()
        goal.command.name = [self._joint]
        goal.command.position = [position]
        if effort is not None:
            goal.command.effort = [effort]   # used only if max_effort_interface is set
        handle = self._client.send_goal_async(goal)
        # The node is spun elsewhere (MultiThreadedExecutor), so these waits return
        if not handle_wait(handle, timeout) or not handle.result().accepted:
            raise RuntimeError('gripper goal rejected or timed out')
        result_future = handle.result().get_result_async()
        if not handle_wait(result_future, timeout):
            raise RuntimeError('gripper did not finish in time')
        res = result_future.result().result
        return res.state.position[0], res.stalled, res.reached_goal


def handle_wait(future, timeout: float) -> bool:
    end = time.monotonic() + timeout
    while not future.done() and time.monotonic() < end:
        time.sleep(0.01)
    return future.done()
```

Read the returned position as the finger opening at the end of the close; the grasp checks in
[grasp-checks.md](grasp-checks.md) start from it.

## Choosing the close target and force

- **With a force limit (effort interface or the gripper's own force setting):** command fully
  closed and let the limit set the squeeze. Two friction contacts each carry at most `mu * F`
  along the surface, so a vertical hold needs `F >= k * m * (g + a) / (2 * mu)`: `m` object mass,
  `a` the lift acceleration, `mu` the finger-object friction coefficient (measure it, or use the
  gripper maker's figure), `k` a safety factor you choose. A form-fit grasp (fingers under or around
  the object) needs much less.
- **Position only (hobby servos):** command a target a little smaller than the object's width
  instead of fully closed. The servo pushes in proportion to the remaining error, and a servo held
  in stall for long heats up. If the servo has a torque-limit register, set it in the hardware
  plugin.
- The action's `effort` is documented as newtons, but the hardware plugin decides what the number
  means (amps, percent, a 0 to 255 byte). Write the mapping in the plugin's parameters.

Sources: ros2_controllers `jazzy` (parallel_gripper_controller userdoc, parameter YAML and
`parallel_gripper_action_controller_impl.hpp`; gripper_controllers userdoc, `hardware_interface_adapter.hpp`),
control_msgs `jazzy` (`GripperCommand.action`, `ParallelGripperCommand.action`), ros2_control
`jazzy` (`joints_userdoc.rst`, mimic joints), moveit2 `jazzy` (`moveit_simple_controller_manager.cpp`,
`parallel_gripper_command_controller_handle.hpp`, CHANGELOG 2.12.2), rosdistro `lyrical`.

# Grasp checks and a force guard

Part of [manip-grasping](../SKILL.md). How to tell that the gripper holds the object, keeps
holding it, and stops pushing when it hits something. Signals come from the gripper controller
([gripper.md](gripper.md)) and the F/T broadcaster ([force-torque.md](force-torque.md)). Code
written for this skill, not run. Every threshold below is an example: measure your own signals
on a plot first and set limits from them.

## What to check and when

| When | Signal | Holding if | Fails when |
|---|---|---|---|
| After close | action result `state.position[0]` | between `empty_below` and open minus a tolerance | fingers met (nothing there) or never moved |
| After close | result `stalled` (with `allow_stalling: true`) | true: fingers stopped on something | false with `reached_goal` at the closed position |
| After close | `/joint_states` gripper `effort` (only if the plugin exports it) | above a minimum you measured on a real grasp | near zero: soft contact or no contact |
| After lift | F/T force in `base_link`, compared with just before lift | changed by about the object's weight | no change: object left on the table |
| During transport | finger position vs. right after close | unchanged within a tolerance | creeping closed: the object is sliding out or deforming |
| During transport | F/T force vs. after lift | unchanged | weight gone: dropped |
| Any motion near contact | F/T force vs. a tare taken before the move | change below your limit | above the limit: stop |

A gripper without an effort reading or an F/T sensor still has the first two rows, and a camera
check (object gone from where it was) after the lift.

## Check functions

```python
# my_robot_manipulation/my_robot_manipulation/grasp_checks.py
import math

G = 9.81


def closed_on_object(position, open_position, empty_below, tol):
    """Finger position after closing, in the joint's units."""
    return empty_below < position < open_position - tol


def slipped(position_after_close, position_now, slip_tolerance):
    """Fingers that keep closing mean the object is sliding or being crushed."""
    return position_after_close - position_now > slip_tolerance


def weight_seen(force_before_lift, force_after_lift, expected_mass=None,
                rel_tol=0.3, min_newton=1.0):
    """Forces as (x, y, z) in base_link, gravity-compensated for the tool itself."""
    delta = math.dist(force_before_lift, force_after_lift)
    if expected_mass is None:
        return delta > min_newton           # above the sensor's noise, measured at rest
    return abs(delta - expected_mass * G) < rel_tol * expected_mass * G
```

Take `force_before_lift` with the fingers closed and the object still resting on the table, the
arm still. Take `force_after_lift` after the lift has finished and settled: acceleration adds to
the reading while moving.

## Force guard node

Stops MoveIt's current execution when the wrench changes by more than a limit since the last
tare. MoveIt's trajectory execution manager stops on the string `stop` on
`/trajectory_execution_event` (relative to `move_group`, root namespace assumed); the arm
controller then holds position, or brakes with `constraints.decelerate_on_cancel: true` and
per-joint `max_deceleration_on_cancel` (joint_trajectory_controller 4.39.0 and later on Jazzy).

```python
#!/usr/bin/env python3
# my_robot_manipulation/my_robot_manipulation/force_guard.py
import math

import rclpy
from geometry_msgs.msg import WrenchStamped
from rclpy.node import Node
from std_msgs.msg import String
from std_srvs.srv import Trigger


class ForceGuard(Node):
    def __init__(self):
        super().__init__('force_guard')
        self.limit = self.declare_parameter('force_limit', 30.0).value   # N, example only
        self.timeout = self.declare_parameter('silence_timeout', 0.2).value  # s, example
        topic = self.declare_parameter(
            'wrench_topic', '/fts_wrench_transformer/base_link/wrench_filtered').value
        self.ref = None
        self.tripped = False
        self.last_msg = self.get_clock().now()
        self.stop_pub = self.create_publisher(String, '/trajectory_execution_event', 10)
        self.create_subscription(WrenchStamped, topic, self.on_wrench, 10)
        self.create_service(Trigger, '~/tare', self.on_tare)
        self.create_timer(0.05, self.watch_silence)

    def on_tare(self, _request, response):
        self.ref = None          # next message becomes the reference
        self.tripped = False
        response.success = True
        return response

    def on_wrench(self, msg):
        self.last_msg = self.get_clock().now()
        f = msg.wrench.force
        now = (f.x, f.y, f.z)
        if self.ref is None:
            self.ref = now
            return
        change = math.dist(now, self.ref)
        if change > self.limit:
            self.trip(f'force changed by {change:.1f} N since tare')

    def watch_silence(self):
        silent = (self.get_clock().now() - self.last_msg).nanoseconds * 1e-9
        if silent > self.timeout:
            self.trip(f'no wrench for {silent:.2f} s')   # blind guard: stop rather than continue

    def trip(self, why):
        if not self.tripped:
            self.tripped = True
            self.stop_pub.publish(String(data='stop'))
            self.get_logger().error(f'STOP sent: {why}; call ~/tare to re-arm')


def main():
    rclpy.init()
    rclpy.spin(ForceGuard())


if __name__ == '__main__':
    main()
```

Use it like this: tare (`ros2 service call /force_guard/tare std_srvs/srv/Trigger`) with the arm
still before each move that may touch something (approach, place), and again after closing on an
object, so the held weight does not count. Test it before trusting it: execute a slow move and
press the tool by hand; execution must stop and MoveIt must report the trajectory as stopped.

**This is not a safety function.** The stop passes through DDS, `move_group`, an action cancel and
the controller, each with its own scheduling, so its delay has no bound. It protects the object
and the gripper during normal work. People and the robot are protected by the hardware layers
listed in the skill (emergency stop, the arm's own force and speed limits).

## Effort and current as a force proxy

Without an F/T sensor, motor current or the joint `effort` state rises on contact, but it also
carries friction, gravity and acceleration, and on many hobby servos it is coarse. Use it only for
a coarse "something is in the fingers" check after the fingers have stopped, with a threshold
measured on real grasps of light and heavy objects; not for stopping the arm on contact.

Sources: moveit2 `jazzy` (`trajectory_execution_manager.cpp`: `trajectory_execution_event`,
`stop`); ros2_controllers `jazzy` (`parallel_gripper_action_controller_impl.hpp`: `stalled`,
`reached_goal`; joint_trajectory_controller parameter YAML and CHANGELOG 4.39.0:
`decelerate_on_cancel`); control_msgs `jazzy` (`ParallelGripperCommand.action`).

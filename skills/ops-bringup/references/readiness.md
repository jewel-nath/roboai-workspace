# Start order and readiness checks

Part of [ops-bringup](../SKILL.md). Launch event handlers checked against launch 3.4 and
launch_ros 0.26 (`jazzy`); the script uses rclpy, tf2_ros and rosidl_runtime_py from Jazzy.

## Order by state, not by sleep

A `TimerAction(period=2.0)` only guesses how long a node needs; on a cold boot or a slow board
the guess is wrong. Most of the stack already waits for what it needs:

| Waits by itself | How |
|---|---|
| `spawner` | Retries the controller manager services forever by default; `--controller-manager-timeout 30` turns a dead manager into a visible failure |
| `ros2_control_node` | Waits for `/robot_description` (transient local) before loading hardware |
| Nav2 lifecycle managers | Configure and activate their nodes in order; the global costmap waits for `map` → `base_link` |
| TF users | `lookup_transform` with a timeout, or a `tf2_ros.MessageFilter` |
| Subscribers | Nothing to wait for: a late publisher connects when it appears |

Where order does matter inside one launch file, wait on an event:

```python
from launch.actions import RegisterEventHandler
from launch.event_handlers import OnProcessExit, OnProcessStart
from launch_ros.event_handlers import OnStateTransition

# Start B only after A has exited (a one-shot setup step such as a calibration loader)
RegisterEventHandler(OnProcessExit(target_action=setup_step, on_exit=[node_b]))

# Start B once A's process is running (it may not be ready yet)
RegisterEventHandler(OnProcessStart(target_action=node_a, on_start=[node_b]))

# Start B once lifecycle node A reaches active
RegisterEventHandler(OnStateTransition(
    target_lifecycle_node=driver, goal_state='active', entities=[node_b]))
```

Drivers that open hardware are best written as lifecycle nodes
([ros2-core](../../ros2-core/SKILL.md), workflow step 8): `on_configure` opens the device and fails
cleanly if it is missing, so the order is driven by real state.

Between systemd units, order with `After=` plus `Requires=` or `Wants=`. `After=` waits for the
other unit's `ExecStartPost` to finish, so a unit with the readiness check below is a real gate.

## The readiness check

`wait_ready.py` exits 0 once every listed topic has delivered a message and every listed transform
can be looked up, or 1 after the timeout with the list of what is missing. The unit runs it as
`ExecStartPost`; the first power-on check and an agent run it by hand.

```python
#!/usr/bin/env python3
"""Wait until topics publish and transforms exist; exit 1 on timeout."""
import argparse
import sys
import time

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile
from rclpy.time import Time
from rclpy.utilities import remove_ros_args
from rosidl_runtime_py.utilities import get_message
from tf2_ros import Buffer, TransformListener


class ReadinessCheck(Node):

    def __init__(self, topics):
        super().__init__('wait_ready')
        self.pending = set(topics)
        self.checks = {}
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)

    def try_subscribe(self):
        """Subscribe to each pending topic once a publisher tells us its type and QoS."""
        for topic in self.pending - self.checks.keys():
            publishers = self.get_publishers_info_by_topic(topic)
            if not publishers:
                continue
            # Copy the publisher's reliability and durability so latched topics also arrive
            pub_qos = publishers[0].qos_profile
            qos = QoSProfile(depth=1, reliability=pub_qos.reliability,
                             durability=pub_qos.durability)
            msg_type = get_message(publishers[0].topic_type)
            self.checks[topic] = self.create_subscription(
                msg_type, topic, lambda _msg, t=topic: self.pending.discard(t), qos)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--topics', nargs='*', default=['/joint_states', '/odom'])
    parser.add_argument('--transforms', nargs='*', default=['odom:base_link'],
                        help='parent:child pairs')
    parser.add_argument('--timeout', type=float, default=60.0, help='seconds')
    args = parser.parse_args(remove_ros_args(sys.argv)[1:])

    rclpy.init()
    node = ReadinessCheck(args.topics)
    transforms = {tuple(pair.split(':', 1)) for pair in args.transforms}
    deadline = time.monotonic() + args.timeout
    while rclpy.ok() and time.monotonic() < deadline:
        node.try_subscribe()
        transforms = {(parent, child) for parent, child in transforms
                      if not node.tf_buffer.can_transform(parent, child, Time())}
        if not node.pending and not transforms:
            break
        rclpy.spin_once(node, timeout_sec=0.2)

    missing = sorted(node.pending) + [f'{p} -> {c}' for p, c in sorted(transforms)]
    if missing:
        node.get_logger().error(f'Not ready after {args.timeout:.0f} s: {", ".join(missing)}')
    else:
        node.get_logger().info('Robot ready')
    node.destroy_node()
    rclpy.try_shutdown()
    return 1 if missing else 0


if __name__ == '__main__':
    sys.exit(main())
```

Install it with `install(PROGRAMS scripts/wait_ready.py DESTINATION lib/${PROJECT_NAME})`, keep the
file executable in git (`git update-index --chmod=+x`), and give it the robot's own list:

```bash
source /etc/my_robot/env.sh
ros2 run my_robot_bringup wait_ready.py --timeout 90 \
  --topics /joint_states /odom /scan /imu/data /diagnostics_agg \
  --transforms odom:base_link base_link:lidar_link base_link:imu_link
echo $?    # 0 ready, 1 not ready (the log names what is missing)
```

- The defaults (`/joint_states`, `/odom`, `odom` → `base_link`) suit a ros2_control mobile base;
  put the real list in the unit's `ExecStartPost` line.
- A topic whose publisher sends nothing until asked (a service-driven map, an event topic) does not
  belong in the list; check its node in `ros2 node list` instead.
- With navigation running, add `map:base_link`, or call the lifecycle managers:
  `ros2 service call /lifecycle_manager_navigation/is_active std_srvs/srv/Trigger` returns
  `success=True` once Nav2 is active.
- Strict or lenient: a failing `ExecStartPost` fails the start, stops the stack and lets `Restart=`
  try again. Prefix it with `-` (`ExecStartPost=-/bin/bash -c ...`) to log the result and keep the
  stack running, for robots where a missing optional sensor must not restart the base.
- The aggregated health from [diagnostics.md](diagnostics.md) is the runtime view; this script only
  answers "is it up yet".

## Traps

| Symptom | Cause | Fix |
|---|---|---|
| Works from a terminal, fails at boot | Fixed delays tuned on a warm system | Replace `TimerAction` with events, lifecycle states or the readiness check |
| `wait_ready.py` never sees a latched topic | Subscribed volatile to a transient local publisher that sent once | The script copies the publisher's durability; for your own tools do the same |
| Spawner hangs forever, nothing in the log | No controller manager (crashed, other namespace) and no timeout | `--controller-manager-timeout`; check `ros2 node list` |
| `ExecStartPost` times out and the unit restarts in a loop | Readiness list names a topic nobody publishes on this robot | Fix the list; run the script by hand with the same arguments |
| Unit stays `activating` until `TimeoutStartSec` | `Type=notify` and nothing sends `READY=1` | `Type=exec` plus the readiness check |

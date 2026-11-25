# Heartbeats, watchdogs and a stop gate

A software supervisor that stops passing motion commands when anything it depends on goes quiet, and
stays stopped until someone resets it. It is not a safety function: it runs on Linux, in Python, on an
unrated computer. It makes software faults end in a stop instead of a runaway, and it tells ROS that
the rated chain has tripped.

## Choose how to detect silence

| Method | Detects | Works on | Note |
|---|---|---|---|
| Timer that checks the age of the last message (the node below) | A publisher, its loop, or the link going quiet | Every RMW | Portable; ages use the receiver's monotonic clock, so clock skew does not matter |
| QoS deadline with an event callback | No message within the deadline | Fast DDS, Cyclone DDS; **not implemented in `rmw_zenoh_cpp`** | The publisher must offer a deadline at or below the one requested, or the pair is incompatible and nothing is delivered |
| QoS liveliness `AUTOMATIC` with a lease | The participant (process) is gone | DDS RMWs only: `rmw_zenoh_cpp` accepts `AUTOMATIC` but never fires the liveliness events | A live process with a stuck loop still counts as alive |
| `twist_mux` lock with a `timeout` | The lock publisher going quiet | Every RMW | Engages the lock; the mux then forwards nothing |
| systemd `WatchdogSec=` | A process that stops calling `sd_notify("WATCHDOG=1")` | Linux | Kills and restarts the service; it does not stop the motors |
| Linux hardware watchdog (`RuntimeWatchdogSec=`) | systemd itself hanging | Boards with a watchdog device | Reboots the computer; the motors keep their last command unless the drive or firmware times out |

QoS compatibility and events: the ROS 2 docs page "About Quality of Service settings". Zenoh's QoS
support: `rmw_zenoh` `docs/design.md`.

## Stop gate node (rclpy, Jazzy)

Sits between the command sources (or `twist_mux`) and the rest of the chain. It forwards
`TwistStamped` commands only while the rated chain reports OK, every required heartbeat is fresh and
the last command is fresh. Any failure latches it: it publishes zero commands, holds a `twist_mux` lock
and waits for `~/reset`. It also starts latched, so a freshly started robot needs a deliberate reset.

```python
"""Stop gate: forward motion commands only while the chain is OK and heartbeats are fresh."""
import time

import rclpy
from geometry_msgs.msg import TwistStamped
from rclpy.node import Node
from rclpy.qos import DurabilityPolicy, QoSProfile, ReliabilityPolicy
from std_msgs.msg import Bool, String
from std_srvs.srv import Trigger

LATCHED = QoSProfile(depth=1, reliability=ReliabilityPolicy.RELIABLE,
                     durability=DurabilityPolicy.TRANSIENT_LOCAL)


class StopGate(Node):

    def __init__(self):
        super().__init__('stop_gate')
        self.declare_parameter('heartbeats', ['/base_driver/heartbeat'])
        self.declare_parameter('heartbeat_timeout', 0.3)   # example: tune from the stopping budget
        self.declare_parameter('command_timeout', 0.3)
        self.declare_parameter('rate_hz', 20.0)
        self.hb_timeout = self.get_parameter('heartbeat_timeout').value
        self.cmd_timeout = self.get_parameter('command_timeout').value

        self.chain_ok = False          # unknown counts as tripped
        self.latched = True
        self.reason = 'startup: reset required'
        self.last_cmd_time = 0.0
        self.last_beat = {}
        for topic in self.get_parameter('heartbeats').value:
            self.last_beat[topic] = 0.0
            self.create_subscription(
                Bool, topic, lambda msg, t=topic: self.on_beat(t, msg), 1)

        self.create_subscription(Bool, '/safety/chain_ok', self.on_chain, LATCHED)
        self.create_subscription(TwistStamped, 'cmd_vel_in', self.on_cmd, 1)
        self.cmd_pub = self.create_publisher(TwistStamped, 'cmd_vel_out', 1)
        self.lock_pub = self.create_publisher(Bool, '~/lock', 1)
        self.state_pub = self.create_publisher(String, '~/state', LATCHED)
        self.create_service(Trigger, '~/reset', self.on_reset)
        self.create_timer(1.0 / self.get_parameter('rate_hz').value, self.check)
        self.publish_state()

    def on_beat(self, topic, msg):
        # A heartbeat carries data=True while its sender considers itself healthy.
        if msg.data:
            self.last_beat[topic] = time.monotonic()

    def on_chain(self, msg):
        self.chain_ok = msg.data

    def on_cmd(self, msg):
        self.last_cmd_time = time.monotonic()
        if not self.latched:
            out = TwistStamped()
            out.header.stamp = self.get_clock().now().to_msg()   # restamp with the robot's clock
            out.header.frame_id = msg.header.frame_id
            out.twist = msg.twist
            self.cmd_pub.publish(out)

    def fault(self):
        now = time.monotonic()
        if not self.chain_ok:
            return 'safety chain not OK'
        for topic, stamp in self.last_beat.items():
            if now - stamp > self.hb_timeout:
                return f'heartbeat stale: {topic}'
        return None

    def check(self):
        fault = self.fault()
        if fault and not self.latched:
            self.latched, self.reason = True, fault
            self.get_logger().error(f'stop gate latched: {fault}')
            self.publish_state()
        if not self.latched and time.monotonic() - self.last_cmd_time > self.cmd_timeout:
            self.send_zero()   # stale command: stop, but do not latch
        if self.latched:
            self.send_zero()
        self.lock_pub.publish(Bool(data=self.latched))

    def send_zero(self):
        zero = TwistStamped()
        zero.header.stamp = self.get_clock().now().to_msg()
        self.cmd_pub.publish(zero)

    def on_reset(self, request, response):
        fault = self.fault()
        if fault:
            response.success, response.message = False, f'cannot reset: {fault}'
            return response
        self.latched, self.reason = False, 'running'
        self.publish_state()
        response.success, response.message = True, 'reset; send a new command to move'
        return response

    def publish_state(self):
        self.state_pub.publish(String(data='LATCHED: ' + self.reason if self.latched else 'RUNNING'))


def main():
    rclpy.init()
    node = StopGate()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.try_shutdown()
```

Notes on the design:

- Commands are forwarded in the callback, so the gate adds no rate limit; the timer only enforces
  timeouts and keeps a latched robot commanded to zero. If the gate itself dies, the controller's own
  `cmd_vel_timeout` stops the base.
- Restamping with the robot's clock removes the clock-skew problem described in
  [software-layers.md](software-layers.md); staleness is judged here by receipt time instead.
- `/safety/chain_ok` comes from the node that reads the rated chain's status output
  ([stop-chain.md](stop-chain.md)); publish it latched. A missing publisher keeps the gate latched.
- Reset clears only the latch. The rated chain has its own manual reset, which comes first.
- With `twist_mux` in front, either remap its output into `cmd_vel_in`, or skip the forwarding and use
  only `~/lock` as a mux lock (block-style YAML in software-layers.md). The node publishes `~/lock`
  on every cycle, so a dead gate times the lock out.
- Watch more than topics where it matters: a node's `/diagnostics` level, the controller manager's
  latched `~/activity` topic, battery state. Add each as another fault condition.

Heartbeat in a monitored node, from its main loop (not from a separate timer, which keeps beating
while the loop is stuck):

```python
self.hb_pub = self.create_publisher(Bool, '~/heartbeat', 1)
# at the end of each successful control or driver cycle:
self.hb_pub.publish(Bool(data=self.healthy))
```

Launch (`my_robot_bringup/launch/safety.launch.py`). Nav2's controller output goes to the mux's
`nav_vel` input, and the velocity smoother's input is remapped to `cmd_vel_gated`:

```python
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(package='my_robot_safety', executable='stop_gate', name='stop_gate',
             parameters=[{'heartbeats': ['/base_driver/heartbeat', '/scan_monitor/heartbeat'],
                          'heartbeat_timeout': 0.3, 'command_timeout': 0.3}],
             remappings=[('cmd_vel_in', 'twist_mux/cmd_vel'), ('cmd_vel_out', 'cmd_vel_gated')],
             respawn=True, respawn_delay=1.0),
    ])
```

A respawned gate starts latched, so a crash and restart still needs a reset.

## QoS deadline variant (DDS RMWs only)

```python
from rclpy.duration import Duration
from rclpy.event_handler import SubscriptionEventCallbacks   # rclpy.qos_event is deprecated on Jazzy
from rclpy.qos import QoSProfile

qos = QoSProfile(depth=1, deadline=Duration(seconds=0.3))    # the publisher must offer <= 0.3 s
self.create_subscription(
    Bool, '/base_driver/heartbeat', self.on_heartbeat, qos,
    event_callbacks=SubscriptionEventCallbacks(deadline=self.on_deadline_missed))
```

The publisher has to use the same or a shorter deadline. With the default (no deadline) on the
publisher side, the subscription is incompatible and receives nothing: a silent failure unless the
timer check above also runs. Keep the timer check either way.

## systemd watchdog for a ROS process

Unit lines (the full unit and boot order are in [ops-bringup](../../ops-bringup/SKILL.md)):

```ini
[Service]
Type=exec                     # as in ops-bringup's unit
WatchdogSec=2                 # example
Restart=always                # on-failure misses a clean exit; see ops-bringup
NotifyAccess=all              # ros2 run and ros2 launch start the node as a child process
```

The ping proves only that the process calling `sd_notify` is alive. Under `ros2 launch`, one unit
covers many nodes; one per critical node is clearer.

From the node's main loop, without extra packages (the protocol is in the `sd_notify` man page):

```python
import os
import socket


def sd_notify(state: bytes = b'WATCHDOG=1') -> None:
    addr = os.environ.get('NOTIFY_SOCKET')
    if not addr:
        return                                  # not under systemd, or no watchdog
    if addr.startswith('@'):
        addr = '\0' + addr[1:]                  # abstract namespace socket
    with socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM | socket.SOCK_CLOEXEC) as sock:
        sock.sendto(state, addr)
```

A missed ping ends the service with `SIGABRT` (or `WatchdogSignal=`), and `Restart=on-failure`
restarts it. A restarted gate is latched; a restarted driver must start with its commands at zero.

# Robot health: diagnostics and a health endpoint

Part of [ops-fleet](../SKILL.md). One answer per robot to "is it healthy?", used by the rollout
gate ([ansible-rollout.md](ansible-rollout.md)), the container healthcheck
([releases.md](releases.md)) and fleet alerts ([observability.md](observability.md)). Checked
against `ros/diagnostics` 4.2.7 (`ros2-jazzy` branch, all packages BSD-3-Clause) on 2026-11-25.

## 1. Diagnostics on each robot

Drivers report through `diagnostic_updater`, the host through `diagnostic_common_diagnostics`, and
one `aggregator_node` per robot publishes `/diagnostics_agg` and the worst level on
`/diagnostics_toplevel_state` (OK 0, WARN 1, ERROR 2, STALE 3). Writing reports, the analyzer
file and its traps are in [ops-bringup](../../ops-bringup/references/diagnostics.md). For a fleet:

- Run `hd_monitor.py` on the partition that holds bags as well (`-p path:=/var/lib/my_robot`);
  bags fill disks faster than logs. It warns below 5 % free and errors below 1 %.
- List every driver's status names in the analyzers' `expected`, so a driver that never started
  shows as missing instead of absent, and set `critical: true` so the top level worsens at once.
- With namespaces: the aggregator subscribes to `/diagnostics` and publishes its two topics by
  absolute name, and its node is called `analyzers`, so remap the topics per robot
  ([identity-config.md](identity-config.md)) and key its parameters `/**/analyzers:`.
- Topic rates without code changes: `greenwave_monitor` (NVIDIA, Apache-2.0, Jazzy binary 1.0.0)
  measures rate and latency of listed topics and publishes them as diagnostics. Take its
  parameter names from the README of the version you install; the repository moves ahead of the
  release.

Check: `ros2 topic echo --once /diagnostics_toplevel_state` shows level 0 on a healthy robot;
stopping a sensor driver raises it within the analyzer's `timeout`.

## 2. Serve one health answer

A small node turns the top level and the age of a few critical topics into HTTP 200 or 503.
It binds to `127.0.0.1`: the rollout runs its check on the robot, so the endpoint never needs to
be reachable from the network. Ship it in the release (for example in `my_robot_bringup`,
`ament_python`, depending on `rclpy`, `diagnostic_msgs`, `rosidl_runtime_py`).

```python
#!/usr/bin/env python3
"""Health endpoint for fleet rollouts: GET /healthz returns 200 when healthy, else 503."""
import json
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import rclpy
from diagnostic_msgs.msg import DiagnosticStatus
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from rosidl_runtime_py.utilities import get_message


def level_of(status):
    # 'byte' fields arrive in rclpy as a one-byte bytes object
    return status.level if isinstance(status.level, int) else ord(status.level)


class Health(Node):
    def __init__(self):
        super().__init__('health_endpoint')
        self.bind = self.declare_parameter('bind', '127.0.0.1').value
        self.port = self.declare_parameter('port', 8080).value
        self.diag_timeout = self.declare_parameter('diag_timeout_s', 5.0).value
        self.max_level = self.declare_parameter('max_level', 1).value   # WARN still healthy
        self.pending = list(self.declare_parameter('topics', ['odom', 'scan']).value)
        self.topic_timeout = self.declare_parameter('topic_timeout_s', 2.0).value
        try:
            with open('/etc/my_robot/release') as f:
                self.release = f.read().strip()
        except OSError:
            self.release = 'unknown'
        self.lock = threading.Lock()
        self.toplevel = None      # (monotonic time, level, message)
        self.last_seen = {}       # topic -> monotonic time of last message
        self.create_subscription(
            DiagnosticStatus, '/diagnostics_toplevel_state', self.on_toplevel, 10)
        self.create_timer(1.0, self.subscribe_pending)   # topics can appear after start

    def on_toplevel(self, msg):
        with self.lock:
            self.toplevel = (time.monotonic(), level_of(msg), msg.message)

    def subscribe_pending(self):
        types = dict(self.get_topic_names_and_types())
        ns = self.get_namespace().rstrip('/')
        for name in list(self.pending):
            full = name if name.startswith('/') else f'{ns}/{name}'
            if full not in types:
                continue
            self.create_subscription(
                get_message(types[full][0]), full,
                lambda _msg, t=full: self.mark(t), qos_profile_sensor_data, raw=True)
            with self.lock:
                self.pending.remove(name)
                self.last_seen[full] = time.monotonic()   # grace period starts now

    def mark(self, topic):
        with self.lock:
            self.last_seen[topic] = time.monotonic()

    def report(self):
        now = time.monotonic()
        problems = []
        with self.lock:
            if self.toplevel is None or now - self.toplevel[0] > self.diag_timeout:
                problems.append('no /diagnostics_toplevel_state')
            elif self.toplevel[1] > self.max_level:
                problems.append(f'diagnostics level {self.toplevel[1]}: {self.toplevel[2]}')
            problems += [f'{t}: not advertised' for t in self.pending]
            problems += [f'{t}: silent for over {self.topic_timeout} s'
                         for t, stamp in self.last_seen.items()
                         if now - stamp > self.topic_timeout]
        return {'healthy': not problems, 'release': self.release, 'problems': problems}


def handler_for(node):
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path != '/healthz':
                self.send_error(404)
                return
            body = node.report()
            self.send_response(200 if body['healthy'] else 503)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(body).encode())

        def log_message(self, *args):
            pass   # keep the journal quiet; the rollout logs results
    return Handler


def main():
    rclpy.init()
    node = Health()
    server = ThreadingHTTPServer((node.bind, node.port), handler_for(node))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        server.shutdown()
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()
```

- Parameters: `topics` lists the topics that must flow (relative names get the node's
  namespace); keep at least one entry, since an empty list in YAML cannot be typed as strings.
  Timeouts and port are examples; set `topic_timeout_s` above the slowest listed topic's period.
- The endpoint answers in milliseconds. Never shell out to `ros2 topic hz` or `ros2 topic echo`
  in a health check: each call starts a new node and waits for discovery (and `ros2 topic hz`
  has no `--once`).
- A health check that only opens a TCP port says nothing about the ROS graph; this one fails when
  the aggregator, or any listed topic, goes quiet.

Check: `curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:8080/healthz` on the robot prints
200; stopping the lidar driver turns it to 503 with the reason in the body.

## 3. Where it is used

| User | How |
|---|---|
| Container | `healthcheck:` in compose ([releases.md](releases.md)); `docker compose up --wait` waits for it |
| Rollout | `ansible.builtin.uri` against `127.0.0.1:8080/healthz` on each robot, retried, after the switch |
| Fleet alerts | the diagnostics exporter in [observability.md](observability.md) sends the top level as a metric |
| Safety | not at all: health is for operations. Stops and watchdogs belong in [arch-safety](../../arch-safety/SKILL.md) |

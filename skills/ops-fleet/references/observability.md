# Logs, metrics and fleet alerts

Part of [ops-fleet](../SKILL.md). One agent on each robot ships the journal to Loki and host plus
ROS metrics to Prometheus; Grafana shows the fleet and alerts. Sources (read 2026-11-25): ROS 2
docs "Logging" (jazzy branch), `rcl_logging_spdlog` (jazzy), Grafana Alloy docs (main), Loki's
Promtail page, `diagnostic_remote_logging` README (ros2-jazzy).

| Part | Licence | Runs on |
|---|---|---|
| Grafana Alloy (agent) | Apache-2.0 | each robot |
| Prometheus (metrics store, `--web.enable-remote-write-receiver`) | Apache-2.0 | fleet server |
| Loki (log store) | AGPL-3.0 | fleet server |
| Grafana (dashboards, alerts) | AGPL-3.0 | fleet server; Grafana Cloud is the hosted, paid-beyond-free-tier option |

Promtail, the old log shipper, reached end of life on 2026-03-02; use Alloy (`alloy convert
--source-format=promtail` converts old configs). Vector (MPL-2.0) and Fluent Bit (Apache-2.0) are
alternatives to Alloy.

## Logs on the robot

The robot's own log handling is in [ops-bringup](../../ops-bringup/references/logs.md): ROS output
to the journal, journald limits and rate limits, `RCUTILS_COLORIZED_OUTPUT=0`, and ageing out the
ROS log files, which Jazzy's file logger never rotates (`rcl_logging_spdlog` uses a plain file
sink). For a fleet, add:

- Container output in the journal too, so one agent reads everything:

  ```yaml
  services:
    robot:
      logging:
        driver: journald
        options: {tag: my-robot}
  ```

- A journal sized for the longest time a robot is offline: while it is, its logs wait there.

## The agent: Alloy

Install from Grafana's apt repository (`apt.grafana.com`, package `alloy`); configuration in
`/etc/alloy/config.alloy`, environment in `/etc/default/alloy` (put `ROBOT_ID=robot-01` there).
The `alloy` user must be in the `adm` and `systemd-journal` groups
(`sudo usermod -aG adm,systemd-journal alloy`); otherwise the journal source starts without error
and sends nothing.

```alloy
// /etc/alloy/config.alloy on each robot (rendered by Ansible)
loki.relabel "journal" {
  forward_to = []
  rule {
    source_labels = ["__journal__systemd_unit"]
    target_label  = "unit"
  }
  rule {
    source_labels = ["__journal_priority_keyword"]
    target_label  = "level"
  }
  rule {                       // the Compose logging tag; container logs carry unit docker.service
    source_labels = ["__journal_syslog_identifier"]
    target_label  = "ident"
  }
}

loki.source.journal "robot" {
  forward_to    = [loki.write.fleet.receiver]
  relabel_rules = loki.relabel.journal.rules
}

loki.write "fleet" {
  endpoint {
    url               = "https://logs.fleet.example.com/loki/api/v1/push"
    bearer_token_file = "/etc/alloy/loki-token"
  }
  external_labels = { robot = sys.env("ROBOT_ID") }
}

prometheus.exporter.unix "host" {
  enable_collectors = ["systemd"]              // unit states; off by default
  textfile {
    directory = "/var/lib/my_robot/metrics"    // ROS metrics from the node below
  }
}

prometheus.scrape "host" {
  targets         = prometheus.exporter.unix.host.targets
  forward_to      = [prometheus.remote_write.fleet.receiver]
  scrape_interval = "30s"
}

prometheus.remote_write "fleet" {
  endpoint {
    url               = "https://metrics.fleet.example.com/api/v1/write"
    bearer_token_file = "/etc/alloy/metrics-token"
  }
  external_labels = { robot = sys.env("ROBOT_ID") }
}
```

- Robots push; the fleet server never needs to reach into robot networks.
- Keep labels few and bounded (`robot`, `unit`, `ident`, `level`). Never make a label out of a message,
  a pose or a timestamp; Loki's index grows with every distinct value.
- Offline robots: metrics wait in remote_write's write-ahead log, kept at most `max_keepalive_time`
  (8 h by default), then dropped; logs wait in the journal.

Check: in Grafana, `{robot="robot-01", unit="my-robot.service"}` (native release) or
`{robot="robot-01", ident="my-robot"}` (Compose release) shows the robot's ROS output, and
`node_load1{robot="robot-01"}` has data.

## ROS diagnostics as metrics

A small node writes the aggregated diagnostics ([health.md](health.md)) and the release as
Prometheus text for the `textfile` collector. Same package as the health endpoint.

```python
#!/usr/bin/env python3
"""Write ROS diagnostics and the release as Prometheus text for the textfile collector."""
import os
import tempfile
import time

import rclpy
from diagnostic_msgs.msg import DiagnosticArray, DiagnosticStatus
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node


def level_of(status):
    return status.level if isinstance(status.level, int) else ord(status.level)


def esc(value):
    return value.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')


class DiagMetrics(Node):
    def __init__(self):
        super().__init__('diag_metrics')
        self.path = self.declare_parameter('file', '/var/lib/my_robot/metrics/ros.prom').value
        self.items, self.top = {}, None
        try:
            with open('/etc/my_robot/release') as f:
                self.release = f.read().strip()
        except OSError:
            self.release = 'unknown'
        self.create_subscription(DiagnosticArray, '/diagnostics_agg', self.on_agg, 10)
        self.create_subscription(
            DiagnosticStatus, '/diagnostics_toplevel_state', self.on_top, 10)
        self.create_timer(15.0, self.write)

    def on_agg(self, msg):
        self.items = {s.name: level_of(s) for s in msg.status}

    def on_top(self, msg):
        self.top = level_of(msg)

    def write(self):
        lines = ['# TYPE ros_diagnostic_level gauge']
        lines += [f'ros_diagnostic_level{{name="{esc(n)}"}} {v}' for n, v in sorted(self.items.items())]
        if self.top is not None:
            lines += ['# TYPE ros_diagnostics_toplevel gauge', f'ros_diagnostics_toplevel {self.top}']
        lines += ['# TYPE my_robot_release_info gauge',
                  f'my_robot_release_info{{release="{esc(self.release)}"}} 1',
                  '# TYPE ros_diagnostics_written_seconds gauge',
                  f'ros_diagnostics_written_seconds {time.time():.0f}']
        folder = os.path.dirname(self.path)
        with tempfile.NamedTemporaryFile('w', dir=folder, suffix='.tmp', delete=False) as f:
            f.write('\n'.join(lines) + '\n')
        os.chmod(f.name, 0o644)
        os.replace(f.name, self.path)   # atomic: the collector never reads half a file


def main():
    rclpy.init()
    node = DiagMetrics()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()
```

Already on InfluxDB? `diagnostic_remote_logging` (BSD-3-Clause, in the Jazzy release) has an
`influxdb_connector` node that sends `/diagnostics` and the top level to InfluxDB v2, directly or
through Telegraf; use it instead of writing your own collector.

## Fleet alerts

Example Prometheus rules; every threshold is a starting point to tune.

```yaml
groups:
  - name: fleet
    rules:
      - alert: RobotSilent          # sent metrics an hour ago, nothing now
        expr: count by (robot) (node_boot_time_seconds offset 1h) unless count by (robot) (node_boot_time_seconds)
        for: 10m
      - alert: RobotDiagnosticsError
        expr: ros_diagnostics_toplevel >= 2          # ERROR or STALE
        for: 2m
      - alert: RobotDiagnosticsExporterStale
        expr: time() - ros_diagnostics_written_seconds > 120
      - alert: RobotServiceDown       # native release; for Compose, probe /healthz (health.md)
        expr: node_systemd_unit_state{name="my-robot.service", state="active"} == 0
        for: 2m
      - alert: RobotDiskLow
        expr: node_filesystem_avail_bytes{mountpoint="/"} / node_filesystem_size_bytes{mountpoint="/"} < 0.10
        for: 15m
      - alert: RobotHot             # set below your board's throttling temperature
        expr: max by (robot) (node_thermal_zone_temp) > 80
        for: 10m
```

A fleet dashboard needs little: one row per robot with `my_robot_release_info`, the top-level
diagnostics level, battery (from your driver's diagnostics), disk, temperature and last-seen
time. Annotate deploys (the rollout can post a Grafana annotation) so a fault lines up with the
release that caused it.

## Checks

- Every robot appears in `count by (robot) (node_boot_time_seconds)`.
- Stopping `my-robot.service` on a test robot fires `RobotServiceDown` and its last log lines are
  in Loki under that robot's label.
- `my_robot_release_info` shows the release each robot runs, matching `status.yml`.

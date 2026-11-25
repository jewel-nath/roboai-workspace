# Robot identity and per-robot configuration

Part of [ops-fleet](../SKILL.md). Every robot runs the same release; what differs (name, domain,
calibration, device paths, secrets) lives in `/etc/my_robot/` and is written by the rollout
tool, never edited by hand. Checked against `launch_ros` and `robot_state_publisher` on their
`jazzy` branches and the ROS 2 docs "Passing ROS arguments to nodes" (2026-11-25).

## What lives where

| Layer | Where | Written by | Example |
|---|---|---|---|
| Release defaults | `share/my_robot_bringup/config/*.yaml` in the image or deb | the build | controller gains, Nav2 parameters |
| Identity | `/etc/my_robot/env.sh` (and `robot.env` for compose) | Ansible from `host_vars` | `ROBOT_ID`, `ROS_DOMAIN_ID` |
| Per-robot overlay | `/etc/my_robot/params/robot.yaml` | Ansible from `host_vars` | serial device, wheel radius after calibration |
| Calibration | `/etc/my_robot/calibration/` | the calibration procedure, then copied to the inventory repo | camera intrinsics, lidar extrinsics |
| Secrets | `/etc/my_robot/secrets/` (root, mode 0600) | Ansible Vault | registry pull token, VPN key |
| Release marker | `/etc/my_robot/release` | the rollout | `1.4.0` |

Keep the inventory (and the calibration copies) in a git repository of their own; it is the only
record of how each robot differs. Secrets go into it only encrypted (`ansible-vault`).

## The identity file

Identity goes into the environment file the robot already uses: `/etc/my_robot/env.sh` from
[ops-bringup](../../ops-bringup/references/systemd.md), sourced by the systemd unit and by anyone
running `ros2` on the robot. Ansible renders it from `host_vars`:

```bash
# /etc/my_robot/env.sh - rendered by Ansible; the rest of the file as in ops-bringup
export ROBOT_ID=robot-01
export ROBOT_NAMESPACE=                         # empty: one domain per robot (default here)
export ROS_DOMAIN_ID=11
export RMW_IMPLEMENTATION=rmw_fastrtps_cpp
export ROS_AUTOMATIC_DISCOVERY_RANGE=LOCALHOST  # one computer; SUBNET for two, see discovery.md
```

- For containers, Ansible renders the same variables without `export` into
  `/etc/my_robot/robot.env`, which compose reads with `env_file:` ([releases.md](releases.md)).
  Both come from one `host_vars` file, so they cannot disagree.
- `ROBOT_ID` may contain `-`; a ROS namespace may not. If you need a namespace, derive one
  (`robot_01`) and store both.
- Set nothing identity-related inside the image or the package.

## Per-robot parameter overlay

ROS 2 applies parameter files in order, so a launch file lists the release defaults first and the
robot's overlay last. Use wildcard keys in the overlay: a plain `driver:` key does not match
`/robot_01/driver`, while `/**/driver:` matches it under any namespace ("`**` matches zero or more
tokens").

```yaml
# inventory/host_vars/robot-01.yml (excerpt)
robot_id: robot-01
ros_domain_id: 11
robot_params:
  /**/driver:
    ros__parameters:
      serial_port: /dev/serial/by-id/usb-My_Vendor_My_MCU_0001-if00
  /**/diff_drive_controller:
    ros__parameters:
      wheel_radius: 0.0502            # measured on this robot
```

```jinja
{# templates/robot.yaml.j2 -> /etc/my_robot/params/robot.yaml #}
# Rendered by Ansible for {{ robot_id }}; edit host_vars, not this file.
{{ robot_params | to_nice_yaml(indent=2) }}
```

The bringup launch file reads identity from the environment and adds the overlay when present:

```python
# my_robot_bringup/launch/robot.launch.py (excerpt)
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import GroupAction
from launch_ros.actions import Node, PushROSNamespace

OVERLAY = '/etc/my_robot/params/robot.yaml'


def generate_launch_description():
    share = get_package_share_directory('my_robot_bringup')
    params = [os.path.join(share, 'config', 'robot.yaml')]
    if os.path.exists(OVERLAY):
        params.append(OVERLAY)          # later files override earlier ones

    nodes = [
        Node(package='my_robot_driver', executable='driver_node', name='driver',
             parameters=params),
        # robot_state_publisher, controllers, sensors ... all with parameters=params
    ]
    namespace = os.environ.get('ROBOT_NAMESPACE', '')
    return LaunchDescription([GroupAction([PushROSNamespace(namespace), *nodes])])
```

`PushROSNamespace` is the Jazzy name; `PushRosNamespace` still imports as an alias, and is the
only name on Humble.

Check: `ros2 param get /driver serial_port` (or `/robot_01/driver`) on the robot returns the
overlay value, not the release default.

## One domain per robot, or namespaces

**Default: one `ROS_DOMAIN_ID` per robot, no namespaces.** Each robot's graph is the same as on
the bench, nodes and parameter files need no change, and one robot's `/cmd_vel` cannot reach
another. Fleet tools join a robot's domain to look at it ([discovery.md](discovery.md)).

**Namespaces** when several robots must share one graph (a multi-robot simulation, or a fleet
node that subscribes to all of them in one process). Then:

- Topic names that start with `/` ignore the namespace. Common ones: `/tf`, `/tf_static`,
  `/diagnostics`, `/diagnostics_agg`, `/diagnostics_toplevel_state`, and any absolute name in
  your own code. Remap them per node, for example
  `remappings=[('/tf', 'tf'), ('/tf_static', 'tf_static')]`, the pattern Nav2's bringup uses, or
  `launch_ros.actions.SetRemap(src='/diagnostics', dst='diagnostics')` inside the group.
- Either keep frame names and namespace the TF topics (above), or keep one `/tf` and prefix the
  frames (`robot_state_publisher` parameter `frame_prefix: robot_01/`). Prefixing means every
  node's frame parameters (`base_frame_id`, `odom_frame_id`, ...) change too; namespaced TF
  topics are the smaller change.
- Parameter files need `/**/node:` keys (above), or the namespaced node silently runs on
  defaults.
- Services and actions called by absolute name (`/navigate_to_pose`) must be called with the
  namespace (`/robot_01/navigate_to_pose`).

Check: `ros2 topic list` shows no topic of a robot outside its namespace except `/rosout`,
`/parameter_events` and any you chose to share.

## Domain ID plan

On Linux use domain IDs 0 to 101 (and 215 to 232); others collide with the kernel's ephemeral
ports (ROS 2 docs, "The ROS_DOMAIN_ID"). An example plan to adapt:

| IDs | Use |
|---|---|
| 0 | Development benches and simulations (the default; never on a fielded robot) |
| 1–9 | Fleet tools that bridge robots (`domain_bridge`, dashboards) |
| 10–101 | One per robot: `robot-01` → 11, `robot-02` → 12, ... |

Beyond about 90 robots on one network, DDS domains run out; use namespaces with a discovery
server, or Zenoh with per-site routers.

## Secrets

- One credential per robot where the service allows it (VPN key, Foxlet device token), so a lost
  robot is revoked alone.
- Render them from Ansible Vault into `/etc/my_robot/secrets/` with `mode: "0600"` and
  `no_log: true` on the task; never into the image, the compose file, or `env.sh` and
  `robot.env`, which are world-readable.
- Read them at runtime from the file. Under systemd, `LoadCredential=` in the unit (see
  `systemd.exec(5)`) is a tighter option; the unit itself is in [ops-bringup](../../ops-bringup/SKILL.md).

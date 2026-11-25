# First power-on: the check sequence an agent runs

Part of [ops-bringup](../SKILL.md). This is the software side: commands an agent runs on the robot
computer over SSH, each with what "pass" looks like. The hands-on side (power rails, fuses,
E-stop, wiring) is a person's checklist and belongs to the integration and bringup playbook
(stage 8 in [playbooks](../../../playbooks/README.md)).

## Rules for the agent

- Read-only checks (steps 1 to 8) run without asking.
- **Nothing moves without a person.** Before any command that can move an actuator (step 9), ask
  the person on site to confirm: wheels off the ground or arm clear, E-stop in reach, and that
  they are watching. Stop and report if no one confirms. Stopping hardware safely is
  [arch-safety](../../arch-safety/SKILL.md)'s subject, not this sequence's.
- Start with `hardware:=mock` where the stack supports it, then the real hardware.
- Do not `systemctl enable` the service until it has started and stopped cleanly by hand.
- Record every result (pass, fail, the numbers seen) in the project; a failed step stops the
  sequence until it is fixed.

Run every `ros2` command after `source /etc/my_robot/env.sh`, as the robot user
(`sudo -iu robot`), so domain, middleware and workspace match the service.

## 1. Host

```bash
lsb_release -ds; uname -rm                       # Ubuntu 24.04, the expected kernel and arch
source /etc/my_robot/env.sh && printenv ROS_DISTRO RMW_IMPLEMENTATION ROS_DOMAIN_ID
ros2 doctor --report | grep -iE "distribution|middleware|warn" | head -20
df -h / /var/log; free -h
id robot                                         # dialout, video (and realtime if used)
```

Pass: `jazzy`, the planned RMW and domain on every computer of the robot; free disk and memory as
planned; the groups present.

## 2. Clocks (every computer)

```bash
timedatectl | grep -E "synchronized|NTP service"
chronyc tracking | grep -E "Reference ID|System time|Leap status"
chronyc sources
```

Pass: `System clock synchronized: yes`, `Leap status : Normal`, the robot's time server selected
(`*`) on the clients, offsets well under the tolerance you chose ([time-sync.md](time-sync.md)).

## 3. Devices

```bash
ls -l /dev/my_robot/ /dev/serial/by-id/ /dev/v4l/by-id/ 2>/dev/null
journalctl -k -b | grep -iE "usb.*(disconnect|error)|ttyUSB|ttyACM|uvcvideo" | tail -20
```

Pass: every planned link exists and points at the right node; no repeated disconnects. Ask the
person to unplug and replug one device: its link comes back with the same name ([udev.md](udev.md)).

## 4. Layers one at a time

Start each layer in the background, check it, stop it with SIGINT, then add the next:

```bash
set -m          # job control on: otherwise background jobs ignore SIGINT and cannot be stopped cleanly
run_layer() {   # run_layer <launch file> [args...]; output to ~/check-<file>.log
  ros2 launch my_robot_bringup "$@" > ~/check-"$1".log 2>&1 &
  echo $! > ~/check.pid; sleep 10                # a pause for a human-run check, not an order rule
}
stop_layer() { kill -INT "$(cat ~/check.pid)"; wait "$(cat ~/check.pid)" 2>/dev/null; }

run_layer robot.launch.py hardware:=mock use_localization:=false use_diagnostics:=false
ros2 control list_controllers                    # every controller 'active'
ros2 run tf2_ros tf2_echo base_link lidar_link   # the URDF transform, Ctrl-C after one print
stop_layer; grep -iE "error|exception|fatal" ~/check-robot.launch.py.log

run_layer drivers.launch.py
ros2 node list --no-daemon
ros2 topic hz /scan --window 50                  # the sensor's rated frequency
ros2 topic echo --once /scan --field header.frame_id
stop_layer
```

Pass: no errors in the logs; rates within the planned band; every `frame_id` a sensor publishes
exists in the URDF. Then the full stack on real hardware (`robot.launch.py`), checked by steps 5
to 8 while it runs.

## 5. Control and odometry, not moving

```bash
ros2 control list_hardware_components            # each component 'active'
ros2 control list_hardware_interfaces            # command interfaces [claimed]
ros2 topic echo --once /joint_states
ros2 run tf2_ros tf2_echo odom base_link
```

Pass: hardware active; joint states arrive at the controller manager's rate; `odom` → `base_link`
exists and stays still while the robot stands. Turn a wheel by hand (person): its joint position
changes in the right direction.

## 6. Readiness

```bash
ros2 run my_robot_bringup wait_ready.py --timeout 60 \
  --topics /joint_states /odom /scan /imu/data --transforms odom:base_link base_link:lidar_link
echo $?
```

Pass: exit code 0 within the timeout ([readiness.md](readiness.md)).

## 7. Diagnostics

```bash
ros2 topic echo --once /diagnostics_toplevel_state
ros2 topic echo --once /diagnostics_agg --field status | grep -E "name|level|message"
```

Pass: top level OK (0). Any WARN or ERROR is named and explained before going on
([diagnostics.md](diagnostics.md)).

## 8. Middleware across computers

From a second computer of the robot (or the operator laptop) with the same `env.sh` values:

```bash
ros2 node list --no-daemon
ros2 topic hz /scan
```

Pass: the robot's nodes are listed and data arrives. Nodes listed but no data: shared memory or
firewall; see [choose a ROS 2 middleware](../../../wiki/guides/choose-a-ros2-middleware.md).

## 9. First motion (only after the person confirms)

Mobile base, wheels off the ground, at a low speed:

```bash
ros2 topic pub --times 20 --rate 10 /diff_drive_controller/cmd_vel geometry_msgs/msg/TwistStamped \
  "{twist: {linear: {x: 0.05}}}"                 # 2 s forward at 0.05 m/s (example values)
```

Pass: both wheels turn forward, stop when the messages stop (the controller's `cmd_vel_timeout`),
and `/odom` x increases. Then, on the ground with the person watching: drive 1 m and compare the
odometry with a tape measure; turn one full circle and compare the yaw. A wrong direction or
distance is a wheel parameter or a joint sign in [ros2-control](../../ros2-control/SKILL.md). An
arm: move one joint a few degrees with the trajectory controller, as in that skill.

## 10. The service

```bash
sudo systemctl start my-robot.service
systemctl status my-robot.service --no-pager     # 'active (running)' after the readiness check
journalctl -u my-robot -b --no-pager | grep -iE "error|fatal|exception" | head
sudo systemctl stop my-robot.service
pgrep -u robot -af "ros2|_node" || echo "no ROS processes left"
journalctl -u my-robot -b | grep -iE "SIGKILL|Killing process|timed out" || echo "clean stop"
```

Pass: active within `TimeoutStartSec`; the stop leaves no process behind and needs no SIGKILL.
Then enable it and reboot:

```bash
sudo systemctl enable my-robot.service && sudo reboot
# after the reboot
systemctl is-active my-robot.service
systemd-analyze critical-chain my-robot.service
```

## 11. Recovery

- Ask the person to unplug a respawning sensor: its diagnostics go to ERROR or STALE, the driver
  restarts, and everything is back after replugging.
- Kill a node marked `on_exit=Shutdown()`: `pkill -INT -f battery_monitor`. The unit restarts
  within `RestartSec` and passes the readiness check again.
- Leave it running for an hour: no growing memory (`systemctl status` shows the unit's memory), no
  repeating warnings, `du -sh /var/log/my_robot` grows slowly ([logs.md](logs.md)).

## Report

One line per step: pass or fail, with the numbers (rates, offsets, start time, stop time). Attach
the launch logs and `journalctl -u my-robot -b` for any failure, and commit them with the result
in the project's repository.

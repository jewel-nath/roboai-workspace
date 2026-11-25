# Starting the robot at boot with systemd

Part of [ops-bringup](../SKILL.md). Directives checked against the systemd 255 man pages (the
version in Ubuntu 24.04); `ros2 launch` signal handling against launch 3.4 (`jazzy`). Values marked
"example" are choices to tune, not requirements.

## The robot user

```bash
sudo useradd -m -s /bin/bash robot                 # owns the workspace and runs the stack
sudo usermod -aG dialout,video,input robot         # serial ports, cameras, joysticks
sudo usermod -aG realtime robot                    # only with the realtime group from ros2-control
ls -l /dev/my_robot/                               # any other device: add the group shown here
```

Group changes reach a service at its next start and a shell at the next login.

## One environment file for the service, the checks and people

```bash
# /etc/my_robot/env.sh  (root:root 0644). Sourced, never executed.
# Keep it free of `set -u`: the ROS setup scripts read unset variables.
export ROS_DOMAIN_ID=42                            # example; 0-101 is safe on Linux
export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp       # same value on every computer of the robot
export CYCLONEDDS_URI=file:///etc/my_robot/cyclonedds.xml   # only if you need one
export ROS_AUTOMATIC_DISCOVERY_RANGE=SUBNET        # the default; LOCALHOST for a single computer
export ROS_LOG_DIR=/var/log/my_robot               # created by LogsDirectory= below
export RCUTILS_COLORIZED_OUTPUT=0                  # no colour codes in the journal
export PYTHONUNBUFFERED=1                          # print() from Python nodes appears at once
source /opt/ros/jazzy/setup.bash
source /home/robot/ros2_ws/install/setup.bash
```

An agent or a person on the robot runs `source /etc/my_robot/env.sh` before any `ros2` command, so
the CLI sees the same domain and middleware as the service. The domain range and discovery
variables are from the ROS 2 docs (About Domain ID, Improved Dynamic Discovery); middleware choice
is in [choose a ROS 2 middleware](../../../wiki/guides/choose-a-ros2-middleware.md).

## The unit

```ini
# /etc/systemd/system/my-robot.service
[Unit]
Description=my_robot ROS 2 bringup
Wants=network-online.target
After=network-online.target time-sync.target
# Start-rate limit lives in [Unit]; in [Service] StartLimitIntervalSec= is ignored
StartLimitIntervalSec=600
StartLimitBurst=10

[Service]
Type=exec
User=robot
Group=robot
LogsDirectory=my_robot
# Wait for the devices the robot cannot run without (udev.md); a timeout here fails the start
ExecStartPre=/usr/bin/udevadm wait --timeout=30 /dev/my_robot/motor /dev/my_robot/lidar
# exec: ros2 launch must be the main process, or it never receives the stop signal
ExecStart=/bin/bash -c 'source /etc/my_robot/env.sh && exec ros2 launch my_robot_bringup robot.launch.py'
# The unit turns active only when the robot is ready (readiness.md)
ExecStartPost=/bin/bash -c 'source /etc/my_robot/env.sh && exec ros2 run my_robot_bringup wait_ready.py --timeout 90'
TimeoutStartSec=180
# SIGINT to ros2 launch only; it forwards SIGINT to each node, escalates after 5 s + 5 s
KillMode=mixed
KillSignal=SIGINT
TimeoutStopSec=30
Restart=always
RestartSec=5
RestartSteps=5
RestartMaxDelaySec=60
SyslogIdentifier=my-robot
# Only for ros2_control_node's SCHED_FIFO thread; limits.conf does not apply to services
LimitRTPRIO=99
LimitMEMLOCK=infinity

[Install]
WantedBy=multi-user.target
```

Why each choice:

| Setting | Reason |
|---|---|
| `Type=exec` | `simple` reports success even if the binary cannot start; `notify` waits for a `READY=1` that `ros2 launch` never sends, so the start times out. |
| `After=time-sync.target` | Has an effect only when a wait service (chrony-wait) is enabled; see [time-sync.md](time-sync.md). Do not add it to `Wants=`. |
| `After=`/`Wants=network-online.target` | DDS picks its network interfaces when each node starts; a node started before the robot's network is up can stay unreachable from the other computers. |
| `ExecStartPre=udevadm wait` | Fails the start (and so triggers `Restart=`) if a device is missing, instead of letting drivers crash in a loop. Needs systemd 251. |
| `KillMode=mixed`, `KillSignal=SIGINT` | `ros2 launch` treats SIGTERM as an abort ("can result in orphaned processes"); on SIGINT it stops every node in order. With `mixed`, leftovers get SIGKILL after `TimeoutStopSec`. |
| `TimeoutStopSec=30` | Above launch's own escalation (SIGINT, 5 s, SIGTERM, 5 s, SIGKILL) plus the drivers' shutdown time. Example value. |
| `Restart=always` | `on-failure` does not restart after a clean exit, and both `Shutdown()` in a launch file and a SIGINT exit count as clean. A `systemctl stop` is never restarted. |
| `RestartSteps`/`RestartMaxDelaySec` | Back off from 5 s to 60 s between restarts (systemd 254+). Example values. |
| `StartLimitIntervalSec`/`Burst` | After 10 starts in 10 minutes the unit stays failed until `systemctl reset-failed`; a person must look. Example values. |
| `LimitRTPRIO`/`LimitMEMLOCK` | Without them `ros2_control_node` logs `Could not enable FIFO RT scheduling policy`. |

Install and check it:

```bash
sudo install -m 0644 host/my-robot.service /etc/systemd/system/
sudo systemd-analyze verify /etc/systemd/system/my-robot.service   # prints nothing when clean
sudo systemctl daemon-reload
sudo systemctl start my-robot.service && systemctl status my-robot.service --no-pager
sudo systemctl enable my-robot.service                             # only after it starts cleanly
systemd-analyze critical-chain my-robot.service                     # what it waited for at boot
```

Resource caps are optional: `MemoryMax=` and `CPUQuota=` (systemd.resource-control) limit the
whole stack. `systemctl show -p OOMPolicy my-robot.service` tells what an OOM kill of one node
does: `stop` ends the whole unit (and `Restart=always` brings it back), `continue` leaves the
stack running without that node.

## Splitting the stack into several units

One unit is enough for most robots. Split when a layer must restart without restarting the
hardware, for example navigation:

```ini
# /etc/systemd/system/my-robot-nav.service
[Unit]
Description=my_robot navigation
Requires=my-robot.service
After=my-robot.service
# A stop or restart of the base unit also stops or restarts this one
PartOf=my-robot.service

[Service]
Type=exec
User=robot
Group=robot
ExecStart=/bin/bash -c 'source /etc/my_robot/env.sh && exec ros2 launch my_robot_navigation navigation.launch.py use_rviz:=false'
KillMode=mixed
KillSignal=SIGINT
TimeoutStopSec=30
Restart=always
RestartSec=5
SyslogIdentifier=my-robot-nav

[Install]
WantedBy=my-robot.service
```

`After=my-robot.service` waits for the base unit's `ExecStartPost` readiness check, so navigation
starts on a robot that is already up. Run the base with `use_navigation:=false`.

## Zenoh router

With `RMW_IMPLEMENTATION=rmw_zenoh_cpp`, each computer runs one router before any node:

```ini
# /etc/systemd/system/my-robot-zenohd.service
[Unit]
Description=Zenoh router for ROS 2
Wants=network-online.target
After=network-online.target

[Service]
Type=exec
User=robot
ExecStart=/bin/bash -c 'source /etc/my_robot/env.sh && exec ros2 run rmw_zenoh_cpp rmw_zenohd'
Restart=always
RestartSec=2

[Install]
WantedBy=multi-user.target
```

Add `Requires=my-robot-zenohd.service` and `After=my-robot-zenohd.service` to `my-robot.service`.
A node that starts before the router checks once (`ZENOH_ROUTER_CHECK_ATTEMPTS` unset) and connects
when the router appears; `0` makes it wait forever (rmw_zenoh `jazzy` README).

## robot_upstart

`robot_upstart` 1.0.4 (BSD) has Jazzy and Humble binaries, no Lyrical release.
`ros2 run robot_upstart install my_robot_bringup/launch/robot.launch.py --job my-robot --user robot
--ros_domain_id 42 --rmw rmw_cyclonedds_cpp --logdir /var/log/my_robot` writes a unit and start
script. Check what it generated before relying on it: the unit has no `Restart=`, orders only
`After=network.target` (`--systemd-after` changes that), puts logs in `/tmp` unless `--logdir` is
given, stops the launch with SIGTERM, and drops to the user with `setpriv --reuid` only, so the job
does not get the user's `dialout` or `video` groups. The hand-written unit above avoids all five.

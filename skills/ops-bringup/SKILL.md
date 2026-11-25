---
name: ops-bringup
description: Bring a ROS 2 Jazzy robot up reliably - layered my_robot_bringup launch files, a systemd unit (env, ROS_DOMAIN_ID, RMW, user, restart), robot_upstart,
  udev rules for stable /dev names, start order and readiness checks, diagnostic_updater and diagnostic_aggregator, journald and ROS log cleanup,
  chrony clock sync between computers, and a first power-on check sequence. Use when the robot must start at boot or fails to.
license: Apache-2.0
metadata:
  sources: [robotics-agent-skills]
  evidence: researched
  last_verified: 2026-11-25
---

# Robot bringup

Lets an agent turn a set of working ROS 2 packages into a robot that starts the same way on every
boot, reports its health, keeps its logs bounded and agrees on the time, and prove it with a
check sequence. Written for ROS 2 Jazzy on Ubuntu 24.04 (systemd 255, launch 3.4, diagnostics 4.2,
chrony 4.5); the recipes were researched, not run. Lyrical and Humble differences are at the end.

## When to use

- Writing `my_robot_bringup`: one launch file per layer, a top-level launch with arguments.
- Starting the stack at boot with systemd, or fixing a unit that never becomes active, restarts in
  a loop, or leaves nodes behind on stop.
- Device paths that change between boots, `Permission denied` on a serial port or camera.
- Nodes that start before what they need; a readiness gate for the unit.
- Adding `/diagnostics` to drivers and grouping them; journald and ROS log directories filling the disk.
- TF extrapolation errors between two computers of one robot (clock sync).
- Running the first power-on of a robot computer, or re-checking one after changes.

Elsewhere: Docker images and CI in [ops-docker-ci](../ops-docker-ci/SKILL.md); updates, rollback
and fleets in [ops-fleet](../ops-fleet/SKILL.md); E-stops, watchdogs and safe stopping in
[arch-safety](../arch-safety/SKILL.md); package and node structure in
[arch-robot-architecture](../arch-robot-architecture/SKILL.md); launch-file syntax, QoS and
lifecycle nodes in [ros2-core](../ros2-core/SKILL.md); controllers and hardware interfaces in
[ros2-control](../ros2-control/SKILL.md). The person's first power-on checklist (power, fuses,
wiring) is the integration and bringup playbook (stage 8 in [playbooks](../../playbooks/README.md)).

## Quick start

On the robot computer, with the workspace built in `/home/robot/ros2_ws`:

```bash
sudo useradd -m -s /bin/bash robot && sudo usermod -aG dialout,video robot
sudo install -D -m 0644 host/env.sh /etc/my_robot/env.sh            # references/systemd.md
sudo install -m 0644 host/99-my-robot.rules /etc/udev/rules.d/       # references/udev.md
sudo udevadm control --reload-rules && sudo udevadm trigger --action=add
sudo install -m 0644 host/my-robot.service /etc/systemd/system/
sudo systemd-analyze verify /etc/systemd/system/my-robot.service
sudo systemctl daemon-reload && sudo systemctl start my-robot.service
systemctl status my-robot.service --no-pager      # active once wait_ready.py passed
journalctl -u my-robot -b -e
sudo systemctl enable my-robot.service            # only after a clean start and stop
```

`host/` is a folder in `my_robot_bringup` holding the files installed into `/etc`
([references/launch.md](references/launch.md)).

## Workflow

1. **Fix the robot's environment.** One `ROS_DOMAIN_ID` (0 to 101 on Linux), one
   `RMW_IMPLEMENTATION` (installed, and an `exec_depend` of the bringup package), one robot user in
   `dialout` and `video`, all in `/etc/my_robot/env.sh`, which the service, the checks and people
   source. Middleware choice: [choose a ROS 2 middleware](../../wiki/guides/choose-a-ros2-middleware.md).
   *Check:* `source /etc/my_robot/env.sh && printenv ROS_DOMAIN_ID RMW_IMPLEMENTATION` gives the
   same values on every computer of the robot; `id robot` shows the groups.

2. **Write the bringup package in layers.** `description`, `control`, `drivers`, `localization`,
   `diagnostics`, plus navigation and manipulation included from their own packages; a top-level
   `robot.launch.py` with `hardware:=real|mock|gz`, `use_sim_time` and one `use_<layer>` switch
   each. Give each include its arguments explicitly. For each node decide what happens when it
   dies: `respawn=True`, or `on_exit=Shutdown()` so systemd restarts everything. Files:
   [references/launch.md](references/launch.md).
   *Check:* `ros2 launch my_robot_bringup robot.launch.py --show-args` lists the switches;
   `hardware:=mock` starts with no errors; each layer also starts alone.

3. **Give devices stable names.** Parameters use `/dev/serial/by-id/...` or a role link from a
   udev rule (`/dev/my_robot/lidar`), never `/dev/ttyUSB0`. Match by serial number when it is
   unique, by port path when it is not; set no `MODE="0666"`; keep ModemManager off MCU ports.
   Rules and tests: [references/udev.md](references/udev.md).
   *Check:* after replugging every device and one reboot, `ls -l /dev/my_robot/` shows each link
   on the right device; `sudo -u robot` can open each one.

4. **Order by state, gate on readiness.** No `TimerAction` delays: the spawner, the controller
   manager and Nav2's lifecycle managers already wait; use launch events or lifecycle states for
   the rest. `wait_ready.py` waits for the robot's topics and transforms and runs as the unit's
   `ExecStartPost`, so the unit turns active only when the robot is up.
   [references/readiness.md](references/readiness.md).
   *Check:* `ros2 run my_robot_bringup wait_ready.py --topics ... --transforms ...` exits 0 on a
   running robot and 1, naming what is missing, with one driver stopped.

5. **Report health.** Each driver publishes `/diagnostics` through `diagnostic_updater` (connection
   state, publish rate, hardware ID); `aggregator_node` groups them by analyzers in
   `config/diagnostics.yaml`; the host monitors from `diagnostic_common_diagnostics` cover CPU,
   RAM and disk. [references/diagnostics.md](references/diagnostics.md).
   *Check:* `ros2 topic echo --once /diagnostics_toplevel_state` is level 0; no item sits under
   "Other"; stopping a driver turns its group ERROR or STALE.

6. **Synchronise the clocks.** With more than one computer, run chrony: the main computer serves
   (`allow`, `local stratum 10`), the others use only it, and `chrony-wait.service` delays
   `time-sync.target` on the clients. [references/time-sync.md](references/time-sync.md).
   *Check:* `chronyc tracking` shows `Leap status : Normal` and a small offset on each client;
   `chronyc sources` marks the robot's server `*`.

7. **Start at boot with systemd.** One unit: `Type=exec`, `User=robot`, `After=network-online.target
   time-sync.target`, `ExecStartPre=udevadm wait` for required devices, `ExecStart` that sources
   `env.sh` and `exec`s `ros2 launch`, `KillMode=mixed` + `KillSignal=SIGINT`, `Restart=always`
   with back-off and a start limit in `[Unit]`, `LimitRTPRIO`/`LimitMEMLOCK` for ros2_control.
   Split into several units only for layers that restart alone. `robot_upstart` works on Jazzy but
   needs fixing up. Unit, reasons and alternatives: [references/systemd.md](references/systemd.md).
   *Check:* `systemd-analyze verify` is silent; `systemctl start` returns after the readiness
   check; `systemctl stop` leaves no ROS process and logs no SIGKILL.

8. **Bound the logs.** The journal gets every node's ROS log output; set its size, retention and
   rate limit in a drop-in. ROS log files go to `/var/log/my_robot` (`LogsDirectory=`), aged out by
   a `tmpfiles.d` rule; chatty nodes lose their file log or their debug level.
   [references/logs.md](references/logs.md).
   *Check:* `journalctl -u my-robot -b -1` shows the previous boot; `journalctl --disk-usage` and
   `du -sh /var/log/my_robot` stay within the plan after an hour's run.

9. **Run the first power-on sequence.** Host, clocks, devices, layers one at a time, control,
   readiness, diagnostics, discovery from a second computer, then motion only after a person on
   site confirms the robot is safe to move, then the service, a reboot and recovery tests.
   Commands and pass criteria: [references/first-power-on.md](references/first-power-on.md).
   *Check:* every step recorded as pass with its numbers, in the project's repository.

## Traps

| Symptom | Cause | Fix |
|---|---|---|
| `ros2: command not found` or `package not found` in the unit | systemd reads no `.bashrc` | Source `env.sh` in `ExecStart`; never `.bashrc` |
| `unbound variable` from `setup.bash` | Script runs with `set -u` | Drop `-u` around the ROS `source` lines |
| Unit `activating` until `TimeoutStartSec`, then fails | `Type=notify` and nobody sends `READY=1` | `Type=exec` plus `ExecStartPost` readiness check |
| `systemctl start` succeeds, robot not running | `Type=simple` reports success before exec | `Type=exec`; read `journalctl -u` |
| Stop takes `TimeoutStopSec`, then SIGKILL; nodes orphaned | Default SIGTERM to `ros2 launch` ("can result in orphaned processes"), or `bash -c` without `exec` | `KillSignal=SIGINT`, `KillMode=mixed`, `exec ros2 launch` |
| A node crashed, the unit still `active` | Launch keeps running when one process dies | `respawn=True` or `on_exit=Shutdown()` on that node |
| `on_exit=Shutdown()` fired, unit not restarted | Launch exits 0; `Restart=on-failure` treats that as clean | `Restart=always` |
| Restart limit never applies, or the unit warns about an unknown key | `StartLimitIntervalSec=` written in `[Service]` (ignored there) | Put it and `StartLimitBurst=` in `[Unit]` |
| Unit `failed` after a burst of restarts, never comes back | Start limit hit | Fix the cause; `systemctl reset-failed my-robot` |
| `Could not enable FIFO RT scheduling policy` only under systemd | `limits.conf` applies to logins, not services | `LimitRTPRIO=99`, `LimitMEMLOCK=infinity` in the unit |
| Nodes on the robot invisible from the laptop after boot, fine after restart | Stack started before the network was up | `Wants=`/`After=network-online.target` |
| Boot stalls about two minutes at network-online | A configured interface (unplugged Ethernet) never comes up | Mark it `optional: true` in netplan, or wait-online `--any` |
| `ros2 topic list` empty or stale over SSH | Shell lacks `env.sh`, or the CLI daemon kept old settings | `source /etc/my_robot/env.sh`; `ros2 daemon stop`; `--no-daemon` |
| Driver opens the wrong device after reboot | `/dev/ttyUSB*` numbering | udev link or `/dev/serial/by-id` in parameters |
| `Permission denied` on a device in the service only | Group added after the service started | Restart the service; check `id robot` |
| TF `extrapolation into the future` between computers | Clocks apart | chrony, one server per robot |
| `Detected jump back in time. Clearing TF buffer.` | Clock stepped while running | Sync before start (`chrony-wait`); keep `makestep 1 3` |
| Disk fills over weeks | ROS log files never removed | `tmpfiles.d` age; `hd_monitor.py` on the log disk |
| Journal shows `Suppressed N messages` | journald rate limit per service | Raise `RateLimitBurst` in a drop-in |
| Logs missing after a crash and reboot | Volatile journal, or logs in `/tmp` | `Storage=persistent`; `ROS_LOG_DIR=/var/log/my_robot` |
| Robot keeps moving after the stack stops | Driver leaves the last command in the motor controller | Firmware command timeout and safe stop: [arch-safety](../arch-safety/SKILL.md) |

## Checks

Before reporting the bringup done:

- The first power-on sequence passed, each step recorded with its numbers.
- `systemd-analyze verify` silent; `udevadm verify` silent for the rules file.
- Three reboots in a row: `systemctl is-active my-robot` is `active` and `wait_ready.py` exits 0
  each time; `systemd-analyze critical-chain my-robot.service` shows the expected waits.
- `systemctl stop` leaves no ROS process and no SIGKILL line in the journal.
- Killing one respawning node and one `Shutdown()` node recovers as designed.
- `/diagnostics_toplevel_state` is OK with everything running, and ERROR or STALE with a sensor
  unplugged.
- Clock offsets between computers within the chosen tolerance.
- The unit, env file, udev rules, chrony and journald snippets are committed in `host/` of the
  bringup package, matching what is installed (`diff` against `/etc`).

## Distro differences

- **Lyrical** (Ubuntu 26.04): chrony is the default time daemon, with NTS to Ubuntu's servers in
  `/etc/chrony/sources.d/ubuntu-ntp-pools.sources`; robot clients should drop those for the
  robot's server. `robot_upstart` has no Lyrical release (write the unit by hand).
  `RCL_LOGGING_IMPLEMENTATION=rcl_logging_noop` switches file logging off per process. Fast DDS 3
  reads `FASTDDS_DEFAULT_PROFILES_FILE` (Jazzy: `FASTRTPS_DEFAULT_PROFILES_FILE`). `ros2 launch`
  signal handling (launch 3.9) and the diagnostics API (4.4) behave as on Jazzy.
- **Humble** (Ubuntu 22.04, systemd 249): no `udevadm wait` (251) or `udevadm verify` (254) - use
  a small loop on `test -e` in `ExecStartPre`; no `RestartSteps`/`RestartMaxDelaySec` (254). Launch
  has no `respawn_max_retries` and `LifecycleNode` has no `autostart`. `ROS_LOCALHOST_ONLY`
  instead of `ROS_AUTOMATIC_DISCOVERY_RANGE`. `systemd-timesyncd` is the default time client, as
  on 24.04.

## Related

- References: [launch.md](references/launch.md), [systemd.md](references/systemd.md),
  [udev.md](references/udev.md), [readiness.md](references/readiness.md),
  [diagnostics.md](references/diagnostics.md), [time-sync.md](references/time-sync.md),
  [logs.md](references/logs.md), [first-power-on.md](references/first-power-on.md).
- Skills: [ros2-core](../ros2-core/SKILL.md), [ros2-control](../ros2-control/SKILL.md),
  [ros2-robot-description](../ros2-robot-description/SKILL.md), [nav-nav2](../nav-nav2/SKILL.md),
  [manip-moveit2](../manip-moveit2/SKILL.md), [perception-slam](../perception-slam/SKILL.md),
  [sim-gazebo](../sim-gazebo/SKILL.md), [ops-docker-ci](../ops-docker-ci/SKILL.md),
  [ros2-web-bridge](../ros2-web-bridge/SKILL.md) (remote monitoring), [ops-fleet](../ops-fleet/SKILL.md),
  [arch-safety](../arch-safety/SKILL.md), [arch-robot-architecture](../arch-robot-architecture/SKILL.md).
  Later: firmware and micro-ROS (Phase 5).
- Wiki: [ROS 2](../../wiki/tools/ros2.md), [colcon](../../wiki/tools/colcon.md),
  [ros2_control](../../wiki/software/ros2-control.md), [Nav2](../../wiki/software/nav2.md),
  [robot_localization](../../wiki/software/robot-localization.md), [tf2](../../wiki/software/tf2.md),
  [Fast DDS](../../wiki/software/fast-dds.md), [Cyclone DDS](../../wiki/software/cyclone-dds.md),
  [rmw_zenoh](../../wiki/software/rmw-zenoh.md), [Foxglove](../../wiki/tools/foxglove.md),
  [choose a deployment method](../../wiki/guides/choose-a-deployment-method.md).
- Upstream: systemd man pages (systemd.service, systemd.exec, systemd.kill, systemd.unit,
  tmpfiles.d, journald.conf, udev, udevadm); the `launch` and `launch_ros` `jazzy` branches;
  `ros/diagnostics` `ros2-jazzy`; the ROS 2 Jazzy docs (About Domain ID, About Logging);
  chrony's documentation; `clearpathrobotics/robot_upstart` `jazzy`.

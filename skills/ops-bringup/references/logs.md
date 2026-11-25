# Logs: the journal and the ROS log directory

Part of [ops-bringup](../SKILL.md). Checked against `journald.conf` and `tmpfiles.d` (systemd 255),
the ROS 2 Jazzy logging concept page, and launch 3.4's log handling.

## Where each line goes

| Source | Goes to | Bounded by default? |
|---|---|---|
| ROS log calls (`get_logger().info`, `RCLCPP_INFO`) | stderr → `ros2 launch` → the journal; and a file per process in `ROS_LOG_DIR` | Journal yes; files no |
| A node's stdout (`print`, `std::cout`) | The launch log file only, unless the node has `output='screen'` or `'both'` | No |
| `ros2 launch` itself | `ROS_LOG_DIR/<date>-<host>-<pid>/launch.log` and the journal | No |
| `/rosout` topic | Anyone subscribed (rqt_console, Foxglove, a bag) | — |

`ROS_LOG_DIR` defaults to `$ROS_HOME/log`, and `ROS_HOME` to `~/.ros`. The unit in
[systemd.md](systemd.md) sets `ROS_LOG_DIR=/var/log/my_robot` and creates it with
`LogsDirectory=my_robot`, owned by the robot user.

`RCUTILS_LOGGING_USE_STDOUT` chooses stderr (unset or 0) or stdout (1) for console output; it does
not turn file logging on or off.

## The journal

journald caps itself at 10 % of the file system (at most 4 GB) by default and stores logs on disk
when `/var/log/journal` exists. Set the robot's own limits in a drop-in:

```ini
# /etc/systemd/journald.conf.d/my-robot.conf
[Journal]
Storage=persistent        # keep logs across reboots, to read what happened before a crash
SystemMaxUse=2G           # example; size it to the disk
MaxRetentionSec=1month    # example; off (0) by default
RateLimitIntervalSec=30s  # default 30 s and 10000 messages per service, scaled up with free space
RateLimitBurst=20000      # example: a busy ROS stack is one service and can exceed the default
```

```bash
sudo systemctl restart systemd-journald
journalctl -u my-robot -b                  # this boot
journalctl -u my-robot -b -1 -e            # the end of the previous boot
journalctl -u my-robot -p warning --since "10 min ago"
journalctl -u 'my-robot*' -f               # all robot units, live
journalctl --disk-usage
```

A line such as `Suppressed 1234 messages from my-robot.service` means the rate limit dropped them;
raise it in the drop-in or per unit with `LogRateLimitIntervalSec=`/`LogRateLimitBurst=`.

## The ROS log directory

Nothing removes old ROS log files, and each process writes its own. Age them out with
systemd-tmpfiles, whose cleaning timer runs 15 minutes after boot and then daily:

```text
# /etc/tmpfiles.d/my-robot-logs.conf
# type  path              mode  user   group  age
d       /var/log/my_robot 0750  robot  robot  14d
```

```bash
sudo systemd-tmpfiles --create /etc/tmpfiles.d/my-robot-logs.conf
sudo systemd-tmpfiles --clean                 # run the cleanup now
du -sh /var/log/my_robot
```

The age (example: 14 days) is checked against access and modification times, so files still
being written stay.

Within one long run, a chatty node can still fill the disk, because the file logger does not
rotate. Options, per node:

- Lower the level: `ros_arguments=['--log-level', 'info']` (or `<node>:=warn`).
- Drop the file and keep the journal: `ros_arguments=['--disable-external-lib-logs']` (Jazzy). On
  Lyrical, `RCL_LOGGING_IMPLEMENTATION=rcl_logging_noop` in the environment does it per process.
- Keep the journal small and readable: `--disable-stdout-logs` for nodes whose output only
  matters in their file.

`hd_monitor.py` with `path: /var/log/my_robot` warns through diagnostics before the disk is full
([diagnostics.md](diagnostics.md)).

## Do not

- Rotate ROS logs with logrotate and a `postrotate` that sends SIGHUP: `ros2 launch` has no SIGHUP
  handler and exits, taking the robot down; ROS nodes do not reopen their files either.
- Point `ROS_LOG_DIR` at `/tmp` (robot_upstart's default): the system cleans `/tmp` on its own
  schedule (systemd-tmpfiles, or a tmpfs that empties at reboot), taking the logs of the crash you
  need.

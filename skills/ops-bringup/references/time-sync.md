# Clock sync across the robot's computers with chrony

Part of [ops-bringup](../SKILL.md). Checked against the chrony documentation (`chrony.conf`,
`chronyc`, `examples/chrony-wait.service`) and Ubuntu's chrony packaging for 24.04 (chrony 4.5)
and 26.04 (chrony 4.8). chrony is GPL-2.0; it is installed as a system package, not linked.

## Why it matters

Every message stamp, TF lookup and bag file compares clocks. Two computers a few hundred
milliseconds apart give `Lookup would require extrapolation into the future` in TF, drop messages
in time synchronizers, and record bags that do not line up. A clock that steps backwards while ROS
runs makes `tf2_ros` log `Detected jump back in time. Clearing TF buffer.`

What counts is that the robot's computers agree with each other. Real time matters less, and a
robot often has no internet at all.

## Ubuntu defaults

- **Ubuntu 24.04 (Jazzy):** `systemd-timesyncd` runs by default and can only be a client.
  `sudo apt install chrony` replaces it (both provide `time-daemon`). Config:
  `/etc/chrony/chrony.conf`, extra files in `/etc/chrony/conf.d/*.conf`, extra sources in
  `/etc/chrony/sources.d/*.sources`. The default file already has `makestep 1 3` and `rtcsync`.
- **Ubuntu 26.04 (Lyrical):** chrony is the default time daemon, with Ubuntu's NTS servers in
  `/etc/chrony/sources.d/ubuntu-ntp-pools.sources`. The same layout applies.

## One time server per robot

Pick the main computer (the one with the most uptime and, ideally, internet or a battery-backed
RTC). The others sync to it over the robot's network. Addresses below are documentation examples
(192.0.2.0/24); use the robot's own.

On the main computer:

```text
# /etc/chrony/conf.d/my-robot-server.conf
allow 192.0.2.0/24        # serve time to the robot's other computers
local stratum 10          # keep serving when no upstream source is reachable
```

Keep its upstream pools if it has internet; without them it serves its own clock, which is
enough for the computers to agree. Boards without a battery-backed RTC start from an old clock,
so log timestamps may be wrong in absolute terms; the robot still works.

On every other computer, use only the robot's server, so all clients follow one clock:

```text
# /etc/chrony/sources.d/my-robot.sources
server 192.0.2.10 iburst
```

Comment out the `pool` lines in `/etc/chrony/chrony.conf` (and, on 26.04, the
`ubuntu-ntp-pools.sources` file), then:

```bash
sudo systemctl restart chrony
chronyc sources -v          # the robot's server marked '*' (selected)
chronyc tracking            # 'Leap status : Normal', small 'System time' offset
```

Leave `makestep 1 3` as it is: chrony steps the clock only in its first three updates (at boot)
and slews it afterwards, so ROS never sees a jump while running. If a jump does happen later,
restart the stack rather than letting nodes carry stale TF.

## Start ROS after the clock is synced

`After=time-sync.target` in the robot unit does nothing until a service delays that target.
Ubuntu ships `chrony-wait.service` (waits until the remaining correction is under 0.1 s, at most
180 s) but does not enable it:

```bash
sudo systemctl enable chrony-wait.service       # on the client computers
```

On the main computer, without upstream sources, chrony-wait may wait the full 180 s; leave it
disabled there. The trade-off is a slower boot when the time server is down, against nodes that
start with a wrong clock.

## Check from ROS

`diagnostic_common_diagnostics`'s `ntp_monitor.py` queries an NTP server with `ntplib` and reports
the offset in `/diagnostics`: WARN above `--offset-tolerance` (default 500 µs), ERROR above
`--error-offset-tolerance` (default 5 s).

```python
Node(package='diagnostic_common_diagnostics', executable='ntp_monitor.py',
     arguments=['--ntp_hostname', '192.0.2.10', '--offset-tolerance', '5000', '--no-self-test'],
     parameters=[{'frequency': 0.2}])    # one query every 5 s (example)
```

Its `frequency` parameter defaults to 10 queries per second, so never point it at a public pool
with the default; on the robot's own server, lower it anyway. `--no-self-test` skips a second
check that queries the same server again. The 5 ms tolerance is an example; compare it with your
fastest sensor period.

## Sub-millisecond sync

Lidars and cameras that timestamp in hardware often use PTP (IEEE 1588). That needs a NIC with
hardware timestamping and `linuxptp` (`ptp4l`, `phc2sys`) configured with the sensor vendor's
guide; it is outside this skill.

## Traps

| Symptom | Cause | Fix |
|---|---|---|
| TF extrapolation errors only for data from one computer | That computer's clock is off | `chronyc tracking` on both; sync to one server |
| `chronyc sources` shows `?` or `x` for the robot's server | Server lacks `allow`, firewall blocks UDP 123, or wrong address | Add `allow`; open UDP 123 on the robot network |
| Offsets fine, but robot clocks are years off real time | No upstream source, no RTC | Acceptable for ROS; set the clock by hand or give the server internet once |
| Clock jumps hours after boot, TF buffer cleared | `makestep` with a negative limit, or someone ran `date -s` | Keep `makestep 1 3`; restart the stack after manual changes |
| Robot unit starts before the clock is synced | `chrony-wait.service` not enabled | Enable it on clients; keep `After=time-sync.target` |

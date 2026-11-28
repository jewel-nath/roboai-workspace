# CAN on Linux: SocketCAN, can-utils and python-can

Part of [fw-serial-can](../SKILL.md). Checked against the kernel `networking/can` docs and
`drivers/net/can/dev/netlink.c`, iproute2's `iplink_can.c`, systemd 255 `systemd.network` and
`systemd.link`, can-utils 2023.03 (Ubuntu 24.04) and python-can 4.3.1 (Ubuntu 24.04) and 4.6.1.

## Bring the interface up

```bash
sudo apt install can-utils python3-can
ip -details link show can0                      # driver, clock, timing limits, termination options
sudo ip link set can0 down                      # timing, mode and restart-ms change only while down
sudo ip link set can0 type can bitrate 500000 restart-ms 100
sudo ip link set can0 txqueuelen 1000
sudo ip link set can0 up
ip -details -statistics link show can0
```

- `bitrate` lets the kernel compute the bit timing (CiA sample points by default); add
  `sample-point 0.875` to match MCU nodes, or set `tq`, `prop-seg`, `phase-seg1`, `phase-seg2`,
  `sjw` by hand.
- `restart-ms 100` restarts the controller 100 ms after bus-off; the default 0 leaves it off until
  `ip link set can0 type can restart`. A restart creates an error frame.
- `txqueuelen 1000` is the value the ros2_canopen docs use; the default queue (10) overflows when
  a node sends bursts, and `write()` fails with `ENOBUFS`.
- CAN FD: `sudo ip link set can0 up type can bitrate 500000 sample-point 0.8 dbitrate 2000000
  dsample-point 0.75 fd on` (example rates; every node must match). The MTU becomes 72.
- Switchable termination: `sudo ip link set dev can0 type can termination 120` (or `0`).
- Adapters: candleLight/gs_usb (`gs_usb`), PEAK (`peak_usb`), MCP2515 HATs (`mcp251x`, device-tree
  overlay), SoC controllers (device tree). Check `dmesg` for the driver and `ip link` for the name.
- Serial-line (SLCAN) adapters: `sudo slcand -o -c -s6 /dev/ttyACM0 can0 && sudo ip link set can0 up`
  (`-s6` selects 500 kbit/s; from can-utils).

### At boot

With systemd-networkd running (`systemctl is-active systemd-networkd`; Ubuntu Server runs it under
netplan). Without it, put the `ip` commands above in a oneshot systemd unit instead.

```ini
# /etc/systemd/network/80-can0.network
[Match]
Name=can0

[CAN]
BitRate=500K
SamplePoint=87.5%
RestartSec=100ms
# FD: DataBitRate=2M  DataSamplePoint=75%  FDMode=yes
# Termination=120     # adapters with a switchable resistor
```

```ini
# /etc/systemd/network/80-can0.link  (TX queue; applied when the device appears)
[Match]
OriginalName=can0

[Link]
TransmitQueueLength=1000
```

`sudo systemctl restart systemd-networkd`, replug or reboot, then `networkctl status can0` and
`ip -details link show can0`. A unit that needs the bus can wait with
`ExecStartPre=/usr/bin/udevadm wait --timeout=30 /sys/class/net/can0`
([ops-bringup](../../ops-bringup/SKILL.md)).

## can-utils

| Command | Does |
|---|---|
| `candump -td -x can0` | Print frames with the time since the previous one and RX/TX marks |
| `candump can0,701:7FF` | Only ID 0x701 (filter `id:mask`, hex) |
| `candump -e can0,0:0,#FFFFFFFF` | All data frames plus error frames, decoded |
| `candump -l can0` | Log to `candump-<date>.log`; replay with `canplayer -I <file>` |
| `candump -n 10 -T 2000 can0` | Stop after 10 frames or after 2 s without one (scripted checks) |
| `cansend can0 123#11223344` | One 11-bit frame; 8 hex digits for the ID make it 29-bit |
| `cansend can0 123##1112233` | One CAN FD frame, flags 0x1 (bit rate switch), payload 11 22 33 |
| `cangen can0 -g 10 -I 100 -L 8` | Generate a frame every 10 ms on ID 0x100 with 8 random bytes |
| `canbusload can0@500000 -r -b` | Bus load per interface, bar graph (the bitrate is required) |
| `cansniffer can0` | Live view of changing bytes per ID |

Error counters and state: `ip -details -statistics link show can0` (`berr-counter tx N rx N`,
`bus-errors`, `error-warn`, `error-pass`, `bus-off`).

## python-can

`can.Bus(channel="can0", interface="socketcan")`; pass `fd=True` for CAN FD. `bustype=` still works
but is deprecated since 4.2. Rules that save time:

- `can.Message` defaults to `is_extended_id=True`. Pass `is_extended_id=False` for 11-bit IDs
  (CANopen and most motor drives).
- `bus.recv(timeout)` returns `None` on timeout; never call it without a timeout in a control loop.
- `bus.set_filters([{"can_id": 0x581, "can_mask": 0x7FF, "extended": False}])` filters in the
  kernel; Python then sees only what it needs.
- Error frames arrive as messages with `is_error_frame=True` unless the bus is created with
  `ignore_rx_error_frames=True`.
- `bus.send_periodic(msg, 0.01)` hands a cyclic frame to the kernel's broadcast manager; keep the
  returned task and `stop()` it.
- Use `with can.Bus(...) as bus:` or call `bus.shutdown()`.

### `can_probe.py`: list CANopen heartbeats, read an object over SDO

```python
#!/usr/bin/env python3
"""List CANopen heartbeats on a bus, or read one object with an expedited SDO upload."""
import argparse
import struct
import time

import can

NMT_STATES = {0x00: "boot-up", 0x04: "stopped", 0x05: "operational", 0x7F: "pre-operational"}


def heartbeats(bus: can.BusABC, seconds: float) -> None:
    bus.set_filters([{"can_id": 0x700, "can_mask": 0x780, "extended": False}])
    seen: dict[int, list[tuple[float, int]]] = {}
    end = time.monotonic() + seconds
    while (left := end - time.monotonic()) > 0:
        msg = bus.recv(timeout=left)
        if msg is None or msg.is_error_frame or msg.dlc < 1:
            continue
        seen.setdefault(msg.arbitration_id - 0x700, []).append((msg.timestamp, msg.data[0]))
    for node, beats in sorted(seen.items()):
        gaps = [b[0] - a[0] for a, b in zip(beats, beats[1:])]
        mean = f"{1000 * sum(gaps) / len(gaps):.1f} ms" if gaps else "-"
        state = NMT_STATES.get(beats[-1][1] & 0x7F, hex(beats[-1][1]))
        print(f"node {node}: {state}, {len(beats)} heartbeats, mean period {mean}")


def sdo_read(bus: can.BusABC, node: int, index: int, sub: int, timeout: float) -> bytes:
    bus.set_filters([{"can_id": 0x580 + node, "can_mask": 0x7FF, "extended": False}])
    request = bytes([0x40, index & 0xFF, index >> 8, sub, 0, 0, 0, 0])  # initiate upload
    bus.send(can.Message(arbitration_id=0x600 + node, data=request, is_extended_id=False))
    end = time.monotonic() + timeout
    while (left := end - time.monotonic()) > 0:
        msg = bus.recv(timeout=left)
        if msg is None or msg.dlc < 8 or bytes(msg.data[1:4]) != request[1:4]:
            continue
        cmd = msg.data[0]
        if cmd == 0x80:
            raise RuntimeError(f"SDO abort 0x{struct.unpack_from('<I', msg.data, 4)[0]:08X}")
        if cmd & 0xE2 != 0x42:
            raise RuntimeError("segmented transfer: not handled by this probe")
        size = 4 - ((cmd >> 2) & 0x3) if cmd & 0x1 else 4
        return bytes(msg.data[4:4 + size])
    raise TimeoutError(f"no SDO reply from node {node}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--channel", default="can0")
    ap.add_argument("--seconds", type=float, default=5.0)
    ap.add_argument("--sdo", nargs=3, metavar=("NODE", "INDEX", "SUB"),
                    help="e.g. 2 0x1000 0 (device type)")
    a = ap.parse_args()
    with can.Bus(channel=a.channel, interface="socketcan") as bus:
        if a.sdo:
            node, index, sub = (int(v, 0) for v in a.sdo)
            data = sdo_read(bus, node, index, sub, timeout=0.5)
            print(f"node {node} 0x{index:04X}:{sub} = {data.hex(' ')} "
                  f"(u32 LE {int.from_bytes(data, 'little')})")
        else:
            heartbeats(bus, a.seconds)


if __name__ == "__main__":
    main()
```

`python3 can_probe.py` lists every node's NMT state and heartbeat period;
`python3 can_probe.py --sdo 2 0x1000 0` reads node 2's device type (CiA 402 drives report profile
402, 0x192, in the low 16 bits). Frame layouts are in [canopen.md](canopen.md).

## SocketCAN from C or C++

For a plugin or node that talks raw CAN (when no ROS package fits):

- `socket(PF_CAN, SOCK_RAW, CAN_RAW)`, look up the index with `SIOCGIFINDEX` (or
  `if_nametoindex()`), `bind()` to a `sockaddr_can`.
- Use `can_frame.len`; `can_dlc` is the deprecated name for the same byte.
- CAN FD: enable `CAN_RAW_FD_FRAMES` with `setsockopt` before reading or writing `canfd_frame`;
  without it only classic frames pass. Check the interface MTU (72) first.
- Filters (`CAN_RAW_FILTER`) and the error mask (`CAN_RAW_ERR_FILTER`) run in the kernel; error
  frames carry `CAN_ERR_FLAG` in `can_id`.
- Read with `poll()` and a timeout inside `read()` of a ros2_control plugin; one bounded exchange
  per cycle, as for serial ([serial-motor-bus.md](serial-motor-bus.md)).

## A ROS 2 bridge for raw frames

`sudo apt install ros-jazzy-ros2-socketcan` (1.4.0 on Jazzy and Lyrical), then
`ros2 launch ros2_socketcan socket_can_bridge.launch.xml interface:=can0`: frames from the bus on
`/from_can_bus`, frames to send on `/to_can_bus` (`can_msgs/msg/Frame`; with
`enable_can_fd:=true` they are `from_can_bus_fd` and `to_can_bus_fd`,
`ros2_socketcan_msgs/msg/FdFrame`). The nodes are lifecycle nodes that the launch file configures
and activates. Useful for logging and tools; a control loop should own its socket instead.

Sources: kernel.org `Documentation/networking/can.rst` and `drivers/net/can/dev/netlink.c`;
iproute2 `ip/iplink_can.c`; systemd 255 man pages `systemd.network` ([CAN] section) and
`systemd.link` (`TransmitQueueLength=`); can-utils `candump.c`, `cansend.c`, `canbusload.c`,
README (tag v2023.03 and master); python-can docs `interfaces/socketcan`, `bus.py`, `message.py`
(4.3.1 and main); ros2_canopen manual "Setup CAN controller"; ros2_socketcan 1.4.0 launch files;
rosdistro `jazzy` and `lyrical` distribution files.

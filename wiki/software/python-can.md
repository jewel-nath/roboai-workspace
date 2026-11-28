---
type: tool
name: python-can
summary: The standard Python CAN library; one Bus API over SocketCAN, slcan, candleLight (gs_usb), PCAN, Kvaser, Vector and other adapters, with listeners, log files and replay; the quick way to test a CAN device before writing a ROS 2 driver.
tags: [can, python, python-can, socketcan, slcan, gs-usb, pcan, can-fd, logging, cantools]
kind: library
area: firmware
support:
license: LGPL-3.0-only
links: {repo: "https://github.com/hardbyte/python-can", docs: "https://python-can.readthedocs.io/en/stable/", site: "https://pypi.org/project/python-can/"}
version: {tested: , latest: 4.6.1, as_of: 2026-11-27}
platforms: [linux, windows, macos]
agent_access: script
registry:
evidence: researched
last_verified: 2026-11-27
sources:
  - {url: "https://github.com/hardbyte/python-can", title: "python-can repository: README, LICENSE.txt, pyproject.toml, changelog and SocketCAN source (main and v4.6.1)", accessed: 2026-11-27}
  - {url: "https://pypi.org/project/python-can/", title: "PyPI: python-can", accessed: 2026-11-27}
  - {url: "https://python-can.readthedocs.io/en/stable/", title: "python-can 4.6.1 docs: SocketCAN, configuration, gs_usb, notifier and listeners", accessed: 2026-11-27}
  - {url: "https://packages.ubuntu.com/noble/python3-can", title: "Ubuntu 24.04 package: python3-can", accessed: 2026-11-27}
  - {url: "https://github.com/hardbyte/python-can/issues/2121", title: "python-can issue 2121: slcan on Windows loses frames on 4.6.1", accessed: 2026-11-27}
---

# python-can

python-can gives Python one `can.Bus` API over SocketCAN, slcan serial adapters, candleLight
(`gs_usb`), PCAN, Kvaser, Vector, IXXAT and other adapters, with listeners, periodic sending, log
files (can-utils `.log`, ASC, BLF, MF4, TRC, CSV, SQLite) and CLI tools [1]. LGPL-3.0-only [1]:
scripts may use it freely; shipping a modified copy means publishing the changed library source.

## When to use it

- Testing a CAN motor or sensor from a laptop before writing a driver: send a command, check the
  reply and scaling, log a run, then move the frame layout into a C++
  [ros2_control](ros2-control.md) hardware interface. cantools adds DBC decoding on top.
- Windows or macOS hosts, which lack SocketCAN and [can-utils](../tools/can-utils.md) [1]. CiA 402
  drives: [ros2_canopen](ros2-canopen.md); your own CANopen node: [CANopenNode](canopennode.md).

## Setup

Newest release 4.6.1 (2025-08-12), Python 3.9+ [2]; `main` (2026-11-27) has unreleased fixes and
needs Python 3.11 [1]. Ubuntu 24.04's apt `python3-can` is 4.3.1 [4], before slcan CAN FD (4.6) [1].

```bash
python3 -m venv ~/canenv && . ~/canenv/bin/activate
pip install "python-can[serial]"      # slcan; [gs-usb] for candleLight on Windows or macOS
python -m can.viewer -i socketcan -c vcan0            # live table of IDs
python -m can.logger -i socketcan -c can0 -f run.log  # can-utils format, replayable
```

```python
import can
with can.Bus(interface="socketcan", channel="can0") as bus:   # shut down on exit
    bus.send(can.Message(arbitration_id=0x123, data=[1, 2, 3], is_extended_id=False))
    reply = bus.recv(timeout=0.5)                             # None on timeout
```

## How an agent works with it

Test on `vcan0` first with `receive_own_messages=True`, then on the bus; assert on `recv(timeout)`
[1]. `can.Notifier(bus, [can.Printer(), can.Logger("run.asc")])` feeds listeners from a thread or
asyncio loop; `CAN_INTERFACE`, `CAN_CHANNEL`, `CAN_BITRATE`, `CAN_CONFIG` or `~/can.conf` keep
adapter details out of scripts [3]. Skill: [fw-serial-can](../../skills/fw-serial-can/SKILL.md).

## Traps

- **`bitrate=` ignored on SocketCAN.** `SocketcanBus` has no bitrate parameter and swallows extra
  arguments; the bus runs at whatever `ip link` set [1][3]. gs_usb takes only fixed rates [3].
- **Error frames and FD.** SocketCAN buses deliver error frames (check `msg.is_error_frame`) unless
  you pass `ignore_rx_error_frames=True`; CAN FD frames need `fd=True` [1].
- **`Failed to transmit: No buffer space available`.** 4.6.1 raises `CanOperationError` when a
  burst fills the queue; `main` retries [1]. Raise `txqueuelen`, pace sends, or use
  `send_periodic`, which hands cyclic frames to the kernel on SocketCAN [3].
- **slcan on Windows drops frames under load in 4.6.1**, though Linux got every frame in the same
  test; the fix is on `main`, unreleased on 2026-11-27 [5].
- **gs_usb on Windows** in 4.6.1 needs the device switched to libusbK, for example with Zadig;
  gs_usb devices also cannot filter messages [3].

## Alternatives

[can-utils](../tools/can-utils.md) on Linux; PCAN-Basic or Kvaser CANlib; `ros2_socketcan`.

## Sources

1. [python-can repository: README, LICENSE.txt, pyproject.toml, changelog and SocketCAN source (main and v4.6.1)](https://github.com/hardbyte/python-can), accessed 2026-11-27
2. [PyPI: python-can](https://pypi.org/project/python-can/), accessed 2026-11-27
3. [python-can 4.6.1 docs: SocketCAN, configuration, gs_usb, notifier and listeners](https://python-can.readthedocs.io/en/stable/), accessed 2026-11-27
4. [Ubuntu 24.04 package: python3-can](https://packages.ubuntu.com/noble/python3-can), accessed 2026-11-27
5. [python-can issue 2121: slcan on Windows loses frames on 4.6.1](https://github.com/hardbyte/python-can/issues/2121), accessed 2026-11-27

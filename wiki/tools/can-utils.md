---
type: tool
name: can-utils and SocketCAN
summary: The Linux kernel's CAN networking layer (SocketCAN) and its standard command-line tools (candump, cansend, cangen, canbusload, slcand); the first thing to run when bringing up or debugging a robot's CAN bus.
tags: [can, socketcan, can-utils, candump, cansend, can-fd, vcan, gs-usb, candlelight, slcan, usb-can, linux]
kind: tool
area: firmware
support: documented
license: "(GPL-2.0-only OR BSD-3-Clause) AND GPL-2.0-only AND LGPL-2.0-only"
links: {repo: "https://github.com/linux-can/can-utils", docs: "https://docs.kernel.org/networking/can.html", site: }
version: {tested: , latest: v2025.01, as_of: 2026-11-27}
platforms: [linux]
agent_access: cli
registry:
evidence: researched
last_verified: 2026-11-27
sources:
  - {url: "https://github.com/linux-can/can-utils", title: "can-utils README, LICENSES and SPDX file headers", accessed: 2026-11-27}
  - {url: "https://docs.kernel.org/networking/can.html", title: "Linux kernel docs: SocketCAN", accessed: 2026-11-27}
  - {url: "https://packages.ubuntu.com/noble/can-utils", title: "Ubuntu 24.04 package: can-utils", accessed: 2026-11-27}
  - {url: "https://github.com/candle-usb/candleLight_fw", title: candleLight_fw README, accessed: 2026-11-27}
  - {url: "https://github.com/CANopenNode/CANopenLinux", title: "CANopenLinux README: CAN interfaces", accessed: 2026-11-27}
  - {url: "https://ros-industrial.github.io/ros2_canopen/manual/rolling/quickstart/operation.html", title: "ros2_canopen manual: setup CAN controller", accessed: 2026-11-27}
  - {url: "https://www.ni.com/en/support/documentation/supplemental/09/can-physical-layer-and-termination-guide.html", title: "NI: CAN physical layer and termination guide", accessed: 2026-11-27}
---

# can-utils and SocketCAN

SocketCAN is the Linux kernel's CAN layer: each adapter is a network interface such as `can0`, set
up with `ip link` [2]. can-utils is its toolbox: `candump`, `cansend`, `cangen`, `canbusload`,
`slcand`, ISO-TP and J1939 tools [1]. Licences differ per file: core tools GPL-2.0-only or
BSD-3-Clause, your choice; `slcand`, `canfdtest` and the J1939 tools GPL-2.0-only; ISOBus tools
LGPL-2.0-only [1]. A robot image that ships the GPL binaries must offer their source.

## When to use it

- First contact with a CAN device on Linux: set the bitrate, watch frames, send one, record with
  `candump -l` for `canplayer` [1]; skill: [fw-serial-can](../../skills/fw-serial-can/SKILL.md).
- Scripts, or Windows and macOS hosts: [python-can](../software/python-can.md). CANopen:
  [CANopenNode](../software/canopennode.md) and [ros2_canopen](../software/ros2-canopen.md).

## Setup

Ubuntu 24.04 ships 2023.03 [3]; upstream's newest tag is v2025.01, last commit 2026-10-14 [1].

```bash
sudo apt install can-utils
sudo ip link set can0 up type can bitrate 500000 restart-ms 100   # classic CAN, set while down
sudo ip link set can0 up type can bitrate 500000 dbitrate 4000000 fd on   # or CAN FD [2]
sudo ip link set can0 txqueuelen 1000
sudo modprobe vcan && sudo ip link add dev vcan0 type vcan && sudo ip link set vcan0 up  # tests
```

**Adapters.** candleLight boards (CANable 1.x, CANtact, other STM32F042 or F072 designs) use the
mainline `gs_usb` driver; STM32F103 boards cannot run it [4]. PEAK uses `peak_usb` [6]. For slcan
run `sudo slcand -f -o -c -s5 /dev/ttyACM0 can0` (`-s5` is 250 kbit/s), then bring `can0` up [5].

## How an agent works with it

- `ip -details -statistics link show can0`: state (ERROR-ACTIVE to BUS-OFF), bitrate, counters;
  MTU 72 means FD is on [2]. `cangen vcan0` makes traffic; `canbusload can0@500000 -r -t -b` [1].
- `candump -td -e can0,0:0,#FFFFFFFF` adds readable error frames; `candump -n 1 -T 1000 can0`
  stops after one frame or 1 s; `cansend can0 123#DEADBEEF`, FD `cansend can0 123##1DEADBEEF` [1].

## Traps

- **Termination.** One 120 Ω resistor at each end, none between [7]; powered off, CAN_H to CAN_L
  then reads about 60 Ω. Adapters and drives often have a termination jumper: count them.
- **Bitrate mismatch** shows as error frames and rising error counters: every node needs the same
  bitrate. At 1 Mbit/s keep the bus near 40 m at most; NI's general stub limit is 1 m [7], and the
  ISO 11898 figure at 1 Mbit/s is 0.3 m ([wiring](../../skills/fw-serial-can/references/wiring.md)).
- **Bus-off** stops all traffic until `restart-ms` or `ip link set can0 type can restart` [2].
- **ENOBUFS, "No buffer space available"**: the writer outruns the bus; the kernel's example
  queue holds 10 frames [2]. Set `txqueuelen 1000`, as ros2_canopen does [6], and pace sends.
- **Cheap adapters and CAN FD.** slcan may lose frames under load [5]; `gs_usb` candleLight boards
  are better but classic-only, as mainline firmware lacks the STM32G0B1 and G431 boards [4]. For FD,
  pick an adapter whose Linux driver supports it and check that `fd on` took [2].

## Alternatives

[python-can](../software/python-can.md); SavvyCAN or Wireshark as GUIs; `ros2_socketcan` for ROS 2.

## Sources

1. [can-utils README, LICENSES and SPDX file headers](https://github.com/linux-can/can-utils), accessed 2026-11-27
2. [Linux kernel docs: SocketCAN](https://docs.kernel.org/networking/can.html), accessed 2026-11-27
3. [Ubuntu 24.04 package: can-utils](https://packages.ubuntu.com/noble/can-utils), accessed 2026-11-27
4. [candleLight_fw README](https://github.com/candle-usb/candleLight_fw), accessed 2026-11-27
5. [CANopenLinux README: CAN interfaces](https://github.com/CANopenNode/CANopenLinux), accessed 2026-11-27
6. [ros2_canopen manual: setup CAN controller](https://ros-industrial.github.io/ros2_canopen/manual/rolling/quickstart/operation.html), accessed 2026-11-27
7. [NI: CAN physical layer and termination guide](https://www.ni.com/en/support/documentation/supplemental/09/can-physical-layer-and-termination-guide.html), accessed 2026-11-27
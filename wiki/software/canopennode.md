---
type: tool
name: CANopenNode
summary: Apache-2.0 CANopen protocol stack in C for microcontrollers and Linux (CiA 301 with LSS, gateway and safety objects), with CANopenEditor for the object dictionary and EDS file; for making your own board a CANopen joint, sensor or I/O node.
tags: [canopen, can, cia301, object-dictionary, eds, canopeneditor, canopenlinux, stm32, zephyr, firmware]
kind: library
area: firmware
support:
license: Apache-2.0
links: {repo: "https://github.com/CANopenNode/CANopenNode", docs: "https://canopennode.github.io", site: }
version: {tested: , latest: v4.1, as_of: 2026-11-27}
platforms: [linux, windows]
agent_access: cli
registry:
evidence: researched
last_verified: 2026-11-27
sources:
  - {url: "https://github.com/CANopenNode/CANopenNode", title: "CANopenNode README, LICENSE, doc/deviceSupport.md, CANopen.h, 301/CO_driver.h and example OD files", accessed: 2026-11-27}
  - {url: "https://github.com/CANopenNode/CANopenLinux", title: CANopenLinux README, accessed: 2026-11-27}
  - {url: "https://github.com/CANopenNode/CANopenEditor", title: "CANopenEditor README, LICENSE and EDSSharp CLI", accessed: 2026-11-27}
  - {url: "https://github.com/CANopenNode/CanOpenSTM32", title: CANopenSTM32 README and LICENSE, accessed: 2026-11-27}
  - {url: "https://github.com/zephyrproject-rtos/CANopenNodeZephyr", title: "CANopenNodeZephyr README, Kconfig and submodule pin", accessed: 2026-11-27}
  - {url: "https://github.com/CANopenNode/CANopenNode/issues", title: CANopenNode issue tracker, accessed: 2026-11-27}
---

# CANopenNode

CANopenNode is a CANopen stack in ANSI C for 16-bit and larger MCUs and Linux, bare metal or on an
RTOS: CiA 301 (NMT, heartbeat, PDO, SDO, EMCY, SYNC, TIME), LSS (CiA 305), the CiA 309-3 gateway
and CANopen Safety (CiA 304) [1]. Builders use it to make their own board a CANopen node. It is
Apache-2.0, so closed firmware may link it if the licence and notices ship along [1].

## When to use it

- A robot needs CANopen when its drives speak it (CiA 402 drives ship an EDS file); their ROS 2
  master is [ros2_canopen](ros2-canopen.md). Other drives: plain CAN, [python-can](python-can.md).
- CANopenNode is for your own board on such a bus. It has no CiA 402 profile [1]: a drive built
  on it needs the 0x6040 and 0x6041 objects and the drive state machine written by you.

## Setup

The repo holds only the stack; each target needs a driver behind `301/CO_driver.h`. Ports:
CANopenLinux (SocketCAN, master features), CanOpenSTM32 (MIT, bxCAN and FDCAN via ST's HAL [4]),
CANopenPIC, ADI MAX32662 and MAX32690, Zephyr, Mbed; the smallest example, a dsPIC30F4011 with 4
TPDOs and 4 RPDOs, needs under 2 kB RAM [1]. Tag v4.1 (2025-11-22); last commit 2026-07-10 by the
author, Janez Paternoster; 96 open issues, some recent ones unanswered [1][6]. On Linux [2]:

```bash
git clone --recurse-submodules https://github.com/CANopenNode/CANopenLinux && cd CANopenLinux
make && sudo make install                                  # installs canopend
sudo modprobe vcan && sudo ip link add dev can0 type vcan && sudo ip link set up can0
canopend can0 -i 4 -c "stdio"    # node 4; then type: 4 read 0x1018 1 u32
candump -td can0                 # other terminal: boot-up and heartbeat on 0x704
```

**Object dictionary.** CANopenEditor (GPL-3.0, a Windows GUI on .NET 8; the cross-platform GUI2 is
unfinished) imports and exports EDS, DCF and XDD and writes `OD.h` and `OD.c` [3].

## How an agent works with it

- Keep the XDD project as the source; regenerate `OD.c` (never hand-edit it) with
  `EDSSharp --infile joint.xdd --outfile OD.c --type CanOpenNodeV4`; ship the `.eds` [3][1].
- `canopend can0 -i 1 -c "local-/tmp/CO_command_socket"` plus `cocomm` sends commands such as
  `4 read 0x1017 0 u16` [2]; heartbeats sit at 0x700 + ID, SDO replies at 0x580 + ID [1].

## Traps

- **Node IDs.** 1 to 127, unique per bus; 0xFF means unconfigured, with PDOs off [1]. COB-IDs are
  base + ID, so two nodes with one ID collide. `canopend` without `-i` waits for LSS [2].
- **Zephyr's integration is old.** CANopenNodeZephyr pins a 2020, pre-v4 stack, off in CAN FD mode
  [5]; V4 `OD.c` files `#error` on it [1], so use the older `CanOpenNode` exporter [3].
- **Emergency on the first `canopend` start**: storage files are missing. Save with
  `4 write 0x1010 1 vs save` (node 4) and restart; give each instance its own storage path [2].
- **Bus-off on STM32.** Enable automatic bus-off recovery (bxCAN) or protocol exception handling
  (FDCAN) in CubeMX, plus RX and TX interrupts and a 1 ms timer interrupt [4].
- **Threads.** The real-time thread typically runs every 1 ms [1]; with several threads, wrap
  application access to the dictionary in `CO_LOCK_OD` and `CO_UNLOCK_OD` [2].

## Alternatives

Lely CANopen (lely-core), under [ros2_canopen](ros2-canopen.md); commercial stacks.

## Sources

1. [CANopenNode README, LICENSE, doc/deviceSupport.md, CANopen.h, 301/CO_driver.h and example OD files](https://github.com/CANopenNode/CANopenNode), accessed 2026-11-27
2. [CANopenLinux README](https://github.com/CANopenNode/CANopenLinux), accessed 2026-11-27
3. [CANopenEditor README, LICENSE and EDSSharp CLI](https://github.com/CANopenNode/CANopenEditor), accessed 2026-11-27
4. [CANopenSTM32 README and LICENSE](https://github.com/CANopenNode/CanOpenSTM32), accessed 2026-11-27
5. [CANopenNodeZephyr README, Kconfig and submodule pin](https://github.com/zephyrproject-rtos/CANopenNodeZephyr), accessed 2026-11-27
6. [CANopenNode issue tracker](https://github.com/CANopenNode/CANopenNode/issues), accessed 2026-11-27

---
name: fw-serial-can
description: Build and check the wire between boards and a ROS 2 Jazzy computer - framed UART and RS-485 links (COBS, CRC-16, sequence numbers, timeouts)
  under a ros2_control hardware interface, serial ports on Linux (udev names, dialout, pyserial, FTDI latency), CAN and CAN FD with SocketCAN, can-utils
  and python-can, CANopen with CANopenNode and ros2_canopen CiA 402 drives, termination, ground and bitrate checks, and where EtherCAT fits.
license: Apache-2.0
metadata:
  sources: []
  evidence: researched
  last_verified: 2026-11-27
---

# Serial and CAN links

Lets an agent design, bring up and prove the link between a motor or sensor board and the robot
computer: a framed serial protocol, a SocketCAN bus, or a CANopen drive under ros2_control. Checked
on 2026-11-27 against the kernel SocketCAN docs, iproute2, can-utils 2023.03 and python-can 4.3.1
(Ubuntu 24.04), pyserial 3.5, CANopenNode v4 and ros2_canopen 0.3.4 (Jazzy); recipes not run.

## When to use

- Designing or debugging the byte protocol between an MCU and a Linux node over UART, USB or RS-485.
- Writing the bus layer under a ros2_control plugin for a serial motor board.
- A serial port that changes name, refuses permission, or answers 16 ms late.
- Bringing up `can0`, testing a device with `candump`, `cansend` and python-can, bus-off.
- A CANopen device in firmware (CANopenNode), or a CiA 402 servo drive through ros2_canopen.
- Checking wiring: termination, ground, stubs, bitrate and sample point. Judging EtherCAT.

Not here: boards, toolchains, UART and CAN peripheral setup, DMA and watchdogs
([fw-mcu](../fw-mcu/SKILL.md)); micro-ROS transports ([fw-rtos-micro-ros](../fw-rtos-micro-ros/SKILL.md));
controllers and the plugin skeleton ([ros2-control](../ros2-control/SKILL.md)); udev and systemd
([ops-bringup](../ops-bringup/SKILL.md)); stop chains ([arch-safety](../arch-safety/SKILL.md)).
Later batches: I2C, SPI and sensor drivers (`fw-peripherals`, `fw-drivers`), motor control, FOC and
encoders (`fw-motor-control`), PID (`control-systems`).

## Quick start

A CAN loop on one Linux machine, no hardware:

```bash
sudo apt install can-utils python3-can
sudo modprobe vcan
sudo ip link add dev vcan0 type vcan && sudo ip link set up vcan0
candump -td -x vcan0 &                  # delta timestamps, RX/TX marks
cansend vcan0 123#DEADBEEF              # 11-bit ID 0x123, 4 data bytes
python3 -c 'import can
with can.Bus(channel="vcan0", interface="socketcan") as bus:
    bus.send(can.Message(arbitration_id=0x123, data=[1, 2, 3], is_extended_id=False))'
```

A real adapter (USB-CAN, CAN HAT or SoC controller), interface down while you set it:

```bash
sudo ip link set can0 down
sudo ip link set can0 type can bitrate 500000 restart-ms 100   # example bitrate: match the devices
sudo ip link set can0 up
ip -details -statistics link show can0      # state ERROR-ACTIVE, berr-counter tx 0 rx 0
```

Serial boards: the frame format and shared C code are in
[serial-protocol.md](references/serial-protocol.md), the MCU loop in
[serial-firmware.md](references/serial-firmware.md); test the link with `serial_link_test.py` from
[serial-link-test.md](references/serial-link-test.md).

## Workflow

1. **Choose the link and write its spec down.** UART over USB for one board next to the computer;
   RS-485 for several boards on one pair (one master polls, one talker at a time); CAN for several
   nodes with hardware arbitration and error handling (8 bytes per frame, CAN FD 64); CANopen when
   the devices are off-the-shelf drives (CiA 402) or I/O; EtherCAT only for many axes with sub-ms
   cycles ([ethercat.md](references/ethercat.md)). Record bitrate or baud, node IDs, message IDs,
   byte order, periods, timeouts, which nodes terminate, and what stops the motors when the link dies.
   *Check:* the spec is in the project repo, and every motor-driving message has a timeout owner.

2. **Wire it and measure before power.** CAN: one twisted pair, 120 Ω at the two far ends only,
   short stubs, transceiver grounds joined. RS-485: same idea, plus fail-safe bias where the
   transceivers lack it. UART: TX to RX, common ground, same logic level. Bus, connector and
   measurement details: [wiring.md](references/wiring.md).
   *Check:* power off, CANH to CANL reads about 60 Ω (120 Ω means one terminator, about 40 Ω means
   three); after power-up the controller stays `ERROR-ACTIVE` with zero bus errors.

3. **Frame the serial protocol.** COBS frames ending in 0x00, each `[seq][type][payload][CRC-16]`;
   fields packed byte by byte, little-endian, never a `memcpy` of a struct. CRC-16/CCITT-FALSE
   (check value 0x29B1). The reply echoes `seq`; the host drops replies with another one. The host
   waits less than one control period; the firmware stops the motors and latches disabled when no
   valid command arrives within its timeout (example 100 ms). Budget bytes: 8N1 costs 10 bit times
   per byte, so 115200 baud moves about 11.5 bytes per ms. Shared C code and test vectors are in
   [serial-protocol.md](references/serial-protocol.md), the MCU loop in
   [serial-firmware.md](references/serial-firmware.md).
   *Check:* the CRC and COBS vectors pass on the MCU and on the host.

4. **Open the port properly on Linux.** A stable name (`/dev/serial/by-id/...` or a udev link such as
   `/dev/my_robot_mcu`), the user in `dialout`, ModemManager kept off CDC-ACM ports, the FTDI latency
   timer at 1 ms, exclusive raw access, input flushed after open. Rules and a POSIX port class are
   in [serial-linux.md](references/serial-linux.md), the pyserial tester in
   [serial-link-test.md](references/serial-link-test.md).
   *Check:* `serial_link_test.py --port /dev/my_robot_mcu` runs 60 s at the control rate with zero
   CRC errors and lost replies, and its p99 round trip is under the host timeout.

5. **Put the link under ros2_control.** Implement the `MotorBus` seam the
   [ros2-control](../ros2-control/SKILL.md) plugin calls: `write()` makes one bounded exchange
   (velocities out, state back), `read()` uses that reply or polls while the component is inactive,
   a few consecutive misses return `false` so the component errors and its controllers stop. No
   retries or sleeps in the loop. Code: [serial-motor-bus.md](references/serial-motor-bus.md).
   *Check:* `ros2 control list_hardware_components` shows it `active`; with the wheels off the
   ground, pulling the cable stops the motors within the firmware timeout and the log names the bus.

6. **Bring up CAN on Linux.** Set bitrate (and `dbitrate ... fd on` for CAN FD) with the interface
   down, `restart-ms` for bus-off recovery, `txqueuelen` for bursts, switchable termination if the
   adapter has it; make it persistent with systemd-networkd. Commands and files:
   [can-linux.md](references/can-linux.md).
   *Check:* `ip -details -statistics link show can0` shows `ERROR-ACTIVE`, the bitrate and sample
   point you chose, and the error counters stay still while devices talk.

7. **Test a device with candump and python-can.** Watch traffic and periods (`candump -td -x can0`),
   error frames (`candump -e can0,0:0,#FFFFFFFF`), load (`canbusload can0@500000`); send by hand
   with `cansend`; script request-response and timing with python-can (`is_extended_id=False` for
   11-bit IDs). `can_probe.py` lists CANopen heartbeats and reads objects over SDO:
   [can-linux.md](references/can-linux.md).
   *Check:* each device's frames arrive at their period, there are no error frames, and bus load is
   inside the spec's budget.

8. **Make a board a CANopen device with CANopenNode.** Edit the object dictionary in CANopenEditor
   (it generates `OD.c`, `OD.h` and the EDS), run `CO_process()` in the main loop and SYNC, RPDO and
   TPDO processing in a 1 ms task. For safety, consume the master's heartbeat (0x1016), stop on
   heartbeat or RPDO timeout, and drive motors only in NMT operational. Objects, frames and code:
   [canopen.md](references/canopen.md).
   *Check:* NMT commands from `cansend` change the heartbeat state byte; silencing the master's
   heartbeat stops the motors within the consumer time.

9. **Run a CiA 402 drive through ros2_canopen.** Jazzy binaries; a config package with `bus.yml`,
   the drive's EDS and `cogen_dcf()`; the `canopen_ros2_control/RobotSystem` plugin in the URDF;
   SI scale factors set per drive; first on `vcan0` with `canopen_fake_slaves`. Activation enables
   the drive and runs homing if 0x6098 is non-zero; deactivation sends quick stop. Files and steps:
   [ros2-canopen.md](references/ros2-canopen.md).
   *Check:* every node reaches NMT operational and `Operation enabled`; one revolution by hand
   moves the joint state by 2π rad with the right sign; a pulled CAN cable makes the drive react as
   its 0x6007 setting says.

## Traps

| Symptom | Cause | Fix |
|---|---|---|
| Serial frames lost at random, CRC errors at higher baud | Ring buffer overrun, baud error between clocks, missing common ground | DMA or interrupt RX into a ring buffer ([fw-mcu](../fw-mcu/SKILL.md)); check clock error; join grounds |
| Values garbled only between two compilers or CPUs | Struct `memcpy`: padding and byte order | Pack each field little-endian by hand |
| Request/response takes 16 ms on a USB-serial adapter | FTDI latency timer (16 ms default) | udev rule setting `latency_timer` to 1 ([serial-linux.md](references/serial-linux.md)) |
| MCU resets whenever the node opens the port | DTR auto-reset on Arduino-style boards | Wait for the board's first frame after open; or disable auto-reset in hardware |
| Modbus RTU slave never answers a hand-built frame | Non-reflected CRC (CRC-16/CMS) instead of CRC-16/MODBUS | Use a Modbus library, or the reflected CRC sent low byte first |
| RS-485 replies cut off or garbled | Driver-enable released before the last stop bit left | Drop DE on transmit-complete, not buffer-empty; or hardware DE |
| `RTNETLINK answers: Device or resource busy` | Bitrate or `restart-ms` changed while `can0` is up | `ip link set can0 down` first |
| `write: No buffer space available` (ENOBUFS) | Default CAN TX queue (10 frames) overflows in bursts | `txqueuelen 1000` (ros2_canopen docs value) |
| Sender's error counter climbs, state `ERROR-PASSIVE` or `BUS-OFF` | Nobody acknowledges: node alone, bitrates differ, or a wiring fault | Second node at the same bitrate, 60 Ω check, `restart-ms` |
| python-can frames show 29-bit IDs | `can.Message` defaults to `is_extended_id=True` | Pass `is_extended_id=False` |
| CAN FD frames break a working bus | A Classical-CAN-only node flags FD frames as errors | Every node FD-capable, or stay on Classical CAN |
| Drive moves at activation | ros2_canopen `init` runs homing when 0x6098 is non-zero | Set the homing method deliberately in `sdo:`; clear the axis |
| Joint 1000 times too far or too fast | ros2_canopen default scales are 1000 and 0.001 | Set `scale_pos_to_dev` and the other five per drive |
| Drive unplugged, ros2_control stays `active` | `RobotSystem` `read()`/`write()` return OK in 0.3.4 whatever the bus does | Drive-side heartbeat consumer and 0x6007; watch the drivers' `/diagnostics` |
| Robot keeps moving after ROS dies | No timeout below the link | Firmware command timeout; CANopen heartbeat consumer; EtherCAT SM watchdog |

## Checks

Before reporting the link done:

- The link spec exists; every motor-driving message has a timeout, and pulling the cable stops the
  motors (measured, wheels off the ground or arm clear).
- Serial: 60 s of `serial_link_test.py` at the control rate with zero CRC errors and lost replies;
  the port is opened through its stable name by the robot user.
- CAN: 60 Ω measured; `ERROR-ACTIVE` with steady error counters after 10 minutes of normal traffic;
  bus load inside budget; the interface comes back the same after a reboot.
- CANopen: every node's heartbeat at its period; NMT start, stop and reset behave; a lost master
  heartbeat stops the drive.
- ros2_control: component `active`, controllers `active`, joint directions and scales checked by hand.

## Distro differences

- **Lyrical** (Ubuntu 26.04): `canopen_ros2_control` has no Lyrical binary, and its source still
  overrides the export methods ros2_control 6 removed; use the 402 driver's ROS services and topics
  or a plugin of your own. python3-can is 4.6.1; `bustype=` is deprecated (removal planned for 5.0),
  use `interface=`. The serial `MotorBus` code works unchanged.
- **Humble** (Ubuntu 22.04): ros2_canopen 0.2.13 from its `humble` branch; python3-can 3.3.2 and
  can-utils 2020.11 (check `candump --help` for options); the plugin around `MotorBus` uses the
  Humble ros2_control API ([ros2-control](../ros2-control/SKILL.md)).
- **EtherCAT:** `ethercat_driver_ros2` has no binary on any distro; its `jazzy` branch builds from source.

## Related

- References: [serial-protocol.md](references/serial-protocol.md),
  [serial-firmware.md](references/serial-firmware.md), [serial-linux.md](references/serial-linux.md),
  [serial-link-test.md](references/serial-link-test.md), [serial-motor-bus.md](references/serial-motor-bus.md),
  [wiring.md](references/wiring.md), [can-linux.md](references/can-linux.md),
  [canopen.md](references/canopen.md), [ros2-canopen.md](references/ros2-canopen.md),
  [ethercat.md](references/ethercat.md).
- Skills: [fw-mcu](../fw-mcu/SKILL.md), [fw-rtos-micro-ros](../fw-rtos-micro-ros/SKILL.md),
  [ros2-control](../ros2-control/SKILL.md), [ros2-core](../ros2-core/SKILL.md),
  [ops-bringup](../ops-bringup/SKILL.md), [ops-docker-ci](../ops-docker-ci/SKILL.md),
  [arch-safety](../arch-safety/SKILL.md).
- Wiki: [CANopenNode](../../wiki/software/canopennode.md), [ros2_canopen](../../wiki/software/ros2-canopen.md),
  [python-can](../../wiki/software/python-can.md), [can-utils](../../wiki/tools/can-utils.md),
  [ros2_control](../../wiki/software/ros2-control.md), [ROS 2](../../wiki/tools/ros2.md),
  [choose an MCU and firmware stack](../../wiki/guides/choose-an-mcu-and-firmware-stack.md).
- Upstream: kernel.org `networking/can` and `serial-rs485`; `linux-can/can-utils`; python-can docs;
  `CANopenNode/CANopenNode`; ros2_canopen manual and `canopen_tests`; TI SLLA270 and SLLA272D.

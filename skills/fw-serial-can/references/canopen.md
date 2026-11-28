# CANopen: the frames you test with, and a device with CANopenNode

Part of [fw-serial-can](../SKILL.md). The CiA 301 services as they appear on the bus, the CiA 402
objects a drive needs, and the firmware side with CANopenNode v4 (Apache-2.0). Checked against
CANopenNode `master` (headers `CO_driver.h`, `CO_NMT_Heartbeat.h`, `CO_PDO.h`, `CO_Emergency.h`,
`example/`) and the ros2_canopen 0.3.4 CiA 402 driver and test EDS.

## Default identifiers (11-bit, node ID 1 to 127)

| Service | COB-ID | Direction |
|---|---|---|
| NMT command | 0x000 | master to all |
| SYNC | 0x080 | producer to all |
| EMCY | 0x080 + node | device to all |
| TPDO1 to TPDO4 | 0x180, 0x280, 0x380, 0x480 + node | device to all |
| RPDO1 to RPDO4 | 0x200, 0x300, 0x400, 0x500 + node | to the device |
| SDO request / response | 0x600 + node / 0x580 + node | client to server / back |
| Heartbeat | 0x700 + node | device to all |

All multi-byte values in SDO and PDO data are little-endian.

## Test it by hand with cansend

```bash
cansend can0 000#8102      # NMT reset node 2 (0x81); 0x82 reset communication
cansend can0 000#8000      # all nodes to pre-operational (node 0 = all)
cansend can0 000#0102      # start node 2 (operational); 0x02 = stop
candump -td can0,702:7FF   # node 2 heartbeat: 1 byte state at its period
cansend can0 602#4000100000000000   # SDO read 0x1000:00 (device type) from node 2
cansend can0 602#2B17100064000000   # SDO write 0x1017:00 = 100 ms (2 bytes) to node 2
```

| Heartbeat byte | NMT state | | SDO command byte | Meaning |
|---|---|---|---|---|
| 0x00 | boot-up | | 0x40 | upload (read) request |
| 0x7F | pre-operational | | 0x43 / 0x47 / 0x4B / 0x4F | read reply with 4 / 3 / 2 / 1 bytes |
| 0x05 | operational | | 0x23 / 0x27 / 0x2B / 0x2F | write request with 4 / 3 / 2 / 1 bytes |
| 0x04 | stopped | | 0x60 / 0x80 | write confirmed / abort (code in bytes 4 to 7) |

SDO bytes 1 and 2 are the index (low byte first), byte 3 the sub-index. Use
`can_probe.py` from [can-linux.md](can-linux.md) to script the same.

## PDO configuration (pre-operational)

A PDO has a communication object (RPDO 0x1400+, TPDO 0x1800+) and a mapping object (RPDO 0x1600+,
TPDO 0x1A00+). Each mapping entry is a `u32`: `index << 16 | sub-index << 8 | length in bits`, for
example 0x60410010 maps the 16-bit statusword. To change one:

1. Set bit 31 of the COB-ID (communication object sub 1) to disable the PDO.
2. Write 0 to mapping sub 0, write the entries to sub 1, 2 ..., then write their count to sub 0.
3. Set the transmission type (communication sub 2): 0 synchronous acyclic, 1 to 240 every n-th
   SYNC, 254 or 255 event-driven; and the event timer (sub 5, ms) if wanted.
4. Clear bit 31 to enable it again.

At most 8 bytes per PDO on Classical CAN. ros2_canopen does all of this from `bus.yml`.

## CiA 402 drive objects

| Object | Name | Notes |
|---|---|---|
| 0x6040 | Controlword | 0x06 shutdown, 0x07 switch on, 0x0F enable operation, 0x02 quick stop, 0x00 disable voltage, 0x80 fault reset (rising edge) |
| 0x6041 | Statusword | `sw & 0x6F`: 0x40 or 0x60 switch on disabled, 0x21 ready to switch on, 0x23 switched on, 0x27 operation enabled, 0x07 quick stop active; `sw & 0x4F == 0x08` fault |
| 0x6060 / 0x6061 | Modes of operation / display | 1 profile position, 3 profile velocity, 4 profile torque, 6 homing, 7 interpolated position, 8 / 9 / 10 cyclic synchronous position / velocity / torque |
| 0x6064, 0x606C, 0x6077 | Position, velocity, torque actual | Device units |
| 0x607A, 0x60FF, 0x6071 | Target position, velocity, torque | Device units |
| 0x6081, 0x6083 | Profile velocity, acceleration | Profile modes |
| 0x6098 | Homing method | Non-zero makes ros2_canopen home at activation |
| 0x605A | Quick stop option code | What quick stop does (decelerate, then hold or disable) |
| 0x6007 | Abort connection option code | What the drive does when its master link is lost |
| 0x6502 | Supported drive modes | Bit n-1 set when mode n is supported |

The enable sequence is shutdown (0x06), switch on (0x07), enable operation (0x0F), each after the
statusword confirms the previous state. Read the drive manual for its own limits and units.

## A device with CANopenNode

CANopenNode is the device-side stack (NMT slave, SDO server, PDO, heartbeat, EMCY, LSS). It has no
hardware drivers: start from a port (CANopenSTM32, CANopenPIC, CANopenLinux, or the list in
`doc/deviceSupport.md`) and edit the object dictionary in CANopenEditor, which generates `OD.c`,
`OD.h`, the EDS file for the master and documentation.

Structure, after `example/main_blank.c`:

```c
// my_robot_firmware/src/canopen_app.c (outline; init arguments as in example/main_blank.c)
#define NMT_CONTROL (CO_NMT_ERR_ON_BUSOFF_HB | CO_NMT_ERR_TO_STOPPED | CO_NMT_ERR_ON_ERR_REG \
                     | CO_ERR_REG_GENERIC_ERR | CO_ERR_REG_COMMUNICATION)

// Main loop: NMT, SDO, heartbeat, EMCY. Act on reset requests it returns.
reset = CO_process(CO, false, time_difference_us, NULL);

// 1 ms timer task or interrupt: PDO and SYNC, with the OD locked
CO_LOCK_OD(CO->CANmodule);
if (!CO->nodeIdUnconfigured && CO->CANmodule->CANnormal) {
  bool_t sync_was = CO_process_SYNC(CO, time_difference_us, NULL);
  CO_process_RPDO(CO, sync_was, time_difference_us, NULL);
  motion_update();  // reads RPDO-mapped targets, writes TPDO-mapped state
  CO_process_TPDO(CO, sync_was, time_difference_us, NULL);
}
CO_UNLOCK_OD(CO->CANmodule);

// Motion gate: drive motors only when the network is healthy
static bool motion_allowed(void)
{
  return CO_NMT_getInternalState(CO->NMT) == CO_NMT_OPERATIONAL &&
         !CO_isError(CO->em, CO_EM_HEARTBEAT_CONSUMER) &&
         !CO_isError(CO->em, CO_EM_RPDO_TIME_OUT);
}
```

Safety settings in the object dictionary (values are examples; set them from the risk assessment):

- **0x1016 consumer heartbeat:** `node_id << 16 | time_ms` for the master, e.g. 0x0001012C watches
  node 1 with a 300 ms timeout. With `CO_NMT_ERR_ON_BUSOFF_HB` and `CO_NMT_ERR_TO_STOPPED` the device
  leaves operational on heartbeat loss or bus-off, and `motion_allowed()` goes false.
- **0x1017 producer heartbeat:** e.g. 100 ms, so the master sees this device.
- **RPDO event timer (0x1400+ sub 5):** with `CO_CONFIG_RPDO_TIMERS_ENABLE` set in `CO_CONFIG_PDO`,
  a missing command RPDO raises `CO_EM_RPDO_TIME_OUT`; make it about three command periods.
- Stop the motors (and keep them stopped until a fresh command in operational) whenever
  `motion_allowed()` is false; latch faults in the error register so the master sees them.
- Keep the MCU hardware watchdog running ([fw-mcu](../../fw-mcu/SKILL.md)).

*Check:* with the device as node 3 and a test master on node 1 producing heartbeats,
`cansend can0 000#0103` starts it and its heartbeat byte turns 0x05; stop the master's heartbeat
and the device goes to 0x04 (stopped) and its motors stop within the consumer time;
`python3 can_probe.py --sdo 3 0x1018 1` reads its vendor ID.

Sources: CANopenNode README, `301/CO_driver.h` (default CAN IDs), `301/CO_NMT_Heartbeat.h` (NMT
commands, states, control flags), `301/CO_PDO.h` (PDO procedure, transmission types),
`301/CO_PDO.c` (mapping entry layout), `301/CO_Emergency.h`, `example/main_blank.c`,
`example/DS301_profile.md` (0x1016, 0x1017); ros2_canopen 0.3.4 `canopen_402_driver` (`state.cpp`,
`command.cpp`, `base.hpp`, `motor.cpp`) and `canopen_tests/config/robot_control/cia402_slave.eds`.

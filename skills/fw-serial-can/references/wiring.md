# Wiring checks for CAN, RS-485 and UART

Part of [fw-serial-can](../SKILL.md). What to check with a multimeter and the Linux tools before
blaming firmware. Numbers come from TI's application reports SLLA270 (CAN physical layer, 2008)
and SLLA272D (RS-485 design guide, 2021) and from the kernel SocketCAN docs; your transceiver's
data sheet wins where it differs.

## CAN (ISO 11898-2 high-speed)

- **Topology:** one line of twisted pair (120 Ω characteristic impedance), nodes on short stubs. No
  star. The ISO 11898 figures TI quotes: up to 1 Mbit/s over 40 m with up to 30 nodes, unterminated
  stubs at most 0.3 m at 1 Mbit/s. Lower the bitrate for longer runs.
- **Termination:** 120 Ω at each of the two far ends of the line, nowhere else. Split termination
  (two 60 Ω in series with a capacitor, typically 4.7 nF, to ground) improves emissions.
  - Power everything off and measure CANH to CANL anywhere on the bus: about **60 Ω** is right,
    about 120 Ω means one terminator is missing, about 40 Ω or less means three or more.
  - Many adapters and boards have a jumper, DIP switch or software switch for their resistor. With
    a switchable one on Linux: `ip -details link show can0` lists the values,
    `sudo ip link set dev can0 type can termination 120` turns it on (interface down first).
- **Ground:** the standard tolerates a ground offset of -2 V to +7 V between nodes (common-mode
  range). Join the transceiver grounds (CAN_GND) through the cable; on a robot every node normally
  shares the battery negative. Between separately powered systems use isolated transceivers.
- **Bitrate and sample point:** every node at the same bitrate. Let the kernel pick the timing from
  `bitrate`; it uses the CiA-recommended sample point unless you give one: 87.5 % up to 500 kbit/s,
  80 % up to 800 kbit/s, 75 % above. Set MCU nodes to the same sample point (the controller's
  timing calculator, or `can-calc-bit-timing` from can-utils for the arithmetic).
- **CAN FD:** a second (data) bitrate, and every node must handle FD frames; the arbitration phase
  still follows the rules above, and the data phase is far less tolerant of stubs and reflections.
- **Connector:** CiA 303-1 defines CANopen pinouts for the 9-pin D-sub, M12, RJ45 and other
  connectors; vendors also use terminal blocks. Take the pinout from each device's manual and
  check CANH, CANL and CAN_GND continuity end to end with a meter.

After power-up:

```bash
ip -details -statistics link show can0
# want: state ERROR-ACTIVE (berr-counter tx 0 rx 0), the bitrate and sample-point you set,
# and the bus-errors / error-warn / error-pass / bus-off counters not rising
candump -e can0,0:0,#FFFFFFFF     # data frames plus decoded error frames
```

| Reading | Likely cause |
|---|---|
| Bus errors on every frame, sender `ERROR-PASSIVE` | No other node at that bitrate; or CANH and CANL swapped |
| Errors that come and go with motion or motor current | Missing or doubled termination, long stubs, ground offset, cable next to motor phases |
| `BUS-OFF` after plugging a node in | That node runs a different bitrate or sample point |
| Works at 125 kbit/s, fails at 1 Mbit/s | Bus too long, stubs too long, or wrong termination |

## RS-485

- **Cable and termination:** twisted pair, 120 Ω characteristic impedance, a 120 Ω resistor at each
  end of the trunk only, stubs as short as possible.
- **Fail-safe bias:** an idle bus (nobody driving) must read as a defined level. Modern transceivers
  have internal fail-safe; in noisy places add external bias resistors (SLLA272D works an example:
  two 523 Ω resistors with 120 Ω termination at 5 V). Bias counts toward the bus load.
- **Load:** a standard driver drives 32 unit loads; reduced-load transceivers (1/8 UL) allow up to
  256 nodes, or 96 once external fail-safe bias (up to 20 unit loads) is on the bus.
- **Ground:** RS-485 also has a limited common-mode range. Carry a signal ground with the pair; for
  long runs between separately powered systems use isolated transceivers (SLLA272D §11).
- **A and B:** vendors label the lines inconsistently. If a correctly configured slave never
  answers, swap A and B before anything else.
- **Direction control:** release driver-enable only after the UART's transmit-complete flag (last
  stop bit sent), not when its data register empties; otherwise the last byte is cut off.

## UART (TTL or USB serial)

- TX of one side to RX of the other, both ways; a common ground wire.
- Logic levels: a 5 V TX into a 3.3 V-only RX pin can damage it; use a level shifter or a 5 V
  tolerant pin (check the MCU data sheet).
- Keep TTL UART runs short (inside the robot). For longer runs or near motor wiring, use RS-485 or CAN.
- Baud error: both ends' clocks must land close to the nominal rate; compute the error from the
  MCU's clock and divider ([fw-mcu](../../fw-mcu/SKILL.md)).

Sources: TI SLLA270 "Controller Area Network Physical Layer Requirements" (sections 4.2 to 4.8);
TI SLLA272D "The RS-485 Design Guide" (sections 5 to 8 and 11); kernel docs `networking/can`
(switchable termination, bit timing); can-utils `can-calc-bit-timing` (CiA sample points).

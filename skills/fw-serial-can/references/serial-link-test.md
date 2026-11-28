# Serial link tester (pyserial)

Part of [fw-serial-can](../SKILL.md). Tests the link in [serial-protocol.md](serial-protocol.md)
from Linux without ROS, before the ros2_control plugin is involved.

Sends `GET_STATE` at a fixed rate and reports lost replies, CRC errors and round-trip times. It
never sends a motion command. Runs with `python3-serial` (pyserial 3.5) on Ubuntu 24.04.

```python
#!/usr/bin/env python3
"""Exercise the my_robot serial link without ROS (GET_STATE only, no motion)."""
import argparse
import struct
import time

import serial

GET_STATE, STATE = 0x03, 0x82


def crc16(data: bytes) -> int:
    crc = 0xFFFF  # CRC-16/CCITT-FALSE
    for b in data:
        crc ^= b << 8
        for _ in range(8):
            crc = ((crc << 1) ^ 0x1021) & 0xFFFF if crc & 0x8000 else (crc << 1) & 0xFFFF
    return crc


def cobs_encode(src: bytes) -> bytes:
    out, block = bytearray(), bytearray()
    for i, b in enumerate(src):
        if b == 0:
            out += bytes([len(block) + 1]) + block
            block.clear()
            continue
        block.append(b)
        if len(block) == 254 and i + 1 < len(src):
            out += b"\xff" + block
            block.clear()
    return bytes(out + bytes([len(block) + 1]) + block)


def cobs_decode(src: bytes) -> bytes | None:
    out, i = bytearray(), 0
    while i < len(src):
        code = src[i]
        if code == 0 or i + code > len(src):
            return None
        out += src[i + 1:i + code]
        i += code
        if code != 0xFF and i < len(src):
            out.append(0)
    return bytes(out)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", default="/dev/my_robot_mcu")
    ap.add_argument("--baud", type=int, default=115200)
    ap.add_argument("--rate", type=float, default=100.0, help="requests per second")
    ap.add_argument("--seconds", type=float, default=60.0)
    ap.add_argument("--timeout", type=float, default=0.005, help="reply deadline, s")
    a = ap.parse_args()
    ser = serial.Serial(a.port, a.baud, timeout=a.timeout, exclusive=True)
    time.sleep(2.0)  # example: covers a board that resets on open and runs its bootloader
    ser.reset_input_buffer()
    seq = sent = lost = bad = 0
    rtts = []
    next_t = time.monotonic()
    end = next_t + a.seconds
    while time.monotonic() < end:
        seq = (seq + 1) & 0xFF
        raw = bytes([seq, GET_STATE])
        t0 = time.monotonic()
        ser.write(cobs_encode(raw + struct.pack("<H", crc16(raw))) + b"\x00")
        sent += 1
        got = False
        while not got and time.monotonic() - t0 < a.timeout:
            enc = ser.read_until(b"\x00")
            if not enc.endswith(b"\x00"):
                break  # read timed out
            frame = cobs_decode(enc[:-1])
            if not frame or len(frame) < 4 or crc16(frame[:-2]) != struct.unpack("<H", frame[-2:])[0]:
                bad += 1
            elif frame[0] == seq and frame[1] == STATE:
                got = True
                rtts.append(time.monotonic() - t0)
        lost += not got
        next_t += 1.0 / a.rate
        time.sleep(max(0.0, next_t - time.monotonic()))
    rtts.sort()
    p50 = 1000 * rtts[len(rtts) // 2] if rtts else float("nan")
    p99 = 1000 * rtts[int(len(rtts) * 0.99)] if rtts else float("nan")
    print(f"sent {sent} lost {lost} bad {bad} rtt p50 {p50:.2f} ms p99 {p99:.2f} ms")


if __name__ == "__main__":
    main()
```

Pass: `lost 0 bad 0`, and p99 below the timeout the plugin will use. A few lost replies per minute
point at USB latency or an overloaded MCU loop; any `bad` count points at wiring, baud or ground.

Sources: pyserial 3.5 API documentation (`Serial`, `exclusive`, `read_until`,
`reset_input_buffer`); the CRC RevEng catalogue (CRC-16/IBM-3740). The functions were run
against the frame test vectors in a Python test.

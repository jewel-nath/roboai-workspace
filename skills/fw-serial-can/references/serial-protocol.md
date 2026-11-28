# A framed serial protocol for a motor board

Part of [fw-serial-can](../SKILL.md). One request, one reply, over UART, USB CDC or RS-485. The C
code below is shared by `my_robot_firmware` and the host plugin
([serial-motor-bus.md](serial-motor-bus.md)); it is plain C99 and also compiles as C++.

## Frame

Before encoding, a frame is:

| Bytes | Field | Notes |
|---|---|---|
| 1 | `seq` | Host increments it per request; the reply echoes it |
| 1 | `type` | Message type (table below) |
| 0 to 60 | payload | Fixed layout per type, little-endian, packed byte by byte |
| 2 | CRC | CRC-16/CCITT-FALSE over `seq`, `type` and payload, low byte first |

The frame is then COBS-encoded, which removes every 0x00 byte, and a 0x00 delimiter is appended. A
receiver that starts mid-stream or loses bytes resynchronises at the next 0x00. COBS adds at most
one byte per 254 plus one.

- **CRC-16/CCITT-FALSE** (catalogued as CRC-16/IBM-3740): polynomial 0x1021, initial value 0xFFFF,
  no reflection, no final XOR. Check value over ASCII `123456789`: **0x29B1**.
- **Modbus RTU is different:** CRC-16/MODBUS is the reflected form (0x8005 reflected, initial
  0xFFFF), sent low byte first, check value **0x4B37**. The non-reflected 0x8005 variant (CRC-16/CMS,
  check 0xAEE7) will never match a Modbus slave. On the Linux side use a library: libmodbus
  (LGPL-2.1+, `libmodbus-dev` on Ubuntu; link it dynamically or meet the LGPL terms) or pymodbus
  (BSD-3-Clause).

## Messages (example set)

| Type | Name | Direction | Payload |
|---|---|---|---|
| 0x01 | `SET_ENABLE` | host to MCU | `u8` 1 = enable, 0 = disable |
| 0x02 | `SET_VELOCITY` | host to MCU | `i32` ticks/s per joint |
| 0x03 | `GET_STATE` | host to MCU | none; does **not** refresh the command timeout |
| 0x82 | `STATE` | MCU to host | per joint `i32` position ticks, `i32` ticks/s; then `u8` flags |
| 0x7F | `ERROR` | MCU to host | `u8` code: 1 unknown type, 2 bad length |

Flags: bit 0 enabled, bit 1 command timeout tripped, bit 2 driver fault. Every valid request gets
exactly one reply with the same `seq`; a corrupt one gets none, and the host counts a miss. Grow the
set by adding types; never change a payload layout without a new type or a version field.

## Shared code: `link.h` and `link.c`

```c
// link.h - shared by my_robot_firmware and my_robot_hardware
#pragma once
#include <stddef.h>
#include <stdint.h>
#ifdef __cplusplus
extern "C" {
#endif

#define LINK_MAX_FRAME 64u  // decoded bytes incl. seq, type and CRC (choice)
#define LINK_MAX_ENCODED (LINK_MAX_FRAME + LINK_MAX_FRAME / 254u + 2u)  // COBS + delimiter

uint16_t link_crc16(const uint8_t * data, size_t len);
size_t link_cobs_encode(const uint8_t * src, size_t len, uint8_t * dst);
size_t link_cobs_decode(const uint8_t * src, size_t len, uint8_t * dst, size_t cap);
// Returns bytes written to out, delimiter included; 0 if the payload is too long.
size_t link_encode_frame(uint8_t seq, uint8_t type, const uint8_t * payload, size_t n,
                         uint8_t * out, size_t cap);
// enc: one frame without its 0x00. Returns the payload length, or -1 for a bad frame.
int link_decode_frame(const uint8_t * enc, size_t n, uint8_t * seq, uint8_t * type,
                      uint8_t * payload, size_t cap);

static inline void link_put_i32(uint8_t * p, int32_t v)
{
  const uint32_t u = (uint32_t)v;
  p[0] = (uint8_t)u; p[1] = (uint8_t)(u >> 8); p[2] = (uint8_t)(u >> 16); p[3] = (uint8_t)(u >> 24);
}
static inline int32_t link_get_i32(const uint8_t * p)
{
  return (int32_t)((uint32_t)p[0] | ((uint32_t)p[1] << 8) | ((uint32_t)p[2] << 16) |
                   ((uint32_t)p[3] << 24));
}

#ifdef __cplusplus
}
#endif
```

```c
// link.c
#include "link.h"

uint16_t link_crc16(const uint8_t * data, size_t len)
{
  uint16_t crc = 0xFFFF;  // CRC-16/CCITT-FALSE
  for (size_t i = 0; i < len; ++i) {
    crc ^= (uint16_t)(data[i] << 8);
    for (int b = 0; b < 8; ++b) {
      crc = (crc & 0x8000) ? (uint16_t)((crc << 1) ^ 0x1021) : (uint16_t)(crc << 1);
    }
  }
  return crc;
}

size_t link_cobs_encode(const uint8_t * src, size_t len, uint8_t * dst)
{
  size_t code_idx = 0, out = 1;
  uint8_t code = 1;
  for (size_t i = 0; i < len; ++i) {
    if (src[i] == 0) {
      dst[code_idx] = code; code_idx = out++; code = 1;
    } else {
      dst[out++] = src[i];
      // A full block of 254 data bytes ends without an implied zero
      if (++code == 0xFF && i + 1 < len) {
        dst[code_idx] = code; code_idx = out++; code = 1;
      }
    }
  }
  dst[code_idx] = code;
  return out;
}

size_t link_cobs_decode(const uint8_t * src, size_t len, uint8_t * dst, size_t cap)
{
  size_t in = 0, out = 0;
  while (in < len) {
    const uint8_t code = src[in++];
    if (code == 0 || in + code - 1 > len) return 0;  // corrupt
    for (uint8_t k = 1; k < code; ++k) {
      if (out >= cap) return 0;
      dst[out++] = src[in++];
    }
    if (code != 0xFF && in < len) {
      if (out >= cap) return 0;
      dst[out++] = 0;
    }
  }
  return out;
}

size_t link_encode_frame(uint8_t seq, uint8_t type, const uint8_t * payload, size_t n,
                         uint8_t * out, size_t cap)
{
  uint8_t raw[LINK_MAX_FRAME];
  if (n + 4 > sizeof raw || cap < LINK_MAX_ENCODED) return 0;
  raw[0] = seq;
  raw[1] = type;
  for (size_t i = 0; i < n; ++i) raw[2 + i] = payload[i];
  const uint16_t crc = link_crc16(raw, n + 2);
  raw[n + 2] = (uint8_t)crc;
  raw[n + 3] = (uint8_t)(crc >> 8);
  size_t len = link_cobs_encode(raw, n + 4, out);
  out[len++] = 0x00;
  return len;
}

int link_decode_frame(const uint8_t * enc, size_t n, uint8_t * seq, uint8_t * type,
                      uint8_t * payload, size_t cap)
{
  uint8_t raw[LINK_MAX_FRAME];
  const size_t len = link_cobs_decode(enc, n, raw, sizeof raw);
  if (len < 4) return -1;
  const uint16_t got = (uint16_t)(raw[len - 2] | (raw[len - 1] << 8));
  if (link_crc16(raw, len - 2) != got || len - 4 > cap) return -1;
  *seq = raw[0];
  *type = raw[1];
  for (size_t i = 0; i < len - 4; ++i) payload[i] = raw[2 + i];
  return (int)(len - 4);
}
```

## Firmware side

The MCU loop (UART bytes to frames, message handling, the command timeout that stops the motors)
is in [serial-firmware.md](serial-firmware.md).

## Test vectors

Run them in a host unit test and once on the MCU (print or assert).

| Input (hex) | COBS output (hex, no delimiter) |
|---|---|
| `00` | `01 01` |
| `00 00` | `01 01 01` |
| `11 22 00 33` | `03 11 22 02 33` |
| `11 22 33 44` | `05 11 22 33 44` |
| `11 00 00 00` | `02 11 01 01 01` |
| `01 02 ... FE` (254 bytes) | `FF 01 02 ... FE` |
| `00 01 ... FE` (255 bytes) | `01 FF 01 ... FE` |

A full frame: `seq` 0x01, `SET_VELOCITY`, joints +1000 and -1000 ticks/s gives the raw bytes
`01 02 E8 03 00 00 18 FC FF FF`, CRC 0xEB22, and on the wire
`05 01 02 E8 03 01 07 18 FC FF FF 22 EB 00`.

Sources: the CRC RevEng catalogue of 16-bit CRCs (CRC-16/IBM-3740, CRC-16/MODBUS, CRC-16/CMS);
Cheshire and Baker, "Consistent Overhead Byte Stuffing" (IEEE/ACM ToN, 1999); libmodbus licence from
Ubuntu's `libmodbus` copyright file; pymodbus licence from PyPI. The vectors were computed with a
Python port of this code.

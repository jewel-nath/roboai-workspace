# Firmware side of the serial link

Part of [fw-serial-can](../SKILL.md). The MCU end of the protocol in
[serial-protocol.md](serial-protocol.md): frame assembly from the UART, message handling, and the
command timeout that stops the motors when the host goes quiet. Plain C99; `link.h` and `link.c`
come from that file.

`uart_read_byte()`, `uart_write()`, `millis()` and the motor and encoder calls are your board layer
([fw-mcu](../../fw-mcu/SKILL.md)); feed UART RX into a ring buffer from DMA or an interrupt.

```c
// my_robot_firmware/src/link_task.c - call link_poll() every main-loop pass or from a task
#include <stdbool.h>
#include "board.h"
#include "link.h"

#define NUM_JOINTS 2
#define CMD_TIMEOUT_MS 100u  // example: 10 periods at 100 Hz; tune to how far the robot may coast

enum { SET_ENABLE = 0x01, SET_VELOCITY = 0x02, GET_STATE = 0x03, STATE = 0x82, ERROR_MSG = 0x7F };

static uint8_t rx[LINK_MAX_ENCODED];
static size_t rx_len;
static bool rx_overflow, enabled, timed_out;
static uint32_t last_cmd_ms;
static uint32_t bad_frames;  // expose in STATE or a debug message

static void send(uint8_t seq, uint8_t type, const uint8_t * p, size_t n)
{
  uint8_t out[LINK_MAX_ENCODED];
  const size_t len = link_encode_frame(seq, type, p, n, out, sizeof out);
  if (len > 0) uart_write(out, len);
}

static void reply_state(uint8_t seq)
{
  uint8_t p[NUM_JOINTS * 8 + 1];
  for (int j = 0; j < NUM_JOINTS; ++j) {
    link_put_i32(&p[j * 8], encoder_ticks(j));
    link_put_i32(&p[j * 8 + 4], encoder_ticks_per_s(j));
  }
  p[NUM_JOINTS * 8] = (uint8_t)((enabled ? 1 : 0) | (timed_out ? 2 : 0) | (driver_fault() ? 4 : 0));
  send(seq, STATE, p, sizeof p);
}

static void handle(const uint8_t * enc, size_t n)
{
  uint8_t seq, type, p[LINK_MAX_FRAME];
  const int m = link_decode_frame(enc, n, &seq, &type, p, sizeof p);
  if (m < 0) { ++bad_frames; return; }  // no reply: the host times out and counts a miss
  if (type == SET_ENABLE && m == 1) {
    enabled = p[0] != 0;
    timed_out = false;
    if (!enabled) motors_stop();
    last_cmd_ms = millis();
  } else if (type == SET_VELOCITY && m == NUM_JOINTS * 4) {
    for (int j = 0; j < NUM_JOINTS; ++j) {
      motor_set_velocity(j, enabled ? link_get_i32(&p[j * 4]) : 0);
    }
    last_cmd_ms = millis();
  } else if (type != GET_STATE || m != 0) {
    const uint8_t code = (type == SET_ENABLE || type == SET_VELOCITY || type == GET_STATE) ? 2 : 1;
    send(seq, ERROR_MSG, &code, 1);
    return;
  }
  reply_state(seq);
}

void link_poll(void)
{
  uint8_t b;
  while (uart_read_byte(&b)) {
    if (b != 0x00) {
      if (rx_len < sizeof rx) rx[rx_len++] = b; else rx_overflow = true;
      continue;
    }
    if (!rx_overflow && rx_len > 0) handle(rx, rx_len);
    rx_len = 0;
    rx_overflow = false;
  }
  // Host silent (cable out, node crashed, computer hung): stop and stay disabled until re-enabled
  if (enabled && (uint32_t)(millis() - last_cmd_ms) > CMD_TIMEOUT_MS) {
    enabled = false;
    timed_out = true;
    motors_stop();
  }
}
```

This timeout is a software layer under the hardware E-stop chain, not a replacement for it
([arch-safety](../../arch-safety/SKILL.md)). Clamp commanded velocity to the motor's limit inside
`motor_set_velocity()`, and keep the MCU's hardware watchdog running so a hung loop also stops.

Checks on the bench, motors unpowered or wheels off the ground:

- `serial_link_test.py` ([serial-link-test.md](serial-link-test.md)) reports no lost or bad replies.
- Send `SET_ENABLE 1` and a small `SET_VELOCITY`, then stop sending: the motors stop after
  `CMD_TIMEOUT_MS` and the next `STATE` has flag bit 1 set and bit 0 clear.
- A corrupted frame (flip one byte) gets no reply and raises `bad_frames`.

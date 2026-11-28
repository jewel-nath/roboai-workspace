# The serial MotorBus under ros2_control

Part of [fw-serial-can](../SKILL.md). Implements the `MotorBus` seam that the `MyRobotSystem` plugin
in [ros2-control hardware-interface.md](../../ros2-control/references/hardware-interface.md) calls,
over the protocol in [serial-protocol.md](serial-protocol.md) and the port class in
[serial-linux.md](serial-linux.md). This header replaces the seam's placeholder header; the plugin
code does not change. It contains nothing distro-specific (Jazzy, Kilted and Lyrical alike).

## How it fits the control loop

Each controller-manager cycle calls the plugin's `read()`, the controllers, then `write()`:

- `write_velocities()` sends `SET_VELOCITY` and waits for the `STATE` reply: one exchange per cycle.
- `read_joints()` returns the state from that reply (one cycle old). While the component is inactive
  no `write()` runs, so `read_joints()` polls with `GET_STATE` itself.
- An exchange waits at most `kReplyTimeout`; a few misses in a row return `false`, the plugin
  returns `return_type::ERROR`, the component leaves `active` and its controllers stop.
- If the reply shows the firmware disabled itself (its command timeout fired) while the host
  expects it enabled, the call fails at once.

## Header

```cpp
// include/my_robot_hardware/motor_bus.hpp
#pragma once
#include <chrono>
#include <cstdint>
#include <string>
#include <vector>

#include "my_robot_hardware/serial_port.hpp"

namespace my_robot_hardware
{
class MotorBus
{
public:
  bool open(const std::string & port, int baud_rate);
  void close();
  bool enable(bool on);
  bool read_joints(std::vector<double> & ticks, std::vector<double> & ticks_per_s);
  bool write_velocities(const std::vector<double> & ticks_per_s);

private:
  bool exchange(uint8_t type, const uint8_t * payload, std::size_t n,
                std::chrono::milliseconds timeout);
  bool miss();

  SerialPort port_;
  uint8_t seq_{0};
  int misses_{0};
  bool fresh_{false};           // a reply arrived since the last read_joints()
  bool expect_enabled_{false};
  uint8_t flags_{0};
  std::vector<int32_t> pos_, vel_;
  std::vector<uint8_t> tx_, rx_;  // reused buffers: no allocation per cycle
};
}  // namespace my_robot_hardware
```

## Implementation

```cpp
// src/motor_bus.cpp
#include "my_robot_hardware/motor_bus.hpp"

#include <algorithm>
#include <cmath>
#include <limits>

#include "my_robot_hardware/link.h"

namespace my_robot_hardware
{
namespace
{
constexpr uint8_t kSetEnable = 0x01, kSetVelocity = 0x02, kGetState = 0x03, kState = 0x82;
constexpr uint8_t kFlagEnabled = 0x01;
constexpr std::chrono::milliseconds kReplyTimeout{5};   // example: half of a 100 Hz period
constexpr std::chrono::milliseconds kBootTimeout{100};  // per try while the board boots
constexpr int kBootTries = 20;                          // example: about 2 s in total
constexpr int kMaxMisses = 3;                           // example: consecutive lost replies
}  // namespace

bool MotorBus::open(const std::string & port, int baud_rate)
{
  if (!port_.open(port, baud_rate)) return false;
  tx_.reserve(LINK_MAX_FRAME);
  rx_.reserve(LINK_MAX_ENCODED);
  expect_enabled_ = false;
  misses_ = 0;
  const uint8_t off = 0;
  for (int i = 0; i < kBootTries; ++i) {  // on_configure: waiting here is allowed
    if (exchange(kSetEnable, &off, 1, kBootTimeout)) return true;  // starts disabled
  }
  port_.close();
  return false;
}

void MotorBus::close()
{
  if (!port_.is_open()) return;
  const uint8_t off = 0;
  exchange(kSetEnable, &off, 1, kReplyTimeout);  // best effort; the firmware timeout covers a failure
  port_.close();
}

bool MotorBus::enable(bool on)
{
  expect_enabled_ = on;
  const uint8_t value = on ? 1 : 0;
  return exchange(kSetEnable, &value, 1, kReplyTimeout) &&
         ((flags_ & kFlagEnabled) != 0) == on;
}

bool MotorBus::write_velocities(const std::vector<double> & ticks_per_s)
{
  tx_.resize(ticks_per_s.size() * 4);
  for (std::size_t j = 0; j < ticks_per_s.size(); ++j) {
    // The plugin already replaced NaN with 0; clamp keeps the cast defined
    const double v = std::clamp(
      std::round(ticks_per_s[j]), double(std::numeric_limits<int32_t>::min()),
      double(std::numeric_limits<int32_t>::max()));
    link_put_i32(&tx_[j * 4], static_cast<int32_t>(v));
  }
  if (!exchange(kSetVelocity, tx_.data(), tx_.size(), kReplyTimeout)) return miss();
  misses_ = 0;
  fresh_ = true;
  return !(expect_enabled_ && (flags_ & kFlagEnabled) == 0);  // firmware stopped on its own
}

bool MotorBus::read_joints(std::vector<double> & ticks, std::vector<double> & ticks_per_s)
{
  if (!fresh_) {  // no write() since the last read(): component inactive, or first cycle
    if (exchange(kGetState, nullptr, 0, kReplyTimeout)) {
      misses_ = 0;
    } else if (!miss()) {
      return false;
    }
  }
  fresh_ = false;
  if (pos_.size() != ticks.size() || ticks_per_s.size() != ticks.size()) return false;
  for (std::size_t j = 0; j < ticks.size(); ++j) {
    ticks[j] = pos_[j];
    ticks_per_s[j] = vel_[j];
  }
  return true;
}

bool MotorBus::miss()
{
  return ++misses_ < kMaxMisses;
}

bool MotorBus::exchange(
  uint8_t type, const uint8_t * payload, std::size_t n, std::chrono::milliseconds timeout)
{
  const uint8_t seq = ++seq_;
  uint8_t out[LINK_MAX_ENCODED];
  const std::size_t len = link_encode_frame(seq, type, payload, n, out, sizeof out);
  if (len == 0 || !port_.write_all(out, len)) return false;

  const auto deadline = SerialPort::Clock::now() + timeout;
  uint8_t rseq = 0, rtype = 0, p[LINK_MAX_FRAME];
  while (port_.read_frame(rx_, deadline)) {
    const int m = link_decode_frame(rx_.data(), rx_.size(), &rseq, &rtype, p, sizeof p);
    if (m < 0 || rseq != seq) continue;  // corrupt, or a late reply to an earlier request
    if (rtype != kState || m < 1 || (m - 1) % 8 != 0) return false;  // ERROR reply or bad layout
    const std::size_t joints = static_cast<std::size_t>(m - 1) / 8;
    pos_.resize(joints);
    vel_.resize(joints);
    for (std::size_t j = 0; j < joints; ++j) {
      pos_[j] = link_get_i32(&p[j * 8]);
      vel_[j] = link_get_i32(&p[j * 8 + 4]);
    }
    flags_ = p[m - 1];
    return true;
  }
  return false;
}
}  // namespace my_robot_hardware
```

Add `src/link.c`, `src/serial_port.cpp` and `src/motor_bus.cpp` to the plugin library in
`CMakeLists.txt` (`project(... LANGUAGES C CXX)`), and keep `link.h` and `link.c` identical in the
firmware repository: copy them with a version comment, or share them as a git submodule.

## Checks

- **Bench, motors unpowered:** launch with `hardware:=real`;
  `ros2 control list_hardware_components -v` shows the component `active`; `ros2 topic hz
  /joint_states` matches the broadcaster rate; no "Joint read failed" lines.
- **Controller-manager overruns:** none in the log at the chosen `update_rate`. If they appear,
  raise the baud rate, shorten payloads, or lower the rate; do not raise `kReplyTimeout` past half
  the period.
- **Cable pull, wheels off the ground:** a forward command, then unplug. The firmware stops the
  motors within `CMD_TIMEOUT_MS`; the plugin logs the failure within `kMaxMisses` cycles; the
  component drops to `unconfigured` (the default `on_error`) and its controllers stop. Replug, then
  `ros2 control set_hardware_component_state my_robot_system active` configures (reopens the port)
  and activates it, which re-enables the firmware through `enable(true)`; reactivate the controllers.
- **Inactive component:** `ros2 control set_hardware_component_state my_robot_system inactive`
  releases the motors and `/joint_states` keeps updating from `GET_STATE`.
- **Directions:** one wheel revolution by hand moves its position by 6.28 rad with the sign the URDF
  axis predicts ([ros2-control](../../ros2-control/SKILL.md), step 6).

Sources: the ros2-control skill's plugin and seam (ros2_control 4.50 on Jazzy, 6.13 on Lyrical:
`read()`/`write()` errors deactivate the component); termios(3), poll(2).

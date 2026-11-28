# Serial ports on Linux

Part of [fw-serial-can](../SKILL.md). Names, permissions and latency for USB serial and on-board
UARTs on Ubuntu 24.04, and a raw POSIX port class for C++ nodes and plugins. Checked against the
kernel `ftdi_sio` driver and `serial-rs485` docs, termios(3) and pyserial 3.5.

## Names and permissions

- Use `/dev/serial/by-id/...` or a udev link (`/dev/my_robot_mcu`) in parameters, never
  `/dev/ttyUSB0` or `/dev/ttyACM0`: numbering follows probe order. Rules, matching by serial number
  or port path, and tests are in [ops-bringup udev.md](../../ops-bringup/references/udev.md).
- Serial devices are `root:dialout 0660` on Ubuntu: `sudo usermod -aG dialout $USER`, then log in
  again (or restart the service). Do not use `MODE="0666"`.
- MCUs on USB CDC-ACM (`ttyACM*`) can be probed by ModemManager with `AT` commands at plug-in: set
  `ENV{ID_MM_DEVICE_IGNORE}="1"` in their rule.
- On-board UARTs (`ttyS*`, `ttyAMA*`, `ttyTHS*`) may carry a login console; free the port from the
  kernel command line and `serial-getty@` first.

## Latency

- **FTDI adapters** hold received bytes up to the latency timer before sending them over USB. The
  driver keeps the chip's value, normally 16 ms, so a 100 Hz request/response loop misses every
  deadline. Set it to 1 ms when the adapter appears:

  ```udev
  # /etc/udev/rules.d/99-my-robot-ftdi.rules
  ACTION=="add", SUBSYSTEM=="usb-serial", DRIVER=="ftdi_sio", ATTR{latency_timer}="1"
  ```

  Check: `cat /sys/bus/usb-serial/devices/ttyUSB0/latency_timer` prints `1`.
- **CDC-ACM** (the MCU's own USB, as on RP2040, ESP32-S3 or Teensy boards): the baud rate setting
  does not limit the link and there is no FTDI-style timer; data moves in USB packets. Opening the
  port raises DTR, and Arduino-style boards reset on it, so wait for the board's first reply rather
  than sending at once.
- Budget the bytes: 8N1 costs 10 bit times per byte. At 115200 baud a 23-byte state reply plus a
  14-byte command take about 3.2 ms on the wire; at 100 Hz that is a third of the period. Raise the
  baud rate (both ends, within the UART clocks' error) or shrink the payload.

## RS-485 from Linux

USB RS-485 adapters switch the driver direction themselves. An on-board UART driving a transceiver
through RTS needs the kernel's RS-485 mode (`TIOCSRS485` with `SER_RS485_ENABLED` and
`SER_RS485_RTS_ON_SEND`, or the `rs485-*` device-tree properties), if its driver supports it;
pyserial exposes the same through `serial.rs485.RS485Settings`. The bus is half duplex: the host is
master, one request is outstanding at a time, and each slave has its own address byte.

## A raw port class for C++

Used by [serial-motor-bus.md](serial-motor-bus.md). Raw mode, exclusive, non-blocking reads with a
deadline; it returns whole 0x00-terminated frames.

```cpp
// include/my_robot_hardware/serial_port.hpp
#pragma once
#include <chrono>
#include <cstdint>
#include <string>
#include <vector>

namespace my_robot_hardware
{
class SerialPort
{
public:
  using Clock = std::chrono::steady_clock;
  ~SerialPort() { close(); }
  bool open(const std::string & path, int baud_rate);
  void close();
  bool is_open() const { return fd_ >= 0; }
  bool write_all(const uint8_t * data, std::size_t n);
  // One frame without its 0x00 delimiter, or false at the deadline or on a device error.
  bool read_frame(std::vector<uint8_t> & frame, Clock::time_point deadline);

private:
  int fd_{-1};
  std::vector<uint8_t> pending_;  // received bytes not yet split into frames
};
}  // namespace my_robot_hardware
```

```cpp
// src/serial_port.cpp
#include "my_robot_hardware/serial_port.hpp"

#include <fcntl.h>
#include <poll.h>
#include <sys/ioctl.h>
#include <termios.h>
#include <unistd.h>

#include <algorithm>
#include <cerrno>

namespace my_robot_hardware
{
namespace
{
speed_t to_speed(int baud)
{
  switch (baud) {
    case 115200: return B115200;
    case 230400: return B230400;
    case 460800: return B460800;
    case 921600: return B921600;
    case 1000000: return B1000000;
    default: return B0;
  }
}
}  // namespace

bool SerialPort::open(const std::string & path, int baud_rate)
{
  const speed_t speed = to_speed(baud_rate);
  if (speed == B0) return false;
  // O_NONBLOCK so open() never waits for carrier detect; cleared below
  fd_ = ::open(path.c_str(), O_RDWR | O_NOCTTY | O_NONBLOCK | O_CLOEXEC);
  if (fd_ < 0) return false;
  termios tio{};
  if (::ioctl(fd_, TIOCEXCL) != 0 || ::tcgetattr(fd_, &tio) != 0) { close(); return false; }
  ::cfmakeraw(&tio);  // 8 data bits, no parity, no echo, no CR/LF translation
  tio.c_cflag |= CLOCAL | CREAD;
  tio.c_cflag &= ~(CSTOPB | CRTSCTS);
  tio.c_cc[VMIN] = 0;  // read() returns what is there; poll() does the waiting
  tio.c_cc[VTIME] = 0;
  if (::cfsetispeed(&tio, speed) != 0 || ::cfsetospeed(&tio, speed) != 0 ||
      ::tcsetattr(fd_, TCSANOW, &tio) != 0)
  {
    close();
    return false;
  }
  ::fcntl(fd_, F_SETFL, ::fcntl(fd_, F_GETFL) & ~O_NONBLOCK);
  ::tcflush(fd_, TCIOFLUSH);  // drop boot messages and stale bytes
  pending_.clear();
  pending_.reserve(4096);
  return true;
}

void SerialPort::close()
{
  if (fd_ >= 0) ::close(fd_);
  fd_ = -1;
}

bool SerialPort::write_all(const uint8_t * data, std::size_t n)
{
  while (n > 0) {
    const ssize_t w = ::write(fd_, data, n);
    if (w < 0) {
      if (errno == EINTR) continue;
      return false;  // EIO: the USB device went away
    }
    data += w;
    n -= static_cast<std::size_t>(w);
  }
  return true;
}

bool SerialPort::read_frame(std::vector<uint8_t> & frame, Clock::time_point deadline)
{
  for (;;) {
    const auto zero = std::find(pending_.begin(), pending_.end(), uint8_t{0});
    if (zero != pending_.end()) {
      frame.assign(pending_.begin(), zero);
      pending_.erase(pending_.begin(), zero + 1);
      if (!frame.empty()) return true;
      continue;  // back-to-back delimiters
    }
    const auto left = std::chrono::ceil<std::chrono::milliseconds>(deadline - Clock::now());
    if (left.count() <= 0) return false;
    pollfd pfd{fd_, POLLIN, 0};
    if (::poll(&pfd, 1, static_cast<int>(left.count())) <= 0) return false;
    if (pfd.revents & (POLLERR | POLLHUP | POLLNVAL)) return false;
    uint8_t chunk[256];
    const ssize_t n = ::read(fd_, chunk, sizeof chunk);
    if (n <= 0) return false;
    pending_.insert(pending_.end(), chunk, chunk + n);
    if (pending_.size() > 4096) pending_.clear();  // noise with no delimiter
  }
}
}  // namespace my_robot_hardware
```

`poll()` has millisecond resolution; for timeouts under 2 ms use `ppoll()` with a `timespec`.

## Link tester

`serial_link_test.py` (pyserial, `GET_STATE` only, reports lost replies, CRC errors and round-trip
times) is in [serial-link-test.md](serial-link-test.md).

Sources: Linux `drivers/usb/serial/ftdi_sio.c` (latency timer default and sysfs attribute);
kernel docs `driver-api/serial/serial-rs485`; termios(3) and poll(2) man pages; pyserial 3.5
`serial/rs485.py`.

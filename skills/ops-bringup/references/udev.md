# Stable device names and permissions with udev

Part of [ops-bringup](../SKILL.md). Checked against the udev and udevadm man pages and the rules
shipped with systemd 255 (`60-serial.rules`, `60-persistent-v4l.rules`, `99-systemd.rules`), and
ModemManager's `80-mm-candidate.rules`.

## Use the names that already exist first

systemd's own rules already give every USB serial adapter and every camera stable links:

```bash
ls -l /dev/serial/by-id/ /dev/serial/by-path/    # ttyUSB*, ttyACM*
ls -l /dev/v4l/by-id/ /dev/v4l/by-path/          # video* nodes, with -video-index0/1
```

`by-id` is built from vendor, model and serial number, so it survives a move to another port.
`by-path` is built from the physical port, so it survives swapping two identical devices. A
parameter like `port: /dev/serial/by-id/usb-FTDI_FT232R_USB_UART_A1B2C3D4-if00-port0` is already
stable. Write your own rule when you want a short, role-based name (`/dev/my_robot/lidar`), a
`systemd` device unit, or ModemManager kept away.

## Find the attributes

```bash
udevadm info -q property -n /dev/ttyUSB0 | grep -E 'ID_VENDOR_ID|ID_MODEL_ID|ID_SERIAL_SHORT|ID_PATH='
udevadm info -a -n /dev/ttyUSB0 | grep -E 'idVendor|idProduct|serial' | head -6   # parent attributes
```

Check that the serial number is unique before you rely on it: many CP210x adapters report the
same `0001`, and CH340 adapters (`1a86:7523`) have no serial number at all. For those, match the
port path (`ID_PATH`) and label the port on the robot.

## Rules

```udev
# /etc/udev/rules.d/99-my-robot.rules
# Serial adapter with a unique serial number: name follows the device
SUBSYSTEM=="tty", ATTRS{idVendor}=="0403", ATTRS{idProduct}=="6001", ATTRS{serial}=="A1B2C3D4", \
  SYMLINK+="my_robot/imu"

# MCU on USB CDC-ACM: keep ModemManager from probing it with AT commands
SUBSYSTEM=="tty", ATTRS{idVendor}=="2e8a", ATTRS{idProduct}=="000a", ATTRS{serial}=="0123456789ABCDEF", \
  SYMLINK+="my_robot/motor", ENV{ID_MM_DEVICE_IGNORE}="1"

# Adapter without a usable serial number: name follows the physical port
SUBSYSTEM=="tty", ENV{ID_PATH}=="pci-0000:00:14.0-usb-0:3:1.0", SYMLINK+="my_robot/lidar"

# Camera: only the capture node (index 0), tagged so systemd sees it as a device unit
SUBSYSTEM=="video4linux", ATTRS{idVendor}=="046d", ATTRS{idProduct}=="0825", \
  ATTRS{serial}=="01234567", ATTR{index}=="0", SYMLINK+="my_robot/camera_front", TAG+="systemd"
```

The vendor, product and serial values are placeholders; use what `udevadm info` prints.

- **Permissions:** on Ubuntu serial ports are already `root:dialout 0660` and cameras
  `root:video 0660`, so the rules above set no `MODE`. Put the robot user in those groups instead
  of `MODE="0666"`, which opens the device to every account. Set `GROUP=` and `MODE="0660"` only
  for a device whose default group is wrong.
- **`ATTRS{...}`** matches the device or any parent (the USB device carries `idVendor`,
  `idProduct`, `serial`); `ATTR{...}` matches only the device itself (`index` on a video node).
- **USB cameras** create two video nodes; index 0 captures, index 1 carries metadata.
- **Depth cameras** used through libusb (RealSense and similar) are not opened by path: select
  them with the driver's serial-number parameter and install the vendor's own udev rules.
- **systemd device units:** tty devices are tagged `systemd` by default; video nodes are not,
  hence `TAG+="systemd"`. The unit name of a link is
  `systemd-escape -p --suffix=device /dev/my_robot/camera_front` (`dev-my_robot-camera_front.device`).

## Apply and test

```bash
sudo install -m 0644 host/99-my-robot.rules /etc/udev/rules.d/
sudo udevadm verify /etc/udev/rules.d/99-my-robot.rules     # syntax check, systemd 254+
sudo udevadm control --reload-rules
sudo udevadm trigger --action=add --subsystem-match=tty --subsystem-match=video4linux
ls -l /dev/my_robot/                                         # every link, pointing at the right node
udevadm test "$(udevadm info -q path -n /dev/ttyUSB0)" 2>&1 | grep -i my_robot   # why a rule did or did not match
```

Unplug and replug each device, then reboot once: the links must come back with the same targets.
Swap two identical adapters between ports when you matched by port: the names must follow the port.

## Waiting for devices

The service waits for the devices it cannot run without:

```ini
ExecStartPre=/usr/bin/udevadm wait --timeout=30 /dev/my_robot/motor /dev/my_robot/lidar
```

`udevadm wait` (systemd 251+) returns once the links exist and udev has processed them, and fails
after the timeout, which fails the start and lets `Restart=` try again. Optional devices are not
listed; their drivers retry and report through diagnostics. A device that must stop the robot when
it disappears can bind the unit instead: `BindsTo=dev-my_robot-motor.device` with
`After=dev-my_robot-motor.device`; the unit then stops when the device goes, and starts again only
when someone or something starts it.

## Traps

| Symptom | Cause | Fix |
|---|---|---|
| `/dev/ttyUSB0` is the lidar on one boot and the IMU on the next | Kernel numbering follows probe order | Use `/dev/serial/by-id/...` or a rule's `SYMLINK` in parameters |
| Two identical adapters fight for one link | Same or empty serial number | Match `ENV{ID_PATH}` and fix the port |
| `Permission denied` opening the port as the robot user | User not in `dialout`/`video`, or not since the last login or service start | `usermod -aG`, then restart the service |
| MCU on `ttyACM*` receives `AT` strings or resets at boot | ModemManager probes new serial ports | `ENV{ID_MM_DEVICE_IGNORE}="1"` in the rule, or remove `modemmanager` |
| Rule edited, nothing changes | Rules not reloaded, or `trigger` limited to `change` events | `udevadm control --reload-rules`, then `trigger --action=add` or replug |
| Camera link points at the metadata node | No `ATTR{index}=="0"` | Add it |
| Rule never matches | `ATTRS` values from a different parent than the one matched, or a typo in a key | `udevadm test` on the device; `udevadm verify` |

# Build, flash and capture output from the shell

Part of [fw-mcu](../SKILL.md). Checked on 2026-11-27 against the PlatformIO 6.2 docs, the
arduino-cli 1.6 docs, the ESP-IDF 6.1.1 docs and `idf.py` source, the esptool 5.7 migration
guide, the `pico-sdk` and `picotool` 2.3.1 sources, the Zephyr 4.5 getting started guide and runner
sources, and PJRC's `teensy_loader_cli` page. Nothing here was run.

Each recipe ends the same way: the build prints its memory use, the flasher exits 0, and the board
reports the new build ID.

## Before any flash

- **Port:** `/dev/serial/by-id/...` or the udev link `/dev/my_robot_mcu`
  ([ops-bringup udev](../../ops-bringup/references/udev.md)), never a bare `/dev/ttyACM0`.
- **Permissions:** the user in `dialout` (serial) and `plugdev` (probes, with the vendor's or
  PlatformIO's udev rules); log in again after `usermod`.
- **Motor power off,** or wheels off the ground: outputs float through reset and the bootloader.
- **Version pins:** record each tool's version in the project README; the commands below change
  between majors (esptool 5 renamed `write_flash` to `write-flash`).

## Build ID and capture

Give every build an ID and make the board print it, with the reset cause, at boot and on request:

```cmake
# CMake projects (ESP-IDF, Pico SDK, STM32 CMake, Zephyr): pass the git state to the code
execute_process(COMMAND git describe --always --dirty --tags
                OUTPUT_VARIABLE FW_BUILD_ID OUTPUT_STRIP_TRAILING_WHITESPACE)
add_compile_definitions(FW_BUILD_ID="${FW_BUILD_ID}")   # firmware prints "build=<id> reset=<cause>"
```

Interactive monitors (`idf.py monitor`, `pio device monitor`, `arduino-cli monitor`) need a
terminal and a key to exit; an agent captures for a fixed time instead:

```bash
PORT=/dev/my_robot_mcu
stty -F "$PORT" 115200 raw -echo          # baud is ignored by native USB CDC ports
timeout 5 cat "$PORT" | tee /tmp/fw.log    # timeout ends the read after 5 s
grep -m1 "build=$(git describe --always --dirty --tags)" /tmp/fw.log
```

A native USB port (Pico, STM32 USB, ESP32-S3 USB) can vanish and return during a reset; wait with
`udevadm wait --timeout=10 "$PORT"` before capturing. Opening the port resets Arduino AVR boards,
so the capture shows their boot banner.

## PlatformIO (ESP32, STM32, Teensy, AVR)

```ini
; platformio.ini
[platformio]
default_envs = esp32s3

[env]
monitor_speed = 115200
upload_port = /dev/my_robot_mcu
monitor_port = /dev/my_robot_mcu

[env:esp32s3]
platform = espressif32 @ 8.0.0        ; Arduino-ESP32 3.3.12 and ESP-IDF 6.1; before 8.0 it was Arduino 2.0.17
board = esp32-s3-devkitc-1
framework = arduino                   ; or espidf

[env:nucleo_f446re]
platform = ststm32                    ; pin to the version `pio pkg list` shows once it works
board = nucleo_f446re
framework = stm32cube
upload_protocol = stlink
debug_tool = stlink

[env:native]                          ; host unit tests of control and protocol code
platform = native
test_framework = unity
```

```bash
pio run -e esp32s3                     # build
pio run -e esp32s3 -t upload           # flash (upload_port above)
pio test -e native                     # unit tests on the host, no board
pio debug -e nucleo_f446re --interface=gdb -- -x .pioinit   # GDB session through the probe
```

PlatformIO's `raspberrypi` platform offers only the Arduino framework; Pico SDK projects use their
own CMake (below).

## arduino-cli (AVR, Teensy, Arduino-ESP32)

```bash
curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/master/install.sh | BINDIR=~/.local/bin sh
arduino-cli config init
URLS=https://espressif.github.io/arduino-esp32/package_esp32_index.json,https://www.pjrc.com/teensy/package_teensy_index.json
arduino-cli core update-index --additional-urls "$URLS"
arduino-cli core install arduino:avr                        # or esp32:esp32@3.3.13, teensy:avr
arduino-cli board listall --additional-urls "$URLS"         # find the FQBN, e.g. arduino:avr:mega
arduino-cli compile -b arduino:avr:mega --warnings all --output-dir build my_robot_firmware
arduino-cli upload -b arduino:avr:mega -p /dev/my_robot_mcu --input-dir build -t my_robot_firmware
```

The sketch folder and its `.ino` share the name `my_robot_firmware`. Teensy uploads through PJRC's
loader instead of a serial port:

```bash
teensy_loader_cli --mcu=TEENSY41 -w -v build/my_robot_firmware.ino.hex   # -s asks a running Teensy to reboot
```

Teensy on Linux also needs PJRC's `00-teensy.rules` in `/etc/udev/rules.d/`.

## ESP-IDF (`idf.py`)

ESP-IDF 6.x installs through the ESP-IDF Installation Manager (`eim`); the `install.sh` route is
the legacy method from before 6.0.

```bash
eim install -i v6.1.1                  # prints the activation command, e.g. source ~/.espressif/tools/activate_idf_v6.1.1.sh
source ~/.espressif/tools/activate_idf_v6.1.1.sh     # use the path eim printed
idf.py set-target esp32s3              # once; writes sdkconfig from sdkconfig.defaults
idf.py build                           # app, bootloader, partition table
idf.py -p /dev/my_robot_mcu flash      # esptool underneath; ESPPORT also sets the port
idf.py size                            # memory use; --format json2 for scripts (6.0 dropped json)
```

`sdkconfig.defaults` (committed) holds the options you changed, such as
`CONFIG_ESP_TASK_WDT_PANIC=y`; `sdkconfig` is generated. Flash a prebuilt image with esptool 5
directly:

```bash
idf.py merge-bin                       # one image: build/merged-binary.bin
esptool --chip esp32s3 -p /dev/my_robot_mcu -b 460800 write-flash 0x0 build/merged-binary.bin
```

esptool 5 renamed every command and option from `_` to `-` (`write-flash`, `--before
default-reset`); the old names and `esptool.py` still work with a warning until the next major.

## STM32 (STM32CubeMX + CMake)

STM32CubeMX (or STM32CubeMX2) generates a CMake project with a GCC toolchain file and
`CMakePresets.json`; STM32CubeCLT bundles GCC, CMake, Ninja and `STM32_Programmer_CLI`. Both are
under ST's SLA0048 licence; the generated HAL code is BSD-3-Clause.

```bash
cmake --list-presets                   # preset names differ between CubeMX versions
cmake --preset Debug && cmake --build --preset Debug
STM32_Programmer_CLI --connect port=swd --download build/Debug/my_robot_firmware.elf -rst
```

Without ST's tools, flash the same ELF through the Nucleo's ST-LINK with OpenOCD or probe-rs:

```bash
openocd -f interface/stlink.cfg -f target/stm32f4x.cfg \
  -c "program build/Debug/my_robot_firmware.elf verify reset exit"
probe-rs download --chip STM32F446RETx build/Debug/my_robot_firmware.elf   # chip names: probe-rs chip list
probe-rs reset --chip STM32F446RETx
```

## Raspberry Pi Pico SDK (RP2040, RP2350)

```bash
export PICO_SDK_PATH=~/pico-sdk        # a clone at tag 2.3.1, submodules updated
cmake -S . -B build -DPICO_BOARD=pico  # pico, pico_w, pico2, pico2_w
cmake --build build -j
picotool load -v -x build/my_robot_firmware.uf2 -f   # -f reboots a running SDK app into BOOTSEL first
```

`-f` works when the running firmware links `pico_stdio_usb` (its reset interface is on by
default); otherwise hold BOOTSEL while plugging in, or copy the UF2 to the `RPI-RP2` drive. With
several boards, pick one with `--ser <serial>`. With a Debug Probe:

```bash
openocd -f interface/cmsis-dap.cfg -f target/rp2040.cfg -c "adapter speed 5000" \
  -c "program build/my_robot_firmware.elf verify reset exit"
```

OpenOCD 0.12.0 (the Ubuntu 24.04 package) has `target/rp2040.cfg` but no RP2350 target; use
Raspberry Pi's OpenOCD build or probe-rs for RP2350.

## Zephyr (`west`)

```bash
python3 -m venv ~/zephyrproject/.venv && source ~/zephyrproject/.venv/bin/activate
pip install west
west init -m https://github.com/zephyrproject-rtos/zephyr --mr v4.5.0 ~/zephyrproject
cd ~/zephyrproject && west update && west packages pip --install && west zephyr-export
(cd zephyr && west sdk install)
west build -p auto -b nucleo_f446re my_robot_firmware      # rpi_pico; esp32s3_devkitc/esp32s3/procpu
west flash                                                   # board's default runner
west flash --runner openocd                                  # or probe-rs, stm32cubeprogrammer, jlink
```

ESP32 boards also need `west blobs fetch hal_espressif` (Espressif's binary radio and PHY
libraries, under their own licence). An application repository can carry its own `west.yml`
manifest pinning the Zephyr revision.

## Traps

| Symptom | Cause | Fix |
|---|---|---|
| `Permission denied` on the port or probe | User not in `dialout`/`plugdev`, or no udev rules for the probe | Groups, vendor or PlatformIO udev rules, log in again |
| esptool: `Failed to connect` | Board not in download mode, or the port is held by a monitor | Close other readers; hold BOOT while resetting; lower `-b` |
| Flash succeeds, board runs the old code | Wrong port or board among several | Select by serial (`--ser`, by-id path); check the build ID |
| `externally-managed-environment` from pip | Ubuntu 24.04 protects the system Python (PEP 668) | pipx, a venv, or the tool's own installer |
| `idf.py`: command not found in a new shell | Activation script not sourced | Source the path `eim` printed, in each shell or CI step |
| Pico SDK: `PICO_BOARD` warnings, wrong flash size | Board not set | `-DPICO_BOARD=...` on the first configure; delete `build/` when changing it |
| OpenOCD: `init mode failed` on STM32 | Firmware sleeps or reuses the SWD pins | Connect under reset (NRST wired): `-c "reset_config srst_only srst_nogate connect_assert_srst"` |

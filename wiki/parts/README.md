# Parts

Profiles of the parts robots are built from. Template: [templates/part.md](../../templates/part.md).

| Folder | Holds |
|---|---|
| `actuators/` | Servos, BLDC and stepper motors, gearboxes, linear actuators |
| `mcu/` | Microcontrollers and development boards |
| `drivers/` | Motor drivers and controllers |
| `sensors/` | Cameras, lidars, IMUs, encoders, force-torque sensors |
| `compute/` | Single-board computers and edge AI modules |
| `power/` | Batteries, BMS, regulators, e-stop parts |
| `materials/` | Filaments, sheet stock, fasteners |

- Name a file `<maker>-<model>.md`: `feetech-sts3215.md`, `espressif-esp32-s3.md`.
- Put units in spec keys (`stall_torque_kgcm`, `voltage_v`) so tables can compare them.
- Every price is dated and sourced.
- The index below lists the robots that use each part, read from the robot profiles' `stack`.

## Index

<!-- index:start -->
| Part | Category | Subcategory | Interfaces | Cost (USD) | Used in | Verified |
|---|---|---|---|---|---|---|
| [Arduino Mega 2560 Rev3](mcu/arduino-mega-2560.md) | mcu | mcu-board | uart, i2c, spi, usb | 49.9 (2026-11-27) | [BCN3D Moveo](../robots/bcn3d-moveo.md), [InMoov](../robots/inmoov.md), [Thor (AngelLM)](../robots/angellm-thor.md) | 2026-11-27 |
| [Espressif ESP32-S3](mcu/espressif-esp32-s3.md) | mcu | wireless-mcu | uart, i2c, spi, can, usb, wifi, bluetooth, sdio | 19.95 (2026-11-27) | [Aero Hand Open](../robots/aero-hand-open.md), [Coglet](../robots/coglet.md), [Sesame](../robots/sesame.md), [Stack-chan](../robots/stack-chan.md) | 2026-11-27 |
| [PJRC Teensy 4.1](mcu/pjrc-teensy-4-1.md) | mcu | mcu-board | uart, i2c, spi, can, usb, ethernet, sdio | 31.5 (2026-11-27) | — | 2026-11-27 |
| [Raspberry Pi RP2040](mcu/raspberry-pi-rp2040.md) | mcu | mcu | uart, i2c, spi, usb | 4.0 (2026-11-27) | [Coglet](../robots/coglet.md), [Kayra](../robots/kayra.md) | 2026-11-27 |
| [ROBOTIS OpenCR 1.0](mcu/robotis-opencr.md) | mcu | robot-controller | uart, i2c, spi, can, usb | 247.14 (2026-11-27) | [OpenManipulator-X](../robots/openmanipulator-x.md), [ROBOTIS OP3](../robots/robotis-op3.md), [TurtleBot3](../robots/turtlebot3.md) | 2026-11-27 |
| [ST NUCLEO-F446RE](mcu/st-nucleo-f446re.md) | mcu | dev-board | uart, i2c, spi, can, usb | 18.82 (2026-11-27) | — | 2026-11-27 |
<!-- index:end -->

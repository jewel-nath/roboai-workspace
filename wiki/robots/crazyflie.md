---
type: robot
name: Bitcraze Crazyflie 2.x
summary: Bitcraze's palm-sized open quadcopter (Crazyflie 2.1+ and 2.1 Brushless, with 2.0, 2.1 and 1.0 as history), with GPL firmware, published schematics and the Crazyswarm2 ROS 2 stack; the standard nano-drone for swarm and learning research.
tags: [drone, quadcopter, nano-drone, swarm, stm32, nrf51, crazyswarm2, ros2, mujoco, bitcraze]
category: other
tier: B
openness: partial
maker: Bitcraze AB
year: 2014
license: {hardware: , software: GPL-3.0-only, docs: }
links: {repo: "https://github.com/bitcraze/crazyflie-firmware", docs: "https://www.bitcraze.io/documentation/repository/crazyflie-firmware/master/", cad: , paper: "https://doi.org/10.1109/ICRA.2017.7989376", site: "https://www.bitcraze.io/products/crazyflie-2-1-plus/"}
specs: {dof: 4, payload_kg: 0.015, reach_mm: , mass_kg: 0.029, size_mm: "92 x 92 x 29", speed_mps: , runtime_h: 0.12}
stack: {actuators: "four motors with 47-17 propellers (2.1+); four 08028-10000KV brushless motors (2.1 Brushless)", mcu: "STM32F405 (application) and nRF51822 (radio and power)", compute: , sensors: ["BMI088 accelerometer and gyroscope", "BMP388 pressure sensor"], sim_models: ["MJCF (MuJoCo Menagerie, bitcraze_crazyflie_2)", "URDF (crazyswarm2 crazyflie_description)", "crazyflie_sim with the firmware in the loop (crazyswarm2)"], ros2: community}
cost: {type: retail, usd: 262.20, as_of: 2026-11-18, source: "https://www.robotshop.com/products/bitcraze-crazyflie-21"}
build: {difficulty: , hours: , print_hours: }
maturity: {last_commit: 2026-11-16, stars: 1577, active: true}
use_cases: [research, education, reinforcement-learning, navigation, hobby]
evidence: researched
last_verified: 2026-11-18
sources:
  - {url: "https://www.bitcraze.io/products/crazyflie-2-1-plus/", title: "Bitcraze: Crazyflie 2.1+ product page", accessed: 2026-11-18}
  - {url: "https://www.bitcraze.io/products/crazyflie-2-1-brushless/", title: "Bitcraze: Crazyflie 2.1 Brushless product page", accessed: 2026-11-18}
  - {url: "https://www.bitcraze.io/products/old-products/crazyflie-2-1/", title: "Bitcraze: Crazyflie 2.1 (discontinued) product page", accessed: 2026-11-18}
  - {url: "https://www.robotshop.com/products/bitcraze-crazyflie-21", title: "RobotShop US: Bitcraze Crazyflie 2.1+", accessed: 2026-11-18}
  - {url: "https://github.com/bitcraze/crazyflie-firmware", title: "crazyflie-firmware repository", accessed: 2026-11-18}
  - {url: "https://www.bitcraze.io/open-source-philosophy/", title: "Bitcraze: open source philosophy", accessed: 2026-11-18}
  - {url: "https://github.com/IMRCLab/crazyswarm2", title: "Crazyswarm2 repository and docs", accessed: 2026-11-18}
  - {url: "https://crazyswarm.readthedocs.io/en/latest/", title: "Crazyswarm (version 1) documentation, citing Preiss et al., ICRA 2017", accessed: 2026-11-18}
  - {url: "https://github.com/google-deepmind/mujoco_menagerie/tree/main/bitcraze_crazyflie_2", title: "MuJoCo Menagerie: bitcraze_crazyflie_2", accessed: 2026-11-18}
  - {url: "https://en.wikipedia.org/wiki/Crazyflie_2.0", title: "Wikipedia: Crazyflie 2.0", accessed: 2026-11-18}
---

# Bitcraze Crazyflie 2.x

The Crazyflie is a 29 g palm-sized quadcopter from Bitcraze, sold as a development platform with open
firmware and published schematics [1][6]. The 2.0 came out in December 2014 [10]; the current models are
the Crazyflie 2.1+ and the larger Crazyflie 2.1 Brushless [1][2]. For a builder it is the standard small
drone for swarm, control and learning research, with a ROS 2 stack (Crazyswarm2) and a MuJoCo model [7][9].

## Specs

| Item | Value | Source |
|---|---|---|
| Variant in frontmatter | Crazyflie 2.1+; four motors, `dof: 4` | 1 |
| Mass, size | 29 g at takeoff; 92 x 92 x 29 mm motor to motor (maker's claims) | 1 |
| Payload, flight | 15 g recommended; about 7 min flight (0.12 h) and 40 min charge on the stock battery (maker's claims) | 1 |
| MCUs | STM32F405 (Cortex-M4, 168 MHz, 1 MB flash) for flight; nRF51822 (Cortex-M0) for radio and power | 1 |
| Sensors | BMI088 accelerometer and gyroscope; BMP388 pressure sensor | 1 |
| Radio | 2.4 GHz with Bluetooth LE, 20 dBm amplifier; over 1 km line of sight with a Crazyradio PA (maker's claim) | 1 |

## How it works

Two microcontrollers split the work: the STM32F405 is the main application MCU that runs the flight
code, and the nRF51822 handles the radio and power [1]. A PC talks to the drone over the Crazyradio PA
USB dongle or Bluetooth LE [1][7]. Add-on boards called decks plug on top, and Bitcraze publishes a
KiCad template for making your own deck [6]. The firmware in `crazyflie-firmware` serves the Crazyflie 2.x family; the 2017.06
release was the last to support the 1.0 [5]. It also builds Python bindings of the firmware, which
Crazyswarm2's simulator uses to run the real flight code in the loop [5][7].

Crazyswarm2 is a ROS 2 stack (Humble or Jazzy) for drones with Bitcraze flight computers. Its server
links many Crazyflies over one or more Crazyradio dongles, maps firmware parameters and logs to ROS 2,
and offers takeoff, land, go-to and trajectory services; its backends are C++, Python (cflib) or the
simulator [7]. It replaces Crazyswarm, which flew 49 Crazyflies on three Crazyradios and is tuned for
motion capture [8]. MuJoCo Menagerie has an MJCF model with a 27 g mass, derived from the ROS description [9].

| Variant | Status | Mass | Payload | Flight time | Source |
|---|---|---|---|---|---|
| Crazyflie 1.0 | First generation; firmware support ended at release 2017.06 | | | | 5 |
| Crazyflie 2.0 | Released December 2014 | | | | 10 |
| Crazyflie 2.1 | Discontinued, replaced by the 2.1+ | 29 g | 15 g | 7 min | 3 |
| Crazyflie 2.1+ | Current; new battery and propellers, up to 15% better flight performance (maker's claim) | 29 g | 15 g | 7 min | 1 |
| Crazyflie 2.1 Brushless | Current; 100 mm frame, 08028 brushless motors of up to 30 g thrust each | 34 g with legs | 40 g | 10 min | 2 |

## What it is used for

- **Swarms:** Crazyswarm flew 49 Crazyflies at once; Crazyswarm2 carries this work to ROS 2 [7][8].
- **Control and learning research:** the firmware-in-the-loop simulator and the MuJoCo model let
  controllers and policies be tested before flight [7][9].
- **Indoor flight labs:** at 29 g it flies indoors, tracked by motion capture, Lighthouse or LPS [1][8].

## Cost and BOM

The Crazyflie 2.1+ costs **$262.20** at RobotShop US on 2026-11-18 (type `retail`) [4]. Bitcraze's own
store refused automated reads, so its price was not checked.

## What is open

| Item | Format | Where | Licence |
|---|---|---|---|
| Flight firmware | C | [crazyflie-firmware](https://github.com/bitcraze/crazyflie-firmware) [5] | GPL-3.0 in LICENSE and source headers; the README says LGPL-3.0 |
| Schematics, datasheets | PDF | bitcraze.io product pages [1][6] | None found; layouts, Gerbers and BOM are not published |
| Deck template | KiCad | Bitcraze [6] | Not checked |
| ROS 2 stack and simulator | ROS 2 | [crazyswarm2](https://github.com/IMRCLab/crazyswarm2) [7] | MIT |
| MuJoCo model | MJCF | Menagerie `bitcraze_crazyflie_2` [9] | MIT |

## Strengths and limits

- **Strengths:** open firmware with a firmware-in-the-loop simulator [5][7]; a maintained ROS 2 swarm
  stack [7]; a Menagerie model [9]; a retail price under $300 [4].
- **Limits:** 15 g payload and about 7 min flight on the 2.1+ [1]; editable hardware files are not
  published [6]; the firmware licence is stated two ways [5]; Crazyswarm2 is a lab project [7].

## Related robots

- [OpenBot](openbot.md): another cheap research platform for learned control, on the ground.
- [TurtleBot](turtlebot.md): the ground robot many of the same labs use to learn ROS 2.

## Sources

1. [Bitcraze: Crazyflie 2.1+ product page](https://www.bitcraze.io/products/crazyflie-2-1-plus/), accessed 2026-11-18
2. [Bitcraze: Crazyflie 2.1 Brushless product page](https://www.bitcraze.io/products/crazyflie-2-1-brushless/), accessed 2026-11-18
3. [Bitcraze: Crazyflie 2.1 (discontinued) product page](https://www.bitcraze.io/products/old-products/crazyflie-2-1/), accessed 2026-11-18
4. [RobotShop US: Bitcraze Crazyflie 2.1+](https://www.robotshop.com/products/bitcraze-crazyflie-21), accessed 2026-11-18
5. [crazyflie-firmware repository](https://github.com/bitcraze/crazyflie-firmware), accessed 2026-11-18
6. [Bitcraze: open source philosophy](https://www.bitcraze.io/open-source-philosophy/), accessed 2026-11-18
7. [Crazyswarm2 repository and docs](https://github.com/IMRCLab/crazyswarm2), accessed 2026-11-18
8. [Crazyswarm (version 1) documentation, citing Preiss et al., ICRA 2017](https://crazyswarm.readthedocs.io/en/latest/), accessed 2026-11-18
9. [MuJoCo Menagerie: bitcraze_crazyflie_2](https://github.com/google-deepmind/mujoco_menagerie/tree/main/bitcraze_crazyflie_2), accessed 2026-11-18
10. [Wikipedia: Crazyflie 2.0](https://en.wikipedia.org/wiki/Crazyflie_2.0), accessed 2026-11-18

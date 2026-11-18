---
type: robot
name: Hello Robot Stretch (RE1, Stretch 2, Stretch 3, Stretch 4)
summary: Hello Robot's light home mobile manipulator with a lift and a telescoping arm on a small base (Stretch 3, 24.5 kg, $24,950 in 2024), a popular home-robotics research platform with open ROS 2 and Python software, GPL firmware, Apache accessory CAD and non-commercial robot-part CAD; Stretch 4 now replaces it on sale.
tags: [telescoping-arm, home-robot, assistive, ros2, python, mujoco, dynamixel, hello-robot]
category: mobile-manipulator
tier: B
openness: partial
maker: Hello Robot
year:
license: {hardware: CC-BY-NC-SA-4.0 AND Apache-2.0, software: Apache-2.0 AND LGPL-3.0-only AND GPL-3.0-only AND BSD-3-Clause-Clear, docs: }
links: {repo: "https://github.com/hello-robot/stretch_ros2", docs: "https://docs.hello-robot.com", cad: "https://github.com/hello-robot/stretch_tool_share", paper: "https://arxiv.org/abs/2109.10892", site: "https://hello-robot.com"}
specs: {dof: 8, payload_kg: 2, reach_mm: 520, mass_kg: 24.5, size_mm: "330 x 340 x 1410", speed_mps: , runtime_h: 2}
stack: {actuators: "closed-loop steppers on the lift (belt drive, with brake) and the five-link telescoping arm; Dynamixel XC430, XM540 and XM430 in the wrist; Dynamixel XL430 gripper; Dynamixel head pan and tilt; differential-drive base", mcu: "Arduino-based boards: Mechaduino-derived stepper controllers, a power and IMU board (Pimu) and a wrist board (Wacc) with an Atmel SAMD21", compute: , sensors: ["Intel RealSense D435if in the head", "wide-angle RGB camera in the head", "Intel RealSense D405 at the gripper", "ReSpeaker 4-mic array", "BNO085 9-DoF IMU in the base", "4 cliff sensors", "ADXL343 wrist accelerometer"], sim_models: ["URDF (hello-robot/stretch_ros2 stretch_description, BSD-3-Clause-Clear)", "MuJoCo driven through ROS 2 (stretch_ros2 stretch_simulation)", "MJCF (MuJoCo Menagerie hello_robot_stretch_3)", "MJCF of Stretch 2 (MuJoCo Menagerie hello_robot_stretch)"], ros2: official}
cost: {type: retail, usd: 24950, as_of: 2024-02-15, source: "https://www.therobotreport.com/stretch-3-mobile-manipulator-hello-robot-designed-open-source-development/"}
build: {difficulty: , hours: , print_hours: }
maturity: {last_commit: 2026-10-06, stars: 129, active: true}
use_cases: [research, manipulation, navigation, hri, teleop]
evidence: researched
last_verified: 2026-11-18
sources:
  - {url: "https://www.therobotreport.com/stretch-3-mobile-manipulator-hello-robot-designed-open-source-development/", title: "The Robot Report: Stretch 3 mobile manipulator from Hello Robot (2024-02-15)", accessed: 2026-11-18}
  - {url: "https://docs-arch.hello-robot.com/0.3/hardware/hardware_guide_stretch_3/", title: "Hello Robot docs (archive): Stretch 3 hardware guide", accessed: 2026-11-18}
  - {url: "https://hello-robot.com/purchase", title: "Hello Robot: purchase page", accessed: 2026-11-18}
  - {url: "https://hello-robot.com/wp-content/uploads/2026/05/HelloRobot-DataSheet-Stretch-4-Rev5_AsLaunched.pdf", title: "Hello Robot: Stretch 4 data sheet (Rev 5, as launched)", accessed: 2026-11-18}
  - {url: "https://arxiv.org/abs/2109.10892", title: "Kemp et al.: The design of Stretch, a compact, lightweight mobile manipulator for indoor human environments (ICRA 2022)", accessed: 2026-11-18}
  - {url: "https://github.com/hello-robot/stretch_ros2", title: "hello-robot/stretch_ros2 (humble)", accessed: 2026-11-18}
  - {url: "https://github.com/hello-robot/stretch_body", title: "hello-robot/stretch_body", accessed: 2026-11-18}
  - {url: "https://github.com/hello-robot/stretch_firmware", title: "hello-robot/stretch_firmware", accessed: 2026-11-18}
  - {url: "https://github.com/hello-robot/stretch_tool_share", title: "hello-robot/stretch_tool_share", accessed: 2026-11-18}
  - {url: "https://github.com/google-deepmind/mujoco_menagerie", title: "MuJoCo Menagerie: hello_robot_stretch and hello_robot_stretch_3", accessed: 2026-11-18}
---

# Hello Robot Stretch

A light mobile manipulator from Hello Robot, grown from Georgia Tech prototypes: a lift and a
telescoping arm on a 34 cm-wide two-wheeled base, sized for homes [5]. Stretch 3 sold for $24,950 in
2024 [1]; the purchase page now lists only Stretch 4 [3]. Open ROS 2 and Python software, firmware
and accessory CAD make it a common platform for home and assistive robotics research [1][6][7][8][9].

## Specs

| Item | Value | Source |
|---|---|---|
| Variant in frontmatter | Stretch 3 | [1][2] |
| Degrees of freedom | 8 counted: lift, telescoping arm, wrist yaw, pitch and roll, gripper, head pan and tilt; the two drive wheels are not counted | [2] |
| Payload, reach | 2 kg recommended maximum; arm reach 0.52 m (maker's claims) | [1][2] |
| Mass, size, runtime | 24.5 kg; 33 x 34 x 141 cm; 2 to 5 h, the frontmatter uses 2 h (maker's claims) | [1] |
| Lift and arm | closed-loop steppers; belt-driven lift with a brake; five telescoping aluminium links | [2] |
| Wrist, gripper | Dynamixel yaw (+256/−76°), pitch (+20/−90°) and roll (±172.5°); gripper on a Dynamixel XL430 with a RealSense D405 | [2] |
| Head, base | head pan 346°, tilt 115°, RealSense D435if, wide-angle camera, 4-mic array; differential base on 4 in wheels, BNO085 IMU, four cliff sensors | [2] |
| Speed, computer | not found in the sources read | — |

## How it works

The RE1 base is narrower than a person's hips, the gripper reaches from floor to 110 cm, and base,
lift and arm move in Cartesian axes, with static stability modelled to set loads [5]. Lift and arm
use closed-loop steppers on Mechaduino-derived boards; wrist and head use Dynamixel servos [2][8].

`stretch_body` is the Python API for Stretch 1 to 3; Stretch 4 has `stretch4_body` [7]. `stretch_ros2`
holds ROS 2 Humble drivers, calibration, Nav2, RTAB-Map, FUNMAP, perception demos and a MuJoCo
simulation bridge, last changed on 2026-10-06 [6]. Arduino firmware runs the stepper, wrist and base
boards [8]. Menagerie holds Hello Robot's MJCF models of Stretch 2 and Stretch 3 [10].

| Variant | Main differences | Source |
|---|---|---|
| Stretch RE1 | first product, after prototypes until May 2020; 23 kg, 34 cm wide; extensions: 1-DoF stow wrist, 2-DoF dexterous wrist; $20,000 in the paper's comparison table | [5] |
| Stretch 2 | MJCF and STEP models published | [9][10] |
| Stretch 3 | three-axis dexterous wrist and a D405 at the gripper; $24,950 in 2024 | [1][2] |
| Stretch 4 | three-wheel omni base; 9 DoF by the maker's count; 2.5 kg arm extended, 4 kg retracted; 46 kg; 160 cm; 8 h on a swappable 512 Wh LiFePO4 pack; Intel NUC 15 and Jetson Orin NX; two 3D lidars; $29,950 | [3][4] |

## What it is used for

- Home and assistive robotics: teleoperated and autonomous tasks in real homes [5].
- An open research community in over 14 countries that shares code, data and models [1].
- Simulation and learning in MuJoCo, with Menagerie models and a ROS 2 bridge [6][10].

## Cost and BOM

Stretch 3: retail $24,950 at launch on 2024-02-15 [1]. Stretch 4: $29,950 on the purchase page on
2026-11-18, which offers no upgrades from older Stretches; Stretch 3 sales were not confirmed [3].

## What is open

| Item | Format | Where | Licence |
|---|---|---|---|
| ROS 2 packages | ROS 2 Humble, URDF | [stretch_ros2](https://github.com/hello-robot/stretch_ros2) [6] | Apache-2.0; calibration GPL-3.0; FUNMAP LGPL-3.0; description BSD-3-Clause-Clear |
| Python API and tools | Python packages | [stretch_body](https://github.com/hello-robot/stretch_body) [7] | LGPL-3.0 (body), Apache-2.0 (tools) |
| Firmware, RE1 stepper board | Arduino; schematic, BOM, Gerbers | [stretch_firmware](https://github.com/hello-robot/stretch_firmware) [8] | GPL-3.0 |
| Robot-part and accessory CAD | STEP, STL, SolidWorks, xacro | [stretch_tool_share](https://github.com/hello-robot/stretch_tool_share) [9] | robot parts CC BY-NC-SA 4.0, non-commercial, patents not licensed; accessories Apache-2.0 |
| MuJoCo models | MJCF | [Menagerie](https://github.com/google-deepmind/mujoco_menagerie) [10] | Stretch 2 Clear BSD; Stretch 3 Apache-2.0 |

## Strengths and limits

- **Strengths:** 24.5 kg and about 34 cm wide, sized for homes [1][5]; predictable Cartesian motion
  of lift and arm [5]; open software and firmware, with official ROS 2 [6][7][8].
- **Limits:** 2 kg payload [2]; a two-wheeled base that cannot move sideways [2]; robot-part CAD is
  non-commercial and patented [9]; Stretch 3 may no longer be sold [3]; software licences are mixed [6][7].

## What to reuse

- A lift plus a telescoping arm on a narrow base: Cartesian reach from floor to counter, low mass [5].

## Related robots

- [Fetch](fetch.md), [TIAGo](tiago.md), [PR2](pr2.md): larger research mobile manipulators.
- [TidyBot](tidybot.md): an open holonomic base for home mobile manipulation research.

## Sources

1. [The Robot Report: Stretch 3 mobile manipulator from Hello Robot (2024-02-15)](https://www.therobotreport.com/stretch-3-mobile-manipulator-hello-robot-designed-open-source-development/), accessed 2026-11-18
2. [Hello Robot docs (archive): Stretch 3 hardware guide](https://docs-arch.hello-robot.com/0.3/hardware/hardware_guide_stretch_3/), accessed 2026-11-18
3. [Hello Robot: purchase page](https://hello-robot.com/purchase), accessed 2026-11-18
4. [Hello Robot: Stretch 4 data sheet (Rev 5, as launched)](https://hello-robot.com/wp-content/uploads/2026/05/HelloRobot-DataSheet-Stretch-4-Rev5_AsLaunched.pdf), accessed 2026-11-18
5. [Kemp et al.: The design of Stretch, a compact, lightweight mobile manipulator for indoor human environments (ICRA 2022)](https://arxiv.org/abs/2109.10892), accessed 2026-11-18
6. [hello-robot/stretch_ros2 (humble)](https://github.com/hello-robot/stretch_ros2), accessed 2026-11-18
7. [hello-robot/stretch_body](https://github.com/hello-robot/stretch_body), accessed 2026-11-18
8. [hello-robot/stretch_firmware](https://github.com/hello-robot/stretch_firmware), accessed 2026-11-18
9. [hello-robot/stretch_tool_share](https://github.com/hello-robot/stretch_tool_share), accessed 2026-11-18
10. [MuJoCo Menagerie: hello_robot_stretch and hello_robot_stretch_3](https://github.com/google-deepmind/mujoco_menagerie), accessed 2026-11-18

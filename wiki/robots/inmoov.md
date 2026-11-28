---
type: robot
name: InMoov
summary: Life-size 3D-printed humanoid by sculptor Gaël Langevin, started in 2012, built from ABS parts that fit a 12 cm printer, hobby servos with tendon-driven fingers, Arduino Mega boards and the MyRobotLab software; its STL files are CC-BY-NC-3.0, so non-commercial only.
tags: [3d-printed, life-size, hobby-servo, tendon-hand, arduino-mega, myrobotlab, non-commercial, maker, upper-body]
category: humanoid
tier: B
openness: partial
maker: Gaël Langevin
year: 2012
license: {hardware: CC-BY-NC-3.0, software: Apache-2.0, docs: }
links: {repo: "https://github.com/MyRobotLab/InMoov2", docs: "https://inmoov.fr/default-hardware-map/", cad: "https://inmoov.fr/inmoov-stl-parts-viewer/", paper: , site: "https://inmoov.fr"}
specs: {dof: , payload_kg: , reach_mm: , mass_kg: , size_mm: , speed_mps: , runtime_h: }
stack: {actuators: "hobby servos: HK15298B (fingers, jaw, neck), MG996R (wrists), Hitec HS-805BB (shoulders, arms, head, stomach), DS929HV (eyes)", mcu: [arduino-mega-2560, "2 x Arduino Mega with Nervo servo boards"], compute: "PC running MyRobotLab; the maker's current build uses an Intel NUC (8th-gen i7)", sensors: ["Kinect 360 or OAK-D-Lite depth camera", "webcam in the head", "PIR sensor", "2 x HC-SR04 ultrasonic sensors", "finger pressure sensors"], sim_models: ["InMoov2 simulator in MyRobotLab (WebXR)", "URDF/xacro with ros2_control and Gazebo (community inmoov_urdf, ROS 2 Jazzy)"], ros2: community}
cost: {type: , usd: , as_of: , source: }
build: {difficulty: 3, hours: , print_hours: }
maturity: {last_commit: 2026-06-11, stars: 37, active: true}
use_cases: [hobby, education, hri, research]
evidence: researched
last_verified: 2026-11-18
sources:
  - {url: "https://inmoov.fr/project/", title: InMoov project page (inmoov.fr), accessed: 2026-11-18}
  - {url: "https://inmoov.fr/default-hardware-map/", title: InMoov default hardware map and BOM, accessed: 2026-11-18}
  - {url: "https://inmoov.fr/inmoov-stl-parts-viewer/", title: InMoov STL parts library, accessed: 2026-11-18}
  - {url: "https://github.com/MyRobotLab/myrobotlab", title: MyRobotLab repository, accessed: 2026-11-18}
  - {url: "https://github.com/MyRobotLab/InMoov2", title: InMoov2 service for MyRobotLab, accessed: 2026-11-18}
  - {url: "https://github.com/Sentience-Robotics/inmoov_urdf", title: "Sentience Robotics inmoov_urdf (community ROS 2 description)", accessed: 2026-11-18}
  - {url: "https://makezine.com/2015/06/19/in-our-image/", title: "Make: InMoov, the life-size humanoid robot you can print at home (2015)", accessed: 2026-11-18}
---

# InMoov

A life-size humanoid that can be printed on a home 3D printer, designed by the French sculptor and
designer Gaël Langevin since January 2012 [1]. It began as a printed prosthetic hand [7] and grew
into a torso, arms and head on hobby servos, run by Arduino boards and the MyRobotLab software
[2][4]. Langevin calls it the first open-source 3D-printed life-size robot [1]. Its files are
CC-BY-NC-3.0: **non-commercial use only** [1][3].

## Specs

| Item | Value | Source |
|---|---|---|
| Variant in frontmatter | the default upper body in the hardware map (BOM marked updated 04/05/2016) | [2] |
| Printer needed | 12 x 12 x 12 cm build volume | [1] |
| Servos listed | 31: hands and wrists 12, arms and shoulders 8, head, jaw, eyes and neck 7, stomach 4 | [2] |
| Degrees of freedom | not published; it depends on the build, so `dof` is empty | [2] |
| Fingers | pulled by servos through braided fishing line | [2] |
| Controllers | 2 Arduino Mega boards with Nervo servo boards | [2] |
| Computer | a PC running MyRobotLab; the maker uses an Intel NUC (8th-gen i7 8550, 32 GB RAM) | [2] |
| Sensors | Kinect 360 or OAK-D-Lite, webcam, PIR sensor, 2 ultrasonic sensors, finger pressure sensors | [2] |
| Power | one 6 V 12 Ah battery, or a 6 V switching supply for all-day use | [2] |
| Height, mass | not published | — |

## How it works

The body is printed in ABS in parts small enough for a 12 cm printer [1][2]. Hobby servos in the
forearm pull each finger through braided line; big Hitec HS-805BB servos move the shoulders, arms
and head, and smaller servos work the jaw, eyes and neck [2][3]. The parts library now lists legs,
an i2 head and i2 hands, while the 2016 hardware map still says legs and waist were to come [2][3].

Two Arduino Megas on Nervo boards drive the servos, and a PC runs MyRobotLab, a Java framework with a
web interface [2][4]. The InMoov2 service adds gestures, a chatbot, configuration and a state
machine with telepresence and sleep modes [5]. MyRobotLab ships a WebXR InMoov2 simulator [4].
There is no official ROS package; Sentience Robotics keeps an InMoov-derived ROS 2 Jazzy
description with ros2_control and Gazebo [6].

## What it is used for

- Hobby and school builds, part by part; Langevin told Make of families building one on Sundays [7].
- Prosthetics: Langevin redesigned the hand for the Bionico open prosthetics project [7].
- Human-robot interaction and telepresence demos through MyRobotLab [4][5].
- A base for research robots, such as the ROS 2 description behind Sentience Robotics' Lucy [6].

## Cost and BOM

The 2016 BOM prices main items in euros, such as €180 for ten hand servos, and warns that prices
may be outdated [2]. Make wrote in June 2015 that it could be built for under $1,000, depending on
sourcing [7]. Neither is a dated USD total, so `cost` stays empty.

## Building it

**Difficulty 3:** print the ABS parts from the STLs per body section, thread the finger tendons,
wire 31 servos to two Arduino Megas and set up MyRobotLab [2][3][4]. Print and build hours are not
stated. Some substitute servos need changes, such as a resistor and reversed polarity for the
HK15338 [2].

## What is open

| Item | Format | Where | Licence |
|---|---|---|---|
| Printable parts | STL only; no native CAD offered | [STL library](https://inmoov.fr/inmoov-stl-parts-viewer/) [3] | CC-BY-NC-3.0, non-commercial |
| Hardware map, BOM, guides | web pages | [inmoov.fr](https://inmoov.fr/default-hardware-map/) [2] | not stated |
| Control software | Java, Python | [MyRobotLab](https://github.com/MyRobotLab/myrobotlab) [4], [InMoov2](https://github.com/MyRobotLab/InMoov2) [5] | Apache-2.0 |
| ROS 2 description (community) | URDF/xacro, ros2_control, Gazebo | [inmoov_urdf](https://github.com/Sentience-Robotics/inmoov_urdf) [6] | GPL-3.0; meshes marked CC BY-NC 4.0 there |

## Strengths and limits

- **Strengths:** life-size and printable on a small printer [1]; cheap hobby servos and Arduinos
  [2]; a maintained software stack with a simulator [4][5]; a ROS 2 description exists [6].
- **Limits:** non-commercial licence [1]; STL only, so changes start from meshes [3]; no published
  DoF, height or mass; a BOM from 2016 with some broken links [2].

## What to reuse

- Tendon-driven fingers, with the finger servos moved back into the forearm [2][3].
- Splitting large parts so each fits a 12 cm print bed [1].

## Related robots

- [Poppy Humanoid](poppy-humanoid.md) and [Kayra](kayra.md): open printed humanoids; [iCub](icub.md): a costly research one.

## Sources

1. [InMoov project page (inmoov.fr)](https://inmoov.fr/project/), accessed 2026-11-18
2. [InMoov default hardware map and BOM](https://inmoov.fr/default-hardware-map/), accessed 2026-11-18
3. [InMoov STL parts library](https://inmoov.fr/inmoov-stl-parts-viewer/), accessed 2026-11-18
4. [MyRobotLab repository](https://github.com/MyRobotLab/myrobotlab), accessed 2026-11-18
5. [InMoov2 service for MyRobotLab](https://github.com/MyRobotLab/InMoov2), accessed 2026-11-18
6. [Sentience Robotics inmoov_urdf (community ROS 2 description)](https://github.com/Sentience-Robotics/inmoov_urdf), accessed 2026-11-18
7. [Make: InMoov, the life-size humanoid robot you can print at home (2015)](https://makezine.com/2015/06/19/in-our-image/), accessed 2026-11-18

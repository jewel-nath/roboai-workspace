---
type: robot
name: Reachy Mini
summary: Desktop robot kit from Pollen Robotics and Hugging Face (2025) with a six-axis Stewart-platform head, a turning body, two antennas, camera and microphones; the SDK, URDF and MuJoCo model are Apache-2.0, but only STLs are published and the hardware licence is non-commercial (CC BY-NC-SA).
tags: [desktop-robot, social, stewart-platform, dynamixel, raspberry-pi, hugging-face, pollen-robotics, mujoco, kit, python, javascript, llm]
category: social
tier: B
openness: partial
maker: Pollen Robotics and Hugging Face
year: 2025
license: {hardware: CC-BY-NC-SA, software: Apache-2.0, docs: }
links: {repo: "https://github.com/pollen-robotics/reachy_mini", docs: "https://huggingface.co/docs/reachy_mini/", cad: "https://github.com/pollen-robotics/reachy_mini/tree/main/src/reachy_mini/descriptions/reachy_mini/mjcf/assets", paper: , site: "https://www.pollen-robotics.com/reachy-mini/"}
specs: {dof: 9, payload_kg: , reach_mm: , mass_kg: 1.475, size_mm: "300 x 200 x 155", speed_mps: , runtime_h: }
stack: {actuators: "9 ROBOTIS Dynamixel servos: 6 XL330-M288-T in the Stewart-platform head, 2 XL330-M077-T for the antennas, 1 custom XC330-M288-PG for body rotation", mcu: , compute: "Raspberry Pi Compute Module 4 (CM4104016: Wi-Fi, 4 GB RAM, 16 GB flash) in the Wireless; the Lite runs from a computer over USB-C", sensors: ["Raspberry Pi Camera Module 3 Wide (Sony IMX708, 12 MP, autofocus)", "4 PDM MEMS microphones on an XMOS XVF3800 board", "IMU (Wireless only)"], sim_models: ["URDF and MJCF with STL meshes (reachy_mini repo, descriptions/)", "MuJoCo simulation daemon (reachy-mini[mujoco])"], ros2: none}
cost: {type: retail, usd: 499, as_of: 2026-11-18, source: "https://www.pollen-robotics.com/reachy-mini/"}
build: {difficulty: , hours: , print_hours: }
maturity: {last_commit: 2026-11-18, stars: 1673, active: true}
use_cases: [hri, companion, education, hobby, research]
evidence: researched
last_verified: 2026-11-18
sources:
  - {url: "https://www.pollen-robotics.com/reachy-mini/", title: Pollen Robotics Reachy Mini page (prices), accessed: 2026-11-18}
  - {url: "https://techcrunch.com/2025/07/09/hugging-face-opens-up-orders-for-its-reachy-mini-desktop-robots/", title: "TechCrunch: Hugging Face opens up orders for its Reachy Mini desktop robots (2025-07-09)", accessed: 2026-11-18}
  - {url: "https://huggingface.co/blog/reachy-mini", title: "Hugging Face blog: Reachy Mini launch (2025-07-09)", accessed: 2026-11-18}
  - {url: "https://github.com/pollen-robotics/reachy_mini", title: reachy_mini repository README and licence, accessed: 2026-11-18}
  - {url: "https://huggingface.co/docs/reachy_mini/platforms/reachy_mini/hardware", title: Reachy Mini (Wireless) hardware datasheet, accessed: 2026-11-18}
  - {url: "https://huggingface.co/docs/reachy_mini/platforms/reachy_mini_lite/hardware", title: Reachy Mini Lite hardware datasheet, accessed: 2026-11-18}
  - {url: "https://huggingface.co/docs/reachy_mini/troubleshooting", title: Reachy Mini troubleshooting and FAQ, accessed: 2026-11-18}
  - {url: "https://huggingface.co/docs/reachy_mini/platforms/simulation/get_started", title: Reachy Mini simulation guide, accessed: 2026-11-18}
  - {url: "https://huggingface.co/blog/hugging-face-pollen-robotics-acquisition", title: "Hugging Face blog: acquisition of Pollen Robotics (2025-04-14)", accessed: 2026-11-18}
---

# Reachy Mini

A small expressive desktop robot from Pollen Robotics, part of Hugging Face since April 2025 [9],
launched in July 2025 as a kit you assemble [2][3]. Its head moves in six axes on a Stewart
platform, and it ships with an Apache-2.0 SDK and app store [4]. The hardware is **not** fully
open: only STLs are out, under a **non-commercial** Creative Commons licence [4][7].

## Specs

| Item | Value | Source |
|---|---|---|
| Variant in frontmatter | Reachy Mini Wireless; the Lite is in the variant table | [5][6] |
| Degrees of freedom | 9 motors: head 6 (three rotations, three translations), body rotation 1, antennas 2 | [5] |
| Size, mass | 30 x 20 x 15.5 cm extended; 1.475 kg (Lite 1.35 kg). The launch blog says 28 cm tall, 16 cm wide | [3][5][6] |
| Motors | Dynamixel: 6 XL330-M288-T (head), 2 XL330-M077-T (antennas), custom XC330-M288-PG with plastic gears (body) | [5] |
| Camera | Raspberry Pi Camera Module 3 Wide: Sony IMX708, 12 MP, autofocus, 120° | [5] |
| Audio | 4 PDM MEMS microphones on an XMOS XVF3800 board; 5 W speaker | [5] |
| Power | 6.8–7.6 V input; Wireless battery LiFePO4 6.4 V, 2000 mAh, 12.8 Wh; runtime not published, no battery gauge | [5][7] |
| Assembly | 2 to 3 hours per the guide; testers report 1.5 to 2 hours | [4][7] |

## How it works

Six XL330 servos move the head through rods with ball joints, a Stewart platform that gives
three rotations and three translations; a seventh servo turns the body and two more move
the antennas [5][7]. The shell is ABS and PC with aluminium and steel parts [5].

A daemon drives the motors and serves a REST API and WebSocket; the Wireless runs it on its CM4, the
Lite on your computer over USB-C [4][5][6]. Apps use the Python SDK or a JavaScript SDK over WebRTC,
and community apps install from Hugging Face Spaces, for example an LLM conversation app [4]. Pollen
ships no ROS 2 package. The repo holds URDF and MJCF models with STL meshes, and
`reachy-mini-daemon --sim` runs the robot in MuJoCo with the same SDK [4][8].

| Version | Compute | Power | IMU | Mass | Launch price, 2025-07-09 | Price, 2026-11-18 | Source |
|---|---|---|---|---|---|---|---|
| Wireless | Raspberry Pi CM4 onboard, Wi-Fi | LiFePO4 battery | Yes | 1.475 kg | $449 | $499 | [1][2][5] |
| Lite | Your computer, over USB-C | Wall supply | No | 1.35 kg | $299 | $399 | [1][2][6] |

## What it is used for

- Human-robot interaction and companion apps: conversation with LLMs, hand tracking, radio [4].
- Learning to program a robot in Python or JavaScript, with a no-hardware MuJoCo mode [4][8].

## Cost and BOM

Retail, from Pollen: **Wireless $499, Lite $399** on 2026-11-18, excluding shipping, duties and taxes;
orders ship within 90 days, and buyers outside the EU, UK, US and Canada go through Seeed Studio [1].
A $149 Hoverboard base for the Wireless is on pre-order [1]. Launch prices on 2025-07-09 were $449 and
$299 [2]. No BOM is published.

## What is open

| Item | Format | Where | Licence |
|---|---|---|---|
| Daemon, Python and JavaScript SDKs, apps | Python, TypeScript | [reachy_mini](https://github.com/pollen-robotics/reachy_mini) [4] | Apache-2.0 |
| Robot description, simulation | URDF, MJCF | repo `src/reachy_mini/descriptions/` [4] | Apache-2.0 (repo licence) |
| Mechanical parts | STL only; STEP not released yet | [mjcf/assets](https://github.com/pollen-robotics/reachy_mini/tree/main/src/reachy_mini/descriptions/reachy_mini/mjcf/assets) [7] | CC BY-NC-SA, version not stated: **non-commercial** [4] |
| Electronics | — | Not published; the datasheet lists the boards [5] | — |
| Docs | Markdown | [Hugging Face docs](https://huggingface.co/docs/reachy_mini/) from the repo [4] | No separate licence; repo is Apache-2.0 |

## Strengths and limits

- **Strengths:** a six-axis expressive head, wide camera and four-microphone array for $399–$499;
  Apache-2.0 SDKs, a MuJoCo twin and an app catalogue on Hugging Face Spaces [1][4][5][8].
- **Limits:** no arms; only STLs, no STEP or electronics, under a non-commercial licence, though the
  launch blog calls the hardware fully open source [3][4][7]; no runtime figure or battery gauge [7].

## What to reuse

- A Stewart platform of six small serial-bus servos for a 6-DoF head in a tiny volume [5].

## Related robots

- [Reachy](reachy.md): Pollen's full-size research humanoid.
- [Stack-chan](stack-chan.md), [Anki Vector](anki-vector.md), [Jibo](jibo.md), [Blossom](blossom.md),
  [ElectronBot](electronbot.md) and [Coglet](coglet.md): other small social robots.
- [SO-101](so-101.md): the arm in the same Hugging Face LeRobot ecosystem.

## Sources

1. [Pollen Robotics Reachy Mini page (prices)](https://www.pollen-robotics.com/reachy-mini/), accessed 2026-11-18
2. [TechCrunch: Hugging Face opens up orders for its Reachy Mini desktop robots (2025-07-09)](https://techcrunch.com/2025/07/09/hugging-face-opens-up-orders-for-its-reachy-mini-desktop-robots/), accessed 2026-11-18
3. [Hugging Face blog: Reachy Mini launch (2025-07-09)](https://huggingface.co/blog/reachy-mini), accessed 2026-11-18
4. [reachy_mini repository README and licence](https://github.com/pollen-robotics/reachy_mini), accessed 2026-11-18
5. [Reachy Mini (Wireless) hardware datasheet](https://huggingface.co/docs/reachy_mini/platforms/reachy_mini/hardware), accessed 2026-11-18
6. [Reachy Mini Lite hardware datasheet](https://huggingface.co/docs/reachy_mini/platforms/reachy_mini_lite/hardware), accessed 2026-11-18
7. [Reachy Mini troubleshooting and FAQ](https://huggingface.co/docs/reachy_mini/troubleshooting), accessed 2026-11-18
8. [Reachy Mini simulation guide](https://huggingface.co/docs/reachy_mini/platforms/simulation/get_started), accessed 2026-11-18
9. [Hugging Face blog: acquisition of Pollen Robotics (2025-04-14)](https://huggingface.co/blog/hugging-face-pollen-robotics-acquisition), accessed 2026-11-18

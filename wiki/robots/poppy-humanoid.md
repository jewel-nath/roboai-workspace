---
type: robot
name: Poppy Humanoid
summary: 3D-printed 84 cm, 3.5 kg humanoid from Inria's Flowers lab with 25 Dynamixel servos, a Raspberry Pi and the Python library pypot; CC-BY-SA-4.0 hardware (SolidWorks, STEP, STL) and GPL-3.0 software. Dormant since 2021-22, with its websites offline; Poppy Torso and the Ergo Jr arm share the project.
tags: [3d-printed, dynamixel, pypot, python, raspberry-pi, education, inria, poppy-torso, poppy-ergo-jr, dormant]
category: humanoid
tier: B
openness: full
maker: Inria Flowers laboratory (Poppy Project), now hosted by the Poppy Station non-profit
year: 2013
license: {hardware: CC-BY-SA-4.0, software: GPL-3.0-only, docs: }
links: {repo: "https://github.com/poppy-project/poppy-humanoid", docs: , cad: "https://github.com/poppy-project/poppy-humanoid/releases", paper: "https://inria.hal.science/hal-01096338", site: }
specs: {dof: 25, payload_kg: , reach_mm: , mass_kg: 3.5, size_mm: , speed_mps: , runtime_h: }
stack: {actuators: "25 Robotis Dynamixel servos: 19 MX-28, 4 MX-64, 2 AX-12", mcu: , compute: "Raspberry Pi 3 or 4 with Poppy's system image, or a PC through a USB2Dynamixel or USB2AX adapter", sensors: [], sim_models: ["URDF (poppy-humanoid repo, hardware/URDF)", "V-REP scene (poppy-humanoid repo, software)", "URDF for Poppy Torso and Ergo Jr (robot_descriptions)"], ros2: none}
cost: {type: bom, usd: 8000, as_of: 2015-02-16, source: "https://github.com/poppy-project/poppy-humanoid#build-your-own-poppy-humanoid"}
build: {difficulty: 2, hours: 7, print_hours: }
maturity: {last_commit: 2021-12-06, stars: 1107, active: false}
use_cases: [research, education, locomotion, hri]
evidence: researched
last_verified: 2026-11-18
sources:
  - {url: "https://github.com/poppy-project/poppy-humanoid", title: Poppy Humanoid repository README, accessed: 2026-11-18}
  - {url: "https://github.com/poppy-project/poppy-humanoid/blob/master/software/poppy_humanoid/configuration/poppy_humanoid.json", title: Poppy Humanoid motor configuration, accessed: 2026-11-18}
  - {url: "https://inria.hal.science/hal-01096338", title: "Lapeyre et al. (2014): Poppy Project, open-source fabrication of 3D printed humanoid robot for science, education and art", accessed: 2026-11-18}
  - {url: "https://github.com/poppy-project/pypot", title: pypot repository, accessed: 2026-11-18}
  - {url: "https://github.com/poppy-project/poppy-torso", title: Poppy Torso repository README, accessed: 2026-11-18}
  - {url: "https://github.com/poppy-project/poppy-ergo-jr", title: Poppy Ergo Jr repository README and BOM, accessed: 2026-11-18}
  - {url: "https://github.com/poppy-project/poppy_controllers", title: poppy_controllers (ROS Noetic) README, accessed: 2026-11-18}
  - {url: "https://github.com/robot-descriptions/robot_descriptions.py", title: robot_descriptions model list, accessed: 2026-11-18}
---

# Poppy Humanoid

A 3D-printed humanoid from Inria's Flowers lab, started in 2012 and first shown at Humanoids 2013,
to study how body shape affects movement and learning, and used to teach [1][3]. It stands 84 cm,
weighs 3.5 kg and moves 25 Dynamixel servos from Python [2][3]. It is **dormant**: the last commit is
from December 2021, and poppy-project.org, its docs and forum did not resolve on 2026-11-18.

## Specs

| Item | Value | Source |
|---|---|---|
| Variant in frontmatter | Poppy Humanoid, 1.0 hardware release (2015) and later | [1] |
| Degrees of freedom | 25 servos: 19 Dynamixel MX-28, 4 MX-64, 2 AX-12 | [2] |
| Height, mass | 84 cm, 3.5 kg | [3] |
| Computer | Raspberry Pi 3 or 4, or a PC with a USB2Dynamixel or USB2AX adapter | [1] |
| Electronics | Arduino-based, released as open hardware (2014) | [3] |
| Walking | with external support; the 2014 robot had no balance control | [3] |

## How it works

A printed skeleton holds the 25 Dynamixels on an upper-body bus and a leg bus [2]. The design is in
SolidWorks; releases add STL, STEP and Parasolid files [1]. The thighs bend by 6 degrees, a
human-like shape that cut falling speed by almost 60% in single support compared with straight
thighs [3].

Control runs in Python through pypot, which drives the Dynamixel buses and adds kinematics, motion
primitives, a REST API and a CoppeliaSim (V-REP) link [1][4]. Poppy ships a Raspberry Pi image, and
`pip install poppy-humanoid` runs it from a PC [1]. The repo holds a URDF and a V-REP scene [1].
There is no ROS 2 driver; `poppy_controllers` is a ROS Noetic package that supports only the Ergo Jr
[7]. robot_descriptions has Torso and Ergo Jr URDFs but no Humanoid [8]; no MuJoCo model was found.

| Variant | DoF | Hardware | Cost | Last commit | Source |
|---|---|---|---|---|---|
| Poppy Humanoid | 25 | Dynamixel MX-28, MX-64, AX-12; Raspberry Pi | $8,000–9,000 to build (2015) | 2021-12 | [1][2] |
| Poppy Torso | 13 | the Humanoid's upper body on a table mount; Python 3 and Snap! | €5,300 kit at Génération Robots, undated | 2022-03 | [5][8] |
| Poppy Ergo Jr | 6 | printed teaching arm: Dynamixel XL-320, Raspberry Pi 2 or 3, Pixl board; lamp, gripper and pen tools | — | 2022-04 | [6] |

## What it is used for

- Research on morphology and biped balance, such as the bent-thigh study [3].
- Education: in 2014, 15 people of all ages built a working Poppy in two days at a Paris museum [3].
- Teaching with the cheaper Torso (Python 3 and Snap!) and the Ergo Jr arm [5][6].
- Art projects with interactive installations, one of the project's three target fields [3].

## Cost and BOM

The README has said since February 2015 that a full build costs $8,000–9,000, about 60% of it for
the 25 Dynamixels [1]; the frontmatter takes the low end. The detailed BOM was on the offline docs
site; the Ergo Jr BOM is in its repo [6].

## Building it

**Difficulty 2:** print the parts and assemble them with off-the-shelf Dynamixels and a Raspberry Pi
running Poppy's image; the README gives about 7 h of assembly, and no print time [1]. The assembly
guides were on the offline docs site.

## What is open

| Item | Format | Where | Licence |
|---|---|---|---|
| Mechanical design | SolidWorks (Git LFS); STL, STEP, Parasolid in releases | [poppy-humanoid](https://github.com/poppy-project/poppy-humanoid) [1] | CC-BY-SA-4.0 |
| Robot software, V-REP scene | Python | [poppy-humanoid/software](https://github.com/poppy-project/poppy-humanoid/tree/master/software) [1] | GPL-3.0-only |
| Motor library | Python | [pypot](https://github.com/poppy-project/pypot) [4] | GPL-3.0-only |
| Model | URDF | [hardware/URDF](https://github.com/poppy-project/poppy-humanoid/tree/master/hardware/URDF) [1] | CC-BY-SA-4.0 |
| Variants | same layout | [Torso](https://github.com/poppy-project/poppy-torso) [5], [Ergo Jr](https://github.com/poppy-project/poppy-ergo-jr) [6] | CC-BY-SA-4.0 hardware, GPL-3.0-only software |

## Strengths and limits

- **Strengths:** a complete open humanoid with share-alike hardware and native CAD [1]; light at
  3.5 kg [3]; simple Python control with pypot [4]; cheaper Torso and Ergo Jr versions [5][6].
- **Limits:** dormant, with docs and forum offline; $8,000–9,000 in 2015, mostly servos [1]; walks
  only with support [3]; SolidWorks-only sources; ROS 1 support covers only Ergo Jr [7].

## Related robots

- [ROBOTIS OP3](robotis-op3.md): a commercial Dynamixel humanoid with ROS support.
- [InMoov](inmoov.md) and [Kayra](kayra.md): other open printed humanoids; [iCub](icub.md): a costly one.

## Sources

1. [Poppy Humanoid repository README](https://github.com/poppy-project/poppy-humanoid), accessed 2026-11-18
2. [Poppy Humanoid motor configuration](https://github.com/poppy-project/poppy-humanoid/blob/master/software/poppy_humanoid/configuration/poppy_humanoid.json), accessed 2026-11-18
3. [Lapeyre et al. (2014): Poppy Project, open-source fabrication of 3D printed humanoid robot for science, education and art](https://inria.hal.science/hal-01096338), accessed 2026-11-18
4. [pypot repository](https://github.com/poppy-project/pypot), accessed 2026-11-18
5. [Poppy Torso repository README](https://github.com/poppy-project/poppy-torso), accessed 2026-11-18
6. [Poppy Ergo Jr repository README and BOM](https://github.com/poppy-project/poppy-ergo-jr), accessed 2026-11-18
7. [poppy_controllers (ROS Noetic) README](https://github.com/poppy-project/poppy_controllers), accessed 2026-11-18
8. [robot_descriptions model list](https://github.com/robot-descriptions/robot_descriptions.py), accessed 2026-11-18

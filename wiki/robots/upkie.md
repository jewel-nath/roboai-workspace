---
type: robot
name: Upkie
summary: Open wheeled biped on mjbots actuators and a Raspberry Pi, with FreeCAD parts and one Python API for simulation and the real robot; Cookie is a community redesign.
tags: [wheeled-biped, wheel-legged, mjbots, qdd100, moteus, raspberry-pi, gymnasium, pybullet, freecad, 3d-printed]
category: legged
tier: A
openness: full
maker: Stéphane Caron and contributors (Inria)
year: 2022
license: {hardware: Apache-2.0, software: Apache-2.0, docs: Apache-2.0}
links: {repo: "https://github.com/upkie/upkie", docs: "https://upkie.github.io/upkie/", cad: "https://github.com/upkie/upkie_parts", paper: , site: "https://hackaday.io/project/185729-upkie-wheeled-biped-robots"}
specs: {dof: 6, payload_kg: , reach_mm: , mass_kg: , size_mm: , speed_mps: , runtime_h: }
stack: {actuators: "4 mjbots qdd100 beta 3 servos (hips, knees) and 2 mj5208 motors on moteus r4.11 controllers (wheels)", mcu: "moteus controllers on every actuator, mjbots pi3hat (CAN-FD)", compute: "Raspberry Pi 4 Model B", sensors: ["IMU on the pi3hat", "joint position, velocity and torque from the moteus controllers"], sim_models: ["URDF (upkie_description, robot_descriptions.py)", "URDF (cookie_description, for Cookie)"], ros2: none}
cost: {type: , usd: , as_of: , source: }
build: {difficulty: 3, hours: , print_hours: 60}
maturity: {last_commit: 2026-11-03, stars: 464, active: true}
use_cases: [research, reinforcement-learning, locomotion]
evidence: researched
last_verified: 2026-11-17
sources:
  - {url: "https://github.com/upkie/upkie", title: "upkie/upkie repository README", accessed: 2026-11-17}
  - {url: "https://upkie.github.io/upkie/build-your-own.html", title: "Upkie docs, Build your own", accessed: 2026-11-17}
  - {url: "https://upkie.github.io/upkie/bill-of-materials.html", title: "Upkie docs, Bill of materials", accessed: 2026-11-17}
  - {url: "https://upkie.github.io/upkie/getting-started.html", title: "Upkie docs, Getting started", accessed: 2026-11-17}
  - {url: "https://upkie.github.io/upkie/printing-3d.html", title: "Upkie docs, 3D printing", accessed: 2026-11-17}
  - {url: "https://upkie.github.io/upkie/assembly.html", title: "Upkie docs, Assembly", accessed: 2026-11-17}
  - {url: "https://upkie.github.io/upkie/kinematics.html", title: "Upkie docs, Kinematics and joint limits", accessed: 2026-11-17}
  - {url: "https://upkie.github.io/upkie/spines.html", title: "Upkie docs, Spines", accessed: 2026-11-17}
  - {url: "https://upkie.github.io/upkie/gym-environments.html", title: "Upkie docs, Gym environments", accessed: 2026-11-17}
  - {url: "https://github.com/upkie/upkie/blob/main/CHANGELOG.md", title: "upkie/upkie changelog", accessed: 2026-11-17}
  - {url: "https://github.com/upkie/upkie_parts", title: "upkie_parts repository README and changelog", accessed: 2026-11-17}
  - {url: "https://github.com/upkie/upkie_description", title: "upkie_description repository", accessed: 2026-11-17}
  - {url: "https://hackaday.io/project/185729-upkie-wheeled-biped-robots", title: "Upkie wheeled biped robots on Hackaday.io", accessed: 2026-11-17}
  - {url: "https://mjbots.com/products/qdd100-beta-3", title: "mjbots qdd100 beta 3 servo product page", accessed: 2026-11-17}
  - {url: "https://mjbots.com/products/moteus-r4-11-developer-kit", title: "mjbots moteus r4.11 developer kit product page", accessed: 2026-11-17}
  - {url: "https://mjbots.com/products/mjbots-pi3hat-r4-5", title: "mjbots pi3hat r4.5 product page", accessed: 2026-11-17}
  - {url: "https://mjbots.com/products/mjbots-power-dist-r4-5b", title: "mjbots power dist r4.5b product page", accessed: 2026-11-17}
  - {url: "https://github.com/upkie/upkie/discussions/559", title: "Upkie discussion 559, Motors requirements", accessed: 2026-11-17}
  - {url: "https://github.com/upkie/upkie/discussions", title: "Upkie discussions forum", accessed: 2026-11-17}
  - {url: "https://github.com/upkie/upkie/discussions/545", title: "Upkie discussion 545, Robot Cookie", accessed: 2026-11-17}
  - {url: "https://github.com/MichaelMathieu/upkie-T-public", title: "upkie-T-public repository (Cookie)", accessed: 2026-11-17}
  - {url: "https://codeberg.org/upkie/cookie_description", title: "cookie_description repository", accessed: 2026-11-17}
  - {url: "https://inria-paris-robotics-lab.github.io/Robots/Upkie.html", title: "Inria Paris robotics lab, Upkie", accessed: 2026-11-17}
  - {url: "https://arxiv.org/abs/2410.12345", title: "Gökbakan, Dümbgen and Caron, A Data-driven Contact Estimation Method for Wheeled-Biped Robots", accessed: 2026-11-17}
  - {url: "https://github.com/MarcDcls/mjlab_upkie", title: "MjLab Upkie repository", accessed: 2026-11-17}
  - {url: "https://github.com/robot-descriptions/robot_descriptions.py", title: "robot_descriptions.py README", accessed: 2026-11-17}
  - {url: "https://github.com/upkie/upkie/discussions/464", title: "Upkie discussion 464, Alternative BLDC motors?", accessed: 2026-11-17}
---

# Upkie

An open-source wheeled biped: two printed legs with a wheel at each foot, balancing like an inverted
pendulum and bending its legs to cross uneven ground [1]. Started by Stéphane Caron in 2022 and now
maintained with Inria contributors [13][1]. Builders get a clean, tested software stack where one Python
API drives both simulation and the real robot; the catch is that its actuators are costly and hard to buy.

## Specs

| Item | Value | Source |
|---|---|---|
| Actuated joints (`dof`) | 6: hip and knee on each leg, plus one wheel per leg | 3, 23 |
| Hip and knee actuators | 4 × mjbots qdd100 beta 3; 16 N·m peak (under 1 s), 507 g each | 7, 14 |
| Hip and knee speed limit | 28.8 rad/s at 18 V, derived by the docs from the qdd100 rating | 7 |
| Wheel actuators | 2 × moteus r4.11 developer kits with mj5208 motors; limits set to 1.7 N·m and 111 rad/s | 3, 7, 15 |
| Top ground speed | Not measured; the wheel limit is chosen to keep it near 20 km/h | 7 |
| Wheels | RC 1:8 rubber tyres, 112 mm outer diameter by default, 17 mm hex drive | 3 |
| Compute | Raspberry Pi 4 Model B with mjbots pi3hat and power dist board | 3 |
| Battery | RYOBI 18 V compatible power-tool battery | 3 |
| Mass | Not published. The URDF sums to about 5.3 kg, without screws and cables | 12, 7 |
| Print time | 60+ hours (maker's claim) | 13 |

## How it works

### Mechanics and actuation

Each leg is a femur and tibia printed in PETG, with a quasi-direct-drive qdd100 at the hip and the
knee and a hub-mounted RC tyre at the end [5][3]. The wheel hub must be a tight fit in the tyre; changing
the hex or axle size means editing the printed hub [3]. The torso first reused meshes from the mjbots
quad [11]. Version 2 of the parts (upkie_parts 2.0.0, January 2026, by Etienne Arlaud and Valentin
Tordjman--Levavasseur) merges seven torso plates into one case, makes femur and tibia single parts,
embeds the hip actuators in the case so the robot is 6 cm narrower, and adds optional bearing supports
to take radial load off the hip and knee actuators [11][13].

### Electronics and firmware

All electronics are mjbots boards. The pi3hat sits on the Raspberry Pi and provides the CAN-FD ports
and the IMU; the power dist board feeds the actuators from the 18 V battery through XT30 cables [3][7][18].
Every motor must be driven by a moteus controller over CAN-FD; that, not the qdd100 itself, is what
the software requires [18]. mjbots publishes the moteus firmware, hardware and software [1].

### Software and control

A *spine* is a C++ process that talks to the hardware or to a simulator in a loop. The pi3hat spine
runs on the robot with real-time priority and has read-only and mock modes; the Bullet spine runs the same
loop in simulation [8]. Agents are Python programs using the `upkie` package from PyPI or conda-forge.
It exposes Gymnasium environments named `Upkie-<Backend>-<ActionSpace>`, with Mock, PyBullet and Spine
backends and Pendulum, Servos, Gyropod and BaseVelocity action spaces [1][9]. Switching from simulation
to the robot means changing the backend name [1]. Examples include PD and MPC balancers, lying
genuflection and joystick driving [1]. Version 12 (July 2026) removed the Genesis backend, and version
13 (October 2026) moved RL training out to separate projects [10][19].

### Simulation

The URDF and Xacro model is in upkie_description, which robot_descriptions.py can load [12][26]. The
Bullet spine downloads as a pre-compiled binary [8]. For RL there is MjLab Upkie (MuJoCo Warp, needs
an Nvidia GPU, Apache-2.0) and two CPU balancer playgrounds on Codeberg [1][25].

### Cookie variant

Cookie is Michael Mathieu's redesign of the whole Upkie body, released as STL files in upkie-T-public
[20][21]. It routes all cables inside, holds the battery cells and BMS in the body, can charge while on,
has bumpers for falls and a touchscreen on its back [20]. Its BOM lists six qdd100 beta 3 servos (not
beta 2), two moteus developer kits, a pi3hat, a power dist board, a Raspberry Pi 4 and a 12–44 V battery
with an XT90 plug; the README does not say which joint each actuator drives [21]. Its tyres are printed
in flexible filament [21]. The cookie_description URDF on Codeberg has the same six joints as Upkie, and
the upkie package registers `Cookie-*-*` environments [22][10]. The Cookie README's assembly section is
unfinished and several quantities are marked TODO [21].

## What it is used for

- **Research at Inria:** policy learning, whole-body control and state estimation [23]. A data-driven
  contact estimator was tested on Upkie (ICRA 2025) [24][23].
- **RL for wheel-legged robots:** sim-to-real balancing and whole-body velocity policies [1][25].
- **Community builds:** the forum's Real robots category lists several, including Cookie and two
  versions of Michel Strogoff [19].

## Cost and BOM

The BOM lists parts and suppliers but no prices or total [3].

- **mjbots parts, at list price on 2026-11-17 (type `bom`, partial):** 4 × qdd100 at USD 879, two moteus
  r4.11 developer kits at USD 219 and USD 249, pi3hat USD 149, power dist USD 149: **USD 4,282** [14][15][16][17].
  This excludes the Raspberry Pi, battery, wheels, couplers, fan, fasteners and filament, so it is
  a lower bound; the frontmatter cost stays empty until a full priced BOM exists.
- **Availability:** the qdd100 page says it is not stocked, with a minimum order of 50; the developer kit
  shows sold out; the pi3hat and power dist pages show both sold out and a stock count [14][15][16][17].
- The maintainer says qdd100s cost about USD 400–500 when the project began [18].
- **Alternatives:** any actuator driven by moteus works. He suggests a driverless CubeMars AK80-9 with a
  moteus controller as easier than a CyberGear, which needs its own driver removed (untested) [18].
- **Cookie:** its README lists qdd100 at USD 539 plus VAT, developer kits at USD 244 plus VAT, and the
  pi3hat and power dist at USD 149 plus VAT each; the prices are undated, last changed 2024-01-05 [21].
- No kit or assembled robot is sold.

## Building it

**Difficulty 3:** printing, crimping JST PH cables, soldering XT connectors, about 100 heat-set inserts,
configuring moteus controllers and setting up the Pi; no custom PCB.

- **Printing:** PETG at 0.2 mm layers, infill 20–60% by part in the docs' table. The docs describe 3MF
  projects tuned for a Prusa i3 MK3S+; the v2 repo ships FreeCAD and STL files only [5][11].
- **Tools:** JST PH crimper, ball-tip hex drivers for M2.5 and M3, soldering iron, wire cutters [4].
- **Steps:** get started, print, set up the Pi, test electronics, install motion software, assemble [2].
- **Pitfalls:**
  - The build guide still points to the v1 parts at a pinned commit, while upkie_parts now holds v2,
    which changes the parts and the IMU orientation [5][11].
  - Mount the head plate the right way round; otherwise the XT30 cables are hard to plug in and the IMU
    frame in the URDF must be changed [6].
  - A troubleshooting thread covers servos reporting zero velocity after a moteus firmware update [19].
  - Actuator supply is the main risk; check stock before printing anything [14][15].

## What is open

| Item | Format | Where | Licence |
|---|---|---|---|
| Mechanical CAD, v2 | FreeCAD (.FCStd), STL | [upkie_parts](https://github.com/upkie/upkie_parts) | Apache-2.0 |
| Mechanical CAD, v1 | STL, 3MF (per the docs) | pinned commit linked from the docs | Apache-2.0 |
| BOM and build guide | Markdown, Doxygen site | [docs](https://upkie.github.io/upkie/) | Apache-2.0 |
| Electronics | Off-the-shelf mjbots boards | mjbots | mjbots' own; not checked here |
| Software | C++ spines, Python package | [upkie/upkie](https://github.com/upkie/upkie) | Apache-2.0 |
| Robot model | URDF, Xacro | [upkie_description](https://github.com/upkie/upkie_description) | Apache-2.0; tyre mesh CC-BY-4.0 |
| RL playground | Python, MuJoCo Warp | [mjlab_upkie](https://github.com/MarcDcls/mjlab_upkie) | Apache-2.0 |
| Cookie parts and BOM | STL, Markdown | [upkie-T-public](https://github.com/MichaelMathieu/upkie-T-public) | Apache-2.0 |
| Cookie model | URDF, Xacro | [cookie_description](https://codeberg.org/upkie/cookie_description) | Apache-2.0 |

Cookie publishes STL files only, with no editable CAD [21].

## Strengths and limits

**Strengths**
- One Gymnasium API across mock, PyBullet and the real robot, with versioned releases and CI [1][9].
- Quasi-direct-drive joints with torque readings, good for estimation and control research [7][24].
- Editable FreeCAD parts under Apache-2.0, and a growing set of community builds [11][19].

**Limits**
- Expensive: the mjbots parts alone are over USD 4,000 at list price, and the qdd100 is not stocked [14].
- Only six joints and no arms; a balancing platform, not a manipulator.
- Docs lag the hardware: the guide still describes v1 parts [5][11].
- No published mass, battery life or measured speed.

## What to reuse

- The spine pattern: a small real-time process owns the hardware loop, and agents in any language talk to it [8].
- One environment API with swappable backends, so the same agent runs in simulation and on the robot [1].
- Power-tool batteries as a cheap, safe, swappable pack [3].
- Bearing supports that take radial load off direct-drive actuators [11].
- Requiring a motor controller protocol (moteus over CAN-FD) rather than one actuator model [18].

## Related robots

- [Open Duck Mini](open-duck-mini.md): a cheaper printed biped with an RL sim-to-real pipeline.
- [Berkeley Humanoid Lite](berkeley-humanoid-lite.md): printed custom actuators instead of bought ones.
- [ToddlerBot](toddlerbot.md): low-cost printed humanoid for ML research.
- MABEL, an open wheeled biped the maintainer suggests to builders asking for a cheaper design [27].

## Sources

1. [upkie/upkie repository README](https://github.com/upkie/upkie), accessed 2026-11-17
2. [Upkie docs, Build your own](https://upkie.github.io/upkie/build-your-own.html), accessed 2026-11-17
3. [Upkie docs, Bill of materials](https://upkie.github.io/upkie/bill-of-materials.html), accessed 2026-11-17
4. [Upkie docs, Getting started](https://upkie.github.io/upkie/getting-started.html), accessed 2026-11-17
5. [Upkie docs, 3D printing](https://upkie.github.io/upkie/printing-3d.html), accessed 2026-11-17
6. [Upkie docs, Assembly](https://upkie.github.io/upkie/assembly.html), accessed 2026-11-17
7. [Upkie docs, Kinematics and joint limits](https://upkie.github.io/upkie/kinematics.html), accessed 2026-11-17
8. [Upkie docs, Spines](https://upkie.github.io/upkie/spines.html), accessed 2026-11-17
9. [Upkie docs, Gym environments](https://upkie.github.io/upkie/gym-environments.html), accessed 2026-11-17
10. [upkie/upkie changelog](https://github.com/upkie/upkie/blob/main/CHANGELOG.md), accessed 2026-11-17
11. [upkie_parts repository README and changelog](https://github.com/upkie/upkie_parts), accessed 2026-11-17
12. [upkie_description repository](https://github.com/upkie/upkie_description), accessed 2026-11-17
13. [Upkie wheeled biped robots on Hackaday.io](https://hackaday.io/project/185729-upkie-wheeled-biped-robots), accessed 2026-11-17
14. [mjbots qdd100 beta 3 servo product page](https://mjbots.com/products/qdd100-beta-3), accessed 2026-11-17
15. [mjbots moteus r4.11 developer kit product page](https://mjbots.com/products/moteus-r4-11-developer-kit), accessed 2026-11-17
16. [mjbots pi3hat r4.5 product page](https://mjbots.com/products/mjbots-pi3hat-r4-5), accessed 2026-11-17
17. [mjbots power dist r4.5b product page](https://mjbots.com/products/mjbots-power-dist-r4-5b), accessed 2026-11-17
18. [Upkie discussion 559, Motors requirements](https://github.com/upkie/upkie/discussions/559), accessed 2026-11-17
19. [Upkie discussions forum](https://github.com/upkie/upkie/discussions), accessed 2026-11-17
20. [Upkie discussion 545, Robot Cookie](https://github.com/upkie/upkie/discussions/545), accessed 2026-11-17
21. [upkie-T-public repository (Cookie)](https://github.com/MichaelMathieu/upkie-T-public), accessed 2026-11-17
22. [cookie_description repository](https://codeberg.org/upkie/cookie_description), accessed 2026-11-17
23. [Inria Paris robotics lab, Upkie](https://inria-paris-robotics-lab.github.io/Robots/Upkie.html), accessed 2026-11-17
24. [Gökbakan, Dümbgen and Caron, A Data-driven Contact Estimation Method for Wheeled-Biped Robots](https://arxiv.org/abs/2410.12345), accessed 2026-11-17
25. [MjLab Upkie repository](https://github.com/MarcDcls/mjlab_upkie), accessed 2026-11-17
26. [robot_descriptions.py README](https://github.com/robot-descriptions/robot_descriptions.py), accessed 2026-11-17
27. [Upkie discussion 464, Alternative BLDC motors?](https://github.com/upkie/upkie/discussions/464), accessed 2026-11-17

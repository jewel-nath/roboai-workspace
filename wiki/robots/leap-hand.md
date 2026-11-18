---
type: robot
name: LEAP Hand
summary: Low-cost four-finger research hand from Carnegie Mellon, 16 Dynamixel servos and printed parts for about $1,770; printed parts are CC BY-SA, but the API's licence file is non-commercial (CC BY-NC).
tags: [dexterous-hand, four-finger, dynamixel, 3d-printed, low-cost, isaac-gym, mujoco, non-commercial]
category: gripper
tier: B
openness: full
maker: Carnegie Mellon University (Kenneth Shaw, Ananye Agarwal, Deepak Pathak)
year: 2023
license: {hardware: CC-BY-SA-4.0, software: CC-BY-NC-4.0, docs: }
links: {repo: "https://github.com/leap-hand/LEAP_Hand_API", docs: "https://v1.leaphand.com/assembly", cad: "https://v1.leaphand.com/cad_request", paper: "https://arxiv.org/abs/2309.06440", site: "https://leaphand.com"}
specs: {dof: 16, payload_kg: , reach_mm: , mass_kg: 0.595, size_mm: , speed_mps: , runtime_h: }
stack: {actuators: "16 x Dynamixel XC330-M288-T serial-bus servos (XL330-M288-T in the Lite build)", mcu: "none; a Dynamixel U2D2 USB adapter", compute: "host PC over USB", sensors: ["servo encoders (16), with velocity and current readback"], sim_models: ["URDF (LEAP_Hand_Sim)", "Isaac Gym environment (LEAP_Hand_Sim)", "USD and Isaac Lab environment (LEAP_Hand_Isaac_Lab)", "MJCF (MuJoCo Menagerie, leap_hand)"], ros2: official}
cost: {type: bom, usd: 1771.74, as_of: 2023-08-01, source: "https://v1.leaphand.com/parts"}
build: {difficulty: 2, hours: 4, print_hours: 24}
maturity: {last_commit: 2025-10-20, stars: 179, active: false}
use_cases: [research, reinforcement-learning, teleop, imitation-learning, manipulation]
evidence: researched
last_verified: 2026-11-18
sources:
  - {url: "https://github.com/leap-hand/LEAP_Hand_API", title: LEAP Hand API repository README, accessed: 2026-11-18}
  - {url: "https://arxiv.org/abs/2309.06440", title: "LEAP Hand: Low-Cost, Efficient, and Anthropomorphic Hand for Robot Learning", accessed: 2026-11-18}
  - {url: "https://v1.leaphand.com/parts", title: LEAP Hand v1 parts list, accessed: 2026-11-18}
  - {url: "https://v1.leaphand.com/", title: LEAP Hand v1 website, accessed: 2026-11-18}
  - {url: "https://v1.leaphand.com/cad_request", title: LEAP Hand v1 CAD request form, accessed: 2026-11-18}
  - {url: "https://v1.leaphand.com/leap_cad", title: LEAP Hand v1 CAD downloads, accessed: 2026-11-18}
  - {url: "https://v1.leaphand.com/assembly", title: LEAP Hand v1 assembly guide, accessed: 2026-11-18}
  - {url: "https://v1.leaphand.com/purchase", title: LEAP Hand v1 purchase page, accessed: 2026-11-18}
  - {url: "https://github.com/leap-hand/LEAP_Hand_API/blob/main/LICENSE", title: LEAP Hand API licence file, accessed: 2026-11-18}
  - {url: "https://github.com/leap-hand/LEAP_Hand_API/tree/main/ros2_module", title: LEAP Hand ROS 2 module README, accessed: 2026-11-18}
  - {url: "https://github.com/leap-hand/LEAP_Hand_Sim", title: LEAP Hand simulation repository README, accessed: 2026-11-18}
  - {url: "https://github.com/leap-hand/LEAP_Hand_Isaac_Lab", title: LEAP Hand Isaac Lab repository README, accessed: 2026-11-18}
  - {url: "https://github.com/google-deepmind/mujoco_menagerie/tree/main/leap_hand", title: "MuJoCo Menagerie: LEAP Hand description", accessed: 2026-11-18}
  - {url: "https://v2.leaphand.com/", title: LEAP Hand v2 website, accessed: 2026-11-18}
  - {url: "https://github.com/leap-hand/LEAP_Hand_V2_API", title: LEAP Hand v2 API repository README, accessed: 2026-11-18}
  - {url: "https://v2-adv.leaphand.com/", title: LEAP Hand v2 Advanced website, accessed: 2026-11-18}
  - {url: "https://github.com/leap-hand/LEAP_Hand_V2_Adv_API", title: LEAP Hand v2 Advanced API repository README, accessed: 2026-11-18}
  - {url: "https://arxiv.org/abs/2504.13165", title: "RUKA: Rethinking the Design of Humanoid Hands with Learning", accessed: 2026-11-18}
---

# LEAP Hand

A four-finger research hand built from sixteen Dynamixel servos and a few printed parts, published
by Carnegie Mellon University at RSS 2023 [1][2]. It costs under $2,000 to build, an eighth of the
Allegro Hand by the paper's count, and comes with Isaac Gym, Isaac Lab and MuJoCo models
[2][11][12][13]. Two newer hands share the name, LEAP Hand v2 and v2 Advanced; this page covers v1,
the documented build, and lists the others below [4][14][16].

## Specs

| Item | Value | Source |
|---|---|---|
| Variant in frontmatter | LEAP Hand v1, Full build (XC330 servos) | [3] |
| Fingers and DoF | 3 fingers + thumb; 16 joints, one servo each | [2] |
| Servos | 16 x Dynamixel XC330-M288-T (Full) or XL330-M288-T (Lite); do not mix them | [3] |
| Mass | 595 g | [2] |
| Size | about 30% larger than an adult hand, similar to the Allegro Hand | [2] |
| Joint speed | about 8 rad/s | [2] |
| Pull-out force | 19.5 N per finger, against 8.5 N for the Allegro and 26.5 N for an adult hand (authors' test) | [2] |
| Endurance | held 2 kg on one fingertip for an hour; joint error under 0.025 rad after an hour of cycling | [2] |
| Power | 5 V; the BOM lists a 5 V, 30 A supply | [1][3] |
| Current limit | 300 mA by default in the API; up to 550 mA on the Full build | [1] |
| Host link | USB through a Dynamixel U2D2; position, velocity and current read at up to 500 Hz | [1] |
| Payload | not stated by the authors; the RUKA authors measured 4.0 kg | [18] |

## How it works

Each finger has a knuckle (MCP) driven by two servos, then two hinge joints (PIP and DIP) with one
servo each [2]. The two knuckle axes are arranged so the finger can still move side to side when it
is bent, which the authors call a universal MCP joint [2]. The servos form the structure: off-the-
shelf Dynamixel frames join them, and printed PLA parts make the palm, spacers and fingertips, with
optional soft tips in NinjaFlex and grip tape on the contact surfaces [3].

There is no custom electronics: the servos share one Dynamixel bus, a power hub feeds them 5 V, and
a U2D2 adapter connects the bus to the host over USB [1][3]. The API runs current-limited PID
position control by default and also supports velocity and current modes, from Python, C++, ROS 1 or
ROS 2 (tested on Humble, Ubuntu 22.04) [1][10]. Helper tools map MANO human-hand poses to LEAP
joints, and separate repositories cover teleoperation with Manus gloves or an Apple Vision Pro
[1][4].

For simulation, `LEAP_Hand_Sim` holds the URDF, an Isaac Gym environment and a sim-to-real in-hand
rotation policy [11]. `LEAP_Hand_Isaac_Lab` ports it to Isaac Lab, and MuJoCo Menagerie has a
`leap_hand` MJCF derived from the dexsuite URDF [12][13].

| Variant | Actuation | Cost given | Files | Source |
|---|---|---|---|---|
| v1 Full | 16 x Dynamixel XC330 | $1,771.74 BOM | CAD after a short form | [3][5] |
| v1 Lite | 16 x Dynamixel XL330, weaker current limit | $714.30 BOM | as v1 Full | [1][3] |
| v2 | 8 servos for 16 joints, tendon-driven finger curl; 7.6 V; Feetech tools in the API | "$200" | CAD after a form; CAD CC BY-NC-SA, code MIT per README | [14][15] |
| v2 Advanced | 17 powered motors for 21 DoF, hybrid rigid-soft fingers, powered palm | "$3000" | CAD on request; print files promised on paper acceptance | [16][17] |

The v2 site calls the hand both 8-DoF and 16-DoF, and the v2 Advanced API README says 17-DoF while
its site says 21 [14][16][17].

## What it is used for

- **Sim-to-real RL:** the paper trains in-hand cube rotation in Isaac Gym and runs it on the hand
  [2][11].
- **Teleoperation and imitation learning:** the paper's teleoperation and behaviour-cloning tests
  beat the Allegro Hand on most tasks [2]; glove and Vision Pro teleoperation code is public [4].
- **Baseline for newer open hands:** the RUKA paper tests against it [18].

## Cost and BOM

| Item | Price (USD) | Type | Date | Source |
|---|---|---|---|---|
| v1 Full parts | 1,771.74 | BOM | the page dates its prices to August 2023, so the frontmatter uses 2023-08-01; read 2026-11-18 | [3] |
| v1 Lite parts | 714.30 | BOM | as above | [3] |
| Assembled v1 hand from the team | about 2,200 | retail (approximate) | read 2026-11-18 | [8] |

The sixteen servos are $1,439.84 of the Full BOM [3]. Tools are extra; the list suggests a $299.99
printer, hex keys, a PH00 screwdriver and a soldering iron for inserts [3]. Assembled hands are
ordered by email from the team's Pennsylvania company, which warns that copies sold on Taobao and
similar sites are not theirs [8].

## Building it

**Difficulty 2:** printing and assembly of off-the-shelf servos; the only soldering-iron work is
pressing brass inserts at 250 °C [7].

- **Printing:** PLA, palm at 60% infill with supports, other parts at 100%; soft tips need a
  direct-drive printer; all parts print in under 24 hours [3].
- **Time:** under three hours on the website, about four hours in the paper [2][3].
- **Pitfalls:** a joint off by 90°, 180° or 270° means the servo horn is mounted wrong; check servo
  IDs and U2D2 wiring if servos are missing; frequent overload errors mean the current limit is too
  high; Dynamixel Wizard must be closed while the API runs [1].

## What is open

| Item | Format | Where | Licence |
|---|---|---|---|
| Printed parts | STL, STEP, URDF | v1.leaphand.com, after a short form [5][6] | CC-BY-SA-4.0, commercial use allowed |
| API | Python, C++, ROS 1, ROS 2 | [LEAP_Hand_API](https://github.com/leap-hand/LEAP_Hand_API) | CC-BY-NC-4.0 in the licence file; the README says MIT |
| Simulation | URDF, Isaac Gym | [LEAP_Hand_Sim](https://github.com/leap-hand/LEAP_Hand_Sim) | MIT |
| Isaac Lab | USD, Python | [LEAP_Hand_Isaac_Lab](https://github.com/leap-hand/LEAP_Hand_Isaac_Lab) | MIT (README) |
| MuJoCo model | MJCF | MuJoCo Menagerie | MIT [13] |
| BOM and assembly guide | web pages | [v1.leaphand.com](https://v1.leaphand.com/) | not stated |

**The licences disagree.** The CAD pages grant CC BY-SA 4.0, including commercial use [5][6]. The
API README says the code is MIT and the CAD is CC BY-NC-SA [1], while the API's licence file is
CC BY-NC 4.0 for the whole repository [9]. Until the authors settle it, treat the API as
non-commercial and ask them before selling anything that ships it.

## Strengths and limits

- **Strengths:** about an eighth of the Allegro's price [2]; stronger fingers than the Allegro in
  the authors' and RUKA's tests [2][18]; no custom PCB, so parts are easy to buy and replace [3];
  models for Isaac Gym, Isaac Lab and MuJoCo [11][12][13]; assembled hands can be bought [8].
- **Limits:** conflicting licences [1][5][9]; larger than a human hand and only four digits [2];
  the servos are over 80% of the cost [3]; no touch sensing in the BOM [3]; the simulation repo's
  last commit is May 2024 [11]; three hand lines now share the name [4][14][16].

## What to reuse

- Arrange two knuckle servos so side-to-side motion survives at any bend angle [2].
- Use the servo frames as the finger's structure and print only spacers and the palm [3].
- Run current-limited position control so fingers comply on contact without force sensors [1].

## Related robots

- [Allegro Hand](allegro-hand.md): the commercial hand the paper benchmarks it against.
- [RUKA](ruka.md) and [Aero Hand Open](aero-hand-open.md): newer open hands that use tendons and
  fewer motors.
- [Shadow Dexterous Hand](shadow-dexterous-hand.md): the high-end reference.
- A printed top plate fits the [UFACTORY xArm](ufactory-xarm.md), [Franka Panda](franka-panda.md)
  and [Universal Robots UR5](universal-robots.md) [6].

## Sources

1. [LEAP Hand API repository README](https://github.com/leap-hand/LEAP_Hand_API), accessed 2026-11-18
2. [LEAP Hand: Low-Cost, Efficient, and Anthropomorphic Hand for Robot Learning](https://arxiv.org/abs/2309.06440), accessed 2026-11-18
3. [LEAP Hand v1 parts list](https://v1.leaphand.com/parts), accessed 2026-11-18
4. [LEAP Hand v1 website](https://v1.leaphand.com/), accessed 2026-11-18
5. [LEAP Hand v1 CAD request form](https://v1.leaphand.com/cad_request), accessed 2026-11-18
6. [LEAP Hand v1 CAD downloads](https://v1.leaphand.com/leap_cad), accessed 2026-11-18
7. [LEAP Hand v1 assembly guide](https://v1.leaphand.com/assembly), accessed 2026-11-18
8. [LEAP Hand v1 purchase page](https://v1.leaphand.com/purchase), accessed 2026-11-18
9. [LEAP Hand API licence file](https://github.com/leap-hand/LEAP_Hand_API/blob/main/LICENSE), accessed 2026-11-18
10. [LEAP Hand ROS 2 module README](https://github.com/leap-hand/LEAP_Hand_API/tree/main/ros2_module), accessed 2026-11-18
11. [LEAP Hand simulation repository README](https://github.com/leap-hand/LEAP_Hand_Sim), accessed 2026-11-18
12. [LEAP Hand Isaac Lab repository README](https://github.com/leap-hand/LEAP_Hand_Isaac_Lab), accessed 2026-11-18
13. [MuJoCo Menagerie: LEAP Hand description](https://github.com/google-deepmind/mujoco_menagerie/tree/main/leap_hand), accessed 2026-11-18
14. [LEAP Hand v2 website](https://v2.leaphand.com/), accessed 2026-11-18
15. [LEAP Hand v2 API repository README](https://github.com/leap-hand/LEAP_Hand_V2_API), accessed 2026-11-18
16. [LEAP Hand v2 Advanced website](https://v2-adv.leaphand.com/), accessed 2026-11-18
17. [LEAP Hand v2 Advanced API repository README](https://github.com/leap-hand/LEAP_Hand_V2_Adv_API), accessed 2026-11-18
18. [RUKA: Rethinking the Design of Humanoid Hands with Learning](https://arxiv.org/abs/2504.13165), accessed 2026-11-18

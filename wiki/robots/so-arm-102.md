---
type: robot
name: SO-ARM 102
summary: Robonine's stiffer, longer-reach SO-101 derivative with a parallel gripper, PET-CF links and stronger shoulder servos; LeRobot-compatible, about $390 in parts or as a kit.
tags: [leader-follower, feetech, lerobot, 3d-printed, pet-cf, parallel-gripper, so-101-derivative]
category: arm
tier: A
openness: full
maker: Robonine
year: 2026
license: {hardware: CERN-OHL-P-2.0, software: Apache-2.0, docs: CC-BY-4.0}
links: {repo: "https://github.com/roboninecom/SO-ARM102", docs: "https://github.com/roboninecom/SO-ARM102/tree/main/docs", cad: "https://github.com/roboninecom/SO-ARM102/tree/main/models/step", paper: , site: "https://robonine.com"}
specs: {dof: 6, payload_kg: 0.3, reach_mm: 483, mass_kg: , size_mm: , speed_mps: , runtime_h: }
stack: {actuators: "Feetech serial-bus servos: follower 2 x STS3250, 2 x STS3235, 2 x STS3215 (12 V); leader 6 x STS3215", mcu: "none on the arm; one Waveshare Bus Servo Adapter (USB to serial bus) per arm", compute: "host PC over USB", sensors: ["servo encoders", "OV2735 USB wrist camera"], sim_models: ["URDF/Xacro (SO-ARM102 repo, simulation/urdf)"], ros2: none}
cost: {type: bom, usd: 388.4, as_of: 2026-11-17, source: "https://github.com/roboninecom/SO-ARM102/blob/main/docs/bom.md"}
build: {difficulty: 2, hours: , print_hours: 52.5}
maturity: {last_commit: 2026-11-12, stars: 237, active: true}
use_cases: [teleop, imitation-learning, data-collection, education, research]
evidence: researched
last_verified: 2026-11-17
sources:
  - {url: "https://github.com/roboninecom/SO-ARM102", title: SO-ARM 102 repository README, accessed: 2026-11-17}
  - {url: "https://github.com/roboninecom/SO-ARM102/blob/main/docs/specifications.md", title: SO-ARM 102 specifications and test results, accessed: 2026-11-17}
  - {url: "https://github.com/roboninecom/SO-ARM102/blob/main/docs/bom.md", title: SO-ARM 102 bill of materials, accessed: 2026-11-17}
  - {url: "https://github.com/roboninecom/SO-ARM102/blob/main/docs/printing.md", title: SO-ARM 102 printing guide, accessed: 2026-11-17}
  - {url: "https://github.com/roboninecom/SO-ARM102/blob/main/docs/assembly-guide.md", title: SO-ARM 102 assembly guide, accessed: 2026-11-17}
  - {url: "https://github.com/roboninecom/SO-ARM102/blob/main/docs/lerobot.md", title: SO-ARM 102 LeRobot setup, accessed: 2026-11-17}
  - {url: "https://github.com/roboninecom/SO-ARM102/blob/main/LICENSING.md", title: SO-ARM 102 licensing map, accessed: 2026-11-17}
  - {url: "https://github.com/roboninecom/SO-ARM102/blob/main/NOTICE", title: SO-ARM 102 NOTICE (design lineage), accessed: 2026-11-17}
  - {url: "https://robonine.com/shop/so-arm102-robotic-arm-kit/", title: Robonine SO-ARM102 kit page, accessed: 2026-11-17}
  - {url: "https://github.com/roboninecom/SO-ARM-102-Lerobot", title: SO-ARM 102 LeRobot plugin README, accessed: 2026-11-17}
  - {url: "https://github.com/roboninecom/SO-ARM100-101-Parallel-Gripper", title: Robonine SO-ARM100/101 Parallel Gripper README, accessed: 2026-11-17}
  - {url: "https://github.com/roboninecom/SO-ARM100-101-Parallel-Gripper/blob/main/RELICENSING.md", title: Parallel gripper relicensing record, accessed: 2026-11-17}
  - {url: "https://github.com/TheRobotStudio/SO-ARM100", title: SO-ARM100 repository README (SO-101), accessed: 2026-11-17}
---

# SO-ARM 102

A leader-follower teleoperation arm by Robonine that keeps the SO-101 joint layout but redesigns
every part: carbon-fibre PET links, stronger shoulder and elbow servos, a bearing-supported base and
a parallel gripper [1][8]. Pick it over the SO-101 when the arm must carry more, reach further or
hold position better, and you can still use LeRobot and the SO-101 leader [1][6].

## Specs

| Item | Value | Source |
|---|---|---|
| Degrees of freedom | 6: five arm joints plus a parallel gripper | [1] |
| Horizontal reach (gripper tip centre) | 483 mm; 473 mm behind the base; up to 544 mm high (computed from the model) | [2] |
| Rated payload | 300 g (maker's rating) | [2] |
| Repeatability | about 0.1 mm (maker's measurement) | [2] |
| Joint ranges | base 352°, shoulder 224°, elbow 243°, wrist flex 196°, wrist roll 328° | [2] |
| Link lengths, axis to axis | 85, 119, 139, 62 and 132 mm, base to gripper tip | [2] |
| Gripper | rack and pinion, two moving jaws, 0 to 85 mm; boxes up to about 75 mm | [2] |
| Tip deflection, 300 g, full extension | 3.4 mm (3.9 mm on a second run), frame only, PET-CF17 at 25% infill | [2] |
| Shoulder and elbow speed | 75 RPM no-load at 12 V (servo maker's rating) | [2] |
| Base joint backlash | 5.00 encoder counts; ±1.85 mm tip error (calculated) | [2] |
| Follower current, 300 g load | 1.26 A average, 3.28 A peak; servos up to 46 °C at 30 °C ambient | [2] |
| Noise at 1 m | 60 dB | [2] |
| Supply | follower 12 V, leader 5 V | [1] |
| Mass | not measured; the URDF export estimates 0.889 kg | [1] |

All figures are Robonine's own, measured on its prototypes in August and September 2026 unless
marked calculated [2]. Absolute accuracy is still being tuned: with stock servo PID gains the tip
sagged about 50 mm at full extension, about 5 mm after tuning [2].

## How it works

### Mechanics and actuation

The arm keeps the SO-101 joint layout and servo ID order, so it stays compatible with LeRobot
[3][8]. The follower puts the strongest servos where the load is: two brushless STS3250 (50 kg·cm) at the
shoulder and elbow, two lower-backlash STS3235 (30 kg·cm) at the base and wrist flex, and two
12 V STS3215 at the wrist roll and gripper [3]. A 6812 thin-section ball bearing carries each base
[3]. The gripper is a revision of Robonine's earlier SO-101 parallel gripper: a servo-driven pinion
moves two racks on steel or carbon guide rods [2][3][4][8]. The leader is printed in PLA+ with six
7.4 V STS3215 servos, read only as encoders; rubber O-rings between servo and horn add friction
so it does not feel loose [1][3].

### Electronics and firmware

Each arm has one Waveshare Bus Servo Adapter linking its servo bus to the host over USB-C, plus a
5.5 x 2.1 mm barrel supply: 12 V 5 A for the follower, 5 V 2 A for the leader [3]. The STS3250
servos come with longer cables, and two extra 300 mm cables are needed [3]. The servos run
Feetech's own firmware, which is not part of the repository [8]. A USB camera (OV2735 module in the prototype) sits on
the gripper [3].

### Software and control

Robonine maintains a separate LeRobot plugin for the follower's mixed servo set; the leader uses
LeRobot's standard SO-101 leader type [6][10]. The plugin is an alpha release pinned to LeRobot
0.6.1 [6][10]. Servo IDs, calibration and lessons are on Robonine's lab site [1].

### Simulation

The repository has a URDF and Xacro export with STL visuals, box collisions on all eight links and
recorded mass assumptions [1]. No MJCF and no ROS 2 package were found.

## What it is used for

Teleoperation and recording demonstrations for imitation learning, as a single pair or as a
bimanual setup of two pairs [1]. It is a 2026 design, and no projects or papers using it were
found yet.

## Cost and BOM

| Item | Price (USD) | Type | Date | Source |
|---|---|---|---|---|
| Leader and follower, components only | 342.40 | BOM | read 2026-11-17 | [3] |
| Same, plus printing material | 388.40 | BOM | read 2026-11-17 | [3] |
| Buying full packs and spools from scratch | 429.80 | BOM | read 2026-11-17 | [3] |
| Robonine kit: PET-CF parts, all servos and electronics, camera, unassembled | 389, plus shipping and duty | kit | 2026-11-17 | [9] |

Servos are the bulk of the cost: $240.70 for twelve [3]. Electronics with the camera cost $50.50,
bearings, rods and clamps $40, fasteners $11.20, and filament $46 [3]. Robonine calls these
reference prices, not quotes; shipping, taxes and tools are excluded [3]. The kit ships from China
[9].

## Building it

**Difficulty 2:** print the parts and assemble off-the-shelf servos and boards with hex keys, with
no soldering; the effort is in printing carbon-fibre filament and careful assembly.

- **Printing:** follower links in PET-CF (annealing optional), follower gripper and base in
  PETG-CF, leader in PLA+ [4]. The three supplied Bambu Studio projects take 15.5 h, 14 h and 23 h
  on a Bambu Lab A1 with a 0.4 mm nozzle, so about 52.5 h in total [4]. Parts fit a 180 x 180 mm
  bed; the supplied plates need 256 x 256 mm [4]. Gripper gears and racks print at 100% infill [4].
- **Tools:** 1.5 mm and 2 mm hex keys and a PH1 screwdriver; a removable threadlocker suited to
  plastic is advised [3][5].
- **Assembly:** a 32-page A5 booklet (v0.8) and a step list; build the arm body twice, then the
  gripper, follower and leader ends [1][5]. The kit page puts assembly at one or two evenings [9].
- **Known issues:** use booklet v0.8, as older ones show other parts; several M2 screws are hard to
  reach; gripper clamps are tight on rods whose diameter varies by supplier; check servo cable
  lengths before closing joints; read two steps ahead in two awkward places [1].
- **Do not swap the supplies:** the follower runs on 12 V, the leader on 5 V [1].

## What is open

| Item | Format | Where | Licence |
|---|---|---|---|
| CAD | STEP | [models/step/](https://github.com/roboninecom/SO-ARM102/tree/main/models/step) | CERN-OHL-P-2.0 |
| Print files | STL, 3MF slicer projects | [models/](https://github.com/roboninecom/SO-ARM102/tree/main/models) | CERN-OHL-P-2.0 |
| BOM | Markdown with buy links | [docs/bom.md](https://github.com/roboninecom/SO-ARM102/blob/main/docs/bom.md) | CC-BY-4.0 |
| Docs | Markdown, PDF booklet | [docs/](https://github.com/roboninecom/SO-ARM102/tree/main/docs) | CC-BY-4.0 |
| Model | URDF, Xacro, STL meshes | [simulation/urdf/](https://github.com/roboninecom/SO-ARM102/tree/main/simulation/urdf) | CC-BY-4.0 |
| Software | LeRobot plugin, Python | [SO-ARM-102-Lerobot](https://github.com/roboninecom/SO-ARM-102-Lerobot) | Apache-2.0 [10] |
| Electronics, firmware | Off-the-shelf boards, closed servo firmware | — | — |

The licence files confirm the split: CERN-OHL-P-2.0 for `models/`, Apache-2.0 for configuration
and CI, CC-BY-4.0 for docs, images and the `simulation/` folder [7]. GitHub reports only CC-BY-4.0.
The NOTICE says no SO-101 geometry was copied; all parts are new designs [8].

## Strengths and limits

- **Strengths:** about half the tip deflection of an SO-101 and twice the rated payload [2]; wider
  base rotation and longer reach [2]; a parallel gripper with a wrist camera [2]; measured test
  data published with the design [2]; permissive hardware licence with a file-by-file map [7].
- **Limits:** components cost about $110 more than the SO-101 parts list, before filament
  [3][13]; carbon-fibre filament and a
  large print job; the LeRobot plugin is alpha [10]; no MJCF or ROS 2 package; the figures are all
  the maker's own. One doc inconsistency: the current test mentions six STS3250 servos, while the
  BOM has two [2][3].

## What to reuse

- Choose filament per part role: stiff PET-CF for links, tough PETG-CF for parts that take knocks,
  cheap PLA+ for a leader that only has to be light [4].
- Spend on servos only where torque is highest: brushless servos at shoulder and elbow, cheap ones
  at the wrist [3].
- A large thin-section bearing at the base takes bending load off the base servo [3].
- Rack-and-pinion parallel jaws on guide rods, driven by one hobby servo [2][4].
- O-rings between servo and horn give a passive leader smooth friction [1][3].
- Test frame stiffness with printed servo dummies, so the frame is compared without servo play [2].

## Related robots

- [SO-101](so-101.md): the arm this design succeeds; its leader works with the SO-ARM 102 follower
  [6][13].
- Robonine's SO-ARM100/101 parallel gripper is the add-on this gripper grew from [8][11]. Its
  hardware is now under CERN-OHL-P-2.0, but the move from GPL-3.0 still waits for some
  contributors' consent [12].

## Sources

1. [SO-ARM 102 repository README](https://github.com/roboninecom/SO-ARM102), accessed 2026-11-17
2. [SO-ARM 102 specifications and test results](https://github.com/roboninecom/SO-ARM102/blob/main/docs/specifications.md), accessed 2026-11-17
3. [SO-ARM 102 bill of materials](https://github.com/roboninecom/SO-ARM102/blob/main/docs/bom.md), accessed 2026-11-17
4. [SO-ARM 102 printing guide](https://github.com/roboninecom/SO-ARM102/blob/main/docs/printing.md), accessed 2026-11-17
5. [SO-ARM 102 assembly guide](https://github.com/roboninecom/SO-ARM102/blob/main/docs/assembly-guide.md), accessed 2026-11-17
6. [SO-ARM 102 LeRobot setup](https://github.com/roboninecom/SO-ARM102/blob/main/docs/lerobot.md), accessed 2026-11-17
7. [SO-ARM 102 licensing map](https://github.com/roboninecom/SO-ARM102/blob/main/LICENSING.md), accessed 2026-11-17
8. [SO-ARM 102 NOTICE (design lineage)](https://github.com/roboninecom/SO-ARM102/blob/main/NOTICE), accessed 2026-11-17
9. [Robonine SO-ARM102 kit page](https://robonine.com/shop/so-arm102-robotic-arm-kit/), accessed 2026-11-17
10. [SO-ARM 102 LeRobot plugin README](https://github.com/roboninecom/SO-ARM-102-Lerobot), accessed 2026-11-17
11. [Robonine SO-ARM100/101 Parallel Gripper README](https://github.com/roboninecom/SO-ARM100-101-Parallel-Gripper), accessed 2026-11-17
12. [Parallel gripper relicensing record](https://github.com/roboninecom/SO-ARM100-101-Parallel-Gripper/blob/main/RELICENSING.md), accessed 2026-11-17
13. [SO-ARM100 repository README (SO-101)](https://github.com/TheRobotStudio/SO-ARM100), accessed 2026-11-17

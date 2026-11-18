# Robot Atlas

One research profile per notable robot: specs, how it works, what it is used for, cost, how hard it
is to build, and what is worth reusing. Template: [templates/robot.md](../../templates/robot.md).

| Tier | Which robots | What they get |
|---|---|---|
| A | Open hardware with files and a BOM, still active | A full profile here |
| B | Partly open, older but important, or commercial references | A short card here |
| C | Everything else found in a source | A row in that source's triage note in [sources/](../../sources/) |

- Name a file after the robot's common name: `so-101.md`, `mobile-aloha.md`.
- Robots known only from vendor datasheets share one note per group, `reference-<group>.md`, with
  `evidence: vendor-claim`.
- In `stack`, name a part by its slug when it has a page in [parts/](../parts/), so the part page
  can list the robots that use it.
- Your own robot gets a profile here once its project is public, with `evidence: built`.

## Index

<!-- index:start -->
| Robot | Category | Tier | Openness | DOF | Payload (kg) | Cost (USD) | Evidence | Verified |
|---|---|---|---|---|---|---|---|---|
| [AgileX PiPER](agilex-piper.md) | arm | B | software-only | 7 | 1.5 | 3500 retail (2026-11-18) | researched | 2026-11-18 |
| [Baxter](baxter.md) | arm | B | software-only | 15 | 2.2 | 22000 retail (2012-09-18) | researched | 2026-11-18 |
| [BCN3D Moveo](bcn3d-moveo.md) | arm | B | full | 6 | — | — | researched | 2026-11-18 |
| [Franka Emika Panda and Franka Research 3](franka-panda.md) | arm | B | software-only | 7 | 3 | — | researched | 2026-11-18 |
| [Interbotix X-Series arms (ViperX 300 S, WidowX 250 S)](interbotix-x-series-arms.md) | arm | B | software-only | 7 | 0.75 | — | researched | 2026-11-18 |
| [Kinova Gen3, Gen3 lite and Gen2](kinova-gen3.md) | arm | B | software-only | 7 | 2 | — | researched | 2026-11-18 |
| [Koch v1.1](koch-v1-1.md) | arm | B | full | 6 | — | 477 bom (2024-09-17) | researched | 2026-11-18 |
| [KUKA LBR iiwa and LBR Med](kuka-lbr-iiwa.md) | arm | B | closed-reference | 7 | 14 | — | researched | 2026-11-18 |
| [OpenManipulator-X](openmanipulator-x.md) | arm | B | partial | 5 | 0.5 | 1629.09 retail (2026-11-18) | researched | 2026-11-18 |
| [Sawyer](sawyer.md) | arm | B | software-only | 8 | 4 | 29000 retail (2015-03-19) | researched | 2026-11-18 |
| [SO-101](so-101.md) | arm | A | full | 6 | — | 229.88 bom (2026-11-17) | researched | 2026-11-17 |
| [SO-ARM 102](so-arm-102.md) | arm | A | full | 6 | 0.3 | 388.4 bom (2026-11-17) | researched | 2026-11-17 |
| [UFACTORY xArm and Lite 6](ufactory-xarm.md) | arm | B | software-only | 6 | 5 | 9175.86 retail (2026-11-18) | researched | 2026-11-18 |
| [Universal Robots UR3, UR5, UR10 and e-Series](universal-robots.md) | arm | B | software-only | 6 | 5 | — | researched | 2026-11-18 |
| [Aero Hand Open](aero-hand-open.md) | gripper | A | full | 7 | — | 316.48 bom (2026-11-17) | researched | 2026-11-17 |
| [Allegro Hand](allegro-hand.md) | gripper | B | software-only | 16 | 5 | — | vendor-claim | 2026-11-18 |
| [LEAP Hand](leap-hand.md) | gripper | B | full | 16 | — | 1771.74 bom (2023-08-01) | researched | 2026-11-18 |
| [Robotiq 2F-85](robotiq-2f-85.md) | gripper | B | software-only | 1 | 5 | 9271.41 retail (2026-11-18) | researched | 2026-11-18 |
| [RUKA](ruka.md) | gripper | B | partial | 11 | 6 | 1307.11 bom (2025-02-19) | researched | 2026-11-18 |
| [Shadow Dexterous Hand](shadow-dexterous-hand.md) | gripper | B | software-only | 20 | — | — | vendor-claim | 2026-11-18 |
| [UMI gripper (Universal Manipulation Interface)](umi-gripper.md) | gripper | B | partial | 1 | — | 371 bom (2024-03-06) | researched | 2026-11-18 |
| [Berkeley Humanoid Lite](berkeley-humanoid-lite.md) | humanoid | A | full | 24 | — | 4351 bom (2026-11-17) | researched | 2026-11-17 |
| [Microban](microban.md) | humanoid | A | full | 19 | — | 567 bom (2026-11-17) | researched | 2026-11-17 |
| [ToddlerBot](toddlerbot.md) | humanoid | A | full | 30 | 1.48 | 5728 bom (2026-11-17) | researched | 2026-11-17 |
| [Open Duck Mini v2](open-duck-mini.md) | legged | A | full | 16 | — | 437 bom (2026-11-17) | researched | 2026-11-17 |
| [Sesame](sesame.md) | legged | A | full | 8 | — | 60 bom (2026-11-17) | researched | 2026-11-17 |
| [Upkie](upkie.md) | legged | A | full | 6 | — | — | researched | 2026-11-17 |
| [F1TENTH (RoboRacer)](f1tenth.md) | mobile-base | A | partial | 2 | — | 3022.29 bom (2026-05-15) | researched | 2026-11-17 |
| [JPL Open Source Rover](jpl-open-source-rover.md) | mobile-base | A | full | 10 | — | 1421.18 bom (2026-11-17) | researched | 2026-11-17 |
| [NanoSaur](nanosaur.md) | mobile-base | A | full | 2 | — | — | researched | 2026-11-17 |
| [OpenBot](openbot.md) | mobile-base | A | full | 2 | — | 50 bom (2021-03-10) | researched | 2026-11-17 |
| [Robot Soccer Kit (RSK)](robot-soccer-kit.md) | mobile-base | A | full | 3 | — | — | researched | 2026-11-17 |
| [TurtleBot3](turtlebot3.md) | mobile-base | A | partial | 2 | 15 | 783.5 kit (2026-11-17) | researched | 2026-11-17 |
| [TriFinger](trifinger.md) | other | B | full | 9 | — | 5000 bom (2020-08-08) | researched | 2026-11-18 |
| [Coglet](coglet.md) | social | A | partial | 9 | — | 189.38 kit (2026-11-17) | researched | 2026-11-17 |
| [Stack-chan](stack-chan.md) | social | A | full | 2 | — | 99 retail (2026-11-17) | researched | 2026-11-17 |
<!-- index:end -->

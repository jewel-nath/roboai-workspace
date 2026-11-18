---
type: source
name: Awesome Robot Descriptions
registry: awesome-robot-descriptions
url: https://github.com/robot-descriptions/awesome-robot-descriptions
commit: "bb41b10"
read_on: 2026-11-17
counts: {entries: 161, pages: 54, waiting: 0, index_only: 54, deferred: 0, rejected: 4}
---

# Awesome Robot Descriptions: what it gives RoboAI

A curated table of URDF, MJCF and Xacro models for about 160 robots, grouped by type, with each
model's licence and whether it has visuals, inertias and collisions. It is the best single map of
which robots can be simulated today, so it seeds the Atlas and every profile's `sim_models`. Most
entries are commercial robots seen only through their models; the open designs worth building
are few, and several of them live in repos the list does not link.

## How it was read

- Read at commit `bb41b10` on 2026-11-17, all ten robot sections in full. Rows that repeat one
  robot once per model format were merged, so 161 entries remain from the list's rows.
- Triage was split across three agents (arms, hands, drones and educational; bipeds, humanoids
  and quadrupeds; mobile manipulators and wheeled), then slugs were reconciled across them and
  with the other Phase 3 lists.
- For open designs, the robot's own hardware repo was found and checked with a shallow git clone:
  last commit, licence files, and whether CAD and a BOM exist. Commercial robots were judged by how
  often builders and researchers meet them; their licence below is the model's, marked "(model)".
- Variants of one design share a page (for example UR3 to UR10e, or ANYmal B to D). The licence
  of a simulation model says nothing about the robot's hardware.
- Dead links found on 2026-11-17: the unitree_mujoco paths for A1, Aliengo, Go1 and Laikago (that
  repo now holds newer robots only), and three deep links whose paths moved (Flexiv Rizon4 Xacro,
  KUKA Med 7 and Med 14 in lbr-stack). Several entries link third-party copies rather than the
  maker's model: Atlas v4 (openai/roboschool), Digit, Mini Cheetah, Minitaur, Fetch, PR2, TIAGo,
  RBY1 and the Gepetto example-robot-data copies.
- Where the list's licence differs from the repo today: SO-ARM 102 is CERN-OHL-P-2.0 for hardware
  (the list gives the docs licence, CC-BY-4.0), and the SO-ARM100/101 parallel gripper is moving
  from GPL-3.0 to CERN-OHL-P-2.0.

## Pages made

| Entry | Page | Tier |
|---|---|---|
| SO-ARM 100, SO-ARM 101 (The Robot Studio) | [SO-101](../wiki/robots/so-101.md) | A |
| SO-ARM 102 (Robonine) | [SO-ARM 102](../wiki/robots/so-arm-102.md) | A |
| Aero Hand (TetherIA, now Chestnut Robotics) | [Aero Hand Open](../wiki/robots/aero-hand-open.md) | A |
| BD-X (Disney) | [Open Duck Mini v2](../wiki/robots/open-duck-mini.md) | A |
| Upkie (Stéphane Caron), Cookie (Michael Mathieu) | [Upkie](../wiki/robots/upkie.md) | A |
| Berkeley Humanoid (Hybrid Robotics) | [Berkeley Humanoid Lite](../wiki/robots/berkeley-humanoid-lite.md) | A |
| Microban (Rhoban) | [Microban](../wiki/robots/microban.md) | A |
| ToddlerBot 2XC, ToddlerBot 2XM (Stanford) | [ToddlerBot](../wiki/robots/toddlerbot.md) | A |
| RSK omnidirectional (Robot Soccer Kit) | [Robot Soccer Kit (RSK)](../wiki/robots/robot-soccer-kit.md) | A |
| Koch v1.1, Low-Cost Robot Arm (Alexander Koch) | [Koch v1.1](../wiki/robots/koch-v1-1.md) | B |
| FingerEdu, TriFingerEdu (ODRI) | [TriFinger](../wiki/robots/trifinger.md) | B |
| UMI Gripper (UMI project) | [UMI gripper (Universal Manipulation Interface)](../wiki/robots/umi-gripper.md) | B |
| LEAP Hand v1 (Carnegie Mellon University) | [LEAP Hand](../wiki/robots/leap-hand.md) | B |
| Panda, FR3, FR3 v2 (Franka Robotics) | [Franka Emika Panda and Franka Research 3](../wiki/robots/franka-panda.md) | B |
| UR3, UR3e, UR5, UR5e, UR10, UR10e (Universal Robots) | [Universal Robots UR3, UR5, UR10 and e-Series](../wiki/robots/universal-robots.md) | B |
| Gen2, Gen3, Gen3 Lite (Kinova) | [Kinova Gen3, Gen3 lite and Gen2](../wiki/robots/kinova-gen3.md) | B |
| iiwa 7, iiwa 14, Med 7, Med 14, Dual iiwa 14 (KUKA) | [KUKA LBR iiwa and LBR Med](../wiki/robots/kuka-lbr-iiwa.md) | B |
| Lite 6, xArm5, xArm6, xArm7 (UFACTORY) | [UFACTORY xArm and Lite 6](../wiki/robots/ufactory-xarm.md) | B |
| ViperX 300, WidowX 250 (Trossen Robotics) | [Interbotix X-Series arms (ViperX 300 S, WidowX 250 S)](../wiki/robots/interbotix-x-series-arms.md) | B |
| PiPER (AgileX) | [AgileX PiPER](../wiki/robots/agilex-piper.md) | B |
| Sawyer (Rethink Robotics) | [Sawyer](../wiki/robots/sawyer.md) | B |
| Baxter (Rethink Robotics) | [Baxter](../wiki/robots/baxter.md) | B |
| Allegro Hand (Wonik Robotics) | [Allegro Hand](../wiki/robots/allegro-hand.md) | B |
| Robotiq 2F-85 (Robotiq) | [Robotiq 2F-85](../wiki/robots/robotiq-2f-85.md) | B |
| Shadow Hand E3M5 (The Shadow Robot Company) | [Shadow Dexterous Hand](../wiki/robots/shadow-dexterous-hand.md) | B |
| Pupper v3 (Stanford) | [Stanford Pupper v3](../wiki/robots/pupper-v3.md) | B |
| Mini Cheetah (MIT) | [MIT Mini Cheetah](../wiki/robots/mini-cheetah.md) | B |
| Solo (ODRI) | [ODRI Solo-8, Solo-12 and Bolt](../wiki/robots/odri-solo.md) | B |
| iCub (IIT) | [iCub](../wiki/robots/icub.md) | B |
| AgiBot X1 (AgibotTech) | [AgiBot X1 (Lingxi X1)](../wiki/robots/agibot-x1.md) | B |
| OP3 (ROBOTIS) | [ROBOTIS OP3](../wiki/robots/robotis-op3.md) | B |
| Cassie (Agility Robotics) | [Agility Robotics Cassie](../wiki/robots/cassie.md) | B |
| Digit (Agility Robotics) | [Agility Digit](../wiki/robots/agility-digit.md) | B |
| Atlas DRC v3, Atlas v4 (Boston Dynamics) | [Boston Dynamics Atlas](../wiki/robots/boston-dynamics-atlas.md) | B |
| Booster T1 (Booster Robotics) | [Booster T1](../wiki/robots/booster-t1.md) | B |
| G1 (Unitree) | [Unitree G1](../wiki/robots/unitree-g1.md) | B |
| H1 (Unitree) | [Unitree H1 and H1-2](../wiki/robots/unitree-h1.md) | B |
| GR-1 (Fourier) | [Fourier GR-1 and GR-2](../wiki/robots/fourier-gr-1.md) | B |
| NAO (Aldebaran, formerly SoftBank Robotics) | [NAO](../wiki/robots/nao.md) | B |
| TALOS (PAL Robotics) | [PAL Robotics TALOS](../wiki/robots/pal-talos.md) | B |
| A1, Aliengo, Laikago (Unitree) | [Unitree A1, Aliengo and Laikago](../wiki/robots/unitree-a1.md) | B |
| Go1, Go2 (Unitree) | [Unitree Go1 and Go2](../wiki/robots/unitree-go2.md) | B |
| ANYmal B, ANYmal C, ANYmal D (ANYbotics) | [ANYmal B, C, D and X](../wiki/robots/anymal.md) | B |
| Spot (Boston Dynamics) | [Boston Dynamics Spot](../wiki/robots/boston-dynamics-spot.md) | B |
| Crazyflie 1.0, Crazyflie 2.0 (Bitcraze) | [Bitcraze Crazyflie 2.x](../wiki/robots/crazyflie.md) | B |
| Fetch (Fetch Robotics) | [Fetch Robotics Fetch and Freight](../wiki/robots/fetch.md) | B |
| Google Robot (Everyday Robots) | [Google Robot (Everyday Robots mobile manipulator)](../wiki/robots/google-robot.md) | B |
| Pepper (SoftBank Robotics) | [Pepper](../wiki/robots/pepper.md) | B |
| PR2 (Willow Garage) | [Willow Garage PR2](../wiki/robots/pr2.md) | B |
| Reachy (Pollen Robotics) | [Reachy and Reachy 2](../wiki/robots/reachy.md) | B |
| Stretch RE1, Stretch 2, Stretch 3 (Hello Robot) | [Hello Robot Stretch (RE1, Stretch 2, Stretch 3, Stretch 4)](../wiki/robots/hello-robot-stretch.md) | B |
| TIAGo (PAL Robotics) | [PAL Robotics TIAGo, TIAGo++ and TIAGo Pro](../wiki/robots/tiago.md) | B |
| Tidybot (Stanford) | [Stanford TidyBot and TidyBot++](../wiki/robots/tidybot.md) | B |
| Boxer, Dingo, Husky, Jackal, Ridgeback (Clearpath Robotics) | [Clearpath research bases (Husky, Jackal, Dingo, Ridgeback, Boxer)](../wiki/robots/clearpath-robots.md) | B |

## Waiting for a page

| Entry | Page | Tier | Why it matters |
|---|---|---|---|

## Index only

| Entry | What it is | Last commit | Licence |
|---|---|---|---|
| e.DO (Comau) | Small educational 6-axis arm, rarely met outside classrooms | — | BSD-3-Clause (model) |
| M-710iC (FANUC) | Heavy-payload industrial arm | — | BSD-3-Clause (model) |
| Rizon4 (Flexiv) | Force-controlled 7-DoF commercial arm | — | Apache-2.0 (model) |
| Z1 (Unitree) | Add-on arm for Unitree quadrupeds | — | BSD-3-Clause (model) |
| Poppy Ergo Jr (Poppy Project) | Printed 6-DoF teaching arm, inactive; on the `poppy-humanoid` page | 2022-04-30 | CC-BY-SA-4.0 (hardware), GPL-3.0 (software) |
| DACH_TRON2A (LimX Dynamics) | Dual-arm configuration of the TRON 2 | — | Apache-2.0 (model) |
| NEXTAGE (Kawada Robotics) | Dual-arm industrial upper-body humanoid | — | BSD (model) |
| Poppy Torso (Poppy Project) | Upper body of Poppy Humanoid; on its page | 2022-03-24 | CC-BY-SA-4.0 (hardware), GPL-3.0 (software) |
| Sciurus17 (RT Corporation) | Dual-arm research upper body; model has no licence | — | none stated |
| YuMi (ABB) | Small dual-arm assembly cobot | — | BSD-2-Clause (model) |
| X2 (Skydio) | Enterprise autonomous quadcopter | — | Apache-2.0 (model) |
| Ingenuity (NASA JPL) | Mars helicopter; the URDF is a community approximation | — | Apache-2.0 (model) |
| Dynamixel 2R arm | Two-joint friction-identification test bench | — | MIT (model) |
| Ability Hand (PSYONIC) | Commercial bionic hand also sold for robots | — | MIT (model and API) |
| BarrettHand (Barrett Technology) | Classic three-finger research hand, now rarely used | — | BSD (model) |
| Dagana Gripper (IIT) | IIT lab gripper | — | Apache-2.0 (model) |
| DexHand (The Robot Studio, IoT Design Shop) | Printed tendon hand; inactive, newer open hands cover it | 2024-07-26 | CC-BY-NC-SA-4.0 |
| IIT SoftFoot (IIT) | Soft adaptive foot for legged robots | — | BSD-3-Clause (model) |
| SCHUNK EGP, EGU 50, PZN-plus, PZV 64, WSG 50 | Industrial catalogue grippers | — | GPL-3.0 or BSD-3-Clause (models) |
| SCHUNK SVH Hand | Five-finger servo-electric hand, little research use | — | GPL-3.0 (model) |
| Shadow DEX-EE (The Shadow Robot Company) | Rugged three-finger hand made with Google DeepMind; on the Shadow hand page | — | Apache-2.0 (model) |
| SO-ARM100/101 Parallel Gripper (Robonine) | Printed gripper add-on; on the SO-101 and SO-ARM 102 pages | 2026-10-28 | CERN-OHL-P-2.0 (hardware), relicensing in progress |
| Bolt (ODRI) | Small 6-DoF biped from ODRI modules; on the `odri-solo` page | 2022-09-06 | BSD-3-Clause |
| TRON1: PF, SF and WF variants A and B (LimX Dynamics) | Commercial research biped with point, sole or wheel feet | — | Apache-2.0 (model) |
| TRON2: SF, SFYG, WF, WFYG (LimX Dynamics) | Newer LimX biped with dual-arm variants | — | Apache-2.0 (model) |
| Rhea (Gabrael Levine) | Hobby wheeled biped; URDF only | 2024-02-21 | MIT |
| Spryped (Benjamin Bokser) | Personal biped controller and URDF, no CAD | 2021-07-05 | GPL-3.0 |
| Adam Lite (PNDbotics) | Commercial full-size humanoid | — | MIT (model) |
| Apollo (Apptronik) | Industrial humanoid not sold to researchers | — | Apache-2.0 (model) |
| Draco3 (Apptronik) | Lab research humanoid | — | BSD-2-Clause (model) |
| Elf2 (BXI Robotics) | Commercial 25-DoF humanoid | — | Apache-2.0 (model) |
| ergoCub (IIT) | iCub successor, not sold; on the `icub` page | — | BSD-3-Clause (model) |
| GENE.01 (Generative Bionics) | New commercial humanoid | — | CC-BY-NC-4.0 (model) |
| JAXON (JSK) | Lab research humanoid | — | CC-BY-SA-4.0 (model) |
| JVRC-1 (AIST) | Simulation-only humanoid for the JVRC challenge | — | BSD-2-Clause |
| N1 (Fourier) | Humanoid announced as open; drawings and BOM not found yet | 2026-10-25 | Apache-2.0 (model) |
| Oli (LimX Dynamics) | Full-size commercial humanoid | — | Apache-2.0 (model) |
| Robonaut 2 (NASA JSC) | Torso humanoid flown on the ISS; retired | — | NASA-1.3 (model) |
| Romeo (Aldebaran) | Research humanoid prototype; project ended | — | BSD-3-Clause (model) |
| SigmaBan (Rhoban) | Kid-size RoboCup humanoid; URDF only | 2022-10-14 | MIT |
| Valkyrie (NASA JSC) | DRC-era humanoid, few units | — | NASA-1.3 (model) |
| WALK-MAN (IIT) | DRC-era disaster-response humanoid | — | BSD-3-Clause (model) |
| B1, B2 (Unitree) | Industrial heavy-payload quadrupeds | — | BSD-3-Clause (model) |
| Barkour v0, Barkour vb (Google) | In-house agility quadruped, not for sale | — | Apache-2.0 (model) |
| HyQ (IIT) | Hydraulic research quadruped | — | Apache-2.0 (model) |
| Minitaur (Ghost Robotics) | Discontinued direct-drive quadruped | — | BSD-2-Clause (model) |
| BamBot (Tim Qian) | Omni base with two SO-100-style arms; hardware docs unfinished | 2025-07-14 | Apache-2.0 |
| Eve R3 (Halodi, now 1X) | Wheeled humanoid service robot | — | Apache-2.0 (model) |
| Ginger (Paaila Technology) | Wheeled humanoid service robot | — | BSD (model) |
| R1 (Galaxea Dynamics) | Wheeled dual-arm robot with a lifting torso; model has no licence | — | none stated |
| RBY1 (Rainbow Robotics) | Wheeled dual-arm robot; third-party model | — | MIT (model) |
| Perseverance (NASA JPL) | Mars rover with an arm; hobby model | — | Apache-2.0 (model) |
| RB-KAIROS, RB-KAIROS+, RB-ROBOUT, RB-ROBOUT+, RB-SUMMIT, RB-THERON, RB-VOGUI, RB-VOGUI+ (Robotnik) | European commercial base and mobile-manipulator line | — | BSD-3-Clause (models) |
| WL P311D, WL P311E (LimX Dynamics) | Wheel-legged quadruped | 2026-11-05 | Apache-2.0 (models) |

## Deferred

| Entry | What it is | Phase |
|---|---|---|

## Rejected

| Entry | Why | Date |
|---|---|---|
| Gundam RX-78 (Bandai Namco Filmworks) | Model of a life-size statue: no licence, nothing to build or use | 2026-11-17 |
| Double Pendulum | A test model for dynamics libraries, not a robot | 2026-11-17 |
| Simple Humanoid (LAAS) | A test model for dynamics libraries, not a robot | 2026-11-17 |
| MuJoCo Humanoid | A simulation benchmark, not a robot; MuJoCo itself comes in Phase 4 | 2026-11-17 |

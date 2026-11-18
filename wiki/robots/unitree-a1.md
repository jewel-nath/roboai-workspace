---
type: robot
name: Unitree A1, Aliengo and Laikago
summary: Unitree's early quadrupeds; the 12 kg A1 was the legged-RL workhorse of the legged_gym era. The A1 and Laikago are no longer on Unitree's shop, but their URDFs, a legacy SDK and MuJoCo, Isaac Gym and Isaac Lab models remain.
tags: [quadruped, unitree, a1, aliengo, laikago, legged-gym, isaac-lab, mujoco, rma, commercial, discontinued]
category: legged
tier: B
openness: software-only
maker: Unitree Robotics
year: 2020
license: {hardware: , software: BSD-3-Clause, docs: }
links: {repo: "https://github.com/unitreerobotics/unitree_ros", docs: , cad: , paper: , site: "https://www.unitree.com/a1/"}
specs: {dof: 12, payload_kg: 5, reach_mm: , mass_kg: 12, size_mm: "500 x 300 x 400", speed_mps: 3.3, runtime_h: 1}
stack: {actuators: "12 Unitree joint motors, 33.5 N·m and 21 rad/s each (reseller listing)", mcu: , compute: "Raspberry Pi (Basic) or NVIDIA TX2 / NX (Explorer) for perception, per a reseller listing", sensors: ["Intel RealSense depth camera", "optional 2D lidar"], sim_models: ["URDF (unitree_ros: a1, aliengo, laikago)", "MJCF (MuJoCo Menagerie unitree_a1)", "Isaac Gym (legged_gym a1 task)", "USD (Isaac Lab A1 velocity task)"], ros2: none}
cost: {type: , usd: , as_of: , source: }
build: {difficulty: , hours: , print_hours: }
maturity: {last_commit: 2026-11-13, stars: 1650, active: true}
use_cases: [research, reinforcement-learning, locomotion]
evidence: researched
last_verified: 2026-11-18
sources:
  - {url: "https://newatlas.com/robotics/unitree-a1-quadruped-robot/", title: "New Atlas: Unitree A1 quadruped robot (2020-05-04)", accessed: 2026-11-18}
  - {url: "https://www.mybotshop.de/Unitree-A1-Quadruped_1", title: "MYBOTSHOP (reseller): Unitree A1 product page", accessed: 2026-11-18}
  - {url: "https://github.com/unitreerobotics/unitree_ros", title: unitree_ros README and robot descriptions, accessed: 2026-11-18}
  - {url: "https://github.com/unitreerobotics/unitree_legged_sdk", title: unitree_legged_sdk README (v3.8.6) and v3.3.1 release, accessed: 2026-11-18}
  - {url: "https://github.com/google-deepmind/mujoco_menagerie/tree/main/unitree_a1", title: "MuJoCo Menagerie: unitree_a1", accessed: 2026-11-18}
  - {url: "https://github.com/leggedrobotics/legged_gym", title: legged_gym README and task registry, accessed: 2026-11-18}
  - {url: "https://github.com/isaac-sim/IsaacLab", title: "Isaac Lab: Unitree asset configs and A1 velocity task", accessed: 2026-11-18}
  - {url: "https://arxiv.org/abs/2107.04034", title: "RMA: Rapid Motor Adaptation for Legged Robots", accessed: 2026-11-18}
  - {url: "https://shop.unitree.com/", title: Unitree shop product list, accessed: 2026-11-18}
  - {url: "https://github.com/unitreerobotics/unitree_mujoco", title: unitree_mujoco README and robot list, accessed: 2026-11-18}
---

# Unitree A1, Aliengo and Laikago

Unitree's early quadrupeds. The 12 kg A1, announced in 2020 at under US$10,000, became the cheap
legged-RL workhorse of the legged_gym era [1][6]. Unitree's own shop no longer lists the A1 or
Laikago and current SDK releases support only newer robots, though one reseller still lists the A1
on request [2][4][9]; no dated end-of-sale notice was found. Builders meet it now mostly in sim.

## Specs

| Item | Value | Source |
|---|---|---|
| Variant in frontmatter | A1, announced May 2020 | [1] |
| Degrees of freedom | 12, three per leg; no gripper | [3] |
| Mass, payload | 12 kg with battery; 5 kg maximum payload (maker's claims) | [1] |
| Size | 500 x 300 x 400 mm standing (maker's claim) | [1] |
| Speed, runtime | 3.3 m/s; 1 to 2.5 h per charge (maker's claims) | [1] |
| Joint motors | 33.5 N·m and 21 rad/s per motor (maker's specs on a reseller page) | [2] |
| Compute | Raspberry Pi (Basic) or NVIDIA TX2 or NX (Explorer) for perception (reseller page) | [2] |
| Sensors | Intel RealSense depth camera, optional 2D lidar [2]; New Atlas reports dual depth cameras [1] | [1][2] |

## How it works

Twelve Unitree joint motors, three per leg, drive the robot; users command walking at a high level
or send joint-level commands [3]. A PC talks to the control board over UDP with unitree_legged_sdk,
a prebuilt C++ library with headers and examples; the A1, Aliengo and Laikago need release v3.3.1,
because current releases support only the Go1 [4].

unitree_ros holds the URDFs and ROS 1 Gazebo packages for all three; its Gazebo setup does
joint-level control only, not walking, and the separate unitree_ros_to_real package drives the
real robot [3]. No ROS 2 support from Unitree for these models was found. Menagerie has an A1
MJCF [5], legged_gym an A1 rough-terrain task [6], and Isaac Lab an A1 velocity task with a DC
motor model [7]. unitree_mujoco now holds newer robots only, so Menagerie's links to it for the A1
are dead [5][10].

| Variant | Mass | Payload | Speed | Runtime | On Unitree's shop (2026-11-18) | Source |
|---|---|---|---|---|---|---|
| A1 | 12 kg | 5 kg | 3.3 m/s | 1–2.5 h | no | [1][9] |
| Laikago | 22 kg | 9 kg | 1.4 m/s | up to 3 h | no; US$45,000 when New Atlas saw it | [1][9] |
| Aliengo | — | — | — | — | yes, at US$50,000 | [9] |

## What it is used for

- Legged RL in simulation: legged_gym's `a1` task and Isaac Lab's A1 task [6][7].
- Sim-to-real research: RMA (Kumar et al., RSS 2021) trained only in simulation and ran on the A1
  without fine-tuning, over rocks, sand, grass and stairs [8].

## Cost and BOM

New Atlas reported a launch price under US$10,000 for the A1 [1]; no exact price was
found, so `cost` stays empty. Unitree's shop now lists the Aliengo at US$50,000 and the Go1 from
US$2,700 (2026-11-18) [9]. MYBOTSHOP lists the A1 as price on request [2].

## What is open

| Item | Format | Where | Licence |
|---|---|---|---|
| URDFs and Gazebo packages (A1, Aliengo, Laikago) | URDF, ROS 1 | unitree_ros [3] | BSD-3-Clause |
| SDK for these models | C++ static library and headers | unitree_legged_sdk v3.3.1 [4] | BSD-3-Clause; the core library is prebuilt |
| MuJoCo model (A1) | MJCF | Menagerie `unitree_a1` [5] | BSD-3-Clause |
| RL tasks | Python | legged_gym [6], Isaac Lab [7] | BSD-3-Clause |
| Hardware, motor and controller firmware | — | Not published | Closed |

## Strengths and limits

- **Strengths:** light (12 kg) and fast (3.3 m/s) for its price [1]; ready models and tasks in
  Menagerie, legged_gym and Isaac Lab, and papers such as RMA to build on [5][6][7][8].
- **Limits:** gone from Unitree's own shop [9]; tied to an old SDK release and ROS 1 [3][4]; a
  prebuilt SDK core and closed firmware [4]; key specs only from press and reseller pages [1][2].

## Related robots

- [Unitree Go2](unitree-go2.md): the current Unitree research quadruped, with Go1 before it.
- [ANYmal](anymal.md): the industrial quadruped legged_gym was first built around.
- [MIT Mini Cheetah](mini-cheetah.md): an earlier small quadruped with low-cost electric actuators.

## Sources

1. [New Atlas: Unitree A1 quadruped robot (2020-05-04)](https://newatlas.com/robotics/unitree-a1-quadruped-robot/), accessed 2026-11-18
2. [MYBOTSHOP (reseller): Unitree A1 product page](https://www.mybotshop.de/Unitree-A1-Quadruped_1), accessed 2026-11-18
3. [unitree_ros README and robot descriptions](https://github.com/unitreerobotics/unitree_ros), accessed 2026-11-18
4. [unitree_legged_sdk README (v3.8.6) and v3.3.1 release](https://github.com/unitreerobotics/unitree_legged_sdk), accessed 2026-11-18
5. [MuJoCo Menagerie: unitree_a1](https://github.com/google-deepmind/mujoco_menagerie/tree/main/unitree_a1), accessed 2026-11-18
6. [legged_gym README and task registry](https://github.com/leggedrobotics/legged_gym), accessed 2026-11-18
7. [Isaac Lab: Unitree asset configs and A1 velocity task](https://github.com/isaac-sim/IsaacLab), accessed 2026-11-18
8. [RMA: Rapid Motor Adaptation for Legged Robots](https://arxiv.org/abs/2107.04034), accessed 2026-11-18
9. [Unitree shop product list](https://shop.unitree.com/), accessed 2026-11-18
10. [unitree_mujoco README and robot list](https://github.com/unitreerobotics/unitree_mujoco), accessed 2026-11-18

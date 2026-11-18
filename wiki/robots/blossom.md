---
type: robot
name: Blossom
summary: Cornell's handcrafted soft social robot (Suguitan and Hoffman), a string-suspended head on five Dynamixel XL-320 servos inside a laser-cut wood frame with a knitted cover; MIT-licensed files and Python software, under USD 250 in parts, inactive since 2022.
tags: [hri, soft-robot, tensile, handcrafted, laser-cut, dynamixel, xl-320, pypot, knitted, research-platform]
category: social
tier: B
openness: full
maker: Michael Suguitan and Guy Hoffman, Human-Robot Collaboration and Companionship Lab, Cornell
year: 2017
license: {hardware: MIT, software: MIT, docs: MIT}
links: {repo: "https://github.com/hrc2/blossom-public", docs: "https://github.com/hrc2/blossom-public/wiki", cad: "https://github.com/hrc2/blossom-public/tree/master/assembly", paper: "https://doi.org/10.1145/3310356", site: }
specs: {dof: 5, payload_kg: , reach_mm: , mass_kg: , size_mm: , speed_mps: , runtime_h: }
stack: {actuators: "5 Dynamixel XL-320 servos: 3 tower motors that pull the head by strings, 1 base yaw, 1 for the ears", mcu: "USB2AX Dynamixel adapter", compute: "host computer running Python 3 (pypot, Flask); a Raspberry Pi also works", sensors: [], sim_models: [], ros2: none}
cost: {type: bom, usd: 250, as_of: 2019-05-21, source: "https://news.cornell.edu/node/311226"}
build: {difficulty: 2, hours: 3, print_hours: }
maturity: {last_commit: 2022-10-31, stars: 52, active: false}
use_cases: [hri, research, companion]
evidence: researched
last_verified: 2026-11-18
sources:
  - {url: "https://github.com/hrc2/blossom-public", title: Blossom repository README and code (config.py, kinematics.py), accessed: 2026-11-18}
  - {url: "https://doi.org/10.1145/3310356", title: "Suguitan and Hoffman: Blossom: A Handcrafted Open-Source Robot, ACM THRI 8(1), 2019", accessed: 2026-11-18}
  - {url: "https://spectrum.ieee.org/blossom-a-creative-handmade-approach-to-social-robotics-from-cornell-and-google", title: "IEEE Spectrum: Blossom, a creative handmade approach to social robotics from Cornell and Google (2017-08-23)", accessed: 2026-11-18}
  - {url: "https://github.com/hrc2/blossom-public/tree/master/assembly", title: Blossom assembly files and BOM (assembly_files.zip), accessed: 2026-11-18}
  - {url: "https://github.com/hrc2/blossom-public/wiki", title: Blossom build guide (GitHub wiki), accessed: 2026-11-18}
  - {url: "https://news.cornell.edu/node/311226", title: "Cornell Chronicle: Soft, social robot brings coziness to home robotics (2019-05-21)", accessed: 2026-11-18}
  - {url: "https://phys.org/news/2024-02-robot-friend-ai-accessible.html", title: "USC via Phys.org: How to build your own robot friend (2024-02-23)", accessed: 2026-11-18}
  - {url: "https://github.com/hrc2/blossom-public/blob/master/LICENSE", title: Blossom LICENSE file, accessed: 2026-11-18}
---

# Blossom

A handcrafted social robot from Guy Hoffman's lab at Cornell: a head hung in a laser-cut wooden
frame, moved by five small Dynamixel servos and dressed in a knitted cover [1][2]. Shown in 2017
with Google's creative technology team [3] and published in 2019 [2], it is a cheap, soft HRI
robot under MIT; the repo has had no commits since 2022-10-31.

## Specs

| Item | Value | Source |
|---|---|---|
| Variant in frontmatter | the Cornell design in `hrc2/blossom-public` | [1] |
| Degrees of freedom | 5 Dynamixel XL-320: three tower motors (IDs 1–3) pull the head; base yaw (ID 4), −140° to 140°; ears (ID 5) | [1] |
| Frame | laser-cut wood, one 6 mm and three 3 mm 12 x 12 in boards; one 1.5 mm acrylic board; a bearing; printed clips | [4] |
| Compliance | the head hangs on six double-looped rubber bands and is pulled by strings | [4][5] |
| Controller | USB2AX adapter from the servo bus to a host computer; no sensors | [4] |
| Cover | knitted or crocheted to published dimensions; ears from any material | [4][5] |

## How it works

Three servos in a central tower pull strings tied to a floating head platform, which hangs from
the tower on rubber bands; a fourth servo turns the whole body, and a fifth pulls the ears on
strings [1][5][6]. The compliant structure makes motion look soft, and the cover hides the
mechanism [3][6]. The kinematics module maps head pitch, roll and height to the tower motors [1].

The software is Python 3 on pypot and Flask: `start.py` plays named gesture sequences from a
command line and serves a web UI on port 8000. A React Native phone app steers the head by
tilting the phone and records gestures, and a Blockly editor ties gestures to a YouTube video's
timeline. The repo ships 115 recorded happy, sad, angry and fearful gestures [1]. There is no
ROS driver or simulation model.

## What it is used for

- **HRI research:** planned with Google as a developer platform and a learning companion for
  autistic children; its first job was reacting physically to videos with a viewer [3].
- **Teaching:** a USC team cut it to 20 printed parts, from 63, for AI education; about USD 250 [7].

## Cost and BOM

The parts cost less than USD 250 (bom, 2019-05-21); the frontmatter uses that upper bound [6].
The repo's BOM lists every part, with McMaster-Carr numbers for the hardware but no prices; the
five XL-320 servos and the USB2AX are the main items [4].

## Building it

**Difficulty 2:** laser cutting, a little printing and gluing, off-the-shelf servos with IDs set
and a calibration script; no soldering or firmware [1][5].

- **Tools:** a 12 x 12 in laser cutter, a small 3D printer and basic hand tools [5].
- **Time:** assembly takes 2 to 3 hours for a first-timer once parts are cut and printed;
  cutting and printing time is not stated [5]. The cut files are CorelDRAW only [4].

## What is open

| Item | Format | Where | Licence |
|---|---|---|---|
| Laser-cut plates, clips, BOM | CorelDRAW (.cdr), STEP, Word | `assembly/assembly_files.zip` [4] | MIT (2018, no holder named) [8] |
| Robot software, kinematics, gestures | Python (pypot, Flask), JSON | repo root, `src/` [1] | MIT [8] |
| Phone app and video editor | React Native (Expo), Blockly HTML | `BlossomApp/`, `blossom_blockly/` [1] | MIT [8] |
| Build guide, knitting dimensions | GitHub wiki | [wiki](https://github.com/hrc2/blossom-public/wiki) [5] | None stated |

## Strengths and limits

- **Strengths:** cheap, soft and easy to restyle; MIT for hardware and software [6][8]; a
  published design with recorded gestures and three ways to puppeteer it [1][2].
- **Limits:** no sensors, so a computer or phone drives it [1]; no published size or mass;
  CorelDRAW-only cut files [4]; Python 3.5-era dependencies such as pycrypto and Flask 1.1.1;
  inactive since 2022 [1].

## What to reuse

- **Hanging head:** rubber bands and three string-pulling servos give soft, springy motion [1][5].
- **Phone-tilt puppeteering:** record gestures quickly, then replay them by name [1].

## Related robots

- [Jibo](jibo.md): a commercial robot with a similar focus on expressive body motion.
- [Stack-chan](stack-chan.md) and [Coglet](coglet.md): open desk companions with printed bodies.

## Sources

1. [Blossom repository README and code (config.py, kinematics.py)](https://github.com/hrc2/blossom-public), accessed 2026-11-18
2. [Suguitan and Hoffman: Blossom: A Handcrafted Open-Source Robot, ACM THRI 8(1), 2019](https://doi.org/10.1145/3310356), accessed 2026-11-18
3. [IEEE Spectrum: Blossom, a creative handmade approach to social robotics from Cornell and Google (2017-08-23)](https://spectrum.ieee.org/blossom-a-creative-handmade-approach-to-social-robotics-from-cornell-and-google), accessed 2026-11-18
4. [Blossom assembly files and BOM (assembly_files.zip)](https://github.com/hrc2/blossom-public/tree/master/assembly), accessed 2026-11-18
5. [Blossom build guide (GitHub wiki)](https://github.com/hrc2/blossom-public/wiki), accessed 2026-11-18
6. [Cornell Chronicle: Soft, social robot brings coziness to home robotics (2019-05-21)](https://news.cornell.edu/node/311226), accessed 2026-11-18
7. [USC via Phys.org: How to build your own robot friend (2024-02-23)](https://phys.org/news/2024-02-robot-friend-ai-accessible.html), accessed 2026-11-18
8. [Blossom LICENSE file](https://github.com/hrc2/blossom-public/blob/master/LICENSE), accessed 2026-11-18

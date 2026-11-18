---
type: robot
name: Jibo
summary: Cynthia Breazeal's countertop social robot (Jibo Inc., 2017), a three-section body turned by three motors with a screen face; a landmark for expressive motion, it lost its cloud in 2019, its assets passed to NTT Disruption in 2020, and a community MIT-licensed server project tries to revive it.
tags: [social-robot, companion, expressive-motion, screen-face, cloud-dependent, discontinued, commercial, mit-media-lab]
category: social
tier: B
openness: closed-reference
maker: Jibo Inc. (assets to SQN Venture Partners in 2018, NTT Disruption in 2020)
year: 2017
license: {hardware: , software: , docs: }
links: {repo: , docs: , cad: , paper: , site: "https://hri2024.jibo.media.mit.edu/"}
specs: {dof: 3, payload_kg: , reach_mm: , mass_kg: 2.7, size_mm: , speed_mps: , runtime_h: }
stack: {actuators: "3 DC motors with belt drives turning the base, torso and head sections", mcu: , compute: "ARM-based embedded processor running Linux; speech and skills through Jibo's cloud", sensors: ["stereo cameras", "six microphones", "touch screen", "touch sensors"], sim_models: [], ros2: none}
cost: {type: retail, usd: 899, as_of: 2017-10-25, source: "https://prnewswire.com/news-releases/meet-jibo-your-new-best-friend-introducing-the-first-social-robot-for-the-home-300542856.html"}
build: {difficulty: , hours: , print_hours: }
maturity: {last_commit: , stars: , active: }
use_cases: [companion, hri, research]
evidence: researched
last_verified: 2026-11-18
sources:
  - {url: "https://prnewswire.com/news-releases/meet-jibo-your-new-best-friend-introducing-the-first-social-robot-for-the-home-300542856.html", title: "PR Newswire: Meet Jibo, your new best friend (2017-10-25)", accessed: 2026-11-18}
  - {url: "https://www.therobotreport.com/jibo-social-robot-assets-acquired-ntt-disruption/", title: "The Robot Report: Jibo social robot assets acquired by NTT Disruption (2020-03-18)", accessed: 2026-11-18}
  - {url: "https://www.engadget.com/2019-03-04-social-robot-jibo-shutting-down-message.html", title: "Engadget: Social robot Jibo does one last dance before its servers shut down (2019-03-04)", accessed: 2026-11-18}
  - {url: "https://www.bartneck.de/2024/01/10/jibo-is-dead-again/", title: "Christoph Bartneck: Jibo is dead (again) (2024-01-10)", accessed: 2026-11-18}
  - {url: "https://spectrum.ieee.org/jibo-is-as-good-as-social-robots-get-but-is-that-good-enough", title: "IEEE Spectrum: Jibo is as good as social robots get. But is that good enough? (2015-12-23)", accessed: 2026-11-18}
  - {url: "https://hri2024.jibo.media.mit.edu/", title: "MIT Media Lab: Jibo Community Social Robot Research Platform, HRI 2024 tutorial", accessed: 2026-11-18}
  - {url: "https://github.com/transcendentsoftware-jd/JiboExperiments", title: JiboExperiments (OpenJibo) repository README and LICENSE, accessed: 2026-11-18}
---

# Jibo

A countertop social robot from Jibo Inc., co-founded by MIT professor Cynthia Breazeal, sold from
October 2017 at USD 899 [1]. **Discontinued:** the company shut down in November 2018 [2], its
servers began going offline in March 2019 [3], NTT Disruption bought its assets in 2020 [2], and
a 2024 blog post reports that NTT Disruption closed in 2023 [4]. Builders study it as a reference
for expressive motion: three motors, a screen face and a voice give it a lot of character.

## Specs

| Item | Value | Source |
|---|---|---|
| Variant in frontmatter | the 2017 consumer Jibo, the only version sold | [1] |
| Degrees of freedom | 3: base, torso and head sections, each turned by a DC motor with a belt drive | [5] |
| Height, mass | about 11 in (about 280 mm); about 6 lb (about 2.7 kg) (maker's claims) | [1] |
| Cameras, audio | stereo cameras; six microphones; two speakers | [5] |
| Face | LCD touch screen | [5] |
| Computer, other | ARM-based embedded processor running Linux; two cooling fans; touch sensors, LEDs, Wi-Fi, Bluetooth | [5] |

The hardware list comes from a December 2015 preview, before shipping [5]. No source gives width,
depth or runtime.

## How it works

The body is three roughly cylindrical sections, base, torso and head, joined on slanted planes.
Turning the sections against each other bends the robot into different poses, so three motors
give a wide range of postures. The team routed wires through the centre so each section can
rotate continuously without twisting cables [5]. Expression combines body motion, the screen face
and a voice built from about 14,000 recorded phrases [5].

Jibo relied on its cloud for most functions [3]. The maker promised a developer SDK for 2018 [1].
When the servers went offline in 2019, Jibo still answered its wake word but no other voice
commands [3]. The MIT Media Lab now runs Jibo as a research platform with a Jibo-ROS framework and
lends robots to US researchers [6]. OpenJibo, an MIT-licensed community project, is building a
self-hosted replacement server; its README calls it experimental, and its last commit was
2026-11-17 [7]. No simulation model was found.

## What it is used for

- **Home companion** in 2017–2019: talking, reacting to people and taking photos [3].
- **HRI research:** the MIT Media Lab's community research platform, shown at HRI 2024 [6].
- **Design reference:** an example of how much character three motors and a screen can carry [5].

## Cost and BOM

| Item | Price | Type | Date | Source |
|---|---|---|---|---|
| Jibo at public launch | USD 899 | retail | 2017-10-25 | [1] |
| Prerelease batch before launch (sold out) | USD 750 | retail | 2015-12-23 | [5] |

Jibo Inc. raised more than USD 3.5 million on Indiegogo in 2014 and nearly USD 73 million in
venture capital [2]. No new units are sold, and no current price was found.

## What is open

| Item | Format | Where | Licence |
|---|---|---|---|
| Hardware, robot software, original cloud | — | Not published; patents went to NTT Disruption [2] | Proprietary |
| OpenJibo replacement server and notes | source, docs | [JiboExperiments](https://github.com/transcendentsoftware-jd/JiboExperiments) [7] | MIT |
| Jibo-ROS research framework | — | MIT Media Lab tutorial materials [6] | None stated |

## Strengths and limits

- **Strengths:** a carefully designed expressive body that gets many poses from three motors [5];
  continuous rotation in every section [5]; still used in HRI research in 2024 [6].
- **Limits:** dead without its cloud since 2019 [3]; its assets changed hands twice and the last
  owner reportedly closed [2][4]; no public SDK, drawings or models; the community server is
  experimental [7].

## What to reuse

- **Slanted joints between stacked sections:** rotating sections on angled planes gives bending
  and leaning poses from simple rotary motors [5].
- **Wiring through the centre** so every joint can turn without limit [5].

## Related robots

- [Vector](anki-vector.md): another consumer social robot whose maker folded; wire-pod revived it.
- [Blossom](blossom.md): an open research robot that also gets its expression from body motion.
- [Pepper](pepper.md): a larger interaction robot that outlived its production.

## Sources

1. [PR Newswire: Meet Jibo, your new best friend (2017-10-25)](https://prnewswire.com/news-releases/meet-jibo-your-new-best-friend-introducing-the-first-social-robot-for-the-home-300542856.html), accessed 2026-11-18
2. [The Robot Report: Jibo social robot assets acquired by NTT Disruption (2020-03-18)](https://www.therobotreport.com/jibo-social-robot-assets-acquired-ntt-disruption/), accessed 2026-11-18
3. [Engadget: Social robot Jibo does one last dance before its servers shut down (2019-03-04)](https://www.engadget.com/2019-03-04-social-robot-jibo-shutting-down-message.html), accessed 2026-11-18
4. [Christoph Bartneck: Jibo is dead (again) (2024-01-10)](https://www.bartneck.de/2024/01/10/jibo-is-dead-again/), accessed 2026-11-18
5. [IEEE Spectrum: Jibo is as good as social robots get. But is that good enough? (2015-12-23)](https://spectrum.ieee.org/jibo-is-as-good-as-social-robots-get-but-is-that-good-enough), accessed 2026-11-18
6. [MIT Media Lab: Jibo Community Social Robot Research Platform, HRI 2024 tutorial](https://hri2024.jibo.media.mit.edu/), accessed 2026-11-18
7. [JiboExperiments (OpenJibo) repository README and LICENSE](https://github.com/transcendentsoftware-jd/JiboExperiments), accessed 2026-11-18

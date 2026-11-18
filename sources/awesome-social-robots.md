---
type: source
name: Awesome Social Robots
registry: awesome-social-robots
url: https://github.com/jcarolinares/awesome-social-robots
commit: "01e8eba"
read_on: 2026-11-17
counts: {entries: 92, pages: 11, waiting: 0, index_only: 45, deferred: 0, rejected: 36}
---

# Awesome Social Robots: what it gives RoboAI

A list of social and companion robots, open and closed, plus virtual pets and learning material.
It finds a few strong open designs (Stack-chan, Sesame, Coglet, ElectronBot, Blossom, InMoov) and
the commercial social robots that set expectations (Jibo, Vector). Most of its entries are small
contest builds, screen gadgets with no moving parts, or virtual pets, so over half are rejected.
Its licence claims are often loose and were checked one by one.

## How it was read

- Read at commit `01e8eba` on 2026-11-17. Phase 3 covers the four robot sections (Open-Source
  Robots, Not Open-Source Robots, To do more social, Virtual Pets): 61 entries.
- **Phase 4** read Libraries, Books, Articles, Blogs, Documentaries, Tutorials and Video
  Tutorials on 2026-11-18 at the same commit, and decided the Cardboard Robots row Phase 3
  deferred: 32 entries, none earning a page. They are small eye-animation and voice libraries for
  social-robot faces, two books, articles and short tutorials. Every link was checked with an HTTP
  request; licences in Libraries are the list's own claims. The Pocket link to the dementia
  article now redirects to Wired, and one library link is dead. Nothing in the README addresses
  agents.
- Repos were checked with shallow git clones; Hackster, Instructables and Arduino Project Hub
  pages were read for files and a stated licence. Instructables builds its pages with JavaScript,
  so four of its licences stay `unknown`; Thingiverse and Printables refuse automated reads.
- A robot needs actuators: devices that only sense and show a face on a screen are rejected as
  not robots. A page needs files a builder can use under a stated licence; non-commercial
  licences are accepted for important projects and named on the page.
- Wrong or loose licence claims in the list, corrected here: Reachy Mini's software is Apache-2.0
  (the list says AGPL-3.0) and its hardware licence is non-commercial; Coglet is CC-BY-NC-4.0, not
  "all resources provided"; InMoov is CC-BY-NC-3.0; Gus 2.0, Grumpy Hedgehog and Omicro Flux state
  no licence at all.
- Dead or moved on 2026-11-17: the Opla Flower and Buddy links (both still on Hackster), jibo.com
  and embodied.com (no response). The Stack-chan link redirects to `stack-chan/stack-chan`, and
  the Reachy link to the Reachy 2 page.

## Pages made

| Entry | Page | Tier |
|---|---|---|
| Stackchan | [Stack-chan](../wiki/robots/stack-chan.md) | A |
| Sesame | [Sesame](../wiki/robots/sesame.md) | A |
| Coglet (Will Cogley) | [Coglet](../wiki/robots/coglet.md) | A |
| InMoov (Gaël Langevin) | [InMoov](../wiki/robots/inmoov.md) | B |
| Kayra | [Kayra](../wiki/robots/kayra.md) | B |
| Reachy Mini (Pollen Robotics) | [Reachy Mini](../wiki/robots/reachy-mini.md) | B |
| Reachy (Pollen Robotics) | [Reachy and Reachy 2](../wiki/robots/reachy.md) | B |
| Blossom (Cornell) | [Blossom](../wiki/robots/blossom.md) | B |
| ElectronBot (Peng Zhihui) | [ElectronBot](../wiki/robots/electronbot.md) | B |
| Jibo (Jibo Inc.) | [Jibo](../wiki/robots/jibo.md) | B |
| Vector (Anki, then Digital Dream Labs) | [Vector (Anki, Digital Dream Labs)](../wiki/robots/anki-vector.md) | B |

## Waiting for a page

| Entry | Page | Tier | Batch | Why it matters |
|---|---|---|---|---|

## Index only

| Entry | What it is | Last commit | Licence |
|---|---|---|---|
| IrisOLED | Arduino library for animated robot eyes on small OLEDs | — | MIT |
| ESP32_Faces | Robot faces on two 8x8 LED matrices | — | GPL-3.0 |
| Robot_eyes | Robot face animations for ESP32 displays | — | GPL-3.0 |
| Spchcat | Offline speech-to-text command-line tool for Linux and Raspberry Pi | 2022-03-03 | MPL-2.0 |
| Googly_Eye | CircuitPython googly eye for a round display with an accelerometer | — | MIT |
| Oled Eye Display | Animated eye library for OLED displays (Intellar) | — | Apache-2.0 |
| (ES) Animación de Ojos Robóticos en Arduino Uno | Spanish-language Arduino library for animated robot eyes | — | none stated |
| Snowboy | Community fork of the discontinued Kitt.AI wake-word engine | 2021-05-02 | Apache-2.0 |
| M5Stack Avatar MIC | M5Stack avatar faces that lip-sync to microphone input | — | MIT |
| M5Stack Avatar | Face library for M5Stack screens, by Stack-chan's creator | — | MIT |
| Voice ChatGPT | Raspberry Pi voice chat with ChatGPT | — | CC-BY-NC (version not stated) |
| Grobot_Animations | Physics-based eye animation library for TFT displays | — | MIT |
| Stack-chan minimal | Gachapon-sized Stack-chan variant with an English voice; on the `stack-chan` page | 2025-08-22 | AGPL-3.0 |
| Wally | M5StickC servo robot for young cancer patients, a contest build | — | CC-BY-NC-SA-4.0 |
| Robot Butterfly | Outdoor companion butterfly kit with KiCad and STEP files, no BOM | 2026-11-13 | CERN-OHL-P-2.0, MIT, CC-BY-SA-4.0 |
| 3D Printed WALL·E | Movie replica with a Raspberry Pi web interface; 3D files carry no licence | 2024-06-09 | GPL-3.0 (code) |
| Cozmars | Printable fan robot in the style of Cozmo; firmware unfinished | 2026-09-10 | MIT (firmware); 3D files unknown |
| Buddy (Slant Concepts) | One-servo printed Arduino desk robot kit, a 2019 showcase | — | CC-BY-NC-ND-4.0 |
| EWON | Raspberry Pi home robot with servo ears and a screen face, a 2020 one-off | — | unknown |
| High-Fivey | Cardboard micro:bit robot for classrooms | — | none found |
| Bipedal Companion Robot (dmt-labs) | Modular printed biped companion, no BOM; inactive | 2025-03-09 | GPL-3.0 |
| Swervebot | LEGO-compatible printed swerve-drive robot | 2025-01-12 | MIT (code) |
| Clawrophyll | Robotic planter with a face and one servo, a contest build | 2026-10-30 | MIT |
| Moxie (Embodied) | Children's companion robot; it stopped working when its maker shut down in 2024 | — | — |
| SkoBots (STEAM Connection) | Shoulder-worn robot that speaks Anishinaabemowin; not sold | — | — |
| ElliQ (Intuition Robotics) | Tabletop eldercare companion | — | — |
| Misa (Misa Robotics) | Wheeled companion robot for children | — | — |
| Cardboard Robots (LOFI Robot) | Classroom cardboard-robot ideas; free plans, paid templates, not open source | — | — |
| PLEN2 | Small printable humanoid with Fusion files; inactive since 2018 | 2018-12-10 | MIT (firmware), CC-BY-4.0 (3D) |
| MiniPlan V6 | Small printed ESP8266 servo robot; inactive, no licence file | 2019-10-17 | none found |
| Human-Robot Interaction in Social Robotics | Book on HRI with social robots (Kanda and Ishiguro) | — | — |
| Designing Sociable Robots | Cynthia Breazeal's book on the Kismet sociable robot | — | — |
| Dogs Obey Commands Given by Social Robots | IEEE Spectrum news on a dog and robot study | — | — |
| Is It Ever OK to Bash a Robot? | Essay on how people treat robots | — | — |
| My Parents' Dementia Felt Like the End of Joy. Then Came the Robots | Wired feature on companion robots in dementia care | — | — |
| Olfactory Puppetry (1 paper) | Paper on smell in social robots and puppetry (DIS 2024) | — | — |
| Vanessa The Robot | Write-up of building a modern animatronic figure | — | — |
| Good night Oppy | Documentary about the Opportunity Mars rover | — | — |
| Retro Tech: Robots | Video on retro consumer robots and people's expectations | — | — |
| Arduino OLED Eyes Animation for Robotics Projects | CircuitDigest round-up of OLED eye libraries for Arduino | — | — |
| Eye animation on OLED display with Arduino Nano | Intellar's tutorial for its OLED eye library | — | — |
| My digital cat - Blinking and making cat's noises | Beginner Arduino tutorial: blinking LED eyes and cat sounds | — | — |
| Doll Blinking Eyes using Arduino UNO Board | Video: blinking doll eyes driven by coils | — | — |
| Oled Moving Eyes Arduino Tutorial | Video: animated OLED eyes on Arduino | — | — |
| Robot eyes animation - Arduino Uno | Video: robot eye animation on Arduino | — | — |

## Deferred

| Entry | What it is | Phase |
|---|---|---|

## Rejected

| Entry | Why | Date |
|---|---|---|
| Cozmo Eyes | One Arduino sketch file; too thin to help a builder | 2026-11-18 |
| Oled Simple Animated Eye | One script, and the list gives no licence | 2026-11-18 |
| OLED-Moving-Eyes-Arduino | Dead link (404) | 2026-11-18 |
| Gus 2.0 | Air-quality monitor with a face: no actuators, no licence | 2026-11-17 |
| Omicro Flux | No licence and no files, only a story page | 2026-11-17 |
| Smart Signage Sentient | A smart sign with no actuators | 2026-11-17 |
| Opla Flower Companion | Dead link, and no actuators | 2026-11-17 |
| Arduino Spider Robot (Quadruped) | Generic 2018 build, not social, licence unverifiable; better open quadrupeds exist | 2026-11-17 |
| Alertin | LED alert box with no actuators | 2026-11-17 |
| Fytó | Smart planter with a screen face, no actuators | 2026-11-17 |
| Grumpy Hedgehog | Gesture-sensor gadget, not a social robot; no licence | 2026-11-17 |
| Baymax Lamp | A timed colour lamp | 2026-11-17 |
| Akno | Arduino code only, no CAD, wiring or BOM | 2026-11-17 |
| Study Buddy | Light sensor and screen only | 2026-11-17 |
| Color-Chan | Colour-to-music gadget with no actuators | 2026-11-17 |
| Power Pet | Hackathon prototype with no build files for the physical part | 2026-11-17 |
| A Robot Arm That Sees You | One-off contest build with no licence | 2026-11-17 |
| Xiaozhi AI Desk Buddy | Voice chatbot with a screen face, no actuators | 2026-11-17 |
| Transparent AI Assistant | News article about Xiaozhi AI Desk Buddy; a duplicate | 2026-11-17 |
| Mei | Student design-portfolio page, no files or product | 2026-11-17 |
| Robotzu useless boxes | A shop for novelty toys | 2026-11-17 |
| Pikachu's Animatronic | A video only, of a trademarked character | 2026-11-17 |
| Duolingo's Owl | A video only, of a trademarked character | 2026-11-17 |
| PettingZoo | Roomba add-on code with no licence; inactive since 2018 | 2026-11-17 |
| OpenTama | Virtual pet handheld, not a robot | 2026-11-17 |
| MCUGotchi | Virtual pet emulator, not a robot | 2026-11-17 |
| Pixel-Pets | Virtual pets for M5Stack screens, not a robot | 2026-11-17 |
| Esp32-Tamagotchi | Virtual pet on a screen, not a robot | 2026-11-17 |
| SIMBIONTE | Screen companion for a 3D printer, not a robot | 2026-11-17 |
| Pet2Dial | Desktop pet on an M5Stack Dial screen, not a robot | 2026-11-17 |
| Clawy | Coding-session status pet on an M5StickC screen, not a robot | 2026-11-17 |
| ArduinoGotchi | Virtual pet emulator, not a robot | 2026-11-17 |
| Arduino Nano Tamagotchi | Port of ArduinoGotchi; not a robot | 2026-11-17 |
| Deskbuddy 2.0 | ESP32 desk pet with a screen face and no licence | 2026-11-17 |
| Plant Monitor Pet | Plant monitor with an animated screen face | 2026-11-17 |
| (ES) Creando un Tamagotchi desde cero | A virtual pet build, not a robot, as in Phase 3 | 2026-11-18 |

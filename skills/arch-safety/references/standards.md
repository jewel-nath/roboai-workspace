# Standards and risk assessment

The standards that decide a robot's safety functions, their editions as the official catalogues
listed them on 2026-11-25, and what the builder brings to a risk assessment. Standards are sold, not
published: buy the ones that apply, cite their catalogue pages, and never copy their text into a
repository. Several are under revision, so open the catalogue page again before relying on an edition.

## By robot type

| Robot | Product (type-C) standard | Status on 2026-11-25 |
|---|---|---|
| Industrial arm, as a product | [ISO 10218-1:2025](https://www.iso.org/standard/73933.html) Robotics — Safety requirements — Part 1: Industrial robots | Edition 3, published 2025-02; the 2011 edition is withdrawn |
| Industrial arm in a cell or application, collaborative applications included | [ISO 10218-2:2025](https://www.iso.org/standard/73934.html) Part 2: Industrial robot applications and robot cells | Edition 2, published 2025-02; the 2011 edition is withdrawn |
| Collaborative application, contact limits | [ISO/TS 15066:2016](https://www.iso.org/standard/62996.html) Robots and robotic devices — Collaborative robots | Still listed as current (confirmed 2022), stage 90.92 "to be revised"; to be replaced by [ISO/AWI 15066-1](https://www.iso.org/standard/91522.html) Physical contact with robots — Part 1: Biomechanical thresholds and data (stage 20.00) |
| AGV, AMR, tugger, under-cart robot in industrial use | [ISO 3691-4:2023](https://www.iso.org/standard/83545.html) Industrial trucks — Safety requirements and verification — Part 4: Driverless industrial trucks and their systems | Edition 2, published 2023-06, stage 90.92; edition 3 at [ISO/DIS 3691-4](https://www.iso.org/standard/88615.html), close of voting (40.60) |
| Industrial mobile robot (mobile manipulator and similar) | [ISO/WD 26058-1](https://www.iso.org/standard/92460.html) Safety requirements for industrial mobile robots — Part 1 | Working draft (20.60); nothing to buy yet |
| Personal care robot: mobile servant, physical assistant, person carrier | [ISO 13482:2014](https://www.iso.org/standard/53820.html) Robots and robotic devices — Safety requirements for personal care robots | Current (confirmed 2020), stage 90.92 |
| Service robot, personal or professional/commercial use | [ISO 13482](https://www.iso.org/standard/83498.html) edition 2, Robotics — Safety requirements for service robots | Under publication (60.00); will replace ISO 13482:2014 and widens the scope to professional use; excludes industrial and medical robots |
| Any other machine | No type-C standard: work from ISO 12100 and the group standards below | — |

Robots outside these scopes, medical robots among them, need their own standards; this skill does not
cover them.

### What the 2025 ISO 10218 did to ISO/TS 15066

From A3's [FAQ on the updated ISO 10218](https://www.automate.org/robotics/blogs/updated-iso-10218-faq)
(2025-03-20; A3 is secretary of the ISO working group):

- The safety requirements for collaborative applications that were the content of ISO/TS 15066 moved
  into ISO 10218-2:2025. The safety functions that enable a collaborative task can sit in the robot,
  in a protective device, or both.
- The standard speaks of a "collaborative application", not a "collaborative robot": only an
  application can be designed, tested and confirmed as collaborative.
- "Safety-rated monitored stop" is renamed "monitored standstill".
- Functional safety requirements are stated explicitly, and Part 2 adds cybersecurity requirements
  where they bear on robot safety.

ISO/TS 15066:2016 itself is still listed as current while its replacement is drafted. Which document
supplies the contact limits for a given application is a question for the assessor.

## Group and basic standards

| Standard | Edition on its catalogue page | Use it for |
|---|---|---|
| [ISO 12100:2010](https://www.iso.org/standard/51528.html) Safety of machinery — General principles for design — Risk assessment and risk reduction | Edition 1, stage 90.92; [ISO/DIS 12100.3](https://www.iso.org/standard/88578.html) (edition 2) at close of voting (40.60) | The risk assessment method |
| [ISO 13849-1:2023](https://www.iso.org/standard/73481.html) Safety-related parts of control systems — Part 1: General principles for design | Edition 4, published 2023-04 | Designing and integrating a safety function to its required performance level (PLr) |
| [IEC 62061:2021+AMD1:2024+AMD2:2026](https://webstore.iec.ch/en/publication/112847) Functional safety of safety-related control systems | Consolidated edition 2.2, 2026-03 | The IEC route, rated in SIL instead of PL |
| [IEC 60204-1:2016](https://webstore.iec.ch/en/publication/26037) with [AMD1:2021](https://webstore.iec.ch/en/publication/66124) Electrical equipment of machines — Part 1 | Edition 6.0, stability date 2027 | Stop categories, emergency stop wiring, control circuits, Safe Torque Off of drive systems |
| [ISO 13850:2015](https://www.iso.org/standard/59970.html) Emergency stop function — Principles for design | Edition 3, stage 90.92; ISO/WD 13850 under development | The emergency stop function itself |
| [IEC 61800-5-2:2016+AMD1:2026](https://webstore.iec.ch/en/publication/117563) Power drive systems — Safety requirements — Functional | Consolidated edition 2.1, 2026-10 | Drives whose safety sub-functions (such as Safe Torque Off) are rated |

ISO 13849-1 itself says it does not set the safety functions or the PLr for a given application: those
come from the type-C standard or from the risk assessment. Any table that maps "emergency stop" or
"protective stop" to a fixed PL or SIL is invented.

Regional law decides which standards a product must meet (machinery regulation, workplace rules); a
national adoption of an ISO standard can lag the ISO edition. Check both with the assessor.

## Risk assessment: what the builder brings

ISO 12100's method, per its abstract: identify hazards, estimate and evaluate risks over every phase of
the machine's life, remove hazards or reduce risks enough, and document and verify the result. Risk
reduction follows a fixed priority, summarised by Keyence's
[3-step method page](https://www.keyence.com/ss/products/safetyknowledge/about/method/): inherently
safe design first, then safeguarding and complementary protective measures (fences, light curtains,
scanners, emergency stop), then information for use. A ROS node is none of these three: at most it
makes a hazard less likely to be reached in normal use.

A qualified person leads the assessment. Bring them facts, not conclusions:

| Bring | From |
|---|---|
| Intended use, foreseeable misuse, who is near the robot and how often | The project brief, site visit |
| Every life phase: transport, commissioning, teaching, normal work, fault recovery, maintenance, cleaning, disposal | The bringup and maintenance plans |
| Masses, payloads, maximum speeds and forces, stored energy (springs, batteries, raised loads, pneumatics) | URDF inertials, motor and drive data sheets, battery data |
| Measured stopping time and distance for each stop category, at maximum speed and payload | Tests in [stop-chain.md](stop-chain.md) |
| Each mode (automatic, manual, teach, maintenance) and how it is selected | The state machine and the operator panel |
| What every software layer does and how it was tested | [software-layers.md](software-layers.md), the fault-injection log |
| Network exposure: who can command the robot, from where | [sros2.md](sros2.md), the network plan |

What comes back, and what the build needs from it:

- A hazard list, each hazard with its risk reduction measure and who owns the measure.
- For each safety function (emergency stop, protective stop, speed or zone limiting, enabling
  device in teach mode, and so on): its trigger, its reaction, the stop category, the PLr or SIL,
  and the rated parts that will implement it.
- The tests that validate each safety function, and when they repeat.
- The residual risks that go into the manual and onto the robot.

Keep it in the project, for example `projects/<name>/docs/safety/` with the assessment, the
fault-injection log and the parameter values the tests used. Re-assess when the robot, its task, its
place or its speed changes.

## Signs the work is not ready for an assessor

- Any hazard whose only measure is a ROS node, a topic, a Linux service or an unrated microcontroller.
- An emergency stop that reaches the motors through software.
- No measured stopping distance.
- Limits and timeouts in the parameter files that differ from the ones in the test log.

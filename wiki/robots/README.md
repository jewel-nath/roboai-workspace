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
| [SO-101](so-101.md) | arm | A | full | 6 | — | 229.88 bom (2026-11-17) | researched | 2026-11-17 |
| [SO-ARM 102](so-arm-102.md) | arm | A | full | 6 | 0.3 | 388.4 bom (2026-11-17) | researched | 2026-11-17 |
| [Aero Hand Open](aero-hand-open.md) | gripper | A | full | 7 | — | 316.48 bom (2026-11-17) | researched | 2026-11-17 |
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
| [Coglet](coglet.md) | social | A | partial | 9 | — | 189.38 kit (2026-11-17) | researched | 2026-11-17 |
| [Stack-chan](stack-chan.md) | social | A | full | 2 | — | 99 retail (2026-11-17) | researched | 2026-11-17 |
<!-- index:end -->

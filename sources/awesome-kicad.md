---
type: source
name: Awesome Kicad
registry: awesome-kicad
url: https://github.com/joanbono/awesome-kicad
commit: "57a3635"
read_on: 2026-11-26
counts: {entries: 87, pages: 0, waiting: 11, index_only: 46, deferred: 0, rejected: 30}
---

# Awesome Kicad: what it gives RoboAI

A list of 87 KiCad add-ons and resources: the official IPC API bindings, plugins for
panelisation, fab outputs, PCB design, presentation, review and conversion, the official
libraries, tutorials and project lists. The list is also published as a third-party KiCad PCM
repository. It grew fast in 2026, mostly through entries added by their own authors, and nine of
them are AI or agent tools. It gives the PCB batch seven helper pages (KiKit, KiBot,
Interactive HTML BOM, kicad-jlcpcb-tools, SKiDL, kicad-python, KiCad StepUp) and the official
libraries for the KiCad page. It names no general KiCad MCP server.

## How it was read

- Read at commit `57a3635` (2026-11-25) on 2026-11-26 from a full clone: the README in full (87
  entries: an API section, plugins in eight subsections, symbols, footprints, 3D models,
  tutorials, component import, Verilog tools and project collections), `CONTRIBUTING.md`, and
  `scripts/build_pcm_repository.py`, read but not run.
- The list doubles as a third-party PCM repository. KiCad users can add its `repository.json`,
  which the script rebuilds from the listed add-ons that ship a PCM archive, taking each
  upstream's metadata as it is. KiCad does not review it; the official index is triaged in
  [kicad-pcm-index](kicad-pcm-index.md).
- Dating and licences: every linked repo was dated on 2026-11-26 from a depth-1 clone without
  blobs (head commit date). Licences come from the github.com page, GitLab's project data for
  gitlab.com repos, or the licence file or README where GitHub shows none or cannot classify it:
  kicanvas and Gingerbread are MIT, plotkicadsch is BSD-3-Clause, typeCAD is Apache-2.0 (its
  `package.json`), and KiCad StepUp is AGPL-3.0 by its README and `package.xml`, with no licence
  file. Web-only entries were checked with one HTTP request.
- Page candidates had their READMEs read and their newest release taken from github.com: KiKit
  v1.8.1, PcbDraw v1.3.0, KiBot v1.9.1, Interactive HTML BOM v2.12.0, kicad-jlcpcb-tools
  2026.04.03, SKiDL 3.0.0, kicad-happy v3.0.2. kicad-python (GitLab, MIT, 2026-11-24) says the IPC
  API needs KiCad 9 or later and a running KiCad, and that the SWIG bindings are removed in
  KiCad 11. kicad-jlcpcb-tools installs from its author's own PCM repository, not the official
  index; the official index carries bennymeg's Fabrication Toolkit instead (an index row there).
- Rules: rejected when archived, without a licence, a closed web service, a vendor's teaching
  material, off-topic, or small (under 50 stars) with no commit since 2025-05-26. The official
  libraries are rows of the KiCad page. Tools that are also in the official index have the same
  slug and decision in [kicad-pcm-index](kicad-pcm-index.md). KiCad StepUp is a FreeCAD workbench,
  so the CAD batch and the FreeCAD Addons note may meet it too; `tools/kicad-stepup` is a proposed
  slug, not a shared one.
- AI and agent entries, triaged with care for the PCB batch's KiCad MCP guide: kicad-happy (index;
  agent skills that read and review KiCad files), akcli and kicad-splitplane (index; splitplane's
  MCP server does one task), Cherry Blossom (index; MCP only through its hosted app), Koppar,
  BoardRepo, Calligraphy and CircuitAgent (rejected: paid or hosted services, or an open-core
  alpha), and Circuitron (rejected: archived). None is a general KiCad MCP server, and Konnect is
  not listed. kicad-python is the API such a server would use.
- Moved: KiCost to `hildogjr/KiCost`; kicad-footprint-generator to
  `kicad/libraries/kicad-library-tools`, which now holds footprint, symbol and 3D-model
  generators; kicad-component-handler to `HarveyBates/kandle`; open-pcb-routing-benchmark to
  `calligraphysystems-admin`. No link was dead on 2026-11-26.
- Errors in the list: the Calligraphy entry promises a KiCad 8, 9 and 10 plugin with local
  impedance and DFM tools and an MCP server, while its README offers a KiCad 8 and 9 front end for
  a paid routing service and points to a separate MCP repo (`vibe-hardware-mcp`, not checked).
  Circuitron's README says the project is archived; GitHub does not mark it so. Svg2Shenzhen is
  marked discontinued. KiCad RF Tools is GPL-3.0 on GitHub but GPL-2.0 in its PCM metadata.
- Most entries added in 2026 came from their own authors or vendors (commit authors match the
  linked repos), and several are weeks old with no stars. One account added four PCBA Partner
  items: a toolkit and three teaching items.
- Addressed to agents: kicad-happy's README tells the reader to "have your AI agent read" its
  install guidance. Calligraphy and kicad-splitplane ship `llms.txt` files and agent skills, and
  BoardRepo's README says its server's instructions govern agents. None was followed; nothing past
  the READMEs was read. The list's own README addresses no agent.
- No section holds only papers. Nothing is deferred.
- Cross-check across the Phase 5 notes (2026-11-26) moved two rows to Index only: PcbDraw, to
  match the awesome-robotic-tooling note (KiBot drives it, and the KiCad page can name it), and
  kicad-happy, because a skill pack is not a wiki page: the PCB batch reviews it as a possible
  source for the `pcb-kicad` skill and registers it if the skill uses it.

## Pages made

| Entry | Page | Tier |
|---|---|---|

## Waiting for a page

| Entry | Page | Tier | Batch | Why it matters |
|---|---|---|---|---|
| kicad-python | `software/kicad-python` | B | pcb | Official Python client for KiCad's IPC API (KiCad 9+); the supported way for a script or an agent to drive a running KiCad, as the SWIG bindings go in KiCad 11 |
| KiKit | `tools/kikit` | B | pcb | Panelises boards and exports fab files from presets, by CLI, library or plugin; the most-starred KiCad automation tool here |
| Kicad JLCPCB Tools | `tools/kicad-jlcpcb-tools` | B | pcb | Assigns LCSC parts and writes JLCPCB's Gerber, BOM and placement files; JLCPCB is the fab several Atlas robots name |
| KiBot | `tools/kibot` | B | pcb | Makes every fab and documentation output from one YAML file, in CI or a Makefile; the scriptable output route |
| SKiDL | `software/skidl` | B | pcb | Circuits written in Python, output as KiCad netlists and schematics; the code-first design route an agent can write |
| InteractiveHtmlBom | `tools/interactive-html-bom` | B | pcb | Interactive BOM that highlights each part on the board; the standard aid for hand assembly |
| KiCadStepUp | `tools/kicad-stepup` | B | pcb | FreeCAD workbench that moves boards, outlines and 3D models between KiCad and FreeCAD; the bridge between two first-class tools |
| Official KiCad Symbols | `tools/kicad` | A | pcb | KiCad's stock symbol library (CC-BY-SA-4.0); the KiCad page covers the official libraries |
| Official KiCad Footprints | `tools/kicad` | A | pcb | KiCad's stock footprint library (CC-BY-SA-4.0) |
| KiCad Footprint Generator | `tools/kicad` | A | pcb | Now `kicad-library-tools` (GPL-3.0): the official scripts that generate footprints, symbols and 3D models; the scripted way to make custom parts |
| Official KiCad 3D Models | `tools/kicad` | A | pcb | KiCad's stock 3D part models (CC-BY-SA-4.0), behind the board STEP export to CAD |

## Index only

| Entry | What it is | Last commit | Licence |
|---|---|---|---|
| PcbDraw | Draws boards as 2D images for pinout diagrams and build docs; KiBot drives it, and the `tools/kicad` page names it | 2026-10-09 | MIT |
| kicad-happy | Agent skills (Claude Code, Codex and others) that parse and review KiCad projects; the PCB batch reviews it for the `pcb-kicad` skill | 2026-11-15 | MIT |
| kicad-rs | Official Rust bindings for the IPC API | 2025-11-09 | GPL-3.0-or-later |
| ReplicateLayout | Copies one hierarchical sheet's layout to its other copies; also in the PCM | 2026-05-07 | GPL-2.0 |
| KiABOM | BOM with supplier prices and stock from online APIs | 2026-10-23 | GPL-3.0 |
| KiCost | Cost spreadsheet from distributor prices; moved to `hildogjr/KiCost` | 2026-07-08 | MIT |
| JLCKicadTools | CLI that turns KiCad outputs into JLCPCB BOM and placement files; low activity | 2025-05-01 | GPL-3.0 |
| kicad-gerberzipper | Plots and zips Gerbers per fab house; the PCM carries its successor, Gerber Zipper 2 | 2026-07-13 | MIT |
| gerber_to_order | Zips Gerbers for Elecrow, FusionPCB, PCBWay or JLCPCB; also in the PCM | 2026-09-29 | MIT |
| KiCad Better BOM | Another formatted BOM generator | 2026-06-17 | MIT |
| PCB TraceMill | Turns KiCad Gerber and drill files into G-code for milling boards on a hobby CNC router | 2026-11-24 | MIT |
| PCBA Partner Fabrication Toolkit | Exports Gerber, BOM and placement files with a pre-flight report; from an assembly vendor | 2026-10-15 | GPL-3.0 |
| NCCM | Clearance matrix between net classes, written as custom rules; also in the PCM | 2026-03-31 | GPL-3.0 |
| Gingerbread | Browser tool that turns vector art into KiCad board graphics; replaces Svg2Shenzhen | 2026-08-16 | MIT |
| silk reel | Turns a board file into a short animated film | 2026-11-21 | Apache-2.0 |
| KiBuzzard | Silkscreen labels in many fonts; also in the PCM | 2026-04-09 | MIT |
| Kobee Studio | Silkscreen labels, icons, QR codes and header overlays; grew out of KiBuzzard; also in the PCM | 2026-11-11 | GPL-2.0 (PCM metadata) |
| Stretch | Round trip between KiCad and Inkscape for artistic boards; also in the PCM | 2025-06-06 | GPL-3.0 |
| FreeRouting | Open autorouter with an official KiCad plugin in the PCM; needs Java | 2026-11-25 | GPL-3.0 |
| uConfig | Extracts pinouts from datasheet PDFs into KiCad symbols | 2026-02-24 | GPL-3.0 |
| KiCad RF Tools | RF footprint wizards, rounded tracks, via fences and mask tools; also in the PCM | 2024-11-11 | GPL-3.0 |
| Import-LIB-KiCad-Plugin | Imports parts downloaded from SnapEDA, Ultra Librarian and others; in the PCM as impart GUI | 2026-10-20 | GPL-3.0 |
| typeCAD | Designs boards in TypeScript and writes KiCad files; alpha | 2026-11-21 | Apache-2.0 |
| Rectangulator | Turns zones into exact rectangles | 2026-04-30 | MIT |
| Img2Silk | Dithers images into silkscreen or copper graphics | 2026-07-07 | MIT |
| RFgen | Generates RF footprints and antennas | 2026-09-14 | MIT |
| kicad-splitplane | Splits a shared power layer into one zone per net; plugin, CLI and an MCP server for that one task; also in the PCM | 2026-11-23 | MIT |
| Cherry Blossom | Browser schematic and PCB editor that imports and exports KiCad projects; agents connect only through its hosted app's MCP server | 2026-11-22 | AGPL-3.0 |
| plotkicadsch | Plots KiCad schematics to image files | 2026-07-26 | BSD-3-Clause |
| KiCad-Diff | Image diffs of board layouts between revisions; inactive since 2023, used by kiri | 2023-03-19 | MIT |
| kiri | Visual review of schematic and layout changes across git commits | 2026-06-22 | MIT |
| gerber2blend | Builds Blender 3D models of boards from Gerbers (Antmicro) | 2025-12-03 | Apache-2.0 |
| gerber2ems | Simulates trace signal integrity from Gerbers with openEMS (Antmicro) | 2026-11-19 | Apache-2.0 |
| kicanvas | Interactive browser viewer for KiCad schematics and boards | 2026-04-29 | MIT |
| RFsim | KiCad 10 plugin that simulates RF structures with openEMS | 2026-10-20 | MIT |
| akcli | Python CLI that lets an agent write and check `.kicad_sch` files from JSON op-lists, with ERC, ngspice and JLCPCB parts; young | 2026-11-23 | MIT |
| KiCAD-Prism | Self-hosted web app for reviewing KiCad projects from git | 2026-11-05 | Apache-2.0 |
| ZiroEDA | KiCad 10 ported to run in the browser | 2026-11-20 | GPL-3.0 |
| kicad-irdrop | DC voltage-drop analysis of power rails on the real copper | 2026-11-25 | Apache-2.0 |
| kisi | Signal and power integrity checks in a browser viewer or CLI; also in the PCM | 2026-11-22 | GPL-3.0 |
| KiCad Color Schemes | Colour themes; seven of them are in the PCM | 2021-12-05 | CC0-1.0 |
| autorouter-bench | Benchmark of six autorouters, Freerouting among them, on eight open boards, scored by kicad-cli; made by Koppar, a vendor | 2026-10-22 | MIT |
| open-pcb-routing-benchmark | Routing benchmark scored by kicad-cli DRC; made by Calligraphy, a vendor; moved to `calligraphysystems-admin` | 2026-11-11 | MIT |
| Arduino Kicad Library | Symbols and footprints for Arduino boards and modules; also in the PCM | 2026-11-15 | CC-BY-SA-4.0 |
| KiCadVerilog | Generates Verilog from a KiCad netlist | 2024-11-02 | MIT |
| Awesome KiCad Projects | A list of open hardware projects designed in KiCad | 2026-11-13 | CC-BY-4.0 |

## Deferred

| Entry | What it is | Phase |
|---|---|---|

## Rejected

| Entry | Why | Date |
|---|---|---|
| panelize-plugin | Inactive since 2020, no licence; KiKit covers panelisation | 2026-11-26 |
| KiBoM | Archived upstream; KiCad's own BOM export and KiBot cover it | 2026-11-26 |
| KiZip | Inactive since 2022; the fab-export plugins cover it | 2026-11-26 |
| KiCad JLCPCB BOM Plugin | No licence, inactive since 2023; Kicad JLCPCB Tools covers it | 2026-11-26 |
| kicad-bom-seeedstudio | Inactive since 2017, no licence | 2026-11-26 |
| Copper Thief Plugin | Small (13 stars) and inactive since 2024; Copper Filler in the PCM does the same | 2026-11-26 |
| BOM2Md | No licence, inactive since 2023 | 2026-11-26 |
| Salitronic Gerber Analyzer | Closed web tool from a vendor; KiCad's GerbView views Gerbers | 2026-11-26 |
| Wave Fixture AI | Off-topic: wave-soldering fixtures for production lines; added by its author, 1 star | 2026-11-26 |
| Svg2Shenzhen | Discontinued, as the list says; Gingerbread replaces it | 2026-11-26 |
| svg2mod | Inactive since 2018; a fork lives at `svg2mod/svg2mod` | 2026-11-26 |
| Laser Stencil Plugin | Small (22 stars) and inactive since 2024 | 2026-11-26 |
| Stimulu KiCad Plugins | Inactive since 2019, no licence, 1 star | 2026-11-26 |
| KiCad Templates | Inactive since 2019, from the KiCad 5 era | 2026-11-26 |
| Circuitron | Its README says the project is archived; it was an OpenAI Agents pipeline that wrote SKiDL | 2026-11-26 |
| Koppar | Closed paid service (three free designs, then per board or subscription), with an MCP server | 2026-11-26 |
| CircuitAgent | Alpha open-core layer: the compiler is not in the repo; 2 stars, added by its author | 2026-11-26 |
| calligraphy-kicad-plugin | Front end for a paid routing service; the list's description does not match its README | 2026-11-26 |
| BoardRepo | Plugin wrapper for a hosted, closed MCP service that needs an account | 2026-11-26 |
| Loft Gerber Viewer | Closed web tool from a vendor | 2026-11-26 |
| Loft Compare PDF | Closed web tool; a general PDF diff | 2026-11-26 |
| Altium2Kicad | Archived upstream; KiCad imports Altium designs itself | 2026-11-26 |
| Eagle to KiCad | Inactive since 2022; KiCad's own Eagle importer and Eagle Exhumer (PCM) cover it | 2026-11-26 |
| kicad-wakatime | Off-topic (time tracking), no licence, made for KiCad 8.99 nightlies | 2026-11-26 |
| Keyboard PCB guide | Keyboard tutorial from 2017 (KiCad 4 era), no licence | 2026-11-26 |
| Hawk | Tutorial inactive since 2020, no licence | 2026-11-26 |
| KiCad BOM and placement export exercises | Vendor teaching material (PCBA Partner), added by the vendor | 2026-11-26 |
| Gerber layer checks teaching pack | Vendor teaching material (PCBA Partner), 0 stars | 2026-11-26 |
| KiCad export compatibility teaching pack | Vendor teaching material (PCBA Partner), 0 stars | 2026-11-26 |
| Kandle | Small (48 stars) and inactive since 2024; impart GUI covers importing vendor parts | 2026-11-26 |

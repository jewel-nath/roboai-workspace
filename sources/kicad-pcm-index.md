---
type: source
name: Official KiCad Addon Metadata Repository
registry: kicad-pcm-index
url: https://gitlab.com/kicad/addons/metadata
commit: "00a8f3c"
read_on: 2026-11-26
counts: {entries: 133, pages: 0, waiting: 3, index_only: 98, deferred: 0, rejected: 32}
---

# KiCad PCM index: what it gives RoboAI

The metadata behind KiCad's official Plugin and Content Manager: one file per package, 150 in all
(115 plugins, 17 libraries, 18 colour themes), each with its versions, KiCad range, licence and
download. It is what a builder can install from inside KiCad without adding a third-party
repository, so it shows which helpers are packaged and current. It gives the PCB batch two pages,
KiKit and Interactive HTML BOM, both shared with [awesome-kicad](awesome-kicad.md). Most of the
rest are small single-task PCB plugins, fab-house plugins and part libraries, which are index
rows. It holds no MCP server.

## How it was read

- Read at commit `00a8f3c` (2026-11-15) on 2026-11-26 from a full clone (648 commits since
  2021-08): the README and all 150 `packages/*/metadata.json` files (name, type, licence,
  description, versions with status and KiCad range), with each package's first and last change
  from the git history. The README says KiCad's CI builds the public repository
  (`kicad/addons/repository`) from this folder; the published `packages.json` at
  repository.kicad.org (updated 2026-11-16) lists the same 150 packages.
- The 18 colour themes are one Index only row, so 150 packages make 133 rows.
- Licence: each package's own metadata. Where the linked repo says otherwise, both are given
  (PCB Coil Creator, KiCAD Testpoints, RF-Tools, kicad-action-scripts). Last commit: the linked
  repo's head commit, from a depth-1 clone without blobs on 2026-11-26; `—` where the package
  links no repo. Stars and archive flags come from the github.com pages, as in awesome-kicad.
- Seven packages have no version left and do not install: the PCBGOGO pair and the GitLab NextPCB
  pair (English and Japanese each), CB KiCAD Libraries, Length Matching (named "[Delisted]") and
  the Eagle Dark theme, which is counted in the themes row.
- Rules, as in awesome-kicad: rejected when no version is left, a duplicate, archived, for KiCad 7
  or older only, off-topic (keyboards, tamper meshes, note-taking, instrument panels, magazine
  symbol styles), or small (under 50 stars) with no commit since 2025-05-26. Eleven fab-house
  plugins (PCBWay, Huaqiu's NextPCB and HQ, AISLER, AIVON, LionCircuits, Sierra Circuits) are
  index rows marked vendor. Tools also in awesome-kicad have the same slug and decision there.
- The index lags some upstreams: KiKit is 1.6.0 here (metadata last changed 2024-07-19) while its
  newest release is v1.8.1, and Freerouting is 2.5.0 against v2.6.0. The KiKit page should give
  the upstream install as well.
- Moved: `bennymeg/JLC-Plugin-for-KiCad` is now `bennymeg/Fabrication-Toolkit`;
  `2231puppy/kicad-vampire` is `miameows/kicad-vampire`; `franzee/kicad-addons` redirects to
  `mgyger/kicad-addons`, so the two Elektuur packages are one library under an old and a new
  identifier.
- AI and agents: no package is an MCP server. traces uses an LLM (local Ollama or OpenRouter) for
  part sourcing and netlist checks through a local server, which its repo also offers as an MCP
  server; kicad-splitplane's MCP server ships separately on PyPI; VelaTrace's description cites AI
  reviewers for its own validation. KiCad itself, its official libraries and Konnect are not
  packages here.
- Nothing in the metadata is addressed to agents. No package is a paper; nothing is deferred.

## Pages made

| Entry | Page | Tier |
|---|---|---|

## Waiting for a page

| Entry | Page | Tier | Batch | Why it matters |
|---|---|---|---|---|
| KiKit | `tools/kikit` | B | pcb | Panelisation and fab outputs by CLI, library or plugin; the index holds 1.6.0 while upstream is at v1.8.1 |
| KiKit Library | `tools/kikit` | B | pcb | KiKit's symbols and footprints for panel annotations, installed beside KiKit |
| Interactive Html Bom | `tools/interactive-html-bom` | B | pcb | Interactive BOM that highlights each part on the board; the standard aid for hand assembly; 2.12.0 for KiCad 6 to 10 |

## Index only

| Entry | What it is | Last commit | Licence |
|---|---|---|---|
| Freerouting | Official KiCad integration of the Freerouting autorouter; needs Java; 2.5.0 here, v2.6.0 upstream | 2026-11-25 | GPL-3.0 |
| kicad-splitplane | Splits a shared power layer into one zone per net; its MCP server ships separately on PyPI | 2026-11-23 | MIT |
| SpinRender | Animated renders and videos of boards | 2026-10-06 | GPL-3.0 |
| pcb2blender | Exports boards to Blender for product renders; KiCad 9 only | 2026-04-21 | GPL-3.0 |
| 4ms Kicad Libraries | Symbols and footprints with part numbers, some with JLCPCB numbers; made for audio gear | 2026-11-21 | Unlicense |
| PCB Coil Creator | Single and multilayer PCB coils as footprints or on the board | 2025-09-12 | GPL-3.0 (repo: AGPL-3.0) |
| Space-Filling_Curve | Draws Hilbert, Moore and Peano curves as copper | 2025-11-23 | GPL-3.0 |
| HQ DFM | Vendor DFM check (Huaqiu) for about ten manufacturing risks | 2026-10-26 | MIT |
| HQ PCB | Vendor plugin: exports fab files and uploads them for an HQ PCB quote (Huaqiu) | 2026-05-13 | MIT |
| Component Search | Vendor part search (Huaqiu) by part number, description or parameters | 2025-04-12 | MIT |
| NextPCB | Vendor plugin: exports fab files and uploads them for a NextPCB quote (Huaqiu) | 2026-05-13 | MIT |
| Net Class Clearance Matrix (NCCM) | Clearance matrix between net classes | 2026-03-31 | GPL-3.0 |
| Archive 3D Models | Copies a board's 3D models into the project; KiCad 6 to 9.1 | 2026-04-08 | GPL-2.0 |
| Place Footprints | Places footprints in lines, circles or grids; KiCad 10 | 2026-04-08 | GPL-2.0 |
| Replicate Layout | Copies one hierarchical sheet's layout to its copies; KiCad 10 | 2026-05-07 | GPL-2.0 |
| Save/Restore Layout | Saves a sheet's partial layout for reuse in other projects; KiCad 9 | 2026-05-07 | GPL-2.0 |
| SwapStubs | Swaps two pins' connections and keeps the schematic in sync; KiCad 8 to 9.1 | 2026-04-08 | GPL-2.0 |
| LionCircuits Fabrication Export | Vendor plugin: one-click Gerber, drill, BOM, placement and test-netlist export; 0 stars | 2026-08-12 | MIT |
| SiFli Library | Symbols, footprints and 3D models for SiFli chips and modules | 2026-06-11 | CC-BY-SA-4.0 |
| Parasitics | DC resistance and inductance between two points on a board | 2026-10-18 | GPL-3.0 |
| impart GUI for KiCad | Imports parts downloaded from Octopart, SamacSys, Ultra Librarian, SnapEDA and EasyEDA | 2026-10-20 | GPL-3.0 |
| PCB to Fritzing Part | Exports a board as a Fritzing part | 2026-06-03 | MIT |
| Parts Placer | Places, flips and rotates parts from a spreadsheet, so mechanical positions stay in version control | 2025-06-26 | LGPL-2.1 |
| KiCAD Testpoints | Report of pads marked as test points | 2025-06-26 | LGPL-3.0 (repo: LGPL-2.1) |
| Via Patterns | Adds vias in patterns | 2026-07-23 | MIT |
| Bakery | Copies global symbols, footprints and 3D models into project libraries; KiCad 10 | 2026-10-31 | GPL-3.0 |
| AISLER Push for KiCad | Vendor plugin: one-click upload to AISLER | 2026-09-30 | MIT |
| AIVON Production Toolkit | Vendor plugin: exports Gerber, netlist, BOM and placement files; 0 stars | 2026-08-05 | MIT |
| AIVON Plug-in for KiCad | Vendor plugin: uploads a project to AIVON for a quote; 0 stars | 2026-08-05 | MIT |
| KiCad Library for Arduino Modules | Symbols and footprints for Arduino boards and modules | 2026-11-15 | CC-BY-SA-4.0 |
| Kicad2Gcode | GRBL G-code for milling the outline and drilling holes | 2026-07-07 | MIT |
| gerber to order | Zips Gerbers for several fab houses | 2026-09-29 | MIT |
| OrthoRoute | GPU autorouter over the IPC API; KiCad 10 | 2026-10-20 | MIT |
| Fabrication Toolkit | JLCPCB Gerber, BOM and placement export; repo now `bennymeg/Fabrication-Toolkit` | 2026-09-29 | Apache-2.0 |
| AutoLED | Fills a shape from an image with an LED grid, with schematic and LED map | 2026-09-29 | MIT |
| Kikakuka Footprints | Footprints for Kikakuka's FreekiCAD assembly alignment and fabrication planner | 2026-11-13 | MIT |
| Pinout Generator | Writes component pinouts as Markdown, CSV, C enums, Python dicts or WireViz | 2026-04-23 | MIT |
| kimotor | Parametric PCB motor (stator coil) design; development status | 2024-06-09 | GPL-2.0 |
| prefab-gate | Runs kicad-cli DRC and a schematic parity check on a copy and says whether the board can go to fab | 2026-11-11 | MIT |
| Alternate Kicad Library | About 36,700 symbols and 10,400 footprints aimed at readable schematics | 2026-05-24 | CC-BY-SA |
| KiCad Routing Tools | Rust-accelerated A* autorouter with differential pairs and BGA fanout; testing | 2026-11-25 | MIT |
| KiPI | Power integrity: DC drop, current density and PDN impedance | 2026-11-11 | GPL-3.0 |
| SubLayout | Reuses layouts of hierarchical sheets; development status | 2026-10-14 | BSD-3-Clause |
| pcb-action-tools | Annular-ring check, grid snap, missing 3D model check and more | 2024-11-09 | GPL-2.0 |
| RF-Tools | Rounded tracks, tapers, via fences and track length for RF work | 2024-11-11 | GPL-2.0 (repo: GPL-3.0) |
| VelaTrace | Pre-order checks: part numbers against values, JLCPCB stock, LEDs without resistors; testing | 2026-11-08 | MIT |
| gerber2png Plug-in for KiCad | Exports fab files and opens Fab Lab Kerala's Gerber2Png web app | 2026-10-25 | MIT |
| Gerber Zipper 2 | Gerber, ZIP, BOM and placement output per fab house | 2026-06-28 | MIT |
| KiBuzzard | Silkscreen labels in many fonts | 2026-04-09 | MIT |
| KiComLib Client | Part data through KiCad's HTTP library; needs a KiComLib server | 2026-10-12 | GPL-3.0 |
| Localize Dependencies | Copies external symbols, footprints and 3D models into the project over the IPC API; KiCad 10 | 2026-11-09 | GPL-3.0 |
| Via Stitching | Stitching vias between a net's zones | 2026-11-13 | GPL-3.0 |
| PosOrient | Table of footprint positions and rotations to edit | 2025-09-05 | GPL-3.0 |
| Stretch | Round trip between KiCad and Inkscape | 2025-06-06 | GPL-3.0 |
| kicad-action-scripts | Via stitching and circular zones; KiCad 9 | 2026-03-17 | GPL-2.0 (repo: GPL-3.0) |
| Breadboard Builder | Virtual breadboard checked against the schematic netlist, for teaching | 2026-09-15 | GPL-3.0 |
| Copper Filler | Fills empty board areas with copper patterns (copper thieving) | 2026-06-01 | MIT |
| Pinout Image Generator | Annotated pinout image from the open board | 2026-10-31 | MIT |
| Layout Clone | Copies repeated-circuit placement; KiCad 10; testing, 0 stars | 2026-11-02 | MIT |
| PCB Heatmap | DC current, voltage-drop and temperature maps; KiCad 10; testing | 2026-11-03 | MIT |
| Tracklayer autorouter | Pure-Python autorouter over the KiCad API; testing, 1 star | 2026-11-24 | MIT |
| Round Tracks | Rounds track corners, for flex boards or looks | 2024-12-04 | Apache-2.0 |
| Kobee Studio | Silkscreen labels, icons, QR codes and header overlays; KiCad 10 | 2026-11-11 | GPL-2.0 |
| Project Instances | Includes another KiCad project as a sheet and replicates its layout | 2026-03-29 | MIT |
| HoleFinder | Groups holes by drill size or net and finds them on the board; KiCad 10 | 2026-09-14 | GPL-3.0 |
| ViaFence | Via fences along selected tracks | 2026-09-14 | GPL-3.0 |
| PCBWay Fabrication Toolkit | Vendor plugin: exports Gerber, netlist, BOM and placement files for PCBWay | 2026-03-31 | MIT |
| PCBWay Plug-in for KiCad | Vendor plugin: uploads a project to PCBWay for a quote | 2026-03-31 | MIT |
| kisi – SI/PI checks | Opens the board in kisi's browser viewer for signal and power integrity checks; testing | 2026-11-22 | GPL-3.0 |
| Place By Sch | Places footprints by their schematic positions | 2026-02-24 | GPL-3.0 |
| Snap To Grid | Snaps selected footprints to the grid | 2026-10-11 | GPL-3.0 |
| TraceForge | Signal-path timing, via tools and PCBWay or PCBPower packages; Windows and KiCad 10 only; 1 star | 2026-11-20 | MIT |
| Silk Reference Tools | Centres, hides or resizes reference designators in bulk over the IPC API | 2026-10-14 | MIT |
| SparkFun KiCad Libraries | SparkFun's parts library with 3D models | 2026-11-11 | CC-BY-4.0 |
| SparkFun KiCad CAMmer | Gerber and drill export, zipped | 2026-06-17 | MIT |
| SparkFun KiCad Panelizer | Simple panels with V-scores | 2026-09-29 | MIT |
| Xyce Simulation Plugin for KiCad | Runs Sandia's Xyce simulator from the schematic editor; KiCad 10 | 2026-11-17 | Apache-2.0 |
| PNG Export | PNG export of a board area; testing | 2026-11-18 | GPL-3.0 |
| traces | LLM part sourcing and netlist checks (local Ollama or OpenRouter) through a local server; macOS, KiCad 10, testing | 2026-09-08 | MIT |
| ViaStitcher | Fills a zone with stitching vias | 2026-10-14 | MIT |
| T-Junction Teardrops | Fillets at T-junctions between tracks | 2026-10-27 | MIT |
| Eagle Exhumer | Imports Eagle designs into KiCad 10 and repairs what the import breaks; testing | 2026-10-29 | GPL-3.0 |
| Z2Labs EMS | openEMS field simulation of a board from the PCB editor; testing | 2026-11-14 | GPL-3.0 |
| Z2 Via Colino | Adaptive via stitching with DRC checks | 2026-10-29 | MIT |
| Board2Pdf | Custom PDF prints of a board | 2026-11-25 | GPL-3.0 |
| Z0 Field Solver | 2D field solver for track width and gap from a target impedance; KiCad 10 | 2026-10-23 | GPL-3.0 |
| Z0 Wavelab | Simplified TDR, yield and plane-slot simulations of routed boards; KiCad 10 | 2026-10-23 | GPL-3.0 |
| eC-registration panel & stencil | Panel frame with Eurocircuits registration holes and a matching stencil outline | 2026-07-30 | MIT |
| Vulcan's Trials | GPU auto-placer and autorouter (Vulkan) | 2026-11-10 | GPL-3.0 |
| Stenchill | 3D-printable solder-paste stencils; the files are processed on stenchill.com | 2026-08-31 | MIT |
| KiCoil | Planar spiral and toroid inductors as footprints | 2025-12-22 | Apache-2.0 |
| KiVar | Assembly variants from rules in component fields | 2026-10-12 | MIT |
| KiCad FabLib | Library matching the Fab Lab inventory | 2026-08-10 | CC-BY-4.0 |
| LW Antenna Check | PCB antenna VSWR, efficiency and gain; needs the closed LW RF Studio | — | GPL-3.0 |
| Sierra Quote Plugin | Vendor plugin: reads the board and requests a Sierra Circuits quote | — | GPL-3.0 |
| Component Position Exporter | Component position CSV with DNP support | 2026-08-29 | MIT |
| Fanout Tool | Escape routing (fanout) for QFN, QFP and BGA packages | 2026-09-10 | MIT |
| Colour themes (18 packages) | Editor colour themes: Witch Hazel, Vampire, Monokai High Contrast, Gruvbox, Gruvbox Light, Skyline, seven from pointhi's kicad-color-schemes (Eagle Dark has no version left), Nuova Elettronica, Hartia, KiCadMaxColors, Arcana, dragonmux | — | CC0-1.0 (11), MIT (5), Apache-2.0, CC-BY-NC-SA-4.0 |

## Deferred

| Entry | What it is | Phase |
|---|---|---|

## Rejected

| Entry | Why | Date |
|---|---|---|
| KiSidian | Off-topic: Markdown notes inside KiCad | 2026-11-26 |
| Dial Scale FrontPanel Footprint Wizard | Off-topic: dial scales for instrument front panels | 2026-11-26 |
| TextPostionSize | Small (2 stars) and inactive since 2025-04 | 2026-11-26 |
| Thermal Relief Via | Small (1 star) and inactive since 2024; testing | 2026-11-26 |
| KiCAD Coil Generator | Small (11 stars) and inactive since 2024; PCB Coil Creator and KiCoil cover it | 2026-11-26 |
| Schematic Blocks Plug-In | Small (31 stars) and inactive since 2023; testing release 0.1 | 2026-11-26 |
| Simple Libraries | Small (25 stars) and inactive since 2023; development release | 2026-11-26 |
| Git plugin | Small (44 stars) and inactive since 2024 | 2026-11-26 |
| Keyboard footprints placer | Off-topic: mechanical keyboard layout | 2026-11-26 |
| CB KiCAD Libraries | No version left: removed from the index in 2023 | 2026-11-26 |
| HierarchicalPCB | Archived upstream | 2026-11-26 |
| KLEPlacement | Archived upstream; keyboard-specific | 2026-11-26 |
| Hide References | Small (13 stars) and inactive since 2024 | 2026-11-26 |
| openinput library | Small and inactive since 2022; testing; input-device parts only | 2026-11-26 |
| KiCad用PCBGOGOプラグイ | No version left: the vendor plugin was removed in 2024 | 2026-11-26 |
| PCBGOGO Plug-in for KiCad | No version left: the vendor plugin was removed in 2024 | 2026-11-26 |
| Keyswitch Kicad Library | Off-topic (keyboard switches); inactive since 2023 | 2026-11-26 |
| Set Hole Diameter | Small (4 stars) and inactive since 2024 | 2026-11-26 |
| Cut tracks at line | Small (3 stars) and inactive since 2024 | 2026-11-26 |
| Nuova Elettronica Symbols Library | Magazine-style symbol set; small (8 stars) and inactive since 2025-04 | 2026-11-26 |
| Bulk hide silkscreen designators | Small (9 stars) and inactive since 2023 | 2026-11-26 |
| Elektuur Style Symbol Library (franzee) | Duplicate: the old identifier of the mgyger library below; its repo redirects there | 2026-11-26 |
| Generic Symbol Library (franzee) | Niche symbol set; inactive since 2023 | 2026-11-26 |
| Elektuur Style Symbol Library (mgyger) | Magazine-style symbol set; inactive since 2023 | 2026-11-26 |
| Oktizer Action Plugin | For KiCad 5.1 to 7 only | 2026-11-26 |
| NextPCB JP Kicad用プラグイン | No version left: removed as outdated in 2023; Huaqiu's NextPCB package is current | 2026-11-26 |
| NextPCB Plug-in for KiCad | No version left: removed as outdated in 2023; Huaqiu's NextPCB package is current | 2026-11-26 |
| KiNotes | Off-topic: engineering notes inside KiCad | 2026-11-26 |
| KiMesh (footprints) | Off-topic (tamper-detection meshes); inactive since 2023 | 2026-11-26 |
| KiMesh (plugin) | Off-topic (tamper-detection meshes); inactive since 2023 | 2026-11-26 |
| Transform It | Small (25 stars) and inactive since 2024 | 2026-11-26 |
| [Delisted] Length Matching | Delisted: no version and no homepage left | 2026-11-26 |

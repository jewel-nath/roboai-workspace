---
type: source
name: FreeCAD Addon Index
registry: freecad-addons-index
url: https://github.com/FreeCAD/Addons
commit: "467ab72"
read_on: 2026-11-26
counts: {entries: 182, pages: 0, waiting: 5, index_only: 88, deferred: 0, rejected: 89}
---

# FreeCAD Addon Index: what it gives RoboAI

The official index that the Addon Manager in FreeCAD 1.0 and later reads: one data file,
`Data/Index.json`, with 182 addons (workbenches, macros, preference packs and libraries). Each entry
names its repository and branch, and may carry FreeCAD version limits and a "curated" flag. It
replaced FreeCAD/FreeCAD-addons, which now serves only FreeCAD before 1.0. For Phase 5 it gives the
CAD batch three mechanical cards (Fasteners, Gears, SheetMetal), the PCB batch KiCad StepUp, and the
CAD-to-sim batch Assembly2MuJoCo, the only exporter in the index that turns a FreeCAD assembly into
a simulation model. About a third of the index is UI themes, layout tweaks or other engineering
domains (architecture, roads, ships, rockets, guitars, furniture).

## How it was read

- Read at commit `467ab72` (2026-11-19, "Add ClaudeCodeWB") on 2026-11-26: the README,
  `Data/Index.json` in full (182 addon keys, 197 branch entries), both licence files (data CC0-1.0,
  code LGPL-2.1) and the issue templates. `Data/Python/` holds the Python packages addons may
  depend on, per Python version; it has no addon entries.
- The index has no descriptions. Every addon's repository was shallow-cloned on 2026-11-26 at the
  branch its first index entry installs. "Last commit" is that branch's last commit. "Licence" is
  the `<license>` tag in the addon's `package.xml`, or the root licence file where there is none.
  KiCad StepUp, Defeaturing, pcb and Manipulator declare their licence only in `package.xml`. Stars
  and archived flags come from the github.com pages of the 176 GitHub-hosted addons; the five on
  Codeberg and one on salsa.debian.org were cloned only. 36 entries carry `"curated": false`
  (marked "not curated" in the tables); 13 offer more than one branch.
- **The move.** FreeCAD/FreeCAD-addons (1,135 stars) now calls itself the legacy index, kept so old
  FreeCAD versions can still install addons. New Addon Managers read this repository. The old
  index was used only to confirm this.
- **Rules used.** A page for what robot builders use in almost every design. Index only for
  mechanical design and making: assembly, frames and profiles, threads and gears, laser, CNC and
  3D-print helpers, CAM and FEM add-ons, exchange formats, parts libraries, BOMs and drawings, mesh
  repair, version history and agent connectors. Rejected: UI themes and layout, other engineering
  domains, clients for outside services, addons with no commit since 2023, and addons made for
  FreeCAD before 1.0 only.
- **CAD to robot model.** The index has no CROSS or RobotCAD workbench. Both live outside it, at
  galou/freecad.cross and drfenixion/freecad.robotcad (both answered `git ls-remote` on
  2026-11-26), and install as custom repositories; the cad-to-sim batch reads them upstream.
  Assembly2MuJoCo v0.4.0 (2026-05-05, 37 stars) exports FreeCAD's built-in Assembly to MJCF with
  OBJ meshes. It converts fixed, revolute, cylindrical, slider and ball joints and handles
  kinematic loops. It has no URDF output.
- **MCP and agents.** The workspace's registered `freecad-mcp` (neka-nat) is not in the index; its
  FreeCAD addon is installed by hand. freecad-mcp-bridge (CREATeNG, MIT, 36 stars, not curated)
  runs an MCP server inside FreeCAD over HTTP with a bearer token and lets an agent run Python in
  the live session. ClaudeCodeWB (3 stars, added by the head commit) drives FreeCAD through the
  Claude Code CLI. Both are index rows; the CAD batch compares the bridge with `freecad-mcp` before
  it writes `mcp/freecad.md`.
- **Batches.** KiCad StepUp is a FreeCAD workbench but a KiCad helper; it waits in the PCB batch
  with the slug the awesome-kicad note uses. The FreeCAD page itself comes from other notes
  (`tools/freecad`, A, cad); built-in CAM, FEM and Assembly belong on it. ExplodedAssembly, Movie,
  AnimationFreeCAD and Render are index rows the video track's V3 (exploded views) may want.
- **State of entries.** Archived on GitHub but still listed: ConstraintDesign, offline-documentation
  and symbols_library. Render calls itself unmaintained. drawing_dimensioning is limited to FreeCAD
  0.19 and btl to 1.0. dxf-library's README says FreeCAD has not needed it since 0.16. pyrate's
  GitHub copy is abandoned; the index already points to salsa.debian.org. fcVM and
  workfeature-macro have no licence. All 182 repositories could be cloned: no dead links.
- Nothing in the fetched files was addressed to agents. The ClaudeCodeWB and freecad-mcp-bridge
  READMEs describe agent tools to their users.

## Pages made

| Entry | Page | Tier |
|---|---|---|

## Waiting for a page

| Entry | Page | Tier | Batch | Why it matters |
|---|---|---|---|---|
| Assembly2MuJoCo | tools/assembly2mujoco | B | cad-to-sim | Exports a FreeCAD 1.x assembly to MJCF with meshes: the FreeCAD route to MuJoCo the plan asks for |
| fasteners | tools/freecad-fasteners | B | cad | Standard screws, nuts, washers and threaded rods as parametric parts, in almost every robot assembly |
| freecad.gears | tools/freecad-gears | B | cad | Involute, cycloid, bevel, worm, planetary and timing-belt gears for drives and reducers |
| kicadStepUpMod | tools/kicad-stepup | B | pcb | Moves boards, footprints and outlines between KiCad and FreeCAD, to fit electronics into a robot |
| sheetmetal | tools/freecad-sheetmetal | B | cad | Bent-sheet brackets and chassis that unfold to flat patterns for laser cutting |

## Index only

| Entry | What it is | Last commit | Licence |
|---|---|---|---|
| A2plus | Assembly workbench extending Assembly 2; FreeCAD 1.x's built-in Assembly covers most uses | 2026-02-15 | LGPL-2.1-or-later |
| addFC | Toolbox: BOM, batch sheet-metal export, exploded views, a parts library | 2026-10-25 | LGPL-2.1-or-later |
| AddonManager | The Addon Manager itself, shipped with FreeCAD and updated here; belongs on the FreeCAD page | 2026-09-26 | LGPL-2.1-or-later |
| Alternate_OpenSCAD | Imports OpenSCAD files as editable FreeCAD geometry; belongs on the OpenSCAD page | 2026-11-08 | LGPL-2.1-or-later |
| AnimationFreeCAD | Animates objects with PyFlow node graphs; a candidate for explainer videos | 2025-03-03 | Apache-2.0 |
| Assembly3 | Assembly workbench on the SolveSpace solver | 2025-11-08 | GPL-3.0-only |
| Assembly4 | Assembly by local coordinate systems, popular before the built-in Assembly (Codeberg) | 2026-10-14 | LGPL-2.1-only |
| Assembly4.1 | Community fork of Assembly4 | 2026-05-30 | LGPL-2.1-only |
| AssemblyCut | Cuts several PartDesign bodies with one sketch; FreeCAD 1.1+, not curated | 2026-08-11 | LGPL-2.1-or-later |
| BillOfMaterials | BOMs that work with any assembly workbench | 2026-11-13 | LGPL-3.0-or-later |
| BrickFace | Turns a face into LEGO-compatible studs or sockets; not curated | 2026-08-31 | MIT |
| btl | Tool library manager for CAM; limited to FreeCAD 1.0 and earlier | 2025-08-28 | MIT |
| Cables | Electrical cable drawing, aimed at buildings but usable inside devices | 2026-10-27 | LGPL-3.0-or-later |
| cadquery_module | Runs CadQuery scripts inside FreeCAD; belongs on the CadQuery page | 2026-07-02 | Apache-2.0 |
| CamScripts | Scripts that configure each step of FreeCAD's CAM process | 2026-04-29 | LGPL-2.1-or-later |
| CarteGrid | Batch-exports variants of a parametric model from a parameter grid; not curated | 2026-10-04 | MIT |
| CfdOF | CFD with OpenFOAM inside FreeCAD; rarely needed for robots | 2026-11-09 | LGPL-3.0-or-later |
| Channels | Live link from FreeCAD to Blender; development release | 2026-04-01 | LGPL-3.0-or-later |
| ClaudeCodeWB | Unofficial chat panel that lets Claude Code drive FreeCAD 1.1+; 3 stars, not curated | 2026-11-09 | MIT |
| CurvedShapes | Builds 3D shapes from 2D curves | 2026-05-23 | LGPL-2.1 |
| Curves | NURBS curve and surface tools, for shells and covers | 2026-11-21 | LGPL-2.1-or-later |
| Defeaturing | Simplifies STEP models: removes holes and faces, fixes tolerances | 2026-06-18 | AGPL-3.0 |
| Design456 | Direct-modelling workbench, marked work in progress by its author | 2026-10-02 | GPL-3.0-or-later |
| Design-Proof | Tests a parametric model by varying its dimensions; not curated | 2026-04-22 | LGPL-2.1-or-later |
| Detessellate | Tools to turn meshes back into solids; not curated | 2026-09-12 | LGPL-2.1-or-later |
| DFM | Checks a design against manufacturing-process rules; not curated | 2026-11-14 | LGPL-2.1-or-later |
| DynamicData | Property containers for driving parameters, instead of a spreadsheet | 2026-04-16 | LGPL-2.1-or-later |
| EasyProfileFrame | Frames from aluminium extrusion profiles, with a BOM | 2025-04-11 | LGPL-3.0-or-later |
| Estimate | Estimates material volume and weight of selected parts | 2026-05-02 | LGPL-3.0-or-later |
| ExplodedAssembly | Exploded-view animations of assemblies; for the video track's V3 | 2024-02-24 | LGPL-2.1 |
| Motion-Control | Drives an Assembly4 model from a PLC over OPC UA; not curated | 2026-04-18 | GPL-3.0-or-later |
| FoamCut | G-code for 4- and 5-axis hot-wire foam cutters | 2026-11-13 | LGPL-2.1-or-later |
| FreeCAD-Beginner-Assistant | Checks Part and Sketcher models against good practice | 2024-12-29 | LGPL-2.1-or-later |
| FreeCAD-Documentation-html | Offline copy of the FreeCAD wiki | 2026-11-25 | GPL-2.0-or-later |
| freecad-mcp-bridge | MCP server inside FreeCAD that lets an agent run Python in the live session; not curated, compare with `freecad-mcp` | 2026-11-15 | MIT |
| FeedsAndSpeeds | Basic feeds and speeds for CAM | 2025-12-22 | LGPL-2.1-or-later |
| FEM_FrontISTR | Adds the FrontISTR nonlinear FEM solver | 2026-10-13 | LGPL-2.1-or-later |
| FEMbyGEN | Generative design studies with FEM results | 2026-11-05 | LGPL-2.1-only |
| frame | Beams and frames | 2026-08-01 | LGPL-2.1-or-later |
| FrameForge | Frames and beams with mitre and trim cuts | 2026-11-11 | LGPL-3.0-only |
| free2ki | Exports VRML at the right scale for KiCad 3D models and Blender | 2025-12-27 | GPL-3.0-or-later |
| FreekiCAD | Two-way KiCad board sync over KiCad's IPC API; young, not curated | 2026-10-10 | MIT |
| FusedFilamentDesign | PartDesign helpers for FDM 3D printing | 2026-09-01 | LGPL-2.1-or-later |
| GearWorkBench | Gears for 3D printing (spur, helical, rack, bevel, cycloidal); not curated, freecad.gears covers more | 2026-10-01 | LGPL-2.1-or-later |
| HexFill | Fills a sketch with a honeycomb to lighten panels; not curated | 2026-08-19 | MIT |
| HistoryWorkbench | Version history and 3D comparison of documents; FreeCAD 1.1+, not curated | 2026-10-10 | LGPL-2.1-or-later |
| IDF | Imports IDF board files, an older ECAD-to-MCAD format | 2026-03-08 | LGPL-2.1-or-later |
| ImportNURBS | Imports Rhino 3dm files | 2026-04-20 | LGPL-2.1 |
| InstrumentInput | Bluetooth calipers and other instruments as input devices (Codeberg) | 2026-06-13 | Apache-2.0 |
| InventorLoader | Imports Inventor, ACIS and Fusion 360 (.f3d) files | 2024-12-17 | LGPL-3.0-or-later |
| KiConnect | Live PCB sync with KiCad 9+ over its IPC API (Codeberg); the StepUp page can name it | 2026-08-09 | LGPL-2.1-or-later |
| lattice2 | Arrays and local coordinate systems | 2026-07-15 | LGPL-2.0-or-later |
| LCInterlocking | Interlocking tabs for laser-cut and CNC-milled plate parts | 2025-11-29 | LGPL-2.1-or-later |
| parts_library | FreeCAD's community parts library in FCStd, STEP and STL (2,093 stars) | 2026-11-21 | CC-BY-3.0 |
| LiveSectionAnalyzer | Live section views of large assemblies; not curated | 2026-10-30 | MIT |
| Machines | Community CNC machine definitions for FreeCAD's CAM post-processing | 2026-11-10 | CC-BY-SA-4.0 |
| MakerWorkbench | Parametric mechatronic and optical components | 2024-12-10 | LGPL-3.0 |
| Manipulator | Move, align and measure helpers (not robot manipulators) | 2026-03-25 | GPL-3.0 |
| MBDWorkbench | Model-based definition: semantic PMI and AP242 STEP export; not curated | 2026-08-08 | LGPL-2.1-only |
| MeshRemodel | Rebuilds and repairs mesh objects | 2026-09-05 | LGPL-2.1-or-later |
| MeshStudy | Mesh refinement studies for FEM; not curated | 2026-09-20 | LGPL-2.1-or-later |
| MeshToFeatures | Rebuilds STL meshes of prismatic parts as editable PartDesign bodies; not curated | 2026-11-08 | LGPL-2.1-or-later |
| Movie | Animated cameras and videos of animations; for the video track | 2026-11-01 | LGPL-2.1-or-later |
| Nesting | Nests 2D parts on sheets for laser and CNC cutting; not curated | 2026-09-25 | LGPL-2.1-or-later |
| Nodes | Visual scripting | 2024-10-04 | LGPL-2.1-or-later |
| osh-autodoc-workbench | Assembly manuals and BOMs for open-source hardware (Codeberg) | 2026-02-05 | LGPL-3.0-or-later |
| PartDesignUpgrade | PartDesign helpers: pipes along paths, ribs, multi-body cuts; not curated | 2026-10-28 | LGPL-2.1-or-later |
| pcb | Older PCB workbench from the FreeCAD 0.18 era; KiCad StepUp covers the need | 2026-03-07 | AGPL-3.0 |
| Quetzal | Frames and pipelines; dodo's successor | 2026-10-31 | LGPL-3.0-or-later |
| QuickMeasure | Quick measurements of selected features | 2025-08-06 | GPL-3.0 |
| Ratchet | Parametric ratchets | 2026-04-06 | LGPL-3.0-or-later |
| Render | Photorealistic rendering with outside engines; calls itself unmaintained | 2026-05-16 | LGPL-2.1-or-later |
| ShapeStrings | Text shapes for labels and engraving | 2026-08-09 | LGPL-2.1-or-later |
| Silk | NURBS surface modelling | 2026-08-16 | GPL-3.0-or-later |
| StandardBeams | Standard structural beam profiles | 2026-01-23 | LGPL-2.1-or-later |
| STEMFIE | Parts of the STEMFIE 3D-printable construction set | 2025-01-15 | GPL-2.0-or-later |
| stepParts | Searches the step.parts catalogue of open STEP parts and inserts them; not curated | 2026-08-11 | LGPL-2.1-or-later |
| Supplemental-Materials | Extra material cards for FreeCAD's materials system | 2026-08-24 | LGPL-3.0-or-later |
| SvgWorkbench | Imports and edits SVG geometry; early development | 2026-08-13 | LGPL-3.0-or-later |
| Templater | Templates, symbols and views for TechDraw drawings (Codeberg) | 2026-06-19 | LGPL-3.0-or-later |
| ThreadProfile | Internal and external thread profiles | 2026-09-14 | LGPL-2.1 |
| ThreadWorkbench | Metric and inch threads; not curated | 2026-07-05 | GPL-3.0-or-later |
| TitleBlock | Fills TechDraw title blocks from a spreadsheet | 2025-08-28 | LGPL-2.1-or-later |
| toSketch | Helps rebuild editable models from STEP files | 2026-01-04 | GPL-2.0-or-later |
| Vars | Named variables as document objects, instead of raw VarSets | 2026-06-24 | LGPL-3.0-or-later |
| WebTools | Keeps documents in Git, plus BIM-server tools | 2025-09-08 | LGPL-2.1-or-later |
| workfeature | Reference geometry: points, axes and planes | 2025-01-01 | GPL-3.0 |
| yaml-workbench | Builds and edits objects from YAML files | 2025-09-13 | LGPL-2.1-or-later |

## Deferred

| Entry | What it is | Phase |
|---|---|---|

## Rejected

| Entry | Why | Date |
|---|---|---|
| 3D_Printing_Tools | Inactive since 2019; the Mesh workbench covers it | 2026-11-26 |
| AIGenFurniture | Off topic: furniture cabinets | 2026-11-26 |
| AirPlaneDesign | Off topic: aircraft design | 2026-11-26 |
| ArchTextures | Off topic: architecture textures; inactive since 2022 | 2026-11-26 |
| BananaForScale | Novelty: adds a banana model for scale | 2026-11-26 |
| Behave-Dark-Colors | UI theme | 2026-11-26 |
| Beltrami | Off topic: turbomachine blades | 2026-11-26 |
| BulletDesigner | Off topic: ammunition design | 2026-11-26 |
| boltsfc | Inactive since 2022; Fasteners covers standard hardware | 2026-11-26 |
| CadbaseLibrary | Client for the CADBase component-sharing platform | 2026-11-26 |
| CADExchanger | Needs the paid CAD Exchanger app; last commit 2024-09-17 | 2026-11-26 |
| Catppuccin | UI theme | 2026-11-26 |
| Cfd | Inactive since 2021; CfdOF continues the work | 2026-11-26 |
| CommandPanel | UI layout; inactive since 2019 | 2026-11-26 |
| ConstraintDesign | Archived by its author in favour of FreeCAD's own topological-naming work | 2026-11-26 |
| Color-Palette-Theme | UI theme | 2026-11-26 |
| Corridor-Road | Off topic: road design | 2026-11-26 |
| CubeMenu | UI layout; inactive since 2020 | 2026-11-26 |
| Cubinets | Off topic: cabinets and cut lists | 2026-11-26 |
| DesignSPHysics | Off topic: SPH fluid simulation | 2026-11-26 |
| dodo | Superseded by Quetzal, its own successor; last commit 2024-05-25 | 2026-11-26 |
| Dracula | UI theme | 2026-11-26 |
| drawing_dimensioning | Made for FreeCAD 0.19 and earlier; TechDraw replaced it | 2026-11-26 |
| dxf-library | Not needed since FreeCAD 0.16's built-in DXF importer, by its own README | 2026-11-26 |
| EMStudio | Off topic: RF and electromagnetic simulation | 2026-11-26 |
| fcVM | No licence in its files or metadata | 2026-11-26 |
| FileExplorerExt | UI: file browser panel | 2026-11-26 |
| FreecadDiscordPresence | Off topic: Discord status | 2026-11-26 |
| Freecad-Built-in-themes-beta | UI theme | 2026-11-26 |
| freecad.optics_design_workbench | Off topic: optics ray tracing | 2026-11-26 |
| FreeCAD-Ribbon | UI layout | 2026-11-26 |
| FreeCAD-themes | UI theme | 2026-11-26 |
| freecad-xr-workbench | Off topic: viewing models in VR | 2026-11-26 |
| freecad_streamdeck_addon | UI: Stream Deck input | 2026-11-26 |
| FreeGrid | Off topic: workshop storage system | 2026-11-26 |
| GDML | Off topic: particle-physics geometry for Geant4 | 2026-11-26 |
| Gridfinity | Off topic: workshop storage bins | 2026-11-26 |
| IconThemes | UI theme; inactive since 2020 | 2026-11-26 |
| Lapidary | Off topic: gemstone faceting | 2026-11-26 |
| Launcher | UI: command search | 2026-11-26 |
| Lithophane | Off topic: lithophane art; inactive since 2021 | 2026-11-26 |
| Marz | Off topic: guitar design | 2026-11-26 |
| MnesarcoUtils | Personal utility pack (camera views, input devices) | 2026-11-26 |
| MyCustomPiping | Off topic: process piping | 2026-11-26 |
| NeoRibbon | UI layout | 2026-11-26 |
| NikraDAP | Inactive since 2023; planar multibody dynamics, alpha | 2026-11-26 |
| NordicFC | UI theme | 2026-11-26 |
| nurbs | Inactive since 2019 | 2026-11-26 |
| Nxt | UI layout | 2026-11-26 |
| offline-documentation | Archived; FreeCAD-Documentation-html is the maintained offline wiki | 2026-11-26 |
| Ondsel-Lens | Client for Ondsel Lens team servers, not a builder need | 2026-11-26 |
| OpenTheme | UI theme | 2026-11-26 |
| OpticsWorkbench | Off topic: optics ray tracing | 2026-11-26 |
| OSAFE | Off topic: building foundations | 2026-11-26 |
| ose-piping | Off topic: piping; inactive since 2022 | 2026-11-26 |
| Part-o-magic | Experiment made for FreeCAD 0.17 to 0.20 | 2026-11-26 |
| PieMenu | UI layout | 2026-11-26 |
| pivy_trackers | Developer library; inactive since 2019 | 2026-11-26 |
| Plot | Plot-editing tools, not a robot-building need | 2026-11-26 |
| ProDarkThemePreferencePack | UI theme | 2026-11-26 |
| Pyramids-and-Polyhedrons | Off topic: polyhedra | 2026-11-26 |
| pyOpToolsWorkbench | Off topic: optics ray tracing | 2026-11-26 |
| pyrate | Off topic: optical design | 2026-11-26 |
| Reinforcement | Off topic: concrete rebar | 2026-11-26 |
| Road | Off topic: roads and geomatics | 2026-11-26 |
| Rocket | Off topic: model rockets | 2026-11-26 |
| RotaryMoulder | Off topic: cookie moulds | 2026-11-26 |
| SaveAndRestore | UI: settings backup | 2026-11-26 |
| SearchBar | UI: search bar | 2026-11-26 |
| SelectorToolbar | UI layout; inactive since 2019 | 2026-11-26 |
| Ship | Off topic: naval architecture | 2026-11-26 |
| SimplyPrint | Client for the SimplyPrint cloud printing service | 2026-11-26 |
| slic3r-tools | Inactive since 2020 | 2026-11-26 |
| Smooth-Toolsync | Client for a Loobric tool-data server | 2026-11-26 |
| SlopedPlanesMacro | Off topic: roofs; inactive since 2020 | 2026-11-26 |
| Solar | Off topic: solar analysis of buildings | 2026-11-26 |
| SteelColumn | Off topic: building columns | 2026-11-26 |
| symbols_library | Archived; TechDraw's built-in symbols replaced it | 2026-11-26 |
| TabBar | UI layout; inactive since 2019 | 2026-11-26 |
| Telemetry | Sends usage metrics to FreeCAD's developers | 2026-11-26 |
| TexturedObjImporter | Imports textured OBJ meshes for looks, not parts | 2026-11-26 |
| taack-plm-freecad | Client for the Taack PLM intranet server | 2026-11-26 |
| ToolbarStyle | UI layout; inactive since 2019 | 2026-11-26 |
| ToolSeek | UI: command palette | 2026-11-26 |
| freecad-wakatime | Off topic: time tracking | 2026-11-26 |
| WB_Organizer | UI layout | 2026-11-26 |
| Woods | Off topic: wood materials | 2026-11-26 |
| woodworking | Off topic: furniture and carpentry | 2026-11-26 |
| workfeature-macro | No licence; the workfeature workbench replaces it | 2026-11-26 |

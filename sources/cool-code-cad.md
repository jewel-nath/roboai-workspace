---
type: source
name: Cool Code CAD
registry: cool-code-cad
url: https://github.com/kylegrover/cool-code-cad
commit: "d065e6f"
read_on: 2026-11-26
counts: {entries: 205, pages: 0, waiting: 4, index_only: 86, deferred: 0, rejected: 115}
---

# Cool Code CAD: what it gives RoboAI

A one-person field guide to code-first CAD and programmatic manufacturing, with 205 entries: code
CAD (B-rep, CSG and mesh, SDF, node-based, Blender, Rust kernels), G-code generation, CAM and
slicers, CNC and printer firmware, geometry and mesh libraries, G-code viewers, print simulation,
browser CAD, plotters, and a short section on agent CAD loops. For Phase 5 it confirms the CAD
batch's code-CAD half: FreeCAD and the three documented tools (OpenSCAD, CadQuery, build123d) wait
for pages, and their editors, viewers, libraries and kernels become index rows those pages and the
"Choose a CAD tool" guide can name. More than half the list is rejected: mostly G-code viewers,
print simulation, plotter art and creative coding, which are off topic here, plus duplicates and
inactive projects.

## How it was read

- Read at commit `d065e6f` (2026-09-06, "Add GitHub suggestion flow and catalog README") on
  2026-11-26: the README in full, `data.js` (the catalogue the README is generated from) parsed in
  full, `llm.txt` (a plain-text edition for language models), `PROJECTS.md` and `package.json`.
  `data.js` holds 10 sections, 41 subsections and 205 items; the README and `llm.txt` both say 205,
  where the plan estimated about 260. The first section, "How the CAD Stack Fits Together", is an
  explainer with no entries. `PROJECTS.md` is the maintainer's notes on his own projects and says
  it is not the catalogue, so it was not triaged.
- The list's star counts date from 2026-03-26 and 27 and lag behind (FreeCAD: 29,360 in the list,
  35,784 on github.com on 2026-11-26). Its licence field says only "Open Source" for most entries.
- Dates and licences: all 109 GitHub repositories the entries link were shallow-cloned on
  2026-11-26 for the last commit and the root licence file; stars and archived flags for the page
  candidates and the oldest repos come from their github.com pages. Other entries use the list's
  licence when it names one (MIT, proprietary), else `—`. PyPI's release data dated pygcode. Every
  non-GitHub link was fetched on 2026-11-26.
- Archived on GitHub: Curv, Fornjot and CADmium (CADmium is also under the Elastic License 2.0,
  which is not open source).
- Dead or moved on 2026-11-26: plasm.net is a parked domain for sale; the SDFeditor page returns
  404; BlenderBIM's link goes to bonsaibim.org (it was renamed Bonsai); OCCT's goes to occt3d.com;
  IceSL's goes to icesl.github.io; SmartSlice's goes to Markforged's simulation page. SourceForge,
  npm, Sienci, Hexagon, MDPI, INL (MOOSE) and Markforged refuse scripted requests (403); they were
  counted as live.
- Errors in the list: six entries appear twice (Replicad, JSCAD, OpenCascade.js, py2g, js2g,
  PlotterFiles); the second copy of each is rejected as a duplicate. "FreeCAD Path Workbench" has
  been the CAM Workbench since FreeCAD 1.0. The claim that FreeCAD's FEM workbench includes topology
  optimisation through CalculiX was not confirmed.
- **Rules used.** A page for FreeCAD and the three documented code-CAD tools. Index only for other
  code CAD, kernels, geometry and mesh libraries, file formats, CAM, slicers, CNC firmware and
  senders, the solvers FreeCAD uses, and agent CAD tools. Rejected: G-code viewers and editors,
  printer monitoring, metal additive-manufacturing research, industrial CNC verification, plotter
  art, creative coding, architecture and GIS tools, closed or non-commercial licences, and inactive
  projects. Slicers, CNC firmware and senders stay index rows: no Phase 5 batch covers making
  parts, and the Phase 6 playbooks can link them.
- **Shared with the FreeCAD Addon Index note.** That index lists addons, not FreeCAD itself; its
  cadquery_module and Alternate_OpenSCAD rows point at this note's CadQuery and OpenSCAD pages.
  CAD Exchanger is rejected in both notes (a paid product). FreeCAD's CAM and FEM workbenches are
  built in, so their rows here name the FreeCAD page.
- **Agents and CAD-to-sim.** build123d-mcp (163 stars, Apache-2.0) gives an agent a live build123d
  session with renders and measurements; it stays an index row because this workspace's MCP choice
  is FreeCAD's, but the build123d page can name it. MeshLab and Trimesh are index rows the
  cad-to-sim guide may cite for simplifying meshes.
- The list's author includes his own projects (fullcontrol-js, py2g, js2g, VolcoGUI); they are
  rejected as young or off topic, the same test as every other entry.
- Nothing in the fetched files was addressed to agents. The "Agent-Ready CAD Loops" section and
  `llm.txt` are written for readers.

## Pages made

| Entry | Page | Tier |
|---|---|---|

## Waiting for a page

| Entry | Page | Tier | Batch | Why it matters |
|---|---|---|---|---|
| CadQuery | tools/cadquery | B | cad | Python B-rep code CAD on OpenCascade; the documented script route beside FreeCAD |
| Build123d | tools/build123d | B | cad | Newer Pythonic API on the same OpenCASCADE kernel, with an MCP server for agents |
| FreeCAD | tools/freecad | A | cad | This workspace's first-class CAD, scriptable headless with `freecadcmd` |
| OpenSCAD | tools/openscad | B | cad | The classic CSG code CAD; many printed robot parts ship as `.scad` files |

## Index only

| Entry | What it is | Last commit | Licence |
|---|---|---|---|
| CQ-editor | CadQuery's desktop editor with live reload and a 3D viewer | 2026-11-20 | Apache-2.0 |
| OCP CAD Viewer | VS Code and standalone viewer for CadQuery and build123d models | 2026-11-21 | Apache-2.0 |
| pythonOCC | Python bindings to most of OpenCASCADE; lower level than CadQuery | 2026-11-17 | LGPL-3.0 |
| Dune3D | GUI parametric CAD on OpenCASCADE with a SolveSpace-style solver, aimed at enclosures | 2026-11-18 | GPL-3.0 |
| SolveSpace | Small parametric 2D and 3D CAD with a strong constraint solver | 2026-11-23 | GPL-3.0 |
| BRL-CAD | Long-running CSG modeller and ray tracer, scriptable from Tcl | 2026-11-24 | LGPL |
| Replicad | TypeScript B-rep modelling on opencascade.js with a browser studio | 2026-11-06 | MIT |
| PythonSCAD | OpenSCAD fork that adds Python scripting | — | — |
| SolidPython2 | Python front end that writes OpenSCAD files | 2026-01-04 | LGPL-2.1 |
| BOSL2 | OpenSCAD standard library: threads, gears, rounding, joints | 2026-11-17 | BSD-2-Clause |
| NopSCADlib | OpenSCAD library of screws, bearings, steppers and printed parts, with BOMs | 2026-09-24 | GPL-3.0 |
| JSCAD (OpenJSCAD) | JavaScript parametric CAD in the browser and on the command line | 2026-11-07 | MIT |
| Manifold | Fast mesh booleans with guaranteed manifold output; OpenSCAD's new back end | 2026-11-25 | Apache-2.0 |
| MicroCAD | Young language for parametric parts, compiled to STL and SVG (Codeberg) | — | — |
| ShapeScript | Scripted 3D modelling app for macOS and iOS | 2026-11-24 | MIT |
| Fidget | Fast implicit-surface evaluation in Rust, by libfive's author | 2026-11-17 | MPL-2.0 |
| libfive | Implicit (f-rep) modelling kernel with the Studio live-coding editor | 2026-10-16 | MPL-2.0 (library) |
| ImplicitCAD | Implicit CAD in Haskell with OpenSCAD-like syntax | 2026-03-20 | AGPL-3.0 |
| sdf (fogleman) | Small Python library that meshes SDF shapes | 2024-08-10 | MIT |
| sdfx | SDF CAD kernel in Go | 2026-11-23 | MIT |
| Inigo Quilez | Reference articles on SDF primitives and ray marching | — | — |
| bitbybit | Browser node editor and TypeScript API over JSCAD, OpenCASCADE and Manifold | — | — |
| Blender Python API | Blender's `bpy` scripting; phobos builds robot models on it | — | — |
| CAD Sketcher | Constraint-based sketching inside Blender | 2026-11-23 | GPL-3.0 |
| Truck | Rust NURBS B-rep kernel with STEP I/O | 2026-11-23 | Apache-2.0 |
| Monstertruck | Experimental Truck fork adding fillets and other CAD pieces | 2026-11-23 | Apache-2.0 |
| vcad | Young Rust and WASM B-rep CAD stack | 2026-11-22 | Apache-2.0 |
| brepkit / brepjs | New Rust and WASM B-rep engine with a TypeScript API | 2026-11-25 | AGPL-3.0 |
| FullControl | Python library that designs 3D-printer toolpaths directly | 2026-10-09 | GPL-3.0 |
| gcodepreview | PythonSCAD-based G-code preview and toolpath generator | 2026-10-12 | LGPL-2.1 |
| PrusaSlicer | Widely used open slicer with a command-line interface | 2026-11-24 | AGPL-3.0 |
| OrcaSlicer | Community slicer forked from Bambu Studio | 2026-11-25 | AGPL-3.0 |
| CuraEngine | Cura's slicing engine, usable from the command line | 2026-11-18 | AGPL-3.0 |
| SuperSlicer | PrusaSlicer fork with calibration tools | 2026-11-21 | AGPL-3.0 |
| IceSL | Lua-scripted modeller and slicer from Inria; site moved to icesl.github.io | — | — |
| Kiri:Moto | Browser slicer and CAM for 3D printing, CNC milling and lasers | 2026-07-26 | MIT |
| FreeCAD Path Workbench | FreeCAD's built-in CAM, renamed CAM Workbench in 1.0; belongs on the FreeCAD page | 2026-11-25 | LGPL-2.1 |
| dxf2gcode | DXF to G-code for milling and drag knives (SourceForge) | — | — |
| OpenCAMLib | C++ toolpath library with Python bindings; FreeCAD's CAM uses it | 2026-10-17 | LGPL-2.1 |
| Blender CAM | Blender add-on that makes CNC toolpaths | 2026-11-24 | GPL-3.0 |
| LightBurn | Commercial laser layout and control software, common for hobby lasers | — | Proprietary |
| LaserGRBL | Open Windows G-code sender for GRBL lasers | — | — |
| FlatCAM | Turns Gerber and Excellon files into isolation-milling G-code for prototype boards | — | MIT |
| pcb2gcode | Command-line Gerber to G-code for milled boards | 2026-11-25 | GPL-3.0 |
| Klipper | 3D-printer firmware split between a host computer and an MCU | 2026-11-24 | GPL-3.0 |
| Marlin | The most common 3D-printer firmware | 2026-11-24 | GPL-3.0 |
| grbl | G-code motion controller for AVR Arduinos, in hobby CNCs and lasers; grblHAL continues it | 2021-01-22 | GPL-3.0 |
| FluidNC | grbl-compatible CNC firmware for ESP32, configured in YAML | 2026-11-24 | GPL-3.0 |
| LinuxCNC | Real-time machine controller on Linux with HAL; also drives some robot arms | 2026-11-25 | GPL-2.0 |
| RepRapFirmware | Printer and CNC firmware for Duet boards | 2026-11-25 | GPL-3.0 |
| grblHAL | 32-bit grbl successor for ARM, ESP32 and RP2040 boards | 2026-11-23 | GPL-3.0 |
| Smoothieware | G-code firmware for LPC17xx boards | 2026-10-22 | GPL-3.0 |
| TinyG | Synthetos's 6-axis motion-control firmware, now kept as a historical line | 2026-11-16 | — |
| OpenCASCADE (OCCT) | The open B-rep kernel under FreeCAD, CadQuery and build123d; site moved to occt3d.com | — | — |
| CGAL | Computational geometry library | 2026-11-25 | GPL-3.0 or LGPL-3.0, per file |
| OpenCascade.js | WASM build of OpenCASCADE behind Replicad, CascadeStudio and Chili3D | — | — |
| Trimesh | Python triangle-mesh library, common in robot-model tooling | 2026-11-21 | MIT |
| numpy-stl | Fast STL reading and writing in Python | 2026-11-17 | BSD-3-Clause |
| Open3D | Has a page: [Open3D](../wiki/software/open3d.md) | 2026-11-13 | MIT |
| libigl | Header-only C++ geometry processing | 2026-11-25 | MPL-2.0 |
| MeshLab (PyMeshLab) | Mesh cleanup and decimation, often used to lighten robot meshes for simulation | 2026-07-24 | GPL-3.0 |
| VTK | Kitware's visualisation toolkit; PCL's viewer is built on it | 2026-11-25 | BSD-3-Clause |
| lib3mf | Official 3MF file SDK | 2026-03-02 | BSD-2-Clause |
| Assimp | Importer for over 40 mesh formats | 2026-11-20 | BSD-3-Clause |
| ezdxf | Python DXF reading and writing, for laser-cut and CNC plates | — | — |
| MeshFix | Repairs triangle meshes into watertight solids | 2026-05-21 | — |
| CAMotics | Open 3-axis CNC simulator that shows material removal | — | — |
| Universal Gcode Sender (UGS) | Java G-code sender for GRBL and FluidNC machines | — | — |
| CNCjs | Web G-code sender that runs on a Raspberry Pi | — | — |
| gSender | Sienci Labs' free CNC sender | — | — |
| Candle | Qt GRBL controller with a G-code viewer | 2026-11-21 | GPL-3.0 |
| bCNC | Python GRBL controller with auto-levelling and DXF import | 2026-11-10 | GPL-2.0 |
| RoboDK | Commercial offline programming and simulation for industrial arms | — | Proprietary |
| CalculiX | Open FEA solver behind FreeCAD's FEM workbench | — | — |
| OpenFOAM | Open CFD platform behind FreeCAD's CfdOF addon | — | — |
| ManifoldCAD | Manifold's browser scripting playground | — | — |
| Chili3D | Browser CAD on OpenCASCADE (WASM) and Three.js | 2026-11-21 | AGPL-3.0 |
| CascadeStudio | Live-scripted browser CAD on opencascade.js | — | — |
| build123d-mcp | MCP server that gives an agent a live build123d session with renders and measurements | 2026-11-19 | Apache-2.0 |
| Zoo.dev (formerly KittyCAD) | KCL-based CAD app with an AI assistant; open client, closed geometry service | 2026-11-25 | MIT (client) |
| TopOpt (DTU) | Teaching codes for topology optimisation in MATLAB and Python | — | — |
| FreeCAD FEM + Topology | FreeCAD's FEM workbench with CalculiX; belongs on the FreeCAD page | 2026-11-25 | LGPL-2.1 |
| NIST RS274/NGC Interpreter Specification | The reference for the G-code dialect LinuxCNC uses | — | — |
| RepRap G-Code Reference | Community wiki of 3D-printer G-codes | — | — |
| curated-code-cad | Older list of code-CAD projects; no commit since 2024-01 | 2024-01-02 | MIT |
| awesome-cadquery | List of CadQuery and build123d resources; the plan left it out as small | 2026-10-26 | CC0-1.0 |

## Deferred

| Entry | What it is | Phase |
|---|---|---|

## Rejected

| Entry | Why | Date |
|---|---|---|
| PLaSM | Dead link: plasm.net is a parked domain for sale | 2026-11-26 |
| oscad (openscad-occt) | Very young experiment with no licence | 2026-11-26 |
| cqparts | Inactive since 2019; built for CadQuery 1 | 2026-11-26 |
| Topologic | Off topic: spatial modelling for architecture | 2026-11-26 |
| Curv | Archived; a maths-art language | 2026-11-26 |
| SDF Modeler | Closed freeware for SDF art, not parts | 2026-11-26 |
| SDFeditor | Dead link: the page returns 404 | 2026-11-26 |
| editSDF | Archived art experiment (its URL sits under /archive/) | 2026-11-26 |
| nTopology | Proprietary enterprise design software | 2026-11-26 |
| Grasshopper (Rhino) | Proprietary; needs Rhino | 2026-11-26 |
| Blender Geometry Nodes | Off topic: procedural modelling for graphics | 2026-11-26 |
| Sverchok | Off topic: generative art and architecture in Blender | 2026-11-26 |
| Antimony | In maintenance mode, by the list's own note; libfive and Fidget replace it | 2026-11-26 |
| BlockMill | Small educational block-programming toy for milling | 2026-11-26 |
| BlenderBIM | Off topic: building information modelling; renamed Bonsai | 2026-11-26 |
| Blender GIS | Off topic: geographic data | 2026-11-26 |
| Fornjot | Archived; its author stopped the project | 2026-11-26 |
| fullcontrol-js | Young port by the list's author (2 stars); FullControl itself is an index row | 2026-11-26 |
| mecode | Inactive since 2019 | 2026-11-26 |
| pygcode | Last release 2017-10-11 | 2026-11-26 |
| PythonicGcodeMachine | Only release, V0, dated 2018-12-22 | 2026-11-26 |
| pygdk | Small (29 stars); FullControl covers it | 2026-11-26 |
| LinuxCNC G-Code Generators | Inactive since 2020 | 2026-11-26 |
| py2g (Programmatic G-Code) | Beta web app by the list's author for printer-path design; not a robot-building tool | 2026-11-26 |
| js2g (Programmatic G-Code) | Beta web app by the list's author for printer-path design; not a robot-building tool | 2026-11-26 |
| Slic3r | Inactive since 2022; PrusaSlicer continues it | 2026-11-26 |
| PyCAM | Inactive since 2021 | 2026-11-26 |
| F-Engrave | Niche engraving tool; last commit 2024-07-11 | 2026-11-26 |
| PyMesh | Inactive since 2020 | 2026-11-26 |
| cadexchanger | Proprietary paid converter; the FreeCAD addon for it is rejected too | 2026-11-26 |
| NC Viewer | G-code viewer only; not a robot-building tool | 2026-11-26 |
| 3DPEA G-Code Simulator | G-code viewer only; not a robot-building tool | 2026-11-26 |
| gCodeViewer | G-code viewer only; not a robot-building tool | 2026-11-26 |
| webgcode | G-code viewer only; not a robot-building tool | 2026-11-26 |
| CutViewer | G-code viewer only; not a robot-building tool | 2026-11-26 |
| PrintPal G-Code Viewer | G-code viewer only; not a robot-building tool | 2026-11-26 |
| Zupfe | G-code viewer and OctoPrint plugin; not a robot-building tool | 2026-11-26 |
| GCodeAnalyser | Print-time estimator; not a robot-building tool | 2026-11-26 |
| gcode-preview | JavaScript G-code viewer component; off topic | 2026-11-26 |
| gcode-viewer (aligator) | JavaScript G-code viewer component; off topic | 2026-11-26 |
| @polar3d/gcode-viewer | JavaScript G-code viewer component under a custom licence; off topic | 2026-11-26 |
| @sindarius/gcodeviewer | JavaScript G-code viewer component; off topic | 2026-11-26 |
| react-gcode-viewer | JavaScript G-code viewer component, inactive since 2022 | 2026-11-26 |
| Three.js GCodeLoader | Three.js example loader; off topic | 2026-11-26 |
| PrusaSlicer G-Code Viewer | Part of PrusaSlicer, an index row | 2026-11-26 |
| Repetier-Host | Closed freeware printer host | 2026-11-26 |
| Mainsail G-Code Viewer | Viewer inside a printer web UI; off topic | 2026-11-26 |
| Fluidd G-Code Viewer | Viewer inside a printer web UI; off topic | 2026-11-26 |
| PrettyGCode | OctoPrint viewer plugin; off topic | 2026-11-26 |
| PrintTimeGenius | OctoPrint print-time plugin; off topic | 2026-11-26 |
| pyGCodeDecode | Research tool for G-code timing; off topic | 2026-11-26 |
| gcode-simulator | Small G-code timing package; off topic | 2026-11-26 |
| gcodeparser | Small G-code parser; off topic | 2026-11-26 |
| gcode-rs | G-code parser crate; off topic | 2026-11-26 |
| gcode-nom | G-code parser crate (7 stars); off topic | 2026-11-26 |
| gcode2obj | G-code to OBJ converter crate; off topic | 2026-11-26 |
| G-code Genius | VS Code extension for G-code; off topic | 2026-11-26 |
| G-Code Syntax | VS Code extension for G-code; off topic | 2026-11-26 |
| CIMCO Edit | Proprietary industrial CNC editor | 2026-11-26 |
| NCPlot | Freeware CNC backplotter; off topic | 2026-11-26 |
| Discriminator | Freeware CNC editor; off topic | 2026-11-26 |
| NCneticNpp | Notepad++ G-code plugin; off topic | 2026-11-26 |
| Stitch3R | Proprietary Blender renderer for print files | 2026-11-26 |
| GCode-Parser-and-Viz | Small Blender scripts, inactive since 2024-03 | 2026-11-26 |
| Vericut | Proprietary industrial CNC verification | 2026-11-26 |
| NCSIMUL | Proprietary industrial CNC verification | 2026-11-26 |
| VOLCO | Off topic: research simulator of printed shapes | 2026-11-26 |
| VolcoGUI | Off topic: GUI by the list's author for VOLCO | 2026-11-26 |
| AdditiveFOAM | Off topic: metal additive-manufacturing research | 2026-11-26 |
| OpenAM-SimCCX | Off topic: a paper on additive-manufacturing simulation | 2026-11-26 |
| MALAMUTE (MOOSE) | Off topic: additive-manufacturing research | 2026-11-26 |
| Truchas / Truchas-PBF | Off topic: casting and metal-printing research | 2026-11-26 |
| PySLM | Off topic: laser powder-bed scan paths | 2026-11-26 |
| Helio Additive "Dragon" | Proprietary cloud print simulation | 2026-11-26 |
| SmartSlice for Cura | Gone: the link now lands on Markforged's simulation page | 2026-11-26 |
| Markforged Simulation | Vendor feature of Markforged printers | 2026-11-26 |
| 5minlab 3D Printer Simulator | A game | 2026-11-26 |
| Obico | Off topic: printer failure monitoring | 2026-11-26 |
| PrintWatch | Off topic: printer failure monitoring | 2026-11-26 |
| FEniCS | General PDE research framework; not a robot-building tool | 2026-11-26 |
| MOOSE Framework | Off topic: multiphysics research framework | 2026-11-26 |
| py2g (Browser-Based CAD) | Duplicate of py2g above | 2026-11-26 |
| js2g (Browser-Based CAD) | Duplicate of js2g above | 2026-11-26 |
| Rig Cad | Freemium closed web app, new in 2026 | 2026-11-26 |
| CADmium | Archived; Elastic License 2.0 is not open source | 2026-11-26 |
| Replicad (Browser-Based CAD) | Duplicate of Replicad above | 2026-11-26 |
| JSCAD (Browser-Based CAD) | Duplicate of JSCAD (OpenJSCAD) above | 2026-11-26 |
| CadHub | Still "pre-alpha"; its repo has had no commit since 2023-01-28 | 2026-11-26 |
| OpenCascade.js (Browser-Based CAD) | Duplicate of OpenCascade.js above | 2026-11-26 |
| Pyodide | Off topic: Python in the browser | 2026-11-26 |
| vpype | Off topic: pen-plotter art | 2026-11-26 |
| DrawingBotV3 | Off topic: pen-plotter art | 2026-11-26 |
| AxiDraw / NextDraw Software | Off topic: control software for one plotter brand | 2026-11-26 |
| DrawBot | Off topic: 2D graphics on macOS | 2026-11-26 |
| vsketch | Off topic: pen-plotter art | 2026-11-26 |
| Cuttle.xyz | Proprietary web app for 2D laser designs | 2026-11-26 |
| PlotterFiles | Off topic: plotter SVG sharing | 2026-11-26 |
| ChiselCAD (LTKMN) | Its own code is under a non-commercial licence | 2026-11-26 |
| Topy | Inactive since 2022 | 2026-11-26 |
| DL4TO | Research code, inactive since 2024-11 | 2026-11-26 |
| Processing | Off topic: creative coding | 2026-11-26 |
| p5.js | Off topic: creative coding | 2026-11-26 |
| Paper.js | Off topic: vector graphics scripting | 2026-11-26 |
| Observable / D3.js | Off topic: data notebooks | 2026-11-26 |
| Beetle Blocks | Off topic: block coding for art; inactive since 2020 | 2026-11-26 |
| Tinkercad Codeblocks | Proprietary block coding for education | 2026-11-26 |
| Descartes.jl | Small Julia CAD; last commit 2024-07-07 | 2026-11-26 |
| Comodo.jl | Off topic: Julia computational-mechanics research | 2026-11-26 |
| Meshes.jl | Off topic: Julia computational geometry | 2026-11-26 |
| Klipper G-Code Reference | Part of Klipper's docs; Klipper is an index row | 2026-11-26 |
| FullControl LLM Reference | Part of FullControl's repo; FullControl is an index row | 2026-11-26 |
| FullControl GCode Designer (Legacy) | Superseded by FullControl's Python library | 2026-11-26 |
| LinuxCNC G-Code Reference | Part of LinuxCNC's docs; LinuxCNC is an index row | 2026-11-26 |
| awesome-plotters | Off topic: pen plotters | 2026-11-26 |
| PlotterFiles (Resources) | Duplicate of PlotterFiles above | 2026-11-26 |

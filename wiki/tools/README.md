# Tools

The programs and platforms you design, simulate and build in. Template:
[templates/tool.md](../../templates/tool.md).

Every tool page says its **support tier** (plan §7):

| Tier | Meaning | Tools |
|---|---|---|
| `first-class` | Skills, a tested setup, an MCP server where one exists | FreeCAD (Python), KiCad (with Konnect), MuJoCo, ROS 2 |
| `documented` | This wiki page only | Fusion 360, EasyEDA, build123d, CadQuery, OpenSCAD, Isaac Sim |

Video tools go in `video/` once the video track starts.

- Name a file after the tool: `freecad.md`, `kicad.md`, `mujoco.md`.
- Record the version you tested and the date; tools move fast.
- A tool we install or take from has an entry in the [source registry](../../sources/registry.yaml);
  its page names that entry in `registry`.

## Index

<!-- index:start -->
| Name | Kind | Area | Support | Licence | Tested | Agent access | Verified |
|---|---|---|---|---|---|---|---|
| [colcon](colcon.md) | tool | ros2 | documented | Apache-2.0 | — | cli | 2026-11-18 |
| [Foxglove](foxglove.md) | tool | ros2 | documented | — | — | mcp | 2026-11-18 |
| [Pixi (with RoboStack)](pixi.md) | tool | ros2 | documented | BSD-3-Clause | — | cli | 2026-11-18 |
| [PlotJuggler](plotjuggler.md) | tool | ros2 | documented | MPL-2.0 | — | gui-only | 2026-11-18 |
| [Rerun](rerun.md) | tool | ros2 | documented | MIT OR Apache-2.0 | — | api | 2026-11-18 |
| [ROS 2](ros2.md) | framework | ros2 | first-class | Apache-2.0 | — | cli | 2026-11-18 |
<!-- index:end -->

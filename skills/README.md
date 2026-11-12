# Skills

How an agent does the work. Each skill is a folder with a `SKILL.md` in the
[Agent Skills](https://agentskills.io) format, written from
[templates/skill/SKILL.md](../templates/skill/SKILL.md).

**Flat folders with a category prefix.** That is the layout agents discover reliably.

| Prefix | Area |
|---|---|
| `ros2-` | ROS 2 core, control, robot description, web bridge |
| `sim-` | MuJoCo, Gazebo, sim-to-real |
| `cad-` | FreeCAD scripting and build systems, 3D printing |
| `pcb-` | KiCad schematics, layout, manufacturing |
| `fw-` | MCUs, peripherals, RTOS, micro-ROS, motor control |
| `perception-` | Cameras, lidar, SLAM |
| `nav-` | Nav2, path planning |
| `manip-` | MoveIt 2, grasping |
| `control-` | Control systems |
| `learn-` | Robot learning, edge deployment |
| `arch-` | Robot architecture, safety |
| `ops-` | Bringup, fleets, Docker and CI |
| `video-` | Video production |
| `diagram-` | Diagrams and figures |

- Every skill lists the registry ids it was taken or distilled from in `metadata.sources`, and a
  skill that keeps upstream files has an `upstream.md`.
- Keep `SKILL.md` short; move long reference material into `references/` beside it.
- Skills that only one project needs live in that project's `.claude/skills/`, not here.

The old skills wait in [legacy/skills/](../legacy/skills/) until Phase 2 re-files them, as
[docs/legacy-audit.md](../docs/legacy-audit.md) records.

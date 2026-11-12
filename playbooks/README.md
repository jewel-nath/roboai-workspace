# Playbooks

The path from an idea to a working robot, one playbook per stage. Each playbook is a checklist
that names the skills, wiki pages and tools the stage uses, and says what "done" means.

| # | Stage | Covers |
|---|---|---|
| 1 | Idea and requirements | Goal, use cases, budget, constraints, reference robots from the Atlas |
| 2 | Architecture | Block diagram, compute and MCU split, power, safety |
| 3 | Mechanical | Skeleton, CAD in FreeCAD, design for printing, assembly |
| 4 | Electronics | Schematic and PCB in KiCad, wiring, BOM |
| 5 | Firmware | MCU, peripherals, RTOS, micro-ROS, motor control |
| 6 | Software | ROS 2, perception, navigation, manipulation |
| 7 | Simulation | MuJoCo model from CAD, checks, Gazebo with ROS 2 |
| 8 | Integration and bringup | First power-on, calibration, hardware integration |
| 9 | Testing | Unit, integration, simulation, hardware-in-the-loop, field |
| 10 | Learning | Data collection, training, deployment on the robot |
| 11 | Deployment | Production setup, updates, fleets |
| 12 | Showing it | Documentation and videos |

Playbooks are written in Phase 6. Until then, the old guides are in
[legacy/guides/](../legacy/guides/).

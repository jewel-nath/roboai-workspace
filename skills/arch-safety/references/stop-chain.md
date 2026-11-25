# The stop chain: hardware decides, ROS is told

How the emergency and protective stops are built, what each stop category means, and the one-way
connection between the rated chain and ROS. The parts, their ratings and the stop categories come out
of the risk assessment ([standards.md](standards.md)); this page shows the shape, not a certified design.

## Stop categories (IEC 60204-1)

The three categories, in the words of a drive maker's explanation
([Kollmorgen, stop and emergency stop function](https://www.kollmorgen.com/en-us/developer-network/stop-and-emergency-stop-function)),
for the edition listed in [standards.md](standards.md):

| Category | What happens | Typical means |
|---|---|---|
| 0 | Power to the actuators is cut at once: an uncontrolled stop; axes coast or are held by brakes | Safe Torque Off (STO) in each drive, or a contactor on motor power |
| 1 | The drives brake under power to standstill, then power is cut | A safety controller or safety drive function that brakes, then removes torque |
| 2 | The drives brake to standstill and stay powered | A normal controlled stop; never an emergency stop |

Rules from the same page that shape the software:

- The category of each stop is chosen by the risk assessment.
- An emergency stop is category 0 or 1, has priority over every other function in every mode, and
  is triggered by one manual action.
- Resetting a stop must not restart the machine. Restart is a separate, deliberate command.

## Shape of the chain

```text
Emergency stop buttons (two channels) ─┐
Safety scanner outputs (OSSD) ─────────┼──> safety relay or ──> STO input of every drive
Door switches, enabling device ────────┤    safety controller   (or contactor on motor power; brakes)
Manual reset button ───────────────────┘          │
                                                  ├──> status output (not safety-rated) ──> robot I/O ──> ROS
Robot computer: "allow motion" output ────────────┘    (optional input: absent signal means stop)
```

1. Every path from a stop device to the motors is rated hardware. No Linux, ROS, USB, Wi-Fi or
   unrated microcontroller sits in it.
2. ROS reads the chain's status and may ask for a stop. It never resets, mutes, bypasses or
   reconfigures the chain.
3. If ROS gets an input into the safety controller, wire it so that a missing signal means stop:
   the computer has to hold "allow motion" active, so a crashed or unpowered computer stops the robot.
4. Reset is a manual action by a person who can see the robot. Putting it on a web page or a ROS
   service defeats it.
5. Axes that fall or roll when torque is removed (arm joints, lifts, a base on a slope) need brakes
   that hold without power; whether category 1 is needed instead of 0 is the assessor's call.
6. A wireless or remote stop counts only if the product is rated for that use. A ROS topic from a
   tablet is not a stop button.
7. STO removes torque; it does not make the electrics safe to touch. Battery and bus isolation for
   maintenance is a separate measure.

## Safety sensors and their ROS drivers

A safety laser scanner stops the robot through its own outputs into the safety controller, using
fields configured and validated in the device. If the fields must change with speed or task, that
switching also happens in the rated parts, not from ROS. The ROS driver only gives a copy of the data
for navigation, logging and display.

| Package (Jazzy binary, 2026-11-25) | Device | What ROS gets |
|---|---|---|
| `sick_safetyscanners2` 1.0.5, Apache-2.0 | SICK microScan3, nanoScan3, outdoorScan3 (Ethernet) | `LaserScan`, an extended scan with intrusion data, output path status, raw data |
| `sick_safevisionary_ros2` 1.0.5, Apache-2.0 | SICK safeVisionary2 | its data for ROS; read the README for topics |
| `sicks300_ros2` 1.4.0, Apache 2.0 | SICK S300 | `LaserScan` |

Other makers' scanners without a ROS 2 driver can still guard the robot: the safety function never
needed ROS. Feed the scan to Nav2 costmaps and the collision monitor; never let a ROS topic decide
that the robot may move.

## Telling ROS about a stop

**Status in.** Read the safety controller's status output (a GPIO, an I/O module or a fieldbus status
word) and publish it latched: a `std_msgs/Bool` or your own message on `/safety/state` with
`TRANSIENT_LOCAL` durability and depth 1, so late subscribers see the current state. The stop gate in
[watchdog-node.md](watchdog-node.md) subscribes to it.

**Hardware interface.** When the drive reports STO or a fault, let `write()` return
`hardware_interface::return_type::DEACTIVATE`. With Jazzy's default
`deactivate_controllers_on_hardware_self_deactivate: true` (controller manager, ros2_control 4.50),
the controllers using that component are deactivated. The same value returned from `read()` is treated
as `ERROR` (the component goes to `on_error`). The controller manager's latched `~/activity` topic
reports the change. Plugin structure: [ros2-control](../../ros2-control/SKILL.md).

**Reaction in ROS.** Stop publishing motion, latch the stop gate, cancel Nav2 and MoveIt goals, log
the event with its reason. Nothing in ROS should try to "recover" by itself.

**Recovery, after the chain is reset by hand:**

```bash
ros2 service call /stop_gate/reset std_srvs/srv/Trigger          # operator confirms in ROS too
ros2 control set_hardware_component_state my_robot_system active
ros2 control switch_controllers --activate diff_drive_controller
```

The hardware interface's `on_activate` sets commands to the measured state (zero velocity, current
position), so nothing jumps. Command sources start from zero; the next goal is a deliberate act.

## Tests

Run them before the first powered motion, after any change to the chain or its wiring, and at the
interval the assessment sets. Log each with date, software versions and result.

| Test | Pass |
|---|---|
| Each emergency stop, robot computer switched off | Torque off; no motion on release; no motion on reset |
| Each emergency stop while ROS commands motion at full speed and payload | Same, with stop time and distance recorded |
| Body into each protective field, ROS stack killed | The robot stops |
| One channel of an emergency stop opened (simulated wiring fault) | The relay or controller stays stopped and needs reset, as its manual describes |
| Robot computer powered off while driving | The robot stops (drive or firmware command timeout) |
| Chain status reaches ROS | `/safety/state` changes; controllers deactivate; the stop gate latches |
| Reset sequence | No motion until a new command |

For engineering numbers, record `/joint_states` (or odometry) and `/safety/state` with `ros2 bag` at
full speed and payload; the stopping distance is the travel after the trigger. These are estimates
from unrated clocks. The assessor decides how stopping performance is measured for the record.

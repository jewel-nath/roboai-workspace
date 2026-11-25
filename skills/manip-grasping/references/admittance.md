# Compliant contact with the admittance controller

Part of [manip-grasping](../SKILL.md). Makes a position-controlled arm give way to contact forces
measured at the wrist, for placing, light pressing or hand guiding at low speed. Checked
against ros2_controllers 4.43.1 (`admittance_controller` userdoc, parameter YAML, source and test
parameters) and kinematics_interface 1.7.2, `jazzy`. Not run. Tuning theory (impedance versus
admittance, stability, contact dynamics) is for the later `control-` skills.

## How it fits

`admittance_controller` is a chainable controller. MoveIt still sends a `FollowJointTrajectory`
goal to `arm_controller`; the trajectory controller writes its references into the admittance
controller's reference interfaces (`admittance_controller/<joint>/position` and `velocity`), and
the admittance controller adds the motion that the measured wrench calls for, then writes the
hardware's joint commands. It needs a kinematics plugin and the F/T sensor's six state interfaces.

```bash
sudo apt install ros-jazzy-admittance-controller ros-jazzy-kinematics-interface-kdl
```

`kinematics_interface_kdl` is only a test dependency of the controller, so it is not installed
with it. Without it the controller cannot load its kinematics plugin and fails to configure.

## Controller YAML

```yaml
# my_robot_bringup/config/controllers.yaml (joint_state_broadcaster and ft_broadcaster as before)
admittance_controller:
  ros__parameters:
    type: admittance_controller/AdmittanceController
    joints: [joint1, joint2, joint3, joint4, joint5, joint6]
    command_interfaces: [position]             # what the hardware takes
    state_interfaces: [position, velocity]
    chainable_command_interfaces: [position, velocity]   # default
    kinematics:
      plugin_name: kinematics_interface_kdl/KinematicsInterfaceKDL
      plugin_package: kinematics_interface     # package of the base class, not of the plugin
      base: base_link
      tip: tcp                                 # every frame below must be on base -> tip
      alpha: 0.01                              # default; pseudo-inverse damping
    ft_sensor:
      name: ft_sensor                          # prefix of force.x ... torque.z
      frame:
        id: ft_sensor_link
      filter_coefficient: 0.05                 # default; exponential smoothing
    control:
      frame:
        id: tcp                                # admittance axes are this frame's axes
    fixed_world_frame:
      frame:
        id: base_link                          # gravity must point along -z here
    gravity_compensation:
      frame:
        id: ft_sensor_link
      CoG:
        pos: [0.0, 0.0, 0.06]                  # example: tool CoG in that frame, m
        force: 8.8                             # example: tool weight in N (mass x 9.81), positive
    admittance:
      selected_axes: [false, false, false, false, false, false]   # x y z rx ry rz: start all off
      mass: [5.5, 6.6, 7.7, 8.8, 9.9, 10.1]                       # upstream test values
      damping_ratio: [2.83, 2.83, 2.83, 2.83, 2.83, 2.83]         # upstream test values
      stiffness: [214.1, 214.2, 214.3, 214.4, 214.5, 214.6]       # upstream test values
      joint_damping: 5.0                       # default
    enable_parameter_update_without_reactivation: true   # default: ros2 param set acts live

arm_controller:
  ros__parameters:
    type: joint_trajectory_controller/JointTrajectoryController
    joints: [joint1, joint2, joint3, joint4, joint5, joint6]           # states from hardware
    command_joints: [admittance_controller/joint1, admittance_controller/joint2,
                     admittance_controller/joint3, admittance_controller/joint4,
                     admittance_controller/joint5, admittance_controller/joint6]
    command_interfaces: [position, velocity]   # fill both references the admittance exports
    state_interfaces: [position, velocity]
```

- The mass, damping-ratio and stiffness lines are the values in the package's test file for a
  test robot. They show the format and load; they are not tuning for your arm. Units: kg, -, N/m
  for x y z; kg m^2, -, N m/rad for the rotations. Every float needs its decimal point.
- Damping is computed as `D = damping_ratio * 2 * sqrt(mass * stiffness)`. A stiffness of 0 on a
  selected axis therefore also gives 0 Cartesian damping there; only `joint_damping` remains and
  the arm keeps drifting after a push. Keep some stiffness on every selected axis.
- The controller reads the sensor's state interfaces itself and applies its own gravity
  compensation and smoothing. The broadcaster's `offset` and filter chain do not reach it.
  Tare the sensor in hardware with no tool fitted (or through the driver), then give the tool's
  weight and CoG here. `~/wrench_reference` (`WrenchStamped` in the sensor frame) is added to the
  measurement, which can cancel a small constant residual.

## Spawn the chain

The two controllers must become active together (`--activate-as-group`):

```bash
ros2 run controller_manager spawner joint_state_broadcaster ft_broadcaster \
  --param-file my_robot_bringup/config/controllers.yaml
ros2 run controller_manager spawner admittance_controller arm_controller --activate-as-group \
  --param-file my_robot_bringup/config/controllers.yaml
ros2 control list_controllers        # both active; arm_controller chained to admittance_controller
ros2 control list_hardware_interfaces | grep admittance   # its reference interfaces, claimed
```

MoveIt's `moveit_controllers.yaml` keeps pointing at `arm_controller`
([manip-moveit2](../../manip-moveit2/SKILL.md)).

## Bring-up order on the real arm

1. Mock hardware first: the chain activates and MoveIt moves the mock arm exactly as without it.
2. Real arm, all `selected_axes` false, slow MoveIt scaling, emergency stop in hand: motion must
   be identical to the plain trajectory controller.
3. Watch `/admittance_controller/status` (`control_msgs/msg/AdmittanceControllerState`):
   `wrench_base` near zero with the arm still in several orientations. If not, fix the tare or
   `gravity_compensation` before enabling any axis.
4. Enable one axis (z for placing), with high stiffness. Push the tool gently along it: it must
   give way and come back without oscillating. Lower stiffness step by step (`ros2 param set
   /admittance_controller admittance.stiffness "[...]"`) until it yields with the force you want.
   Oscillation or buzzing: raise the damping ratio or the mass, or go back to the last good step.
5. Only then use it in a task, and still with the force guard from
   [grasp-checks.md](grasp-checks.md) armed: compliance limits the force growth, not the force.

## For pick and place

- **Placing:** z compliance in `tcp` lets the object settle on a surface whose height you know only
  roughly; move down to slightly below the expected height and open when the force guard or the
  status wrench shows contact.
- **Grasping from a table:** z compliance absorbs a fingertip landing a little early.
- **Insertion, polishing, peg-in-hole, force-tracking:** these need force control and search
  strategies, beyond this skill (later `control-` skills).

## Limits it does not give you

The admittance controller has no force, velocity or workspace limit of its own. A strong push or
a wrong gravity setting moves the arm as far as the joint limits allow. Keep
`enforce_command_limits: true` on the controller manager (default `false` on Jazzy), slow MoveIt
scaling, the force guard, and the arm's own safety settings.

Sources: ros2_controllers `jazzy` (admittance_controller userdoc, `admittance_controller_parameters.yaml`,
`admittance_controller.cpp` topics and `add_wrenches`, `admittance_rule_impl.hpp` damping and
gravity terms, `test/test_params.yaml`, `package.xml`; joint_trajectory_controller parameter YAML:
`command_joints`); kinematics_interface `jazzy` (`kinematics_interface_kdl.cpp`: links must be on
the chain); ros2_control `jazzy` (`spawner.py`: `--activate-as-group`; controller_manager
parameters: `enforce_command_limits`); control_msgs `jazzy` (`AdmittanceControllerState.msg`).

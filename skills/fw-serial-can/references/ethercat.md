# EtherCAT: what is checkable today

Part of [fw-serial-can](../SKILL.md). Only what the current upstream repositories state, read on
2026-11-27: the IgH EtherCAT Master (`stable-1.6`, release 1.6.13), SOEM (v2.0.1 and `master`) and
`ethercat_driver_ros2` (`jazzy` branch, v2.0.0). Nothing here was run. EtherCAT's own terms are now
MainDevice and SubDevice; the tools and code below still say master and slave.

## When it is worth it

Many servo axes or I/O modules on one cable with cycle times well under a millisecond and
distributed clocks. The costs: a dedicated Ethernet port, a real-time capable kernel and setup,
GPL-licensed masters, and drives that cost more than CAN ones. For a few axes at 100 Hz to 1 kHz,
CAN or CANopen ([ros2-canopen.md](ros2-canopen.md)) is simpler.

## Masters

| | IgH EtherCAT Master | SOEM |
|---|---|---|
| Form | Kernel modules plus the `libethercat` user library and the `ethercat` tool | A user-space C library on a raw socket |
| Licence | GPL-2.0 (master, modules); LGPL-2.1 (`lib/`) | GPL-3.0, or a commercial licence from RT-Labs |
| Install | From source: `./bootstrap`, `./configure --sysconfdir=/etc`, `make all modules`, `make modules_install install`, `depmod` | CMake build; link the library |
| Config | `/etc/ethercat.conf`: `MASTER0_DEVICE` (MAC address or interface name), `DEVICE_MODULES` (`generic` or a native driver) | In code: the interface name passed to `ecx_init()` |
| Start | `sudo systemctl start ethercat` | Your process (needs raw-socket rights) |

- **IgH:** rebuild the modules after every kernel update. Native drivers (`e1000e`, `r8169`,
  `igb`, `igc` and others) are off by default and need their `--enable-<driver>` configure switch;
  `generic` works with any NIC. Character devices are `root` 0660; IgH's INSTALL suggests a udev rule
  `KERNEL=="EtherCAT[0-9]*", MODE="0664"` for read access. Tool commands: `ethercat master`,
  `ethercat slaves`, `ethercat pdos`, `ethercat upload` / `download` (SDO), `ethercat states`,
  `ethercat cstruct`. Secure Boot blocks unsigned modules (ethercat_driver_ros2 install notes).
- **SOEM 2.x** has only the context API: `ecx_init(&ctx, ifname)`, `ecx_config_init`,
  `ecx_config_map_group`, `ecx_configdc`, `ecx_statecheck`, `ecx_writestate`,
  `ecx_send_processdata`, `ecx_receive_processdata`, with SubDevices in `ctx.slavelist`. The old
  global API (`ec_init`, `ec_config_init(FALSE)`, `ec_slave[]`) is gone; code written for SOEM 1.x
  needs porting. Its `samples/simple_ng` shows the loop: send, receive, compare the working counter
  with `outputsWKC * 2 + inputsWKC`.

## ros2_control: `ethercat_driver_ros2`

- No binary package on Jazzy or Lyrical (rosdistro, 2026-11-27). Build the `jazzy` branch from
  source in a workspace; it needs the IgH master installed (its CMake looks in `/usr/local/etherlab`
  and the system paths). Apache-2.0, but it links IgH's LGPL library.
- Its install docs still describe Ubuntu 22.04, IgH `stable-1.5` and `/etc/init.d/ethercat`; IgH's
  own INSTALL for 1.6 uses `/etc/ethercat.conf` and systemd. Its CI builds IgH 1.5's user library on
  Jazzy; whether it runs against 1.6 was not checked.
- Plugin `ethercat_driver/EthercatDriver` (`master_id`, `control_frequency` parameters), one
  `<ec_module>` per SubDevice with `alias`, `position` and a `slave_config` YAML (vendor and product
  ID, PDO mapping with `command_interface` / `state_interface` names, startup SDOs). Generic plugins:
  `ethercat_generic_plugins/GenericEcSlave` and `ethercat_generic_plugins/EcCiA402Drive`.
- `EcCiA402Drive` brings the drive to Operation enabled by itself at start unless a `control_word`
  command interface is used, and sends the last read position as target while the position command
  is NaN. Keep the axis clear at launch.
- It overrides `export_state_interfaces()`; ros2_control 6 (Lyrical) removed that method, so it
  will not build there without porting.

## Safety

- The SubDevice's process-data watchdog drops its outputs when frames stop; configure it with
  `ecrt_slave_config_watchdog()` (IgH) and check the drive's reaction in its manual.
- Drives with Safe Torque Off wired to the E-stop chain are the stop function; FSoE (FailSafe over
  EtherCAT, supported by `EthercatSafetyDriver`) needs certified safety devices
  ([arch-safety](../../arch-safety/SKILL.md)).

## First checks

```bash
sudo systemctl start ethercat
ethercat master            # link up, the NIC you configured
ethercat slaves            # every SubDevice listed, state PREOP before the application runs
ethercat pdos -p 0         # PDO mapping of the first SubDevice, to write slave_config from
```

Sources: IgH EtherCAT Master `README.md`, `INSTALL.md`, `NEWS.md`, `script/ethercat.conf`,
`include/ecrt.h`, `tool/Command*.cpp` (gitlab.com/etherlab.org/ethercat, `stable-1.6`); SOEM
`LICENSE.md`, `README.md`, `include/soem/*.h`, `samples/simple_ng` (OpenEtherCATsociety/SOEM);
ethercat_driver_ros2 `INSTALL.md`, sphinx docs (installation, configuration, CiA 402 drive,
safety), `ethercat_driver/ethercat_driver_plugin.xml`, `ethercat_interface/CMakeLists.txt`,
`.github/workflows/ci.yml` and `.docker/Dockerfile` (ICube-Robotics, `jazzy`).

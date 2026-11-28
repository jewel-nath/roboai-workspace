# Over-the-air update tools

Part of [ops-fleet](../SKILL.md). Releases of your ROS software ([releases.md](releases.md)) and
updates of the operating system underneath are separate problems. Containers or debs with the
Ansible rollout cover the first. An A/B image tool covers the second: it writes the new root
filesystem to the inactive slot, boots it once, and falls back to the old slot if the new one
does not come up and confirm. Facts below were read on 2026-11-25 from each project's repository,
docs and pricing page; prices change, so re-check before choosing.

## Compared

| Tool | What it updates | Licence | Paid parts | Raspberry Pi | Jetson |
|---|---|---|---|---|---|
| Your images or debs + Ansible | ROS software only | Ansible GPL-3.0 (control machine) | none | yes | yes |
| Mender | Root filesystem A/B; containers with its docker-compose Update Module (client 6.0+) | Client and mender-convert Apache-2.0; open-source server free to self-host | Hosted: Basic $34/month to 50 devices, Professional $291/month to 250, Enterprise custom; delta updates from Professional; phased rollouts, RBAC, audit logs and server-side delta generation are Enterprise | mender-convert core configs: Raspberry Pi OS 64-bit (bookworm) on Pi 3 and 4, Ubuntu 32-bit on Pi 4; Pi 5 configs exist | Yocto with `meta-mender-tegra` (meta-mender-community) |
| RAUC | A/B slots from signed bundles | LGPL-2.1 | none; pair with Eclipse hawkBit (EPL-2.0) as the rollout server | `meta-rauc-raspberrypi` (Yocto) | no layer in meta-rauc-community |
| SWUpdate | Images, files, scripts; A/B or rescue system | GPL-2.0 with an OpenSSL exception; control library LGPL-2.1 | none; hawkBit via its suricatta mode | `meta-swupdate-boards` (Yocto) | OE4T `tegra-demo-distro` ships `meta-swupdate` |
| balena | balenaOS host OS plus your containers | balenaOS Apache-2.0; openBalena server AGPL-3.0 | balenaCloud: Free 10 devices; Prototype $159/month for 30; Pilot $329/month for 60; Production $1,439/month for 110 | Pi 4 (64-bit), Pi 5 | AGX Orin, Orin NX, Orin Nano boards on its device list |
| NVIDIA Jetson Linux OTA | Jetson Linux (bootloader, kernel, root filesystem) | NVIDIA | none | — | Image-based OTA covers AGX Orin and Orin NX/Nano in the r36.4 guide; apt covers point releases |

## How to choose

- **Ubuntu 24.04 with ROS 2 Jazzy on the host** (the common case): ship ROS software as images or
  debs with the Ansible rollout; let `unattended-upgrades` apply Ubuntu security updates (its
  default: security origin only, no automatic reboot), and reboot robots in a maintenance window
  when `/var/run/reboot-required` exists. Add an A/B tool only when a failed OS update in the field
  would strand a robot.
- **You build the OS image yourself (Yocto or Buildroot)**: RAUC or SWUpdate, both free, with
  hawkBit if you want a server with rollout campaigns; Mender if you want a ready server and UI.
  Their A/B layouts and bootloader hooks are set up per board.
- **Mender on stock images**: mender-convert supports Raspberry Pi OS 64-bit officially, not
  Ubuntu 64-bit on the Pi (only a 32-bit Ubuntu config; ROS 2 Jazzy has no 32-bit ARM binaries). On
  a Pi running Ubuntu 24.04, use Mender for container updates only, or move the OS layer to
  Raspberry Pi OS and run ROS in containers. Mender's older "app" update module (`app-gen`) is
  discontinued; use the docker-compose Update Module.
- **balena**: the host is balenaOS, not Ubuntu; ROS 2 runs in your containers (`ros:jazzy`
  images work). Good when you want the whole stack managed; budget for balenaCloud beyond 10
  devices, or self-host openBalena (single user, CLI only, full image downloads, no remote
  diagnostics).
- **Jetson with JetPack**: within a Jetson Linux minor release, `apt upgrade` updates NVIDIA's
  packages (`nvidia-l4t-core` blocks partial upgrades); across releases, NVIDIA's image-based
  OTA. Root filesystem A/B redundancy is off by default and is chosen when the device is flashed.
  Mender, SWUpdate and balena on Jetson replace JetPack's Ubuntu with their own image.
- **RAUC and SWUpdate on Ubuntu**: both are packaged in Ubuntu 24.04 (universe: `rauc`
  1.11.3, `swupdate` 2023.12.1), older than upstream; the slot layout and bootloader integration
  are still yours to build.

## Rules whatever the tool

- **Update only idle robots.** Gate the update on the robot's state (docked, no task); an OS
  tool's server does not know the robot is carrying a load.
- **Confirm only after the robot works.** A/B tools commit the new slot when told to. Tie the
  commit to the health endpoint ([health.md](health.md)), not to "the system booted".
- **Keep a path back for configuration.** Files under `/etc/my_robot/` and data partitions
  survive slot switches only if they live on a partition outside the slots; plan the layout so
  calibration and identity are not lost on update.
- **Same version everywhere you test.** The OS image, the ROS release and the firmware
  ([fw-mcu](../../fw-mcu/SKILL.md)) each carry a version; record all three in the health report.
- **Paid tiers count devices**: spares, test benches and simulators that register count too.

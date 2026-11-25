---
type: guide
name: Choose a deployment method
summary: How to package, install, start and update the software on a ROS 2 robot (PC, Raspberry Pi or Jetson), from one robot to a fleet - native apt and systemd, your own debs, Docker or Podman images, jetson-containers, snaps, Pixi, Nix, A/B OS update tools and balena - decided by hardware access, robot count, site network, rollback, team skills and paid terms.
tags: [deployment, packaging, updates, ota, rollback, systemd, robot-upstart, apt, bloom, aptly, docker, compose, podman, quadlet, jetson, jetson-containers, isaac-ros, snap, snapcraft, pixi, robostack, nix, mender, rauc, swupdate, balena, ansible, fleet, open-rmf, sros2, ros2]
question: How should I package, install and update the software on my ROS 2 robot?
options: [apt-systemd, own-debs, docker-compose, podman-quadlet, jetson-containers, snap, pixi, nix, ota-image, balena]
recommendation: "Native for the first robot: ROS 2 Jazzy from apt, a colcon workspace and a hand-written systemd unit; from the second robot or the first field deployment, versioned releases - Docker Engine and Compose images deployed by digest, or your own debs on small hosts - with a health-gated rollout and rollback; jetson-containers or Isaac ROS images for CUDA on Jetson; an A/B OS update tool only when a failed OS update must never strand a robot."
evidence: researched
last_verified: 2026-11-25
sources:
  - {url: "https://github.com/ros/rosdistro", title: "rosdistro distribution files: humble, jazzy, kilted, lyrical (robot_upstart, rmf_ros2, fastrtps, fastdds)", accessed: 2026-11-25}
  - {url: "https://github.com/clearpathrobotics/robot_upstart", title: "robot_upstart tag 1.0.4 and jazzy branch: systemd unit, start and stop templates, job.py", accessed: 2026-11-25}
  - {url: "https://docs.docker.com/subscription/desktop-license/", title: "Docker docs: Docker Desktop license agreement", accessed: 2026-11-25}
  - {url: "https://docs.docker.com/engine/network/drivers/host/", title: "Docker docs: Host network driver (platform support, Docker Desktop limitations)", accessed: 2026-11-25}
  - {url: "https://docs.podman.io/en/latest/markdown/podman-auto-update.1.html", title: "Podman docs: podman-auto-update(1); containers/podman LICENSE", accessed: 2026-11-25}
  - {url: "https://github.com/canonical/snapcraft/tree/main/snapcraft/extensions", title: "snapcraft repository (main): ROS 2 Humble, Jazzy and Lyrical extensions", accessed: 2026-11-25}
  - {url: "https://snapcraft.io/docs/how-to-guides/manage-snaps/manage-updates/", title: "Snapcraft docs: Manage updates", accessed: 2026-11-25}
  - {url: "https://github.com/lopsided98/nix-ros-overlay", title: "nix-ros-overlay repository (develop): README, LICENSE", accessed: 2026-11-25}
  - {url: "https://mender.io/pricing", title: "Mender pricing and plan comparison", accessed: 2026-11-25}
  - {url: "https://www.balena.io/pricing", title: "balenaCloud pricing", accessed: 2026-11-25}
---

# Choose a deployment method

How does your software get onto the robot, start at every boot, and give way to the next version
without stranding the robot? For a builder with one robot today and perhaps a fleet later, on a PC,
a Raspberry Pi (64-bit Ubuntu) or an NVIDIA Jetson, with ROS 2 Jazzy; Lyrical and Humble are noted.
Starting at boot is in [ops-bringup](../../skills/ops-bringup/SKILL.md); releases, rollouts and OTA
in [ops-fleet](../../skills/ops-fleet/SKILL.md); images and CI in
[ops-docker-ci](../../skills/ops-docker-ci/SKILL.md).

## Short answer

- **The first robot, during bring-up:** ROS 2 from apt on Ubuntu 24.04 ([ROS 2](../tools/ros2.md)),
  your packages in a colcon workspace, and one hand-written systemd unit that sources one
  environment file ([systemd.md](../../skills/ops-bringup/references/systemd.md)). Nothing stands
  between the drivers and the serial ports, cameras, CAN bus, GPU or real-time limits.
- **Not `robot_upstart` for that unit:** 1.0.4 is released for Humble and Jazzy, not for Kilted or
  Lyrical [1]. Its unit is `Type=simple` with no `Restart=`, is ordered only after
  `network.target`, logs to `/tmp` unless told otherwise and switches user with `setpriv --reuid`
  alone, so the job lacks the user's device groups [2]. Use it only to see a first draft.
- **From the second robot or the first field deployment:** ship releases, never a copied
  workspace. Default: one image per release on [Docker](../tools/docker.md) Engine with Compose,
  deployed by digest, switched by an Ansible rollout that waits for a health check and restores
  the previous digest on failure ([releases.md](../../skills/ops-fleet/references/releases.md),
  [ansible-rollout.md](../../skills/ops-fleet/references/ansible-rollout.md)). Small hosts without
  a container runtime: your own debs built with bloom, in an apt repository you host.
- **Jetson with CUDA work beside ROS:** [jetson-containers](../tools/jetson-containers.md) images
  (ROS built from source, Jazzy at most), or NVIDIA's Isaac ROS environment, which targets Lyrical.
- **The operating system underneath:** Ubuntu security updates through `unattended-upgrades`; add
  an A/B image tool or balena only when a failed OS update must never strand a robot
  ([ota-tools.md](../../skills/ops-fleet/references/ota-tools.md)).

## What decides it

- **Hardware access.** Native nodes open devices like any process. A container gets each device
  passed in: `--device` binds at creation and misses a replugged USB device, `--privileged` grants
  everything and is no sandbox, real-time needs `--cap-add=sys_nice --ulimit rtprio=99`, and GPUs
  need the NVIDIA Container Toolkit ([Docker](../tools/docker.md)). On the host network a container
  shares the host's network stack [4], so SocketCAN interfaces are reachable there too. Fast DDS
  containers also need `--ipc host`, or nodes show up without data ([Docker](../tools/docker.md)).
  Snaps run strictly confined or in devmode [6]: plan each device's access before choosing them.
- **How many robots.** One robot needs a unit file. A few need one release artifact and a rollout
  from a control machine over SSH. Robots you can rarely reach pull instead: `ansible-pull` on a
  timer, or an OTA server they poll
  ([ansible-rollout.md](../../skills/ops-fleet/references/ansible-rollout.md)).
- **The network at the site.** Download the new image or debs while the old release still runs, so
  the switch is only a restart ([releases.md](../../skills/ops-fleet/references/releases.md)). On
  LTE, transfer size counts: Mender ships binary delta updates of the root filesystem from its
  Professional plan [9]; self-hosted openBalena downloads full images
  ([ota-tools.md](../../skills/ops-fleet/references/ota-tools.md)). Behind customer firewalls,
  robots reach the registry, apt repository and log servers outbound, over a VPN
  ([remote-access.md](../../skills/ops-fleet/references/remote-access.md)).
- **Rollback.** Images: the previous digest, with its image kept on disk. Debs: every release
  package pinned, `--allow-downgrades`, old versions still published
  ([releases.md](../../skills/ops-fleet/references/releases.md)). Snaps: `snap revert` [7]. Podman:
  `podman auto-update` restores the previous image when the restarted unit fails [5]. The OS: an
  A/B tool boots the old slot when the new one does not confirm. A copied `install/` folder has no
  version to go back to.
- **Team skills.** Docker and Ansible are widely known. RAUC and SWUpdate mean building the OS
  image yourself (Yocto or Buildroot) with per-board bootloader work; Nix is a language of its own.
- **Licences and paid terms.** Docker Engine is Apache-2.0 and free. Docker Desktop is free for
  businesses under 250 employees and USD 10 million revenue, personal use, education and
  non-commercial open source; larger companies and government bodies need a paid plan; Engine's
  terms are unchanged [3]. Mender hosting starts at $34/month for 50 devices [9]; balenaCloud is
  free for 10 devices [10]. jetson-containers' MIT licence covers its scripts, not the CUDA,
  cuDNN and TensorRT in its images ([jetson-containers](../tools/jetson-containers.md)). Free VPN
  tiers of Tailscale and Husarnet are non-commercial
  ([remote-access.md](../../skills/ops-fleet/references/remote-access.md)).

## Options compared

| Option | Cost | Strengths | Limits | Best when |
|---|---|---|---|---|
| Apt + colcon + systemd unit | Free; Jazzy binaries for amd64 and arm64 ([ROS 2](../tools/ros2.md)); effort: one unit and one env file | Direct device, GPU and real-time access; easiest to debug; the [ops-bringup](../../skills/ops-bringup/SKILL.md) recipes | No version or rollback; `apt upgrade` also moves upstream ROS; an `install/` copied between machines or architectures breaks | One robot; bring-up; a small team |
| Your own debs (bloom + aptly) | Free tools (aptly is MIT); a signed apt repository to host; one build per architecture | Native access with versions; rollback by downgrade; no container runtime | Pin every release package and keep old versions published; pin upstream ROS with the snapshot repository ([releases.md](../../skills/ops-fleet/references/releases.md)) | Small hosts, a few robots, teams fluent in apt |
| Docker Engine + Compose | Engine Apache-2.0, free [3]; a registry; a read-only pull token per robot | The image CI tested is what runs; digest rollback; Compose waits for a healthcheck; `ros` images for Humble to Lyrical on amd64 and arm64 ([Docker](../tools/docker.md)) | Devices, real-time and GPU passed in one by one; DDS needs `--network host --ipc host`; published ports bypass ufw | The default from the second robot on |
| Podman + Quadlet | Apache-2.0 [5]; free | No daemon; each container a systemd unit; `podman auto-update` checks the registry, restarts and rolls back on failure [5] | Auto-update watches a tag for a new digest, so robots cannot be pinned to one digest while it runs [5]; fewer ROS recipes here | Teams that want containers managed as systemd units |
| jetson-containers | MIT scripts; NVIDIA terms for CUDA, cuDNN, TensorRT; NVMe and swap for builds | CUDA, PyTorch and LLM images beside ROS on Orin and Thor ([page](../tools/jetson-containers.md)) | ROS from source, Jazzy at most; no releases; JetPack 7.2 Orin builds failing; `autotag` can pick a wrong L4T image | ML-heavy Jetson robots on JetPack 6.2 or 7 |
| Snap (snapcraft `ros2-jazzy`) | Free to build; a store account; effort: confinement per device | Bundles the ROS runtime; `ros2-humble` (core22) and `ros2-jazzy` (core24) extensions are stable [6]; refresh, hold and revert built in [7] | Devices only through confinement; `ros2-lyrical` and the content-sharing variants are experimental [6]; refreshes run four times a day unless held [7] | Ubuntu Core devices and products shipped to customers |
| Pixi + RoboStack | Pixi BSD-3-Clause; free | One lock file; Linux x86-64 and ARM, macOS and Windows; ROS beside PyTorch ([Pixi](../tools/pixi.md)) | Conda rebuilds, not the upstream debs; no rosdep; Kilted deprecated there | Non-Ubuntu hosts, Windows or macOS machines, ML environments |
| Nix (nix-ros-overlay) | Apache-2.0 [8]; free | Reproducible builds for Humble, Jazzy, Kilted, Lyrical and Rolling [8] | Its free binary cache ran out of room; an experimental cache stands in [8]; Nix skills | Teams already on NixOS |
| A/B OS image (Mender, RAUC, SWUpdate) | Mender client Apache-2.0, hosted from $34/month, Enterprise custom [9]; RAUC LGPL-2.1, SWUpdate GPL-2.0, free with hawkBit ([ota-tools](../../skills/ops-fleet/references/ota-tools.md)) | Atomic OS updates; fallback to the old slot; Mender also updates Compose projects | Per-board slot layout and bootloader; Yocto for RAUC and SWUpdate; mender-convert has no 64-bit Ubuntu config for the Pi | A failed OS update must never strand a robot |
| balena | balenaOS Apache-2.0, openBalena AGPL-3.0; balenaCloud free to 10 devices, then $159/month for 30, $329 for 60, $1,439 for 110 [10] | Host OS and containers managed together; Pi 4 and 5, Orin boards ([ota-tools](../../skills/ops-fleet/references/ota-tools.md)) | The host is balenaOS, not Ubuntu; openBalena is single-user and CLI-only | A managed fleet, paid per device |

## Rules for any update

- **Update only idle robots.** Gate on docked or no task; an update server does not know the robot
  is carrying a load ([ota-tools.md](../../skills/ops-fleet/references/ota-tools.md)).
- **Confirm only after the robot works.** The health endpoint decides, not "it booted"
  ([health.md](../../skills/ops-fleet/references/health.md)); `docker compose up --wait` waits
  only for a service that has a healthcheck.
- **Keep identity outside the release.** Domain ID, parameter overlay, calibration and secrets live
  in `/etc/my_robot/`, written by the rollout and kept off image slots
  ([identity-config.md](../../skills/ops-fleet/references/identity-config.md)).
- **Stopping the stack is not stopping the robot.** A restart or reboot leaves drives on their last
  command unless the firmware times out ([arch-safety](../../skills/arch-safety/SKILL.md)).
- **Record every version:** OS image, ROS release and firmware, in the health report.

## When the answer changes

- **Lyrical:** no `robot_upstart` release, so write the unit by hand [1]; the snapcraft extension
  is experimental on core26 [6]; jetson-containers has no Lyrical images, Isaac ROS does
  ([jetson-containers](../tools/jetson-containers.md)). Fast DDS 3.6 reads
  `FASTDDS_DEFAULT_PROFILES_FILE`, Jazzy's 2.14.7 `FASTRTPS_DEFAULT_PROFILES_FILE` [1]
  ([Fast DDS](../software/fast-dds.md)): rename it in images and env files when you move.
- **Humble:** the snap extension builds on core22 [6]; systemd 249 lacks `udevadm wait`
  ([ops-bringup](../../skills/ops-bringup/SKILL.md)).
- **Development machines on Windows or macOS:** Docker Desktop has host networking from 4.34, after
  sign-in, at layer 4 only, and containers cannot bind the host's addresses [4]; test discovery
  before relying on it. [Pixi](../tools/pixi.md) runs ROS there natively.
- **Robots on shared Wi-Fi or a building network:** add [SROS2](../software/sros2.md). Its
  governance and permission files cover the domain ID set at creation, so make keystores after the
  per-robot domain plan; ship `public/` and that robot's enclaves, and keep `private/` off robots
  and images.
- **Several fleets, or robots that ride lifts and pass doors:** add
  [Open-RMF](../software/open-rmf.md) (`rmf_ros2` 2.7.3 on Jazzy; Lyrical has 2.13.0 but no
  `rmf_dev` [1]). It coordinates traffic and tasks; it does not install, update or monitor robots.
- **Robots offline for weeks:** pull-based updates (`ansible-pull`, an OTA server) and a journal
  sized for the longest gap
  ([observability.md](../../skills/ops-fleet/references/observability.md)).

## Sources

1. [rosdistro distribution files: humble, jazzy, kilted, lyrical (robot_upstart, rmf_ros2, fastrtps, fastdds)](https://github.com/ros/rosdistro), accessed 2026-11-25
2. [robot_upstart tag 1.0.4 and jazzy branch: systemd unit, start and stop templates, job.py](https://github.com/clearpathrobotics/robot_upstart), accessed 2026-11-25
3. [Docker docs: Docker Desktop license agreement](https://docs.docker.com/subscription/desktop-license/), accessed 2026-11-25
4. [Docker docs: Host network driver (platform support, Docker Desktop limitations)](https://docs.docker.com/engine/network/drivers/host/), accessed 2026-11-25
5. [Podman docs: podman-auto-update(1); containers/podman LICENSE](https://docs.podman.io/en/latest/markdown/podman-auto-update.1.html), accessed 2026-11-25
6. [snapcraft repository (main): ROS 2 Humble, Jazzy and Lyrical extensions](https://github.com/canonical/snapcraft/tree/main/snapcraft/extensions), accessed 2026-11-25
7. [Snapcraft docs: Manage updates](https://snapcraft.io/docs/how-to-guides/manage-snaps/manage-updates/), accessed 2026-11-25
8. [nix-ros-overlay repository (develop): README, LICENSE](https://github.com/lopsided98/nix-ros-overlay), accessed 2026-11-25
9. [Mender pricing and plan comparison](https://mender.io/pricing), accessed 2026-11-25
10. [balenaCloud pricing](https://www.balena.io/pricing), accessed 2026-11-25

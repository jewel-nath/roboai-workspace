---
name: ops-fleet
description: >-
  Run ROS 2 Jazzy on several robots: versioned releases (image digests or a bloom-built apt repo), Ansible rollouts with
  health gates and rollback, OTA tools (Mender, RAUC, SWUpdate, balena, Jetson OTA), per-robot identity and params, VPN
  access, ROS_DOMAIN_ID, Fast DDS Discovery Server or Zenoh routers across robots, logs, bags, metrics, Open-RMF.
license: Apache-2.0
metadata:
  sources: []
  evidence: researched
  last_verified: 2026-11-25
---

# Robot fleet operations

Lets an agent take ROS 2 software that works on one robot and run it on many: ship versioned releases,
roll them out with a health gate and automatic rollback, keep each robot's identity and ROS graph
apart, reach robots remotely, and collect logs, metrics and bags. Written for ROS 2 Jazzy on Ubuntu
24.04 (Raspberry Pi and Jetson class computers included); packages and tools checked on 2026-11-25,
recipes not run. Lyrical and Humble differences are at the end.

## When to use

- A second robot is coming, or several robots already run hand-copied workspaces.
- Defining what a release is, writing the rollout, rolling back a bad release.
- Choosing an OTA tool for the operating system, with its licence, paid tiers and board support.
- Per-robot names, domain IDs, calibration and device paths; namespaces when robots share a graph.
- Reaching robots behind NAT or LTE: VPN, SSH, ROS tools across the VPN.
- Fleet logs, metrics, alerts, bag recording and upload; "which robot runs what, and is it healthy?"
- Deciding whether Open-RMF is needed.

Elsewhere: images, compose and CI in [ops-docker-ci](../ops-docker-ci/SKILL.md); starting the stack
at boot (systemd units, udev) in [ops-bringup](../ops-bringup/SKILL.md); SROS 2 keystores, safety
stops and watchdogs in [arch-safety](../arch-safety/SKILL.md) and [SROS 2](../../wiki/software/sros2.md);
browser dashboards and bridges in [ros2-web-bridge](../ros2-web-bridge/SKILL.md); multi-robot
navigation in [nav-nav2](../nav-nav2/SKILL.md).

## The parts

| Concern | Default here | Reference |
|---|---|---|
| What runs | one release: an image by digest, or debs from your apt repository | [releases.md](references/releases.md) |
| How it gets there | Ansible: health gate, canary, batches, rollback | [ansible-rollout.md](references/ansible-rollout.md) |
| The OS underneath | unattended security updates; an A/B image tool when needed | [ota-tools.md](references/ota-tools.md) |
| Who each robot is | identity in `/etc/my_robot/env.sh`, a parameter overlay, its own domain ID | [identity-config.md](references/identity-config.md) |
| Reaching robots | VPN with one identity per robot, SSH keys only | [remote-access.md](references/remote-access.md) |
| ROS graphs | one per robot; join one on purpose (static peers, discovery server, Zenoh) | [discovery.md](references/discovery.md) |
| Is it healthy | diagnostics aggregator and a `/healthz` endpoint | [health.md](references/health.md) |
| Logs, metrics, alerts | journal and host metrics through Alloy to Loki, Prometheus, Grafana | [observability.md](references/observability.md) |
| Bags | split MCAP or snapshots, quota, upload | [bags.md](references/bags.md) |

## Quick start

From a control machine on the VPN, with the `fleet-ops` repository from
[ansible-rollout.md](references/ansible-rollout.md) and an image built by CI:

```bash
ansible-playbook playbooks/provision.yml --limit robot-04   # identity, compose project, agent
ansible-playbook playbooks/status.yml                       # release and health of every robot
# set release_version and release_image (ghcr.io/my-org/my_robot@sha256:<digest>) in group_vars
ansible-playbook playbooks/rollout.yml -e target=canary     # one robot; let it work a while
ansible-playbook playbooks/rollout.yml -e target=fleet      # the rest, in batches
```

On a robot:

```bash
curl -s http://127.0.0.1:8080/healthz     # {"healthy": true, "release": "1.4.0", "problems": []}
cd /opt/my_robot && cp .env.previous .env && docker compose up -d --wait   # manual rollback
```

## Workflow

1. **Define a release.** One immutable artifact per version: a container image deployed by digest
   (default), or debs from `bloom-generate rosdebian` in an apt repository you host (aptly). Never
   `rsync` a workspace `install/` across robots. The version goes to `/etc/my_robot/release`.
   [releases.md](references/releases.md).
   *Check:* the release installs on a bench robot, and going back to the previous one comes up healthy.

2. **Give each robot an identity.** Every robot runs the same release; differences live only in
   `/etc/my_robot/`: `env.sh` (`ROBOT_ID`, `ROS_DOMAIN_ID`, RMW, discovery range), a parameter
   overlay loaded after the release defaults with `/**/node:` keys, calibration files, and secrets
   from Ansible Vault. All rendered from the inventory. [identity-config.md](references/identity-config.md).
   *Check:* `ros2 param get` on a robot returns its overlay values; the inventory's git history
   explains every difference between robots.

3. **Keep the ROS graphs apart.** One domain ID per robot (0 to 101 on Linux; 0 stays for benches),
   discovery limited to the robot (`ROS_AUTOMATIC_DISCOVERY_RANGE=LOCALHOST`, a local discovery
   server, or a local Zenoh router). Namespaces only when robots must share one graph, and then
   remap absolute names such as `/tf` and `/diagnostics`. [discovery.md](references/discovery.md).
   *Check:* robot-02's topics never appear on robot-01; a laptop on the VPN joins robot-01's graph
   only when told to.

4. **Make health measurable.** Diagnostics and one aggregator per robot, as in
   [ops-bringup](../ops-bringup/references/diagnostics.md), plus a `/healthz` endpoint on
   `127.0.0.1` that also checks critical topics and reports the release. [health.md](references/health.md).
   *Check:* stopping a sensor driver turns `/healthz` to 503 with the reason.

5. **Connect the robots to you.** A VPN with one key per robot (a WireGuard hub, or Headscale,
   NetBird or a paid Tailscale plan for meshes), SSH by key only, robots unable to reach each other,
   bridges bound to localhost and tunnelled. [remote-access.md](references/remote-access.md).
   *Check:* `ssh ops@robot-01` works by key over the VPN, password login fails, and robot-01 cannot
   reach robot-02.

6. **Roll out behind a gate.** Ansible picks robots that are online, healthy and idle; pulls first;
   switches; waits for health on the new release; on failure restores the previous release and
   fails the robot so later batches stop. A canary, a soak, then `serial: [1, "25%"]` with
   `max_fail_percentage: 0`. [ansible-rollout.md](references/ansible-rollout.md).
   *Check:* a deliberately broken release on a test robot rolls back and stops the run.

7. **Look after the operating system.** Ubuntu security updates through `unattended-upgrades`
   (security only, no automatic reboot), reboots in maintenance windows. Add an A/B image tool when
   a failed OS update must never strand a robot; Mender, RAUC, SWUpdate, balena and Jetson OTA
   differ in licence, paid tiers and board support. [ota-tools.md](references/ota-tools.md).
   *Check:* an A/B test update that fails the health check boots back into the old slot.

8. **Collect logs and metrics.** The journal (container output through the `journald` log driver)
   and host metrics go through Grafana Alloy to Loki and Prometheus with a `robot` label; ROS
   diagnostics and the release become textfile metrics; ROS log files are aged out as in
   ops-bringup, since Jazzy never rotates them. [observability.md](references/observability.md).
   *Check:* Grafana shows robot-01's log lines and its `my_robot_release_info`.

9. **Record bags.** Split MCAP recordings of state topics, or snapshot mode triggered by incidents;
   robot and release in `--custom-data`; a disk quota; closed files uploaded to storage you own.
   [bags.md](references/bags.md).
   *Check:* a forced incident produces a bag in fleet storage within one upload interval.

10. **Watch the fleet.** Alerts for silent robots, ERROR diagnostics, stopped services, low disk and
    heat; one dashboard row per robot (release, health, battery, last seen); deploys annotated.
    [observability.md](references/observability.md#fleet-alerts).
    *Check:* switching a test robot off fires `RobotSilent`.

11. **Add Open-RMF only for traffic between fleets.** Open-RMF (Apache-2.0; `ros-jazzy-rmf-dev`,
    `rmf_ros2` 2.7.3 on Jazzy) coordinates robots of several fleets or vendors in shared space:
    traffic schedule and negotiation, task allocation, doors and lifts. Each fleet joins through a
    fleet adapter (the `EasyFullControl` API in `rmf_fleet_adapter`; for Nav2 robots, `free_fleet`,
    built from source, which links non-namespaced Nav2 stacks through `zenoh-bridge-ros2dds`). It
    does not deploy, update or monitor robots; the steps above still apply.
    [Open-RMF](../../wiki/software/open-rmf.md).
    *Check:* you have more than one fleet, or shared doors, lifts or corridors, before adding it.

## Traps

| Symptom | Cause | Fix |
|---|---|---|
| A robot obeys another robot's commands | Same domain without namespaces on one network, or Zenoh routers of same-domain robots joined | A domain per robot; join routers only across different domains or fully namespaced graphs |
| `ros2 topic list` from a laptop is empty over the VPN | Multicast discovery does not cross the tunnel; the daemon kept old settings | Static peers, discovery server or Zenoh client ([discovery.md](references/discovery.md)); `ros2 daemon stop` |
| With a discovery server the CLI sees part of the graph | Tools are plain clients | `ROS_SUPER_CLIENT=TRUE`, then restart the daemon |
| Fast DDS XML profile ignored on Jazzy | `FASTDDS_DEFAULT_PROFILES_FILE` is read from Fast DDS 3 (Lyrical) | `FASTRTPS_DEFAULT_PROFILES_FILE` on Jazzy |
| Rollout went on after a robot failed | A successful `rescue` clears the failure | End the rescue with `ansible.builtin.fail` |
| Playbook rejected: `rescue` not valid | `rescue` written at play level | Put it in a `block` |
| Rollback impossible | Previous image pruned, or old debs no longer published | Keep the previous image; publish aptly snapshots that keep old versions |
| Broken links or wrong architecture after copying `install/` | `--symlink-install` links into the build machine; amd64 build | Ship a release artifact built for the robot's architecture |
| `docker compose up --wait` returns, robot broken | No `healthcheck`, or a check that only opens a port | Healthcheck on `/healthz` ([health.md](references/health.md)) |
| Health check slow or hangs | Shells out to `ros2 topic hz` (which has no `--once`) | The node-based endpoint |
| Namespaced node runs on defaults | Parameter key `driver:` does not match `/robot_01/driver` | `/**/driver:` keys |
| Namespaced robots share `/tf` or `/diagnostics` | Absolute names ignore the namespace | Remap per node or `SetRemap` |
| Robot disk fills up | ROS log files (no rotation on Jazzy), bags, journal | `--disable-external-lib-logs` or tmpfiles cleanup; bag quota; `SystemMaxUse` |
| Alloy runs, nothing in Loki | `alloy` user not in `adm` and `systemd-journal` | `usermod -aG adm,systemd-journal alloy` |
| Password login still accepted after hardening | An earlier file in `sshd_config.d` wins | Name the drop-in to sort first; `sshd -T` |
| Robot unreachable after a firewall change | `ufw` enabled before SSH on the VPN interface was allowed | Allow first, canary first |
| A free plan turns out not to cover the fleet | Tailscale Personal and Husarnet Free are non-commercial; Foxglove and balena count devices | Paid plan, or self-host (Headscale, NetBird, rclone, openBalena) |
| Update interrupted a robot at work | No idle gate | Check docked or idle before switching |

## Checks

Before reporting a fleet setup done:

- `status.yml` shows every reachable robot healthy on the intended release, matching
  `my_robot_release_info` in Prometheus.
- A broken release on a test robot rolled back by itself and stopped the rollout.
- robot-01's graph is invisible from robot-02; a VPN laptop joins it only with the documented
  variables.
- Each robot's logs and metrics arrive under its `robot` label; `RobotSilent` fires for a robot
  switched off.
- Bag quota and upload work; finished bags carry robot and release in their metadata.
- No secret sits unencrypted in the inventory, in an image or in a compose file; each robot has
  its own VPN key and tokens; licences and paid tiers of every service used are written down.

## Distro differences

- **Lyrical** (Ubuntu 26.04, Python 3.14): Fast DDS 3 reads `FASTDDS_DEFAULT_PROFILES_FILE`;
  `rmw_zenoh` 0.10 is Tier 1, same environment variables; rosbag2 0.33 drops positional topics and
  adds `--max-bag-files`, `--repeat-transient-local` and `--max-cache-duration`; `domain_bridge` and
  the `rmf_dev` metapackage are not released (the Open-RMF packages are); bloom versions end in
  `-0resolute`. OTA tool support for Ubuntu 26.04 was not checked.
- **Humble** (Ubuntu 22.04): no `ROS_AUTOMATIC_DISCOVERY_RANGE` or `ROS_STATIC_PEERS` (use
  `ROS_LOCALHOST_ONLY` or middleware XML); rosbag2 defaults to sqlite3 (install
  `ros-humble-rosbag2-storage-mcap`, record with `-s mcap`) and has no `--custom-data` or
  `--disable-keyboard-controls`; only `PushRosNamespace`; bloom versions end in `-0jammy`.

## Related

- References: [releases.md](references/releases.md), [ansible-rollout.md](references/ansible-rollout.md),
  [ota-tools.md](references/ota-tools.md), [identity-config.md](references/identity-config.md),
  [discovery.md](references/discovery.md), [remote-access.md](references/remote-access.md),
  [health.md](references/health.md), [observability.md](references/observability.md),
  [bags.md](references/bags.md).
- Skills: [ops-docker-ci](../ops-docker-ci/SKILL.md), [ops-bringup](../ops-bringup/SKILL.md),
  [arch-safety](../arch-safety/SKILL.md), [arch-robot-architecture](../arch-robot-architecture/SKILL.md),
  [ros2-core](../ros2-core/SKILL.md), [ros2-web-bridge](../ros2-web-bridge/SKILL.md),
  [nav-nav2](../nav-nav2/SKILL.md), [sim-to-real](../sim-to-real/SKILL.md); later
  `learn-edge-deployment` (models on Jetson) and the Phase 5 firmware skills (firmware updates).
- Wiki: [Open-RMF](../../wiki/software/open-rmf.md), [SROS 2](../../wiki/software/sros2.md),
  [rmw_zenoh](../../wiki/software/rmw-zenoh.md), [Fast DDS](../../wiki/software/fast-dds.md),
  [Cyclone DDS](../../wiki/software/cyclone-dds.md), [Foxglove](../../wiki/tools/foxglove.md),
  [Rerun](../../wiki/tools/rerun.md), [PlotJuggler](../../wiki/tools/plotjuggler.md),
  [choose a ROS 2 middleware](../../wiki/guides/choose-a-ros2-middleware.md),
  [choose a deployment method](../../wiki/guides/choose-a-deployment-method.md).
- Lifecycle: [playbooks](../../playbooks/README.md) (stage 11, Deployment).
- Upstream: ROS 2 docs (Domain ID, Improved Dynamic Discovery, Discovery Server, Logging, custom
  deb packages), `ros/diagnostics`, `ros2/rosbag2`, `ros2/rmw_zenoh`, `ros2/domain_bridge`,
  Grafana Alloy docs, Ansible docs, and each OTA and VPN project's own documentation.

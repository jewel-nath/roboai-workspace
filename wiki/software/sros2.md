---
type: tool
name: SROS2
summary: ROS 2's security tooling - the `ros2 security` CLI builds a keystore of certificates, governance and permissions so DDS-Security authenticates, encrypts and access-controls nodes; Apache-2.0, part of ros_core in every distro. rmw_zenoh reuses the same keystore through its own mTLS and access-control configs.
tags: [sros2, security, dds-security, keystore, enclave, governance, permissions, encryption, authentication, access-control, ros-security-keystore, rmw-zenoh, mtls]
kind: tool
area: ros2
support:
license: Apache-2.0
links: {repo: "https://github.com/ros2/sros2", docs: "https://docs.ros.org/en/jazzy/Tutorials/Advanced/Security/Security-Main.html", site: }
version: {tested: , latest: 0.17.1, as_of: 2026-11-25}
platforms: [linux, macos, windows]
agent_access: cli
registry:
evidence: researched
last_verified: 2026-11-25
sources:
  - {url: "https://github.com/ros2/sros2", title: "sros2 repository: README, SROS2_Linux.md, LICENSE, CHANGELOG, package.xml, keystore and policy code, issues", accessed: 2026-11-25}
  - {url: "https://design.ros2.org/articles/ros2_dds_security.html", title: "ROS 2 design: ROS 2 DDS-Security integration (2019)", accessed: 2026-11-25}
  - {url: "https://design.ros2.org/articles/ros2_security_enclaves.html", title: "ROS 2 design: ROS 2 Security Enclaves (2020)", accessed: 2026-11-25}
  - {url: "https://docs.ros.org/en/jazzy/Concepts/Intermediate/About-Security.html", title: "ROS 2 docs (Jazzy): ROS 2 Security, read from the ros2_documentation source", accessed: 2026-11-25}
  - {url: "https://docs.ros.org/en/jazzy/Tutorials/Advanced/Security/Security-Main.html", title: "ROS 2 docs (Jazzy): security tutorials - setup, access controls, network traffic, deployment guidelines; read from the ros2_documentation source", accessed: 2026-11-25}
  - {url: "https://github.com/ros2/rmw_zenoh/tree/rolling/zenoh_security_tools", title: "rmw_zenoh: zenoh_security_tools README, source and changelogs per distro branch; pull request 1007", accessed: 2026-11-25}
  - {url: "https://fast-dds.docs.eprosima.com/en/latest/fastdds/transport/datasharing.html", title: "Fast DDS docs: Data-sharing delivery", accessed: 2026-11-25}
  - {url: "https://github.com/ros/rosdistro", title: "rosdistro distribution files: humble, jazzy, kilted, lyrical, rolling", accessed: 2026-11-25}
---

# SROS2

SROS2 switches on DDS-Security for ROS 2: `ros2 security` makes a certificate authority, a
governance file and an identity and permissions per enclave [3], so nodes authenticate, encrypt
and keep to topic rules; the 2019 design article explains it [1][2]. Off until enabled [4].
Apache-2.0, by the ROS Security Working Group; tag 0.17.1 (2026-11-03); 35 open issues [1].
Released: Humble 0.10.9, Jazzy 0.13.6, Kilted 0.15.5, Lyrical 0.16.6 [8]; installs include it [5].

## When to use it

- Robots on Wi-Fi, a building LAN or a fleet network, where anyone could join the graph.
- Fast DDS and Cyclone DDS binaries carry the plugins; RTI Connext needs the licensed Connext
  Secure [1][4]. Different vendors cannot talk securely [5]. [rmw_zenoh](rmw-zenoh.md) skips
  `ROS_SECURITY_*`; its tool makes mutual-TLS, default-deny configs from the same keystore [6].

## Setup

```bash
ros2 security create_keystore ~/keystore     # apt: ros-jazzy-sros2, part of a ROS 2 install
ros2 security create_enclave ~/keystore /robot/driver
export ROS_SECURITY_KEYSTORE=~/keystore ROS_SECURITY_ENABLE=true ROS_SECURITY_STRATEGY=Enforce
ros2 run demo_nodes_cpp talker --ros-args --enclave /robot/driver
```

## How an agent works with it

- **Access control:** `ros2 security generate_policy policy.xml` records the running graph; trim it,
  then `ros2 security create_permission ~/keystore /robot/driver policy.xml`. The default policy
  allows everything [1][5]. CLI tools: set `ROS_SECURITY_ENCLAVE_OVERRIDE`, use `--no-daemon` [1].
- **Check:** a listener without the variables receives nothing; a node remapped outside its policy
  fails; tcpdump across hosts shows ciphertext (one host: Fast DDS uses shared memory) [1][5].
- **rmw_zenoh:** `ros2 run zenoh_security_tools generate_configs` turns the policy and enclaves
  into per-node and router configs, loaded via `ZENOH_SESSION_CONFIG_URI` and `_ROUTER_` [6].

## Traps

- **Permissive by default.** Without `ROS_SECURITY_STRATEGY=Enforce` a node missing its keys runs
  unsecured and hears nothing; `true` and `Enforce` are case-sensitive [2][4].
- **Domain and clock baked in.** Files cover only the `ROS_DOMAIN_ID` set at creation (default 0);
  certificates start at creation, valid ten years [1]. Regenerate after a domain change; a robot
  clock behind the signing machine's makes them not yet valid.
- **CA key on robots.** One self-signed CA signs identities and permissions [1]. Ship `public/` and
  that device's `enclaves/` only; keep `private/` off robots and images, and back it up [5].
- **Costs.** By default all traffic, discovery included, is encrypted and signed [1]; Fast DDS
  loses zero-copy data-sharing [7]; secured discovery is slower, hence `--spin-time` [5].
- **Hand-written rules.** Raw permissions use DDS names (`rt/chatter`), need rosout, parameter
  topics and `ros_discovery_info`, and must be re-signed [5]. rmw_zenoh fixed publish DENY rules
  acting as allows in Rolling (#1007, July 2026), unlisted in distro changelogs: avoid DENY [6].

## Alternatives

A VPN (WireGuard); [rmw_zenoh](rmw-zenoh.md); keystores in images: [Docker](../tools/docker.md).

## Sources

1. [sros2 repository: README, SROS2_Linux.md, LICENSE, CHANGELOG, package.xml, keystore and policy code, issues](https://github.com/ros2/sros2), accessed 2026-11-25
2. [ROS 2 design: ROS 2 DDS-Security integration (2019)](https://design.ros2.org/articles/ros2_dds_security.html), accessed 2026-11-25
3. [ROS 2 design: ROS 2 Security Enclaves (2020)](https://design.ros2.org/articles/ros2_security_enclaves.html), accessed 2026-11-25
4. [ROS 2 docs (Jazzy): ROS 2 Security, read from the ros2_documentation source](https://docs.ros.org/en/jazzy/Concepts/Intermediate/About-Security.html), accessed 2026-11-25
5. [ROS 2 docs (Jazzy): security tutorials - setup, access controls, network traffic, deployment guidelines; read from the ros2_documentation source](https://docs.ros.org/en/jazzy/Tutorials/Advanced/Security/Security-Main.html), accessed 2026-11-25
6. [rmw_zenoh: zenoh_security_tools README, source and changelogs per distro branch; pull request 1007](https://github.com/ros2/rmw_zenoh/tree/rolling/zenoh_security_tools), accessed 2026-11-25
7. [Fast DDS docs: Data-sharing delivery](https://fast-dds.docs.eprosima.com/en/latest/fastdds/transport/datasharing.html), accessed 2026-11-25
8. [rosdistro distribution files: humble, jazzy, kilted, lyrical, rolling](https://github.com/ros/rosdistro), accessed 2026-11-25

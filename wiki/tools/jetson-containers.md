---
type: tool
name: jetson-containers
summary: Modular build system and launcher for CUDA containers on NVIDIA Jetson (ROS, PyTorch, LLM and VLM servers); MIT scripts started by NVIDIA's Dustin Franklin, tested on JetPack 6.2 and 7, ROS built from source up to Jazzy; work slowed after mid-2026.
tags: [jetson, jetpack, l4t, nvidia, containers, docker, cuda, tensorrt, pytorch, ros2, autotag, orin, thor, edge-ai]
kind: tool
area: ros2
support: documented
license: MIT
links: {repo: "https://github.com/dusty-nv/jetson-containers", docs: "https://github.com/dusty-nv/jetson-containers/tree/master/docs", site: "https://www.jetson-ai-lab.com"}
version: {tested: , latest: , as_of: 2026-11-25}
platforms: [linux]
agent_access: cli
registry:
evidence: researched
last_verified: 2026-11-25
sources:
  - {url: "https://github.com/dusty-nv/jetson-containers", title: "jetson-containers repository: README, LICENSE.md, CITATION.cff, run.sh, commit history, issues", accessed: 2026-11-25}
  - {url: "https://github.com/dusty-nv/jetson-containers/tree/master/docs", title: "jetson-containers docs: system setup, building and running containers", accessed: 2026-11-25}
  - {url: "https://github.com/dusty-nv/jetson-containers/tree/master/jetson_containers", title: "jetson-containers build code: l4t_version.py and container.py", accessed: 2026-11-25}
  - {url: "https://github.com/dusty-nv/jetson-containers/tree/master/packages/physicalAI/ros", title: "jetson-containers ROS package: README and version.py", accessed: 2026-11-25}
  - {url: "https://github.com/dusty-nv/jetson-containers/issues/1736", title: "jetson-containers issue 1736: JetPack 7.2 / CUDA 13.2 Orin build issues", accessed: 2026-11-25}
  - {url: "https://developer.nvidia.com/embedded/jetpack-archive", title: NVIDIA JetPack archive, accessed: 2026-11-25}
  - {url: "https://catalog.ngc.nvidia.com/orgs/nvidia/containers/l4t-jetpack", title: "NGC catalog: l4t-jetpack container", accessed: 2026-11-25}
  - {url: "https://nvidia-isaac-ros.github.io/getting_started/index.html", title: "Isaac ROS docs: Getting started", accessed: 2026-11-25}
---

# jetson-containers

A build system that chains package Dockerfiles into CUDA images for NVIDIA Jetson, plus a launcher
with Jetson defaults; packages include ROS, PyTorch, vLLM, Ollama and VLMs [1]. Builders use it for
GPU-ready ML beside ROS 2. MIT, copyright NVIDIA; author Dustin Franklin (NVIDIA) last committed
2025-05-31. No releases; last code change 2026-06-25, last commit 2026-10-13; 189 open issues [1].

## When to use it

- ML beside ROS 2 on Orin or Thor; only JetPack 6.2 (CUDA 12.6) and 7 (CUDA 13) are tested [1].
- Its ROS images build ROS from source, up to Jazzy, with no Kilted or Lyrical; the README lists
  prebuilt Jazzy images only for L4T r36.4.0, Ubuntu 24.04 (2025-03-03, 5.1 GB `ros-base`) [4].
- For Isaac ROS its docs point to NVIDIA's environment (below) [4]; x86 builds are unsupported [2].

## Setup

NVIDIA ships JetPack 6.2.x (L4T 36.4.3 to 36.5.2) for Orin, 7.0 and 7.1 (L4T 38.x) for Thor only,
and 7.2.x (L4T 39.2.x) for both [6]; Orin on 7.2 needs CUDA 13.2 and driver R595 or newer [1].

```bash
git clone https://github.com/dusty-nv/jetson-containers
bash jetson-containers/install.sh                 # puts jetson-containers and autotag on PATH
jetson-containers run $(autotag l4t-pytorch)      # local image, else Docker Hub, else build
LSB_RELEASE=24.04 jetson-containers build --name=my_robot pytorch ros:jazzy-ros-base
```

JetPack 6 builds default to `ubuntu:22.04`, hence `LSB_RELEASE` [2]. For builds set
`"default-runtime": "nvidia"` in `/etc/docker/daemon.json`, move Docker's `data-root` to NVMe and
add swap; `--simulate` prints the docker commands [2]. `run` adds `--runtime nvidia`,
`--network host`, `--shm-size=8g`, a `/data` cache and camera, audio, USB and I2C devices [1][2].
Check: `python3 -c "import torch; print(torch.cuda.is_available())"` prints True.

## Traps

- **Wrong L4T image.** `autotag` takes the newest local image with no L4T check; on L4T 38
  or 39 hosts it takes registry images for any L4T [3]. Pin full tags; see `/etc/nv_tegra_release`.
- **JetPack 7.2 on Orin.** Its version table ends at L4T 39.1.0, but 7.2 is 39.2.x [3][6]; Orin
  builds fail on pip wheels and ffmpeg, and issue 1736 has no maintainer reply since 2026-08 [5].
- **ROS packages from apt.** ROS sits in `/opt/ros` as a source build, so `ros-jazzy-*` debs do
  not fit it; build add-ons with `/ros2_install.sh <package or git URL>` [4].
- **Root and a private IPC namespace.** `run` runs as root and mounts `/var/run/docker.sock` [1][2].
  `DOCKER_USER=1000:1000` adds the GPU device groups, but CSI cameras through Argus need root [2].
  It sets no `--ipc host`; add it for Fast DDS shared memory with host nodes ([Docker](docker.md)).
- **Licences beyond MIT.** MIT covers the scripts, not the CUDA, cuDNN and TensorRT that JetPack 6
  and 7 builds install on plain Ubuntu [2]. Pulling NVIDIA's `l4t-jetpack` base accepts the JetPack
  EULA; its newest tag is r36.4.0 (2024-11-07) [7]. Read NVIDIA's terms before shipping images.

## Alternatives

**Isaac ROS CLI**: NVIDIA's packages for ROS 2 Lyrical on Ubuntu 24.04 and JetPack 7.2 (Thor and
Orin), in Docker (recommended), a venv or bare metal [8]. **NGC** images such as `l4t-jetpack` [7].
Plain [Docker](docker.md) with the arm64 `ros` images, which carry no CUDA.

## Sources

1. [jetson-containers repository: README, LICENSE.md, CITATION.cff, run.sh, commit history, issues](https://github.com/dusty-nv/jetson-containers), accessed 2026-11-25
2. [jetson-containers docs: system setup, building and running containers](https://github.com/dusty-nv/jetson-containers/tree/master/docs), accessed 2026-11-25
3. [jetson-containers build code: l4t_version.py and container.py](https://github.com/dusty-nv/jetson-containers/tree/master/jetson_containers), accessed 2026-11-25
4. [jetson-containers ROS package: README and version.py](https://github.com/dusty-nv/jetson-containers/tree/master/packages/physicalAI/ros), accessed 2026-11-25
5. [jetson-containers issue 1736: JetPack 7.2 / CUDA 13.2 Orin build issues](https://github.com/dusty-nv/jetson-containers/issues/1736), accessed 2026-11-25
6. [NVIDIA JetPack archive](https://developer.nvidia.com/embedded/jetpack-archive), accessed 2026-11-25
7. [NGC catalog: l4t-jetpack container](https://catalog.ngc.nvidia.com/orgs/nvidia/containers/l4t-jetpack), accessed 2026-11-25
8. [Isaac ROS docs: Getting started](https://nvidia-isaac-ros.github.io/getting_started/index.html), accessed 2026-11-25

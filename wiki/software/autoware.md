---
type: tool
name: Autoware
summary: The Autoware Foundation's Apache-2.0 self-driving stack on ROS 2 for cars, shuttles and delivery vehicles; 2.1.0 supports Humble and Jazzy, installs from source with Ansible or as Docker images, and only Autoware Core has apt packages. Far too heavy for a small indoor robot, where Nav2 fits.
tags: [self-driving, autonomous-vehicle, ros2, lanelet2, ndt, point-cloud-map, planning, perception, cuda, tensorrt, docker, ansible]
kind: framework
area: nav
support:
license: Apache-2.0
links: {repo: "https://github.com/autowarefoundation/autoware", docs: "https://docs.autoware.org/main/home/", site: "https://www.autoware.org/"}
version: {tested: , latest: 2.1.0, as_of: 2026-11-24}
platforms: [linux]
agent_access: cli
registry:
evidence: researched
last_verified: 2026-11-24
sources:
  - {url: "https://github.com/autowarefoundation/autoware", title: "Autoware repository: README, LICENSE, DISCLAIMER, repositories/autoware.repos, ansible roles, docker/README.md, tags; autoware_core and autoware_universe LICENSE files", accessed: 2026-11-24}
  - {url: "https://github.com/autowarefoundation/autoware/releases", title: "Autoware release notes: 2.0.0 and 2.1.0", accessed: 2026-11-24}
  - {url: "https://docs.autoware.org/main/installation/", title: "Autoware docs: Installation", accessed: 2026-11-24}
  - {url: "https://docs.autoware.org/main/installation/autoware/source-installation/", title: "Autoware docs: Source installation", accessed: 2026-11-24}
  - {url: "https://docs.autoware.org/main/installation/autoware/docker-installation/", title: "Autoware docs: Docker installation", accessed: 2026-11-24}
  - {url: "https://github.com/ros/rosdistro", title: "rosdistro distribution files: humble, jazzy, kilted, lyrical, rolling", accessed: 2026-11-24}
  - {url: "https://huggingface.co/AutowareFoundation", title: "AutowareFoundation on Hugging Face: model repositories and licence tags", accessed: 2026-11-24}
  - {url: "https://gitlab.com/autowarefoundation/autoware.auto/AutowareAuto", title: "Autoware.Auto repository on GitLab: README and last commit", accessed: 2026-11-24}
---

# Autoware

The Autoware Foundation's self-driving software on ROS 2: NDT localization, lidar, camera and
radar perception, Lanelet2 lane planning and drive-by-wire control for robo-taxis, shuttles and
cars [1]. Apache-2.0; 2.1.0 published 2026-11-10, last commit 2026-11-21 [1][2]. Autoware.Auto,
the older GitLab rewrite, is frozen: work moved to GitHub in 2022; last commit 2023-03-02 [8].

## When to use it

- **Use it** for a car-sized vehicle with drive-by-wire, 3D lidar, cameras and GNSS, in an area
  you can map into a point cloud and a Lanelet2 map [1]. Learn it in its planning or scenario
  simulation [1] or [CARLA](../tools/carla.md) (role added in 2.1.0) [2].
- **Not for** a small indoor or differential-drive robot: it assumes lanes, a car's sensors and an
  8-core, 16 GB computer [1][3]. Use [Nav2](nav2.md) and [SLAM Toolbox](slam-toolbox.md).

## Setup

2.1.0 supports Ubuntu 22.04 with Humble and 24.04 with Jazzy, amd64 and arm64, 8+ cores, 16 GB
RAM [2][3]. A 4 GB NVIDIA GPU is optional, but lidar and camera detection and traffic lights need
one [3]. **Docker:** pull `ghcr.io/autowarefoundation/autoware:universe-cuda-jazzy-2.1.0` (or
`universe-jazzy-2.1.0`; CUDA images need driver 580+ on Jazzy), run it as `docker/README.md` shows,
then `ros2 launch autoware_launch autoware.launch.xml` [1][5]. **Source** [4]:

```bash
git clone https://github.com/autowarefoundation/autoware.git && cd autoware && git checkout 2.1.0
bash ansible/scripts/install-ansible.sh && source ~/.bashrc
ansible-galaxy collection install -f -r ansible-galaxy-requirements.yaml
ansible-playbook autoware.dev_env.install_dev_env --ask-become-pass   # --skip-tags nvidia: no GPU
mkdir -p src && vcs import src < repositories/autoware.repos
source /opt/ros/jazzy/setup.bash && rosdep install -y --from-paths src --ignore-src
colcon build --symlink-install --cmake-args -DCMAKE_BUILD_TYPE=Release
```

The playbook installs CUDA 13.0 and TensorRT 10.13 on Jazzy and stops on other Ubuntu versions
[4]. Only Autoware Core has binaries: `ros-jazzy-autoware-core` 1.9.0, Humble and Jazzy only [3][6].

## Traps

- **apt Core lags.** It is 1.9.0 while 2.1.0 pins `autoware_core` 1.10.0 [2][6]; do not mix apt
  Core with a source Universe.
- **No GPU, no detection.** Built with `--skip-tags nvidia` or from a non-CUDA image, it runs, but
  lidar and camera detection and traffic lights do not [3][4].
- **Licences beyond Apache-2.0.** CUDA, cuDNN and TensorRT carry NVIDIA licences, the CUDA images
  NVIDIA's Deep Learning Container licence [4][5]. Most Hugging Face models are tagged Apache-2.0,
  but `auto_e2e` is CC BY-NC-SA 4.0, non-commercial [7]. The DISCLAIMER gives no warranty [1].
- **Releases break workspaces.** 2.0.0 moved models to per-variant folders (download them again
  with the `artifacts` tag), and 2.1.0 moved CUDA packages to `autoware_cuda`, so colcon fails on
  duplicates until the old copies go [2]. Take models from a release tag, not `main` [1].

## Alternatives

[Nav2](nav2.md) for robots smaller than a car; Baidu Apollo and openpilot outside ROS 2.

## Sources

1. [Autoware repository: README, LICENSE, DISCLAIMER, repositories/autoware.repos, ansible roles, docker/README.md, tags; autoware_core and autoware_universe LICENSE files](https://github.com/autowarefoundation/autoware), accessed 2026-11-24
2. [Autoware release notes: 2.0.0 and 2.1.0](https://github.com/autowarefoundation/autoware/releases), accessed 2026-11-24
3. [Autoware docs: Installation](https://docs.autoware.org/main/installation/), accessed 2026-11-24
4. [Autoware docs: Source installation](https://docs.autoware.org/main/installation/autoware/source-installation/), accessed 2026-11-24
5. [Autoware docs: Docker installation](https://docs.autoware.org/main/installation/autoware/docker-installation/), accessed 2026-11-24
6. [rosdistro distribution files: humble, jazzy, kilted, lyrical, rolling](https://github.com/ros/rosdistro), accessed 2026-11-24
7. [AutowareFoundation on Hugging Face: model repositories and licence tags](https://huggingface.co/AutowareFoundation), accessed 2026-11-24
8. [Autoware.Auto repository on GitLab: README and last commit](https://gitlab.com/autowarefoundation/autoware.auto/AutowareAuto), accessed 2026-11-24

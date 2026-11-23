---
type: tool
name: CloudCompare
summary: GPL desktop application for inspecting, aligning, comparing and cleaning point clouds and meshes, with a command-line mode for batch runs; builders use it to check a SLAM map against a reference scan and to clean maps.
tags: [cloudcompare, point-cloud, mesh, c2c-distance, c2m-distance, icp, registration, map-cleaning, slam-evaluation, lidar, las, ply, pcd, gui]
kind: tool
area: perception
support: documented
license: GPL-2.0-or-later
links: {repo: "https://github.com/CloudCompare/CloudCompare", docs: "https://www.cloudcompare.org/doc/wiki/index.php/Main_Page", site: "https://www.cloudcompare.org"}
version: {tested: , latest: 2.13.2, as_of: 2026-11-23}
platforms: [linux, windows, macos]
agent_access: cli
registry:
evidence: researched
last_verified: 2026-11-23
sources:
  - {url: "https://github.com/CloudCompare/CloudCompare", title: "CloudCompare repository: README, license.txt, CHANGELOG, BUILD.md, qCC command-line sources, plugin CMake options (master)", accessed: 2026-11-23}
  - {url: "https://github.com/CloudCompare/CCCoreLib", title: "CCCoreLib repository: README, LICENSE.txt and CCTypes.h", accessed: 2026-11-23}
  - {url: "https://www.cloudcompare.org/release/index.html", title: "CloudCompare downloads (stable and beta)", accessed: 2026-11-23}
  - {url: "https://www.cloudcompare.org/doc/wiki/index.php/Command_line_mode", title: "CloudCompare wiki: Command line mode", accessed: 2026-11-23}
  - {url: "https://www.cloudcompare.org/doc/wiki/index.php/Cloud-to-Cloud_Distance", title: "CloudCompare wiki: Cloud-to-Cloud distance", accessed: 2026-11-23}
  - {url: "https://packages.ubuntu.com/search?keywords=cloudcompare&searchon=names&suite=all&section=all", title: "Ubuntu packages: cloudcompare", accessed: 2026-11-23}
---

# CloudCompare

A desktop application for 3D point clouds and triangle meshes, built around an octree for
comparing two clouds, or a cloud and a mesh, and for clouds of many millions of points [1].
Builders use it to check a SLAM map against a reference scan or an earlier run, to clean a map
before localization, and to convert formats. The application is GPL-2.0-or-later [1].

## When to use it

By hand or in batch: crop, subsample, remove outliers, align with ICP, and measure cloud-to-cloud
(C2C) or cloud-to-mesh distances [4]. Not for live topics (RViz, [Foxglove](foxglove.md),
[Rerun](rerun.md)); in code, use [Open3D](../software/open3d.md) or [PCL](../software/pcl.md).

## Setup

Stable **2.13.2** dates from mid-2024; the maintained line is the 2.14 beta, updated
21 November 2026, with commits the same day [1][3].

- **Linux:** `flatpak install flathub org.cloudcompare.CloudCompare` [1][3]. Ubuntu 24.04's apt
  `cloudcompare` is 2.11.3, from 2020; 26.04 has a 2.13.2 snapshot [6].
- **Windows:** installer or 7z for 2.13.2 and the beta. **macOS:** third-party builds (Paul
  Rascle); the 2.14 alpha needs macOS 13+ on arm64 [3]. **Source:** CMake, Qt 6 on 24.04 [1].

## How an agent works with it

Commands run in order: `-SILENT` first, `-O` loads files, `-AUTO_SAVE OFF` plus `-SAVE_CLOUDS`
controls output, `-NO_TIMESTAMP` keeps names (and overwrites) [4]:

```bash
CloudCompare -SILENT -AUTO_SAVE OFF -NO_TIMESTAMP -C_EXPORT_FMT PLY \
  -O map.ply -SS SPATIAL 0.05 -SOR 8 1.0 -SAVE_CLOUDS        # clean: 5 cm subsample, outliers
CloudCompare -SILENT -AUTO_SAVE OFF -C_EXPORT_FMT PLY -O slam_map.ply \
  -O reference.ply -ICP -C2C_DIST -MAX_DIST 0.5 -SAVE_CLOUDS  # align, then C2C to reference
```

C2C stores a distance field on the first (compared) cloud; `-ICP` writes its matrix to a text
file [4]. In the GUI, the histogram shows overall fit; bright patches show drift or ghosts.
Procedures: [perception-slam](../../skills/perception-slam/SKILL.md).

## Traps

- **C2C is nearest-neighbour distance**, not true surface distance: make the densest, widest
  cloud the reference, and use a local model when it is sparse [5]. Align roughly before ICP.
- **PCD may not open:** it needs the qPCL plugin, off by default in source builds [1]; convert
  with `pcl_pcd2ply` from [PCL](../software/pcl.md)'s `pcl-tools` or check your build's plugins.
- **Licence:** GPL-2.0-or-later; "This code cannot be used in a closed source software" [1].
  CCCoreLib and `qCC_db` are LGPL-2.0-or-later [1][2]. Running the tool is unrestricted.
- **Headless servers:** even `-SILENT` creates the Qt application [1], so a machine without a
  display may need a virtual one such as `xvfb-run` (not tested here).
- **Large coordinates:** points are 32-bit floats [2], so georeferenced (UTM) maps lose
  precision; load with `-O -GLOBAL_SHIFT AUTO map.ply`, or accept the GUI's shift [4].

## Alternatives

Code: [Open3D](../software/open3d.md), [PCL](../software/pcl.md); CloudComPy (third-party Python
bindings) and MeshLab not reviewed. [Choose a SLAM system](../guides/choose-a-slam-system.md).

## Sources

1. [CloudCompare repository: README, license.txt, CHANGELOG, BUILD.md, qCC command-line sources, plugin CMake options (master)](https://github.com/CloudCompare/CloudCompare), accessed 2026-11-23
2. [CCCoreLib repository: README, LICENSE.txt and CCTypes.h](https://github.com/CloudCompare/CCCoreLib), accessed 2026-11-23
3. [CloudCompare downloads (stable and beta)](https://www.cloudcompare.org/release/index.html), accessed 2026-11-23
4. [CloudCompare wiki: Command line mode](https://www.cloudcompare.org/doc/wiki/index.php/Command_line_mode), accessed 2026-11-23
5. [CloudCompare wiki: Cloud-to-Cloud distance](https://www.cloudcompare.org/doc/wiki/index.php/Cloud-to-Cloud_Distance), accessed 2026-11-23
6. [Ubuntu packages: cloudcompare](https://packages.ubuntu.com/search?keywords=cloudcompare&searchon=names&suite=all&section=all), accessed 2026-11-23

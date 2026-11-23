---
type: source
name: Awesome Robotics Datasets
registry: awesome-robotics-datasets
url: https://github.com/mint-lab/awesome-robotics-datasets
commit: "9178fbf"
read_on: 2026-11-18
counts: {entries: 77, pages: 2, waiting: 0, index_only: 52, deferred: 0, rejected: 23}
---

# Awesome Robotics Datasets: what it gives RoboAI

A 2021 list of datasets for robotics and computer vision, grouped by place (driving, flying,
underwater, outdoor, indoor), by topic (SLAM, planning, features, tracking, recognition) and by
research group. Most entries are driving or general vision benchmarks that serve perception
research more than robot building, and 21 of its links are dead five years on. For RoboAI it gives
two SLAM benchmark pages, KITTI and TUM RGB-D, and a reference index of older datasets. It has
none of today's robot-learning datasets (Open X-Embodiment, DROID) or newer SLAM sets (EuRoC,
Newer College, Hilti).

## How it was read

- Read at commit `9178fbf` (2021-08-27) on 2026-11-18: the whole README, 77 entries counting
  every linked line and sub-item. KITTI and KITTI-360 share one line, so they share one row. The
  repo has no licence file.
- Every link was requested once on 2026-11-18, following redirects, and failures were tried a
  second time with a longer timeout. Rejected as dead: hosts that no longer resolve or answer,
  pages that return 404 or a 5xx error, and pages that now redirect to a login screen or a site's
  home page. The list itself already marks Radish as not working.
- **Moved but alive:** KAIST Complex Urban (now on Google Sites), Blackbird (`mit-aera`
  organisation), TUM CVG (cvg.cit.tum.de), the ATR mall data (dil.atr.jp), ChangeDetection.NET
  (loads without `www`), Roh's dataset (`mint-lab` organisation), and BDD100K, whose HTTPS
  certificate has expired while the plain HTTP site still loads.
- **Page candidates** were checked for download and use. KITTI: files on its `avg-kitti` S3
  bucket answer (the odometry calibration and a raw drive, dated 2018; checked with HEAD requests,
  nothing downloaded); licence CC-BY-NC-SA-3.0, so non-commercial; site changelog last updated
  2021-02-25; 2026 lidar-odometry papers still report KITTI results (for example arXiv
  2503.21293, revised March 2026). TUM RGB-D: the `freiburg1_xyz` sequence answers from
  webshare.cvg.cit.tum.de; data under CC-BY-4.0 and tools under BSD-2-Clause; the group page
  has news from June 2026; RTAB-Map's 2024 paper (arXiv 2403.06341) evaluates on it.
- **Batch:** both dataset pages go in `learning/` but are SLAM benchmarks, so the perception batch
  writes them.
- No section holds only papers. Nothing suspicious, and no prompt-like text, in the README.

## Pages made

| Entry | Page | Tier |
|---|---|---|
| KITTI Vision Benchmark Suite and KITTI-360 | [KITTI and KITTI-360](../wiki/learning/datasets/kitti.md) | B |
| TUM CVG Datasets | [TUM RGB-D](../wiki/learning/datasets/tum-rgbd.md) | B |

## Waiting for a page

| Entry | Page | Tier | Batch | Why it matters |
|---|---|---|---|---|

## Index only

| Entry | What it is | Last commit | Licence |
|---|---|---|---|
| Repository of Robotics and Computer Vision Datasets (MRPT) | MRPT's index of classic datasets, including the Malaga sets | — | — |
| IJRR Data Papers | IJRR's collection of robotics dataset papers | — | — |
| Awesome SLAM Datasets | Curated list of SLAM datasets by sensor and platform | — | — |
| CVonline Image Databases | Large index of computer vision image datasets | — | — |
| Computer Vision Datasets on the Web (CVPapers) | Index of computer vision datasets | — | — |
| Machine Learning Repository (UCI) | General machine learning dataset archive, little robotics | — | — |
| Kaggle Datasets | General dataset hosting site | — | — |
| IEEE DataPort | IEEE's general dataset hosting site | — | — |
| SemanticKITTI | Point-wise semantic labels for the KITTI odometry lidar scans | — | — |
| Waymo Open Dataset | Large lidar and camera driving dataset with yearly challenges | — | — |
| Cityscapes Dataset | Urban street-scene semantic segmentation benchmark | — | — |
| ApolloScape Dataset | Baidu driving dataset for segmentation, lanes and trajectories | — | — |
| Berkeley DeepDrive Dataset (BDD100K) | 100,000 driving videos with detection and lane labels | — | — |
| nuScenes Dataset | Multi-sensor driving dataset with radar; a 3D detection standard | — | — |
| KAIST Multi-spectral Recognition Dataset in Day and Night | Paired colour and thermal driving images, day and night | — | — |
| KAIST Complex Urban Dataset | Urban lidar and camera SLAM dataset from Korean cities | — | — |
| CULane Dataset | Lane-detection benchmark from Beijing road video | — | — |
| ROMA (ROad MArkings) Image Database | Small road-marking image set | — | — |
| The Zurich Urban Micro Aerial Vehicle Dataset | Low-altitude drone camera, IMU and GPS over Zurich streets | — | — |
| The UZH-FPV Drone Racing Dataset | Aggressive drone-racing visual-inertial odometry benchmark | — | — |
| The Blackbird Dataset | MIT high-speed quadrotor flights with rendered camera images | — | — |
| Marine Robotics Datasets (ACFR) | Underwater vehicle seafloor survey data from Sydney | — | — |
| The Rawseeds Project | 2009 multi-sensor indoor and outdoor SLAM benchmark | — | — |
| Planetary Mapping and Navigation Datasets | Toronto planetary-analogue rover navigation data | — | — |
| Robotics 2D-Laser Datasets | Classic pre-2014 2D laser SLAM logs | — | — |
| Long-Term Mobile Robot Operations | Lincoln long-term indoor mobile-robot logs | — | — |
| MIT Stata Center Data Set | Long-term indoor RGB-D, laser and odometry logs | — | — |
| Shopping Mall Datasets | Pedestrian tracks from laser scanners in a Japanese mall | — | — |
| RGB-D Dataset 7-Scenes | Microsoft RGB-D camera relocalisation benchmark | — | — |
| SLAM Benchmarking | Freiburg metric and data for comparing SLAM results | — | — |
| Robotic 3D Scan Repository | 3D laser scans for registration and mapping | — | — |
| 3D Pose Graph Optimization | Standard pose-graph files for testing SLAM back ends | — | — |
| Pathfinding Benchmarks | Grid-map pathfinding and multi-agent pathfinding benchmark sets | — | — |
| Task and Motion Planner Benchmarking | 2018 RSS workshop's task-and-motion planning problems | — | — |
| Affine Covariant Features Datasets | Oxford image pairs for feature-detector repeatability | — | — |
| A list of feature performance evaluation datasets (openMVG) | openMVG's list of feature evaluation datasets | — | — |
| MIT Saliency Benchmark | Human-fixation saliency benchmark, not robotics | — | — |
| Salient Object Detection: A Benchmark | Salient object detection benchmark, not robotics | — | — |
| ChangeDetection.NET | Video background-subtraction benchmark | — | — |
| Fuji-SfM Dataset | Apple-orchard images and 3D models for structure from motion | — | — |
| Large Geometric Models Archive | Georgia Tech archive of classic 3D meshes | — | — |
| The Stanford 3D Scanning Repository | Classic scanned meshes such as the bunny and dragon | — | — |
| Photo Tourism Data | Internet photo collections behind early large-scale structure from motion | — | — |
| Visual Object Tracking Challenge (VOT) | Yearly single-object visual tracking challenge | — | — |
| Daimler Pedestrian Benchmark Data Sets | Classic pedestrian detection benchmarks | — | — |
| CrowdHuman | Crowded-scene person detection benchmark | — | — |
| RGB-D Object Dataset | 300 household objects captured in RGB-D | — | — |
| VIRAT Video Dataset | Surveillance video for human activity recognition | — | — |
| Oxford VGG Datasets | Oxford VGG datasets for features, recognition and 3D | — | — |
| Univ. of Bonn Stachniss Lab Datasets | Stachniss lab data, including recent lidar datasets | — | — |
| EPFL CVLAB Datasets | EPFL vision datasets for 3D, keypoints and optical flow | — | — |
| The Middlebury Computer Vision Pages | Stereo and optical-flow benchmarks | — | — |

## Deferred

| Entry | What it is | Phase |
|---|---|---|

## Rejected

| Entry | Why | Date |
|---|---|---|
| Radish: The Robotics Data Set Repository | Dead link: the list itself marks it as not working | 2026-11-18 |
| YACVID: Yet Another Computer Vision Index To Datasets | Dead link: returns 404 | 2026-11-18 |
| Computer Vision Online Datasets | Dead link: returns 404 | 2026-11-18 |
| D²-City Dataset | Dead link: DiDi's page returns 404 | 2026-11-18 |
| Ford Campus Vision and Lidar Data Set | Dead link: the page now redirects to a login screen | 2026-11-18 |
| MIT DARPA Urban Challenge Dataset | Dead link: the wiki returns 403 Forbidden | 2026-11-18 |
| New College Dataset | Dead link: returns 404 | 2026-11-18 |
| Chinese Driving from a Bike View (CDBV) | Dead link: the host no longer resolves | 2026-11-18 |
| MultiDrone Public Dataset | Dead link: returns 404 | 2026-11-18 |
| KTH and COLD Database | Dead link: the site returns a server error | 2026-11-18 |
| Range-only Data for Localization | Dead link: redirects to the CMU Field Robotics Center home page | 2026-11-18 |
| Roh's Angulation Dataset | Too thin: a small test set inside a MATLAB triangulation toolbox | 2026-11-18 |
| Wireless Sensor Network Dataset | Dead link: the server does not answer | 2026-11-18 |
| Repeatability Benchmark Tutorial (VLFeat) | Too thin: a tutorial page for the Oxford features entry | 2026-11-18 |
| AdelaideRMF: Robust Model Fitting Data Set | Dead link: returns 404 | 2026-11-18 |
| IVL-SYNTHESFM v2 | Dead link: returns HTTP 500 | 2026-11-18 |
| Visual Tracker Benchmark (OTB) | Dead link: returns 404 | 2026-11-18 |
| EuroCity Persons Dataset | Dead link: the server does not answer | 2026-11-18 |
| Sweet Pepper and Peduncle 3D Datasets | Dead link: the site returns a server error | 2026-11-18 |
| Loop Closure Detection | Dead link: the host no longer resolves | 2026-11-18 |
| BEST: Benchmark and Evaluation of Surveillance Task | Dead link: the host no longer resolves | 2026-11-18 |
| QUT CyPhy Datasets | Dead link: the wiki now requires a QUT login | 2026-11-18 |
| Caltech CVG Datasets | Dead link: the archive page returns 404 | 2026-11-18 |

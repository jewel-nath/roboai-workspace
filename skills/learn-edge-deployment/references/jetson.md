# Jetson: power modes, clocks, thermals and containers

Part of [learn-edge-deployment](../SKILL.md). From the Jetson Linux developer guides (Orin: r36.4.3 "Platform
Power and Performance"; Thor: r38.4, and its Tegrastats Utility page), `rbonghi/jetson_stats` (7.3.0,
commit ccc4094), the Isaac ROS 4.6 docs and the [jetson-containers](../../../wiki/tools/jetson-containers.md)
page; read 2026-11-25, not run. Check the guide for your own L4T release: modes change between releases.

## Power modes (`nvpmodel`)

```bash
sudo nvpmodel -q --verbose        # current mode, name and settings
sudo nvpmodel -m <id>             # switch; persists across reboots
grep -n "POWER_MODEL" /etc/nvpmodel.conf   # the IDs and names this board really has
```

Mode IDs are per module, so `-m 0` means different things:

| Module | IDs and names (default in bold) |
|---|---|
| Orin Nano 8GB | 0 15W (**default**), 1 7W; with the Super flash configuration: 0 15W, 1 25W (**default**), 2 MAXN_SUPER |
| Orin Nano 4GB | 0 10W (**default**), 1 7W_AI, 2 7W_CPU; Super: 0 10W, 1 25W (**default**), 2 MAXN_SUPER |
| Orin NX 16GB | 0 MAXN, 1 10W, 2 15W (**default**), 3 25W; Super: 0 MAXN_SUPER, 1 10W, 2 15W, 3 25W, 4 40W (**default**) |
| Orin NX 8GB | 0 MAXN, 1 10W, 2 15W (**default**), 3 20W; Super: 0 MAXN_SUPER, 1 10W, 2 15W, 3 20W, 4 40W (**default**) |
| AGX Orin 32GB | 0 MAXN, 1 15W, 2 30W (**default**), 3 40W |
| AGX Orin 64GB | 0 MAXN, 1 15W, 2 30W (**default**), 3 50W |
| Thor T5000 | 0 MAXN (experimental, not for prolonged heavy load), 1 120W (**default**), 2 90W, 3 70W |
| Thor T4000 | 0 MAXN (experimental), 1 70W (**default**) |

Orin rows are from r36.4.3 (JetPack 6.2); MAXN_SUPER exists only when the board was flashed with the Super
configuration. Thor rows are from r38.4. JetPack 7.2 adds AGX Orin 32GB Super mode (r39.2 release notes), so
read `/etc/nvpmodel.conf` on 7.2 boards rather than this table.

- A mode switch rarely needs a reboot; when it does, `nvpmodel` warns and asks.
- Pick the mode for the robot's power supply and cooling, then test it hot ([below](#thermals)). A mode the
  battery or the enclosure cannot sustain gives the best benchmark and the worst robot.
- Custom modes go into `/etc/nvpmodel.conf` with a new ID and `NAME`; NVIDIA's Power Estimator
  (jetson-tools.nvidia.com/powerestimator) can generate one.

## Fixed clocks (`jetson_clocks`)

```bash
sudo jetson_clocks --show         # current CPU, GPU and memory clocks
sudo jetson_clocks --store        # save the current settings (default ~/.jetsonclocks_conf.txt)
sudo jetson_clocks                # pin CPU, GPU and EMC clocks to the mode's maximum
sudo jetson_clocks --restore      # back to the stored settings
sudo jetson_clocks --fan          # fan at maximum PWM
```

- `jetson_clocks` removes frequency scaling inside the current mode: less latency spread, more power and heat.
  Set the mode first, then `jetson_clocks`; after changing modes, run it again.
- If the deployed robot runs with it, start it from a systemd unit before the inference node
  ([ops-bringup](../../ops-bringup/references/systemd.md)) and benchmark with it on; if not, benchmark without it.
  Published Jetson numbers are usually taken at MAXN with `jetson_clocks` on (GR00T's are), which a robot on
  battery may never run.

## tegrastats

```bash
sudo tegrastats --interval 1000 --logfile /var/log/my_robot/tegrastats.log &   # one line per second
sudo tegrastats --stop
```

| Field | Example | Meaning |
|---|---|---|
| `RAM` | `RAM 220/38955MB (lfb 847x4MB)` | Used / total MB (CPU and GPU share it); `lfb` largest free block, shrinks as memory fragments |
| `SWAP` | `SWAP 0/1978MB (cached 0MB)` | Swap in use: on a robot it should stay near zero |
| `CPU` | `CPU [1%@102,5%@102,...]` | Load and MHz per core; `off` for a core powered down |
| `EMC_FREQ` | `EMC_FREQ 95%@1600` | Memory bandwidth used and its clock |
| `GR3D_FREQ` | `GR3D_FREQ 99%@[1098,1098,1098]` | GPU load and per-GPC MHz (AGX Orin two GPCs, Thor three) |
| temperatures | `MCPU@45C` | Per thermal zone, °C |
| power rails | `VDD_GPU 10687mW/9815mW` | Instant / average mW |

A GPU or CPU clock that falls during a long run while load stays high is throttling. Keep the log of every
latency test with the test ([latency.md](latency.md#report)).

`jtop` (`jetson-stats` 7.3.0, AGPL-3.0) shows the same data interactively and supports Thor; on Ubuntu 24.04 its
README installs it with `sudo pip3 install --break-system-packages -U jetson-stats` or an install script.
It is optional: `tegrastats` ships with JetPack and logs to a file.

## Thermals

- When the module reaches its power or over-current limits, hardware throttles CPU and GPU clocks (the Thor
  guide gives 50 % or 75 % depending on the level). Do not relax the sysfs current or power limits to avoid it:
  the guide warns this can damage the module.
- Fan profiles: `sudo nvfancontrol -q` shows the active one; `FAN_DEFAULT_PROFILE` in `/etc/nvfancontrol.conf`
  sets it (Thor's default is `cool`). To change it: stop the `nvfancontrol` service, edit the file, delete
  `/var/lib/nvfancontrol/status`, start the service.
- **Test in the real enclosure at the hottest expected ambient**, with the full stack and the deployed mode,
  for at least as long as the robot works between pauses. Compare minute one with minute ten in `~/timing`
  and `tegrastats`. A developer kit on a desk proves nothing about a sealed robot body.

## Containers

- **jetson-containers**: images per L4T release with CUDA, TensorRT, PyTorch and ROS (built from source; Jazzy
  on JetPack 6 needs `LSB_RELEASE=24.04`). Pin full image tags, since `autotag` can pick an image for another
  L4T. Details and traps on the [wiki page](../../../wiki/tools/jetson-containers.md).
- **Isaac ROS 4.6**: `isaac-ros init docker` gives NVIDIA's Jazzy environment on JetPack 7.2
  ([ros2-node.md](ros2-node.md#isaac-ros-46-tensorrt-node-jazzy)).
- **Plain `ros:jazzy` arm64 images** run on a Jetson but carry no CUDA or TensorRT
  ([ops-docker-ci](../../ops-docker-ci/references/gpu-display.md#jetson)).
- Run with `--runtime nvidia` (or `"default-runtime": "nvidia"` in `/etc/docker/daemon.json`) so the GPU is
  visible inside.
- **Engines and containers**: the engine is tied to the TensorRT inside the image and to the module. Build it in
  the container on the robot at first start (or during install), store it with the timing cache on a mounted
  volume (`/var/cache/my_robot/trt`), and key the file name by model hash and TensorRT version so an image
  update triggers a rebuild instead of a load failure.
- Images that contain CUDA, cuDNN or TensorRT, or NVIDIA's `l4t-jetpack` base, carry NVIDIA's licence terms;
  read them before publishing images.

## Upgrades

- Upgrade JetPack on a bench robot first. JetPack 7.2.1 to 7.2.2 (`apt dist-upgrade`) moves TensorRT from
  10.16.2 to 11.4.1: `--fp16` and `--int8` disappear, engines must be rebuilt (unless built version-compatible), and an ONNX Runtime TensorRT EP
  built for TensorRT 10 no longer loads ([tensorrt.md](tensorrt.md), [onnx-runtime.md](onnx-runtime.md)).
- From JetPack 6 to 7 the module is reflashed (Ubuntu 22.04 to 24.04): Python 3.10 to 3.12, CUDA 12 to 13,
  every wheel and engine rebuilt; Jazzy becomes available from apt.
- After any upgrade, rerun the parity checks, the latency report and the thermal test before the robot works
  again; record the new versions beside the model.

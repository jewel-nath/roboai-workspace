# Targets: versions, ROS 2, Python, memory and off-board inference

Part of [learn-edge-deployment](../SKILL.md). Versions are from NVIDIA's JetPack download pages (6.2.3, 7.1,
7.2.1, 7.2.2), the Jetson Linux developer guides (r36.4.3, r38.4), the TensorRT 10.x-to-11.x Jetson migration
guide and the GR00T deployment guide (`NVIDIA/Isaac-GR00T` commit 708617f), read on 2026-11-25. They change with
every point release: read them again from the device before relying on them.

## Read what is installed

```bash
cat /etc/nv_tegra_release                          # L4T release and revision (Jetson only)
dpkg-query -W -f='${Package} ${Version}\n' nvidia-l4t-core 'libnvinfer*' 'cuda-toolkit*' 'cudnn*' 2>/dev/null
python3 -c "import tensorrt as trt; print(trt.__version__)"
python3 -c "import onnxruntime as ort; print(ort.__version__, ort.get_available_providers())"
sudo nvpmodel -q                                   # power mode (Jetson)
nvidia-smi                                         # desktop: driver version and the newest CUDA it supports
```

Write the output into the versions file that travels with the model and the engine.

## JetPack releases

| JetPack | L4T | Ubuntu, kernel | CUDA | cuDNN | TensorRT | Modules |
|---|---|---|---|---|---|---|
| 6.2.3 | 36.5.2 | 22.04, 5.15 | 12.6.10 | 9.3.0 | 10.3.0 | AGX Orin, Orin NX, Orin Nano |
| 7.1 | 38.4 | 24.04, 6.8 | 13.0.0 | 9.12.0 | 10.13.3.9 | AGX Thor dev kit, T5000, T4000 |
| 7.2.1 | 39.2.1 | 24.04, 6.8 | 13.2.2 | 9.20.0 | 10.16.2 | Thor (dev kit, T5000, T4000) and the Orin family |
| 7.2.2 | 39.2.2 | 24.04, 6.8 | 13.2.2 | 9.20.0 | 11.4.1 | as 7.2.1; installed from the 7.2.1 ISO, then `sudo apt update && sudo apt dist-upgrade` |

- JetPack 7.0 (L4T 38.2) was Thor-only; JetPack 6.0 to 6.2.2 (L4T 36.3 to 36.5.0) were Orin-only.
- The Orin Nano developer kit has no SD card image from JetPack 7.2 on: a unified ISO on a USB stick flashes
  it, with the Super configuration by default.
- **TensorRT 11 on Jetson** (migration guide): only 11.4.1, on JetPack 7.2.2 or later, for AGX Orin and Thor,
  from the Linux SBSA package. TensorRT 11.0 to 11.4.0 and 11.5.0 do not support JetPack, and Orin on JetPack
  6.x stays on TensorRT 10. The guide names only AGX Orin and Thor; check the support matrix for Orin NX and
  Orin Nano before moving them to 7.2.2.
- Projects that need JetPack 7.2: Isaac ROS 4.6 (Jazzy) and GR00T's Jetson setup (which no longer supports
  JetPack 6).

## ROS 2 Jazzy on each target

| Target | Jazzy | Notes |
|---|---|---|
| Jetson on JetPack 7.x (Ubuntu 24.04, arm64) | `ros-jazzy-*` from packages.ros.org | As on any arm64 Ubuntu 24.04; Python 3.12 |
| Jetson on JetPack 6.2.x (Ubuntu 22.04) | No binaries (Jazzy's Tier 1 is 24.04) | A container built with `LSB_RELEASE=24.04` by [jetson-containers](../../../wiki/tools/jetson-containers.md) (ROS from source), a source build, or Humble on the host |
| PC with an NVIDIA GPU | apt on Ubuntu 24.04 | GPU in containers: [ops-docker-ci](../../ops-docker-ci/references/gpu-display.md) |
| Raspberry Pi 5 or x86 mini PC | apt on Ubuntu 24.04 (arm64 or amd64) | Raspberry Pi OS has no Jazzy binaries; use Ubuntu or a container |

jetson-containers builds ROS from source into `/opt/ros`, so `ros-jazzy-*` debs do not fit inside its images;
add packages with its `/ros2_install.sh` (see the wiki page).

## Python on the robot

- The system Python is 3.10 on JetPack 6 and 3.12 on JetPack 7. JetPack's TensorRT Python module comes from apt
  (`python3-libnvinfer`), built for that interpreter.
- Ubuntu 24.04 refuses `pip install` into the system Python (PEP 668). Use a virtual environment that still sees
  the apt packages (`rclpy`, `cv_bridge`, `tensorrt`):

  ```bash
  python3 -m venv --system-site-packages ~/ros2_ws/venv && touch ~/ros2_ws/venv/COLCON_IGNORE
  source ~/ros2_ws/venv/bin/activate
  pip install "numpy<2" "cuda-python==13.*"     # cuda-python major = CUDA major (12.* on JetPack 6)
  python -c "import tensorrt, cuda.bindings.runtime, rclpy; print(tensorrt.__version__)"
  ```

  `numpy<2` keeps `cv_bridge` (built against the apt NumPy 1.26) importable
  ([perception-camera](../../perception-camera/references/detection-node.md#python-environment)).
- **Never `pip install tensorrt` on a Jetson.** On 2026-11-25 PyPI's `tensorrt` metapackage is 11.5.0.63 and
  pulls `tensorrt_cu13` 11.5, a release that does not support JetPack.
- `cuda-python` provides `cuda.bindings.runtime` for device buffers; NVIDIA's TensorRT samples moved from
  PyCUDA to it in TensorRT 10.14 and pin `cuda-python==12.9.0` for CUDA 12.
- PyTorch on Jetson comes from wheels built for the JetPack (NVIDIA's Jetson AI Lab index, jetson-containers,
  or, on JetPack 7.2, PyTorch's own `cu132` index, which GR00T uses for Thor and Orin). The CUDA wheels on PyPI
  target desktop and SBSA GPUs.

## Memory

- A Jetson's CPU and GPU share one DRAM. Weights, TensorRT workspace and activations, camera buffers, every ROS
  node and the desktop draw from the same pool; `tegrastats` RAM shows the total
  ([jetson.md](jetson.md#tegrastats)). Measure with the whole stack running, not the model alone.
- The engine build is the peak. Build before the rest of the stack starts (or at install time on the same
  device) and load the saved engine at run time.
- A robot without a monitor can boot to `multi-user.target` (`sudo systemctl set-default multi-user.target`)
  so no desktop session holds memory.
- Swap keeps a build from failing; it does not make inference usable. A model that only fits with swap is too big.

## DLA (Deep Learning Accelerator)

- Some Orin modules have DLA cores; Orin Nano modules and Thor have none (Thor: TensorRT Jetson migration
  guide). With TensorRT 10 on JetPack 6, `trtexec --useDLACore=0 --allowGPUFallback` builds for it; with
  TensorRT 11 only 11.4.1 on AGX Orin with JetPack 7.2.2 supports DLA, and DLA builds are strongly typed.
- Layers DLA cannot run fall back to the GPU, with copies between the two. Use DLA when the GPU is busy with
  other work, and check that total latency still fits the budget.

## CPU-only targets

- ONNX Runtime CPU ([onnx-runtime.md](onnx-runtime.md#cpu)). Give it the cores you can spare, not all of them:
  drivers and the ROS executor need CPU time at the control rate.
- Whether a model fits the control period on a CPU depends on its size and input resolution: measure on the
  device ([latency.md](latency.md)), and shrink the input or the model before quantizing.
- For steadier timing, the `performance` CPU frequency governor (`cpupower frequency-set -g performance`,
  from `linux-tools`) costs power and heat; measure both.

## Off-board inference

When a VLA or a large diffusion policy does not fit the robot's computer, run it on a GPU server on the
robot's network and keep a small client on the robot. The servers belong to
[learn-robot-learning](../../learn-robot-learning/SKILL.md):

| Model family | Server | Client on the robot |
|---|---|---|
| openpi (pi0, pi0.5) | `uv run scripts/serve_policy.py ...` (websocket, port 8000 by default) | `openpi-client` (`websocket_client_policy`) |
| LeRobot policies | `lerobot-policy-server --config_path=server.yaml` (Zenoh; TLS and ACL example configs) | `lerobot-rollout` with the remote backend |
| GR00T | `gr00t/eval/run_gr00t_server.py` (ZMQ, port 5555) | the robot's client script |

GR00T also runs on the robot: `scripts/deployment/build_trt_pipeline.py` exports ONNX, builds the TensorRT
engines on the device, checks accuracy and benchmarks, on Thor and Orin with JetPack 7.2. Its README reports a
median complete policy call (N1.7, LIBERO checkpoint, batch 1, two 256x256 cameras, four denoising steps,
pre- and post-processing included, RPC excluded) of 76.8 ms on AGX Thor and 149.0 ms on Jetson Orin with the
TensorRT pipeline, both at MAXN with `jetson_clocks`, and 35.6 ms on Thor with mixed NVFP4. Each call returns a
chunk of 40 actions, so the robot executes a chunk while the next one is computed.

Rules for off-board inference:

- The network is now part of the latency budget. Measure its p99 and maximum on the robot's real link
  (Wi-Fi spikes), not on a cable at the desk.
- The robot must hold or stop safely when a fresh action does not arrive in time: a deadline on the robot
  side, never only on the server ([arch-safety](../../arch-safety/SKILL.md)).
- Secure and authenticate the link (LeRobot ships TLS and ACL configs for Zenoh); never expose a policy port
  to an untrusted network.
- Weights carry their own terms: GR00T N1.7 under the NVIDIA Open Model License, openpi's base models under the
  Gemma terms ([GR00T](../../../wiki/learning/models/gr00t.md), [pi0](../../../wiki/learning/models/pi0.md)).

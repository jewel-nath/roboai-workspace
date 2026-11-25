---
name: learn-edge-deployment
description: Run trained policies and detectors on the robot's computer - target choice (Jetson Orin or Thor and its JetPack/L4T,
  desktop GPU, CPU-only), PyTorch to ONNX export and checks, TensorRT engines (trtexec, Python API, FP16, INT8 Q/DQ via ModelOpt),
  ONNX Runtime CUDA/TensorRT EPs, a ROS 2 Jazzy inference node, Isaac ROS TensorRT, latency and jitter, nvpmodel, tegrastats.
license: Apache-2.0
metadata:
  sources: []
  evidence: researched
  last_verified: 2026-11-25
---

# Edge deployment of learned models

Lets an agent take a trained model (policy or detector) and make it run on the robot's own computer at the
rate the task needs: choose the runtime, export and convert it without changing its outputs, wrap it in a
ROS 2 node, and prove latency, jitter, memory and temperature on the target. Checked on 2026-11-25 against
JetPack 6.2.3, 7.1, 7.2.1 and 7.2.2, TensorRT 10 and 11 (11.5 on GitHub), ONNX Runtime 1.32, PyTorch 2.15,
TensorRT Model Optimizer and Isaac ROS 4.6 (Jazzy); the recipes were not run. Lyrical and Humble notes are at the end.

## When to use

- A trained policy or detector must run on a Jetson, a PC with an NVIDIA GPU, or a CPU-only computer
  (Raspberry Pi 5, x86 mini PC).
- Exporting PyTorch to ONNX, building a TensorRT engine, choosing FP16 or INT8, and proving outputs still match.
- A model is too slow, misses its control rate, jitters, runs out of memory or slows down after some minutes.
- Setting Jetson power modes and clocks; reporting latency numbers someone else can trust.
- A JetPack or TensorRT upgrade broke engines, flags or Python code.

Elsewhere: training, datasets, checkpoints and the policy servers of LeRobot, openpi and GR00T in
[learn-robot-learning](../learn-robot-learning/SKILL.md); the deploy spec, the policy runner with its soft start,
watchdog and staged robot tests in [sim-to-real](../sim-to-real/SKILL.md); cameras, `cv_bridge` and a detector node
in [perception-camera](../perception-camera/SKILL.md); images and GPU containers in
[ops-docker-ci](../ops-docker-ci/SKILL.md); boot and systemd in [ops-bringup](../ops-bringup/SKILL.md); stops and
limits in [arch-safety](../arch-safety/SKILL.md).

## Pick the target

| Target | Stack (NVIDIA pages, 2026-11-25) | ROS 2 Jazzy there | Start with |
|---|---|---|---|
| Jetson Orin, JetPack 6.2.x | L4T 36.4-36.5, Ubuntu 22.04, CUDA 12.6, TensorRT 10.3 | No binaries (22.04): container or source build | TensorRT 10 (`--fp16` works) |
| Jetson Thor, JetPack 7.0/7.1 | L4T 38.x, Ubuntu 24.04, CUDA 13.0, TensorRT 10.13 | apt, arm64 | TensorRT 10 |
| Jetson Orin or Thor, JetPack 7.2.x | L4T 39.2.x, Ubuntu 24.04, CUDA 13.2; TensorRT 10.16.2 (7.2, 7.2.1) or **11.4.1 (7.2.2)** | apt, arm64; Isaac ROS 4.6 | TensorRT; check the major version first |
| PC with an NVIDIA GPU | Ubuntu 24.04, driver, CUDA 12 or 13; TensorRT 10 or 11 | apt | ONNX Runtime CUDA EP; TensorRT when it must be faster |
| CPU only | - | apt (amd64, arm64) | ONNX Runtime CPU |
| Policy too big for the robot | GPU server on the robot's network | client side only | The model's own server ([learn-robot-learning](../learn-robot-learning/SKILL.md)) |

Versions, Python, DLA, memory and off-board inference: [references/targets.md](references/targets.md).

## Quick start

On the target, with `policy.onnx` exported and checked ([references/onnx-export.md](references/onnx-export.md)):

```bash
cat /etc/nv_tegra_release                                    # L4T release (Jetson)
python3 -c "import tensorrt as trt; print(trt.__version__)"  # 10.x or 11.x decides the flags below
TRTEXEC=/usr/src/tensorrt/bin/trtexec
# TensorRT 10: reduced precision by builder flag
$TRTEXEC --onnx=policy.onnx --fp16 --saveEngine=policy.engine --timingCacheFile=trt.cache --skipInference
# TensorRT 11: precision comes from the model; convert it first (ModelOpt AutoCast, on a workstation)
python -m modelopt.onnx.autocast --onnx_path policy.onnx --output_path policy_fp16.onnx \
  --calibration_data recorded_inputs/                        # NPZ files of real inputs
$TRTEXEC --onnx=policy_fp16.onnx --saveEngine=policy.engine --timingCacheFile=trt.cache --skipInference
# Latency of the engine alone, on this device, in the power mode you will run
$TRTEXEC --loadEngine=policy.engine --percentile=50,99 --duration=30
```

Then put the engine behind the node in [references/ros2-node.md](references/ros2-node.md) and measure the whole
loop with [references/latency.md](references/latency.md).

## Workflow

1. **Write the budget and pin the stack.** Control rate, end-to-end budget (sensor stamp to command out), memory
   left after the rest of the stack, power mode. Record L4T or JetPack, CUDA, TensorRT, ONNX Runtime, the model
   file's hash and its training commit. [references/targets.md](references/targets.md).
   *Check:* one versions file sits beside the model (or in the [sim-to-real](../sim-to-real/references/deployment.md)
   deploy spec), and `sudo nvpmodel -q` shows the mode you will deploy in.

2. **Export to ONNX** with the model in `eval()` mode and its normalisation and action scaling inside the graph,
   batch 1, one file. PyTorch 2.15 exports through `torch.export` by default (opset 20; `dynamic_axes` and the
   TorchScript exporter are deprecated). [references/onnx-export.md](references/onnx-export.md).
   *Check:* `onnx.checker.check_model` passes and ONNX Runtime (CPU) matches PyTorch on a few hundred recorded
   inputs within a tolerance you wrote down first.

3. **Choose the runtime.** ONNX Runtime CPU for CPU targets; ONNX Runtime with the CUDA EP for a quick GPU path;
   TensorRT directly for the lowest and steadiest latency on Jetson; the Isaac ROS TensorRT node for camera
   pipelines on JetPack 7.2. [references/onnx-runtime.md](references/onnx-runtime.md),
   [references/tensorrt.md](references/tensorrt.md).
   *Check:* `session.get_providers()` starts with the provider you meant; ONNX Runtime falls back to CPU silently.

4. **Lower precision only for a measured reason.** FP16 first on a GPU (TensorRT 10: `--fp16`; TensorRT 11:
   AutoCast); INT8 only as explicit Q/DQ from ModelOpt with recorded robot inputs as calibration data; on CPU,
   static QDQ for CNNs, dynamic for transformers and RNNs. A small MLP policy may gain nothing; measure.
   *Check:* the task metric (action error against FP32 in units of the action range, or detector mAP on held-out
   robot images) stays within the tolerance from step 2.

5. **Build the engine on the target.** Engines are tied to the TensorRT version and the GPU that built them.
   Build on the robot (or an identical module with the same JetPack), keep the timing cache, store the engine
   with its versions, rebuild after any JetPack or TensorRT change. [references/tensorrt.md](references/tensorrt.md).
   *Check:* `trtexec --loadEngine` runs, and Polygraphy compares the engine with ONNX Runtime on recorded inputs.

6. **Wrap it in a ROS 2 node.** Load and warm up in the constructor, report ready only after warm-up, take the
   newest data (best effort, depth 1), copy the input stamp to the output, and keep inference out of the inner
   control loop (its own process, or a policy that sends targets to a ros2_control controller). For a policy,
   plug the backend into the sim-to-real runner. [references/ros2-node.md](references/ros2-node.md).
   *Check:* with every other node running, the output rate meets the target and output stamps equal input stamps.

7. **Measure latency and jitter honestly.** Per stage and end to end, percentiles and maximum, for ten minutes
   or more under full load, in the deployed power mode, with `tegrastats` logging. trtexec numbers are only the
   compute part. [references/latency.md](references/latency.md).
   *Check:* the report lists p50, p99 and max per stage, missed deadlines, versions, power mode and peak
   temperature, and p99 fits the budget from step 1.

8. **Set the power mode and watch thermals.** Mode IDs differ per module (mode 0 is 15 W on an Orin Nano 8GB,
   MAXN on AGX Orin, and an experimental MAXN on Thor). [references/jetson.md](references/jetson.md).
   *Check:* the rate at minute ten equals the rate at minute one, and the `tegrastats` log shows steady GPU
   clocks and temperatures under the throttle points in the enclosure the robot really has.

9. **Package and start at boot.** A container built for the target's L4T (jetson-containers or Isaac ROS images)
   or a native install; engine and timing cache on a persistent volume; systemd from
   [ops-bringup](../ops-bringup/SKILL.md). [references/jetson.md](references/jetson.md#containers).
   *Check:* after a reboot the node loads the cached engine (no build in the log) and reports ready within its
   readiness timeout.

## Traps

| Symptom | Cause | Fix |
|---|---|---|
| `--fp16` or `--int8` unknown; `BuilderFlag` has no `FP16`; calibrator classes missing | TensorRT 11 removed weak typing and implicit INT8 | AutoCast for FP16, ModelOpt Q/DQ for INT8, `--stronglyTyped` builds on TensorRT 10 too |
| Engine fails to deserialize after an upgrade or on another board | Engines are tied to TensorRT version and GPU | Keep the ONNX; rebuild on the target; record versions beside the engine |
| Everything broke after `apt dist-upgrade` on JetPack 7.2.1 | 7.2.2 moves TensorRT from 10.16.2 to 11.4.1 | Upgrade on a bench robot first; rerun step 4-7 checks |
| `pip install tensorrt` on a Jetson, then nothing works | PyPI's metapackage is TensorRT 11.5 for CUDA 13, which does not support JetPack | Use JetPack's `python3-libnvinfer`; venv with `--system-site-packages` |
| ONNX Runtime runs on the CPU without an error | GPU libraries not found, or both `onnxruntime` and `onnxruntime-gpu` installed | One package only; check `get_providers()`; on Jetson use a build for that JetPack |
| First inference takes minutes | TensorRT EP or Isaac ROS node building the engine at start | Engine cache on disk; warm up before reporting ready |
| Isaac ROS TensorRT node rebuilds the engine every start | `force_engine_update` defaults to `true` | Set it `false` with a fixed `engine_file_path` |
| Exported model disagrees with PyTorch | Train mode (dropout, batch norm), normalisation left out, wrong channel order, stochastic action | `eval()`, normalisation in the graph, `deterministic=True`, compare on recorded data |
| `policy.onnx.data` missing on the robot | PyTorch 2.15 writes external weights by default | `external_data=False` for small models, or copy both files; parse from the file path |
| INT8 accuracy collapses | Random or unrepresentative calibration data | Calibrate on recorded robot inputs; leave sensitive layers in higher precision |
| Fast in the benchmark, misses the rate on the robot | Benchmark alone, without pre/post-processing, other nodes, the real power mode | Measure the node end to end under full load ([latency.md](references/latency.md)) |
| Rate drops after a few minutes | Thermal or power-cap throttling | `tegrastats` log; cooling; a lower mode with steady clocks |
| Control loop jitters while the model runs | Inference in the same executor thread or process as the loop; Python GIL | Separate process; inner loop in ros2_control; callback groups for light work only |
| Drivers or SLAM OOM-killed | Jetson CPU and GPU share one RAM | Measure RAM in `tegrastats` with everything running; smaller or FP16 model |
| `torch.load` fails with "Weights only load failed" | PyTorch 2.6+ defaults to `weights_only=True` | Rebuild the class and load the `state_dict`; `weights_only=False` only for files you made |

## Checks

Before reporting a model deployed:

- The versions file names L4T or JetPack, CUDA, TensorRT, ONNX Runtime, the model hash and the power mode, and
  the engine was built on this device and loads without a rebuild.
- Numeric parity is recorded: ONNX against PyTorch, engine against ONNX, on recorded inputs, with tolerances.
- After any precision change the task metric is within its tolerance.
- End-to-end latency p50, p99 and max and the control-period spread under full load for at least ten minutes are
  inside the budget, with a `tegrastats` log showing no throttling and enough free RAM.
- The node's limits, stale-input watchdog and stop path are tested as in [sim-to-real](../sim-to-real/SKILL.md)
  and [arch-safety](../arch-safety/SKILL.md), with a hardware E-stop within reach for the first powered runs.
- Licences are written down: TensorRT, CUDA and JetPack (NVIDIA terms), Isaac ROS, the model code and weights.

## Distro differences

- **Lyrical** (Isaac ROS 5.x, 5.1 released 2026-11-16): Isaac ROS 5 targets Lyrical with packages for Ubuntu
  24.04 from its own buildfarm and moves from NITROS type adaptation to `rosidl::Buffer` (new in Lyrical's
  rosidl, absent in Jazzy). Lyrical's Tier 1 platform is Ubuntu 26.04, for which no JetPack exists, so on Jetson
  use Isaac ROS's builds or a container. TensorRT Python bindings for Python 3.14 arrived in TensorRT 11.1.
- **Humble**: native on JetPack 6 (Ubuntu 22.04) from apt; Isaac ROS 3.2 is the Humble line (JetPack 6.1 and 6.2).

## Related

- References: [targets.md](references/targets.md), [onnx-export.md](references/onnx-export.md),
  [tensorrt.md](references/tensorrt.md), [onnx-runtime.md](references/onnx-runtime.md),
  [ros2-node.md](references/ros2-node.md), [latency.md](references/latency.md), [jetson.md](references/jetson.md).
- Skills: [learn-robot-learning](../learn-robot-learning/SKILL.md), [sim-to-real](../sim-to-real/SKILL.md),
  [perception-camera](../perception-camera/SKILL.md), [ops-docker-ci](../ops-docker-ci/SKILL.md),
  [ops-bringup](../ops-bringup/SKILL.md), [ops-fleet](../ops-fleet/SKILL.md), [arch-safety](../arch-safety/SKILL.md),
  [ros2-control](../ros2-control/SKILL.md), [ros2-core](../ros2-core/SKILL.md).
- Wiki: [TensorRT](../../wiki/software/tensorrt.md), [jetson-containers](../../wiki/tools/jetson-containers.md),
  [Docker](../../wiki/tools/docker.md), [YOLO](../../wiki/learning/models/yolo.md),
  [GR00T](../../wiki/learning/models/gr00t.md), [pi0](../../wiki/learning/models/pi0.md),
  [SmolVLA](../../wiki/learning/models/smolvla.md), [ACT](../../wiki/learning/policies/act.md),
  [Diffusion Policy](../../wiki/learning/policies/diffusion-policy.md), [LeRobot](../../wiki/learning/frameworks/lerobot.md),
  [Stable-Baselines3](../../wiki/learning/frameworks/stable-baselines3.md),
  [choose a robot learning policy](../../wiki/guides/choose-a-robot-learning-policy.md),
  [choose a deployment method](../../wiki/guides/choose-a-deployment-method.md).
- Upstream: NVIDIA JetPack and Jetson Linux pages (r36.4.3, r38.4), TensorRT 10.x and 11.x docs (release notes,
  10.x to 11.x migration incl. Jetson, engine compatibility), `NVIDIA/TensorRT` (trtexec, Polygraphy, samples),
  `NVIDIA/TensorRT-Model-Optimizer`, onnxruntime.ai docs, PyTorch 2.15 `torch.onnx`, Isaac ROS 4.6 docs and
  `isaac_ros_dnn_inference`.

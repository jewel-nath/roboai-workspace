---
type: tool
name: TensorRT
summary: NVIDIA's inference optimiser and runtime that turns a trained network (usually ONNX) into a GPU-specific engine, the standard way to run detectors, pose models and VLAs fast on Jetson; the GitHub repo (parser, plugins, samples, trtexec source, tools) is Apache-2.0 but the core libraries are proprietary under NVIDIA's SDK licence. 11.5 on x86-64; JetPack 6.2 ships 10.3 and JetPack 7.2.2 ships 11.4.1.
tags: [tensorrt, nvidia, inference, onnx, trtexec, fp16, int8, fp8, quantization, engine, jetson, jetpack, thor, orin, dla, polygraphy, isaac-ros, deployment, edge-ai]
kind: library
area: learning
support:
license: Apache-2.0
links: {repo: "https://github.com/NVIDIA/TensorRT", docs: "https://docs.nvidia.com/deeplearning/tensorrt/latest/", site: "https://developer.nvidia.com/tensorrt"}
version: {tested: , latest: 11.5.0, as_of: 2026-11-25}
platforms: [linux, windows]
agent_access: cli
registry:
evidence: researched
last_verified: 2026-11-25
sources:
  - {url: "https://github.com/NVIDIA/TensorRT", title: "TensorRT OSS repository: README (11.x migration notes), LICENSE, CHANGELOG, VERSION, tags, trtexec sources", accessed: 2026-11-25}
  - {url: "https://docs.nvidia.com/deeplearning/tensorrt/latest/reference/sla.html", title: "TensorRT: License Agreement for NVIDIA Software Development Kits, with TensorRT supplement", accessed: 2026-11-25}
  - {url: "https://docs.nvidia.com/deeplearning/tensorrt/latest/getting-started/support-matrix.html", title: "TensorRT 11.5 Support Matrix", accessed: 2026-11-25}
  - {url: "https://docs.nvidia.com/deeplearning/tensorrt/latest/installing-tensorrt/installing.html", title: "TensorRT: Installing TensorRT", accessed: 2026-11-25}
  - {url: "https://docs.nvidia.com/deeplearning/tensorrt/latest/inference-library/engine-compatibility.html", title: "TensorRT: Engine Compatibility", accessed: 2026-11-25}
  - {url: "https://developer.nvidia.com/embedded/jetpack/downloads", title: "NVIDIA JetPack SDK downloads and archive notes (JetPack 7.0, 7.2, 7.2.2)", accessed: 2026-11-25}
  - {url: "https://developer.nvidia.com/embedded/jetpack-sdk-62", title: "NVIDIA JetPack 6.2 components", accessed: 2026-11-25}
  - {url: "https://nvidia-isaac-ros.github.io/repositories_and_packages/isaac_ros_dnn_inference/isaac_ros_tensor_rt/index.html", title: "Isaac ROS docs: isaac_ros_tensor_rt (release 5.1)", accessed: 2026-11-25}
---

# TensorRT

TensorRT compiles a trained network, usually ONNX, into an engine tuned for one NVIDIA GPU and
runs it [1]; builders use it to run detectors and VLA policies at camera rate on a Jetson.
**Licences:** the GitHub repo (ONNX parser, plugins, samples with `trtexec`, Polygraphy) is
Apache-2.0 [1]; the core libraries are binaries under NVIDIA's SDK licence, which lets you bundle
the runtime in your own application, for NVIDIA GPUs only [2]. 11.5 shipped 2026-11-18 [1].

## When to use it

Low-latency inference on NVIDIA GPUs: [YOLO](../learning/models/yolo.md) exports engines and
[GR00T](../learning/models/gr00t.md) builds a TensorRT pipeline. Elsewhere use ONNX Runtime.

## Setup

x86-64 needs compute capability 7.5+ (Turing on), Ubuntu 22.04 to 26.04 or Windows, and CUDA
13.5 or 12.9 [3]. `pip install tensorrt-cu13` (or `-cu12`) gives the Python API only; `trtexec`
comes in the `.deb`, tar or NGC container [4]. Jetson uses JetPack's TensorRT [4][6][7]:

| JetPack | TensorRT | CUDA |
|---|---|---|
| 6.2 (Orin, Ubuntu 22.04) | 10.3.0 [7] | 12.6 [7] |
| 7.0 (Thor) and 7.2 (Thor, Orin) | 10.13.2 and 10.16.2 [6] | 13.0 and 13.2.1 [6] |
| 7.2.2 (Thor, Orin) | 11.4.1 [6] | 13.2.2 [6] |

## How an agent works with it

```bash
trtexec --onnx=model.onnx --saveEngine=model.plan   # dynamic inputs: add --minShapes etc.
polygraphy run model.onnx --trt --onnxrt            # compare engine outputs with ONNX Runtime
```

TensorRT 11 is strongly typed: the engine keeps the ONNX graph's types, so export FP16 weights
for FP16, and add quantize and dequantize nodes (NVIDIA's Model Optimizer) for INT8, FP8 or FP4
[1]. ROS 2: Isaac ROS `isaac_ros_tensor_rt` runs an ONNX model or plan, `tensor_pub` in,
`tensor_sub` out, on Lyrical (5.1) [8]. Plugins cover layers the ONNX parser lacks [1]. Skill:
[learn-edge-deployment](../../skills/learn-edge-deployment/SKILL.md).

## Traps

- **Engines do not travel.** A plan runs only on the TensorRT version and GPU compute capability
  it was built for, unless built version-compatible; build on the robot. Hardware-compatible
  plans fail on JetPack, and any plan holds executable code, so load only your own [5].
- **TensorRT 10 guides break on 11:** `trtexec --fp16` and `--best`, builder precision flags,
  implicit INT8 calibration and `IPluginV2` are gone; port custom plugins to `IPluginV3` [1].
- **Jetson lags x86:** no 11.5 for JetPack; JetPack 6.2 has 10.3 and 7.2 has 10.16 [4][6][7].
- **Slow ROS start.** `force_engine_update` defaults to true, rebuilding the engine at every
  launch; save a plan and set it false [8].

## Alternatives

ONNX Runtime, Torch-TensorRT, OpenVINO; TensorRT-LLM and TensorRT Edge-LLM for language models.

## Sources

1. [TensorRT OSS repository: README (11.x migration notes), LICENSE, CHANGELOG, VERSION, tags, trtexec sources](https://github.com/NVIDIA/TensorRT), accessed 2026-11-25
2. [TensorRT: License Agreement for NVIDIA Software Development Kits, with TensorRT supplement](https://docs.nvidia.com/deeplearning/tensorrt/latest/reference/sla.html), accessed 2026-11-25
3. [TensorRT 11.5 Support Matrix](https://docs.nvidia.com/deeplearning/tensorrt/latest/getting-started/support-matrix.html), accessed 2026-11-25
4. [TensorRT: Installing TensorRT](https://docs.nvidia.com/deeplearning/tensorrt/latest/installing-tensorrt/installing.html), accessed 2026-11-25
5. [TensorRT: Engine Compatibility](https://docs.nvidia.com/deeplearning/tensorrt/latest/inference-library/engine-compatibility.html), accessed 2026-11-25
6. [NVIDIA JetPack SDK downloads and archive notes (JetPack 7.0, 7.2, 7.2.2)](https://developer.nvidia.com/embedded/jetpack/downloads), accessed 2026-11-25
7. [NVIDIA JetPack 6.2 components](https://developer.nvidia.com/embedded/jetpack-sdk-62), accessed 2026-11-25
8. [Isaac ROS docs: isaac_ros_tensor_rt (release 5.1)](https://nvidia-isaac-ros.github.io/repositories_and_packages/isaac_ros_dnn_inference/isaac_ros_tensor_rt/index.html), accessed 2026-11-25

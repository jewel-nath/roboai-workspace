# TensorRT: precision, engines, inference and comparison

Part of [learn-edge-deployment](../SKILL.md). Sources: `NVIDIA/TensorRT` at v11.5 (trtexec options in
`samples/trtexecCommon/sampleOptions.cpp`, `samples/python/common_runtime.py`, Polygraphy README and examples),
TensorRT 11.0 release notes, the 8.x-to-10.x and 10.x-to-11.x migration guides (Python API and Jetson), the
TensorRT 10.2 release notes, and `NVIDIA/TensorRT-Model-Optimizer` (ModelOpt, Apache-2.0) at commit 27a5044.
Read on 2026-11-25; not run. TensorRT, CUDA and cuDNN are under NVIDIA's licence terms: read them before
shipping them in an image.

## The version decides the recipe

| | TensorRT 10.x (JetPack 6.2.x, 7.0-7.2.1) | TensorRT 11.x (JetPack 7.2.2 = 11.4.1; desktops) |
|---|---|---|
| Typing | Weak by default; strong with `--stronglyTyped` or `STRONGLY_TYPED` | Always strong; `--stronglyTyped` is a no-op |
| FP16 | `--fp16` / `BuilderFlag.FP16` | No flag: convert the ONNX with ModelOpt AutoCast |
| INT8 | Explicit Q/DQ preferred; calibrators deprecated in 10.1, implicit INT8 in 10.2 | Explicit Q/DQ only; `IInt8Calibrator` and its subclasses removed |
| trtexec timing | Host-device copies included; CUDA graph off | Copies excluded; CUDA graph and spin wait on |
| Python | `build_serialized_network`, `set_memory_pool_limit`, `num_io_tensors`, `set_tensor_address`, `execute_async_v3` | Same |

Gone since TensorRT 10 (8.x-to-10.x guide): `build_engine`, `max_workspace_size`, the binding-index API
(`num_bindings`, `get_binding_shape`, `binding_is_input`) and the `EXPLICIT_BATCH` flag. Old samples with PyCUDA
and these calls do not run on any current JetPack.

**One path for both versions:** convert precision in the ONNX (AutoCast for FP16, ModelOpt Q/DQ for INT8) and
build strongly typed. On TensorRT 10 that means `--stronglyTyped`; on 11 it is the default.

## Find the tools

```bash
ls /usr/src/tensorrt/bin/trtexec        # JetPack and NVIDIA's deb packages put trtexec here
python3 -c "import tensorrt as trt; print(trt.__version__)"
```

ModelOpt runs on a workstation with a GPU: `pip3 install --extra-index-url https://pypi.nvidia.com "nvidia-modelopt[all]"`.
Its output is ordinary ONNX, so convert there and build the engine on the robot.

## FP16

TensorRT 10, weak typing:

```bash
trtexec --onnx=policy.onnx --fp16 --saveEngine=policy.engine --timingCacheFile=trt.cache --skipInference
```

TensorRT 11 (or TensorRT 10 strongly typed):

```bash
# Workstation. --calibration_data: one NPZ per batch keyed by input name, a directory of them, or a
# Polygraphy JSON of inputs; random inputs if omitted. --nodes_to_exclude keeps matching nodes in FP32.
python -m modelopt.onnx.autocast --onnx_path policy.onnx --output_path policy_fp16.onnx \
  --calibration_data recorded_inputs/
# Robot
trtexec --onnx=policy_fp16.onnx --saveEngine=policy.engine --timingCacheFile=trt.cache --skipInference
#  TensorRT 10 only: add --stronglyTyped
```

AutoCast runs the model on the calibration inputs to decide which nodes keep FP32; real inputs matter for the
same reason as in INT8.

## INT8 with Q/DQ

```bash
# Workstation: calibration NPZ keyed by input name, samples stacked on axis 0 (a few hundred recorded inputs)
python -m modelopt.onnx.quantization --onnx_path detector.onnx --quantize_mode int8 \
  --calibration_data_path calib.npz --output_path detector.int8.onnx
#  default --calibration_method for int8 is entropy (max also available); the rest becomes FP16 (--high_precision_dtype)
# Robot
trtexec --onnx=detector.int8.onnx --saveEngine=detector.engine --timingCacheFile=trt.cache --skipInference
#  TensorRT 10 only: add --stronglyTyped
```

- Without `--calibration_data_path` ModelOpt calibrates on random data: the engine builds, the scales are
  meaningless. The same holds for TensorRT 10's `trtexec --int8` without a calibration cache (the trtexec README
  says INT8 mode uses random weights): it measures speed, not accuracy.
- Calibrate on the robot's own data (its camera, lighting, observations across the task), not only on the
  public training set.
- Check on the target that the INT8 engine is really faster than the FP16 one for this model before accepting
  any accuracy loss; if PTQ loses too much, quantization-aware training with ModelOpt's PyTorch API
  (`modelopt.torch.quantization.quantize(model, INT8_DEFAULT_CFG, forward_loop)`) belongs in training.

## Build in Python (TensorRT 10.3 and later, and 11)

```python
"""Build a strongly typed engine from an ONNX file; keeps a timing cache and a versions file."""
import json
import platform
from pathlib import Path

import tensorrt as trt


def build_engine(onnx_path: str, engine_path: str, cache_path: str = "trt.cache", workspace_mib: int = 1024):
    logger = trt.Logger(trt.Logger.WARNING)
    builder = trt.Builder(logger)
    network = builder.create_network(1 << int(trt.NetworkDefinitionCreationFlag.STRONGLY_TYPED))
    parser = trt.OnnxParser(network, logger)
    if not parser.parse_from_file(onnx_path):          # from the path, so external weights are found
        raise RuntimeError("\n".join(str(parser.get_error(i)) for i in range(parser.num_errors)))

    config = builder.create_builder_config()
    config.set_memory_pool_limit(trt.MemoryPoolType.WORKSPACE, workspace_mib << 20)
    cache_file = Path(cache_path)
    cache = config.create_timing_cache(cache_file.read_bytes() if cache_file.exists() else b"")
    config.set_timing_cache(cache, ignore_mismatch=False)

    plan = builder.build_serialized_network(network, config)
    if plan is None:
        raise RuntimeError("engine build failed; rerun with trt.Logger.VERBOSE")
    Path(engine_path).write_bytes(plan)
    cache_file.write_bytes(config.get_timing_cache().serialize())

    tegra = Path("/etc/nv_tegra_release")
    Path(engine_path + ".json").write_text(json.dumps({
        "tensorrt": trt.__version__, "onnx": onnx_path, "machine": platform.machine(),
        "l4t": tegra.read_text().splitlines()[0] if tegra.exists() else None}, indent=2))
```

### Dynamic shapes

An ONNX with a dynamic axis needs an optimisation profile; the engine is fastest at the `opt` shape.

```bash
trtexec --onnx=model.onnx --minShapes=obs:1x48 --optShapes=obs:1x48 --maxShapes=obs:8x48 --saveEngine=model.engine
```

In Python: `profile = builder.create_optimization_profile()`, `profile.set_shape("obs", (1, 48), (1, 48), (8, 48))`,
`config.add_optimization_profile(profile)`, and at run time `context.set_input_shape("obs", shape)` before
allocating outputs. A robot sending batch 1 should export static shapes instead.

## Run in Python

```python
"""Static-shape TensorRT engine: dict of NumPy arrays in, dict out. One instance per thread."""
from pathlib import Path

import numpy as np
import tensorrt as trt
from cuda.bindings import runtime as cudart


def _check(result):
    err, *values = result
    if err != cudart.cudaError_t.cudaSuccess:
        raise RuntimeError(f"CUDA error: {cudart.cudaGetErrorName(err)[1]}")
    return values[0] if len(values) == 1 else values


class TrtModel:
    def __init__(self, engine_path: str):
        self._runtime = trt.Runtime(trt.Logger(trt.Logger.WARNING))
        self.engine = self._runtime.deserialize_cuda_engine(Path(engine_path).read_bytes())
        if self.engine is None:
            raise RuntimeError(f"{engine_path} was built by another TensorRT version or GPU: rebuild it here")
        self.context = self.engine.create_execution_context()
        self.stream = _check(cudart.cudaStreamCreate())
        self.inputs, self.outputs = {}, {}
        for i in range(self.engine.num_io_tensors):
            name = self.engine.get_tensor_name(i)
            shape = tuple(self.engine.get_tensor_shape(name))
            if any(d < 0 for d in shape):
                raise ValueError(f"{name} is dynamic {shape}: build a static engine or set input shapes first")
            host = np.empty(shape, dtype=trt.nptype(self.engine.get_tensor_dtype(name)))
            device = _check(cudart.cudaMalloc(host.nbytes))
            self.context.set_tensor_address(name, int(device))
            is_input = self.engine.get_tensor_mode(name) == trt.TensorIOMode.INPUT
            (self.inputs if is_input else self.outputs)[name] = (host, device)

    def __call__(self, feeds: dict) -> dict:
        h2d, d2h = cudart.cudaMemcpyKind.cudaMemcpyHostToDevice, cudart.cudaMemcpyKind.cudaMemcpyDeviceToHost
        for name, (host, device) in self.inputs.items():
            host[...] = feeds[name]                         # casts, e.g. float32 to an FP16 input
            _check(cudart.cudaMemcpyAsync(device, host.ctypes.data, host.nbytes, h2d, self.stream))
        if not self.context.execute_async_v3(self.stream):
            raise RuntimeError("TensorRT enqueue failed")
        for name, (host, device) in self.outputs.items():
            _check(cudart.cudaMemcpyAsync(host.ctypes.data, device, host.nbytes, d2h, self.stream))
        _check(cudart.cudaStreamSynchronize(self.stream))
        return {name: host.copy() for name, (host, _) in self.outputs.items()}
```

- Host buffers here are ordinary (pageable) memory; NVIDIA's `common_runtime.py` shows pinned buffers with
  `cudaMallocHost` when copies must overlap compute.
- The engine, context and buffers belong to one thread; give each node or thread its own `TrtModel`.
- Free nothing by hand while the node runs; let the process exit release device memory, or add
  `cudaFree`/`cudaStreamDestroy` in a `close()` for long-lived processes that reload models.

## Engines are tied to their builder

- By default an engine runs only with the TensorRT version that built it, on the same GPU model. Build on the
  robot, or on an identical module with the same JetPack; never ship an engine built on an x86 desktop to a Jetson.
- `--versionCompatible` (newer TensorRT of the same major can load it) and `--hardwareCompatibilityLevel`
  (`ampere+`, `sameComputeCapability`) trade speed for portability; ONNX Runtime's TensorRT EP docs say
  Jetson Orin is not eligible for hardware-compatible engines.
- Version-compatible engines carry executable code: deserialize only engines you built.
- The timing cache (`--timingCacheFile`) makes rebuilds after small changes faster; it is tied to the device too.
- Ship the ONNX and the build command, not the engine: build at install or first start on the device, then
  reuse the saved file ([jetson.md](jetson.md#containers)).

## Compare engine and ONNX

Polygraphy (`pip install colored polygraphy --extra-index-url https://pypi.ngc.nvidia.com`) runs both and
compares, preferably on recorded inputs. A data loader script defines `load_data()` that yields dicts of input
name to array.

```bash
polygraphy run policy.onnx --onnxrt --data-loader-script recorded.py --save-inputs in.json --save-outputs ref.json
polygraphy run policy.engine --model-type=engine --trt --load-inputs in.json --load-outputs ref.json \
  --atol 1e-3 --rtol 1e-3 --check-error-stat median
```

Choose tolerances from the task (action units, box pixels), not from the defaults. For detectors, also run the
engine on a held-out set of robot images and compare mAP with the FP32 model; per-tensor tolerances alone do
not show that a box moved.

## Traps

| Symptom | Cause | Fix |
|---|---|---|
| `AttributeError: ... 'build_engine'`, `max_workspace_size`, `num_bindings` | Pre-TensorRT 10 code | `build_serialized_network`, `set_memory_pool_limit`, IO tensor API |
| `No module named pycuda` or PyCUDA errors on CUDA 13 | NVIDIA samples moved to `cuda-python` | `from cuda.bindings import runtime as cudart` |
| Build runs out of memory on a Jetson | Workspace plus the rest of the stack | Build before starting the stack; lower `--memPoolSize=workspace:<MiB>` |
| Builds take minutes at every start | Engine built at run time, no cache | Save the engine and timing cache on a persistent path |
| FP16 output wrong (NaN, inf, saturation) | Values beyond FP16 range in some layers | AutoCast with real calibration data, `--nodes_to_exclude`; find the layer with Polygraphy (`--trt-outputs '*' --onnx-outputs '*'`) |
| trtexec latency far below what the node sees | TensorRT 11 trtexec excludes copies and uses CUDA graphs by default | `--includeDataTransfers --noCudaGraph` to match a plain Python node; then time the node itself |
| `--useDLACore` fails | No DLA on the module, or TensorRT 11 outside AGX Orin on 7.2.2 | GPU only ([targets.md](targets.md#dla-deep-learning-accelerator)) |

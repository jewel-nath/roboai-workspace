# ONNX Runtime: CPU, CUDA and TensorRT execution providers

Part of [learn-edge-deployment](../SKILL.md). Sources: onnxruntime.ai docs (install, CUDA and TensorRT
execution providers, quantization) and PyPI (`onnxruntime-gpu` 1.32.0, 2026-11-13), the TensorRT 11.1
release notes, and `dusty-nv/jetson-containers` `packages/ml/onnxruntime` (commit 271f90d); read 2026-11-25,
not run. ONNX Runtime is MIT; its GPU providers load NVIDIA's CUDA, cuDNN and TensorRT under NVIDIA's terms.

The simpler path: one `InferenceSession` runs the same `.onnx` on CPU, CUDA or TensorRT, so the robot code
does not change between a laptop and the robot. TensorRT directly ([tensorrt.md](tensorrt.md)) gives more
control over engines, memory and timing.

## Install the right build

Install **one** of `onnxruntime` (CPU) or `onnxruntime-gpu`: both provide the `onnxruntime` module, and with both
installed one silently shadows the other.

| Target | Build |
|---|---|
| CPU only (amd64, arm64) | `pip install onnxruntime` |
| PC with NVIDIA GPU | `pip install onnxruntime-gpu`. The CUDA EP docs list the PyPI wheel as the CUDA 13.0 build from 1.27 (to 1.30 in their table; CUDA 12.8 builds are published separately), while the install page still says CUDA 12; `onnxruntime-gpu[cuda,cudnn]` also pulls the CUDA and cuDNN runtime wheels. Check the CUDA EP requirements table against your driver |
| Jetson | A build for that JetPack: jetson-containers' `onnxruntime` package (1.25.1 by default for L4T 36 and CUDA 12.6 or newer) or NVIDIA's Jetson builds; PyPI's GPU wheels target desktop and SBSA CUDA |

The TensorRT EP links against one TensorRT major: ONNX Runtime 1.27 and later build it against TensorRT 11
(TensorRT 11.1 release notes), so on a TensorRT 10 JetPack use an ONNX Runtime built for TensorRT 10.

```bash
python3 -c "import onnxruntime as ort; print(ort.__version__, ort.get_available_providers())"
```

`get_available_providers()` lists what the build contains, not what will load: a provider whose libraries are
missing is dropped when the session is created. Always check `session.get_providers()`.

## CPU

```python
import onnxruntime as ort

opts = ort.SessionOptions()
opts.intra_op_num_threads = 2          # cores you can spare from drivers and the ROS executor
opts.inter_op_num_threads = 1
opts.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
session = ort.InferenceSession("policy.onnx", sess_options=opts, providers=["CPUExecutionProvider"])
```

Leaving `intra_op_num_threads` at its default lets ONNX Runtime use every core, which competes with the rest of
the robot and widens jitter. Try one, two and more threads on the target under load and keep the lowest p99
([latency.md](latency.md)).

### Quantizing for the CPU

From ONNX Runtime's quantization guide: dynamic quantization for RNNs and transformers, static quantization for
CNNs; on CPU, S8S8 in QDQ format is the default and first choice; Arm processors with dot-product instructions
gain most.

```python
"""Static QDQ quantization from recorded inputs, for a CNN on a CPU target."""
import numpy as np
from onnxruntime.quantization import (CalibrationDataReader, QuantFormat, QuantType,
                                      quantize_dynamic, quantize_static)


class RecordedReader(CalibrationDataReader):
    def __init__(self, path: str, input_name: str):
        self._rows = iter(np.load(path).astype(np.float32))   # N samples of the model's input, batch 1 each
        self._name = input_name

    def get_next(self):
        row = next(self._rows, None)
        return None if row is None else {self._name: row[None]}


quantize_static("model_infer.onnx", "model_int8.onnx", RecordedReader("calib.npy", "image"),
                quant_format=QuantFormat.QDQ, activation_type=QuantType.QInt8,
                weight_type=QuantType.QInt8, per_channel=True)
# Transformer or RNN instead: quantize_dynamic("model_infer.onnx", "model_int8.onnx", weight_type=QuantType.QInt8)
```

Run `python -m onnxruntime.quantization.preprocess --input model.onnx --output model_infer.onnx` first (shape
inference and optimisation; its optimisation step cannot write models over 2 GB). Then compare accuracy and
p99 latency against FP32 on the target: a small MLP policy may be no faster quantized.

## GPU: CUDA and TensorRT providers

```python
import onnxruntime as ort

trt_options = {
    "trt_engine_cache_enable": True,               # keep built engines; the first run builds them
    "trt_engine_cache_path": "/var/cache/my_robot/trt",
    "trt_timing_cache_enable": True,
    "trt_timing_cache_path": "/var/cache/my_robot/trt",
    "trt_fp16_enable": True,                       # TensorRT 10 builds; with TensorRT 11 feed an AutoCast model
    "trt_builder_optimization_level": 3,           # 0-5, default 3
}
cuda_options = {"device_id": 0, "cudnn_conv_algo_search": "HEURISTIC"}   # EXHAUSTIVE (default) is slower to start
session = ort.InferenceSession(
    "detector.onnx",
    providers=[("TensorrtExecutionProvider", trt_options),
               ("CUDAExecutionProvider", cuda_options),
               "CPUExecutionProvider"])
assert session.get_providers()[0] == "TensorrtExecutionProvider", session.get_providers()
```

- Order is priority: nodes TensorRT cannot run go to CUDA, then CPU. Each partition boundary costs copies; set
  `trt_dump_subgraphs` once to see how the graph was split.
- The TensorRT EP builds engines at the first `run`, which can take minutes on a Jetson. Warm up before the
  node reports ready, and keep the cache on a persistent path. A changed model, input shape, ONNX Runtime or
  TensorRT version means a new build.
- Dynamic inputs need `trt_profile_min_shapes`, `trt_profile_opt_shapes` and `trt_profile_max_shapes`
  (all three), or the EP rebuilds when a new shape arrives.
- CUDA EP only (no TensorRT): drop the first entry. Simplest GPU path, usually slower than TensorRT.

### Avoid copies: I/O binding

```python
import numpy as np
import onnxruntime as ort

x = ort.OrtValue.ortvalue_from_numpy(np.zeros((1, 3, 480, 640), np.float32), "cuda", 0)
binding = session.io_binding()
binding.bind_ortvalue_input("image", x)
binding.bind_output("boxes", "cuda")

def infer(frame: np.ndarray) -> np.ndarray:
    x.update_inplace(frame)            # copy into the same device buffer
    session.run_with_iobinding(binding)
    return binding.copy_outputs_to_cpu()[0]
```

CUDA graphs (`enable_cuda_graph` for the CUDA EP, `trt_cuda_graph_enable` for TensorRT) need this binding, since
replay reuses the same device addresses; update inputs in place, do not rebind.

## Traps

| Symptom | Cause | Fix |
|---|---|---|
| Inference on CPU, no error | Missing CUDA, cuDNN or TensorRT libraries, wrong CUDA major, or CPU package shadowing the GPU one | `session.get_providers()`; one package; a build for this CUDA and TensorRT |
| `libnvinfer.so.10` or `.so.11` not found | ONNX Runtime built for the other TensorRT major | ONNX Runtime matching the installed TensorRT |
| First frames take minutes, then fine | TensorRT EP building engines | Engine cache, warm-up before ready |
| Every restart rebuilds | Cache path not persistent (container `/tmp`) or input shapes change | Volume for the cache; static shapes or profiles |
| p99 much worse than median on CPU | Too many threads competing with ROS and drivers | Fewer `intra_op_num_threads`; measure under load |
| Quantized model slower | Quantize/dequantize overhead dominates a small model | Keep FP32 |

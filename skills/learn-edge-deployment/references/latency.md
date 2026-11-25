# Measuring latency and jitter honestly

Part of [learn-edge-deployment](../SKILL.md). Tool options from `NVIDIA/TensorRT` v11.5 (`trtexec` help text)
and the Jetson Linux r38.4 developer guide (`tegrastats`); `ros2 topic` verbs as in Jazzy's `ros2cli`. The
measurement method is ours; the sim-to-real skill measures command-to-motion latency on the actuators
([reality-gap.md](../../sim-to-real/references/reality-gap.md#2-latency-and-control-rate)).

## What to measure

| Stage | From → to | Tool |
|---|---|---|
| Model compute | engine enqueue → outputs ready | `trtexec --loadEngine`, the benchmark below |
| Inference step | step start → command published (pre-processing, copies, model, post-processing) | the node's `~/timing` ([ros2-node.md](ros2-node.md#timing-every-step)) |
| Input age | sensor `header.stamp` → command published | `~/timing`, `ros2 topic delay` |
| Control period | one command → the next | `~/timing`, `ros2 topic hz` |
| Command to motion | command published → measured motion | sim-to-real's spike test |

The robot feels the sum: input age plus the actuator's response. A model that computes in a few milliseconds can
still act on old data if frames queue in front of it.

## Rules

- **On the target**, never only on the workstation; in the power mode and clocks you deploy with
  ([jetson.md](jetson.md)), with `jetson_clocks` on or off as deployed.
- **Under full load**: every driver, SLAM, the camera pipeline, logging and bag recording running, as on a
  working robot.
- **After warm-up**, and long enough to include heat: ten minutes or more, with `tegrastats` logging.
- **Percentiles and maximum**, not the mean: p50, p99 and max, and the count of late steps. One late step in a
  hundred is a stutter every two seconds at 50 Hz.
- **Monotonic clocks for durations** (`time.monotonic()`, `time.perf_counter()`), ROS time only for stamps.
  Never `time.time()` for intervals: NTP or chrony may step it.
- **GPU work is asynchronous**: a timer around an enqueue measures nothing. Time after the stream synchronises
  (the `TrtModel` call does), or let the framework do it.
- **Real inputs**: recorded frames or observations, since some models' run time depends on content (NMS with
  many boxes, early exits).
- **Write the conditions down** with the numbers (report template below).

## trtexec: the compute part only

```bash
trtexec --loadEngine=policy.engine --warmUp=2000 --duration=60 --percentile=50,90,99
# TensorRT 11 defaults exclude host-device copies and use CUDA graphs and spin wait.
# To approximate a plain Python node:
trtexec --loadEngine=policy.engine --duration=60 --percentile=50,99 --includeDataTransfers --noCudaGraph --noSpinWait
# Per-layer times, to find the slow layer:
trtexec --loadEngine=policy.engine --dumpProfile --exportTimes=times.json
```

On TensorRT 10, copies are included by default and `--noDataTransfers`, `--useCudaGraph` and `--useSpinWait`
turn the optimisations on; the same engine reports different numbers under 10 and 11 defaults, so always print
the flags with the result.

## A benchmark on recorded inputs

```python
"""bench.py: p50/p99/max of the backend on recorded inputs, run on the target with the stack running."""
import sys
import time

import numpy as np

from my_robot_inference.backend import make_backend

model, inputs_path, name = sys.argv[1], sys.argv[2], sys.argv[3]
inputs = np.load(inputs_path).astype(np.float32)            # N rows of one input, batch 1 each
call, used = make_backend(model, {name: inputs[:1]}, warmup_runs=50)
times = []
for i in range(5000):
    x = inputs[i % len(inputs)][None]
    t0 = time.perf_counter()
    call({name: x})                                          # synchronous: returns host arrays
    times.append(time.perf_counter() - t0)
ms = 1e3 * np.asarray(times)
print(f"{model} on {used}: p50 {np.percentile(ms, 50):.2f} p99 {np.percentile(ms, 99):.2f} "
      f"max {ms.max():.2f} ms over {len(ms)} runs")
```

Run it twice: alone, then with the robot stack running. The gap between the two is what the other nodes cost
the model; the node-level `~/timing` then adds pre- and post-processing and executor delays.

## On the robot

```bash
ros2 topic hz /joint_group_position_controller/commands --window 500   # rate, min, max, std dev
ros2 topic delay /detections                    # now - header.stamp, per message
ros2 bag record -s mcap -o latency_$(date +%Y%m%d_%H%M) --topics /policy/timing /joint_states /diagnostics
sudo tegrastats --interval 1000 --logfile /var/log/my_robot/tegrastats_$(date +%Y%m%d_%H%M).log &
```

Summarise the bag's `~/timing` messages, rather than reading the console:

```python
"""timing_summary.py: percentiles from a bag's ~/timing topic (period, input age, inference in ms)."""
import sys

import numpy as np
from rclpy.serialization import deserialize_message
from rosbag2_py import ConverterOptions, SequentialReader, StorageOptions
from std_msgs.msg import Float32MultiArray

reader = SequentialReader()
reader.open(StorageOptions(uri=sys.argv[1], storage_id="mcap"), ConverterOptions("cdr", "cdr"))
rows = []
while reader.has_next():
    topic, data, _ = reader.read_next()
    if topic == sys.argv[2]:
        rows.append(deserialize_message(data, Float32MultiArray).data)
ms = np.asarray(rows)
for col, label in enumerate(["period", "input age", "inference"]):
    p50, p99 = np.percentile(ms[:, col], [50, 99])
    print(f"{label:10s} p50 {p50:6.2f}  p99 {p99:6.2f}  max {ms[:, col].max():6.2f} ms")
```

Usage: `python3 timing_summary.py latency_<date> /policy/timing`. Plot the period over time as well: a slow
upward drift is heat or memory, single spikes are scheduling or garbage collection, regular spikes match some
other node's period.

## Report

```text
Device: <module>, JetPack <x> (L4T <r>), power mode <name/id>, jetson_clocks <on/off>, fan <profile>, enclosure <yes/no>
Software: TensorRT <v> / ONNX Runtime <v> (<provider>), model <file> <sha256>, precision <fp32/fp16/int8>
Input: <shape>, recorded from <source>; stack running: <list>; duration <min>
Model compute (trtexec, flags <...>): p50 / p99 / max
Inference step (~/timing): p50 / p99 / max
Input age: p50 / p99 / max; control period: p50 / p99 / max, late steps <n> of <N>
Peak temperatures and any clock drop (tegrastats): <...>; RAM used / total: <...>
```

## When the budget is missed

Try, roughly in this order, and measure after each change:

1. Remove queueing: best effort depth 1, newest input only, no reliable QoS on sensor streams.
2. Move pre- and post-processing into the graph or into vectorised NumPy; avoid per-pixel Python.
3. TensorRT instead of ONNX Runtime CUDA; FP16; static shapes; a smaller input resolution.
4. Split processes so the model does not share an executor with the loop; move the inner loop into
   ros2_control.
5. A smaller model (fewer parameters, distillation in training: [learn-robot-learning](../../learn-robot-learning/SKILL.md)).
6. INT8 with real calibration data, then re-check accuracy.
7. A higher power mode, with the thermal test repeated.
8. A larger computer, or off-board inference with a deadline on the robot ([targets.md](targets.md#off-board-inference)).

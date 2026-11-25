# Export to ONNX and prove it matches

Part of [learn-edge-deployment](../SKILL.md). Written against PyTorch 2.15 (`torch.onnx`, branch
`release/2.15`), ONNX Runtime 1.32 and the Stable-Baselines3 export guide; not run. Training and checkpoints
come from [learn-robot-learning](../../learn-robot-learning/SKILL.md).

## What PyTorch 2.15 does by default

| Setting | Default | Note |
|---|---|---|
| `dynamo` | `True` (since 2.9) | Exports through `torch.export`; needs `pip install onnx onnxscript` |
| `opset_version` | `None` = opset 20 | Below 18 the exporter builds at 18 and tries to convert down, which may fail |
| `external_data` | `True` | Weights go to `<file>.onnx.data` beside the graph; set `False` for one file under 2 GB |
| `optimize` | `True` (since 2.7) | Constant folding and clean-up |
| `dynamic_shapes` | `None` (static) | Replaces `dynamic_axes`, which is deprecated with `dynamo=True` |
| `verify`, `report` | `False` | `verify=True` runs the model in ONNX Runtime; `report=True` writes a markdown report on failure |

`dynamo=False` still runs the TorchScript exporter, with a `DeprecationWarning`. `do_constant_folding`,
`training` and `operator_export_type` are deprecated arguments. Pick the opset from what the target accepts:
the TensorRT ONNX parser of the target's TensorRT version (its support matrix), or the ONNX Runtime version.

## Rules

- `model.eval()` before export: dropout off, batch norm on running statistics.
- Put everything the robot code would otherwise re-implement inside the graph: observation normalisation,
  image scaling and channel order, action clipping and unscaling. Then the deployment code has nothing to get
  wrong, and one comparison proves the whole chain.
- Batch 1 and static shapes unless the robot really sends varying shapes. A static engine is simpler to build,
  allocate and time.
- Name inputs and outputs (`obs`, `action`, `image`) and keep the names in the deploy spec.
- Compare on **recorded** inputs from the robot or the simulator, never only on random tensors: random inputs
  miss the ranges where precision and normalisation errors show.
- Load checkpoints as `state_dict` into the model class. Since PyTorch 2.6, `torch.load` defaults to
  `weights_only=True` and refuses pickled whole modules; `weights_only=False` runs arbitrary code from the file,
  so use it only on files you produced.

## A policy with its normalisation inside

```python
"""Export a policy with normalisation and action scaling inside the graph, then check it against PyTorch."""
import numpy as np
import onnx
import onnxruntime as ort
import torch


class DeployPolicy(torch.nn.Module):
    """Raw observation in, action in robot units out."""

    def __init__(self, net, obs_mean, obs_std, act_low, act_high):
        super().__init__()
        self.net = net
        for name, value in dict(obs_mean=obs_mean, obs_std=obs_std, act_low=act_low, act_high=act_high).items():
            self.register_buffer(name, torch.as_tensor(value, dtype=torch.float32))

    def forward(self, obs):
        x = (obs - self.obs_mean) / self.obs_std
        a = torch.clamp(self.net(x), -1.0, 1.0)            # the clip used in training
        return self.act_low + 0.5 * (a + 1.0) * (self.act_high - self.act_low)


def export(policy: DeployPolicy, obs_dim: int, path: str = "policy.onnx", opset: int = 20) -> None:
    policy.eval()
    torch.onnx.export(
        policy, (torch.zeros(1, obs_dim),), path,
        input_names=["obs"], output_names=["action"],
        opset_version=opset,           # at or below what the target's runtime accepts
        external_data=False,           # one file; models over 2 GB need external data
        dynamo=True,
    )
    onnx.checker.check_model(onnx.load(path))


def compare(policy: DeployPolicy, path: str, recorded_obs: np.ndarray, atol: float) -> float:
    """Largest absolute difference between PyTorch and ONNX Runtime over recorded observations."""
    session = ort.InferenceSession(path, providers=["CPUExecutionProvider"])
    worst = 0.0
    with torch.no_grad():
        for row in recorded_obs.astype(np.float32):
            obs = row[None]                                 # batch 1, as exported
            ref = policy(torch.from_numpy(obs)).numpy()
            out = session.run(["action"], {"obs": obs})[0]
            worst = max(worst, float(np.max(np.abs(ref - out))))
    if worst > atol:
        raise AssertionError(f"ONNX differs from PyTorch by {worst:.3g} (> {atol})")
    return worst
```

Set `atol` before you look at the result, from what matters on the robot (for example a fraction of the
smallest command step the actuators resolve). Record a few hundred observations across the task, including
starts, contacts and ends of episodes (`np.save("recorded_obs.npy", ...)` from a bag or from simulation).

Only if the robot sends varying batch sizes: `dynamic_shapes={"obs": {0: "batch"}}` (the key is the
`forward` argument's name; a string marks the axis dynamic). Then TensorRT needs an optimisation profile
([tensorrt.md](tensorrt.md#dynamic-shapes)).

## Image inputs

- Feed the graph what the camera node already has: `uint8` HWC in the camera's channel order, and do the cast,
  `/ 255`, mean and standard deviation, transpose to NCHW and BGR-to-RGB swap inside `forward`. It also saves a
  float copy on the CPU.
- Resizing stays outside the graph (in `image_proc`'s `ResizeNode` or OpenCV), so each resized stream keeps its
  own `camera_info` ([perception-camera](../../perception-camera/SKILL.md)).
- Check the preprocessing against the training pipeline on a few recorded frames: the same frame through the
  training transforms and through the exported graph must give the same model input.

## Stable-Baselines3 policies

From SB3's export guide: wrap the policy so `forward` returns `policy(observation, deterministic=True)` (PPO,
A2C) or `model.policy.actor(observation, deterministic=True)` (SAC, TD3). The wrapper includes SB3's
preprocessing (image scaling for CNN policies) but **not** the post-processing:

- PPO with a Box action space returns unclipped actions: add the clip to the action space bounds.
- SAC returns squashed actions in [-1, 1]: rescale with `low + 0.5 * (a + 1) * (high - low)`.
- `VecNormalize` statistics are outside the policy: put `clip((obs - obs_rms.mean) / sqrt(obs_rms.var + epsilon),
  -clip_obs, clip_obs)` into the wrapper from the saved `VecNormalize` object, as `DeployPolicy` does above.
- Images must arrive channel-first, as SB3 transposed them in training.

## LeRobot, openpi and GR00T policies

These are not single fixed graphs: action chunk queues, temporal ensembling, diffusion or flow-matching steps,
language tokenisers and processors run around the networks.

- Export only the parts that are fixed graphs (a vision encoder, a denoiser step) and keep the loops in Python
  around the engines; then compare the whole loop's actions with the original's `select_action` (LeRobot) or
  `infer` output on recorded episodes.
- Prefer the project's own path where it exists: GR00T's `build_trt_pipeline.py` exports, builds, verifies and
  benchmarks its engines ([targets.md](targets.md#off-board-inference)). It uses the TorchScript exporter on
  purpose (`dynamo=False`), because the dynamo exporter can fix dynamic sequence lengths to the example's value.
- Otherwise run the policy in PyTorch on the robot's GPU, or off-board.

## Traps

| Symptom | Cause | Fix |
|---|---|---|
| `torch.export` fails on data-dependent control flow | Python `if` on tensor values, unsupported ops | `report=True` for the reason; rewrite with `torch.where` or `torch.cond`; export the fixed sub-network only |
| Input that should be dynamic came out fixed | The exporter specialised the axis to the example's size | Inspect input shapes with `onnx.load(path).graph.input`; `dynamic_shapes`; check with a second size |
| ONNX Runtime and PyTorch disagree beyond float noise | `train()` mode, a buffer not registered (stays on the Python side), wrong dtype on the input | `eval()`; `register_buffer`; feed `float32` |
| Warning that opset 13 was converted, or conversion failed | Old `opset_version` from earlier code | Use 18 or newer if the target's runtime accepts it |
| Engine build cannot find weights | `.onnx.data` not copied, or the parser was given bytes instead of the path | `external_data=False`, or copy both files and parse from the file |
| Actions out of range on the robot only | Post-processing (clip, unscale) left in training code | Put it in the graph; compare in robot units |

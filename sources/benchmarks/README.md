# Benchmarks

A benchmark is a fixed test for a source in `trial` or `in-use`. It is re-run on every version bump,
so "is the new version better?" is answered with numbers, not impressions. The registry points to
it from the entry's `benchmark.path`.

```
benchmarks/<id>/
├── brief.md       ← the fixed input; frozen once a result exists
├── run.md         ← the exact steps and commands, and how each metric is read
└── results.csv    ← one row per run
```

## Rules

- **The brief never changes** after the first result. A changed brief is a new benchmark with a new
  id, so old and new results are never compared by mistake.
- **One row per run** in `results.csv`: the date, the version or commit of every source under test,
  the model that drove it, the metrics, a 1–10 human score, and notes.
- **Numbers only.** Rendered outputs (videos, images, meshes) are not committed; keep them locally or
  attach them to a release if they are worth sharing.
- **Columns may change only before the first row.** After that, add a column at the end and leave
  it empty in older rows.
- After a run, add a `history` line to each source's registry entry naming the benchmark result.

| Benchmark | Tests | Status |
|---|---|---|
| [pid-60s](pid-60s/) | explainroo with video-director: a 60-second narrated PID explainer | planned: first run in the video track's V1 pilot |

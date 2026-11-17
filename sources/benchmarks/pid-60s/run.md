# Run: pid-60s

Tests [explainroo](https://github.com/vincentsch/explainroo) together with
[video-director](https://github.com/win4r/video-director). Draft: the steps and columns are fixed
on the first run (video track V1), and frozen after it.

## Steps

1. Note the versions: explainroo (`npx --yes explainroo --version`), video-director's commit, and
   the model driving the agent.
2. In an empty folder outside git, give the agent [brief.md](brief.md) as written. Time the run
   from the prompt to the final MP4.
3. Run both checks on the result:

   ```bash
   npx --yes explainroo check videos/<name> --json
   ```

   ```bash
   python3 <video-director>/scripts/qa_video.py out/video.mp4 --out qa/
   ```

4. Watch it once and give it a score from 1 to 10 against the brief's five points.
5. Add one row to [results.csv](results.csv), and a `history` line to both registry entries.

## Metrics

| Column | From | Meaning |
|---|---|---|
| `wall_minutes` | stopwatch | Prompt to final MP4 |
| `duration_s` | ffprobe | Length of the video |
| `black_frames` | explainroo check | Black or blank frames found |
| `frozen_spans` | explainroo check | Stretches where the picture stands still |
| `small_text` | explainroo check | Frames with text too small for a phone |
| `loudness_lufs` | explainroo check | Integrated loudness |
| `true_peak_dbtp` | explainroo check | True peak |
| `misheard_words` | explainroo check `--script` | Script words the speech model did not hear |
| `qa_issues` | qa_video.py | Issues video-director's QA reports |
| `score` | a person | 1–10 against the brief |

# Tools

Runnable scripts, so the agent runs the numbers instead of guessing them.

| Path | What | Phase |
|---|---|---|
| `calc/` | Calculators: torque sizing, battery runtime, power budget, wire gauge, e-stop timing | 2 |
| `lint/` | Checks for frontmatter, links, stale dates and registry two-way links | 1 |
| `build_index.py` | Writes the generated index sections of the wiki and `sources/README.md` | 1 |
| `check_sources.py` | Compares each registry entry with its upstream today | 1 |

Rules for every script:

- Python 3, standard library first; any other dependency is named at the top of the file.
- `--help` explains it; `--json` gives machine-readable output where that makes sense.
- No network access unless the script says so; `check_sources.py` reads a GitHub token from the
  `GITHUB_TOKEN` environment variable and never stores it.

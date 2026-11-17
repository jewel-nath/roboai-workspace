# Tools

Runnable scripts, so the agent runs the numbers and the checks instead of guessing them.

| Script | Does |
|---|---|
| [build_index.py](build_index.py) | Writes the generated sections: each wiki section's index table, the summary in `sources/README.md`, and `NOTICE` |
| [lint.py](lint.py) | Checks frontmatter against [schema.yaml](schema.yaml), file names, links and anchors, the source registry, skills and their two-way links with the registry, and that generated sections are current |
| [check_sources.py](check_sources.py) | Compares each registry entry with its GitHub upstream: new commits and releases, archived, moved, licence changes, no recent push. With `--pages`, checks each Robot Atlas page against its repo: moved, archived, licence, and a stale `maturity` |
| [common.py](common.py) | Shared helpers for the scripts above |
| `calc/` | Calculators: torque sizing, battery runtime, power budget, wire gauge (Phase 5) |

## Running

The scripts declare their dependencies inline ([PEP 723](https://peps.python.org/pep-0723/)), so
[uv](https://docs.astral.sh/uv/) installs them on first run:

```bash
uv run tools/build_index.py
```

```bash
uv run tools/lint.py
```

```bash
uv run tools/check_sources.py --report --record
```

```bash
uv run tools/check_sources.py --pages --report
```

Each takes `--help`.

## Rules for scripts

- Python 3.10 or newer, standard library first; any other dependency goes in the script's
  `# /// script` block.
- `--help` explains it; `--json` gives machine-readable output where that makes sense.
- No network access unless the script says so. `check_sources.py` is the only one that goes
  online; it reads a GitHub token from the `GITHUB_TOKEN` environment variable and never stores it.
- A script that writes files says so in its help, and writes only what it names.

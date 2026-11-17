# Verification scope

[Home](../README.md) · [Setup](setup.md)

## What the checks mean

- **Static checks:** validate the 18 active notebooks, local input references,
  and local documentation links. Historical checkpoints are excluded.
- **Offline smoke checks:** execute the gathering, cleaning, exploration, and
  visualization **solution** notebooks selected by `scripts/smoke_notebooks.py`.
  Executed copies and a report belong in `artifacts/smoke/`, not source folders.
- **Data preservation:** supplied datasets, lecture PDF, and archived checkpoints
  were compared with the original Git versions during reorganization.

Smoke execution uses fresh kernels and notebook-directory working directories.
Unexpected errors must fail the run. It does not globally allow errors or claim
to test every course demonstration.

## Deliberately outside the smoke subset

- Blank assignments and unsolved projects
- Deliberately invalid path examples and optional MySQL installation/server
- Live Wikipedia HTML parsing
- The slice-warning teaching sequence in the mid-course solution
- Full mid-course/final-project execution and every optional transfer example
- Archived checkpoints

These exclusions are limits, not passing runtime results.

## Reading reports

Use `make check` and `make smoke` after setup. Inspect the generated report and
executed notebook copies to diagnose failures. A previous successful run does
not validate later code changes; rerun the affected checks.

The installed environment is local and ignored by Git. `requirements.txt`
specifies the baseline; `uv pip freeze --python .venv/bin/python` records the
complete resolved environment for a particular run.

## Verified baseline

The completed enrichment was checked on macOS with Python **3.11.18**,
NumPy **1.26.4**, pandas **2.2.3**, nbclient **0.10.4**, and nbformat **5.11.1**.

| Command or comparison | Result |
|---|---|
| `make setup` (including repeat setup) | Exit 0 |
| `make check` | Exit 0: four checker tests, 18 notebook schemas, 159 local references |
| `make smoke` | Exit 0: all four selected solution notebooks passed in fresh kernels |
| `git diff --check` | Exit 0 |
| Smoke source hashes | All four unchanged and matching committed source files |
| Smoke data hashes | All 26 data files unchanged |
| Original Git artifact comparison | 26 datasets, lecture PDF, and 20 archived checkpoints byte-identical |
| Assignment preservation comparison | Every original assignment cell retained unchanged and in order |

All 18 primary notebooks received explanatory additions: **94 new Markdown
cells** in total. The bounded executable changes were explicit assignment for
two missing-value fills, a separate generated-pickle output location, and
`numeric_only=True` for the song correlation calculation.

The correlation change fixes a reproduced pandas 2.x failure on song-title
strings; it does not establish that every numerically encoded field is an
appropriate correlation variable. The other excluded course cells remain
outside these passing runtime claims.

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

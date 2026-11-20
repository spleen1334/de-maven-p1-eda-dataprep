# Setup and execution

[Home](../README.md) · [Study guide](study_guide.md)

## Requirements

- Git, an internet connection for initial dependency installation, and
  [uv](https://docs.astral.sh/uv/getting-started/installation/)
- Python **3.11**, selected explicitly rather than whichever `python3` is on PATH
- Make is optional; equivalent commands are provided below.

The compatibility baseline retains NumPy 1.x and pandas 2.x for the original
2023 examples. In particular, the cleaning demo uses `np.NaN`, removed in NumPy
2. A baseline is not a recommendation to use old APIs in new projects.

## Create the environment

From the repository root:

```sh
make setup
make notebook
```

Without Make:

```sh
uv venv --python 3.11 --allow-existing .venv
uv pip install --python .venv/bin/python -r requirements.txt
.venv/bin/python -m jupyterlab
```

uv can download the requested interpreter if it is not installed. Dependencies
and a server are not installed globally. Setup requires network access; most
course exercises can subsequently use only bundled local data.

Open a notebook from `notebooks/` and select the kernel backed by `.venv`.
Confirm inside the notebook:

```python
import sys
from pathlib import Path
print(sys.executable)
print(Path.cwd())
```

The executable should belong to this repository's `.venv`. For active course
notebooks, the working directory should be their containing folder, such as
`notebooks/demos/`, **not the repository root**. Local paths such as
`../../data/course_offerings.csv` resolve from that directory. Exercise
solutions are one level deeper in `notebooks/exercises/solutions/`, so their
input paths start with `../../../data/`.

JupyterLab normally starts a new notebook kernel in its containing directory.
If you changed directories manually, restart the kernel and check again.
Notebook terminals and the server process may have different working directories.

## First notebook exercise

Follow the [first notebook exercise](lectures/03-jupyter-notebooks.md#try-it-saved-output-versus-live-state)
to practice running cells and see what a kernel restart does.

## Commands

| Command | Purpose |
|---|---|
| `make help` | Show available targets |
| `make setup` | Create the environment and install dependencies |
| `make notebook` | Launch JupyterLab |
| `make check` | Validate active notebook structure and local references |
| `make smoke` | Execute a selected offline subset into `artifacts/` |

`check` is static validation, not proof that every cell executes successfully.
Smoke tests must stop on unexpected errors; globally allowing errors would hide
real failures.

Without Make, the checks are:

```sh
.venv/bin/python scripts/check_notebooks.py
.venv/bin/python scripts/smoke_notebooks.py
```

## Execution boundaries

- **Assignments:** blank cells are intentional. Add your work rather than
  copying solution results into them.
- **Gathering demo:** some cells illustrate invalid/local-only paths.
  The MySQL example requires a separately configured server and optional
  `mysql-connector-python`; SQLite requires no server or extra package.
  Do not treat illustrative credentials as usable configuration.
- **Modeling demo:** the Wikipedia HTML table is live, and its headers may
  differ from historical output. Inspect the source rather than guessing a
  replacement column name.
- **Cleaning demo:** saving a regenerated groceries pickle is an output step.
  Keep generated data in `artifacts/`, separate from supplied course inputs.
- **EDA demo:** reads the bundled groceries pickle independently of that output.
  Only deserialize pickle data from a trusted source.
- **Mid-course solution:** demonstrates a slice-assignment warning and a safer
  approach. Understand the contrast rather than suppressing all warnings.

Archived checkpoints are historical artifacts, not maintained runnable notebooks.
They retain their original paths and may duplicate or differ from active lessons.

## Troubleshooting

| Symptom | Check |
|---|---|
| `ModuleNotFoundError` | Kernel executable; installing into another Python does not update this kernel |
| `FileNotFoundError` | Working directory, exact filename/case, and whether the path is an intentional example |
| Excel engine error | Install the requirements into `.venv`; XLSX examples use openpyxl |
| HTML parsing/network error | Network, current page structure, and optional HTML parser; local exercises need not depend on this demo |
| MySQL connection error | Optional server/database/user setup; not a SQLite problem |
| Output appears only after running cells out of order | Restart the kernel, run prerequisites in order, and inspect hidden state assumptions |
| Missing-value or mutation behavior differs | Check NumPy/pandas versions against `requirements.txt` |

## Recording a reproducible result

Record the notebook, dataset version/source, interpreter and package versions,
execution order, optional cells excluded, and decision assumptions. Saved course
outputs are historical examples, not fresh validation.

```sh
.venv/bin/python --version
uv pip freeze --python .venv/bin/python
git status --short
```

`make smoke` checks four selected offline solution notebooks, not every course
cell. External-service examples and deliberately invalid-path demonstrations
remain outside that check.

# Agent and maintainer guide

This file contains repository-maintenance conventions and historical validation
evidence, not learning material. The learner entry point is [README.md](README.md).

## Editing conventions

- Preserve the demo → assignment → solution learning sequence. Do not fill
  assignment blanks or leak answer-specific results into hints.
- Put explanations directly in notebooks/docs; PDF references are optional
  provenance. Use tiny inline datasets for standalone reference examples.
- Keep supplied `data/`, lecture PDF, and archived checkpoints intact. Generated
  outputs belong in ignored `artifacts/`.
- Active notebooks run with their containing directory as the kernel cwd and
  use `../../data/`. Archive notebooks retain historical paths.
- Preserve notebook format compatibility: existing minor-4 notebooks must not
  receive cell IDs unless the format is deliberately upgraded consistently.
- Use the `.venv` interpreter. Run focused checks for changed material, review
  the diff, and commit each verified logical step as requested by the user.
- Distinguish schema/link validation, example execution, and fresh-kernel
  notebook execution. Do not report unexecuted exclusions as passing tests.

See [setup](docs/setup.md) for environment commands.

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

## Historical verification: initial enrichment

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

## Historical verification: second explanatory pass

Added a self-contained concept guide with six independently executable inline
examples, and targeted comments tracing pivots, row masks, customer aggregates,
dummy variables, date arithmetic, ID parsing, and event-versus-session counts.
PDF references are optional source notes throughout the active notebooks.

Checks after reconciling this pass:

- All six concept-guide examples executed independently without external data.
- All **600 code cells** across the 18 notebooks have unchanged parsed Python
  syntax trees compared with the previous completed pass; IPython command lines
  were excluded from Python parsing. Assignment code cells are unchanged.
- Cell order, saved outputs, and execution counts were preserved.
- `make check`: exit 0; four checker tests, 18 schemas, **165 local references**.
- `make smoke`: exit 0; the same four offline solutions passed and all 26
  datasets remained unchanged.
- `git diff --check`: exit 0.

The runtime exclusions above still apply; more explanation does not imply
broader execution coverage.

## Historical verification: reference expansion and visual explanations

- Replaced the modeling warning checklist with a worked customer-table lesson.
- Expanded the patterns reference and glossary based on methods/concepts found
  in the active notebooks, without claiming complete library coverage.
- Executed 21 documentation Python blocks independently: six concept-guide,
  fourteen patterns, and one modeling-table example; all passed with inline data.
- Rendered all five Mermaid blocks using `mmdc` and the installed Chrome browser.
  The CLI's default headless-shell binary was unavailable; an explicit
  `executablePath` in a local Puppeteer configuration resolved rendering.
  Rendered artifacts/configuration are ignored under `artifacts/mermaid/`.
- `make check`: exit 0; four tests, 18 notebook schemas, 170 local references.
- Compared all notebook code cells with their pre-change Git versions: identical.
  Notebook changes were mechanical Markdown link/label updates only.
- `git diff --check`: exit 0.

No new fresh-kernel notebook run was needed for these documentation-only changes;
the earlier smoke results are historical evidence, not a newly expanded claim.

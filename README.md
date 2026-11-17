# Data preparation and exploratory data analysis

A learning workspace for Maven Analytics' **Data Science in Python, Part 1**.
Work through gathering, cleaning, exploring, and preparing data using pandas,
with selected NumPy and seaborn examples. This is not a production data pipeline
or a complete machine-learning course.

## Start here

1. Follow the [setup guide](docs/setup.md).
2. Read the [self-contained concept guide](docs/concept_guide.md), then the
   explanations embedded in the relevant notebook.
3. Run the demo, attempt the assignment without opening its solution, then compare
   your reasoning—not just your output.
4. Use the [study guide](docs/study_guide.md) for retrieval practice and the
   [reference index](docs/reference/README.md) when you need a reminder.

The [dataset guide](docs/data_guide.md) describes the bundled inputs; the
[verification notes](docs/verification.md) distinguish checks from untested examples.

## Learning map

The notebooks and documentation explain the concepts directly; opening the PDF
is optional. Page numbers below are source notes for the original lecture,
including section-divider slides.

| Topic | Slides | Demo | Practice | Solution |
|---|---|---|---|---|
| Data science and scoping | 7–40 | — | Define a question, audience, and data requirements | — |
| Jupyter basics | 41–61 | — | Create Markdown and code cells; restart a kernel | — |
| Gathering | 62–76 | [Demo](notebooks/demos/section04_gathering_data_code.ipynb) | [Assignment](notebooks/assignments/section04_assignments.ipynb) | [Solution](notebooks/solutions/section04_solutions.ipynb) |
| Cleaning | 77–131 | [Demo](notebooks/demos/section05_cleaning_data_code.ipynb) | [Assignment](notebooks/assignments/section05_assignments.ipynb) | [Solution](notebooks/solutions/section05_solutions.ipynb) |
| Exploring | 132–160 | [EDA demo](notebooks/demos/section06_exploratory_data_analysis_code.ipynb) | [Assignment](notebooks/assignments/section06_exploring_data_assignment.ipynb) | [Solution](notebooks/solutions/section06_exploring_data_solution.ipynb) |
| Visualizing | 132–160 | Same EDA demo | [Assignment](notebooks/assignments/section06_visualizing_data_assignments.ipynb) | [Solution](notebooks/solutions/section06_visualizing_data_solutions.ipynb) |
| Rotten Tomatoes project | 161–162 | — | [Project](notebooks/assignments/section07_midcourse_project.ipynb) | [Solution](notebooks/solutions/section07_midcourse_project_solutions.ipynb) |
| Modeling preparation | 163–193 | [Demo](notebooks/demos/section08_preparing_for_modeling_code.ipynb) | [Assignment](notebooks/assignments/section08_prepping_for_modeling_assignments.ipynb) | [Solution](notebooks/solutions/section08_prepping_for_modeling_solutions.ipynb) |
| Maven Music project | 194–196 | — | [Project](notebooks/assignments/section09_final_project.ipynb) | [Solution](notebooks/solutions/section09_final_project_solutions.ipynb) |

## Layout

```text
data/                          supplied datasets; original filenames retained
notebooks/demos/                worked lecture examples
notebooks/assignments/          exercises and unsolved projects
notebooks/solutions/            worked answers: attempt exercises first
docs/lectures/                 original lecture PDF
docs/reference/                concise command and reasoning references
archive/notebook_checkpoints/  preserved historical copies, not the curriculum
artifacts/                     generated reports/notebooks; ignored by Git
```

All active notebooks are two folders below the root, so their local inputs use
`../../data/`. Relative paths resolve from the **kernel's working directory**,
not inherently from the file's location. See [setup](docs/setup.md).

## Reproducibility and boundaries

- The gathering demo includes deliberately machine-specific path examples and an
  optional MySQL server example. They are not prerequisites for local exercises.
- The modeling demo reads a live Wikipedia table. Network access, page structure,
  and values can change independently of this repository.
- The EDA demo reads the supplied groceries pickle. Load pickle files only when
  you trust their source; deserialization can execute code.
- Saved outputs reflect previous runs. Restart the kernel and run in order when
  checking your work; a displayed result is not proof that a clean run succeeds.
- The course's “numeric, non-null single table” is a teaching target, not a
  universal rule for every model. Review [modeling safeguards](docs/reference/modeling_safeguards.md).

## Attribution and rights

Original lecture slides, notebooks, and datasets are supplied Maven Analytics
course materials; the lecture credits instructor Alice Zhao. Added learning
notes are supplementary, not official corrections or an endorsement.
No repository-wide license is asserted over third-party materials. Confirm
redistribution rights before publishing the PDF, notebooks, or datasets.

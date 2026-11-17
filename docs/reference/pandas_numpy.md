# Pandas and NumPy patterns

[Reference index](README.md) · [Official pandas guide](https://pandas.pydata.org/docs/user_guide/index.html)

Examples below are independent patterns. Adapt column names and paths to your
notebook; they are not completed course assignments.

## Load and inspect

```python
import pandas as pd
import numpy as np

df = pd.read_csv("../../data/course_offerings.csv")
df.head()
df.shape
df.info()
df.isna().sum()
```

Use `pd.read_excel(path, sheet_name="...")` for an Excel sheet and
`pd.read_sql_query(query, connection)` for SQL. SQLite is included with Python;
Excel reading needs an engine such as openpyxl.

## Select deliberately

```python
example = pd.DataFrame({"group": ["A", "A", "B"], "score": [4, 8, 6]})
selected = example.loc[
    (example["group"] == "A") & (example["score"] > 5),
    ["group", "score"],
].copy()
```

`.loc` selects by labels and conditions; `.iloc` selects by integer position.
Use `.copy()` when you intend to edit an independently filtered table. Do not
assume editing a selected Series updates its parent under every pandas version.

## Clean with a reason

```python
values = pd.Series([2.0, np.nan, 8.0])
filled = values.fillna(values.median())
```

Median imputation here is an illustration, not a recommended default. First
ask why the value is missing and what this replacement would change.
Prefer explicit assignment, such as `df["score"] = df["score"].fillna(value)`,
over chained `inplace=True` operations on a selected column.

```python
example["high_score"] = np.where(example["score"] >= 6, 1, 0)
```

`np.where(condition, yes, no)` expresses conditional selection. It does not
automatically make an operation better or faster than every pandas equivalent.

## Group and preserve meaning

```python
summary = example.groupby("group")["score"].agg(["count", "mean"])
```

The result now has one row per group. `count` counts non-missing values;
`size` counts rows. `groupby` drops missing grouping keys by default; consider
`dropna=False` when missing keys are part of the question.

## Join and check cardinality

```python
facts = pd.DataFrame({"item_id": [1, 1, 2], "quantity": [2, 3, 1]})
lookup = pd.DataFrame({"item_id": [1, 2], "category": ["book", "pen"]})
joined = facts.merge(lookup, on="item_id", how="left", validate="many_to_one")
assert len(joined) == len(facts)
```

Duplicate the lookup key and predict what happens. `validate` turns an
assumption into an executable check. An outer join with `indicator=True` helps
inspect unmatched keys; the appropriate join type depends on the question.

## Indexes and alignment

```python
combined = pd.concat([example, example], ignore_index=True)
```

Without `ignore_index=True`, concatenation normally preserves source indexes.
`reset_index(drop=True)` returns a new object unless assigned or used in place.
Assigning a Series to a column aligns index labels: use an explicit keyed merge
when business identity—not row labels—determines the match.

## Plot and explain

```python
import seaborn as sns
sns.histplot(data=example, x="score", discrete=True)
```

Choose a plot to answer a question. Histograms show distributions, scatterplots
show numerical relationships, and boxplots summarize distributions using
conventions that should not be mistaken for universal error-detection rules.

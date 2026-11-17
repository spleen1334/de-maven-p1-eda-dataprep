# Pandas and NumPy: worked patterns

[Reference index](README.md) · [Glossary](glossary.md) ·
[Customer-table walkthrough](modeling_preparation.md)

This reference covers operations used in the course, plus small validation
extensions such as merge checks. It is not a complete pandas or NumPy manual.
Each Python block is independently runnable, includes its own tiny data, and
avoids giving completed course-assignment answers.

## Find the operation you need

| Question | Section |
|---|---|
| Did I load the intended table? | 1: loading and inspection |
| Which rows/columns do I want? | 2: labels, positions, and masks |
| Why did rows or columns change shape? | 3: axes and persistence; 7: grouping; 8: pivot |
| How do I interpret messy values? | 4–6: types, missingness, strings, dates, duplicates |
| How do I combine tables without misassigning values? | 9–10: concatenation, joins, alignment |
| How do category indicators become customer features? | 11: dummy variables |
| What does NumPy contribute? | 12–13: arrays, conditionals, transformations, statistics |
| How do I inspect distributions and relationships? | 14: plotting and correlation |

## 1. Load and inspect before transforming

```python
from io import StringIO
import sqlite3
import pandas as pd

df = pd.read_csv(StringIO("course_id,fee\n101,20\n102,\n"))
assert df.shape == (2, 2)
assert df["fee"].isna().sum() == 1
print(df.head())       # first rows, not a random sample
df.info()             # prints a summary; returns None
print(df.describe())  # numerical summaries, with non-null counts

with sqlite3.connect(":memory:") as conn:
    result = pd.read_sql_query("SELECT 101 AS course_id", conn)
assert result.loc[0, "course_id"] == 101
```

`read_csv` interprets delimiters, headers, and missing-value tokens. A wrong
delimiter may produce one large column without raising an error.
`read_excel(path, sheet_name="...")` selects an Excel sheet; numeric sheet
positions are zero-based. `read_sql_query` executes SQL using a connection.
SQLite is part of Python; XLSX examples require openpyxl.

Compare columns, row count, dtypes, units, and grain with the source specification.
`shape` is an attribute; `head()` is a method. `info()` returning `None` is normal.

## 2. Select by label, position, or condition

```python
import pandas as pd

df = pd.DataFrame({"group": ["A", "A", "B"], "score": [4, 8, 6]},
                  index=[10, 20, 30])
assert df.loc[20, "score"] == 8       # index label 20
assert df.iloc[1, 1] == 8            # second row, second column
assert isinstance(df["score"], pd.Series)
assert isinstance(df[["score"]], pd.DataFrame)

mask = (df["group"] == "A") & (df["score"] > 5)
selected = df.loc[mask, ["group", "score"]].copy()
assert selected.index.tolist() == [20]
assert df.loc[df["group"].isin(["A", "B"])].shape[0] == 3
```

`.loc[rows, columns]` uses labels/masks; `.iloc[rows, columns]` uses positions.
Positional slices exclude their stop; label slices normally include their stop.
`df["score"]` is one-dimensional; `df[["score"]]` remains two-dimensional.

Use `&`, `|`, and `~` for elementwise AND, OR, and NOT, with parentheses around
comparisons. Python `and`/`or` do not combine whole Series elementwise.
Use `.copy()` when you intend to edit an independent filtered table.

## 3. Know which axis is reduced and whether a change persists

```python
import pandas as pd

df = pd.DataFrame({"a": [1.0, None], "b": [2.0, 3.0]})
assert df.isna().any(axis=1).tolist() == [False, True]  # one result per row
assert df.isna().sum(axis=0).to_dict() == {"a": 1, "b": 0}
assert df.sum(axis=1).tolist() == [3.0, 3.0]           # skip missing by default

changed = df.dropna()
assert len(df) == 2 and len(changed) == 1
df["a"] = df["a"].fillna(0)  # explicit persistent assignment
```

For reductions, `axis=0` reduces down rows, yielding column results; `axis=1`
reduces across columns, yielding row results. For concatenation, the axis names
where objects are appended—see section 9. Many operations return a new object.
Avoid relying on chained `inplace=True` calls on a selected Series to update its
parent across pandas versions.

## 4. Convert types and handle missingness deliberately

```python
import numpy as np
import pandas as pd

raw = pd.Series(["$12.50", "unknown", None])
numeric = pd.to_numeric(raw.str.replace("$", "", regex=False), errors="coerce")
assert numeric.isna().tolist() == [False, True, True]
assert numeric.notna().sum() == 1

nullable = pd.Series([1, None], dtype="Int64")  # capital I: nullable integer dtype
assert pd.isna(nullable.iloc[1])
values = pd.Series([2.0, np.nan, 8.0])
filled = values.fillna(values.median())
assert filled.tolist() == [2.0, 5.0, 8.0]
```

`to_numeric(errors="coerce")` replaces invalid tokens with missing values; it
does not prove those tokens were genuinely absent. Count conversion failures.
`astype(...)` is useful when values are already valid for the requested dtype;
converting to text can turn missing values into literal strings.

Use `isna()`/`notna()`, not equality with `np.nan`. pandas commonly skips missing
values in reductions; an all-missing sum can become zero unless you require
`min_count=1`. `pd.NA`, `np.nan`, `None`, and datetime `NaT` are not interchangeable
in every dtype. Use `np.nan` in new code; the legacy course environment also
supports the older `np.NaN` alias.

Imputation here demonstrates syntax, not a default cleaning policy.
`dropna(subset=[...])` removes rows based on selected fields; `fillna(...)`
replaces values. Both require a rationale and a before/after impact check.

## 5. Clean strings without hiding matching assumptions

```python
import pandas as pd

labels = pd.Series([" Pop ", "POP MUSIC", None])
clean = labels.str.strip().str.lower().replace({"pop music": "pop"})
assert clean.iloc[:2].tolist() == ["pop", "pop"]
contains = clean.str.contains("pop", regex=False, na=False)
assert contains.tolist() == [True, True, False]

ids = pd.Series(["S-12", "P-7"], index=[4, 8])
parts = ids.str.split("-", n=1, expand=True)
parts.columns = ["type", "audio_id"]
assert parts.index.tolist() == [4, 8]
assert parts.loc[4, "audio_id"] == "12"  # still text until explicitly converted
```

`.str` applies text methods to each value. `strip` removes surrounding
whitespace; `lower` normalizes case; `replace` can map known whole values.
`str.replace` replaces substrings/patterns within values.

`str.contains` treats its pattern as a regular expression by default;
`regex=False` asks for literal matching. `na=False` treats unknown text as
not matching **for this mask**, not as proof of absence in the source.
`str[6:]` slices every string from a fixed position and therefore assumes a
stable prefix. Splitting with `expand=True` preserves the Series index;
building a DataFrame from `.to_list()` normally creates a fresh index.

## 6. Dates, durations, and duplicate definitions

```python
import pandas as pd

dates = pd.to_datetime(pd.Series(["2023-05-20", "bad date"]), errors="coerce")
assert dates.isna().tolist() == [False, True]
assert dates.dt.month.iloc[0] == 5
elapsed = (pd.Timestamp("2023-06-01") - dates).dt.days
assert elapsed.iloc[0] == 12

rows = pd.DataFrame({"event_id": [1, 1, 2], "customer": ["A", "A", "A"]})
assert rows.duplicated(subset=["event_id"]).tolist() == [False, True, False]
assert rows.duplicated(subset=["event_id"], keep=False).tolist() == [True, True, False]
deduped = rows.drop_duplicates(subset=["event_id"], keep="first")
assert len(deduped) == 2
```

Parse before using `.dt`. Datetime subtraction returns timedeltas; `.dt.days`
extracts whole-day components, not a fractional-day duration. Use
`.dt.total_seconds() / 86400` when fractional elapsed days are needed.
Prefer year-aware bounds over `.dt.month < 6` on multi-year datasets.

Deduplication above assumes repeated `event_id` identifies the same event.
Repeated customer IDs alone are legitimate at event grain.
`keep=False` flags all group members; the default flags later occurrences.

## 7. Group, aggregate, and understand the result's shape

```python
import pandas as pd

events = pd.DataFrame({"customer": ["A", "A", "B"],
                       "item": ["pen", "pen", "book"],
                       "amount": [10.0, None, 5.0]})
assert events.groupby("customer").size().to_dict() == {"A": 2, "B": 1}
assert events.groupby("customer")["amount"].count().to_dict() == {"A": 1, "B": 1}
assert events.groupby("customer")["item"].nunique().to_dict() == {"A": 1, "B": 1}

totals = events.groupby("customer")["amount"].sum()  # customer-indexed Series
table = totals.rename("total_spend").to_frame().reset_index()
assert table.columns.tolist() == ["customer", "total_spend"]
summary = events.groupby("customer").agg(
    event_rows=("item", "size"), total_spend=("amount", "sum")
).reset_index()
assert len(summary) == 2

# Select an actual highest-priced row, keeping its associated item/customer.
winners = events.sort_values("amount", ascending=False).groupby("customer").head(1)
assert winners.set_index("customer").loc["A", "amount"] == 10
```

| Operation | What it counts or computes |
|---|---|
| `size()` | Rows, including rows with missing measured values |
| `count()` | Non-null entries in each selected column |
| `nunique()` | Distinct non-null values by default |
| `sum()`, `mean()`, `max()` | Numerical or dtype-appropriate summaries |
| `.agg(...)` | One or more named summaries per group |

`groupby` first creates a grouping object. Selecting one column and aggregating
often returns a Series indexed by group keys. `rename` names the values;
`to_frame` makes a DataFrame; `reset_index` restores key columns. Multiple group
keys can produce a MultiIndex. `as_index=False` is an alternative for many
DataFrame aggregations.

Missing group keys are excluded by default; use `dropna=False` when they should
form a group. Columnwise `max()` can combine values from different rows:
the maximum item name is not the item belonging to the maximum amount.
Selecting a row preserves that relationship; ties need an explicit policy.

## 8. Pivot long data to wide data for comparison

```python
import pandas as pd

long = pd.DataFrame({"year": [2020, 2020, 2021, 2021],
                     "country": ["A", "B", "A", "B"],
                     "score": [5.0, 6.0, 5.5, 6.5]})
wide = long.pivot(index="year", columns="country", values="score")
assert wide.shape == (2, 2)
assert wide.loc[2021, "B"] == 6.5
```

Each year becomes a row and each country a column; the score fills each cell.
`pivot` requires at most one value for each index/column pair. Missing
combinations become null. `pivot_table` can aggregate duplicate combinations,
but that changes the question—choose a justified aggregation, not a silent fix.

## 9. Concatenate rows or merge keys

```python
import pandas as pd

april = pd.DataFrame({"item_id": [1], "quantity": [2]})
may = pd.DataFrame({"item_id": [1, 2], "quantity": [3, 1]})
facts = pd.concat([april, may], axis=0, ignore_index=True)
lookup = pd.DataFrame({"lookup_id": [1, 2], "category": ["book", "pen"]})
joined = facts.merge(
    lookup, left_on="item_id", right_on="lookup_id", how="left",
    validate="many_to_one", indicator=True,
)
assert len(joined) == 3
assert joined["_merge"].eq("both").all()
```

`concat(axis=0)` stacks rows and aligns column names; differing schemas can
introduce nulls. Source indexes remain unless reset or ignored.
`concat(axis=1)` aligns indexes while attaching columns; it is not a key join.

| Merge type | Records retained, before considering repeated matches |
|---|---|
| `inner` | Matching keys |
| `left` | All left records and their matches |
| `right` | All right records and their matches |
| `outer` | Keys from both sides, exposing unmatched records |

Check key meaning, dtype, uniqueness, and unmatched records. Duplicate keys
can multiply rows. `validate` checks an expected relationship; `indicator`
labels matched/unmatched rows. pandas can match null join keys to each other,
unlike typical SQL null comparisons.

## 10. Distinguish label alignment from position

```python
import pandas as pd

base = pd.DataFrame({"name": ["B", "A"]}, index=[20, 10])
metrics = pd.Series([25.0, 80.0], index=[10, 20])
base["by_label"] = metrics
base["by_position"] = metrics.to_numpy()
assert base["by_label"].tolist() == [80.0, 25.0]
assert base["by_position"].tolist() == [25.0, 80.0]

left = pd.DataFrame({"customer": ["B", "A"]})
right = pd.DataFrame({"customer": ["A", "B"], "share": [25.0, 80.0]})
safe = left.merge(right, on="customer", how="left", validate="one_to_one")
assert safe["share"].tolist() == [80.0, 25.0]
```

A pandas Series carries labels; a NumPy array carries positions. Both operations
above are valid but mean different things. Do not discard labels just to make a
shape error disappear. When business identity matters, keep and join its key.
`reset_index(drop=True)` changes labels, not the identity or order of records.

## 11. Encode categories, then aggregate at the desired grain

```python
import pandas as pd

events = pd.DataFrame({"customer": ["A", "A", "B"],
                       "kind": ["book", "pen", "book"]})
flags = pd.get_dummies(events["kind"], dtype=int)
counts = pd.concat([events["customer"], flags], axis=1).groupby("customer").sum()
assert counts.loc["A"].to_dict() == {"book": 1, "pen": 1}
assert counts.loc["B"].to_dict() == {"book": 1, "pen": 0}
```

Dummy variables encode category membership without an arbitrary numeric order.
After summing per customer they are counts, not binary flags.
Missing categories are all-zero by default; `dummy_na=True` can represent
missingness explicitly. `drop_first=True` omits a reference category.
For future modeling, preserve the training category vocabulary and handle new
categories deliberately; do not infer their meaning from column position.

## 12. NumPy arrays, vectorization, broadcasting, and conditionals

```python
import numpy as np
import pandas as pd

prices = np.array([10.0, 20.0, 30.0])
assert prices.shape == (3,) and prices.ndim == 1
assert (prices * 1.05).tolist() == [10.5, 21.0, 31.5]
assert np.where(prices >= 20, 1, 0).tolist() == [0, 1, 1]

matrix = np.array([[1, 2], [3, 4]])
assert (matrix + np.array([10, 20])).tolist() == [[11, 22], [13, 24]]
assert np.isnan(np.array([1.0, np.nan])).tolist() == [False, True]

series = pd.Series([10, 20], index=["A", "B"])
result = np.where(series >= 20, "high", "low")
assert isinstance(result, np.ndarray)  # result has no pandas row labels
```

An `ndarray` has a shape, dimensions, and dtype, but no pandas index.
Vectorized operations work on arrays/Series rather than explicit Python
element loops; they are not automatically the fastest choice for every task.

Broadcasting allows compatible shapes: dimensions compared from the right
must be equal or one. A scalar broadcasts across a whole array; the two-value
row above broadcasts across the two matrix rows. Incompatible shapes fail.
`np.where(condition, yes, no)` selects values elementwise; it normally returns
an array and does not preserve a Series index. Missing Boolean conditions may
need an explicit policy before calling it.

## 13. Numerical summaries and transformations

```python
import numpy as np
import pandas as pd

values = np.array([1.0, 2.0, 3.0])
assert np.isclose(np.std(values, ddof=0), np.sqrt(2 / 3))
assert np.isclose(pd.Series(values).std(), 1.0)  # default ddof=1
assert np.isnan(np.mean([1.0, np.nan]))
assert np.nanmean([1.0, np.nan]) == 1.0

scaled = (values - values.min()) / (values.max() - values.min())
assert np.allclose(scaled, [0.0, 0.5, 1.0])
logged = np.log(np.array([1.0, np.e]))
assert np.allclose(logged, [0.0, 1.0])
assert np.isfinite(logged).all()
```

`ddof` changes the variance divisor to `N - ddof`: NumPy defaults to population
SD (`0`); pandas Series defaults to sample SD (`1`). NumPy array reductions such
as `np.mean` generally propagate NaN; `np.nanmean` explicitly skips it.
That differs from many pandas reductions.

Min–max scaling needs a nonzero range; standardization needs nonzero SD.
`np.log` requires positive real inputs for finite real outputs. These transforms
do not prove data is normal or improve every model. A three-SD outlier flag
requires distribution/context interpretation, not automatic deletion.
Fitted transformation parameters must come from training data in a later ML
workflow.

## 14. Inspect distributions and relationships

```python
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

sample = pd.DataFrame({"label": ["A", "B", "C", "D"],
                       "hours": [1.0, 2.0, 3.0, 4.0],
                       "score": [2.0, 4.0, 6.0, 8.0]})
assert sample["label"].value_counts().sum() == 4
correlations = sample[["hours", "score"]].corr()
assert correlations.loc["hours", "score"] == 1.0
sns.histplot(data=sample, x="hours", bins=4)
plt.close("all")
```

`value_counts()` counts values and excludes nulls by default; use
`dropna=False` to inspect missingness. A histogram shows a distribution;
its bins affect the apparent shape. Boxplots use quartile-based fences, not
universal valid-value limits. Scatterplots and pairplots help reveal clusters,
outliers, and nonlinear structure.

`corr()` summarizes pairwise linear relationships by default and can use
different non-missing rows for each pair. Select meaningful numerical measures:
`numeric_only=True` avoids text conversion failures, but numeric IDs/category
codes are not automatically sensible continuous measures. Constant columns
have undefined correlation. Association is not causation.

## Optional official documentation

- [pandas indexing](https://pandas.pydata.org/docs/user_guide/indexing.html)
- [Missing data](https://pandas.pydata.org/docs/user_guide/missing_data.html)
- [GroupBy](https://pandas.pydata.org/docs/user_guide/groupby.html)
- [Reshaping](https://pandas.pydata.org/docs/user_guide/reshaping.html)
- [Combining tables](https://pandas.pydata.org/docs/user_guide/merging.html)
- [Time series](https://pandas.pydata.org/docs/user_guide/timeseries.html)
- [NumPy fundamentals](https://numpy.org/doc/stable/user/basics.html)
- [seaborn tutorial](https://seaborn.pydata.org/tutorial.html)

These links support further study; the examples above stand alone.

# Glossary for preparation and EDA

[Reference index](README.md) · [Worked patterns](pandas_numpy.md) ·
[Modeling preparation](modeling_preparation.md)

This covers recurring concepts in the supplied notebooks and the adjacent
explanations needed to interpret them. It is a course-oriented glossary, not
every term in Python, statistics, pandas, NumPy, or machine learning.

## 1. Tables, identity, and execution

| Term | Meaning and practical distinction |
|---|---|
| DataFrame | A two-dimensional labeled table. Columns can have different dtypes. |
| Series | A one-dimensional labeled array, often a column. Its index affects arithmetic and assignment. |
| Record / observation | One row of collected information; its meaning depends on the grain. |
| Grain / unit of analysis | What one row represents: an event, customer, or customer-month. |
| Schema | Expected fields, types, and constraints; a readable file can still violate it. |
| Dtype | Storage/operation type, not business meaning. An integer ID is not automatically a measurement. |
| `object` dtype | General Python-object storage, often used for text in these notebooks; not a guarantee every value is a string. |
| Nullable dtype | A dtype supporting a missing marker without ordinary float coercion; pandas `Int64` differs from NumPy `int64`. |
| Index | Row labels used for selection/alignment; not necessarily unique or a business key. |
| RangeIndex | A compact integer index, often `0, 1, ...`; it does not establish row identity across tables. |
| MultiIndex | Labels with multiple levels, often produced by grouping on several keys. |
| Business key | Field(s) identifying a real entity/event; verify uniqueness at the intended grain. |
| Composite key | Multiple fields jointly identifying a row, such as customer plus month. |
| Lookup table | Attributes indexed by a key; uniqueness matters before enriching fact/event rows. |
| Kernel | The Python process executing notebook code; it retains state between cell runs. |
| Hidden state | Values or mutations left by earlier execution, including out-of-order runs. |
| Working directory | The process location used to resolve relative paths; not inherently the notebook file's location. |
| Parsing | Interpreting stored text/bytes as fields and types; success does not prove correct interpretation. |
| Delimiter / header | Field separator / column-name row in a text table. Wrong settings can silently change shape. |
| Provenance | Where data came from and what transformations produced the current version. |
| Reproducibility | Repeating a result with recorded inputs, environment, and execution order. |

## 2. Selection, shapes, and combining data

| Term | Meaning and practical distinction |
|---|---|
| Shape | Dimensions: a DataFrame reports `(rows, columns)`; an array can have more axes. |
| Axis | A dimension. A reduction over `axis=0` produces column results; `axis=1` produces row results in a DataFrame. |
| Label-based selection | `.loc` uses labels or masks; integer labels are not necessarily integer positions. |
| Position-based selection | `.iloc` uses zero-based integer positions; its slice stop is excluded. |
| Boolean mask | A true/false selection condition. Combine Series conditions with parenthesized `&`, `|`, and `~`. |
| Filtering | Retaining selected observations, changing the population described. |
| Sorting | Reordering observations without inherently excluding them. |
| Copy / mutation | An independent object / modification of an existing object. Make the intended update target explicit. |
| Copy-on-Write | pandas behavior controlling when shared data is copied on mutation; selected-column updates differ across versions/settings. |
| Alignment | pandas matches labels in many operations rather than matching positions. Equal lengths are insufficient. |
| Concatenation | Appending objects along an axis: row stacking or index-aligned column attachment. |
| Merge / join | Combining records by matching keys; not the same as positional or index-aligned attachment. |
| Join cardinality | Key relationship: one-to-one, many-to-one, one-to-many, or many-to-many. |
| Row multiplication | A join produces multiple output rows per input because a key matches repeatedly. |
| Unmatched key | A key without a counterpart; its treatment depends on join type and population requirements. |
| Aggregation | Reducing observations to summaries, often changing grain. |
| GroupBy | A split–apply–combine grouping object, not yet the final aggregated table. |
| Reduction | An operation returning fewer values, such as `sum`, `mean`, or `max`. |
| Distinct count | Number of different values, usually `nunique`; unlike event count or non-null count. |
| Long format | Repeated row entries encode a variable/category, such as one row per country-year. |
| Wide format | Separate columns encode those categories, such as one column per country. |
| Pivot | Reshaping long to wide; plain `pivot` needs a unique value per row/column-key pair. |
| Resetting an index | Moving index labels into columns, or dropping them; does not deduplicate or sort rows. |

## 3. Cleaning, strings, and time

| Term | Meaning and practical distinction |
|---|---|
| Missing value | Unavailable/undefined information, not necessarily zero or false. |
| `NaN` / `np.nan` | Floating missing/not-a-number marker. Detect with missing-value functions, not equality. |
| `pd.NA` | pandas missing scalar for nullable types; Boolean/arithmetic behavior is not identical to `np.nan`. |
| `None` | Python absence marker, sometimes interpreted as missing by pandas. |
| `NaT` | Missing datetime/timedelta marker. |
| Empty string | A zero-length text value; not automatically a missing marker after every operation. |
| Coercion | Conversion under a rule; `errors="coerce"` turns invalid parse inputs into missing values. |
| Imputation | Replacing missing values using an assumption; can alter variability and relationships. |
| Domain rule | A business/context constraint, such as a known valid grade range or currency. |
| Duplicate | Repetition under a defined key/grain; repeated customers can be valid event rows. |
| Normalization of labels | Standardizing text representations, such as spaces/case/synonyms; distinct from numeric scaling. |
| String accessor (`.str`) | Elementwise text operations on a Series, such as strip, split, and contains. |
| Regular expression | Pattern syntax used by many text methods; request literal matching when that is intended. |
| Datetime | A date/time value supporting chronological operations after parsing. |
| Datetime accessor (`.dt`) | Access to datetime/timedelta components such as month, weekday, and days. |
| Timedelta | A duration, such as the difference between two timestamps. |
| Time window | An explicit interval of observations; state boundaries and whether endpoints are included. |

## 4. NumPy, summaries, and numerical transformations

| Term | Meaning and practical distinction |
|---|---|
| `ndarray` | NumPy's multidimensional array; has shape/dtype but no pandas index labels. |
| Scalar | One value, often broadcast across an array in arithmetic. |
| Vectorization | Array-oriented operations rather than explicit Python element loops; not a universal performance guarantee. |
| Broadcasting | Expanding compatible array shapes during an operation; compared trailing dimensions must match or be one. |
| Conditional selection | Choosing values by a condition, for example `np.where(condition, yes, no)`. |
| Finite value | Neither infinity nor NaN; `np.isfinite` helps check transformed numerical features. |
| Mean / median | Arithmetic average / middle ordered value; they respond differently to skew and extremes. |
| Variance / standard deviation | Squared spread / spread in original units; results depend on missingness and divisor conventions. |
| `ddof` | Degrees-of-freedom correction in a variance divisor `N - ddof`; NumPy and pandas SD defaults differ. |
| Quantile / percentile | A location in an ordered distribution; percentile uses a 0–100 scale. |
| IQR | Interquartile range, Q3 minus Q1; used in common boxplot fences. |
| Outlier | An unusual observation relative to context, not necessarily an error. |
| Distribution | How observed values are spread across possible values. |
| Skew | Distribution asymmetry; often relevant when comparing means and medians. |
| Histogram bin | A value interval whose observations are counted; bin choices affect appearance. |
| Boxplot fence | A conventional quartile-based boundary for flagging extremes, not a domain validity limit. |
| Correlation | Association measure; default Pearson correlation summarizes linear relationships, not causation. |
| Confounding | Another variable helps explain an observed association, limiting causal interpretation. |
| Log transform | A logarithmic representation compressing multiplicative scale; finite real logs require positive inputs. |
| Min–max scaling | Subtract a fitted minimum and divide by fitted range; constant ranges need handling. |
| Standardization | Center using a fitted mean and scale using fitted SD; not a guarantee of normality. |
| Denominator | The reference count/quantity in a ratio; defines what a percentage means. |
| Zero denominator | Makes a ratio undefined; a replacement is a policy, not an observed percentage. |

## 5. Business interpretation and modeling preparation

| Term | Meaning and practical distinction |
|---|---|
| EDA | Exploring distributions, relationships, and data quality to inform questions and hypotheses. |
| Population / sample | The group of interest / the observations available to study it. |
| Cohort | A group defined by eligibility criteria and often a time reference. |
| Selection bias | Inclusion rules create systematic differences from the population a claim purports to describe. |
| Feature / predictor (`X`) | Input for a future model, available at the relevant prediction time. |
| Target / outcome (`y`) | What a supervised model would predict; not an input feature. |
| Nominal category | Labels without a natural order, such as genre. Arbitrary codes do not create meaningful distances. |
| Ordinal category | Ordered levels; order alone does not imply equal numerical spacing. |
| Dummy / one-hot indicator | A category-membership column; grouped sums become counts rather than flags. |
| Reference category | The category omitted under reduced dummy encoding; identify it explicitly. |
| Frequency / monetary / recency | Activity count / spend / elapsed time since an event, with explicit grain/window. |
| Prediction cutoff | Time at which inputs must be available to make a prediction. |
| Outcome horizon | Future interval in which the target is measured. |
| Event time / availability time | When something occurred / when the system could know it. These can differ. |
| Leakage | Target or unavailable information entering predictors or fitted preprocessing. |
| Training / validation / test data | Data used to fit / tune / evaluate models; a later-ML topic, not a completed step in these notebooks. |
| Fitted preprocessing | Transformations whose parameters are learned from data, such as imputation means or scaling ranges. |
| Held-out evaluation | Assessing a model on data not used to fit it; plots/correlations are not a substitute. |
| Censoring | An outcome time is not fully observed; a retained customer may cancel after observation ends. |
| Invariant | A property expected to remain true, such as key uniqueness after a many-to-one join. |
| Sensitivity analysis | Checking whether reasonable alternative assumptions change the conclusion. |
| Causal claim | A statement about effects of an intervention, requiring more than observational association. |

For executable examples, use [worked patterns](pandas_numpy.md). For a complete
small customer-table construction, use [modeling preparation](modeling_preparation.md).

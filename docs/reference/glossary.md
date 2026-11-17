# Glossary

[Reference index](README.md)

| Term | Meaning and practical check |
|---|---|
| DataFrame | A labeled two-dimensional table. Inspect both values and dtypes. |
| Series | A labeled one-dimensional array, often a DataFrame column. Its index matters. |
| Grain | What one row represents: transaction, customer, or customer-month, for example. |
| Key | Column(s) identifying an entity or row. Verify uniqueness at the intended grain. |
| Index | Row labels used for selection and alignment; not automatically a business key. |
| Schema | Expected columns, types, and constraints. Loading successfully does not prove conformance. |
| Missing value | Unavailable data, not necessarily zero. `NaN`, `pd.NA`, and `None` have different dtype behavior. |
| Imputation | Replacing missing values using an explicit rule; it can alter distributions and relationships. |
| Duplicate | Repetition under a chosen definition. Repeated customers may be valid transaction rows. |
| Outlier | An unusual observation relative to context; not necessarily an error. |
| Vectorization | Array-oriented operations rather than explicit Python element loops; performance still depends on the operation. |
| Boolean mask | True/false selection conditions. Use parentheses around conditions combined with `&` or `|`. |
| Aggregation | Reducing rows to summaries, usually changing grain. State grouping keys and denominator. |
| Join cardinality | The matching relationship between keys: one-to-one, many-to-one, or many-to-many. |
| Alignment | pandas matches labels during many operations, rather than simply matching positions. |
| Feature | An input variable for analysis/modeling; it must be meaningful and available at the relevant time. |
| Target | The outcome a supervised model would predict; it is not an input feature. |
| Leakage | Information unavailable at prediction time entering training or preprocessing. |
| Invariant | A property expected to remain true, such as unique customer IDs after a many-to-one join. |
| EDA | Exploring distributions, relationships, and data quality to inform questions and hypotheses. |
| Correlation | A measure of association, not proof of causation. |
| Reproducibility | Being able to repeat a result with recorded inputs, environment, and execution order. |

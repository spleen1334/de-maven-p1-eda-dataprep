# Modeling safeguards

[Reference index](README.md) · [Slides](../lectures/lecture.pdf)

The course prepares tables for future modeling; it does not implement a
complete training and evaluation workflow.

## Table design

Write down:

1. **Question:** What outcome is useful to predict?
2. **Grain:** What does one input row represent?
3. **Key:** Which columns identify that row?
4. **Cutoff:** When would the prediction be made?
5. **Outcome window:** When is the future outcome measured?

Aggregate transaction/listening records to the desired grain before combining
tables. Verify key uniqueness, join cardinality, unmatched records, and row
counts. A numeric table can still be semantically wrong.

## Time and leakage

The modeling demo's April/May predictors and June outcome provide a useful
starting point: future information must not enter earlier features.

For churn, cancellation dates may define an outcome, but post-cancellation
activity or attributes recorded after the prediction cutoff can leak it.
A retrospective association is not automatically a deployable predictive feature.

In a later ML course, separate training and evaluation data before learning
imputation values, scaling parameters, feature selection, or other fitted
transformations. Random splitting may be inappropriate for time-dependent data
or repeated observations of the same entity.

## Simplifications to recognize

- Slide 193's non-null numeric single table is the target for these exercises;
  some models support missing values, categorical inputs, or different structures.
- Encoding a category as a number does not establish a meaningful numeric order.
- IDs are useful join keys, not automatically meaningful numerical predictors.
- Missing does not necessarily mean false or zero.
- A three-standard-deviation rule is a normal-distribution-oriented heuristic;
  unusual values require domain review.
- Correlation and discount–churn associations do not establish causal effects.

## Minimal checks

Check unique keys, feature availability at cutoff, missingness, meaningful
ranges, join row counts, and the units/denominators of derived features.
For percentage features, decide what a zero denominator means rather than
silently replacing every undefined ratio with zero.

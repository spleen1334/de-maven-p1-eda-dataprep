# Study guide

[Home](../README.md) · [Reference](reference/README.md)

Start with the [concept guide](concept_guide.md) if a term or operation is new.
The explanations here and in the notebooks stand alone; slide numbers are
optional source references.

## A repeatable study session

1. Name the question and what one row represents.
2. Predict the output shape and one value before running code.
3. Run the example, then explain why its result makes sense.
4. Change one assumption or input and predict the new result.
5. Attempt the corresponding assignment without the solution.
6. Compare approaches and record a mistake you could recognize next time.

Looking up syntax is normal. Aim to remember **how to choose an operation,
what assumptions it makes, and how to detect a plausible but wrong answer**.

## Retrieval practice

Revisit a topic after roughly 1, 3, 7, and 14 days; adjust the intervals to your
difficulty. Close the notebook first:

- Explain the concept aloud in two sentences.
- Predict a tiny example's output.
- Write a transformation from memory, then check documentation if needed.
- Check an invariant: key uniqueness, row count, missingness, or valid range.
- State a limitation and one alternative.

Keep a short record:

| Topic | What I could explain | Mistake or uncertainty | Next review |
|---|---|---|---|
| Example: left join | Left rows are retained | Duplicate right keys can multiply rows | Choose a date |

## Decision log

Use this for important cleaning or feature decisions, not every line of code:

```text
Question:
Input grain → output grain:
Observation:
Chosen action and justification:
Rejected alternative:
Validation:
Interpretation and remaining uncertainty:
```

## Checkpoints by topic

### Gathering

- Can I explain CSV versus Excel sheets versus a SQL table?
- Can I diagnose a wrong working directory without changing random paths?
- Did I inspect columns, types, and row counts after loading?

### Cleaning

- Is a missing value unknown, not applicable, or a true zero?
- What constitutes a duplicate for this question?
- Is an extreme value invalid or just unusual?
- What evidence supports an imputation or correction?
- What changes if I retain rather than remove the affected records?

### Exploration and visualization

- What population does a filter leave me describing?
- What is the denominator of this percentage?
- Does an average hide different group sizes or a skewed distribution?
- Are axes, units, missing values, and sample sizes clear?
- Am I describing an association or making an unsupported causal claim?

### Modeling preparation

- What does one row represent, and is its key unique?
- Can a join multiply rows?
- Would each feature exist at prediction time?
- Are identifiers being used as keys rather than arbitrary numeric features?
- What must be learned only from a training set in a later modeling workflow?

## Project conclusions

Before opening a project solution, write:

**Claim → evidence → population/time scope → alternative explanation → limitation.**

For Rotten Tomatoes, explain how popularity filtering changes the population.
For Maven Music, distinguish retrospective churn descriptions from predictions
about future churn. Discount–cancellation association alone does not show that
discounts cause cancellation.

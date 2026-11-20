# 01 · Introduction to data science

Data science uses data to answer questions and support decisions. A useful
result might be a chart, a recommendation, or a prediction. The right result
depends on what someone needs to decide, not on how sophisticated the method is.

> **Where this course fits.** You'll gather, clean, explore, and prepare data
> in Python. You'll practice on movie ratings and finish with a music-service
> project that combines those skills. You will prepare data for modeling, but
> you won't need to train a machine-learning model.

## Four skills, one question

Suppose a museum wants to know whether to open more ticket counters on
Saturday mornings.

| Skill | What it contributes |
| --- | --- |
| **Programming** | Combine the daily queue logs and make the steps repeatable. |
| **Statistics** | Compare typical waits and unusually long waits across several Saturdays, rather than treating one busy morning as normal. |
| **Domain knowledge** | Ask staff when the queue clock starts and whether school groups use a different entrance. |
| **Communication** | Explain when waits tend to be longest, how much evidence you have, and what staffing change is worth testing. |

All four matter. A correct calculation can still mislead if it combines
different queues, and a sound finding is of little use if staff can't tell
when to act on it.

## Explore first; model when the decision calls for it

**Exploratory data analysis (EDA)** uses summaries and plots to understand
recorded data. “When were the longest waits last month?” is an EDA question.
A chart of waits by hour can help the museum choose when to try extra staffing.
It doesn't establish that adding a counter will shorten the wait.

**Machine learning** fits patterns from examples. If the museum must schedule
staff a week ahead, predicting next Saturday's waits might be useful:

- **Supervised learning** uses past examples with a known outcome, called the
  **target**. Predicting a future wait from historical waits, calendars, and
  bookings is supervised learning. A forecast needs to be tested on data not
  used to fit it.
- **Unsupervised learning** looks for structure without a target for the task.
  For example, grouping days by their hourly arrival patterns may reveal
  common kinds of busy days. Those groups don't predict the next wait.

## The work is iterative

Start by defining the question and decision. Gather data, check and clean it,
then explore the patterns. If the decision calls for prediction, prepare
inputs and evaluate a model; otherwise, communicate what the evidence shows
and what it leaves uncertain. A gap in the queue logs may send you back to
gathering rather than forward to modeling.

**Quick check:** If one Saturday's log starts recording an hour late, what
should you do before comparing its opening-hour waits with other Saturdays?
Confirm the gap and report that hour as unobserved, not as a zero-minute wait.

*Optional source: Maven Analytics, Data Science in Python, Part 1, PDF pp. 1–22.*

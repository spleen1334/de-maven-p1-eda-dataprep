# 02 · Scoping a data project

A **scope** states the decision, the question the data can answer, and the
limits of the work. Write it before you collect extra data or choose a model.

## Start with a decision

A bike-share coordinator can move one vanload of bikes each weekday morning.
She asks, “Where do we run out of bikes?” Make the request specific: **which
downtown stations were most often empty at 8 a.m. on weekdays last month?**
The coordinator can use that comparison to choose stations to inspect first.
Start with observed counts, not a prediction model: the immediate question is
about the recent past.

## Specify the evidence

| Scope choice | Bike-share example |
| --- | --- |
| Population and window | Downtown stations operating on weekdays last month. |
| Row grain | One station on one weekday at 8 a.m. A station appears on multiple dates. |
| Sources | Use the station roster for eligibility and timestamped inventory snapshots for counts. Trip logs alone cannot show how many bikes were docked. |
| Measure | For each station, divide the number of observed mornings with zero bikes by the number with a valid snapshot. Report that denominator and the eligible-morning count alongside the rate. A missing snapshot is not an empty station. |
| Limits | A snapshot can miss shortages before or after 8 a.m. The comparison doesn't show why stations were empty or whether moving bikes would prevent it. |

> **Written scope:** To help the coordinator choose where to inspect morning
> bike supply, compare the share of observed weekday 8 a.m. snapshots with
> zero bikes at operating downtown stations last month. Report counts and
> missing coverage by station. Treat the results as a snapshot-based
> comparison, not a measurement of all shortages or the effect of moving bikes.

## If the decision changes, the table may change

Suppose the coordinator now needs a **7 a.m. warning** for stations that might be
empty at 8 a.m. A supervised learning table would pair each past example's
inputs available by 7 a.m. with its **target**: the later outcome to predict.
For example, these two rows are from the same weekday:

| Station | Bikes at 7 a.m. | Docks | Empty at 8 a.m.? (target) |
| --- | ---: | ---: | --- |
| Oak | 2 | 12 | Yes |
| Pine | 8 | 16 | No |

If the question instead is “Which stations have similar early-morning
conditions?”, the same measurements can be used without an outcome column.
Station is an identifier; bike and dock counts are possible inputs.

| Station | Bikes at 7 a.m. | Docks |
| --- | ---: | ---: |
| Oak | 2 | 12 |
| Pine | 8 | 16 |

This second table is **unlabeled for that task**: it has columns, but none
serves as a known outcome to predict. These toy rows illustrate table layout;
they are not enough to fit a model or discover meaningful groups.

**Quick check:** Could “bikes at 7:45 a.m.” be an input for the 7 a.m. warning?
No. It isn't known when the warning must go out. Using it in historical
examples would give the prediction access to information it couldn't have
in practice.

*Optional source: Maven Analytics, Data Science in Python, Part 1, PDF pp. 23–40.*

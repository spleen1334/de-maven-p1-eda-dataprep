# Dataset guide

[Home](../README.md) · [Reference](reference/README.md)

Files live in `data/`. Original filenames are retained to preserve correspondence
with course prompts and slide examples. Counts below describe supplied CSV
records, excluding the header; they are not assertions about cleaned results.

| Files | Learning role |
|---|---|
| `course_offerings.csv`, `Course Offerings.xlsx`, `maven.db` | Gathering from CSV, Excel sheets, and SQLite |
| `Student Grades.xlsx`, `Run Times.xlsx`, `Groceries.xlsx` | Types, missing values, outliers, and calculated columns |
| `Alarm Survey Data.xlsx` | Cleaning assignments |
| `groceries_with_new_columns.pkl` | Prepared groceries input for EDA; trusted pickle only |
| `student_data.csv` | Exploration and visualization exercises |
| `Rotten Tomatoes Movies.csv` | Mid-course movie-ratings project |
| `happiness_data_*.txt`, `happiness_survey_data.csv` | Concatenation, schema differences, and joins |
| `Sales Tables.xlsx`, `online_shop.db` | Combining tables and customer-level modeling preparation |
| `Book_Sales_April.xlsx`, `Book_Sales_May.xlsx`, `Book_Sales_June.xlsx`, `Book_Customers.csv` | Modeling-preparation assignments |
| `Pen Sales Data.xlsx`, `house_listings.csv`, `spotify_songs.csv` | Additional preparation/feature examples |
| `maven_music_customers.csv`, `maven_music_listening_history.xlsx` | Final customer/listening-history project |

## Raw CSV inventory

| File | Rows | Columns |
|---|---:|---:|
| `Book_Customers.csv` | 28 | 5 |
| `Rotten Tomatoes Movies.csv` | 16,638 | 17 |
| `course_offerings.csv` | 5 | 3 |
| `happiness_survey_data.csv` | 2,089 | 6 |
| `house_listings.csv` | 343 | 27 |
| `maven_music_customers.csv` | 30 | 8 |
| `spotify_songs.csv` | 100 | 8 |
| `student_data.csv` | 200 | 5 |

The two SQLite databases contain `courses` (`maven.db`) and
`items`/`transactions` (`online_shop.db`). Inspect schemas before querying.
The happiness text files intentionally differ: Costa Rica has a differently
named country column, and the US file lacks the life-expectancy column.

## Input versus output

Treat supplied data as read-only learning inputs. Write derived artifacts to
`artifacts/`, not over the originals. Record transformations and their reasons;
“cleaned” is relative to a particular question, not a universal state.

External sources, such as the Wikipedia table in the modeling demo, are not
versioned with these local files. Historical notebook outputs do not freeze
those remote inputs.

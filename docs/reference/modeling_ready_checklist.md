# Preparing data for modeling: examples and checklist

[Reference index](README.md) · [Modeling demo with code](../../notebooks/demos/section08_preparing_for_modeling_code.ipynb)

> To prepare for modeling means to transform the data into a structure and
> format that can be used as a direct input for a machine learning algorithm.
> — Maven Analytics, slide 167

EDA is for exploration; the modeling table supplies inputs to an algorithm.
The examples below follow the slides, with smaller tables and no code required.

## 1. Build one table: stack rows, then add columns

- **`concat` stacks rows.** May and June sales have the same columns, so
  put June's rows below May's to make one sales table. There is no need to
  match store IDs.
- **`merge` matches rows by a key.** Use the store ID to match each sale to
  the store directory and bring in its region. The directory lists A as North
  and C as West, but has no entry for B.

| Month | Store | Sales | Region after a left join |
|---|---|---:|---|
| May | A | 300 | North |
| May | B | 200 | — |
| June | A | 250 | North |

Here, a **left** join keeps all sales, even though B has no region on file.
An **inner** join keeps only the two matched A sales. A **right** join keeps
all stores in the directory, so C appears without a sale and B drops out.
An **outer** join keeps both B and C, with blanks where no match exists.

Before stacking, check that columns mean the same thing in both batches.
Before joining, check that the directory has one row per store; two entries
for A would duplicate its sales. If you put columns side by side with
`concat`, pandas matches index labels, not store IDs.

## 2. Prepare rows: decide what one observation represents

Slide 175 calls this the **granularity** of the table: what one row represents.
To predict who will buy dog food in June, you need one row per **customer**,
not one row per **purchase**. Start with the purchase log:

| Customer | Month | Item | Price |
|---|---|---|---:|
| Lee | April | Dog leash | $20 |
| Lee | May | Cat litter | $30 |
| Sam | May | Garden gloves | $30 |
| Lee | June | Dog food | $15 |

Summarize April and May purchases into one row per customer, then attach the
June answer:

| Customer | Pet-supply purchases before June | Total spent before June | Bought dog food in June? |
|---|---:|---:|---:|
| Lee | 2 | $50 | 1 |
| Sam | 0 | $30 | 0 |

The two summaries are **features** (`X`); the June yes/no answer is the
**target** (`y`). “Bought at least once” is different from “bought three
times.” Use June records to find the answer, not to build the inputs. Keep
the customer ID for matching and checking rows, not as a number the model
should learn from. Sam's `0` is justified only if the June records are
complete; otherwise the answer may be unknown.

## 3. Prepare the columns

Slide 177 gives two goals: **“All values should be non-null”** and **“All
values should be numeric.”** That's the input format taught here, not a
requirement for every model.

- **Non-null:** Use `info()` or `isna()` to find missing values. Correct them
  from the source, fill them with a justified estimate, or leave out the row
  or column. A missing bedroom count doesn't mean zero bedrooms.
- **Numeric:** A price written as `"$250,000"` is text until you convert it.
  For categories and dates, choose a numeric representation that preserves
  what's useful.

> A dummy variable is a field that only contains zeros and ones to represent
> the presence (1) or absence (0) of a value, also known as one-hot encoding.
> — Slide 178

Instead of ranking blue, white, and yellow as 1, 2, and 3, give each color
its own column:

| Original color | Blue | White | Yellow |
|---|---:|---:|---:|
| Blue | 1 | 0 | 0 |
| White | 0 | 1 | 0 |
| Yellow | 0 | 0 | 1 |

If every color is known, two columns can be enough: if White and Yellow are
both `0`, the house is Blue. That's what dropping a **reference category**
means. A missing or previously unseen color shouldn't silently look like Blue.
Indicators also work on purchase rows: add up the `Pet supply` indicators for
a customer, and you have their pet-supply purchase count.

### Three ways to turn dates into features

Slides 180–183 show three approaches: **dummy variables**, **days from
“today”**, and **average time between dates**. The first treats a calendar
component like month as a category. The other two measure elapsed time.

Say a customer made purchases on **April 10, April 20, and May 20**, and you
want to make a prediction on **June 1**. Those dates can tell you three
different things:

1. **Purchases by month: when were they active?** Give each purchase an April
   or May indicator, just like the house colors above. An April purchase gets
   `April = 1` and `May = 0`; a May purchase gets the reverse. Add the
   indicators across the customer's purchases: **2 in April, 1 in May**.
   The result is a count in each column, not the month numbers `4` and `5`.
2. **Days since the last purchase (recency): how recently did they buy?**
   Count from the most recent purchase, May 20, to the prediction date,
   June 1. That's **12 days**. Use the date the prediction is made, not the
   day you happen to run the analysis. If there's no prior purchase,
   recency is unknown, not zero.
3. **Average gap: how often do they come back?** Put the purchases in date
   order and measure the time between each pair of consecutive purchases.
   April 10 to April 20 is **10 days**, and April 20 to May 20 is **30 days**.
   The average is **(10 + 30) ÷ 2 = 20 days**. Three purchases give two gaps;
   one purchase gives no gap at all. The 12 days after May 20 don't count
   here because June 1 is the prediction date, not another purchase.

Use only purchases known before the prediction date for all three features.
The same idea works for clock times: an order at 14:30 picked up at 15:10
waited **40 minutes**. Use that feature only if pickup has already happened
when you make the prediction.

## 4. Feature engineering

> Feature engineering is the process of creating columns that you think will
> be helpful inputs for improving a model (help predict, segment, etc.).
> — Slide 185

You already did this in Step 3: “days since last purchase” is a new input
column. Combine it with the number of purchases and total spend to get the
lecture's **recency, frequency, and monetary value (RFM)** example (slide 190).

> Transformations require mapping a set of values to another in a consistent
> way.
> — Slide 186

The slide compares a histogram of house prices with a histogram of their
logs. A **log transform** compresses the high end of a right-skewed price
distribution. It can make the distribution less skewed, but it doesn't
guarantee a bell shape. An ordinary log needs positive values.

**Scaling** puts input features on a similar scale (slides 187–188). The
lecture compares prices and bedroom counts using two methods:

| Method | What you do | Bedroom example |
|---|---|---|
| **Normalization (min–max scaling)** | Subtract the minimum and divide by the range to put the training values between 0 and 1. | If the range is 1 to 5 bedrooms, 1 maps to **0**, 3 to **0.5**, and 5 to **1**. |
| **Standardization** | Subtract the mean and divide by the standard deviation so the training values have mean 0 and standard deviation 1. | If the mean is 3 bedrooms and the standard deviation is 1, then 2, 3, and 4 map to **−1, 0, and +1**. |

Scaling changes the units, not what the feature measures. You don't need both
scaling methods, and some models need neither. If a training column is
constant, both formulas would divide by zero. A new value beyond the training
range can go below 0 or above 1 after min–max scaling. Learn fill values,
which categories get columns, and scaling numbers from training data only;
reuse those choices on new rows.

> A proxy variable is a feature meant to approximately represent another.
> — Slide 189

The lecture uses ZIP codes to look up **area median income** or **distance to
the city center**. The ZIP code is a label, not a measurement. The lookup is
only an approximation: area median income isn't a household's income, and
distance from the center of a ZIP area isn't distance from the house itself.

## 5. Review the table before modeling

The four preparation steps from slide 167, with a check for each:

- [ ] **Create a single table.** Did stacking and joining keep the rows I
  intended, without accidental duplicates?
- [ ] **Set the correct row granularity.** What does one row represent, and
  what am I predicting for it?
- [ ] **Ensure each input column is non-null and numeric** for this workflow.
  Did I handle missing values, categories, and dates deliberately?
- [ ] **Engineer features for the model.** Why might each feature help, and
  is it available when the prediction is made?

Keep future outcomes separate from the inputs. Reuse the same columns and
training-derived preprocessing choices on new data.

The lecture ends with a **preview**, not a model-building lesson: fit a
classifier (logistic regression in the slides) on past customers with known
yes/no answers, then estimate the probability of a purchase for other
customers. A tidy table makes this possible; comparing predictions with
outcomes the model wasn't trained on tells you how well it works. If it
performs poorly, go back to the data and ask whether you measured the right
things.

For a longer example of building one row per customer, see the
[customer-table walkthrough](modeling_preparation.md).

Source: Maven Analytics, *Data Science in Python, Part 1*, slides 163–193.

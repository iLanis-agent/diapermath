# Diaper Math

Diaper size planning: weight gain against the next size line, diapers, packs, cost and the size-up date. The 6200-gram baby at 150 grams a week reaches the 8000-gram size line in 12 weeks and 0 days.

## Named constants

None. Every number is the owner's own entry.

## What it computes

- **The size truth** - the gap from the current weight (1000 to 20000 grams) to the size line (1001 to 30000 grams, above the current weight) at the weekly gain (1 to 1000 grams), as whole weeks and days, ceiling on the day so the line is truly reached.
- **The diapers truth** - the daily pace (1 to 30 diapers) multiplied by those days.
- **The packs truth** - the packs (1 to 200 diapers each) the diapers fill, what the last pack holds, the cost at the pack price (1 to 99999 cents), and the price of one diaper, money at two decimals, half-up on display only.
- **The date truth** - the start date (a real date from 2000 to 2100) plus those days, with the weekday, computed by civil-date arithmetic with no library.

## Boundary

Arithmetic only. Counting applied as written. It has not seen any baby, scale or store and does not know whether the gain will hold, a size truly fits or the price will stay, and it gives no verdict that a weight is healthy or a size is right. Every number is the owner's own entry.

## Files

- `index.html` - landing page with the boundary and starting examples.
- `app.html` - the planner; every keystroke recomputes.
- `engine.js` - the four truths, shared by the page and the tests.
- `oracle.py` - an independent Python re-implementation; writes `expected.json`.
- `test.js` - runs the engine against `expected.json` (104 cases, 20 error cases).

## Tests

```
python3 oracle.py
node test.js
```

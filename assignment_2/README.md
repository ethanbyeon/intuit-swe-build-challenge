# Assignment 2: Sales Analysis

This module analyzes sales data for a small spicy chicken sandwich shop using
a CSV file and functional style aggregation in Python.

---

## Requirements

- Python 3.10+

No third party libraries are required.
Only the Python standard library is used.

---

## Project Structure

```text
assignment_2/
    hot_chicken_sales.csv  # Sample sales dataset
    sales_analysis.py      # Data model, CSV loader, analysis functions
    run_analysis.py        # Main file
    test_sales_analysis.py # Unit tests for all analysis functions
```

---

## Dataset

**File:** `hot_chicken_sales.csv`

Each row represents a single line item in an order.

Columns:

- `order_id`
- `order_datetime` (YYYY-MM-DD HH:MM)
- `store_id`
- `store_city`
- `item`
- `category` (sandwich, sides, drinks, etc.)
- `quantity`
- `unit_price`
- `payment_method` (cash, card, etc.)
- `order_total` (total for the whole order, repeated per line)

---

## Design

### `SaleRecord` and CSV loader (`sales_analysis.py`)

- `SaleRecord` is an immutable dataclass that models one line of the CSV.
- `parse_order_datetime` parses `order_datetime` from string to `datetime`.
- `load_sales_from_csv(path)` reads the CSV with `csv.DictReader` and returns
  a list of `SaleRecord` instances.
- `SaleRecord.line_revenue` is a convenience property that computes `quantity * unit_price`.

**Analysis functions (`sales_analysis.py`)**

All analysis functions take an `Iterable[SaleRecord]` and return aggregated
results.

- `total_revenue(records)`\
  Sum of `line_revenue` over all records, using `map` and a lambda.
- `revenue_by_city(records)`\
  Revenue grouped by `store_city`.
- `revenue_by_category(records)`\
  Revenue grouped by `category`.
- `total_quantity_by_item(records)`\
  Total units sold per `item`.
- `top_n_items_by_revenue(records, n)`\
  Top `n` items by revenue, using a `dict` of item to revenue and `sorted` with a lambda key.
- `revenue_by_payment_method(records)`\
  Revenue grouped by `payment_method`.
- `average_order_total(records)`\
  Average order total (ticket size), using `order_total` aggregated by `order_id`. Supports orders that have multiple line items.

This design keeps the model and analysis logic separate from the command line
interface. The functions are reusable from tests and from the runner.

---

## Running the analysis

From the `assignment_2/` directory:

```bash
python run_analysis.py
```

This will:

- Load `hot_chicken_sales.csv`.
- Compute all summary metrics.
- Print a formatted summary report to the console.

Example output (values will match the CSV):

```text
==================================================
         Spicy Chicken Shop Sales Summary
==================================================
Date range   : 2025-11-20 to 2025-11-21
Total orders : 12
Total revenue: $148.00
--------------------------------------------------

Revenue by city
--------------------------------------------------
Burbank                  : $     58.00
Glendale                 : $     36.00
Los Angeles              : $     54.00

Revenue by category
--------------------------------------------------
drinks                   : $      7.00
sandwich                 : $     99.00
sides                    : $     12.00
tenders                  : $     30.00

Top 5 items by revenue
--------------------------------------------------
Spicy Chicken Sandwich   : $     72.00
Spicy Tenders            : $     30.00
Chicken Sandwich         : $     27.00
Fries                    : $     12.00
Lemonade                 : $      4.00

Total quantity sold per item
--------------------------------------------------
Chicken Sandwich         :    3
Fries                    :    4
Lemonade                 :    2
Spicy Chicken Sandwich   :    6
Spicy Tenders            :    3
Vanilla Shake            :    1

Revenue by payment method
--------------------------------------------------
card                     : $    139.00
cash                     : $      9.00
--------------------------------------------------

Average order total: $12.33
==================================================
```

## Running the tests

From the `assignment_2/` directory:

```bash
python -m unittest -v
```

This runs `test_sales_analysis.py`.

**Test coverage**

- `total_revenue`
- `revenue_by_city`
- `revenue_by_category`
- `total_quantity_by_item`
- `top_n_items_by_revenue` (including case where `n` is larger than the number
  of items)
- `revenue_by_payment_method`
- `average_order_total`

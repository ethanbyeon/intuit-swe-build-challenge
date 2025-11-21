# Intuit SWE 1 - Build Challenge

This repo contains my solutions for the Intuit SWE 1 Build Challenge. \
Each assignment lives in its own directory with source code, tests, and a
`README`.

---

## Assignment 1: Producer Consumer

**Path:** `assignment_1/` \
**Language:** Python 3.10+

Implements a classic producer-consumer pattern using a bounded blocking queue
and threads in Python. The focus is on:

- Correct thread synchronization.
- A custom bounded blocking queue.
- Explicit use of `threading.Lock` and `threading.Condition` (`wait()` /
  `notify()`).

### Structure

```text
assignment_1/
    blocking_queue.py         # BoundedBlockingQueue implementation
    producer_consumer.py      # Producer-consumer pipeline and main file
    test_blocking_queue.py    # Unit tests for the queue
    test_producer_consumer.py # Unit tests for the pipeline
    README.md                 # Detailed design and usage
```

### How to run Assignment 1

From the repo root:

```bash
cd assignment_1
python producer_consumer.py
```

Run all tests:

```bash
cd assignment_1
python -m unittest -v
```

For more details on the design, blocking behavior, and test coverage,
see [assignment_1/README.md](assignment_1/README.md).

---

## Assignment 2: Sales Analysis

**Path:** `assignment_2/` \
**Language:** Python 3.10+

Performs aggregation and grouping queries over a small sales dataset for a
spicy chicken sandwich shop. The focus is on:

- CSV based data ingestion.
- Functional style analysis functions (iterables, lambdas, `map`, `sorted`).
- Grouped and aggregated business metrics.

### Structure

```text
assignment_2/
    hot_chicken_sales.csv  # Sample sales dataset
    sales_analysis.py      # Data model, CSV loader, analysis functions
    run_analysis.py        # Main file
    test_sales_analysis.py # Unit tests for all analysis functions
    README.md              # Detailed design and usage
```

### How to run Assignment 2

From the repo root:

```bash
cd assignment_2
python run_analysis.py
```

Run all tests:

```bash
cd assignment_2
python -m unittest -v
```

For more details on the design, dataset, and test coverage,
see [assignment_2/README.md](assignment_2/README.md).

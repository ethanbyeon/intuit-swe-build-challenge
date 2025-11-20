# Assignment 1: Producer Consumer

This module implements a producer-consumer pattern using a bounded
blocking queue and threads in Python, demonstrating thread synchronization and use of wait/notify primitives.

---

## Requirements

- Python 3.10+

No third party libraries are required.
Only the Python standard library is used.

---

## Project Structure

```text
assignment_1/
    blocking_queue.py         # BoundedBlockingQueue implementation
    producer_consumer.py      # Producer-consumer pipeline and main file
    test_blocking_queue.py    # Unit tests for the queue
    test_producer_consumer.py # Unit tests for the pipeline
```

---

## Design

### `BoundedBlockingQueue` (`blocking_queue.py`)

- Generic, thread safe, bounded FIFO queue.
- Fixed capacity set at initialization.
- `put(item)`: blocks when the queue is full until space is available.
- `get()`: blocks when the queue is empty until an item is available.
- Safe for multiple producer and consumer threads.

**Implementation details**

- Stores items in `collections.deque`.
- Uses one `threading.Lock` and two `threading.Condition` objects that share
  that lock:
  - `_not_empty` to block consumers when the queue is empty.
  - `_not_full` to block producers when the queue is full.
- Both `put` and `get`:
  - Call `Condition.wait()` in a `while` loop.
  - Call `Condition.notify()` after modifying the queue size.

Python provides `queue.Queue`, which is a thread safe bounded blocking queue. \
Here a custom `BoundedBlockingQueue` is implemented to explicitly
demonstrate use of `threading.Lock` and `threading.Condition`.

---

### Producer-consumer pipeline (`producer_consumer.py`)

- `producer(source: list[float], queue: BoundedBlockingQueue[float])`
  - Reads values from a source list.
  - Enqueues each value into the blocking queue.

- `consumer(num_items: int, queue: BoundedBlockingQueue[float], destination:
list[float])`
  - Dequeues exactly `num_items` values from the queue.
  - Applies `math.cos(value)`.
  - Appends results to a destination list.

- `run_pipeline(source: list[float], queue_capacity: int = 64) -> list[float]`
  - Creates a `BoundedBlockingQueue` with the given capacity.
  - Starts a producer thread and a consumer thread.
  - Waits for both threads to complete.
  - Returns the destination list of transformed values.
  - Prints a small timing summary to the console.

The pipeline mirrors a three stage flow (load, compute, store) but is
simplified to a single producer and a single consumer that share one
bounded queue.

---

## Running the example

From the `assignment_1/` directory:

```bash
python producer_consumer.py
```

This will:

- Create a list of input values.
- Run the producer-consumer pipeline with a bounded queue.
- Print timing information and an accuracy check.

Example output (timing will vary):

```bash
Processed 8192 items in 0.011018 seconds
Max absolute error vs math.cos: 0.000000e+00
```

## Running the tests

From the `assignment_1/` directory:

```bash
python -m unittest discover -v
```

Or run individual test modules:

```bash
python -m unittest -v test_blocking_queue
python -m unittest -v test_producer_consumer
```

**Test Coverage**

- `test_blocking_queue.py`
  - FIFO behavior in a single thread.
  - Capacity validation.
  - Interaction between a producer thread and a consumer thread.
  - Interaction between multiple producer threads and a consumer thread.
  - Blocking scenario that verifies `put` and `get` do not deadlock
    when the opposite side is active.
- `test_producer_consumer.py`
  - Behavior of the pipeline with an empty source list.
  - Numerical correctness: each output is approximately `math.cos(input_value)`

## Notes

I chose to implement my own bounded queue (instead of using `queue.Queue`)
so the synchronization and wait/notify logic is fully visible.

"""
Producer-consumer demo using BoundedBlockingQueue.

- Producer thread reads from a source container and enqueues items.
- Consumer thread dequeues items, applies a transformation,
  and writes them into a destination container.

This file wires together the blocking queue and worker threads and
can be used as the main entry point for Assignment 1.
"""

import math
import threading
from time import perf_counter
from typing import List

from blocking_queue import BoundedBlockingQueue


def producer(source: List[float], queue: BoundedBlockingQueue[float]) -> None:
    """
    Producer thread function.

    Reads values from the source list and enqueues them
    into the blocking queue.
    """
    for value in source:
        queue.put(value)


def consumer(
    num_items: int, queue: BoundedBlockingQueue[float], destination: List[float]
) -> None:
    """
    Consumer thread function.

    Dequeues values from the blocking queue, applies a transformation,
    and appends results to the destination list.
    """
    for _ in range(num_items):
        value = queue.get()
        transformed = math.cos(value)
        destination.append(transformed)


def run_pipeline(source: List[float], queue_capacity: int = 64) -> List[float]:
    """
    Run the producer-consumer pipeline.

    Args:
        source: Input data to process.
        queue_capacity: Maximum number of items in the queue at once.

    Returns:
        A list containing the transformed results in the same order as source.
    """
    if not source:
        return []

    queue = BoundedBlockingQueue[float](queue_capacity)
    destination: List[float] = []

    producer_thread = threading.Thread(
        target=producer, args=(source, queue), name="ProducerThread"
    )
    consumer_thread = threading.Thread(
        target=consumer, args=(len(source), queue, destination), name="ConsumerThread"
    )

    start_time = perf_counter()

    producer_thread.start()
    consumer_thread.start()

    producer_thread.join()
    consumer_thread.join()

    elapsed = perf_counter() - start_time
    print(f"Processed {len(source)} items in {elapsed:.6f} seconds")

    return destination


if __name__ == "__main__":
    size = 1024 * 8
    source_data = [0.5 + i for i in range(size)]
    results = run_pipeline(source_data, queue_capacity=128)

    max_abs_error = max(abs(a - math.cos(x)) for a, x in zip(results, source_data))
    print(f"Max absolute error vs math.cos: {max_abs_error:.6e}")

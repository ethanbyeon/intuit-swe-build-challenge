"""
Bounded blocking queue implemented with threading.Condition.

This class provides:
    - put(item): blocks when the queue is full
    - get(): blocks when the queue is empty

It is safe for multiple producer and consumer threads.
"""

from collections import deque
from threading import Condition, Lock
from typing import Deque, Generic, TypeVar

T = TypeVar("T")


class BoundedBlockingQueue(Generic[T]):
    """A thread safe bounded blocking queue backed by a deque."""

    def __init__(self, capacity: int) -> None:
        """
        Initialize the queue.

        Args:
            capacity: Maximum number of items that can be stored.
        Raises:
            ValueError: If capacity is not positive.
        """
        if capacity <= 0:
            raise ValueError("capacity must be positive")

        self._capacity: int = capacity
        self._queue: Deque[T] = deque()
        self._lock: Lock = Lock()
        # Conditions share the same underlying lock
        self._not_empty: Condition = Condition(self._lock)
        self._not_full: Condition = Condition(self._lock)

    def put(self, item: T) -> None:
        """
        Put an item into the queue.

        Blocks if the queue is full until space becomes available.
        """
        with self._not_full:
            # Wait while queue is full
            while len(self._queue) >= self._capacity:
                self._not_full.wait()

            self._queue.append(item)
            # Signal that at least one item is available
            self._not_empty.notify()

    def get(self) -> T:
        """
        Remove and return an item from the queue.

        Blocks if the queue is empty until an item is available.
        """
        with self._not_empty:
            # Wait while queue is empty
            while not self._queue:
                self._not_empty.wait()

            item = self._queue.popleft()
            # Signal that space is now available
            self._not_full.notify()
            return item

    def q_size(self) -> int:
        """Return the approximate size of the queue."""
        with self._lock:
            return len(self._queue)

    def is_empty(self) -> bool:
        """Return True if the queue is empty."""
        with self._lock:
            return len(self._queue) == 0

    def is_full(self) -> bool:
        """Return True if the queue is full."""
        with self._lock:
            return len(self._queue) >= self._capacity

    @property
    def capacity(self) -> int:
        """Return configured capacity of the queue."""
        return self._capacity

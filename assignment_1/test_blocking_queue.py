import threading
import time
import unittest

from blocking_queue import BoundedBlockingQueue


class TestBoundedBlockingQueue(unittest.TestCase):
    def test_fifo_single_thread(self) -> None:
        q = BoundedBlockingQueue[int](capacity=3)
        q.put(1)
        q.put(2)
        q.put(3)

        self.assertTrue(q.is_full())
        self.assertEqual(q.q_size(), 3)

        self.assertEqual(q.get(), 1)
        self.assertEqual(q.get(), 2)
        self.assertEqual(q.get(), 3)
        self.assertTrue(q.is_empty())

    def test_capacity_must_be_positive(self) -> None:
        with self.assertRaises(ValueError):
            BoundedBlockingQueue(0)

        with self.assertRaises(ValueError):
            BoundedBlockingQueue(-1)

    def test_producer_consumer_interaction(self) -> None:
        q = BoundedBlockingQueue[int](capacity=1)
        produced = []
        consumed = []

        def producer() -> None:
            for i in range(5):
                q.put(i)
                produced.append(i)

        def consumer() -> None:
            for _ in range(5):
                value = q.get()
                consumed.append(value)

        t_prod = threading.Thread(target=producer)
        t_cons = threading.Thread(target=consumer)

        t_prod.start()
        t_cons.start()

        # Give both threads time to run
        # If either is still active after join,
        # the queue logic likely deadlocked.
        t_prod.join(timeout=2.0)
        t_cons.join(timeout=2.0)

        self.assertEqual(produced, consumed)
        self.assertFalse(q.is_full())
        self.assertTrue(q.is_empty())

        self.assertFalse(t_prod.is_alive())
        self.assertFalse(t_cons.is_alive())

    def test_blocking_behavior_no_deadlock(self) -> None:
        """
        This test does not prove blocking semantics perfectly,
        but it checks that put() on a full queue and get() on an
        empty queue do not deadlock when the opposite side runs.
        """
        q = BoundedBlockingQueue[int](capacity=1)
        q.put(1)

        def delayed_consumer() -> None:
            # Delay to ensure the producer hits the blocking path in put()
            time.sleep(0.05)
            _ = q.get()

        t_cons = threading.Thread(target=delayed_consumer)
        t_cons.start()

        # This call should block until the consumer removes the first item
        q.put(2)

        t_cons.join(timeout=1.0)
        # If execution reaches here without timing out,
        # the blocking behavior is sane.
        self.assertEqual(q.get(), 2)

        self.assertFalse(t_cons.is_alive())

    def test_multiple_producers_single_consumer(self) -> None:
        q = BoundedBlockingQueue[int](capacity=2)
        produced = []
        consumed = []

        num_producers = 2
        items_per_producer = 5
        total_items = num_producers * items_per_producer

        def producer(start: int) -> None:
            for i in range(start, start + items_per_producer):
                q.put(i)
                produced.append(i)

        def consumer() -> None:
            for _ in range(total_items):
                consumed.append(q.get())

        t_prod = threading.Thread(target=producer, args=(0,))
        t_prod_2 = threading.Thread(target=producer, args=(100,))
        t_cons = threading.Thread(target=consumer)

        t_prod.start()
        t_prod_2.start()
        t_cons.start()

        t_prod.join()
        t_prod_2.join()
        t_cons.join()

        # Order is not guaranteed with multiple producers,
        # so compare as multisets.
        self.assertCountEqual(produced, consumed)

        self.assertFalse(t_prod.is_alive())
        self.assertFalse(t_prod_2.is_alive())
        self.assertFalse(t_cons.is_alive())


if __name__ == "__main__":
    unittest.main()

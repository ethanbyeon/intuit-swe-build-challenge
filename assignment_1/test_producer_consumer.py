import math
import unittest

from producer_consumer import run_pipeline


class TestProducerConsumerPipeline(unittest.TestCase):
    def test_empty_source(self) -> None:
        result = run_pipeline([])
        self.assertEqual(result, [])

    def test_cosine_transformation(self) -> None:
        size = 1000
        source = [0.5 + i for i in range(size)]
        result = run_pipeline(source, queue_capacity=16)

        self.assertEqual(len(result), len(source))
        for x, y in zip(source, result):
            self.assertAlmostEqual(y, math.cos(x), places=7)


if __name__ == "__main__":
    unittest.main()

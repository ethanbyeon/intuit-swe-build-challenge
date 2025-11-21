import unittest
from datetime import datetime

from sales_analysis import (SaleRecord, average_order_total,
                            revenue_by_category, revenue_by_city,
                            revenue_by_payment_method, top_n_items_by_revenue,
                            total_quantity_by_item, total_revenue)


class TestSalesAnalysis(unittest.TestCase):
    def setUp(self) -> None:
        self.records = [
            SaleRecord(
                order_id="1",
                order_datetime=datetime(2025, 11, 20, 12, 00),
                store_id="LA-01",
                store_city="Los Angeles",
                item="A",
                category="sandwich",
                quantity=2,
                unit_price=3.00,
                payment_method="card",
                order_total=6.00,
            ),
            SaleRecord(
                order_id="2",
                order_datetime=datetime(2025, 11, 20, 12, 1),
                store_id="LA-01",
                store_city="Los Angeles",
                item="B",
                category="sandwich",
                quantity=1,
                unit_price=2.00,
                payment_method="cash",
                order_total=2.00,
            ),
            SaleRecord(
                order_id="3",
                order_datetime=datetime(2025, 11, 20, 12, 2),
                store_id="LA-02",
                store_city="Glendale",
                item="C",
                category="sides",
                quantity=3,
                unit_price=3.00,
                payment_method="card",
                order_total=9.00,
            ),
        ]

    def test_total_revenue(self) -> None:
        expected = sum(r.line_revenue for r in self.records)
        self.assertAlmostEqual(total_revenue(self.records), expected, places=7)

    def test_revenue_by_city(self) -> None:
        result = revenue_by_city(self.records)

        # Los Angeles should include two orders
        la_total = self.records[0].line_revenue + self.records[1].line_revenue
        self.assertIn("Los Angeles", result)
        self.assertIn("Glendale", result)
        self.assertAlmostEqual(result["Los Angeles"], la_total, places=7)
        self.assertAlmostEqual(
            result["Glendale"], self.records[2].line_revenue, places=7
        )

    def test_revenue_by_category(self) -> None:
        result = revenue_by_category(self.records)

        sandwich_total = self.records[0].line_revenue + self.records[1].line_revenue
        sides_total = self.records[2].line_revenue

        self.assertIn("sandwich", result)
        self.assertIn("sides", result)
        self.assertAlmostEqual(result["sandwich"], sandwich_total, places=7)
        self.assertAlmostEqual(result["sides"], sides_total, places=7)

    def test_total_quantity_by_item(self) -> None:
        result = total_quantity_by_item(self.records)

        self.assertEqual(result["A"], 2)
        self.assertEqual(result["B"], 1)
        self.assertEqual(result["C"], 3)

    def test_top_n_items_by_revenue(self) -> None:
        top_two = top_n_items_by_revenue(self.records, n=2)
        # First item should be the highest revenue
        item_names = [name for name, _ in top_two]
        self.assertIn("A", item_names)
        self.assertIn("C", item_names)

    def test_top_n_items_more_than_available(self) -> None:
        # Asking for more items than exist should just return all items
        top_many = top_n_items_by_revenue(self.records, n=10)
        self.assertEqual(len(top_many), 3)

    def test_revenue_by_payment_method(self) -> None:
        result = revenue_by_payment_method(self.records)
        card_total = self.records[0].line_revenue + self.records[2].line_revenue
        cash_total = self.records[1].line_revenue

        self.assertIn("card", result)
        self.assertIn("cash", result)
        self.assertAlmostEqual(result["card"], card_total, places=7)
        self.assertAlmostEqual(result["cash"], cash_total, places=7)

    def test_average_order_total(self) -> None:
        expected = sum(r.order_total for r in self.records) / len(self.records)
        self.assertAlmostEqual(average_order_total(self.records), expected, places=7)


if __name__ == "__main__":
    unittest.main()

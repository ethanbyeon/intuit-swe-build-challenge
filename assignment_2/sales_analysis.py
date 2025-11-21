"""
Core data model and analysis functions for spicy chicken shop sales.

- Defines the SaleRecord dataclass and CSV loader.
- Provides aggregation and grouping functions over sales records.
- Uses a functional, stream-style approach (iterables, lambdas, map, sorted).
"""

from __future__ import annotations

import csv
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Iterable, List, Tuple


@dataclass(frozen=True)
class SaleRecord:
    """Single sale record parsed from the CSV file."""

    order_id: str
    order_datetime: datetime
    store_id: str
    store_city: str
    item: str
    category: str
    quantity: int
    unit_price: float
    payment_method: str
    order_total: float

    @property
    def line_revenue(self) -> float:
        """Revenue for this line (quantity * unit price)."""
        return self.quantity * self.unit_price


def parse_order_datetime(value: str) -> datetime:
    """Parse order datetime in 'YYYY-MM-DD HH:MM' format."""
    return datetime.strptime(value, "%Y-%m-%d %H:%M")


def load_sales_from_csv(path: str) -> List[SaleRecord]:
    """
    Load sales records from a CSV file.

    Args:
        path: Path to the CSV file.

    Returns:
        List of SaleRecord instances.
    """
    records: List[SaleRecord] = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            record = SaleRecord(
                order_id=row["order_id"],
                order_datetime=parse_order_datetime(row["order_datetime"]),
                store_id=row["store_id"],
                store_city=row["store_city"],
                item=row["item"],
                category=row["category"],
                quantity=int(row["quantity"]),
                unit_price=float(row["unit_price"]),
                payment_method=row["payment_method"],
                order_total=float(row["order_total"]),
            )
            records.append(record)
    return records


# --- Analysis functions ---


def total_revenue(records: Iterable[SaleRecord]) -> float:
    """Compute total revenue across all records."""
    return sum(map(lambda r: r.line_revenue, records))


def revenue_by_city(records: Iterable[SaleRecord]) -> Dict[str, float]:
    """Compute total revenue grouped by store city."""
    totals: Dict[str, float] = defaultdict(float)
    for r in records:
        totals[r.store_city] += r.line_revenue
    return dict(totals)


def revenue_by_category(records: Iterable[SaleRecord]) -> Dict[str, float]:
    """Compute total revenue grouped by category."""
    totals: Dict[str, float] = defaultdict(float)
    for r in records:
        totals[r.category] += r.line_revenue
    return dict(totals)


def total_quantity_by_item(records: Iterable[SaleRecord]) -> Dict[str, int]:
    """Compute total quantity sold per item."""
    totals: Dict[str, int] = defaultdict(int)
    for r in records:
        totals[r.item] += r.quantity
    return dict(totals)


def top_n_items_by_revenue(
    records: Iterable[SaleRecord], n: int = 3
) -> List[Tuple[str, float]]:
    """
    Return the top N items by revenue.

    Returns:
        List of (item, revenue) sorted descending by revenue.
    """
    totals: Dict[str, float] = defaultdict(float)
    for r in records:
        totals[r.item] += r.line_revenue

    sorted_items = sorted(totals.items(), key=lambda kv: kv[1], reverse=True)
    return sorted_items[:n]


def revenue_by_payment_method(records: Iterable[SaleRecord]) -> Dict[str, float]:
    """Compute total revenue grouped by payment method."""
    totals: Dict[str, float] = defaultdict(float)
    for r in records:
        totals[r.payment_method] += r.line_revenue
    return dict(totals)


def average_order_total(records: Iterable[SaleRecord]) -> float:
    """
    Compute the average order total (average ticket size).

    Uses order_total aggregated per order_id to support multi-line orders.
    """
    totals_by_order: Dict[str, float] = defaultdict(float)
    for r in records:
        # If order_total is repeated per line, this keeps the last one
        totals_by_order[r.order_id] = r.order_total

    if not totals_by_order:
        return 0.0

    total_revenue_all = sum(totals_by_order.values())
    return total_revenue_all / len(totals_by_order)

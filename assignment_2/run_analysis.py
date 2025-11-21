"""
Sales analysis for a spicy chicken sandwich shop.

- Reads sales records from a CSV file.
- Uses analysis functions from sales_analysis.
- Formats and prints a summary report to the console.
"""

from sales_analysis import (average_order_total, load_sales_from_csv,
                            revenue_by_category, revenue_by_city,
                            revenue_by_payment_method, top_n_items_by_revenue,
                            total_quantity_by_item, total_revenue)


def main() -> None:
    data_path = "hot_chicken_sales.csv"
    sales = load_sales_from_csv(data_path)

    if not sales:
        print("No sales records found.")
        return

    total = total_revenue(sales)
    total_orders = len({r.order_id for r in sales})
    first_date = min(r.order_datetime for r in sales).date()
    last_date = max(r.order_datetime for r in sales).date()

    line_width = 50

    print("=" * line_width)
    print("Spicy Chicken Shop Sales Summary".center(line_width))
    print("=" * line_width)
    print(f"Date range   : {first_date} to {last_date}")
    print(f"Total orders : {total_orders}")
    print(f"Total revenue: ${total:,.2f}")
    print("-" * line_width)

    # Revenue by city
    by_city = revenue_by_city(sales)
    print("\nRevenue by city")
    print("-" * line_width)
    for city, value in sorted(by_city.items(), key=lambda kv: kv[0]):
        # left-align label, right-align amount
        print(f"{city:<25}: ${value:10.2f}")

    # Revenue by category
    by_category = revenue_by_category(sales)
    print("\nRevenue by category")
    print("-" * line_width)
    for category, value in sorted(by_category.items(), key=lambda kv: kv[0]):
        print(f"{category:<25}: ${value:10.2f}")

    # Top N items by revenue
    top_items = top_n_items_by_revenue(sales, n=5)
    print("\nTop 5 items by revenue")
    print("-" * line_width)
    for item, value in top_items:
        print(f"{item:<25}: ${value:10.2f}")

    # Total quantity per item
    qty_by_item = total_quantity_by_item(sales)
    print("\nTotal quantity sold per item")
    print("-" * line_width)
    for item, qty in sorted(qty_by_item.items(), key=lambda kv: kv[0]):
        print(f"{item:<25}: {qty:4}")

    # Revenue by payment method
    by_payment = revenue_by_payment_method(sales)
    print("\nRevenue by payment method")
    print("-" * line_width)
    for method, value in sorted(by_payment.items(), key=lambda kv: kv[0]):
        print(f"{method:<25}: ${value:10.2f}")

    avg_order = average_order_total(sales)
    print("-" * line_width)
    print(f"\nAverage order total: ${avg_order:,.2f}")
    print("=" * line_width)


if __name__ == "__main__":
    main()

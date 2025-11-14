import sqlite3
from pathlib import Path

query = """
WITH user_order_totals AS (
    SELECT
        o.order_id,
        o.user_id,
        o.total_amount AS order_total,
        SUM(o.total_amount) OVER (PARTITION BY o.user_id) AS lifetime_spend
    FROM orders o
)
SELECT
    u.user_id,
    u.full_name AS user_name,
    o.order_id,
    o.order_date,
    p.product_name,
    p.category,
    oi.quantity,
    oi.price_per_unit,
    oi.line_total,
    uot.order_total,
    uot.lifetime_spend
FROM users u
JOIN user_order_totals uot ON u.user_id = uot.user_id
JOIN orders o ON o.order_id = uot.order_id
JOIN order_items oi ON oi.order_id = o.order_id
JOIN products p ON p.product_id = oi.product_id
ORDER BY uot.lifetime_spend DESC, o.order_date DESC;
"""

def main():
    db_path = Path(__file__).resolve().parent / "ecommerce.db"
    conn = sqlite3.connect(db_path)
    try:
        cur = conn.execute(query)
        columns = [col[0] for col in cur.description]
        print("\t".join(columns))
        for row in cur:
            print("\t".join(str(val) for val in row))
    finally:
        conn.close()

if __name__ == "__main__":
    main()

import sqlite3
from pathlib import Path

import pandas as pd


SCHEMA_SQL = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS users (
    user_id TEXT PRIMARY KEY,
    full_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    phone TEXT,
    created_at TEXT NOT NULL,
    country TEXT NOT NULL,
    gender TEXT,
    age INTEGER CHECK(age BETWEEN 13 AND 120),
    is_prime_member INTEGER NOT NULL CHECK (is_prime_member IN (0,1))
);

CREATE TABLE IF NOT EXISTS products (
    product_id TEXT PRIMARY KEY,
    product_name TEXT NOT NULL,
    category TEXT NOT NULL,
    sub_category TEXT NOT NULL,
    brand TEXT NOT NULL,
    price REAL NOT NULL CHECK(price >= 0),
    rating REAL CHECK(rating BETWEEN 0 AND 5),
    stock_quantity INTEGER NOT NULL CHECK(stock_quantity >= 0)
);

CREATE TABLE IF NOT EXISTS orders (
    order_id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    order_date TEXT NOT NULL,
    payment_method TEXT NOT NULL,
    order_status TEXT NOT NULL,
    total_amount REAL NOT NULL CHECK(total_amount >= 0),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS order_items (
    order_item_id TEXT PRIMARY KEY,
    order_id TEXT NOT NULL,
    product_id TEXT NOT NULL,
    quantity INTEGER NOT NULL CHECK(quantity > 0),
    price_per_unit REAL NOT NULL CHECK(price_per_unit >= 0),
    line_total REAL NOT NULL CHECK(line_total >= 0),
    FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

CREATE TABLE IF NOT EXISTS reviews (
    review_id TEXT PRIMARY KEY,
    product_id TEXT NOT NULL,
    user_id TEXT NOT NULL,
    rating INTEGER NOT NULL CHECK(rating BETWEEN 1 AND 5),
    review_text TEXT,
    review_date TEXT NOT NULL,
    FOREIGN KEY (product_id) REFERENCES products(product_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE INDEX IF NOT EXISTS idx_orders_user_id ON orders(user_id);
CREATE INDEX IF NOT EXISTS idx_order_items_order_id ON order_items(order_id);
CREATE INDEX IF NOT EXISTS idx_order_items_product_id ON order_items(product_id);
CREATE INDEX IF NOT EXISTS idx_reviews_product_id ON reviews(product_id);
CREATE INDEX IF NOT EXISTS idx_reviews_user_id ON reviews(user_id);
"""

CSV_FILES = {
    "users": "users.csv",
    "products": "products.csv",
    "orders": "orders.csv",
    "order_items": "order_items.csv",
    "reviews": "reviews.csv",
}


def ensure_files_exist(base_dir: Path) -> None:
    missing = [name for name, rel in CSV_FILES.items() if not (base_dir / rel).exists()]
    if missing:
        raise FileNotFoundError(f"Missing CSV files: {', '.join(missing)}")


def prepare_users(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["is_prime_member"] = (
        df["is_prime_member"]
        .astype(str)
        .str.strip()
        .str.lower()
        .map({"true": 1, "false": 0})
        .fillna(0)
        .astype(int)
    )
    df["age"] = pd.to_numeric(df["age"], errors="coerce").fillna(0).astype(int)
    return df


def prepare_products(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
    df["stock_quantity"] = pd.to_numeric(df["stock_quantity"], errors="coerce").fillna(0).astype(int)
    return df


def prepare_orders(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["total_amount"] = pd.to_numeric(df["total_amount"], errors="coerce").fillna(0.0)
    return df


def prepare_order_items(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce").fillna(0).astype(int)
    df["price_per_unit"] = pd.to_numeric(df["price_per_unit"], errors="coerce")
    df["line_total"] = pd.to_numeric(df["line_total"], errors="coerce")
    return df


def prepare_reviews(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["rating"] = pd.to_numeric(df["rating"], errors="coerce").fillna(0).astype(int)
    return df


PREP_FUNCTIONS = {
    "users": prepare_users,
    "products": prepare_products,
    "orders": prepare_orders,
    "order_items": prepare_order_items,
    "reviews": prepare_reviews,
}


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    ensure_files_exist(base_dir)

    conn = sqlite3.connect(base_dir / "ecommerce.db")
    try:
        conn.executescript(SCHEMA_SQL)
        with conn:
            for table in ["order_items", "reviews", "orders", "products", "users"]:
                conn.execute(f"DELETE FROM {table}")

            for table_name in ["users", "products", "orders", "order_items", "reviews"]:
                csv_path = base_dir / CSV_FILES[table_name]
                df = pd.read_csv(csv_path)
                prep_fn = PREP_FUNCTIONS[table_name]
                df_prepared = prep_fn(df)
                df_prepared.to_sql(table_name, conn, if_exists="append", index=False)

        print("Ingestion completed successfully")
    finally:
        conn.close()


if __name__ == "__main__":
    main()


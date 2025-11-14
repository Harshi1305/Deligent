# E-Commerce Synthetic Dataset

This workspace includes a full synthetic e-commerce dataset (2024–2025 context), a SQLite ingestion script, and a helper query runner. The pipeline covers data generation, loading, and analysis-ready querying.

## Contents
- `generate_dataset.py`: builds five CSVs (`users`, `products`, `orders`, `order_items`, `reviews`) with realistic constraints and relationships.
- `ingest_to_sqlite.py`: loads the CSVs into `ecommerce.db`, creating tables with keys, constraints, and indexes.
- `run_query.py`: executes a reporting join showing line items with per-order totals and customer lifetime spend.
- Generated CSV files and `ecommerce.db` (after running the scripts).

## Prerequisites
- Python 3.9+ with `pandas` installed.
- SQLite (bundled with Python’s `sqlite3`).
- PowerShell or another terminal.

Install dependencies (if needed):
```
pip install pandas
```

## Usage
From the project root (`C:\Users\prana\Projects\diligent_assignment_H`):

1. **Generate synthetic CSVs**
```
python generate_dataset.py
```

2. **Ingest into SQLite database**
```
python ingest_to_sqlite.py
```
Creates/updates `ecommerce.db`, enforces schema (PKs, FKs, CHECK constraints) and indexes, and prints `Ingestion completed successfully`.

3. **Run analytics query**
```
python run_query.py
```
Outputs joined data with user, order, product details, per-order totals, and lifetime spend sorted by highest spenders.

## Data Volumes
- Users: 50
- Products: 80
- Orders: 150
- Order items: 350
- Reviews: 120

All identifiers are UUIDs, and foreign keys maintain referential integrity across tables.

## Customization Tips
- Adjust category definitions, brand lists, or distribution parameters inside `generate_dataset.py` to shift the catalog mix.
- Extend `ingest_to_sqlite.py` with additional indexes or views as needed.
- Modify `run_query.py` (or draft new SQL) for alternative analytics, exporting results to CSV via pandas if desired.

## Verification
After generation and ingestion, you can validate record counts with:
```
python -c "import pandas as pd; \
[print(f, len(pd.read_csv(f))) for f in ['users.csv','products.csv','orders.csv','order_items.csv','reviews.csv']]"
```

---
Feel free to extend this dataset for dashboards, prototyping recommendation algorithms, or database performance exercises.


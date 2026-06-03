import duckdb
import pandas as pd
from pathlib import Path

DB_PATH  = Path(__file__).resolve().parent.parent / "02_data_warehouse" / "churn_dw.duckdb"
OUT_DIR  = Path(__file__).resolve().parent / "data"
OUT_DIR.mkdir(exist_ok=True)

conn = duckdb.connect(str(DB_PATH))

tables = ["fact_churn", "dim_client", "dim_compte", 
          "dim_industry", "dim_currency", "dim_closure"]

for table in tables:
    df = conn.execute(f"SELECT * FROM {table}").df()
    out = OUT_DIR / f"{table}.csv"
    df.to_csv(str(out), index=False, encoding='utf-8-sig')
    print(f"OK: {table} -> {len(df):,} lignes")

conn.close()
print("\nTous les fichiers exportes dans 03_power_bi/data/")
import duckdb
import pandas as pd
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[2] / "02_data_warehouse" / "churn_dw.duckdb"

def load_to_duckdb(df):
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    print(f"Connexion a DuckDB : {DB_PATH.name}")
    conn = duckdb.connect(str(DB_PATH))
    conn.execute("DROP TABLE IF EXISTS fact_churn")
    conn.execute("CREATE TABLE fact_churn AS SELECT * FROM df")
    count = conn.execute("SELECT COUNT(*) FROM fact_churn").fetchone()[0]
    print(f"  OK: Table fact_churn -> {count} lignes chargees")
    conn.close()
    print(f"  OK: Base sauvegardee -> {DB_PATH}")
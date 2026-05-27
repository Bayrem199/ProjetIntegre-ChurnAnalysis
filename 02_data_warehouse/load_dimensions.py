import duckdb
import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DB_PATH  = Path(__file__).resolve().parent / "churn_dw.duckdb"

def load_all_dimensions():
    conn = duckdb.connect(str(DB_PATH))
    print("Chargement des dimensions dans DuckDB...")

    # dim_client
    fact = conn.execute("SELECT * FROM fact_churn").df()

    dim_client = fact[['CUSTOMER_NO','NATIONALITY','RESIDENCE',
                        'MARITAL_STATUS','DATE_OF_BIRTH','AGE',
                        'NATURE_CLIENT','SALARY',
                        'CUST_OPENING_DATE','CUST_SENIORITY_YEARS']].drop_duplicates(subset=['CUSTOMER_NO'])
    conn.execute("DROP TABLE IF EXISTS dim_client")
    conn.execute("CREATE TABLE dim_client AS SELECT * FROM dim_client")
    print(f"  OK: dim_client -> {len(dim_client)} lignes")

    # dim_compte
    dim_compte = fact[['ACCOUNT_NO','CUSTOMER_NO','ACCOUNT_STATUS',
                        'ACCOUNT_CATEGORY','ACCOUNT_TYPE_DESC',
                        'ACCOUNTNATURE','CURRENCY','ACCT_BALANCE',
                        'ACCT_OPENING_DATE','ACCT_CLOSE_DATE',
                        'CLOSURE_REASON','BRANCH']].drop_duplicates(subset=['ACCOUNT_NO'])
    conn.execute("DROP TABLE IF EXISTS dim_compte")
    conn.execute("CREATE TABLE dim_compte AS SELECT * FROM dim_compte")
    print(f"  OK: dim_compte -> {len(dim_compte)} lignes")

    # dim_produit
    dim_produit = fact[['PRODUCT','PRODUCT_LINE','PRODUCT_GROUP',
                         'PRODUCT_STATUS','AMOUNT','LOB']].drop_duplicates()
    conn.execute("DROP TABLE IF EXISTS dim_produit")
    conn.execute("CREATE TABLE dim_produit AS SELECT * FROM dim_produit")
    print(f"  OK: dim_produit -> {len(dim_produit)} lignes")

    # dim_industry depuis fichier Excel
    dim_industry = pd.read_excel(DATA_DIR / "dim_INDUSTRY.xlsx")
    conn.execute("DROP TABLE IF EXISTS dim_industry")
    conn.execute("CREATE TABLE dim_industry AS SELECT * FROM dim_industry")
    print(f"  OK: dim_industry -> {len(dim_industry)} lignes")

    # dim_currency depuis fichier Excel
    dim_currency = pd.read_excel(DATA_DIR / "dim_CURRENCY.xlsx")
    conn.execute("DROP TABLE IF EXISTS dim_currency")
    conn.execute("CREATE TABLE dim_currency AS SELECT * FROM dim_currency")
    print(f"  OK: dim_currency -> {len(dim_currency)} lignes")

    # dim_closure depuis fichier Excel
    dim_closure = pd.read_excel(DATA_DIR / "dim_Closure_reason.xlsx")
    conn.execute("DROP TABLE IF EXISTS dim_closure")
    conn.execute("CREATE TABLE dim_closure AS SELECT * FROM dim_closure")
    print(f"  OK: dim_closure -> {len(dim_closure)} lignes")

    # Liste toutes les tables
    tables = conn.execute("SHOW TABLES").fetchdf()
    print(f"\nTables dans DuckDB :")
    for t in tables['name']:
        count = conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
        print(f"  {t:20s} -> {count:,} lignes")

    conn.close()
    print("\nData Warehouse pret !")

if __name__ == "__main__":
    load_all_dimensions()
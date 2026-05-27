import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[2] / "data"

def load_main_data():
    path = DATA_DIR / "data_churn.csv"
    print(f"Chargement de {path.name}...")
    df = pd.read_csv(path, low_memory=False)
    print(f"OK: {df.shape[0]} lignes x {df.shape[1]} colonnes")
    return df

def load_dimensions():
    dims = {
        "category": "dim_CATEGORY.ACCOUNT.xlsx",
        "closure": "dim_Closure_reason.xlsx",
        "currency": "dim_CURRENCY.xlsx",
        "dao": "dim_DAO.xlsx",
        "industry": "dim_INDUSTRY.xlsx",
        "sector": "dim_SECTOR.xlsx",
        "target": "dim_TARGET.xlsx",
        "transaction": "dim_TRANSACTION.xlsx",
    }
    result = {}
    print("Chargement des dimensions...")
    for key, filename in dims.items():
        result[key] = pd.read_excel(DATA_DIR / filename)
        print(f"  OK: {key} -> {result[key].shape[0]} lignes")
    return result
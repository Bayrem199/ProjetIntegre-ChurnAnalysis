import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from extract import load_main_data, load_dimensions
from transform import run_transform
from load import load_to_duckdb

def run_pipeline():
    print("=" * 50)
    print("   PIPELINE ETL - CHURN ANALYSIS")
    print("=" * 50)
    print("\n ETAPE 1 - EXTRACT")
    df_raw = load_main_data()
    dims   = load_dimensions()
    print("\n ETAPE 2 - TRANSFORM")
    df_clean = run_transform(df_raw)
    print("\n ETAPE 3 - LOAD")
    load_to_duckdb(df_clean)
    print("\n PIPELINE ETL TERMINE !")
    return df_clean

if __name__ == "__main__":
    df = run_pipeline()
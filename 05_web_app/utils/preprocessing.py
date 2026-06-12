import pandas as pd
import duckdb
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[2] / "02_data_warehouse" / "churn_dw.duckdb"

def load_kpis():
    conn = duckdb.connect(str(DB_PATH))
    
    total     = conn.execute("SELECT COUNT(*) FROM fact_churn").fetchone()[0]
    churners  = conn.execute("SELECT COUNT(*) FROM fact_churn WHERE CHURN=1").fetchone()[0]
    actifs    = conn.execute("SELECT COUNT(*) FROM fact_churn WHERE CHURN=0").fetchone()[0]
    taux      = round(churners / total * 100, 1)
    solde_moy = conn.execute("SELECT AVG(ACCT_BALANCE) FROM fact_churn WHERE ACCT_BALANCE IS NOT NULL").fetchone()[0]
    anciennete= conn.execute("SELECT AVG(CUST_SENIORITY_YEARS) FROM fact_churn WHERE CUST_SENIORITY_YEARS IS NOT NULL").fetchone()[0]
    
    conn.close()
    
    return {
        "total"     : total,
        "churners"  : churners,
        "actifs"    : actifs,
        "taux_churn": taux,
        "solde_moy" : round(solde_moy, 2),
        "anciennete": round(anciennete, 1)
    }
import pandas as pd
import numpy as np
import duckdb
import joblib
import warnings
warnings.filterwarnings('ignore')

from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from xgboost import XGBClassifier
from sklearn.metrics import roc_auc_score, f1_score, average_precision_score

DB_PATH    = Path(__file__).resolve().parents[2] / "02_data_warehouse" / "churn_dw.duckdb"
MODEL_PATH = Path(__file__).resolve().parents[1] / "models" / "model_final.pkl"

FEATURES = [
    'AGE', 'CUST_SENIORITY_YEARS', 'ACCT_BALANCE', 'SALARY',
    'NATURE_CLIENT', 'SCORE_KYC', 'MARITAL_STATUS',
    'CURRENCY', 'NATIONALITY', 'RESIDENCE',
    'LOB', 'INDUSTRY', 'COMPLETED_FILE'
]
TARGET = 'CHURN'

def train():
    print("📥 Chargement des données...")
    conn = duckdb.connect(str(DB_PATH))
    df = conn.execute("SELECT * FROM fact_churn").df()
    conn.close()

    df_ml = df[FEATURES + [TARGET]].copy()

    for col in ['AGE','CUST_SENIORITY_YEARS','ACCT_BALANCE','SALARY']:
        df_ml[col] = df_ml[col].fillna(df_ml[col].median())

    for col in ['NATURE_CLIENT','SCORE_KYC','MARITAL_STATUS',
                'CURRENCY','NATIONALITY','RESIDENCE','COMPLETED_FILE']:
        le = LabelEncoder()
        df_ml[col] = le.fit_transform(df_ml[col].fillna('UNKNOWN').astype(str))

    X = df_ml.drop(TARGET, axis=1)
    y = df_ml[TARGET]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y)

    print("🔄 Entraînement XGBoost...")
    model = XGBClassifier(
        n_estimators=300, max_depth=6, learning_rate=0.1,
        scale_pos_weight=(y_train==0).sum()/(y_train==1).sum(),
        random_state=42, eval_metric='logloss', verbosity=0)
    model.fit(X_train, y_train)

    y_proba = model.predict_proba(X_test)[:, 1]
    y_pred  = model.predict(X_test)

    print(f"✅ ROC-AUC : {roc_auc_score(y_test, y_proba):.4f}")
    print(f"✅ PR-AUC  : {average_precision_score(y_test, y_proba):.4f}")
    print(f"✅ F1-Score: {f1_score(y_test, y_pred):.4f}")

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    print(f"✅ Modèle sauvegardé : {MODEL_PATH.name}")

if __name__ == "__main__":
    train()
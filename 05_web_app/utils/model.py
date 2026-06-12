import joblib
import numpy as np
import pandas as pd
from pathlib import Path

# =========================
# FIX PATH FOR STREAMLIT CLOUD
# =========================
BASE_DIR = Path(__file__).resolve().parent

MODEL_PATH = BASE_DIR / "models" / "model_final.pkl"
ENCODERS_PATH = BASE_DIR / "models" / "encoders.pkl"
RISK_PATH = BASE_DIR / "models" / "clients_a_risque.csv"

# =========================
# FEATURES
# =========================
FEATURES = [
    'AGE', 'CUST_SENIORITY_YEARS', 'ACCT_BALANCE', 'SALARY',
    'NATURE_CLIENT', 'SCORE_KYC', 'MARITAL_STATUS',
    'CURRENCY', 'NATIONALITY', 'RESIDENCE',
    'LOB', 'INDUSTRY', 'COMPLETED_FILE'
]

# =========================
# LOAD FUNCTIONS
# =========================
def load_model():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"Model file not found: {MODEL_PATH}")
    return joblib.load(MODEL_PATH)


def load_encoders():
    if not ENCODERS_PATH.exists():
        raise FileNotFoundError(f"Encoders file not found: {ENCODERS_PATH}")
    return joblib.load(ENCODERS_PATH)


def load_clients_a_risque():
    if not RISK_PATH.exists():
        raise FileNotFoundError(f"Risk file not found: {RISK_PATH}")
    return pd.read_csv(RISK_PATH)

# =========================
# PREDICTION FUNCTION
# =========================
def predict(client_data: dict):
    model = load_model()
    encoders = load_encoders()

    df = pd.DataFrame([client_data])

    CAT_COLS = [
        'NATURE_CLIENT', 'SCORE_KYC', 'MARITAL_STATUS',
        'CURRENCY', 'NATIONALITY', 'RESIDENCE', 'COMPLETED_FILE'
    ]

    for col in CAT_COLS:
        le = encoders[col]
        val = df[col].iloc[0]

        if val not in le.classes_:
            val = 'UNKNOWN'

        df[col] = le.transform([val])

    proba = model.predict_proba(df[FEATURES])[0][1]
    pred = int(proba >= 0.5)

    if proba >= 0.7:
        risque = "🔴 Élevé"
    elif proba >= 0.4:
        risque = "🟠 Moyen"
    else:
        risque = "🟢 Faible"

    return {
        "probabilite": round(proba * 100, 1),
        "prediction": pred,
        "risque": risque
    }
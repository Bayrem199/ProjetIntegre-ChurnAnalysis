import joblib
import numpy as np
import pandas as pd
from pathlib import Path

MODEL_PATH   = Path(__file__).resolve().parents[2] / "04_machine_learning" / "models" / "model_final.pkl"
ENCODERS_PATH= Path(__file__).resolve().parents[2] / "04_machine_learning" / "models" / "encoders.pkl"
RISK_PATH    = Path(__file__).resolve().parents[2] / "04_machine_learning" / "models" / "clients_a_risque.csv"

FEATURES = [
    'AGE', 'CUST_SENIORITY_YEARS', 'ACCT_BALANCE', 'SALARY',
    'NATURE_CLIENT', 'SCORE_KYC', 'MARITAL_STATUS',
    'CURRENCY', 'NATIONALITY', 'RESIDENCE',
    'LOB', 'INDUSTRY', 'COMPLETED_FILE'
]

def load_model():
    return joblib.load(MODEL_PATH)

def load_encoders():
    return joblib.load(ENCODERS_PATH)

def load_clients_a_risque():
    return pd.read_csv(RISK_PATH)

def predict(client_data: dict):
    model    = load_model()
    encoders = load_encoders()

    df = pd.DataFrame([client_data])

    CAT_COLS = ['NATURE_CLIENT', 'SCORE_KYC', 'MARITAL_STATUS',
                'CURRENCY', 'NATIONALITY', 'RESIDENCE', 'COMPLETED_FILE']

    for col in CAT_COLS:
        le = encoders[col]
        val = df[col].iloc[0]
        if val not in le.classes_:
            val = 'UNKNOWN'
        df[col] = le.transform([val])

    proba = model.predict_proba(df[FEATURES])[0][1]
    pred  = int(proba >= 0.5)

    if proba >= 0.7:
        risque = "🔴 Élevé"
    elif proba >= 0.4:
        risque = "🟠 Moyen"
    else:
        risque = "🟢 Faible"

    return {
        "probabilite": round(proba * 100, 1),
        "prediction" : pred,
        "risque"     : risque
    }
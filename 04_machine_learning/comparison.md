# Comparaison des Modèles ML — Churn Analysis

## Modèles testés

| Modèle              | Accuracy | Precision | Recall | F1-Score | ROC-AUC | PR-AUC |
|---------------------|----------|-----------|--------|----------|---------|--------|
| Logistic Regression | 0.6209   | 0.6096    | 0.4800 | 0.5371   | 0.6940  | 0.6385 |
| Random Forest       | 0.8822   | 0.9341    | 0.7993 | 0.8614   | 0.9402  | 0.9479 |
| **XGBoost ✅**      | 0.8963   | 0.9319    | 0.8346 | 0.8805   | 0.9496  | 0.9562 |

## Modèle retenu : XGBoost

**Justification :**
- Meilleur ROC-AUC (0.9496) et PR-AUC (0.9562)
- Robuste aux déséquilibres via `scale_pos_weight`
- Meilleure interprétabilité via feature importance

## Top 5 Features
1. CURRENCY (0.691)
2. LOB (0.162)
3. COMPLETED_FILE (0.031)
4. ACCT_BALANCE (0.031)
5. SCORE_KYC (0.016)
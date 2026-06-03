# Documentation des Mesures DAX — Churn Analysis

## Source de données
- Fichier : `fact_churn.csv` exporté depuis DuckDB
- Lignes : 484 443 · Colonnes : 33
- Outil : Power BI Desktop

## Mesures DAX

| Mesure | Formule | Description |
|---|---|---|
| Total Clients | `COUNTROWS(fact_churn)` | Nombre total de lignes |
| Total Churners | `CALCULATE(COUNTROWS(fact_churn), fact_churn[CHURN]=1)` | Comptes clôturés |
| Total Actifs | `CALCULATE(COUNTROWS(fact_churn), fact_churn[CHURN]=0)` | Comptes actifs |
| Taux de Churn | `DIVIDE([Total Churners],[Total Clients],0)` | Ratio churn |
| Taux de Churn % | `FORMAT([Taux de Churn],"0.00%")` | Format pourcentage |
| Solde Moyen | `CALCULATE(AVERAGE(fact_churn[ACCT_BALANCE]), NOT ISBLANK(fact_churn[ACCT_BALANCE]))` | Solde moyen hors nulls |
| Salaire Moyen | `CALCULATE(AVERAGE(fact_churn[SALARY]), NOT ISBLANK(fact_churn[SALARY]))` | Salaire moyen hors nulls |
| Anciennete Moyenne | `ROUND(AVERAGE(fact_churn[CUST_SENIORITY_YEARS]),1)` | Ancienneté en années |
| Age Moyen | `ROUND(CALCULATE(AVERAGE(fact_churn[AGE]), NOT ISBLANK(fact_churn[AGE])),0)` | Âge moyen clients |
| Taux Churn Segment | `DIVIDE(CALCULATE([Total Churners]),CALCULATE([Total Clients]),0)` | Taux par segment |

## Colonne calculée
| Colonne | Formule | Description |
|---|---|---|
| AGE_GROUP | `IF(AGE<30,"<30",IF(AGE<40,"30-40",IF(AGE<50,"40-50",IF(AGE<60,"50-60","60+"))))` | Tranches d'âge |

## Pages du rapport
| Page | Contenu |
|---|---|
| Page 1 — Vue d'ensemble | KPIs globaux, évolution churn, répartition |
| Page 2 — Analyse du churn | Segmentation par nature, KYC, âge, marital |
| Page 3 — Segmentation client | Profils risque, tableau clients, churn par devise |
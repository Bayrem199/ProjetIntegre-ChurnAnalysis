# KPIs — Churn Analysis

## 1. KPIs Principaux

| KPI | Définition | Formule |
|---|---|---|
| **Taux de Churn Global** | % de comptes clôturés | `COUNT(CHURN=1) / COUNT(*) * 100` |
| **Nombre de Churners** | Total comptes clôturés | `COUNT(CHURN=1)` |
| **Nombre de Clients Actifs** | Total comptes actifs | `COUNT(CHURN=0)` |
| **Solde Moyen** | Moyenne des balances | `AVG(ACCT_BALANCE)` |
| **Salaire Moyen** | Moyenne des salaires | `AVG(SALARY)` |
| **Ancienneté Moyenne** | Années depuis ouverture | `AVG(CUST_SENIORITY_YEARS)` |

---

## 2. KPIs par Segment

| KPI | Définition | Formule |
|---|---|---|
| **Churn par Nature Client** | Taux par type (PPH, PM, PRO) | `COUNT(CHURN=1) GROUP BY NATURE_CLIENT` |
| **Churn par Score KYC** | Taux par niveau de risque | `COUNT(CHURN=1) GROUP BY SCORE_KYC` |
| **Churn par Devise** | Taux par devise du compte | `COUNT(CHURN=1) GROUP BY CURRENCY` |
| **Churn par Statut Marital** | Taux par situation familiale | `COUNT(CHURN=1) GROUP BY MARITAL_STATUS` |
| **Churn par Tranche d'âge** | Taux par groupe d'âge | `COUNT(CHURN=1) GROUP BY AGE_GROUP` |
| **Churn par Ancienneté** | Taux par années de relation | `COUNT(CHURN=1) GROUP BY SENIORITY_GROUP` |

---

## 3. KPIs Produit

| KPI | Définition | Formule |
|---|---|---|
| **Churn par Produit** | Taux par type de produit | `COUNT(CHURN=1) GROUP BY PRODUCT` |
| **Churn par Ligne Produit** | Taux par ligne | `COUNT(CHURN=1) GROUP BY PRODUCT_LINE` |
| **Montant Moyen par Produit** | Encours moyen | `AVG(AMOUNT) GROUP BY PRODUCT` |

---

## 4. KPIs Risque

| KPI | Définition | Formule |
|---|---|---|
| **Clients Haut Risque** | Score KYC H1/H2/H3 | `COUNT(*) WHERE SCORE_KYC IN ('H1','H2','H3')` |
| **Taux Churn Haut Risque** | Churn parmi H1/H2/H3 | `COUNT(CHURN=1) / COUNT(*) WHERE SCORE_KYC IN ('H1','H2','H3')` |
| **Motifs de Clôture** | Répartition des raisons | `COUNT(*) GROUP BY CLOSURE_REASON` |

---

## 5. Règles de calcul importantes

- **Churn = 1** si `ACCOUNT_STATUS = 'Closed'`
- **Churn = 0** si `ACCOUNT_STATUS = 'Active'`
- Les lignes avec `ACCOUNT_STATUS = NULL` sont **exclues** de l'analyse
- L'**ancienneté** est calculée depuis `CUST_OPENING_DATE` jusqu'au 01/01/2025
- L'**âge** est calculé comme `2025 - DATE_OF_BIRTH`
- Les `DATE_OF_BIRTH` hors de la plage **[1930-2007]** sont considérées aberrantes
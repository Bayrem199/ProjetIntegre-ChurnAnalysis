import pandas as pd
import numpy as np

def convert_dates(df):
    date_cols = ['CUST_OPENING_DATE', 'LAST_REVIEW_DATE', 'NEXT__REVIEW_DATE',
                 'ACCT_OPENING_DATE', 'ACCT_CLOSE_DATE', 'STARTDATE', 'MATURITYDATE']
    for col in date_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(
                df[col].astype(str).str.split('.').str[0],
                format='%Y%m%d', errors='coerce')
    return df

def clean_date_of_birth(df):
    df['DATE_OF_BIRTH'] = pd.to_numeric(df['DATE_OF_BIRTH'], errors='coerce')
    df.loc[(df['DATE_OF_BIRTH'] < 1930) | (df['DATE_OF_BIRTH'] > 2005), 'DATE_OF_BIRTH'] = np.nan
    df['AGE'] = 2025 - df['DATE_OF_BIRTH']
    return df

def clean_salary(df):
    p99 = df['SALARY'].quantile(0.99)
    df['SALARY'] = df['SALARY'].clip(upper=p99)
    return df

def define_churn(df):
    df = df[df['ACCOUNT_STATUS'].notna()].copy()
    df['CHURN'] = (df['ACCOUNT_STATUS'] == 'Closed').astype(int)
    return df

def compute_seniority(df):
    df['CUST_SENIORITY_YEARS'] = (
        (pd.Timestamp('2025-01-01') - df['CUST_OPENING_DATE'])
        .dt.days / 365.25).round(1)
    return df

def encode_categoricals(df):
    cat_cols = ['MARITAL_STATUS', 'NATURE_CLIENT', 'SCORE_KYC',
                'CURRENCY', 'NATIONALITY', 'RESIDENCE']
    for col in cat_cols:
        df[col] = df[col].fillna('UNKNOWN')
    return df

def select_final_columns(df):
    cols = [
        'CUSTOMER_NO', 'ACCOUNT_NO',
        'NATIONALITY', 'RESIDENCE', 'MARITAL_STATUS',
        'NATURE_CLIENT', 'SCORE_KYC', 'DATE_OF_BIRTH', 'AGE',
        'CUST_OPENING_DATE', 'CUST_SENIORITY_YEARS',
        'ACCT_OPENING_DATE', 'ACCT_CLOSE_DATE',
        'LAST_REVIEW_DATE', 'NEXT__REVIEW_DATE',
        'ACCOUNT_STATUS', 'ACCOUNT_CATEGORY',
        'ACCOUNT_TYPE_DESC', 'ACCOUNTNATURE',
        'CURRENCY', 'ACCT_BALANCE',
        'PRODUCT', 'PRODUCT_LINE', 'PRODUCT_GROUP',
        'PRODUCT_STATUS', 'AMOUNT',
        'INDUSTRY', 'SALARY', 'LOB', 'BRANCH',
        'COMPLETED_FILE', 'CLOSURE_REASON',
        'CHURN'
    ]
    cols = [c for c in cols if c in df.columns]
    return df[cols]

def run_transform(df):
    print("Transformations en cours...")
    df = convert_dates(df)
    print("  OK: Dates converties")
    df = clean_date_of_birth(df)
    print("  OK: AGE calcule")
    df = clean_salary(df)
    print("  OK: SALARY nettoye")
    df = define_churn(df)
    print(f"  OK: CHURN defini -> {df['CHURN'].sum()} churners")
    df = compute_seniority(df)
    print("  OK: Anciennete calculee")
    df = encode_categoricals(df)
    print("  OK: Categoriques nettoyes")
    df = select_final_columns(df)
    print(f"  OK: {df.shape[0]} lignes x {df.shape[1]} colonnes")
    return df
-- ============================================
-- DATA WAREHOUSE - CHURN ANALYSIS
-- Modele dimensionnel en etoile
-- ============================================

-- Table de faits principale
CREATE TABLE IF NOT EXISTS fact_churn (
    CUSTOMER_NO         VARCHAR,
    ACCOUNT_NO          VARCHAR,
    NATIONALITY         VARCHAR,
    RESIDENCE           VARCHAR,
    MARITAL_STATUS      VARCHAR,
    NATURE_CLIENT       VARCHAR,
    SCORE_KYC           VARCHAR,
    DATE_OF_BIRTH       DOUBLE,
    AGE                 DOUBLE,
    CUST_OPENING_DATE   DATE,
    CUST_SENIORITY_YEARS DOUBLE,
    ACCT_OPENING_DATE   DATE,
    ACCT_CLOSE_DATE     DATE,
    LAST_REVIEW_DATE    DATE,
    NEXT__REVIEW_DATE   DATE,
    ACCOUNT_STATUS      VARCHAR,
    ACCOUNT_CATEGORY    DOUBLE,
    ACCOUNT_TYPE_DESC   VARCHAR,
    ACCOUNTNATURE       VARCHAR,
    CURRENCY            VARCHAR,
    ACCT_BALANCE        DOUBLE,
    PRODUCT             VARCHAR,
    PRODUCT_LINE        VARCHAR,
    PRODUCT_GROUP       VARCHAR,
    PRODUCT_STATUS      VARCHAR,
    AMOUNT              DOUBLE,
    INDUSTRY            BIGINT,
    SALARY              DOUBLE,
    LOB                 BIGINT,
    BRANCH              VARCHAR,
    COMPLETED_FILE      VARCHAR,
    CLOSURE_REASON      VARCHAR,
    CHURN               BIGINT
);

-- Dimension Client
CREATE TABLE IF NOT EXISTS dim_client (
    CUSTOMER_NO          VARCHAR PRIMARY KEY,
    NATIONALITY          VARCHAR,
    RESIDENCE            VARCHAR,
    MARITAL_STATUS       VARCHAR,
    DATE_OF_BIRTH        DOUBLE,
    AGE                  DOUBLE,
    NATURE_CLIENT        VARCHAR,
    SALARY               DOUBLE,
    CUST_OPENING_DATE    DATE,
    CUST_SENIORITY_YEARS DOUBLE
);

-- Dimension Compte
CREATE TABLE IF NOT EXISTS dim_compte (
    ACCOUNT_NO        VARCHAR PRIMARY KEY,
    CUSTOMER_NO       VARCHAR,
    ACCOUNT_STATUS    VARCHAR,
    ACCOUNT_CATEGORY  DOUBLE,
    ACCOUNT_TYPE_DESC VARCHAR,
    ACCOUNTNATURE     VARCHAR,
    CURRENCY          VARCHAR,
    ACCT_BALANCE      DOUBLE,
    ACCT_OPENING_DATE DATE,
    ACCT_CLOSE_DATE   DATE,
    CLOSURE_REASON    VARCHAR,
    BRANCH            VARCHAR
);

-- Dimension Produit
CREATE TABLE IF NOT EXISTS dim_produit (
    PRODUCT        VARCHAR,
    PRODUCT_LINE   VARCHAR,
    PRODUCT_GROUP  VARCHAR,
    PRODUCT_STATUS VARCHAR,
    AMOUNT         DOUBLE,
    LOB            BIGINT
);

-- Dimension Industrie
CREATE TABLE IF NOT EXISTS dim_industry (
    industry_code  VARCHAR,
    industry_label VARCHAR
);

-- Dimension Devise
CREATE TABLE IF NOT EXISTS dim_currency (
    currency_code  VARCHAR,
    currency_label VARCHAR
);

-- Dimension Motif Cloture
CREATE TABLE IF NOT EXISTS dim_closure (
    closure_code   VARCHAR,
    closure_label  VARCHAR
);
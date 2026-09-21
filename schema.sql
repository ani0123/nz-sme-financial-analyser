-- ============================================================
--  NZ SME Financial Health Analyser
--  Database Schema — PostgreSQL
-- ============================================================

CREATE TABLE businesses (
    id              SERIAL PRIMARY KEY,
    name            VARCHAR(100)    NOT NULL,
    industry        VARCHAR(50),
    business_age    INT,
    num_employees   INT,
    created_at      TIMESTAMP       DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE financials (
    id              SERIAL PRIMARY KEY,
    business_id     INT             NOT NULL REFERENCES businesses(id) ON DELETE CASCADE,
    year            INT             NOT NULL,
    revenue         NUMERIC(15,2),
    cogs            NUMERIC(15,2),
    operating_exp   NUMERIC(15,2),
    interest_exp    NUMERIC(15,2),
    tax_paid        NUMERIC(15,2),
    net_profit      NUMERIC(15,2),
    UNIQUE (business_id, year)
);

CREATE TABLE balance_sheet (
    id              SERIAL PRIMARY KEY,
    business_id     INT             NOT NULL REFERENCES businesses(id) ON DELETE CASCADE,
    year            INT             NOT NULL,
    cash            NUMERIC(15,2),
    accounts_rec    NUMERIC(15,2),
    inventory       NUMERIC(15,2),
    current_assets  NUMERIC(15,2),
    total_assets    NUMERIC(15,2),
    current_liab    NUMERIC(15,2),
    total_debt      NUMERIC(15,2),
    total_equity    NUMERIC(15,2),
    UNIQUE (business_id, year)
);

CREATE TABLE ratios (
    id              SERIAL PRIMARY KEY,
    business_id     INT             NOT NULL REFERENCES businesses(id) ON DELETE CASCADE,
    year            INT             NOT NULL,
    gross_margin    NUMERIC(8,2),
    net_margin      NUMERIC(8,2),
    current_ratio   NUMERIC(8,2),
    quick_ratio     NUMERIC(8,2),
    debt_to_equity  NUMERIC(8,2),
    roe             NUMERIC(8,2),
    roa             NUMERIC(8,2),
    health_score    INT             CHECK (health_score BETWEEN 0 AND 100),
    calculated_at   TIMESTAMP       DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (business_id, year)
);

CREATE TABLE industry_benchmarks (
    id                  SERIAL PRIMARY KEY,
    industry            VARCHAR(50)     UNIQUE NOT NULL,
    avg_gross_margin    NUMERIC(8,2),
    avg_net_margin      NUMERIC(8,2),
    avg_current_ratio   NUMERIC(8,2),
    avg_quick_ratio     NUMERIC(8,2),
    avg_debt_to_eq      NUMERIC(8,2),
    avg_roe             NUMERIC(8,2),
    avg_roa             NUMERIC(8,2),
    data_source         VARCHAR(150),
    year_reference      INT
);

CREATE OR REPLACE VIEW v_financial_ratios AS
SELECT
    b.id                                                AS business_id,
    b.name                                              AS business_name,
    b.industry,
    b.num_employees,
    b.business_age,
    f.year,
    f.revenue,
    f.net_profit,
    bs.total_assets,
    bs.total_equity,
    bs.total_debt,
    bs.cash,
    r.health_score,
    ROUND((f.revenue - f.cogs) / NULLIF(f.revenue, 0) * 100, 2)                AS gross_margin,
    ROUND(f.net_profit / NULLIF(f.revenue, 0) * 100, 2)                        AS net_margin,
    ROUND(bs.current_assets / NULLIF(bs.current_liab, 0), 2)                   AS current_ratio,
    ROUND((bs.current_assets - bs.inventory) / NULLIF(bs.current_liab, 0), 2)  AS quick_ratio,
    ROUND(bs.total_debt / NULLIF(bs.total_equity, 0), 2)                       AS debt_to_equity,
    ROUND(bs.total_debt / NULLIF(bs.total_assets, 0) * 100, 2)                 AS debt_to_assets,
    ROUND(f.net_profit / NULLIF(bs.total_equity, 0) * 100, 2)                  AS roe,
    ROUND(f.net_profit / NULLIF(bs.total_assets, 0) * 100, 2)                  AS roa
FROM businesses b
JOIN financials    f  ON b.id = f.business_id
JOIN balance_sheet bs ON b.id = bs.business_id AND f.year = bs.year
LEFT JOIN ratios   r  ON b.id = r.business_id  AND f.year = r.year;

INSERT INTO industry_benchmarks
    (industry, avg_gross_margin, avg_net_margin, avg_current_ratio,
     avg_quick_ratio, avg_debt_to_eq, avg_roe, avg_roa, data_source, year_reference)
VALUES
    ('Hospitality / Food & Beverage', 62.5,  6.5,  1.2, 0.9, 1.4, 12.0,  6.5, 'Stats NZ AES + Xero XSBI', 2024),
    ('Construction / Trades',         32.0,  5.8,  1.5, 1.2, 1.1, 14.5,  7.2, 'Stats NZ AES',             2024),
    ('Technology',                    72.0, 14.0,  2.1, 2.0, 0.6, 18.0, 11.0, 'Stats NZ AES',             2024),
    ('Agriculture / Primary',         45.0, 11.5,  1.8, 1.1, 1.6,  9.5,  7.8, 'Stats NZ AES',             2024),
    ('Retail',                        35.0,  4.5,  1.4, 0.8, 1.2, 13.0,  6.0, 'Stats NZ AES + Xero XSBI', 2024),
    ('Professional Services',         72.0, 13.5,  1.9, 1.8, 0.5, 22.0, 14.0, 'Stats NZ AES',             2024),
    ('Transport / Logistics',         28.0,  5.2,  1.3, 1.0, 1.8, 11.0,  5.5, 'Stats NZ AES',             2024),
    ('Healthcare',                    62.0,  9.0,  1.7, 1.5, 0.8, 16.0,  9.5, 'Stats NZ AES',             2024),
    ('Manufacturing',                 38.0,  6.0,  1.6, 1.0, 1.3, 12.5,  7.0, 'Stats NZ AES',             2024);
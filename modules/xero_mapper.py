# ══════════════════════════════════════════════════════
#  xero_mapper.py
#  Maps Xero CSV export column names to our schema
#  Supports both Xero P&L and Balance Sheet exports
# ══════════════════════════════════════════════════════

import pandas as pd


# ── Xero column name mappings ─────────────────────────
# Xero uses different names — we map them to ours

XERO_PNL_MAP = {
    'Total Income':               'revenue',
    'Total Revenue':              'revenue',
    'Income':                     'revenue',
    'Cost of Sales':              'cogs',
    'Cost of Goods Sold':         'cogs',
    'Total Cost of Sales':        'cogs',
    'Operating Expenses':         'operating_exp',
    'Total Operating Expenses':   'operating_exp',
    'Expenses':                   'operating_exp',
    'Interest Expense':           'interest_exp',
    'Finance Costs':              'interest_exp',
    'Interest Paid':              'interest_exp',
    'Income Tax Expense':         'tax_paid',
    'Tax':                        'tax_paid',
    'Net Profit':                 'net_profit',
    'Net Profit / (Loss)':        'net_profit',
    'Profit for the Year':        'net_profit',
    'Net Income':                 'net_profit',
}

XERO_BS_MAP = {
    'Cash and Cash Equivalents':  'cash',
    'Cash':                       'cash',
    'Bank':                       'cash',
    'Total Bank':                 'cash',
    'Accounts Receivable':        'accounts_rec',
    'Trade Debtors':              'accounts_rec',
    'Total Current Assets':       'current_assets',
    'Inventory':                  'inventory',
    'Stock':                      'inventory',
    'Total Assets':               'total_assets',
    'Accounts Payable':           'current_liab',
    'Total Current Liabilities':  'current_liab',
    'Loans':                      'total_debt',
    'Total Liabilities':          'total_debt',
    'Total Equity':               'total_equity',
    'Equity':                     'total_equity',
    'Net Assets':                 'total_equity',
}

REQUIRED_COLS = [
    'name', 'industry', 'business_age', 'num_employees', 'year',
    'revenue', 'cogs', 'operating_exp', 'interest_exp', 'tax_paid',
    'net_profit', 'cash', 'accounts_rec', 'inventory',
    'current_assets', 'total_assets', 'current_liab',
    'total_debt', 'total_equity'
]

INDUSTRIES = [
    'Hospitality / Food & Beverage',
    'Construction / Trades',
    'Technology',
    'Agriculture / Primary',
    'Retail',
    'Professional Services',
    'Transport / Logistics',
    'Healthcare',
    'Manufacturing',
    'Other'
]


def detect_file_type(df):
    """
    Detects whether an uploaded CSV is:
    - 'template'  : our standard template format
    - 'xero'      : a Xero export
    - 'unknown'   : unrecognised format
    """
    cols = [c.strip() for c in df.columns.tolist()]

    # Check if it matches our template
    if 'revenue' in cols and 'name' in cols:
        return 'template'

    # Check if it looks like a Xero export
    xero_signals = ['Total Income', 'Total Revenue', 'Net Profit',
                    'Total Assets', 'Total Equity', 'Accounts Receivable']
    matches = sum(1 for s in xero_signals if s in cols)
    if matches >= 2:
        return 'xero'

    return 'unknown'


def map_xero_columns(df):
    """
    Renames Xero column names to our standard schema names.
    Combines PnL and Balance Sheet mappings.
    """
    combined_map = {**XERO_PNL_MAP, **XERO_BS_MAP}
    df = df.rename(columns=combined_map)
    return df


def validate_dataframe(df):
    """
    Checks that all required columns are present.
    Returns (is_valid, missing_columns, warnings)
    """
    missing  = [c for c in REQUIRED_COLS if c not in df.columns]
    warnings = []

    # Check for zero/null values in critical columns
    critical = ['revenue', 'total_assets', 'total_equity']
    for col in critical:
        if col in df.columns:
            if df[col].isnull().any() or (df[col] == 0).any():
                warnings.append(f"Warning: '{col}' contains zero or missing values.")

    is_valid = len(missing) == 0
    return is_valid, missing, warnings


def process_upload(df, business_name=None, industry=None,
                   business_age=None, num_employees=None, year=2024):
    """
    Master function — takes a raw uploaded DataFrame,
    detects its type, maps columns if needed, validates,
    and returns a clean DataFrame ready for the database.
    """
    file_type = detect_file_type(df)

    if file_type == 'xero':
        df = map_xero_columns(df)

    # If business info columns are missing (e.g. from Xero),
    # fill them from the form inputs
    if 'name' not in df.columns and business_name:
        df['name'] = business_name
    if 'industry' not in df.columns and industry:
        df['industry'] = industry
    if 'business_age' not in df.columns and business_age:
        df['business_age'] = business_age
    if 'num_employees' not in df.columns and num_employees:
        df['num_employees'] = num_employees
    if 'year' not in df.columns:
        df['year'] = year

    # Clean numeric columns
    numeric_cols = [c for c in REQUIRED_COLS
                    if c not in ['name', 'industry']]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

    is_valid, missing, warnings = validate_dataframe(df)

    return {
        'dataframe':  df,
        'file_type':  file_type,
        'is_valid':   is_valid,
        'missing':    missing,
        'warnings':   warnings
    }
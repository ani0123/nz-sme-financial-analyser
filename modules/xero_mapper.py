# ══════════════════════════════════════════════════════
#  xero_mapper.py
#  Maps Xero CSV export column names to our schema
#  Supports both Xero P&L and Balance Sheet exports
# ══════════════════════════════════════════════════════

import re

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


def _xero_label(value):
    return re.sub(r"[^a-z0-9]+", " ", str(value).casefold()).strip()


def _xero_amount(value):
    text = re.sub(r"\s|,|NZD|NZ\$|\$", "", str(value).upper()).replace("−", "-")
    if text in {"-", "–", "—"}:
        return 0.0
    if text.startswith("(") and text.endswith(")"):
        text = "-" + text[1:-1]
    if re.fullmatch(r"[+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)", text):
        return float(text)
    return None


def _xero_period(value):
    """Return a period end (year, month, day), using zeroes for a year-only label."""
    text = str(value).strip()
    year = re.fullmatch(r"(?i)(?:FY\s*)?((?:19|20)\d{2})(?:\.0)?", text)
    if year:
        return int(year.group(1)), 0, 0
    month = re.fullmatch(r"(?i)[a-z]{3,9}\s+(?:19|20)\d{2}", text)
    if month:
        date = pd.to_datetime(f"1 {text}", dayfirst=True, errors="coerce")
        if pd.notna(date):
            return date.year, date.month, date.days_in_month

    dates = re.findall(
        r"(?i)\b(?:\d{4}-\d{1,2}-\d{1,2}|\d{1,2}/\d{1,2}/\d{4}|"
        r"\d{1,2}\s+[a-z]{3,9}\s+\d{4})\b",
        text,
    )
    if dates:
        date_text = dates[-1]
        date = pd.to_datetime(date_text, dayfirst=not date_text[:4].isdigit(), errors="coerce")
        if pd.notna(date):
            return date.year, date.month, date.day
    return None


def _xero_report_periods(df, aliases, report_name):
    """Read totals from either columns or account rows and retain their period labels."""
    if df.empty:
        raise ValueError(f"The {report_name} report is empty.")
    rows = df.fillna("").astype(str).to_numpy().tolist()
    if not isinstance(df.columns, pd.RangeIndex):
        rows.insert(0, [str(column) for column in df.columns])
    labels = pd.DataFrame(rows).apply(lambda column: column.map(_xero_label))
    field_map = {_xero_label(name): field for name, field in aliases.items()}
    matches = labels.apply(lambda column: column.map(field_map).notna())
    priorities = {name: rank for rank, name in enumerate(field_map)}

    def extract(names, amounts):
        values = {}
        for name, amount in sorted(zip(names, amounts), key=lambda pair: priorities.get(pair[0], len(priorities))):
            if name in field_map:
                number = _xero_amount(amount)
                if number is not None:
                    values.setdefault(field_map[name], number)
        return values

    periods = []
    header = matches.sum(axis=1).idxmax()
    if matches.loc[header].sum() >= 2 and header < len(rows) - 1:
        # In a flat export, one row names the financial fields and each data row is a period.
        names = labels.loc[header].tolist()
        period_column = next(
            (index for index, name in enumerate(names)
             if name in {"year", "financial year", "period", "period end", "date", "as at"}),
            None,
        )
        for row in rows[header + 1:]:
            values = extract(names, row)
            if values:
                period = _xero_period(row[period_column]) if period_column is not None else None
                periods.append((period, values))
    elif matches.any().any():
        # Xero report exports place account labels down a column and amounts across periods.
        account_column = matches.sum().idxmax()
        names = labels[account_column].tolist()
        first_account = matches.index[matches[account_column]][0]
        for column in range(account_column + 1, labels.shape[1]):
            amounts = [row[column] for row in rows]
            values = extract(names, amounts)
            if not values:
                continue
            period = next(
                (date for value in reversed(amounts[:first_account]) if (date := _xero_period(value))),
                None,
            )
            periods.append((period, values))
        dated_periods = [entry for entry in periods if entry[0] is not None]
        if dated_periods:
            # Ignore undated budget, percentage and total columns next to dated actuals.
            periods = dated_periods
        elif len(periods) == 1:
            # A single-period export can put its date in the report title instead.
            period = next(
                (date for row in reversed(rows[:first_account])
                 if (date := _xero_period(row[account_column]))),
                None,
            )
            periods = [(period, periods[0][1])]

    if not periods:
        raise ValueError(f"No numeric {report_name} totals were found.")
    period_ends = [period for period, _ in periods]
    if len(period_ends) != len(set(period_ends)) or (len(periods) > 1 and None in period_ends):
        raise ValueError(f"The {report_name} needs one amount column or distinct dated period columns.")
    return periods


def map_xero_exports(pnl_df, bs_df):
    """Map the latest shared period in separate Xero reports to the CSV loader schema."""
    pnl_aliases = {
        "Total Trading Income": "revenue",
        "Total Cost of Sales": "cogs",
        "Total Direct Costs": "cogs",
        "Total Cost of Goods Sold": "cogs",
        "Gross Profit": "gross_profit",
        "Gross Profit (Loss)": "gross_profit",
        "Net Profit After Tax": "net_profit",
        "Net Profit (Loss)": "net_profit",
        "Total Operating Expenses": "operating_exp",
        "Total Expenses": "operating_exp",
        **XERO_PNL_MAP,
    }
    bs_aliases = {
        "Total Current Liabilities": "current_liabilities",
        "Current Liabilities": "current_liabilities",
        "current_liab": "current_liabilities",
        "Total Liabilities": "total_liabilities",
        "Total Debt": "total_debt",
        "Total Borrowings": "total_debt",
        "Borrowings": "total_debt",
        "Total Bank": "cash",
        "Stock on Hand": "inventory",
        "Inventories": "inventory",
        **{name: field for name, field in XERO_BS_MAP.items()
           if name not in {"Accounts Payable", "Total Current Liabilities", "Total Liabilities"}},
    }
    for aliases in (pnl_aliases, bs_aliases):
        for field in list(aliases.values()):
            aliases.setdefault(field, field)

    pnl_periods = _xero_report_periods(pnl_df, pnl_aliases, "Profit and Loss")
    bs_periods = _xero_report_periods(bs_df, bs_aliases, "Balance Sheet")
    matches = []
    for pnl_period, pnl in pnl_periods:
        for bs_period, bs in bs_periods:
            if pnl_period is None or bs_period is None:
                if len(pnl_periods) == len(bs_periods) == 1:
                    matches.append((pnl_period or bs_period, pnl, bs))
            elif pnl_period == bs_period:
                matches.append((pnl_period, pnl, bs))
            elif pnl_period[0] == bs_period[0] and (pnl_period[1] == 0 or bs_period[1] == 0):
                matches.append((max(pnl_period, bs_period), pnl, bs))
    if not matches:
        raise ValueError("The Profit and Loss and Balance Sheet do not have a matching reporting period.")
    period, pnl, bs = max(matches, key=lambda match: match[0] or (0, 0, 0))

    if "revenue" in pnl:
        if "cogs" in pnl:
            pnl.setdefault("gross_profit", round(pnl["revenue"] - pnl["cogs"], 2))
        elif "gross_profit" in pnl:
            pnl["cogs"] = round(pnl["revenue"] - pnl["gross_profit"], 2)
    if "total_assets" in bs and "total_equity" in bs:
        bs.setdefault("total_liabilities", round(bs["total_assets"] - bs["total_equity"], 2))
    if "total_liabilities" in bs:
        bs.setdefault("total_debt", bs["total_liabilities"])

    required_totals = {
        "revenue": "Total Trading Income or Total Revenue",
        "cogs": "Cost of Sales or Gross Profit",
        "net_profit": "Net Profit",
        "total_assets": "Total Assets",
        "current_assets": "Total Current Assets",
        "current_liabilities": "Total Current Liabilities",
        "total_equity": "Total Equity or Net Assets",
    }
    values = {**pnl, **bs}
    missing = [label for field, label in required_totals.items() if field not in values]
    if missing:
        raise ValueError(f"Missing or non-numeric report totals: {', '.join(missing)}.")

    mapped = {field: values[field] for field in (
        "revenue", "cogs", "gross_profit", "net_profit", "total_assets", "current_assets",
        "current_liabilities", "total_liabilities", "total_equity", "total_debt",
    )}
    mapped["current_liab"] = mapped["current_liabilities"]
    for field in ("operating_exp", "interest_exp", "tax_paid", "cash", "accounts_rec", "inventory"):
        mapped[field] = values.get(field, 0.0)
    if period is not None:
        mapped["year"] = period[0]
    return pd.DataFrame([mapped])


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
    if 'business_age' not in df.columns and business_age is not None:
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
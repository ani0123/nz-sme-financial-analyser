# ══════════════════════════════════════════════════════
#  data_loader.py
#  Reads CSV files and loads them into PostgreSQL
#  This is the ETL pipeline — Extract, Transform, Load
# ══════════════════════════════════════════════════════

import pandas as pd
from modules.db_connection import get_engine, get_connection

def load_business(name, industry, business_age, num_employees):
    """
    Inserts a single business into the businesses table.
    Returns the new business_id.
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO businesses (name, industry, business_age, num_employees)
            VALUES (%s, %s, %s, %s)
            RETURNING id
        """, (name, industry, int(business_age), int(num_employees)))
        business_id = cursor.fetchone()[0]
        conn.commit()
        print(f"✓ Business inserted: {name} (id={business_id})")
        return business_id
    except Exception as e:
        conn.rollback()
        print(f"✗ Failed to insert business: {e}")
        return None
    finally:
        cursor.close()
        conn.close()


def load_financials(business_id, year, revenue, cogs, operating_exp,
                    interest_exp, tax_paid, net_profit):
    """
    Inserts a single row into the financials table.
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO financials
                (business_id, year, revenue, cogs, operating_exp,
                 interest_exp, tax_paid, net_profit)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (business_id, int(year), float(revenue), float(cogs),
              float(operating_exp), float(interest_exp),
              float(tax_paid), float(net_profit)))
        conn.commit()
        print(f"✓ Financials inserted for business_id={business_id}")
    except Exception as e:
        conn.rollback()
        print(f"✗ Failed to insert financials: {e}")
    finally:
        cursor.close()
        conn.close()


def load_balance_sheet(business_id, year, cash, accounts_rec, inventory,
                       current_assets, total_assets, current_liab,
                       total_debt, total_equity):
    """
    Inserts a single row into the balance_sheet table.
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO balance_sheet
                (business_id, year, cash, accounts_rec, inventory,
                 current_assets, total_assets, current_liab,
                 total_debt, total_equity)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (business_id, int(year), float(cash), float(accounts_rec),
              float(inventory), float(current_assets), float(total_assets),
              float(current_liab), float(total_debt), float(total_equity)))
        conn.commit()
        print(f"✓ Balance sheet inserted for business_id={business_id}")
    except Exception as e:
        conn.rollback()
        print(f"✗ Failed to insert balance sheet: {e}")
    finally:
        cursor.close()
        conn.close()


def load_from_csv(filepath):
    """
    Master function — reads a CSV file and loads all three
    tables automatically in one go.

    Expected CSV columns:
    name, industry, business_age, num_employees, year,
    revenue, cogs, operating_exp, interest_exp, tax_paid, net_profit,
    cash, accounts_rec, inventory, current_assets, total_assets,
    current_liab, total_debt, total_equity
    """
    print(f"\nLoading data from: {filepath}")
    print("─" * 50)

    try:
        df = pd.read_csv(filepath)
        print(f"✓ CSV read successfully — {len(df)} rows found")
    except Exception as e:
        print(f"✗ Could not read CSV: {e}")
        return

    # Validate required columns exist
    required_cols = [
        'name', 'industry', 'business_age', 'num_employees', 'year',
        'revenue', 'cogs', 'operating_exp', 'interest_exp', 'tax_paid',
        'net_profit', 'cash', 'accounts_rec', 'inventory',
        'current_assets', 'total_assets', 'current_liab',
        'total_debt', 'total_equity'
    ]
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        print(f"✗ Missing columns in CSV: {missing}")
        return

    print(f"✓ All required columns present\n")

    success_count = 0
    fail_count = 0

    for _, row in df.iterrows():
        print(f"Processing: {row['name']}")

        # Step 1 — insert business, get back its ID
        business_id = load_business(
            row['name'], row['industry'],
            row['business_age'], row['num_employees']
        )
        if not business_id:
            fail_count += 1
            continue

        # Step 2 — insert financials using that ID
        load_financials(
            business_id, row['year'],
            row['revenue'], row['cogs'], row['operating_exp'],
            row['interest_exp'], row['tax_paid'], row['net_profit']
        )

        # Step 3 — insert balance sheet using that ID
        load_balance_sheet(
            business_id, row['year'],
            row['cash'], row['accounts_rec'], row['inventory'],
            row['current_assets'], row['total_assets'],
            row['current_liab'], row['total_debt'], row['total_equity']
        )

        success_count += 1
        print()

    print("─" * 50)
    print(f"Done — {success_count} businesses loaded, {fail_count} failed")


if __name__ == "__main__":
    # Test with sample CSV when run directly
    load_from_csv("data/sample_businesses.csv")
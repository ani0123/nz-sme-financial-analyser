# ══════════════════════════════════════════════════════
#  populate_ratios.py
#  Calculates health scores using the same Python logic
#  as the app and stores results in the ratios table
# ══════════════════════════════════════════════════════

from modules.db_connection import get_engine, get_connection
from modules.narrative_generator import get_ratios_for_business, calculate_health_score
import pandas as pd

def populate_ratios_table():
    """
    Loops through all businesses, calculates ratios and
    health scores using the exact same Python logic as
    the app, and stores them in the ratios table.
    """
    engine = get_engine()
    conn   = get_connection()
    cursor = conn.cursor()

    # Get all business IDs
    businesses = pd.read_sql("SELECT id, name FROM businesses ORDER BY id", engine)
    print(f"Found {len(businesses)} businesses to process\n")

    for _, row in businesses.iterrows():
        bid  = int(row['id'])
        name = row['name']

        # Get ratios from view
        ratios = get_ratios_for_business(bid, year=2024)
        if ratios is None:
            print(f"✗ No 2024 data for: {name}")
            continue

        # Calculate health score using exact same function as app
        health_score = calculate_health_score(ratios)

        # Upsert into ratios table
        try:
            cursor.execute("""
                INSERT INTO ratios 
                    (business_id, year, gross_margin, net_margin, current_ratio,
                     quick_ratio, debt_to_equity, roe, roa, health_score)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (business_id, year) 
                DO UPDATE SET
                    gross_margin   = EXCLUDED.gross_margin,
                    net_margin     = EXCLUDED.net_margin,
                    current_ratio  = EXCLUDED.current_ratio,
                    quick_ratio    = EXCLUDED.quick_ratio,
                    debt_to_equity = EXCLUDED.debt_to_equity,
                    roe            = EXCLUDED.roe,
                    roa            = EXCLUDED.roa,
                    health_score   = EXCLUDED.health_score,
                    calculated_at  = CURRENT_TIMESTAMP
            """, (
                bid, 2024,
                float(ratios['gross_margin']),
                float(ratios['net_margin']),
                float(ratios['current_ratio']),
                float(ratios['quick_ratio']),
                float(ratios['debt_to_equity']),
                float(ratios['roe']),
                float(ratios['roa']),
                health_score
            ))
            conn.commit()
            print(f"✓ {name} — Health Score: {health_score}/100")
        except Exception as e:
            conn.rollback()
            print(f"✗ Failed for {name}: {e}")

    cursor.close()
    conn.close()
    print("\nDone — ratios table populated with accurate health scores.")


if __name__ == "__main__":
    populate_ratios_table()
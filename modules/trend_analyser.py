# ══════════════════════════════════════════════════════
#  trend_analyser.py
#  Detects year-on-year ratio trends for a business
#  and generates AI commentary on what they mean
# ══════════════════════════════════════════════════════

import pandas as pd
from modules.db_connection import get_engine
from modules.ai_client import ask_claude


def get_multi_year_ratios(business_id):
    """
    Fetches ratios for all available years for a business.
    Returns a DataFrame sorted by year ascending.
    """
    engine = get_engine()
    query = f"""
        SELECT * FROM v_financial_ratios
        WHERE business_id = {business_id}
        ORDER BY year ASC
    """
    df = pd.read_sql(query, engine)
    return df


def calculate_trends(df):
    """
    Calculates year-on-year change for each ratio.
    Returns a dict of ratio trends with direction flags.
    """
    if len(df) < 2:
        return None

    ratio_cols = [
        'gross_margin', 'net_margin', 'current_ratio',
        'quick_ratio', 'debt_to_equity', 'roe', 'roa'
    ]

    trends = {}
    latest = df.iloc[-1]
    previous = df.iloc[-2]

    for col in ratio_cols:
        latest_val   = round(float(latest[col]), 2)
        previous_val = round(float(previous[col]), 2)
        change       = round(latest_val - previous_val, 2)
        pct_change   = round((change / abs(previous_val)) * 100, 1) if previous_val != 0 else 0

        # For debt_to_equity lower is better
        if col == 'debt_to_equity':
            if change < 0:   direction = 'Improving'
            elif change > 0: direction = 'Worsening'
            else:             direction = 'Stable'
        else:
            if change > 0:   direction = 'Improving'
            elif change < 0: direction = 'Worsening'
            else:             direction = 'Stable'

        trends[col] = {
            'previous':   previous_val,
            'latest':     latest_val,
            'change':     change,
            'pct_change': pct_change,
            'direction':  direction
        }

    return trends


def analyse_trends(business_id):
    """
    Main function — fetches multi-year data, calculates
    trends and generates AI commentary.
    """
    df = get_multi_year_ratios(business_id)

    if df.empty:
        print(f"✗ No data found for business_id={business_id}")
        return None

    if len(df) < 2:
        print(f"✗ Need at least 2 years of data for trend analysis.")
        print(f"  Only found data for year: {df.iloc[0]['year']}")
        return None

    business_name = df.iloc[0]['business_name']
    industry      = df.iloc[0]['industry']
    years         = df['year'].tolist()

    print(f"\nTrend Analysis: {business_name}")
    print(f"Industry: {industry}")
    print(f"Years analysed: {' → '.join(map(str, years))}")
    print("─" * 75)

    trends = calculate_trends(df)

    # Print trend table
    label_map = {
        'gross_margin':   'Gross Margin',
        'net_margin':     'Net Margin',
        'current_ratio':  'Current Ratio',
        'quick_ratio':    'Quick Ratio',
        'debt_to_equity': 'Debt to Equity',
        'roe':            'ROE',
        'roa':            'ROA',
    }
    unit_map = {
        'gross_margin': '%', 'net_margin': '%',
        'current_ratio': 'x', 'quick_ratio': 'x',
        'debt_to_equity': 'x', 'roe': '%', 'roa': '%'
    }

    print(f"{'Ratio':<18} {str(years[0]):>8} {str(years[-1]):>8} {'Change':>8}  {'Trend'}")
    print("─" * 75)

    improving = []
    worsening = []

    for col, label in label_map.items():
        t    = trends[col]
        unit = unit_map[col]
        arrow = '↑' if t['direction'] == 'Improving' else ('↓' if t['direction'] == 'Worsening' else '→')
        print(
            f"{label:<18} "
            f"{str(t['previous'])+unit:>8} "
            f"{str(t['latest'])+unit:>8} "
            f"{('+' if t['change'] > 0 else '')+str(t['change'])+unit:>8}  "
            f"{arrow} {t['direction']}"
        )
        if t['direction'] == 'Improving': improving.append(label)
        if t['direction'] == 'Worsening': worsening.append(label)

    print("─" * 75)
    print(f"Improving: {len(improving)} ratios  |  Worsening: {len(worsening)} ratios")

    # Build trend summary for AI
    trend_summary = []
    for col, label in label_map.items():
        t    = trends[col]
        unit = unit_map[col]
        trend_summary.append(
            f"{label}: {t['previous']}{unit} → {t['latest']}{unit} "
            f"({'+' if t['change'] > 0 else ''}{t['change']}{unit}, {t['direction']})"
        )

    prompt = f"""You are a NZ financial analyst reviewing year-on-year performance trends.
Provide a 2 paragraph commentary on this business's trajectory. Be direct and specific.

Business: {business_name}
Industry: {industry}
Period: {years[0]} to {years[-1]}

Ratio Trends:
{chr(10).join(trend_summary)}

Paragraph 1 — Overall trajectory: is the business improving or deteriorating?
Paragraph 2 — Most critical trend to watch and recommended action

Keep it under 120 words. Be direct and NZ-specific."""

    print(f"\nAI Trend Commentary:")
    print("─" * 75)
    commentary = ask_claude(prompt, max_tokens=250)
    print(commentary)
    print("─" * 75)

    return {
        "business_name": business_name,
        "industry":      industry,
        "years":         years,
        "trends":        trends,
        "commentary":    commentary
    }


if __name__ == "__main__":
    # Test with Harbour View Café — should show improvement
    analyse_trends(business_id=1)
    print("\n")
    # Test with FinSpark — should show deeper distress
    analyse_trends(business_id=10)
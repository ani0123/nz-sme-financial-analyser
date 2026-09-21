# ══════════════════════════════════════════════════════
#  narrative_generator.py
#  Fetches ratios from DB and generates AI CFO narrative
# ══════════════════════════════════════════════════════

import pandas as pd
from modules.db_connection import get_engine
from modules.ai_client import ask_claude


def get_ratios_for_business(business_id, year=2024):
    """
    Fetches all calculated ratios for a business
    directly from the v_financial_ratios view.
    """
    engine = get_engine()
    query = f"""
        SELECT * FROM v_financial_ratios
        WHERE business_id = {business_id}
        AND year = {year}
    """
    df = pd.read_sql(query, engine)
    if df.empty:
        return None
    return df.iloc[0]


def calculate_health_score(ratios):
    """
    Calculates a health score out of 100
    based on the 7 financial ratios.
    """
    score = 50

    # Profitability
    if ratios['gross_margin'] >= 50:   score += 8
    elif ratios['gross_margin'] >= 25: score += 3
    else:                               score -= 5

    if ratios['net_margin'] >= 10:   score += 8
    elif ratios['net_margin'] >= 0:  score += 2
    else:                             score -= 12

    # Liquidity
    if ratios['current_ratio'] >= 2:   score += 10
    elif ratios['current_ratio'] >= 1.2: score += 5
    else:                                score -= 10

    # Leverage
    if ratios['debt_to_equity'] < 0.5:  score += 6
    elif ratios['debt_to_equity'] < 1.5: score += 2
    else:                                 score -= 8

    # Returns
    if ratios['roe'] >= 15: score += 5
    if ratios['roa'] >= 10: score += 5

    return max(5, min(98, round(score)))


def generate_cfo_narrative(business_id, year=2024):
    """
    Main function — fetches ratios and generates
    a full AI CFO narrative for a business.
    """
    # Step 1 — get ratios from database
    ratios = get_ratios_for_business(business_id, year)
    if ratios is None:
        print(f"✗ No data found for business_id={business_id}")
        return None

    # Step 2 — calculate health score
    health_score = calculate_health_score(ratios)

    # Step 3 — build the prompt
    prompt = f"""You are a senior CFO advisor specialising in New Zealand SMEs. 
Analyse this business and provide a concise, plain-English financial health narrative in 3 paragraphs.
Be direct, specific, and use NZ business context where relevant.

Business: {ratios['business_name']}
Industry: {ratios['industry']}
Year: {year}
Health Score: {health_score}/100

Financial Ratios:
- Gross Margin: {ratios['gross_margin']}%
- Net Margin: {ratios['net_margin']}%
- Current Ratio: {ratios['current_ratio']}
- Quick Ratio: {ratios['quick_ratio']}
- Debt to Equity: {ratios['debt_to_equity']}
- Return on Equity (ROE): {ratios['roe']}%
- Return on Assets (ROA): {ratios['roa']}%

Paragraph 1 — Overall assessment of financial health
Paragraph 2 — Key strengths and risks
Paragraph 3 — What this business should focus on in the next 6-12 months

Reference NZ market context where relevant (NZ interest rates, IRD obligations, 
NZ SME benchmarks). Keep it under 250 words total."""

    # Step 4 — call Claude
    print(f"\nGenerating AI analysis for: {ratios['business_name']}")
    print("─" * 50)
    narrative = ask_claude(prompt, max_tokens=500)

    # Step 5 — print results
    print(f"Business:     {ratios['business_name']}")
    print(f"Industry:     {ratios['industry']}")
    print(f"Health Score: {health_score}/100")
    print(f"\nKey Ratios:")
    print(f"  Gross Margin:    {ratios['gross_margin']}%")
    print(f"  Net Margin:      {ratios['net_margin']}%")
    print(f"  Current Ratio:   {ratios['current_ratio']}")
    print(f"  Debt to Equity:  {ratios['debt_to_equity']}")
    print(f"  ROE:             {ratios['roe']}%")
    print(f"\nAI CFO Narrative:")
    print("─" * 50)
    print(narrative)
    print("─" * 50)

    return {
        "business_name": ratios['business_name'],
        "industry":      ratios['industry'],
        "health_score":  health_score,
        "ratios":        ratios.to_dict(),
        "narrative":     narrative
    }


if __name__ == "__main__":
    # Test with Harbour View Café (business_id=1)
    generate_cfo_narrative(business_id=1)
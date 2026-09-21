# ══════════════════════════════════════════════════════
#  benchmarker.py
#  Compares a business's ratios against NZ industry
#  averages from the industry_benchmarks table
# ══════════════════════════════════════════════════════

import pandas as pd
from modules.db_connection import get_engine
from modules.ai_client import ask_claude


def get_industry_benchmark(industry):
    """
    Fetches the NZ average ratios for a given industry.
    """
    engine = get_engine()
    query = f"""
        SELECT * FROM industry_benchmarks
        WHERE industry = '{industry}'
    """
    df = pd.read_sql(query, engine)
    if df.empty:
        return None
    return df.iloc[0]


def compare_to_benchmark(business_id, year=2024):
    """
    Compares a business's ratios to its NZ industry average.
    Returns a detailed comparison with gap analysis.
    """
    engine = get_engine()

    # Get business ratios from view
    query = f"""
        SELECT * FROM v_financial_ratios
        WHERE business_id = {business_id}
        AND year = {year}
    """
    df = pd.read_sql(query, engine)
    if df.empty:
        print(f"✗ No data found for business_id={business_id}")
        return None

    ratios    = df.iloc[0]
    benchmark = get_industry_benchmark(ratios['industry'])

    if benchmark is None:
        print(f"✗ No benchmark found for industry: {ratios['industry']}")
        return None

    # Build comparison for each ratio
    comparisons = []
    ratio_pairs = [
        ('Gross Margin',   'gross_margin',   'avg_gross_margin',   '%'),
        ('Net Margin',     'net_margin',     'avg_net_margin',     '%'),
        ('Current Ratio',  'current_ratio',  'avg_current_ratio',  'x'),
        ('Quick Ratio',    'quick_ratio',    'avg_quick_ratio',    'x'),
        ('Debt to Equity', 'debt_to_equity', 'avg_debt_to_eq',     'x'),
        ('ROE',            'roe',            'avg_roe',            '%'),
        ('ROA',            'roa',            'avg_roa',            '%'),
    ]

    for label, biz_col, bench_col, unit in ratio_pairs:
        biz_val   = round(float(ratios[biz_col]), 2)
        bench_val = round(float(benchmark[bench_col]), 2)
        gap       = round(biz_val - bench_val, 2)

        # For debt_to_equity lower is better
        if biz_col == 'debt_to_equity':
            if gap < 0:   status = 'Better than average'
            elif gap == 0: status = 'On average'
            else:          status = 'Worse than average'
        else:
            if gap > 0:   status = 'Above average'
            elif gap == 0: status = 'On average'
            else:          status = 'Below average'

        comparisons.append({
            'ratio':     label,
            'business':  biz_val,
            'benchmark': bench_val,
            'gap':       gap,
            'unit':      unit,
            'status':    status
        })

    # Print comparison table
    print(f"\nBenchmark Comparison: {ratios['business_name']}")
    print(f"Industry: {ratios['industry']}")
    print("─" * 70)
    print(f"{'Ratio':<18} {'Business':>10} {'NZ Average':>12} {'Gap':>8}  {'Status'}")
    print("─" * 70)

    for c in comparisons:
        unit = c['unit']
        print(
            f"{c['ratio']:<18} "
            f"{str(c['business'])+unit:>10} "
            f"{str(c['benchmark'])+unit:>12} "
            f"{str(c['gap'])+unit:>8}  "
            f"{c['status']}"
        )

    print("─" * 70)

    # Generate AI benchmark commentary
    above = [c for c in comparisons if 'Above' in c['status'] or 'Better' in c['status']]
    below = [c for c in comparisons if 'Below' in c['status'] or 'Worse' in c['status']]

    prompt = f"""You are a NZ business analyst. Compare this SME's performance against 
its NZ industry average and give a 2 paragraph commentary. Be specific about the gaps.

Business: {ratios['business_name']}
Industry: {ratios['industry']}

Above industry average: {', '.join([c['ratio'] + ' (gap: +' + str(c['gap']) + c['unit'] + ')' for c in above])}
Below industry average: {', '.join([c['ratio'] + ' (gap: ' + str(c['gap']) + c['unit'] + ')' for c in below])}

Paragraph 1 — Where this business outperforms its NZ industry peers
Paragraph 2 — Where it underperforms and what to do about it

Keep it under 150 words. Be direct and NZ-specific."""

    print(f"\nAI Benchmark Commentary:")
    print("─" * 70)
    commentary = ask_claude(prompt, max_tokens=300)
    print(commentary)
    print("─" * 70)

    return {
        "business_name": ratios['business_name'],
        "industry":      ratios['industry'],
        "comparisons":   comparisons,
        "commentary":    commentary
    }


if __name__ == "__main__":
    # Test with Wellington Legal Partners (business_id=6)
    # Professional services — should be strong performer
    compare_to_benchmark(business_id=6)
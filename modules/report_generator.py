# ══════════════════════════════════════════════════════
#  report_generator.py
#  Generates a professional PDF financial health report
#  combining all AI analysis outputs
# ══════════════════════════════════════════════════════

from fpdf import FPDF, XPos, YPos
from datetime import date
from modules.narrative_generator import generate_cfo_narrative, calculate_health_score, get_ratios_for_business
from modules.benchmarker import compare_to_benchmark
from modules.trend_analyser import analyse_trends


def clean_text(text):
    """Remove characters unsupported by FPDF latin-1 encoding."""
    if not text:
        return ''
    return (text
        .replace('\u2014', '-')
        .replace('\u2013', '-')
        .replace('\u2018', "'")
        .replace('\u2019', "'")
        .replace('\u201c', '"')
        .replace('\u201d', '"')
        .replace('\u2026', '...')
        .replace('\u2192', '->')
        .replace('\u2191', '^')
        .replace('\u2193', 'v')
        .replace('#', '')
        .replace('**', '')
        .replace('*', '')
    )


class SMEReport(FPDF):
    """Custom PDF class with header and footer."""

    def header(self):
        self.set_font('Helvetica', 'B', 10)
        self.set_fill_color(24, 95, 165)
        self.set_text_color(255, 255, 255)
        self.rect(0, 0, 210, 14, 'F')
        self.set_y(3)
        self.cell(0, 8, 'NZ SME Financial Health Analyser', align='C')
        self.set_text_color(0, 0, 0)
        self.ln(14)

    def footer(self):
        self.set_y(-12)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 8,
            f'Generated {date.today().strftime("%d %B %Y")}  |  '
            f'For internal use only  |  Page {self.page_no()}',
            align='C')


def score_color(score):
    if score >= 75: return (29, 158, 117)
    if score >= 50: return (186, 117, 23)
    return (163, 45, 45)

def score_label(score):
    if score >= 75: return 'Healthy'
    if score >= 50: return 'Moderate'
    return 'At Risk'

def cell(pdf, w, h, txt, **kwargs):
    """Wrapper that auto-cleans text before every cell call."""
    pdf.cell(w, h, clean_text(str(txt)), **kwargs)

def mcell(pdf, w, h, txt, **kwargs):
    """Wrapper that auto-cleans text before every multi_cell call."""
    pdf.multi_cell(w, h, clean_text(str(txt)), **kwargs)


def generate_report(business_id, year=2024, output_dir='outputs'):
    """
    Generates a full PDF report for a business.
    Saves to outputs/ folder and returns the file path.
    """
    print(f"\nGenerating PDF report for business_id={business_id}...")

    # ── Gather all data ──────────────────────────────
    ratios = get_ratios_for_business(business_id, year)
    if ratios is None:
        print("No data found.")
        return None

    health_score  = calculate_health_score(ratios)
    analysis      = generate_cfo_narrative(business_id, year)
    benchmark     = compare_to_benchmark(business_id, year)
    trends        = analyse_trends(business_id)
    business_name = ratios['business_name']
    industry      = ratios['industry']

    print(f"\nBuilding PDF for: {business_name}")

    # ── Build PDF ────────────────────────────────────
    pdf = SMEReport()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_margins(15, 20, 15)

    # ── COVER SECTION ────────────────────────────────
    pdf.set_font('Helvetica', 'B', 20)
    pdf.set_text_color(24, 95, 165)
    pdf.ln(4)
    cell(pdf, 0, 10, business_name,
         new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')

    pdf.set_font('Helvetica', '', 11)
    pdf.set_text_color(100, 100, 100)
    cell(pdf, 0, 6, f'{industry}  |  Financial Year {year}',
         new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
    pdf.ln(6)

    col = score_color(health_score)
    pdf.set_fill_color(*col)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font('Helvetica', 'B', 13)
    cell(pdf, 0, 10,
         f'Health Score: {health_score}/100  -  {score_label(health_score)}',
         new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C', fill=True)
    pdf.set_text_color(0, 0, 0)
    pdf.ln(6)

    # ── SECTION 1: Key Ratios ────────────────────────
    pdf.set_font('Helvetica', 'B', 12)
    pdf.set_fill_color(230, 241, 251)
    cell(pdf, 0, 8, '  1.  Key Financial Ratios',
         new_x=XPos.LMARGIN, new_y=YPos.NEXT, fill=True)
    pdf.ln(2)

    ratio_data = [
        ('Gross Margin',   f"{ratios['gross_margin']}%"),
        ('Net Margin',     f"{ratios['net_margin']}%"),
        ('Current Ratio',  f"{ratios['current_ratio']}x"),
        ('Quick Ratio',    f"{ratios['quick_ratio']}x"),
        ('Debt to Equity', f"{ratios['debt_to_equity']}x"),
        ('ROE',            f"{ratios['roe']}%"),
        ('ROA',            f"{ratios['roa']}%"),
    ]

    col_w = 87
    pdf.set_font('Helvetica', '', 10)
    for i, (label, value) in enumerate(ratio_data):
        fill = i % 2 == 0
        pdf.set_fill_color(245, 245, 242)
        cell(pdf, col_w, 7, f'  {label}', border=0, fill=fill)
        pdf.set_font('Helvetica', 'B', 10)
        cell(pdf, col_w, 7, f'  {value}', border=0, fill=fill,
             new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.set_font('Helvetica', '', 10)
    pdf.ln(4)

    # ── SECTION 2: Benchmark Comparison ─────────────
    pdf.set_font('Helvetica', 'B', 12)
    pdf.set_fill_color(230, 241, 251)
    cell(pdf, 0, 8, '  2.  NZ Industry Benchmark Comparison',
         new_x=XPos.LMARGIN, new_y=YPos.NEXT, fill=True)
    pdf.ln(2)

    if benchmark and benchmark.get('comparisons'):
        pdf.set_font('Helvetica', 'B', 9)
        pdf.set_fill_color(24, 95, 165)
        pdf.set_text_color(255, 255, 255)
        cell(pdf, 55, 7, '  Ratio',    fill=True)
        cell(pdf, 35, 7, 'Business',   fill=True, align='C')
        cell(pdf, 35, 7, 'NZ Average', fill=True, align='C')
        cell(pdf, 30, 7, 'Gap',        fill=True, align='C')
        cell(pdf, 0,  7, 'Status',     fill=True,
             new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.set_text_color(0, 0, 0)

        pdf.set_font('Helvetica', '', 9)
        for i, c in enumerate(benchmark['comparisons']):
            fill = i % 2 == 0
            pdf.set_fill_color(245, 245, 242)
            u       = c['unit']
            gap_str = ('+' if c['gap'] > 0 else '') + str(c['gap']) + u

            if 'Above' in c['status'] or 'Better' in c['status']:
                pdf.set_text_color(29, 158, 117)
            elif 'Below' in c['status'] or 'Worse' in c['status']:
                pdf.set_text_color(163, 45, 45)
            else:
                pdf.set_text_color(0, 0, 0)

            cell(pdf, 55, 6, f"  {c['ratio']}", fill=fill)
            pdf.set_text_color(0, 0, 0)
            cell(pdf, 35, 6, f"{c['business']}{u}",  fill=fill, align='C')
            cell(pdf, 35, 6, f"{c['benchmark']}{u}", fill=fill, align='C')
            cell(pdf, 30, 6, gap_str,                 fill=fill, align='C')

            if 'Above' in c['status'] or 'Better' in c['status']:
                pdf.set_text_color(29, 158, 117)
            elif 'Below' in c['status'] or 'Worse' in c['status']:
                pdf.set_text_color(163, 45, 45)

            cell(pdf, 0, 6, c['status'], fill=fill,
                 new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.set_text_color(0, 0, 0)

        pdf.ln(3)
        pdf.set_font('Helvetica', '', 9)
        pdf.set_text_color(100, 100, 100)
        mcell(pdf, 0, 5, benchmark.get('commentary', ''))
        pdf.set_text_color(0, 0, 0)

    pdf.ln(4)

    # ── SECTION 3: Trend Analysis ────────────────────
    pdf.set_font('Helvetica', 'B', 12)
    pdf.set_fill_color(230, 241, 251)
    cell(pdf, 0, 8, '  3.  Year-on-Year Trend Analysis',
         new_x=XPos.LMARGIN, new_y=YPos.NEXT, fill=True)
    pdf.ln(2)

    if trends and trends.get('trends'):
        label_map = {
            'gross_margin':   'Gross Margin',
            'net_margin':     'Net Margin',
            'current_ratio':  'Current Ratio',
            'quick_ratio':    'Quick Ratio',
            'debt_to_equity': 'Debt to Equity',
            'roe':            'ROE',
            'roa':            'ROA'
        }
        unit_map = {
            'gross_margin': '%', 'net_margin': '%',
            'current_ratio': 'x', 'quick_ratio': 'x',
            'debt_to_equity': 'x', 'roe': '%', 'roa': '%'
        }
        years = trends['years']

        pdf.set_font('Helvetica', 'B', 9)
        pdf.set_fill_color(24, 95, 165)
        pdf.set_text_color(255, 255, 255)
        cell(pdf, 55, 7, '  Ratio',        fill=True)
        cell(pdf, 30, 7, str(years[0]),    fill=True, align='C')
        cell(pdf, 30, 7, str(years[-1]),   fill=True, align='C')
        cell(pdf, 30, 7, 'Change',         fill=True, align='C')
        cell(pdf, 0,  7, 'Direction',      fill=True,
             new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.set_text_color(0, 0, 0)

        pdf.set_font('Helvetica', '', 9)
        for i, (col, label) in enumerate(label_map.items()):
            t    = trends['trends'][col]
            unit = unit_map[col]
            fill = i % 2 == 0
            pdf.set_fill_color(245, 245, 242)
            change_str = ('+' if t['change'] > 0 else '') + str(t['change']) + unit
            direction  = 'Improving' if t['direction'] == 'Improving' else (
                         'Worsening' if t['direction'] == 'Worsening' else 'Stable')

            if t['direction'] == 'Improving':
                pdf.set_text_color(29, 158, 117)
            elif t['direction'] == 'Worsening':
                pdf.set_text_color(163, 45, 45)

            cell(pdf, 55, 6, f"  {label}", fill=fill)
            pdf.set_text_color(0, 0, 0)
            cell(pdf, 30, 6, f"{t['previous']}{unit}", fill=fill, align='C')
            cell(pdf, 30, 6, f"{t['latest']}{unit}",   fill=fill, align='C')
            cell(pdf, 30, 6, change_str,                fill=fill, align='C')

            if t['direction'] == 'Improving':
                pdf.set_text_color(29, 158, 117)
            elif t['direction'] == 'Worsening':
                pdf.set_text_color(163, 45, 45)

            cell(pdf, 0, 6, direction, fill=fill,
                 new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.set_text_color(0, 0, 0)

        pdf.ln(3)
        if trends.get('commentary'):
            pdf.set_font('Helvetica', '', 9)
            pdf.set_text_color(100, 100, 100)
            mcell(pdf, 0, 5, trends['commentary'])
            pdf.set_text_color(0, 0, 0)
    else:
        pdf.set_font('Helvetica', 'I', 9)
        pdf.set_text_color(100, 100, 100)
        cell(pdf, 0, 6,
             '  Only one year of data - trend analysis requires 2+ years.',
             new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.set_text_color(0, 0, 0)

    pdf.ln(4)

    # ── SECTION 4: AI CFO Narrative ──────────────────
    pdf.set_font('Helvetica', 'B', 12)
    pdf.set_fill_color(230, 241, 251)
    cell(pdf, 0, 8, '  4.  AI CFO Narrative',
         new_x=XPos.LMARGIN, new_y=YPos.NEXT, fill=True)
    pdf.ln(2)
    pdf.set_font('Helvetica', '', 9)
    pdf.set_text_color(60, 60, 60)
    if analysis and analysis.get('narrative'):
        mcell(pdf, 0, 5, analysis['narrative'])
    pdf.set_text_color(0, 0, 0)
    pdf.ln(4)

    # ── DISCLAIMER ───────────────────────────────────
    pdf.set_font('Helvetica', 'I', 7)
    pdf.set_text_color(150, 150, 150)
    pdf.set_fill_color(245, 245, 242)
    mcell(pdf, 0, 4,
        'Disclaimer: This report is generated by an AI-powered tool for '
        'indicative purposes only. It does not constitute financial advice. '
        'Please consult a qualified NZ financial advisor or accountant '
        'before making business decisions.',
        fill=True)

    # ── Save PDF ─────────────────────────────────────
    safe_name = business_name.replace(' ', '_').replace('/', '-')
    filename  = f"{output_dir}/{safe_name}_{year}_report.pdf"
    pdf.output(filename)
    print(f"\n✓ PDF report saved: {filename}")
    return filename


if __name__ == "__main__":
    generate_report(business_id=1)
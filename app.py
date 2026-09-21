# ══════════════════════════════════════════════════════
#  app.py
#  NZ SME Financial Health Analyser
#  Main Streamlit application entry point
# ══════════════════════════════════════════════════════

import streamlit as st

# ── Page config — must be first Streamlit command ────
st.set_page_config(
    page_title="NZ SME Financial Health Analyser",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ───────────────────────────────────────
st.markdown("""
<style>
    .main-header {
        font-size: 2rem;
        font-weight: 700;
        color: #185FA5;
        margin-bottom: 0.25rem;
    }
    .sub-header {
        font-size: 1rem;
        color: #666360;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: #F7F6F2;
        border: 1px solid #E3E1DA;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
    }
    .section-header {
        font-size: 1.1rem;
        font-weight: 600;
        color: #185FA5;
        border-bottom: 2px solid #E6F1FB;
        padding-bottom: 0.5rem;
        margin-bottom: 1rem;
    }
    .health-score-healthy  { color: #1D9E75; font-size: 2.5rem; font-weight: 700; }
    .health-score-moderate { color: #BA7517; font-size: 2.5rem; font-weight: 700; }
    .health-score-risk     { color: #A32D2D; font-size: 2.5rem; font-weight: 700; }
        .flag-danger  { background: #FCEBEB; border-left: 4px solid #A32D2D; padding: 0.5rem 1rem; border-radius: 4px; margin-bottom: 0.5rem; color: #791F1F; }
    .flag-warning { background: #FAEEDA; border-left: 4px solid #BA7517; padding: 0.5rem 1rem; border-radius: 4px; margin-bottom: 0.5rem; color: #633806; }
    .flag-success { background: #EAF3DE; border-left: 4px solid #1D9E75; padding: 0.5rem 1rem; border-radius: 4px; margin-bottom: 0.5rem; color: #27500A; }
    .stButton > button {
        background-color: #185FA5;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 2rem;
        font-weight: 600;
        width: 100%;
    }
    .stButton > button:hover { background-color: #0C447C; }
</style>
""", unsafe_allow_html=True)


# ── Sidebar ──────────────────────────────────────────
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/Flag_of_New_Zealand.svg/320px-Flag_of_New_Zealand.svg.png",
             width=80)
    st.markdown("## NZ SME Analyser")
    st.markdown("*AI-powered financial health analysis for New Zealand businesses*")
    st.divider()

    page = st.radio(
        "Navigation",
        ["🏠 Home", "📊 Analyse a Business", "📈 Benchmarks", "ℹ️ About"],
        label_visibility="collapsed"
    )

    st.divider()
    st.markdown("**Data sources**")
    st.markdown("- Stats NZ Annual Enterprise Survey")
    st.markdown("- Xero Small Business Insights NZ")
    st.markdown("- RBNZ Financial Stability Reports")
    st.caption("Benchmarks last updated: 2024")


# ── Pages ────────────────────────────────────────────
if page == "🏠 Home":
    st.markdown('<div class="main-header">NZ SME Financial Health Analyser</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">AI-powered financial analysis for New Zealand small and medium businesses</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h2 style="color:#185FA5;">550,000+</h2>
            <p style="color:#666360;">NZ SMEs</p>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h2 style="color:#1D9E75;">7</h2>
            <p style="color:#666360;">Financial ratios analysed</p>
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h2 style="color:#534AB7;">9</h2>
            <p style="color:#666360;">NZ industries benchmarked</p>
        </div>""", unsafe_allow_html=True)

    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### What this tool does")
        st.markdown("""
        - 📥 Upload your financial data (CSV or Xero export)
        - 🔢 Calculates 7 key financial ratios instantly
        - 🏆 Compares you against NZ industry averages
        - 🤖 Generates an AI CFO-level narrative
        - 📈 Tracks year-on-year trends
        - 📄 Downloads a professional PDF report
        """)
    with col2:
        st.markdown("### Who is this for?")
        st.markdown("""
        - **SME owners** wanting a free financial health check
        - **Accountants** looking for fast client assessments
        - **Banks & lenders** doing SME pre-screening
        - **Business advisors** benchmarking client performance
        """)

    st.divider()
    st.markdown("### How it works")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown("**① Upload**\n\nUpload your financials as a CSV or use our demo data")
    with c2:
        st.markdown("**② Calculate**\n\nSystem calculates all 7 ratios and your health score")
    with c3:
        st.markdown("**③ Benchmark**\n\nCompare against NZ industry averages from Stats NZ")
    with c4:
        st.markdown("**④ Report**\n\nDownload your AI-generated PDF report")

    st.divider()
    if st.button("Start Analysis →"):
        st.session_state['page'] = '📊 Analyse a Business'
        st.rerun()


elif page == "📊 Analyse a Business":
    st.markdown('<div class="main-header">Analyse a Business</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Upload your financial data to get an AI-powered health analysis</div>', unsafe_allow_html=True)

    # ── Upload method selection ───────────────────────
    st.markdown('<div class="section-header">Step 1 — Choose your data source</div>', unsafe_allow_html=True)

    upload_method = st.radio(
        "How would you like to provide your data?",
        ["📂 Upload your own CSV", "📥 Use Xero export", "🏢 Use demo data"],
        horizontal=True
    )

    df_raw = None

    if upload_method == "📂 Upload your own CSV":
        col1, col2 = st.columns([2, 1])
        with col1:
            uploaded_file = st.file_uploader(
                "Upload your CSV file",
                type=['csv'],
                help="Upload a CSV file with your financial data"
            )
            if uploaded_file:
                import pandas as pd
                df_raw = pd.read_csv(uploaded_file)
                st.success(f"✓ File uploaded: {uploaded_file.name} ({len(df_raw)} rows)")
                st.dataframe(df_raw.head(), use_container_width=True)
        with col2:
            st.markdown("**Don't have the format?**")
            st.markdown("Download our template, fill it in Excel, and upload it back.")
            with open("data/upload_template.csv", "rb") as f:
                st.download_button(
                    label="⬇ Download Template CSV",
                    data=f,
                    file_name="nz_sme_template.csv",
                    mime="text/csv"
                )

    elif upload_method == "📥 Use Xero export":
        st.info("""
        **How to export from Xero:**
        1. In Xero → Reports → Profit & Loss → Export as CSV
        2. In Xero → Reports → Balance Sheet → Export as CSV
        3. Upload both files below — we'll map the columns automatically
        """)
        col1, col2 = st.columns(2)
        with col1:
            pnl_file = st.file_uploader("Upload Profit & Loss CSV", type=['csv'], key="pnl")
        with col2:
            bs_file = st.file_uploader("Upload Balance Sheet CSV", type=['csv'], key="bs")

        if pnl_file and bs_file:
            import pandas as pd
            pnl_df = pd.read_csv(pnl_file)
            bs_df  = pd.read_csv(bs_file)
            df_raw = pd.concat([pnl_df, bs_df], axis=1)
            st.success("✓ Both Xero files uploaded — columns will be mapped automatically")

    elif upload_method == "🏢 Use demo data":
        import pandas as pd
        from modules.db_connection import get_engine
        engine = get_engine()
        businesses = pd.read_sql("SELECT id, name, industry FROM businesses ORDER BY name", engine)

        st.markdown("**Select a demo company to analyse:**")
        selected = st.selectbox(
            "Choose a business",
            businesses['name'].tolist(),
            label_visibility="collapsed"
        )
        selected_id = int(businesses[businesses['name'] == selected]['id'].values[0])
        st.session_state['demo_business_id'] = selected_id
        st.session_state['demo_mode'] = True
        st.success(f"✓ Selected: {selected}")

    st.divider()

    # ── Business info form (for CSV uploads) ─────────
    if upload_method in ["📂 Upload your own CSV", "📥 Use Xero export"]:
        st.markdown('<div class="section-header">Step 2 — Business details</div>', unsafe_allow_html=True)
        from modules.xero_mapper import INDUSTRIES

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            biz_name = st.text_input("Business name", placeholder="e.g. Kiwi Café Ltd")
        with col2:
            industry = st.selectbox("Industry", INDUSTRIES)
        with col3:
            biz_age = st.number_input("Years in operation", min_value=0, max_value=100, value=3)
        with col4:
            employees = st.number_input("Number of employees", min_value=1, max_value=10000, value=10)

        year = st.selectbox("Financial year", [2024, 2023, 2022], index=0)

    st.divider()

    # ── Run analysis button ───────────────────────────
    st.markdown('<div class="section-header">Step 3 — Run analysis</div>', unsafe_allow_html=True)

    run_btn = st.button("🤖 Analyse with AI →", use_container_width=True)

    if run_btn:
        # Demo mode
        if upload_method == "🏢 Use demo data":
            if 'demo_business_id' not in st.session_state:
                st.error("Please select a demo company first.")
            else:
                with st.spinner("Running AI analysis... this takes 15–20 seconds"):
                    from modules.narrative_generator import generate_cfo_narrative, get_ratios_for_business, calculate_health_score
                    from modules.benchmarker import compare_to_benchmark
                    from modules.trend_analyser import analyse_trends

                    bid      = st.session_state['demo_business_id']
                    ratios   = get_ratios_for_business(bid)
                    score    = calculate_health_score(ratios)
                    analysis = generate_cfo_narrative(bid)
                    benchmark= compare_to_benchmark(bid)
                    trends   = analyse_trends(bid)

                    st.session_state['results'] = {
                        'ratios':     ratios,
                        'score':      score,
                        'analysis':   analysis,
                        'benchmark':  benchmark,
                        'trends':     trends
                    }
                    st.success("✓ Analysis complete! Go to results below.")
                    st.rerun()

        # CSV upload mode
        elif df_raw is not None:
            from modules.xero_mapper import process_upload
            result = process_upload(
                df_raw,
                business_name=biz_name,
                industry=industry,
                business_age=biz_age,
                num_employees=employees,
                year=year
            )
            if not result['is_valid']:
                st.error(f"Missing columns: {result['missing']}")
            else:
                for w in result['warnings']:
                    st.warning(w)

                with st.spinner("Saving data and running AI analysis..."):
                    from modules.data_loader import load_from_csv
                    import tempfile, os
                    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv',
                                                     delete=False, newline='') as tmp:
                        result['dataframe'].to_csv(tmp.name, index=False)
                        tmp_path = tmp.name
                    load_from_csv(tmp_path)
                    os.unlink(tmp_path)
                    st.success("✓ Data loaded and analysis complete!")
        else:
            st.error("Please upload a file or select demo data first.")

    # ── Show results if available ─────────────────────
        # ── Show results if available ─────────────────────
    if 'results' in st.session_state:
        r        = st.session_state['results']
        ratios   = r['ratios']
        score    = r['score']
        analysis = r['analysis']
        benchmark= r['benchmark']
        trends   = r['trends']

        import plotly.graph_objects as go
        import plotly.express as px
        from modules.report_generator import generate_report, clean_text
        import pandas as pd

        st.divider()
        st.markdown("## 📊 Analysis Results")

        # ── Health score + summary metrics ───────────
        col1, col2, col3, col4 = st.columns(4)

        score_col = "#1D9E75" if score >= 75 else ("#BA7517" if score >= 50 else "#A32D2D")
        score_lbl = "Healthy" if score >= 75 else ("Moderate" if score >= 50 else "At Risk")

        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div style="font-size:0.85rem;color:#666360;">Health Score</div>
                <div style="font-size:2.5rem;font-weight:700;color:{score_col};">{score}</div>
                <div style="font-size:0.9rem;font-weight:600;color:{score_col};">{score_lbl}</div>
            </div>""", unsafe_allow_html=True)
        with col2:
            st.metric("Annual Revenue",
                      f"NZD {float(ratios['revenue']):,.0f}")
        with col3:
            st.metric("Net Profit",
                      f"NZD {float(ratios['net_profit']):,.0f}",
                      f"{float(ratios['net_margin'])}% margin")
        with col4:
            st.metric("Total Assets",
                      f"NZD {float(ratios['total_assets']):,.0f}")

        st.divider()

        # ── Ratio table + benchmark chart ────────────
        col1, col2 = st.columns(2)

        with col1:
            st.markdown('<div class="section-header">Key Financial Ratios</div>', unsafe_allow_html=True)

            ratio_rows = [
                ("Gross Margin",    f"{ratios['gross_margin']}%",  float(ratios['gross_margin']) >= 40),
                ("Net Margin",      f"{ratios['net_margin']}%",    float(ratios['net_margin']) >= 5),
                ("Current Ratio",   f"{ratios['current_ratio']}x", float(ratios['current_ratio']) >= 1.5),
                ("Quick Ratio",     f"{ratios['quick_ratio']}x",   float(ratios['quick_ratio']) >= 1.0),
                ("Debt to Equity",  f"{ratios['debt_to_equity']}x",float(ratios['debt_to_equity']) <= 1.5),
                ("ROE",             f"{ratios['roe']}%",           float(ratios['roe']) >= 10),
                ("ROA",             f"{ratios['roa']}%",           float(ratios['roa']) >= 5),
            ]

            for label, value, is_good in ratio_rows:
                c1, c2, c3 = st.columns([3, 2, 1])
                with c1:
                    st.markdown(f"**{label}**")
                with c2:
                    st.markdown(f"`{value}`")
                with c3:
                    st.markdown("🟢" if is_good else "🔴")

        with col2:
            st.markdown('<div class="section-header">vs NZ Industry Average</div>', unsafe_allow_html=True)

            if benchmark and benchmark.get('comparisons'):
                comps = benchmark['comparisons']
                labels  = [c['ratio'] for c in comps]
                biz_vals= [c['business'] for c in comps]
                bench_vals=[c['benchmark'] for c in comps]

                fig = go.Figure()
                fig.add_trace(go.Bar(
                    name='This Business',
                    x=labels, y=biz_vals,
                    marker_color='#185FA5'
                ))
                fig.add_trace(go.Bar(
                    name='NZ Industry Average',
                    x=labels, y=bench_vals,
                    marker_color='#D1CFC8'
                ))
                fig.update_layout(
                    barmode='group',
                    height=320,
                    margin=dict(l=0, r=0, t=10, b=0),
                    legend=dict(orientation='h', yanchor='bottom', y=1.02),
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                )
                st.plotly_chart(fig, use_container_width=True)

        st.divider()

        # ── Risk flags ───────────────────────────────
        st.markdown('<div class="section-header">Risk Flags</div>', unsafe_allow_html=True)

        flags = []
        if float(ratios['current_ratio']) < 1.2:
            flags.append(('danger',  f"Low liquidity — current ratio {ratios['current_ratio']} is below 1.2"))
        elif float(ratios['current_ratio']) >= 2:
            flags.append(('success', f"Strong liquidity — current ratio {ratios['current_ratio']}"))
        else:
            flags.append(('warning', f"Adequate liquidity — current ratio {ratios['current_ratio']}"))

        if float(ratios['net_margin']) < 0:
            flags.append(('danger',  f"Business is loss-making — net margin {ratios['net_margin']}%"))
        elif float(ratios['net_margin']) >= 10:
            flags.append(('success', f"Strong profitability — net margin {ratios['net_margin']}%"))
        else:
            flags.append(('warning', f"Thin margins — net margin {ratios['net_margin']}%"))

        if float(ratios['debt_to_equity']) > 1.5:
            flags.append(('danger',  f"High leverage — debt to equity {ratios['debt_to_equity']}"))
        elif float(ratios['debt_to_equity']) < 0.5:
            flags.append(('success', f"Low leverage — debt to equity {ratios['debt_to_equity']}"))
        else:
            flags.append(('warning', f"Moderate leverage — debt to equity {ratios['debt_to_equity']}"))

        if float(ratios['roe']) >= 15:
            flags.append(('success', f"Excellent return on equity — {ratios['roe']}%"))
        elif float(ratios['roe']) < 0:
            flags.append(('danger',  f"Negative return on equity — {ratios['roe']}%"))

        for flag_type, msg in flags:
            icon = "✅" if flag_type == 'success' else ("⚠️" if flag_type == 'warning' else "🚨")
            st.markdown(
                f'<div class="flag-{flag_type}">{icon} {msg}</div>',
                unsafe_allow_html=True
            )

        st.divider()

        # ── Trend analysis ───────────────────────────
        if trends and trends.get('trends'):
            st.markdown('<div class="section-header">Year-on-Year Trends</div>', unsafe_allow_html=True)

            trend_data = trends['trends']
            years      = trends['years']
            labels     = ['Gross Margin','Net Margin','Current Ratio',
                          'Quick Ratio','Debt to Equity','ROE','ROA']
            keys       = ['gross_margin','net_margin','current_ratio',
                          'quick_ratio','debt_to_equity','roe','roa']

            cols = st.columns(4)
            for i, (label, key) in enumerate(zip(labels[:4], keys[:4])):
                t = trend_data[key]
                arrow = "↑" if t['direction'] == 'Improving' else ("↓" if t['direction'] == 'Worsening' else "→")
                col_delta = "normal" if t['direction'] == 'Improving' else ("inverse" if t['direction'] == 'Worsening' else "off")
                with cols[i]:
                    st.metric(label,
                              f"{t['latest']}",
                              f"{arrow} {t['change']} vs {years[0]}",
                              delta_color=col_delta)

            cols2 = st.columns(3)
            for i, (label, key) in enumerate(zip(labels[4:], keys[4:])):
                t = trend_data[key]
                arrow = "↑" if t['direction'] == 'Improving' else ("↓" if t['direction'] == 'Worsening' else "→")
                col_delta = "normal" if t['direction'] == 'Improving' else ("inverse" if t['direction'] == 'Worsening' else "off")
                with cols2[i]:
                    st.metric(label,
                              f"{t['latest']}",
                              f"{arrow} {t['change']} vs {years[0]}",
                              delta_color=col_delta)

            st.divider()

        # ── AI CFO Narrative ─────────────────────────
        st.markdown('<div class="section-header">🤖 AI CFO Narrative</div>', unsafe_allow_html=True)
        if analysis and analysis.get('narrative'):
            clean = clean_text(analysis['narrative'])
            st.markdown(f'<div style="background:#EEEDFE;border-left:4px solid #534AB7;padding:1rem 1.25rem;border-radius:8px;line-height:1.8;color:#1A1916;">{clean}</div>', unsafe_allow_html=True)

        st.divider()

        # ── Benchmark commentary ──────────────────────
        if benchmark and benchmark.get('commentary'):
            st.markdown('<div class="section-header">📊 Benchmark Commentary</div>', unsafe_allow_html=True)
            st.markdown(f'<div style="background:#EAF3DE;border-left:4px solid #1D9E75;padding:1rem 1.25rem;border-radius:8px;line-height:1.8;color:#1A1916;">{clean_text(benchmark["commentary"])}</div>', unsafe_allow_html=True)
            st.divider()

                # ── Scenario Modelling ───────────────────────
        st.divider()
        st.markdown('<div class="section-header">🔮 What-If Scenario Modelling</div>', unsafe_allow_html=True)
        st.markdown("Adjust the sliders to model how changes would affect the health score and key ratios.")

        col1, col2, col3 = st.columns(3)
        with col1:
            revenue_change = st.slider(
                "Revenue change %",
                min_value=-30, max_value=50, value=0, step=5,
                help="How would a revenue increase or decrease affect your ratios?"
            )
        with col2:
            cost_change = st.slider(
                "Cost reduction %",
                min_value=-20, max_value=30, value=0, step=5,
                help="How would reducing operating costs affect profitability?"
            )
        with col3:
            debt_repay = st.slider(
                "Debt repayment (NZD)",
                min_value=0, max_value=200000, value=0, step=10000,
                help="How would paying down debt affect your leverage ratios?"
            )

        if revenue_change != 0 or cost_change != 0 or debt_repay != 0:
            orig_revenue  = float(ratios['revenue'])
            orig_profit   = float(ratios['net_profit'])
            orig_debt     = float(ratios['total_debt'])
            orig_equity   = float(ratios['total_equity'])
            orig_assets   = float(ratios['total_assets'])

            new_revenue = orig_revenue * (1 + revenue_change/100)
            new_profit  = orig_profit + (new_revenue - orig_revenue) * 0.4 - (orig_revenue * cost_change/100 * 0.3)
            new_debt    = max(0, orig_debt - debt_repay)
            new_equity  = orig_equity + debt_repay

            new_gross_margin  = round((new_revenue - float(ratios['revenue']) * float(ratios['gross_margin'])/100 * (1 - cost_change/100)) / new_revenue * 100, 2) if new_revenue > 0 else 0
            new_net_margin    = round(new_profit / new_revenue * 100, 2) if new_revenue > 0 else 0
            new_debt_equity   = round(new_debt / new_equity, 2) if new_equity > 0 else 0
            new_roe           = round(new_profit / new_equity * 100, 2) if new_equity > 0 else 0
            new_roa           = round(new_profit / orig_assets * 100, 2) if orig_assets > 0 else 0

            from modules.narrative_generator import calculate_health_score
            scenario_ratios = ratios.copy()
            scenario_ratios['gross_margin']   = new_gross_margin
            scenario_ratios['net_margin']     = new_net_margin
            scenario_ratios['debt_to_equity'] = new_debt_equity
            scenario_ratios['roe']            = new_roe
            scenario_ratios['roa']            = new_roa
            new_score = calculate_health_score(scenario_ratios)

            st.markdown("#### Scenario Results")
            c1, c2, c3, c4, c5 = st.columns(5)

            with c1:
                st.metric("Health Score",
                          f"{new_score}/100",
                          f"{new_score - score:+d} vs current",
                          delta_color="normal" if new_score >= score else "inverse")
            with c2:
                st.metric("Net Margin",
                          f"{new_net_margin}%",
                          f"{round(new_net_margin - float(ratios['net_margin']), 2):+.2f}%",
                          delta_color="normal" if new_net_margin >= float(ratios['net_margin']) else "inverse")
            with c3:
                st.metric("Revenue",
                          f"NZD {new_revenue:,.0f}",
                          f"{revenue_change:+d}%",
                          delta_color="normal" if revenue_change >= 0 else "inverse")
            with c4:
                st.metric("Debt to Equity",
                          f"{new_debt_equity}x",
                          f"{round(new_debt_equity - float(ratios['debt_to_equity']), 2):+.2f}x",
                          delta_color="inverse" if new_debt_equity > float(ratios['debt_to_equity']) else "normal")
            with c5:
                st.metric("ROE",
                          f"{new_roe}%",
                          f"{round(new_roe - float(ratios['roe']), 2):+.2f}%",
                          delta_color="normal" if new_roe >= float(ratios['roe']) else "inverse")

            if st.button("🤖 Get AI advice on this scenario"):
                with st.spinner("Asking AI for scenario advice..."):
                    from modules.ai_client import ask_claude
                    scenario_prompt = f"""You are a NZ business advisor. A business owner is modelling a financial scenario.

Business: {ratios['business_name']} | Industry: {ratios['industry']}

Current situation:
- Health Score: {score}/100
- Net Margin: {ratios['net_margin']}%
- Debt to Equity: {ratios['debt_to_equity']}x
- ROE: {ratios['roe']}%

Proposed scenario:
- Revenue change: {revenue_change:+d}%
- Cost reduction: {cost_change:+d}%
- Debt repayment: NZD {debt_repay:,}

Projected outcome:
- New Health Score: {new_score}/100
- New Net Margin: {new_net_margin}%
- New Debt to Equity: {new_debt_equity}x
- New ROE: {new_roe}%

In 2 short paragraphs:
1. Is this a realistic and worthwhile scenario for a NZ SME?
2. What should the business prioritise first to achieve this?

Be direct and NZ-specific. Under 120 words."""

                    advice = ask_claude(scenario_prompt, max_tokens=250)
                    st.markdown(
                        f'<div style="background:#EEEDFE;border-left:4px solid #534AB7;'
                        f'padding:1rem 1.25rem;border-radius:8px;line-height:1.8;color:#1A1916;">'
                        f'{advice}</div>',
                        unsafe_allow_html=True
                    )
        else:
            st.info("Move the sliders above to model different scenarios.", icon="💡")

        st.divider()

        # ── PDF Download ─────────────────────────────
        st.markdown('<div class="section-header">📄 Download Report</div>', unsafe_allow_html=True)
        if st.button("Generate & Download PDF Report", use_container_width=True):
            with st.spinner("Generating PDF..."):
                bid = st.session_state.get('demo_business_id', 1)
                pdf_path = generate_report(business_id=bid)
                if pdf_path:
                    with open(pdf_path, "rb") as f:
                        st.download_button(
                            label="⬇ Download PDF",
                            data=f,
                            file_name=pdf_path.split('/')[-1],
                            mime="application/pdf"
                        )


elif page == "📈 Benchmarks":
    st.markdown('<div class="main-header">NZ Industry Benchmarks</div>', unsafe_allow_html=True)
    st.info("🚧 This section is being built — come back soon!", icon="🔨")


elif page == "ℹ️ About":
    st.markdown('<div class="main-header">About This Project</div>', unsafe_allow_html=True)

    st.markdown("""
    ### NZ SME Financial Health Analyser

    This tool was built as a capstone project for the **Master of Business Analytics**
    program at the **University of Auckland**, specialising in FinTech.

    **The problem:** New Zealand has over 550,000 SMEs, yet most lack access to
    affordable professional financial analysis. Banks and large corporations take
    financial health monitoring for granted — SMEs shouldn't have to.

    **The solution:** An AI-powered tool that delivers CFO-level financial analysis
    in seconds, completely free, benchmarked against real NZ industry data.
    """)

    st.divider()
    st.markdown("### Tech Stack")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        - 🐍 **Python** — data pipeline and AI integration
        - 🗄️ **PostgreSQL** — relational database
        - 🤖 **Claude AI (Anthropic)** — CFO narrative generation
        - 📊 **Streamlit** — web application framework
        """)
    with col2:
        st.markdown("""
        - 📈 **Power BI** — executive dashboard
        - 🐼 **Pandas** — data processing
        - 📉 **Plotly** — interactive charts
        - 📄 **FPDF2** — PDF report generation
        """)

    st.divider()
    st.markdown("### Data Sources")
    st.markdown("""
    - **Stats NZ Annual Enterprise Survey** — industry financial benchmarks
    - **Xero Small Business Insights NZ** — SME performance data
    - **Reserve Bank of NZ (RBNZ)** — financial stability context
    """)
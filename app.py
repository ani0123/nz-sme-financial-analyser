# ══════════════════════════════════════════════════════
#  app.py
#  NZ SME Financial Health Analyser
#  Main Streamlit application entry point
# ══════════════════════════════════════════════════════

import streamlit as st
from modules.xero_mapper import INDUSTRIES

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
        **How to export from Xero**
        1. Run the standard Profit and Loss and Balance Sheet reports for matching financial periods.
        2. Export each report as a CSV, or export to Excel or Google Sheets and save each report as a CSV.
        3. Keep the account labels, totals and period headings, then upload both files below.
        """)
        col1, col2 = st.columns(2)
        with col1:
            pnl_file = st.file_uploader("Upload Profit & Loss CSV", type=['csv'], key="pnl")
        with col2:
            bs_file = st.file_uploader("Upload Balance Sheet CSV", type=['csv'], key="bs")

        if pnl_file and bs_file:
            import csv
            from io import StringIO

            import pandas as pd
            from modules.xero_mapper import map_xero_exports

            try:
                # Report titles and notes can have fewer columns than the totals.
                pnl_df = pd.DataFrame(list(csv.reader(StringIO(pnl_file.getvalue().decode("utf-8-sig")), strict=True)))
                bs_df = pd.DataFrame(list(csv.reader(StringIO(bs_file.getvalue().decode("utf-8-sig")), strict=True)))
                mapped = map_xero_exports(pnl_df, bs_df)
            except (csv.Error, ValueError) as error:
                st.error(
                    f"Could not map the Xero reports. {error} "
                    "Upload separate UTF-8 CSV copies of the standard Profit and Loss and Balance Sheet "
                    "with account labels, report totals and amount columns for matching periods."
                )
            else:
                if "year" not in mapped.columns:
                    reporting_year = st.number_input(
                        "Reporting year for these undated exports", min_value=1900, max_value=2099,
                        value=None, step=1, key="xero_reporting_year",
                    )
                    if reporting_year is not None:
                        mapped["year"] = reporting_year
                if "year" in mapped.columns:
                    df_raw = mapped
                    st.success(f"✓ Both Xero reports mapped for {int(mapped['year'].iloc[0])}")
                st.dataframe(mapped.drop(columns="current_liab").head(), width="stretch")

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

    # ── Business info — auto-detect or manual ─────────
    if upload_method in ["📂 Upload your own CSV", "📥 Use Xero export"]:

        # Check if CSV already has all required business info columns
        required_cols = ['name', 'industry', 'business_age', 'num_employees', 'year']
        if df_raw is not None and all(col in df_raw.columns for col in required_cols):
            # Auto-read from CSV — no form needed
            year       = int(df_raw['year'].max())
            latest_row = df_raw[df_raw['year'] == year].iloc[0]
            biz_name   = latest_row['name']
            industry   = latest_row['industry']
            biz_age    = int(latest_row['business_age'])
            employees  = int(latest_row['num_employees'])

            st.markdown('<div class="section-header">Step 2 — Business details (auto-detected from your file)</div>', unsafe_allow_html=True)
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.info(f"**Business:** {biz_name}")
            with col2:
                st.info(f"**Industry:** {industry}")
            with col3:
                st.info(f"**Age:** {biz_age} years")
            with col4:
                st.info(f"**Employees:** {employees}")

        else:
            # Manual entry — CSV missing business info columns
            st.markdown('<div class="section-header">Step 2 — Business details</div>', unsafe_allow_html=True)
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                biz_name = st.text_input("Business name", placeholder="e.g. Kiwi Cafe Ltd")
            with col2:
                industry = st.selectbox("Industry", INDUSTRIES)
            with col3:
                biz_age = st.number_input("Years in operation", min_value=0, max_value=100, value=3)
            with col4:
                employees = st.number_input("Number of employees", min_value=1, max_value=10000, value=10)
            year = None

    st.divider()

    # ── Run analysis button ───────────────────────────
    st.markdown('<div class="section-header">Step 3 — Run analysis</div>', unsafe_allow_html=True)

    run_btn = st.button("🤖 Analyse with AI →", use_container_width=True)

    if run_btn:

        # ── Demo mode ────────────────────────────────
        if upload_method == "🏢 Use demo data":
            if 'demo_business_id' not in st.session_state:
                st.error("Please select a demo company first.")
            else:
                with st.spinner("Running AI analysis... this takes 15-20 seconds"):
                    from modules.narrative_generator import generate_cfo_narrative, get_ratios_for_business, calculate_health_score
                    from modules.benchmarker import compare_to_benchmark
                    from modules.trend_analyser import analyse_trends

                    bid       = st.session_state['demo_business_id']
                    ratios    = get_ratios_for_business(bid)
                    score     = calculate_health_score(ratios)
                    analysis  = generate_cfo_narrative(bid)
                    benchmark = compare_to_benchmark(bid)
                    trends    = analyse_trends(bid)

                    st.session_state['results'] = {
                        'ratios':    ratios,
                        'score':     score,
                        'analysis':  analysis,
                        'benchmark': benchmark,
                        'trends':    trends
                    }
                    st.success("Analysis complete! Scroll down to see results.")
                    st.rerun()

        # ── CSV upload mode ───────────────────────────
        elif df_raw is not None:
            from modules.xero_mapper import process_upload
            import pandas as pd

            # Auto-detect latest year from uploaded data
            if 'year' in df_raw.columns:
                year       = int(df_raw['year'].max())
                latest_row = df_raw[df_raw['year'] == year].iloc[0]
            else:
                year       = 2024
                latest_row = df_raw.iloc[0]

            # Auto-detect business info from latest year row
            if 'num_employees' in df_raw.columns:
                employees = int(latest_row['num_employees'])
            if 'business_age' in df_raw.columns:
                biz_age = int(latest_row['business_age'])
            if 'name' in df_raw.columns:
                biz_name = str(latest_row['name'])
            if 'industry' in df_raw.columns and latest_row['industry'] in INDUSTRIES:
                industry = str(latest_row['industry'])

            if upload_method == "📥 Use Xero export":
                biz_name = biz_name.strip()
                if not biz_name:
                    st.error("Enter a business name in Step 2 before analysing your Xero reports.")
                    st.stop()

                df_raw = df_raw.assign(
                    name=biz_name,
                    industry=industry,
                    business_age=biz_age,
                    num_employees=employees,
                    year=year,
                )

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
                    from modules.narrative_generator import generate_cfo_narrative, get_ratios_for_business, calculate_health_score
                    from modules.benchmarker import compare_to_benchmark
                    from modules.trend_analyser import analyse_trends
                    from modules.db_connection import get_engine
                    import tempfile, os, pandas as pd

                    # Save to temp CSV and load into database
                    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv',
                                                     delete=False, newline='') as tmp:
                        result['dataframe'].to_csv(tmp.name, index=False)
                        tmp_path = tmp.name
                    load_from_csv(tmp_path)
                    os.unlink(tmp_path)

                    # Find the business_id just inserted
                    engine = get_engine()
                    biz_df = pd.read_sql(
                        f"SELECT id FROM businesses WHERE name = '{biz_name}' ORDER BY id DESC LIMIT 1",
                        engine
                    )

                    if not biz_df.empty:
                        bid = int(biz_df.iloc[0]['id'])
                        st.session_state['demo_business_id'] = bid

                        # Get latest year available for this business
                        year_df = pd.read_sql(
                            f"SELECT MAX(year) as max_year FROM financials WHERE business_id = {bid}",
                            engine
                        )
                        actual_year = int(year_df.iloc[0]['max_year'])
                        ratios = get_ratios_for_business(bid, year=actual_year)

                        if ratios is None:
                            st.error("Could not load financial ratios. Please check your CSV data.")
                            st.stop()

                        score     = calculate_health_score(ratios)
                        analysis  = generate_cfo_narrative(bid, year=actual_year)
                        benchmark = compare_to_benchmark(bid, year=actual_year)
                        trends    = analyse_trends(bid)

                        st.session_state['results'] = {
                            'ratios':    ratios,
                            'score':     score,
                            'analysis':  analysis,
                            'benchmark': benchmark,
                            'trends':    trends
                        }
                        st.success("Analysis complete! Scroll down to see results.")
                        st.rerun()
                    else:
                        st.error("Could not find the uploaded business. Please check your CSV.")
        else:
            st.error("Please upload a file or select demo data first.")


    # ── Show results if available ─────────────────────
    if 'results' in st.session_state:
        r         = st.session_state['results']
        ratios    = r['ratios']
        score     = r['score']
        analysis  = r['analysis']
        benchmark = r['benchmark']
        trends    = r['trends']

        import plotly.graph_objects as go
        from modules.report_generator import generate_report, clean_text
        import pandas as pd

        st.divider()
        st.markdown("## Analysis Results")

        # ── Health score + summary metrics ────────────
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            score_label = "Healthy" if score >= 75 else ("Moderate" if score >= 50 else "At Risk")
            health_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=score,
                number=dict(valueformat=".0f", font=dict(size=32)),
                domain=dict(x=[0, 1], y=[0.25, 1]),
                gauge=dict(
                    axis=dict(range=[0, 100], tickvals=[0, 50, 75, 100], tickfont=dict(size=10)),
                    bar=dict(color="#263445", thickness=0.28),
                    borderwidth=0,
                    bgcolor="rgba(0,0,0,0)",
                    steps=[
                        dict(range=[0, 50], color="#A32D2D"),
                        dict(range=[50, 75], color="#BA7517"),
                        dict(range=[75, 100], color="#1D9E75"),
                    ],
                ),
            ))
            health_gauge.add_annotation(
                text=f"<b>{score_label}</b>",
                x=0.5, y=0.08,
                xref="paper", yref="paper",
                xanchor="center", yanchor="middle",
                showarrow=False,
                font=dict(size=14),
            )
            health_gauge.update_layout(
                height=170,
                margin=dict(l=18, r=18, t=10, b=8),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
            )
            st.plotly_chart(health_gauge, width="stretch", config={"displayModeBar": False})
        with col2:
            st.metric("Annual Revenue",   f"NZD {float(ratios['revenue']):,.0f}")
        with col3:
            st.metric("Net Profit",
                      f"NZD {float(ratios['net_profit']):,.0f}",
                      f"{float(ratios['net_margin'])}% margin")
        with col4:
            st.metric("Total Assets",     f"NZD {float(ratios['total_assets']):,.0f}")

        st.divider()

        # ── Ratio table + benchmark chart ─────────────
        col1, col2 = st.columns(2)

        with col1:
            st.markdown('<div class="section-header">Key Financial Ratios</div>', unsafe_allow_html=True)
            ratio_rows = [
                ("Gross Margin",   f"{ratios['gross_margin']}%",   float(ratios['gross_margin'])  >= 40),
                ("Net Margin",     f"{ratios['net_margin']}%",     float(ratios['net_margin'])    >= 5),
                ("Current Ratio",  f"{ratios['current_ratio']}x",  float(ratios['current_ratio']) >= 1.5),
                ("Quick Ratio",    f"{ratios['quick_ratio']}x",    float(ratios['quick_ratio'])   >= 1.0),
                ("Debt to Equity", f"{ratios['debt_to_equity']}x", float(ratios['debt_to_equity'])<= 1.5),
                ("ROE",            f"{ratios['roe']}%",            float(ratios['roe'])           >= 10),
                ("ROA",            f"{ratios['roa']}%",            float(ratios['roa'])           >= 5),
            ]
            for label, value, is_good in ratio_rows:
                c1, c2, c3 = st.columns([3, 2, 1])
                with c1: st.markdown(f"**{label}**")
                with c2: st.markdown(f"`{value}`")
                with c3: st.markdown("🟢" if is_good else "🔴")

        with col2:
            st.markdown('<div class="section-header">vs NZ Industry Average</div>', unsafe_allow_html=True)
            if benchmark and benchmark.get('comparisons'):
                comps      = benchmark['comparisons']
                fig = go.Figure()
                fig.add_trace(go.Bar(name='This Business',      x=[c['ratio'] for c in comps], y=[c['business']  for c in comps], marker_color='#185FA5'))
                fig.add_trace(go.Bar(name='NZ Industry Average',x=[c['ratio'] for c in comps], y=[c['benchmark'] for c in comps], marker_color='#D1CFC8'))
                fig.update_layout(barmode='group', height=320,
                                  margin=dict(l=0,r=0,t=10,b=0),
                                  legend=dict(orientation='h',yanchor='bottom',y=1.02),
                                  plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig, use_container_width=True)

        st.divider()

        # ── Risk flags ────────────────────────────────
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
            st.markdown(f'<div class="flag-{flag_type}">{icon} {msg}</div>', unsafe_allow_html=True)

        st.divider()

        # ── Trend analysis ────────────────────────────
        st.markdown('<div class="section-header">Year-on-Year Trends</div>', unsafe_allow_html=True)
        ratio_specs = [
            ("gross_margin", "Gross Margin", "#185FA5", "%"),
            ("net_margin", "Net Margin", "#1D9E75", "%"),
            ("current_ratio", "Current Ratio", "#534AB7", "x"),
            ("quick_ratio", "Quick Ratio", "#BA7517", "x"),
            ("debt_to_equity", "Debt to Equity", "#A32D2D", "x"),
            ("roe", "ROE", "#2E8B57", "%"),
            ("roa", "ROA", "#D4860B", "%"),
        ]
        trend_data = trends.get("trends") if trends else None
        years = trends["years"] if trends else []
        has_yearly_change = bool(trend_data) and len(years) >= 2

        if has_yearly_change:
            older_years = years[:-2]
            history = {}
            if older_years:
                # The saved trend summary only contains the latest two years.
                from sqlalchemy.exc import SQLAlchemyError
                from modules.trend_analyser import get_multi_year_ratios

                if "chart_history" not in trends:
                    try:
                        historical_ratios = get_multi_year_ratios(int(ratios["business_id"]))
                    except (SQLAlchemyError, KeyError, ValueError):
                        st.warning("Earlier ratio values could not be loaded. The latest two years are shown.")
                    else:
                        ratio_keys = [key for key, _, _, _ in ratio_specs]
                        historical_ratios = historical_ratios.set_index("year").reindex(older_years)[ratio_keys]
                        trends["chart_history"] = (
                            historical_ratios.astype(object)
                            .where(historical_ratios.notna(), None)
                            .to_dict("list")
                        )
                history = trends.get("chart_history", {})

            trends_chart = go.Figure()
            for key, label, color, unit in ratio_specs:
                ratio_trend = trend_data[key]
                values = history.get(key, [None] * len(older_years))
                trends_chart.add_trace(go.Scatter(
                    x=years,
                    y=[*values, ratio_trend["previous"], ratio_trend["latest"]],
                    name=label,
                    mode="lines+markers",
                    line=dict(color=color),
                    yaxis="y" if unit == "%" else "y2",
                    hovertemplate=f"{label}: %{{y:.2f}}{unit}<extra></extra>",
                ))
            trends_chart.update_layout(
                height=300,
                showlegend=True,
                legend=dict(orientation="h", x=0, y=-0.16, yanchor="top"),
                hovermode="x unified",
                margin=dict(l=0, r=0, t=10, b=0),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                xaxis=dict(tickmode="array", tickvals=years, showgrid=False, zeroline=False),
                yaxis=dict(ticksuffix="%", showgrid=False, zeroline=False),
                yaxis2=dict(ticksuffix="x", overlaying="y", side="right", showgrid=False, zeroline=False),
            )
            st.plotly_chart(trends_chart, width="stretch")
            st.caption("Year-on-year ratio trends — hover to see values")

        trend_directions = {"Improving": ("↑", "normal"), "Worsening": ("↓", "inverse")}
        for group in (ratio_specs[:4], ratio_specs[4:]):
            for column, (key, label, _, _) in zip(st.columns(len(group)), group):
                if has_yearly_change:
                    ratio_trend = trend_data[key]
                    arrow, delta_color = trend_directions.get(ratio_trend["direction"], ("→", "off"))
                    column.metric(
                        label, f"{ratio_trend['latest']}",
                        f"{arrow} {ratio_trend['change']} vs {years[-2]}",
                        delta_color=delta_color,
                    )
                else:
                    column.metric(label, f"{ratios[key]}")

        st.divider()

        # ── AI CFO Narrative ──────────────────────────
        st.markdown('<div class="section-header">🤖 AI CFO Narrative</div>', unsafe_allow_html=True)
        if analysis and analysis.get('narrative'):
            st.markdown(
                f'<div style="background:#EEEDFE;border-left:4px solid #534AB7;padding:1rem 1.25rem;'
                f'border-radius:8px;line-height:1.8;color:#1A1916;">{clean_text(analysis["narrative"])}</div>',
                unsafe_allow_html=True)

        st.divider()

        # ── Benchmark commentary ──────────────────────
        if benchmark and benchmark.get('commentary'):
            st.markdown('<div class="section-header">📊 Benchmark Commentary</div>', unsafe_allow_html=True)
            st.markdown(
                f'<div style="background:#EAF3DE;border-left:4px solid #1D9E75;padding:1rem 1.25rem;'
                f'border-radius:8px;line-height:1.8;color:#1A1916;">{clean_text(benchmark["commentary"])}</div>',
                unsafe_allow_html=True)
            st.divider()

        # ── Scenario Modelling ────────────────────────
        st.divider()
        st.markdown('<div class="section-header">🔮 What-If Scenario Modelling</div>', unsafe_allow_html=True)
        st.markdown("Adjust the sliders to model how changes would affect the health score and key ratios.")

        col1, col2, col3 = st.columns(3)
        with col1:
            revenue_change = st.slider("Revenue change %",    min_value=-30, max_value=50,     value=0, step=5)
        with col2:
            cost_change    = st.slider("Cost reduction %",    min_value=-20, max_value=30,     value=0, step=5)
        with col3:
            debt_repay     = st.slider("Debt repayment (NZD)",min_value=0,   max_value=200000, value=0, step=10000)

        if revenue_change != 0 or cost_change != 0 or debt_repay != 0:
            orig_revenue = float(ratios['revenue'])
            orig_profit  = float(ratios['net_profit'])
            orig_debt    = float(ratios['total_debt'])
            orig_equity  = float(ratios['total_equity'])
            orig_assets  = float(ratios['total_assets'])

            new_revenue      = orig_revenue * (1 + revenue_change/100)
            new_profit       = orig_profit + (new_revenue - orig_revenue)*0.4 - (orig_revenue*cost_change/100*0.3)
            new_debt         = max(0, orig_debt - debt_repay)
            new_equity       = orig_equity + debt_repay
            new_gross_margin = round((new_revenue - orig_revenue*(float(ratios['gross_margin'])/100)*(1 - cost_change/100))/new_revenue*100, 2) if new_revenue > 0 else 0
            new_net_margin   = round(new_profit/new_revenue*100, 2) if new_revenue > 0 else 0
            new_debt_equity  = round(new_debt/new_equity, 2) if new_equity > 0 else 0
            new_roe          = round(new_profit/new_equity*100, 2) if new_equity > 0 else 0
            new_roa          = round(new_profit/orig_assets*100, 2) if orig_assets > 0 else 0

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
            with c1: st.metric("Health Score",   f"{new_score}/100",          f"{new_score-score:+d} vs current",                                    delta_color="normal" if new_score >= score else "inverse")
            with c2: st.metric("Net Margin",     f"{new_net_margin}%",        f"{round(new_net_margin-float(ratios['net_margin']),2):+.2f}%",         delta_color="normal" if new_net_margin >= float(ratios['net_margin']) else "inverse")
            with c3: st.metric("Revenue",        f"NZD {new_revenue:,.0f}",   f"{revenue_change:+d}%",                                               delta_color="normal" if revenue_change >= 0 else "inverse")
            with c4: st.metric("Debt to Equity", f"{new_debt_equity}x",       f"{round(new_debt_equity-float(ratios['debt_to_equity']),2):+.2f}x",   delta_color="inverse" if new_debt_equity > float(ratios['debt_to_equity']) else "normal")
            with c5: st.metric("ROE",            f"{new_roe}%",               f"{round(new_roe-float(ratios['roe']),2):+.2f}%",                      delta_color="normal" if new_roe >= float(ratios['roe']) else "inverse")

            if st.button("🤖 Get AI advice on this scenario"):
                with st.spinner("Asking AI for scenario advice..."):
                    from modules.ai_client import ask_claude
                    advice = ask_claude(f"""You are a NZ business advisor. A business owner is modelling a financial scenario.
Business: {ratios['business_name']} | Industry: {ratios['industry']}
Current: Health Score {score}/100, Net Margin {ratios['net_margin']}%, D/E {ratios['debt_to_equity']}x, ROE {ratios['roe']}%
Scenario: Revenue {revenue_change:+d}%, Cost reduction {cost_change:+d}%, Debt repayment NZD {debt_repay:,}
Projected: Health Score {new_score}/100, Net Margin {new_net_margin}%, D/E {new_debt_equity}x, ROE {new_roe}%
In 2 short paragraphs: (1) Is this realistic for a NZ SME? (2) What to prioritise first?
Be direct and NZ-specific. Under 120 words.""", max_tokens=250)
                    st.markdown(
                        f'<div style="background:#EEEDFE;border-left:4px solid #534AB7;padding:1rem 1.25rem;'
                        f'border-radius:8px;line-height:1.8;color:#1A1916;">{advice}</div>',
                        unsafe_allow_html=True)
        else:
            st.info("Move the sliders above to model different scenarios.", icon="💡")

        st.divider()

        # ── PDF Download ──────────────────────────────
        st.markdown('<div class="section-header">📄 Download Report</div>', unsafe_allow_html=True)
        if st.button("Generate & Download PDF Report", use_container_width=True):
            with st.spinner("Generating PDF..."):
                bid      = st.session_state.get('demo_business_id', 1)
                pdf_path = generate_report(business_id=bid)
                if pdf_path:
                    with open(pdf_path, "rb") as f:
                        st.download_button(label="⬇ Download PDF", data=f,
                                           file_name=pdf_path.split('/')[-1],
                                           mime="application/pdf")

        # ── Business comparison ──────────────────────
        from html import escape

        from sqlalchemy.exc import SQLAlchemyError

        from modules.db_connection import get_engine
        from modules.narrative_generator import calculate_health_score, get_ratios_for_business
        from modules.trend_analyser import get_multi_year_ratios

        st.divider()
        st.markdown(
            '<div class="section-header">📊 Compare with another business</div>',
            unsafe_allow_html=True,
        )

        current_business_id = int(ratios["business_id"])
        comparison_source = (current_business_id, int(ratios["year"]))
        comparison_metrics = [
            ("gross_margin", "Gross Margin", "%"),
            ("net_margin", "Net Margin", "%"),
            ("current_ratio", "Current Ratio", "x"),
            ("quick_ratio", "Quick Ratio", "x"),
            ("debt_to_equity", "Debt to Equity", "x"),
            ("roe", "ROE", "%"),
            ("roa", "ROA", "%"),
        ]

        try:
            businesses = pd.read_sql("SELECT id, name, industry FROM businesses ORDER BY name", get_engine())
        except (SQLAlchemyError, ValueError):
            st.error("The business list could not be loaded. Please try again later.")
        else:
            other_businesses = businesses[businesses["id"] != current_business_id]
            if other_businesses.empty:
                st.info("There are no other businesses available to compare.")
            else:
                business_labels = {}
                for business in other_businesses.itertuples(index=False):
                    industry = business.industry if pd.notna(business.industry) else "Unknown industry"
                    business_labels[business.id] = f"{business.name} ({industry}, ID {business.id})"
                comparison_id = st.selectbox(
                    "Business to compare",
                    options=list(business_labels),
                    format_func=business_labels.__getitem__,
                    index=None,
                    placeholder="Select another business",
                    key=f"comparison_business_{current_business_id}",
                )
                if st.button("Compare", key="compare_business", disabled=comparison_id is None):
                    st.session_state.pop("comparison", None)
                    try:
                        selected_ratios = get_ratios_for_business(int(comparison_id))
                        if selected_ratios is None:
                            available_ratios = get_multi_year_ratios(int(comparison_id))
                            if not available_ratios.empty:
                                selected_ratios = available_ratios.iloc[-1]
                    except (SQLAlchemyError, ValueError):
                        st.error("The selected business's ratios could not be loaded. Please try again later.")
                    else:
                        if selected_ratios is None:
                            st.info("Financial ratios are unavailable for the selected business.")
                        else:
                            score_keys = [key for key, _, _ in comparison_metrics if key != "quick_ratio"]
                            selected_score = None
                            if selected_ratios[score_keys].notna().all():
                                selected_score = calculate_health_score(selected_ratios)
                            st.session_state["comparison"] = {
                                "source": comparison_source,
                                "ratios": selected_ratios,
                                "score": selected_score,
                            }

        comparison = st.session_state.get("comparison")
        if comparison and comparison["source"] == comparison_source:
            selected_ratios = comparison["ratios"]
            table_headers = []
            for business, role in ((ratios, "Current business"), (selected_ratios, "Selected business")):
                name = escape(str(business["business_name"]))
                year = int(business["year"])
                table_headers.append(
                    f'<th scope="col"><div class="metric-card" style="color:#403E3A;">'
                    f'<strong style="color:#185FA5;">{name}</strong><br>'
                    f'{role} · {year}</div></th>'
                )

            table_rows = []
            for key, label, unit in comparison_metrics:
                current_value = ratios[key]
                selected_value = selected_ratios[key]
                current_text = f"{current_value:.2f}{unit}" if pd.notna(current_value) else "Unavailable"
                selected_text = f"{selected_value:.2f}{unit}" if pd.notna(selected_value) else "Unavailable"
                if pd.notna(current_value) and pd.notna(selected_value) and current_value != selected_value:
                    current_is_better = (
                        current_value < selected_value if key == "debt_to_equity" else current_value > selected_value
                    )
                    if current_is_better:
                        current_text += " ✅"
                    else:
                        selected_text += " ✅"
                table_rows.append(f'<tr><th scope="row">{label}</th><td>{current_text}</td><td>{selected_text}</td></tr>')

            selected_score = comparison["score"]
            selected_score_text = f"{selected_score}/100" if selected_score is not None else "Unavailable"
            table_rows.append(
                f'<tr><th scope="row">Health Score</th><td>{score}/100</td><td>{selected_score_text}</td></tr>'
            )
            st.html(
                '<table aria-label="Financial comparison" style="width:100%;">'
                f'<thead><tr><th scope="col">Metric</th>{"".join(table_headers)}</tr></thead>'
                f'<tbody>{"".join(table_rows)}</tbody></table>'
            )


elif page == "📈 Benchmarks":
    st.markdown('<div class="main-header">NZ Industry Benchmarks</div>', unsafe_allow_html=True)
    from html import escape

    import pandas as pd
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    from sqlalchemy.exc import SQLAlchemyError

    from modules.benchmarker import get_industry_benchmark

    selected_industry = st.selectbox("Industry", INDUSTRIES, key="benchmark_industry")
    ratio_definitions = [
        ("Gross Margin", "avg_gross_margin", "%",
         "Share of sales left after paying the direct cost of goods or services."),
        ("Net Margin", "avg_net_margin", "%",
         "Share of sales left as profit after all expenses and taxes."),
        ("Current Ratio", "avg_current_ratio", "x",
         "Dollars of short-term assets for every dollar owed in the short term."),
        ("Quick Ratio", "avg_quick_ratio", "x",
         "Dollars of short-term assets excluding inventory for every dollar owed in the short term."),
        ("Debt to Equity", "avg_debt_to_eq", "x",
         "Dollars of debt for every dollar of owners' equity."),
        ("Return on Equity (ROE)", "avg_roe", "%",
         "Net profit as a percentage of the owners' equity in the business."),
        ("Return on Assets (ROA)", "avg_roa", "%",
         "Net profit as a percentage of the value of everything the business owns."),
    ]

    try:
        industry_benchmark = get_industry_benchmark(selected_industry)
    except (SQLAlchemyError, ValueError):
        industry_benchmark = None
        st.error("Industry benchmarks could not be loaded. Please try again later.")
    else:
        if industry_benchmark is None:
            st.info(f"No NZ industry benchmark is available for {selected_industry}.")

    if industry_benchmark is not None:
        benchmark_source = industry_benchmark.get("data_source")
        benchmark_year = industry_benchmark.get("year_reference")
        source_details = []
        if pd.notna(benchmark_source):
            source_details.append(str(benchmark_source))
        if pd.notna(benchmark_year):
            source_details.append(f"Reference year {benchmark_year:.0f}")
        if source_details:
            source_text = escape(" | ".join(source_details))
            st.markdown(
                f'<div class="metric-card" style="color:#403E3A;margin-bottom:1rem;">'
                f'<strong style="color:#185FA5;">Benchmark source</strong><br>{source_text}</div>',
                unsafe_allow_html=True,
            )

    benchmark_rows = []
    for label, column, unit, description in ratio_definitions:
        raw_value = industry_benchmark.get(column) if industry_benchmark is not None else None
        value = float(raw_value) if pd.notna(raw_value) else None
        benchmark_rows.append({
            "Ratio": label,
            "NZ Industry Average": f"{value:.2f}{unit}" if value is not None else "Unavailable",
            "What it means": description,
            "value": value,
            "unit": unit,
        })

    st.markdown('<div class="section-header">Benchmark values and definitions</div>', unsafe_allow_html=True)
    benchmark_table = pd.DataFrame(benchmark_rows).set_index("Ratio")
    st.table(benchmark_table[["NZ Industry Average", "What it means"]])

    chart_data = benchmark_table.dropna(subset=["value"])
    if not chart_data.empty:
        st.markdown('<div class="section-header">Benchmark chart</div>', unsafe_allow_html=True)
        unit_groups = chart_data.groupby("unit")
        fig = make_subplots(rows=unit_groups.ngroups, cols=1, vertical_spacing=0.18)
        for row, (unit, unit_data) in enumerate(unit_groups, start=1):
            fig.add_trace(
                go.Bar(
                    x=unit_data["value"],
                    y=unit_data.index.tolist(),
                    text=unit_data["NZ Industry Average"],
                    textposition="auto",
                    orientation="h",
                    marker_color="#185FA5",
                    hovertemplate="%{y}: %{text}<extra></extra>",
                ),
                row=row, col=1,
            )
            fig.update_xaxes(ticksuffix=unit, row=row, col=1)
            fig.update_yaxes(autorange="reversed", automargin=True, row=row, col=1)
        fig.update_layout(
            showlegend=False,
            height=440,
            margin=dict(l=0, r=20, t=10, b=0),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig, width="stretch")


elif page == "ℹ️ About":
    st.markdown('<div class="main-header">About This Project</div>', unsafe_allow_html=True)
    st.markdown("""
    ### NZ SME Financial Health Analyser

    This tool was built as a capstone project for the **Master of Business Analytics**
    program at the **University of Auckland**, specialising in FinTech.

    **The problem:** New Zealand has over 550,000 SMEs, yet most lack access to
    affordable professional financial analysis. Banks and large corporations take
    financial health monitoring for granted — SMEs should not have to.

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

# NZ SME Financial Health Analyser

**AI-powered financial analysis for New Zealand small and medium businesses.**

🔗 **Live app:** [nz-sme-analyser.streamlit.app](https://nz-sme-analyser.streamlit.app)

---

## What it does

New Zealand has over 550,000 SMEs, but most can't afford a CFO or professional financial analysis. This tool gives any SME owner a CFO-level financial health check in seconds — completely free.

Upload your financial data, and the app will:

- Calculate 7 key financial ratios instantly
- Score your business health out of 100
- Benchmark your ratios against real NZ industry averages (Stats NZ + Xero Small Business Insights)
- Generate an AI narrative from Anthropic's Claude — written like a CFO, not a spreadsheet
- Model what-if scenarios (revenue changes, cost cuts, debt repayment)
- Compare your business side-by-side with others in the database
- Download a professional PDF report

---

## Features

| Feature | Description |
|---|---|
| 📥 CSV Upload | Upload your own financials using the provided template |
| 📥 Xero Integration | Upload Xero P&L + Balance Sheet exports directly |
| 🏢 Demo Data | Try the app instantly with pre-loaded NZ businesses |
| 📊 Health Score Gauge | Visual speedometer showing your score from 0–100 |
| 🏆 Industry Benchmarks | Compare against 9 NZ industry averages |
| 📈 Trend Charts | Year-on-year ratio tracking with line charts |
| 🔮 Scenario Modelling | Slider-based what-if analysis with AI advice |
| 🤝 Business Comparison | Side-by-side ratio comparison with any business in the database |
| 📄 PDF Report | Downloadable professional report with AI narrative |

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| AI Narrative | Anthropic Claude API (claude-haiku-4-5) |
| Database | PostgreSQL via Supabase |
| Data Processing | Python, Pandas |
| Charts | Plotly |
| PDF Generation | FPDF2 |
| ORM | SQLAlchemy |
| Deployment | Streamlit Cloud |

---

## Financial Ratios Analysed

1. **Gross Margin** — revenue after cost of goods sold
2. **Net Margin** — bottom-line profitability
3. **Current Ratio** — short-term liquidity
4. **Quick Ratio** — liquidity without inventory
5. **Debt to Equity** — financial leverage
6. **Return on Equity (ROE)** — returns for shareholders
7. **Return on Assets (ROA)** — asset efficiency

---

## NZ Industry Benchmarks

Benchmarks sourced from:
- Stats NZ Annual Enterprise Survey
- Xero Small Business Insights NZ
- Reserve Bank of NZ (RBNZ) Financial Stability Reports

Industries covered: Retail, Hospitality/Food & Beverage, Construction, Professional Services, Manufacturing, Agriculture, Healthcare, Technology, Transport & Logistics.

---

## Running Locally

### Prerequisites
- Python 3.10+
- A Supabase PostgreSQL database
- An Anthropic API key

### Setup

```bash
# Clone the repository
git clone https://github.com/ani0123/nz-sme-financial-analyser.git
cd nz-sme-financial-analyser

# Install dependencies
pip install -r requirements.txt

# Create a .env file with your credentials
ANTHROPIC_API_KEY=your_key_here
DATABASE_URL=your_supabase_connection_string
```

### Run the app

```bash
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

### Database setup

Run the schema file against your Supabase database:

```bash
psql your_supabase_connection_string < schema.sql
```

---

## Project Structure

```
nz_sme_analyser/
├── app.py                  # Main Streamlit application
├── schema.sql              # Database schema
├── requirements.txt        # Python dependencies
├── data/
│   ├── upload_template.csv # CSV template for user uploads
│   └── sample_businesses.csv
├── modules/
│   ├── ai_client.py        # Claude API wrapper
│   ├── benchmarker.py      # NZ industry benchmark comparisons
│   ├── data_loader.py      # CSV to database loader
│   ├── db_connection.py    # SQLAlchemy database connection
│   ├── narrative_generator.py  # AI CFO narrative generation
│   ├── populate_ratios.py  # Financial ratio calculations
│   ├── report_generator.py # PDF report generation
│   ├── trend_analyser.py   # Year-on-year trend analysis
│   └── xero_mapper.py      # Xero CSV column mapping
└── outputs/                # Generated PDF reports
```

---

## Built By

Anirudh Bhardwaj  
Master of Business Analytics (FinTech), University of Auckland  
[LinkedIn](https://www.linkedin.com/in/anirudh-bhardwaj-929967219) · [GitHub](https://github.com/ani0123/nz-sme-financial-analyser)

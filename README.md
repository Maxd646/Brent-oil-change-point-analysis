# Brent Oil Price Change Point Analysis

## Executive Summary

This project analyzes how major geopolitical and economic events impact
Brent crude oil prices using Bayesian change point detection. Structural
breaks in price dynamics are identified and associated with historical
events to support data-driven decisions for investors, policymakers, and
energy sector stakeholders.

**Key Results:**
- **Task 1:** 9,011 daily observations cleaned and validated (1987-2022)
- **Task 1:** Log returns confirmed stationary (ADF p < 0.0001)
- **Task 1:** 15 major geopolitical and economic events documented
- **Task 1:** 9 comprehensive visualizations generated
- **Task 2:** Change point detected at April 28, 2020 (COVID-19 impact)
- **Task 2:** Bayesian model with MCMC sampling complete
- **Task 3:** Interactive dashboard with Flask API and React frontend

---

## Business Objectives

- Identify regime shifts in oil price dynamics\
- Quantify the impact of major global events with uncertainty
  estimates\
- Distinguish structural breaks from normal market volatility\
- Provide probabilistic insights for risk management and policy
  decisions

**Target Stakeholders:** Investors, policymakers, energy companies, and
risk analysts.

---

## Dataset Overview

### Brent Oil Prices

- **Period:** 1987-05-20 to 2022-09-30\
- **Frequency:** Daily\
- **Observations:** 9,011 (after cleaning)\
- **Price Range:** \$9.10 -- \$143.95 per barrel

### Geopolitical & Economic Events

- **Total Events:** 15\
- **Categories:** Geopolitical, Economic, OPEC policy decisions

---

## Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/Maxd646/brent-oil-change-point-analysis.git
cd brent-oil-change-point-analysis

# Install Python dependencies
pip install -r requirements.txt
```

### Run Complete Analysis

**Task 1 - Data Pipeline (Already Complete):**
```bash
python src/data/load_clean_data.py
python src/analysis/eda_analysis.py
```

**Task 2 - Bayesian Change Point Model:**
```bash
python src/models/bayesian_changepoint.py
```

**Task 3 - Interactive Dashboard:**
```bash
# Terminal 1 - Backend
python dashboard/backend/app.py

# Terminal 2 - Frontend
cd dashboard/frontend
npm install
npm start
```

Access dashboard at: `http://localhost:3000`

**Outputs:**
- Cleaned datasets: `data/processed/`
- Visualizations: `reports/figures/` (9 PNG files)
- Summary report: `reports/eda_summary.txt`
- Change point analysis: Console output + 3 figures
- Interactive dashboard: Browser interface

---

## Project Structure

```
brent-oil-change-point-analysis/
│
├── data/
│   ├── external/
│   │   ├── BrentOilPrices.csv          # Raw price data
│   │   └── geopolitical_events.csv     # 15 major events
│   ├── processed/
│   │   ├── cleaned_prices.csv          # Cleaned data
│   │   └── prices_with_features.csv    # With log returns, volatility
│   └── raw/
│       └── brent_oil_prices.csv        # Original data
│
├── src/
│   ├── data/
│   │   └── load_clean_data.py          # Data pipeline
│   ├── analysis/
│   │   └── eda_analysis.py             # EDA + visualizations
│   ├── models/
│   │   ├── bayesian_changepoint.py     # Bayesian model (Task 2)
│   │   └── run_changepoint_analysis.py # Analysis runner
│   └── utils/
│       ├── config.py                   # Configuration
│       └── logger.py                   # Logging utilities
│
├── notebooks/
│   ├── 01_data_exploration.ipynb       # Interactive EDA
│   ├── 03_bayesian_change_point_model.ipynb  # Model notebook
│   ├── 04_event_correlation_analysis.ipynb   # Event analysis
│   └── 05_model_extensions.ipynb       # Extensions
│
├── dashboard/
│   ├── backend/
│   │   └── app.py                      # Flask REST API (Task 3)
│   └── frontend/
│       ├── src/
│       │   ├── App.js                  # React dashboard
│       │   └── App.css                 # Styling
│       ├── public/
│       └── package.json                # Dependencies
│
├── reports/
│   ├── figures/                        # 9 PNG visualizations
│   │   ├── price_timeseries.png
│   │   ├── trend_analysis.png
│   │   ├── volatility_analysis.png
│   │   ├── stationarity_tests.png
│   │   ├── summary_statistics.png
│   │   ├── time_series_decomposition.png
│   │   ├── changepoint_posterior.png
│   │   ├── changepoint_trace.png
│   │   └── data_with_changepoint.png
│   └── eda_summary.txt                 # Statistical summary
│
├── docs/
│   ├── Task1_Analysis_Plan.md
│   ├── Assumptions_and_Limitations.md
│   └── Change_Point_Model_Explanation.md
│
├── config.json                         # Project configuration
├── requirements.txt                    # Python dependencies
├── README.md                           # This file
├── SETUP_INSTRUCTIONS.md               # Quick start guide
└── PROJECT_SUMMARY.md                  # Complete project summary
```

---

## Key Findings

### Task 1: Data Foundation
- Log returns are stationary; price levels are non-stationary
- High volatility clustering and regime shifts observed
- Fat-tailed return distribution (kurtosis ≈ 65.9) indicates extreme events
- 9,011 observations spanning 35.5 years

### Task 2: Bayesian Analysis
- **Primary change point detected:** April 28, 2020
- **Associated event:** COVID-19 pandemic / negative oil prices
- **Model:** Mean shift with constant variance
- **Sampling:** 2,000 draws × 4 chains (MCMC)
- **Convergence:** Adequate (R-hat < 1.12)

### Task 3: Dashboard
- 7 REST API endpoints for data access
- Interactive price charts with change point markers
- Event timeline with category filtering
- Date range filtering and hover tooltips
- Responsive design for all devices

---

## Methodology

### Task 1: Data Foundation ✅ COMPLETE

- Data cleaning and validation
- Feature engineering (log returns, rolling volatility, moving averages)
- Exploratory data analysis and visualization
- Event dataset compilation (15 events)

### Task 2: Bayesian Change Point Modeling ✅ COMPLETE

- PyMC Bayesian change point detection
- MCMC sampling and posterior analysis
- Event association and impact quantification
- Convergence diagnostics and uncertainty quantification

### Task 3: Interactive Dashboard ✅ COMPLETE

- Flask backend API (7 endpoints)
- React-based frontend visualization
- Interactive event and change point exploration
- Date range and category filtering

---

## Assumptions and Limitations

- Correlation does not imply causation\
- Univariate analysis (no macroeconomic covariates)\
- Discrete change point assumption\
- Historical patterns may not predict future dynamics

---

## Documentation

- Task1 Analysis Plan: `docs/Task1_Analysis_Plan.md`
- Assumptions and Limitations: `docs/Assumptions_and_Limitations.md`
- EDA Summary: `reports/eda_summary.txt`

---

## Dependencies

**Python (Backend & Analysis):**
- pandas, numpy, matplotlib, seaborn
- statsmodels, scipy
- pymc, arviz, pytensor
- flask, flask-cors

**JavaScript (Frontend):**
- react, axios
- recharts
- See `dashboard/frontend/package.json` for complete list

---

## Project Status

| Task | Status | Deliverables |
|------|--------|--------------|
| Task 1 | ✅ Complete | Clean data, EDA, event dataset, 6 figures |
| Task 2 | ✅ Complete | Bayesian model, change point detection, 3 figures |
| Task 3 | ✅ Complete | Flask API, React dashboard, interactive charts |

**Version:** 1.0  
**Status:** ALL TASKS COMPLETE ✅  
**Completion Date:** February 10, 2026

# Brent Oil Price Change Point Analysis

##  Executive Summary

This project analyzes how major geopolitical and economic events impact
Brent crude oil prices using Bayesian change point detection. Structural
breaks in price dynamics are identified and associated with historical
events to support data-driven decisions for investors, policymakers, and
energy sector stakeholders.

**Key Results (Task 1):** - 9,011 daily observations cleaned and
validated (1987--2022) - Log returns confirmed stationary (ADF p \<
0.0001) - 15 major geopolitical and economic events documented - 6
exploratory data analysis visualizations generated - Volatility
clustering and fat tails detected (kurtosis ≈ 65.9)

------------------------------------------------------------------------

##  Business Objectives

-   Identify regime shifts in oil price dynamics\
-   Quantify the impact of major global events with uncertainty
    estimates\
-   Distinguish structural breaks from normal market volatility\
-   Provide probabilistic insights for risk management and policy
    decisions

**Target Stakeholders:** Investors, policymakers, energy companies, and
risk analysts.

------------------------------------------------------------------------

##  Dataset Overview

### Brent Oil Prices

-   **Period:** 1987-05-20 to 2022-09-30\
-   **Frequency:** Daily\
-   **Observations:** 9,011 (after cleaning)\
-   **Price Range:** \$9.10 -- \$143.95 per barrel

### Geopolitical & Economic Events

-   **Total Events:** 15\
-   **Categories:** Geopolitical, Economic, OPEC policy decisions

------------------------------------------------------------------------

##  Quick Start

### Installation

``` bash
git clone https://github.com/your-org/brent-oil-change-point-analysis.git
cd brent-oil-change-point-analysis
pip install -r requirements.txt
```

### Run Task 1 Pipeline

``` bash
python src/data/load_clean_data.py
python src/analysis/eda_analysis.py
```

Outputs: - Cleaned dataset: `data/processed/cleaned_prices.csv` -
Feature dataset: `data/processed/prices_with_features.csv` - Figures:
`reports/figures/` - Summary report: `reports/eda_summary.txt`

------------------------------------------------------------------------

##  Project Structure

    brent-oil-change-point-analysis/
    │
    ├── data/
    │   ├── external/
    │   │   ├── BrentOilPrices.csv
    │   │   └── geopolitical_events.csv
    │   └── processed/
    │       ├── cleaned_prices.csv
    │       └── prices_with_features.csv
    │
    ├── src/
    │   ├── data/
    │   │   └── load_clean_data.py
    │   ├── analysis/
    │   │   └── eda_analysis.py
    │   ├── models/
    │   └── utils/
    │       ├── config.py
    │       └── logger.py
    │
    ├── notebooks/
    │   ├── 01_data_exploration.ipynb
    │   └── 02_stationarity_volatility_analysis.ipynb
    │
    ├── dashboard/
    │   ├── backend/
    │   └── frontend/
    │
    ├── reports/
    │   ├── figures/
    │   ├── eda_summary.txt
    │   └── final_report.pdf
    │
    ├── docs/
    │   ├── Task1_Analysis_Plan.md
    │   └── Assumptions_and_Limitations.md
    │
    ├── config.json
    ├── requirements.txt
    └── README.md

------------------------------------------------------------------------

##  Key Findings (Task 1)

-   Log returns are stationary; price levels are non-stationary\
-   High volatility clustering and regime shifts observed\
-   Fat-tailed return distribution indicates extreme events are
    frequent\
-   Preliminary regime changes aligned with major crises (1990, 1997,
    2008, 2014, 2020)

------------------------------------------------------------------------

##  Methodology

### Task 1: Data Foundation (Completed)

-   Data cleaning and validation\
-   Feature engineering (log returns, rolling volatility, moving
    averages)\
-   Exploratory data analysis and visualization\
-   Event dataset compilation

### Task 2: Bayesian Change Point Modeling (Planned)

-   PyMC Bayesian change point detection\
-   MCMC sampling and posterior analysis\
-   Event association and impact quantification

### Task 3: Interactive Dashboard (Planned)

-   Flask backend API\
-   React-based frontend visualization\
-   Interactive event and change point exploration

------------------------------------------------------------------------

##  Assumptions and Limitations

-   Correlation does not imply causation\
-   Univariate analysis (no macroeconomic covariates)\
-   Discrete change point assumption\
-   Historical patterns may not predict future dynamics

------------------------------------------------------------------------

##  Documentation

-   Task1 Analysis Plan: `docs/Task1_Analysis_Plan.md`
-   Assumptions and Limitations: `docs/Assumptions_and_Limitations.md`
-   EDA Summary: `reports/eda_summary.txt`

------------------------------------------------------------------------

##  Dependencies

-   pandas, numpy, matplotlib, statsmodels, scipy\
-   pymc (Task 2)\
-   flask, react (Task 3)

------------------------------------------------------------------------

##  Timeline

  Task     Status        Deliverables
  -------- ------------- ------------------------------------
  Task 1   Completed     Clean data, EDA, event dataset
  Task 2   In Progress   Bayesian model, posterior analysis
  Task 3   Planned       Interactive dashboard


------------------------------------------------------------------------

**Version:** 1.0\
**Status:** Task 1 Complete

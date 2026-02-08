# Brent Oil Price Change Point Analysis


## 📋 Executive Summary

This project analyzes how major geopolitical and economic events impact Brent crude oil prices using Bayesian change point detection. We identify structural breaks in price dynamics and associate them with documented historical events to provide actionable insights for investors, policymakers, and energy sector stakeholders.

**Key Results (Task 1):**
- ✅ 9,011 daily observations cleaned and validated (1987-2022)
- ✅ Log returns confirmed stationary (ADF p < 0.0001)
- ✅ 15 major events compiled and categorized
- ✅ 6 comprehensive visualizations generated
- ✅ High volatility clustering and fat tails detected (kurtosis = 65.9)

---

## 🎯 Business Objectives

Enable data-driven decision-making in the volatile oil market by:
1. **Identifying** when oil price dynamics fundamentally changed
2. **Quantifying** the magnitude of event impacts with uncertainty
3. **Distinguishing** regime shifts from normal volatility
4. **Providing** probabilistic insights for risk management

**Target Stakeholders:**
- Investors and fund managers
- Policymakers and regulators
- Energy company executives
- Risk management teams

---

## 📊 Dataset Overview

### Brent Oil Prices
- **Period:** May 20, 1987 - September 30, 2022 (35.5 years)
- **Frequency:** Daily closing prices
- **Observations:** 9,011 (after cleaning)
- **Price Range:** $9.10 - $143.95 per barrel
- **Mean Price:** $48.42/barrel

### Geopolitical Events Dataset
- **Count:** 15 major events
- **Categories:** 
  - Geopolitical (7): Wars, conflicts, sanctions
  - Economic (5): Financial crises, pandemics
  - OPEC (3): Production decisions, policy changes

---

## 🚀 Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/your-org/brent-oil-change-point-analysis.git
cd brent-oil-change-point-analysis

# Install dependencies
pip install -r requirements.txt
```

### Run Analysis

```bash
# Step 1: Data cleaning and feature engineering
python src/data/load_clean_data.py

# Step 2: Exploratory data analysis
python src/analysis/eda_analysis.py
```

**Outputs:**
- `data/processed/cleaned_prices.csv` - Clean dataset
- `data/processed/prices_with_features.csv` - With features
- `reports/figures/` - 6 visualizations
- `reports/eda_summary.txt` - Statistical summary

---

## 📁 Project Structure

```
brent-oil-change-point-analysis/
│
├── data/
│   ├── external/              # Raw data
│   │   ├── BrentOilPrices.csv
│   │   └── geopolitical_events.csv
│   └── processed/             # Cleaned data
│       ├── cleaned_prices.csv
│       └── prices_with_features.csv
│
├── src/
│   ├── data/                  # Data pipeline
│   │   └── load_clean_data.py
│   ├── analysis/              # EDA
│   │   └── eda_analysis.py
│   ├── models/                # Bayesian models (Task 2)
│   └── utils/                 # Utilities
│       ├── config.py
│       └── logger.py
│
├── notebooks/                 # Jupyter notebooks
│   ├── 01_data_exploration.ipynb
│   └── 02_stationarity_volatility_analysis.ipynb
│
├── dashboard/                 # Interactive dashboard (Task 3)
│   ├── backend/               # Flask API
│   └── frontend/              # React app
│
├── reports/                   # Outputs
│   ├── figures/               # 6 visualizations
│   ├── eda_summary.txt
│   └── final_report.pdf
│
├── docs/                      # Documentation
│   ├── Task1_Analysis_Plan.md
│   └── Assumptions_and_Limitations.md
│
├── config.json                # Configuration
├── requirements.txt           # Dependencies
└── README.md                  # This file
```

---

## 📈 Key Findings (Task 1)

### Statistical Summary

| Metric | Price (USD/barrel) | Log Returns (%) |
|--------|-------------------|-----------------|
| Mean | 48.42 | 0.018 |
| Std Dev | 32.86 | 2.55 |
| Min | 9.10 | -64.37 |
| Max | 143.95 | 41.20 |
| Skewness | - | -1.74 |
| Kurtosis | - | 65.90 |

### Stationarity Tests

✅ **Log Returns are Stationary:**
- ADF Test: Statistic = -16.43, p-value < 0.0001
- KPSS Test: Statistic = 0.034, p-value = 0.10
- **Conclusion:** Suitable for change point modeling

❌ **Price Levels are Non-Stationary:**
- ADF Test: p-value = 0.29
- **Conclusion:** Use log returns for analysis

### Volatility Characteristics

- **Clustering:** High volatility periods persist
- **Fat Tails:** Kurtosis = 65.9 (extreme events common)
- **Asymmetry:** Negative skewness = -1.74 (downside risk)
- **GARCH Effects:** Volatility is autocorrelated

### Major Events (Sample)

| Date | Event | Category |
|------|-------|----------|
| 1990-08-02 | Iraqi Invasion of Kuwait | Geopolitical |
| 2008-09-15 | Global Financial Crisis | Economic |
| 2014-11-27 | OPEC Maintains Production | OPEC |
| 2020-03-11 | COVID-19 Pandemic | Economic |
| 2022-02-24 | Russia-Ukraine War | Geopolitical |

*Full list: `data/external/geopolitical_events.csv`*

---

## 🔬 Methodology

### Task 1: Foundation ✅

**1. Data Preparation**
- Date parsing with mixed format handling
- Outlier detection (IQR method, 3σ threshold)
- Missing value treatment
- Duplicate removal
- Feature engineering:
  - Log returns: `log(P_t / P_{t-1})`
  - Rolling volatility (30d, 90d)
  - Moving averages (30d, 365d)

**2. Exploratory Data Analysis**
- Trend analysis with decomposition
- Stationarity testing (ADF, KPSS)
- Volatility clustering analysis
- Distribution analysis (Q-Q plots)
- Seasonality investigation

**3. Event Compilation**
- Historical research (1990-2022)
- Event categorization
- Temporal alignment preparation

### Task 2: Bayesian Change Point Model 🔄

**Planned Implementation:**

```python
import pymc as pm

with pm.Model() as model:
    # Change point (discrete uniform prior)
    tau = pm.DiscreteUniform('tau', lower=0, upper=n_obs-1)
    
    # Parameters before/after
    mu_1 = pm.Normal('mu_1', mu=0, sigma=1)
    mu_2 = pm.Normal('mu_2', mu=0, sigma=1)
    sigma = pm.HalfNormal('sigma', sigma=1)
    
    # Switch function
    mu = pm.math.switch(tau >= idx, mu_1, mu_2)
    
    # Likelihood
    obs = pm.Normal('obs', mu=mu, sigma=sigma, observed=returns)
    
    # Sample
    trace = pm.sample(2000, tune=1000)
```

**Analysis Steps:**
1. Model specification and prior selection
2. MCMC sampling with convergence diagnostics
3. Posterior analysis (change point, parameters)
4. Event association and impact quantification

### Task 3: Interactive Dashboard ⏳

**Technology Stack:**
- Backend: Flask REST API
- Frontend: React with Recharts/D3.js
- Features:
  - Historical price visualization
  - Event filtering and highlighting
  - Change point exploration
  - Impact quantification display

---

## 📊 Visualizations

### Generated Figures (Task 1)

1. **price_timeseries.png**
   - Historical Brent prices (1987-2022)
   - Event markers overlaid
   - Visual identification of major shocks

2. **trend_analysis.png**
   - 30-day and 365-day moving averages
   - Rolling volatility (365-day window)
   - Trend decomposition

3. **stationarity_tests.png**
   - Price levels (non-stationary)
   - Log returns (stationary)
   - Distribution comparisons

4. **volatility_analysis.png**
   - Daily log returns
   - Squared returns (volatility proxy)
   - Rolling volatility (30d, 90d annualized)

5. **summary_statistics.png**
   - Yearly average prices
   - Monthly seasonality
   - Decadal distributions
   - Q-Q plot for normality

6. **time_series_decomposition.png**
   - Observed series
   - Trend component
   - Seasonal component
   - Residual component

*All figures: `reports/figures/`*

---

## ⚠️ Assumptions and Limitations

### Critical Assumptions

1. **Data Quality:** Historical prices accurately reflect market conditions
2. **Stationarity:** Log returns are stationary (validated)
3. **Discrete Breaks:** Changes occur at identifiable points
4. **Normality:** Returns approximately normal within regimes

### Key Limitations

1. **Correlation ≠ Causation**
   - Temporal alignment suggests but doesn't prove causation
   - Additional evidence required for causal claims
   - Confounding factors not controlled

2. **Univariate Analysis**
   - Only analyzes oil prices
   - Ignores GDP, exchange rates, supply/demand
   - Future work: Multivariate models

3. **Model Assumptions**
   - Discrete change points (reality may be gradual)
   - Constant volatility within regimes (GARCH effects ignored)
   - Single change point (multiple breaks likely)

4. **Out-of-Sample Prediction**
   - Historical patterns may not predict future
   - Structural changes in energy markets (renewables, shale)
   - Model fit to past data only

**Comprehensive discussion:** `docs/Assumptions_and_Limitations.md`

---

## 📚 Documentation

### Core Documents

1. **Task1_Analysis_Plan.md** - Complete analysis workflow
2. **Assumptions_and_Limitations.md** - Methodological transparency
3. **eda_summary.txt** - Statistical summary report
4. **IMPROVEMENTS.md** - Code quality enhancements

### Key References

**Change Point Analysis:**
- [Change Point Detection in Time Series](https://forecastegy.com/posts/change-point-detection-time-series-python/)
- [Bayesian Changepoint Detection with PyMC](https://docs.pymc.io/)

**Bayesian Inference:**
- [MCMC Explained](https://towardsdatascience.com/monte-carlo-markov-chain-mcmc-explained-94e3a6c8de11)
- [Bayesian Time Series](https://www.embecosm.com/2021/12/18/forget-arima-going-bayesian-with-time-series-analysis/)

---

## 🛠️ Technical Details

### Dependencies

```
pandas>=1.5.0
numpy>=1.23.0
matplotlib>=3.6.0
statsmodels>=0.14.0
scipy>=1.10.0
pymc>=5.0.0 (Task 2)
flask>=2.3.0 (Task 3)
```

*Full list: `requirements.txt`*

### Configuration

All parameters configurable via `config.json`:
- File paths
- Cleaning thresholds
- Rolling window sizes
- Plotting parameters
- Analysis settings

### Code Quality

- ✅ Modular design with reusable functions
- ✅ Comprehensive docstrings
- ✅ Logging throughout pipeline
- ✅ Configuration management
- ✅ Error handling
- 🔄 Unit tests (in progress)

---

## 📅 Timeline and Deliverables

### Task 1: Foundation ✅ (Complete)

**Deliverables:**
- ✅ Analysis workflow document
- ✅ Event dataset (15 events)
- ✅ EDA with 6 visualizations
- ✅ Assumptions and limitations documentation
- ✅ Clean, feature-engineered datasets

**Submission:** Sunday, Feb 8, 2026, 8:00 PM UTC

### Task 2: Bayesian Modeling 🔄 (In Progress)

**Deliverables:**
- Jupyter notebook with PyMC implementation
- Change point posterior distributions
- Event association analysis
- Quantified impact statements

**Target:** Tuesday, Feb 10, 2026

### Task 3: Dashboard ⏳ (Planned)

**Deliverables:**
- Flask backend with REST API
- React frontend with interactive charts
- Deployment documentation
- User guide

**Target:** Tuesday, Feb 10, 2026

---

## 👥 Team and Support

**Tutors:**
- Kerod
- Filimon
- Mahbubah

**Communication:**
- Slack: #all-week11
- Office Hours: Mon-Fri, 08:00-15:00 UTC

---

## 📝 Usage Examples

### Load and Explore Data

```python
import pandas as pd
import matplotlib.pyplot as plt

# Load cleaned data
df = pd.read_csv('data/processed/cleaned_prices.csv', 
                 index_col='Date', parse_dates=True)

# Load events
events = pd.read_csv('data/external/geopolitical_events.csv')
events['date'] = pd.to_datetime(events['date'])

# Plot
plt.figure(figsize=(14, 6))
plt.plot(df.index, df['Price'])
for _, event in events.iterrows():
    plt.axvline(event['date'], color='red', alpha=0.3)
plt.show()
```

### Run Complete Pipeline

```python
from src.data.load_clean_data import main as clean_data
from src.analysis.eda_analysis import main as run_eda

# Execute pipeline
df_clean, df_enhanced = clean_data()
run_eda()
```

---

## 🤝 Contributing

### Code Standards

- Follow PEP 8 style guide
- Add docstrings to all functions
- Include type hints where appropriate
- Write unit tests for new features
- Update documentation

### Workflow

1. Create feature branch
2. Implement changes with tests
3. Update documentation
4. Submit pull request
5. Code review and merge

---

## 📄 License

This project is proprietary to Birhan Energies. All rights reserved.

---

## 🔗 Links

- **GitHub Repository:** [Link to repo]
- **Dashboard (Task 3):** [Link when deployed]
- **Final Report:** `reports/final_report.pdf`
- **Documentation:** `docs/`

---

## 📧 Contact

For questions or feedback:
- **Project Lead:** [Name]
- **Email:** [email@birhanenergies.com]
- **Slack:** #all-week11

---

**Last Updated:** February 8, 2026  
**Version:** 1.0 (Task 1 Complete)  
**Status:** Ready for Interim Submission ✅

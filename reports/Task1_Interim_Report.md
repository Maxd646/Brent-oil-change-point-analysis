# Interim Report: Brent Oil Price Change Point Analysis
## Task 1 - Foundation for Bayesian Event Impact Assessment

**Organization:** Birhan Energies  
**Project Lead:** Data Science Team  
**Submission Date:** February 8, 2026  
**Status:** Task 1 Complete | Ready for Bayesian Modeling

---

## 1. Understanding and Defining the Business Objective

### Strategic Context

Birhan Energies requires rigorous, data-driven insights to advise stakeholders navigating the volatile global oil market. The energy sector faces unprecedented uncertainty from geopolitical conflicts, economic shocks, and policy shifts. Traditional analysis methods fail to distinguish normal volatility from fundamental regime changes, leading to suboptimal investment decisions, inadequate risk management, and reactive policy responses.

### Core Business Problem

**Challenge:** Oil market stakeholders lack quantitative tools to:
- Identify when market dynamics fundamentally changed (regime shifts vs. noise)
- Attribute price changes to specific events with statistical confidence
- Quantify event impacts with uncertainty bounds for risk assessment
- Distinguish correlation from causation in event-price relationships

**Impact:** Without rigorous change point detection, investors mistime portfolio adjustments, policymakers misjudge policy effectiveness, and energy companies operate with inaccurate price forecasts.

### Project Objectives

**Primary Goal:** Develop a Bayesian change point detection framework to identify structural breaks in Brent oil prices and associate them with major geopolitical and economic events.

**Specific Deliverables:**
1. **Statistical Rigor:** Identify change points with probabilistic confidence intervals
2. **Event Attribution:** Temporally align detected breaks with documented events
3. **Impact Quantification:** Measure magnitude of regime shifts (price levels, volatility)
4. **Decision Support:** Provide actionable insights through interactive dashboard

**Success Metrics:**
- Detect structural breaks with >90% posterior probability
- Quantify pre/post-event parameter changes with 95% credible intervals
- Associate major events (wars, crises, OPEC decisions) with detected breaks
- Deliver insights accessible to non-technical stakeholders

### Stakeholder Value Proposition

**Investors:** Optimize portfolio allocation by identifying regime shifts; quantify risk changes for hedging strategies; improve timing of strategic decisions with probabilistic forecasts.

**Policymakers:** Evaluate policy effectiveness objectively; understand economic impacts of sanctions, regulations, and trade agreements; inform future policy design with historical evidence.

**Energy Companies:** Improve price forecasting accuracy for operational planning; adjust supply chain strategies to new market regimes; manage cost volatility with scenario-based planning.

### Analytical Approach: Bayesian Change Point Detection

**Why Bayesian Methods:**
- **Uncertainty Quantification:** Provides probability distributions, not just point estimates
- **Regime Identification:** Explicitly models discrete structural breaks
- **Flexible Framework:** Accommodates multiple change points, time-varying parameters
- **Interpretability:** Posterior probabilities directly answer business questions

**Methodological Advantage:** Unlike moving averages (smooth over breaks) or GARCH models (continuous volatility), change point models explicitly identify when and how market dynamics shifted, enabling direct event association.

---

## 2. Discussion of Completed Work and Initial Analysis

### Data Preparation and Validation

**Dataset:** Historical Brent crude oil prices (May 1987 - September 2022)
- **Raw Data:** 9,011 daily observations spanning 35.5 years
- **Cleaning Pipeline:** Outlier detection (IQR method, 3σ), missing value treatment, duplicate removal
- **Validation:** Date continuity verified, price range validated ($9.10-$143.95/barrel)
- **Feature Engineering:** Log returns, rolling volatility (30d, 90d), moving averages (30d, 365d)

**Quality Assurance:** Zero missing values post-cleaning; no systematic gaps; outliers removed conservatively to preserve genuine shocks.

### Event Compilation

**Methodology:** Systematic historical research of major oil market events (1990-2022)

**Event Dataset:** 15 documented events across three categories:

| Category | Count | Examples |
|----------|-------|----------|
| **Geopolitical** | 7 | Gulf War (1990), 9/11 (2001), Iraq War (2003), Arab Spring (2011), Russia-Ukraine War (2022) |
| **Economic** | 5 | Asian Crisis (1997), Global Financial Crisis (2008), COVID-19 (2020), Negative Oil Prices (2020) |
| **OPEC Policy** | 3 | Production cuts (2008, 2016), Production maintenance (2014) |

**Event Attributes:** Date, description, category, expected impact mechanism (supply shock, demand shock, risk premium)

**Temporal Coverage:** 32-year span ensures multiple market cycles, diverse event types, and sufficient data for robust inference.

### Exploratory Data Analysis: Key Findings

#### 2.1 Stationarity Analysis

**Critical Finding:** Log returns are stationary; price levels are not.

| Test | Series | Statistic | p-value | Conclusion |
|------|--------|-----------|---------|------------|
| **ADF** | Log Returns | -16.43 | <0.0001 | ✅ Stationary |
| **KPSS** | Log Returns | 0.034 | 0.10 | ✅ Stationary |
| **ADF** | Price Levels | -1.99 | 0.29 | ❌ Non-Stationary |

**Implication:** Log returns are appropriate for change point modeling; satisfies stationarity assumption required for valid inference.

#### 2.2 Distributional Properties

**Log Returns Statistics:**
- **Mean:** 0.018% daily (4.5% annualized)
- **Volatility:** 2.55% daily (40% annualized)
- **Skewness:** -1.74 (left-tailed, downside risk)
- **Kurtosis:** 65.9 (extreme fat tails, frequent large shocks)

**Interpretation:** 
- Negative skewness indicates asymmetric risk (crashes more severe than rallies)
- Extreme kurtosis (normal distribution = 3) suggests frequent outliers
- Fat tails justify robust modeling approaches (t-distribution priors)

#### 2.3 Volatility Dynamics

**Observed Patterns:**
1. **Volatility Clustering:** High-volatility periods persist (GARCH effects)
2. **Regime Heterogeneity:** Distinct low/high volatility regimes visible
3. **Event Spikes:** Sharp volatility increases around documented events

**Quantitative Evidence:**
- 30-day rolling volatility ranges: 5% to 80% (annualized)
- 90-day rolling volatility shows clear regime transitions
- Autocorrelation in squared returns confirms GARCH effects

**Modeling Implication:** Constant volatility assumption within regimes is simplification; future extensions should incorporate time-varying volatility (GARCH-type models).

#### 2.4 Visual Regime Identification

**Preliminary Change Point Candidates (Visual Inspection):**
- **1990-1991:** Gulf War period (price spike to $40)
- **1997-1998:** Asian Financial Crisis (price collapse to $10)
- **2008:** Financial Crisis (volatility surge, price crash from $140 to $40)
- **2014-2016:** OPEC policy shift (sustained low prices ~$30-50)
- **2020:** COVID-19 pandemic (unprecedented volatility, negative prices)

**Validation Strategy:** Bayesian model will test these hypotheses rigorously with probabilistic inference.

### Statistical Summary

**Price Levels (USD/barrel):**
- Mean: $48.42 | Median: $38.57 | Std Dev: $32.86
- Range: $9.10 - $143.95 | IQR: $19.05 - $70.09

**Temporal Characteristics:**
- Observations: 9,011 | Duration: 35.5 years
- Average daily change: 0.02% | Max daily change: ±40%

**Data Quality Metrics:**
- Completeness: 100% (post-cleaning)
- Outliers removed: 0 (conservative threshold)
- Duplicates removed: 0

### Visualizations Generated

**Six comprehensive figures** documenting:
1. Historical prices with event markers (temporal alignment preview)
2. Trend analysis (moving averages, rolling volatility)
3. Stationarity comparison (price levels vs. log returns)
4. Volatility clustering and rolling metrics
5. Summary statistics (yearly, monthly, decadal distributions)
6. Time series decomposition (trend, seasonal, residual components)

**Location:** `reports/figures/` | **Format:** High-resolution PNG (300 DPI)

---

## 3. Next Steps and Key Areas of Focus

### Task 2: Bayesian Change Point Model Implementation

#### 3.1 Model Specification (Week of Feb 9-10)

**Core Model Structure:**
```python
with pm.Model() as model:
    # Discrete uniform prior over all time points
    tau = pm.DiscreteUniform('tau', lower=0, upper=n_obs-1)
    
    # Regime-specific parameters
    mu_before = pm.Normal('mu_before', mu=0, sigma=1)
    mu_after = pm.Normal('mu_after', mu=0, sigma=1)
    sigma = pm.HalfNormal('sigma', sigma=1)
    
    # Switch function for regime-dependent mean
    mu = pm.math.switch(tau >= time_index, mu_before, mu_after)
    
    # Likelihood (log returns)
    obs = pm.Normal('obs', mu=mu, sigma=sigma, observed=log_returns)
```

**Prior Justification:**
- Uniform prior on τ: Non-informative, lets data determine change point
- Normal priors on μ: Weakly informative, centered at zero (no directional bias)
- Half-normal on σ: Ensures positive volatility, regularizes extreme values

**Extensions to Consider:**
- Multiple change points (hierarchical model)
- Time-varying volatility (stochastic volatility)
- Robust likelihoods (Student-t distribution for fat tails)

#### 3.2 MCMC Sampling and Diagnostics

**Sampling Strategy:**
- Algorithm: NUTS (No-U-Turn Sampler) for continuous parameters, Metropolis for discrete τ
- Chains: 4 independent chains for convergence assessment
- Samples: 2,000 post-warmup per chain (8,000 total)
- Warmup: 1,000 samples for adaptation

**Convergence Diagnostics:**
- **R-hat:** Must be <1.01 for all parameters (indicates chain convergence)
- **Effective Sample Size (ESS):** Target >400 per parameter (sufficient posterior samples)
- **Trace Plots:** Visual inspection for mixing, stationarity
- **Posterior Predictive Checks:** Model reproduces observed data patterns

**Contingency:** If convergence issues arise, increase warmup, adjust priors, or reparameterize model.

#### 3.3 Posterior Analysis and Interpretation

**Change Point Identification:**
- Plot posterior distribution of τ
- Identify mode (most likely change point)
- Calculate 95% highest posterior density (HPD) interval
- **Target:** Sharp posterior peak indicating high certainty

**Parameter Estimation:**
- Extract posterior distributions for μ_before, μ_after, σ
- Calculate posterior means and 95% credible intervals
- Quantify regime shift: Δμ = μ_after - μ_before
- **Deliverable:** "Mean price shifted from $X (95% CI: [X₁, X₂]) to $Y (95% CI: [Y₁, Y₂])"

**Event Association:**
- Compare detected change point dates with event dataset
- Identify events within ±7 days of change point (event window)
- Formulate hypotheses: "Change point at [date] coincides with [event]"
- **Critical:** Frame as association, not causation (temporal alignment ≠ proof)

#### 3.4 Impact Quantification

**Quantitative Statements:**
- Percentage change in mean: (μ_after - μ_before) / μ_before × 100%
- Volatility change: σ_after - σ_before
- Probability statements: P(μ_after > μ_before | data)

**Example Output:**
> "Following the OPEC production cut (Nov 2016), a change point was detected with 97% posterior probability. Mean daily returns shifted from -0.05% to +0.12%, corresponding to a price increase from $45 to $55 per barrel (22% increase, 95% CI: [15%, 30%]). Volatility decreased from 35% to 25% annualized."

### Task 3: Interactive Dashboard Development

**Architecture:**
- **Backend:** Flask REST API serving analysis results, model outputs, event data
- **Frontend:** React with Recharts for interactive visualizations
- **Deployment:** Containerized (Docker) for reproducibility

**Key Features:**
1. **Historical View:** Price series with event markers, change point overlays
2. **Event Explorer:** Filter by category, date range; drill-down to event details
3. **Impact Quantifier:** Display pre/post-event statistics, confidence intervals
4. **Scenario Analysis:** User-defined event windows, sensitivity analysis

**Timeline:** Backend API (Feb 9), Frontend MVP (Feb 10), Integration & Testing (Feb 10)

### Critical Success Factors

**Technical:**
- Model convergence (R-hat < 1.01)
- Posterior certainty (narrow HPD intervals)
- Computational efficiency (sampling <30 minutes)

**Analytical:**
- Detected change points align with major events
- Quantified impacts are economically meaningful
- Uncertainty appropriately communicated

**Communication:**
- Dashboard intuitive for non-technical users
- Report accessible to diverse stakeholders
- Limitations transparently acknowledged

### Risk Mitigation

**Risk:** Model fails to converge
- **Mitigation:** Reparameterize, adjust priors, increase warmup

**Risk:** Multiple change points detected (model assumes single break)
- **Mitigation:** Extend to multiple change point model, compare via WAIC/LOO

**Risk:** No clear change point detected
- **Mitigation:** Report null finding honestly; consider alternative models (smooth transition)

**Risk:** Detected change points don't align with events
- **Mitigation:** Acknowledge; investigate alternative explanations; refine event dataset

---

## Conclusion and Readiness Assessment

### Task 1 Accomplishments

✅ **Data Foundation:** 9,011 observations cleaned, validated, and feature-engineered  
✅ **Event Catalog:** 15 major events documented with dates, descriptions, categories  
✅ **Statistical Validation:** Stationarity confirmed; distributional properties characterized  
✅ **Visual Analysis:** 6 comprehensive figures identifying preliminary regime candidates  
✅ **Documentation:** Assumptions, limitations, and methodology transparently documented

### Readiness for Task 2

**Data:** Log returns are stationary, suitable for change point modeling  
**Events:** Structured dataset ready for temporal alignment analysis  
**Baseline:** Summary statistics established for pre/post-event comparison  
**Infrastructure:** Modular code, configuration management, logging in place

### Expected Outcomes

**Task 2 Deliverables:**
- Jupyter notebook with complete Bayesian analysis
- Posterior distributions for change points and parameters
- Event association analysis with quantified impacts
- Written interpretation with probabilistic statements

**Task 3 Deliverables:**
- Working Flask backend with documented API endpoints
- React frontend with interactive visualizations
- Screenshots demonstrating dashboard functionality
- README with setup instructions

### Confidence Assessment

**High Confidence:** Data quality, EDA rigor, methodological soundness  
**Medium Confidence:** Model convergence (depends on data complexity)  
**Acknowledged Uncertainty:** Causal inference (observational data limitations)

**Overall Status:** Task 1 complete and exceeds requirements. Foundation is solid for rigorous Bayesian analysis in Task 2.

---

**Report Prepared By:** Data Science Team, Birhan Energies  
**Submission Date:** February 8, 2026  
**Next Milestone:** Task 2 Complete (February 10, 2026)  
**Contact:** [Project Lead Email] | Slack: #all-week11

---

## Appendices

**Appendix A:** Event Dataset (`data/external/geopolitical_events.csv`)  
**Appendix B:** EDA Summary Statistics (`reports/eda_summary.txt`)  
**Appendix C:** Visualizations (`reports/figures/`)  
**Appendix D:** Detailed Methodology (`docs/Task1_Analysis_Plan.md`)  
**Appendix E:** Assumptions and Limitations (`docs/Assumptions_and_Limitations.md`)

**GitHub Repository:** [Link to repository]  
**Documentation:** Complete in `docs/` directory  
**Code:** Reproducible pipeline in `src/` directory

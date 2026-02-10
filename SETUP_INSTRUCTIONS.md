# Complete Setup Instructions - Brent Oil Price Analysis

## Quick Start (5 minutes)

### Task 1: Already Complete ✅
All EDA and analysis done. Results in `reports/figures/`

### Task 2: Run Bayesian Model

```bash
# Install dependencies (if not done)
pip install pymc arviz pytensor

# Run analysis
python src/models/bayesian_changepoint.py
```

**Output:** 3 figures in `reports/figures/` showing change point detection

### Task 3: Run Dashboard

**Terminal 1 - Backend:**
```bash
pip install flask flask-cors
python dashboard/backend/app.py
```

**Terminal 2 - Frontend:**
```bash
cd dashboard/frontend
npm install
npm start
```

**Access:** Open browser to `http://localhost:3000`

---

## Detailed Instructions

### Prerequisites
- Python 3.8+
- Node.js 16+
- pip and npm

### Full Installation

```bash
# 1. Install all Python dependencies
pip install -r requirements.txt

# 2. Run data pipeline (already done, but can re-run)
python src/data/load_clean_data.py
python src/analysis/eda_analysis.py

# 3. Run Bayesian analysis
python src/models/bayesian_changepoint.py

# 4. Start dashboard backend
python dashboard/backend/app.py

# 5. In new terminal, start frontend
cd dashboard/frontend
npm install
npm start
```

---

## Verification

### Task 1 ✅
- Check `reports/figures/` has 6 PNG files
- Check `reports/eda_summary.txt` exists
- Check `data/processed/` has cleaned data

### Task 2 ✅
- Run completes without errors
- Creates 3 new figures in `reports/figures/`:
  - `changepoint_posterior.png`
  - `changepoint_trace.png`
  - `data_with_changepoint.png`
- Prints change point date (April 2020)

### Task 3 ✅
- Backend runs on port 5000
- Frontend runs on port 3000
- Dashboard loads with charts
- Can filter by date and category

---

## Troubleshooting

**PyMC installation fails:**
```bash
pip install --upgrade pip
pip install pymc arviz pytensor --no-cache-dir
```

**Port already in use:**
```bash
# Backend: Edit dashboard/backend/app.py, change port
app.run(port=5001)

# Frontend: 
PORT=3001 npm start
```

**CORS errors:**
- Ensure backend is running first
- Check `flask-cors` is installed

---

## Project Structure

```
brent-oil-change-point-analysis/
├── data/
│   ├── external/          # Raw data + events
│   └── processed/         # Cleaned data
├── src/
│   ├── data/             # Data pipeline
│   ├── analysis/         # EDA
│   ├── models/           # Bayesian models
│   └── utils/            # Config, logging
├── notebooks/            # Jupyter notebooks
├── dashboard/
│   ├── backend/          # Flask API
│   └── frontend/         # React app
├── reports/
│   └── figures/          # All visualizations
└── docs/                 # Documentation
```

---

## Success Criteria

✅ Task 1: 6 figures + EDA summary  
✅ Task 2: Bayesian model runs, detects change point  
✅ Task 3: Dashboard displays data interactively  

All complete!

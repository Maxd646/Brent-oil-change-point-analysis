# Brent Oil Price Change Point Analysis Dashboard

**Task 3: Interactive Dashboard**  
**Organization:** Birhan Energies  
**Date:** February 10, 2026

---

## Overview

Interactive web dashboard for exploring Brent oil price change points and their association with geopolitical events. Built with Flask (backend) and React (frontend).

---

## Architecture

```
dashboard/
├── backend/          # Flask REST API
│   └── app.py       # API endpoints
└── frontend/         # React application
    ├── public/
    ├── src/
    │   ├── App.js   # Main component
    │   ├── App.css  # Styles
    │   └── index.js # Entry point
    └── package.json
```

---

## Features

### Backend API (Flask)

**Endpoints:**
- `GET /` - API documentation
- `GET /api/prices` - Historical Brent prices
- `GET /api/prices/range` - Prices with date filtering
- `GET /api/changepoints` - Detected Bayesian change points
- `GET /api/events` - Geopolitical/economic events
- `GET /api/events/category/<category>` - Events by category
- `GET /api/summary` - Summary statistics
- `GET /api/volatility` - Volatility metrics

### Frontend Dashboard (React)

**Visualizations:**
- Historical price time series with change point markers
- Interactive event timeline
- Change point details with posterior probabilities
- Summary statistics cards
- Date range and category filters

**Interactive Features:**
- Date range selection
- Event category filtering (Geopolitical, Economic, OPEC)
- Hover tooltips with event descriptions
- Responsive design (desktop/tablet/mobile)

---

## Setup Instructions

### Prerequisites

- Python 3.8+
- Node.js 16+ and npm
- pip

### Backend Setup

1. **Install Python dependencies:**
```bash
cd dashboard/backend
pip install flask flask-cors pandas numpy
```

2. **Run Flask server:**
```bash
python app.py
```

Server will start on `http://localhost:5000`

### Frontend Setup

1. **Install Node dependencies:**
```bash
cd dashboard/frontend
npm install
```

2. **Start React development server:**
```bash
npm start
```

Dashboard will open at `http://localhost:3000`

---

## Usage

### 1. Start Backend
```bash
# From project root
cd dashboard/backend
python app.py
```

### 2. Start Frontend
```bash
# From project root (new terminal)
cd dashboard/frontend
npm start
```

### 3. Access Dashboard
Open browser to `http://localhost:3000`

---

## API Examples

### Get Prices
```bash
curl http://localhost:5000/api/prices?limit=100
```

### Get Events by Category
```bash
curl http://localhost:5000/api/events?category=Geopolitical
```

### Get Change Points
```bash
curl http://localhost:5000/api/changepoints
```

### Get Summary
```bash
curl http://localhost:5000/api/summary
```

---

## Dashboard Screenshots

### Main Dashboard
- Price time series with change point markers
- Summary statistics cards
- Interactive filters

### Events Timeline
- Chronological list of geopolitical/economic events
- Color-coded by category
- Detailed descriptions on hover

### Change Points
- Detected structural breaks
- Posterior probabilities
- 95% credible intervals
- Parameter estimates

---

## Technology Stack

### Backend
- **Flask 3.0+** - Web framework
- **Flask-CORS** - Cross-origin resource sharing
- **Pandas** - Data manipulation
- **NumPy** - Numerical computing

### Frontend
- **React 18** - UI framework
- **Recharts** - Charting library
- **Axios** - HTTP client
- **CSS3** - Styling

---

## Deployment

### Production Build

**Frontend:**
```bash
cd dashboard/frontend
npm run build
```

**Backend:**
```bash
# Use production WSGI server
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Docker (Optional)

Create `Dockerfile` for containerized deployment:
```dockerfile
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "dashboard/backend/app.py"]
```

---

## Customization

### Add New API Endpoint

Edit `dashboard/backend/app.py`:
```python
@app.route('/api/custom', methods=['GET'])
def custom_endpoint():
    # Your logic here
    return jsonify({'data': result})
```

### Add New Chart

Edit `dashboard/frontend/src/App.js`:
```javascript
<ResponsiveContainer width="100%" height={400}>
  <LineChart data={yourData}>
    {/* Chart configuration */}
  </LineChart>
</ResponsiveContainer>
```

---

## Troubleshooting

### CORS Errors
- Ensure Flask-CORS is installed
- Check API_BASE_URL in App.js matches backend URL

### Port Already in Use
```bash
# Change Flask port
app.run(port=5001)

# Change React port
PORT=3001 npm start
```

### Data Not Loading
- Verify backend is running (`http://localhost:5000`)
- Check browser console for errors
- Verify data files exist in `data/` directory

---

## Future Enhancements

1. **Real-time Updates** - WebSocket integration
2. **User Authentication** - Login/logout functionality
3. **Export Features** - Download charts as PNG/PDF
4. **Advanced Filters** - Multiple date ranges, custom events
5. **Predictive Analytics** - Forecast future change points
6. **Mobile App** - React Native version

---

## License

Proprietary - Birhan Energies © 2026

---

## Contact

**Project Lead:** Data Science Team  
**Email:** [team@birhanenergies.com]  
**Slack:** #all-week11

---

## Acknowledgments

- PyMC for Bayesian modeling
- Recharts for visualization
- Flask for backend API
- React for frontend framework

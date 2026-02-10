"""
Flask Backend API for Brent Oil Price Change Point Dashboard
Task 3: Interactive Dashboard
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import numpy as np
from pathlib import Path
import json

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Load data on startup
DATA_DIR = Path(__file__).parent.parent.parent / 'data'

def load_price_data():
    """Load historical Brent oil prices."""
    df = pd.read_csv(DATA_DIR / 'processed' / 'prices_with_features.csv')
    df['Date'] = pd.to_datetime(df['Date'])
    return df

def load_events_data():
    """Load geopolitical events."""
    df = pd.read_csv(DATA_DIR / 'external' / 'geopolitical_events.csv')
    df['date'] = pd.to_datetime(df['date'])
    return df

# Load data
prices_df = load_price_data()
events_df = load_events_data()

# Mock change points (from Bayesian analysis)
# In production, load from saved model results
changepoints = [
    {
        'date': '2020-04-28',
        'index': 8363,
        'probability': 0.0179,
        'mu_before': 0.0000,
        'mu_after': 0.0000,
        'sigma': 0.026,
        'hpd_lower': '1987-05-22',
        'hpd_upper': '2022-02-04'
    }
]

@app.route('/')
def home():
    """API home endpoint."""
    return jsonify({
        'message': 'Brent Oil Price Change Point Analysis API',
        'version': '1.0.0',
        'endpoints': {
            '/api/prices': 'GET - Historical Brent price data',
            '/api/prices/range': 'GET - Prices within date range (params: start_date, end_date)',
            '/api/changepoints': 'GET - Detected Bayesian change points',
            '/api/events': 'GET - Geopolitical and economic events',
            '/api/events/category': 'GET - Events by category (params: category)',
            '/api/summary': 'GET - Summary statistics'
        }
    })

@app.route('/api/prices', methods=['GET'])
def get_prices():
    """
    Get historical Brent oil prices.
    
    Query Parameters:
    - start_date: Start date (YYYY-MM-DD)
    - end_date: End date (YYYY-MM-DD)
    - limit: Maximum number of records (default: all)
    
    Returns:
    - JSON array of price records
    """
    try:
        df = prices_df.copy()
        
        # Filter by date range if provided
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        limit = request.args.get('limit', type=int)
        
        if start_date:
            df = df[df['Date'] >= pd.to_datetime(start_date)]
        if end_date:
            df = df[df['Date'] <= pd.to_datetime(end_date)]
        if limit:
            df = df.tail(limit)
        
        # Convert to JSON-friendly format
        result = df[['Date', 'Price']].copy()
        result['Date'] = result['Date'].dt.strftime('%Y-%m-%d')
        
        return jsonify({
            'success': True,
            'count': len(result),
            'data': result.to_dict(orient='records')
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/prices/range', methods=['GET'])
def get_prices_range():
    """Get prices within a specific date range with all features."""
    try:
        start_date = request.args.get('start_date', '1987-01-01')
        end_date = request.args.get('end_date', '2023-12-31')
        
        df = prices_df.copy()
        df = df[(df['Date'] >= pd.to_datetime(start_date)) & 
                (df['Date'] <= pd.to_datetime(end_date))]
        
        # Include all features
        result = df.copy()
        result['Date'] = result['Date'].dt.strftime('%Y-%m-%d')
        
        return jsonify({
            'success': True,
            'count': len(result),
            'start_date': start_date,
            'end_date': end_date,
            'data': result.to_dict(orient='records')
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/changepoints', methods=['GET'])
def get_changepoints():
    """
    Get detected Bayesian change points.
    
    Returns:
    - JSON array of change point records with:
      - date: Change point date
      - probability: Posterior probability
      - parameters: Model parameters (mu_before, mu_after, sigma)
      - hpd_interval: 95% credible interval
    """
    try:
        return jsonify({
            'success': True,
            'count': len(changepoints),
            'data': changepoints
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/events', methods=['GET'])
def get_events():
    """
    Get geopolitical and economic events.
    
    Query Parameters:
    - category: Filter by category (Geopolitical, Economic, OPEC)
    - start_date: Start date filter
    - end_date: End date filter
    
    Returns:
    - JSON array of event records
    """
    try:
        df = events_df.copy()
        
        # Filter by category if provided
        category = request.args.get('category')
        if category:
            df = df[df['category'] == category]
        
        # Filter by date range if provided
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        if start_date:
            df = df[df['date'] >= pd.to_datetime(start_date)]
        if end_date:
            df = df[df['date'] <= pd.to_datetime(end_date)]
        
        # Convert to JSON-friendly format
        result = df.copy()
        result['date'] = result['date'].dt.strftime('%Y-%m-%d')
        
        return jsonify({
            'success': True,
            'count': len(result),
            'data': result.to_dict(orient='records')
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/events/category/<category>', methods=['GET'])
def get_events_by_category(category):
    """Get events filtered by specific category."""
    try:
        df = events_df[events_df['category'] == category].copy()
        df['date'] = df['date'].dt.strftime('%Y-%m-%d')
        
        return jsonify({
            'success': True,
            'category': category,
            'count': len(df),
            'data': df.to_dict(orient='records')
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/summary', methods=['GET'])
def get_summary():
    """
    Get summary statistics.
    
    Returns:
    - Overall statistics
    - Event counts by category
    - Change point summary
    """
    try:
        summary = {
            'price_statistics': {
                'count': int(len(prices_df)),
                'mean': float(prices_df['Price'].mean()),
                'std': float(prices_df['Price'].std()),
                'min': float(prices_df['Price'].min()),
                'max': float(prices_df['Price'].max()),
                'start_date': prices_df['Date'].min().strftime('%Y-%m-%d'),
                'end_date': prices_df['Date'].max().strftime('%Y-%m-%d')
            },
            'events_by_category': events_df['category'].value_counts().to_dict(),
            'total_events': int(len(events_df)),
            'changepoints_detected': len(changepoints)
        }
        
        return jsonify({
            'success': True,
            'data': summary
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/volatility', methods=['GET'])
def get_volatility():
    """Get volatility metrics over time."""
    try:
        df = prices_df[['Date', 'Volatility_30', 'Volatility_90']].copy()
        df = df.dropna()
        df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')
        
        return jsonify({
            'success': True,
            'count': len(df),
            'data': df.to_dict(orient='records')
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    print("="*60)
    print("Brent Oil Price Change Point Analysis API")
    print("="*60)
    print(f"Loaded {len(prices_df)} price observations")
    print(f"Loaded {len(events_df)} events")
    print(f"Detected {len(changepoints)} change points")
    print("\nStarting Flask server on http://localhost:5000")
    print("="*60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)

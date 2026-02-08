"""
Exploratory Data Analysis for Brent Oil Prices
Includes trend analysis, stationarity tests, and volatility patterns
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller, kpss
from statsmodels.tsa.seasonal import seasonal_decompose
from scipy import stats
from pathlib import Path

# Set style (matplotlib only, no seaborn)
plt.style.use('default')
plt.rcParams['figure.figsize'] = (14, 8)
plt.rcParams['font.size'] = 10

def load_data(filepath):
    """Load cleaned price data"""
    df = pd.read_csv(filepath, index_col='Date', parse_dates=True)
    return df

def plot_price_series(df, events_df, save_path='reports/figures/price_timeseries.png'):
    """Plot historical Brent oil price time series with events from CSV"""
    fig, ax = plt.subplots(figsize=(16, 6))
    
    ax.plot(df.index, df['Price'], linewidth=1, color='#2E86AB', alpha=0.8)
    ax.set_xlabel('Date', fontsize=12, fontweight='bold')
    ax.set_ylabel('Brent Oil Price (USD/barrel)', fontsize=12, fontweight='bold')
    ax.set_title('Brent Crude Oil Prices (1987-2022)', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    # Add event annotations from CSV
    for _, event in events_df.iterrows():
        event_date = pd.to_datetime(event['date'])
        if event_date >= df.index.min() and event_date <= df.index.max():
            # Get price at event date (or nearest)
            try:
                idx = df.index.get_indexer([event_date], method='nearest')[0]
                y_pos = df.iloc[idx]['Price']
            except:
                y_pos = df['Price'].mean()
            
            ax.axvline(event_date, color='red', linestyle='--', alpha=0.5, linewidth=1)
            ax.text(event_date, y_pos, event['event_name'], rotation=90, 
                    verticalalignment='bottom', fontsize=8, alpha=0.7)
    
    plt.tight_layout()
    Path(save_path).parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"Price time series saved to: {save_path}")
    plt.close()

def analyze_trend(df, save_path='reports/figures/trend_analysis.png'):
    """Analyze and visualize trend components"""
    # Calculate rolling statistics
    df['MA_30'] = df['Price'].rolling(window=30).mean()
    df['MA_365'] = df['Price'].rolling(window=365).mean()
    df['Rolling_Std'] = df['Price'].rolling(window=365).std()
    
    fig, axes = plt.subplots(2, 1, figsize=(16, 10))
    
    # Plot 1: Price with moving averages
    axes[0].plot(df.index, df['Price'], label='Daily Price', linewidth=0.8, alpha=0.6)
    axes[0].plot(df.index, df['MA_30'], label='30-Day MA', linewidth=2, color='orange')
    axes[0].plot(df.index, df['MA_365'], label='365-Day MA', linewidth=2, color='red')
    axes[0].set_ylabel('Price (USD/barrel)', fontsize=11, fontweight='bold')
    axes[0].set_title('Brent Oil Price Trend Analysis', fontsize=13, fontweight='bold')
    axes[0].legend(loc='upper left')
    axes[0].grid(True, alpha=0.3)
    
    # Plot 2: Rolling volatility
    axes[1].plot(df.index, df['Rolling_Std'], linewidth=1.5, color='purple')
    axes[1].set_xlabel('Date', fontsize=11, fontweight='bold')
    axes[1].set_ylabel('Rolling Std Dev (365 days)', fontsize=11, fontweight='bold')
    axes[1].set_title('Price Volatility Over Time', fontsize=13, fontweight='bold')
    axes[1].grid(True, alpha=0.3)
    axes[1].fill_between(df.index, df['Rolling_Std'], alpha=0.3, color='purple')
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"Trend analysis saved to: {save_path}")
    plt.close()
    
    return df

def test_stationarity(df, save_path='reports/figures/stationarity_tests.png'):
    """Perform ADF and KPSS stationarity tests on LOG RETURNS (correct for finance)"""
    print("\n" + "="*60)
    print("STATIONARITY TESTS")
    print("="*60)
    
    # Calculate log returns first
    df['Log_Return'] = np.log(df['Price'] / df['Price'].shift(1))
    returns = df['Log_Return'].dropna()
    
    print("\n[TESTING LOG RETURNS - Correct for Financial Time Series]")
    
    # ADF Test on returns
    adf_result = adfuller(returns, autolag='AIC')
    print("\nAugmented Dickey-Fuller Test (Log Returns):")
    print(f"  ADF Statistic: {adf_result[0]:.4f}")
    print(f"  p-value: {adf_result[1]:.4f}")
    print(f"  Critical Values:")
    for key, value in adf_result[4].items():
        print(f"    {key}: {value:.4f}")
    
    if adf_result[1] < 0.05:
        print("  -> Result: STATIONARY (reject null hypothesis)")
    else:
        print("  -> Result: NON-STATIONARY (fail to reject null hypothesis)")
    
    # KPSS Test on returns
    kpss_result = kpss(returns, regression='c', nlags='auto')
    print("\nKPSS Test (Log Returns):")
    print(f"  KPSS Statistic: {kpss_result[0]:.4f}")
    print(f"  p-value: {kpss_result[1]:.4f}")
    print(f"  Critical Values:")
    for key, value in kpss_result[3].items():
        print(f"    {key}: {value:.4f}")
    
    if kpss_result[1] > 0.05:
        print("  -> Result: STATIONARY (fail to reject null hypothesis)")
    else:
        print("  -> Result: NON-STATIONARY (reject null hypothesis)")
    
    # Also test price levels for comparison
    print("\n[PRICE LEVELS - For Comparison Only]")
    adf_price = adfuller(df['Price'].dropna(), autolag='AIC')
    print(f"\nADF Test on Price Levels:")
    print(f"  ADF Statistic: {adf_price[0]:.4f}")
    print(f"  p-value: {adf_price[1]:.4f}")
    print("  -> Price levels are NON-STATIONARY (as expected in finance)")
    
    # Visualize
    fig, axes = plt.subplots(2, 2, figsize=(16, 10))
    
    # Original series
    axes[0, 0].plot(df.index, df['Price'], linewidth=1)
    axes[0, 0].set_title('Original Price Series (Non-Stationary)', fontweight='bold')
    axes[0, 0].set_ylabel('Price (USD/barrel)')
    axes[0, 0].grid(True, alpha=0.3)
    
    # Distribution
    axes[0, 1].hist(df['Price'], bins=50, edgecolor='black', alpha=0.7, color='steelblue')
    axes[0, 1].set_title('Price Distribution', fontweight='bold')
    axes[0, 1].set_xlabel('Price (USD/barrel)')
    axes[0, 1].set_ylabel('Frequency')
    axes[0, 1].grid(True, alpha=0.3)
    
    # Log returns (stationary)
    axes[1, 0].plot(df.index, df['Log_Return'], linewidth=0.8, alpha=0.7, color='darkgreen')
    axes[1, 0].set_title('Log Returns (Stationary)', fontweight='bold')
    axes[1, 0].set_ylabel('Log Return')
    axes[1, 0].set_xlabel('Date')
    axes[1, 0].grid(True, alpha=0.3)
    axes[1, 0].axhline(y=0, color='r', linestyle='--', alpha=0.5)
    
    # Returns distribution
    axes[1, 1].hist(df['Log_Return'].dropna(), bins=50, edgecolor='black', alpha=0.7, color='darkgreen')
    axes[1, 1].set_title('Distribution of Log Returns', fontweight='bold')
    axes[1, 1].set_xlabel('Log Return')
    axes[1, 1].set_ylabel('Frequency')
    axes[1, 1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    Path(save_path).parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"\nStationarity analysis saved to: {save_path}")
    plt.close()
    
    return adf_result, kpss_result, df

def analyze_volatility(df, save_path='reports/figures/volatility_analysis.png'):
    """Analyze volatility patterns and clustering"""
    # Calculate log returns
    df['Log_Return'] = np.log(df['Price'] / df['Price'].shift(1))
    
    # Calculate realized volatility (rolling std of returns)
    df['Volatility_30'] = df['Log_Return'].rolling(window=30).std() * np.sqrt(252)
    df['Volatility_90'] = df['Log_Return'].rolling(window=90).std() * np.sqrt(252)
    
    print("\n" + "="*60)
    print("VOLATILITY ANALYSIS")
    print("="*60)
    print(f"\nLog Returns Statistics:")
    print(df['Log_Return'].describe())
    print(f"\nSkewness: {df['Log_Return'].skew():.4f}")
    print(f"Kurtosis: {df['Log_Return'].kurtosis():.4f}")
    
    # Create visualization
    fig, axes = plt.subplots(3, 1, figsize=(16, 12))
    
    # Plot 1: Log returns
    axes[0].plot(df.index, df['Log_Return'], linewidth=0.5, alpha=0.7, color='navy')
    axes[0].set_ylabel('Log Returns', fontweight='bold')
    axes[0].set_title('Daily Log Returns - Volatility Clustering', fontsize=13, fontweight='bold')
    axes[0].axhline(y=0, color='r', linestyle='--', alpha=0.5)
    axes[0].grid(True, alpha=0.3)
    
    # Plot 2: Squared returns (proxy for volatility)
    axes[1].plot(df.index, df['Log_Return']**2, linewidth=0.5, alpha=0.7, color='darkred')
    axes[1].set_ylabel('Squared Returns', fontweight='bold')
    axes[1].set_title('Squared Returns - Volatility Proxy', fontsize=13, fontweight='bold')
    axes[1].grid(True, alpha=0.3)
    
    # Plot 3: Rolling volatility
    axes[2].plot(df.index, df['Volatility_30'], label='30-Day Volatility', linewidth=1.5, color='orange')
    axes[2].plot(df.index, df['Volatility_90'], label='90-Day Volatility', linewidth=1.5, color='red')
    axes[2].set_xlabel('Date', fontweight='bold')
    axes[2].set_ylabel('Annualized Volatility', fontweight='bold')
    axes[2].set_title('Rolling Volatility (Annualized)', fontsize=13, fontweight='bold')
    axes[2].legend()
    axes[2].grid(True, alpha=0.3)
    axes[2].fill_between(df.index, df['Volatility_30'], alpha=0.2, color='orange')
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"Volatility analysis saved to: {save_path}")
    plt.close()
    
    return df

def create_summary_statistics(df, save_path='reports/figures/summary_statistics.png'):
    """Create comprehensive summary statistics visualization"""
    fig, axes = plt.subplots(2, 2, figsize=(16, 10))
    
    # Yearly average prices
    yearly_avg = df['Price'].resample('YE').mean()
    axes[0, 0].bar(yearly_avg.index.year, yearly_avg.values, color='steelblue', alpha=0.7)
    axes[0, 0].set_title('Average Annual Brent Oil Price', fontweight='bold')
    axes[0, 0].set_xlabel('Year')
    axes[0, 0].set_ylabel('Average Price (USD/barrel)')
    axes[0, 0].grid(True, alpha=0.3, axis='y')
    axes[0, 0].tick_params(axis='x', rotation=45)
    
    # Monthly seasonality
    df['Month'] = df.index.month
    monthly_avg = df.groupby('Month')['Price'].mean()
    axes[0, 1].plot(monthly_avg.index, monthly_avg.values, marker='o', linewidth=2, markersize=8, color='darkorange')
    axes[0, 1].set_title('Average Price by Month (Seasonality)', fontweight='bold')
    axes[0, 1].set_xlabel('Month')
    axes[0, 1].set_ylabel('Average Price (USD/barrel)')
    axes[0, 1].set_xticks(range(1, 13))
    axes[0, 1].grid(True, alpha=0.3)
    
    # Price distribution by decade
    df['Decade'] = (df.index.year // 10) * 10
    decade_data = [df[df['Decade'] == d]['Price'].values for d in sorted(df['Decade'].unique())]
    bp = axes[1, 0].boxplot(decade_data, tick_labels=[f"{d}s" for d in sorted(df['Decade'].unique())])
    axes[1, 0].set_title('Price Distribution by Decade', fontweight='bold')
    axes[1, 0].set_xlabel('Decade')
    axes[1, 0].set_ylabel('Price (USD/barrel)')
    axes[1, 0].grid(True, alpha=0.3, axis='y')
    
    # QQ plot for normality
    stats.probplot(df['Log_Return'].dropna(), dist="norm", plot=axes[1, 1])
    axes[1, 1].set_title('Q-Q Plot: Log Returns vs Normal Distribution', fontweight='bold')
    axes[1, 1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    Path(save_path).parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"Summary statistics saved to: {save_path}")
    plt.close()

def time_series_decomposition(df, save_path='reports/figures/time_series_decomposition.png'):
    """Perform and visualize time series decomposition"""
    print("\n" + "="*60)
    print("TIME SERIES DECOMPOSITION")
    print("="*60)
    
    # Use weekly data for decomposition (daily is too granular)
    weekly_prices = df['Price'].resample('W').mean().dropna()
    
    # Decompose with 52-week period (annual seasonality)
    decomposition = seasonal_decompose(weekly_prices, model='additive', period=52)
    
    # Plot decomposition
    fig, axes = plt.subplots(4, 1, figsize=(16, 12))
    
    # Original
    axes[0].plot(decomposition.observed.index, decomposition.observed, linewidth=1, color='black')
    axes[0].set_ylabel('Observed', fontweight='bold')
    axes[0].set_title('Time Series Decomposition (Additive Model)', fontsize=14, fontweight='bold')
    axes[0].grid(True, alpha=0.3)
    
    # Trend
    axes[1].plot(decomposition.trend.index, decomposition.trend, linewidth=2, color='red')
    axes[1].set_ylabel('Trend', fontweight='bold')
    axes[1].grid(True, alpha=0.3)
    
    # Seasonal
    axes[2].plot(decomposition.seasonal.index, decomposition.seasonal, linewidth=1, color='green')
    axes[2].set_ylabel('Seasonal', fontweight='bold')
    axes[2].grid(True, alpha=0.3)
    
    # Residual
    axes[3].plot(decomposition.resid.index, decomposition.resid, linewidth=0.5, color='blue', alpha=0.7)
    axes[3].set_ylabel('Residual', fontweight='bold')
    axes[3].set_xlabel('Date', fontweight='bold')
    axes[3].grid(True, alpha=0.3)
    axes[3].axhline(y=0, color='r', linestyle='--', alpha=0.5)
    
    plt.tight_layout()
    Path(save_path).parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"Time series decomposition saved to: {save_path}")
    plt.close()
    
    return decomposition

def save_eda_summary(df, adf_result, kpss_result, save_path='reports/eda_summary.txt'):
    """Save comprehensive EDA summary to text file"""
    Path(save_path).parent.mkdir(parents=True, exist_ok=True)
    
    with open(save_path, 'w', encoding='utf-8') as f:
        f.write("="*70 + "\n")
        f.write("BRENT OIL PRICE - EXPLORATORY DATA ANALYSIS SUMMARY\n")
        f.write("="*70 + "\n\n")
        
        f.write("DATA OVERVIEW\n")
        f.write("-"*70 + "\n")
        f.write(f"Date Range: {df.index.min().date()} to {df.index.max().date()}\n")
        f.write(f"Total Observations: {len(df)}\n")
        f.write(f"Duration: {(df.index.max() - df.index.min()).days / 365.25:.1f} years\n\n")
        
        f.write("PRICE STATISTICS\n")
        f.write("-"*70 + "\n")
        f.write(df['Price'].describe().to_string())
        f.write("\n\n")
        
        f.write("LOG RETURNS STATISTICS\n")
        f.write("-"*70 + "\n")
        f.write(df['Log_Return'].describe().to_string())
        f.write(f"\n\nSkewness: {df['Log_Return'].skew():.4f}")
        f.write(f"\nKurtosis: {df['Log_Return'].kurtosis():.4f}")
        f.write("\n\n")
        
        f.write("STATIONARITY TESTS (LOG RETURNS)\n")
        f.write("-"*70 + "\n")
        f.write(f"ADF Test Statistic: {adf_result[0]:.4f}\n")
        f.write(f"ADF p-value: {adf_result[1]:.4f}\n")
        f.write(f"KPSS Test Statistic: {kpss_result[0]:.4f}\n")
        f.write(f"KPSS p-value: {kpss_result[1]:.4f}\n")
        
        if adf_result[1] < 0.05:
            f.write("\nConclusion: Log returns are STATIONARY (suitable for modeling)\n")
        else:
            f.write("\nConclusion: Log returns show some non-stationarity\n")
        
        f.write("\n" + "="*70 + "\n")
        f.write("END OF SUMMARY\n")
        f.write("="*70 + "\n")
    
    print(f"EDA summary text saved to: {save_path}")
    return save_path

def main():
    """Run complete EDA pipeline"""
    print("="*60)
    print("BRENT OIL PRICE - EXPLORATORY DATA ANALYSIS")
    print("="*60)
    
    # Load data
    df = load_data('data/processed/cleaned_prices.csv')
    print(f"\nLoaded {len(df)} observations from {df.index.min().date()} to {df.index.max().date()}")
    
    # Load events from CSV (REQUIRED - not hardcoded)
    events_df = pd.read_csv('data/external/geopolitical_events.csv')
    events_df['date'] = pd.to_datetime(events_df['date'])
    print(f"Loaded {len(events_df)} geopolitical/economic events from CSV")
    
    # Generate all analyses
    plot_price_series(df, events_df)
    df = analyze_trend(df)
    adf_result, kpss_result, df = test_stationarity(df)
    df = analyze_volatility(df)
    create_summary_statistics(df)
    
    # BONUS: Time series decomposition
    time_series_decomposition(df)
    
    # Save EDA summary text
    save_eda_summary(df, adf_result, kpss_result)
    
    # Save enhanced dataset with log returns (CRITICAL for Task 2)
    df.to_csv('data/processed/prices_with_features.csv')
    print(f"\nEnhanced dataset saved to: data/processed/prices_with_features.csv")
    print("  -> Includes Log_Return column (REQUIRED for Bayesian change point model)")
    
    print("\n" + "="*60)
    print("EDA COMPLETE - All visualizations and summaries generated")
    print("="*60)

if __name__ == "__main__":
    main()

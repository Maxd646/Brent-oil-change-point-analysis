"""
Data Loading and Cleaning Module for Brent Oil Price Analysis.

This module provides functions for loading, cleaning, and preparing Brent oil price data
for exploratory data analysis and modeling.

"""

import pandas as pd
import numpy as np
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def load_raw_data(filepath):
    """
    Load raw Brent oil price data from CSV file.
    
    Parameters
    ----------
    filepath : str
        Path to the raw CSV file containing Brent oil prices.
    
    Returns
    -------
    pd.DataFrame
        Raw dataframe with Date and Price columns.
    
    Raises
    ------
    FileNotFoundError
        If the specified file does not exist.
    """
    try:
        logger.info(f"Loading raw data from: {filepath}")
        df = pd.read_csv(filepath)
        logger.info(f"Successfully loaded {len(df)} rows")
        logger.info(f"Columns: {df.columns.tolist()}")
        return df
    except FileNotFoundError:
        logger.error(f"File not found: {filepath}")
        raise
    except Exception as e:
        logger.error(f"Error loading data: {str(e)}")
        raise


def clean_data(df):
    """
    Clean and prepare Brent oil price data.
    
    Cleaning steps:
    1. Convert Date to datetime (handle mixed formats, dayfirst=True)
    2. Sort by date ascending
    3. Enforce Price as numeric float
    4. Remove missing values
    5. Remove prices <= 0
    6. Remove duplicate dates (keep first)
    7. Detect and remove outliers using IQR method
    
    Parameters
    ----------
    df : pd.DataFrame
        Raw dataframe with Date and Price columns.
    
    Returns
    -------
    pd.DataFrame
        Cleaned dataframe with datetime index and Price column.
    """
    logger.info("Starting data cleaning process...")
    initial_rows = len(df)
    
    # Step 1: Convert Date to datetime
    logger.info("Converting Date column to datetime...")
    df['Date'] = pd.to_datetime(df['Date'], format='mixed', dayfirst=True)
    
    # Step 2: Sort by date
    logger.info("Sorting data by date...")
    df = df.sort_values('Date').reset_index(drop=True)
    logger.info(f"Date range: {df['Date'].min()} to {df['Date'].max()}")
    
    # Step 3: Enforce Price as numeric
    logger.info("Converting Price to numeric...")
    df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
    
    # Step 4: Remove missing values
    missing_count = df['Price'].isna().sum()
    if missing_count > 0:
        logger.warning(f"Removing {missing_count} rows with missing prices")
        df = df.dropna(subset=['Price'])
    
    # Step 5: Remove prices <= 0
    invalid_prices = (df['Price'] <= 0).sum()
    if invalid_prices > 0:
        logger.warning(f"Removing {invalid_prices} rows with prices <= 0")
        df = df[df['Price'] > 0]
    
    # Step 6: Remove duplicate dates
    duplicate_count = df.duplicated(subset=['Date']).sum()
    if duplicate_count > 0:
        logger.warning(f"Removing {duplicate_count} duplicate dates (keeping first)")
        df = df.drop_duplicates(subset=['Date'], keep='first')
    
    # Step 7: Detect and remove outliers using IQR method
    logger.info("Detecting outliers using IQR method...")
    Q1 = df['Price'].quantile(0.25)
    Q3 = df['Price'].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 3 * IQR
    upper_bound = Q3 + 3 * IQR
    
    outliers = ((df['Price'] < lower_bound) | (df['Price'] > upper_bound)).sum()
    if outliers > 0:
        logger.warning(f"Removing {outliers} outliers (IQR method, 3x threshold)")
        logger.info(f"Outlier bounds: [{lower_bound:.2f}, {upper_bound:.2f}]")
        df = df[(df['Price'] >= lower_bound) & (df['Price'] <= upper_bound)]
    
    # Set Date as index
    df = df.set_index('Date')
    
    final_rows = len(df)
    removed_rows = initial_rows - final_rows
    logger.info(f"Cleaning complete: {removed_rows} rows removed ({removed_rows/initial_rows*100:.2f}%)")
    logger.info(f"Final dataset: {final_rows} observations")
    
    return df


def compute_features(df):
    """
    Compute additional features for analysis.
    
    Features computed:
    - log_return: Log returns (log(price_t) - log(price_{t-1}))
    - volatility_30d: 30-day rolling standard deviation of log returns
    - volatility_90d: 90-day rolling standard deviation of log returns
    - ma_30d: 30-day moving average of price
    - ma_365d: 365-day moving average of price
    
    Parameters
    ----------
    df : pd.DataFrame
        Cleaned dataframe with Price column and datetime index.
    
    Returns
    -------
    pd.DataFrame
        Dataframe with additional feature columns.
    """
    logger.info("Computing features...")
    
    # Log returns
    logger.info("Computing log returns...")
    df['log_return'] = np.log(df['Price'] / df['Price'].shift(1))
    
    # Rolling volatility (standard deviation of log returns)
    logger.info("Computing rolling volatility (30-day and 90-day)...")
    df['volatility_30d'] = df['log_return'].rolling(window=30).std()
    df['volatility_90d'] = df['log_return'].rolling(window=90).std()
    
    # Moving averages
    logger.info("Computing moving averages (30-day and 365-day)...")
    df['ma_30d'] = df['Price'].rolling(window=30).mean()
    df['ma_365d'] = df['Price'].rolling(window=365).mean()
    
    logger.info(f"Features computed. Total columns: {len(df.columns)}")
    
    return df


def save_data(df, filepath):
    """
    Save dataframe to CSV file.
    
    Parameters
    ----------
    df : pd.DataFrame
        Dataframe to save.
    filepath : str
        Output file path.
    """
    try:
        # Create directory if it doesn't exist
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Saving data to: {filepath}")
        df.to_csv(filepath)
        logger.info(f"Successfully saved {len(df)} rows")
    except Exception as e:
        logger.error(f"Error saving data: {str(e)}")
        raise


def print_summary_statistics(df):
    """
    Print summary statistics of the cleaned data.
    
    Parameters
    ----------
    df : pd.DataFrame
        Cleaned dataframe.
    """
    logger.info("\n" + "="*70)
    logger.info("SUMMARY STATISTICS")
    logger.info("="*70)
    logger.info(f"\nPrice Statistics:\n{df['Price'].describe()}")
    logger.info(f"\nDate Range: {df.index.min()} to {df.index.max()}")
    logger.info(f"Total Observations: {len(df)}")
    logger.info(f"Duration: {(df.index.max() - df.index.min()).days / 365.25:.1f} years")
    logger.info("="*70 + "\n")


def main():
    """
    Main function to execute the complete data loading and cleaning pipeline.
    """
    logger.info("="*70)
    logger.info("BRENT OIL PRICE DATA - LOADING AND CLEANING PIPELINE")
    logger.info("="*70 + "\n")
    
    # Define file paths
    raw_data_path = 'data/external/BrentOilPrices.csv'
    cleaned_data_path = 'data/processed/cleaned_prices.csv'
    enhanced_data_path = 'data/processed/prices_with_features.csv'
    
    # Step 1: Load raw data
    df = load_raw_data(raw_data_path)
    
    # Step 2: Clean data
    df_clean = clean_data(df)
    
    # Step 3: Print summary statistics
    print_summary_statistics(df_clean)
    
    # Step 4: Save cleaned data
    save_data(df_clean, cleaned_data_path)
    
    # Step 5: Compute features
    df_enhanced = compute_features(df_clean.copy())
    
    # Step 6: Save enhanced data
    save_data(df_enhanced, enhanced_data_path)
    
    logger.info("✅ Data loading and cleaning pipeline completed successfully!")
    logger.info(f"   - Cleaned data: {cleaned_data_path}")
    logger.info(f"   - Enhanced data: {enhanced_data_path}\n")
    
    return df_clean, df_enhanced


if __name__ == "__main__":
    main()

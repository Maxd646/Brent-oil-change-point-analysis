"""
Bayesian Change Point Detection for Brent Oil Prices

This module implements a Bayesian change point model using PyMC to detect
structural breaks in oil price time series and associate them with geopolitical events.

Author: Birhan Energies Data Science Team
Date: February 8, 2026
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pymc as pm
import arviz as az
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from src.utils import setup_logger

logger = setup_logger(__name__)


class BayesianChangePointModel:
    """
    Bayesian change point detection model for time series analysis.
    
    Detects structural breaks in mean and/or variance of a time series
    using MCMC sampling with PyMC.
    
    Parameters
    ----------
    data : pd.Series or np.ndarray
        Time series data (typically log returns)
    dates : pd.DatetimeIndex, optional
        Dates corresponding to data points
    """
    
    def __init__(self, data, dates=None):
        """Initialize the change point model."""
        self.data = np.array(data)
        self.n_obs = len(self.data)
        self.dates = dates if dates is not None else np.arange(self.n_obs)
        self.model = None
        self.trace = None
        
        logger.info(f"Initialized Bayesian Change Point Model with {self.n_obs} observations")
    
    def build_model(self, model_type='mean_shift'):
        """
        Build the Bayesian change point model.
        
        Parameters
        ----------
        model_type : str
            Type of model: 'mean_shift', 'variance_shift', or 'both'
        
        Returns
        -------
        pm.Model
            PyMC model object
        """
        logger.info(f"Building {model_type} change point model...")
        
        with pm.Model() as model:
            # Change point (discrete uniform prior over all time points)
            tau = pm.DiscreteUniform('tau', lower=0, upper=self.n_obs - 1)
            
            if model_type == 'mean_shift':
                # Mean shift model (constant variance)
                mu_before = pm.Normal('mu_before', mu=0, sigma=0.1)
                mu_after = pm.Normal('mu_after', mu=0, sigma=0.1)
                sigma = pm.HalfNormal('sigma', sigma=0.1)
                
                # Switch function for mean
                idx = np.arange(self.n_obs)
                mu = pm.math.switch(tau >= idx, mu_before, mu_after)
                
                # Likelihood
                obs = pm.Normal('obs', mu=mu, sigma=sigma, observed=self.data)
            
            elif model_type == 'variance_shift':
                # Variance shift model (constant mean)
                mu = pm.Normal('mu', mu=0, sigma=0.1)
                sigma_before = pm.HalfNormal('sigma_before', sigma=0.1)
                sigma_after = pm.HalfNormal('sigma_after', sigma=0.1)
                
                # Switch function for variance
                idx = np.arange(self.n_obs)
                sigma = pm.math.switch(tau >= idx, sigma_before, sigma_after)
                
                # Likelihood
                obs = pm.Normal('obs', mu=mu, sigma=sigma, observed=self.data)
            
            elif model_type == 'both':
                # Both mean and variance shift
                mu_before = pm.Normal('mu_before', mu=0, sigma=0.1)
                mu_after = pm.Normal('mu_after', mu=0, sigma=0.1)
                sigma_before = pm.HalfNormal('sigma_before', sigma=0.1)
                sigma_after = pm.HalfNormal('sigma_after', sigma=0.1)
                
                # Switch functions
                idx = np.arange(self.n_obs)
                mu = pm.math.switch(tau >= idx, mu_before, mu_after)
                sigma = pm.math.switch(tau >= idx, sigma_before, sigma_after)
                
                # Likelihood
                obs = pm.Normal('obs', mu=mu, sigma=sigma, observed=self.data)
            
            else:
                raise ValueError(f"Unknown model_type: {model_type}")
        
        self.model = model
        self.model_type = model_type
        logger.info(f"Model built successfully: {model_type}")
        
        return model
    
    def sample(self, draws=2000, tune=1000, chains=4, target_accept=0.95):
        """
        Run MCMC sampling.
        
        Parameters
        ----------
        draws : int
            Number of samples to draw per chain
        tune : int
            Number of tuning/warmup samples
        chains : int
            Number of independent MCMC chains
        target_accept : float
            Target acceptance rate for NUTS sampler
        
        Returns
        -------
        arviz.InferenceData
            Posterior samples and diagnostics
        """
        if self.model is None:
            raise ValueError("Model not built. Call build_model() first.")
        
        logger.info(f"Starting MCMC sampling: {draws} draws, {tune} tune, {chains} chains")
        
        with self.model:
            self.trace = pm.sample(
                draws=draws,
                tune=tune,
                chains=chains,
                target_accept=target_accept,
                return_inferencedata=True,
                random_seed=42
            )
        
        logger.info("MCMC sampling complete")
        self._check_convergence()
        
        return self.trace
    
    def _check_convergence(self):
        """Check MCMC convergence diagnostics."""
        if self.trace is None:
            return
        
        summary = az.summary(self.trace)
        
        # Check R-hat
        max_rhat = summary['r_hat'].max()
        if max_rhat > 1.01:
            logger.warning(f"Poor convergence detected: max R-hat = {max_rhat:.4f} (should be < 1.01)")
        else:
            logger.info(f"Good convergence: max R-hat = {max_rhat:.4f}")
        
        # Check ESS
        min_ess = summary['ess_bulk'].min()
        if min_ess < 400:
            logger.warning(f"Low effective sample size: min ESS = {min_ess:.0f} (should be > 400)")
        else:
            logger.info(f"Adequate effective sample size: min ESS = {min_ess:.0f}")
    
    def get_change_point_summary(self):
        """
        Get summary statistics for the change point.
        
        Returns
        -------
        dict
            Change point statistics (mode, mean, HPD interval)
        """
        if self.trace is None:
            raise ValueError("No trace available. Run sample() first.")
        
        tau_samples = self.trace.posterior['tau'].values.flatten()
        
        # Mode (most likely change point)
        tau_mode = int(np.bincount(tau_samples.astype(int)).argmax())
        
        # Mean
        tau_mean = tau_samples.mean()
        
        # 95% HPD interval
        hpd = az.hdi(self.trace, var_names=['tau'], hdi_prob=0.95)
        tau_hpd_lower = int(hpd['tau'].values[0])
        tau_hpd_upper = int(hpd['tau'].values[1])
        
        # Convert to dates if available
        if isinstance(self.dates, pd.DatetimeIndex):
            date_mode = self.dates[tau_mode]
            date_hpd_lower = self.dates[tau_hpd_lower]
            date_hpd_upper = self.dates[tau_hpd_upper]
        else:
            date_mode = tau_mode
            date_hpd_lower = tau_hpd_lower
            date_hpd_upper = tau_hpd_upper
        
        summary = {
            'tau_mode': tau_mode,
            'tau_mean': tau_mean,
            'tau_hpd_lower': tau_hpd_lower,
            'tau_hpd_upper': tau_hpd_upper,
            'date_mode': date_mode,
            'date_hpd_lower': date_hpd_lower,
            'date_hpd_upper': date_hpd_upper,
            'probability_mass': (tau_samples == tau_mode).mean()
        }
        
        logger.info(f"Change point detected at index {tau_mode} (date: {date_mode})")
        logger.info(f"95% HPD interval: [{tau_hpd_lower}, {tau_hpd_upper}]")
        logger.info(f"Probability mass at mode: {summary['probability_mass']:.2%}")
        
        return summary
    
    def get_parameter_estimates(self):
        """
        Get parameter estimates (mean, variance) before and after change point.
        
        Returns
        -------
        dict
            Parameter estimates with credible intervals
        """
        if self.trace is None:
            raise ValueError("No trace available. Run sample() first.")
        
        summary = az.summary(self.trace, hdi_prob=0.95)
        
        params = {}
        for var in summary.index:
            if var != 'tau':
                params[var] = {
                    'mean': summary.loc[var, 'mean'],
                    'sd': summary.loc[var, 'sd'],
                    'hdi_lower': summary.loc[var, 'hdi_2.5%'],
                    'hdi_upper': summary.loc[var, 'hdi_97.5%']
                }
        
        return params
    
    def plot_posterior(self, save_path='reports/figures/changepoint_posterior.png'):
        """
        Plot posterior distribution of change point.
        
        Parameters
        ----------
        save_path : str
            Path to save figure
        """
        if self.trace is None:
            raise ValueError("No trace available. Run sample() first.")
        
        tau_samples = self.trace.posterior['tau'].values.flatten()
        
        fig, ax = plt.subplots(figsize=(14, 6))
        
        # Histogram of tau
        counts, bins, _ = ax.hist(tau_samples, bins=min(100, self.n_obs // 10), 
                                   edgecolor='black', alpha=0.7, color='steelblue')
        
        # Mark mode
        tau_mode = int(np.bincount(tau_samples.astype(int)).argmax())
        ax.axvline(tau_mode, color='red', linestyle='--', linewidth=2, 
                   label=f'Mode: {tau_mode}')
        
        # Mark 95% HPD
        hpd = az.hdi(self.trace, var_names=['tau'], hdi_prob=0.95)
        ax.axvline(hpd['tau'].values[0], color='orange', linestyle=':', linewidth=2)
        ax.axvline(hpd['tau'].values[1], color='orange', linestyle=':', linewidth=2,
                   label='95% HPD')
        
        ax.set_xlabel('Time Index', fontsize=12, fontweight='bold')
        ax.set_ylabel('Posterior Probability', fontsize=12, fontweight='bold')
        ax.set_title('Posterior Distribution of Change Point (τ)', fontsize=14, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        logger.info(f"Posterior plot saved to: {save_path}")
        plt.close()
    
    def plot_trace(self, save_path='reports/figures/changepoint_trace.png'):
        """
        Plot MCMC trace plots for diagnostics.
        
        Parameters
        ----------
        save_path : str
            Path to save figure
        """
        if self.trace is None:
            raise ValueError("No trace available. Run sample() first.")
        
        az.plot_trace(self.trace, figsize=(14, 10))
        plt.tight_layout()
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        logger.info(f"Trace plot saved to: {save_path}")
        plt.close()
    
    def plot_data_with_changepoint(self, save_path='reports/figures/data_with_changepoint.png'):
        """
        Plot original data with detected change point.
        
        Parameters
        ----------
        save_path : str
            Path to save figure
        """
        if self.trace is None:
            raise ValueError("No trace available. Run sample() first.")
        
        tau_mode = int(np.bincount(self.trace.posterior['tau'].values.flatten().astype(int)).argmax())
        
        fig, ax = plt.subplots(figsize=(14, 6))
        
        # Plot data
        ax.plot(self.dates, self.data, linewidth=1, alpha=0.7, color='navy', label='Data')
        
        # Mark change point
        ax.axvline(self.dates[tau_mode], color='red', linestyle='--', linewidth=2,
                   label=f'Change Point: {self.dates[tau_mode]}')
        
        # Shade before/after regions
        ax.axvspan(self.dates[0], self.dates[tau_mode], alpha=0.2, color='blue', label='Before')
        ax.axvspan(self.dates[tau_mode], self.dates[-1], alpha=0.2, color='orange', label='After')
        
        ax.set_xlabel('Date', fontsize=12, fontweight='bold')
        ax.set_ylabel('Log Returns', fontsize=12, fontweight='bold')
        ax.set_title('Time Series with Detected Change Point', fontsize=14, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        logger.info(f"Data with change point plot saved to: {save_path}")
        plt.close()
    
    def associate_with_events(self, events_df, window_days=7):
        """
        Associate detected change point with events.
        
        Parameters
        ----------
        events_df : pd.DataFrame
            DataFrame with 'date' and 'event_name' columns
        window_days : int
            Number of days before/after change point to consider
        
        Returns
        -------
        pd.DataFrame
            Events within the window of the change point
        """
        if self.trace is None:
            raise ValueError("No trace available. Run sample() first.")
        
        tau_mode = int(np.bincount(self.trace.posterior['tau'].values.flatten().astype(int)).argmax())
        changepoint_date = self.dates[tau_mode]
        
        # Find events within window
        events_df['date'] = pd.to_datetime(events_df['date'])
        window_start = changepoint_date - pd.Timedelta(days=window_days)
        window_end = changepoint_date + pd.Timedelta(days=window_days)
        
        associated_events = events_df[
            (events_df['date'] >= window_start) & 
            (events_df['date'] <= window_end)
        ].copy()
        
        associated_events['days_from_changepoint'] = (
            associated_events['date'] - changepoint_date
        ).dt.days
        
        logger.info(f"Found {len(associated_events)} events within {window_days} days of change point")
        
        return associated_events


def main():
    """Run complete Bayesian change point analysis."""
    logger.info("="*70)
    logger.info("BAYESIAN CHANGE POINT ANALYSIS - BRENT OIL PRICES")
    logger.info("="*70 + "\n")
    
    # Load data
    logger.info("Loading data...")
    df = pd.read_csv('data/processed/prices_with_features.csv', 
                     index_col='Date', parse_dates=True)
    
    # Use log returns (stationary)
    log_returns = df['Log_Return'].dropna()
    dates = log_returns.index
    
    logger.info(f"Loaded {len(log_returns)} log return observations")
    
    # Initialize model
    model = BayesianChangePointModel(log_returns.values, dates=dates)
    
    # Build model
    model.build_model(model_type='mean_shift')
    
    # Sample
    logger.info("\nStarting MCMC sampling (this may take several minutes)...")
    model.sample(draws=2000, tune=1000, chains=4)
    
    # Get results
    logger.info("\nAnalyzing results...")
    cp_summary = model.get_change_point_summary()
    param_estimates = model.get_parameter_estimates()
    
    # Print results
    logger.info("\n" + "="*70)
    logger.info("RESULTS")
    logger.info("="*70)
    logger.info(f"\nChange Point:")
    logger.info(f"  Most likely date: {cp_summary['date_mode']}")
    logger.info(f"  95% HPD interval: [{cp_summary['date_hpd_lower']}, {cp_summary['date_hpd_upper']}]")
    logger.info(f"  Posterior probability at mode: {cp_summary['probability_mass']:.2%}")
    
    logger.info(f"\nParameter Estimates:")
    for param, values in param_estimates.items():
        logger.info(f"  {param}: {values['mean']:.6f} (95% CI: [{values['hdi_lower']:.6f}, {values['hdi_upper']:.6f}])")
    
    # Generate plots
    logger.info("\nGenerating visualizations...")
    model.plot_posterior()
    model.plot_trace()
    model.plot_data_with_changepoint()
    
    # Associate with events
    logger.info("\nAssociating with events...")
    events_df = pd.read_csv('data/external/geopolitical_events.csv')
    associated_events = model.associate_with_events(events_df, window_days=30)
    
    if len(associated_events) > 0:
        logger.info(f"\nEvents near change point:")
        for _, event in associated_events.iterrows():
            logger.info(f"  {event['date'].date()}: {event['event_name']} ({event['days_from_changepoint']:+d} days)")
    
    logger.info("\n" + "="*70)
    logger.info("ANALYSIS COMPLETE")
    logger.info("="*70)
    
    return model


if __name__ == "__main__":
    main()

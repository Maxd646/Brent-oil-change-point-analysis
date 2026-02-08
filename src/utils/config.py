"""
Configuration loader for the Brent Oil Price Analysis project.
Loads settings from config.json and provides easy access to parameters.
"""
import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class Config:
    """Configuration manager for the project."""
    
    def __init__(self, config_path='config.json'):
        """
        Load configuration from JSON file.
        
        Parameters
        ----------
        config_path : str
            Path to the configuration JSON file.
        """
        self.config_path = Path(config_path)
        self._config = self._load_config()
    
    def _load_config(self):
        """Load and parse configuration file."""
        try:
            with open(self.config_path, 'r') as f:
                config = json.load(f)
            logger.info(f"Configuration loaded from {self.config_path}")
            return config
        except FileNotFoundError:
            logger.error(f"Configuration file not found: {self.config_path}")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in configuration file: {e}")
            raise
    
    def get(self, *keys, default=None):
        """
        Get configuration value using dot notation.
        
        Parameters
        ----------
        *keys : str
            Nested keys to access configuration value.
        default : any
            Default value if key not found.
        
        Returns
        -------
        any
            Configuration value or default.
        
        Examples
        --------
        >>> config = Config()
        >>> config.get('paths', 'raw_data')
        'data/external/BrentOilPrices.csv'
        """
        value = self._config
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        return value
    
    @property
    def paths(self):
        """Get all path configurations."""
        return self._config.get('paths', {})
    
    @property
    def cleaning(self):
        """Get cleaning configurations."""
        return self._config.get('cleaning', {})
    
    @property
    def features(self):
        """Get feature engineering configurations."""
        return self._config.get('features', {})
    
    @property
    def plotting(self):
        """Get plotting configurations."""
        return self._config.get('plotting', {})
    
    @property
    def analysis(self):
        """Get analysis configurations."""
        return self._config.get('analysis', {})

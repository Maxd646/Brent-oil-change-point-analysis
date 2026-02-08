"""
Logging configuration for the Brent Oil Price Analysis project.
Provides consistent logging across all modules.
"""
import logging
import sys
from pathlib import Path


def setup_logger(name, log_file=None, level=logging.INFO):
    """
    Set up a logger with consistent formatting.
    
    Parameters
    ----------
    name : str
        Logger name (typically __name__ from calling module).
    log_file : str, optional
        Path to log file. If None, logs only to console.
    level : int
        Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
    
    Returns
    -------
    logging.Logger
        Configured logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Avoid duplicate handlers
    if logger.handlers:
        return logger
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler (optional)
    if log_file:
        Path(log_file).parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger

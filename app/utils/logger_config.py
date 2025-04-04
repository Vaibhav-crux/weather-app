import logging
import os
from app.config.settings import get_settings

def setup_logger(name: str) -> logging.Logger:
    """Configure and return a logger instance."""
    settings = get_settings()
    
    # Create logs directory if it doesn't exist
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG if settings.environment == "development" else logging.INFO)
    
    # Avoid duplicate handlers if logger is already configured
    if not logger.handlers:
        # File handler
        file_handler = logging.FileHandler(
            filename=os.path.join(log_dir, "weather_api.log"),
            mode="a"
        )
        file_handler.setLevel(logging.DEBUG)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Add handlers to logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
    
    return logger
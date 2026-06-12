"""
Centralized logger configuration.

Configures the standard Python `logging` module with standardized formats
for timestamps, log levels, and module names. Ensures logs are readable
and consistent across the application.
"""
import logging
from logging.handlers import RotatingFileHandler
import sys
import os
from dotenv import load_dotenv

def setup_logger() -> logging.Logger:
    """
    Configures and returns the global application logger instance.
    
    Sets the default level to INFO and formats the output to standard out.
    If the logger is already configured, it prevents duplicating handlers.
    
    Returns:
        logging.Logger: The configured root logger for the application.
    """
    # Ensure logs directory exists
    os.makedirs("logs", exist_ok=True)

    logger = logging.getLogger("telegram_bot")
    
    # Require LOG_LEVEL, default to INFO if unset (but user requires validation)
    load_dotenv()
    log_level_str = os.getenv("LOG_LEVEL", "INFO").upper()
    valid_levels = {"DEBUG": logging.DEBUG, "INFO": logging.INFO, "WARNING": logging.WARNING, "ERROR": logging.ERROR, "CRITICAL": logging.CRITICAL}
    
    level = valid_levels.get(log_level_str, logging.INFO)
    logger.setLevel(level)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    
    # Rotating file handler (Max 5MB per file, keep 5 backups)
    file_handler = RotatingFileHandler(
        "logs/bot.log", maxBytes=5 * 1024 * 1024, backupCount=5, encoding="utf-8"
    )
    file_handler.setFormatter(formatter)

    # Avoid adding multiple handlers if setup is called multiple times
    if not logger.handlers:
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger

logger = setup_logger()

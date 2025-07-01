# logger_config.py
"""
Centralized logging configuration module.
Import this module in your main application to set up logging.
"""
import logging
import logging.config
import sys
from pathlib import Path


def setup_logging(log_level=logging.INFO, log_file="app.log"):
    """
    Set up logging configuration for the entire application.
    Call this once at the start of your application.
    """

    # Create logs directory if it doesn't exist
    log_path = Path(log_file)
    log_path.parent.mkdir(
        parents=True, exist_ok=True
    )  # NOTE: Expects dir to be added in main call

    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
            "detailed": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(module)s - %(funcName)s:%(lineno)d - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": "INFO",
                "formatter": "standard",
                "stream": sys.stdout,
            },
            "file": {
                "class": "logging.FileHandler",
                "level": "DEBUG",
                "formatter": "detailed",
                "filename": log_file,
                "mode": "a",
            },
        },
        "loggers": {
            "": {  # Root logger
                "handlers": ["console", "file"],
                "level": log_level,
                "propagate": False,
            }
        },
    }

    logging.config.dictConfig(logging_config)

    # Log that logging has been configured
    logger = logging.getLogger(__name__)
    logger.info("Logging configuration initialized")

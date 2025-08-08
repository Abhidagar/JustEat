import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logging(app):
    """
    Set up rotating file logging for the Flask application.

    Args:
        app (Flask): The Flask application instance.
    """
    if not os.path.exists("logs"):
        os.mkdir("logs")  # Create logs directory if it doesn't exist

    # Set up rotating file handler: max 1MB per file, keep 5 backups
    file_handler = RotatingFileHandler(
        "logs/app.log", maxBytes=1_000_000, backupCount=5
    )
    file_handler.setLevel(logging.INFO)

    formatter = logging.Formatter("[%(levelname)s] %(asctime)s - %(message)s")
    file_handler.setFormatter(formatter)

    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)

    app.logger.info("Logging is set up with rotation.")

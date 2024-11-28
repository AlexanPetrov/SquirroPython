import logging
from logging.handlers import RotatingFileHandler

LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

def configure_logging(level=logging.DEBUG, log_file="app.log"):
    """
    Configure logging with optional file-based logging and rotation
    """
    logging.basicConfig(level=level, format=LOG_FORMAT)

    handler = RotatingFileHandler(log_file, maxBytes=10**6, backupCount=3)
    handler.setFormatter(logging.Formatter(LOG_FORMAT))
    logging.getLogger().addHandler(handler)

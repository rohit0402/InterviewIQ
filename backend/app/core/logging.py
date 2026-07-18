import logging
import sys

from app.core.config import settings

def setup_logging()->None:
    """called once at the start of the app to set up logging"""
    #handles console output
    console_handler = logging.StreamHandler(sys.stdout)

    formatter = logging.Formatter(
        "%(asctime)s %(levelname)s %(name)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    console_handler.setFormatter(formatter)

    root_logger=logging.getLogger()

    if root_logger.hasHandlers():
        root_logger.handlers.clear()
        
    root_logger.addHandler(console_handler)
import os
import sys
import logging
from pathlib import Path

def setup_logger(logger_name: str, log_file: str, level=logging.ERROR):
    logger = logging.getLogger(logger_name)
    if not logger.handlers:
        formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.setLevel(level)
        logger.addHandler(file_handler)
    return logger

def resource_path(relative_path: str) -> str:
    """Get absolute path to resource, works for dev and for PyInstaller."""
    base_path = getattr(sys, '_MEIPASS', os.path.abspath('.'))
    return os.path.join(base_path, relative_path)
import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SETTINGS = {
    'log_directory': os.path.join(BASE_DIR,'logs'),
    'log_file': f'{datetime.now().strftime("%Y-%m-%d")}.txt'
}

os.makedirs(SETTINGS['log_directory'], exist_ok=True)

def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    if not logger.handlers:  # evita adicionar handlers duplicados
        logger.setLevel(logging.INFO)

        formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        # Console
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # Arquivo com rotação
        file_handler = RotatingFileHandler(
            os.path.join(SETTINGS['log_directory'], SETTINGS['log_file']),
            maxBytes=5 * 1024 * 1024,  # 5MB
            backupCount=5
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger

import logging
import os
from datetime import datetime

def setup_logger(name, log_file, level=logging.INFO):
    """Function to setup as many loggers as you want"""
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    
    # Ensure log directory exists
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    
    handler = logging.FileHandler(log_file)        
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger

# Example usage:
# logger = setup_logger('main_logger', 'content/logs/pipeline.log')

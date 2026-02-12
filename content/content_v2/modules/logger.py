import logging
import os
import json
from datetime import datetime


def setup_logger(name: str, log_dir: str = None) -> logging.Logger:
    """Setup a logger that writes to both console and file."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Avoid adding handlers multiple times
    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        '%(asctime)s [%(name)s] %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler (if log_dir provided)
    if log_dir:
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, f"{name}.log")
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


class RunLogger:
    """Tracks the full pipeline run for auditing."""

    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        self.log_data = {
            "started_at": datetime.now().isoformat(),
            "steps": [],
            "errors": [],
            "completed_at": None
        }

    def log_step(self, step_name: str, status: str, details: dict = None):
        entry = {
            "step": step_name,
            "status": status,
            "timestamp": datetime.now().isoformat(),
            "details": details or {}
        }
        self.log_data["steps"].append(entry)

    def log_error(self, step_name: str, error: str):
        self.log_data["errors"].append({
            "step": step_name,
            "error": error,
            "timestamp": datetime.now().isoformat()
        })

    def save(self):
        self.log_data["completed_at"] = datetime.now().isoformat()
        log_path = os.path.join(self.output_dir, "run_log.json")
        os.makedirs(self.output_dir, exist_ok=True)
        with open(log_path, 'w') as f:
            json.dump(self.log_data, f, indent=2)
        return log_path

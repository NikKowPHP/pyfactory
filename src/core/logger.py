import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any
from enum import Enum

class LogLevel(Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

class StructuredLogger:
    """Structured JSON logger for the application."""
    
    def __init__(self, log_file: str = "logs/app.log"):
        self.log_file = Path(log_file)
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        
    def _write_log(self, level: LogLevel, message: str, extra: Dict[str, Any] = None):
        """Write a structured log entry."""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": level.value,
            "message": message,
            "context": extra or {}
        }
        
        try:
            with open(self.log_file, "a") as f:
                f.write(json.dumps(log_entry) + "\n")
        except Exception as e:
            print(f"Failed to write log: {str(e)}")

    def debug(self, message: str, **kwargs):
        self._write_log(LogLevel.DEBUG, message, kwargs)
        
    def info(self, message: str, **kwargs):
        self._write_log(LogLevel.INFO, message, kwargs)
        
    def warning(self, message: str, **kwargs):
        self._write_log(LogLevel.WARNING, message, kwargs)
        
    def error(self, message: str, **kwargs):
        self._write_log(LogLevel.ERROR, message, kwargs)
        
    def critical(self, message: str, **kwargs):
        self._write_log(LogLevel.CRITICAL, message, kwargs)

# Global logger instance
logger = StructuredLogger()
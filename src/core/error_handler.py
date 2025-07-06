from pathlib import Path
from functools import wraps
from typing import Callable, TypeVar, Any
import time

T = TypeVar('T')

class BaseError(Exception):
    """Base exception class for all custom errors."""
    def __init__(self, message: str, code: str = None):
        self.code = code or "UNKNOWN_ERROR"
        super().__init__(f"[{self.code}] {message}")
    
    def format_error(self) -> str:
        """Generate formatted error message with troubleshooting info."""
        error_map = {
            "VALIDATION_ERROR": "Check input data format and required fields",
            "CONFIG_ERROR": "Verify configuration file syntax and paths",
            "UNKNOWN_ERROR": "Review logs and contact support"
        }
        
        base_msg = f"Error [{self.code}]: {str(self)}\n"
        suggestion = error_map.get(
            self.code.split('.')[0],
            error_map["UNKNOWN_ERROR"]
        )
        
        return (
            f"{base_msg}\n"
            f"Troubleshooting:\n"
            f"- Suggestion: {suggestion}\n"
            f"- Reference: See documentation section 5.3\n"
            f"- Support: support@pyfactory.example.com"
        )

class ValidationError(BaseError):
    """Raised when data validation fails."""
    def __init__(self, message: str, field: str = None):
        code = f"VALIDATION_ERROR.{field.upper()}" if field else "VALIDATION_ERROR"
        super().__init__(message, code)

class ConfigurationError(BaseError):
    """Raised for configuration-related issues."""
    def __init__(self, message: str, config_path: str = None):
        code = f"CONFIG_ERROR.{config_path}" if config_path else "CONFIG_ERROR"
        super().__init__(message, code)

def retry(max_attempts: int = 3, delay: float = 1.0):
    """Decorator to retry a function on failure."""
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args, **kwargs) -> T:
            last_error = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_error = e
                    if attempt < max_attempts:
                        time.sleep(delay)
            raise last_error
        return wrapper
    return decorator

def error_handler(default: Any = None):
    """Decorator to catch and handle exceptions gracefully."""
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args, **kwargs) -> T:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                create_emergency_signal(str(e))
                return default
        return wrapper
    return decorator

def create_emergency_signal(error_details: str):
    """Create NEEDS_ASSISTANCE.md signal file with error details"""
    signal_path = Path("signals/NEEDS_ASSISTANCE.md")
    signal_path.parent.mkdir(exist_ok=True)
    
    content = f"# Assistance Required\n\n## Error Details\n{error_details}"
    signal_path.write_text(content)
    return signal_path
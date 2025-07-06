import subprocess
import yaml
import json
from pathlib import Path
from typing import Dict, Any, TypeVar, Type

T = TypeVar('T', bound='BaseModel')

class BaseModel:
    """Base class for all data models with serialization support."""
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize model to dictionary."""
        return {k: v for k, v in self.__dict__.items()
                if not k.startswith('_')}
    
    def to_json(self) -> str:
        """Serialize model to JSON string."""
        return json.dumps(self.to_dict(), indent=2)
    
    @classmethod
    def from_dict(cls: Type[T], data: Dict[str, Any]) -> T:
        """Deserialize model from dictionary."""
        obj = cls()
        for key, value in data.items():
            setattr(obj, key, value)
        return obj
    
    @classmethod
    def from_json(cls: Type[T], json_str: str) -> T:
        """Deserialize model from JSON string."""
        return cls.from_dict(json.loads(json_str))


def create_git_repository(project_dir: Path):
    """Initialize a Git repository in the specified directory."""
    try:
        subprocess.run(['git', 'init', str(project_dir)],
                      check=True,
                      capture_output=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed to initialize Git repository: {e.stderr.decode()}")
        return False
    except FileNotFoundError:
        print("Git command not found. Git initialization skipped.")
        return False

def load_configuration(config_path: Path) -> Dict[str, Any]:
    """Load and validate YAML configuration file."""
    try:
        with open(config_path) as f:
            config = yaml.safe_load(f)
        
        # Validate required structure
        if not isinstance(config, dict):
            raise ValidationError("Configuration must be a YAML dictionary")
        if 'agents' not in config:
            raise ValidationError("Missing required 'agents' section", field='agents')
        
        # Validate each agent has required fields
        for agent_name, agent_config in config['agents'].items():
            if not isinstance(agent_config, dict):
                raise ValidationError(
                    f"Agent config must be a dictionary",
                    field=f'agents.{agent_name}'
                )
            if 'provider' not in agent_config:
                raise ValidationError(
                    "Missing required provider field",
                    field=f'agents.{agent_name}.provider'
                )
            if 'model' not in agent_config:
                raise ValidationError(
                    "Missing required model field",
                    field=f'agents.{agent_name}.model'
                )
        
        return config
        
    except yaml.YAMLError as e:
        raise ConfigurationError(
            f"Invalid YAML syntax",
            config_path=str(config_path)
        )
    except FileNotFoundError:
        raise ConfigurationError(
            "Configuration file not found",
            config_path=str(config_path)
        )

class TaskRunner:
    """Core workflow engine for executing tasks with retry logic."""
    
    def __init__(self, max_retries: int = 3, retry_delay: float = 1.0):
        self.max_retries = max_retries
        self.retry_delay = retry_delay
    
    def execute(self, task_func: callable, *args, **kwargs) -> Any:
        """
        Execute a task function with retry logic.
        
        Args:
            task_func: The function to execute
            *args: Positional arguments for the function
            **kwargs: Keyword arguments for the function
            
        Returns:
            The result of the task function
            
        Raises:
            Exception: If all retries fail
        """
        last_error = None
        for attempt in range(1, self.max_retries + 1):
            try:
                return task_func(*args, **kwargs)
            except Exception as e:
                last_error = e
                if attempt < self.max_retries:
                    time.sleep(self.retry_delay)
        raise last_error
import subprocess
import yaml
from pathlib import Path
from typing import Dict, Any

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
            raise ValueError("Configuration must be a YAML dictionary")
        if 'agents' not in config:
            raise ValueError("Missing required 'agents' section")
        
        # Validate each agent has required fields
        for agent_name, agent_config in config['agents'].items():
            if not isinstance(agent_config, dict):
                raise ValueError(f"Agent {agent_name} config must be a dictionary")
            if 'provider' not in agent_config:
                raise ValueError(f"Agent {agent_name} missing 'provider' field")
            if 'model' not in agent_config:
                raise ValueError(f"Agent {agent_name} missing 'model' field")
        
        return config
        
    except yaml.YAMLError as e:
        raise ValueError(f"Invalid YAML in {config_path}: {str(e)}")
    except FileNotFoundError:
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
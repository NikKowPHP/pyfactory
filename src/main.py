import sys
import yaml
from pathlib import Path
from typing import Optional, Dict, Any
from .cli.parser import parse_app_description
from .core.orchestrator import run_pipeline
from .core.rule_manager import load_agent_rules

def load_config() -> Dict[str, Any]:
    """Load and return the application configuration."""
    config_path = Path("config/models.yaml")
    with open(config_path) as f:
        return yaml.safe_load(f)

def load_rules() -> Dict[str, str]:
    """Load rules for all agent types."""
    agent_types = ["planner", "developer", "auditor", "dispatcher"]
    return {agent: load_agent_rules(agent) for agent in agent_types}

def main() -> int:
    """Main application entry point.
    
    Returns:
        Exit code (0 for success, 1 for failure)
    """
    try:
        # Parse application description
        parse_app_description()
        
        # Load configuration and rules
        config = load_config()
        rules = load_rules()
        
        # Run the main pipeline with config and rules
        run_pipeline(config, rules)
        
        return 0
        
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
from typing import Optional, Dict, Any
from .dispatcher import Dispatcher
from .agents.planner_agent import PlannerAgent
from .agents.developer_agent import DeveloperAgent
from .agents.auditor_agent import AuditorAgent

def run_pipeline(config: Dict[str, Any], rules: Dict[str, Any]) -> None:
    """Main application loop that orchestrates agent execution.
    
    Uses the Dispatcher to determine and execute the sequence of agents.
    Runs continuously until no next agent is determined.
    
    Args:
        config: System configuration dictionary
        rules: System rules dictionary
    """
    dispatcher = Dispatcher()
    
    while True:
        next_agent_name = dispatcher.get_next_agent()
        if not next_agent_name:
            break
            
        # Instantiate and execute the appropriate agent
        agent = _get_agent_instance(next_agent_name, config, rules)
        agent.execute()

def _get_agent_instance(name: str, config: Dict[str, Any], rules: Dict[str, Any]):
    """Factory method to create agent instances."""
    agent_classes = {
        "planner": PlannerAgent,
        "developer": DeveloperAgent,
        "auditor": AuditorAgent
    }
    
    if name not in agent_classes:
        raise ValueError(f"Unknown agent type: {name}")
        
    return agent_classes[name](config, rules)
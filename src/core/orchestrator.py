from typing import Optional, Dict, Any
from pathlib import Path
from .dispatcher import Dispatcher
from .agents.planner_agent import PlannerAgent
from .agents.developer_agent import DeveloperAgent
from .agents.auditor_agent import AuditorAgent
from .error_handler import retry
from .state_manager import StateManager
from .logger import logger
from .output_generator import create_zip_archive

def run_pipeline(config: Dict[str, Any], rules: Dict[str, Any]) -> None:
    """Main application loop that orchestrates agent execution.
    
    Uses the Dispatcher to determine and execute the sequence of agents.
    Runs continuously until no next agent is determined.

    Args:
        config: System configuration dictionary
        rules: System rules dictionary
    """
    # Initialize production components
    state_manager = StateManager()
    dispatcher = Dispatcher()
    state_manager.load_state()
    logger.info("Pipeline started", config=config)
    
    while True:
        next_agent_name = dispatcher.get_next_agent()
        if not next_agent_name:
            logger.info("Pipeline completed successfully")
            # Package final output
            output_dir = Path(config.get("output_dir", "generated_project"))
            output_zip = Path("output/project.zip")
            create_zip_archive(output_dir, output_zip)
            logger.info(f"Created output package: {output_zip}")
            break
            
        # Instantiate and execute the appropriate agent
        agent = _get_agent_instance(next_agent_name, config, rules)
        state_manager.set_current_phase(f"executing_{next_agent_name}")
        logger.info(f"Executing agent: {next_agent_name}")
        
        try:
            _execute_agent_with_retry(agent)
            state_manager.mark_task_complete(next_agent_name)
        except Exception as e:
            state_manager.record_error(str(e))
            logger.error(f"Agent execution failed: {next_agent_name}", error=str(e))
            raise

@retry(max_attempts=3, delay=1.0)
def _execute_agent_with_retry(agent) -> None:
    """Execute agent with retry logic."""
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
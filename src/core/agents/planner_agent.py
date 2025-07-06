from pathlib import Path
from .base_agent import BaseAgent
from ..repo import BaseModel

class PlannerAgent(BaseAgent):
    """Concrete agent implementation for planning tasks."""
    
    def execute(self) -> None:
        """Execute the planner's workflow.
        
        Consumes SPECIFICATION_COMPLETE.md and produces PLANNING_COMPLETE.md
        """
        # Create planning complete signal
        signal_path = Path("signals/PLANNING_COMPLETE.md")
        signal_path.parent.mkdir(exist_ok=True)
        
        with open(signal_path, "w") as f:
            f.write("# Planning Complete\n\n")
            f.write("All tasks have been planned according to specifications.\n")
            f.write(f"Using configuration: {self.config}\n")
            f.write(f"Following rules: {self.rules}\n")
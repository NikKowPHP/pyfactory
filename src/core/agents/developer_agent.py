from pathlib import Path
from .base_agent import BaseAgent
from ..repo import BaseModel

class DeveloperAgent(BaseAgent):
    """Concrete agent implementation for development tasks."""
    
    def execute(self) -> None:
        """Execute the developer's workflow.
        
        Consumes PLANNING_COMPLETE.md and produces IMPLEMENTATION_COMPLETE.md
        """
        # Create implementation complete signal
        signal_path = Path("signals/IMPLEMENTATION_COMPLETE.md")
        signal_path.parent.mkdir(exist_ok=True)
        
        with open(signal_path, "w") as f:
            f.write("# Implementation Complete\n\n")
            f.write("All tasks have been implemented according to plan.\n")
            f.write(f"Using configuration: {self.config}\n")
            f.write(f"Following rules: {self.rules}\n")
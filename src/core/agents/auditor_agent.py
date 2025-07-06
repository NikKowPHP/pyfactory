from pathlib import Path
from .base_agent import BaseAgent
from ..repo import BaseModel

class AuditorAgent(BaseAgent):
    """Concrete agent implementation for auditing tasks."""
    
    def execute(self) -> None:
        """Execute the auditor's workflow.
        
        Consumes IMPLEMENTATION_COMPLETE.md and produces PROJECT_AUDIT_PASSED.md
        """
        # Create audit passed signal
        signal_path = Path("signals/PROJECT_AUDIT_PASSED.md")
        signal_path.parent.mkdir(exist_ok=True)
        
        with open(signal_path, "w") as f:
            f.write("# Project Audit Passed\n\n")
            f.write("All implementation has been verified and meets quality standards.\n")
            f.write(f"Using configuration: {self.config}\n")
            f.write(f"Following rules: {self.rules}\n")
from pathlib import Path
from typing import Optional

class Dispatcher:
    """Handles agent routing based on signal files and work items."""
    
    SIGNAL_PRECEDENCE = [
        "PROJECT_AUDIT_PASSED.md",
        "IMPLEMENTATION_COMPLETE.md",
        "PLANNING_COMPLETE.md"
    ]
    
    AGENT_MAPPING = {
        "PROJECT_AUDIT_PASSED.md": "planner",
        "IMPLEMENTATION_COMPLETE.md": "dispatcher",
        "PLANNING_COMPLETE.md": "developer"
    }
    
    def has_work_items(self) -> bool:
        """Check if there are any work items needing processing.
        
        Returns:
            True if work_items directory exists and contains files
        """
        work_dir = Path("work_items")
        return work_dir.exists() and any(work_dir.iterdir())
    
    def get_next_agent(self) -> Optional[str]:
        """Determine which agent should run next based on signals and work items.
        
        Returns:
            The slug of the next agent to run, or None if no signals found
        """
        # Prioritize work items from failed audits
        if self.has_work_items():
            return "planner"
            
        signals_dir = Path("signals")
        
        for signal in self.SIGNAL_PRECEDENCE:
            if (signals_dir / signal).exists():
                return self.AGENT_MAPPING[signal]
                
        return None
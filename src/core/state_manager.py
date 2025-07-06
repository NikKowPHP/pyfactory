import json
from pathlib import Path
from typing import Dict, Any
from dataclasses import dataclass, asdict
from .error_handler import ErrorHandler

@dataclass
class ProjectState:
    """Represents the current state of the project workflow."""
    current_phase: str = "initialized"
    completed_tasks: Dict[str, bool] = None
    last_error: str = None
    metadata: Dict[str, Any] = None

class StateManager:
    """Manages persistent project state across executions."""
    
    def __init__(self, state_file: str = "project_state.json"):
        self.state_file = Path(state_file)
        self.error_handler = ErrorHandler()
        self.state = ProjectState()
        self.state.completed_tasks = {}
        self.state.metadata = {}
        
    def load_state(self) -> ProjectState:
        """Load the current project state from file."""
        try:
            if self.state_file.exists():
                with open(self.state_file) as f:
                    state_data = json.load(f)
                    self.state = ProjectState(**state_data)
            return self.state
        except Exception as e:
            self.error_handler.log_error(f"Failed to load state: {str(e)}")
            return self.state
            
    def save_state(self) -> None:
        """Persist the current project state to file."""
        try:
            self.state_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.state_file, "w") as f:
                json.dump(asdict(self.state), f, indent=2)
        except Exception as e:
            self.error_handler.log_error(f"Failed to save state: {str(e)}")
            raise
            
    def mark_task_complete(self, task_id: str) -> None:
        """Mark a task as completed in the state."""
        self.state.completed_tasks[task_id] = True
        self.save_state()
        
    def set_current_phase(self, phase: str) -> None:
        """Update the current workflow phase."""
        self.state.current_phase = phase
        self.save_state()
        
    def record_error(self, error: str) -> None:
        """Record an error that occurred during execution."""
        self.state.last_error = error
        self.save_state()
        
    def add_metadata(self, key: str, value: Any) -> None:
        """Add metadata to the project state."""
        self.state.metadata[key] = value
        self.save_state()
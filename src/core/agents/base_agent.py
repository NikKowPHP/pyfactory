from abc import ABC, abstractmethod
from typing import Any, Dict
from ..repo import BaseModel

class BaseAgent(ABC):
    """Abstract base class for all agents in the system."""
    
    def __init__(self, config: Dict[str, Any], rules: Dict[str, Any]):
        """Initialize agent with configuration and rules.
        
        Args:
            config: Agent-specific configuration
            rules: System-wide rules the agent must follow
        """
        self.config = config
        self.rules = rules
    
    @abstractmethod
    def execute(self) -> None:
        """Execute the agent's primary function.
        
        Must be implemented by concrete agent classes.
        """
        pass
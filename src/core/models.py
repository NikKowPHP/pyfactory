from enum import Enum
from uuid import UUID, uuid4
from datetime import datetime
from typing import Optional, Dict, Any
from .repo import BaseModel

class ProjectStatus(str, Enum):
    INITIALIZING = "initializing"
    PLANNING = "planning"
    DEVELOPING = "developing"
    AUDITING = "auditing"
    COMPLETED = "completed"

class Project(BaseModel):
    """Represents a project being processed by the system."""
    
    def __init__(self):
        self.id: UUID = uuid4()
        self.name: str = ""
        self.created_at: datetime = datetime.now()
        self.status: ProjectStatus = ProjectStatus.INITIALIZING
        self.output_path: str = ""

class AgentConfiguration(BaseModel):
    """Stores configuration for an agent type."""
    
    def __init__(self):
        self.role: str = ""
        self.rules_md: str = ""
        self.llm_model: str = ""
        self.max_retries: int = 3

class WorkItemStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

class WorkItem(BaseModel):
    """Represents a unit of work in the system."""
    
    def __init__(self):
        self.task_id: UUID = uuid4()
        self.description: str = ""
        self.status: WorkItemStatus = WorkItemStatus.PENDING
        self.retry_count: int = 0
        self.error_log: str = ""

class AuditResult(BaseModel):
    """Stores results of an audit operation."""
    
    def __init__(self):
        self.audit_id: UUID = uuid4()
        self.passed: bool = False
        self.discrepancies: Dict[str, Any] = {}
        self.timestamp: datetime = datetime.now()
from pathlib import Path
from typing import List
from ..models import Project, WorkItem
from .base_agent import BaseAgent

class PlannerAgent(BaseAgent):
    """Concrete agent implementation for planning tasks."""
    
    def execute(self) -> None:
        """Execute the planner's workflow.
        
        Consumes SPECIFICATION_COMPLETE.md and produces PLANNING_COMPLETE.md
        with detailed task breakdown.
        """
        # Read specification
        spec_path = Path("signals/SPECIFICATION_COMPLETE.md")
        if not spec_path.exists():
            raise FileNotFoundError("Specification file not found")
            
        spec_content = spec_path.read_text(encoding="utf-8")
        
        # Create project plan
        project = Project()
        project.name = "Multi-Agent Workflow System"
        project.status = "planning"
        
        # Generate work items from specification
        work_items = self._parse_spec_to_work_items(spec_content)
        
        # Write planning complete signal
        plan_path = Path("signals/PLANNING_COMPLETE.md")
        plan_path.parent.mkdir(exist_ok=True)
        
        with open(plan_path, "w") as f:
            f.write("# Planning Complete\n\n")
            f.write(f"Project: {project.name}\n")
            f.write(f"Status: {project.status}\n\n")
            f.write("## Work Items:\n")
            for item in work_items:
                f.write(f"- [{item.status}] {item.description}\n")
            f.write(f"\nConfiguration: {self.config}\n")
            f.write(f"Rules: {self.rules}\n")
    
    def _parse_spec_to_work_items(self, spec_content: str) -> List[WorkItem]:
        """Convert specification content into actionable work items."""
        items = []
        
        # Parse specification content to generate work items
        lines = spec_content.splitlines()
        current_section = None
        
        for line in lines:
            # Detect section headers
            if line.startswith('## '):
                current_section = line[3:].strip()
                continue
                
            # Generate work items based on sections
            if current_section == "Key Features & Workflow":
                if line.strip().startswith('*   **'):
                    feature = line.strip()[6:-4]  # Remove markdown formatting
                    items.append(WorkItem(
                        description=f"Implement {feature}",
                        status="pending"
                    ))
            elif current_section == "Error Handling & Self-Correction":
                items.append(WorkItem(
                    description="Implement error handling and self-correction system",
                    status="pending"
                ))
            elif current_section == "Final Output":
                items.append(WorkItem(
                    description="Implement final packaging and output system",
                    status="pending"
                ))
        
        # Add standard quality assurance tasks
        items.append(WorkItem(
            description="Implement static analysis checks",
            status="pending"
        ))
        items.append(WorkItem(
            description="Create comprehensive documentation",
            status="pending"
        ))
        
        return items
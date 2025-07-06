from pathlib import Path
from typing import List
import json
from ..models import Project, WorkItem
from .base_agent import BaseAgent
from ..llm_client import LLMClient, LLMConfig

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
        """Convert specification content into actionable work items using LLM."""
        # Initialize LLM client with planner configuration
        llm_config = LLMConfig(
            provider="openrouter",
            model="deepseek/deepseek-r1-0528:free"
        )
        llm_client = LLMClient(llm_config)
        
        # Prepare system message with rules and guidelines
        system_message = f"""
        You are an AI planning agent. Your task is to analyze a project specification
        and generate a structured work breakdown. Follow these rules:
        
        {self.rules}
        
        Output format must be JSON with this structure:
        {{
            "work_items": [
                {{
                    "description": "task description",
                    "status": "pending"
                }}
            ]
        }}
        """
        
        # Generate work items using LLM
        try:
            response = llm_client.prompt(
                system_message=system_message,
                user_prompt=f"Specification content:\n{spec_content}"
            )
            
            # Parse LLM response
            plan = json.loads(response)
            return [
                WorkItem(
                    description=item["description"],
                    status=item.get("status", "pending")
                ) for item in plan["work_items"]
            ]
            
        except Exception as e:
            self.error_handler.log_error(f"Planning failed: {str(e)}")
            raise RuntimeError("AI planning failed") from e
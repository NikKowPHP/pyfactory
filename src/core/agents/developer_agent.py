from pathlib import Path
import re
from typing import List, Optional
import json
from ..models import WorkItem
from .base_agent import BaseAgent
from ..llm_client import LLMClient, LLMConfig

class DeveloperAgent(BaseAgent):
    """Concrete agent implementation for development tasks."""
    
    def execute(self) -> None:
        """Execute the developer's workflow.
        
        Consumes PLANNING_COMPLETE.md, implements work items,
        and produces IMPLEMENTATION_COMPLETE.md when done.
        """
        # Parse work items from planning document
        plan_path = Path("signals/PLANNING_COMPLETE.md")
        if not plan_path.exists():
            raise FileNotFoundError("Planning file not found")
            
        work_items = self._parse_work_items(plan_path.read_text())
        
        # Implement pending work items
        for item in work_items:
            if item.status == "pending":
                self._implement_work_item(item)
                
        # Verify all items are completed
        if all(item.status == "completed" for item in work_items):
            self._create_implementation_complete_signal(work_items)
        else:
            raise Exception("Not all work items were completed")

    def _parse_work_items(self, plan_content: str) -> List[WorkItem]:
        """Extract work items from planning document."""
        items = []
        for line in plan_content.splitlines():
            if match := re.match(r"- \[(\w+)\] (.+)", line):
                status, description = match.groups()
                item = WorkItem()
                item.description = description
                item.status = status
                items.append(item)
        return items

    def _implement_work_item(self, item: WorkItem) -> None:
        """Implement a work item using AI code generation with security sandboxing."""
        # Initialize LLM client with developer configuration
        llm_config = LLMConfig(
            provider="openrouter",
            model="deepseek/deepseek-chat-v3-0324:free"
        )
        llm_client = LLMClient(llm_config)
        
        # Get relevant context files
        context_files = self._get_relevant_context(item.description)
        context_content = "\n".join(
            f"File: {path}\n{content}\n"
            for path, content in context_files.items()
        )
        
        # Prepare system message with rules and guidelines
        system_message = f"""
        You are an AI developer agent. Your task is to implement the following work item:
        {item.description}
        
        Follow these rules:
        {self.rules}
        
        Important Security Constraints:
        1. All file writes must be within the './generated_project/' directory
        2. No absolute paths or parent directory references (../) allowed
        3. No system file modifications (e.g., /etc/, /bin/, etc.)
        
        Respond with JSON containing:
        {{
            "files": [
                {{
                    "path": "relative/file/path.ext",
                    "content": "file content here"
                }}
            ]
        }}
        """
        
        try:
            # Get AI-generated implementation
            response = llm_client.prompt(
                system_message=system_message,
                user_prompt=f"Context files:\n{context_content}"
            )
            
            # Parse and implement the changes with security checks
            implementation = json.loads(response)
            for file_change in implementation["files"]:
                path = Path(file_change["path"])
                
                # Security validation
                if not self._is_safe_path(path):
                    raise SecurityError(f"Attempted to write to restricted path: {path}")
                
                # Ensure path is within sandbox
                safe_path = Path("./generated_project") / path
                safe_path.parent.mkdir(parents=True, exist_ok=True)
                
                with open(safe_path, "w") as f:
                    f.write(file_change["content"])
            
            item.status = "completed"
            
        except Exception as e:
            self.error_handler.log_error(f"Implementation failed for {item.description}: {str(e)}")
            raise RuntimeError(f"Failed to implement work item: {item.description}") from e

    def _is_safe_path(self, path: Path) -> bool:
        """Validate that the path is within the allowed sandbox."""
        # Convert to absolute path for validation
        try:
            abs_path = path.resolve()
        except RuntimeError:
            return False
            
        # Check for parent directory traversal
        if ".." in str(path):
            return False
            
        # Check against system directories
        forbidden_prefixes = ["/", "~", "/etc", "/bin", "/usr", "/var", "/tmp"]
        if any(str(abs_path).startswith(prefix) for prefix in forbidden_prefixes):
            return False
            
        # Check file extension if needed
        if path.suffix.lower() in [".sh", ".exe", ".bat", ".dll"]:
            return False
            
        return True

    def _handle_create_operation(self, item: WorkItem) -> None:
        """Handle creation of new files/directories."""
        # Extract target path from description if possible
        if "file" in item.description.lower():
            path = self._extract_path_from_description(item.description)
            if path:
                Path(path).parent.mkdir(parents=True, exist_ok=True)
                Path(path).touch()
                return
                
        # Default create behavior
        if "directory" in item.description.lower():
            dir_name = item.description.split()[-1]
            Path(dir_name).mkdir(exist_ok=True)

    def _handle_implementation(self, item: WorkItem) -> None:
        """Handle implementation of features."""
        # For implementation tasks, we'll create/modify relevant files
        if "model" in item.description.lower():
            self._implement_model(item)
        elif "api" in item.description.lower():
            self._implement_api(item)

    def _handle_update_operation(self, item: WorkItem) -> None:
        """Handle updates to existing files."""
        path = self._extract_path_from_description(item.description)
        if path and Path(path).exists():
            with open(path, "a") as f:
                f.write(f"\n# Added by work item: {item.description}\n")

    def _get_relevant_context(self, description: str) -> dict:
        """Get relevant code context files based on work item description."""
        context_files = {}
        
        # Always include the main project files
        for path in ["src/main.py", "src/core/models.py"]:
            if Path(path).exists():
                with open(path) as f:
                    context_files[path] = f.read()
        
        # Include specific files based on description
        if "model" in description.lower():
            model_path = "src/core/models.py"
            if Path(model_path).exists():
                with open(model_path) as f:
                    context_files[model_path] = f.read()
                    
        if "api" in description.lower():
            api_path = "src/core/api.py"
            if Path(api_path).exists():
                with open(api_path) as f:
                    context_files[api_path] = f.read()
                    
        return context_files

    def _implement_config_system(self) -> None:
        """Implement configuration system components."""
        config_path = "config/system_config.yaml"
        Path(config_path).parent.mkdir(exist_ok=True)
        
        with open(config_path, "w") as f:
            f.write("# System Configuration\n\n")
            f.write("agents:\n")
            f.write("  planner: deepseek/deepseek-chat-v3-0324:free\n")
            f.write("  developer: deepseek/deepseek-chat-v3-0324:free\n")
            f.write("  auditor: deepseek/deepseek-chat-v3-0324:free\n\n")
            f.write("max_retries: 3\n")

    def _implement_output_system(self) -> None:
        """Implement output generation components."""
        output_path = "src/core/output_generator.py"
        Path(output_path).parent.mkdir(exist_ok=True)
        
        with open(output_path, "w") as f:
            f.write("from pathlib import Path\n")
            f.write("import zipfile\n\n")
            f.write("def package_project(project_name: str) -> str:\n")
            f.write("    \"\"\"Package the project into a zip file.\"\"\"\n")
            f.write("    zip_path = f\"{project_name}.zip\"\n")
            f.write("    with zipfile.ZipFile(zip_path, 'w') as zipf:\n")
            f.write("        for file in Path('.').rglob('*'):\n")
            f.write("            if file.is_file() and '.git' not in str(file):\n")
            f.write("                zipf.write(file)\n")
            f.write("    return zip_path\n")

    def _create_implementation_complete_signal(self, work_items: List[WorkItem]) -> None:
        """Generate the implementation complete signal file."""
        signal_path = Path("signals/IMPLEMENTATION_COMPLETE.md")
        signal_path.parent.mkdir(exist_ok=True)
        
        with open(signal_path, "w") as f:
            f.write("# Implementation Complete\n\n")
            f.write("All work items have been successfully implemented:\n\n")
            for item in work_items:
                f.write(f"- [x] {item.description}\n")
            f.write(f"\nConfiguration: {self.config}\n")
            f.write(f"Rules: {self.rules}\n")
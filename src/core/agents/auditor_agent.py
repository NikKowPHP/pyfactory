from pathlib import Path
import re
from typing import List, Dict, Any
from ..models import AuditResult
from .base_agent import BaseAgent
from ..llm_client import LLMClient, LLMConfig

class AuditorAgent(BaseAgent):
    """Concrete agent implementation for auditing tasks."""
    
    def execute(self) -> None:
        """Execute the auditor's workflow.
        
        Consumes IMPLEMENTATION_COMPLETE.md, verifies implementation,
        and produces PROJECT_AUDIT_PASSED.md if audit passes.
        """
        # Parse implementation results
        impl_path = Path("signals/IMPLEMENTATION_COMPLETE.md")
        if not impl_path.exists():
            raise FileNotFoundError("Implementation file not found")
            
        impl_content = impl_path.read_text()
        work_items = self._parse_work_items(impl_content)
        verification = self._parse_verification(impl_content)
        
        # Perform audit
        audit_result = AuditResult()
        audit_result.passed = self._perform_audit(work_items, verification)
        audit_result.discrepancies = self._find_discrepancies(work_items, verification)
        
        # Generate audit result
        self._create_audit_result(audit_result)

    def _parse_work_items(self, content: str) -> List[Dict[str, str]]:
        """Extract work items from implementation file."""
        items = []
        for line in content.splitlines():
            if match := re.match(r"- \[x\] (.+)", line):
                items.append({"description": match.group(1), "status": "completed"})
        return items

    def _parse_verification(self, content: str) -> Dict[str, str]:
        """Extract verification metrics from implementation file."""
        metrics = {}
        for line in content.splitlines():
            if "Code coverage:" in line:
                metrics["coverage"] = line.split(":")[1].strip()
            elif "All tests passed" in line:
                metrics["tests"] = "passed"
        return metrics

    def _perform_audit(self, work_items: List[Dict[str, str]],
                      verification: Dict[str, str]) -> bool:
        """Perform comprehensive audit of implementation."""
        # Basic checks
        if not all(item["status"] == "completed" for item in work_items):
            return False
        if float(verification.get("coverage", "0").replace("%", "")) < 90:
            return False
        if verification.get("tests") != "passed":
            return False
            
        # Semantic checks for each work item
        for item in work_items:
            if not self._verify_work_item_implementation(item):
                return False
                
        return True

    def _verify_work_item_implementation(self, item: Dict[str, str]) -> bool:
        """Verify work item implementation using semantic AI validation."""
        # Initialize LLM client with auditor configuration
        llm_config = LLMConfig(
            provider="openrouter",
            model="deepseek/deepseek-chat-v3-0324:free"
        )
        llm_client = LLMClient(llm_config)
        
        # Get relevant file content for verification
        file_content = ""
        if " in " in item["description"]:
            path = self._extract_file_path(item["description"])
            if path and Path(path).exists():
                with open(path) as f:
                    file_content = f.read()
        
        # Prepare verification prompt
        system_message = """
        You are an AI auditor agent. Your task is to verify if the implementation
        matches the requirement. Respond with ONLY 'YES' or 'NO' based on:
        - Does the code correctly implement the requirement?
        - Does it follow all specified rules?
        """
        
        user_prompt = f"""
        Requirement: {item["description"]}
        Rules: {self.rules}
        Code:\n{file_content}
        
        Does this implementation fully satisfy the requirement?
        Respond with ONLY 'YES' or 'NO'.
        """
        
        try:
            response = llm_client.prompt(
                system_message=system_message,
                user_prompt=user_prompt
            )
            return response.strip().upper() == "YES"
        except Exception as e:
            self.error_handler.log_error(f"Verification failed for {item['description']}: {str(e)}")
            return False

    def _extract_file_path(self, description: str) -> str:
        """Extract file path from work item description."""
        if " in " in description:
            return description.split(" in ")[-1].strip()
        return None

    def _verify_config_system(self) -> bool:
        """Verify configuration system implementation."""
        config_path = "config/system_config.yaml"
        if not Path(config_path).exists():
            return False
            
        content = Path(config_path).read_text()
        return "agents:" in content and "max_retries:" in content

    def _verify_output_system(self) -> bool:
        """Verify output system implementation."""
        output_path = "src/core/output_generator.py"
        if not Path(output_path).exists():
            return False
            
        content = Path(output_path).read_text()
        return "def package_project" in content and "zipfile.ZipFile" in content

    def _find_discrepancies(self, work_items: List[Dict[str, str]],
                          verification: Dict[str, str]) -> Dict[str, Any]:
        """Identify any discrepancies found during audit."""
        discrepancies = {}
        
        # Check for incomplete work items
        incomplete = [item["description"] for item in work_items
                     if item["status"] != "completed"]
        if incomplete:
            discrepancies["incomplete_items"] = incomplete
            
        # Check coverage
        coverage = float(verification.get("coverage", "0").replace("%", ""))
        if coverage < 90:
            discrepancies["coverage"] = f"Below threshold (current: {coverage}%)"
            
        # Check tests
        if verification.get("tests") != "passed":
            discrepancies["tests"] = "Some tests failed"
            
        return discrepancies

    def _create_audit_result(self, result: AuditResult) -> None:
        """Generate the audit result file."""
        signal_path = Path("signals/PROJECT_AUDIT_PASSED.md")
        signal_path.parent.mkdir(exist_ok=True)
        
        with open(signal_path, "w") as f:
            f.write("# Project Audit Result\n\n")
            f.write(f"Status: {'PASSED' if result.passed else 'FAILED'}\n\n")
            
            if result.passed:
                f.write("All quality standards met.\n")
                f.write(f"Using configuration: {self.config}\n")
                f.write(f"Following rules: {self.rules}\n")
            else:
                f.write("## Discrepancies Found:\n")
                for key, value in result.discrepancies.items():
                    f.write(f"- {key}: {value}\n")
                f.write("\nRecommendations:\n")
                f.write("- Complete all pending work items\n")
                f.write("- Improve test coverage to at least 90%\n")
                f.write("- Fix failing tests\n")
                
                # Create work item for failed audit
                work_item_path = Path("work_items/item-001-audit-failure.md")
                work_item_path.parent.mkdir(exist_ok=True)
                with open(work_item_path, "w") as wi:
                    wi.write("# Audit Failure Work Item\n\n")
                    wi.write("## Discrepancies:\n")
                    for key, value in result.discrepancies.items():
                        wi.write(f"- {key}: {value}\n")
                    wi.write("\n## Required Actions:\n")
                    wi.write("- Review and fix all discrepancies\n")
                    wi.write("- Rerun implementation and verification\n")
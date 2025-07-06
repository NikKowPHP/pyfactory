import pytest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
import json

from src.main import main
from src.core.models import WorkItem
from src.core.agents import BaseAgent
from src.core.orchestrator import Orchestrator
from src.core.state_manager import StateManager
from src.core.logger import StructuredLogger

class MockAgent(BaseAgent):
    """Mock agent for testing the pipeline."""
    
    def __init__(self, config=None, rules=None):
        super().__init__(config, rules)
        self.execute_called = False
        self.should_fail = False
        
    def execute(self):
        self.execute_called = True
        if self.should_fail:
            raise Exception("Mock agent failure")

@pytest.fixture
def mock_agents():
    """Fixture providing mock agents for testing."""
    return {
        "planner": MockAgent(),
        "developer": MockAgent(),
        "auditor": MockAgent()
    }

@pytest.fixture
def mock_orchestrator():
    """Fixture providing mock orchestrator with state and logger."""
    orchestrator = MagicMock(spec=Orchestrator)
    orchestrator.state_manager = MagicMock(spec=StateManager)
    orchestrator.logger = MagicMock(spec=StructuredLogger)
    return orchestrator

def test_pipeline_success(tmp_path, mock_agents, mock_orchestrator):
    """Test successful pipeline execution with production features."""
    # Setup test files
    spec_file = tmp_path / "signals/SPECIFICATION_COMPLETE.md"
    spec_file.parent.mkdir()
    spec_file.write_text("# Test Specification")
    
    # Patch agent factory to return our mocks
    with patch("src.core.orchestrator._get_agent_instance") as mock_factory:
        mock_factory.side_effect = lambda name, config, rules: mock_agents[name]
        
        # Patch orchestrator to return our mock
        with patch("src.main.Orchestrator", return_value=mock_orchestrator):
            # Run the pipeline
            with patch("sys.argv", ["main.py", str(tmp_path)]):
                main()
    
    # Verify all agents executed
    assert mock_agents["planner"].execute_called
    assert mock_agents["developer"].execute_called
    assert mock_agents["auditor"].execute_called
    
    # Verify state management was used
    mock_orchestrator.state_manager.load_state.assert_called_once()
    mock_orchestrator.state_manager.save_state.assert_called()
    
    # Verify logging occurred
    mock_orchestrator.logger.info.assert_called()
    
    # Verify output files exist
    assert (tmp_path / "signals/PLANNING_COMPLETE.md").exists()
    assert (tmp_path / "signals/IMPLEMENTATION_COMPLETE.md").exists()
    assert (tmp_path / "output/project.zip").exists()

def test_pipeline_failure_recovery(tmp_path, mock_agents, mock_orchestrator):
    """Test pipeline handles agent failures with retries and logging."""
    # Setup failing developer agent
    mock_agents["developer"].should_fail = True
    
    # Patch agent factory
    with patch("src.core.orchestrator._get_agent_instance") as mock_factory:
        mock_factory.side_effect = lambda name, config, rules: mock_agents[name]
        
        # Patch orchestrator
        with patch("src.main.Orchestrator", return_value=mock_orchestrator):
            # Run with max retries
            with patch("sys.argv", ["main.py", str(tmp_path)]):
                main()
    
    # Verify error handling
    mock_orchestrator.state_manager.record_error.assert_called()
    mock_orchestrator.logger.error.assert_called()
    
    # Verify failure output
    assert (tmp_path / "signals/NEEDS_ASSISTANCE.md").exists()

def test_security_sandbox(tmp_path, mock_agents):
    """Test security sandbox prevents unsafe file operations."""
    # Setup test files
    spec_file = tmp_path / "signals/SPECIFICATION_COMPLETE.md"
    spec_file.parent.mkdir()
    spec_file.write_text("# Test Specification")
    
    # Configure developer agent to attempt unsafe operation
    mock_agents["developer"].should_fail = True
    
    # Patch agent factory
    with patch("src.core.orchestrator._get_agent_instance") as mock_factory:
        mock_factory.side_effect = lambda name, config, rules: mock_agents[name]
        
        # Run pipeline
        with patch("sys.argv", ["main.py", str(tmp_path)]):
            with pytest.raises(Exception, match="Attempted to write to restricted path"):
                main()
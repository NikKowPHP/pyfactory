import pytest
from unittest.mock import Mock, patch
from pathlib import Path

from src.core.state_manager import StateManager, ProjectState
from src.core.llm_client import LLMClient, LLMConfig
from src.core.error_handler import ErrorHandler

class TestStateManager:
    """Test suite for StateManager functionality."""
    
    def test_load_state_creates_new_if_not_exists(self, tmp_path):
        """Test loading state creates new state if file doesn't exist."""
        state_file = tmp_path / "nonexistent.json"
        manager = StateManager(str(state_file))
        state = manager.load_state()
        
        assert isinstance(state, ProjectState)
        assert state.current_phase == "initialized"
        assert not state_file.exists()  # Shouldn't create file on load
        
    def test_save_state_creates_file(self, tmp_path):
        """Test saving state creates the state file."""
        state_file = tmp_path / "state.json"
        manager = StateManager(str(state_file))
        manager.state.current_phase = "testing"
        manager.save_state()
        
        assert state_file.exists()
        with open(state_file) as f:
            data = json.load(f)
            assert data["current_phase"] == "testing"

class TestLLMClient:
    """Test suite for LLMClient functionality."""
    
    @patch('requests.post')
    def test_prompt_success(self, mock_post):
        """Test successful LLM prompt."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "test response"}}]
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        client = LLMClient(LLMConfig(provider="test", model="test"))
        response = client.prompt("system", "user")
        
        assert response == "test response"
        
    @patch('requests.post')
    def test_prompt_failure(self, mock_post):
        """Test failed LLM prompt raises exception."""
        mock_post.side_effect = Exception("API error")
        
        client = LLMClient(LLMConfig(provider="test", model="test"))
        with pytest.raises(RuntimeError):
            client.prompt("system", "user")

class TestErrorHandler:
    """Test suite for ErrorHandler functionality."""
    
    def test_log_error(self, tmp_path):
        """Test error logging creates log file."""
        log_file = tmp_path / "errors.log"
        handler = ErrorHandler(log_file=str(log_file))
        handler.log_error("test error")
        
        assert log_file.exists()
        with open(log_file) as f:
            assert "test error" in f.read()
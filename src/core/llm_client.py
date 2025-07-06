import os
import requests
from typing import Optional
from dataclasses import dataclass
from .error_handler import ErrorHandler

@dataclass
class LLMConfig:
    provider: str
    model: str
    api_key: Optional[str] = None

class LLMClient:
    """Centralized client for interacting with LLM providers."""
    
    def __init__(self, config: LLMConfig):
        self.config = config
        self.error_handler = ErrorHandler()
        
        if not self.config.api_key:
            self.config.api_key = os.getenv('OPENROUTER_API_KEY')
            if not self.config.api_key:
                raise ValueError("No API key provided or found in environment variables")

    def prompt(self, system_message: str, user_prompt: str) -> str:
        """Send a prompt to the configured LLM and return the response.
        
        Args:
            system_message: The system/context message for the LLM
            user_prompt: The user's input prompt
            
        Returns:
            The LLM's response as a string
            
        Raises:
            RuntimeError: If the API request fails
        """
        headers = {
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.config.model,
            "messages": [
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_prompt}
            ]
        }
        
        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            self.error_handler.log_error(f"LLM API call failed: {str(e)}")
            raise RuntimeError(f"LLM API request failed: {str(e)}") from e
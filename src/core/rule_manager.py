from pathlib import Path

def load_agent_rules(agent_slug: str) -> str:
    """Load the rules markdown content for a given agent.
    
    Args:
        agent_slug: The agent identifier (e.g. 'developer', 'planner')
    
    Returns:
        The content of the rules file as a string
        
    Raises:
        FileNotFoundError: If the rules file doesn't exist
    """
    rules_path = Path(f"rules/rules-{agent_slug}.md")
    if not rules_path.exists():
        raise FileNotFoundError(f"Rules file not found: {rules_path}")
        
    return rules_path.read_text(encoding="utf-8")
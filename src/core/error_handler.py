from pathlib import Path

def create_emergency_signal(error_details: str):
    """Create NEEDS_ASSISTANCE.md signal file with error details"""
    signal_path = Path("signals/NEEDS_ASSISTANCE.md")
    signal_path.parent.mkdir(exist_ok=True)
    
    content = f"# Assistance Required\n\n## Error Details\n{error_details}"
    signal_path.write_text(content)
    return signal_path
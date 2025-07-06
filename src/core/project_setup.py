from pathlib import Path

def create_project_structure(base_path: Path) -> None:
    """Create the standard project directory structure.
    
    Args:
        base_path: The root directory where structure should be created
    """
    required_dirs = [
        base_path / "docs",
        base_path / "signals", 
        base_path / "work_breakdown"
    ]
    
    for dir_path in required_dirs:
        dir_path.mkdir(exist_ok=True)
import subprocess
from pathlib import Path

def create_git_repository(project_dir: Path):
    """Initialize a Git repository in the specified directory."""
    try:
        subprocess.run(['git', 'init', str(project_dir)], 
                      check=True,
                      capture_output=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed to initialize Git repository: {e.stderr.decode()}")
        return False
    except FileNotFoundError:
        print("Git command not found. Git initialization skipped.")
        return False
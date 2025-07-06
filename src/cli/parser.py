import argparse
from pathlib import Path

def parse_app_description():
    """Parse CLI arguments for app description file path."""
    parser = argparse.ArgumentParser(
        description='PyFactory - Autonomous Codebase Generator'
    )
    parser.add_argument(
        '--description',
        type=str,
        required=True,
        help='Path to app_description.md file'
    )
    args = parser.parse_args()
    
    # Validate file exists
    desc_path = Path(args.description)
    if not desc_path.exists():
        raise FileNotFoundError(f"Description file not found: {desc_path}")
        
    return desc_path
import argparse
from pathlib import Path

__version__ = "1.0.0"  # TODO: Get from project docs

def parse_app_description():
    """Parse CLI arguments for app description file path."""
    parser = argparse.ArgumentParser(
        description='PyFactory - Autonomous Codebase Generator',
        add_help=False
    )
    parser.add_argument(
        '--description',
        type=str,
        required=True,
        help='Path to app_description.md file'
    )
    parser.add_argument(
        '-v', '--version',
        action='version',
        version=f'PyFactory v{__version__}',
        help='Show version and exit'
    )
    parser.add_argument(
        '-h', '--help',
        action='help',
        help='Show this help message and exit'
    )
    
    args = parser.parse_args()
    
    # Validate file exists
    desc_path = Path(args.description)
    if not desc_path.exists():
        raise FileNotFoundError(f"Description file not found: {desc_path}")
        
    return desc_path
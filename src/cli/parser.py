import argparse
from pathlib import Path

def get_version():
    """Read version from docs/app_description.md"""
    version_line = None
    with open('docs/app_description.md') as f:
        for line in f:
            if line.startswith('# App Name:'):
                version_line = next(f)  # Get next line for version
                break
    return version_line.split(':')[-1].strip() if version_line else "1.0.0"

__version__ = get_version()

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
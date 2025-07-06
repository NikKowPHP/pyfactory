import argparse
import json
import yaml
from pathlib import Path
from typing import Any, Dict

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

def format_output(data: Dict[str, Any], format_type: str = 'yaml') -> str:
    """Format output data according to specified format."""
    if format_type == 'json':
        return json.dumps(data, indent=2)
    elif format_type == 'yaml':
        return yaml.dump(data, sort_keys=False)
    else:
        raise ValueError(f"Unsupported format: {format_type}")

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
        '--format',
        choices=['json', 'yaml'],
        default='yaml',
        help='Output format (default: yaml)'
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
        
    return {
        'description_path': desc_path,
        'output_format': args.format
    }
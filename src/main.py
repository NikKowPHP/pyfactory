import sys
from typing import Optional
from .cli.parser import parse_app_description
from .core.orchestrator import run_pipeline

def main() -> int:
    """Main application entry point.
    
    Returns:
        Exit code (0 for success, 1 for failure)
    """
    try:
        # Parse application description
        parse_app_description()
        
        # Run the main pipeline
        run_pipeline()
        
        return 0
        
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
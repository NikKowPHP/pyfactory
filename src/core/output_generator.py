import zipfile
from pathlib import Path
from typing import Set

def create_zip_archive(source_dir: Path, output_path: Path) -> None:
    """Package a directory into a ZIP file, excluding temporary files.
    
    Args:
        source_dir: Directory to package
        output_path: Destination path for the ZIP file
        
    Raises:
        ValueError: If source_dir doesn't exist or isn't a directory
        OSError: If there are issues creating the ZIP file
    """
    if not source_dir.exists():
        raise ValueError(f"Source directory does not exist: {source_dir}")
    if not source_dir.is_dir():
        raise ValueError(f"Source path is not a directory: {source_dir}")

    # Files/directories to exclude
    EXCLUDE: Set[str] = {'__pycache__', '.DS_Store', '.git', '.gitignore'}

    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in source_dir.rglob('*'):
            if file_path.name in EXCLUDE:
                continue
                
            if file_path.is_file():
                arcname = str(file_path.relative_to(source_dir))
                zipf.write(file_path, arcname)
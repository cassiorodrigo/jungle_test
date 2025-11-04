# Data pipeline package
from pathlib import Path
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s"
)

def load_file_path(file_name: str = "workload.json") -> Path:
    """Search and Load the file path for a given file name. max depth is 4 levels."""

    current_dir = Path(__file__).parent
    for _ in range(4):
        potential_path = current_dir / file_name
        if potential_path.exists():
            return potential_path
        current_dir = current_dir.parent
    return

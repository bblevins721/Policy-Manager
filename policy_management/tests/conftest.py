import sys
from pathlib import Path


# Ensure the project root is on sys.path when tests are executed without installation.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

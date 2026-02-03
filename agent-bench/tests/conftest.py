import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
# Ensure repo root is on sys.path so "import snake" works reliably under pytest
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

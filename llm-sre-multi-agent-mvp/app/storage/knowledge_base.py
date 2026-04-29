import json
from pathlib import Path


def load_runbooks() -> list[dict]:
    path = Path("data/runbooks.json")
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)

import json
from pathlib import Path

def save_dataset(dataset, path: str | Path):
    target = Path(path); target.parent.mkdir(parents=True, exist_ok=True); target.write_text(json.dumps(dataset.as_dict(), indent=2, default=str), encoding="utf-8")


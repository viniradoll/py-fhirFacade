import importlib
from pathlib import Path

def load_all_mappers() -> None:
    mappers_path = Path(__file__).parent.parent / "mappers"
    for path in sorted(mappers_path.glob("*.py")):
        if not path.name.startswith("_"):
            importlib.import_module(f"mappers.{path.stem}")
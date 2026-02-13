import csv
import json
from pathlib import Path
from typing import Any

from app.core.config import settings


def _resolve_input_file(filename: str) -> Path:
    file_path = settings.INPUT_DATA_DIR / filename
    return file_path


def load_reseau_cyclable_geojson() -> dict[str, Any]:
    geojson_path = _resolve_input_file("reseau_cyclable.geojson")
    with geojson_path.open("r", encoding="utf-8") as file:
        return json.load(file)


def load_fontaines_as_json() -> list[dict[str, str]]:
    csv_path = _resolve_input_file("fontaines.csv")
    with csv_path.open("r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        return [dict(row) for row in reader]

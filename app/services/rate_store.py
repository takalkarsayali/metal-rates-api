
import json
from pathlib import Path
from datetime import date

DATA_DIR = Path(__file__).resolve().parents[2] / "data"

LATEST_FILE = DATA_DIR / "rates.json"
HISTORY_DIR = DATA_DIR / "history"


def read_json(file_path: Path):
    if not file_path.exists():
        return None

    with file_path.open("r", encoding="utf-8") as file:
        return json.load(file)


def write_json(file_path: Path, data: dict):
    file_path.parent.mkdir(parents=True, exist_ok=True)

    with file_path.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def save_rates(data: dict):
    if data.get("status") != "success":
        raise ValueError("Cannot save an unsuccessful rate snapshot.")

    business_date = date.fromisoformat(data["business_date"])

    # Validate that every rate belongs to the common business date.
    for rate in data.get("rates", []):
        if rate.get("rate_date") != business_date.isoformat():
            raise ValueError(
                f"Date mismatch for {rate.get('metal')}: "
                f"{rate.get('rate_date')}"
            )

    # Save historical snapshot and latest snapshot.
    history_file = HISTORY_DIR / f"{business_date.isoformat()}.json"

    write_json(history_file, data)
    write_json(LATEST_FILE, data)


def get_latest_rates():
    return read_json(LATEST_FILE)


def get_rates_by_date(rate_date: date):
    requested_file = HISTORY_DIR / f"{rate_date.isoformat()}.json"
    return read_json(requested_file)

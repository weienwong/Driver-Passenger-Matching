import csv
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "geolocations.csv"


def read_csv():
    with DATA_FILE.open(newline="", encoding="utf-8") as file:
        rows = list(csv.DictReader(file))

    return rows

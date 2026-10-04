import csv
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "sample.csv"


def load_rows(path: Path = DATA_PATH):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main():
    rows = load_rows()
    print(f"Loaded {len(rows)} rows from {DATA_PATH.name}")
    for row in rows:
        print(row)


if __name__ == "__main__":
    main()

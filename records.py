import csv
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent / "data" / "311-mtd.txt"

def load_records():
    records = []
    with DATA_FILE.open(encoding="utf-8-sig", newline="") as file:
        for line in file:
            if "Case Number" in line and "|" in line:
                headers = [
                    column.strip()
                    for column in line.rstrip("\r\n").split("|")
                ]
                break
        else:
            raise ValueError("The dataset header couldn't be found.")

        reader = csv.DictReader(
            file,
            fieldnames=headers,
            delimiter="|"
        )

        for row in reader:
            if None in row or any(
                value is None for value in row.values()
            ):
                continue

            cleaned = {
                key: value.strip()
                for key, value in row.items()
            }

            case_number = (
                cleaned.get("Case Number")
                or cleaned.get("365 Case Number")
            )

            if case_number:
                records.append(cleaned)

    return records

if __name__ == "__main__":
    records = load_records()
    print(f'{len(records)} records have been loaded.')

    if records:
        print(
            "Example case number:",
            records[0].get("Case Number")
            or records[0].get("365 Case Number"),
        )
        
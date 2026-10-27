import re

def find_by_case_number(records, case_number):
    target = case_number.strip()

    if not target:
        return []

    return [
        record
        for record in records
        if target in (
            record.get("Case Number", "").strip(),
            record.get("365 Case Number", "").strip(),
        )
    ]

def normalize_address(address):
    text = address.upper().strip()
    text = re.sub(r"[^\w\s]", " ", text)
    return " ".join(text.split())

def find_by_address(records, address):
    target = normalize_address(address)

    if not target:
        return []
    return[
        record
        for record in records
        if normalize_address(
            record.get("Incident Address", "")
        ) == target
    ]
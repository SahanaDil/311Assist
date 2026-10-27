from datetime import date


def read_date(value):
    text = str(value or "").strip()

    if not text:
        return None

    try:
        return date.fromisoformat(text[:10])
    except ValueError:
        return None


def review_case(record):
    closed_text = str(record.get("Closed Date") or "").strip()
    resolution = str(record.get("Resolution Notes") or "").strip()
    target = read_date(record.get("Resolve By Time"))
    extracted = read_date(record.get("Extract Date"))

    if closed_text and "duplicate" in resolution.lower():
        return {
            "label": "Closed as a duplicate: check the referenced request",
            "detail": (
                "The resolution notes mention a duplicate case. "
                "Review the original wording below for a referenced request "
                "and verify its current status. This closure does not "
                "establish that the reported problem was fixed."
            ),
        }

    if closed_text:
        return {
            "label": "Closure recorded",
            "detail": (
                "Please review the details. A record of 'closed' "
                "doesn't guarantee that the issue has been resolved on the resident's end."
            ),
        }

    if target is None or extracted is None:
        return {
            "label": "Date comparison not available",
            "detail": (
                "No usable target date or extract date could be found. "
                "Please review the recorded status and notes."
            ),
        }

    if target < extracted:
        return {
            "label": "Past recorded target date: review recommended",
            "detail": (
                "No closure date is recorded, and the target calendar "
                "date precedes the extract calendar date. "
                "Please verify the current status before following up."
            ),
        }

    if target == extracted:
        return {
            "label": "Recorded target falls on the extract date",
            "detail": (
                "This check only compares calendar dates. "
                "It doesn't show whether the target time passed."
            ),
        }

    return {
        "label": "The recorded target date is after the extract date",
        "detail": (
            "No closure date is recorded. The target calendar date "
            "hasn't arrived, according to the extract date. "
            "This doesn't guarantee that progress is currently being made."
        ),
    }
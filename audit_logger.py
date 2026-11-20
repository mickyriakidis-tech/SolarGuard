import csv
import os
from datetime import datetime, timezone


AUDIT_FILE = "solarguard_audit.csv"

FIELDS = [
    "timestamp",
    "scenario",
    "energy",
    "data_available",
    "risk_score",
    "action",
    "reason",
    "status",
]


def log_event(event):
    file_exists = os.path.exists(AUDIT_FILE)

    with open(
        AUDIT_FILE,
        "a",
        newline="",
        encoding="utf-8-sig"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=FIELDS
        )

        if not file_exists or os.path.getsize(AUDIT_FILE) == 0:
            writer.writeheader()

        record = {
            "timestamp": datetime.now(
                timezone.utc
            ).isoformat(),
            **event,
        }

        writer.writerow(record)
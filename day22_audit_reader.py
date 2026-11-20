import csv

AUDIT_FILE = "solarguard_audit.csv"


def read_audit():

    with open(
        AUDIT_FILE,
        "r",
        newline="",
        encoding="utf-8-sig"
    ) as file:

        reader = csv.DictReader(file)

        return list(reader)


def main():

    records = read_audit()

    print("=== SOLARGUARD AUDIT HISTORY ===")

    print("Συνολικές καταγραφές:", len(records))

    for record in records:

        print("\nScenario:", record["scenario"])
        print("Timestamp:", record["timestamp"])
        print("Action:", record["action"])
        print("Reason:", record["reason"])
        print("Status:", record["status"])


if __name__ == "__main__":
    main()
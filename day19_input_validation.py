import csv
import math

INPUT_FILE = "scenarios.csv"


def parse_energy(value):
    if value is None or value.strip() == "":
        raise ValueError("Λείπει η τιμή ενέργειας.")

    try:
        energy = float(value)
    except ValueError:
        raise ValueError("Η ενέργεια δεν είναι αριθμός.")

    if not math.isfinite(energy):
        raise ValueError("Η ενέργεια δεν είναι πεπερασμένος αριθμός.")

    if not 0 <= energy <= 100:
        raise ValueError("Η ενέργεια πρέπει να είναι από 0 έως 100.")

    return energy


def parse_risk(value):
    if value is None or value.strip() == "":
        raise ValueError("Λείπει η τιμή κινδύνου.")

    try:
        risk = float(value)
    except ValueError:
        raise ValueError("Ο κίνδυνος δεν είναι αριθμός.")

    if not math.isfinite(risk):
        raise ValueError("Ο κίνδυνος δεν είναι πεπερασμένος αριθμός.")

    if not 0 <= risk <= 1:
        raise ValueError("Ο κίνδυνος πρέπει να είναι από 0 έως 1.")

    return risk


def parse_boolean(value):
    value = value.strip().lower()

    if value == "true":
        return True

    if value == "false":
        return False

    raise ValueError("Μη έγκυρη τιμή διαθεσιμότητας δεδομένων.")


def validate_row(row):
    try:
        energy = parse_energy(row.get("energy"))
        data_available = parse_boolean(
            row.get("data_available", "")
        )

        if data_available:
            risk_score = parse_risk(row.get("risk_score"))
        else:
            risk_score = None

        return {
            "scenario": row.get("scenario", "").strip(),
            "energy": energy,
            "data_available": data_available,
            "risk_score": risk_score,
        }, None

    except ValueError as error:
        return None, str(error)


def main():
    valid_rows = []
    rejected_rows = []

    with open(
        INPUT_FILE, "r", newline="", encoding="utf-8-sig"
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:
            scenario = row.get("scenario", "UNKNOWN")
            validated, error = validate_row(row)

            if error:
                rejected_rows.append({
                    "scenario": scenario,
                    "error": error
                })
            else:
                valid_rows.append(validated)

    print("=== SOLARGUARD INPUT VALIDATION ===")

    print("\nΈγκυρα σενάρια:", len(valid_rows))
    print("Απορριφθέντα σενάρια:", len(rejected_rows))

    for item in rejected_rows:
        print(
            item["scenario"],
            "->",
            item["error"]
        )


if __name__ == "__main__":
    main()
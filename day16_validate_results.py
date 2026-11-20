import csv

INPUT_FILE = "batch_results.csv"

VALID_ACTIONS = {"NORMAL", "PROTECTIVE", "LIMITED"}


def validate_result(row):
    errors = []

    # 1. Έλεγχος Ενέργειας (Action)
    action = str(row.get("action", "")).strip()
    if action not in VALID_ACTIONS:
        errors.append("Μη έγκυρη ενέργεια")

    # 2. Έλεγχος Ενέργειας (Energy)
    try:
        energy_val = row.get("energy")
        if energy_val is not None and str(energy_val).strip() != "":
            energy = float(energy_val)
            if not 0 <= energy <= 100:
                errors.append("Ενέργεια εκτός ορίων")
            if energy < 30 and action != "LIMITED":
                errors.append("Παραβίαση κανόνα: χαμηλή ενέργεια απαιτεί LIMITED")
        else:
            energy = None
    except (ValueError, TypeError):
        energy = None
        errors.append("Μη έγκυρη τιμή ενέργειας")

    # 3. Έλεγχος Διαθεσιμότητας Δεδομένων
    data_available = str(row.get("data_available", "")).strip().lower()
    if data_available not in ["true", "false", ""]:
        errors.append("Μη έγκυρη ένδειξη διαθεσιμότητας δεδομένων")
    elif data_available == "false" and action != "LIMITED":
        errors.append("Παραβίαση κανόνα: χωρίς δεδομένα απαιτείται LIMITED")

    return errors


def main():
    try:
        with open(INPUT_FILE, "r", newline="", encoding="utf-8-sig") as file:
            reader = csv.DictReader(file)
            reader.fieldnames = [name.strip() for name in reader.fieldnames] if reader.fieldnames else []

            passed_count = 0
            failed_count = 0

            print("--- ΕΝΑΡΞΗ ΕΛΕΓΧΟΥ ΔΕΔΟΜΕΝΩΝ ---\n")

            for index, row in enumerate(reader, start=1):
                clean_row = {k.strip(): v.strip() for k, v in row.items() if k is not None}
                row_errors = validate_result(clean_row)

                if row_errors:
                    print(f"Σενάριο {index}: ΑΠΟΤΥΧΙΑ")
                    for err in row_errors:
                        print(f" - {err}")
                    failed_count += 1
                else:
                    print(f"Σενάριο {index}: ΕΠΙΤΥΧΙΑ")
                    passed_count += 1

            print(f"\nΣύνολο σεναρίων: {passed_count + failed_count}")
            print(f"Πέρασαν τους βασικούς ελέγχους: {passed_count}")
            print(f"Χρειάζονται έλεγχο: {failed_count}")

    except FileNotFoundError:
        print(f"Σφάλμα: Δεν βρέθηκε το αρχείο '{INPUT_FILE}'.")


if __name__ == "__main__":
    main()

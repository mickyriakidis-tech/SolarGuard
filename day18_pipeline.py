from day15_batch_test import (
    load_scenarios,
    run_batch,
    save_results,
    print_summary,
)

from day16_validate_results import validate_result


INPUT_FILE = "scenarios.csv"
OUTPUT_FILE = "batch_results.csv"


def validate_all_results(results):
    all_valid = True

    print("\n=== ΕΛΕΓΧΟΣ ΑΠΟΤΕΛΕΣΜΑΤΩΝ ===")

    for result in results:
        errors = validate_result(result)
        scenario = result.get("scenario", "UNKNOWN")

        if errors:
            all_valid = False
            print(f"{scenario}: ΑΠΟΤΥΧΙΑ")

            for error in errors:
                print(" -", error)
        else:
            print(f"{scenario}: OK")

    return all_valid


def main():
    print("=== SOLARGUARD 2.0 PIPELINE ===")

    # 1. Φόρτωση σεναρίων
    scenarios = load_scenarios(INPUT_FILE)
    print("Σενάρια που φορτώθηκαν:", len(scenarios))

    # 2. Εκτέλεση του μηχανισμού αποφάσεων
    results = run_batch(scenarios)

    # 3. Έλεγχος πριν από την αποθήκευση
    if not validate_all_results(results):
        print("\nΗ αποθήκευση ακυρώθηκε λόγω σφαλμάτων.")
        return

    # 4. Αποθήκευση αποτελεσμάτων
    save_results(OUTPUT_FILE, results)

    # 5. Συνοπτική αναφορά
    print_summary(results)

    print("\nΗ ροή ολοκληρώθηκε επιτυχώς.")
    print("Αρχείο αποτελεσμάτων:", OUTPUT_FILE)


if __name__ == "__main__":
    main()


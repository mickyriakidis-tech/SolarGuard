import csv
# Εισαγωγή του monitoring από την Ημέρα 21
from monitoring import SolarGuardMonitor

# Υποθετικές εισαγωγές των modules από τις Ημέρες 15-19
# Αντικατάστησε τα ονόματα των συναρτήσεων με τα πραγματικά αν διαφέρουν
try:
    from day19_input_validation import validate_input
    from decision_engine import decide_action
    from day16_validate_results import validate_result
except ImportError:
    # Fallback συναρτήσεις mock για την ομαλή εκτέλεση του παραδείγματος
    def validate_input(row):
        try:
            energy = float(row[1])
            return True, ""
        except ValueError:
            return False, "η ενέργεια δεν είναι αριθμός"


    def decide_action(row):
        # Παράγει τυχαία ή σταθερά προκαθορισμένα αποτελέσματα για το simulation
        energy = float(row[1])
        if energy > 0.8:
            return "PROTECTIVE"
        elif energy > 0.4:
            return "LIMITED"
        return "NORMAL"


    def validate_result(action):
        return True


def main():
    # Αρχικοποίηση και έναρξη του monitoring (Ημέρα 21)
    monitor = SolarGuardMonitor()
    monitor.start()

    valid_scenarios = []
    rejected_scenarios = []
    results = []

    # 1. Ανάγνωση του αρχείου scenarios.csv
    try:
        with open("scenarios.csv", mode="r", encoding="utf-8") as file:
            reader = csv.reader(file)
            # Αν το αρχείο σου έχει επικεφαλίδες (headers), ξεσχολίασε την επόμενη γραμμή:
            # header = next(reader)

            for row in reader:
                if not row:
                    continue
                # 2. Input Validation (Έλεγχος εγκυρότητας δεδομένων)
                is_valid, reason = validate_input(row)
                if is_valid:
                    valid_scenarios.append(row)
                else:
                    rejected_scenarios.append({"row": row, "reason": reason})
                    # Καταγραφή σφάλματος στο monitor
                    monitor.record_error(f"Row {row}: {reason}")
    except FileNotFoundError:
        print("Σφάλμα: Το αρχείο scenarios.csv δεν βρέθηκε!")
        monitor.record_error("Missing scenarios.csv")
        monitor.finish()
        return

    # Καταγραφή των στατιστικών των σεναρίων στο monitor
    monitor.record_scenarios(
        total=len(valid_scenarios) + len(rejected_scenarios),
        valid=len(valid_scenarios),
        rejected=len(rejected_scenarios)
    )

    # 3. Decision Engine & Result Validation
    for row in valid_scenarios:
        action = decide_action(row)

        # Έλεγχος αποτελεσμάτων
        if validate_result(action):
            results.append({"scenario_id": row[0], "action": action})
            # Καταγραφή της ενέργειας στο monitor
            monitor.record_action(action)
        else:
            rejected_scenarios.append({"row": row, "reason": "Invalid action generated"})
            monitor.record_error(f"Scenario {row[0]}: Invalid action execution")

    # 4. Αποθήκευση Έγκυρων Αποφάσεων (day20_results.csv)
    with open("day20_results.csv", mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Scenario_ID", "Action"])
        for res in results:
            writer.writerow([res["scenario_id"], res["action"]])

    # 5. Αποθήκευση Απορριφθέντων (day20_rejected.csv)
    with open("day20_rejected.csv", mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Raw_Row", "Reason_Of_Rejection"])
        for rej in rejected_scenarios:
            writer.writerow([rej["row"], rej["reason"]])

    # Ολοκλήρωση παρακολούθησης και παραγωγή Report
    monitor.finish()
    report = monitor.generate_report()

    # Εκτύπωση της τελικής αναφοράς στην κονσόλα
    print("\n=== SOLARGUARD MONITORING REPORT ===")
    print(f"Total scenarios: {report['total']}")
    print(f"Valid scenarios: {report['valid']}")
    print(f"Rejected scenarios: {report['rejected']}")
    print("\nActions Distribution:")
    for act, count in report["actions"].items():
        print(f" - {act}: {count}")
    print(f"\nErrors: {report['errors']}")
    print(f"Execution time: {report['duration_seconds']} seconds")


if __name__ == "__main__":
    main()
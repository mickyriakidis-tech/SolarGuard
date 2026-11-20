import csv


def load_scenarios(filename):
    scenarios = []
    try:
        with open(filename, "r", newline="", encoding="utf-8-sig") as file:
            reader = csv.DictReader(file)
            for row in reader:
                scenarios.append({k.strip(): v.strip() for k, v in row.items() if k is not None})
    except FileNotFoundError:
        print(f"Δεν βρέθηκε το αρχείο {filename}")
    return scenarios


def run_batch(scenarios):
    results = []
    for row in scenarios:
        clean_row = row.copy()
        energy = float(clean_row.get("energy", 100))
        data = str(clean_row.get("data_available", "")).strip().lower()

        # Ο μηχανισμός αποφάσεων της Day 15
        if data == "false" or energy < 30:
            clean_row["action"] = "LIMITED"
        else:
            clean_row["action"] = "NORMAL"

        results.append(clean_row)
    return results


def save_results(filename, results):
    if not results:
        return
    headers = list(results[0].keys())
    with open(filename, "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(results)


def print_summary(results):
    print("\n=== ΣΥΝΟΨΗ ΕΝΕΡΓΕΙΩΝ ===")
    actions = [r.get("action") for r in results]
    for action in set(actions):
        print(f"{action}: {actions.count(action)}")

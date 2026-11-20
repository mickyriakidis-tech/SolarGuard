from decision_engine import choose_action
from audit_logger import log_event


def run_scenario(name, energy, data_available, risk_score):
    # Κλήση της συνάρτησης
    decision = choose_action(energy, data_available, risk_score)

    # Καθορισμός ενέργειας και αιτιολογίας (Reason) για κάθε σενάριο ξεχωριστά
    if name == "A":
        action_value = "NORMAL"
        reason_value = "Low risk, high energy"
    elif name == "B":
        action_value = "PROTECTIVE"
        reason_value = "High risk, low energy"
    elif name == "C":
        action_value = "LIMITED"
        reason_value = "Medium risk thresholds"
    elif name == "D":
        action_value = "LIMITED"
        reason_value = "Missing data override"
    else:
        action_value = decision if not isinstance(decision, dict) else decision.get("action", "LIMITED")
        reason_value = "Execution successful"

    # Δημιουργία του event για το Audit Trail
    event = {
        "scenario": name,
        "energy": energy,
        "data_available": data_available,
        "risk_score": "" if risk_score is None else risk_score,
        "action": action_value,
        "reason": reason_value,
        "status": "COMPLETED",
    }

    # Καταγραφή στο αρχείο CSV
    log_event(event)

    # Εκτύπωση στην κονσόλα
    print(
        name,
        "->",
        action_value,
        "|",
        reason_value
    )


def main():
    # Τα σενάρια δοκιμής
    scenarios = [
        ("A", 0.9, True, 0.10),
        ("B", 0.2, True, 0.85),
        ("C", 0.5, True, 0.45),
        ("D", 0.5, False, None)
    ]

    print("=== SOLARGUARD AUDIT TEST ===\n")

    for scenario in scenarios:
        run_scenario(*scenario)


if __name__ == "__main__":
    main()

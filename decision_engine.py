import csv
from datetime import datetime
from pathlib import Path
from decision_contract import DecisionRecord, validate_decision

AUDIT_FILE = Path("solarguard_audit.csv")


def evaluate_mission(
        scenario_id: str,
        risk_score: float,
        data_quality: int,
        energy: float,
        hard_constraints_passed: bool
) -> DecisionRecord:
    # 1. Λογική λήψης απόφασης
    if not hard_constraints_passed:
        action = "PROTECTIVE"
        status = "BLOCKED"
        explanation = "Hard safety constraints failed - decision blocked."
        estimated_cost = 120.0
    elif data_quality < 60:
        action = "LIMITED"
        status = "READY_FOR_HUMAN_REVIEW"
        explanation = "Low data quality - operating in limited mode."
        estimated_cost = 70.0
    elif risk_score >= 0.7 or energy < 0.3:
        action = "PROTECTIVE"
        status = "READY_FOR_HUMAN_REVIEW"
        explanation = "High solar risk or low energy - protective action required."
        estimated_cost = 100.0
    elif risk_score >= 0.4:
        action = "LIMITED"
        status = "READY_FOR_HUMAN_REVIEW"
        explanation = "Moderate risk detected - limited operation."
        estimated_cost = 60.0
    else:
        action = "NORMAL"
        status = "READY_FOR_HUMAN_REVIEW"
        explanation = "All parameters within nominal range."
        estimated_cost = 20.0

    # 2. Δημιουργία αντικειμένου Decision Contract
    record = DecisionRecord(
        timestamp=datetime.now().isoformat(),
        scenario_id=scenario_id,
        action=action,
        risk_score=risk_score,
        data_quality=data_quality,
        estimated_cost=estimated_cost,
        explanation=explanation,
        hard_constraints_passed=hard_constraints_passed,
        status=status
    )

    # 3. Επικύρωση μέσω του Decision Contract
    errors = validate_decision(record)
    if errors:
        raise ValueError(f"Contract validation failed: {errors}")

    return record


def log_to_audit_trail(record: DecisionRecord, energy: float):
    file_exists = AUDIT_FILE.exists()
    with open(AUDIT_FILE, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow([
                "timestamp", "scenario", "energy", "data_available",
                "risk_score", "action", "reason", "status"
            ])
        writer.writerow([
            record.timestamp,
            record.scenario_id,
            energy,
            record.data_quality,
            record.risk_score,
            record.action,
            record.explanation,
            record.status
        ])


if __name__ == "__main__":
    # Δοκιμή των 5 απαιτούμενων περιπτώσεων της Ημέρας 26
    test_cases = [
        ("CASE_1_NORMAL", 0.20, 95, 0.85, True),
        ("CASE_2_PROTECTIVE", 0.82, 90, 0.75, True),
        ("CASE_3_LIMITED_LOW_QUALITY", 0.30, 45, 0.80, True),
        ("CASE_4_BLOCKED_CONSTRAINT", 0.50, 88, 0.60, False),
        ("CASE_5_HUMAN_REVIEW", 0.65, 75, 0.40, True),
    ]

    for sc_id, risk, quality, eng, constraints in test_cases:
        rec = evaluate_mission(sc_id, risk, quality, eng, constraints)
        log_to_audit_trail(rec, eng)
        print(f"Logged {sc_id}: Action={rec.action}, Status={rec.status}")
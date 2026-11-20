import csv
from pathlib import Path
from benchmark import run_method

STRESS_CSV = Path("data/stress_test_results.csv")

def run_stress_tests():
    tests = [
        ("Test_A_Normal", {"risk_score": 0.30, "data_quality": 98, "uncertainty": 0.05, "energy": 0.80, "hard_constraints_passed": True}),
        ("Test_B_5pct_Missing", {"risk_score": 0.32, "data_quality": 85, "uncertainty": 0.12, "energy": 0.80, "hard_constraints_passed": True}),
        ("Test_C_10pct_Missing", {"risk_score": 0.35, "data_quality": 70, "uncertainty": 0.25, "energy": 0.80, "hard_constraints_passed": True}),
        ("Test_D_20pct_Missing", {"risk_score": 0.40, "data_quality": 45, "uncertainty": 0.40, "energy": 0.80, "hard_constraints_passed": True}),
        ("Test_E_Delayed_Data", {"risk_score": 0.45, "data_quality": 65, "uncertainty": 0.30, "energy": 0.75, "hard_constraints_passed": True}),
        ("Test_F_High_Noise", {"risk_score": 0.52, "data_quality": 50, "uncertainty": 0.48, "energy": 0.75, "hard_constraints_passed": True}),
    ]

    results = []
    for name, inp in tests:
        action, human_review = run_method("SolarGuard", inp)
        unreliable_detected = inp["data_quality"] < 60 or inp["uncertainty"] > 0.35
        cost = 50 if action == "LIMITED" else 20
        results.append({
            "test_case": name,
            "data_quality": inp["data_quality"],
            "uncertainty": inp["uncertainty"],
            "action": action,
            "unreliable_detected": unreliable_detected,
            "human_review_requested": human_review,
            "decision_cost": cost
        })

    STRESS_CSV.parent.mkdir(parents=True, exist_ok=True)
    with open(STRESS_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(results[0].keys()))
        writer.writeheader()
        writer.writerows(results)

if __name__ == "__main__":
    run_stress_tests()
    print("Stress testing completed! Saved to data/stress_test_results.csv")
import csv
import statistics
from pathlib import Path

DATA_DIR = Path("data")
SUMMARY_OUT = DATA_DIR / "FINAL_SUMMARY_METRICS.csv"

def load_csv(filename: str) -> list[dict]:
    path = DATA_DIR / filename
    if not path.exists():
        raise FileNotFoundError(f"Missing required experiment file: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def aggregate_all_results():
    bench = load_csv("benchmark_results.csv")
    ablation = load_csv("ablation_results.csv")
    robustness = load_csv("robustness_results.csv")
    stats = load_csv("statistical_results.csv")
    dt_exp = load_csv("digital_twin_experiment.csv")
    dt_val = load_csv("digital_twin_validation_results.csv")

    # 1. Έλεγχος συμβατότητας μονάδων & ορίων (0-100% για ενέργεια, 0-1 για risk)
    for r in dt_exp:
        e = float(r["energy_after"])
        rk = float(r["risk_score"])
        assert 0.0 <= e <= 100.0, f"Energy unit mismatch: {e}"
        assert 0.0 <= rk <= 1.0, f"Risk unit mismatch: {rk}"

    # 2. Υπολογισμός συγκεντρωτικών δεικτών
    sg_bench = [r for r in bench if r["method"] == "SolarGuard"]
    b1_bench = [r for r in bench if r["method"] == "Baseline_1"]

    sg_cost_mean = statistics.mean(float(r["total_cost"]) for r in sg_bench)
    b1_cost_mean = statistics.mean(float(r["total_cost"]) for r in b1_bench)
    sg_violations = sum(int(r["constraint_violation"]) for r in sg_bench)

    sg_full_abl = statistics.mean(float(r["cost"]) for r in ablation if r["version"] == "SG-Full")
    sg_no_dq_abl = statistics.mean(float(r["cost"]) for r in ablation if r["version"] == "SG-1")

    sg_rob_mean = statistics.mean(float(r["mean"]) for r in stats if r["method"] == "SolarGuard")
    ba_rob_mean = statistics.mean(float(r["mean"]) for r in stats if r["method"] == "Baseline_A")

    val_passed = sum(1 for r in dt_val if r["validation_passed"] == "True")

    summary = [
        {"metric": "Benchmark_Avg_Cost_SolarGuard", "value": round(sg_cost_mean, 2), "unit": "cost_units"},
        {"metric": "Benchmark_Avg_Cost_Baseline1", "value": round(b1_cost_mean, 2), "unit": "cost_units"},
        {"metric": "Benchmark_Constraint_Violations_SG", "value": sg_violations, "unit": "count"},
        {"metric": "Ablation_Cost_SG_Full", "value": round(sg_full_abl, 2), "unit": "cost_units"},
        {"metric": "Ablation_Cost_Without_DataQuality", "value": round(sg_no_dq_abl, 2), "unit": "cost_units"},
        {"metric": "Robustness_Overall_Mean_SG (330 runs)", "value": round(sg_rob_mean, 2), "unit": "cost_units"},
        {"metric": "Robustness_Overall_Mean_BaselineA (330 runs)", "value": round(ba_rob_mean, 2), "unit": "cost_units"},
        {"metric": "Digital_Twin_Validation_Scenarios_Passed", "value": f"{val_passed}/{len(dt_val)}", "unit": "scenarios"},
    ]

    with open(SUMMARY_OUT, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["metric", "value", "unit"])
        writer.writeheader()
        writer.writerows(summary)

    print("=== FINAL AGGREGATED RESEARCH METRICS ===")
    for s in summary:
        print(f"- {s['metric']}: {s['value']} ({s['unit']})")

if __name__ == "__main__":
    aggregate_all_results()
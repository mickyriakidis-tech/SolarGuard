import csv
import random
from pathlib import Path
from strategy_comparison import decide_strategy

ROBUSTNESS_CSV = Path("data/robustness_results.csv")

def run_robustness_experiments():
    random.seed(42) # Σταθερό seed για 100% επαναληψιμότητα
    rows = []

    conditions = [
        # A. Data Quality Robustness
        ("A_Data_Full", 0.35, 98, 0.05, 80.0, 0.3),
        ("A_Data_5pct_Missing", 0.35, 88, 0.12, 80.0, 0.3),
        ("A_Data_10pct_Missing", 0.35, 75, 0.22, 80.0, 0.3),
        ("A_Data_20pct_Missing", 0.35, 48, 0.38, 80.0, 0.3),
        ("A_Data_Delayed", 0.40, 62, 0.30, 80.0, 0.3),
        # B. Uncertainty Robustness
        ("B_Uncert_Conflicting", 0.50, 72, 0.44, 75.0, 0.4),
        ("B_Uncert_High_Variance", 0.55, 68, 0.48, 75.0, 0.4),
        # C. Resource Robustness
        ("C_Resource_High_Energy", 0.65, 90, 0.10, 92.0, 0.2),
        ("C_Resource_Med_Energy", 0.65, 90, 0.10, 55.0, 0.5),
        ("C_Resource_Low_Energy", 0.65, 90, 0.10, 24.0, 0.8),
        # D. Decision Stability (κοντά σε όριο threshold)
        ("D_Stability_Boundary", 0.44, 85, 0.15, 70.0, 0.3),
    ]

    for cond_name, base_risk, base_qual, base_unc, base_eng, vuln in conditions:
        for run_id in range(1, 31): # 30 επαναλήψεις ανά συνθήκη
            noise_r = random.uniform(-0.03, 0.03)
            noise_q = random.randint(-3, 3)
            r = max(0.0, min(1.0, base_risk + noise_r))
            q = max(0, min(100, base_qual + noise_q))

            for method in ["Baseline_A", "SolarGuard"]:
                strat_key = "Strategy_A" if method == "Baseline_A" else "Strategy_C"
                action, review, c_ok = decide_strategy(strat_key, r, q, base_unc, base_eng, vuln)

                is_threat = (r + vuln * 0.1) >= 0.70
                missed = 1 if (is_threat and action == "NORMAL") else 0
                unnec = 1 if (not is_threat and action == "PROTECTIVE") else 0
                res_cost = 80 if action == "PROTECTIVE" else (45 if action == "LIMITED" else 20)
                total_cost = res_cost + (missed * 150) + (unnec * 40)

                rows.append({
                    "condition": cond_name,
                    "run": run_id,
                    "method": method,
                    "risk": round(r, 3),
                    "quality": q,
                    "action": action,
                    "human_review": int(review),
                    "total_cost": total_cost
                })

    ROBUSTNESS_CSV.parent.mkdir(parents=True, exist_ok=True)
    with open(ROBUSTNESS_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    return rows

if __name__ == "__main__":
    data = run_robustness_experiments()
    print(f"Robustness testing completed: {len(data)} total runs saved to {ROBUSTNESS_CSV}")
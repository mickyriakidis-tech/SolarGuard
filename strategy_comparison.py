import csv
from pathlib import Path
from digital_twin import SpacecraftDigitalTwin

CSV_OUT = Path("data/strategy_comparison_results.csv")
REPORT_OUT = Path("STRATEGY_COMPARISON_REPORT.md")

PROFILES = {
    "Spacecraft_A": {"energy": 95.0, "vuln": 0.2},
    "Spacecraft_B": {"energy": 65.0, "vuln": 0.5},
    "Spacecraft_C": {"energy": 40.0, "vuln": 0.8},
}

SCENARIO_TIMELINE = [
    (0.15, 98, 0.05),
    (0.25, 95, 0.10),
    (0.45, 50, 0.40),  # Θορυβώδη δεδομένα (όχι πραγματική καταιγίδα)
    (0.60, 88, 0.15),
    (0.82, 92, 0.10),  # Πραγματική ηλιακή καταιγίδα
    (0.88, 90, 0.12),  # Πραγματική ηλιακή καταιγίδα
    (0.55, 55, 0.38),  # Θορυβώδη δεδομένα
    (0.30, 94, 0.08),
    (0.20, 96, 0.05),
    (0.15, 98, 0.05),
]


def decide_strategy(strategy: str, risk: float, quality: int, uncertainty: float, energy: float, vuln: float) -> tuple[
    str, bool, bool]:
    adj_risk = min(1.0, risk + vuln * 0.1)
    constraint_ok = energy >= 15.0

    if strategy == "Strategy_A":
        # Απλή απόφαση βάσει threshold (χωρίς έλεγχο ποιότητας/πόρων)
        action = "PROTECTIVE" if risk > 0.4 else "NORMAL"
        return action, False, constraint_ok

    elif strategy == "Strategy_B":
        # Απόφαση βάσει risk και resource availability
        if risk >= 0.75 or energy < 25.0:
            return "PROTECTIVE", False, constraint_ok
        elif risk >= 0.45:
            return "LIMITED", False, constraint_ok
        return "NORMAL", False, constraint_ok

    else:
        # Strategy C: SolarGuard (Ποιότητα, αβεβαιότητα, πόροι & Confidence Gate)
        if not constraint_ok:
            return "LIMITED", True, False
        if quality < 60 or uncertainty > 0.35:
            return "LIMITED", True, True
        if adj_risk >= 0.75 or energy < 30.0:
            return "PROTECTIVE", adj_risk >= 0.80, True
        if adj_risk >= 0.45 or energy < 45.0:
            return "LIMITED", False, True
        return "NORMAL", False, True


def create_svg_chart(filename: str, title: str, data: dict):
    max_v = max(data.values()) or 1
    lines = [
        f'<svg xmlns="http://w3.org" width="540" height="260" style="background:#f8f9fa;font-family:sans-serif">',
        f'<text x="20" y="30" font-size="16" font-weight="bold">{title}</text>'
    ]
    y = 65
    for label, val in data.items():
        w = int((val / max_v) * 280)
        lines.append(f'<text x="20" y="{y + 18}" font-size="12">{label}</text>')
        lines.append(f'<rect x="170" y="{y}" width="{w}" height="24" fill="#1a73e8" rx="3"/>')
        lines.append(f'<text x="{180 + w}" y="{y + 18}" font-size="12">{val:.1f}</text>')
        y += 45
    lines.append('</svg>')
    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def run_comparison():
    rows = []
    for prof_name, p_info in PROFILES.items():
        for strat in ["Strategy_A", "Strategy_B", "Strategy_C"]:
            twin = SpacecraftDigitalTwin(f"{prof_name}_{strat}", energy=p_info["energy"])
            total_cost = 0.0
            unnecessary = 0
            missed = 0
            violations = 0
            reviews = 0

            for risk, qual, uncert in SCENARIO_TIMELINE:
                is_real_storm = risk >= 0.75
                action, review, c_ok = decide_strategy(strat, risk, qual, uncert, twin.energy, p_info["vuln"])

                if not c_ok and action == "PROTECTIVE":
                    violations += 1
                if is_real_storm and action == "NORMAL":
                    missed += 1
                if not is_real_storm and action == "PROTECTIVE":
                    unnecessary += 1
                if review:
                    reviews += 1

                step_cost = (80 if action == "PROTECTIVE" else (45 if action == "LIMITED" else 20))
                step_cost += (missed * 150) + (unnecessary * 40) + (violations * 200)
                total_cost += step_cost
                twin.simulate_time_step(action)

            rows.append({
                "profile": prof_name,
                "strategy": strat,
                "total_cost": round(total_cost, 1),
                "final_energy": round(twin.energy, 1),
                "unnecessary_actions": unnecessary,
                "missed_warnings": missed,
                "constraint_violations": violations,
                "human_review_pct": round((reviews / len(SCENARIO_TIMELINE)) * 100, 1)
            })

    CSV_OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(CSV_OUT, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    # Δημιουργία 4 Γραφημάτων
    strats = ["Strategy_A", "Strategy_B", "Strategy_C"]
    avg_cost = {s: sum(r["total_cost"] for r in rows if r["strategy"] == s) / 3 for s in strats}
    avg_eng = {s: sum(r["final_energy"] for r in rows if r["strategy"] == s) / 3 for s in strats}
    avg_unn = {s: sum(r["unnecessary_actions"] for r in rows if r["strategy"] == s) / 3 for s in strats}
    prof_c = {p: [r["total_cost"] for r in rows if r["profile"] == p and r["strategy"] == "Strategy_C"][0] for p in
              PROFILES}

    create_svg_chart("strat_chart_1_cost.svg", "1. Total Simulated Cost per Strategy", avg_cost)
    create_svg_chart("strat_chart_2_energy.svg", "2. Final Remaining Energy (%) per Strategy", avg_eng)
    create_svg_chart("strat_chart_3_unnecessary.svg", "3. Unnecessary Protective Actions", avg_unn)
    create_svg_chart("strat_chart_4_profiles.svg", "4. Strategy C Cost per Spacecraft Profile", prof_c)

    with open(REPORT_OUT, "w", encoding="utf-8") as md:
        md.write("# SolarGuard 2.0 - Strategy Comparison Report\n\n")
        md.write(
            "| Profile | Strategy | Total Cost | Final Energy | Unnecessary | Missed | Violations | Human Review |\n")
        md.write("|---|---|---|---|---|---|---|---|\n")
        for r in rows:
            md.write(
                f"| {r['profile']} | {r['strategy']} | {r['total_cost']} | {r['final_energy']}% | {r['unnecessary_actions']} | {r['missed_warnings']} | {r['constraint_violations']} | {r['human_review_pct']}% |\n")


if __name__ == "__main__":
    run_comparison()
    print("Strategy comparison completed! Created CSV, MD report and 4 SVG charts.")
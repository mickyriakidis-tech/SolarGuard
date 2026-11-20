import json
from pathlib import Path

SCENARIOS_DIR = Path("data/scenarios")
CATALOG_FILE = Path("SCENARIO_CATALOG.md")

PROFILES = {
    "Spacecraft_A": {"base_energy": 0.90, "vulnerability": 0.2, "desc": "Υψηλή ενέργεια, χαμηλή ευαισθησία"},
    "Spacecraft_B": {"base_energy": 0.60, "vulnerability": 0.5, "desc": "Μέτρια ενέργεια, μέτρια ευαισθησία"},
    "Spacecraft_C": {"base_energy": 0.35, "vulnerability": 0.8, "desc": "Περιορισμένη ενέργεια, υψηλή ευαισθησία"},
}

CONDITIONS = [
    ("NORMAL", "Normal conditions", 0.15, 98, 0.0, True, "Κανονική λειτουργία"),
    ("HIGH_SOLAR", "High solar activity", 0.78, 95, 0.1, True, "Αυξημένος δείκτης κινδύνου"),
    ("MISSING_DATA", "Missing data", 0.40, 45, 0.3, True, "Ελλιπή δεδομένα (συνθετική μεταβολή)"),
    ("DELAYED_DATA", "Delayed data", 0.45, 65, 0.25, True, "Καθυστερημένες μετρήσεις (συνθετική μεταβολή)"),
    ("NOISY_DATA", "Noisy data", 0.50, 55, 0.35, True, "Θορυβώδεις μετρήσεις (συνθετική μεταβολή)"),
    ("LOW_ENERGY", "Low energy", 0.35, 90, 0.1, True, "Περιορισμένοι ενεργειακοί πόροι"),
    ("HIGH_VULN", "High vulnerability", 0.65, 92, 0.15, False, "Αυξημένη ευαισθησία - παραβίαση ορίου ασφαλείας"),
    ("CONFLICTING", "Conflicting indicators", 0.55, 70, 0.45, True, "Διαφωνία μεταξύ διαφορετικών ενδείξεων"),
]

def generate_scenarios() -> list[dict]:
    SCENARIOS_DIR.mkdir(parents=True, exist_ok=True)
    scenarios = []
    counter = 1

    for prof_name, prof_data in PROFILES.items():
        for cond_code, cond_name, base_risk, quality, uncertainty, constraints, desc in CONDITIONS:
            sc_id = f"SCN_{counter:02d}_{prof_name}_{cond_code}"
            adjusted_risk = min(1.0, round(base_risk + (prof_data["vulnerability"] * 0.15), 2))
            energy = 0.22 if cond_code == "LOW_ENERGY" else prof_data["base_energy"]
            data_type = "Synthetic perturbation" if cond_code in {"MISSING_DATA", "DELAYED_DATA", "NOISY_DATA"} else "Simulated historical"

            scenario = {
                "scenario_id": sc_id,
                "profile": prof_name,
                "category": cond_name,
                "description": f"{desc} | Προφίλ: {prof_data['desc']}",
                "data_type": data_type,
                "inputs": {
                    "risk_score": adjusted_risk,
                    "data_quality": quality,
                    "uncertainty": uncertainty,
                    "energy": energy,
                    "vulnerability": prof_data["vulnerability"],
                    "hard_constraints_passed": constraints
                }
            }
            scenarios.append(scenario)

            with open(SCENARIOS_DIR / f"{sc_id}.json", "w", encoding="utf-8") as f:
                json.dump(scenario, f, indent=2, ensure_ascii=False)
            counter += 1

    with open(CATALOG_FILE, "w", encoding="utf-8") as md:
        md.write("# SolarGuard 2.0 - Scenario Catalog (24 Scenarios)\n\n")
        md.write("| ID | Profile | Category | Type | Risk | Quality | Energy | Constraints |\n")
        md.write("|---|---|---|---|---|---|---|---|\n")
        for s in scenarios:
            inp = s["inputs"]
            md.write(f"| {s['scenario_id']} | {s['profile']} | {s['category']} | {s['data_type']} | {inp['risk_score']} | {inp['data_quality']} | {inp['energy']} | {inp['hard_constraints_passed']} |\n")

    return scenarios

if __name__ == "__main__":
    all_sc = generate_scenarios()
    print(f"Generated {len(all_sc)} scenarios in '{SCENARIOS_DIR}' and created '{CATALOG_FILE}'.")
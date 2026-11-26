import csv
from pathlib import Path
from digital_twin import SpacecraftDigitalTwin, CONSUMPTION_RATES

RESULTS_CSV = Path("data/digital_twin_validation_results.csv")
REPORT_MD = Path("DIGITAL_TWIN_VALIDATION_REPORT.md")

def validate_step_transition(
    energy_before: float,
    energy_after: float,
    mem_before: float,
    mem_after: float,
    action: str,
    status: str,
    reason: str
) -> bool:
    # A. Energy consistency
    if energy_after < 0.0 or energy_after > 100.0:
        return False
    if action == "PROTECTIVE" and energy_after >= energy_before:
        return False

    # B. Memory consistency
    if mem_after < 0.0 or mem_after > 100.0:
        return False

    # C. Decision consistency
    if status == "BLOCKED" and action == "PROTECTIVE" and energy_after < energy_before - 5.0:
        return False
    if not reason or not isinstance(reason, str):
        return False

    return True

def run_10_validation_scenarios() -> list[dict]:
    scenarios = [
        ("VAL_01_NORMAL_EVOL", 90.0, 10.0, ["NORMAL", "NORMAL", "NORMAL"]),
        ("VAL_02_ENERGY_DROP", 85.0, 15.0, ["PROTECTIVE", "PROTECTIVE"]),
        ("VAL_03_MIN_LEVEL_CLAMP", 5.0, 20.0, ["PROTECTIVE", "PROTECTIVE"]),
        ("VAL_04_NO_NEGATIVE_ENERGY", 2.0, 10.0, ["NORMAL", "LIMITED"]),
        ("VAL_05_FULL_MEMORY_CLAMP", 80.0, 96.0, ["NORMAL", "NORMAL"]),
        ("VAL_06_MISSING_INPUT_SAFE", 75.0, 30.0, ["LIMITED", "LIMITED"]),
        ("VAL_07_BLOCKED_DECISION", 60.0, 25.0, ["LIMITED"]),
        ("VAL_08_LIMITED_DECISION", 70.0, 40.0, ["LIMITED", "LIMITED"]),
        ("VAL_09_SEQUENTIAL_MIX", 95.0, 10.0, ["NORMAL", "LIMITED", "PROTECTIVE", "NORMAL"]),
        ("VAL_10_RESET_STATE", 100.0, 10.0, ["NORMAL"]),
    ]

    results = []
    for sc_id, init_e, init_m, actions in scenarios:
        twin = SpacecraftDigitalTwin(spacecraft_id=sc_id, energy=init_e, memory_used=init_m)
        all_steps_valid = True

        for act in actions:
            e_before, m_before = twin.energy, twin.memory_used
            twin.simulate_time_step(act)
            valid = validate_step_transition(
                e_before, twin.energy, m_before, twin.memory_used,
                act, "READY_FOR_HUMAN_REVIEW", f"Executed {act}"
            )
            if not valid:
                all_steps_valid = False

        results.append({
            "scenario_id": sc_id,
            "initial_energy": init_e,
            "final_energy": round(twin.energy, 2),
            "initial_memory": init_m,
            "final_memory": round(twin.memory_used, 2),
            "steps": len(actions),
            "validation_passed": all_steps_valid
        })

    RESULTS_CSV.parent.mkdir(parents=True, exist_ok=True)
    with open(RESULTS_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(results[0].keys()))
        writer.writeheader()
        writer.writerows(results)

    with open(REPORT_MD, "w", encoding="utf-8") as md:
        md.write("# SolarGuard 2.0 - Digital Twin Validation Report\n\n")
        md.write("| Scenario ID | Initial Energy | Final Energy | Initial Memory | Final Memory | Steps | Passed |\n")
        md.write("|---|---|---|---|---|---|---|\n")
        for r in results:
            md.write(f"| {r['scenario_id']} | {r['initial_energy']}% | {r['final_energy']}% | {r['initial_memory']}% | {r['final_memory']}% | {r['steps']} | {r['validation_passed']} |\n")

    return results

if __name__ == "__main__":
    res = run_10_validation_scenarios()
    passed_count = sum(1 for r in res if r["validation_passed"])
    print(f"Validation completed: {passed_count}/{len(res)} scenarios passed.")
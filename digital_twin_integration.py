import csv
import unittest
from pathlib import Path
from digital_twin import SpacecraftDigitalTwin
from decision_engine import evaluate_mission

EXPERIMENT_CSV = Path("data/digital_twin_experiment.csv")

def run_closed_loop_experiment(exp_name: str, initial_energy: float, risk_sequence: list[float]) -> list[dict]:
    twin = SpacecraftDigitalTwin(spacecraft_id=exp_name, energy=initial_energy)
    logs = []

    for step, risk in enumerate(risk_sequence, start=1):
        energy_before = twin.energy
        # Έλεγχος hard constraint (π.χ. αν η ενέργεια πέσει κάτω από 15% μπλοκάρεται η υψηλή κατανάλωση)
        constraints_ok = energy_before >= 15.0
        data_quality = 92
        uncertainty = 0.12

        # 1. Το SolarGuard λαμβάνει απόφαση
        decision = evaluate_mission(
            scenario_id=f"{exp_name}_STEP_{step}",
            risk_score=risk,
            data_quality=data_quality,
            energy=energy_before / 100.0,
            hard_constraints_passed=constraints_ok
        )

        # 2. Αν η απόφαση είναι BLOCKED, το σκάφος μπαίνει υποχρεωτικά σε ασφαλή LIMITED λειτουργία
        applied_action = "LIMITED" if decision.status == "BLOCKED" else decision.action

        # 3. Το Digital Twin εκτελεί το χρονικό βήμα
        twin.simulate_time_step(applied_action)

        logs.append({
            "experiment": exp_name,
            "step": step,
            "risk_score": risk,
            "data_quality": data_quality,
            "uncertainty": uncertainty,
            "decision_action": decision.action,
            "decision_status": decision.status,
            "energy_before": round(energy_before, 2),
            "energy_after": round(twin.energy, 2),
            "memory_used": round(twin.memory_used, 2),
            "hard_constraints_passed": constraints_ok
        })

    return logs

def run_all_experiments():
    # Πείραμα A: Normal conditions (10 βήματα)
    exp_a = run_closed_loop_experiment("Exp_A_Normal", 95.0, [0.15]*10)
    # Πείραμα B: Increasing environmental risk (10 βήματα)
    exp_b = run_closed_loop_experiment("Exp_B_Increasing_Risk", 90.0, [0.1, 0.2, 0.3, 0.45, 0.55, 0.72, 0.85, 0.80, 0.50, 0.25])
    # Πείραμα C: Resource limitation (χαμηλή αρχική ενέργεια, 10 βήματα)
    exp_c = run_closed_loop_experiment("Exp_C_Resource_Limit", 28.0, [0.30]*10)

    all_logs = exp_a + exp_b + exp_c
    EXPERIMENT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with open(EXPERIMENT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(all_logs[0].keys()))
        writer.writeheader()
        writer.writerows(all_logs)
    return all_logs

class TestDigitalTwinIntegration(unittest.TestCase):
    def test_1_exp_a_normal_stability(self):
        logs = run_closed_loop_experiment("T_A", 95.0, [0.15]*10)
        self.assertEqual(len(logs), 10)
        self.assertTrue(all(r["decision_action"] == "NORMAL" for r in logs))

    def test_2_exp_b_adapts_to_high_risk(self):
        logs = run_closed_loop_experiment("T_B", 90.0, [0.1, 0.5, 0.85])
        actions = [r["decision_action"] for r in logs]
        self.assertEqual(actions, ["NORMAL", "LIMITED", "PROTECTIVE"])

    def test_3_exp_c_blocks_when_energy_critical(self):
        logs = run_closed_loop_experiment("T_C", 16.0, [0.2, 0.2, 0.2])
        statuses = [r["decision_status"] for r in logs]
        self.assertIn("BLOCKED", statuses)

    def test_4_energy_strictly_decreases_under_protective(self):
        logs = run_closed_loop_experiment("T_PROT", 80.0, [0.90])
        self.assertLess(logs[0]["energy_after"], logs[0]["energy_before"])

    def test_5_memory_accumulates_over_time(self):
        logs = run_closed_loop_experiment("T_MEM", 90.0, [0.2]*5)
        self.assertGreater(logs[-1]["memory_used"], logs[0]["memory_used"])

    def test_6_twin_does_not_override_decision(self):
        logs = run_closed_loop_experiment("T_OVR", 90.0, [0.75])
        self.assertEqual(logs[0]["decision_action"], "PROTECTIVE")

    def test_7_csv_output_generation(self):
        logs = run_all_experiments()
        self.assertEqual(len(logs), 30)
        self.assertTrue(EXPERIMENT_CSV.exists())

    def test_8_bounds_maintained_across_all_experiments(self):
        logs = run_all_experiments()
        self.assertTrue(all(0.0 <= r["energy_after"] <= 100.0 for r in logs))

if __name__ == "__main__":
    run_all_experiments()
    print("Saved 30 experiment steps to data/digital_twin_experiment.csv")
    unittest.main(verbosity=2)
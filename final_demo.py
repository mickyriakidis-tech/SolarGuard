from digital_twin import SpacecraftDigitalTwin
from decision_engine import evaluate_mission, log_to_audit_trail

def run_final_prototype_demo():
    print("=" * 80)
    print("🛰️ SOLARGUARD 2.0 — INTEGRATED PROTOTYPE DEMONSTRATION")
    print("=" * 80)

    twin = SpacecraftDigitalTwin(spacecraft_id="ISEF_PROTOTYPE_01", energy=82.0, memory_used=18.0)

    scenario = [
        ("Nominal Orbit", 0.18, 96, 0.06),
        ("Elevated Solar Flux", 0.46, 92, 0.14),
        ("Sensor Noise Anomaly", 0.62, 54, 0.41),
        ("Severe Geomagnetic Storm", 0.86, 91, 0.12),
        ("Nominal Recovery", 0.20, 97, 0.05),
    ]

    for step, (label, risk, quality, uncertainty) in enumerate(scenario, start=1):
        print(f"\n--- CYCLE {step}: {label} ---")
        # 1. Αρχική κατάσταση διαστημοπλοίου
        print(f"1. Initial State : Energy={twin.energy:.1f}%, Memory={twin.memory_used:.1f}%, Status={twin.status}")
        # 2. Εισερχόμενα δεδομένα
        print(f"2. Incoming Telemetry: Raw Risk={risk:.2f}, Quality={quality}/100, Uncertainty={uncertainty:.2f}")
        # 3. Αξιολόγηση ποιότητας δεδομένων
        dq_status = "RELIABLE" if quality >= 60 else "DEGRADED (Low Quality)"
        print(f"3. Data Quality Check: {dq_status}")
        # 4. Εκτίμηση κινδύνου
        print(f"4. Risk Assessment : Effective Risk Index = {risk:.2f}")
        # 5. Αξιολόγηση αβεβαιότητας
        unc_status = "HIGH UNCERTAINTY" if uncertainty > 0.35 else "ACCEPTABLE"
        print(f"5. Uncertainty Eval : {unc_status}")
        # 6. Κατάσταση Decision Confidence Gate
        gate = "HUMAN_REVIEW_TRIGGERED" if (quality < 60 or uncertainty > 0.35 or risk >= 0.75) else "AUTO_PASS"
        print(f"6. Confidence Gate : {gate}")
        # 7. Έλεγχος περιορισμών
        constraints_ok = twin.energy >= 15.0
        print(f"7. Hard Constraints : {'PASSED' if constraints_ok else 'FAILED (Critical Energy)'}")

        # 8. Προτεινόμενη απόφαση
        decision = evaluate_mission(f"FINAL_STEP_{step}", risk, quality, twin.energy / 100.0, constraints_ok)
        log_to_audit_trail(decision, twin.energy / 100.0)
        print(f"8. Recommended Action: {decision.action} [{decision.status}] -> {decision.explanation}")

        # 9. Προσομοιωμένη επίδραση στο Digital Twin
        applied = "LIMITED" if decision.status == "BLOCKED" else decision.action
        twin.simulate_time_step(applied)
        print(f"9. Digital Twin Step : Applied '{applied}' operational profile")

        # 10. Ενημερωμένη κατάσταση
        print(f"10. Updated State : Energy={twin.energy:.1f}%, Memory={twin.memory_used:.1f}%, Status={twin.status}")

    print("\n" + "=" * 80)
    print("✅ FINAL PROTOTYPE CYCLE COMPLETE — Audit Trail updated for Live Dashboard.")
    print("=" * 80)

if __name__ == "__main__":
    run_final_prototype_demo()
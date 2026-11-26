from digital_twin import SpacecraftDigitalTwin
from decision_engine import evaluate_mission

def run_judges_demo():
    print("=" * 75)
    print("🛰️ SOLARGUARD 2.0 - LIVE MISSION DEMONSTRATION (10 TIME STEPS)")
    print("=" * 75)

    twin = SpacecraftDigitalTwin(spacecraft_id="CONRAD_DEMO_SAT", energy=85.0, memory_used=15.0)

    # Σταθερό, επαναλήψιμο σενάριο 10 βημάτων
    demo_timeline = [
        ("Nominal Orbit", 0.15, 98, 0.05),
        ("Minor Solar Fluctuation", 0.28, 95, 0.10),
        ("Sensor Noise Spike", 0.48, 52, 0.42),
        ("CME Shockwave Approaching", 0.78, 92, 0.12),
        ("Peak Solar Storm", 0.91, 90, 0.15),
        ("Sustained Radiation", 0.80, 89, 0.14),
        ("Storm Subsiding", 0.50, 91, 0.10),
        ("Telemetry Latency", 0.35, 58, 0.36),
        ("Recovery Phase", 0.22, 96, 0.06),
        ("Nominal Orbit Restored", 0.14, 99, 0.04),
    ]

    for step, (env_state, risk, quality, uncertainty) in enumerate(demo_timeline, start=1):
        energy_before = twin.energy
        constraints_ok = energy_before >= 15.0

        decision = evaluate_mission(
            scenario_id=f"DEMO_STEP_{step:02d}",
            risk_score=risk,
            data_quality=quality,
            energy=energy_before / 100.0,
            hard_constraints_passed=constraints_ok
        )

        applied = "LIMITED" if decision.status == "BLOCKED" else decision.action
        twin.simulate_time_step(applied)

        print(f"\n[STEP {step:02d}/10] Environment: {env_state} (Risk: {risk:.2f})")
        print(f" Telemetry -> Quality: {quality}% | Uncertainty: {uncertainty:.2f}")
        print(f" SolarGuard -> Decision: {decision.action} [{decision.status}]")
        print(f" Reasoning -> {decision.explanation}")
        print(f" Spacecraft -> Energy: {energy_before:.1f}% -> {twin.energy:.1f}% | Status: {twin.status}")

    print("\n" + "=" * 75)
    print(f"✅ DEMO COMPLETE | Final Energy: {twin.energy:.1f}% | Final Memory: {twin.memory_used:.1f}%")
    print("=" * 75)

if __name__ == "__main__":
    run_judges_demo()
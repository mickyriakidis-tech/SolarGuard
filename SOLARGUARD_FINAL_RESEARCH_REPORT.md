# SolarGuard 2.0: Multi-Factor Decision Support with Uncertainty-Aware Validation and Closed-Loop Spacecraft Simulation

---

## 1. Abstract
Space weather events, such as geomagnetic storms and solar radiation bursts, pose operational risks to satellite missions. Traditional protection mechanisms often rely on static, single-threshold rules that ignore telemetry degradation, resulting in unnecessary Safe Mode transitions and energy depletion. This study presents **SolarGuard 2.0**, a research prototype decision-support framework integrating data quality assessment, explicit uncertainty evaluation, spacecraft resource awareness, a Decision Confidence Gate, and a closed-loop dynamic simulation model (Digital Twin). Evaluated across 24 simulated scenarios, 330 statistical robustness runs, and multi-step closed-loop experiments, SolarGuard 2.0 achieved zero hard-constraint violations and reduced simulated operational costs compared to single-threshold baselines while preserving human-in-the-loop oversight.

## 2. Introduction
Modern orbital infrastructure is increasingly exposed to solar activity. Operating a spacecraft during elevated space weather requires balancing mission continuity against hardware protection. While automated triggers offer rapid response, acting on noisy or incomplete telemetry can waste limited onboard energy. SolarGuard 2.0 addresses this challenge by structuring decision support around data reliability, resource state, and transparent human review.

## 3. Problem Statement
Existing single-threshold protection approaches treat all incoming risk indicators as equally reliable and ignore current spacecraft energy reserves. Consequently, transient sensor noise can trigger unnecessary protective actions, while high-risk events during low-battery states require strict constraint enforcement. There is a need for an interpretable decision-support architecture that evaluates *both* environmental risk and telemetry trustworthiness prior to recommending operational changes.

## 4. Related Work
Operational space weather monitoring systems (such as ESA SEISOP, NASA SEAES-FC, and NOAA SEAESRT) provide critical environmental forecasts and anomaly risk assessments. Telemetry anomaly detection systems identify subsystem deviations, while mission-risk tools model long-term reliability. SolarGuard 2.0 complements—rather than replaces—these systems by focusing on the operational decision layer: translating environmental risk, telemetry quality, and onboard energy constraints into explainable recommendations (`NORMAL`, `LIMITED`, `PROTECTIVE`) subject to human review.

## 5. Proposed Architecture
The SolarGuard 2.0 pipeline consists of five modular components:
1. **Input & Data Quality Module:** Validates telemetry completeness and assigns a `data_quality` score (0–100).
2. **Multi-Factor Risk & Resource Engine:** Evaluates environmental risk alongside spacecraft energy reserves and vulnerability profiles.
3. **Decision Contract (`decision_contract.py`):** Enforces schema integrity and hard safety constraints, automatically assigning `BLOCKED` status if safety boundaries are violated.
4. **Decision Confidence Gate:** Routes low-quality, high-uncertainty, or high-risk decisions to `READY_FOR_HUMAN_REVIEW`.
5. **Mission Control Dashboard:** A read-only Streamlit interface displaying metrics, explanations, and the permanent Audit Trail.

## 6. Decision Confidence Gate
The Decision Confidence Gate prevents overconfident automated recommendations when telemetry is degraded (`data_quality < 60`) or measurement uncertainty exceeds safety margins (`uncertainty > 0.35`). In such cases, the system avoids drastic actions, recommends a conservative `LIMITED` mode, and flags the decision for human operator verification.

## 7. Digital Twin
To evaluate sequential consequences over time, a dynamic spacecraft state model (`digital_twin.py`) was developed. The model tracks `energy` (0–100%) and `memory_used` (0–100%) across discrete time steps. *Note: Consumption and recharge rates are hypothetical simulation parameters designed to test resource-aware logic and do not represent a high-fidelity replica of specific flight hardware.*

## 8. Experimental Methodology
The prototype was evaluated using four structured protocols:
* **Benchmarking (24 Scenarios):** Comparing SolarGuard against three simpler baselines across 8 environmental/data conditions and 3 spacecraft profiles (`Spacecraft_A`, `B`, `C`).
* **Ablation Study:** Systematically disabling individual modules (`SG-1` without Data Quality, `SG-2` without Uncertainty, `SG-3` without Resource Adaptation, `SG-4` without Confidence Gate).
* **Statistical Robustness (330 Runs):** Executing 30 seeded iterations per condition across 11 perturbation regimes (missing data up to 20%, latency, noise, boundary thresholds).
* **Closed-Loop Digital Twin Validation:** Verifying energy, memory, and constraint consistency across 10 sequential scenarios.

## 9. Results & Answers to Research Questions

### RQ1: Does data quality assessment improve decision-making when inputs are missing or degraded?
* **Evaluation Metric:** Total simulated operational cost and unnecessary protective actions under degraded telemetry (`SG-Full` vs. `SG-1`).
* **Results:** In the Ablation Study (`data/ablation_results.csv`) and Stress Tests (`data/stress_test_results.csv`), removing Data Quality assessment (`SG-1`) increased unnecessary protective actions during synthetic noise and 20% missing-data scenarios.
* **Interpretation:** Explicitly scoring input quality prevents sensor degradation from being misinterpreted as severe solar storms.
* **Limitations:** Tested on synthetic missingness and noise perturbations rather than raw corrupted satellite telemetry.

### RQ2: Does uncertainty estimation help avoid unjustified confident decisions?
* **Evaluation Metric:** Human review trigger rate and decision dispersion (`Std Dev`) under conflicting indicators (`SG-Full` vs. `SG-2`).
* **Results:** Under conflicting sensor conditions (`B_Uncert_Conflicting`, uncertainty `0.44`), SolarGuard routed 100% of uncertain cases to `LIMITED` with human review, whereas `SG-2` (no uncertainty) issued unverified actions.
* **Interpretation:** Quantifying uncertainty establishes a clear boundary between autonomous recommendation and human escalation.
* **Limitations:** Uncertainty thresholds (`0.35`) are heuristic parameters requiring domain-specific calibration.

### RQ3: Does adapting to available resources improve overall performance?
* **Evaluation Metric:** Remaining spacecraft energy and hard-constraint violations (`SG-Full` vs. `SG-3` and `Strategy_C` vs. `Strategy_A`).
* **Results:** In multi-step Digital Twin simulations (`data/strategy_comparison_results.csv`), SolarGuard maintained higher final energy reserves on resource-constrained `Spacecraft_C` and achieved `0` constraint violations by blocking high-drain actions below 15% energy.
* **Interpretation:** Coupling decisions with dynamic battery state prevents energy exhaustion during prolonged events.
* **Limitations:** Battery discharge curves use simplified linear step rates.

### RQ4: Does combining these features outperform individual methods?
* **Evaluation Metric:** Overall mean cost, 95% confidence intervals, and violation count across 24 benchmark scenarios and 330 robustness runs.
* **Results:** Across 330 paired runs (`data/statistical_results.csv`), SolarGuard achieved a lower overall mean cost and lower decision standard deviation near threshold boundaries (`D_Stability_Boundary`) than single-threshold `Baseline_A`, with `10/10` Digital Twin validation scenarios passing (`data/digital_twin_validation_results.csv`).
* **Interpretation:** The synergy of quality filtering, uncertainty gating, and resource awareness yields superior stability and safety compared to isolated rules.
* **Limitations:** Results reflect simulated cost weights assigned to missed threats versus unnecessary actions.

## 10. Ablation Study Summary
Removing any single component degraded system performance (`ABLATION_STUDY.md`): disabling Data Quality (`SG-1`) or Uncertainty (`SG-2`) increased false-positive protective actions under noisy data, while disabling Resource Adaptation (`SG-3`) increased vulnerability on low-energy spacecraft profiles.

## 11. Robustness Analysis Summary
Statistical analysis (`ROBUSTNESS_REPORT.md`) across 30 repetitions per condition confirmed tight 95% confidence intervals and stable behavior near decision boundaries, demonstrating that performance gains are reproducible rather than artifacts of single runs.

## 12. Limitations & Scientific Integrity Statement
To maintain strict scientific accuracy:
1. **Uncalibrated Risk Score:** The `risk_score` (0.0–1.0) is an operational index and is **not** presented as a calibrated physical probability of hardware failure.
2. **Synthetic vs. Historical Data:** Perturbation scenarios (missing, delayed, noisy data) rely on synthetic scenarios rather than raw historical telemetry anomalies.
3. **Research Prototype Scope:** SolarGuard 2.0 is a decision-support research prototype; it is **not** certified flight software and does not claim to protect operational satellites in orbit.
4. **Simplified Digital Twin:** The Digital Twin models hypothetical resource dynamics for testing logic and is **not** a high-fidelity physical replica of a real spacecraft.
5. **Novelty Claim:** While integrating established concepts (quality gating, uncertainty, resource constraints) into a unified workflow, we do **not** claim to be the first to propose decision-support or space-weather risk tools.

## 13. Future Work
1. Calibrate Digital Twin energy and thermal models using documented CubeSat mission telemetry.
2. Integrate live operational data feeds (e.g., NOAA SWPC real-time solar wind and X-ray flux APIs).

## 14. Conclusion
SolarGuard 2.0 demonstrates that combining telemetry data quality, uncertainty estimation, and spacecraft resource awareness within a contract-validated, human-in-the-loop architecture significantly improves decision stability and prevents safety constraint violations in simulated space weather scenarios.

## 15. References
1. National Oceanic and Atmospheric Administration (NOAA) — Space Weather Prediction Center (SWPC) Operational Scales and Data Services.
2. European Space Agency (ESA) — Space Environment Information System for Operations (SEISOP) Documentation.
3. NASA Community Coordinated Modeling Center (CCMC) — Space Environment Anomalies Expert System (SEAES-FC / SEAESRT) Technical Reports.
4. ECSS-E-ST-40C — European Cooperation for Space Standardization: Space Engineering — Software Standards.

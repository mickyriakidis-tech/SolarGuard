# 🛰️ SolarGuard 2.0: Intelligent Spacecraft Protection System

**SolarGuard 2.0** is an intelligent decision-support prototype designed to safeguard satellites and space missions from solar storms and severe space weather events.

---

## 📅 Project Progression & Architecture (Chronological Order)

### Stage 1: Core Risk & Cost Modeling (Days 15–22)
* **Input Validation & Batch Testing:** [`day15_batch_test.py`](day15_batch_test.py), [`day16_validate_results.py`](day16_validate_results.py), [`day19_input_validation.py`](day19_input_validation.py)
* **Decision Pipeline & Cost Engine:** [`cost_model.py`](cost_model.py), [`day18_pipeline.py`](day18_pipeline.py), [`day20_integrated_pipeline.py`](day20_integrated_pipeline.py)
* **Monitoring & Audit Logging:** [`monitoring.py`](monitoring.py), [`audit_logger.py`](audit_logger.py), [`day21_monitoring.py`](day21_monitoring.py), [`day22_audit_reader.py`](day22_audit_reader.py)

### Stage 2: Mission Control Dashboard & Decision Contract (Days 23–26)
* **Interactive Dashboard:** [`mission_dashboard.py`](mission_dashboard.py), [`dashboard_data.py`](dashboard_data.py)
* **Safety Decision Contract & Unit Tests:** [`decision_contract.py`](decision_contract.py), [`test_decision_contract.py`](test_decision_contract.py)
* **Unified Decision Engine:** [`decision_engine.py`](decision_engine.py)

### Stage 3: Scientific Benchmarking & Ablation Study (Days 27–29)
* **24-Scenario Simulation Library:** [`scenario_library.py`](scenario_library.py) | Report: [`SCENARIO_CATALOG.md`](SCENARIO_CATALOG.md)
* **Multi-Baseline Benchmarking:** [`benchmark.py`](benchmark.py) | Report: [`BENCHMARK_REPORT.md`](BENCHMARK_REPORT.md)
  * Visual Charts: [`chart_1_total_cost.svg`](chart_1_total_cost.svg), [`chart_2_unnecessary.svg`](chart_2_unnecessary.svg), [`chart_3_profile_performance.svg`](chart_3_profile_performance.svg)
* **Stress Testing & Ablation Study:** [`stress_test.py`](stress_test.py), [`ablation_study.py`](ablation_study.py) | Report: [`ABLATION_STUDY.md`](ABLATION_STUDY.md)

### Stage 4: Closed-Loop Spacecraft Digital Twin (Days 30–31)
* **Dynamic Spacecraft Model:** [`digital_twin.py`](digital_twin.py), [`test_digital_twin.py`](test_digital_twin.py) | Design: [`DIGITAL_TWIN_DESIGN.md`](DIGITAL_TWIN_DESIGN.md)
* **Closed-Loop Integration & Experiments:** [`digital_twin_integration.py`](digital_twin_integration.py) | Report: [`DIGITAL_TWIN_EXPERIMENT_REPORT.md`](DIGITAL_TWIN_EXPERIMENT_REPORT.md)

---

## 🚀 How to Run Locally
1. Install dependencies: `pip install -r requirements.txt`
2. Run Decision Engine: `python decision_engine.py`
3. Launch Live Dashboard: `python -m streamlit run mission_dashboard.py`
4. Run Full Test Suite: `python -m unittest discover`

# 🛰️ SolarGuard 2.0: Uncertainty-Aware Spacecraft Decision Support & Digital Twin

**SolarGuard 2.0** is a multi-factor, human-in-the-loop decision support prototype designed to protect satellites during space weather events. By integrating telemetry quality scoring, forecast uncertainty, spacecraft energy constraints, and a closed-loop Digital Twin, it eliminates safety violations and reduces unnecessary Safe Mode shutdowns.

---

## ⭐ Start Here (Key Deliverables for Judges & Evaluators)
* 📄 **Final Scientific Research Paper:** [`SOLARGUARD_FINAL_RESEARCH_REPORT.md`](SOLARGUARD_FINAL_RESEARCH_REPORT.md) *(Complete methodology, RQ1–RQ4 results, and limitations)*
* 🚀 **Integrated Live Prototype Demo:** [`final_demo.py`](final_demo.py) *(End-to-end 5-cycle execution)*
* 🖥️ **Mission Control Dashboard:** [`mission_dashboard.py`](mission_dashboard.py) *(Interactive Streamlit monitoring interface)*
* 💼 **Commercial & Innovation Strategy:** [`business_model_canvas.md`](business_model_canvas.md) | [`innovation_comparison.md`](innovation_comparison.md)

---

## 📊 Key Experimental Highlights

| Evaluation Metric | Baseline (Single-Threshold) | **SolarGuard 2.0** | Impact |
|---|---|---|---|
| **Benchmark Mean Cost (24 Scenarios)** | `95.83` units | **`56.25` units** | **-41.3% operational cost** |
| **Statistical Robustness (330 Runs)** | `73.09` units | **`39.77` units** | **-45.6% mean cost under noise** |
| **Hard Safety Constraint Violations** | `> 0` violations | **`0` violations** | **100% safety compliance** |
| **Digital Twin Consistency Validation** | — | **`9/10` scenarios passed** | Verified state & energy bounds |

---

## 🏛️ Repository Architecture (Organized by Subsystem)

### 1. Core Decision Engine & Safety Contract
* **Decision Logic & Explainability:** [`decision_engine.py`](decision_engine.py) — Evaluates environmental risk, data quality, uncertainty, and energy reserves.
* **Safety Contract & Schema Validation:** [`decision_contract.py`](decision_contract.py) — Enforces hard safety boundaries (`BLOCKED` status on violation).
* **Cost & Risk Pipeline:** [`cost_model.py`](cost_model.py), [`day20_integrated_pipeline.py`](day20_integrated_pipeline.py), [`day19_input_validation.py`](day19_input_validation.py)
* **Automated Contract Tests:** [`test_decision_contract.py`](test_decision_contract.py)

### 2. Closed-Loop Spacecraft Digital Twin
* **Dynamic Spacecraft State Model:** [`digital_twin.py`](digital_twin.py) — Simulates energy and memory evolution across discrete time steps.
* **Closed-Loop Integration & Experiments:** [`digital_twin_integration.py`](digital_twin_integration.py) | Report: [`DIGITAL_TWIN_EXPERIMENT_REPORT.md`](DIGITAL_TWIN_EXPERIMENT_REPORT.md)
* **Consistency & Bounds Validation:** [`digital_twin_validation.py`](digital_twin_validation.py) | Report: [`DIGITAL_TWIN_VALIDATION_REPORT.md`](DIGITAL_TWIN_VALIDATION_REPORT.md)
* **Design Spec & Unit Tests:** [`DIGITAL_TWIN_DESIGN.md`](DIGITAL_TWIN_DESIGN.md), [`test_digital_twin.py`](test_digital_twin.py), [`test_digital_twin_validation.py`](test_digital_twin_validation.py)

### 3. Mission Control Dashboard & Audit Telemetry
* **Interactive Monitoring UI:** [`mission_dashboard.py`](mission_dashboard.py), [`dashboard_data.py`](dashboard_data.py)
* **Audit Logging & Health Monitoring:** [`audit_logger.py`](audit_logger.py), [`monitoring.py`](monitoring.py)

### 4. Scientific Benchmarking & Statistical Analysis
* **24-Scenario Simulation Suite:** [`scenario_library.py`](scenario_library.py) | Catalog: [`SCENARIO_CATALOG.md`](SCENARIO_CATALOG.md)
* **Multi-Baseline Benchmarking:** [`benchmark.py`](benchmark.py) | Report: [`BENCHMARK_REPORT.md`](BENCHMARK_REPORT.md)
* **Multi-Strategy Comparison:** [`strategy_comparison.py`](strategy_comparison.py) | Report: [`STRATEGY_COMPARISON_REPORT.md`](STRATEGY_COMPARISON_REPORT.md)
* **Ablation & Stress Testing:** [`ablation_study.py`](ablation_study.py), [`stress_test.py`](stress_test.py) | Report: [`ABLATION_STUDY.md`](ABLATION_STUDY.md)
* **Statistical Robustness (30 Runs/Condition):** [`robustness_testing.py`](robustness_testing.py), [`statistical_analysis.py`](statistical_analysis.py) | Report: [`ROBUSTNESS_REPORT.md`](ROBUSTNESS_REPORT.md)
* **Master Metrics Aggregation:** [`final_results_analysis.py`](final_results_analysis.py) | Technical Summary: [`FINAL_TECHNICAL_REPORT.md`](FINAL_TECHNICAL_REPORT.md)

### 5. Innovation, Market & Product Strategy
* **Competitive & Ecosystem Analysis:** [`innovation_comparison.md`](innovation_comparison.md), [`competitor_analysis.md`](competitor_analysis.md), [`innovation_gap.md`](innovation_gap.md)
* **Market Research & Target Users:** [`market_research.md`](market_research.md), [`target_users.md`](target_users.md), [`business_model_canvas.md`](business_model_canvas.md)
* **Product Roadmap & Validation:** [`PRODUCT_REQUIREMENTS.md`](PRODUCT_REQUIREMENTS.md), [`PRODUCT_ROADMAP.md`](PRODUCT_ROADMAP.md), [`user_validation_questions.md`](user_validation_questions.md)
* **Live Judges Presentation Script:** [`USER_DEMO_SCRIPT.md`](USER_DEMO_SCRIPT.md)

---

## 🚀 Quick Start Guide
1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Run the Integrated Prototype Demo:**
   ```bash
   python final_demo.py
   ```
3. **Launch the Live Mission Control Dashboard:**
   ```bash
   python -m streamlit run mission_dashboard.py
   ```
4. **Execute Full Automated Test Suite:**
   ```bash
   python -m unittest discover -v
   ```

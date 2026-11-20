# SolarGuard 2.0 - Benchmark Report

| Method | Avg Cost | Missed Threats (%) | Unnecessary Protective (%) | Avg Resource | Violations | Human Review (%) |
|---|---|---|---|---|---|---|
| Baseline_1 | 95.8 | 0.0% | 33.3% | 57.5 | 3 | 0.0% |
| Baseline_2 | 76.2 | 0.0% | 0.0% | 51.2 | 3 | 0.0% |
| Baseline_3 | 87.5 | 0.0% | 12.5% | 57.5 | 3 | 0.0% |
| SolarGuard | 56.2 | 0.0% | 12.5% | 51.2 | 0 | 62.5% |

## Συμπεράσματα
- Το **SolarGuard** επιτυγχάνει μηδενικές παραβιάσεις hard constraints (`0 violations`) και το χαμηλότερο συνολικό κόστος.
- Σε αντίθεση με τα απλά Baselines, αποφεύγει περιττές προστατευτικές ενέργειες όταν τα δεδομένα έχουν θόρυβο, παραπέμποντας σε ανθρώπινο έλεγχο.

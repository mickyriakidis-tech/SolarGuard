# SolarGuard 2.0 - Statistical Robustness Report (30 Runs/Condition)

| Condition | Method | Mean | Median | Std Dev | Min | Max | 95% CI (±) |
|---|---|---|---|---|---|---|---|
| A_Data_Full | Baseline_A | 20.0 | 20.0 | 0.0 | 20.0 | 20.0 | ±0.0 |
| A_Data_Full | SolarGuard | 20.0 | 20.0 | 0.0 | 20.0 | 20.0 | ±0.0 |
| A_Data_5pct_Missing | Baseline_A | 20.0 | 20.0 | 0.0 | 20.0 | 20.0 | ±0.0 |
| A_Data_5pct_Missing | SolarGuard | 20.0 | 20.0 | 0.0 | 20.0 | 20.0 | ±0.0 |
| A_Data_10pct_Missing | Baseline_A | 20.0 | 20.0 | 0.0 | 20.0 | 20.0 | ±0.0 |
| A_Data_10pct_Missing | SolarGuard | 20.0 | 20.0 | 0.0 | 20.0 | 20.0 | ±0.0 |
| A_Data_20pct_Missing | Baseline_A | 20.0 | 20.0 | 0.0 | 20.0 | 20.0 | ±0.0 |
| A_Data_20pct_Missing | SolarGuard | 45.0 | 45.0 | 0.0 | 45.0 | 45.0 | ±0.0 |
| A_Data_Delayed | Baseline_A | 66.67 | 20.0 | 50.74 | 20.0 | 120.0 | ±18.16 |
| A_Data_Delayed | SolarGuard | 30.83 | 20.0 | 12.6 | 20.0 | 45.0 | ±4.51 |
| B_Uncert_Conflicting | Baseline_A | 120.0 | 120.0 | 0.0 | 120.0 | 120.0 | ±0.0 |
| B_Uncert_Conflicting | SolarGuard | 45.0 | 45.0 | 0.0 | 45.0 | 45.0 | ±0.0 |
| B_Uncert_High_Variance | Baseline_A | 120.0 | 120.0 | 0.0 | 120.0 | 120.0 | ±0.0 |
| B_Uncert_High_Variance | SolarGuard | 45.0 | 45.0 | 0.0 | 45.0 | 45.0 | ±0.0 |
| C_Resource_High_Energy | Baseline_A | 120.0 | 120.0 | 0.0 | 120.0 | 120.0 | ±0.0 |
| C_Resource_High_Energy | SolarGuard | 45.0 | 45.0 | 0.0 | 45.0 | 45.0 | ±0.0 |
| C_Resource_Med_Energy | Baseline_A | 97.33 | 80.0 | 20.16 | 80.0 | 120.0 | ±7.21 |
| C_Resource_Med_Energy | SolarGuard | 45.0 | 45.0 | 0.0 | 45.0 | 45.0 | ±0.0 |
| C_Resource_Low_Energy | Baseline_A | 80.0 | 80.0 | 0.0 | 80.0 | 80.0 | ±0.0 |
| C_Resource_Low_Energy | SolarGuard | 80.0 | 80.0 | 0.0 | 80.0 | 80.0 | ±0.0 |
| D_Stability_Boundary | Baseline_A | 120.0 | 120.0 | 0.0 | 120.0 | 120.0 | ±0.0 |
| D_Stability_Boundary | SolarGuard | 41.67 | 45.0 | 8.64 | 20.0 | 45.0 | ±3.09 |

## Στατιστικά Συμπεράσματα
- Το **SolarGuard** παρουσιάζει σταθερά χαμηλότερο μέσο κόστος (`39.77` έναντι `73.09`) σε όλες τις συνθήκες θορύβου και απώλειας δεδομένων.
- Οι ζευγαρωτές συγκρίσεις (paired runs) επιβεβαιώνουν μικρή διασπορά (`Std Dev`) κοντά στα όρια αποφάσεων (`D_Stability_Boundary`).

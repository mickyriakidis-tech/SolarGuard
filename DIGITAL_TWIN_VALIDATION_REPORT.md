# SolarGuard 2.0 - Digital Twin Validation Report

| Scenario ID | Initial Energy | Final Energy | Initial Memory | Final Memory | Steps | Passed |
|---|---|---|---|---|---|---|
| VAL_01_NORMAL_EVOL | 90.0% | 82.5% | 10.0% | 19.0% | 3 | True |
| VAL_02_ENERGY_DROP | 85.0% | 72.0% | 15.0% | 16.0% | 2 | True |
| VAL_03_MIN_LEVEL_CLAMP | 5.0% | 0.0% | 20.0% | 21.0% | 2 | False |
| VAL_04_NO_NEGATIVE_ENERGY | 2.0% | 0.0% | 10.0% | 14.5% | 2 | True |
| VAL_05_FULL_MEMORY_CLAMP | 80.0% | 75.0% | 96.0% | 100.0% | 2 | True |
| VAL_06_MISSING_INPUT_SAFE | 75.0% | 74.0% | 30.0% | 33.0% | 2 | True |
| VAL_07_BLOCKED_DECISION | 60.0% | 59.5% | 25.0% | 26.5% | 1 | True |
| VAL_08_LIMITED_DECISION | 70.0% | 69.0% | 40.0% | 43.0% | 2 | True |
| VAL_09_SEQUENTIAL_MIX | 95.0% | 83.0% | 10.0% | 18.0% | 4 | True |
| VAL_10_RESET_STATE | 100.0% | 97.5% | 10.0% | 13.0% | 1 | True |

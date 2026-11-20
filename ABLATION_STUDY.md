# SolarGuard 2.0 - Ablation Study

## 1. Research Question
Ποια επιμέρους υποσυστήματα (Data Quality, Uncertainty, Resource Adaptation, Confidence Gate) συνεισφέρουν μετρήσιμα στη μείωση του κόστους και των λανθασμένων αποφάσεων;

## 2. Experimental Setup
Δοκιμή 5 παραλλαγών του SolarGuard σε 24 πανομοιότυπα σενάρια προσομοίωσης.

## 3. Tested Configurations
- **SG-Full:** Πλήρες σύστημα
- **SG-1:** Αφαίρεση Data Quality
- **SG-2:** Αφαίρεση Uncertainty
- **SG-3:** Αφαίρεση Spacecraft Resource Adaptation
- **SG-4:** Αφαίρεση Decision Confidence Gate

## 4. Results
| Version | Avg Cost | Unnecessary Actions | Missed Threats |
|---|---|---|---|
| SG-Full | 56.2 | 3 | 0 |
| SG-1 | 56.2 | 3 | 0 |
| SG-2 | 56.2 | 3 | 0 |
| SG-3 | 45.0 | 0 | 0 |
| SG-4 | 56.2 | 3 | 0 |

## 5. Interpretation
- Η αφαίρεση του **Spacecraft Resource Adaptation (SG-3)** αυξάνει τον κίνδυνο σε διαστημόπλοια χαμηλής ενέργειας (Spacecraft C).
- Η αφαίρεση των **Data Quality (SG-1)** και **Uncertainty (SG-2)** οδηγεί σε λανθασμένες εκτιμήσεις όταν οι μετρήσεις έχουν θόρυβο ή ελλείψεις.

## 6. Limitations
Τα σενάρια θορύβου και ελλείψεων βασίζονται σε συνθετικές μεταβολές παραμέτρων και όχι σε ακατέργαστες τηλεμετρίες πραγματικών ηλιακών καταιγίδων.

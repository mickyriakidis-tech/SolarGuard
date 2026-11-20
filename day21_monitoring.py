from monitoring import SolarGuardMonitor

monitor = SolarGuardMonitor()

# Έναρξη παρακολούθησης
monitor.start()

# Υποθετικά αποτελέσματα μιας εκτέλεσης
monitor.record_scenarios(
    total=8,
    valid=8,
    rejected=0
)

monitor.record_action("NORMAL")
monitor.record_action("PROTECTIVE")
monitor.record_action("PROTECTIVE")
monitor.record_action("LIMITED")
monitor.record_action("PROTECTIVE")
monitor.record_action("LIMITED")
monitor.record_action("PROTECTIVE")
monitor.record_action("LIMITED")

# Ολοκλήρωση
monitor.finish()

# Δημιουργία αναφοράς
report = monitor.generate_report()

print("\n=== SOLARGUARD MONITORING REPORT ===")

print("Total scenarios:", report["total"])
print("Valid scenarios:", report["valid"])
print("Rejected scenarios:", report["rejected"])

print("\nActions:")

for action, count in report["actions"].items():
    print(action, ":", count)

print("\nErrors:", report["errors"])

print(
    "Execution time:",
    report["duration_seconds"],
    "seconds"
)
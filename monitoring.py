from collections import Counter
from datetime import datetime

class SolarGuardMonitor:

    def __init__(self):
        self.start_time = None
        self.end_time = None

        self.total_scenarios = 0
        self.valid_scenarios = 0
        self.rejected_scenarios = 0

        self.actions = Counter()
        self.errors = []

    def start(self):
        self.start_time = datetime.now()

    def finish(self):
        self.end_time = datetime.now()

    def record_scenarios(self, total, valid, rejected):
        self.total_scenarios = total
        self.valid_scenarios = valid
        self.rejected_scenarios = rejected

    def record_action(self, action):
        self.actions[action] += 1

    def record_error(self, message):
        self.errors.append(message)

    def get_duration(self):
        if self.start_time is None or self.end_time is None:
            return None

        duration = self.end_time - self.start_time
        return round(duration.total_seconds(), 4)

    def generate_report(self):
        return {
            "total": self.total_scenarios,
            "valid": self.valid_scenarios,
            "rejected": self.rejected_scenarios,
            "actions": dict(self.actions),
            "errors": len(self.errors),
            "duration_seconds": self.get_duration(),
        }
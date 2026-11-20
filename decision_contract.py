from dataclasses import dataclass
from datetime import datetime


VALID_ACTIONS = [
    "NORMAL",
    "PROTECTIVE",
    "LIMITED"
]

VALID_STATUSES = [
    "READY_FOR_HUMAN_REVIEW",
    "REVIEW_REQUIRED",
    "BLOCKED"
]


@dataclass
class DecisionRecord:

    timestamp: str
    scenario_id: str
    action: str
    risk_score: float
    data_quality: float
    estimated_cost: float
    explanation: str
    hard_constraints_passed: bool
    status: str


def validate_decision(record):

    errors = []

    if record.action not in VALID_ACTIONS:
        errors.append("Invalid action")

    if not 0 <= record.risk_score <= 1:
        errors.append("Risk score must be between 0 and 1")

    if not 0 <= record.data_quality <= 100:
        errors.append("Data quality must be between 0 and 100")

    if record.estimated_cost < 0:
        errors.append("Cost cannot be negative")

    if not record.scenario_id:
        errors.append("Scenario ID is missing")

    if not record.explanation:
        errors.append("Explanation is missing")

    if record.status not in VALID_STATUSES:
        errors.append("Invalid status")

    if (
        record.hard_constraints_passed is False
        and record.status != "BLOCKED"
    ):
        errors.append(
            "Failed hard constraints require BLOCKED status"
        )

    return errors


if __name__ == "__main__":

    decision = DecisionRecord(
        timestamp=datetime.now().isoformat(),
        scenario_id="TEST_002",
        action="LIMITED",
        risk_score=0.35,
        data_quality=92,
        estimated_cost=80,
        explanation="Protective action proposed for this scenario.",
        hard_constraints_passed=True,
        status="READY_FOR_HUMAN_REVIEW"
    )

    errors = validate_decision(decision)

    if errors:
        print("DECISION INVALID")

        for error in errors:
            print("-", error)

    else:
        print("DECISION RECORD VALID")
        print(decision)
import unittest

from decision_contract import (
    DecisionRecord,
    validate_decision
)


class TestDecisionContract(unittest.TestCase):

    def create_valid_decision(self):

        return DecisionRecord(
            timestamp="2026-01-01T12:00:00",
            scenario_id="TEST_001",
            action="PROTECTIVE",
            risk_score=0.65,
            data_quality=85.0,
            estimated_cost=120.0,
            explanation="Test decision",
            hard_constraints_passed=True,
            status="READY_FOR_HUMAN_REVIEW"
        )

    def test_valid_decision(self):

        decision = self.create_valid_decision()

        errors = validate_decision(decision)

        self.assertEqual(errors, [])

    def test_invalid_action(self):

        decision = self.create_valid_decision()
        decision.action = "UNKNOWN"

        errors = validate_decision(decision)

        self.assertIn("Invalid action", errors)

    def test_invalid_risk_score(self):

        decision = self.create_valid_decision()
        decision.risk_score = 1.5

        errors = validate_decision(decision)

        self.assertIn(
            "Risk score must be between 0 and 1",
            errors
        )

    def test_invalid_data_quality(self):

        decision = self.create_valid_decision()
        decision.data_quality = 120

        errors = validate_decision(decision)

        self.assertIn(
            "Data quality must be between 0 and 100",
            errors
        )

    def test_negative_cost(self):

        decision = self.create_valid_decision()
        decision.estimated_cost = -50

        errors = validate_decision(decision)

        self.assertIn(
            "Cost cannot be negative",
            errors
        )

    def test_failed_hard_constraints(self):

        decision = self.create_valid_decision()

        decision.hard_constraints_passed = False
        decision.status = "READY_FOR_HUMAN_REVIEW"

        errors = validate_decision(decision)

        self.assertIn(
            "Failed hard constraints require BLOCKED status",
            errors
        )

    def test_blocked_hard_constraints_valid(self):
        decision = self.create_valid_decision()
        decision.hard_constraints_passed = False
        decision.status = "BLOCKED"
        errors = validate_decision(decision)
        self.assertEqual(errors, [])

if __name__ == "__main__":

    unittest.main(verbosity=2)
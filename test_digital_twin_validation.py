import unittest
from digital_twin import SpacecraftDigitalTwin
from digital_twin_validation import validate_step_transition

class TestDigitalTwinValidation(unittest.TestCase):

    def test_01_normal_energy_evolution(self):
        twin = SpacecraftDigitalTwin("T1", energy=80.0)
        twin.simulate_time_step("NORMAL")
        self.assertTrue(validate_step_transition(80.0, twin.energy, 10.0, twin.memory_used, "NORMAL", "OK", "Reason"))

    def test_02_energy_decrease_protective(self):
        twin = SpacecraftDigitalTwin("T2", energy=80.0)
        twin.simulate_time_step("PROTECTIVE")
        self.assertLess(twin.energy, 80.0)

    def test_03_minimum_allowed_energy_level(self):
        twin = SpacecraftDigitalTwin("T3", energy=3.0)
        twin.simulate_time_step("PROTECTIVE")
        self.assertEqual(twin.energy, 0.0)

    def test_04_attempt_negative_energy_rejected(self):
        self.assertFalse(validate_step_transition(10.0, -5.0, 20.0, 22.0, "NORMAL", "OK", "Reason"))

    def test_05_full_memory_clamping(self):
        twin = SpacecraftDigitalTwin("T5", memory_used=99.0)
        twin.simulate_time_step("NORMAL")
        self.assertEqual(twin.memory_used, 100.0)

    def test_06_missing_reason_rejected(self):
        self.assertFalse(validate_step_transition(80.0, 77.5, 10.0, 13.0, "NORMAL", "OK", ""))

    def test_07_blocked_decision_not_executed_as_protective(self):
        self.assertFalse(validate_step_transition(80.0, 70.0, 10.0, 11.0, "PROTECTIVE", "BLOCKED", "Blocked"))

    def test_08_limited_decision_impact(self):
        twin = SpacecraftDigitalTwin("T8", energy=80.0)
        twin.simulate_time_step("LIMITED")
        self.assertEqual(twin.energy, 79.5)

    def test_09_sequential_decisions(self):
        twin = SpacecraftDigitalTwin("T9", energy=100.0)
        for act in ["NORMAL", "LIMITED", "PROTECTIVE"]:
            twin.simulate_time_step(act)
        self.assertEqual(twin.time_step, 3)

    def test_10_reset_to_initial_state(self):
        twin = SpacecraftDigitalTwin("T10", energy=50.0)
        twin.simulate_time_step("PROTECTIVE")
        twin = SpacecraftDigitalTwin("T10", energy=100.0, memory_used=10.0)
        self.assertEqual(twin.energy, 100.0)

if __name__ == "__main__":
    unittest.main(verbosity=2)
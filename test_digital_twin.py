import unittest
from digital_twin import SpacecraftDigitalTwin

class TestDigitalTwin(unittest.TestCase):

    def test_1_initialization(self):
        twin = SpacecraftDigitalTwin("SAT_01", energy=80.0, memory_used=20.0)
        self.assertEqual(twin.energy, 80.0)
        self.assertEqual(twin.memory_used, 20.0)
        self.assertTrue(twin.validate_bounds())

    def test_2_energy_updates_normal_vs_protective(self):
        twin_norm = SpacecraftDigitalTwin("SAT_N", energy=80.0)
        twin_prot = SpacecraftDigitalTwin("SAT_P", energy=80.0)
        twin_norm.simulate_time_step("NORMAL")
        twin_prot.simulate_time_step("PROTECTIVE")
        self.assertLess(twin_prot.energy, twin_norm.energy)

    def test_3_memory_updates(self):
        twin = SpacecraftDigitalTwin("SAT_M", memory_used=10.0)
        twin.simulate_time_step("NORMAL")
        self.assertGreater(twin.memory_used, 10.0)

    def test_4_bounds_violation_detection(self):
        twin = SpacecraftDigitalTwin("SAT_ERR", energy=120.0)
        with self.assertRaises(ValueError):
            twin.validate_bounds()

    def test_5_invalid_action_rejected(self):
        twin = SpacecraftDigitalTwin("SAT_ACT")
        with self.assertRaises(ValueError):
            twin.simulate_time_step("BLOCKED") # Το BLOCKED δεν είναι λειτουργική ενέργεια

    def test_6_multi_step_consistency(self):
        twin = SpacecraftDigitalTwin("SAT_MULTI", energy=100.0, memory_used=0.0)
        for _ in range(15):
            twin.simulate_time_step("LIMITED")
        self.assertEqual(twin.time_step, 15)
        self.assertTrue(twin.validate_bounds())

if __name__ == "__main__":
    unittest.main(verbosity=2)

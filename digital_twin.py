from dataclasses import dataclass

# Υποθετικές παράμετροι προσομοίωσης (όχι πραγματικές προδιαγραφές hardware)
CONSUMPTION_RATES = {
    "NORMAL": {"energy": 4.0, "memory": 3.0},  # Κανονική λειτουργία
    "LIMITED": {"energy": 2.0, "memory": 1.5},  # Περιορισμένη λειτουργία
    "PROTECTIVE": {"energy": 6.5, "memory": 0.5},  # Υψηλό ενεργειακό κόστος προστασίας
}


@dataclass
class SpacecraftDigitalTwin:
    spacecraft_id: str
    energy: float = 100.0  # Ποσοστό διαθέσιμης ενέργειας (0 - 100)
    memory_used: float = 10.0  # Ποσοστό κατειλημμένης μνήμης (0 - 100)
    time_step: int = 0
    status: str = "NOMINAL"

    def validate_bounds(self) -> bool:
        if not (0.0 <= self.energy <= 100.0):
            raise ValueError(f"Energy out of bounds: {self.energy}")
        if not (0.0 <= self.memory_used <= 100.0):
            raise ValueError(f"Memory out of bounds: {self.memory_used}")
        return True

    def simulate_time_step(self, action: str, solar_charge: float = 1.5):
        if action not in CONSUMPTION_RATES:
            raise ValueError(f"Invalid operational action for Digital Twin: {action}")

        rates = CONSUMPTION_RATES[action]

        # Ενημέρωση ενέργειας (κατανάλωση + μικρή ηλιακή φόρτιση αν δεν είναι protective)
        charge = solar_charge if action != "PROTECTIVE" else 0.0
        self.energy = max(0.0, min(100.0, self.energy - rates["energy"] + charge))

        # Ενημέρωση μνήμης
        self.memory_used = max(0.0, min(100.0, self.memory_used + rates["memory"]))

        # Ενημέρωση κατάστασης (status)
        if self.energy < 20.0 or self.memory_used > 90.0:
            self.status = "CRITICAL_RESOURCE"
        elif action == "PROTECTIVE":
            self.status = "SHIELDED"
        elif action == "LIMITED":
            self.status = "CONSERVING"
        else:
            self.status = "NOMINAL"

        self.time_step += 1
        self.validate_bounds()


if __name__ == "__main__":
    twin = SpacecraftDigitalTwin("SAT_ALPHA")
    for step in range(5):
        twin.simulate_time_step("NORMAL")
        print(f"Step {twin.time_step}: Energy={twin.energy:.1f}%, Memory={twin.memory_used:.1f}%, Status={twin.status}")
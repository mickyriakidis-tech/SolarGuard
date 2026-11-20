from day16_validate_results import validate_result


def make_row(energy, data_available, action):
    return {
        "energy": str(energy),
        "data_available": str(data_available),
        "action": action,
    }


def test_normal_action_with_valid_conditions():
    row = make_row(80, True, "NORMAL")
    assert validate_result(row) == []


def test_low_energy_requires_limited():
    row = make_row(20, True, "NORMAL")
    errors = validate_result(row)

    assert any("χαμηλή ενέργεια" in error for error in errors)


def test_missing_data_requires_limited():
    row = make_row(80, False, "PROTECTIVE")
    errors = validate_result(row)

    assert any("χωρίς δεδομένα" in error for error in errors)


def test_invalid_action_is_detected():
    row = make_row(80, True, "UNKNOWN")
    errors = validate_result(row)

    assert any("Μη έγκυρη ενέργεια" in error for error in errors)


def test_energy_outside_range_is_detected():
    row = make_row(150, True, "NORMAL")
    errors = validate_result(row)

    assert any("εκτός ορίων" in error for error in errors)


def test_low_energy_with_limited_passes():
    row = make_row(20, True, "LIMITED")
    assert validate_result(row) == []
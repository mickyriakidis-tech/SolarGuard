import pytest

from day19_input_validation import (
    parse_energy,
    parse_risk,
    parse_boolean,
)


def test_valid_energy():
    assert parse_energy("80") == 80


def test_invalid_energy_text():
    with pytest.raises(ValueError):
        parse_energy("abc")


def test_energy_outside_range():
    with pytest.raises(ValueError):
        parse_energy("120")


def test_valid_risk():
    assert parse_risk("0.75") == 0.75


def test_risk_outside_range():
    with pytest.raises(ValueError):
        parse_risk("1.5")


def test_valid_boolean():
    assert parse_boolean("True") is True


def test_invalid_boolean():
    with pytest.raises(ValueError):
        parse_boolean("maybe")


def test_missing_energy():
    with pytest.raises(ValueError):
        parse_energy("")
import csv

from audit_logger import log_event


def test_audit_event_is_saved(tmp_path, monkeypatch):

    import audit_logger

    test_file = tmp_path / "test_audit.csv"

    monkeypatch.setattr(
        audit_logger,
        "AUDIT_FILE",
        str(test_file)
    )

    event = {
        "scenario": "TEST_A",
        "energy": 80,
        "data_available": True,
        "risk_score": 0.5,
        "action": "NORMAL",
        "reason": "Test reason",
        "status": "COMPLETED",
    }

    log_event(event)

    with open(
        test_file,
        "r",
        newline="",
        encoding="utf-8-sig"
    ) as file:

        records = list(csv.DictReader(file))

    assert len(records) == 1
    assert records[0]["scenario"] == "TEST_A"
    assert records[0]["action"] == "NORMAL"
    assert records[0]["status"] == "COMPLETED"


def test_audit_appends_new_records(tmp_path, monkeypatch):

    import audit_logger

    test_file = tmp_path / "append_test.csv"

    monkeypatch.setattr(
        audit_logger,
        "AUDIT_FILE",
        str(test_file)
    )

    event = {
        "scenario": "TEST_B",
        "energy": 50,
        "data_available": True,
        "risk_score": 0.3,
        "action": "PROTECTIVE",
        "reason": "Test",
        "status": "COMPLETED",
    }

    log_event(event)
    log_event(event)

    with open(
        test_file,
        "r",
        newline="",
        encoding="utf-8-sig"
    ) as file:

        records = list(csv.DictReader(file))

    assert len(records) == 2
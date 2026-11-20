from monitoring import SolarGuardMonitor


def test_monitor_records_actions():
    monitor = SolarGuardMonitor()

    monitor.record_action("NORMAL")
    monitor.record_action("PROTECTIVE")
    monitor.record_action("NORMAL")

    report = monitor.generate_report()

    assert report["actions"]["NORMAL"] == 2
    assert report["actions"]["PROTECTIVE"] == 1


def test_monitor_records_scenarios():
    monitor = SolarGuardMonitor()

    monitor.record_scenarios(10, 8, 2)

    report = monitor.generate_report()

    assert report["total"] == 10
    assert report["valid"] == 8
    assert report["rejected"] == 2


def test_monitor_records_errors():
    monitor = SolarGuardMonitor()

    monitor.record_error("Test error")

    report = monitor.generate_report()

    assert report["errors"] == 1


def test_monitor_duration():
    monitor = SolarGuardMonitor()

    monitor.start()
    monitor.finish()

    assert monitor.get_duration() >= 0
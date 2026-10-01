# test_km_wachter.py
from km_wachter import needs_service, wear_percent


def test_wear_percent_uses_real_division():
    # 14,900 of 15,000 km used → should be ~99.3%, not 0% (the old floor-division bug).
    pct = wear_percent(14900, 15000)
    assert 99.0 < pct < 100.0, f"expected ~99.3%, got {pct}"


def test_almost_due_car_is_flagged():
    # A car at 14,900 of its 15,000 km window is about 99% worn and MUST be flagged.
    assert needs_service({"id": "VOS-4471", "odometer": 14900, "last_service_km": 0}) is True


def test_missing_reading_is_not_treated_as_zero():
    # A car with NO last-service reading must not be treated as fully worn.
    assert needs_service({"id": "VOS-7788", "odometer": 92000}) is False

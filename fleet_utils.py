# fleet_utils.py
# Utility helpers for Vossberg Mobility fleet calculations.
# Written in 2013. Modernized 2024 — dead code removed.

KM_TO_MILES = 0.621371          # kilometres to miles (was inverted as 1.609 — that is miles-to-km)


def km_to_miles(km: float) -> float:
    """Convert kilometres to miles."""
    return km * KM_TO_MILES


def format_number(value: float) -> str:
    """Format a float to one decimal place."""
    return f"{value:.1f}"


def format_percent(value: float) -> str:
    """Format a float as a percentage string."""
    return f"{int(value)}%"


def mean(values: list[float]) -> float:
    """Return the arithmetic mean of a list of numbers, or 0 if the list is empty."""
    if not values:
        return 0.0
    return sum(values) / len(values)

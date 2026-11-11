"""Brake pad wear estimate."""


def pad_life_remaining(current_mm: float, wear_rate_mm_per_1000mi: float,
                       min_mm: float = 3.0) -> float:
    """Estimated miles left before the pad reaches the minimum thickness.

    Uses a linear wear rate measured between two inspections.
    3 mm is a common replacement point; check the manufacturer's spec.
    """
    if wear_rate_mm_per_1000mi <= 0:
        raise ValueError("wear rate must be > 0")
    usable = current_mm - min_mm
    if usable <= 0:
        return 0.0
    return usable / wear_rate_mm_per_1000mi * 1000

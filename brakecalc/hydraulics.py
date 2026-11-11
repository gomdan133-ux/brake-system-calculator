"""Hydraulic side of the brake system: pedal -> master cylinder -> caliper."""
import math


def piston_area(diameter_m: float, count: int = 1) -> float:
    """Total area (m^2) of `count` pistons of the given diameter."""
    if diameter_m <= 0 or count < 1:
        raise ValueError("diameter must be > 0 and count >= 1")
    return count * math.pi * (diameter_m / 2) ** 2


def line_pressure(pedal_force_n: float, pedal_ratio: float,
                  master_cyl_diameter_m: float, booster_gain: float = 1.0) -> float:
    """Brake line pressure (Pa).

    P = (F_pedal * pedal_ratio * booster_gain) / A_master
    """
    if pedal_force_n < 0 or pedal_ratio <= 0 or booster_gain <= 0:
        raise ValueError("invalid pedal force, ratio or booster gain")
    pushrod_force = pedal_force_n * pedal_ratio * booster_gain
    return pushrod_force / piston_area(master_cyl_diameter_m)


def clamp_force(pressure_pa: float, caliper_piston_area_m2: float) -> float:
    """Clamp force (N) the caliper puts on the pad: F = P * A.

    For a floating caliper, use the area of the pistons on one side.
    For a fixed caliper, use the area of the pistons on ONE side as well
    (the opposing side produces the equal reaction force).
    """
    if pressure_pa < 0 or caliper_piston_area_m2 <= 0:
        raise ValueError("invalid pressure or area")
    return pressure_pa * caliper_piston_area_m2

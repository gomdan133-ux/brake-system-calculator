"""Stopping distance and deceleration."""

G = 9.80665  # m/s^2


def deceleration_from_force(total_braking_force_n: float, vehicle_mass_kg: float,
                            tire_mu: float | None = None) -> float:
    """Vehicle deceleration (m/s^2) = F / m.

    If `tire_mu` is given, the result is capped at mu * g, because the tires
    cannot transmit more force than the road grip allows (wheels lock or ABS
    intervenes).
    """
    if vehicle_mass_kg <= 0:
        raise ValueError("mass must be > 0")
    a = total_braking_force_n / vehicle_mass_kg
    if tire_mu is not None:
        a = min(a, tire_mu * G)
    return a


def stopping_distance(speed_mps: float, decel_mps2: float,
                      reaction_time_s: float = 0.0) -> dict:
    """Stopping distance (m).

    reaction distance = v * t_reaction
    braking distance  = v^2 / (2a)
    """
    if speed_mps < 0 or decel_mps2 <= 0 or reaction_time_s < 0:
        raise ValueError("invalid input")
    reaction = speed_mps * reaction_time_s
    braking = speed_mps ** 2 / (2 * decel_mps2)
    return {"reaction_m": reaction, "braking_m": braking, "total_m": reaction + braking}

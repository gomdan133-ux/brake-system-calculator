"""Brake torque at the rotor and braking force at the tire."""


def brake_torque(clamp_force_n: float, pad_mu: float, effective_radius_m: float,
                 friction_faces: int = 2) -> float:
    """Brake torque (N*m) from one caliper.

    T = clamp_force * mu * faces * r_eff
    A standard disc brake has 2 friction faces (inner and outer pad).
    """
    if clamp_force_n < 0 or pad_mu <= 0 or effective_radius_m <= 0 or friction_faces < 1:
        raise ValueError("invalid input")
    return clamp_force_n * pad_mu * friction_faces * effective_radius_m


def wheel_braking_force(torque_nm: float, tire_rolling_radius_m: float) -> float:
    """Braking force (N) at the tire contact patch: F = T / r_tire."""
    if tire_rolling_radius_m <= 0:
        raise ValueError("tire radius must be > 0")
    return torque_nm / tire_rolling_radius_m

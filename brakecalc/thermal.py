"""Brake heat: energy from a stop and rotor temperature rise."""

CAST_IRON_SPECIFIC_HEAT = 460.0  # J/(kg*K), typical grey cast iron


def kinetic_energy(mass_kg: float, v_start_mps: float, v_end_mps: float = 0.0) -> float:
    """Energy (J) removed by braking from v_start to v_end: 1/2 m (v1^2 - v2^2)."""
    if mass_kg <= 0 or v_start_mps < v_end_mps or v_end_mps < 0:
        raise ValueError("invalid input")
    return 0.5 * mass_kg * (v_start_mps ** 2 - v_end_mps ** 2)


def rotor_temperature_rise(energy_j: float, front_bias: float, rotor_mass_kg: float,
                           specific_heat: float = CAST_IRON_SPECIFIC_HEAT,
                           rotors_on_axle: int = 2) -> float:
    """Temperature rise (K) of one front rotor for a single stop.

    Assumes all heat goes into the rotors (worst case, no cooling during the
    stop), split by brake bias and evenly between the rotors on the axle.

    dT = (E * front_bias / rotors) / (m_rotor * c)
    """
    if not 0 <= front_bias <= 1:
        raise ValueError("front_bias must be between 0 and 1")
    if rotor_mass_kg <= 0 or specific_heat <= 0 or rotors_on_axle < 1:
        raise ValueError("invalid rotor data")
    energy_per_rotor = energy_j * front_bias / rotors_on_axle
    return energy_per_rotor / (rotor_mass_kg * specific_heat)

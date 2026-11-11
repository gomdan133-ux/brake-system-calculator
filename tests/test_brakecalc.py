import math

import pytest

from brakecalc import (
    brake_torque, clamp_force, deceleration_from_force, kinetic_energy,
    line_pressure, pad_life_remaining, piston_area, rotor_temperature_rise,
    stopping_distance, wheel_braking_force,
)
from brakecalc.stopping import G


def test_piston_area_single_and_double():
    a1 = piston_area(0.054)
    assert a1 == pytest.approx(math.pi * 0.027 ** 2)
    assert piston_area(0.054, 2) == pytest.approx(2 * a1)


def test_line_pressure_known_value():
    # 100 N pedal, 4:1 ratio, 1.0 booster, 25.4 mm master cylinder
    p = line_pressure(100, 4, 0.0254)
    assert p == pytest.approx(400 / (math.pi * 0.0127 ** 2))
    assert p / 1e6 == pytest.approx(0.789, rel=1e-3)  # ~0.79 MPa


def test_booster_multiplies_pressure():
    assert line_pressure(100, 4, 0.0254, booster_gain=5) == pytest.approx(
        5 * line_pressure(100, 4, 0.0254))


def test_clamp_force_is_p_times_a():
    assert clamp_force(5e6, 0.002) == pytest.approx(10_000)


def test_brake_torque_two_faces():
    # 10 kN clamp, mu 0.4, 2 faces, 0.13 m radius -> 1040 N*m
    assert brake_torque(10_000, 0.4, 0.13) == pytest.approx(1040)


def test_wheel_force():
    assert wheel_braking_force(1040, 0.325) == pytest.approx(3200)


def test_deceleration_capped_by_tire_grip():
    a = deceleration_from_force(50_000, 1500, tire_mu=0.9)
    assert a == pytest.approx(0.9 * G)


def test_stopping_distance_60mph():
    v = 26.8224  # 60 mph
    d = stopping_distance(v, 0.8 * G, reaction_time_s=1.5)
    assert d["braking_m"] == pytest.approx(45.85, rel=1e-3)
    assert d["reaction_m"] == pytest.approx(40.23, rel=1e-3)
    assert d["total_m"] == pytest.approx(d["braking_m"] + d["reaction_m"])


def test_kinetic_energy():
    assert kinetic_energy(1500, 30) == pytest.approx(675_000)
    assert kinetic_energy(1000, 20, 10) == pytest.approx(150_000)


def test_rotor_temperature_rise():
    # 675 kJ, 70% front, 2 rotors of 9 kg cast iron
    dt = rotor_temperature_rise(675_000, 0.7, 9.0)
    assert dt == pytest.approx(236_250 / (9 * 460))  # ~57 K


def test_pad_life():
    assert pad_life_remaining(9.0, 0.5) == pytest.approx(12_000)
    assert pad_life_remaining(2.5, 0.5) == 0.0


@pytest.mark.parametrize("fn,args", [
    (piston_area, (0,)),
    (line_pressure, (100, 0, 0.0254)),
    (brake_torque, (1000, 0, 0.1)),
    (stopping_distance, (20, 0)),
    (rotor_temperature_rise, (1000, 1.5, 9)),
    (pad_life_remaining, (8, 0)),
])
def test_invalid_inputs_raise(fn, args):
    with pytest.raises(ValueError):
        fn(*args)

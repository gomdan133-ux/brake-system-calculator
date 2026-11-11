"""Worked example: midsize sedan, panic stop from 60 mph.

Run from the repo root:  python examples/full_system.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from brakecalc import (  # noqa: E402
    brake_torque, clamp_force, deceleration_from_force, kinetic_energy,
    line_pressure, pad_life_remaining, piston_area, rotor_temperature_rise,
    stopping_distance, wheel_braking_force,
)

MPH = 0.44704

vehicle_mass = 1600          # kg
pedal_force = 300            # N (firm panic-stop push)
pedal_ratio = 4.0
booster_gain = 4.0
master_cyl_d = 0.0254        # 1.0 in bore
front_piston_d = 0.057       # single-piston floating caliper, 57 mm
pad_mu = 0.40
rotor_eff_radius = 0.125     # m
tire_radius = 0.33           # m
tire_mu = 0.9                # dry asphalt
front_bias = 0.70
rotor_mass = 9.0             # kg
speed = 60 * MPH

p = line_pressure(pedal_force, pedal_ratio, master_cyl_d, booster_gain)
f_clamp = clamp_force(p, piston_area(front_piston_d))
t_front = brake_torque(f_clamp, pad_mu, rotor_eff_radius)
f_front_wheel = wheel_braking_force(t_front, tire_radius)

# Front axle supplies front_bias of the total braking force
total_force = 2 * f_front_wheel / front_bias
a = deceleration_from_force(total_force, vehicle_mass, tire_mu=tire_mu)
d = stopping_distance(speed, a, reaction_time_s=1.5)
e = kinetic_energy(vehicle_mass, speed)
dt = rotor_temperature_rise(e, front_bias, rotor_mass)

print(f"Line pressure:          {p / 1e6:6.2f} MPa ({p / 6894.76:,.0f} psi)")
print(f"Front clamp force:      {f_clamp / 1000:6.2f} kN")
print(f"Front brake torque:     {t_front:6.0f} N*m per wheel")
print(f"Deceleration:           {a:6.2f} m/s^2 ({a / 9.80665:.2f} g)")
print(f"Braking distance:       {d['braking_m']:6.1f} m")
print(f"Total w/ 1.5 s reaction:{d['total_m']:6.1f} m")
print(f"Energy removed:         {e / 1000:6.0f} kJ")
print(f"Front rotor temp rise:  {dt:6.0f} C (single stop, no cooling)")
print(f"Pad life (8 mm, 0.4 mm/1000 mi): {pad_life_remaining(8, 0.4):,.0f} miles")

# Brake System Calculator

A small, tested Python library for working through a vehicle's brake system from the driver's foot to the tire: hydraulic pressure, clamp force, brake torque, deceleration, stopping distance, rotor heat, and pad life.

Built by an ASE-certified (Brakes) technician to connect what happens in the shop to the engineering behind it.

## The physics

**1. Pedal to line pressure**

$$P = \frac{F_{pedal} \cdot R_{pedal} \cdot G_{booster}}{A_{master}}$$

**2. Caliper clamp force**

$$F_{clamp} = P \cdot A_{piston}$$

**3. Brake torque** (2 friction faces per disc)

$$T = F_{clamp} \cdot \mu_{pad} \cdot 2 \cdot r_{eff}$$

**4. Force at the tire**

$$F_{tire} = \frac{T}{r_{tire}}$$

**5. Deceleration** (capped by tire grip)

$$a = \min\left(\frac{F_{total}}{m}, \; \mu_{tire} \cdot g\right)$$

**6. Stopping distance**

$$d = v \cdot t_{reaction} + \frac{v^2}{2a}$$

**7. Rotor temperature rise** (one stop, worst case with no cooling)

$$\Delta T = \frac{\tfrac{1}{2} m v^2 \cdot \text{bias}_{front} / n_{rotors}}{m_{rotor} \cdot c_{iron}}$$

**8. Pad life**: linear estimate from measured wear rate down to the minimum thickness.

All functions use SI units (N, m, Pa, kg, J).

## Install and test

```bash
pip install pytest
pytest -q
```

## Example

```bash
python examples/full_system.py
```

```
Line pressure:            9.47 MPa (1,374 psi)
Front clamp force:       24.17 kN
Front brake torque:       2417 N*m per wheel
Deceleration:             8.83 m/s^2 (0.90 g)
Braking distance:         40.8 m
Total w/ 1.5 s reaction:  81.0 m
Energy removed:            576 kJ
Front rotor temp rise:      49 C (single stop, no cooling)
Pad life (8 mm, 0.4 mm/1000 mi): 12,500 miles
```

In this example the brakes can make more force than the tires can use, so deceleration is limited by tire grip (0.9 g). That's why tires, not brakes, usually limit the stopping distance of a healthy system.

## Shop takeaways

- Doubling speed makes the braking distance **4x** longer (v²).
- Repeated stops add heat faster than the rotor can shed it, which is how brake fade happens on mountain descents.
- A seized slide pin cuts clamp force on one side, which shows up as a pull and uneven pad wear.

## Project layout

```
brakecalc/
  hydraulics.py   pedal, master cylinder, caliper
  torque.py       brake torque and tire force
  stopping.py     deceleration and stopping distance
  thermal.py      energy and rotor temperature
  wear.py         pad life
tests/            pytest suite
examples/         worked example
```

## License

MIT

"""Design scenarios only; not measured performance. Python standard library."""
import csv, json, math
from pathlib import Path
out = Path(__file__).resolve().parent
mass, diameter, eta, crr = 30.0, .145, .8, .05
ratio = (46 / 13) * (38 / 11)  # 11T axle input remains unverified.
speeds = []
for speed in [.1, .5, 1, 1.5, 2]:
    wheel = 60 * speed / (math.pi * diameter)
    speeds.append(dict(speed_m_s=speed, wheel_rpm=wheel, motor_rpm=wheel*ratio))
scenarios = []
for angle in [0, 10, 20]:
    rad = math.radians(angle)
    force = mass * 9.81 * (math.sin(rad) + crr * math.cos(rad))
    scenarios.append(dict(slope_deg=angle, force_N=force,
                          total_wheel_torque_Nm=force*diameter/2,
                          motor_torque_Nm=force*diameter/2/ratio/eta,
                          motor_shaft_power_W_at_2m_s=force*2/eta))
for name, rows in [('speed_table',speeds),('load_scenarios',scenarios)]:
    with (out/(name+'.csv')).open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
(out/'calculation.json').write_text(json.dumps(dict(mass_kg=mass,ratio_assumed=ratio,
    axle_input_teeth_assumed=11,drivetrain_efficiency_assumed=eta,
    rolling_resistance_assumed=crr,speeds=speeds,load_scenarios=scenarios),indent=2))
assert abs(speeds[-1]['wheel_rpm'] / speeds[0]['wheel_rpm'] - 20) < 1e-10
print('Calculation tables written; assumptions remain unverified.')

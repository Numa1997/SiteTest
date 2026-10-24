"""L4: are the full-model numbers the notes quote converged?  Compares L4_check.py at 2000 steps per turn (band 1e-3 of the
swing scale) with 4000 steps (band 3e-4), both with the model of L4_full.py (version 3).  PASS if the load power and the power the rotor pays agree within 1 % at every mounting.
Run after both checks: python3 -I L4_converge.py"""
import json, os, sys
H = os.path.dirname(os.path.abspath(__file__))
a = json.load(open(os.path.join(H, 'L4_check_2000.json'))); b = json.load(open(os.path.join(H, 'L4_check_4000.json')))
worst = 0.0
for x, y in zip(a, b):
    d = max(abs(y['P_load']/x['P_load'] - 1), abs(y['P_paid']/x['P_paid'] - 1)); worst = max(worst, d)
    print(f"{x['wind']:.0f} m/s {x['frac']*100:.0f} %: load {x['P_load']*1e3:.3f} / {y['P_load']*1e3:.3f} mW, "
          f"paid {x['P_paid']*1e3:.2f} / {y['P_paid']*1e3:.2f} mW ({d*100:.2f} %)")
print(f"largest difference {worst*100:.2f} %:", 'PASS' if worst < 0.01 else 'FAIL'); sys.exit(0 if worst < 0.01 else 1)

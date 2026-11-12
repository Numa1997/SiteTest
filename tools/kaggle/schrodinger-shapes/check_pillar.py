"""Convergence of pillar.py in the time step, for one finite and one hard column (E = 2, R = 4): the probabilities behind and
ahead of the column at the end, and the norm, for dt and dt/2, and the mirror symmetry y -> -y of the whole field."""
import numpy as np
from pillar import run, HARD
for V0, dts in ((3.0, (0.005, 0.0025, 0.00125)), (HARD, (0.001, 0.0005, 0.00025))):
    rows = []
    for dt in dts:
        r = run(2.0, V0, 4.0, dt=dt, hard_dt=dt); t, n, b, a, sy = r["curves"][-1]; rows.append((dt, n, b, a))
        print(f"V0={'hard' if V0 >= HARD else V0} dt={dt}: norm {n:.5f} behind {b:.5f} ahead {a:.5f}")
    d1 = abs(rows[1][3] - rows[0][3]); d2 = abs(rows[2][3] - rows[1][3])
    print(f"   change of 'ahead' when dt is halved: {d1:.5f} then {d2:.5f} (ratio {d1/max(d2,1e-12):.2f}; 4 means second order, 2 first)")
    pe = r["full_end"]; print("   mirror y/-y, largest |psi| difference / peak:", float(np.abs(np.abs(pe[:, 1:]) - np.abs(pe[:, ::-1][:, :-1])).max() / np.abs(pe).max()))

"""Grid-aligned double barriers for the 3D runs: faces on cell boundaries of the dx = 0.5 grid (odd multiples of 0.25).
Resonances by transfer matrix, and the 1D split-step of the 3D solver's scheme against the exact packet transmission."""
import numpy as np, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../tools/kaggle/resonant-tunnelling"))
from grid_test import split_step, T_packet, staircase
from tm import solve, double
import recon
for V0, d, s in ((3.0, 1.0, 2.5), (3.0, 1.0, 3.5), (2.0, 1.0, 2.5), (3.0, 1.0, 1.5)):
    segs = double(V0, d, s)
    res = [r for r in recon.resonances(segs, Emin=0.1, Emax=4.5) ]
    print(f"V0={V0} d={d} s={s}: resonances " + ", ".join(f"E={r['E']:.3f} Gamma={r['Gamma']:.4f} tau={r['tau']:.1f}" for r in res))
    for r in res[:2]:
        E = round(r['E'], 3); k0 = np.sqrt(2*E); x0 = -s/2 - d/2 - 15 - 1
        tend = (30 + abs(x0))/k0 + 3*r['tau']
        for N in (128, 256):
            P, x, Vg = split_step(E, segs, N, 64.0, 3.0, x0, tend)
            print(f"   E={E} dx={64/N}: split-step {P:.4f} | exact staircase {T_packet(staircase(x, Vg, 64/N), k0, 3.0):.4f} | exact intended {T_packet(segs, k0, 3.0):.4f} | t_end {tend:.0f}")

"""Can the 3D solver's grid (dx = 0.5 a, split-step Fourier, dt = 0.01, Fig. 14's border) resolve a two-barrier resonance?
For flat walls the 3D problem separates exactly, so the 1D split-step of the same scheme on the same x-axis answers it.
Compares the packet's transmitted probability with the exact transfer-matrix value (a) of the potential the grid actually
holds (cell-averaged staircase) and (b) of the intended square barriers. Usage: python3 grid_test.py"""
import numpy as np, sys, os, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../tools/kaggle/resonant-tunnelling"))
from tm import solve

def cellV(x, dx, segs):
    V = np.zeros_like(x)
    for (l, r, V0) in segs:
        V += V0 * np.clip(np.minimum(x + dx/2, r) - np.maximum(x - dx/2, l), 0, None) / dx
    return V

def split_step(E, segs, N, L, s0, x0, t_end, dt=0.01):
    dx = L / N; x = (np.arange(N) - N // 2) * dx; k = 2*np.pi*np.fft.fftfreq(N, dx)
    W = max(4, N // 10); m = np.ones(N); e = np.arange(W); m[:W] = np.sin(0.5*np.pi*e/W)**0.125; m[-W:] = m[:W][::-1]
    V = cellV(x, dx, segs); k0 = np.sqrt(2*E)
    p = np.exp(-(x-x0)**2/(4*s0**2) + 1j*k0*x); p /= np.sqrt((abs(p)**2).sum()*dx)
    hv = np.exp(-0.5j*V*dt); kin = np.exp(-0.5j*k**2*dt)
    xr = max(r for (_, r, _) in segs); acc_out = 0.0
    for n in range(int(round(t_end/dt))):
        p = hv*p; p = np.fft.ifft(kin*np.fft.fft(p)); p = hv*p
        before = abs(p)**2
        p = p*m
        # count what the border removes on the right as transmitted, on the left as reflected
        lost = (before - abs(p)**2)*dx
        acc_out += lost[x > xr].sum()
    ahead = (abs(p[x > xr])**2).sum()*dx + acc_out
    return ahead, x, V

def T_packet(segs, k0, s0):
    ks = np.linspace(max(k0-8/(2*s0), 0.01), k0+8/(2*s0), 4001)
    w = np.exp(-2*s0**2*(ks-k0)**2); w /= np.trapezoid(w, ks)
    T = np.array([abs(solve(kk*kk/2, segs)[0])**2 for kk in ks])
    return float(np.trapezoid(w*T, ks))

def staircase(x, V, dx):
    return [(xi - dx/2, xi + dx/2, v) for xi, v in zip(x, V) if v > 0]

rows = []
for (N, L) in ((128, 64.0), (256, 64.0)):
    for (V0, d, s, E, s0) in ((3.0, 1.0, 2.343, 1.0, 3.0), (3.0, 1.0, 2.343, 1.0, 6.0), (2.0, 1.0, 3.0, 1.0, 3.0)):
        segs = [(-s/2-d/2, -s/2+d/2, V0), (s/2-d/2, s/2+d/2, V0)]
        k0 = np.sqrt(2*E); x0 = -s/2 - d/2 - 5*s0 - 1; t_end = 1.0*(30 + abs(x0))/k0 + 60
        t0 = time.time(); P, x, Vg = split_step(E, segs, N, L, s0, x0, t_end); wall = time.time()-t0
        Tst = T_packet(staircase(x, Vg, L/N), k0, s0); Tin = T_packet(segs, k0, s0)
        rows.append((N, L/N, V0, d, s, E, s0, P, Tst, Tin))
        print(f"dx={L/N:.3f} V0={V0} d={d} s={s} E={E} s0={s0}: split-step P_ahead={P:.4f} | exact T of grid staircase={Tst:.4f} | "
              f"exact T of intended barriers={Tin:.4f} | t_end={t_end:.0f} ({wall:.1f}s)", flush=True)

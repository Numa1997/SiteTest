"""Fig. 15 grid audit: which numerical source shifts the resonances of the 1D twin away from the exact transfer matrices.
The twin is the solver's own 1D twin (rt3d2.run1d logic): Strang split-step, spectral kinetic exp(-i k^2 dt/2), barriers as
np.where(|x - c| < D/2, V0, 0) sampled on the grid, sin^(1/8) absorbing border in the outer tenth. Each source is varied alone:
  dx      grid spacing (0.5 stored; 0.25, 0.125)              -> (b) barriers sampled on the grid
  dt      time step (0.01 stored; 0.0025)                     -> (c) split-operator phase error
  L       box length (stored; x 2, border fraction the same)  -> (d) border reflection
  vmode   'step' (stored) or 'cell' (cell-averaged potential: each grid cell holds the mean of V over its width)
T = transmitted + absorbed on the right, as rt3d2.run1d counts it; exact = packet-averaged transfer-matrix T, as file_rt3d2.py."""
import sys, os, json, time
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "tools", "kaggle", "resonant-tunnelling"))
import rt3d2, tm

def exact_bar(sp, n=20001):
    sk = 1 / (2 * sp["sx"]); k0 = np.sqrt(2 * sp["E"]); kk = np.linspace(max(1e-3, k0 - 6 * sk), k0 + 6 * sk, n)
    T = np.array([abs(tm.solve(q * q / 2, rt3d2.segs_1d(sp))[0])**2 for q in kk]); w = np.exp(-(kk - k0)**2 / (2 * sk**2))
    return float((w * T).sum() / w.sum())

def twin(sp, dx=0.5, dt=0.01, Lmul=1.0, vmode="step", Nx_stored=None):
    L = Nx_stored * 0.5 * Lmul; n = int(round(L / dx)); n += n % 2
    x = (np.arange(n) - n // 2) * dx; k = 2 * np.pi * np.fft.fftfreq(n, dx)
    W = max(4, n // 10); m = np.ones(n); e = np.arange(W); m[:W] = np.sin(0.5 * np.pi * e / W) ** 0.125; m[-W:] = m[:W][::-1]
    V = np.zeros(n)
    for c in rt3d2.centres(sp):
        if vmode == "step": V += np.where(np.abs(x - c) < sp["D"] / 2, sp["V0"], 0.0)
        else:  # cell average: overlap of [x - dx/2, x + dx/2] with the barrier, divided by dx
            lo = np.maximum(x - dx / 2, c - sp["D"] / 2); hi = np.minimum(x + dx / 2, c + sp["D"] / 2)
            V += sp["V0"] * np.clip(hi - lo, 0, None) / dx
    k0 = np.sqrt(2 * sp["E"]); x0 = rt3d2.x0_of(sp)
    chi = np.exp(-(x - x0)**2 / (4 * sp["sx"]**2) + 1j * k0 * x); chi /= np.sqrt((abs(chi)**2).sum() * dx)
    hv = np.exp(-0.5j * V * dt); kin = np.exp(-0.5j * k**2 * dt)
    steps = int(round(rt3d2.t_end_of(sp, tm) / dt)); lost_r = 0.0; xl, xr = rt3d2.extent(sp)
    for _ in range(steps):
        chi = hv * np.fft.ifft(kin * np.fft.fft(hv * chi))
        b = abs(chi)**2; chi *= m; lost_r += ((b - abs(chi)**2) * dx)[x > 0].sum()
    return float((abs(chi[x > xr])**2).sum() * dx + lost_r)

if __name__ == "__main__":
    cases = [dict(shape="flat", N=2, V0=3.0, D=1.0, P=2.5, R=0.0, E=0.7827, bias=0.0, sx=12.0, sp=3.0, Nx=512),
             dict(shape="flat", N=2, V0=2.0, D=1.0, P=2.5, R=0.0, E=0.821, bias=0.0, sx=12.0, sp=3.0, Nx=512),
             dict(shape="flat", N=2, V0=2.0, D=1.0, P=2.5, R=0.0, E=0.75, bias=0.0, sx=3.0, sp=3.0, Nx=192)]
    out = []
    for sp in cases:
        ex = exact_bar(sp); row = dict(spec=sp, exact=ex)
        for name, kw in [("stored", {}), ("dx0.25", dict(dx=0.25)), ("dx0.125", dict(dx=0.125)), ("dt0.0025", dict(dt=0.0025)),
                         ("box x2", dict(Lmul=2.0)), ("cell-avg dx0.5", dict(vmode="cell")), ("cell-avg dx0.25", dict(vmode="cell", dx=0.25))]:
            t0 = time.time(); T = twin(sp, Nx_stored=sp["Nx"], **kw); row[name] = T
            print(f'V0={sp["V0"]} sx={sp["sx"]} E={sp["E"]}  {name:16s} T={T:.5f}  exact={ex:.5f}  diff={T-ex:+.5f}  ({time.time()-t0:.0f} s)', flush=True)
        out.append(row)
    json.dump(out, open(os.path.join(os.path.dirname(__file__), "twin_sources.json"), "w"), indent=1)

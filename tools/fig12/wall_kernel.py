"""Fig. 12: the memory of wall friction as a short sum of exponentials.

The stress of the Stokes layer on a wall (derived in Wolfram, 11 November 2026; docs/simulations/fig12-beer-slosh.md):
    tau(t) = rho sqrt(nu) * Integral_0^t K(t - t') U'(t') dt',   K(t) = 1 / sqrt(pi t),   Laplace: K^(s) = s^(-1/2)
with U the slip speed of the core just outside the layer. The solver cannot keep the whole history, so K is replaced by
    K_N(t) = sum_k a_k exp(-t / T_k)        (each term: one number per wall face, updated exactly each step)
with T_k spaced evenly in log between T_min and T_max and a_k >= 0 fitted (non-negative least squares) to the complex
response 1/sqrt(i w) over the band that matters, relative error weighted equally per decade.
python tools/fig12/wall_kernel.py [out.json]   -> prints the worst error in amplitude and phase over the band; exit 1 if
the stated tolerance is missed.
"""
import json, sys
import numpy as np
from scipy.optimize import nnls

F_LO, F_HI = 0.05, 200.0      # Hz: slowest cart motion to well above the highest slosh mode that the grid carries (~15 Hz)
N_TERMS = 12
T_MIN, T_MAX = 1.0 / (2 * np.pi * 2000.0), 1.0 / (2 * np.pi * 0.005)
TOL_AMP, TOL_PHASE_DEG = 0.01, 0.6   # stated before the fit

def fit():
    T = np.geomspace(T_MIN, T_MAX, N_TERMS)
    w = 2 * np.pi * np.geomspace(F_LO, F_HI, 400)
    target = 1.0 / np.sqrt(1j * w)
    # basis: Laplace of exp(-t/T) at s = i w is 1/(i w + 1/T); relative error -> divide rows by |target|
    B = 1.0 / (1j * w[:, None] + 1.0 / T[None, :])
    Wt = 1.0 / np.abs(target)
    A = np.vstack([(B * Wt[:, None]).real, (B * Wt[:, None]).imag])
    b = np.concatenate([(target * Wt).real, (target * Wt).imag])
    a, _ = nnls(A, b)
    return T, a, w

def response(T, a, w):
    return (a[None, :] / (1j * w[:, None] + 1.0 / T[None, :])).sum(1)

if __name__ == '__main__':
    T, a, w = fit()
    wc = 2 * np.pi * np.geomspace(F_LO, F_HI, 3001)       # check on a finer grid than the fit
    r = response(T, a, wc) * np.sqrt(1j * wc)              # 1 if exact
    amp = np.max(np.abs(np.abs(r) - 1)); ph = np.max(np.abs(np.degrees(np.angle(r))))
    # Stokes layer at the slosh frequency 3.41 Hz: the damping is set by the real part of the response
    w1 = 2 * np.pi * 3.4114; r1 = (response(T, a, np.array([w1])) * np.sqrt(1j * w1))[0]
    print(f'{N_TERMS} terms, T from {T_MIN*1e6:.1f} us to {T_MAX:.1f} s; band {F_LO}-{F_HI} Hz')
    print(f'worst amplitude error {100*amp:.3f} %, worst phase error {ph:.3f} deg (tolerance {100*TOL_AMP} %, {TOL_PHASE_DEG} deg)')
    print(f'at 3.4114 Hz: amplitude {abs(r1):.5f}, phase {np.degrees(np.angle(r1)):+.4f} deg')
    if len(sys.argv) > 1:
        json.dump({'about': 'Fig. 12 wall-friction memory K(t) = 1/sqrt(pi t) ~ sum a_k exp(-t/T_k), by tools/fig12/wall_kernel.py',
                   'T': [float(x) for x in T], 'a': [float(x) for x in a], 'band_Hz': [F_LO, F_HI],
                   'worst_amp_error': float(amp), 'worst_phase_deg': float(ph)}, open(sys.argv[1], 'w'), indent=1)
    ok = amp < TOL_AMP and ph < TOL_PHASE_DEG
    print('PASS' if ok else 'FAIL'); sys.exit(0 if ok else 1)

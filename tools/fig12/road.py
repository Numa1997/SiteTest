"""Road profiles z_r(x) for the cart (metres), the same formulas as the page's JavaScript.
  bump:    a sinusoidal hump, height h over length L (a speed bump: h = 0.05 m, L = 0.5 m),
  kerb:    a step of height h smoothed over 0.05 m,
  cobbles: a periodic profile of amplitude h and spacing L (sin^2 humps),
  random:  ISO 8608 class C by its roughness G_d(n0) = 256e-6 m^3 at n0 = 0.1 cycles/m, a sum of 120 sinusoids with the page's
           fixed phases, PSD G_d(n) = G_d(n0) (n/n0)^-2 between 0.05 and 10 cycles/m; the same numbers as the page's zRoad('rough').
ISO 8608 (1995): class A (very good) G_d(n0) = 16e-6 m^3, B 64e-6, C 256e-6, D 1024e-6 (geometric means).
"""
import numpy as np

def bump(x, h=0.05, L=0.5, x0=1.0):
    u = (x - x0) / L; return np.where((u > 0) & (u < 1), 0.5 * h * (1 - np.cos(2 * np.pi * u)), 0.0)

def kerb(x, h=0.03, x0=1.0, w=0.05):
    return 0.5 * h * (1 + np.tanh((x - x0) / (w / 4)))

def cobbles(x, h=0.01, L=0.10, x0=1.0):
    return np.where(x > x0, h * np.sin(np.pi * (x - x0) / L) ** 2, 0.0)

def _lcg_phases(N=120, seed=12345):
    """The page's phases: seed <- (seed * 1103515245 + 12345) mod 2^31 in IEEE double arithmetic, as JavaScript does it."""
    s = np.float64(seed); out = []
    for _ in range(N):
        s = np.fmod(s * np.float64(1103515245.0) + np.float64(12345.0), np.float64(2147483648.0)); out.append(2 * np.pi * s / 2147483648.0)
    return np.array(out)

ROUGH_PEAK = 0.0127      # m: the highest point of the class-C profile below, in its first 3 m (the page's ROUGH_PEAK; measured in node and here)

def iso_random(x, h=ROUGH_PEAK, Gd0=256e-6, n_lo=0.05, n_hi=10.0, N=120, x0=1.0):
    """The page's rough road: ISO 8608 class C as generated (N sinusoids on a geometric grid, amplitude sqrt(2 G_d(n) dn), fixed
    LCG phases), scaled so that its highest point in the first 3 m is h (h = ROUGH_PEAK leaves it as generated), and faded in
    over 0.2 m so that it starts without a step."""
    n0 = 0.1; i = np.arange(N); nlo = n_lo * (n_hi / n_lo) ** (i / N); nhi = n_lo * (n_hi / n_lo) ** ((i + 1) / N); nn = np.sqrt(nlo * nhi)
    amp = np.sqrt(2 * Gd0 * (nn / n0) ** -2 * (nhi - nlo)); ph = _lcg_phases(N)
    xx = np.asarray(x, float) - x0
    z = sum(a * np.sin(2 * np.pi * n * xx + p) for a, n, p in zip(amp, nn, ph))
    u = np.clip(xx / 0.2, 0, 1)
    return np.where(xx > 0, z * (h / ROUGH_PEAK) * u * u * (3 - 2 * u), 0.0)

PROFILES = dict(bump=bump, kerb=kerb, cobbles=cobbles, random=iso_random)

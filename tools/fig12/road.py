"""Road profiles z_r(x) for the cart (metres), the same formulas as the page's JavaScript.
  bump:    a sinusoidal hump, height h over length L (a speed bump: h = 0.05 m, L = 0.5 m),
  kerb:    a step of height h smoothed over 0.05 m,
  cobbles: a periodic profile of amplitude h and spacing L (sin^2 humps),
  random:  ISO 8608 class by its roughness G_d(n0) at n0 = 0.1 cycles/m, a sum of 200 sinusoids with random phases
           (seeded), PSD G_d(n) = G_d(n0) (n/n0)^-2 between 0.05 and 10 cycles/m.
ISO 8608 (1995): class A (very good) G_d(n0) = 16e-6 m^3, B 64e-6, C 256e-6, D 1024e-6 (geometric means).
"""
import numpy as np

def bump(x, h=0.05, L=0.5, x0=1.0):
    u = (x - x0) / L; return np.where((u > 0) & (u < 1), 0.5 * h * (1 - np.cos(2 * np.pi * u)), 0.0)

def kerb(x, h=0.03, x0=1.0, w=0.05):
    return 0.5 * h * (1 + np.tanh((x - x0) / (w / 4)))

def cobbles(x, h=0.01, L=0.10, x0=1.0):
    return np.where(x > x0, h * np.sin(np.pi * (x - x0) / L) ** 2, 0.0)

def iso_random(x, Gd0=256e-6, seed=1, n_lo=0.05, n_hi=10.0, N=200, x0=1.0):
    rng = np.random.default_rng(seed); n0 = 0.1
    ns = np.geomspace(n_lo, n_hi, N); dn = np.gradient(ns)
    amp = np.sqrt(2 * Gd0 * (ns / n0) ** -2 * dn); ph = rng.uniform(0, 2 * np.pi, N)
    z = sum(a * np.sin(2 * np.pi * n * (x - x0) + p) for a, n, p in zip(amp, ns, ph))
    return np.where(x > x0, z, 0.0)

PROFILES = dict(bump=bump, kerb=kerb, cobbles=cobbles, random=iso_random)

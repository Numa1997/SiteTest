"""Fig. 1 lecture note: recompute the note's numbers from the page's formulas (float64 replica of precompute()).

Run: python3 -I notes/fig01/check.py
The page itself is measured in Chromium by measure.cjs; this script checks the formulas the note quotes.
"""
import numpy as np
import mpmath as mp

W, R = 800.0, 300.0
# wide screen: canvas 770 x 347 css px, grid 360 x 162 (measured by measure.cjs)
box_w, box_h, cols, rows = 770, 347, 360, 162
worldH = W * box_h / box_w
ys = worldH - 10
jc = rows // 2
yc = (jc + 0.5) * worldH / rows
h = ys - yc
print(f"worldH = {worldH:.3f}  y_s = {ys:.3f}  centre row y = {yc:.3f}  h = {h:.3f}")

def U(xs, x, y, lam, gam):
    k, g, N = 2 * np.pi / lam, gam / R, len(xs)
    x = np.asarray(x, float)[..., None]
    r = np.sqrt((x - np.asarray(xs)) ** 2 + (y - ys) ** 2)
    return (np.exp(-g * r) * np.exp(1j * k * r)).sum(-1) / N

xcells = (np.arange(cols) + 0.5) * W / cols

# ---- section 3: Hankel corrections ----
for z in [4 * np.pi]:
    H = mp.hankel1(0, z)
    asym = mp.sqrt(2 / (mp.pi * z)) * mp.e ** (1j * (z - mp.pi / 4))
    ratio = H / asym
    print(f"kr = {z:.3f}: phase of H/asym = {float(mp.arg(ratio)):.5f} rad (1/(8kr) = {1/(8*z):.5f}), |H/asym| - 1 = {float(abs(ratio))-1:.2e}")
print("e^-0.15 =", round(np.exp(-0.15), 4), " lambda/2pi =", round(30 / (2 * np.pi), 3))

# ---- section 5: two sources ----
two = [200.0, 600.0]
for lam in (30, 60):
    m = [mm for mm in range(-40, 40) if abs(mm + 0.5) * lam < 400]
    print(f"lambda {lam}: calm lines m = {m[0]}..{m[-1]}, count {len(m)}; 2s/lambda = {800/lam:.2f}")
for gam in (0.15, 0.6):
    # residue on calm lines along the centre row: |a1 - a2|/2 where Delta r = (m + 1/2) lambda
    x = np.linspace(0, 800, 800001)
    r1 = np.sqrt((x - 200) ** 2 + h ** 2); r2 = np.sqrt((x - 600) ** 2 + h ** 2)
    a1 = np.exp(-gam * r1 / R); a2 = np.exp(-gam * r2 / R)
    dr = r2 - r1
    best = 0
    for mm in range(-14, 14):
        target = (mm + 0.5) * 30
        idx = np.where(np.diff(np.sign(dr - target)) != 0)[0]
        for i in idx:
            best = max(best, abs(a1[i] - a2[i]) / 2)
    # and the stored map minima on the grid
    A = np.abs(U(two, xcells, yc, 30, gam))
    mins = [A[i] for i in range(1, cols - 1) if A[i] < A[i - 1] and A[i] < A[i + 1]]
    print(f"gamma {gam}: calm-line residue max |a1-a2|/2 on centre row = {best:.4f}; grid local minima of A max = {max(mins):.4f}; edge cell value {A[0]:.4f}")

# ---- crest speed on the bisector (my addition, section 4) ----
r = np.hypot(200, h)
print(f"bisector at centre row: r = {r:.3f}, r/h = {r/h:.4f}, local wavelength = {30*r/h:.2f} px, crest speed = {33*r/h:.2f} px/s")

# ---- section 6: array factor ----
line = [64 + 44.8 * n for n in range(16)]
N, s = 16, 44.8
th = np.radians(np.arange(-900, 901) / 10)
def F(lam, th, w=None):
    beta = 2 * np.pi / lam * s * np.sin(th)
    n = np.arange(N)
    w = np.ones(N) if w is None else w
    return np.abs((w[None, :] * np.exp(-1j * n[None, :] * beta[:, None])).sum(1)) / w.sum()
f30 = F(30, th)
# strongest side lobe: between the first zeros of two neighbouring full beams, beta in (2 pi/N, 2 pi - 2 pi/N)
b = np.linspace(2 * np.pi / N + 1e-9, 2 * np.pi - 2 * np.pi / N - 1e-9, 2000001)
lobes = np.abs(np.sin(N * b / 2) / (N * np.sin(b / 2)))
nlobes = int(((lobes[1:-1] > lobes[:-2]) & (lobes[1:-1] > lobes[2:])).sum())
edge = np.degrees(np.arcsin(30 / (N * s)))
g1 = np.degrees(np.arcsin(30 / s))
print(f"main-beam edge {edge:.4f} deg, first grating lobe {g1:.4f} deg, strongest side lobe {lobes.max():.4f}, side lobes between full beams {nlobes}")
for lam in (40, 44, 45, 64):
    v = lam / s
    print(f"lambda {lam}: sin(theta1) = {v:.4f}" + (f", theta1 = {np.degrees(np.arcsin(v)):.2f} deg" if v <= 1 else ", none"), end="")
    print(f"; |F| at 90 deg = {F(lam, np.array([np.pi/2]))[0]:.3f}")
print("lambda 64 edge:", round(np.degrees(np.arcsin(64 / (N * s))), 4))
# damping taper in the far field: amplitudes e^{gamma n s sin(theta)/R}; normalise by their sum
for gam in (0.15, 0.6):
    worst = 0; worst_at = 0
    for lam in (30, 64):
        for t in th:
            w = np.exp(gam * np.arange(N) * s * np.sin(t) / R)
            d = abs(F(lam, np.array([t]), w)[0] - F(lam, np.array([t]))[0])
            if d > worst: worst, worst_at = d, (lam, np.degrees(t))
    print(f"gamma {gam}: largest change of |F| from the damping taper = {worst:.4f} at lambda, theta = {worst_at}")
# far-field check of (12) against the exact sum with gamma = 0, at distance Rf from the row centre
for Rf in (1e6, 1e7):
    xc, yc0 = 400.0, ys
    k = 2 * np.pi / 30
    px = xc + Rf * np.sin(th); py = yc0 - Rf * np.cos(th)
    r = np.sqrt((px[:, None] - np.array(line)) ** 2 + (py[:, None] - ys) ** 2)
    Uex = np.abs(np.exp(1j * k * r).sum(1)) / N
    print(f"far-field check at {Rf:.0e} px: max | |U| - |F| | = {np.max(np.abs(Uex - f30)):.2e}")

# ---- section 7 ----
D = 672.0
print(f"D^2/lambda = {D*D/30:.1f} px = {D*D/30/800:.2f} field widths; D^2/(8 lambda) = {D*D/240:.1f}")
x = np.arange(0, 801)
def spread(Nn):
    return [64 + 672 * n / (Nn - 1) for n in range(Nn)]
cont = np.linspace(64, 736, 67201)
mid = (x >= 200) & (x <= 600)
res = {}
for Nn in (2, 4, 16):
    A = np.abs(U(spread(Nn), x, yc, 64, 0.15)); res[Nn] = A
    print(f"N={Nn}, lambda 64: A on 200..600 from {A[mid].min():.3f} to {A[mid].max():.3f}, mean {A[mid].mean():.4f}")
Uc = np.zeros(len(x), complex)
for c0 in range(0, len(cont), 2000):
    part = cont[c0:c0 + 2000]
    k, g = 2 * np.pi / 64, 0.15 / R
    r = np.sqrt((x[:, None] - part) ** 2 + h ** 2)
    Uc += (np.exp(-g * r) * np.exp(1j * k * r)).sum(1)
Ac = np.abs(Uc) / len(cont)
print(f"continuous row: mean on 200..600 {Ac[mid].mean():.4f}; max |A16 - Acont| over 0..800 = {np.max(np.abs(res[16]-Ac)):.4f}, on 200..600 = {np.max(np.abs(res[16]-Ac)[mid]):.4f}")
A30 = np.abs(U(line, x, yc, 30, 0.15))
print(f"Line of 16, lambda 30: A over 0..800 from {A30.min():.3f} to {A30.max():.3f}; over 200..600 from {A30[mid].min():.3f} to {A30[mid].max():.3f}")
fz = np.sqrt(64 * h)
print(f"Fresnel zone sqrt(lambda h) = {fz:.2f}; (17) A = {fz/672*np.exp(-0.15*h/R):.4f}")
for hh in (50, 100, 169.148, 250, 340):
    A = np.abs(U(line, x, ys - hh, 64, 0.15))
    print(f"h = {hh}: mean A(16 sources) on 200..600 = {A[mid].mean():.4f}")

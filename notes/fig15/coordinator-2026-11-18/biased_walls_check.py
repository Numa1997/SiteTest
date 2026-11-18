# Fig. 15: independent check of the exact biased walls (Kaggle CPU, no GPU, writes nothing but stdout).
# T_ref of each wall run was computed by exact_wall.py / exact_wall_jax.py (stationary scattering states).
# Here, independently: an own transfer matrix in (psi, psi') form over thin flat slices of
#   V(x) = V0 inside each barrier + ramp, ramp = -bias * clip((x - xl) / (xr - xl), 0, 1)   (rt3d2.py vbias)
# and T(k) = (kR / k) |t|^2, kR = sqrt(k^2 + 2 bias), averaged over the packet's |phi(k)|^2 ~ exp(-2 sx^2 (k - k0)^2).
# Slice width 0.25/m; m = 100 and 200 show the slicing error.
import json, urllib.request
import numpy as np
C = "808c91ab"
rows = [json.loads(l) for l in urllib.request.urlopen(
    f"https://raw.githubusercontent.com/Numa1997/SiteTest/{C}/notes/fig15/correction/walls_runs.jsonl").read().decode().splitlines()]
biased = sorted([r for r in rows if r["spec"]["bias"]], key=lambda r: (r["spec"]["bias"], r["spec"]["N"], r["spec"]["sx"], r["spec"]["E"]))
plain = sorted([r for r in rows if not r["spec"]["bias"]], key=lambda r: (r["spec"]["N"], r["spec"]["sx"], r["spec"]["E"]))
print("walls", len(rows), "biased", len(biased), "unbiased", len(plain))
pick = [biased[int(i)] for i in np.linspace(0, len(biased) - 1, 12).round()] + [plain[int(i)] for i in np.linspace(0, len(plain) - 1, 3).round()]


def centres(sp):
    N, P, D = sp["N"], sp["P"], sp["D"]
    for c in (0.0, 0.25):
        cs = [c + (k - (N - 1) / 2) * P for k in range(N)]
        faces = [f for ck in cs for f in (ck - D / 2, ck + D / 2)]
        if all(abs((f - 0.25) / 0.5 - round((f - 0.25) / 0.5)) < 1e-9 for f in faces): return cs
    raise ValueError(sp)


def packet_T(sp, m):
    cs = centres(sp); D, V0, b = sp["D"], sp["V0"], sp["bias"]
    xl, xr = cs[0] - D / 2, cs[-1] + D / 2
    n = int(round((xr - xl) / (0.25 / m))); h = (xr - xl) / n; xm = xl + (np.arange(n) + 0.5) * h
    V = np.zeros(n)
    for c in cs: V[np.abs(xm - c) < D / 2] = V0
    if b: V -= b * np.clip((xm - xl) / (xr - xl), 0, 1)
    k0 = np.sqrt(2 * sp["E"]); s = 1 / (2 * sp["sx"])
    k = np.linspace(max(1e-4, k0 - 7 * s), k0 + 7 * s, 3001); w = np.exp(-2 * sp["sx"] ** 2 * (k - k0) ** 2)
    E = 0.5 * k * k
    M11 = np.ones_like(k, complex); M12 = np.zeros_like(k, complex); M21 = np.zeros_like(k, complex); M22 = np.ones_like(k, complex)
    for Vj in V:                                     # M <- T_j M, T_j the exact flat-slice propagator of (psi, psi')
        q = np.sqrt(2 * (E - Vj) + 0j); qh = q * h
        c = np.cos(qh); sq = np.where(np.abs(q) > 1e-12, np.sin(qh) / np.where(q == 0, 1, q), h); qs = -q * np.sin(qh)
        M11, M12, M21, M22 = c * M11 + sq * M21, c * M12 + sq * M22, qs * M11 + c * M21, qs * M12 + c * M22
    kR = np.sqrt(k * k + 2 * b)
    # left: psi = 1 + r, psi' = i k (1 - r); right: psi = t, psi' = i kR t;  M (1 + r, ik(1 - r)) = (t, i kR t)
    a1 = M11 + 1j * k * M12; a2 = M11 - 1j * k * M12          # first row on u and w
    b1 = M21 + 1j * k * M22; b2 = M21 - 1j * k * M22          # second row
    # a1 + r a2 = t ;  b1 + r b2 = i kR t  ->  r = (i kR a1 - b1) / (b2 - i kR a2)
    r = (1j * kR * a1 - b1) / (b2 - 1j * kR * a2); t = a1 + r * a2
    T = (kR / k) * np.abs(t) ** 2; R = np.abs(r) ** 2
    return float(np.trapezoid(w * T, k) / np.trapezoid(w, k)), float(np.max(np.abs(T + R - 1)))


print(f"{'file':52s} {'T_ref':>10s} {'TM m=100':>10s} {'TM m=200':>10s} {'diff':>9s} {'slicing':>9s} {'flux':>8s}")
worst = 0
for rr in pick:
    sp = rr["spec"]; t1, f1 = packet_T(sp, 100); t2, f2 = packet_T(sp, 200)
    d = t2 - rr["T_ref"]; worst = max(worst, abs(d))
    print(f"{rr['file']:52s} {rr['T_ref']:10.6f} {t1:10.6f} {t2:10.6f} {d:9.2e} {t2 - t1:9.1e} {max(f1, f2):8.1e}", flush=True)
print("largest |TM - T_ref|:", f"{worst:.2e}", "; gate absolute part 0.005")

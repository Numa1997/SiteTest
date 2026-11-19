"""Fig. 16, kerb ride with control off: does the stout thrown over the rim LEAVE the lip or FOLLOW the outer wall? (20 Nov 2026)
Kaggle CPU, read-only on the stored ride (no flight, no rerun). Dataset numakoudsie/fig16-guinness-cart-control attached.
    python3 lip_detach.py OUTDIR

WHY. The stored solver flies every marker that crosses the rim under the full frame equation (stout_jax.py:871-875), but it never lets
liquid cling to the glass's outer wall: a marker over the rim is in free flight at once (stout_jax.py:866-869). Under the ideal,
fully wetted conditions a slow sheet should turn round the lip and run down the outside (the teapot effect). If most of the mass is
fast enough to leave the lip, the stored flight stands; if not, the wall film is the main physics.

INPUTS, per picture interval k -> k+1, all stored:
  Q      mass flux over the rim = (nact_k - nact_{k+1}) mp / dt  (the stored books close exactly, v5 run)
  h_rim  the sheet's thickness over the rim: H - z_rim on the outermost ring of cavity columns (H the stored free surface per grid
         column, dx = 1.5 mm; mean of pictures k and k+1), over the columns where H > z_rim
  b      the overflowing arc: (overflowing ring columns / ring columns) x 2 pi R_rim
  u0     = Q / (rho b h_rim)                                            continuity across the rim
  r_lip  = half the stored wall thickness, 2.5 mm / 2 (stout_jax.py:100: WALL = 0.0025; a rounded lip assumed)
  g_n    the effective gravity pressing the sheet onto the lip's top: -(gz - alpha x) at the rim point (frame Euler term with the
         pitch acceleration alpha = d(om)/dt; the centrifugal om^2 (z - zS) and Coriolis 2 om v_x terms are left out: om^2 z ~ 0.1
         m/s^2 against 10 m/s^2, stated)
TWO THRESHOLDS
  D_simple = (u0^2 / r_lip) / (g_n + 2 gamma / (rho h_rim r_lip))        centripetal need against gravity + capillary pull
  D_wet    = We / We_c,  We = rho u0^2 h_rim / gamma,
             We_c = c (R r_lip / h_rim^2) (1 + cos theta0),  R = r_lip + h_rim / 2,  theta0 = 0 (fully wetted)
             Duez, Ybert, Clanet & Bocquet, PRL 104, 084503 (2010) [arXiv:0910.3306], Eq. (2) and Fig. 3b; c = 0.4 read off the
             inset of Fig. 3b (slope 24 at r_i/e0 = 7.5, slope = c (r_i/e0)(r_i/e0 + 1/2)), uncertain by about +-30 %; their
             intercept We_c ~ 2-3 at 1 + cos theta0 = 0 is reported as a variant (c_0 = 2.5 added).
  D > 1: the sheet leaves the lip (stored flight valid);  D < 1: it follows the outer wall.
OUTPUT: REPORT.md, report.json, lip.npz (per interval: t, Q, b, h, u0, g_n, D_simple, D_wet, D_wet0)."""
import glob, json, os, sys, urllib.request
import numpy as np
OUT = sys.argv[1] if len(sys.argv) > 1 else "/kaggle/working"; os.makedirs(OUT, exist_ok=True)
SUB = "fig-16-guinness-cart-with-control/v8/output/2026-11-15"; RIDE = os.environ.get("RIDE", "kerb_off")
RHO, GAM, DX, WALL, C_DUEZ, C0_DUEZ, TH0 = 1007.0, 0.0442, 0.0015, 0.0025, 0.4, 2.5, 0.0
R_LIP = WALL / 2
MD = []; say = lambda s="": (print(s, flush=True), MD.append(s))
Z = np.load(glob.glob(f"/kaggle/input/**/{SUB}/{RIDE}.npz", recursive=True)[0])
js = urllib.request.urlopen("https://raw.githubusercontent.com/Numa1997/SiteTest/main/public/scripts/guinness-glass.js", timeout=30).read().decode()
Rp = np.array([float(v) for v in js.split("R: [")[1].split("]")[0].split(",")]); ZRIM = (len(Rp) - 1) * 0.0005; RRIM = float(Rp[-1])
t = Z["t"].astype(float); nf = len(t); dt = float(np.median(np.diff(t))); mp = float(Z["mp"]); N = int(Z["N"])
nact = Z["nact"].astype(float); H = Z["H"].astype(float); gx, gz, om = Z["gx"].astype(float), Z["gz"].astype(float), Z["om"].astype(float)
al = np.gradient(om, t)
n = H.shape[1]; x0 = -n * DX / 2; xc = x0 + DX * (np.arange(n) + 0.5); XC, YC = np.meshgrid(xc, xc, indexing="ij"); RC = np.hypot(XC, YC)
ring = (RC <= RRIM) & (RC > RRIM - 1.5 * DX)                                   # outermost ring of cavity columns
say(f"# Fig. 16, ride `{RIDE}`: does the spilled stout leave the lip or follow the outer wall?\n")
say(f"Glass: rim radius {RRIM * 1e3:.2f} mm at z = {ZRIM * 1e3:.1f} mm; lip radius r_lip = {R_LIP * 1e3:.2f} mm (half the 2.5 mm wall); "
    f"grid {n} x {n} columns of {DX * 1e3:.1f} mm, outer ring {ring.sum()} columns.\n")
rows = []; fallback_m = 0.0
for k in range(nf - 1):
    dm = max(nact[k] - nact[k + 1], 0.0) * mp
    if dm <= 0: continue
    Q = dm / dt
    Hk = 0.5 * (H[k] + H[k + 1]); hr = Hk[ring] - ZRIM; ok = np.isfinite(hr) & (hr > 0)
    if ok.any():
        h = float(hr[ok].mean()); b = ok.sum() / ring.sum() * 2 * np.pi * RRIM; fb = False
    else:                                                                       # surface below the rim in every ring column (resolution)
        h = DX; b = 2 * np.pi * RRIM * 1 / ring.sum() * 1; fb = True; fallback_m += dm   # one column, one cell: the resolution limit
    u0 = Q / (RHO * b * h)
    phi = np.arctan2(YC[ring][ok], XC[ring][ok]) if ok.any() else np.array([0.0])
    xr = RRIM * np.cos(phi).mean()
    gn = max(-(0.5 * (gz[k] + gz[k + 1]) - 0.5 * (al[k] + al[k + 1]) * xr), 0.0)
    Ds = (u0 ** 2 / R_LIP) / (gn + 2 * GAM / (RHO * h * R_LIP))
    We = RHO * u0 ** 2 * h / GAM; Rr = R_LIP + h / 2
    Wec = C_DUEZ * Rr * R_LIP / h ** 2 * (1 + np.cos(TH0)); Wec0 = C0_DUEZ + Wec
    rows.append((t[k], dm, Q, b, h, u0, gn, Ds, We / Wec, We / Wec0, fb))
A = np.array(rows, float); m = A[:, 1]; M = m.sum()
share = lambda D: (float(m[D > 1].sum() * 1e3), float(m[D <= 1].sum() * 1e3))
fs, cs = share(A[:, 7]); fw, cw = share(A[:, 8]); fw0, cw0 = share(A[:, 9])
wq = lambda q, p: float(np.interp(p, np.cumsum(m[np.argsort(q)]) / M, np.sort(q)))
say(f"Mass over the rim: {M * 1e3:.2f} g in {len(A)} intervals; with no ring column above the rim (thickness set to one cell, arc to one column): {fallback_m * 1e3:.2f} g.\n")
say("| mass-weighted | 10 % | 50 % | 90 % |\n|---|---|---|---|")
for name, j, s_ in (("sheet thickness h_rim (mm)", 4, 1e3), ("overflowing arc b (mm)", 3, 1e3), ("exit speed u0 (m/s)", 5, 1), ("g_n (m/s^2)", 6, 1), ("D_simple", 7, 1), ("D_wet (Duez)", 8, 1)):
    say(f"| {name} | {wq(A[:, j] * s_, 0.1):.3g} | {wq(A[:, j] * s_, 0.5):.3g} | {wq(A[:, j] * s_, 0.9):.3g} |")
say("\n| criterion | leaves the lip, D > 1 (g) | follows the wall, D < 1 (g) | flying share |\n|---|---|---|---|")
say(f"| simple balance: u0^2/r_lip against g_n + 2 gamma/(rho h r_lip) | {fs:.2f} | {cs:.2f} | {100 * fs / (fs + cs):.1f} % |")
say(f"| Duez et al. 2010, Eq. (2), theta0 = 0, c = 0.4 | {fw:.2f} | {cw:.2f} | {100 * fw / (fw + cw):.1f} % |")
say(f"| the same with their intercept We_c += 2.5 | {fw0:.2f} | {cw0:.2f} | {100 * fw0 / (fw0 + cw0):.1f} % |")
REP = dict(mass_g=M * 1e3, fallback_g=fallback_m * 1e3, simple=dict(flies_g=fs, clings_g=cs), duez=dict(flies_g=fw, clings_g=cw), duez_intercept=dict(flies_g=fw0, clings_g=cw0),
           u0_median=wq(A[:, 5], 0.5), h_median_mm=wq(A[:, 4] * 1e3, 0.5), b_median_mm=wq(A[:, 3] * 1e3, 0.5), r_lip_mm=R_LIP * 1e3, c_duez=C_DUEZ)
np.savez_compressed(os.path.join(OUT, "lip.npz"), cols=np.array(["t", "dm", "Q", "b", "h", "u0", "gn", "D_simple", "D_wet", "D_wet0", "fallback"]), A=A)
json.dump(REP, open(os.path.join(OUT, "report.json"), "w"), indent=1); open(os.path.join(OUT, "REPORT.md"), "w").write("\n".join(MD) + "\n")

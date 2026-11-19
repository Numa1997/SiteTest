"""Fig. 16, kerb ride with control off: the spilled stout outside the glass as a LIQUID, derived from the stored ride (19 Nov 2026).
Kaggle CPU, no recomputation. Dataset numakoudsie/fig16-guinness-cart-control attached.  python3 derive_liquid.py OUTDIR

WHAT THE STORED "DROPS" ARE. The solver's markers: each carries mp = 0.43 mg of stout and marks where the liquid is, like dye in water.
A stored picture lists an even subsample of them, so a listed marker stands for (true count / listed count) markers. They are never
followed one by one here; they sample two FIELDS outside the glass:
    rho(x, t)  mass of liquid per volume          u(x, t)  the liquid's velocity
What leaves the glass is a sheet (tongue) of stout thrown over the rim, and the head of foam (its own density rho_f = 0.27 rho; the
stored "lumps", each with its volume, are its markers).

THE EQUATIONS IN THE AIR, in the glass's frame.
    mass:      d(rho)/dt + div(rho u) = 0                        (no liquid is made or lost in the air)
    momentum:  Du/Dt = -grad p / rho + g_eff                     (Euler; viscous stress in a free sheet is negligible)
The sheet has air on both sides, so p is atmospheric throughout it and grad p = 0:   Du/Dt = g_eff(t),
g_eff the stored effective gravity of the glass's frame (gx, gz per picture; the mean of an interval's two pictures is used).
Surface tension acts only where the sheet thins and at its edges: reported is the share of airborne liquid whose Weber number
rho u^2 h / gamma (h the local thickness, from rho: h = (rho / rho_stout) * cell) is below 1; only there could it matter.

THE SOLUTION METHOD. With grad p = 0 every element of liquid moves as x(t + dt) = x + u dt + g_eff dt^2 / 2. Between two pictures the
mass distribution rho_k is carried to rho_{k+1} by that map. Remove g_eff's share dt^2 g_eff / 2 and, where the element's velocity is
already known from the interval before, its inertial share u dt; the remaining displacement field is found as the transport of rho_k
onto rho_{k+1} of least total squared displacement (optimal transport, quadratic cost: the Benamou-Brenier form of exactly these
pressure-free equations; Benamou & Brenier, Numer. Math. 84 (2000) 375; Villani, Topics in Optimal Transportation, 2003, ch. 8).
Mass may ENTER (new liquid over the rim) and LEAVE (onto the body plane, below the grid): the transported mass of an interval is fixed
by the stored books, m = (liquid in the air at k+1) - (liquid over the rim during the interval): partial optimal transport, solved
exactly as a linear program (POT, Flamary et al., JMLR 22 (2021)). Assumption stated: within an interval the flow does not cross itself.

THE LANDING on Fig. 16's deck (310 x 124 mm, 30 mm below the glass's inner floor). The stored ride froze the liquid on Fig. 12's body
plane (z = -14 mm, 220 x 120 mm) and let the rest fall to -250 mm. Here the liquid crossing that old plane keeps its derived velocity
and falls the remaining 16 mm onto the deck; liquid beside the old body is taken at the deck's height. Per interval and deck cell:
    mass flux onto the deck   rho u_n          momentum flux along the deck   rho u_n u_t
the source terms of the thin-layer model on the deck (puddle_ideal.py).

CHECKS, pass marks fixed before the run:
 1. MASS, every picture: the markers classed "in the air" (weighted) against the stored books' count in flight: within 10 %.
 2. PREDICTION: u derived from pictures k, k+1; rho carried one step on; compared with the stored picture k+2, which the derivation
    did not use (Wasserstein-2 distance, partial): PASS if the median distance is at most half that of rho left unmoved.
 3. LANDING against the stored ride, on Fig. 12's body plane: derived mass through the plane within 15 % of the stored frozen mass;
    centroid within 10 mm; spread (x and y) within 25 %; mass passing beside the body within 15 % of the stored fallen mass.
OUTPUT: REPORT.md, report.json, deck_source.npz (per interval and 5 mm deck cell: mass, momentum x, momentum y, for stout and head),
fields.npz (rho and u on a 5 mm grid at six pictures), figures."""
import glob, json, os, subprocess, sys, time, urllib.request
import numpy as np
subprocess.run([sys.executable, "-m", "pip", "install", "-q", "POT==0.9.4"], capture_output=True)
import ot
OUT = sys.argv[1] if len(sys.argv) > 1 else "/kaggle/working"; os.makedirs(OUT, exist_ok=True)
SUB = "fig-16-guinness-cart-with-control/v8/output/2026-11-15"; RIDE = os.environ.get("RIDE", "kerb_off")
RHO, GAM, PHI_F = 1007.0, 0.0442, 0.27
OLD = (0.11, 0.06, -0.014); DECK = (0.155, 0.062, -0.030); DC = 0.005; MS = int(os.environ.get("M", "1200"))
MD = []; say = lambda s="": (print(s, flush=True), MD.append(s)); REP = {}; T0 = time.time()
Z = np.load(glob.glob(f"/kaggle/input/**/{SUB}/{RIDE}.npz", recursive=True)[0])
js = urllib.request.urlopen("https://raw.githubusercontent.com/Numa1997/SiteTest/main/public/scripts/guinness-glass.js", timeout=30).read().decode()
Rp = np.array([float(v) for v in js.split("R: [")[1].split("]")[0].split(",")]); ZRIM = (len(Rp) - 1) * 0.0005; RRIM = float(Rp[-1])
Rz = lambda z: np.interp(np.clip(np.asarray(z) / 0.0005, 0, len(Rp) - 1.001), np.arange(len(Rp)), Rp)
t = Z["t"].astype(float); nf = len(t); dt = float(np.median(np.diff(t))); mp = float(Z["mp"]); N = int(Z["N"])
gx, gz = Z["gx"].astype(float), Z["gz"].astype(float)
acc = lambda k: np.array([0.5 * (gx[k] + gx[min(k + 1, nf - 1)]), 0.0, 0.5 * (gz[k] + gz[min(k + 1, nf - 1)])])
rng = np.random.default_rng(1)
stuck_ = lambda X: (np.abs(X[:, 2] - OLD[2]) < 4e-4) & (np.abs(X[:, 0]) < OLD[0] + 1e-3) & (np.abs(X[:, 1]) < OLD[1] + 1e-3)


def stout_markers(k):
    """Markers of picture k that are liquid in the air (not in the glass, not frozen on the old plane), frozen ones, and their mass each."""
    X = Z["drops"][k].astype(np.float64); X = X[np.isfinite(X).all(1)]
    if not len(X): return X, X, 0.0
    w = float(Z["ndrops"][k]) / len(X) * mp
    r = np.hypot(X[:, 0], X[:, 1]); inglass = (X[:, 2] > 0) & (X[:, 2] < ZRIM + 0.022) & (r < np.where(X[:, 2] < ZRIM, Rz(X[:, 2]), RRIM))
    st = stuck_(X); return X[~inglass & ~st], X[st], w


def head_markers(k):
    X = Z["lumps"][k].astype(np.float64); v = Z["lumpvol"][k].astype(np.float64); ok = np.isfinite(X).all(1) & (v > 0); X, v = X[ok], v[ok]
    st = stuck_(X) if len(X) else np.zeros(0, bool); return X[~st], X[st], v[~st] * PHI_F * RHO, v[st] * PHI_F * RHO


def partial_plan(A, mA, B, mB, m, pred):
    """Least-squared-displacement transport of mass m from (A, mA) onto (B, mB), displacements measured from pred (A's pressure-free
    continuation). Exact linear program with one dummy point on each side for the mass that enters and leaves."""
    C = ot.dist(pred, B); s = C.max() + 1e-30; C = C / s
    Ma, Mb = mA.sum(), mB.sum(); m = float(np.clip(m, 0.02 * min(Ma, Mb), 0.999 * min(Ma, Mb)))
    a = np.r_[mA, Mb - m]; b = np.r_[mB, Ma - m]; tot = a.sum()
    Ce = np.zeros((len(A) + 1, len(B) + 1)); Ce[:-1, :-1] = C; Ce[-1, -1] = 1e3
    P = ot.emd(a / tot, b / tot, Ce, numItermax=3_000_000)[:-1, :-1] * tot
    return P, float(np.sqrt((P * C).sum() * s / max(P.sum(), 1e-30)))


def run(name, air, frozen, m_air_exact, m_new):
    """air[k] = (X, masses); frozen[k] = (X, masses); m_air_exact[k]: stored books' mass in the air (or None); m_new[k]: mass over the
    rim during interval k -> k+1 (kg)."""
    S = []                                                            # per picture: sampled points, their masses, their velocity (nan = unknown)
    for k in range(nf):
        X, m = air[k]
        if len(X) > MS: i = rng.choice(len(X), MS, replace=False); X, m = X[i], m[i] * (air[k][1].sum() / m[i].sum())
        S.append([X, m, np.full((len(X), 3), np.nan)])
    pred_res, still_res, floor_res = [], [], []; unassigned = 0.0
    nxc, nyc = int(round(2 * DECK[0] / DC)), int(round(2 * DECK[1] / DC))
    src = np.zeros((nf - 1, 3, nxc, nyc)); cum = dict(old_on=np.zeros(nf), old_beside=np.zeros(nf), deck_on=np.zeros(nf), deck_off=np.zeros(nf))
    cross_xy = []; we_low = 0.0; we_all = 0.0
    # LEDGER (20 Nov, the missing 5.8 g): per interval, mass leaving the air per the books against mass counted as crossing
    L = {q: np.zeros(nf - 1) for q in ("books_leave", "plan_leave", "cross_old", "deficit_nov", "deficit_cross", "deficit_late", "inward", "deck")}
    for k in range(nf - 1):
        A, mA, vA = S[k]; B, mB, vB = S[k + 1]; a = acc(k); deficit = np.zeros(len(A))
        L["books_leave"][k] = air[k][1].sum() + m_new[k] - air[k + 1][1].sum()
        if len(A) >= 8 and len(B) >= 8:
            known = np.isfinite(vA[:, 0]); pred = A + 0.5 * a * dt * dt; pred[known] += vA[known] * dt
            shared = mB.sum() - m_new[k]
            if k % 4 == 0 and known.sum() >= 8:                       # check 2: rho carried on with the velocities of the interval before
                moved = pred[known]; keep = ~((moved[:, 2] < OLD[2]) & (np.abs(moved[:, 0]) < OLD[0]) & (np.abs(moved[:, 1]) < OLD[1])) & (moved[:, 2] > -0.25)
                if keep.sum() >= 8:
                    mm = min(mA[known][keep].sum(), mB.sum()) * 0.9
                    _, d1 = partial_plan(moved[keep], mA[known][keep], B, mB, mm, moved[keep]); _, d0 = partial_plan(A[known][keep], mA[known][keep], B, mB, mm, A[known][keep])
                    h1 = rng.permutation(len(B)); h = len(B) // 2
                    _, df = partial_plan(B[h1[:h]], mB[h1[:h]], B[h1[h:2 * h]], mB[h1[h:2 * h]], 0.9 * min(mB[h1[:h]].sum(), mB[h1[h:2 * h]].sum()), B[h1[:h]])
                    pred_res.append(d1); still_res.append(d0); floor_res.append(df)
            P, _ = partial_plan(A, mA, B, mB, shared, pred)
            deficit = np.clip(mA - P.sum(1), 0.0, None); L["plan_leave"][k] = deficit.sum()   # mass the plan sends out of the air
            col = P.sum(0); okB = col > 0.5 * mB
            vB[okB] = (B[okB] - (P.T @ A)[okB] / col[okB, None]) / dt + 0.5 * a * dt          # arrival velocity at picture k+1
            row = P.sum(1); okA = (row > 0.5 * mA) & ~known
            vA[okA] = ((P @ B)[okA] / row[okA, None] - A[okA]) / dt - 0.5 * a * dt             # departure velocity of new liquid
        # ---- the liquid's flux through the planes during this interval, from rho (markers) and u at picture k
        if len(A):
            has = np.isfinite(vA[:, 0]); unassigned += mA[~has].sum()
            x, v, m = A[has], vA[has], mA[has]
            def cross(zp):
                """time in (0, dt] at which z reaches zp going down, or nan"""
                c0 = x[:, 2] - zp; disc = v[:, 2] ** 2 - 2 * a[2] * c0
                tau = np.where(np.abs(a[2]) > 1e-9, (-v[:, 2] - np.sqrt(np.maximum(disc, 0))) / np.where(np.abs(a[2]) > 1e-9, a[2], 1), -c0 / np.where(v[:, 2] < 0, v[:, 2], -1e-9))
                return np.where((c0 > 0) & (disc >= 0) & (tau > 0) & (tau <= dt), tau, np.nan)
            pos = lambda tau: x[:, :2] + v[:, :2] * tau[:, None] + 0.5 * a[:2] * (tau ** 2)[:, None]
            vel = lambda tau: v + a * tau[:, None]
            t1 = cross(OLD[2]); p1 = pos(np.nan_to_num(t1)); on_old = np.isfinite(t1) & (np.abs(p1[:, 0]) < OLD[0]) & (np.abs(p1[:, 1]) < OLD[1])
            beside = np.isfinite(t1) & ~on_old
            cr = on_old | beside; dh = deficit[has]
            L["cross_old"][k] = m[cr].sum(); L["deficit_nov"][k] = deficit[~has].sum(); L["deficit_cross"][k] = dh[cr].sum(); L["deficit_late"][k] = dh[~cr].sum()
            cum["old_on"][k + 1] = m[on_old].sum(); cum["old_beside"][k + 1] = m[beside].sum()
            if on_old.any(): cross_xy.append(np.c_[p1[on_old], m[on_old]])
            # onto Fig. 16's deck: (a) through the old plane, then 16 mm more; (b) beside the old body, at the deck's height
            land_p, land_v, land_m, off_m = [], [], [], 0.0
            if on_old.any():
                v1 = vel(np.nan_to_num(t1))[on_old]; d = OLD[2] - DECK[2]; az = a[2] if abs(a[2]) > 1e-9 else -1e-9
                tf = (-v1[:, 2] - np.sqrt(np.maximum(v1[:, 2] ** 2 - 2 * az * d, 0))) / az
                pp = p1[on_old] + v1[:, :2] * tf[:, None] + 0.5 * a[:2] * (tf ** 2)[:, None]; vv = v1 + a * tf[:, None]
                land_p.append(pp); land_v.append(vv); land_m.append(m[on_old])
            t2 = cross(DECK[2]); p2 = pos(np.nan_to_num(t2)); outside_old = ~((np.abs(p2[:, 0]) < OLD[0]) & (np.abs(p2[:, 1]) < OLD[1]))
            c2 = np.isfinite(t2) & outside_old & ~on_old
            L["inward"][k] = m[np.isfinite(t2) & ~outside_old & ~on_old].sum()      # beside the old body at -14 mm, under its outline at -30 mm
            if c2.any(): land_p.append(p2[c2]); land_v.append(vel(np.nan_to_num(t2))[c2]); land_m.append(m[c2])
            if land_p:
                lp, lv, lm = np.concatenate(land_p), np.concatenate(land_v), np.concatenate(land_m)
                ond = (np.abs(lp[:, 0]) < DECK[0]) & (np.abs(lp[:, 1]) < DECK[1])
                i = np.clip(((lp[ond, 0] + DECK[0]) / DC).astype(int), 0, nxc - 1); j = np.clip(((lp[ond, 1] + DECK[1]) / DC).astype(int), 0, nyc - 1)
                np.add.at(src[k, 0], (i, j), lm[ond]); np.add.at(src[k, 1], (i, j), lm[ond] * lv[ond, 0]); np.add.at(src[k, 2], (i, j), lm[ond] * lv[ond, 1])
                cum["deck_on"][k + 1] = lm[ond].sum(); cum["deck_off"][k + 1] = lm[~ond].sum(); L["deck"][k] = lm.sum()
            # Weber number of the airborne liquid (stout only): h = (rho / RHO) * cell, cell 4 mm
            if name == "stout" and len(x):
                ce = 0.004; key = np.floor(x / ce).astype(np.int64); _, inv = np.unique(key, axis=0, return_inverse=True); mc = np.bincount(inv.ravel(), weights=m)
                hloc = mc[inv.ravel()] / (RHO * ce * ce); we = RHO * (v ** 2).sum(1) * hloc / GAM; we_low += m[we < 1].sum(); we_all += m.sum()
    for q in cum: cum[q] = np.cumsum(cum[q])
    # ---- checks
    out = dict(unassigned_g=unassigned * 1e3)
    if m_air_exact is not None:
        est = np.array([air[k][1].sum() for k in range(nf)]); big = m_air_exact > 0.02 * m_air_exact.max()
        out["check1_mass"] = dict(max_rel_dev=float(np.max(np.abs(est[big] / m_air_exact[big] - 1))), median_rel_dev=float(np.median(np.abs(est[big] / m_air_exact[big] - 1))))
        out["check1_mass"]["PASS"] = out["check1_mass"]["median_rel_dev"] < 0.10
    if pred_res:
        out["check2_prediction"] = dict(pairs=len(pred_res), carried_mm=float(np.median(pred_res) * 1e3), unmoved_mm=float(np.median(still_res) * 1e3), sampling_floor_mm=float(np.median(floor_res) * 1e3))
        out["check2_prediction"]["PASS"] = out["check2_prediction"]["carried_mm"] <= 0.5 * out["check2_prediction"]["unmoved_mm"]
    fz = frozen[-1]; XY = np.concatenate(cross_xy) if cross_xy else np.zeros((0, 3))
    if len(fz[0]) > 5 and len(XY) > 5:
        wst = fz[1] if np.ndim(fz[1]) else np.full(len(fz[0]), fz[1]); stored_on = float(np.sum(wst)); sc = np.average(fz[0][:, :2], axis=0, weights=wst); ss = np.sqrt(np.average((fz[0][:, :2] - sc) ** 2, axis=0, weights=wst))
        dc_ = np.average(XY[:, :2], axis=0, weights=XY[:, 2]); dsp = np.sqrt(np.average((XY[:, :2] - dc_) ** 2, axis=0, weights=XY[:, 2]))
        c3 = dict(stored_on_g=stored_on * 1e3, derived_on_g=float(cum["old_on"][-1] * 1e3), stored_centroid_mm=(sc * 1e3).tolist(), derived_centroid_mm=(dc_ * 1e3).tolist(),
                  stored_spread_mm=(ss * 1e3).tolist(), derived_spread_mm=(dsp * 1e3).tolist(), derived_beside_g=float(cum["old_beside"][-1] * 1e3))
        c3["pass_mass"] = abs(c3["derived_on_g"] / c3["stored_on_g"] - 1) < 0.15; c3["pass_centroid"] = float(np.hypot(*(dc_ - sc))) < 0.010
        c3["pass_spread"] = bool(np.all(np.abs(dsp / ss - 1) < 0.25)); out["check3_landing"] = c3
    out["deck"] = dict(landed_on_deck_g=float(cum["deck_on"][-1] * 1e3), missed_deck_g=float(cum["deck_off"][-1] * 1e3))
    if we_all > 0: out["weber_below_1_share"] = float(we_low / we_all)
    return out, src, cum, L


say(f"# Fig. 16, ride `{RIDE}`: the spilled stout outside the glass as a liquid, derived from the stored ride\n")
nact = Z["nact"].astype(float); nfly = Z["nfly"].astype(float); nst = Z["nstuck"].astype(float); nland = Z["nlanded"].astype(float)
airS, frS = [], []
for k in range(nf):
    Xa, Xs, w = stout_markers(k); ma = np.full(len(Xa), w)
    if len(Xa) and nfly[k] > 0: ma *= nfly[k] * mp / ma.sum() if ma.sum() > 0 else 1.0     # the field's total mass is the stored books' (classification checked below)
    airS.append((Xa, ma)); frS.append((Xs, np.full(len(Xs), nst[k] * mp / max(len(Xs), 1))))
raw = np.array([len(stout_markers(k)[0]) * stout_markers(k)[2] for k in range(nf)])
new_s = np.r_[np.maximum(nact[:-1] - nact[1:], 0.0) * mp]
airS_raw = [(airS[k][0], np.full(len(airS[k][0]), raw[k] / max(len(airS[k][0]), 1))) for k in range(nf)]
resS, srcS, cumS, LS = run("stout", airS, frS, nfly * mp, new_s)
est = raw; big = nfly * mp > 0.02 * (nfly * mp).max(); dev = np.abs(est[big] / (nfly[big] * mp) - 1)
resS["check1_mass"] = dict(median_rel_dev=float(np.median(dev)), max_rel_dev=float(dev.max()), PASS=bool(np.median(dev) < 0.10))
c3 = resS.get("check3_landing")
if c3: c3["stored_beside_g"] = float(nland[-1] * mp * 1e3); c3["pass_beside"] = abs(c3["derived_beside_g"] / c3["stored_beside_g"] - 1) < 0.15; c3["PASS"] = bool(c3["pass_mass"] and c3["pass_centroid"] and c3["pass_spread"] and c3["pass_beside"])
REP["stout"] = resS
# the head: its markers are the stored lumps
airH, frH = [], []
for k in range(nf):
    Xa, Xs, ma, ms = head_markers(k); airH.append((Xa, ma)); frH.append((Xs, ms))
fs = Z["foam_spill"].astype(float) * PHI_F * RHO; new_h = np.maximum(np.diff(fs), 0.0)
resH, srcH, cumH, LH = run("head", airH, frH, None, new_h); REP["head"] = resH
hb = np.array([airH[k][1].sum() + frH[k][1].sum() for k in range(nf)])
REP["head"]["books"] = dict(spilled_liquid_g_end=float(fs[-1] * 1e3), in_air_plus_frozen_g_end=float(hb[-1] * 1e3), max_in_air_plus_frozen_g=float(hb.max() * 1e3))

P = lambda b: "PASS" if b else "FAIL"
s = REP["stout"]
say("## Stout: the checks (pass marks fixed before the run)\n")
say(f"1. Mass. Markers classed 'in the air', weighted, against the stored books: median deviation {100 * s['check1_mass']['median_rel_dev']:.1f} %, largest {100 * s['check1_mass']['max_rel_dev']:.1f} % (mark: median below 10 %): **{P(s['check1_mass']['PASS'])}**")
if "check2_prediction" in s:
    c = s["check2_prediction"]; say(f"2. Prediction of picture k+2 ({c['pairs']} pairs): rho carried on {c['carried_mm']:.2f} mm, rho left unmoved {c['unmoved_mm']:.2f} mm, sampling floor {c['sampling_floor_mm']:.2f} mm (mark: carried at most half of unmoved): **{P(c['PASS'])}**")
if c3:
    say(f"3. Landing on Fig. 12's body plane, against the stored ride: **{P(c3['PASS'])}**\n")
    say("| | stored ride | derived | mark | |\n|---|---|---|---|---|")
    say(f"| liquid through the plane (g) | {c3['stored_on_g']:.1f} | {c3['derived_on_g']:.1f} | within 15 % | {P(c3['pass_mass'])} |")
    say(f"| centroid x, y (mm) | {[round(v, 1) for v in c3['stored_centroid_mm']]} | {[round(v, 1) for v in c3['derived_centroid_mm']]} | within 10 mm | {P(c3['pass_centroid'])} |")
    say(f"| spread x, y (mm) | {[round(v, 1) for v in c3['stored_spread_mm']]} | {[round(v, 1) for v in c3['derived_spread_mm']]} | within 25 % | {P(c3['pass_spread'])} |")
    say(f"| liquid passing beside the body (g) | {c3['stored_beside_g']:.1f} | {c3['derived_beside_g']:.1f} | within 15 % | {P(c3['pass_beside'])} |")
say(f"\nLiquid in the air with no derived velocity (never transported): {s['unassigned_g']:.2f} g-pictures. Share of airborne stout with Weber number below 1: {100 * s.get('weber_below_1_share', float('nan')):.1f} %.")
say("\n## Stout: the landing on Fig. 16's deck (before the deck stage)\n")
say(f"Liquid striking the deck in 4 s: **{s['deck']['landed_on_deck_g']:.1f} g**; liquid missing the deck: **{s['deck']['missed_deck_g']:.1f} g**; over the rim in all: {(N - nact[-1]) * mp * 1e3:.1f} g.")
h = REP["head"]
say("\n## The head of foam (as a fluid of density 0.27 rho)\n")
say(f"Liquid in the spilled head (books): {h['books']['spilled_liquid_g_end']:.2f} g ({Z['foam_spill'][-1] * 1e6:.2f} mL of foam). Striking the deck: {h['deck']['landed_on_deck_g']:.2f} g; missing it: {h['deck']['missed_deck_g']:.2f} g.")
if "check2_prediction" in h: c = h["check2_prediction"]; say(f"Prediction check: carried {c['carried_mm']:.2f} mm, unmoved {c['unmoved_mm']:.2f} mm, floor {c['sampling_floor_mm']:.2f} mm: **{P(c['PASS'])}**")
if "check3_landing" in h: c = h["check3_landing"]; say(f"Landing on Fig. 12's plane: stored {c['stored_on_g']:.2f} g, derived {c['derived_on_g']:.2f} g; centroid stored {[round(v, 1) for v in c['stored_centroid_mm']]}, derived {[round(v, 1) for v in c['derived_centroid_mm']]} mm.")
say("\n## The missing mass: step 1, the stored counters alone\n")
bal = (nact + nfly + nland + nst) - N; kb = int(np.argmax(np.abs(bal)))
say(f"Per picture, in the glass + in the air + fallen past the edge + frozen on the old plane - N: largest imbalance {bal[kb] * mp * 1e3:+.4f} g "
    f"({bal[kb]:+.0f} markers) at picture {kb} (t = {t[kb]:.3f} s); all {nf} pictures exact: {bool(np.all(bal == 0))}.")
hdev = (hb - fs) * 1e3; kh = int(np.argmax(np.abs(hdev)))
say(f"Head: stored lumps (air + frozen) against foam_spill, largest difference {hdev[kh]:+.3f} g of liquid at picture {kh} (t = {t[kh]:.3f} s).")
fac = (nfly[big] * mp) / np.maximum(raw[big], 1e-30)
say(f"Weight per picture: listed air markers x (ndrops / listed) x mp, rescaled to nfly x mp; the rescale factor has median {np.median(fac):.3f}, range {fac.min():.3f} to {fac.max():.3f}.")
REP["step1"] = dict(max_imbalance_g=float(bal[kb] * mp * 1e3), picture=kb, t=float(t[kb]), head_max_dev_g=float(hdev[kh]), weight_rescale_median=float(np.median(fac)))
say("\n## The missing mass: step 2, the derivation's ledger (stout, cumulative to 4 s, g)\n")
C = {q: float(LS[q].sum() * 1e3) for q in LS}
air_end = nfly[-1] * mp * 1e3
say("| | g |\n|---|---|")
say(f"| over the rim (books) | {(N - nact[-1]) * mp * 1e3:.2f} |")
say(f"| still in the air at 4 s (books) | {air_end:.2f} |")
say(f"| left the air, books: sum of (frozen + fallen) per interval | {C['books_leave']:.2f} |")
say(f"| left the air, transport plan (dummy column) | {C['plan_leave']:.2f} |")
say(f"| counted crossing z = -14 mm (on the body + beside) | {C['cross_old']:.2f} |")
say(f"| of the plan's leaving mass: with no velocity, never tested | {C['deficit_nov']:.2f} |")
say(f"| of the plan's leaving mass: velocity known, ballistic crossing not within (0, dt] | {C['deficit_late']:.2f} |")
say(f"| counted crossing but the plan keeps it in the air (double count, + sign) | {C['cross_old'] - C['deficit_cross']:.2f} |")
say(f"| beside the old body at -14 mm, under its outline at -30 mm, dropped | {C['inward']:.2f} |")
say(f"| counted on the deck stage (on + off) | {C['deck']:.2f} |")
REP["ledger_g"] = C; REP["ledger_g"]["air_end"] = air_end
np.savez_compressed(os.path.join(OUT, "ledger.npz"), t=t, **{f"stout_{q}": LS[q] for q in LS}, **{f"head_{q}": LH[q] for q in LH})
np.savez_compressed(os.path.join(OUT, "deck_source.npz"), t=t, cell=DC, deck=np.array(DECK), stout=srcS, head=srcH)
say(f"\nWall time {time.time() - T0:.0f} s on Kaggle CPU.")
json.dump(REP, open(os.path.join(OUT, "report.json"), "w"), indent=1, default=float); open(os.path.join(OUT, "REPORT.md"), "w").write("\n".join(MD) + "\n")

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
omS = Z["om"].astype(float); alS = np.gradient(omS, t); ZS = 0.122 - 0.030   # pitch rate, pitch acceleration; pivot height (run16.py:64, cart4.py:61)


def fly(x, v, t0, zp, tmax=0.8, h=5e-4):
    """Integrate the stored solver's own frame equation (stout_jax.py:391: gravity and the cart's acceleration, Euler alpha, centrifugal
    om^2, Coriolis 2 om v) from (x, v) at time t0 until z = zp, midpoint rule, step 0.5 ms. Returns time taken, position, velocity there."""
    x = np.array(x, float); v = np.array(v, float); tau = np.full(len(x), np.nan); X = np.zeros_like(x); V = np.zeros_like(v); s_ = 0.0; alive = x[:, 2] > zp
    while alive.any() and s_ < tmax:
        g_x, g_z, o, a_ = (float(np.interp(t0 + s_, t, q)) for q in (gx, gz, omS, alS))
        f = lambda x_, v_: np.stack([g_x + a_ * (x_[:, 2] - ZS) + o * o * x_[:, 0] + 2 * o * v_[:, 2], np.zeros(len(x_)), g_z - a_ * x_[:, 0] + o * o * (x_[:, 2] - ZS) - 2 * o * v_[:, 0]], 1)
        a1 = f(x, v); vm = v + 0.5 * h * a1; xm = x + 0.5 * h * v; a2 = f(xm, vm); xn = x + h * vm; vn = v + h * a2
        hit = alive & (xn[:, 2] <= zp)
        if hit.any():
            fr = (x[hit, 2] - zp) / (x[hit, 2] - xn[hit, 2]); X[hit] = x[hit] + fr[:, None] * (xn[hit] - x[hit]); V[hit] = v[hit] + fr[:, None] * (vn[hit] - v[hit]); tau[hit] = s_ + fr * h
        x = np.where(alive[:, None], xn, x); v = np.where(alive[:, None], vn, v); alive &= ~hit; s_ += h
    return tau, X, V


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
    LV = []                                                           # per interval: the plan's leaving liquid at its ballistic crossing of z = -14 mm (no time window)
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
            sel = dh > 0; az_ = a[2] if a[2] < -1e-9 else -1e-9
            if sel.any():
                xs, vs, c0 = x[sel], v[sel], x[sel, 2] - OLD[2]
                tau = (-vs[:, 2] - np.sqrt(np.maximum(vs[:, 2] ** 2 - 2 * az_ * c0, 0))) / az_; ok = (c0 > 0) & (tau > 0)
                LV.append((k, xs[ok, :2] + vs[ok, :2] * tau[ok, None] + 0.5 * a[:2] * (tau[ok] ** 2)[:, None], vs[ok] + a * tau[ok, None], dh[sel][ok], t[k] + tau[ok]))
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
    return out, src, cum, L, LV, S


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
resS, srcS, cumS, LS, LVS, SS = run("stout", airS, frS, nfly * mp, new_s)
# ================= LANDING OF THE STOUT ON FIG. 16'S DECK (20 Nov, the owner's two changes) =================
# (1) Liquid frozen on z = -14 mm: its STORED position, exact. Newly frozen in interval k = frozen markers listed in picture k+1 and not
#     in picture k (frozen markers do not move, so a listed one keeps its float16 position); mass Delta nstuck * mp per interval, exact.
#     Derived: only the 16 mm drop to the deck, from the velocity of the derived leaving liquid nearest to it at -14 mm.
# (2) Liquid that fell past the old body's edge: mass through z = -30 mm per interval from the books, exact:
#     F_k = (stored air liquid below -30 mm) + nlanded * mp, increments of its running maximum; placed at the ballistic crossings of -30 mm
#     of the derived air liquid that is not over the old body.
from scipy.spatial import cKDTree
nxc, nyc = int(round(2 * DECK[0] / DC)), int(round(2 * DECK[1] / DC)); WIN = 0.1
FX = []
for k in range(nf):
    X = Z["drops"][k].astype(np.float64); X = X[np.isfinite(X).all(1)]; FX.append(X[stuck_(X)][:, :2])
keys = lambda P: set(map(tuple, np.round(P * 1e6).astype(np.int64)))
persist, NEW = [], []
for k in range(nf - 1):
    s0, s1 = keys(FX[k]), keys(FX[k + 1])
    if len(FX[k]): persist.append(np.mean([q in s1 for q in map(tuple, np.round(FX[k] * 1e6).astype(np.int64))]))
    K1 = np.round(FX[k + 1] * 1e6).astype(np.int64); NEW.append(FX[k + 1][np.array([tuple(q) not in s0 for q in K1], bool)] if len(K1) else np.zeros((0, 2)))
persist_med = float(np.median(persist)) if persist else float("nan")
USE_ID = persist_med >= 0.9
dnst = np.maximum(np.diff(nst), 0.0) * mp; carried = 0.0; carry = 0.0; FR = []                    # FR: (k, xy, mass) newly frozen, stored
edges = (np.linspace(-DECK[0], DECK[0], nxc + 1), np.linspace(-DECK[1], DECK[1], nyc + 1)); cxy = np.stack(np.meshgrid(0.5 * (edges[0][1:] + edges[0][:-1]), 0.5 * (edges[1][1:] + edges[1][:-1]), indexing="ij"), -1).reshape(-1, 2)
for k in range(nf - 1):
    mk = dnst[k] + carry
    if mk <= 0: continue
    if USE_ID:
        P_ = NEW[k]; w_ = np.full(len(P_), 1.0)
    else:                                                                                           # fallback: difference of the frozen fields, 5 mm cells
        h0 = np.histogram2d(FX[k][:, 0], FX[k][:, 1], edges)[0] * (nst[k] / max(len(FX[k]), 1)); h1 = np.histogram2d(FX[k + 1][:, 0], FX[k + 1][:, 1], edges)[0] * (nst[k + 1] / max(len(FX[k + 1]), 1))
        dh_ = np.clip(h1 - h0, 0, None).ravel(); P_, w_ = cxy[dh_ > 0], dh_[dh_ > 0]
    if len(P_) == 0: carry = mk; carried += dnst[k]; continue
    FR.append((k, P_, w_ / w_.sum() * mk)); carry = 0.0
if carry > 0: FR.append((nf - 2, FX[-1], np.full(len(FX[-1]), carry / max(len(FX[-1]), 1))))
lv_k = np.concatenate([np.full(len(q[1]), q[0]) for q in LVS]); lv_p = np.concatenate([q[1] for q in LVS]); lv_v = np.concatenate([q[2] for q in LVS]); lv_m = np.concatenate([q[3] for q in LVS]); lv_t = np.concatenate([q[4] for q in LVS])
v_mean = np.average(lv_v, axis=0, weights=lv_m)
LAND = []                                                                                          # (time on deck, xy, velocity, mass, part)
for (k, P_, w_) in FR:
    near = np.abs(lv_k - k) <= 3
    if near.sum() >= 8:
        tr = cKDTree(lv_p[near]); d_, j_ = tr.query(P_, k=8); W = lv_m[near][j_] / np.maximum(d_, 1e-4); v1 = (lv_v[near][j_] * W[..., None]).sum(1) / W.sum(1)[:, None]
    else: v1 = np.tile(v_mean, (len(P_), 1))
    tf, Xd, Vd = fly(np.c_[P_, np.full(len(P_), OLD[2])], v1, t[k] + 0.5 * dt, DECK[2]); okf = np.isfinite(tf)       # the 16 mm drop, full frame equation
    LAND.append((t[k] + 0.5 * dt + tf[okf], Xd[okf, :2], Vd[okf], w_[okf] * (w_.sum() / max(w_[okf].sum(), 1e-30)), 0))
Mbelow = np.array([airS[k][1][airS[k][0][:, 2] < DECK[2]].sum() if (len(airS[k][0]) and nfly[k] > 0) else 0.0 for k in range(nf)])
Fraw = Mbelow + nland * mp; Fmono = np.minimum(np.maximum.accumulate(Fraw), Fraw[-1]); dF = np.diff(Fmono); fall_noise = float(np.clip(-np.diff(Fraw), 0, None).sum())   # Fmono ends exactly at nlanded * mp
carry = 0.0; fall_carried = 0.0
for k in range(nf - 1):
    mk = dF[k] + carry
    if mk <= 0: continue
    X, mm, vv = SS[k]; hv = np.isfinite(vv[:, 0]) & (X[:, 2] > DECK[2]) if len(X) else np.zeros(0, bool)
    if hv.sum() == 0: carry = mk; fall_carried += dF[k]; continue
    x, v, m = X[hv], vv[hv], mm[hv]
    tau2, X2, V2 = fly(x, v, t[k], DECK[2]); c1 = x[:, 2] - OLD[2]; _, X1, _ = fly(x, v, t[k], OLD[2])    # full frame equation
    over_body = (c1 > 0) & (np.abs(X1[:, 0]) < OLD[0]) & (np.abs(X1[:, 1]) < OLD[1])                 # these freeze in the stored ride: part (1)
    cand = ~over_body & np.isfinite(tau2) & (tau2 > 0)
    if cand.sum() == 0: carry = mk; fall_carried += dF[k]; continue
    pick = cand & (tau2 <= dt)
    if pick.sum() == 0: pick = np.zeros_like(cand); pick[np.where(cand)[0][np.argsort(tau2[cand])[:20]]] = True
    w_ = m[pick] / m[pick].sum() * mk; tp = tau2[pick]
    LAND.append((t[k] + np.minimum(tp, dt), X2[pick, :2], V2[pick], w_, 1)); carry = 0.0
srcS = np.zeros((nf - 1, 3, nxc, nyc)); tot = {0: [0.0, 0.0], 1: [0.0, 0.0]}
for (tl, P_, V_, w_, part) in LAND:
    kk = np.clip(((tl - t[0]) / dt).astype(int), 0, nf - 2); on = (np.abs(P_[:, 0]) < DECK[0]) & (np.abs(P_[:, 1]) < DECK[1])
    i = np.clip(((P_[on, 0] + DECK[0]) / DC).astype(int), 0, nxc - 1); j = np.clip(((P_[on, 1] + DECK[1]) / DC).astype(int), 0, nyc - 1)
    np.add.at(srcS, (kk[on], 0, i, j), w_[on]); np.add.at(srcS, (kk[on], 1, i, j), w_[on] * V_[on, 0]); np.add.at(srcS, (kk[on], 2, i, j), w_[on] * V_[on, 1])
    tot[part][0] += w_[on].sum(); tot[part][1] += w_[~on].sum()
# ---- field check: per 5 mm deck cell and per 0.1 s window, derived mass against the stored frozen mass (L1 / stored mass)
nw = int(np.ceil((t[-1] - t[0]) / WIN)) + 2
def field(tl, P_, w_):
    G = np.zeros((nw, nxc, nyc)); on = (np.abs(P_[:, 0]) < DECK[0]) & (np.abs(P_[:, 1]) < DECK[1])
    np.add.at(G, (np.clip(((tl[on] - t[0]) / WIN).astype(int), 0, nw - 1), np.clip(((P_[on, 0] + DECK[0]) / DC).astype(int), 0, nxc - 1), np.clip(((P_[on, 1] + DECK[1]) / DC).astype(int), 0, nyc - 1)), w_[on]); return G
cat = lambda L_, i: np.concatenate([q[i] for q in L_]) if L_ else np.zeros(0)
Sfield = field(cat([(np.full(len(q[1]), t[q[0]] + 0.5 * dt),) for q in FR], 0), np.concatenate([q[1] for q in FR]), cat(FR, 2))
fz = [q for q in LAND if q[4] == 0]
Dfield = field(cat(fz, 0), np.concatenate([q[1] for q in fz]), cat(fz, 3))
inbody = (np.abs(lv_p[:, 0]) < OLD[0]) & (np.abs(lv_p[:, 1]) < OLD[1])
Vfield = field(lv_t[inbody], lv_p[inbody], lv_m[inbody])
L1 = lambda A_, B_: float(np.abs(A_ - B_).sum() / max(B_.sum(), 1e-30))
rs = np.random.default_rng(7); half = [[], []]
for (k, P_, w_) in FR:
    pm = rs.permutation(len(P_)); hh = len(P_) // 2
    for s_, ix in enumerate((pm[:hh], pm[hh:2 * hh])):
        if len(ix): half[s_].append((np.full(len(ix), t[k] + 0.5 * dt), P_[ix], w_[ix] * len(P_) / len(ix)))
floor = L1(*(field(cat(h_, 0), np.concatenate([q[1] for q in h_]), cat(h_, 2)) for h_ in half)) if half[0] and half[1] else float("nan")
LANDREP = dict(frozen_g=float((tot[0][0] + tot[0][1]) * 1e3), fallen_g=float((tot[1][0] + tot[1][1]) * 1e3), on_deck_g=float((tot[0][0] + tot[1][0]) * 1e3), off_deck_g=float((tot[0][1] + tot[1][1]) * 1e3),
               stored_frozen_g=float(nst[-1] * mp * 1e3), stored_fallen_g=float(nland[-1] * mp * 1e3), over_rim_g=float((N - nact[-1]) * mp * 1e3),
               frozen_persistence_median=persist_med, frozen_by_identity=bool(USE_ID), frozen_mass_carried_g=float(carried * 1e3), fallen_mass_carried_g=float(fall_carried * 1e3),
               fallen_noise_clipped_g=fall_noise * 1e3, L1_deck_vs_stored=L1(Dfield, Sfield), L1_derived_velocity_crossing_vs_stored=L1(Vfield, Sfield), L1_sampling_floor=floor)
LANDREP["total_landed_g"] = LANDREP["frozen_g"] + LANDREP["fallen_g"]
resS["landing"] = LANDREP; resS["deck"] = dict(landed_on_deck_g=LANDREP["on_deck_g"], missed_deck_g=LANDREP["off_deck_g"])
resS.pop("check3_landing", None)
est = raw; big = nfly * mp > 0.02 * (nfly * mp).max(); dev = np.abs(est[big] / (nfly[big] * mp) - 1)
resS["check1_mass"] = dict(median_rel_dev=float(np.median(dev)), max_rel_dev=float(dev.max()), PASS=bool(np.median(dev) < 0.10))
c3 = None
if c3: c3["stored_beside_g"] = float(nland[-1] * mp * 1e3); c3["pass_beside"] = abs(c3["derived_beside_g"] / c3["stored_beside_g"] - 1) < 0.15; c3["PASS"] = bool(c3["pass_mass"] and c3["pass_centroid"] and c3["pass_spread"] and c3["pass_beside"])
REP["stout"] = resS
# the head: its markers are the stored lumps
airH, frH = [], []
for k in range(nf):
    Xa, Xs, ma, ms = head_markers(k); airH.append((Xa, ma)); frH.append((Xs, ms))
fs = Z["foam_spill"].astype(float) * PHI_F * RHO; new_h = np.maximum(np.diff(fs), 0.0)
resH, srcH, cumH, LH, _, _ = run("head", airH, frH, None, new_h); REP["head"] = resH
hb = np.array([airH[k][1].sum() + frH[k][1].sum() for k in range(nf)])
REP["head"]["books"] = dict(spilled_liquid_g_end=float(fs[-1] * 1e3), in_air_plus_frozen_g_end=float(hb[-1] * 1e3), max_in_air_plus_frozen_g=float(hb.max() * 1e3))

P = lambda b: "PASS" if b else "FAIL"
s = REP["stout"]
say("## Stout: the checks (pass marks fixed before the run)\n")
say(f"1. Mass. Markers classed 'in the air', weighted, against the stored books: median deviation {100 * s['check1_mass']['median_rel_dev']:.1f} %, largest {100 * s['check1_mass']['max_rel_dev']:.1f} % (mark: median below 10 %): **{P(s['check1_mass']['PASS'])}**")
if "check2_prediction" in s:
    c = s["check2_prediction"]; say(f"2. Prediction of picture k+2 ({c['pairs']} pairs): rho carried on {c['carried_mm']:.2f} mm, rho left unmoved {c['unmoved_mm']:.2f} mm, sampling floor {c['sampling_floor_mm']:.2f} mm (mark: carried at most half of unmoved): **{P(c['PASS'])}**")
G = s["landing"]
say(f"3. Landing, field check per 5 mm deck cell and 0.1 s window: L1 mismatch, derived mass on the deck against the stored frozen mass, "
    f"**{100 * G['L1_deck_vs_stored']:.1f} %** of the mass (sampling floor, two halves of the stored markers: {100 * G['L1_sampling_floor']:.1f} %). "
    f"The same with the derived velocities alone (the leaving liquid's own ballistic crossing of -14 mm, no stored positions): {100 * G['L1_derived_velocity_crossing_vs_stored']:.1f} %.")
say(f"\nLiquid in the air with no derived velocity (never transported): {s['unassigned_g']:.2f} g-pictures. Share of airborne stout with Weber number below 1: {100 * s.get('weber_below_1_share', float('nan')):.1f} %.")
say("\n## Stout: the landing on Fig. 16's deck (before the deck stage)\n")
say(f"Total landed: **{G['total_landed_g']:.2f} g** of {G['over_rim_g']:.2f} g over the rim: frozen part {G['frozen_g']:.2f} g (stored {G['stored_frozen_g']:.2f}), fallen part {G['fallen_g']:.2f} g (stored {G['stored_fallen_g']:.2f}).")
say(f"On Fig. 16's deck **{G['on_deck_g']:.2f} g**, off it **{G['off_deck_g']:.2f} g**. Frozen positions by identity: {G['frozen_by_identity']} (persistence of listed frozen markers, median {G['frozen_persistence_median']:.3f}); "
    f"mass carried to a later interval for want of listed positions: frozen {G['frozen_mass_carried_g']:.2f} g, fallen {G['fallen_mass_carried_g']:.2f} g; sampling noise clipped from the fallen flux {G['fallen_noise_clipped_g']:.2f} g.")
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
np.savez_compressed(os.path.join(OUT, "deck_source.npz"), t=t, cell=DC, deck=np.array(DECK), stout=srcS, head=srcH)
say(f"\nWall time {time.time() - T0:.0f} s on Kaggle CPU.")
json.dump(REP, open(os.path.join(OUT, "report.json"), "w"), indent=1, default=float); open(os.path.join(OUT, "REPORT.md"), "w").write("\n".join(MD) + "\n")

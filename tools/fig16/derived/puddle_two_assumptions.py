"""Fig. 16, kerb ride with control off: the two-assumption test for the puddle on the deck (19 Nov 2026). Kaggle CPU, no GPU.
Dataset numakoudsie/fig16-guinness-cart-control attached.  python3 puddle_two_assumptions.py OUTDIR
PURPOSE. Do the unknown landing velocities matter? Run A: parcels land with zero sideways speed relative to the deck. Run B: with the
sideways speed of straight flight from the nearest point of the rim to the landing point over t = sqrt(2 * 0.1775 m / |g_z|).
VERDICT, fixed before the run: if A and B differ by less than 5 g (10 % of the 48.6 g on the deck) at every contact angle, the landing
velocities do not matter; otherwise they do, and the CPU rerun's velocities are required. B is only a rough bound (the deck's own
acceleration bends the paths in its frame), so agreement does not replace the rerun; disagreement settles it.

INPUT (the stored ride kerb_off, run 5, notebook v8). Landing map: (1) drops frozen on Fig. 12's plane z = -14 mm: they would fall 16 mm
more onto the deck; positions from each picture's list, mass per picture from the rise of nstuck; (2) drops that fell past Fig. 12's
edge: CROSSINGS of the deck's plane. A crossing is a listed drop with |z + 30 mm| < 3 mm, outside Fig. 12's outline. Weights: (a) each
listed drop stands for ndrops/listed true drops of its picture (the list is an even subsample); (b) a falling drop is inside the 6 mm
band for 6 mm / |v_z| and pictures come every 1/60 s, so it is seen on average |band| / (|v_z| dt) times: each sighting carries
|v_z| dt / 6 mm crossings, with v_z = sqrt(2 |g_z| 0.1775 m) of its picture (free fall from the rim, no initial vertical speed:
an assumption); (c) the crossings are scaled to the stored fallen mass. Uncertainty of the on/off split: bootstrap over pictures, and
the spread between weighting (b) and no correction for speed.

MODEL. Thin layer on the deck, depth h(x, y, t), depth-mean velocity u(x, y, t), in the deck's frame (x along the road):
  dh/dt + div(h u) = S        (S: arriving stout, as depth per time)
  d(hu)/dt + div(h u u) + grad(g_n h^2 / 2) = h a_t - 3 nu u / h * h ... friction 3 nu u / h^2 per unit mass (laminar thin layer)
g_n: the deck frame's effective gravity normal to the deck (pressing the layer down); a_t: along the deck. Both from the stored cart
state DIFFERENCED between pictures (the exact mean acceleration of each interval): deck centre a = (dv/dt, dvzc/dt), pitch rate om,
angular acceleration d(om)/dt; at a point r on the deck, a_P = a_C + alpha x r + om x (om x r); effective gravity in deck axes
g_eff = R(th)^T (g - a_P). The sign conventions (pitch and rotation) are chosen by matching g_eff at the glass's point S (h_g = 0.122 m
above the deck's centre) to the stored gx, gz; the residual is reported.
Finite volumes on 2 mm cells, Rusanov fluxes, friction implicit. The glass's foot (r < 31.2 mm) is a wall. Contact line: no flux into a
dry cell unless the wet side is deeper than the puddle thickness e (a partially wetting liquid does not spread thinner than e).
Deck edge: liquid leaves only where the edge cell is deeper than e and moves outward; elsewhere the edge is a wall.
e = 2 sqrt(gamma / (rho g)) sin(theta / 2): rim force balance, hydrostatic rho g e^2 / 2 against gamma (1 - cos theta) from Young's law
(derived; matches e = theta l_c for small theta, Herminghaus & Brochard, C. R. Physique 7 (2006); de Gennes et al. section 2.2 not read).
CHECKS FIRST: mass conserved to rounding; a puddle on a deck at rest stays and settles to about e; a film on a fixed incline runs at
g sin(alpha) h^2 / (3 nu)."""
import glob, json, os, sys, time
import numpy as np
OUT = sys.argv[1] if len(sys.argv) > 1 else "/kaggle/working"; os.makedirs(OUT, exist_ok=True)
SUB = "fig-16-guinness-cart-with-control/v8/output/2026-11-15"; RIDE = "kerb_off"
RHO, GAM, NU, G0 = 1007.0, 0.0442, 2.05e-6, 9.81
DECK = (0.155, 0.062, -0.030); OLD = (0.11, 0.06, -0.014); BAND = 0.003; FALL = 0.1775; HG = 0.122; RFOOT = 0.0312; RRIM = 0.03747 + 0.0025
DXC = 0.002; DT = 2.5e-4
MD = []; say = lambda s="": (print(s, flush=True), MD.append(s)); REP = {}
efor = lambda th: 2 * np.sqrt(GAM / (RHO * G0)) * np.sin(np.radians(th) / 2)

# ---------------------------------------------------------------- grid and solver
nx, ny = int(round(2 * DECK[0] / DXC)), int(round(2 * DECK[1] / DXC))
xc = -DECK[0] + (np.arange(nx) + 0.5) * DXC; yc = -DECK[1] + (np.arange(ny) + 0.5) * DXC
XX, YY = np.meshgrid(xc, yc, indexing="ij"); SOLID = np.hypot(XX, YY) < RFOOT; OPEN = ~SOLID


class Layer:
    def __init__(s, e):
        s.h = np.zeros((nx, ny)); s.hu = np.zeros((nx, ny)); s.hv = np.zeros((nx, ny)); s.e = e; s.lost = 0.0; s.added = 0.0

    def mass(s): return float(s.h.sum() * DXC * DXC * RHO)

    def step(s, dt, gn, atx, aty):
        """gn: (nx, ny) normal effective gravity pressing down (>= 0 used); atx, aty: tangential accelerations (nx, ny)."""
        h, hu, hv, e = s.h, s.hu, s.hv, s.e; gnp = np.maximum(gn, 0.0)
        u = np.where(h > 1e-7, hu / np.maximum(h, 1e-7), 0.0); v = np.where(h > 1e-7, hv / np.maximum(h, 1e-7), 0.0)
        c = np.sqrt(gnp * h)
        def flux(hL, hR, uL, uR, vL, vR, cL, cR, gL, gR, okL, okR, outward_edge=None):
            # x-direction Rusanov flux between L and R (for y, call with u, v swapped)
            FL = np.stack([hL * uL, hL * uL * uL + 0.5 * gL * hL * hL, hL * uL * vL]); FR = np.stack([hR * uR, hR * uR * uR + 0.5 * gR * hR * hR, hR * uR * vR])
            a = np.maximum(np.abs(uL) + cL, np.abs(uR) + cR); UL = np.stack([hL, hL * uL, hL * vL]); UR = np.stack([hR, hR * uR, hR * vR])
            F = 0.5 * (FL + FR) - 0.5 * a * (UR - UL)
            # contact line: no mass into a dry cell unless the wet side is deeper than e; walls (solids) pass nothing but pressure
            dryR, dryL = hR < 1e-7, hL < 1e-7
            block = (dryR & (hL <= e)) | (dryL & (hR <= e)) | ~okL | ~okR
            pres = np.stack([np.zeros_like(hL), np.where(okL & ~okR, 0.5 * gL * hL * hL, np.where(~okL & okR, 0.5 * gR * hR * hR, 0.0)), np.zeros_like(hL)])
            wall = np.stack([0 * hL, np.where(dryR, 0.5 * gL * hL * hL, 0.5 * gR * hR * hR), 0 * hL])   # a blocked contact line acts as a wall on the wet side
            return np.where(block[None], np.where((okL & okR)[None], wall, pres), F)
        # interior x faces
        Fx = flux(h[:-1], h[1:], u[:-1], u[1:], v[:-1], v[1:], c[:-1], c[1:], gnp[:-1], gnp[1:], OPEN[:-1], OPEN[1:])
        Fy = flux(h[:, :-1], h[:, 1:], v[:, :-1], v[:, 1:], u[:, :-1], u[:, 1:], c[:, :-1], c[:, 1:], gnp[:, :-1], gnp[:, 1:], OPEN[:, :-1], OPEN[:, 1:])
        Fy = Fy[[0, 2, 1]]                                           # back to (h, hu, hv) order
        # deck edges: outflow only where deeper than e and moving outward; else wall (pressure only)
        def edge(hb, un, ut, gb):
            go = (hb > e) & (un > 0)
            return np.where(go[None], np.stack([hb * un, hb * un * un + 0.5 * gb * hb * hb, hb * un * ut]), np.stack([0 * hb, 0.5 * gb * hb * hb, 0 * hb]))
        Ex1 = edge(h[-1], u[-1], v[-1], gnp[-1]); Ex0 = edge(h[0], -u[0], v[0], gnp[0]); Ex0[0] *= -1; Ex0[2] *= -1
        Ey1 = edge(h[:, -1], v[:, -1], u[:, -1], gnp[:, -1])[[0, 2, 1]]; Ey0 = edge(h[:, 0], -v[:, 0], u[:, 0], gnp[:, 0])[[0, 2, 1]]; Ey0[0] *= -1; Ey0[1] *= -1
        U = np.stack([h, hu, hv]); dU = np.zeros_like(U)
        dU[:, :-1] -= Fx; dU[:, 1:] += Fx; dU[:, -1] -= Ex1; dU[:, 0] += Ex0
        dU[:, :, :-1] -= Fy; dU[:, :, 1:] += Fy; dU[:, :, -1] -= Ey1; dU[:, :, 0] += Ey0
        out = float((Ex1[0].sum() - Ex0[0].sum() + Ey1[0].sum() - Ey0[0].sum()) * DXC * dt * RHO)
        U = U + dt / DXC * dU
        U[1] += dt * U[0] * atx; U[2] += dt * U[0] * aty
        hn = np.maximum(U[0], 0.0); f = 1.0 / (1.0 + 3 * NU * dt / np.maximum(hn, 1e-6) ** 2)   # implicit laminar friction
        s.h = np.where(OPEN, hn, 0.0); s.hu = np.where(OPEN & (hn > 1e-7), U[1] * f, 0.0); s.hv = np.where(OPEN & (hn > 1e-7), U[2] * f, 0.0)
        s.lost += out
        return out

    def add(s, m_kg, x, y, ux, uy):
        i = np.clip(((x + DECK[0]) / DXC).astype(int), 0, nx - 1); j = np.clip(((y + DECK[1]) / DXC).astype(int), 0, ny - 1)
        ok = OPEN[i, j]; dh = m_kg / (RHO * DXC * DXC)
        np.add.at(s.h, (i[ok], j[ok]), dh[ok]); np.add.at(s.hu, (i[ok], j[ok]), (dh * ux)[ok]); np.add.at(s.hv, (i[ok], j[ok]), (dh * uy)[ok])
        s.added += float(m_kg[ok].sum()); return float(m_kg[~ok].sum())


# ---------------------------------------------------------------- checks of the model
say("# Fig. 16, kerb ride with control off: does the landing velocity matter for what stays on the deck?\n")
say("## Checks of the thin-layer model\n")
ones = np.ones((nx, ny))
# 1+2: deck at rest, a 20 g blob in front of the glass, 4 s
for th in (30, 60, 90):
    L = Layer(efor(th)); r = np.hypot(XX - 0.08, YY); m0 = 0.020; blob = (r < 0.015) & OPEN; L.h[blob] = m0 / (RHO * DXC * DXC * blob.sum())
    for _ in range(int(4.0 / DT)): L.step(DT, G0 * ones, 0 * ones, 0 * ones)
    wet = L.h > 1e-5; say(f"- At rest, theta {th} deg (e = {L.e * 1e3:.2f} mm): mass {m0 * 1e3:.3f} -> {L.mass() * 1e3:.3f} g (+ {L.lost * 1e3:.3f} g left the deck); "
                          f"largest depth {L.h.max() * 1e3:.2f} mm, mean depth of the wetted area {L.h[wet].mean() * 1e3:.2f} mm, wetted {wet.sum() * 4:.0f} mm^2")
    REP[f"rest_{th}"] = dict(m0=m0, m_end=L.mass(), lost=L.lost, hmax=float(L.h.max()), hmean=float(L.h[wet].mean()), e=L.e)
# 3: incline, uniform film 1 mm, alpha 2 deg, the film's steady speed in the deck's middle
al = np.radians(2.0); h0 = 0.001; L = Layer(0.0); L.h[OPEN] = h0
for _ in range(int(1.0 / DT)): L.step(DT, G0 * np.cos(al) * ones, G0 * np.sin(al) * ones, 0 * ones)
mid = (np.abs(XX) < 0.03) & (np.abs(YY) > 0.04) & OPEN; ucomp = float(np.mean(L.hu[mid] / np.maximum(L.h[mid], 1e-9))); uth = G0 * np.sin(al) * h0 ** 2 / (3 * NU)
say(f"- Incline 2 deg, film 1 mm: speed {ucomp * 1e3:.2f} mm/s against g sin(alpha) h^2 / (3 nu) = {uth * 1e3:.2f} mm/s ({100 * (ucomp / uth - 1):+.1f} %)")
REP["incline"] = dict(u=ucomp, u_theory=uth)

# ---------------------------------------------------------------- the stored ride
src = glob.glob(f"/kaggle/input/**/{SUB}/{RIDE}.npz", recursive=True)
if not src: say("STOP: stored ride not attached"); open(os.path.join(OUT, "REPORT.md"), "w").write("\n".join(MD)); sys.exit(1)
Z = np.load(src[0]); t = Z["t"].astype(float); nf = len(t); mp = float(Z["mp"]); D = Z["drops"].astype(np.float64)
nd = Z["ndrops"].astype(float); nst = Z["nstuck"].astype(float); nland = Z["nlanded"].astype(float); gxs, gzs = Z["gx"].astype(float), Z["gz"].astype(float)
v, vzc, th_, om = (Z[k].astype(float) for k in ("v", "vzc", "th", "om"))
dtp = np.diff(t); ax_c = np.diff(v) / dtp; az_c = np.diff(vzc) / dtp; alp = np.diff(om) / dtp
thm = 0.5 * (th_[1:] + th_[:-1]); omm = 0.5 * (om[1:] + om[:-1])

def geff(rx, rz, sgn):
    """Effective gravity in deck axes at deck point (rx, rz) for every interval; sgn = (s_th, s_om): sign conventions."""
    s1, s2 = sgn; c, s = np.cos(s1 * thm), np.sin(s1 * thm)
    wx, wz = c * rx - s * rz, s * rx + c * rz                      # r in world axes
    o, a = s2 * omm, s2 * alp
    apx = ax_c + a * wz - o * o * wx; apz = az_c - a * wx - o * o * wz  # a_C + alpha x r + om x (om x r), rotation about y
    gx_w, gz_w = -apx, -G0 - apz
    return c * gx_w + s * gz_w, -s * gx_w + c * gz_w

best = None
for sgn in ((1, 1), (1, -1), (-1, 1), (-1, -1)):
    gxe, gze = geff(0.0, HG, sgn); res = np.sqrt(np.mean((gxe - 0.5 * (gxs[1:] + gxs[:-1])) ** 2 + (gze - 0.5 * (gzs[1:] + gzs[:-1])) ** 2))
    if best is None or res < best[1]: best = (sgn, res)
SGN = best[0]; REP["frame"] = dict(signs=SGN, rms_residual_vs_stored=best[1])
say(f"\n## The deck frame from the stored cart state\nSign conventions chosen by matching the glass's point S to the stored effective gravity: {SGN}; "
    f"rms difference {best[1]:.2f} m/s^2 (the stored values are samples at the pictures, these are interval means).")

# ---------------------------------------------------------------- the landing map, with weights
arrivals = []                                                      # (t, m, x, y, kind)
for k in range(1, nf):
    Dk = D[k][np.isfinite(D[k]).all(1)]
    if not len(Dk): continue
    w = nd[k] / len(Dk)
    fr = Dk[np.abs(Dk[:, 2] - OLD[2]) < 4e-4]; dm = max(nst[k] - nst[k - 1], 0.0) * mp
    if dm > 0 and len(fr):
        pick = fr[np.random.default_rng(k).choice(len(fr), min(len(fr), 400), replace=False)]
        for p in pick: arrivals.append((t[k], dm / len(pick), p[0], p[1], 0))
    b = (np.abs(Dk[:, 2] - DECK[2]) < BAND) & ~((np.abs(Dk[:, 0]) < OLD[0]) & (np.abs(Dk[:, 1]) < OLD[1]))
    vz = np.sqrt(2 * max(abs(gzs[k]), 0.5) * FALL)
    for p in Dk[b]: arrivals.append((t[k], w * vz * (1 / 60) / (2 * BAND), p[0], p[1], 1))   # weight in particles, scaled below
A = np.array(arrivals); cr = A[:, 4] == 1
for variant in ("speed-corrected", "uncorrected"):
    m = A[cr, 1] if variant == "speed-corrected" else np.array([nd[np.searchsorted(t, tt)] / max(1, np.isfinite(D[np.searchsorted(t, tt)]).all(1).sum()) for tt in A[cr, 0]])
    on = (np.abs(A[cr, 2]) < DECK[0]) & (np.abs(A[cr, 3]) < DECK[1]); scale = nland[-1] * mp / m.sum()
    REP[f"split_{variant}"] = dict(on_g=float(m[on].sum() * scale * 1e3), off_g=float(m[~on].sum() * scale * 1e3))
pics = np.unique(A[cr, 0]); rng = np.random.default_rng(1); boot = []
on_all = (np.abs(A[cr, 2]) < DECK[0]) & (np.abs(A[cr, 3]) < DECK[1]); mm = A[cr, 1]
for _ in range(400):
    sel = rng.choice(pics, len(pics), replace=True); ww = np.zeros(len(mm))
    for p in sel: ww += (A[cr, 0] == p)
    tot = (ww * mm).sum(); boot.append((ww * mm)[on_all].sum() / tot * nland[-1] * mp * 1e3)
REP["split_bootstrap_on_g"] = [float(np.percentile(boot, 5)), float(np.percentile(boot, 50)), float(np.percentile(boot, 95))]
A[cr, 1] = A[cr, 1] * nland[-1] * mp / A[cr, 1].sum()             # crossings scaled to the stored fallen mass
say("\n## The landing map\n")
say(f"Crossings: {cr.sum():,} listed drops in the 6 mm band about the deck's plane, outside Fig. 12's outline. Of the {nland[-1] * mp * 1e3:.1f} g that fell past "
    f"Fig. 12's edge, ON the deck: speed-corrected {REP['split_speed-corrected']['on_g']:.1f} g, uncorrected {REP['split_uncorrected']['on_g']:.1f} g; "
    f"bootstrap over pictures 5 / 50 / 95 %: {', '.join(f'{x:.1f}' for x in REP['split_bootstrap_on_g'])} g.")

# ---------------------------------------------------------------- runs A and B

# deck-point effective gravity depends on x: evaluate per interval on the grid's x (z = 0 on the deck's top)
GX = np.empty((nf - 1, nx)); GZ = np.empty((nf - 1, nx))
for i, xx in enumerate(xc): GX[:, i], GZ[:, i] = geff(xx, 0.0, SGN)
def geff(rx, rz, sgn, _G=(GX, GZ)):                              # noqa: F811 (grid version for the runs)
    return _G[0][:, :, None] * np.ones((1, 1, ny)), _G[1][:, :, None] * np.ones((1, 1, ny))
GXg, GZg = geff(None, None, None)
REP["deck_frame_range"] = dict(along_min=float(GX.min()), along_max=float(GX.max()), normal_min=float(-GZ.max()), normal_max=float(-GZ.min()))
rows = {}
for thc in (30, 60, 90):
    for kind in ("A", "B"):
        t0 = time.time(); L = Layer(efor(thc)); ia = np.argsort(A[:, 0]); AA = A[ia]; q = 0; missed = 0.0
        onr = (AA[:, 4] == 0) | ((np.abs(AA[:, 2]) < DECK[0]) & (np.abs(AA[:, 3]) < DECK[1]))
        for n in range(int((t[-1] - t[0]) / DT)):
            tn = t[0] + n * DT; k = min(max(np.searchsorted(t, tn, side="right") - 1, 0), nf - 2)
            r0 = q
            while q < len(AA) and AA[q, 0] <= tn: q += 1
            blk = AA[r0:q][onr[r0:q]]
            if len(blk):
                if kind == "A": ux = uy = np.zeros(len(blk))
                else:
                    rr = np.hypot(blk[:, 2], blk[:, 3]); rim = RRIM / np.maximum(rr, 1e-9); tf = np.sqrt(2 * FALL / max(abs(gzs[k]), 0.5))
                    ux = blk[:, 2] * (1 - rim) / tf; uy = blk[:, 3] * (1 - rim) / tf
                missed += L.add(blk[:, 1], blk[:, 2], blk[:, 3], ux, uy)
            L.step(DT, -GZg[k], GXg[k], np.zeros((nx, ny)))
        rows[(thc, kind)] = dict(on_deck_end_g=L.mass() * 1e3, ran_off_g=L.lost * 1e3, landed_g=L.added * 1e3, on_glass_foot_g=missed * 1e3,
                                 books_err_g=(L.added - L.mass() - L.lost) * 1e3, wall_s=round(time.time() - t0, 1))
        say(f"run {kind}, theta {thc}: {rows[(thc, kind)]}")
REP["runs"] = {f"{k[1]}_{k[0]}": v_ for k, v_ in rows.items()}
say("\n## Result: stout on Fig. 16's deck at the end of the ride (4 s)\n")
say("| contact angle | e (mm) | landed on the deck (g) | A: left on the deck (g) | B: left on the deck (g) | A - B (g) | books error (g) |\n|---|---|---|---|---|---|---|")
worst = 0.0
for thc in (30, 60, 90):
    a, b = rows[(thc, "A")], rows[(thc, "B")]; d = a["on_deck_end_g"] - b["on_deck_end_g"]; worst = max(worst, abs(d))
    say(f"| {thc} deg | {efor(thc) * 1e3:.2f} | {a['landed_g']:.1f} | {a['on_deck_end_g']:.1f} | {b['on_deck_end_g']:.1f} | {d:+.1f} | {max(abs(a['books_err_g']), abs(b['books_err_g'])):.1e} |")
REP["verdict"] = dict(max_abs_A_minus_B_g=worst, landing_velocities_matter=bool(worst >= 5.0))
say(f"\n**Verdict (fixed before the run: 5 g):** largest |A - B| = {worst:.1f} g -> " + ("the landing velocities MATTER; the rerun's velocities are required." if worst >= 5.0 else "the landing velocities do not matter at this level; the rerun's velocities remain the final word (B is only a rough bound)."))
json.dump(REP, open(os.path.join(OUT, "report.json"), "w"), indent=1, default=float)
open(os.path.join(OUT, "REPORT.md"), "w").write("\n".join(MD) + "\n")

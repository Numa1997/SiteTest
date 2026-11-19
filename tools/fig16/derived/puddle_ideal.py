"""Fig. 16, kerb ride with control off: the stout on the deck under IDEAL conditions (owner's decision, 19 Nov 2026). Kaggle CPU.
Dataset numakoudsie/fig16-guinness-cart-control attached.  python3 puddle_ideal.py OUTDIR
Replaces puddle_two_assumptions.py (its contact-line rule leaked and its checks failed; its A/B verdict, 11.6-17.4 g against a 5 g
mark, said the landing velocities matter, so the CPU rerun's velocities are required).

IDEAL CONDITIONS. The deck is smooth and fully wetted; the glass is glued to it with no gap (its foot, r < 31.2 mm, is a wall). No
contact angle, no pinning, no puddle depth, no edge rule: stout moving outward at the deck's edge leaves it.

MODEL. A thin layer on the deck in the deck's frame: depth h(x, y, t), depth-mean velocity u(x, y, t).
  dh/dt + div(h u) = S;   d(hu)/dt + div(h u u) + grad(g_n h^2 / 2) = h a_t - 3 nu u / h     (per area; i.e. 3 nu u / h^2 per mass)
The friction 3 nu u / h^2 is exact for a steady film (Nusselt's parabolic profile) and is what the incline check tests. g_n: the
deck frame's effective gravity normal to the deck; a_t: along it. Finite volumes on 2 mm cells, second-order MUSCL reconstruction
(minmod) of h and u, Rusanov fluxes, Heun (second-order) time stepping, friction implicit. Dry cells: h = 0, no rule beyond the fluxes.

CHECKS (before the ride):
 1. Mass: added = on the deck + left over the edges, to rounding.
 2. Spreading on a still, open plane (no deck edges): the constant-volume axisymmetric viscous gravity current. From the thin-film
    equation h_t = (g/3nu) (1/r) d/dr (r h^3 dh/dr) the similarity solution is h = A(t) (1 - r^2/R^2)^(1/3), A = 4V/(3 pi R^2),
    R(t) = (1024 / (81 pi^3))^(1/8) (g V^3 t / (3 nu))^(1/8) = 0.894 (g V^3 t / (3 nu))^(1/8); its mean square radius is (3/7) R^2.
    (Derived here; the constant 0.894 is the one quoted from Huppert, J. Fluid Mech. 121 (1982) 43, whose text was not reachable.)
    The model starts from that profile at R0 = 30 mm, V = 20 mL, and its sqrt(7/3 <r^2>) is compared with R(t) for 4 s.
 3. A uniform film on a fixed incline: speed against g sin(alpha) h^2 / (3 nu) with the LOCAL depth, in the deck's middle.
DECK FRAME. From the stored cart state differenced between pictures; signs fixed by matching the glass's point to the stored gx, gz;
where the residual lies (at the kerb or spread over the ride) is reported.
LANDINGS. Until the CPU rerun gives every parcel's own path, the landing map of land_on_deck.py is used with A: no sideways speed,
B: straight flight from the nearest rim point; this run only tests the model, it is not the deck's result."""
import glob, json, os, sys, time
import numpy as np
OUT = sys.argv[1] if len(sys.argv) > 1 else "/kaggle/working"; os.makedirs(OUT, exist_ok=True)
SUB = "fig-16-guinness-cart-with-control/v8/output/2026-11-15"; RIDE = "kerb_off"
RHO, NU, G0 = 1007.0, 2.05e-6, 9.81
DECK = (0.155, 0.062, -0.030); OLD = (0.11, 0.06, -0.014); BAND = 0.003; FALL = 0.1775; HG = 0.122; RFOOT = 0.0312; RRIM = 0.03747 + 0.0025
DXC = 0.002; DT = 2.5e-4; HMIN = 1e-7
MD = []; say = lambda s="": (print(s, flush=True), MD.append(s)); REP = {}


def minmod(a, b): return np.where(a * b > 0, np.sign(a) * np.minimum(np.abs(a), np.abs(b)), 0.0)


class Layer:
    """Thin layer on a rectangle of nx x ny cells of side DXC; open[i, j] False = wall; edges: 'open' (outflow when moving out) or 'wall'."""
    def __init__(s, nx, ny, open_, edges="open"):
        s.nx, s.ny, s.open, s.edges = nx, ny, open_, edges
        s.U = np.zeros((3, nx, ny)); s.lost = 0.0; s.added = 0.0

    def mass(s): return float(s.U[0].sum() * DXC * DXC * RHO)

    def _rhs(s, U, gn, atx, aty):
        h = np.maximum(U[0], 0.0); wet = h > HMIN
        u = np.where(wet, U[1] / np.maximum(h, HMIN), 0.0); v = np.where(wet, U[2] / np.maximum(h, HMIN), 0.0); g = np.maximum(gn, 0.0)
        R = np.zeros_like(U); out = 0.0
        for ax in (0, 1):
            un, ut = (u, v) if ax == 0 else (v, u)
            W = [h, un, ut]
            # slopes (minmod), reconstructed states at the faces between cell i and i+1 along ax
            def sl(q):
                d = np.diff(q, axis=ax); z = np.zeros_like(np.take(q, [0], axis=ax))
                dl = np.concatenate([z, d], axis=ax); dr = np.concatenate([d, z], axis=ax)
                return minmod(dl, dr)
            Lw = [np.take(q + 0.5 * sl(q), range(q.shape[ax] - 1), axis=ax) for q in W]
            Rw = [np.take(q - 0.5 * sl(q), range(1, q.shape[ax]), axis=ax) for q in W]
            hL, hR = np.maximum(Lw[0], 0), np.maximum(Rw[0], 0)
            gL = np.take(g, range(g.shape[ax] - 1), axis=ax); gR = np.take(g, range(1, g.shape[ax]), axis=ax)
            oL = np.take(s.open, range(s.open.shape[ax] - 1), axis=ax); oR = np.take(s.open, range(1, s.open.shape[ax]), axis=ax)
            def F(hh, un_, ut_, gg): return np.stack([hh * un_, hh * un_ * un_ + 0.5 * gg * hh * hh, hh * un_ * ut_])
            a = np.maximum(np.abs(Lw[1]) + np.sqrt(gL * hL), np.abs(Rw[1]) + np.sqrt(gR * hR))
            UL = np.stack([hL, hL * Lw[1], hL * Lw[2]]); URr = np.stack([hR, hR * Rw[1], hR * Rw[2]])
            Fx = 0.5 * (F(hL, Lw[1], Lw[2], gL) + F(hR, Rw[1], Rw[2], gR)) - 0.5 * a * (URr - UL)
            # walls (solid cells): the open side keeps only its own pressure
            wl = oL & ~oR; wr = ~oL & oR; both = oL & oR
            Fw = np.stack([0 * hL, np.where(wl, 0.5 * gL * hL * hL, np.where(wr, 0.5 * gR * hR * hR, 0.0)), 0 * hL])
            Fx = np.where(both[None], Fx, Fw)
            # domain edges along ax
            hb0, hb1 = np.take(h, [0], axis=ax), np.take(h, [-1], axis=ax)
            un0, un1 = np.take(un, [0], axis=ax), np.take(un, [-1], axis=ax); ut0, ut1 = np.take(ut, [0], axis=ax), np.take(ut, [-1], axis=ax)
            g0, g1 = np.take(g, [0], axis=ax), np.take(g, [-1], axis=ax)
            if s.edges == "open":
                go1 = un1 > 0; go0 = un0 < 0
                E1 = np.where(go1[None], F(hb1, un1, ut1, g1), np.stack([0 * hb1, 0.5 * g1 * hb1 ** 2, 0 * hb1]))
                E0 = np.where(go0[None], F(hb0, un0, ut0, g0), np.stack([0 * hb0, 0.5 * g0 * hb0 ** 2, 0 * hb0]))
            else:
                E1 = np.stack([0 * hb1, 0.5 * g1 * hb1 ** 2, 0 * hb1]); E0 = np.stack([0 * hb0, 0.5 * g0 * hb0 ** 2, 0 * hb0])
            Fall = np.concatenate([E0, Fx, E1], axis=ax + 1)
            dF = -np.diff(Fall, axis=ax + 1) / DXC
            if ax == 1: dF = dF[[0, 2, 1]]
            R += dF
            out += float((np.take(E1[0], 0, axis=ax).sum() - np.take(E0[0], 0, axis=ax).sum()) * DXC * RHO)
        R[1] += h * atx; R[2] += h * aty
        return R, out

    def step(s, dt, gn, atx, aty):
        R1, o1 = s._rhs(s.U, gn, atx, aty); U1 = s._clean(s.U + dt * R1)
        R2, o2 = s._rhs(U1, gn, atx, aty); U2 = 0.5 * (s.U + U1 + dt * R2)
        s.lost += 0.5 * (o1 + o2) * dt
        h = np.maximum(U2[0], 0.0); f = 1.0 / (1.0 + 3 * NU * dt / np.maximum(h, 1e-6) ** 2)
        U2[1] *= f; U2[2] *= f; s.U = s._clean(U2)

    def _clean(s, U):
        U = U.copy(); neg = U[0] < 0
        U[0] = np.where(s.open, np.maximum(U[0], 0.0), 0.0); dry = U[0] <= HMIN
        U[1] = np.where(dry | ~s.open, 0.0, U[1]); U[2] = np.where(dry | ~s.open, 0.0, U[2]); return U

    def add(s, m, x, y, ux, uy, x0, y0):
        i = ((x - x0) / DXC).astype(int); j = ((y - y0) / DXC).astype(int)
        ok = (i >= 0) & (i < s.nx) & (j >= 0) & (j < s.ny); ok[ok] &= s.open[i[ok], j[ok]]
        dh = m / (RHO * DXC * DXC)
        np.add.at(s.U[0], (i[ok], j[ok]), dh[ok]); np.add.at(s.U[1], (i[ok], j[ok]), (dh * ux)[ok]); np.add.at(s.U[2], (i[ok], j[ok]), (dh * uy)[ok])
        s.added += float(m[ok].sum()); return float(m[~ok].sum())


say("# Fig. 16, kerb ride with control off: the stout on the deck under ideal conditions (model checks)\n")
say("## Check 2: spreading on a still, open plane (axisymmetric viscous gravity current)\n")
n2 = 200; c2 = (np.arange(n2) + 0.5 - n2 / 2) * DXC; X2, Y2 = np.meshgrid(c2, c2, indexing="ij"); r2 = np.hypot(X2, Y2)
V = 20e-6; R0 = 0.030; A0 = 4 * V / (3 * np.pi * R0 ** 2); L = Layer(n2, n2, np.ones((n2, n2), bool), edges="wall")
L.U[0] = np.where(r2 < R0, A0 * np.maximum(1 - (r2 / R0) ** 2, 0) ** (1 / 3), 0.0); L.U[0] *= V / (L.U[0].sum() * DXC * DXC)
K = (1024 / (81 * np.pi ** 3)) ** 0.125; t0 = (R0 / K) ** 8 * 3 * NU / (G0 * V ** 3)   # the similarity time at which R = R0
rows = []; m0 = L.mass(); t = 0.0; ones = np.ones((n2, n2))
for target in (0.25, 0.5, 1.0, 2.0, 4.0):
    while t < target - 1e-12: L.step(DT, G0 * ones, 0 * ones, 0 * ones); t += DT
    h = L.U[0]; rm = np.sqrt(7 / 3 * (h * r2 ** 2).sum() / h.sum()); Rth = K * (G0 * V ** 3 * (t0 + t) / (3 * NU)) ** 0.125
    rows.append(dict(t=t, R_model_mm=rm * 1e3, R_theory_mm=Rth * 1e3, err_pct=100 * (rm / Rth - 1), hmax_mm=float(h.max() * 1e3), hmax_theory_mm=float(4 * V / (3 * np.pi * Rth ** 2) * 1e3)))
say("| t (s) | R model (mm) | R similarity (mm) | error | largest depth model / similarity (mm) |\n|---|---|---|---|---|")
for r in rows: say(f"| {r['t']:.2f} | {r['R_model_mm']:.1f} | {r['R_theory_mm']:.1f} | {r['err_pct']:+.1f} % | {r['hmax_mm']:.3f} / {r['hmax_theory_mm']:.3f} |")
say(f"\nMass {m0 * 1e3:.4f} -> {L.mass() * 1e3:.4f} g (walls far away).")
REP["spreading"] = rows

say("\n## Check 3: a film on a fixed incline (2 degrees), speed against g sin(alpha) h^2 / (3 nu) with the local depth\n")
nx, ny = int(round(2 * DECK[0] / DXC)), int(round(2 * DECK[1] / DXC))
xc = -DECK[0] + (np.arange(nx) + 0.5) * DXC; yc = -DECK[1] + (np.arange(ny) + 0.5) * DXC
XX, YY = np.meshgrid(xc, yc, indexing="ij"); OPEN = np.hypot(XX, YY) >= RFOOT
al = np.radians(2.0); L = Layer(nx, ny, OPEN); L.U[0][OPEN] = 0.001; one = np.ones((nx, ny))
for _ in range(int(1.0 / DT)): L.step(DT, G0 * np.cos(al) * one, G0 * np.sin(al) * one, 0 * one)
mid = (np.abs(XX) < 0.03) & (np.abs(YY) > 0.04) & OPEN & (L.U[0] > 1e-5)
hm = L.U[0][mid]; um = L.U[1][mid] / hm; uth = G0 * np.sin(al) * hm ** 2 / (3 * NU)
REP["incline"] = dict(u_mean=float(um.mean()), u_theory_local_mean=float(uth.mean()), ratio=float(np.mean(um / uth)), h_mean=float(hm.mean()))
say(f"Middle of the deck after 1 s: mean depth {hm.mean() * 1e3:.3f} mm, speed {um.mean() * 1e3:.2f} mm/s, law with the local depth {uth.mean() * 1e3:.2f} mm/s, "
    f"ratio {np.mean(um / uth):.3f}.")

say("\n## The deck frame from the stored cart state\n")
src = glob.glob(f"/kaggle/input/**/{SUB}/{RIDE}.npz", recursive=True)
if src:
    Z = np.load(src[0]); t_ = Z["t"].astype(float); gxs, gzs = Z["gx"].astype(float), Z["gz"].astype(float)
    v, vzc, th_, om = (Z[k].astype(float) for k in ("v", "vzc", "th", "om"))
    dtp = np.diff(t_); ax_c = np.diff(v) / dtp; az_c = np.diff(vzc) / dtp; alp = np.diff(om) / dtp; thm = 0.5 * (th_[1:] + th_[:-1]); omm = 0.5 * (om[1:] + om[:-1])
    def geff(rx, rz, s1, s2):
        c, s = np.cos(s1 * thm), np.sin(s1 * thm); wx, wz = c * rx - s * rz, s * rx + c * rz; o, a = s2 * omm, s2 * alp
        apx = ax_c + a * wz - o * o * wx; apz = az_c - a * wx - o * o * wz; gx_w, gz_w = -apx, -G0 - apz
        return c * gx_w + s * gz_w, -s * gx_w + c * gz_w
    best = None
    for sg in ((1, 1), (1, -1), (-1, 1), (-1, -1)):
        a, b = geff(0.0, HG, *sg); d = np.hypot(a - 0.5 * (gxs[1:] + gxs[:-1]), b - 0.5 * (gzs[1:] + gzs[:-1]))
        if best is None or np.sqrt(np.mean(d ** 2)) < best[1]: best = (sg, float(np.sqrt(np.mean(d ** 2))), d)
    sg, rms, d = best; kk = int(np.argmax(np.abs(np.diff(v)))); win = np.abs(np.arange(len(d)) - kk) <= 6
    REP["frame"] = dict(signs=sg, rms=rms, rms_within_0_1s_of_kerb=float(np.sqrt(np.mean(d[win] ** 2))), rms_elsewhere=float(np.sqrt(np.mean(d[~win] ** 2))),
                        largest=float(d.max()), t_largest=float(0.5 * (t_[1:] + t_[:-1])[np.argmax(d)]), t_kerb=float(t_[kk + 1]))
    f = REP["frame"]
    say(f"Signs {sg}; rms miss against the stored effective gravity {rms:.2f} m/s^2: within 0.1 s of the kerb shock (t = {f['t_kerb']:.2f} s) "
        f"{f['rms_within_0_1s_of_kerb']:.2f}, elsewhere {f['rms_elsewhere']:.2f}; largest {f['largest']:.2f} at t = {f['t_largest']:.2f} s. "
        "(The stored values are samples at the pictures; these are interval means, so a shock shows as a miss.)")
else: say("stored ride not attached: frame not checked")
json.dump(REP, open(os.path.join(OUT, "report.json"), "w"), indent=1, default=float)
open(os.path.join(OUT, "REPORT.md"), "w").write("\n".join(MD) + "\n")

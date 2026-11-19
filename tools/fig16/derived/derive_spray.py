"""Fig. 16, kerb ride with control off: the spray's velocities DERIVED from the stored ride, not recomputed (19 Nov 2026). Kaggle CPU.
Dataset numakoudsie/fig16-guinness-cart-control attached.  python3 derive_spray.py OUTDIR

THE OWNER'S METHOD. No recomputation. The stored ride is the solution of a model that is right inside the glass and wrong outside it;
the missing quantities are derived from what it stores, with book physics, and checked against what it stores.

THE PHYSICS. Stout in the air has atmospheric pressure all round it, so each parcel obeys Dv/Dt = a(t), the stored effective gravity of
the glass's frame (gx, gz): the cloud is a pressureless fluid of non-colliding parcels. Between two moments its mass is carried by
the map T(x) = x + v dt + a dt^2 / 2, which is the optimal-transport map for the quadratic cost between the two distributions (Brenier
1991; Benamou & Brenier, Numer. Math. 84 (2000) 375; Villani, Topics in Optimal Transportation, AMS 2003, ch. 2 and 8: for
non-crossing ballistic motion over a short interval the displacement map is the gradient of a convex function, hence the quadratic-cost
optimal map). Each stored picture lists an EVEN subsample of the drops, so it samples the mass distribution faithfully even where single
drops cannot be followed (step 1, measure_stored.py). So:
  v(x_k) = (T(x_k) - x_k) / dt - a_k dt / 2,     T: the optimal map from picture k's cloud to picture k+1's.
Mass enters (over the rim) and leaves (frozen on the old plane, or below -250 mm) between pictures, so T is a PARTIAL optimal transport
of the mass the two pictures share (Figalli, Arch. Ration. Mech. Anal. 195 (2010) 533), computed with POT (Flamary et al., JMLR 22
(2021) 1), exact partial transport as a linear program (no regularisation).

CHECKS AGAINST THE STORED RIDE (the weir estimate failed exactly these):
 1. Parcels flown on from their derived (x, v) under the stored a(t) must come down on Fig. 12's body plane (z = -14 mm, 220 x 120 mm)
    where the stored ride froze its drops: mass, centroid, spread, share in front of the glass.
 2. The mass that misses that plane must match the stored 43.3 g that fell past its edge.
 3. Transport residual: the cloud of picture k moved by (v, a) against picture k+1, as a Wasserstein distance, against the distance
    with no motion.
OUTPUT: REPORT.md, report.json, spray_velocities.npz (per picture: positions, derived velocities, weights in grams), check figures."""
import glob, json, os, subprocess, sys, time
import numpy as np
subprocess.run([sys.executable, "-m", "pip", "install", "-q", "POT==0.9.4"], capture_output=True)
import ot
OUT = sys.argv[1] if len(sys.argv) > 1 else "/kaggle/working"; os.makedirs(OUT, exist_ok=True)
SUB = "fig-16-guinness-cart-with-control/v8/output/2026-11-15"; RIDE = "kerb_off"
ZRIM, RRIM = 0.1475, 0.03747; OLD = (0.11, 0.06, -0.014); M = int(os.environ.get("M", "1500")); REG = float(os.environ.get("REG", "2e-6"))
MD = []; say = lambda s="": (print(s, flush=True), MD.append(s)); REP = {}
src = glob.glob(f"/kaggle/input/**/{SUB}/{RIDE}.npz", recursive=True)
Z = np.load(src[0]); t = Z["t"].astype(float); nf = len(t); mp = float(Z["mp"]); D = Z["drops"].astype(np.float64)
nd = Z["ndrops"].astype(float); nst = Z["nstuck"].astype(float); nland = Z["nlanded"].astype(float); gx, gz = Z["gx"].astype(float), Z["gz"].astype(float)
dt = float(np.median(np.diff(t)))


def cloud(k):
    """Drops of picture k in the air outside the glass (not frozen on the old plane, not inside the cavity or the cylinder above the rim),
    each with the mass it stands for (kg): true count / listed count of its picture."""
    X = D[k][np.isfinite(D[k]).all(1)]
    if not len(X): return X, np.zeros(0)
    w = nd[k] / len(X) * mp
    r = np.hypot(X[:, 0], X[:, 1]); inside = (X[:, 2] > 0) & (r < RRIM + 0.004) & (X[:, 2] < ZRIM + 0.05)
    frozen = np.abs(X[:, 2] - OLD[2]) < 4e-4
    keep = ~inside & ~frozen
    return X[keep], np.full(keep.sum(), w)


say("# Fig. 16, kerb ride with control off: the spray's velocities derived from the stored ride (partial optimal transport)\n")
rng = np.random.default_rng(1); VEL = []; resid = []
for k in range(nf - 1):
    X0, w0 = cloud(k); X1, w1 = cloud(k + 1)
    if len(X0) < 20 or len(X1) < 20: continue
    i0 = rng.choice(len(X0), min(M, len(X0)), replace=False); i1 = rng.choice(len(X1), min(M, len(X1)), replace=False)
    A, B = X0[i0], X1[i1]; mA = w0[i0] * len(X0) / len(i0); mB = w1[i1] * len(X1) / len(i1)       # grams carried by each sample point
    a = np.array([gx[k], 0.0, gz[k]]); Bs = B - 0.5 * a * dt * dt                                   # remove gravity's own part of the step
    share = min(mA.sum(), mB.sum())
    C = ot.dist(A, Bs)                                                                               # squared distances, m^2
    P = ot.partial.partial_wasserstein(mA / mA.sum(), mB / mB.sum(), C / C.max(), m=0.999 * share / max(mA.sum(), mB.sum()), nb_dummy=200)   # exact LP (19 Nov: the entropic version underflowed)
    row = P.sum(1); ok = row > 1e-12
    if ok.sum() < 5: continue
    T = (P @ B)[ok] / row[ok, None]
    v = (T - A[ok]) / dt - 0.5 * a * dt
    VEL.append((k, A[ok], v, mA[ok]))
    moved = A[ok] + v * dt + 0.5 * a * dt * dt
    w_moved = ot.emd2(np.full(len(moved), 1 / len(moved)), np.full(len(B), 1 / len(B)), ot.dist(moved, B)); w_still = ot.emd2(np.full(len(A), 1 / len(A)), np.full(len(B), 1 / len(B)), ot.dist(A, B))
    resid.append((t[k], np.sqrt(w_moved) * 1e3, np.sqrt(w_still) * 1e3))
say(f"Picture pairs with a spray to transport: {len(VEL)} of {nf - 1}; sample points per picture {M}; exact partial transport (linear program).")
R = np.array(resid); REP["transport_residual_mm"] = dict(moved_median=float(np.median(R[:, 1])), still_median=float(np.median(R[:, 2])))
say(f"Check 3, transport residual (Wasserstein-2 to the next picture): moved by (v, a) {np.median(R[:, 1]):.2f} mm (median), not moved {np.median(R[:, 2]):.2f} mm.\n")

# ---------------------------------------------------------------- checks 1 and 2: fly every derived parcel on to Fig. 12's body plane
# each parcel is followed from the FIRST picture it is seen in near the rim only once: take parcels within 15 mm of the rim's height,
# weighted by the mass that left the rim in that picture interval (exact, from nact), so that each gram is counted once
nact = Z["nact"].astype(float); dm_rim = np.r_[np.maximum(nact[:-1] - nact[1:], 0.0), 0.0] * mp
land = []
for (k, X, v, m) in VEL:
    near = (X[:, 2] > ZRIM - 0.015)
    if not near.any() or dm_rim[k] <= 0: continue
    Xn, vn = X[near], v[near]; mn = np.full(near.sum(), dm_rim[k] / near.sum())
    x, vv, tt = Xn.copy(), vn.copy(), t[k]; alive = np.ones(len(x), bool); hit = np.zeros(len(x), bool); hx = np.zeros(len(x)); hy = np.zeros(len(x))
    for _ in range(2000):
        if not alive.any(): break
        aa = np.array([np.interp(tt, t, gx), 0.0, np.interp(tt, t, gz)]); vv[alive] += aa * 1e-3; x[alive] += vv[alive] * 1e-3; tt += 1e-3
        down = alive & (x[:, 2] <= OLD[2]); onb = down & (np.abs(x[:, 0]) < OLD[0]) & (np.abs(x[:, 1]) < OLD[1])
        hit |= onb; hx[onb], hy[onb] = x[onb, 0], x[onb, 1]; alive &= ~down
    land.append((hit, hx, hy, mn))
H = np.concatenate([l[0] for l in land]); HX = np.concatenate([l[1] for l in land]); HY = np.concatenate([l[2] for l in land]); MN = np.concatenate([l[3] for l in land])
Dl = D[-1][np.isfinite(D[-1]).all(1)]; st = Dl[np.abs(Dl[:, 2] - OLD[2]) < 4e-4]
der = dict(on_plane_g=float(MN[H].sum() * 1e3), missed_g=float(MN[~H].sum() * 1e3), followed_g=float(MN.sum() * 1e3),
           centroid_mm=[float(np.average(HX[H], weights=MN[H]) * 1e3), float(np.average(HY[H], weights=MN[H]) * 1e3)] if H.any() else None,
           spread_mm=[float(np.sqrt(np.cov(HX[H], aweights=MN[H])) * 1e3), float(np.sqrt(np.cov(HY[H], aweights=MN[H])) * 1e3)] if H.sum() > 2 else None,
           front=float(MN[H & (HX > 0)].sum() / max(MN[H].sum(), 1e-30)))
sto = dict(on_plane_g=float(nst[-1] * mp * 1e3), missed_g=float(nland[-1] * mp * 1e3), centroid_mm=[float(st[:, 0].mean() * 1e3), float(st[:, 1].mean() * 1e3)],
           spread_mm=[float(st[:, 0].std() * 1e3), float(st[:, 1].std() * 1e3)], front=float(np.mean(st[:, 0] > 0)))
REP["check_old_plane"] = dict(derived=der, stored=sto)
say("## Checks 1 and 2: the derived parcels flown on to Fig. 12's body plane, against the stored ride\n")
say("| | stored ride | derived (optimal transport) | earlier weir estimate (rejected) |\n|---|---|---|---|")
say(f"| on the plane (g) | {sto['on_plane_g']:.1f} | {der['on_plane_g']:.1f} | 27.0 |")
say(f"| past its edge (g) | {sto['missed_g']:.1f} | {der['missed_g']:.1f} | 7.0 (+41.5 down the glass) |")
say(f"| centroid x, y (mm) | {[round(v_, 1) for v_ in sto['centroid_mm']]} | {[round(v_, 1) for v_ in der['centroid_mm']] if der['centroid_mm'] else None} | [-19.4, -2.8] |")
say(f"| spread x, y (mm) | {[round(v_, 1) for v_ in sto['spread_mm']]} | {[round(v_, 1) for v_ in der['spread_mm']] if der['spread_mm'] else None} | [43.5, 39.0] |")
say(f"| share in front (x > 0) | {sto['front']:.2f} | {der['front']:.2f} | 0.30 |")
say(f"\nMass followed from the rim: {der['followed_g']:.1f} g of the {dm_rim.sum() * 1e3:.1f} g over the rim (pictures with a spray near the rim).")
np.savez_compressed(os.path.join(OUT, "spray_velocities.npz"), k=np.concatenate([np.full(len(x), k) for (k, x, v, m) in VEL]),
                    x=np.concatenate([x for (k, x, v, m) in VEL]), v=np.concatenate([v for (k, x, v, m) in VEL]), m=np.concatenate([m for (k, x, v, m) in VEL]))
json.dump(REP, open(os.path.join(OUT, "report.json"), "w"), indent=1, default=float); open(os.path.join(OUT, "REPORT.md"), "w").write("\n".join(MD) + "\n")

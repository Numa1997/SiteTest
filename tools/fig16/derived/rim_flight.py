"""Fig. 16, spill derived from a stored ride, step 2 (19 Nov 2026): the stout leaving the rim, its flight, where it lands on Fig. 16's deck.
Kaggle CPU; nothing runs outside Kaggle. Run on Kaggle with the dataset numakoudsie/fig16-guinness-cart-control attached:
    python3 rim_flight.py OUTDIR        (env RIDE, default kerb_off)

WHY THIS IS LEGITIMATE. The stored ride (old model) is verified inside the glass. Stout that crosses the rim never returns, so the flow
in the glass does not depend on what the spilled stout does afterwards: the stored ride is the source term.

WHAT IS EXACT IN THE STORED RIDE. Per picture (60 a second): the number of particles still in the glass, nact, so the mass over the rim
per picture, dm_k = (nact_{k-1} - nact_k) mp; the surface height H of each 1.5 mm column of the cavity (57 x 57); the effective gravity
of the glass's frame (gx, gz). NOT stored: the drops' velocities, nor which drop is which from one picture to the next (step 1,
measure_stored.py: matching failed).

THE EXIT SPEED, from mass conservation (a weir). Where the stout stands above the rim (columns within 2 cells of the wall, H > z_rim),
the overflow height is h(theta) = H - z_rim. The flux over a weir of length ds and head h goes as h^(3/2) (broad-crested weir; Henderson,
Open Channel Flow, ch. 6); the stored dm_k fixes its magnitude. Each picture's mass is shared over the overflowing arc in proportion to
h^(3/2) ds, and leaves horizontally, outward along the radius (the weir's crest flow), at the speed u = dm_k / (rho dt sum h ds): the mean
speed through the overflow section. The vertical speed at the crest is taken as zero.

THE FLIGHT. Each parcel then moves under the stored effective gravity of its moment (gx(t), gz(t), linear between pictures), in the
glass's frame, step 1 ms. Left out: the deck's pitch rate and angular acceleration (the frame's rotation; stored om, al, at most
5.8 rad/s), air drag, surface tension. A parcel that comes back inside the outside of the glass (r < R(z) + 2.5 mm, 0 < z < z_rim) has
met the glass: it runs down the glass and reaches the deck at the glass's foot.

THE CHECK AGAINST THE STORED RIDE. The stored ride froze every drop that came down on Fig. 12's body (the plane z = -14 mm, 220 x 120
mm) and stored those positions. The same parcels are also landed here on that plane; the two landing patterns (centroid, spread, share
in front of / behind the glass) are compared. Agreement says the exit speed and direction are right; disagreement is reported as such.

OUTPUT: REPORT.md, report.json, landing_deck.png, check_old_body.png, exit.png, parcels.npz (per parcel: exit time, angle, speed, mass,
landing point and time on Fig. 16's deck plane, fate)."""
import glob, json, os, sys, time, urllib.request
import numpy as np

OUT = sys.argv[1] if len(sys.argv) > 1 else "/kaggle/working"; os.makedirs(OUT, exist_ok=True)
P = dict(RIDE=os.environ.get("RIDE", "kerb_off"), SUBPATH="fig-16-guinness-cart-with-control/v8/output/2026-11-15",
         GLASS_URL="https://raw.githubusercontent.com/Numa1997/SiteTest/main/public/scripts/guinness-glass.js",
         DZP=0.0005, WALL=0.0025, RHO=1007.0, DECK=(0.155, 0.062, -0.030), OLD=(0.11, 0.06, -0.014), DT=0.001, TMAX=1.5,
         RIM_BAND_CELLS=2.0, PARCELS_PER_PICTURE=400)
T0 = time.time(); MD = []; REP = {"params": P}
say = lambda s="": (print(s, flush=True), MD.append(s))

src = glob.glob(f"/kaggle/input/**/{P['SUBPATH']}/{P['RIDE']}.npz", recursive=True)
if not src: say("STOP: the stored ride is not attached under /kaggle/input."); open(os.path.join(OUT, "REPORT.md"), "w").write("\n".join(MD)); sys.exit(1)
Z = np.load(src[0])
js = urllib.request.urlopen(P["GLASS_URL"], timeout=30).read().decode()
Rp = np.array([float(v) for v in js.split("R: [")[1].split("]")[0].split(",")])
ZRIM = (len(Rp) - 1) * P["DZP"]; RRIM = float(Rp[-1])
Rz = lambda z: np.interp(np.clip(np.asarray(z) / P["DZP"], 0, len(Rp) - 1.001), np.arange(len(Rp)), Rp)
t = Z["t"].astype(float); nf = len(t); dtp = float(np.median(np.diff(t))); N = int(Z["N"]); mp = float(Z["mp"])
nact = Z["nact"].astype(float); H = Z["H"].astype(float); dx = float(Z["dx"]); x0 = float(Z["x0"]); n = int(Z["n"])
gx = Z["gx"].astype(float); gz = Z["gz"].astype(float)
c = x0 + (np.arange(n) + 0.5) * dx; X, Y = np.meshgrid(c, c, indexing="ij"); Rc = np.hypot(X, Y); TH = np.arctan2(Y, X)
band = Rc > RRIM - P["RIM_BAND_CELLS"] * dx
say(f"# Fig. 16, ride `{P['RIDE']}`: the stout over the rim, its flight, its landing (derived from the stored ride)\n")
say(f"Stored ride: {nf} pictures, {1 / dtp:.0f} a second; {N:,} particles of {mp * 1e6:.3f} mg. Glass: rim at z = {ZRIM * 1e3:.1f} mm, radius {RRIM * 1e3:.2f} mm.")
say(f"Rim band: the {int(band.sum())} columns whose centres lie within {P['RIM_BAND_CELLS']:.0f} cells of the rim's radius.\n")

# ---------------------------------------------------------------- exit: mass per picture, shared over the overflowing arc
dm = np.r_[0.0, np.maximum(nact[:-1] - nact[1:], 0.0)] * mp          # kg over the rim in each picture's interval
parcels = []; nohead = 0; exit_rows = []
ds_col = dx                                                            # each band column stands for one cell of rim length
for k in range(1, nf):
    if dm[k] <= 0: continue
    h = np.where(band & np.isfinite(H[k]), H[k] - ZRIM, -1.0); m = h > 0
    if not m.any():
        # no column reads above the rim at this picture: the stout leaves where the band stands highest (a crest between columns)
        hb = np.where(band & np.isfinite(H[k]), H[k], -np.inf); j = np.unravel_index(np.argmax(hb), hb.shape); m = np.zeros_like(band); m[j] = True
        h = np.where(m, max(float(H[k][j] - ZRIM), 0.5 * dx), -1.0); nohead += 1
    w = np.where(m, h ** 1.5, 0.0); w /= w.sum()
    u = dm[k] / (P["RHO"] * dtp * float(np.sum(np.where(m, h, 0.0)) * ds_col))
    exit_rows.append(dict(t=t[k], dm_g=dm[k] * 1e3, arc_cols=int(m.sum()), h_max_mm=float(h[m].max() * 1e3), u=u))
    # parcels: PARCELS_PER_PICTURE per picture, each carrying an equal share of dm, placed on the arc by the weights, leaving at
    # times spread over the picture's interval
    idx = np.random.default_rng(k).choice(w.size, P["PARCELS_PER_PICTURE"], p=w.ravel())
    th = TH.ravel()[idx]; te = t[k - 1] + dtp * (np.arange(P["PARCELS_PER_PICTURE"]) + 0.5) / P["PARCELS_PER_PICTURE"]
    for a, tt in zip(th, te): parcels.append((tt, a, u, dm[k] / P["PARCELS_PER_PICTURE"]))
pa = np.array(parcels); REP["exit"] = exit_rows
say(f"Mass over the rim: {dm.sum() * 1e3:.1f} g in {len(exit_rows)} pictures; pictures with no column above the rim (crest between columns): {nohead}.")
U = np.array([r["u"] for r in exit_rows]); Wt = np.array([r["dm_g"] for r in exit_rows])
say(f"Exit speed through the overflow (mass-weighted): 10 / 50 / 90 % = {np.percentile(np.repeat(U, np.maximum(1, (Wt * 10).astype(int))), [10, 50, 90]).round(2).tolist()} m/s.\n")

# ---------------------------------------------------------------- flight under the stored effective gravity
def fly(zstop, half):
    """All parcels from the rim's outer edge (radius RRIM + WALL, height ZRIM) under g(t) until z = zstop. Returns landing x, y, time, fate."""
    tt, th, u, mass = pa.T; nP = len(tt)
    x = (RRIM + P["WALL"]) * np.cos(th); y = (RRIM + P["WALL"]) * np.sin(th); z = np.full(nP, ZRIM)   # the outer edge of the rim
    vx = u * np.cos(th); vy = u * np.sin(th); vz = np.zeros(nP)
    t_ = tt.copy(); done = np.zeros(nP, bool); fate = np.zeros(nP, int)  # 0 flying, 1 on the plane, 2 down the glass, 3 past the plane's edge
    for _ in range(int(P["TMAX"] / P["DT"])):
        live = ~done
        if not live.any(): break
        ax = np.interp(t_[live], t, gx); az = np.interp(t_[live], t, gz)
        vx[live] += ax * P["DT"]; vz[live] += az * P["DT"]
        x[live] += vx[live] * P["DT"]; y[live] += vy[live] * P["DT"]; z[live] += vz[live] * P["DT"]; t_[live] += P["DT"]
        r = np.hypot(x, y)
        glass = live & (z > 0) & (z < ZRIM) & (r < Rz(np.maximum(z, 0.008)) + P["WALL"])
        fate[glass] = 2; done |= glass
        down = live & ~glass & (z <= zstop)
        on = down & (np.abs(x) < half[0]) & (np.abs(y) < half[1])
        fate[on] = 1; fate[down & ~on] = 3; done |= down
    return x, y, t_, fate, mass

res = {}
for name, (hx, hy, zp) in (("deck", P["DECK"]), ("old body", P["OLD"])):
    x, y, tl, fate, mass = fly(zp, (hx, hy)); M = mass.sum()
    res[name] = dict(on_plane_g=float(mass[fate == 1].sum() * 1e3), down_glass_g=float(mass[fate == 2].sum() * 1e3),
                     past_edge_g=float(mass[fate == 3].sum() * 1e3), still_flying_g=float(mass[fate == 0].sum() * 1e3),
                     centroid_mm=[float(np.average(x[fate == 1], weights=mass[fate == 1]) * 1e3), float(np.average(y[fate == 1], weights=mass[fate == 1]) * 1e3)] if (fate == 1).any() else None,
                     front_share=float(mass[(fate == 1) & (x > 0)].sum() / max(mass[fate == 1].sum(), 1e-12)))
    res[name + "_xy"] = (x, y, fate, mass)
    say(f"**{name}** (plane z = {zp * 1e3:.0f} mm, {2 * hx * 1e3:.0f} x {2 * hy * 1e3:.0f} mm): on it {res[name]['on_plane_g']:.1f} g, down the glass {res[name]['down_glass_g']:.1f} g, "
        f"past its edge {res[name]['past_edge_g']:.1f} g, still in the air after {P['TMAX']} s {res[name]['still_flying_g']:.1f} g; landed centroid {res[name]['centroid_mm']} mm, share in front (x > 0) {100 * res[name]['front_share']:.0f} %.")
REP["landing"] = {k: v for k, v in res.items() if not k.endswith("_xy")}

# ---------------------------------------------------------------- the check: the stored ride's own frozen drops on the old body plane
D = Z["drops"][-1].astype(float); D = D[np.isfinite(D).all(1)]
st = D[np.abs(D[:, 2] - P["OLD"][2]) < 4e-4]
nst = float(Z["nstuck"][-1]); share_stored = len(st) / max(nst, 1)
chk = dict(stored_frozen_particles=nst, listed=len(st), stored_frozen_g=nst * mp * 1e3,
           stored_centroid_mm=[float(st[:, 0].mean() * 1e3), float(st[:, 1].mean() * 1e3)] if len(st) else None,
           stored_front_share=float(np.mean(st[:, 0] > 0)) if len(st) else None,
           stored_spread_mm=[float(st[:, 0].std() * 1e3), float(st[:, 1].std() * 1e3)] if len(st) else None)
xo, yo, fo, mo = res["old body_xy"]; on = fo == 1
chk.update(derived_on_old_body_g=res["old body"]["on_plane_g"], derived_centroid_mm=res["old body"]["centroid_mm"],
           derived_front_share=res["old body"]["front_share"],
           derived_spread_mm=[float(np.sqrt(np.average((xo[on] - np.average(xo[on], weights=mo[on])) ** 2, weights=mo[on])) * 1e3),
                              float(np.sqrt(np.average((yo[on] - np.average(yo[on], weights=mo[on])) ** 2, weights=mo[on])) * 1e3)] if on.any() else None)
REP["check_old_body"] = chk
say("\n## Check against the stored ride (Fig. 12's body plane, z = -14 mm, 220 x 120 mm)\n")
say("| | stored ride (computed) | derived here |\n|---|---|---|")
say(f"| stout frozen on the plane (g) | {chk['stored_frozen_g']:.1f} | {chk['derived_on_old_body_g']:.1f} |")
say(f"| centroid x, y (mm) | {chk['stored_centroid_mm']} | {chk['derived_centroid_mm']} |")
say(f"| spread x, y (mm, standard deviation) | {chk['stored_spread_mm']} | {chk['derived_spread_mm']} |")
say(f"| share in front of the glass (x > 0) | {chk['stored_front_share']} | {chk['derived_front_share']} |")
say(f"(The stored list at the last picture holds {len(st):,} of the {nst:,.0f} frozen particles, an even subsample.)\n")

try:
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    for name, fn in (("deck", "landing_deck.png"), ("old body", "check_old_body.png")):
        x, y, fate, mass = res[name + "_xy"]; hx, hy, zp = P["DECK"] if name == "deck" else P["OLD"]
        fig, ax = plt.subplots(figsize=(8, 3.8)); s = fate == 1
        ax.scatter(x[s] * 1e3, y[s] * 1e3, s=1, c="tab:blue", label="lands on the plane")
        ax.scatter(x[fate == 3] * 1e3, y[fate == 3] * 1e3, s=1, c="tab:red", label="past the edge")
        if name == "old body" and len(st): ax.scatter(st[:, 0] * 1e3, st[:, 1] * 1e3, s=1, c="k", alpha=0.3, label="stored ride's frozen drops")
        ax.add_patch(plt.Rectangle((-hx * 1e3, -hy * 1e3), 2e3 * hx, 2e3 * hy, fill=False, lw=1.5)); ax.add_patch(plt.Circle((0, 0), (float(Rz(0.008)) + P["WALL"]) * 1e3, fill=False, lw=1))
        ax.set_aspect("equal"); ax.set_xlim(-350, 350); ax.set_ylim(-170, 170); ax.set_xlabel("x along the road (mm)"); ax.set_ylabel("y (mm)"); ax.legend(fontsize=7, markerscale=6)
        ax.set_title(f"{P['RIDE']}: where the spilled stout comes down on the {name} plane (z = {zp * 1e3:.0f} mm)"); fig.tight_layout(); fig.savefig(os.path.join(OUT, fn), dpi=130); plt.close(fig)
    fig, ax = plt.subplots(2, 1, figsize=(8, 5), sharex=True)
    ax[0].bar([r["t"] for r in exit_rows], [r["dm_g"] for r in exit_rows], width=dtp); ax[0].set_ylabel("over the rim per picture (g)")
    ax[1].plot([r["t"] for r in exit_rows], [r["u"] for r in exit_rows], ".-"); ax[1].set_ylabel("exit speed (m/s)"); ax[1].set_xlabel("t (s)")
    fig.tight_layout(); fig.savefig(os.path.join(OUT, "exit.png"), dpi=130); plt.close(fig)
except Exception as e: REP["figures_error"] = str(e)
x, y, tl, fate, mass = fly(P["DECK"][2], P["DECK"][:2])
np.savez_compressed(os.path.join(OUT, "parcels.npz"), t_exit=pa[:, 0], theta=pa[:, 1], u=pa[:, 2], mass=pa[:, 3], x=x, y=y, t_land=tl, fate=fate)
REP["wall_s"] = round(time.time() - T0, 1); say(f"\nWall time {REP['wall_s']} s on Kaggle CPU.")
json.dump(REP, open(os.path.join(OUT, "report.json"), "w"), indent=1, default=float); open(os.path.join(OUT, "REPORT.md"), "w").write("\n".join(MD) + "\n")

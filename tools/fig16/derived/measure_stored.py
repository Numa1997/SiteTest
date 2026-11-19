"""Fig. 16, spill derived from the stored rides: step 1, what the stored data allows (19 Nov 2026). Kaggle CPU, no GPU.

THE IDEA (the owner, 19 Nov 2026). No ride is recomputed. The stored rides were computed with the old model: inside the glass the stout
is a liquid (correct, the pint at rest holds); a particle that crosses the rim becomes a drop in free flight and is frozen where it
lands. Liquid over the rim never returns, so the flow inside the glass does not depend on what the spilled liquid does afterwards.
The stored rides are therefore a valid SOURCE for a second, cheap computation of the liquid outside the glass (its flight with air
drag, its landing on the deck, the puddle, the run-off over the deck's edge).

THIS NOTEBOOK ONLY MEASURES whether the stored data is enough for that. It answers:
  Q1  what arrays one stored ride holds (names, shapes), and the books (how much leaves the rim, when);
  Q2  whether the drops listed per stored picture are complete or a subsample;
  Q3  whether a drop keeps its place in the list from one picture to the next (identity);
  Q4  whether the drops' velocities, which are NOT stored, can be recovered: a drop in free flight obeys x(t+dt) - 2 x(t) + x(t-dt)
      = a dt^2 with a the stored effective gravity of the glass's frame, so for each drop we look for the pair (one drop in the
      picture before, one in the picture after) that satisfies this best, and ask how small the residual is and how unique;
  Q5  with those velocities: how fast the stout leaves the rim (and its Weber number, inertia against surface tension), and where
      it would land on the true deck of Fig. 16 (310 x 124 mm, its top 30 mm below the glass's inner floor);
  Q6  how hard the deck shakes (the effective gravity along the deck), which decides whether a puddle can stay on it.

INPUT. numakoudsie/fig16-guinness-cart-control, file fig-16-guinness-cart-with-control/v8/output/2026-11-15/<RIDE>.npz, written by
tools/fig16/kaggle/run16.py (repository Numa1997/SiteTest). Positions are in the glass's frame: origin on the glass's axis at its
inner floor, x along the road, z up the glass, metres. The glass's profile R(z) comes from public/scripts/guinness-glass.js.

OUTPUT (/kaggle/working): REPORT.md (the findings in words and numbers), report.json (every number), params.json, three figures.
Nothing here changes any stored ride, dataset, page or repository.
"""
import glob, json, os, sys, time, traceback, urllib.request
import numpy as np

# ---------------------------------------------------------------- parameters (all here, echoed to params.json)
P = dict(
    DATASET="numakoudsie/fig16-guinness-cart-control",
    RIDE=os.environ.get("RIDE", "kerb_off"),
    SUBPATH="fig-16-guinness-cart-with-control/v8/output/2026-11-15",
    GLASS_URL="https://raw.githubusercontent.com/Numa1997/SiteTest/main/public/scripts/guinness-glass.js",
    DZP=0.0005,            # m, spacing of the glass profile's points
    WALL=0.0025,           # m, glass wall thickness (stout_jax.Geometry.WALL)
    DECK_HX=0.155, DECK_HY=0.062,   # m, half length and half width of Fig. 16's deck (run16.py DECK)
    DECK_Z=-0.030,         # m, the deck's top below the glass's inner floor (cart4.FLOOR_ABOVE_DECK)
    OLD_BODY_Z=-0.014,     # m, where the old model froze landed drops (stout_jax.BODY_TOP, Fig. 12's body)
    RHO=1007.0, GAMMA=0.0442,       # kg/m^3, N/m (stout_jax)
    H_SHEET=0.003,         # m, thickness assumed for the sheet leaving the rim, for the Weber number only (an assumption)
    VMAX=4.0,              # m/s, the largest drop speed searched for when matching
    NSAMP=1500,            # drops sampled per tested picture for the matching
    NFRAMES=24,            # pictures tested, spread over the ride
    TOL=0.0006,            # m, a match is accepted when the free-flight residual is below this
    SEED=1,
)
OUT = "/kaggle/working"; os.makedirs(OUT, exist_ok=True)
json.dump(P, open(os.path.join(OUT, "params.json"), "w"), indent=1)
REP = {"params": P, "errors": []}; MD = []
T0 = time.time()


def say(s=""):
    print(s, flush=True); MD.append(s)


def finish(code=0):
    REP["wall_s"] = round(time.time() - T0, 1)
    json.dump(REP, open(os.path.join(OUT, "report.json"), "w"), indent=1, default=float)
    open(os.path.join(OUT, "REPORT.md"), "w").write("\n".join(MD) + "\n")
    sys.exit(code)


def guard(name):
    def deco(fn):
        def run(*a, **k):
            try: return fn(*a, **k)
            except Exception as e:
                REP["errors"].append({name: traceback.format_exc()[-1500:]}); say(f"\n**{name} FAILED:** `{type(e).__name__}: {e}`\n")
        return run
    return deco


say(f"# Fig. 16: what the stored ride `{P['RIDE']}` allows for a derived spill\n")
say("Kaggle CPU, no GPU. Written by this notebook; every number is also in report.json. The method is in the notebook's header.\n")

# ---------------------------------------------------------------- the stored ride
src = None; how = None
hits = glob.glob(f"/kaggle/input/**/{P['SUBPATH']}/{P['RIDE']}.npz", recursive=True)
if hits: src, how = hits[0], "dataset attached to the notebook"
else:
    try:
        import kagglehub
        base = kagglehub.dataset_download(P["DATASET"])
        hits = glob.glob(os.path.join(base, "**", f"{P['RIDE']}.npz"), recursive=True)
        hits = [h for h in hits if P["SUBPATH"] in h.replace(os.sep, "/")] or hits
        if hits: src, how = hits[0], "kagglehub download inside the notebook"
    except Exception as e:
        REP["errors"].append({"dataset": traceback.format_exc()[-1500:]})
if src is None:
    say("**STOP: the stored ride could not be read** (neither attached under /kaggle/input nor by kagglehub). See report.json.")
    say("Contents of /kaggle/input: " + ", ".join(sorted(glob.glob('/kaggle/input/*'))[:20]))
    finish(1)
Z = np.load(src); REP["source"] = dict(path=src, how=how, bytes=os.path.getsize(src))
say(f"Source: `{src}` ({os.path.getsize(src) / 1e6:.1f} MB), read by: {how}.\n")

# glass profile
try:
    js = urllib.request.urlopen(P["GLASS_URL"], timeout=30).read().decode()
    Rp = np.array([float(v) for v in js.split("R: [")[1].split("]")[0].split(",")]); REP["glass"] = "profile from the repository"
except Exception as e:
    Rp = np.full(296, 0.0385); REP["glass"] = f"FALLBACK cylinder 38.5 mm ({e})"; say("**Glass profile not fetched; a cylinder of 38.5 mm is used (numbers near the rim are then approximate).**\n")
ZRIM = (len(Rp) - 1) * P["DZP"]; RRIM = float(Rp[-1])
Rz = lambda z: np.interp(np.clip(np.asarray(z) / P["DZP"], 0, len(Rp) - 1.001), np.arange(len(Rp)), Rp)
ROUT_FOOT = float(Rz(0.008)) + P["WALL"]
REP["geometry"] = dict(zrim=ZRIM, Rrim=RRIM, Rout_foot=ROUT_FOOT)

# ---------------------------------------------------------------- Q1 arrays and books
say("## Q1. What the file holds, and the books\n")
keys = {k: (list(Z[k].shape), str(Z[k].dtype)) for k in Z.files}; REP["arrays"] = keys
say("| array | shape | type |\n|---|---|---|")
for k in sorted(keys): say(f"| {k} | {keys[k][0]} | {keys[k][1]} |")
t = Z["t"].astype(float); nf = len(t); dt = float(np.median(np.diff(t))); N = int(Z["N"]); mp = float(Z["mp"])
nact, nfly, nland, nstuck, ndrops = (Z[k].astype(float) for k in ("nact", "nfly", "nlanded", "nstuck", "ndrops"))
spilled_g = (N - nact) * mp * 1e3
books = dict(pictures=nf, dt_s=dt, duration_s=float(t[-1]), particles=N, particle_mass_mg=mp * 1e6, stout_g=N * mp * 1e3,
             spilled_g_end=float(spilled_g[-1]), in_flight_end=float(nfly[-1]), fell_away_end=float(nland[-1]), frozen_on_old_body_end=float(nstuck[-1]),
             books_close=bool(np.all(nact + nfly + nland + nstuck == N)), max_in_flight=float(nfly.max()), max_listed=float(ndrops.max()))
if "foam_spill" in Z.files: books["head_spilled_mL_end"] = float(Z["foam_spill"][-1]) * 1e6
REP["books"] = books
say(f"\n{nf} pictures, {1 / dt:.0f} a second, {t[-1]:.2f} s. {N:,} particles of {mp * 1e6:.3f} mg: {N * mp * 1e3:.1f} g of stout.")
say(f"At the end: **{spilled_g[-1]:.1f} g of stout over the rim** = {N - nact[-1]:,.0f} particles, of which {nfly[-1]:,.0f} still in flight, "
    f"{nland[-1]:,.0f} fallen away (0.25 m below the floor), {nstuck[-1]:,.0f} frozen on the old model's body plane (z = {P['OLD_BODY_Z'] * 1e3:.0f} mm, 220 x 120 mm: Fig. 12's body, not Fig. 16's deck).")
say(f"Books (in glass + in flight + fallen + frozen = all particles) close in every picture: **{books['books_close']}**.")
if "head_spilled_mL_end" in books: say(f"Head spilled: {books['head_spilled_mL_end']:.2f} mL.")
rate = np.gradient(spilled_g, t); i_pk = int(np.argmax(rate))
q = lambda f: float(np.interp(f * spilled_g[-1], spilled_g, t)) if spilled_g[-1] > 0 else float('nan')
REP["rim_flux"] = dict(peak_g_per_s=float(rate[i_pk]), t_peak=float(t[i_pk]), t_10pct=q(0.1), t_50pct=q(0.5), t_90pct=q(0.9))
say(f"The rim flux peaks at {rate[i_pk]:.0f} g/s at t = {t[i_pk]:.2f} s; 10 %, 50 %, 90 % of the spill have left by t = {q(0.1):.2f}, {q(0.5):.2f}, {q(0.9):.2f} s.\n")

# ---------------------------------------------------------------- Q2 the drop list
say("## Q2. Is the stored drop list complete?\n")
D = Z["drops"].astype(np.float64); KEEP = D.shape[1]
fin = np.isfinite(D).all(-1); nlist = fin.sum(1)
sub = ndrops > KEEP
REP["list"] = dict(keep=KEEP, pictures_subsampled=int(sub.sum()), first_subsampled_t=float(t[sub][0]) if sub.any() else None,
                   max_true=float(ndrops.max()), min_share_stored=float((KEEP / np.maximum(ndrops, 1))[sub].min()) if sub.any() else 1.0)
say(f"Each picture lists at most {KEEP:,} drops. The true count exceeds that in **{int(sub.sum())} of {nf} pictures**"
    + (f" (from t = {t[sub][0]:.2f} s; at worst {100 * REP['list']['min_share_stored']:.0f} % of the drops are stored, an even subsample)" if sub.any() else "") + ".")
say("In a subsampled picture a drop's neighbours in time are missing from the list, so velocities cannot be matched there; the COUNTS (books) stay exact.\n")


def classify(X):
    r = np.hypot(X[:, 0], X[:, 1]); z = X[:, 2]
    inside = (z > 0) & (r < np.where(z < ZRIM, Rz(z), RRIM))     # in the cavity, or in the cylinder above the rim
    frozen = np.abs(z - P["OLD_BODY_Z"]) < 4e-4
    return inside, frozen


# ---------------------------------------------------------------- Q3 identity
@guard("Q3")
def q3():
    say("## Q3. Does a drop keep its place in the list?\n")
    same = []
    for f in range(1, nf):
        m = fin[f] & fin[f - 1]
        if m.sum() < 50: continue
        d = np.linalg.norm(D[f][m] - D[f - 1][m], axis=1); same.append(float(np.mean(d < P["VMAX"] * dt)))
    REP["identity"] = dict(pictures=len(same), median_share_same_slot_nearby=float(np.median(same)) if same else None)
    if same: say(f"Over {len(same)} picture pairs, a median {100 * np.median(same):.0f} % of list slots hold a drop within reach ({P['VMAX'] * dt * 1e3:.0f} mm) of the slot's drop one picture earlier. "
                 "(The solver re-sorts its particles by cell after every picture, so a slot is not a drop; this number says how badly.)\n")
q3()

# ---------------------------------------------------------------- Q4 velocities by free-flight matching
from scipy.spatial import cKDTree
rng = np.random.default_rng(P["SEED"])
gx = Z["gx"].astype(float) if "gx" in Z.files else np.zeros(nf); gz = Z["gz"].astype(float) if "gz" in Z.files else np.full(nf, -9.81)


def flying(f):
    X = D[f][fin[f]]; ins, frz = classify(X); return X[~ins & ~frz]


def match(f):
    """For sampled flying drops of picture f: the best pair (before, after) under free flight. Returns positions, velocities, residuals."""
    Pm, P0, Pp = flying(f - 1), flying(f), flying(f + 1)
    if min(len(Pm), len(P0), len(Pp)) < 20: return None
    idx = rng.choice(len(P0), min(P["NSAMP"], len(P0)), replace=False); A = P0[idx]
    a = np.array([gx[f], 0.0, gz[f]])
    tm, tp = cKDTree(Pm), cKDTree(Pp)
    nb = tm.query_ball_point(A, P["VMAX"] * dt)
    cnt = np.array([len(n) for n in nb])
    if cnt.sum() == 0: return None
    if cnt.sum() > 6_000_000:                                   # keep the work bounded in a dense spray
        keep = np.cumsum(cnt) < 6_000_000; A, nb, cnt = A[keep], [n for n, k in zip(nb, keep) if k], cnt[keep]
    rows = np.repeat(np.arange(len(A)), cnt); cols = np.concatenate([np.asarray(n, int) for n in nb if len(n)])
    pred = 2 * A[rows] - Pm[cols] + a * dt * dt
    d, j = tp.query(pred)
    o = np.lexsort((d, rows)); rs, ds, cs, js = rows[o], d[o], cols[o], j[o]
    first = np.r_[True, rs[1:] != rs[:-1]]; i1 = np.nonzero(first)[0]
    best = np.full(len(A), np.inf); second = np.full(len(A), np.inf); vel = np.full((len(A), 3), np.nan)
    best[rs[i1]] = ds[i1]; vel[rs[i1]] = (Pp[js[i1]] - Pm[cs[i1]]) / (2 * dt)
    i2 = i1 + 1; ok2 = (i2 < len(rs)); i2 = i2[ok2]; r1 = rs[i1][ok2]; same = rs[i2] == r1
    second[r1[same]] = ds[i2[same]]
    return dict(X=A, v=vel, best=best, second=second, cand=cnt, n=(len(Pm), len(P0), len(Pp)), a=a)


MATCH = []


@guard("Q4")
def q4():
    say("## Q4. Can the drops' velocities be recovered?\n")
    cand = [f for f in range(1, nf - 1) if not (sub[f - 1] or sub[f] or sub[f + 1]) and nfly[f] >= 50]
    REP["match_candidates"] = len(cand)
    if not cand: say("No picture has a complete list with at least 50 drops in flight before, at and after it: **velocities cannot be recovered from this ride's stored list.**\n"); return
    pick = [cand[i] for i in np.unique(np.linspace(0, len(cand) - 1, min(P["NFRAMES"], len(cand))).round().astype(int))]
    rows = []
    for f in pick:
        m = match(f)
        if m is None: continue
        ok = m["best"] < P["TOL"]; uniq = ok & (m["second"] > 3 * np.maximum(m["best"], 1e-5))
        m["ok"], m["uniq"], m["f"] = ok, uniq, f; MATCH.append(m)
        rows.append(dict(t=float(t[f]), flying=int(m["n"][1]), sampled=int(len(m["X"])), median_candidates=float(np.median(m["cand"])),
                         matched=float(ok.mean()), unique=float(uniq.mean()), median_residual_mm=float(np.median(m["best"][ok]) * 1e3) if ok.any() else None))
    REP["matching"] = rows
    say(f"Pictures usable (complete lists, at least 50 in flight): {len(cand)} of {nf}; tested: {len(rows)}. A match is accepted when the free-flight residual is below {P['TOL'] * 1e3:.1f} mm "
        f"(gravity's own term a dt^2 is {9.81 * dt * dt * 1e3:.2f} mm); it is called unique when the next-best pair is at least 3 times worse.\n")
    say("| t (s) | drops in flight | sampled | candidates before (median) | matched | matched and unique | median residual (mm) |\n|---|---|---|---|---|---|---|")
    for r in rows: say(f"| {r['t']:.2f} | {r['flying']:,} | {r['sampled']:,} | {r['median_candidates']:.0f} | {100 * r['matched']:.0f} % | {100 * r['unique']:.0f} % | {r['median_residual_mm'] if r['median_residual_mm'] is None else round(r['median_residual_mm'], 3)} |")
    if rows:
        w = np.array([r["sampled"] for r in rows], float)
        REP["matching_overall"] = dict(matched=float(np.average([r["matched"] for r in rows], weights=w)), unique=float(np.average([r["unique"] for r in rows], weights=w)))
        say(f"\nOverall (weighted by sample): **{100 * REP['matching_overall']['matched']:.0f} % matched, {100 * REP['matching_overall']['unique']:.0f} % matched uniquely.**\n")
q4()


# ---------------------------------------------------------------- Q5 rim speed, Weber number, landing on the true deck
@guard("Q5")
def q5():
    say("## Q5. How the stout leaves the rim, and where it would land on Fig. 16's deck\n")
    if not MATCH: say("No matched velocities: not answered.\n"); return
    X = np.concatenate([m["X"][m["uniq"]] for m in MATCH]); V = np.concatenate([m["v"][m["uniq"]] for m in MATCH])
    A = np.concatenate([np.tile(m["a"], (int(m["uniq"].sum()), 1)) for m in MATCH])
    if len(X) < 30: say(f"Only {len(X)} uniquely matched drops: not answered.\n"); return
    r = np.hypot(X[:, 0], X[:, 1]); sp = np.linalg.norm(V, axis=1)
    near = (X[:, 2] > ZRIM - 0.010) & (r < RRIM + 0.020)                     # just over the rim
    pc = lambda a_, p_: float(np.percentile(a_, p_))
    We = lambda u: P["RHO"] * u * u * P["H_SHEET"] / P["GAMMA"]
    out = dict(unique_drops=int(len(X)), near_rim=int(near.sum()))
    if near.sum() >= 20:
        s = sp[near]; vr = (V[near, 0] * X[near, 0] + V[near, 1] * X[near, 1]) / np.maximum(r[near], 1e-9)
        out.update(speed_p10=pc(s, 10), speed_p50=pc(s, 50), speed_p90=pc(s, 90), radial_p50=pc(vr, 50), up_p50=pc(V[near, 2], 50),
                   We_p10=We(pc(s, 10)), We_p50=We(pc(s, 50)), We_p90=We(pc(s, 90)), share_We_below_4=float(np.mean(We(s) < 4)))
        say(f"Drops within 20 mm outside the rim and above {1e3 * (ZRIM - 0.010):.0f} mm ({near.sum():,} uniquely matched): speed relative to the glass 10 / 50 / 90 % = "
            f"**{out['speed_p10']:.2f} / {out['speed_p50']:.2f} / {out['speed_p90']:.2f} m/s** (median outward {out['radial_p50']:.2f} m/s, upward {out['up_p50']:.2f} m/s).")
        say(f"Weber number rho U^2 h / gamma with an ASSUMED sheet thickness h = {P['H_SHEET'] * 1e3:.0f} mm: {out['We_p10']:.0f} / {out['We_p50']:.0f} / {out['We_p90']:.0f}. "
            f"Share below 4 (surface tension could hold the liquid to the glass): {100 * out['share_We_below_4']:.0f} %.\n")
    # landing on the deck plane z = DECK_Z by free flight under the picture's effective gravity
    zd = P["DECK_Z"]; az = A[:, 2]; dz = X[:, 2] - zd; ok = (dz > 0) & (az < -1.0)
    disc = V[:, 2] ** 2 - 2 * az * dz; ok &= disc > 0
    tl = np.where(ok, (-V[:, 2] - np.sqrt(np.where(ok, disc, 0))) / np.where(ok, az, -1), np.nan)
    xl = X[:, 0] + V[:, 0] * tl + 0.5 * A[:, 0] * tl ** 2; yl = X[:, 1] + V[:, 1] * tl
    rl = np.hypot(xl, yl); on = ok & (np.abs(xl) < P["DECK_HX"]) & (np.abs(yl) < P["DECK_HY"]); foot = on & (rl < ROUT_FOOT)
    out.update(landing_sample=int(ok.sum()), share_on_deck=float(on[ok].mean()) if ok.any() else None, share_on_glass_foot=float(foot[ok].mean()) if ok.any() else None,
               share_beyond_front_back=float((np.abs(xl[ok]) >= P["DECK_HX"]).mean()) if ok.any() else None, share_beyond_sides=float(((np.abs(yl[ok]) >= P["DECK_HY"]) & (np.abs(xl[ok]) < P["DECK_HX"])).mean()) if ok.any() else None,
               impact_speed_p50=float(np.nanpercentile(np.sqrt((V[:, 2] + az * tl) ** 2 + (V[:, 0] + A[:, 0] * tl) ** 2 + V[:, 1] ** 2)[ok], 50)) if ok.any() else None)
    REP["rim_and_landing"] = out
    if ok.any():
        say(f"Free flight from each matched drop's position and velocity to the deck's plane (z = {zd * 1e3:.0f} mm), with the effective gravity of its picture held constant (an approximation: the cart keeps accelerating during the fall), {ok.sum():,} drops:")
        say(f"**{100 * out['share_on_deck']:.0f} % would land on the deck** ({100 * out['share_on_glass_foot']:.0f} % of all within the glass's own footprint, i.e. they run down the glass), "
            f"{100 * out['share_beyond_front_back']:.0f} % beyond the deck's front or back edge, {100 * out['share_beyond_sides']:.0f} % beyond its sides. Median impact speed {out['impact_speed_p50']:.2f} m/s.")
        say("This sample counts a drop once per tested picture it is seen in, so slow, long-flying drops weigh more than their mass; the derived computation must follow each parcel once.\n")
    try:
        import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(8, 3.6)); ax.scatter(xl[ok] * 1e3, yl[ok] * 1e3, s=2, c=np.where(on[ok], "tab:blue", "tab:red"))
        ax.add_patch(plt.Rectangle((-P["DECK_HX"] * 1e3, -P["DECK_HY"] * 1e3), 2e3 * P["DECK_HX"], 2e3 * P["DECK_HY"], fill=False, lw=1.5)); ax.add_patch(plt.Circle((0, 0), ROUT_FOOT * 1e3, fill=False, lw=1.5))
        ax.set_aspect("equal"); ax.set_xlim(-400, 400); ax.set_ylim(-200, 200); ax.set_xlabel("x along the road (mm)"); ax.set_ylabel("y (mm)"); ax.set_title("Where matched drops would cross the deck's plane (blue: on the deck)")
        fig.tight_layout(); fig.savefig(os.path.join(OUT, "landing.png"), dpi=130); plt.close(fig)
        if near.sum() >= 20:
            fig, ax = plt.subplots(figsize=(6, 3.6)); ax.hist(sp[near], bins=40, color="tab:blue"); ax.set_xlabel("speed relative to the glass, just over the rim (m/s)"); ax.set_ylabel("matched drops"); fig.tight_layout(); fig.savefig(os.path.join(OUT, "rim_speed.png"), dpi=130); plt.close(fig)
    except Exception: REP["errors"].append({"figures": traceback.format_exc()[-800:]})
q5()


# ---------------------------------------------------------------- Q6 the deck's shaking
@guard("Q6")
def q6():
    say("## Q6. How hard the deck shakes\n")
    out = dict(gx_abs_max=float(np.abs(gx).max()), gx_rms=float(np.sqrt(np.mean(gx ** 2))), gz_min=float(gz.min()), gz_max=float(gz.max()),
               share_time_gx_over_1=float(np.mean(np.abs(gx) > 1.0)), share_time_gz_weaker_than_half_g=float(np.mean(gz > -4.9)))
    for k in ("th", "om", "v"):
        if k in Z.files: out[k + "_abs_max"] = float(np.abs(Z[k]).max())
    REP["deck_motion"] = out
    say(f"Effective gravity in the glass's (and deck's) frame, stored per picture: along the deck |g_x| up to **{out['gx_abs_max']:.1f} m/s^2** (rms {out['gx_rms']:.2f}; above 1 m/s^2 for {100 * out['share_time_gx_over_1']:.0f} % of the ride); "
        f"normal to the deck g_z between {out['gz_min']:.1f} and {out['gz_max']:.1f} m/s^2 (weaker than half of g for {100 * out['share_time_gz_weaker_than_half_g']:.0f} % of the ride; positive means the deck drops away faster than free fall).")
    if "th_abs_max" in out: say(f"Largest pitch {np.degrees(out['th_abs_max']):.1f} degrees" + (f", largest pitch rate {out['om_abs_max']:.2f} rad/s" if "om_abs_max" in out else "") + ".")
    say("A puddle of thickness e is pushed along the deck by rho g_x e per area and held at its edge by surface tension, of order gamma (1 - cos theta) / e per area of a strip one thickness wide; with e about 2 mm the two are equal near g_x = gamma / (rho e^2) = "
        f"{P['GAMMA'] / (P['RHO'] * 0.002 ** 2):.0f} m/s^2 times (1 - cos theta). Compare with the |g_x| above.\n")
    try:
        import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
        fig, ax = plt.subplots(3, 1, figsize=(8, 7), sharex=True)
        ax[0].plot(t, spilled_g); ax[0].set_ylabel("stout over the rim (g)")
        ax[1].plot(t, nfly, label="in flight"); ax[1].plot(t, nstuck, label="frozen on the old body plane"); ax[1].plot(t, nland, label="fallen away"); ax[1].axhline(KEEP, color="k", ls=":", lw=0.8); ax[1].set_ylabel("particles"); ax[1].legend(fontsize=8)
        ax[2].plot(t, gx, label="g_x"); ax[2].plot(t, gz, label="g_z"); ax[2].set_ylabel("effective gravity (m/s^2)"); ax[2].set_xlabel("t (s)"); ax[2].legend(fontsize=8)
        fig.tight_layout(); fig.savefig(os.path.join(OUT, "books.png"), dpi=130); plt.close(fig)
    except Exception: REP["errors"].append({"figures": traceback.format_exc()[-800:]})
q6()

say("## Errors\n"); say("none" if not REP["errors"] else json.dumps(REP["errors"], indent=1)[:3000])
say(f"\nWall time {time.time() - T0:.0f} s on Kaggle CPU.")
finish(0)


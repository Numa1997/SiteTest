"""Fig. 16 lecture note: measure every derived number the note quotes, from the code and the stored data, and write them to
notes/fig16/note-numbers.json, which tools/fig16/build_page.py reads to fill the note's {{keys}}. Nothing here is typed by hand
except the choice of what to measure; each entry says how it was obtained.
Sources: tools/fig16/kaggle/cart4.py (CART4, statics, linear_model, design), tools/fig12/kaggle/stout_jax.py (the glass, the head,
Fig. 12's cart), tools/fig12/glass_profile.json, notes/fig16/modes16.json, public/data/fig16/2026-11-14 and 2026-11-15 (the stored
rides and their indexes), public/data/fig12/2026-11-14-run10/index-jax.json.
Run: python3 notes/fig16/note_numbers.py   (numpy, scipy and jax on the CPU; about 20 s)"""
import json, math, os, re, sys
import numpy as np

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
P_ = lambda *a: os.path.join(ROOT, *a)
sys.path.insert(0, P_("tools", "fig16", "kaggle"))
import cart4 as C4   # noqa: E402

out = {}
def put(key, val, how):
    out[key] = dict(value=val, how=how)

P = dict(C4.CART4); G0 = C4.G0
modes = json.load(open(P_("notes", "fig16", "modes16.json")))
ml = modes["ml_kg"]
S = C4.statics(P, ml)
put("g", G0, "cart4.G0")
put("ml_kg", ml, "modes16.json ml_kg: the stout and head as a rigid load (slosh_model.liquid_mass)")
for k in ("Ms", "Mx", "J", "Wf", "Wr", "Nf0", "Nr0"):
    put("st_" + k, S[k], f"cart4.statics(CART4, ml)['{k}']")
put("J_pint", ml * P["hs"] ** 2, "ml * hs^2: the pint's share of the pitch inertia")

# one-body estimates: the deck alone on its four struts (tyres rigid)
w_b = math.sqrt(2 * P["k"] / S["Ms"]); put("f_bounce1", w_b / 2 / math.pi, "sqrt(2k/Ms)/2pi")
put("zeta_bounce1", 2 * P["c"] / (2 * math.sqrt(2 * P["k"] * S["Ms"])), "2c/(2 sqrt(2k Ms))")
kth = P["k"] * (P["af"] ** 2 + P["ar"] ** 2); put("k_theta", kth, "k (af^2 + ar^2), N m/rad")
w_p = math.sqrt(kth / S["J"]); put("f_pitch1", w_p / 2 / math.pi, "sqrt(k(af^2+ar^2)/J)/2pi")
put("zeta_pitch1", P["c"] * (P["af"] ** 2 + P["ar"] ** 2) / (2 * math.sqrt(kth * S["J"])), "c(af^2+ar^2)/(2 sqrt(k_theta J))")
put("f_hop_r1", math.sqrt((P["k"] + P["kt"]) / P["mr"]) / 2 / math.pi, "sqrt((k+kt)/mr)/2pi")
put("f_hop_f1", math.sqrt((P["k"] + P["kt"]) / P["mf"]) / 2 / math.pi, "sqrt((k+kt)/mf)/2pi")
put("static_sag_mm", S["Wf"] / P["k"] * 1e3, "Wf / k: the struts' static compression")

# the modes with the control off (Kaggle CPU, modes16.json), reproduced here from the same linear model
A, B, E = C4.linear_model(P, S, 1.0)
lam = np.linalg.eigvals(A); osc = sorted([l for l in lam if l.imag > 1e-6], key=lambda l: abs(l.imag))
put("modes_here", [dict(f=abs(l.imag) / 2 / math.pi, f_nat=abs(l) / 2 / math.pi, zeta=-l.real / abs(l),
                         f_peak=abs(l) / 2 / math.pi * math.sqrt(max(0.0, 1 - 2 * (l.real / abs(l)) ** 2))) for l in osc],
    "eig(cart4.linear_model(v0=1.0)) here: f = |Im|/2pi (damped), f_nat = |lambda|/2pi, f_peak = f_nat sqrt(1 - 2 zeta^2)")
put("modes16", modes["speeds"][0]["modes"], "modes16.json, v0 = 1.0 m/s")
wf = modes["speeds"][0]["wheelbase_filter"]["five 20 mm bumps (0.29 m apart)"]
put("five_f", wf["f_hz"], "v0 / 0.29 m"); put("five_pitch_drive", wf["pitch_drive"], "|2 sin(pi f wb/v)|")
put("five_heave_drive", wf["heave_drive"], "|2 cos(pi f wb/v)|")
fp = modes["speeds"][0]["modes"][2]
put("ratio_five_pitch", wf["f_hz"] / fp["f_hz"], "f(five bumps) / f(pitch with stout)")
put("band_lo", fp["f_hz"] * (1 - fp["zeta"]), "f(1 - zeta)"); put("band_hi", fp["f_hz"] * (1 + fp["zeta"]), "f(1 + zeta)")
put("kerb_pitch_drive", abs(2 * math.sin(math.pi * C4.PLANT_F0 * 0.22 / 1.5)), "|2 sin(pi f0 wb / 1.5)|")

# the swing the controller is designed on, and the drive of a tilt
put("f0", C4.PLANT_F0, "cart4.PLANT_F0 (run 8, with the head)"); put("zeta0", C4.PLANT_ZETA, "cart4.PLANT_ZETA")
put("beta0", C4.PLANT_BETA, "cart4.PLANT_BETA"); put("w0", 2 * math.pi * C4.PLANT_F0, "2 pi f0")

# the glass and the head
gp = json.load(open(P_("tools", "fig12", "glass_profile.json"))); R = np.asarray(gp["R"]); dzp = 0.0005
fill = 0.125; zrim = (len(R) - 1) * dzp; Rfill = float(np.interp(fill, dzp * np.arange(len(R)), R))
src = open(P_("tools", "fig12", "kaggle", "stout_jax.py")).read()
HEAD0 = float(re.search(r"^HEAD0 = ([0-9.e-]+)", src, re.M).group(1)); PHI_F = float(re.search(r"^PHI_F = ([0-9.e-]+)", src, re.M).group(1))
put("R_fill_mm", Rfill * 1e3, "glass_profile.json R at z = 125 mm (dz 0.5 mm)"); put("zrim_mm", zrim * 1e3, "(len(R)-1) dz")
put("head0_mm", HEAD0 * 1e3, "stout_jax.HEAD0"); put("phi_f", PHI_F, "stout_jax.PHI_F")
free = zrim - fill - HEAD0; put("freeboard_mm", free * 1e3, "zrim - fill - HEAD0")
put("stout_free_mm", (zrim - fill) * 1e3, "zrim - fill")
put("tilt_head_deg", math.degrees(math.atan(free / Rfill)), "atan(freeboard / R): a steady tilt that lifts the head's top to the rim")
put("rise9_mm", Rfill * math.tan(math.radians(9)) * 1e3, "R tan 9 deg")
zS = P["hg"] - C4.FLOOR_ABOVE_DECK; put("zS_mm", zS * 1e3, "hg - FLOOR_ABOVE_DECK: S above the glass's inner floor")
put("rmax_mm", math.hypot(zS, Rfill) * 1e3, "farthest stout from S: the floor's edge, hypot(zS, R)")

# Fig. 12's motor at the kerb's speed (stout_jax CART_COMMON)
c12 = dict(Km=0.02, Ngear=10.0, Rw=0.04, Ra=2.0, Vmax=12.0, Imax=3.0)
m = re.search(r"CART_COMMON = dict\((.*?)\)\s", src, re.S).group(1)
for k in c12: c12[k] = float(re.search(rf"\b{k}=([0-9.e-]+)", m).group(1))
b12 = c12["Km"] * c12["Ngear"] / c12["Rw"]; i12 = min(c12["Imax"], (c12["Vmax"] - b12 * 1.5) / c12["Ra"])
put("F12_max", b12 * i12, "Fig. 12: b = Km Ngear / Rw, i = min(Imax, (Vmax - b v)/Ra) at 1.5 m/s")
put("b12", b12, "Km Ngear / Rw")
# Fig. 16's motors at 1.5 m/s
E16 = P["b"] * 1.5; ilim = min(P["Imax"], (P["Vmax"] - E16) / P["Ra"])
put("E16", E16, "b v, V"); put("i_volt16", (P["Vmax"] - E16) / P["Ra"], "(Vmax - b v)/Ra at 1.5 m/s")
put("F16_max", P["nm"] * P["b"] * ilim, "nm b min(Imax, (Vmax - b v)/Ra)")
put("grip_r", P["mu"] * S["Nr0"], "mu N_r0: the rear tyres' grip at rest")
put("Fd0", P["cx"] * 1.5, "cx v0: drag at 1.5 m/s")

# the controller (run 2's chosen weighting, at both speeds)
W = {"q": 0.00025}
for v0, tag in ((1.5, "k"), (1.0, "g")):
    D = C4.design(P, ml, v0, W)
    ev = np.linalg.eigvals(D["Ad"] - D["Bd"] @ D["K"]); sl = np.max(np.abs(ev))
    put(f"slowest_{tag}", float(sl), "max |eig(Ad - Bd K)|"); put(f"tau_slow_{tag}", -P["Ts"] / math.log(sl), "-Ts / ln|z|")
    # continuous equivalents of the closed-loop poles: s = ln z / Ts; the least damped oscillating one
    s = np.log(ev.astype(complex)) / P["Ts"]; oscs = [x for x in s if x.imag > 1e-3]
    lz = min(oscs, key=lambda x: -x.real / abs(x))
    put(f"cl_least_damped_{tag}", dict(f=abs(lz.imag) / 2 / math.pi, zeta=-lz.real / abs(lz)), "least damped closed-loop pole")
    ol = np.linalg.eigvals(D["Ad"]); put(f"open_max_{tag}", float(np.max(np.abs(ol))), "max |eig(Ad)|")
    nrm = [float(np.linalg.norm(D["Kp"][j])) for j in range(P["Np"])]
    put(f"Kp_norm_{tag}", dict(j0=nrm[0], j50=nrm[50], j100=nrm[100], j249=nrm[249], ratio249=nrm[249] / nrm[0], ratio100=nrm[100] / nrm[0]),
        "Frobenius norm of K_j")
    put(f"K_{tag}", D["K"].tolist(), "LQR gain, rows F_d, u_f, u_r; columns dv, xi, zc, vzc, th, om, zf, vzf, zr, vzr, q, qd")
    put(f"Lk_{tag}", D["Lk"].tolist(), "Kalman gain of the swing's filter (per probe reading)")
    put(f"Q_{tag}", np.diag(D["Q"] / P["Ts"]).tolist(), "diag Q / Ts (Bryson weights)")
put("cands", json.load(open(P_("public", "data", "fig16", "2026-11-15", "index-16.json")))["design"]["candidates"], "index-16.json design")

# the stored rides
I15 = json.load(open(P_("public", "data", "fig16", "2026-11-15", "index-16.json"))); I14 = json.load(open(P_("public", "data", "fig16", "2026-11-14", "index-16.json")))
I12 = json.load(open(P_("public", "data", "fig12", "2026-11-14-run10", "index-jax.json")))
def ride(date, name): return json.load(open(P_("public", "data", "fig16", date, name + ".json")))
rides = {n: ride("2026-11-15", n) for n in ("kerb_full", "kerb_full_seed2", "kerb_off", "resonant_off", "bump25_off")}
rides.update({n + "_v2": ride("2026-11-14", n) for n in ("kerb_full", "resonant_full", "bump25_full")})
for n, d in rides.items():
    t = np.asarray(d["t"]); v = np.asarray(d["v"]); tilt = np.abs(np.asarray(d["tilt_mm"], float)); fps = d.get("fps", 30)
    a = np.gradient(v, t)
    rec = dict(fps=fps, frames=d["frames"], tilt_max=float(np.nanmax(tilt)), tilt_every2_even=float(np.nanmax(tilt[0::2])),
               tilt_every2_odd=float(np.nanmax(tilt[1::2])), t_tilt_max=float(t[int(np.nanargmax(tilt))]),
               v_min=float(v.min()), v_max=float(v.max()), a_min=float(a.min()), a_max=float(a.max()), t_a_min=float(t[int(np.argmin(a))]),
               pitch_max_deg=float(np.degrees(np.max(np.abs(np.asarray(d["th"]) - d["th"][0])))),
               i_max=float(np.max(np.abs(d["i"]))), u_max=float(max(np.max(np.abs(d["uf"])), np.max(np.abs(d["ur"])))),
               head_spill=float(d["head_spill_ml"][-1]), spill_g=float(d["spill_g"][-1]), stout0_g=float(d["stout_g"][0]),
               aeff_max=float(np.max(np.abs(d["aeff"]))))
    if "om" in d:
        om = np.abs(np.asarray(d["om"])); al = np.abs(np.asarray(d["al"]))
        rec.update(om_max=float(om.max()), al_max=float(al.max()), euler_rmax=float(al.max() * math.hypot(zS, Rfill)),
                   centr_rmax=float(om.max() ** 2 * math.hypot(zS, Rfill)), cor_05=float(2 * om.max() * 0.5))
    # the lean a pure tilt would need to cancel the cart's own deceleration at its peak (eq. 2 with a_z = 0)
    rec["lean_needed_deg"] = float(math.degrees(math.atan(-rec["a_min"] / G0)))
    put("ride_" + n, rec, "stored ride file: 60 or 30 pictures a second; acceleration by central differences of the stored speed")
# the two seeds frame by frame (the scatter of the seeding)
k1, k2 = np.asarray(rides["kerb_full"]["tilt_mm"], float), np.asarray(rides["kerb_full_seed2"]["tilt_mm"], float)
put("seed_rms_mm", float(np.sqrt(np.nanmean((k1 - k2) ** 2))), "rms over the 241 stored pictures of the tilt difference of the two seeds")
put("seed_max_mm", float(np.nanmax(np.abs(k1 - k2))), "largest difference")
for n, f in (("kerb", "ride_sharp30_slosh"), ("res", "ride_resonant_joint"), ("b25", "ride_bump25_joint")):
    r = next(x for x in I12["files"] if x["path"] == f + ".json"); put("f12_" + n, r["measured"], "Fig. 12 index-jax.json (run 10)")
put("gpu_v4_min", sum(f["measured"]["run_s"] for f in I15["files"] if f.get("kaggle_version") == 4) / 60, "sum run_s of the v4 rides stored")
put("gpu_v7_min", sum(f["measured"]["run_s"] for f in I15["files"] if f.get("kaggle_version") == 7) / 60, "sum run_s of the v7 rides stored")
put("ms_step_on", [f["measured"]["ms_per_step"] for f in I15["files"] if f["ctrl"] == "full"], "ms a step, control on (v4)")
put("ms_step_off", [f["measured"]["ms_per_step"] for f in I15["files"] if f["ctrl"] == "off"], "ms a step, control off (v7)")
put("steps", {f["path"]: f["measured"]["steps"] for f in I15["files"] + I14["files"]}, "steps per ride")

# check of eq. (1)-(2): g_eff resolved on the tilted axes, against cart4.forces' formula, on random numbers
rng = np.random.default_rng(1); errs = []
for _ in range(1000):
    th, ax, az = rng.normal(0, 0.3), rng.normal(0, 5), rng.normal(0, 5)
    ex = np.array([math.cos(th), math.sin(th)]); ez = np.array([-math.sin(th), math.cos(th)]); geff = np.array([-ax, -G0 - az])
    gx, gz = -(G0 + az) * math.sin(th) - ax * math.cos(th), -(G0 + az) * math.cos(th) + ax * math.sin(th)
    errs.append(max(abs(geff @ ex - gx), abs(geff @ ez - gz)))
put("check_geff", max(errs), "max |g_eff . e - formula| over 1000 random states")
# check of the rotating-frame formula of stout_jax.frame_accel: -al x r - om x (om x r) - 2 om x v with Omega = -om e_y
errs = []
for _ in range(1000):
    om, al, X, Z, vx, vz = rng.normal(size=6)
    Om = np.array([0, -om, 0]); Al = np.array([0, -al, 0]); r = np.array([X, 0, Z]); v = np.array([vx, 0, vz])
    a = -np.cross(Al, r) - np.cross(Om, np.cross(Om, r)) - 2 * np.cross(Om, v)
    errs.append(max(abs(a[0] - (al * Z + om * om * X + 2 * om * vz)), abs(a[2] - (-al * X + om * om * Z - 2 * om * vx))))
put("check_rot", max(errs), "max error of frame_accel's components against the vector formula, Omega = -theta' e_y")
# check of the linearised a_eff in cart4.linear_model against the exact one, at a small state
th, ax, al_ = 0.01, 0.2, 1.0
aSx = ax - P["hg"] * al_ * math.cos(th); aSz = -P["hg"] * al_ * math.sin(th)
exact = aSx * math.cos(th) + (G0 + aSz) * math.sin(th); lin = ax + G0 * th - P["hg"] * al_
put("check_lin", dict(exact=exact, lin=lin), "a_eff exact vs linear at theta 0.01 rad, a_x 0.2 m/s^2, theta'' 1 rad/s^2")

# the acceleration of S on a pitching deck: finite differences of r_S = r_c + h_g (-sin th, cos th) against the exact formula
# a_S = r_c'' + h_g th'' (-cos th, -sin th) + h_g th'^2 (sin th, -cos th), and against cart4.forces' sign of the th'^2 term
tt = np.linspace(0, 1, 20001); thf = 0.3 * np.sin(7 * tt) + 0.2 * np.cos(3 * tt); hg = P["hg"]
rS = np.stack([-hg * np.sin(thf), hg * np.cos(thf)], 1); aS_fd = np.gradient(np.gradient(rS, tt, axis=0), tt, axis=0)
thd = np.gradient(thf, tt); thdd = np.gradient(thd, tt); k = slice(100, -100)
exact = np.stack([-hg * thdd * np.cos(thf) + hg * thd ** 2 * np.sin(thf), -hg * thdd * np.sin(thf) - hg * thd ** 2 * np.cos(thf)], 1)
code = np.stack([-hg * thdd * np.cos(thf) - hg * thd ** 2 * np.sin(thf), -hg * thdd * np.sin(thf) + hg * thd ** 2 * np.cos(thf)], 1)
put("check_aS", dict(exact=float(np.abs(aS_fd[k] - exact[k]).max()), code=float(np.abs(aS_fd[k] - code[k]).max()),
                     scale=float(np.abs(aS_fd[k]).max())), "max |finite difference - formula|, m/s^2: the exact formula and cart4's")
for n in ("kerb_full", "kerb_full_seed2", "kerb_off", "resonant_off", "bump25_off"):
    om = np.asarray(rides[n]["om"]); put("gz_err_" + n, float(2 * hg * np.max(om ** 2)), "2 h_g max th'^2: cart4's error of g_z (along the glass)")
# run 3 against run 2 (controlled kerb) and the two seeds, on run 2's 30-a-second grid
t2 = np.asarray(rides["kerb_full_v2"]["t"]); k2_ = np.asarray(rides["kerb_full_v2"]["tilt_mm"], float)
t3 = np.asarray(rides["kerb_full"]["t"]); idx = [int(np.argmin(np.abs(t3 - x))) for x in t2]
put("run3_run2_rms", float(np.sqrt(np.nanmean((k1[idx] - k2_) ** 2))), "rms of run 3 seed 1 minus run 2, kerb with control, at run 2's 121 picture times")
put("run3_run2_max", float(np.nanmax(np.abs(k1[idx] - k2_))), "largest difference")
put("seed_rms30", float(np.sqrt(np.nanmean((k1[idx] - k2[idx]) ** 2))), "the two seeds at the same 121 times")
# the controlled kerb, seed 1, after 3.2 s: the burst after the probes' jump
d1 = rides["kerb_full"]; t1 = np.asarray(d1["t"]); late = t1 > 3.2
du = np.abs(np.asarray(d1["uf"]) - np.asarray(d1["ur"])) / 2; yq = np.asarray(d1["yq"]) * 1e3
put("late_seed1", dict(du_max=float(du[late].max()), du_before=float(du[(t1 > 1.2) & (t1 < 3.2)].max()), al_max=float(np.abs(np.asarray(d1["al"]))[late].max()),
                       om_max=float(np.abs(np.asarray(d1["om"]))[late].max()), tilt_max=float(np.abs(np.asarray(d1["tilt_mm"]))[late].max()),
                       yq_jump_t=float(t1[late][int(np.argmax(np.abs(np.diff(yq[late]))))]), yq_min=float(yq[late].min()), yq_max=float(yq[late].max())),
    "seed 1 after 3.2 s: actuators' pitch part (|u_f - u_r|/2), deck's angular acceleration, pitch rate, tilt, probe reading")
d2 = rides["kerb_full_seed2"]; t2s = np.asarray(d2["t"])
put("late_seed2", dict(du_max=float((np.abs(np.asarray(d2["uf"]) - np.asarray(d2["ur"])) / 2)[t2s > 3.2].max())), "seed 2 after 3.2 s")
Nf = np.asarray(d1["Nf"]); Nr = np.asarray(d1["Nr"])
put("airborne", dict(front=int((Nf <= 0).sum()), rear=int((Nr <= 0).sum()), t_first=float(t1[(Nf <= 0) | (Nr <= 0)].min()), t_last=float(t1[(Nf <= 0) | (Nr <= 0)].max())),
    "stored pictures of the controlled kerb (seed 1) in which an axle carries no load")
sf = np.asarray(d1["zc"]) + P["af"] * np.sin(d1["th"]) - np.asarray(d1["zf"]); sr = np.asarray(d1["zc"]) - P["ar"] * np.sin(d1["th"]) - np.asarray(d1["zr"])
put("strokes_mm", dict(f_min=float((sf - sf[0]).min() * 1e3), f_max=float((sf - sf[0]).max() * 1e3), r_min=float((sr - sr[0]).min() * 1e3), r_max=float((sr - sr[0]).max() * 1e3)),
    "strut strokes from their first stored value, controlled kerb seed 1")
put("pitch_geom_deg", math.degrees(math.asin(2 * P["smax"] / (P["af"] + P["ar"]))), "asin(2 s_max / wheelbase): the most the struts' travel can tilt the deck")
# the head breaks off once rho_f (g e/2) >= tau_y (Fig. 12's rule, at rest): e = 2 tau_y / (rho_f g)
d12 = json.load(open(P_("public", "data", "fig12", "2026-11-14-run10", "ride_sharp30_slosh.json")))
put("tau_y", d12["head"]["tau_y"], "Fig. 12 ride file, head.tau_y"); put("e_break_mm", 2 * d12["head"]["tau_y"] / (PHI_F * 1007.0 * G0) * 1e3, "2 tau_y / (phi_f rho g)")
put("dt_fluid_ms", 4.0 / next(f for f in I15["files"] if f["path"] == "kerb_full.json")["measured"]["steps"] * 1e3, "4 s / steps of the controlled kerb (run 3)")
dg = json.load(open(P_("notes", "fig12", "damping-grid.json"))); z15 = next(r for r in dg["runs"] if r["dx_mm"] == 1.5)["fit_ring13"]["zeta"]
put("zeta_num", z15, "notes/fig12/damping-grid.json, 1.5 mm"); put("zeta_num_share", z15 / C4.PLANT_ZETA, "zeta_num / zeta with the head")
# the preview law, checked by brute force: a random 3-state system, a known disturbance sequence, the optimal inputs of a long
# horizon from the optimality (KKT) equations with the states as unknowns, against u_0 = -K x_0 - sum_j G (Acl')^j P E w_j
from scipy.linalg import solve_discrete_are
def preview_check(seed=3, NH=300):
    rng = np.random.default_rng(seed); n, m = 3, 1
    A = np.eye(n) + 0.1 * rng.normal(size=(n, n)); B = rng.normal(size=(n, m)); E = rng.normal(size=(n, 1)); Q = np.eye(n); R = np.eye(m)
    Pm = solve_discrete_are(A, B, Q, R); G = np.linalg.solve(R + B.T @ Pm @ B, B.T); K = G @ Pm @ A; Ac = A - B @ K
    x0 = rng.normal(size=n); w = rng.normal(size=(NH, 1)) * np.exp(-np.arange(NH) / 30)[:, None]
    nx, nu = NH * n, NH * m; N = nx + nu; H = np.zeros((N, N))
    for k in range(1, NH): H[(k - 1) * n:k * n, (k - 1) * n:k * n] = Q
    H[(NH - 1) * n:NH * n, (NH - 1) * n:NH * n] = Pm; H[nx:, nx:] = np.kron(np.eye(NH), R)
    C = np.zeros((nx, N)); d = np.zeros(nx)
    for k in range(NH):
        C[k * n:(k + 1) * n, k * n:(k + 1) * n] = np.eye(n)
        if k > 0: C[k * n:(k + 1) * n, (k - 1) * n:k * n] = -A
        C[k * n:(k + 1) * n, nx + k * m:nx + (k + 1) * m] = -B
        d[k * n:(k + 1) * n] = E @ w[k] + (A @ x0 if k == 0 else 0)
    z = np.linalg.solve(np.block([[2 * H, C.T], [C, np.zeros((nx, nx))]]), np.concatenate([np.zeros(N), d]))
    uf = -K @ x0 - sum(G @ np.linalg.matrix_power(Ac.T, j) @ Pm @ E @ w[j] for j in range(NH))
    return float(z[nx]), float(uf[0])
u_opt, u_formula = preview_check()
put("check_preview", dict(u_opt=u_opt, u_formula=u_formula), "first optimal input: optimality equations solved directly vs the preview formula")

json.dump(out, open(P_("notes", "fig16", "note-numbers.json"), "w"), indent=1, default=float)
for k, v in out.items():
    if k.startswith(("K_", "cands", "steps", "Q_")): continue
    print(k, json.dumps(v["value"], default=float)[:300])

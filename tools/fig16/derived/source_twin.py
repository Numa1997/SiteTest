"""Fig. 16 spill, step 2 of notes/spill/DERIVATION-flight-inversion.md section 9: the forward model (section 5) and the TWIN test
(section 7). Kaggle CPU. Needs flight_map.py beside it (same commit) and the dataset fig16-guinness-cart-control (for the frame only:
t, v, vzc, om, th; no stored liquid is used).   python3 source_twin.py OUTDIR
SMOKE=1: a 0.1 s launch window, the full node density, 5 iterations per stage, every block; plus the timing of one full-size evaluation.

THE SOURCE (section 4, extended by step 1's finding A4: 24 % of the liquid in the air at picture 58 sat above the grid's top inside the
rim's radius, so liquid also leaves through the top). Launch surface = the stored solver's leave rule (stout_jax.py:865-867):
  patch 0, the rim's cylinder r = R_rim, z_rim <= z <= z_top;   patch 1, the grid's top disk z = z_top, r < R_rim.
Coordinates on a patch: theta, and xi in [-1, 1] (height on the cylinder, radius on the disk). Unknowns at knots (one per picture of
the launch window), linear in t0 between:
  share logits:  cos(n theta), n = 0..4, times {1, xi}, per patch                        20
  u_r, u_z:      the same basis                                                           20 + 20
  u_theta:       sin(n theta), n = 1..4, times {1, xi}, per patch (odd in y: mirror)      16        -> 76 per knot
The share is a softmax over the nodes of one launch time with log(area) added: the mass is EXACTLY Q(t0) dt0 per launch time
(constraint (2)). The source is a smooth function of (t0, theta, xi): it can be evaluated on any set of nodes.

THE FORWARD MODEL (section 5). Each node carried by eq. (1) with step 1's matrices: [s; 1](t) = Phi(t) Phi(t0)^-1 [s0; 1],
s = (x, z - zS, vx, vz); y = y0 + vy (t - t0). The stored solver's rules: frozen when crossing z = -14 mm inside |x| < 110 mm,
|y| < 60 mm (stout_jax.py:876); landed below z = -250 mm (:878). Each piece is followed K = 30 pictures; frozen and landed liquid
stays counted at every later picture. Crossings between pictures by linear interpolation. For the gradient the yes/no tests are
logistic steps of width 1 mm (the truth 0.01 mm). Predicted: N_fly, N_stuck, N_landed per picture; mass in flight per 10 mm cell.

THE TWIN (section 7). Truth: a hand-chosen source (hand_coeffs). Fit nodes as dense as the truth's (48 theta, 3 xi, 4 launch times
per picture) but SHIFTED: theta by half a spacing, launch times by half a launch spacing (fine grid of 8 per picture), xi on
3-point Gauss-Legendre nodes instead of midpoints. Fake pictures: listed counts per 10 mm cell, Poisson with mean
lambda_j M_jc / m_p, lambda_j = min(1, 16 384 / markers listed); even pictures. Fake N_fly: exact.
GATE (before any fit; marks fixed here): the truth's coefficients evaluated on the FIT's nodes must reproduce the truth's deck field
with L1 < 2 %, and the in-flight mass outside the 10 mm grid must be < 2 %. If not: stop, report, no fit (SMOKE: reported, not
enforced, so that the fit's code is still exercised).
START FROM MOMENTS. The flight map is linear, so the first moment of the in-flight mass at picture j, sum w x and sum w z, is linear
in the launch velocities. With the shares at the first guess (uniform per area), u_theta = 0, and the freezing/landing masks of the
previous iterate held fixed, the mean u_r and u_z per knot follow from linear least squares against the observed moments
(sum over cells of n / lambda * m_p * cell centre), with a small smoothing between knots; three passes. This is C0.
MULTISCALE. Fits warm-started in turn: both fields Gaussian-blurred with sigma 40 mm (MU_HI), sigma 20 mm (MU_HI), then unblurred
for each MU of the ladder MU_HI > ... (continuation). Objective at each stage
  J = sum [mu - n ln mu] (blurred fields when blurred) + sum_j (N_fly_hat - N_fly)^2 / (2 s^2) + MU |D C|^2 + 0.01 MU |C_vel - C0_vel|^2,
s = 1 % of the largest N_fly; L-BFGS-B on the exact JAX gradient. MU by the discrepancy principle among the unblurred fits: the largest
MU whose Poisson deviance per datum is <= 1 (Morozov); if none, the smallest.
PASS MARK (Opinion, fixed before the run): the recovered source evaluated on the TRUTH's nodes; its deck flux under section 8's
geometry (no old body; z = -30 mm, 310 x 124 mm), mass per 20 mm cell and 0.1 s window, L1 against the truth / truth's total <= 5 %.
RE-CONTACT (section 8, extended), reported for truth and recovered: every path, sampled on the fine grid (~2 ms), is classified by the
first solid it meets: (a) comes down through z = z_rim inside r < R_rim: back in the glass, not spilled; (b) meets the outer wall
below the rim, r <= R(z) + 2.5 mm for 0 <= z < z_rim, or the foot, r <= R(0) + 2.5 mm for -14 mm <= z < 0 (assumed shape): wall film;
(c) crosses z = -30 mm inside the deck: deck source; (d) none of these within 30 pictures: off.
OUTPUT: REPORT.md, report.json (rewritten after every block), twin.npz."""
import json, os, sys, time, traceback, urllib.request
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
OUT = sys.argv[1] if len(sys.argv) > 1 else "/kaggle/working"; os.makedirs(OUT, exist_ok=True)
SMOKE = os.environ.get("SMOKE", "0") == "1"
MD, REP, ERR, W = [], {}, [], {}; T0 = time.time()
LIST_CAP, MP_ = 16384, 0.429e-6                                           # listing capacity; kg per marker (handoff 2.3)
EPS_FIT, EPS_TRUE = 1e-3, 1e-5
FROZ = (-0.014, 0.110, 0.060); LAND = -0.25; DECK = (-0.030, 0.155, 0.062); WALL, FOOT = 0.0025, -0.014
GRID = dict(lo=np.array([-0.25, -0.15, -0.26]), h=0.010, n=np.array([50, 30, 51]))
K, SUB = 30, 8
MU_HI, MU_LADDER = 1e2, (1e2, 1e0, 1e-2); MAXIT = 5 if SMOKE else 400
GATE_DECK, GATE_OUT, PASS_L1 = 0.02, 0.02, 0.05
NPK = 76; SL = dict(share=slice(0, 20), ur=slice(20, 40), uth=slice(40, 56), uz=slice(56, 76))


def say(s=""):
    print(s, flush=True); MD.append(s)


def flush():
    md = MD + (["\n## Block failures\n"] + [f"- `{e['block']}`: {e['error']}" for e in ERR] if ERR else [])
    open(os.path.join(OUT, "REPORT.md"), "w").write("\n".join(md) + "\n")
    json.dump(dict(REP, errors=ERR), open(os.path.join(OUT, "report.json"), "w"), indent=1,
              default=lambda o: float(o) if np.ndim(o) == 0 else np.asarray(o).tolist())


class Stop(Exception):
    pass


def block(name, fn):
    t_ = time.time()
    try:
        fn(); print(f"[block {name}: done in {time.time() - t_:.1f} s]", flush=True)
    except Stop as e:
        say(f"\n**STOPPED: {e}**"); print(f"[block {name}: stopped by its gate]", flush=True)
    except Exception as e:
        ERR.append(dict(block=name, error=f"{type(e).__name__}: {e}", trace=traceback.format_exc()))
        print(f"[block {name}: FAILED]\n{traceback.format_exc()}", flush=True)
    flush()


# ------------------------------------------------------------------ the frame (step 1's code, imported)
def frame():
    import flight_map as fm
    fm.load(); fm.frame()
    t = fm.D["t"]; nf = len(t)
    tf = np.concatenate([t[k] + (t[k + 1] - t[k]) * np.arange(SUB) / SUB for k in range(nf - 1)] + [t[-1:]])
    omf = np.interp(tf, t, fm.D["omf"]); alk = np.repeat(fm.D["al_k"], SUB); bf = np.repeat(fm.D["b"], SUB, axis=0)
    ts, Ps, ks = fm.propagate(tf, omf[:-1], alk, bf)
    last = np.r_[0, np.where(np.diff(ks) != 0)[0], len(ts) - 1]; Pf = Ps[last]
    if len(Pf) != len(tf): raise RuntimeError(f"fine grid {len(tf)} against {len(Pf)} matrices")
    js = urllib.request.urlopen("https://raw.githubusercontent.com/Numa1997/SiteTest/main/public/scripts/guinness-glass.js", timeout=30).read().decode()
    Rp = np.array([float(v) for v in js.split("R: [")[1].split("]")[0].split(",")]); zrim = (len(Rp) - 1) * fm.DZP
    nz = int(np.ceil((zrim + 0.02) / fm.DX)) + 2; ztop = -2 * fm.DX + (nz - 1) * fm.DX
    W.update(t=t, nf=nf, tf=tf, Pf=Pf, Ppic=Pf[::SUB], ZS=fm.ZS, Rp=Rp, DZP=fm.DZP, Rrim=float(Rp[-1]), zrim=zrim, ztop=ztop)
    det = float(np.abs(np.linalg.det(Pf[:, :4, :4]) - 1).max())
    say("# Fig. 16 spill, step 2: forward model and twin test (DERIVATION-flight-inversion.md section 9)\n"
        + ("**SMOKE RUN: 0.1 s launch window, 5 iterations per stage; numbers are not results.**\n" if SMOKE else ""))
    say(f"Frame: {nf} pictures, fine grid {len(tf)} times ({SUB} per picture), largest |det Psi - 1| {det:.1e}. Rim z {zrim * 1e3:.1f} mm, "
        f"radius {W['Rrim'] * 1e3:.1f} mm, grid top {ztop * 1e3:.1f} mm.")
    REP["frame"] = dict(fine_times=len(tf), det_err=det, zrim=zrim, Rrim=W["Rrim"], ztop=ztop)


# ------------------------------------------------------------------ nodes, basis, propagators
def nodes(nth, k0, k1, th_shift=0.0, xi_mode="mid", lpp=4, a_off=0):
    Rr, zr, zt = W["Rrim"], W["zrim"], W["ztop"]; th = (np.arange(nth) + 0.5 + th_shift) * 2 * np.pi / nth
    if xi_mode == "mid": xi, wx = np.array([-2 / 3, 0.0, 2 / 3]), np.full(3, 2 / 3)
    else: xi, wx = np.array([-np.sqrt(0.6), 0.0, np.sqrt(0.6)]), np.array([5 / 9, 8 / 9, 5 / 9])
    T, X = np.meshgrid(th, xi, indexing="ij"); _, WX = np.meshgrid(th, wx, indexing="ij"); T, X, WX = T.ravel(), X.ravel(), WX.ravel()
    zc = zr + (X + 1) / 2 * (zt - zr); rc = (X + 1) / 2 * Rr; dth = 2 * np.pi / nth
    pos = np.r_[np.c_[Rr * np.cos(T), Rr * np.sin(T), zc], np.c_[rc * np.cos(T), rc * np.sin(T), np.full_like(T, zt)]]
    patch = np.r_[np.zeros(len(T), int), np.ones(len(T), int)]; Th = np.r_[T, T]; Xi = np.r_[X, X]
    area = np.r_[Rr * dth * (zt - zr) / 2 * WX, rc * dth * Rr / 2 * WX]
    rh = np.c_[np.cos(Th), np.sin(Th), np.zeros_like(Th)]; thh = np.c_[-np.sin(Th), np.cos(Th), np.zeros_like(Th)]
    cos_ = np.stack([np.cos(n * Th) for n in range(5)], 1); sin_ = np.stack([np.sin(n * Th) for n in range(1, 5)], 1)
    def per_patch(F):
        G = np.c_[F, F * Xi[:, None]]; Z = np.zeros_like(G)
        return np.where((patch == 0)[:, None], np.c_[G, Z], np.c_[Z, G])
    B = dict(share=per_patch(cos_), ur=per_patch(cos_), uth=per_patch(sin_), uz=per_patch(cos_))
    a = np.arange(k0 * SUB + a_off, k1 * SUB, SUB // lpp); ka = a // SUB
    nd = dict(pos=pos, patch=patch, logA=np.log(area), rh=rh, thh=thh, B=B, a=a, ka=ka, dt0=(W["t"][1] - W["t"][0]) / lpp)
    tk = W["t"][k0:k1 + 1]; ta = W["tf"][a]; Kt = np.zeros((len(ta), len(tk)))
    i = np.clip(np.searchsorted(tk, ta, side="right") - 1, 0, len(tk) - 2); f = (ta - tk[i]) / (tk[i + 1] - tk[i])
    Kt[np.arange(len(ta)), i] = 1 - f; Kt[np.arange(len(ta)), i + 1] = f; nd["Kt"] = Kt
    nf = W["nf"]; Pinv = np.linalg.inv(W["Pf"][a]); G = np.zeros((len(a), K + 1, 5, 5)); ok = np.zeros((len(a), K + 1), bool)
    jidx = np.zeros((len(a), K + 1), int); tj = np.zeros((len(a), K + 1))
    for m in range(K + 1):
        j = ka + m; jj = np.minimum(j, nf - 1); P = W["Pf"][a] if m == 0 else W["Ppic"][jj]
        G[:, m] = P @ Pinv; ok[:, m] = j < nf; jidx[:, m] = jj; tj[:, m] = ta if m == 0 else W["t"][jj]
    nd.update(G=G, ok=ok, jidx=jidx, tj=tj, Pinv=Pinv); return nd


def launch_Q(nd):
    ta = W["tf"][nd["a"]]; Q = np.exp(-0.5 * ((ta - TC) / SIG) ** 2); return Q * MTOT / (Q.sum() * nd["dt0"])


def build_forward(nd, Q, eps):
    import jax, jax.numpy as jnp
    Bs, Bur, But, Buz = (jnp.asarray(nd["B"][k]) for k in ("share", "ur", "uth", "uz"))
    logA, pos, rh, thh = (jnp.asarray(nd[k]) for k in ("logA", "pos", "rh", "thh"))
    Kt, G, ok, tj = jnp.asarray(nd["Kt"]), jnp.asarray(nd["G"]), jnp.asarray(nd["ok"]), jnp.asarray(nd["tj"])
    mass_t = jnp.asarray(Q * nd["dt0"]); ZS = W["ZS"]; sg = lambda u: jax.nn.sigmoid(u / eps)
    def fwd(C):
        Ca = Kt @ C
        w = mass_t[:, None] * jax.nn.softmax(Ca[:, SL["share"]] @ Bs.T + logA[None, :], axis=1)
        ur = Ca[:, SL["ur"]] @ Bur.T; uth = Ca[:, SL["uth"]] @ But.T; uz = Ca[:, SL["uz"]] @ Buz.T
        u = ur[..., None] * rh[None] + uth[..., None] * thh[None] + uz[..., None] * jnp.array([0.0, 0.0, 1.0])
        s0 = jnp.stack([jnp.broadcast_to(pos[None, :, 0], ur.shape), jnp.broadcast_to(pos[None, :, 2] - ZS, ur.shape), u[..., 0], u[..., 2],
                        jnp.ones_like(ur)], -1)
        S = jnp.einsum("amkl,ail->aimk", G, s0)
        x, z = S[..., 0], S[..., 1] + ZS; y = pos[None, :, 1, None] + u[..., 1, None] * (tj[:, None, :] - tj[:, None, :1])
        zp, zn = z[..., :-1], z[..., 1:]; f = jnp.clip((zp - FROZ[0]) / jnp.where(jnp.abs(zp - zn) > 1e-12, zp - zn, 1e-12), 0.0, 1.0)
        xc = x[..., :-1] + f * (x[..., 1:] - x[..., :-1]); yc = y[..., :-1] + f * (y[..., 1:] - y[..., :-1])
        hit = sg(zp - FROZ[0]) * sg(FROZ[0] - zn) * sg(FROZ[1] - jnp.abs(xc)) * sg(FROZ[2] - jnp.abs(yc))
        surv = jnp.concatenate([jnp.ones_like(z[..., :1]), jnp.cumprod(1 - hit, axis=-1)], -1)
        up = sg(z - LAND); okm = ok[:, None, :]
        return dict(w=w, u=u, x=x, y=y, z=z, fly=surv * up * okm, froz=(1 - surv) * okm, land=surv * (1 - up) * okm)
    return jax.jit(fwd)


def counters(out, nd, nf):
    """N_fly, frozen, landed (kg) per picture. After its K followed pictures a piece stays frozen or landed (carried forward)."""
    import jax.numpy as jnp
    J = jnp.asarray(nd["jidx"][:, 1:]); w = out["w"]
    def snap(q): return jnp.zeros(nf).at[jnp.broadcast_to(J[:, None, :], q[..., 1:].shape).ravel()].add((w[:, :, None] * q[..., 1:]).ravel())
    jt = jnp.asarray(np.minimum(nd["ka"] + K + 1, nf))
    def tail(q):
        d = jnp.zeros(nf + 1).at[jnp.broadcast_to(jt[:, None], w.shape).ravel()].add((w * q[..., -1]).ravel()); return jnp.cumsum(d)[:nf]
    return snap(out["fly"]), snap(out["froz"]) + tail(out["froz"]), snap(out["land"]) + tail(out["land"])


def cic(out, nd, pics):
    import jax.numpy as jnp
    lo, h, n = GRID["lo"], GRID["h"], GRID["n"]; P = jnp.stack([out["x"], out["y"], out["z"]], -1)[..., 1:, :]
    J = nd["jidx"][:, 1:]; sel = np.isin(J, pics) & nd["ok"][:, 1:]; pi = np.searchsorted(pics, np.where(sel, J, pics[0]))
    g = (P - lo) / h - 0.5; i0 = jnp.floor(g); fr = g - i0; i0 = i0.astype(int)
    wm = (out["w"][:, :, None] * out["fly"][..., 1:]) * jnp.asarray(sel)[:, None, :]
    F = jnp.zeros((len(pics),) + tuple(n)); PI = jnp.broadcast_to(jnp.asarray(pi)[:, None, :], wm.shape)
    for c in ((0, 0, 0), (0, 0, 1), (0, 1, 0), (0, 1, 1), (1, 0, 0), (1, 0, 1), (1, 1, 0), (1, 1, 1)):
        cc = jnp.array(c); ii = i0 + cc; wt = jnp.prod(jnp.where(cc == 1, fr, 1 - fr), -1)
        inb = jnp.all((ii >= 0) & (ii < jnp.asarray(n)), -1); iic = jnp.clip(ii, 0, jnp.asarray(n) - 1)
        F = F.at[PI.ravel(), iic[..., 0].ravel(), iic[..., 1].ravel(), iic[..., 2].ravel()].add((wm * wt * inb).ravel())
    return F


def blur_mats(sig):
    """Gaussian blur matrices per axis (10 mm cells), columns normalised so mass is kept: B[a, b] = share of cell b sent to cell a."""
    out = []
    for n in GRID["n"]:
        i = np.arange(n); M = np.exp(-0.5 * ((i[:, None] - i[None, :]) * GRID["h"] / sig) ** 2); out.append(M / M.sum(0, keepdims=True))
    return out


def blur(F, Bm):
    import jax.numpy as jnp
    F = jnp.einsum("ax,pxyz->payz", Bm[0], F); F = jnp.einsum("by,pxyz->pxbz", Bm[1], F); return jnp.einsum("cz,pxyz->pxyc", Bm[2], F)


def deck_field(out, nd, t0, W_=0.1, c=0.02):
    x, y, z, w = (np.asarray(out[k]) for k in ("x", "y", "z", "w")); tj = nd["tj"][:, None, :]; ok = nd["ok"][:, None, :]
    zp, zn = z[..., :-1], z[..., 1:]; cr = (zp > DECK[0]) & (zn <= DECK[0]) & ok[..., 1:]
    f = np.clip((zp - DECK[0]) / np.where(np.abs(zp - zn) > 1e-12, zp - zn, 1e-12), 0, 1)
    xc = x[..., :-1] + f * (x[..., 1:] - x[..., :-1]); yc = y[..., :-1] + f * (y[..., 1:] - y[..., :-1])
    tc = np.broadcast_to(tj[..., :-1] + f * (tj[..., 1:] - tj[..., :-1]), cr.shape); wm = np.broadcast_to(w[..., None], cr.shape)
    on = cr & (np.abs(xc) < DECK[1]) & (np.abs(yc) < DECK[2]); nx, ny = int(round(2 * DECK[1] / c)) + 1, int(round(2 * DECK[2] / c)) + 1
    nw = int(np.ceil((W["t"][-1] - t0) / W_)) + 1; Fd = np.zeros((nw, nx, ny))
    np.add.at(Fd, (np.clip(((tc[on] - t0) / W_).astype(int), 0, nw - 1), ((xc[on] + DECK[1]) / c).astype(int), ((yc[on] + DECK[2]) / c).astype(int)), wm[on])
    return Fd, float(wm[on].sum()), float(wm[cr & ~on].sum())


def recontact(out, nd):
    """Classify every path by the first solid it meets (a: back in the glass, b: wall film, c: deck, d: off); masses in kg."""
    w, u = np.asarray(out["w"]), np.asarray(out["u"]); pos = nd["pos"]; ZS = W["ZS"]; nf = len(W["tf"])
    Rz = lambda z: np.interp(np.clip(z / W["DZP"], 0, len(W["Rp"]) - 1), np.arange(len(W["Rp"])), W["Rp"])
    Rfoot = float(W["Rp"][0]) + WALL; tot = np.zeros(4)
    for i_a, a in enumerate(nd["a"]):
        n_ = np.arange(0, min(K * SUB, nf - 1 - a) + 1); P = W["Pf"][a + n_] @ nd["Pinv"][i_a]       # (T, 5, 5)
        s0 = np.c_[pos[:, 0], pos[:, 2] - ZS, u[i_a, :, 0], u[i_a, :, 2], np.ones(len(pos))]
        S = np.einsum("tkl,il->itk", P, s0); x, z = S[..., 0], S[..., 1] + ZS
        y = pos[:, 1, None] + u[i_a, :, 1, None] * (W["tf"][a + n_] - W["tf"][a])[None]; r = np.hypot(x, y); big = len(n_) + 1
        zp, zn, rn = z[:, :-1], z[:, 1:], r[:, 1:]
        ea = (zp >= W["zrim"]) & (zn < W["zrim"]) & (rn < W["Rrim"])
        rout = np.where(zn >= 0, Rz(zn) + WALL, Rfoot)
        eb = (zn < W["zrim"]) & (zn >= FOOT) & (rn <= rout) & ~ea
        ec = (zp > DECK[0]) & (zn <= DECK[0]) & (np.abs(x[:, 1:]) < DECK[1]) & (np.abs(y[:, 1:]) < DECK[2])
        first = lambda e: np.where(e.any(1), e.argmax(1), big)
        fa, fb, fc = first(ea), first(eb), first(ec); best = np.minimum(np.minimum(fa, fb), fc)
        cls = np.where(best == big, 3, np.where(best == fa, 0, np.where(best == fb, 1, 2)))
        np.add.at(tot, cls, w[i_a])
    return dict(back_in_glass=tot[0], wall_film=tot[1], deck=tot[2], off=tot[3])


# ------------------------------------------------------------------ the twin
TC, SIG, MTOT = 0.85, 0.06, 0.0756


def hand_coeffs(nk, tk):
    """Truth at the knots. Share: cylinder 2.0 cos(theta) + 0.5 xi; top -0.5 + 1.0 cos(theta) (about a quarter through the top).
    Velocities (m/s): cylinder u_r 0.42 + 0.15 cos, u_theta 0.05 sin, u_z 0.25 + 0.05 xi; top u_r 0.20 + 0.10 cos, u_z 0.60;
    all scaled by 1 + 0.3 (t0 - 0.85 s) / 0.1 s."""
    C = np.zeros((nk, NPK)); sc = 1 + 0.3 * (tk - TC) / 0.1
    C[:, 1] = 2.0; C[:, 5] = 0.5; C[:, 10] = -0.5; C[:, 11] = 1.0
    C[:, 20] = 0.42 * sc; C[:, 21] = 0.15 * sc; C[:, 30] = 0.20 * sc; C[:, 31] = 0.10 * sc
    C[:, 40] = 0.05 * sc
    C[:, 56] = 0.25 * sc; C[:, 61] = 0.05 * sc; C[:, 66] = 0.60 * sc
    return C


def first_guess(nk):
    C = np.zeros((nk, NPK)); C[:, 20] = C[:, 30] = 0.30; C[:, 56] = C[:, 66] = 0.10; return C


def moments_start(fF, nd, n_obs, lam, pics, nk, passes=3):
    """C0 from the first moments of the observed in-flight field (linear in the launch velocities; masks of the last pass held)."""
    import jax.numpy as jnp
    lo, h = GRID["lo"], GRID["h"]; cx = [lo[d] + h * (np.arange(GRID["n"][d]) + 0.5) for d in range(3)]
    mass = n_obs / lam[:, None, None, None] * MP_
    obs = np.stack([np.einsum("pxyz,x->p", mass, cx[0]), np.einsum("pxyz,z->p", mass, cx[2])], 1)        # (P, 2): sum m x, sum m z
    use = mass.sum((1, 2, 3)) > 0.01 * mass.sum((1, 2, 3)).max()
    C = first_guess(nk); G = nd["G"]; pos = nd["pos"]; ZS = W["ZS"]; Kt = nd["Kt"]
    J = nd["jidx"][:, 1:]; sel = np.isin(J, pics) & nd["ok"][:, 1:]; pi = np.searchsorted(pics, np.where(sel, J, pics[0]))
    for _ in range(passes):
        o = fF(jnp.asarray(C)); w = np.asarray(o["w"]); fly = np.asarray(o["fly"])[..., 1:] * sel[:, None, :]; wf = w[:, :, None] * fly    # (A, I, M)
        Gm = G[:, 1:]                                                                     # (A, M, 5, 5)
        s_fix = np.stack([np.broadcast_to(pos[:, 0], w.shape), np.broadcast_to(pos[:, 2] - ZS, w.shape), np.ones_like(w)], -1)  # x0, Z0, 1
        rows = []
        for comp in (0, 1):                                                               # x and Z rows of the propagator
            g_fix = Gm[:, :, comp][..., [0, 1, 4]]                                        # (A, M, 3)
            fix = np.einsum("amc,aic->aim", g_fix, s_fix)                                  # (A, I, M)
            dur = np.einsum("am,i->aim", Gm[:, :, comp, 2], nd["rh"][:, 0])               # d/du_r through vx = u_r rhat_x
            duz = np.broadcast_to(Gm[:, :, comp, 3][:, None, :], wf.shape)                # d/du_z through vz = u_z
            add = (comp == 1) * ZS
            def per_pic(q): o_ = np.zeros(len(pics)); np.add.at(o_, np.broadcast_to(pi[:, None, :], q.shape).ravel(), q.ravel()); return o_
            b0 = per_pic(wf * (fix + add))
            Ar = np.stack([per_pic(wf * dur * Kt[:, k][:, None, None]) for k in range(nk)], 1)
            Az = np.stack([per_pic(wf * duz * Kt[:, k][:, None, None]) for k in range(nk)], 1)
            rows.append((np.c_[Ar, Az][use], obs[use, comp] - b0[use]))
        A_ = np.r_[rows[0][0], rows[1][0]]; b_ = np.r_[rows[0][1], rows[1][1]]
        D = np.diff(np.eye(nk), axis=0); R = np.r_[np.c_[D, 0 * D], np.c_[0 * D, D]]; lam_s = 1e-3 * np.trace(A_.T @ A_) / (2 * nk)
        sol = np.linalg.lstsq(np.r_[A_, np.sqrt(lam_s) * R], np.r_[b_, np.zeros(len(R))], rcond=None)[0]
        C[:, 20] = C[:, 30] = sol[:nk]; C[:, 56] = C[:, 66] = sol[nk:]
    return C


def twin():
    import jax, jax.numpy as jnp
    from scipy.optimize import minimize
    jax.config.update("jax_enable_x64", True)
    t, nf = W["t"], W["nf"]; k0 = int(np.searchsorted(t, TC - 3.8 * SIG)); k1 = int(np.searchsorted(t, TC + 4.2 * SIG))
    if SMOKE: k0, k1 = int(np.searchsorted(t, TC - 0.05)), int(np.searchsorted(t, TC + 0.05))
    tk = t[k0:k1 + 1]; nk = len(tk)
    ndT = nodes(48, k0, k1); ndF = nodes(48, k0, k1, th_shift=0.5, xi_mode="gl", a_off=SUB // 8)
    QT, QF = launch_Q(ndT), launch_Q(ndF)
    say(f"\n## Twin: truth {len(ndT['a'])} launch times x {ndT['pos'].shape[0]} nodes, fit {len(ndF['a'])} x {ndF['pos'].shape[0]} (shifted); "
        f"{nk} knots x {NPK} = {nk * NPK} unknowns; launch window t = {tk[0]:.3f} to {tk[-1]:.3f} s\n")
    CT = hand_coeffs(nk, tk); fT = build_forward(ndT, QT, EPS_TRUE); oT = fT(jnp.asarray(CT))
    nfT, nsT, nlT = (np.asarray(q) for q in counters(oT, ndT, nf))
    pics = np.arange(k0 + 1, min(nf, k1 + K + 1)); pics = pics[pics % 2 == 0]
    MT = np.asarray(cic(oT, ndT, pics)); listed = (nfT + nsT) / MP_
    lam = np.minimum(1.0, LIST_CAP / np.maximum(listed, 1.0))[pics]
    rng = np.random.default_rng(5); n_obs = rng.poisson(lam[:, None, None, None] * MT / MP_).astype(float)
    xs, ys, zs = (np.asarray(oT[k])[..., 1:] for k in ("x", "y", "z")); flyw = np.asarray(oT["w"])[:, :, None] * np.asarray(oT["fly"])[..., 1:]
    insel = np.isin(ndT["jidx"][:, 1:], pics)[:, None, :]; hi = GRID["lo"] + GRID["h"] * GRID["n"]
    outside = (xs < GRID["lo"][0]) | (xs > hi[0]) | (ys < GRID["lo"][1]) | (ys > hi[1]) | (zs < GRID["lo"][2]) | (zs > hi[2])
    out_share = float((flyw * insel * outside).sum() / max((flyw * insel).sum(), 1e-30))
    say(f"Truth: {MTOT * 1e3:.2f} g launched; at the last picture frozen {nsT[-1] * 1e3:.2f} g, landed {nlT[-1] * 1e3:.2f} g, in flight "
        f"{nfT[-1] * 1e3:.3f} g. Fake pictures: {len(pics)} even pictures, {int(n_obs.sum()):,} listed markers, thinning {lam.min():.3f} to {lam.max():.3f}.")
    # ---- GATE
    fF = build_forward(ndF, QF, EPS_FIT); fFh = build_forward(ndF, QF, EPS_TRUE)
    FT, onT, offT = deck_field(oT, ndT, t[0]); FTc, _, _ = deck_field(fFh(jnp.asarray(CT)), ndF, t[0])
    L1 = lambda A, B: float(np.abs(A - B).sum() / max(B.sum(), 1e-30)); g_deck = L1(FTc, FT)
    gate_ok = g_deck < GATE_DECK and out_share < GATE_OUT
    REP["gate"] = dict(deck_L1_truth_on_fit_nodes=g_deck, in_flight_outside_grid=out_share, PASS=gate_ok)
    say(f"GATE: the truth's coefficients on the fit's nodes reproduce the truth's deck field to L1 {100 * g_deck:.2f} % (mark < {100 * GATE_DECK:.0f} %); "
        f"in-flight mass outside the grid {100 * out_share:.2f} % (mark < {100 * GATE_OUT:.0f} %): **{'PASS' if gate_ok else 'FAIL'}**")
    if not gate_ok and not SMOKE: raise Stop("the gate failed; no fit is run")
    if not gate_ok: say("(SMOKE: the gate is reported, not enforced; the fit runs to exercise its code.)")
    # ---- start from moments
    t_ = time.time(); C0 = moments_start(fF, ndF, n_obs, lam, pics, nk)
    say(f"Start from moments ({time.time() - t_:.0f} s): mean u_r per knot {C0[0, 20]:.3f} .. {C0[-1, 20]:.3f} m/s, u_z {C0[0, 56]:.3f} .. {C0[-1, 56]:.3f} m/s "
        f"(truth's cylinder means {CT[0, 20]:.3f} .. {CT[-1, 20]:.3f} and {CT[0, 56]:.3f} .. {CT[-1, 56]:.3f}).")
    # ---- multiscale fits
    s_cnt = 0.01 * nfT.max() / MP_; nfly_obs = jnp.asarray(nfT / MP_); lamj = jnp.asarray(lam)
    vel = np.zeros(NPK, bool); vel[20:] = True; C0v = jnp.asarray(C0[:, vel])
    def make_J(Bm):
        nobs = jnp.asarray(n_obs) if Bm is None else blur(jnp.asarray(n_obs), Bm)
        def J(Cflat, MU):
            C = Cflat.reshape(nk, NPK); o = fF(C); M = cic(o, ndF, pics); mu = lamj[:, None, None, None] * M / MP_
            if Bm is not None: mu = blur(mu, Bm)
            mu = mu + 1e-9; nll = jnp.sum(mu - nobs * jnp.log(mu))
            cnt = jnp.sum((counters(o, ndF, nf)[0] / MP_ - nfly_obs) ** 2) / (2 * s_cnt ** 2)
            return nll + cnt + MU * jnp.sum(jnp.diff(C, axis=0) ** 2) + 0.01 * MU * jnp.sum((C[:, vel] - C0v) ** 2)
        return jax.jit(jax.value_and_grad(J))
    def deviance(x):
        o = fF(jnp.asarray(x.reshape(nk, NPK))); mu = np.asarray(lamj[:, None, None, None] * cic(o, ndF, pics) / MP_) + 1e-9; n = n_obs
        use = (n > 0) | (mu > 1e-3); d = 2 * (np.where(n > 0, n * np.log(np.maximum(n, 1) / mu), 0.0) - (n - mu)); return float(d[use].sum() / max(use.sum(), 1)), int(use.sum())
    stages = [("blur 40 mm", 0.040, MU_HI), ("blur 20 mm", 0.020, MU_HI)] + [(f"unblurred MU {m:g}", None, m) for m in MU_LADDER]
    x = C0.ravel(); fits = []; neval = [0]; tev = [0.0]
    for name, sig, MU in stages:
        vg = make_J(None if sig is None else blur_mats(sig)); t_ = time.time()
        def fun(v):
            t1 = time.time(); val, g = vg(jnp.asarray(v), MU); r_ = (float(val), np.asarray(g, float)); neval[0] += 1; tev[0] += time.time() - t1; return r_
        r = minimize(fun, x, jac=True, method="L-BFGS-B", options=dict(maxiter=MAXIT)); x = r.x
        dpd, ncell = deviance(x); fits.append(dict(stage=name, MU=MU, blurred=sig is not None, x=x, dev=dpd, it=int(r.nit), nfev=int(r.nfev), J=float(r.fun), s=time.time() - t_))
        say(f"- {name}: {r.nit} iterations, {r.nfev} evaluations, {time.time() - t_:.0f} s, J = {r.fun:.5g}, unblurred deviance per datum {dpd:.3f} over {ncell:,} cells")
    per_eval = tev[0] / max(neval[0], 1); REP["seconds_per_evaluation"] = per_eval
    say(f"Seconds per evaluation of J and its gradient (measured, after compilation): {per_eval:.3f} s over {neval[0]} evaluations.")
    unb = [f for f in fits if not f["blurred"]]; ok_ = [f for f in unb if f["dev"] <= 1.0]
    best = max(ok_, key=lambda f: f["MU"]) if ok_ else min(unb, key=lambda f: f["MU"])
    say(f"Chosen by the discrepancy principle: MU = {best['MU']:g} (deviance per datum {best['dev']:.3f}{'' if ok_ else '; none reached 1, the smallest MU taken'}).")
    # ---- verdict on the truth's nodes
    CR = best["x"].reshape(nk, NPK); oR = fT(jnp.asarray(CR)); o0 = fT(jnp.asarray(C0)); oG = fT(jnp.asarray(first_guess(nk)))
    FR, onR, offR = deck_field(oR, ndT, t[0]); F0, _, _ = deck_field(o0, ndT, t[0]); FG, _, _ = deck_field(oG, ndT, t[0])
    l1R, l10, l1G = L1(FR, FT), L1(F0, FT), L1(FG, FT)
    _, nsR, nlR = (np.asarray(q) for q in counters(oR, ndT, nf)); dS = float(np.abs(nsR - nsT).max() * 1e3); dL = float(np.abs(nlR - nlT).max() * 1e3)
    say(f"\nDeck under section 8's geometry (the recovered source on the truth's nodes), mass per 20 mm cell and 0.1 s window, L1 against the truth: "
        f"**{100 * l1R:.2f} %** (start from moments {100 * l10:.1f} %, plain first guess {100 * l1G:.1f} %; mark {100 * PASS_L1:.0f} %): **{'PASS' if l1R <= PASS_L1 else 'FAIL'}**")
    say(f"On the deck: truth {onT * 1e3:.2f} g, recovered {onR * 1e3:.2f} g; off it: truth {offT * 1e3:.2f} g, recovered {offR * 1e3:.2f} g. "
        f"Counter curves, largest deviation: frozen {dS:.3f} g, landed {dL:.3f} g.")
    rcT, rcR = recontact(oT, ndT), recontact(oR, ndT)
    say("\nRe-contact, first solid met (truth / recovered, g): " + "; ".join(f"{k.replace('_', ' ')} {rcT[k] * 1e3:.2f} / {rcR[k] * 1e3:.2f}" for k in rcT) + ".")
    REP["twin"] = dict(knots=nk, unknowns=nk * NPK, pics=len(pics), listed=int(n_obs.sum()), fits=[{k: v for k, v in f.items() if k != "x"} for f in fits],
                       MU=best["MU"], L1_deck_recovered=l1R, L1_deck_moments=l10, L1_deck_first_guess=l1G, deck_on_true_g=onT * 1e3, deck_on_rec_g=onR * 1e3,
                       deck_off_true_g=offT * 1e3, deck_off_rec_g=offR * 1e3, max_dev_stuck_g=dS, max_dev_landed_g=dL,
                       recontact_true_g={k: v * 1e3 for k, v in rcT.items()}, recontact_rec_g={k: v * 1e3 for k, v in rcR.items()}, PASS=l1R <= PASS_L1)
    np.savez_compressed(os.path.join(OUT, "twin.npz"), deck_true=FT, deck_rec=FR, deck_moments=F0, stuck_true=nsT, stuck_rec=nsR, landed_true=nlT,
                        landed_rec=nlR, C_true=CT, C_rec=CR, C_moments=C0, t=t)


def timing():
    """SMOKE only: one full-size fit evaluation (full launch window, full node set), timed after compilation."""
    import jax, jax.numpy as jnp
    jax.config.update("jax_enable_x64", True)
    t, nf = W["t"], W["nf"]; k0 = int(np.searchsorted(t, TC - 3.8 * SIG)); k1 = int(np.searchsorted(t, TC + 4.2 * SIG)); nk = k1 - k0 + 1
    nd = nodes(48, k0, k1, th_shift=0.5, xi_mode="gl", a_off=SUB // 8); fF = build_forward(nd, launch_Q(nd), EPS_FIT)
    pics = np.arange(k0 + 1, min(nf, k1 + K + 1)); pics = pics[pics % 2 == 0]; Bm = blur_mats(0.020)
    def J(Cflat):
        C = Cflat.reshape(nk, NPK); o = fF(C); mu = blur(cic(o, nd, pics), Bm) + 1e-9
        return jnp.sum(mu - jnp.log(mu)) + jnp.sum(counters(o, nd, nf)[0] ** 2) + jnp.sum(jnp.diff(C, axis=0) ** 2)
    vg = jax.jit(jax.value_and_grad(J)); x = jnp.asarray(first_guess(nk).ravel())
    t_ = time.time(); v, g = vg(x); g.block_until_ready(); tc = time.time() - t_; ts_ = []
    for _ in range(3):
        t_ = time.time(); v, g = vg(x + 1e-3); g.block_until_ready(); ts_.append(time.time() - t_)
    REP["timing_full_size"] = dict(compile_and_first_s=tc, per_eval_s=float(np.median(ts_)), knots=nk, launch_times=len(nd["a"]), nodes=nd["pos"].shape[0], pictures=len(pics))
    say(f"\nTiming, full size ({len(nd['a'])} launch times x {nd['pos'].shape[0]} nodes, {nk} knots, {len(pics)} pictures, blurred): "
        f"compile + first {tc:.1f} s, then {np.median(ts_):.3f} s per evaluation of J and its gradient (median of 3).")


steps = [("frame", frame), ("twin", twin)] + ([("timing", timing)] if SMOKE else [])
for name, fn in steps:
    block(name, fn)
say(f"\nWall time {time.time() - T0:.0f} s on Kaggle CPU."); flush()
sys.exit(1 if ERR else 0)

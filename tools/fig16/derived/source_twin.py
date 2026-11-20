"""Fig. 16 spill, step 2 of notes/spill/DERIVATION-flight-inversion.md section 9: the forward model (section 5) and the TWIN test
(section 7). Kaggle CPU. Needs flight_map.py beside it (same commit) and the dataset fig16-guinness-cart-control (for the frame only:
t, v, vzc, om, th; no stored liquid is used).   python3 source_twin.py OUTDIR        SMOKE=1: tiny sizes, every block, seconds.

THE SOURCE (section 4, extended by step 1's finding A4: 24 % of the liquid in the air at picture 58 sat above the grid's top inside the
rim's radius, so liquid also leaves through the top). Launch surface = the stored solver's leave rule (stout_jax.py:865-867):
  patch 0, the rim's cylinder r = R_rim, z_rim <= z <= z_top;   patch 1, the grid's top disk z = z_top, r < R_rim.
Quadrature nodes on both patches (theta over the full circle; zeta = height on the cylinder, rho = radius on the disk, each mapped to
xi in [-1, 1]); launch times on a sub-picture grid. Unknowns at knots (one per picture in the launch window), linear in t0 between:
  share logits:  cos(n theta), n = 0..4, times {1, xi}, per patch                        20
  u_r, u_z:      the same basis                                                           20 + 20
  u_theta:       sin(n theta), n = 1..4, times {1, xi}, per patch (odd in y: mirror)      16        -> 76 per knot
The share is a softmax over the nodes of one launch time with log(area) added, so the mass is EXACTLY Q(t0) dt0 per launch time
(constraint (2)): sum over nodes = 1.

THE FORWARD MODEL (section 5). Each node carried by eq. (1) with step 1's matrices: [s; 1](t_j) = Phi(t_j) Phi(t0)^-1 [s0; 1],
s = (x, z - zS, vx, vz); y = y0 + vy (t - t0). The stored solver's rules: frozen when crossing z = -14 mm inside |x| < 110 mm,
|y| < 60 mm (stout_jax.py:876); landed below z = -250 mm (:878). Crossings between pictures by linear interpolation of the state
(positions move ~17 mm per picture, curvature ~1.4 mm at 10 m/s^2). For the gradient the yes/no tests are logistic steps of width
EPS = 1 mm (the truth uses 0.01 mm). Predicted: N_fly(t_j), N_stuck(t_j), N_landed(t_j); mass in flight per 10 mm cell (cloud-in-cell).

THE TWIN (section 7). A source chosen by hand (below), on a FINER quadrature than the fit uses (4 launch times per picture, 48 theta,
3 zeta and 3 rho, against 2, 24, 2, 2), so the fit does not share the truth's discretisation. Fake pictures: listed counts per 10 mm
cell are Poisson with mean lambda_j M_jc / m_p, lambda_j = min(1, 16 384 / markers listed), the stored thinning; even pictures only.
Fake counter N_fly(t_j): exact (noise-free), as stored. The fit minimises
  J = sum_{j even, c} [mu_jc - n_jc ln mu_jc] + sum_j (N_fly_hat - N_fly)^2 / (2 s^2) + MU |D C|^2 + 0.01 MU |C_vel - C_vel,0|^2,
s = 1 % of the largest N_fly (the coarse quadrature's own error), D first differences between knots; L-BFGS-B (SciPy) on the exact
JAX gradient; MU by the discrepancy principle over MU_LADDER: the largest MU whose Poisson deviance per datum is <= 1 (Morozov);
if none, the smallest.
PASS MARK (fixed here before the run; Opinion): the recovered deck flux under section 8's geometry (no old body; the plane z = -30 mm,
310 x 124 mm), mass per 20 mm cell and 0.1 s window, L1 against the truth's divided by the truth's total: <= 5 %. Reported beside it:
the same for the first guess (the baseline the fit must beat), deck mass on and off, the counter curves stuck and landed.
OUTPUT: REPORT.md, report.json (rewritten after every block), twin.npz (truth and recovered deck fields, counter curves)."""
import json, os, sys, time, traceback, urllib.request
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
OUT = sys.argv[1] if len(sys.argv) > 1 else "/kaggle/working"; os.makedirs(OUT, exist_ok=True)
SMOKE = os.environ.get("SMOKE", "0") == "1"
MD, REP, ERR, W = [], {}, [], {}; T0 = time.time()
LIST_CAP, MP = 16384, None
EPS_FIT, EPS_TRUE = 1e-3, 1e-5
FROZ = (-0.014, 0.110, 0.060); LAND = -0.25; DECK = (-0.030, 0.155, 0.062)
GRID = dict(lo=np.array([-0.25, -0.15, -0.26]), h=0.010, n=np.array([50, 30, 51]))
K = 30                                                                    # pictures followed after launch (0.5 s)
MU_LADDER = (1e-2,) if SMOKE else (1e2, 1e0, 1e-2); MAXIT = 5 if SMOKE else 400
PASS_L1 = 0.05


def say(s=""):
    print(s, flush=True); MD.append(s)


def flush():
    md = MD + (["\n## Block failures\n"] + [f"- `{e['block']}`: {e['error']}" for e in ERR] if ERR else [])
    open(os.path.join(OUT, "REPORT.md"), "w").write("\n".join(md) + "\n")
    json.dump(dict(REP, errors=ERR), open(os.path.join(OUT, "report.json"), "w"), indent=1,
              default=lambda o: float(o) if np.ndim(o) == 0 else np.asarray(o).tolist())


def block(name, fn):
    t_ = time.time()
    try:
        fn(); print(f"[block {name}: done in {time.time() - t_:.1f} s]", flush=True)
    except Exception as e:
        ERR.append(dict(block=name, error=f"{type(e).__name__}: {e}", trace=traceback.format_exc()))
        print(f"[block {name}: FAILED]\n{traceback.format_exc()}", flush=True)
    flush()


# ------------------------------------------------------------------ the frame (step 1's code, imported)
def frame():
    import flight_map as fm
    fm.load(); fm.frame()
    t = fm.D["t"]; nf = len(t); SUB = 4
    tf = np.concatenate([t[k] + (t[k + 1] - t[k]) * np.arange(SUB) / SUB for k in range(nf - 1)] + [t[-1:]])
    omf = np.interp(tf, t, fm.D["omf"]); alk = np.repeat(fm.D["al_k"], SUB); bf = np.repeat(fm.D["b"], SUB, axis=0)
    ts, Ps, ks = fm.propagate(tf, omf[:-1], alk, bf)
    last = np.r_[0, np.where(np.diff(ks) != 0)[0], len(ts) - 1]; Pf = Ps[last]
    if len(Pf) != len(tf): raise RuntimeError(f"fine grid {len(tf)} against {len(Pf)} matrices")
    js = urllib.request.urlopen("https://raw.githubusercontent.com/Numa1997/SiteTest/main/public/scripts/guinness-glass.js", timeout=30).read().decode()
    Rp = np.array([float(v) for v in js.split("R: [")[1].split("]")[0].split(",")]); zrim = (len(Rp) - 1) * fm.DZP
    nz = int(np.ceil((zrim + 0.02) / fm.DX)) + 2; ztop = -2 * fm.DX + (nz - 1) * fm.DX
    W.update(t=t, nf=nf, SUB=SUB, tf=tf, Pf=Pf, Ppic=Pf[::SUB], ZS=fm.ZS, Rrim=float(Rp[-1]), zrim=zrim, ztop=ztop)
    det = float(np.abs(np.linalg.det(Pf[:, :4, :4]) - 1).max())
    say("# Fig. 16 spill, step 2: forward model and twin test (DERIVATION-flight-inversion.md section 9)\n" + ("**SMOKE RUN: tiny sizes, numbers are not results.**\n" if SMOKE else ""))
    say(f"Frame: {nf} pictures, fine grid {len(tf)} times ({SUB} per picture), largest |det Psi - 1| {det:.1e}. Rim z {zrim * 1e3:.1f} mm, "
        f"radius {W['Rrim'] * 1e3:.1f} mm, grid top {ztop * 1e3:.1f} mm.")
    REP["frame"] = dict(fine_times=len(tf), det_err=det, zrim=zrim, Rrim=W["Rrim"], ztop=ztop)


# ------------------------------------------------------------------ nodes and basis
def nodes(nth, nxi, launch_per_pic, k0, k1):
    """Launch times (fine-grid indices a, 4 per picture) and surface nodes; basis matrices."""
    Rr, zr, zt = W["Rrim"], W["zrim"], W["ztop"]; th = (np.arange(nth) + 0.5) * 2 * np.pi / nth; xi = (np.arange(nxi) + 0.5) / nxi * 2 - 1
    T, X = np.meshgrid(th, xi, indexing="ij"); T, X = T.ravel(), X.ravel()
    zc = zr + (X + 1) / 2 * (zt - zr); rc = (X + 1) / 2 * Rr
    pos = np.r_[np.c_[Rr * np.cos(T), Rr * np.sin(T), zc], np.c_[rc * np.cos(T), rc * np.sin(T), np.full_like(T, zt)]]
    patch = np.r_[np.zeros(len(T), int), np.ones(len(T), int)]; Th = np.r_[T, T]; Xi = np.r_[X, X]
    dth = 2 * np.pi / nth; area = np.r_[np.full(len(T), Rr * dth * (zt - zr) / nxi), rc * dth * Rr / nxi]
    rh = np.c_[np.cos(Th), np.sin(Th), np.zeros_like(Th)]; thh = np.c_[-np.sin(Th), np.cos(Th), np.zeros_like(Th)]
    cos_ = np.stack([np.cos(n * Th) for n in range(5)], 1); sin_ = np.stack([np.sin(n * Th) for n in range(1, 5)], 1)
    def per_patch(F):                                                  # [F, F xi] in the columns of the node's own patch
        G = np.c_[F, F * Xi[:, None]]; Z = np.zeros_like(G)
        return np.where((patch == 0)[:, None], np.c_[G, Z], np.c_[Z, G])
    B = dict(share=per_patch(cos_), ur=per_patch(cos_), uth=per_patch(sin_), uz=per_patch(cos_))
    SUB = W["SUB"]; step = SUB // launch_per_pic
    a = np.arange(k0 * SUB, k1 * SUB, step); ka = a // SUB
    return dict(pos=pos, patch=patch, logA=np.log(area), rh=rh, thh=thh, B=B, a=a, ka=ka, dt0=(W["t"][1] - W["t"][0]) / launch_per_pic)


def knot_matrix(nd, k0, k1):
    """Linear interpolation from knots at pictures k0..k1 to the launch times."""
    tk = W["t"][k0:k1 + 1]; ta = W["tf"][nd["a"]]; M = np.zeros((len(ta), len(tk)))
    i = np.clip(np.searchsorted(tk, ta, side="right") - 1, 0, len(tk) - 2); f = (ta - tk[i]) / (tk[i + 1] - tk[i])
    M[np.arange(len(ta)), i] = 1 - f; M[np.arange(len(ta)), i + 1] = f; return M


def propagators(nd):
    """G[a, m] = Phi(t_{k_a + m}) Phi(t_a)^-1, m = 0..K (m = 0: the launch itself); mask where the picture exists."""
    nf = W["nf"]; Pinv = np.linalg.inv(W["Pf"][nd["a"]]); G = np.zeros((len(nd["a"]), K + 1, 5, 5)); ok = np.zeros((len(nd["a"]), K + 1), bool)
    jidx = np.zeros((len(nd["a"]), K + 1), int); tj = np.zeros((len(nd["a"]), K + 1))
    for m in range(K + 1):
        j = nd["ka"] + m; okm = j < nf; jj = np.minimum(j, nf - 1)
        P = W["Pf"][nd["a"]] if m == 0 else W["Ppic"][jj]
        G[:, m] = P @ Pinv; ok[:, m] = okm; jidx[:, m] = jj; tj[:, m] = W["tf"][nd["a"]] if m == 0 else W["t"][jj]
    nd.update(G=G, ok=ok, jidx=jidx, tj=tj); return nd


NPK = 76
SL = dict(share=slice(0, 20), ur=slice(20, 40), uth=slice(40, 56), uz=slice(56, 76))


def build_forward(nd, Q, eps):
    """A jitted function C (nknot, 76) -> dict of predicted arrays, for one node set and launch rate Q (kg/s at each launch time)."""
    import jax, jax.numpy as jnp
    jax.config.update("jax_enable_x64", True)
    Bs, Bur, But, Buz = (jnp.asarray(nd["B"][k]) for k in ("share", "ur", "uth", "uz"))
    logA, pos, rh, thh = (jnp.asarray(nd[k]) for k in ("logA", "pos", "rh", "thh"))
    Kt, G, ok, tj = jnp.asarray(nd["Kt"]), jnp.asarray(nd["G"]), jnp.asarray(nd["ok"]), jnp.asarray(nd["tj"])
    mass_t = jnp.asarray(Q * nd["dt0"]); ZS = W["ZS"]; sg = lambda u: jax.nn.sigmoid(u / eps)
    def fwd(C):
        Ca = Kt @ C                                                       # (A, 76) coefficients at each launch time
        logit = Ca[:, SL["share"]] @ Bs.T + logA[None, :]                 # (A, I)
        w = mass_t[:, None] * jax.nn.softmax(logit, axis=1)               # kg per node, sums to Q dt0 per launch time
        ur = Ca[:, SL["ur"]] @ Bur.T; uth = Ca[:, SL["uth"]] @ But.T; uz = Ca[:, SL["uz"]] @ Buz.T
        u = ur[..., None] * rh[None] + uth[..., None] * thh[None] + uz[..., None] * jnp.array([0.0, 0.0, 1.0])   # (A, I, 3)
        s0 = jnp.stack([jnp.broadcast_to(pos[None, :, 0], ur.shape), jnp.broadcast_to(pos[None, :, 2] - ZS, ur.shape), u[..., 0], u[..., 2],
                        jnp.ones_like(ur)], -1)                           # (A, I, 5)
        S = jnp.einsum("amkl,ail->aimk", G, s0)                           # (A, I, M, 5)
        x, z = S[..., 0], S[..., 1] + ZS; y = pos[None, :, 1, None] + u[..., 1, None] * (tj[:, None, :] - tj[:, None, :1])
        zp, zn = z[..., :-1], z[..., 1:]; f = jnp.clip((zp - FROZ[0]) / jnp.where(jnp.abs(zp - zn) > 1e-12, zp - zn, 1e-12), 0.0, 1.0)
        xc = x[..., :-1] + f * (x[..., 1:] - x[..., :-1]); yc = y[..., :-1] + f * (y[..., 1:] - y[..., :-1])
        hit = sg(zp - FROZ[0]) * sg(FROZ[0] - zn) * sg(FROZ[1] - jnp.abs(xc)) * sg(FROZ[2] - jnp.abs(yc))
        surv = jnp.concatenate([jnp.ones_like(z[..., :1]), jnp.cumprod(1 - hit, axis=-1)], -1)        # not frozen by picture m
        up = sg(z - LAND); okm = ok[:, None, :]
        fly = surv * up * okm; froz = (1 - surv) * okm; land = surv * (1 - up) * okm
        return dict(w=w, x=x, y=y, z=z, fly=fly, froz=froz, land=land, S=S)
    return jax.jit(fwd)


def counters(out, nd, nf):
    import jax.numpy as jnp
    J = jnp.asarray(nd["jidx"][:, 1:]); w = out["w"][:, :, None]
    def acc(q): return jnp.zeros(nf).at[jnp.broadcast_to(J[:, None, :], q[..., 1:].shape).ravel()].add((w * q[..., 1:]).ravel())
    return acc(out["fly"]), acc(out["froz"]), acc(out["land"])


def cic(out, nd, pics):
    """Mass in flight per 10 mm cell at the pictures in `pics` (cloud in cell): array (len(pics), nx, ny, nz)."""
    import jax.numpy as jnp
    lo, h, n = GRID["lo"], GRID["h"], GRID["n"]; P = jnp.stack([out["x"], out["y"], out["z"]], -1)[..., 1:, :]
    J = nd["jidx"][:, 1:]; sel = np.isin(J, pics); pi = np.searchsorted(pics, np.where(sel, J, pics[0]))
    g = (P - lo) / h - 0.5; i0 = jnp.floor(g); fr = g - i0; i0 = i0.astype(int)
    wm = (out["w"][:, :, None] * out["fly"][..., 1:]) * jnp.asarray(sel)[:, None, :]
    F = jnp.zeros((len(pics),) + tuple(n)); PI = jnp.broadcast_to(jnp.asarray(pi)[:, None, :], wm.shape)
    for dx_ in (0, 1):
        for dy_ in (0, 1):
            for dz_ in (0, 1):
                ii = i0 + jnp.array([dx_, dy_, dz_]); wt = jnp.prod(jnp.where(jnp.array([dx_, dy_, dz_]) == 1, fr, 1 - fr), -1)
                inb = jnp.all((ii >= 0) & (ii < jnp.asarray(n)), -1); iic = jnp.clip(ii, 0, jnp.asarray(n) - 1)
                F = F.at[PI.ravel(), iic[..., 0].ravel(), iic[..., 1].ravel(), iic[..., 2].ravel()].add((wm * wt * inb).ravel())
    return F


def deck_field(out, nd, t0, W_=0.1, c=0.02):
    """Section 8 geometry (no old body): mass crossing z = -30 mm per 20 mm deck cell and 0.1 s window; and mass on / off the deck."""
    x, y, z, w = (np.asarray(out[k]) for k in ("x", "y", "z", "w")); tj = nd["tj"][:, None, :]; ok = nd["ok"][:, None, :]
    zp, zn = z[..., :-1], z[..., 1:]; cr = (zp > DECK[0]) & (zn <= DECK[0]) & ok[..., 1:]
    f = np.clip((zp - DECK[0]) / np.where(np.abs(zp - zn) > 1e-12, zp - zn, 1e-12), 0, 1)
    xc = x[..., :-1] + f * (x[..., 1:] - x[..., :-1]); yc = y[..., :-1] + f * (y[..., 1:] - y[..., :-1])
    tc = np.broadcast_to(tj[..., :-1] + f * (tj[..., 1:] - tj[..., :-1]), cr.shape); wm = np.broadcast_to(w[..., None], cr.shape)
    on = cr & (np.abs(xc) < DECK[1]) & (np.abs(yc) < DECK[2]); nx, ny = int(round(2 * DECK[1] / c)) + 1, int(round(2 * DECK[2] / c)) + 1
    nw = int(np.ceil((W["t"][-1] - t0) / W_)) + 1; Fd = np.zeros((nw, nx, ny))
    np.add.at(Fd, (np.clip(((tc[on] - t0) / W_).astype(int), 0, nw - 1), ((xc[on] + DECK[1]) / c).astype(int), ((yc[on] + DECK[2]) / c).astype(int)), wm[on])
    return Fd, float(wm[on].sum()), float(wm[cr & ~on].sum())


# ------------------------------------------------------------------ the twin
TC, SIG, MTOT = 0.85, 0.06, 0.0756                                       # the hand source: a pulse of 75.6 g centred at 0.85 s


def hand_coeffs(nk, tk):
    """Truth at the knots. Share: cylinder 2.0 cos(theta) + 0.5 zeta; top -0.5 + 1.0 cos(theta) (about a quarter through the top).
    Velocities (m/s): cylinder u_r 0.42 + 0.15 cos, u_theta 0.05 sin, u_z 0.25 + 0.05 zeta; top u_r 0.20 + 0.10 cos, u_z 0.60;
    all velocities scaled by 1 + 0.3 (t0 - 0.85 s) / 0.1 s."""
    C = np.zeros((nk, NPK)); sc = 1 + 0.3 * (tk - TC) / 0.1
    C[:, 1] = 2.0; C[:, 5] = 0.5; C[:, 10] = -0.5; C[:, 11] = 1.0                         # share: cyl cos1, cyl xi*cos0, top cos0, top cos1
    C[:, 20 + 0] = 0.42 * sc; C[:, 20 + 1] = 0.15 * sc; C[:, 20 + 10] = 0.20 * sc; C[:, 20 + 11] = 0.10 * sc     # u_r
    C[:, 40 + 0] = 0.05 * sc                                                               # u_theta: cylinder sin(theta)
    C[:, 56 + 0] = 0.25 * sc; C[:, 56 + 5] = 0.05 * sc; C[:, 56 + 10] = 0.60 * sc          # u_z
    return C


def first_guess(nk):
    C = np.zeros((nk, NPK)); C[:, 20] = C[:, 30] = 0.30; C[:, 56] = C[:, 66] = 0.10; return C


def twin():
    import jax, jax.numpy as jnp
    from scipy.optimize import minimize
    jax.config.update("jax_enable_x64", True)
    t, nf = W["t"], W["nf"]; k0 = int(np.searchsorted(t, TC - 3.8 * SIG)); k1 = int(np.searchsorted(t, TC + 4.2 * SIG))
    if SMOKE: k0, k1 = int(np.searchsorted(t, TC - 0.05)), int(np.searchsorted(t, TC + 0.05))
    tk = t[k0:k1 + 1]; nk = len(tk)
    fine = dict(nth=12, nxi=2, lpp=2) if SMOKE else dict(nth=48, nxi=3, lpp=4)
    crs = dict(nth=8, nxi=2, lpp=1) if SMOKE else dict(nth=24, nxi=2, lpp=2)
    def prep(p):
        nd = nodes(p["nth"], p["nxi"], p["lpp"], k0, k1); nd["Kt"] = knot_matrix(nd, k0, k1); propagators(nd)
        ta = W["tf"][nd["a"]]; Q = np.exp(-0.5 * ((ta - TC) / SIG) ** 2); Q *= MTOT / (Q.sum() * nd["dt0"]); return nd, Q
    ndT, QT = prep(fine); ndF, QF = prep(crs)
    say(f"\n## Twin: truth {len(ndT['a'])} launch times x {ndT['pos'].shape[0]} nodes, fit {len(ndF['a'])} x {ndF['pos'].shape[0]}; "
        f"{nk} knots x {NPK} = {nk * NPK} unknowns; launch window t = {tk[0]:.3f} to {tk[-1]:.3f} s\n")
    CT = hand_coeffs(nk, tk); fT = build_forward(ndT, QT, EPS_TRUE); oT = fT(jnp.asarray(CT))
    nfT, nsT, nlT = (np.asarray(q) for q in counters(oT, ndT, nf))
    pics = np.arange(k0 + 1, min(nf, k1 + K + 1)); pics = pics[pics % 2 == 0]
    MT = np.asarray(cic(oT, ndT, pics)); listed = (nfT + nsT) / MP_
    lam = np.minimum(1.0, LIST_CAP / np.maximum(listed, 1.0))[pics]
    rng = np.random.default_rng(5); n_obs = rng.poisson(lam[:, None, None, None] * MT / MP_)
    left = float(np.asarray((oT["w"][:, :, None] * oT["fly"])[..., -1]).sum() * 1e3)
    say(f"Truth: {MTOT * 1e3:.2f} g launched; frozen at the end {nsT[-1] * 1e3:.2f} g, landed {nlT[-1] * 1e3:.2f} g, still in flight after "
        f"{K} pictures {left:.3f} g. Fake pictures: {len(pics)} even pictures, {int(n_obs.sum()):,} listed markers, thinning lambda "
        f"{lam.min():.3f} to {lam.max():.3f}.")
    s_cnt = 0.01 * nfT.max() / MP_
    fF = build_forward(ndF, QF, EPS_FIT); nobs = jnp.asarray(n_obs, float); lamj = jnp.asarray(lam); nfly_obs = jnp.asarray(nfT / MP_)
    C0 = first_guess(nk); vel = np.zeros(NPK, bool); vel[20:] = True; C0v = jnp.asarray(C0[:, vel])
    def terms(Cflat):
        C = Cflat.reshape(nk, NPK); o = fF(C); M = cic(o, ndF, pics); mu = lamj[:, None, None, None] * M / MP_ + 1e-9
        nll = jnp.sum(mu - nobs * jnp.log(mu)); nfh = counters(o, ndF, nf)[0] / MP_
        cnt = jnp.sum((nfh - nfly_obs) ** 2) / (2 * s_cnt ** 2)
        return nll, cnt, C, mu
    def J(Cflat, MU):
        nll, cnt, C, _ = terms(Cflat)
        return nll + cnt + MU * jnp.sum(jnp.diff(C, axis=0) ** 2) + 0.01 * MU * jnp.sum((C[:, vel] - C0v) ** 2)
    vg = jax.jit(jax.value_and_grad(J))
    def deviance(Cflat):
        _, _, _, mu = terms(jnp.asarray(Cflat)); mu = np.asarray(mu); n = np.asarray(n_obs, float); use = (n > 0) | (mu > 1e-3)
        d = 2 * (np.where(n > 0, n * np.log(np.maximum(n, 1) / mu), 0.0) - (n - mu)); return float(d[use].sum() / max(use.sum(), 1)), int(use.sum())
    fits = []; x0 = C0.ravel()
    for MU in MU_LADDER:
        t_ = time.time()
        r = minimize(lambda v: tuple(np.asarray(q, float) for q in vg(jnp.asarray(v), MU)), x0, jac=True, method="L-BFGS-B", options=dict(maxiter=MAXIT))
        dpd, nd_ = deviance(r.x); fits.append(dict(MU=MU, x=r.x, dev=dpd, it=int(r.nit), J=float(r.fun), msg=str(r.message), s=time.time() - t_)); x0 = r.x
        say(f"- fit MU = {MU:g}: {r.nit} iterations, {time.time() - t_:.0f} s, J = {r.fun:.4g}, deviance per datum {dpd:.3f} over {nd_:,} cells ({r.message})")
    ok_ = [f for f in fits if f["dev"] <= 1.0]; best = max(ok_, key=lambda f: f["MU"]) if ok_ else min(fits, key=lambda f: f["MU"])
    say(f"Chosen by the discrepancy principle: MU = {best['MU']:g} (deviance per datum {best['dev']:.3f}{'' if ok_ else '; none reached 1, the smallest MU taken'}).")
    oR = fF(jnp.asarray(best["x"].reshape(nk, NPK))); o0 = fF(jnp.asarray(C0))
    FT, onT, offT = deck_field(oT, ndT, t[0]); FR, onR, offR = deck_field(oR, ndF, t[0]); F0, on0, off0 = deck_field(o0, ndF, t[0])
    FTc, _, _ = deck_field(fF(jnp.asarray(CT)), ndF, t[0])                # the truth's own coefficients on the fit's coarse nodes
    L1 = lambda A, B: float(np.abs(A - B).sum() / max(B.sum(), 1e-30)); l1R, l10, l1q = L1(FR, FT), L1(F0, FT), L1(FTc, FT)
    REP["quadrature_floor_L1"] = l1q
    say(f"Quadrature floor (the truth's coefficients on the coarse nodes against the fine truth): L1 {100 * l1q:.2f} %. "
        "A recovered L1 near this floor is all the coarse quadrature allows.")
    _, nsR, nlR = (np.asarray(q) for q in counters(oR, ndF, nf))
    dS = float(np.abs(nsR - nsT).max() * 1e3); dL = float(np.abs(nlR - nlT).max() * 1e3)
    REP["twin"] = dict(knots=nk, unknowns=nk * NPK, pics=len(pics), listed=int(n_obs.sum()), fits=[{k: v for k, v in f.items() if k != "x"} for f in fits],
                       MU=best["MU"], L1_deck_recovered=l1R, L1_deck_first_guess=l10, deck_on_true_g=onT * 1e3, deck_on_rec_g=onR * 1e3,
                       deck_off_true_g=offT * 1e3, deck_off_rec_g=offR * 1e3, max_dev_stuck_g=dS, max_dev_landed_g=dL, PASS=l1R <= PASS_L1)
    say(f"\nDeck under section 8's geometry, mass per 20 mm cell and 0.1 s window: recovered against truth L1 **{100 * l1R:.2f} %** "
        f"(first guess {100 * l10:.1f} %; mark {100 * PASS_L1:.0f} %): **{'PASS' if l1R <= PASS_L1 else 'FAIL'}**")
    say(f"On the deck: truth {onT * 1e3:.2f} g, recovered {onR * 1e3:.2f} g; off it: truth {offT * 1e3:.2f} g, recovered {offR * 1e3:.2f} g. "
        f"Counter curves, largest deviation: frozen {dS:.3f} g, landed {dL:.3f} g.")
    np.savez_compressed(os.path.join(OUT, "twin.npz"), deck_true=FT, deck_rec=FR, deck_first=F0, stuck_true=nsT, stuck_rec=nsR, landed_true=nlT,
                        landed_rec=nlR, C_true=CT, C_rec=best["x"].reshape(nk, NPK), t=t)


def mp():
    global MP_
    MP_ = 0.429e-6 * 1.0                                               # kg per marker (handoff 2.3: mp = 0.429 mg); used only to count markers
    REP["mp_kg"] = MP_


MP_ = None
for name, fn in (("frame", frame), ("marker_mass", mp), ("twin", twin)):
    block(name, fn)
say(f"\nWall time {time.time() - T0:.0f} s on Kaggle CPU."); flush()
sys.exit(1 if ERR else 0)

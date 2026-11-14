"""Fig. 15 correction, walls on the GPU: the exact rebuild of the wall runs listed in walls_all.json (all 1,088 walls),
written as RT3C files in the stored layout at the stored frame times, exactly as rebuild_walls_all.py does on the CPU.

Batching. Walls are grouped by geometry (Nx, N, D, P, sx, biased or not): inside a group the segment faces, the projection
points, the fine structure grid and the output points are the same; only E, V0, the bias and sigma_perp differ. The arrays
of exact_wall_jax.ExactJ are built by one pure function (core) of the per-wall inputs (k, weights, segment potentials, bias,
closed-form projections, start packet on the projection points, frame times); k is padded to the group's largest length with
zero weights (the sums are unchanged), and jax.vmap runs B walls in one call. Biased and unbiased walls never share a batch.
The flux integrals (time grid fixed by each wall's own t_end) run per wall with ExactJ's own _flux_cum.
Check on the GPU: the first wall of every group is also computed by the verified single-wall path (ExactJ); if T_ref differs
by more than 1e-9 or any amplitude level differs by more than 1 (a rounding flip), the whole group falls back to the single-wall path (logged).

One thread per GPU; one progress line per batch in progress.log; runs.jsonl; walls.tar at the end.
Globals a loader may set: OUTROOT, CPU (test without a GPU), JOBS, START, STOP, BATCH_MAX, MEM_BUDGET, CALIB.\nTracking: every progress line carries done/total, elapsed, rate and ETA; timing.json holds per group the compile time and the steady\nseconds per wall; with CALIB = True only two batches per group run and timing.json predicts the time for all walls."""
import os, sys, json, time, hashlib, threading, queue, tarfile, traceback
from types import SimpleNamespace
from math import erfc, sqrt, pi
import numpy as np
T0 = time.time()
ROOT = globals().get("OUTROOT", "/kaggle/working"); os.makedirs(ROOT, exist_ok=True)
LOG = open(ROOT + "/progress.log", "a")
import urllib.request as _ur, threading as _th
NTFY = globals().get("NTFY"); _LAST = [0.0]          # live tracker (owner-approved, this use only): progress lines to ntfy.sh/<NTFY>
_KEY = ("group", "check", "PREDICTION", "done", "FAILED", "failed", "NO GPU", "devices", "MISMATCH", "tar", "smoke", " A ", " B ", " C ", " T ")
def push(s, force=False):
    if not NTFY or (not force and time.time() - _LAST[0] < 30): return
    _LAST[0] = time.time()
    def f():
        try: _ur.urlopen(_ur.Request("https://ntfy.sh/" + NTFY, data=s.encode()[:3500]), timeout=10)
        except Exception: pass
    _th.Thread(target=f, daemon=True).start()
def say(*a):
    s = f"[{time.time()-T0:7.1f} s] " + " ".join(str(x) for x in a); print(s, flush=True); LOG.write(s + "\n"); LOG.flush()
    push(s, any(k in s for k in _KEY))
sys.path.insert(0, ".")
import jax
print(jax.devices())
if not globals().get("CPU") and jax.default_backend() != "gpu":
    say("NO GPU BACKEND"); raise SystemExit("NO GPU BACKEND")
import exact_wall as ew, exact_wall_jax as ej, rebuild_wall as rw
import jax.numpy as jnp
c128 = ej.c128


def layout(Nx):
    x = (np.arange(Nx) - Nx // 2) * 0.5; inner = (Nx // 2 - max(4, Nx // 10)) * 0.5
    return x, int(np.searchsorted(x, -inner)), int(np.searchsorted(x, inner))


def header(j):
    sp = j["spec"]; x, i0, i1 = layout(sp["Nx"])
    return dict(spec=sp, group=j["group"], shape=sp["shape"], E=sp["E"], V0=sp["V0"], D=sp["D"], P=sp["P"], N=sp["N"], size=sp["R"],
                bias=sp["bias"], sigma_x=sp["sx"], sigma_perp=sp["sp"], x0=ew.x0_of(sp), centres=ew.centres(sp),
                extent=[ew.centres(sp)[0] - sp["D"] / 2, ew.centres(sp)[-1] + sp["D"] / 2], n=j["n"], nxs=i1 - i0, nr=64,
                x_first=float(x[i0]), step=0.5, prof_x_first=float(x[0]), prof_nx=sp["Nx"], steps=j["steps"], dt=0.01, t_end=j["t_end"],
                frame_dt=j["frame_dt"], start_in_barrier=j["start_in_barrier"], start_in_border=None, box=[sp["Nx"], 128, 128])


def xs_of(h): return h["prof_x_first"] + np.arange(h["prof_nx"]) * 0.5
def times_of(h): return np.arange(h["n"]) * h["frame_dt"]


def assemble(j, chi, R, lo, hi, T_inf, T_w, carried, dev, secs):
    """Write one RT3C file from chi on the output points (Nx, n) and the region curves: the same lines as the CPU rebuild."""
    h = header(j); sp = h["spec"]; t = times_of(h); xs = xs_of(h)
    i0 = int(round((h["x_first"] - xs[0]) / 0.5)); nxs = h["nxs"]
    Hy = ew.h_free(np.arange(64) * 0.5, t, sp["sp"]).T
    slab = chi[:, i0:i0 + nxs, None] * Hy[:, None, :] * Hy[:, 0, None, None]
    prof = np.abs(chi)**2
    curves = [t, 1 - lo - hi, R["left"] - lo, R["right"] - hi] + ([R["well"]] if sp["N"] > 1 else [])
    names = ["t", "norm", "left", "right"] + (["well"] if sp["N"] > 1 else [])
    head = dict(method="exact: psi = chi(x,t) h(y,t) h(z,t); chi by superposition of the stationary scattering states "
                "(tools/kaggle/resonant-tunnelling/correction/exact_wall.py, exact_wall_jax.py and wall_gpu_run.py on the GPU); "
                "no time grid, no barrier sampling",
                parent=dict(file=j["file"], sha256=j["sha256"]), T_ref=T_inf, T_spectrum_weighted=T_w,
                carried=carried, closure_max=float(np.abs(R["closure"] - 1).max()),
                regions="left, right, norm: inside the box |x| <= box half-length; left_line, right_line: whole line",
                extra_curves=dict(left_line=np.round(R["left"], 7).tolist(), right_line=np.round(R["right"], 7).tolist()),
                device=str(dev) + " (exact)", wall=None, has_1d=True, sep_check_max=0.0, T_1d_splitstep=None, R_1d_splitstep=None,
                T_packet_exact=T_w)
    blob, A, P, peaks = rw.write(h, slab, prof, prof, np.array(curves).T, names, head)
    rec = dict(file=j["file"], spec=sp, T_ref=T_inf, T_w=T_w, carried=carried, closure_max=head["closure_max"],
               sha256_rebuilt=hashlib.sha256(blob).hexdigest(), bytes=len(blob), s=round(secs, 3), device=str(dev))
    return blob, rec, A


def one(j, dev):
    """The verified single-wall path (exact_wall_jax.ExactJ)."""
    t0 = time.time(); h = header(j); sp = h["spec"]; t = times_of(h)
    X = ej.ExactJ(sp, xs_of(h))
    chi = np.asarray(X.chi(t)).T
    half = 0.5 * h["prof_nx"] * 0.5
    R, lo, hi = X.regions_and_tails(t, -half, half)
    return assemble(j, chi, R, lo, hi, X.T_inf, X.T_packet_weights, X.carried, dev, time.time() - t0)


# ---------------------------------------------------------------- batched path
def gkey(sp): return (sp["Nx"], sp["N"], sp["D"], sp["P"], sp["sx"], bool(sp["bias"]))


class Group:
    """Geometry shared by every wall of one group, and the jitted, vmapped core."""

    def __init__(self, jobs, dk=5e-4, nslice=2000, hfine=0.01):
        self.jobs = jobs; sp0 = jobs[0]["spec"]; h0 = header(jobs[0])
        segs, xl, xr = ew.segments(sp0, nslice); self.xl, self.xr = xl, xr
        self.sa = np.array([s[0] for s in segs]); self.sb = np.array([s[1] for s in segs])
        for j in jobs:                                       # the shared geometry is asserted, not assumed
            sg, a, b = ew.segments(j["spec"], nslice)
            assert len(sg) == len(segs) and a == xl and b == xr and np.array_equal(np.array([s[0] for s in sg]), self.sa) \
                and np.array_equal(np.array([s[1] for s in sg]), self.sb), "geometry differs inside the group"
            assert ew.x0_of(j["spec"]) == ew.x0_of(sp0) and j["spec"]["Nx"] == sp0["Nx"] and j["n"] == jobs[0]["n"]
        NB = 1024; self.K = max(-(-len(ew.kgrid(j["spec"], dk)[0]) // NB) * NB for j in jobs); self.dk = dk; self.nslice = nslice
        cs = ew.centres(sp0); D = sp0["D"]
        fa = sorted({round(f, 12) for c in cs for f in (c - D / 2, c + D / 2)})
        fine, fw, fwell = [], [], []
        for a, b in zip(fa[:-1], fa[1:]):
            n = int(np.ceil((b - a) / hfine)); n += (n % 2 == 1); n += 1
            xx = np.linspace(a, b, n); fine.append(xx); fw.append(ew.simpson_w(n, (b - a) / (n - 1)))
            m = 0.5 * (a + b); fwell.append(np.full(n, not any(abs(m - c) < D / 2 for c in cs)))
        self.xf = np.concatenate(fine); wf = np.concatenate(fw); well = np.concatenate(fwell)
        s = sp0["sx"]; xt_hi = max(xr + 1.0, ew.x0_of(sp0) + 8.6 * s)
        ht = 0.02; nt = int(np.ceil((xt_hi - xl) / ht)); nt = -(-nt // 512) * 512 + 1; xt_hi = xl + ht * (nt - 1)
        self.xt = np.linspace(xl, xt_hi, nt); self.wt = ew.simpson_w(nt, (xt_hi - xl) / (nt - 1))
        self.xo = xs_of(h0); self.half = 0.5 * h0["prof_nx"] * 0.5
        self.PL0 = 1 - 0.5 * erfc((xl - ew.x0_of(sp0)) / (sqrt(2) * s))
        sa, sb = self.sa, self.sb
        def pts(x):
            x = np.asarray(x, float); nL = int((x < xl).sum()); nR = int((x > xr).sum()); xi = x[nL:len(x) - nR]
            si = np.clip(np.searchsorted(sa, xi, side="right") - 1, 0, len(sa) - 1)
            return x[:nL], xi, si, xi - sa[si], x[len(x) - nR:]
        Pt, Pf, Po = pts(self.xt), pts(self.xf), pts(self.xo)
        xt_j, wf_j, wfw_j = jnp.asarray(self.xt), jnp.asarray(wf), jnp.asarray(wf * well)
        def lead(x0, k, kR, aP, aM, r, t, tp, rp):
            if x0 < xl:
                e = jnp.exp(1j * k * x0)
                return aP * (e + r / e) + aM * (tp / e), aP * 1j * k * (e - r / e) - aM * 1j * k * tp / e
            e = jnp.exp(1j * kR * x0)
            return aP * t * e + aM * (1 / e + rp * e), aP * 1j * kR * t * e + aM * 1j * kR * (-1 / e + rp * e)

        def core(k, w, bias, V, Gk, Gmk, c0, times):
            E = 0.5 * k * k; kR = jnp.sqrt(k * k + 2 * bias)
            def step(c, seg):
                a, b, v = seg; q = jnp.sqrt(2 * (E - v) + 0j); cc, ss, mm = ej._prop(q, b - a)
                p1, d1, p2, d2 = c
                return (cc * p1 + ss * d1, mm * p1 + cc * d1, cc * p2 + ss * d2, mm * p2 + cc * d2), c
            one_ = jnp.ones_like(k, dtype=c128); zero = jnp.zeros_like(k, dtype=c128)
            (P1, D1, P2, D2), F = jax.lax.scan(step, (one_, zero, zero, one_), (jnp.asarray(sa), jnp.asarray(sb), V))
            ea, eb = jnp.exp(1j * k * xl), jnp.exp(-1j * k * xl)
            A = (ea, 1j * k * ea); B = (eb, -1j * k * eb)
            def split(v):
                ps = v[0] * P1 + v[1] * P2; dp = v[0] * D1 + v[1] * D2
                return 0.5 * (ps + dp / (1j * kR)) * jnp.exp(-1j * kR * xr), 0.5 * (ps - dp / (1j * kR)) * jnp.exp(1j * kR * xr)
            aR, bR = split(A); aRb, bRb = split(B)
            r = -bR / bRb; t = aR + r * aRb; tp = 1 / bRb; rp = aRb / bRb
            alP = (A[0] + r * B[0], A[1] + r * B[1]); alM = (tp * B[0], tp * B[1])
            def values(p):
                xL, xi, si, dx, xR = p; pp, pm = [], []
                if len(xL):
                    eL = jnp.exp(1j * jnp.asarray(xL)[:, None] * k); pp.append(eL + r / eL); pm.append(tp / eL)
                if len(xi):
                    idx = jnp.asarray(si); q = jnp.sqrt(2 * (E[None, :] - V[idx][:, None]) + 0j)
                    c, s_, _ = ej._prop(q, jnp.asarray(dx)[:, None])
                    U1 = c * F[0][idx] + s_ * F[1][idx]; U2 = c * F[2][idx] + s_ * F[3][idx]
                    pp.append(alP[0] * U1 + alP[1] * U2); pm.append(alM[0] * U1 + alM[1] * U2)
                if len(xR):
                    eR = jnp.exp(1j * jnp.asarray(xR)[:, None] * kR); pp.append(t * eR); pm.append(1 / eR + rp * eR)
                return jnp.concatenate(pp, 0), jnp.concatenate(pm, 0)
            Pp, Pm = values(Pt)
            e = jnp.exp(1j * jnp.outer(xt_j, k)); Lp = e + r / e; Lm = tp / e
            cP = Gk + jnp.conj(r) * Gmk + ((jnp.conj(Pp) - jnp.conj(Lp)) * c0[:, None]).sum(0)
            cM = jnp.conj(tp) * Gmk + ((jnp.conj(Pm) - jnp.conj(Lm)) * c0[:, None]).sum(0)
            aP = w / (2 * pi) * cP; aM = w / (2 * pi) * (k / kR) * cM
            carried = (w / (2 * pi) * (jnp.abs(cP)**2 + (k / kR) * jnp.abs(cM)**2)).sum()
            out = cP * t + (k / kR) * cM * rp
            T_inf = (w / (2 * pi) * jnp.abs(out)**2 * (kR / k)).sum()
            g2 = w * jnp.abs(Gk)**2; T_w = (g2 * (kR / k) * jnp.abs(t)**2).sum() / g2.sum()
            ph = jnp.exp(-1j * jnp.outer(E, times))
            def basis(p):
                a, b = values(p); return a * aP + b * aM
            chi_o = basis(Po) @ ph
            rho = jnp.abs(basis(Pf) @ ph)**2
            Pst = (wf_j[:, None] * rho).sum(0); Pw = (wfw_j[:, None] * rho).sum(0)
            el, er = jnp.exp(1j * k * xl), jnp.exp(1j * kR * xr)
            fl = (aP * (el + r / el) + aM * (tp / el), aP * 1j * k * (el - r / el) - aM * 1j * k * tp / el)
            fr = (aP * t * er + aM * (1 / er + rp * er), aP * 1j * kR * t * er + aM * 1j * kR * (-1 / er + rp * er))
            lo = lead(-self.half, k, kR, aP, aM, r, t, tp, rp); hi = lead(self.half, k, kR, aP, aM, r, t, tp, rp)
            return dict(T_inf=T_inf, T_w=T_w, carried=carried, chi=chi_o, Pst=Pst, Pw=Pw, E=E,
                        fl0=fl[0], fl1=fl[1], fr0=fr[0], fr1=fr[1], lo0=lo[0], lo1=lo[1], hi0=hi[0], hi1=hi[1])
        self.fn = jax.jit(jax.vmap(core))
        S = len(sa); nt_, nf, no = len(self.xt), len(self.xf), len(self.xo)
        self.bytes_per_wall = 16 * self.K * (8 * nt_ + 4 * nf + 4 * no + 3 * 200 + 5 * S + 40)
        budget = float(globals().get("MEM_BUDGET", 6e9))
        self.B = int(max(1, min(int(globals().get("BATCH_MAX", 8)), budget // self.bytes_per_wall)))

    def inputs(self, j):
        sp = j["spec"]; k, w = ew.kgrid(sp, self.dk); npad = self.K - len(k)
        if npad: k = np.r_[k, k[-1] + self.dk * np.arange(1, npad + 1)]; w = np.r_[w, np.zeros(npad)]
        V = np.array([s[2] for s in ew.segments(sp, self.nslice)[0]])
        return (k, w, float(sp.get("bias", 0.0) or 0.0), V, ew.G(sp, k), ew.G(sp, -k), ew.chi0(sp, self.xt) * self.wt,
                times_of(header(j)))

    def run(self, batch, dev):
        """batch: list of jobs (len <= B; padded to B by repeating the last, results dropped). Returns [(blob, rec, A)]."""
        t0 = time.time(); jobs = batch + [batch[-1]] * (self.B - len(batch))
        ins = [self.inputs(j) for j in jobs]
        args = [jax.device_put(np.stack([np.asarray(x[i]) for x in ins]), dev) for i in range(8)]
        O = self.fn(*args); O = {kk: v for kk, v in O.items()}
        out = []; tb = time.time() - t0
        for b, j in enumerate(batch):
            t1 = time.time(); t = times_of(header(j)); sp = j["spec"]
            ns = SimpleNamespace(E=O["E"][b])
            pairs = [(O["fl0"][b], O["fl1"][b]), (O["fr0"][b], O["fr1"][b]), (O["lo0"][b], O["lo1"][b]), (O["hi0"][b], O["hi1"][b])]
            cl, cr, clo, chi_ = ej.ExactJ._flux_cum(ns, t, pairs, 0.02)
            PL, PR = self.PL0 - cl, cr; Pst = np.asarray(O["Pst"][b])
            s = sp["sx"]; x0 = ew.x0_of(sp)
            lo = 0.5 * erfc((x0 + self.half) / (sqrt(2) * s)) - clo; hi = 0.5 * erfc((self.half - x0) / (sqrt(2) * s)) + chi_
            R = dict(left=PL, right=PR, well=np.asarray(O["Pw"][b]), struct=Pst, closure=PL + PR + Pst)
            out.append(assemble(j, np.asarray(O["chi"][b]).T, R, lo, hi, float(O["T_inf"][b]), float(O["T_w"][b]),
                                float(O["carried"][b]), dev, tb / len(batch) + time.time() - t1))
        return out


if globals().get("RUN"):
    J = json.load(open(globals().get("JOBS", "walls_all.json")))
    J = J[globals().get("START", 0):globals().get("STOP", len(J))]
    OUTD = ROOT + "/walls"; os.makedirs(OUTD, exist_ok=True)
    groups = {}
    for j in J: groups.setdefault(gkey(j["spec"]), []).append(j)
    if globals().get("CALIB"):
        FULL = {}
        for j in json.load(open(globals().get("JOBS", "walls_all.json"))): FULL[gkey(j["spec"])] = FULL.get(gkey(j["spec"]), 0) + 1
    G = {}
    for key, jobs in groups.items():
        try:
            G[key] = Group(jobs)
            say("group", key, len(jobs), "walls, K", G[key].K, "batch", G[key].B, f"{G[key].bytes_per_wall/1e9:.2f} GB/wall")
        except Exception as e:
            G[key] = None; say("group", key, "single-wall path:", repr(e)[:200])
    if globals().get("CALIB"):                               # two batches per group: the first carries the compile
        groups = {k: v[:2 * (G[k].B if G[k] else 1)] for k, v in groups.items()}; J = [j for v in groups.values() for j in v]
    TIM = []                                                 # one record per batch: group, size, seconds, first
    Q = queue.Queue()
    for key, jobs in groups.items():
        B = G[key].B if G[key] else 1
        for a in range(0, len(jobs), B): Q.put((key, jobs[a:a + B], a == 0))
    LOCK = threading.Lock(); CNT = [0]; ERR = []; CHK = []; DONE = {key: threading.Event() for key in groups}
    JL = open(OUTD + "/runs.jsonl", "a")
    say("devices", jax.devices(), len(J), "walls in", len(groups), "groups")
    def emit(res, dev, how):
        for blob, rec, A in res:
            rec["path"] = how; open(f"{OUTD}/{rec['file']}", "wb").write(blob)
            with LOCK:
                CNT[0] += 1; JL.write(json.dumps(rec) + "\n"); JL.flush()
                el = time.time() - T0; eta = el / CNT[0] * (len(J) - CNT[0])
                say(f"{CNT[0]}/{len(J)} ({100*CNT[0]/len(J):.0f} %) elapsed {el/60:.1f} min, rate {CNT[0]/el*60:.1f} walls/min, "
                    f"ETA {eta/60:.1f} min | {rec['file']} {dev} {how}: T_ref {rec['T_ref']:.6f} closure {rec['closure_max']:.1e} {rec['s']} s/wall")
    def worker(dev):
        with jax.default_device(dev):
            while True:
                try: key, batch, first = Q.get_nowait()
                except queue.Empty: return
                if not first: DONE[key].wait()                     # no batched result before the group's check
                g = G[key]
                try:
                    if g is None: raise RuntimeError("single")
                    tb0 = time.time(); res = g.run(batch, dev)
                    with LOCK: TIM.append(dict(group=str(key), n=len(batch), B=g.B, s=round(time.time() - tb0, 2), first=first, dev=str(dev)))
                    if first:                                         # equivalence check against the verified path
                        b1, r1, A1 = one(batch[0], dev); _, r0, A0 = res[0]
                        dT = abs(r1["T_ref"] - r0["T_ref"]); dA = int(np.abs(np.asarray(A1, int) - np.asarray(A0, int)).max())
                        ok = dT <= 1e-9 and dA <= 1
                        with LOCK: CHK.append(dict(group=str(key), file=batch[0]["file"], dT=dT, dlevel=dA, ok=ok,
                                                   s_single=r1["s"], s_batched=r0["s"]))
                        say("check", key, batch[0]["file"], f"dT {dT:.1e} dlevel {dA}", "OK" if ok else "MISMATCH: group goes single")
                        if not ok: G[key] = None
                        DONE[key].set()
                        if not ok: raise RuntimeError("mismatch")
                    emit(res, dev, "batched")
                except Exception as e:
                    if first and not DONE[key].is_set(): G[key] = None; DONE[key].set()
                    if str(e) not in ("single", "mismatch"): say("batch failed, single path:", repr(e)[:300]); say(traceback.format_exc()[-600:])
                    for j in batch:
                        try:
                            tb0 = time.time(); emit([one(j, dev)], dev, "single")
                            with LOCK: TIM.append(dict(group=str(key), n=1, B=1, s=round(time.time() - tb0, 2), first=False, single=True, dev=str(dev)))
                        except Exception as e2:
                            with LOCK: ERR.append(dict(file=j["file"], error=repr(e2)[:400]))
                            say("FAILED", j["file"], repr(e2)[:300])
    devs = [d for d in jax.devices() if d.platform == "gpu"] or [jax.devices()[0]]
    th = [threading.Thread(target=worker, args=(d,)) for d in devs]; [x.start() for x in th]; [x.join() for x in th]
    JL.close()
    with tarfile.open(OUTD + "/walls.tar", "w") as tf:
        for f in sorted(os.listdir(OUTD)):
            if f.endswith(".bin"): tf.add(f"{OUTD}/{f}", arcname=f)
    for f in os.listdir(OUTD):
        if f.endswith(".bin"): os.remove(f"{OUTD}/{f}")
    json.dump(dict(done=CNT[0], failed=ERR, checks=CHK, total_s=round(time.time() - T0, 1)), open(OUTD + "/summary.json", "w"))
    # timing: per group, compile (first batch minus a steady batch of the same size) and steady seconds per wall
    ndev = len(devs); per = {}
    for t in TIM: per.setdefault(t["group"], []).append(t)
    tg = {}
    for k, L in per.items():
        st = [t for t in L if not t["first"] and not t.get("single")]; fi = [t for t in L if t["first"]]
        spw = (sum(t["s"] for t in st) / sum(t["n"] for t in st)) if st else (sum(t["s"] for t in L) / sum(t["n"] for t in L))
        comp = max(0.0, fi[0]["s"] - spw * fi[0]["n"]) if fi else 0.0
        tg[k] = dict(s_per_wall=round(spw, 3), compile_s=round(comp, 1), B=L[0]["B"], batches=len(L))
    T = dict(devices=[str(d) for d in devs], total_s=round(time.time() - T0, 1), groups=tg, batches=TIM)
    if globals().get("CALIB"):
        pred = {k: FULL[eval(k)] * v["s_per_wall"] for k, v in tg.items()}
        comp = sum(v["compile_s"] for v in tg.values())
        T["prediction"] = dict(walls=sum(FULL.values()), compute_s=round(sum(pred.values()), 1), compile_s_per_gpu=round(comp, 1),
                               wall_clock_s_one_notebook=round(sum(pred.values()) / ndev + comp + 60, 1),
                               wall_clock_s_two_notebooks=round(sum(pred.values()) / (2 * ndev) + comp + 60, 1),
                               note="GPU quota is charged per session wall-clock, not per GPU; two notebooks halve the wall clock")
        say("PREDICTION", json.dumps(T["prediction"]))
    json.dump(T, open(OUTD + "/timing.json", "w"), indent=1)
    say(f"done {CNT[0]}, failed {len(ERR)}, tar {os.path.getsize(OUTD + '/walls.tar')/1e6:.0f} MB")

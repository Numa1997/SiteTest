"""Fig. 15, 3D generation 2 (rt3d2): file the Kaggle runs and write the index the page reads.

Usage: python3 file_rt3d2.py <src> <generation date> <runs destination>
  <src>/<kernel slug>/ holds one notebook's output (rt3d2_*.tar and index.json), e.g. <src>/fig15-rt3d2-shard-1-of-6/.
  The run files are copied byte for byte (SHA-256 checked against the notebook's own index) to <runs destination>/<file>, the
  folder that is uploaded to Cloudflare R2; the index goes to public/data/resonant-tunnelling/<date>/kaggle/index.json.

Per run, the index carries its spec, file, SHA-256, notebook, version, commit, and numbers read once from the stored curves:
  T_far   (P_right + P_well / 2) / P_box at the last frame before any of the wave reaches the absorbing border at the ends of the
          flight (|x| > the box's inner half-length holding < 1e-3 of it); dividing by P_box removes what the side border took.
  tau     lifetime of the trapped wave: a straight-line fit of ln P_in(t) where P_in has fallen from 60 % to 5 % of its peak
          (P_in: between the first and last barrier for walls and discs; inside the outer shell for shells).
A spec computed in two groups (the diode's bias-0 points are also pairs of group A) is filed once, with both groups in `groups`
and the other copy's notebook and SHA-256 in `also_computed`; only a fix notebook's rerun replaces a file (`replaced`).
And for the diode (group F, selected by spec so that bias-0 points filed under A count), the current from the runs:
  J(V) = Int T(E, V) N(E, V) dE over the 25 stored energies 0.10 ... 1.30 (trapezoid), with the Tsu-Esaki supply function
  N = ln[(1 + e^{(E_F - E)/kT}) / (1 + e^{(E_F - E - V)/kT})], E_F = 1.0, kT = 0.05, the same as exact1d.py. T is the share of a
  packet (sigma_x = 3) that got through, not the single-energy T(E, V), so the curve is the exact one smoothed by the packet's
  energy spread. Walls: T is the run's 1D twin, which counts what the border absorbed (the 3D walls equal it by separation; T_far
  reads low under bias, because the faster transmitted wave reaches the border while some is still trapped). Discs: T_far, so their
  curve reads somewhat low. For walls the same integral with the exact single-energy T at the same energies is stored beside it.
"""
import json, sys, os, tarfile, hashlib
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import read_rt3d, tm, iv

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
COMMITS = {"shard-1-of-6": "cdcade45884c3894ef02581d6f70f7f4c80d895f", "shard-2-of-6": "cdcade45884c3894ef02581d6f70f7f4c80d895f",
           "smoke": "cdcade45884c3894ef02581d6f70f7f4c80d895f"}          # every later notebook: 57770d2 (corrected run length)
COMMIT_LATER = "57770d20f1651e76406bd2e6a2b871913ef31ea5"
def commit_of(slug): return next((c for k, c in COMMITS.items() if slug.endswith(k)), COMMIT_LATER)
EF, KT = 1.0, 0.05


def fit_tau(t, P):
    i = int(np.argmax(P)); pk = P[i]
    if pk < 1e-4: return None
    m = np.zeros(len(P), bool); m[i:] = True; m &= (P <= 0.6 * pk) & (P >= 0.05 * pk)
    j = np.where(m)[0]
    if len(j) < 6: return None
    j = j[: np.argmax(np.diff(np.r_[j, 10**9]) > 1) + 1]
    if len(j) < 6: return None
    sl, _ = np.polyfit(t[j], np.log(P[j]), 1)
    return None if sl >= 0 else dict(tau=round(float(-1 / sl), 3), t0=round(float(t[j[0]]), 3), t1=round(float(t[j[-1]]), 3), n=int(len(j)))


def summary(h, prof):
    c = np.array(h["curves"]); C = {n: c[:, i] for i, n in enumerate(h["curve_names"])}; t = C["t"]
    x = h["prof_x_first"] + np.arange(h["prof_nx"]) * h["step"]; inner = (h["prof_nx"] // 2 - max(4, h["prof_nx"] // 10)) * h["step"]
    Bx = prof[:, np.abs(x) > inner].sum(1) * h["step"]
    ok = Bx < 1e-3 * C["norm"]; f = int(np.argmin(ok)) - 1 if not ok.all() else len(ok) - 1
    shell = h["shape"] == "shell"
    if shell: Pin = C["core"] + C.get("gap", 0 * t)
    else: Pin = C.get("well", 0 * t)
    out = dict(frame_dt=h["frame_dt"], t_end=float(t[-1]), peak0=h["peak0"], start_in_barrier=h["start_in_barrier"],
               end={k: round(float(v[-1]), 6) for k, v in C.items() if k != "t"}, steps=h["steps"], wall=h["wall"], device=h["device"],
               P_in_max=round(float(Pin.max()), 6))
    if not shell:
        out["T_far"] = dict(value=round(float((C["right"][f] + 0.5 * (C["well"][f] if "well" in C else 0)) / C["norm"][f]), 5),
                            frame=f, t=round(float(t[f]), 3))
    ft = fit_tau(t, Pin) if Pin.max() > 0 else None
    if ft: out["tau"] = ft
    if h.get("has_1d"):
        out["twin"] = dict(T=round(h["T_1d_splitstep"], 6), R=round(h["R_1d_splitstep"], 6), sep_check_max=h["sep_check_max"],
                           T_exact=(round(h["T_packet_exact"], 6) if h.get("T_packet_exact") is not None else None))
    return out


def supply(E, V):
    return np.log1p(np.exp(np.clip((EF - E) / KT, -60, 60))) - np.log1p(np.exp(np.clip((EF - E - V) / KT, -60, 60)))


def main(src, date, dest):
    os.makedirs(dest, exist_ok=True)
    runs, nbs, replaced = [], [], []
    # a fix notebook (slug with "fix") reruns runs of an earlier notebook under the same file name: its version replaces the other
    slugs = sorted(os.listdir(src), key=lambda s: ("fix" in s, s))
    for slug in slugs:
        d = os.path.join(src, slug)
        if not os.path.isdir(d) or not os.path.exists(os.path.join(d, "index.json")): continue
        idx = json.load(open(os.path.join(d, "index.json"))); sha, grp = {}, {}
        for r in idx["runs"]:   # one spec can sit in two groups (e.g. A and F at bias 0): two entries, one file (the later one written)
            sha.setdefault(r["file"], set()).add(r["sha256"]); grp.setdefault(r["file"], set()).add(r["group"])
        tars = [f for f in os.listdir(d) if f.endswith(".tar")]
        COMMIT = commit_of(slug)
        nb = dict(kaggle="numakoudsie/" + slug, version=1, commit=COMMIT, solver="tools/kaggle/resonant-tunnelling/rt3d2.py",
                  runner="tools/kaggle/resonant-tunnelling/rt3d2_run.py", jobsel=idx.get("jobsel"), shard=idx.get("shard"),
                  device=idx.get("device"), devices=idx.get("devices"), sweep_s=idx.get("sweep_s"), failed=idx.get("failed"),
                  not_started=idx.get("not_started"), filed=0)
        for tname in tars:
            with tarfile.open(os.path.join(d, tname)) as tf:
                for m in tf.getmembers():
                    if not m.name.endswith(".bin"): continue
                    blob = tf.extractfile(m).read(); name = os.path.basename(m.name)
                    digest = hashlib.sha256(blob).hexdigest()
                    assert digest in sha[name], name
                    h, amp, ph, prof, p1 = read_rt3d.read(blob)
                    rec = dict(file=name, group=h["group"], groups=sorted(grp[name]), spec=h["spec"], bytes=len(blob), sha256=digest,
                               notebook=nb["kaggle"], version=1, commit=COMMIT, box=h["box"])
                    rec.update(summary(h, prof))
                    old = next((k for k, r in enumerate(runs) if r["file"] == name), None)
                    if old is not None and "fix" in slug:
                        # a rerun at the corrected run length replaces the earlier file
                        replaced.append(dict(file=name, old_notebook=runs[old]["notebook"], old_commit=runs[old]["commit"], old_sha256=runs[old]["sha256"],
                                             new_notebook=nb["kaggle"], new_sha256=digest,
                                             why="the run length of commit cdcade4 missed the packet's trailing edge and cut-off resonance peaks; this run was more than 15 % too short"))
                        rec["groups"] = sorted(set(rec["groups"]) | set(runs[old]["groups"])); runs[old] = rec
                    elif old is not None:
                        # the same spec computed in another group by another shard: one record, both groups, the other copy noted
                        o = runs[old]; o["groups"] = sorted(set(o["groups"]) | set(rec["groups"]))
                        o.setdefault("also_computed", []).append(dict(notebook=nb["kaggle"], commit=COMMIT, sha256=digest, group=h["group"]))
                        nb["filed"] += 1; continue
                    else: runs.append(rec)
                    open(os.path.join(dest, name), "wb").write(blob)
                    nb["filed"] += 1
        nbs.append(nb)
    key = lambda r: (r["group"], r["spec"]["shape"], r["spec"]["N"], r["spec"]["V0"], r["spec"]["D"], r["spec"]["P"], r["spec"]["R"], r["spec"]["bias"], r["spec"]["sx"], r["spec"]["E"])
    runs.sort(key=key)
    # the diode from the runs (group F)
    ivs = []
    for shape, R in (("flat", 0.0), ("coin", 6.0)):
        FE = set(np.round(np.arange(0.10, 1.301, 0.05), 3).tolist())   # the diode's energy grid
        F = [r for r in runs if r["spec"]["shape"] == shape and r["spec"]["R"] == R and r["spec"]["N"] == 2 and r["spec"]["V0"] == 2
             and r["spec"]["D"] == 1 and r["spec"]["P"] == 2.5 and r["spec"]["sx"] == 3 and round(r["spec"]["E"], 3) in FE and "T_far" in r]
        Vs = sorted({r["spec"]["bias"] for r in F}); J, Jx, Jp = [], [], []
        for V in Vs:
            pts = sorted((r["spec"]["E"], r["twin"]["T"] if r.get("twin") else r["T_far"]["value"]) for r in F if r["spec"]["bias"] == V)
            if len(pts) < 5: continue
            E = np.array([p[0] for p in pts]); T = np.array([p[1] for p in pts]); J.append([V, float(np.trapezoid(T * supply(E, V), E))])
            if shape == "flat":
                iv.V0, iv.D = 2.0, 1.0   # this diode's barriers (iv.py defaults to V0 = 3 for generation 1)
                Tx = iv.T_biased_vec(E, 2.5, V); Jx.append([V, float(np.trapezoid(Tx * supply(E, V), E))])
        ivs.append(dict(shape=shape, R=R, EF=EF, kT=KT, energies=sorted({r["spec"]["E"] for r in F}), J_runs=J,
                        J_exact_single_energy_same_points=(Jx or None)))
    # exact 1D curves for every wall structure without bias (and the limit the discs of the same structure approach)
    import rt3d2
    exact = {}
    for r in runs:
        sp = r["spec"]
        if sp["bias"]: continue
        k = f'{sp["N"]}|{sp["V0"]:g}|{sp["D"]:g}|{sp["P"]:g}|{sp["sx"]:g}'
        if k in exact: continue
        segs = rt3d2.segs_1d(dict(sp, shape="flat"))
        kk = np.linspace(np.sqrt(2 * 0.02), np.sqrt(2 * 3.2), 2400); T = np.array([abs(tm.solve(q * q / 2, segs)[0])**2 for q in kk])
        Eg = np.round(np.arange(0.25, 2.651, 0.01), 3); Tp = np.interp(np.sqrt(2 * Eg), kk, T); sk = 1 / (2 * sp["sx"]); Tb = []
        for e in Eg:
            w = np.exp(-(kk - np.sqrt(2 * e))**2 / (2 * sk**2)); Tb.append(float((w * T).sum() / w.sum()))
        exact[k] = dict(E=Eg.tolist(), T=np.round(Tp, 5).tolist(), Tbar=np.round(Tb, 5).tolist())
    out = dict(generated=date, kind="rt3d2", title="Fig. 15, 3D generation 2: the whole parameter space",
               dx=0.5, dt=0.01, nframes=200, method="Strang split-step Fourier, 3D, complex64; absorbing border sin^(1/8) in the outer tenth of each axis",
               units="hbar = m = 1, lengths in the grid unit a", runs_base=f"resonant-tunnelling/{date}/runs/", notebooks=nbs,
               numbers=__doc__.split("Per run, the index carries")[1].strip(), script="tools/kaggle/resonant-tunnelling/file_rt3d2.py",
               replaced=replaced, iv=ivs, exact=exact, exact_note="exact 1D transfer matrices (tm.py) for walls of the same N, V0, D, P: T is the single-energy transmission, Tbar its average over the packet's spread of wave numbers (sigma_k = 1/(2 sigma_x)); key N|V0|D|P|sigma_x", runs=runs)
    p = os.path.join(ROOT, "public", "data", "resonant-tunnelling", date, "kaggle", "index.json"); os.makedirs(os.path.dirname(p), exist_ok=True)
    json.dump(out, open(p, "w"), separators=(",", ":"), ensure_ascii=False)
    print(len(runs), "runs filed;", round(sum(r["bytes"] for r in runs) / 1e9, 3), "GB; index", round(os.path.getsize(p) / 1e6, 2), "MB")


if __name__ == "__main__":
    main(*sys.argv[1:4])

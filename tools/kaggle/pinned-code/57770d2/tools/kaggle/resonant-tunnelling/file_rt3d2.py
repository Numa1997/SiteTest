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
And for the diode (group F), the current from the runs:
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
COMMIT = "cdcade45884c3894ef02581d6f70f7f4c80d895f"
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
    runs, nbs = [], []
    for slug in sorted(os.listdir(src)):
        d = os.path.join(src, slug)
        if not os.path.isdir(d) or not os.path.exists(os.path.join(d, "index.json")): continue
        idx = json.load(open(os.path.join(d, "index.json"))); sha = {r["file"]: r["sha256"] for r in idx["runs"]}
        tars = [f for f in os.listdir(d) if f.endswith(".tar")]
        nb = dict(kaggle="numakoudsie/" + slug, version=1, commit=COMMIT, solver="tools/kaggle/resonant-tunnelling/rt3d2.py",
                  runner="tools/kaggle/resonant-tunnelling/rt3d2_run.py", jobsel=idx.get("jobsel"), shard=idx.get("shard"),
                  device=idx.get("device"), devices=idx.get("devices"), sweep_s=idx.get("sweep_s"), failed=idx.get("failed"),
                  not_started=idx.get("not_started"), filed=0)
        for tname in tars:
            with tarfile.open(os.path.join(d, tname)) as tf:
                for m in tf.getmembers():
                    if not m.name.endswith(".bin"): continue
                    blob = tf.extractfile(m).read(); name = os.path.basename(m.name)
                    assert hashlib.sha256(blob).hexdigest() == sha[name], name
                    h, amp, ph, prof, p1 = read_rt3d.read(blob)
                    open(os.path.join(dest, name), "wb").write(blob)
                    rec = dict(file=name, group=h["group"], spec=h["spec"], bytes=len(blob), sha256=sha[name], notebook=nb["kaggle"],
                               version=1, commit=COMMIT, box=h["box"])
                    rec.update(summary(h, prof)); runs.append(rec); nb["filed"] += 1
        nbs.append(nb)
    key = lambda r: (r["group"], r["spec"]["shape"], r["spec"]["N"], r["spec"]["V0"], r["spec"]["D"], r["spec"]["P"], r["spec"]["R"], r["spec"]["bias"], r["spec"]["sx"], r["spec"]["E"])
    runs.sort(key=key)
    # the diode from the runs (group F)
    ivs = []
    for shape, R in (("flat", 0.0), ("coin", 6.0)):
        F = [r for r in runs if r["group"] == "F" and r["spec"]["shape"] == shape and r["spec"]["R"] == R and "T_far" in r]
        Vs = sorted({r["spec"]["bias"] for r in F}); J, Jx, Jp = [], [], []
        for V in Vs:
            pts = sorted((r["spec"]["E"], r["twin"]["T"] if r.get("twin") else r["T_far"]["value"]) for r in F if r["spec"]["bias"] == V)
            if len(pts) < 5: continue
            E = np.array([p[0] for p in pts]); T = np.array([p[1] for p in pts]); J.append([V, float(np.trapezoid(T * supply(E, V), E))])
            if shape == "flat":
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
               iv=ivs, exact=exact, exact_note="exact 1D transfer matrices (tm.py) for walls of the same N, V0, D, P: T is the single-energy transmission, Tbar its average over the packet's spread of wave numbers (sigma_k = 1/(2 sigma_x)); key N|V0|D|P|sigma_x", runs=runs)
    p = os.path.join(ROOT, "public", "data", "resonant-tunnelling", date, "kaggle", "index.json"); os.makedirs(os.path.dirname(p), exist_ok=True)
    json.dump(out, open(p, "w"), separators=(",", ":"), ensure_ascii=False)
    print(len(runs), "runs filed;", round(sum(r["bytes"] for r in runs) / 1e9, 3), "GB; index", round(os.path.getsize(p) / 1e6, 2), "MB")


if __name__ == "__main__":
    main(*sys.argv[1:4])

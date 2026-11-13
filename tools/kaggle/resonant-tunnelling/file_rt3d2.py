"""Fig. 15, 3D generation 2 (rt3d2): file the Kaggle runs; generalised from file_rt3d.py (generation 1).
Usage: python3 file_rt3d2.py <folder of notebook outputs: one subfolder per notebook with its tar and index.json> <generation date> <runs destination>
The index goes to public/data/resonant-tunnelling/<date>/kaggle/index.json; the run files to <runs destination> (Cloudflare R2 staging).

Generation 1 docstring follows.
Fig. 15, 3D: file the Kaggle runs on the site, with their provenance and the numbers the page reads.

Input: the output folders of the five Kaggle notebooks (each holds rt3d.tar and index.json, as rt3d_run.py wrote them):
  s1 .. s4  numakoudsie/fig15-rt3d-shard-<n>-of-4, version 1, loader notebooks rt3d_all_<n-1>of4.ipynb at commit eb3cff0
  v2        numakoudsie/fig15-rt3d-singles-v2,     version 1, loader notebook  rt3d_singles_v2.ipynb  at commit db0a60c
Output: public/data/resonant-tunnelling/<date>/kaggle/runs/*.bin (byte for byte as Kaggle wrote them; the SHA-256 of each is
checked against the notebook's own index before it is copied) and kaggle/index.json.

The single wall and single disc of the four shards (version 1) are NOT filed: rt3d.py then centred them at x = 0, where the
test |x| < D/2 holds one grid point only, half the intended thickness. The singles_v2 notebook replaced them.

Per run, index.json also carries numbers read from the stored file (computed here once, so that the page only reads them):
  T_far   the share of the wave on the far side of the barriers, (P_right + P_in / 2) / P_total, at the last frame before any
          of the wave reaches the absorbing border at the ends of the flight (|x| > 38.4 a holding < 1e-3 of it). Half of what
          is still trapped is counted as leaving forwards (a symmetric pair leaks equally both ways). Dividing by P_total
          removes the share the side border took. For the walls it is checked against the exact 1D twin in the same file.
  tau     the lifetime of the trapped wave, from a straight-line fit of ln P_in(t) where P_in has fallen from 60 % to 5 % of
          its largest value (P_in: between the barriers for walls and discs; inside the inner shell for shells).
Usage: python3 file_rt3d.py <kaggle_main folder> <date>
"""
import json, sys, os, tarfile, hashlib, shutil
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import read_rt3d

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
NOTEBOOKS = {
    "s1": ("numakoudsie/fig15-rt3d-shard-1-of-4", 1, "eb3cff020f755221e5a3d4005e9707106506d6c1", "tools/kaggle/resonant-tunnelling/rt3d_all_0of4.ipynb"),
    "s2": ("numakoudsie/fig15-rt3d-shard-2-of-4", 1, "eb3cff020f755221e5a3d4005e9707106506d6c1", "tools/kaggle/resonant-tunnelling/rt3d_all_1of4.ipynb"),
    "s3": ("numakoudsie/fig15-rt3d-shard-3-of-4", 1, "eb3cff020f755221e5a3d4005e9707106506d6c1", "tools/kaggle/resonant-tunnelling/rt3d_all_2of4.ipynb"),
    "s4": ("numakoudsie/fig15-rt3d-shard-4-of-4", 1, "eb3cff020f755221e5a3d4005e9707106506d6c1", "tools/kaggle/resonant-tunnelling/rt3d_all_3of4.ipynb"),
    "v2": ("numakoudsie/fig15-rt3d-singles-v2", 1, "db0a60cc9f3ed5d63b1b4c7e9fb4d51ed4160f79", "tools/kaggle/resonant-tunnelling/rt3d_singles_v2.ipynb"),
}
BORDER_X = 38.4                                   # the absorbing border fills the outer tenth of the 96 a flight axis


def fit_tau(t, P):
    i = int(np.argmax(P)); pk = P[i]
    if pk < 1e-4: return None
    m = np.zeros(len(P), bool); m[i:] = True; m &= (P <= 0.6 * pk) & (P >= 0.05 * pk)
    j = np.where(m)[0]
    if len(j) < 6: return None
    j = j[: np.argmax(np.diff(np.r_[j, 10**9]) > 1) + 1]            # the first unbroken stretch
    if len(j) < 6: return None
    sl, ic = np.polyfit(t[j], np.log(P[j]), 1)
    if sl >= 0: return None
    return dict(tau=float(-1 / sl), t0=float(t[j[0]]), t1=float(t[j[-1]]), n=int(len(j)))


def summary(h, prof, prof1d):
    c = np.array(h["curves"]); C = {n: c[:, i] for i, n in enumerate(h["curve_names"])}; t = C["t"]
    x = h["prof_x_first"] + np.arange(h["prof_nx"]) * h["step"]
    Bx = prof[:, np.abs(x) > BORDER_X].sum(1) * h["step"]
    ok = Bx < 1e-3 * C["norm"]; f = int(np.argmin(ok)) - 1 if not ok.all() else len(ok) - 1
    shell = h["shape"].endswith("shell")
    Pin = C["gap"] + C["core"] if h["shape"] == "dshell" else C["core"] if shell else C.get("well", np.zeros_like(t))
    out = dict(frame_dt=h["frame_dt"], n=h["n"], t_end=float(t[-1]), peak_max=float(max(h["peaks"])), peak0=h["peak0"],
               end={k: round(float(v[-1]), 6) for k, v in C.items() if k != "t"}, start_in_barrier=h["start_in_barrier"],
               start_in_border=h["start_in_border"], steps=h["steps"], wall=h["wall"], device=h["device"])
    if not shell:
        out["T_far"] = dict(value=round(float((C["right"][f] + 0.5 * (C["well"][f] if "well" in C else 0)) / C["norm"][f]), 5),
                            frame=f, t=round(float(t[f]), 3))
    out["P_in_max"] = round(float(Pin.max()), 6)
    ft = fit_tau(t, Pin) if Pin.max() > 0 else None
    if ft: out["tau"] = {k: round(v, 3) if isinstance(v, float) else v for k, v in ft.items()}
    if prof1d is not None:
        out["twin"] = dict(T=round(h["T_1d_splitstep"], 6), R=round(h["R_1d_splitstep"], 6), T_exact=round(h["T_packet_exact"], 6),
                           sep_check_max=h["sep_check_max"])
        # the twin's own trapped probability, from its stored profile, and its lifetime
        inner = S_IN(h)
        if inner:
            Pw = prof1d[:, (np.abs(x) < inner)].sum(1) * h["step"]
            ft1 = fit_tau(t, Pw)
            if ft1: out["twin"]["tau"] = round(ft1["tau"], 3)
    return out


def S_IN(h):
    return (h["S"] / 2 - h["D"] / 2) if h["shape"] == "dflat" else None


def main(src, date):
    dest = os.path.join(ROOT, "public", "data", "resonant-tunnelling", date, "kaggle"); runs_dir = os.path.join(dest, "runs")
    os.makedirs(runs_dir, exist_ok=True)
    runs, nbs, head = [], [], None
    for key in ["s1", "s2", "s3", "s4", "v2"]:
        idx = json.load(open(os.path.join(src, key, "index.json"))); sha = {r["file"]: r["sha256"] for r in idx["runs"]}
        slug, ver, commit, loader = NOTEBOOKS[key]
        nb = dict(kaggle=slug, version=ver, commit=commit, loader=loader, solver="tools/kaggle/resonant-tunnelling/rt3d.py",
                  runner="tools/kaggle/resonant-tunnelling/rt3d_run.py", jobsel=idx["jobsel"], shard=idx["shard"], device=idx["device"],
                  devices=idx["devices"], sweep_s=idx["sweep_s"], filed=0, not_filed=[])
        if head is None: head = {k: idx[k] for k in ["box", "dx", "dt", "nframes", "V0", "D", "S", "packet", "method", "units"]}
        with tarfile.open(os.path.join(src, key, "rt3d.tar")) as tf:
            for m in tf.getmembers():
                if not m.name.endswith(".bin"): continue
                name = os.path.basename(m.name); blob = tf.extractfile(m).read()
                assert hashlib.sha256(blob).hexdigest() == sha[name], name
                if key != "v2" and name.split("_")[0] in ("sflat", "scoin"):
                    nb["not_filed"].append(name); continue
                h, amp, ph, prof, p1 = read_rt3d.read(blob)
                open(os.path.join(runs_dir, name), "wb").write(blob)
                rec = dict(file="runs/" + name, shape=h["shape"], size=h["size"], E=h["E"], bytes=len(blob), sha256=sha[name],
                           notebook=slug, version=ver, commit=commit)
                rec.update(summary(h, prof, p1)); runs.append(rec); nb["filed"] += 1
        nbs.append(nb)
    runs.sort(key=lambda r: (["dflat", "dcoin", "dshell", "sflat", "scoin", "sshell"].index(r["shape"]), r["size"], r["E"]))
    out = dict(generated=date, kind="rt3d",
               title="Fig. 15, 3D: an electron wave packet meets two barriers (walls, discs, spherical shells) and one barrier",
               **head, notebooks=nbs,
               replaced=dict(what="the 20 single-wall and single-disc runs of the four shard notebooks (version 1)",
                             why=("rt3d.py at commit eb3cff0 centred the single wall and disc at x = 0, where the test |x| < D/2 holds one "
                                  "grid point of the 0.5 a grid: half the intended thickness, so they passed far too much (T = 0.388 "
                                  "against the exact 0.075 at E = 0.735). Corrected at commit db0a60c: the single barrier is the pair's "
                                  "left barrier alone, |x + S/2| < D/2, two grid points; rerun in numakoudsie/fig15-rt3d-singles-v2."),
                             by="numakoudsie/fig15-rt3d-singles-v2, version 1"),
               numbers=__doc__.split("Per run, index.json also carries ")[1].split("Usage:")[0].strip(),
               script="tools/kaggle/resonant-tunnelling/file_rt3d.py", runs=runs)
    json.dump(out, open(os.path.join(dest, "index.json"), "w"), indent=0, ensure_ascii=False)
    print(len(runs), "runs filed;", sum(r["bytes"] for r in runs) / 1e6, "MB")
    for r in runs:
        tw = r.get("twin", {})
        print(f"{r['file']:28s} T_far {r.get('T_far', {}).get('value', '-')!s:8} twin {tw.get('T', '-')!s:10.8} exact {tw.get('T_exact', '-')!s:10.8} "
              f"Pin {r['P_in_max']:.3f} tau {r.get('tau', {}).get('tau', '-')!s:7.6} twin-tau {tw.get('tau', '-')}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])

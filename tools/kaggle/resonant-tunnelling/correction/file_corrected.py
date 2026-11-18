"""Fig. 15 correction: file the corrected runs into one new generation and write the index the page reads.

Usage:
  python3 file_corrected.py <src root> <stored index.json> <date> <out index.json> <runs destination> <records dir>
  python3 file_corrected.py --dry <records dir> <stored index.json>
  <src root>         : searched recursively for the correction notebooks' outputs: walls.tar (wall_gpu_run.py), rt2d_*.tar
                       (rt2d_run.py); every new file's header carries T_ref and its parent {file, sha256}.
  <runs destination> : only the NEW files are copied there (byte for byte), the folder uploaded to R2 under <date>/runs/.
  <records dir>      : notes/fig15/correction (walls_runs.jsonl, rt2d_runs/*.jsonl): one record per new file with its SHA-256,
                       T_ref, and for discs and shells T_unc and drift. Every new file must match its record's SHA-256, or the
                       filer stops.
  --dry              : no archives, nothing written: sorts every run from the records and the stored index, prints the counts.

Per stored run (3,697), with T_ref from the new file:
  T_old   walls and discs: the stored T_far. Shells: none. The stored shell index has no transmission number, and P_out / P_box
          (the share outside the sphere) also counts the reflected wave, so stored shells are not gated; every shell takes its
          new (x, rho) file.
  gate    |T_old - T_ref| <= max(0.005, 1 % of T_ref).
  status  "kept"       : passes; the run keeps its stored file (runs_base points to the stored generation);
          "rebuilt"    : a wall that fails; the exact file replaces it;
          "recomputed" : a disc that fails, or any shell; the (x, rho) file replaces it;
          "failed"     : a wall whose closure P_left + P_struct + P_right - 1 exceeds 1e-4 (stored file kept, listed);
          "missing"    : no new file came back for it (stored file kept, listed).
  per run : T_ref, T_old, error, gate, status; closure_max (walls); drift and T_unc (discs, shells).
  provisional : true where T_unc > 0.005. T_unc is the probability still inside the structure when the run stopped, so T_ref is
          undecided by up to that much. Kept runs carry the flag too, since their check is against that T_ref.
The diode current J(V) is recomputed from T_ref (same supply function and energies as file_rt3d2.py).
"""
import json, sys, os, glob, tarfile, hashlib
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE)); sys.path.insert(0, HERE)

GATE = lambda T_old, T_ref: abs(T_old - T_ref) <= max(0.005, 0.01 * abs(T_ref))
CLOSURE_MAX = 1e-4
PROVISIONAL = 0.005      # T_unc above this: T_ref undecided by more than the gate's absolute part


def load_records(rec_dir):
    """file name -> record of the new file (walls_runs.jsonl, rt2d_runs/*.jsonl); sha = SHA-256 of the new file."""
    R = {}
    for f in [os.path.join(rec_dir, "walls_runs.jsonl")] + sorted(glob.glob(os.path.join(rec_dir, "rt2d_runs", "*.jsonl"))):
        for line in open(f):
            r = json.loads(line); r["sha"] = r.get("sha256") or r.get("sha256_rebuilt")
            assert r["file"] not in R, ("two records for", r["file"]); R[r["file"]] = r
    return R


def extras(shape, rec):
    """closure (walls) or drift, T_unc and the provisional flag (discs, shells), from the record."""
    if shape == "flat": return dict(closure_max=rec.get("closure_max"))
    u = rec.get("T_unc"); return dict(drift=rec.get("drift"), T_unc=u, provisional=bool(u is not None and u > PROVISIONAL))


def sort_run(o, rec):
    """status and gate fields of one stored run o, given the record of its new file."""
    shape = o["spec"]["shape"]; T_ref = float(rec["T_ref"]); q = dict(T_ref=round(T_ref, 7)); q.update(extras(shape, rec))
    if shape == "shell":
        q.update(T_old=None, error=None, gate=None, reason="stored shell index has no transmission"); return "recomputed", q
    T_old = float(o["T_far"]["value"]); ok = GATE(T_old, T_ref)
    q.update(T_old=round(T_old, 6), error=round(T_old - T_ref, 7), gate=ok)
    if shape == "flat" and (rec.get("closure_max") is None or rec["closure_max"] > CLOSURE_MAX): return "failed", q
    return ("kept" if ok else ("rebuilt" if shape == "flat" else "recomputed")), q


def dry(rec_dir, old_index):
    OLD = json.load(open(old_index)); REC = load_records(rec_dir); counts, prov = {}, {}
    for name, o in ((r["file"], r) for r in OLD["runs"]):
        s = o["spec"]["shape"]
        if name in REC: st, q = sort_run(o, REC[name])
        else: st, q = "missing", {}
        counts.setdefault(s, {}).setdefault(st, 0); counts[s][st] += 1
        if q.get("provisional"): prov.setdefault(s, {}).setdefault(st, 0); prov[s][st] += 1
    print(json.dumps(dict(stored=len(OLD["runs"]), records=len(REC), unmatched_records=len(set(REC) - {r["file"] for r in OLD["runs"]}),
                          counts=counts, provisional=prov, provisional_total=sum(v for d in prov.values() for v in d.values())), indent=1))


def border_frame(h, prof, C):
    x = h["prof_x_first"] + np.arange(h["prof_nx"]) * h["step"]; inner = (h["prof_nx"] // 2 - max(4, h["prof_nx"] // 10)) * h["step"]
    Bx = prof[:, np.abs(x) > inner].sum(1) * h["step"]
    ok = Bx < 1e-3 * C["norm"]; return int(np.argmin(ok)) - 1 if not ok.all() else len(ok) - 1


def curves(h): c = np.array(h["curves"]); return {n: c[:, i] for i, n in enumerate(h["curve_names"])}


def summary(h, prof):
    """file_rt3d2.summary for the new files (no split-step twin)."""
    C = curves(h); t = C["t"]; f = border_frame(h, prof, C); shell = h["shape"] == "shell"
    Pin = C["core"] + C.get("gap", 0 * t) if shell else C.get("well", 0 * t)
    out = dict(frame_dt=h["frame_dt"], t_end=float(t[-1]), peak0=h["peak0"], start_in_barrier=h.get("start_in_barrier"),
               end={k: round(float(v[-1]), 6) for k, v in C.items() if k != "t"}, steps=h.get("steps"), wall=h.get("wall"),
               device=h.get("device"), P_in_max=round(float(Pin.max()), 6))
    if not shell:
        out["T_far"] = dict(value=round(float((C["right"][f] + 0.5 * (C["well"][f] if "well" in C else 0)) / C["norm"][f]), 5),
                            frame=f, t=round(float(t[f]), 3))
    ft = fit_tau(t, Pin) if Pin.max() > 0 else None
    if ft: out["tau"] = ft
    return out


def main(src, old_index, date, out_index, dest, rec_dir):
    global fit_tau, supply, EF, KT                 # imported here so that --dry needs only the standard library and numpy
    import read_rt3d
    from file_rt3d2 import fit_tau, supply, EF, KT
    os.makedirs(dest, exist_ok=True)
    OLD = json.load(open(old_index)); old_runs = {r["file"]: r for r in OLD["runs"]}; REC = load_records(rec_dir)
    new = {}
    for d, _, fs in os.walk(src):
        for fn in fs:
            if not fn.endswith(".tar"): continue
            with tarfile.open(os.path.join(d, fn)) as tf:
                for m in tf.getmembers():
                    if not m.name.endswith(".bin"): continue
                    blob = tf.extractfile(m).read(); h = read_rt3d.read(blob)[0]
                    par = h["parent"]["file"]; assert par == os.path.basename(m.name), m.name
                    assert h["parent"]["sha256"] == old_runs[par]["sha256"], par
                    digest = hashlib.sha256(blob).hexdigest()
                    assert par in REC and REC[par]["sha"] == digest, ("new file does not match its record", par)
                    new[par] = (os.path.join(d, fn), m.name, digest, len(blob))
    runs, failed, missing = [], [], []; counts = {}
    for name, o in old_runs.items():
        shape = o["spec"]["shape"]; rec = dict(o)
        if name not in new:
            rec.update(status="missing", runs_base=OLD["runs_base"]); missing.append(name)
        else:
            tpath, mname, digest, nbytes = new[name]
            with tarfile.open(tpath) as tf: blob = tf.extractfile(mname).read()
            h, amp, ph, prof, p1 = read_rt3d.read(blob)
            assert abs(float(h["T_ref"]) - float(REC[name]["T_ref"])) <= 1e-9, ("header T_ref differs from record", name)
            st, q = sort_run(o, REC[name])
            if st == "failed":
                rec.update(q, status="failed", runs_base=OLD["runs_base"]); failed.append(dict(file=name, closure_max=q.get("closure_max")))
            elif st == "kept":
                rec.update(q, status="kept", runs_base=OLD["runs_base"], corrected_file=dict(sha256=digest, notebook=os.path.basename(os.path.dirname(tpath))))
            else:
                rec = dict(file=name, group=o["group"], groups=o.get("groups", [o["group"]]), spec=o["spec"], bytes=nbytes, sha256=digest,
                           box=o.get("box"), parent=dict(file=name, sha256=o["sha256"], notebook=o.get("notebook")),
                           method=h.get("method"))
                rec.update(summary(h, prof)); rec.update(q, status=st)
                open(os.path.join(dest, name), "wb").write(blob)
        counts.setdefault(shape, {}).setdefault(rec["status"], 0); counts[shape][rec["status"]] += 1
        runs.append(rec)
    # the diode from T_ref
    ivs = []
    for shape, R in (("flat", 0.0), ("coin", 6.0)):
        FE = set(np.round(np.arange(0.10, 1.301, 0.05), 3).tolist())
        F = [r for r in runs if r["spec"]["shape"] == shape and r["spec"]["R"] == R and r["spec"]["N"] == 2 and r["spec"]["V0"] == 2
             and r["spec"]["D"] == 1 and r["spec"]["P"] == 2.5 and r["spec"]["sx"] == 3 and round(r["spec"]["E"], 3) in FE and "T_ref" in r]
        J = []
        for V in sorted({r["spec"]["bias"] for r in F}):
            pts = sorted((r["spec"]["E"], r["T_ref"]) for r in F if r["spec"]["bias"] == V)
            if len(pts) < 5: continue
            E = np.array([p[0] for p in pts]); T = np.array([p[1] for p in pts]); J.append([V, float(np.trapezoid(T * supply(E, V), E))])
        ivs.append(dict(shape=shape, R=R, EF=EF, kT=KT, T="T_ref of each run", J_runs=J))
    out = {k: v for k, v in OLD.items() if k not in ("runs", "iv", "replaced")}
    out.update(generated=date, kind="rt3d2", title="Fig. 15, 3D generation 2, corrected: exact walls, exact (x, rho) discs and shells",
               runs_base=f"resonant-tunnelling/{date}/runs/", parent_generation=OLD.get("generated"),
               method=("kept runs: the stored 3D split-step file (" + OLD.get("method", "") + "); rebuilt walls: exact, psi = chi(x,t) h(y,t) "
                       "h(z,t), chi by superposition of stationary scattering states; recomputed discs and shells: the exact axisymmetric "
                       "(m = 0) reduction in (x, rho), Strang split-step, FFT in x, order-0 quasi-discrete Hankel transform in rho"),
               gate=("|T_old - T_ref| <= max(0.005, 1 % of T_ref); T_old: walls and discs the stored T_far; shells not gated (the stored "
                     "shell index has no transmission), all replaced"),
               provisional=f"T_unc > {PROVISIONAL}: probability still inside the structure when the run stopped; T_ref undecided by up to T_unc",
               script="tools/kaggle/resonant-tunnelling/correction/file_corrected.py", iv=ivs, counts=counts, failed=failed, missing=missing,
               runs=runs)
    json.dump(out, open(out_index, "w"), separators=(",", ":"))
    S = dict(counts=counts, failed=failed, missing=missing, new_files=sum(1 for r in runs if r["status"] in ("rebuilt", "recomputed")),
             new_bytes=sum(r["bytes"] for r in runs if r["status"] in ("rebuilt", "recomputed")),
             gate_pass={s: sum(1 for r in runs if r["spec"]["shape"] == s and r.get("gate")) for s in counts},
             provisional={s: sum(1 for r in runs if r["spec"]["shape"] == s and r.get("provisional")) for s in counts},
             err_abs_median={s: float(np.median([abs(r["error"]) for r in runs if r["spec"]["shape"] == s and "error" in r] or [0])) for s in counts},
             err_abs_max={s: float(max([abs(r["error"]) for r in runs if r["spec"]["shape"] == s and "error" in r] or [0])) for s in counts})
    json.dump(S, open(os.path.join(os.path.dirname(os.path.abspath(out_index)), "summary.json"), "w"), indent=1)
    print(json.dumps(S, indent=1))


if __name__ == "__main__":
    if sys.argv[1] == "--dry": dry(*sys.argv[2:4])
    else: main(*sys.argv[1:7])

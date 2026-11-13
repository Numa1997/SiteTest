"""Pack the reconstructed runs into the website's derived-data tree, with provenance.

Reads the output of recon.py (SCRATCH/runs/*.bin + summary.json) and writes

  public/data/resonant-tunnelling/
    generations.json                      the list of generations (as for Fig. 14)
    <date>/
      derived/
        index.json                        every run file: parameters, size, SHA-256, and its PARENTS
        runs/s{g}_p{s0}_E{E}.bin          the 'RTF1' frame files
      curves.json                         T(E) of each geometry and of one barrier, resonances, the single-barrier B1 check

Provenance, the owner's rule: data made from other data names its parents. These runs are built from the EXACT single-barrier
scattering amplitudes (transfer matrices, Griffiths & Steinke), which were checked against Fig. 14's stored single-barrier runs
(V0 = 3, d = 1). So each derived file names, as parents, the recon.py script and commit, and the Fig. 14 flat-wall runs of the
same barrier (V0 = 3, every thickness and energy) by generation, file and SHA-256 — the runs that confirm the amplitudes.
Usage: python3 pack.py SCRATCHDIR [--date YYYY-MM-DD]
"""
import json, os, sys, shutil, subprocess, datetime, hashlib
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, "../../.."))
SCRATCH = sys.argv[1]
DATE = next((sys.argv[i + 1] for i, a in enumerate(sys.argv) if a == "--date"), datetime.date.today().isoformat())
DEST = os.path.join(ROOT, "public/data/resonant-tunnelling")
COMMIT = subprocess.run(["git", "-C", ROOT, "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()

summary = json.load(open(os.path.join(SCRATCH, "summary.json")))

# Fig. 14 single-barrier parents: the flat-wall runs with V0 = 3 (j = 8 in its grid), every energy and thickness
f14 = json.load(open(os.path.join(ROOT, "public/data/schrodinger-sphere/2026-11-12/flat/index.json")))
parents = [dict(file="2026-11-12/flat/" + r["file"], sha256=r["sha256"], E=r["E"], V0=r["V0"], a=r["a"])
           for r in f14["runs"] if r["V0"] == summary["V0"]]
b1 = json.load(open(os.path.join(SCRATCH.rsplit("/", 1)[0], "b1_survey.json"))) if os.path.exists(
    os.path.join(SCRATCH.rsplit("/", 1)[0], "b1_survey.json")) else None

dd = os.path.join(DEST, DATE, "derived"); os.makedirs(os.path.join(dd, "runs"), exist_ok=True)
for r in summary["runs"]:
    shutil.copy(os.path.join(SCRATCH, "runs", r["file"]), os.path.join(dd, "runs", r["file"]))

index = dict(generated=DATE, kind="derived", method=summary["runs"][0].get("method", "transfer-matrix superposition"),
             what="Time-dependent double-barrier wave functions, built from the exact single-barrier scattering amplitudes "
                  "(transfer matrices) superposed with the incident packet's spectrum. The page plays these frames; it computes nothing.",
             units="hbar = m = 1, lengths in the grid unit a", V0=summary["V0"], d=summary["d"], gaps=summary["gaps"],
             packets=summary["packets"], dx=summary["dx"], file_format="RTF1 (see tools/kaggle/resonant-tunnelling/recon.py)",
             source=dict(script="tools/kaggle/resonant-tunnelling/recon.py", helper="tools/kaggle/resonant-tunnelling/tm.py",
                         commit=COMMIT, builder="tools/kaggle/resonant-tunnelling/pack.py"),
             parents=dict(what="Fig. 14 flat-wall single-barrier runs of the same barrier (V0 = 3), which confirm the exact "
                          "amplitudes this data is built from (see curves.json, b1_check).",
                          generation="public/data/schrodinger-sphere/2026-11-12/flat/", files=parents),
             runs=[dict(file="runs/" + r["file"], gap=r["gap"], s=r["s"], sigma0=r["sigma0"], E=r["E"], bytes=r["bytes"],
                        sha256=r["sha256"], nf=r["nf"], t_end=r["t_end"], T_packet=r["T_packet"], T_k0=r["T_k0"],
                        P_right_end=r["P_right_end"], P_in_end=r["P_in_end"], norm_min=r["norm_min"], norm_max=r["norm_max"],
                        start_error=r["start_error"], fp16_max_rel=r["fp16_max_rel"], interp_err_max=r["interp_err_max"],
                        peak=r["peak"], zoom_peak=r["zoom_peak"], tau_fit=(r["fit"] or {}).get("tau")) for r in summary["runs"]])
json.dump(index, open(os.path.join(dd, "index.json"), "w"), separators=(",", ":"))

curves = dict(generated=DATE, V0=summary["V0"], d=summary["d"], gaps=summary["gaps"],
              single=summary["single"], geometries=[dict(s=g["s"], resonances=g["resonances"], T_E=g["T_E"]) for g in summary["geometries"]],
              b1_check=(b1 and b1["summary"]))
json.dump(curves, open(os.path.join(DEST, DATE, "curves.json"), "w"), separators=(",", ":"))

gens_path = os.path.join(DEST, "generations.json")
gens = json.load(open(gens_path)) if os.path.exists(gens_path) else []
gens = [g for g in gens if g.get("date") != DATE]
gens.append(dict(date=DATE, index=f"{DATE}/derived/index.json", curves=f"{DATE}/curves.json", kind="derived",
                 runs=len(summary["runs"]), source="tools/kaggle/resonant-tunnelling/recon.py", commit=COMMIT))
gens.sort(key=lambda g: g["date"])
json.dump(gens, open(gens_path, "w"), indent=1)

total = sum(r["bytes"] for r in summary["runs"])
print(f"packed {len(summary['runs'])} runs, {total/1e6:.1f} MB, largest {max(r['bytes'] for r in summary['runs'])/1e3:.0f} kB -> {dd}")
print(f"parents: {len(parents)} Fig. 14 flat runs (V0 = {summary['V0']})")

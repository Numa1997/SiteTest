"""Writes the one Kaggle notebook of Fig. 15, numakoudsie/fig-15-resonant-tunnelling (rule of 14 November 2026:
one notebook and one dataset per figure; docs/kaggle-pipeline.md, "Layout on Kaggle").

JOB = "curate" (CPU) reads the old 26.9 GB dataset numakoudsie/fig15-resonant-tunnelling and writes to /kaggle/working only what
the page plays, checked byte for byte against the live index (the code that made them is in this repository at the commits below):
  resonant-tunnelling/2026-11-18/kaggle/index.json, summary.json   the live index (from the filer's version 4)
  resonant-tunnelling/2026-11-18/runs/*.bin                        2,782 corrected runs (filer version 4)
  resonant-tunnelling/2026-11-14/runs/*.bin                        the 915 generation-2 runs the corrected generation keeps
  MANIFEST.json                                                     size and SHA-256 of every file; the check against the index
The new dataset numakoudsie/fig15-resonant-tunnelling-data is made from this output.
JOB = "check" (CPU) reads that new dataset and checks every file against MANIFEST.json and every run against the live index.
Usage: python3 build.py   (writes fig-15-resonant-tunnelling.ipynb and kernel-metadata.json beside this file)"""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "fig-15-resonant-tunnelling"

INTRO = """# Fig. 15, Resonant Tunnelling: every computation of the figure in one notebook

Phyein Usul, <https://phyeinusul.com/simulations/resonant-tunnelling.html>. An electron wave packet meets one to ten barriers
(walls, discs, spherical shells) and passes almost completely at the resonant energies.

| job | computed | machine | code (repository Numa1997/SiteTest) | old notebooks |
|---|---|---|---|---|
| generation 1 | 115 runs in 3D, two barriers | GPU T4 x2 | `tools/kaggle/resonant-tunnelling/rt3d.py` at `eb3cff0`, `db0a60c` | `fig15-rt3d-shard-1..4-of-4`, `fig15-rt3d-singles-v2` |
| generation 2 | 3,697 runs in 3D, the whole parameter space | GPU T4 x2 | `rt3d2.py` at `cdcade4`, `57770d2` | `fig15-rt3d2-shard-1..6-of-6`, `fig15-rt3d2-fix1` |
| exact walls | 1,088 walls by stationary scattering states | GPU T4 x2 | `correction/wall_gpu_run.py` at `c53a447` | `fig15-correction-walls-gpu` |
| discs and shells | the exact (x, rho) reduction | GPU T4 x2 | `correction/rt2d_run.py` at `5d0490f`, `07ac9bf` | `fig15-correction-2d-*` |
| filing | the corrected generation 2026-11-18 | CPU | `correction/file_corrected.py` at `12b8fd0` | `fig15-filer-2026-11-18` |

`JOB = "curate"` built the dataset `numakoudsie/fig15-resonant-tunnelling-data` from the old one; `JOB = "check"` checks it."""

CFG = '''JOB = "curate"   # or "check"
OLD = "fig15-resonant-tunnelling"         # the old dataset (input of curate)
NEW = "fig15-resonant-tunnelling-data"    # the curated dataset (input of check)
LIVE = "https://phyeinusul.com/data/resonant-tunnelling/2026-11-18/kaggle/index.json"
'''

CODE = r'''import os, re, json, glob, hashlib, shutil, time, datetime, urllib.request
T0 = time.time(); W = "/kaggle/working"
def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 22), b""): h.update(b)
    return h.hexdigest()
def root(name, mark):
    """the folder of an attached dataset: the parent of its first folder named `mark` (Kaggle mounts under /kaggle/input/<slug>
    or /kaggle/input/datasets/<owner>/<slug>)"""
    for d, sub, _ in os.walk("/kaggle/input"):
        if mark in sub: return d
        if d.count("/") > 6: sub[:] = []
    print(os.listdir("/kaggle/input")); raise SystemExit(f"attach the dataset numakoudsie/{name}")
live = json.load(urllib.request.urlopen(urllib.request.Request(LIVE, headers={"User-Agent": "Mozilla/5.0 (Kaggle notebook fig-15)"})))
runs = live["runs"]; BASE = live["runs_base"]
print(len(runs), "runs in the live index;", BASE)

if JOB == "curate":
    DS = root(OLD, "fig15-filer-2026-11-18"); print("old dataset at", DS)
    filer = [p for p in glob.glob(f"{DS}/fig15-filer-2026-11-18/**/v4/output/resonant-tunnelling", recursive=True)]
    assert len(filer) == 1, filer
    F = filer[0]
    # 1. the live index and summary, then the 2,782 corrected runs
    for f in ("index.json", "summary.json"):
        os.makedirs(f"{W}/resonant-tunnelling/2026-11-18/kaggle", exist_ok=True)
        shutil.copyfile(f"{F}/2026-11-18/kaggle/{f}", f"{W}/resonant-tunnelling/2026-11-18/kaggle/{f}")
    assert json.load(open(f"{W}/resonant-tunnelling/2026-11-18/kaggle/index.json"))["runs"] == runs, "filer index differs from the live index"
    new = [r for r in runs if r.get("runs_base", BASE) == BASE]
    kept = [r for r in runs if r.get("runs_base", BASE) != BASE]
    print(len(new), "corrected runs,", len(kept), "kept generation-2 runs")
    # 2. every .bin of generation 2, by name (a name may occur twice: shards and fix1; the SHA-256 decides)
    g2 = {}
    for p in glob.glob(f"{DS}/fig15-rt3d2-*/**/*.bin", recursive=True):
        g2.setdefault(os.path.basename(p), []).append(p)
    bad = []
    def put(r, src_list, dest_dir):
        os.makedirs(dest_dir, exist_ok=True)
        for s in src_list:
            if os.path.getsize(s) == r["bytes"] and sha(s) == r["sha256"]:
                shutil.copyfile(s, f"{dest_dir}/{r['file']}"); return True
        bad.append(r["file"]); return False
    for r in new: put(r, [f"{F}/2026-11-18/runs/{r['file']}"], f"{W}/resonant-tunnelling/2026-11-18/runs")
    for r in kept: put(r, g2.get(r["file"], []), f"{W}/{r['runs_base']}".rstrip("/"))
    print("runs not found or not identical:", len(bad), bad[:10])
    assert not bad
    # 3. manifest
    files = {}
    for p in sorted(glob.glob(f"{W}/**/*", recursive=True)):
        if os.path.isfile(p) and not p.startswith(f"{W}/MANIFEST"):
            files[os.path.relpath(p, W)] = dict(bytes=os.path.getsize(p), sha256=sha(p))
    tot = sum(f["bytes"] for f in files.values())
    json.dump(dict(made=datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"), live_index=LIVE,
                   runs_checked=len(runs), runs_identical=len(runs) - len(bad), files=files, bytes=tot), open(f"{W}/MANIFEST.json", "w"), indent=1)
    print(f"{len(files)} files, {tot/1e9:.3f} GB, {time.time()-T0:.0f} s")

if JOB == "check":
    DS = root(NEW, "resonant-tunnelling"); print("dataset at", DS)
    m = json.load(open(f"{DS}/MANIFEST.json"))
    diff = [k for k, v in m["files"].items() if not os.path.isfile(f"{DS}/{k}") or os.path.getsize(f"{DS}/{k}") != v["bytes"] or sha(f"{DS}/{k}") != v["sha256"]]
    rmiss = [r["file"] for r in runs if m["files"].get(f"{r.get('runs_base', BASE)}{r['file']}", {}).get("sha256") != r["sha256"]]
    rep = dict(files=len(m["files"]), files_different_or_missing=diff, runs=len(runs), runs_not_matching_live_index=rmiss, seconds=round(time.time()-T0))
    json.dump(rep, open(f"{W}/check.json", "w"), indent=1)
    print("ALL OK" if not diff and not rmiss else "PROBLEMS FOUND", json.dumps(rep)[:2000])
'''

def cell(kind, src, i): 
    c = dict(cell_type=kind, metadata={}, source=src, id=f"c{i}")
    if kind == "code": c.update(execution_count=None, outputs=[])
    return c
nb = dict(cells=[cell("markdown", INTRO, 0), cell("code", CFG, 1), cell("code", CODE, 2)], nbformat=4, nbformat_minor=5,
          metadata=dict(kernelspec=dict(display_name="Python 3", language="python", name="python3"), language_info=dict(name="python")))
json.dump(nb, open(f"{HERE}/{SLUG}.ipynb", "w"), indent=1)
json.dump(dict(id=f"numakoudsie/{SLUG}", title="Fig 15 Resonant Tunnelling", code_file=f"{SLUG}.ipynb", language="python",
               kernel_type="notebook", is_private=True, enable_gpu=False, enable_internet=True,
               dataset_sources=["numakoudsie/fig15-resonant-tunnelling"], competition_sources=[], kernel_sources=[]),
          open(f"{HERE}/kernel-metadata.json", "w"), indent=1)
print("wrote", SLUG)

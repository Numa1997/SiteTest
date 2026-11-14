"""Writes one Kaggle notebook per figure: tools/kaggle/figures/<slug>/<slug>.ipynb and its kernel-metadata.json. The slug is the one Kaggle
made from the title (fig-14-schrodinger-sphere, fig-12-guinness-on-a-cart); push with: kaggle kernels push -p <slug>.
Layout rule of 14 November 2026 (docs/kaggle-pipeline.md, "Layout on Kaggle"): one notebook and one dataset per figure.

The figure's notebook has every job of the figure in it. The setting JOB (first code cell) picks one:
  JOB = "check"   (the default; CPU, a few minutes, free) reads the figure's dataset, checks every stored file against its
                  manifest (size and SHA-256) and checks that the code of every job is present and compiles. Writes check.json.
  JOB = "<name>"  runs that job: the exact code of the old notebook that made the data, read from the dataset
                  (<old slug>/source-current-version.ipynb), cell by cell, through IPython. That code fetches its solver
                  from this repository at the pinned commit printed in the job table, so a rerun is the same computation.
                  A GPU job needs the accelerator switched on when the notebook is pushed (column "machine" below).
Each run of the figure's notebook is a new version of the same notebook; its output goes into the figure's dataset as
<figure slug>/v<version>/ (same layout as the old notebooks' folders).
Usage: python3 build.py            (writes every figure)   python3 build.py fig-14-schrodinger-sphere"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
OWNER = "numakoudsie"

FIGURES = {
    "fig-14-schrodinger-sphere": dict(
        title="Fig 14 Schrodinger sphere", figure="Fig. 14, Schrödinger sphere", dataset="fig14-schrodinger-sphere",
        record="public/data/schrodinger-sphere/generations.json",
        jobs=[  # name, old notebook (its code and outputs are in the dataset under this folder), machine, pinned commit (read from the stored code), what it computes
            ("full-grid", "schrodinger-sphere-full-grid", "GPU T4 x2", "10dc1d64200446165d40456972d9b51047846f71", "the sphere in 3D: 9 energies x 9 heights x 5 radii = 405 runs, 128^3 cells"),
            ("3d-wave", "schrodinger-sphere-3d-wave", "GPU T4 x2", "7083b64c90303ffabe4355e7359a347a392a6485", "the 3D wave Re psi for the 3D view of the sphere"),
            ("flat-wall", "schrodinger-flat-wall", "CPU", "76c7ce089557d9939ed1f63f5535021057f387ee", "the flat wall (1D across the wall, exact in 3D)"),
            ("pillar", "schrodinger-pillar", "CPU", "89f6e9d3305f243b2507ae64f6ab9c4a186bdbef", "the pillar (2D in the plane, exact in 3D): 585 runs"),
            ("spherical-wave", "schrodinger-spherical-wave", "CPU", "13dda4cef3aeb6cd00ea3dbb48ee8a770344afcc", "a spherical wave onto the sphere (axisymmetric)"),
            ("shapes-3d", "schrodinger-shapes-3d", "GPU T4 x2", "94d1281585c91001fd6024c67b1045ed01691817", "coin, tube, wells, hard ball, spherical wave from the side (version 2: hard and shell runs, 243)"),
            ("3d-generation", "schrodinger-sphere-3d-generation", "GPU T4 x2", "5941f633a4c2a96a146e08c86bd3e5341e21c02a", "a 3D cloud of 81 runs; on no page, kept as data only"),
        ]),
    "fig-12-guinness-on-a-cart": dict(
        title="Fig 12 Guinness on a cart", figure="Fig. 12, Guinness on a cart", dataset="fig12-guinness-on-a-cart",
        record="public/data/fig12/generations.json",
        jobs=[
            ("stout-in-jax", "guinness-on-a-cart-stout-in-jax", "GPU T4 x2", "58eea6870a20b8edfaa9ef46ee655cf1e890fdfe", "the stout in JAX: the rides the page plays (current code is version 10)"),
            ("stout-sloshing", "guinness-on-a-cart-stout-sloshing", "GPU T4 x2", "70703de1821fc5f28a5592a1a74c8d3c84a73488", "Taichi generation: the rides of rides.json (version 5)"),
            ("free-swing", "guinness-free-swing-v2", "GPU T4 x2", "3d6f61a79c7356fdb044c6f134cf385783a492b7", "Taichi generation: the free swing and its repair (versions 4 and 5)"),
        ]),
}

CHECK = r'''# ---- find the figure's dataset, then check it or run one job ----
import os, json, glob, hashlib, time, datetime
T0 = time.time()
cands = [os.path.dirname(p) for p in glob.glob("/kaggle/input/**/README.md", recursive=True)
         if all(os.path.isdir(os.path.join(os.path.dirname(p), j["folder"])) for j in JOBS)]
assert cands, "attach the dataset %s (Add Input) and run again" % DATASET
DS = cands[0]; print("dataset at", DS)
def source_of(job):
    nb = json.load(open(os.path.join(DS, job["folder"], "source-current-version.ipynb")))
    return [("".join(c["source"]) if isinstance(c["source"], list) else c["source"]) for c in nb["cells"] if c["cell_type"] == "code"]
OUT = "/kaggle/working/" + datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
os.makedirs(OUT, exist_ok=True)
if JOB == "check":
    from IPython.core.inputtransformer2 import TransformerManager
    TM = TransformerManager(); report = dict(dataset=DATASET, path=DS, jobs={}, versions={})
    for j in JOBS:
        cells = source_of(j)
        for n, src in enumerate(cells): compile(TM.transform_cell(src), f"{j['name']} cell {n}", "exec")
        assert any(j["commit"] in src for src in cells), f"job {j['name']}: the stored code does not name commit {j['commit']}"
        report["jobs"][j["name"]] = dict(folder=j["folder"], code_cells=len(cells), compiles=True, commit_in_code=True)
        print(f"job {j['name']:15s} code: {len(cells)} cells, all compile, commit {j['commit'][:7]} named in the code")
    for man in sorted(glob.glob(os.path.join(DS, "*", "v*", "manifest.json"))):
        m = json.load(open(man)); base = os.path.join(os.path.dirname(man), "output")
        same = differ = unpacked = dropped = 0; missing = []
        for f in m["files"]:
            p = os.path.join(base, f["file"])
            if os.path.isfile(p):
                h = hashlib.sha256()
                with open(p, "rb") as fh:
                    for blk in iter(lambda: fh.read(1 << 22), b""): h.update(blk)
                ok = os.path.getsize(p) == f["bytes"] and h.hexdigest() == f["sha256"]
                same += ok; differ += not ok
            elif f["file"].endswith(".tar") and (os.path.isdir(p) or os.path.isdir(p[:-4])): unpacked += 1   # Kaggle unpacks tars
            elif f["file"].endswith(".pyc"): dropped += 1                                                   # Kaggle drops __pycache__
            else: missing.append(f["file"])
        key = os.path.relpath(os.path.dirname(man), DS)
        report["versions"][key] = dict(files=len(m["files"]), identical=same, different=differ, tar_unpacked=unpacked, pyc_dropped=dropped, missing=missing)
        print(f"{key:45s} {len(m['files']):5d} files: {same} identical, {differ} different, {unpacked} tars unpacked, {dropped} .pyc dropped, {len(missing)} missing")
    report["ok"] = all(v["different"] == 0 and not v["missing"] for v in report["versions"].values())
    report["seconds"] = round(time.time() - T0, 1)
    json.dump(report, open(OUT + "/check.json", "w"), indent=1)
    print("ALL OK" if report["ok"] else "PROBLEMS FOUND", "in", report["seconds"], "s")
else:
    job = next(j for j in JOBS if j["name"] == JOB)
    print("running job", JOB, "with the code of", job["folder"], "(commit", job["commit"] + ")")
    for n, src in enumerate(source_of(job)):
        print(f"---- cell {n} ----\n{src}")
        r = get_ipython().run_cell(src)
        if not r.success: raise RuntimeError(f"cell {n} of job {JOB} failed")
'''

def build(slug):
    F = FIGURES[slug]
    jobs = [dict(name=n, folder=f, machine=m, commit=c, what=w) for n, f, m, c, w in F["jobs"]]
    table = "\n".join(f"| `{j['name']}` | {j['what']} | {j['machine']} | `{j['commit'][:7]}` | `{j['folder']}/` |" for j in jobs)
    md = (f"# {F['figure']}: every computation of the figure in one notebook\n\n"
          f"Phyein Usul (phyeinusul.com). Data: dataset `{OWNER}/{F['dataset']}` (attach it as input). "
          f"Record of origin: `{F['record']}` in the site's repository. Built by `tools/kaggle/figures/build.py`.\n\n"
          "Set `JOB` in the first code cell. `check` (default, CPU) verifies every stored file (size and SHA-256 against its "
          "manifest) and that every job's code compiles. Any other name reruns that job with the exact code that made the data; "
          "that code fetches its solver from the repository at the pinned commit. GPU jobs need the GPU switched on.\n\n"
          "| JOB | computes | machine | commit | code and outputs in the dataset |\n|---|---|---|---|---|\n" + table)
    setting = (f'JOB = "check"   # or one of: {", ".join(j["name"] for j in jobs)}\n'
               f'DATASET = "{OWNER}/{F["dataset"]}"\nJOBS = {json.dumps(jobs, ensure_ascii=False, indent=1)}\n')
    cells = [dict(cell_type="markdown", metadata={}, source=md, id="c0"),
             dict(cell_type="code", execution_count=None, metadata={}, outputs=[], source=setting, id="c1"),
             dict(cell_type="code", execution_count=None, metadata={}, outputs=[], source=CHECK, id="c2")]
    nb = dict(cells=cells, nbformat=4, nbformat_minor=5,
              metadata=dict(kernelspec=dict(display_name="Python 3", language="python", name="python3"), language_info=dict(name="python")))
    os.makedirs(os.path.join(HERE, slug), exist_ok=True)
    open(os.path.join(HERE, slug, slug + ".ipynb"), "w").write(json.dumps(nb, ensure_ascii=False, indent=1))
    meta = dict(id=f"{OWNER}/{slug}", title=F["title"], code_file=slug + ".ipynb", language="python", kernel_type="notebook",
                is_private=True, enable_gpu=False, enable_tpu=False, enable_internet=True,
                dataset_sources=[f"{OWNER}/{F['dataset']}"], competition_sources=[], kernel_sources=[], model_sources=[])
    open(os.path.join(HERE, slug, "kernel-metadata.json"), "w").write(json.dumps(meta, indent=1) + "\n")
    print("wrote", slug, len(jobs), "jobs")

for s in (sys.argv[1:] or FIGURES): build(s)

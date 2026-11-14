"""Writes the Kaggle loader notebook of the 2D (x, rho) correction runs: rt2d_smoke.ipynb or rt2d_all_<i>of<n>.ipynb.
The loader fetches axisym.py, axisym_jax.py, rt2d_run.py, rt2d_smoke.py and jobs_2d.json from this repository at a pinned commit,
prints the code, and runs the smoke test or one shard (jobs i, i + n, ...). The runner stops at once without a GPU.
Usage: python3 build_rt2d.py <commit> smoke | all <i> <n>"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
COMMIT = sys.argv[1]; JOBSEL = sys.argv[2]
SHARD = (int(sys.argv[3]), int(sys.argv[4])) if len(sys.argv) > 4 else None
BASE = f"https://raw.githubusercontent.com/Numa1997/SiteTest/{COMMIT}/tools/kaggle/resonant-tunnelling/correction/"
md = ("# Fig. 15 correction: discs and shells in the exact (x, rho) reduction (GPU, JAX)\n\nThe packet flies along the axis of "
      "every disc and shell, so the 3D wave has no angle dependence: the 3D problem is exactly a 2D one in (x, rho). Split-step: FFT "
      "along x (0.0625 a, cell-averaged barriers), order-0 quasi-discrete Hankel transform in rho. "
      f"Job set: {JOBSEL}" + (f", shard {SHARD[0]} of {SHARD[1]}" if SHARD else "") + f". Code from the website's repository at commit {COMMIT}.")
c1 = ('import jax; print(jax.devices())\nif jax.default_backend() != "gpu":\n    print("NO GPU BACKEND"); raise SystemExit("NO GPU BACKEND")\n'
      f'import urllib.request\nBASE = "{BASE}"\n'
      'for f in ("axisym.py", "axisym_jax.py", "rt2d_run.py", "rt2d_smoke.py", "jobs_2d.json"):\n'
      '    urllib.request.urlretrieve(BASE + f, f)\n    if f.endswith(".py"): print("=" * 20, f, "=" * 20); print(open(f).read())\n')
if JOBSEL == "smoke":
    c2 = 'exec(open("rt2d_smoke.py").read())\n'
else:
    c2 = f'RUN = True\nGEN = "2026-11-14b"\nSHARD = {SHARD}\nexec(open("rt2d_run.py").read())\n'
cells = [dict(cell_type="markdown", metadata={}, source=md, id="m0"),
         dict(cell_type="code", execution_count=None, metadata={}, outputs=[], source=c1, id="c1"),
         dict(cell_type="code", execution_count=None, metadata={}, outputs=[], source=c2, id="c2")]
nb = dict(cells=cells, metadata={"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                                 "language_info": {"name": "python"}}, nbformat=4, nbformat_minor=5)
name = "rt2d_" + JOBSEL + (f"_{SHARD[0]}of{SHARD[1]}" if SHARD else "") + ".ipynb"
open(os.path.join(HERE, name), "w").write(json.dumps(nb, indent=1)); print(name, "written")

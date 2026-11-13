"""Writes rt3d2_<JOBSEL>[_<i>of<n>].ipynb (generation 2: the whole parameter space; rt3d2.py, rt3d2_run.py). Formerly: writes rt3d.ipynb: the Kaggle GPU notebook of Fig. 15's 3D runs (two barriers in 3D; tools/kaggle/resonant-tunnelling/rt3d.py).
The notebook is a loader: it fetches rt3d.py, tm.py and rt3d_run.py from this repository at a pinned commit, prints them, and
runs rt3d_run.py, which stops at once if there is no GPU, writes every run as it finishes and logs one line per run.
Usage: python3 build_rt3d.py <commit> [JOBSEL] [SHARD_i SHARD_n]     JOBSEL: smoke | all"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
COMMIT = sys.argv[1]
JOBSEL = sys.argv[2] if len(sys.argv) > 2 else "smoke"
SHARD = (int(sys.argv[3]), int(sys.argv[4])) if len(sys.argv) > 4 else None
BASE = f"https://raw.githubusercontent.com/Numa1997/SiteTest/{COMMIT}/tools/kaggle/resonant-tunnelling/"
md = ("# Fig. 15, resonant tunnelling in 3D, generation 2 (GPU, JAX)\n\nAn electron wave packet meets barriers in 3D: walls, discs (radius 2 to 12) and spherical shells; one, two, three, five and ten in a row; heights 1.5 to 3, thicknesses 1 to 2, spacings 2.5 to 5.5; a bias across the diode; long packets across the narrow resonances. Split-step Fourier on 192 (to 512) x 128 x 128 points (0.5 a), dt = 0.01, 200 frames per run. "
      f"Job set: {JOBSEL}" + (f", shard {SHARD[0]} of {SHARD[1]}" if SHARD else "") + ". Code fetched from the website's repository at "
      f"commit {COMMIT} and printed below.")
c1 = (f'import urllib.request, sys, os\nBASE = "{BASE}"\n'
      'for f in ("rt3d2.py", "tm.py", "rt3d2_run.py"):\n    urllib.request.urlretrieve(BASE + f, f)\n    print("=" * 20, f, "=" * 20); print(open(f).read())\n')
c2 = f'JOBSEL = "{JOBSEL}"\n' + (f"SHARD = {SHARD}\n" if SHARD else "") + 'exec(open("rt3d2_run.py").read())\n'
cells = [dict(cell_type="markdown", metadata={}, source=md, id="m0"),
         dict(cell_type="code", execution_count=None, metadata={}, outputs=[], source=c1, id="c1"),
         dict(cell_type="code", execution_count=None, metadata={}, outputs=[], source=c2, id="c2")]
nb = dict(cells=cells, metadata={"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                                 "language_info": {"name": "python"}}, nbformat=4, nbformat_minor=5)
name = "rt3d2_" + JOBSEL + (f"_{SHARD[0]}of{SHARD[1]}" if SHARD else "") + ".ipynb"
open(os.path.join(HERE, name), "w").write(json.dumps(nb, indent=1))
print(name, "written")

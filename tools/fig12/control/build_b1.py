"""Writes the one-cell Kaggle notebook of Gate B1 (b1.ipynb) that fetches cartctl.py, b1_run.py and ref_series.json at a
pinned commit and runs b1_run.py on the GPU:   python3 tools/fig12/control/build_b1.py <commit>"""
import json, sys, os
commit = sys.argv[1]
cell = f'''# Fig. 12 with control, Gate B1: the JAX port of the cart and every controller against the site's reduced model.
# Code from github.com/Numa1997/SiteTest at commit {commit}, tools/fig12/control/.
import subprocess, sys, os, urllib.request, runpy
print(subprocess.run(["nvidia-smi", "--query-gpu=name,memory.total", "--format=csv,noheader"], capture_output=True, text=True).stdout)
try:
    import jax
    if jax.devices()[0].platform != "gpu": raise ImportError
except Exception:
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", "jax[cuda12]==0.4.35"], check=True)
    import jax
print("jax", jax.__version__, jax.devices())
if jax.devices()[0].platform != "gpu": raise RuntimeError("no GPU: stopping")
D = "/tmp/b1"; os.makedirs(D, exist_ok=True)
BASE = "https://raw.githubusercontent.com/Numa1997/SiteTest/{commit}/tools/fig12/control/"
for f in ["cartctl.py", "b1_run.py", "ref_series.json"]:
    open(os.path.join(D, f), "wb").write(urllib.request.urlopen(BASE + f).read())
sys.path.insert(0, D)
runpy.run_path(os.path.join(D, "b1_run.py"), run_name="__main__")
'''
nb = {"cells": [{"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [], "source": cell}],
      "metadata": {"kernelspec": {"name": "python3", "display_name": "Python 3", "language": "python"}}, "nbformat": 4, "nbformat_minor": 5}
here = os.path.dirname(os.path.abspath(__file__))
json.dump(nb, open(os.path.join(here, "b1.ipynb"), "w"), indent=1)
open(os.path.join(here, "b1_cell.py"), "w").write(cell)
print("wrote b1.ipynb for commit", commit)

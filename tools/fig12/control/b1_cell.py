# Fig. 12 with control, Gate B1: the JAX port of the cart and every controller against the site's reduced model.
# Code from github.com/Numa1997/SiteTest at commit a5c31bdede37851d31f232bebd05d4bd2d75c077, tools/fig12/control/.
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
BASE = "https://raw.githubusercontent.com/Numa1997/SiteTest/a5c31bdede37851d31f232bebd05d4bd2d75c077/tools/fig12/control/"
for f in ["cartctl.py", "b1_run.py", "ref_series.json"]:
    open(os.path.join(D, f), "wb").write(urllib.request.urlopen(BASE + f).read())
sys.path.insert(0, D)
runpy.run_path(os.path.join(D, "b1_run.py"), run_name="__main__")

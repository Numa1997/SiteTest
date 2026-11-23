# Kaggle notebook "phyein-usul-double-pendulum-gpu": Fig. 2, the double pendulum, every start of the page's grid on the GPU.
# It clones Numa1997/SiteTest at a pinned commit and runs tools/kaggle/double-pendulum/dp_gpu.py; the data lands in /kaggle/working/out.
COMMIT = "__COMMIT__"     # the commit whose dp_gpu.py runs
SMOKE = __SMOKE__         # True: a few files of the default cell only (a test of the whole notebook)
import subprocess, sys
def sh(*a, check=True): r = subprocess.run(list(a), capture_output=True, text=True); print(r.stdout[-3000:], r.stderr[-3000:]); r.check_returncode() if check else None; return r
sh("nvidia-smi")
probe = "import jax; print(jax.__version__, jax.devices())"
r = sh(sys.executable, "-c", probe, check=False)
if "cuda" not in (r.stdout + r.stderr).lower() and "gpu" not in r.stdout.lower():
    sh(sys.executable, "-m", "pip", "install", "-q", "-U", "jax[cuda12]")
    r = sh(sys.executable, "-c", probe, check=False)
if "cuda" not in (r.stdout + r.stderr).lower() and "gpu" not in r.stdout.lower():
    raise SystemExit("no GPU seen by JAX: stopping before any computing")
src = "/kaggle/working/src"
sh("git", "clone", "-q", "--filter=blob:none", "--no-checkout", "https://github.com/Numa1997/SiteTest.git", src)
sh("git", "-C", src, "sparse-checkout", "set", "tools/kaggle/double-pendulum")
sh("git", "-C", src, "checkout", "-q", COMMIT)
p = subprocess.run([sys.executable, f"{src}/tools/kaggle/double-pendulum/dp_gpu.py", "/kaggle/working/out"] + (["--smoke"] if SMOKE else []))
sh("rm", "-rf", src)
if p.returncode: raise SystemExit(f"the model ended with status {p.returncode}")

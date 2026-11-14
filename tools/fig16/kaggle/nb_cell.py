# Fig. 16 on Kaggle's GPU: Fig. 12's pint (stout_jax.py, unchanged) on the four-wheel cart with its control system (cart4.py).
# Code from github.com/Numa1997/SiteTest at commit __COMMIT__, laid out as in the repository under /tmp/repo.
import subprocess, sys, os, json, re, urllib.request, runpy
print(subprocess.run(["nvidia-smi", "--query-gpu=name,memory.total", "--format=csv,noheader"], capture_output=True, text=True).stdout)
chk = subprocess.run([sys.executable, "-c", "import jax; print(jax.devices()[0].platform, jax.__version__)"], capture_output=True, text=True)
print("preinstalled jax:", chk.stdout.strip(), chk.stderr.strip()[-300:])
if not chk.stdout.startswith("gpu"):
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", "jax[cuda12]==0.4.35"], check=True)
import jax
print("jax", jax.__version__, jax.devices())
if jax.devices()[0].platform != "gpu": raise RuntimeError("no GPU: stopping")
BASE = "https://raw.githubusercontent.com/Numa1997/SiteTest/__COMMIT__/"
ROOT = "/tmp/repo"
FILES = ["tools/fig12/kaggle/stout_jax.py", "tools/fig12/kaggle/run_b.py", "tools/fig12/glass_profile.json", "tools/fig16/slosh_model.py",
         "tools/fig16/spill.py", "tools/fig16/fit.json", "tools/fig16/validation.json", "tools/fig16/kaggle/cart4.py", "tools/fig16/kaggle/modal4.py",
         "tools/fig16/kaggle/run16.py"]
for f in FILES:
    p = os.path.join(ROOT, f); os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "wb").write(urllib.request.urlopen(BASE + f).read())
js = urllib.request.urlopen(BASE + "public/scripts/guinness-glass.js").read().decode()
R = json.loads(re.search(r"R:\s*(\[[^\]]*\])", js).group(1)); json.dump({"R": R}, open("/tmp/glass.json", "w"))
os.environ["GLASS_JSON"] = "/tmp/glass.json"; os.environ["BUDGET_S"] = "__BUDGET__"
if "__CODECHECK__" == "1": os.environ["CODECHECK"] = "1"
for d in ("tools/fig16/kaggle", "tools/fig16", "tools/fig12/kaggle"): sys.path.insert(0, os.path.join(ROOT, d))
runpy.run_path(os.path.join(ROOT, "tools/fig16/kaggle/run16.py"), run_name="__main__")

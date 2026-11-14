# Fig. 12 in JAX on Kaggle's GPU: the full model (stout 2.06 mPa s, glass boundary layer, surface skin, head of foam with the full
# Tcholakova flow law and, from run 8, its mass), the surface read from the level set with the derived radius 0.505 dx, and a guard
# that stops the session if the pint at rest is not flat and full (run_b.py, task "rest"). The task set is chosen by RUNSET.
# Code from github.com/Numa1997/SiteTest at commit __COMMIT__, tools/fig12/kaggle/.
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
D = "/tmp/fig12"; os.makedirs(D, exist_ok=True)
for f in ["stout_jax.py", "run_b.py"]:
    open(os.path.join(D, f), "wb").write(urllib.request.urlopen(BASE + "tools/fig12/kaggle/" + f).read())
js = urllib.request.urlopen(BASE + "public/scripts/guinness-glass.js").read().decode()
R = json.loads(re.search(r"R:\s*(\[[^\]]*\])", js).group(1)); json.dump({"R": R}, open(os.path.join(D, "glass.json"), "w"))
os.environ["GLASS_JSON"] = os.path.join(D, "glass.json"); os.environ["BUDGET_S"] = "__BUDGET__"
os.environ["RUNSET"] = "__RUNSET__"   # "" run 6's set; "control" run 7's; "run8" every ride the page plays, the head with its mass; "run10" run 8's controlled rides with beta corrected for the head
sys.path.insert(0, D)
runpy.run_path(os.path.join(D, "run_b.py"), run_name="__main__")

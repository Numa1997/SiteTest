# Fig. 12 in JAX on Kaggle's GPU, second run: the full model (stout 2.06 mPa s, glass boundary layer, surface skin, head of foam).
# Code from github.com/Numa1997/SiteTest at commit afe52121716cdff800992387132a38f9a5797396, tools/fig12/kaggle/.
import subprocess, sys, os, json, re, urllib.request, runpy
print(subprocess.run(["nvidia-smi", "--query-gpu=name,memory.total", "--format=csv,noheader"], capture_output=True, text=True).stdout)
chk = subprocess.run([sys.executable, "-c", "import jax; print(jax.devices()[0].platform, jax.__version__)"], capture_output=True, text=True)
print("preinstalled jax:", chk.stdout.strip(), chk.stderr.strip()[-300:])
if not chk.stdout.startswith("gpu"):
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", "jax[cuda12]==0.4.35"], check=True)
import jax
print("jax", jax.__version__, jax.devices())
if jax.devices()[0].platform != "gpu": raise RuntimeError("no GPU: stopping")
BASE = "https://raw.githubusercontent.com/Numa1997/SiteTest/afe52121716cdff800992387132a38f9a5797396/"
D = "/tmp/fig12"; os.makedirs(D, exist_ok=True)
for f in ["stout_jax.py", "run_b.py"]:
    open(os.path.join(D, f), "wb").write(urllib.request.urlopen(BASE + "tools/fig12/kaggle/" + f).read())
js = urllib.request.urlopen(BASE + "public/scripts/guinness-glass.js").read().decode()
R = json.loads(re.search(r"R:\s*(\[[^\]]*\])", js).group(1)); json.dump({"R": R}, open(os.path.join(D, "glass.json"), "w"))
os.environ["GLASS_JSON"] = os.path.join(D, "glass.json"); os.environ["BUDGET_S"] = "1080"
sys.path.insert(0, D)
runpy.run_path(os.path.join(D, "run_b.py"), run_name="__main__")

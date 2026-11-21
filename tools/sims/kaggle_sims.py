# Kaggle notebook "phyein-usul-simulations" (one notebook for every simulation of the site; one version per run).
# It fetches this repository at a pinned commit, runs the simulation's reference model, and writes its data under
# /kaggle/working/<YYYY-MM-DD>/<sim>/, the date of generation (docs/kaggle-pipeline.md, "Storage").
# CPU only: these models are small, so no GPU quota is spent.
JOB = "barton"                      # which simulation to compute; one model file per simulation in tools/sims/
COMMIT = "__COMMIT__"               # the commit of Numa1997/SiteTest whose tools/sims/ code is run
import subprocess, sys, os, json, time, datetime, hashlib, platform
T0 = time.time()
day = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
OUT = f"/kaggle/working/{day}/{JOB}"; os.makedirs(OUT, exist_ok=True)
print(platform.platform(), sys.version.split()[0], os.cpu_count(), "CPUs")
src = "/kaggle/working/src"
subprocess.run(["git", "clone", "-q", "--filter=blob:none", "--no-checkout", "https://github.com/Numa1997/SiteTest.git", src], check=True)
subprocess.run(["git", "-C", src, "sparse-checkout", "set", "tools/sims"], check=True)
subprocess.run(["git", "-C", src, "checkout", "-q", COMMIT], check=True)
sys.path.insert(0, f"{src}/tools/sims")
import numpy, scipy; print("numpy", numpy.__version__, "scipy", scipy.__version__)
mod = __import__(JOB)
hdr = mod.run(OUT)
files = {}
for f in sorted(os.listdir(OUT)):
    b = open(os.path.join(OUT, f), "rb").read(); files[f] = dict(bytes=len(b), sha256=hashlib.sha256(b).hexdigest())
index = dict(project="sims", job=JOB, date=day, source=dict(repo="Numa1997/SiteTest", commit=COMMIT, path=f"tools/sims/{JOB}.py"),
             machine=dict(platform=platform.platform(), cpus=os.cpu_count(), python=sys.version.split()[0], numpy=numpy.__version__, scipy=scipy.__version__),
             files=files, wall_s=time.time() - T0)
json.dump(index, open(f"{OUT}/index-{JOB}.json", "w"), indent=1)
print(json.dumps(index, indent=1))
subprocess.run(["rm", "-rf", src])

# Kaggle notebook "phyein-usul-simulations" (one notebook for every simulation of the site; one version per run or per shard).
# It fetches this repository at a pinned commit, runs the simulation's reference model, and writes its data under
# <working folder>/<YYYY-MM-DD>/<sim>/ (a sharded run: .../<sim>/shard-<i>-of-<n>/), with index-<sim>.json listing every file's
# size and SHA-256, so the engine (tools/sims/pipeline.py) can check what it downloads (docs/kaggle-sims.md).
# The placeholders below are filled by pipeline.py for each push.
JOB = "barton"                      # which simulation to compute; one model file per simulation in tools/sims/
COMMIT = "__COMMIT__"               # the commit of Numa1997/SiteTest whose tools/sims/ code is run
GPU = False                         # True: the registry asked for a GPU; the run stops at once if none is visible
SHARD = 1                           # this version computes part SHARD of SHARDS of the model's parameter grid
SHARDS = 1
FORMAT = 1                          # the data format version of the model's files (registry "format")
import subprocess, sys, os, json, time, datetime, hashlib, platform, shutil
T0 = time.time()

def gpu_name():
    try:
        r = subprocess.run(["nvidia-smi", "--query-gpu=name", "--format=csv,noheader"], capture_output=True, text=True, timeout=60)
        return r.stdout.strip().splitlines()[0].strip() if r.returncode == 0 and r.stdout.strip() else None
    except Exception:
        return None

CARD = gpu_name()
# a GPU model must never quietly run on the CPU: it would take many times longer and its benchmark would be wrong
if GPU and not CARD: sys.exit("GPU = True, but no GPU is visible (nvidia-smi failed): stopping before any computation")
WORK = os.environ.get("KAGGLE_WORKING_DIR", "/kaggle/working")
REPO = os.environ.get("SIMS_REPO_URL", "https://github.com/Numa1997/SiteTest.git")
day = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
OUT = f"{WORK}/{day}/{JOB}" + (f"/shard-{SHARD}-of-{SHARDS}" if SHARDS > 1 else ""); os.makedirs(OUT, exist_ok=True)
print(platform.platform(), sys.version.split()[0], os.cpu_count(), "CPUs,", CARD or "no GPU")
src = f"{WORK}/src"
shutil.rmtree(src, ignore_errors=True)
subprocess.run(["git", "clone", "-q", "--filter=blob:none", "--no-checkout", REPO, src], check=True)
subprocess.run(["git", "-C", src, "sparse-checkout", "set", "tools/sims"], check=True)
subprocess.run(["git", "-C", src, "checkout", "-q", COMMIT], check=True)
sys.path.insert(0, f"{src}/tools/sims")

def version_of(name):
    try: return __import__(name).__version__
    except Exception: return None

libs = dict(python=sys.version.split()[0], numpy=version_of("numpy"), scipy=version_of("scipy"))
try:
    import jax
    libs["jax"] = jax.__version__; libs["jax_devices"] = [str(d) for d in jax.devices()]
except Exception:
    pass
print(json.dumps(libs))
mod = __import__(JOB)
hdr = (mod.run(OUT, shard=SHARD, shards=SHARDS) if SHARDS > 1 else mod.run(OUT)) or {}
hdr = hdr if isinstance(hdr, dict) else {}
files = {}
for f in sorted(os.listdir(OUT)):
    p = os.path.join(OUT, f)
    if not os.path.isfile(p) or f == f"index-{JOB}.json": continue
    h = hashlib.sha256(); n = 0
    with open(p, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 24), b""): h.update(chunk); n += len(chunk)
    files[f] = dict(bytes=n, sha256=h.hexdigest())
index = dict(project="sims", job=JOB, date=day, format=FORMAT, shard=SHARD, shards=SHARDS, grid_part=hdr.get("grid_part"),
             checks_passed=hdr.get("checks_passed"), card=CARD or "cpu", libraries=libs,
             source=dict(repo="Numa1997/SiteTest", commit=COMMIT, path=f"tools/sims/{JOB}.py"),
             machine=dict(platform=platform.platform(), cpus=os.cpu_count(), python=libs["python"], numpy=libs["numpy"], scipy=libs["scipy"]),
             files=files, wall_s=time.time() - T0)
json.dump(index, open(f"{OUT}/index-{JOB}.json", "w"), indent=1)
print(json.dumps(index, indent=1))
shutil.rmtree(src, ignore_errors=True)

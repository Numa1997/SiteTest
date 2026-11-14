# Swing-up of a cart pendulum on the Kaggle GPU (JAX): 64 lengths x 64 random starts x 3000 Adam steps, 32-bit.
# Script version of cases/jax/swingup/kaggle_swingup.ipynb; the code is cloned from phyein-sim at a pinned commit.
REF = "3585fda3569cc8c98e1275d81dbb5ee231627b2e"
LENGTHS, SEEDS, ITERS, X64 = 64, 64, 3000, "0"
import subprocess, sys, os, time, json
print(subprocess.run(["nvidia-smi", "-L"], capture_output=True, text=True).stdout)
probe = lambda: subprocess.run([sys.executable, "-c", "import jax; print(jax.default_backend(), jax.__version__)"], capture_output=True, text=True).stdout.split()
backend, ver = probe(); print("preinstalled jax:", backend, ver)
if backend != "gpu":
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", f"jax[cuda12]=={ver}"], check=True)
    backend, ver = probe(); print("after installing jax[cuda12]:", backend, ver)
assert backend == "gpu", "No GPU visible to JAX: stopping before any GPU time is wasted"
R = "/kaggle/tmp/phyein-sim"
subprocess.run(f"rm -rf {R} && git clone -q https://github.com/numa1997/phyein-sim {R} && cd {R} && git checkout -q {REF}", shell=True, check=True)
S = f"{R}/cases/jax/swingup/swingup.py"
def run(L, Sd, I, out):
    env = dict(os.environ, LENGTHS=str(L), SEEDS=str(Sd), ITERS=str(I), X64=X64, OUT=out)
    t = time.time(); r = subprocess.run([sys.executable, S], env=env, capture_output=True, text=True)
    print(r.stdout[-2500:], r.stderr[-1500:] if r.returncode else ""); print("wall", round(time.time() - t, 1), "s", flush=True); r.check_returncode()
run(4, 4, 200, "/kaggle/working/smoke")
run(LENGTHS, SEEDS, ITERS, "/kaggle/working/full")
print(json.dumps(json.load(open("/kaggle/working/full/timing.json")), indent=1))

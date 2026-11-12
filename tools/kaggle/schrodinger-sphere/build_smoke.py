"""Writes smoke.ipynb, the Kaggle test notebook: GPU check, timing of one split-step, accuracy checks, 8 runs, the panel.
Usage: python3 build_smoke.py <commit>  (the notebook fetches solver.py, pack.py, panel_template.html at that commit)."""
import json
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
COMMIT = sys.argv[1] if len(sys.argv) > 1 else "main"
BASE = f"https://raw.githubusercontent.com/Numa1997/SiteTest/{COMMIT}/tools/kaggle/schrodinger-sphere/"
md0 = """# Schrödinger smoke test: a wave packet meets a sphere (GPU, JAX)

Short test run before the big sweep. It (1) checks the GPU, (2) times one split-step of the 3D time-dependent Schrödinger equation on 128³ and 256³ cells in 32-bit and 64-bit, (3) checks accuracy (32-bit vs 64-bit, Δt vs Δt/2), (4) computes 7 runs and writes the panel `schrodinger_sphere.html` (shown under the last cell). Units ħ = m = 1."""
c1 = r'''import subprocess, sys, time, json, os
T0 = time.time()
LOG = open("/kaggle/working/progress.log", "a")
def say(*a):
    s = f"[{time.time()-T0:7.1f} s] " + " ".join(str(x) for x in a); print(s, flush=True); LOG.write(s + "\n"); LOG.flush()
print(subprocess.run(["nvidia-smi", "--query-gpu=name,memory.total,driver_version", "--format=csv"], capture_output=True, text=True).stdout)
def backend():  # ask a separate Python process, so this process imports jax only once
    r = subprocess.run([sys.executable, "-c", "import jax; print(jax.default_backend())"], capture_output=True, text=True)
    return r.stdout.strip().splitlines()[-1] if r.stdout.strip() else "none: " + r.stderr[-300:]
b = backend(); say("jax backend before install:", b)
if b != "gpu":
    say("installing jax[cuda12]")
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", "-U", "jax[cuda12]"], check=True)
    say("jax backend after install:", backend())
import jax
jax.config.update("jax_enable_x64", True)
DEV = jax.devices()
say("devices:", DEV, "jax", jax.__version__)
assert any(d.platform == "gpu" for d in DEV), "NO GPU: stopping so no quota is wasted on a CPU fallback"
'''
c2 = f'''# the solver, the packer and the panel, fetched from the website's repository at commit {COMMIT}
import urllib.request
BASE = "{BASE}"
for f in ("solver.py", "pack.py", "panel_template.html"):
    urllib.request.urlretrieve(BASE + f, f)
exec(open("solver.py").read()); exec(open("pack.py").read())
TEMPLATE = open("panel_template.html").read()
say("code from", BASE)
'''
c3 = r'''# ---- benchmark: one split-step on N^3 cells ----
def bench(N, dtype, steps=40):
    g = setup(N, 64.0, dtype); rdt = jnp.float32 if dtype == jnp.complex64 else jnp.float64
    kin = jnp.asarray(np.exp(-0.5j * g["K2"] * 0.01), dtype); hv = jnp.ones((N, N, N), dtype); mk = jnp.asarray(g["mask"], rdt)
    p = jnp.asarray(np.random.default_rng(0).standard_normal((N, N, N)), dtype)
    f = jax.jit(lambda p: jax.lax.fori_loop(0, steps, lambda i, p: mk * (hv * jnp.fft.ifftn(kin * jnp.fft.fftn(hv * p))), p))
    f(p).block_until_ready(); t = time.time(); f(p).block_until_ready(); dt = (time.time() - t) / steps
    return dict(N=N, dtype=str(jnp.dtype(dtype)), ms_per_step=round(dt * 1e3, 3), ns_per_cell_step=round(dt / N**3 * 1e9, 3))
BENCH = []
for N in (128, 256):
    for dt_ in (jnp.complex64, jnp.complex128):
        BENCH.append(bench(N, dt_)); say("bench", BENCH[-1])
'''
c4 = r'''# ---- accuracy: the same barrier run in 32-bit, 64-bit, and 32-bit with half the time step ----
ACC = {}
for name, dtype, dt in (("c64 dt=0.01", jnp.complex64, 0.01), ("c128 dt=0.01", jnp.complex128, 0.01), ("c64 dt=0.005", jnp.complex64, 0.005)):
    r = run(setup(128, 64.0, dtype), E=2.0, V0=3.0, R=4.0, dt=dt, nframes=12)
    t, n, b, a, sy = r["curves"][-1]; ACC[name] = dict(norm=n, behind=b, ahead=a, wall=round(r["wall"], 2), steps=r["steps"])
    say("accuracy", name, ACC[name])
'''
c5 = r'''# ---- 7 demo runs at 128^3 (and one at 256^3 for timing), then the panel ----
N, L, DT, OUT = 128, 64.0, 0.01, 128
Es = [1.0, 2.0, 3.0]; Vs = [0.0, 1.0, 2.0, 3.0, 4.0, 6.0]; Rs = [3.0, 4.0, 5.0]
g = setup(N, L); RUNS = []
for E, V, R in [(2.0, v, 4.0) for v in Vs] + [(3.0, 3.0, 4.0)]:
    RUNS.append(run(g, E=E, V0=V, R=R, dt=DT, nframes=48, out=OUT))
    say(f"run E={E} V0={V} R={R}: {RUNS[-1]['steps']} steps in {RUNS[-1]['wall']:.1f} s, ahead {RUNS[-1]['curves'][-1][3]:.3f}")
r256 = run(setup(256, L), E=2.0, V0=3.0, R=4.0, dt=DT, nframes=48, out=128)
say(f"256^3 run: {r256['steps']} steps in {r256['wall']:.1f} s, ahead {r256['curves'][-1][3]:.4f} (128^3: {RUNS[3]['curves'][-1][3]:.4f})")
name = jax.devices()[0].device_kind
page = build_page(TEMPLATE, RUNS, Es, Vs, Rs, N, L, DT, OUT, 3.0, f"Kaggle {name}", dict(sE=1, sV=3, sR=1))
open("/kaggle/working/schrodinger_sphere.html", "w").write(page)
json.dump(dict(device=name, bench=BENCH, accuracy=ACC, runs=[dict(E=r["E"], V0=r["V0"], R=r["R"], steps=r["steps"], wall=r["wall"]) for r in RUNS],
               run256=dict(steps=r256["steps"], wall=r256["wall"], ahead=float(r256["curves"][-1][3])), total_s=round(time.time() - T0, 1)),
          open("/kaggle/working/timing.json", "w"), indent=1)
say(f"panel {len(page)/1e6:.1f} MB written; all done in {time.time()-T0:.0f} s")
import html as _h
from IPython.display import HTML, display
display(HTML(f'<iframe srcdoc="{_h.escape(page)}" style="width:100%;height:1250px;border:0"></iframe>'))
'''
cells = [dict(cell_type="markdown", metadata={}, source=md0, id="s0")]
for n, c in enumerate([c1, c2, c3, c4, c5]):
    cells.append(dict(cell_type="code", execution_count=None, metadata={}, outputs=[], source=c, id=f"s{n+1}"))
nb = dict(cells=cells, metadata=dict(kernelspec=dict(display_name="Python 3", language="python", name="python3"), language_info=dict(name="python")), nbformat=4, nbformat_minor=5)
open(os.path.join(HERE, "smoke.ipynb"), "w").write(json.dumps(nb))
print("notebook bytes", len(json.dumps(nb)))

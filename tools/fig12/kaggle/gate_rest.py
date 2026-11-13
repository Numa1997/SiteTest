# Fig. 12 in JAX: the free check before any GPU launch (notes/fig12/handoff-jax/02-launch-gates.md, gate B).
# A pint at rest for one simulated second on a coarse grid, with the full model, and the numbers that would have caught
# every coding bug of run 2. It prints PASS or FAIL per check and exits with status 1 if any fails.
# WRITTEN 13 Nov 2026 AND NOT YET EXECUTED: the first run of this file is itself to be read line by line.
# Run (CPU, about a minute):  GLASS_JSON=<glass.json> python3 tools/fig12/kaggle/gate_rest.py [dx in m, default 0.004]
# On Kaggle it runs as the first step of run_b.py (GATE=1) and stops the session at once if it fails.
import json, os, sys
import numpy as np
import jax, jax.numpy as jnp
from stout_jax import Geometry, Stout, make_advance, F64, HEAD0


def gate(R, dx=0.004, seconds=1.0, log=print):
    G = Geometry(R, 0.0005, 0.125, dx); S = Stout(G, model="full")
    s = S.init_state(); t = jnp.zeros((), F64)
    adv = make_advance(S, "free", push=(0.3, 0.0, 0.146)); obs = jax.jit(S.observe)
    ex = dict(vmax=jnp.zeros((), F64), t_end=jnp.zeros((), F64))
    o0 = obs(s); head0 = float(jnp.sum(o0["hf"])) * dx * dx; nsel = 0
    for f in range(1, int(round(seconds * 30)) + 1):
        ex = dict(ex, t_end=jnp.asarray(f / 30, F64)); s, t, ex, st = adv(s, t, ex); nsel = max(nsel, int(st["nselmax"]))
    o = obs(s); H = np.asarray(o["H"]); hf = np.asarray(o["hf"])
    c = G.x0 + (np.arange(G.n) + 0.5) * dx; X, Y = np.meshgrid(c, c, indexing="ij"); r = np.hypot(X, Y)
    inside = r < G.Rfill - 1.0 * dx
    # a column lies wholly outside the glass when even its nearest corner is beyond the widest radius; a column whose centre is
    # outside but whose inner part is inside the glass rightly holds stout (13 Nov 2026: the count read-out reads such columns)
    outside = r - dx / np.sqrt(2) > float(G.R.max())
    dev = np.abs(H[inside] - 0.125)
    checks = [
        ("every column well inside the glass holds a surface value", bool(np.isfinite(H[inside]).all()), f"{int(np.isfinite(H[inside]).sum())} of {int(inside.sum())}"),
        # at dx = 4 mm the fill (125 mm) lies a quarter of a cell from the nearest cell centre, so heights rounded to cell centres fail this
        ("the surface at rest is within 0.2 cells of the fill", bool(np.nanmax(dev) < 0.2 * dx), f"largest deviation {np.nanmax(dev) * 1e3:.3f} mm, cell {dx * 1e3:.1f} mm"),
        ("no column outside the glass holds a value", bool(not np.isfinite(H[outside]).any()), f"{int(np.isfinite(H[outside]).sum())} columns"),
        ("the head has lost nothing at rest", bool(abs(float(hf.sum()) * dx * dx - head0) < 1e-9 and float(o["foam_spill"]) == 0.0), f"{head0 * 1e6:.2f} mL before, {float(hf.sum()) * dx * dx * 1e6:.2f} mL after, spilled {float(o['foam_spill']) * 1e6:.3f} mL"),
        ("the head is HEAD0 thick where there is stout", bool(abs(float(hf[inside].max()) - HEAD0) < 1e-6), f"{float(hf[inside].max()) * 1e3:.2f} mm"),
        ("no stout has left the glass", bool(int(o["nact"]) == S.N and int(o["nfly"]) == 0), f"{S.N - int(o['nact'])} particles"),
        ("the stout is still", bool(float(o["KE"]) < 1e-5), f"kinetic energy {float(o['KE']):.2e} J"),
        ("the near-surface list did not overflow", bool(nsel < S.K), f"{nsel} of {S.K}"),
        ("nothing is NaN", bool(np.isfinite(np.asarray(s["xp"])).all() and np.isfinite(np.asarray(s["vp"])).all()), ""),
    ]
    ok = True
    for name, passed, detail in checks:
        log(f"{'PASS' if passed else 'FAIL'}  {name}  ({detail})"); ok = ok and passed
    return ok


if __name__ == "__main__":
    R = json.load(open(os.environ["GLASS_JSON"]))["R"]
    good = gate(R, float(sys.argv[1]) if len(sys.argv) > 1 else 0.004)
    print("GATE B:", "PASS" if good else "FAIL"); sys.exit(0 if good else 1)

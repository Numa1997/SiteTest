"""The JAX port of the site's Cart (stout_jax.Cart) on the same road, load and probe signal as cart_js.cjs, and the
comparison at every fluid step (2 ms) over 3 s on the kerb: position, speed, body height, current, its command, the active
force, and for "slosh" and "joint" the filter's estimate of the swing (the JS runs its filter for every controller, the port
only where it is used). python3 cart_jax.py  (runs the JS reference with node for each controller first).
Run 13 November 2026: speed, preview, skyhook agree to 1e-13; slosh and joint to 3e-8 A in the current (the JS integrates the
Riccati flow to 1e-7; the port solves it exactly). Output: notes/fig12/handoff-jax/portcheck.txt."""
import json, math, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
import numpy as np, jax, jax.numpy as jnp
from stout_jax import Cart, CART_COMMON, road_table

xi = 1.8412; h0 = 0.125; Rs = 0.0391; th = math.tanh(xi * h0 / Rs)
C = dict(bumps=[{"x": 1.5, "h": 0.030, "L": 0.12}], v0=1.5, ml=0.4545, x0=0.5, xmax=8.0, h=0.002, nsub=20, nsteps=1500,
         plant=dict(w=2 * math.pi * 3.278, zeta=0.467, beta=2 * xi * th / (xi * xi - 1)),
         probe=dict(A=0.004, w=2 * math.pi * 3.278, d=0.5),
         cart={k: v for k, v in CART_COMMON.items() if k in ("Mb", "mw", "Rw", "Iw", "k", "c", "kt", "ct", "cx", "Ls", "Ngear", "Km", "Ra", "Jm", "Vmax", "Imax", "tauI", "Ts", "Kp", "Ki", "csky", "Umax", "tauU", "mu")})
json.dump(C, open(os.path.join(HERE, "case.json"), "w"))
road = road_table({"kind": "bumps", "bumps": C["bumps"]}, Rw=C["cart"]["Rw"], xmin=-1.0, xmax=C["xmax"])
yq = lambda t: C["probe"]["A"] * math.sin(C["probe"]["w"] * t) * math.exp(-C["probe"]["d"] * t)
worst = {}
for ctrl, susp in (("speed", 0), ("preview", 0), ("speed", 1), ("slosh", 0), ("joint", 0)):
    out = os.path.join(HERE, f"js_{ctrl}_{susp}.json")
    subprocess.run(["node", os.path.join(HERE, "cart_js.cjs"), ctrl, str(susp), out], check=True)
    J = json.load(open(out))
    cart = Cart(dict(CART_COMMON, v0=C["v0"], ctrl=ctrl, susp=susp, plant=C["plant"]), road)
    c = cart.init(C["x0"], C["ml"])
    step = jax.jit(lambda c, y, fr: jax.lax.fori_loop(0, C["nsub"], lambda _, cc: cart.step(cc, C["h"] / C["nsub"], 0.0, 0.0),
                                                      dict(c, py=y, pfresh=jnp.where(fr, 1.0, c["pfresh"]))))
    rec = {k: [] for k in ("x", "vx", "zb", "zw", "i", "icmd", "us", "xi", "q")}; t = 0.0
    for n in range(C["nsteps"]):
        c = step(c, yq(t) if n > 0 else 0.0, n > 0); t += C["h"]
        for k in rec: rec[k].append(float(c["oxh"][1]) if k == "q" else float(c[k]))
    line = f"{ctrl:8s} susp {susp}:"
    for k, sc in (("x", 1e3), ("vx", 1e3), ("zb", 1e3), ("i", 1.0), ("icmd", 1.0), ("us", 1.0)) + ((("q", 1e3),) if ctrl in ("slosh", "joint") else ()):
        a, b = np.array(rec[k]), np.array(J[k]); d = np.max(np.abs(a - b)); r = np.max(np.abs(b)) + 1e-30
        line += f" {k} {d * sc:.2e} ({d / r:.1e})"; worst[(ctrl, susp, k)] = d / r
    if ctrl in ("slosh", "joint"):
        line += f" | K js {np.round(J['K'], 4).tolist()} jax {np.round(np.asarray(cart.K), 4).tolist()}"
        if ctrl == "joint": line += f" Ks js {np.round(J['Ks'], 3).tolist()} jax {np.round(np.asarray(cart.Ks), 3).tolist()}"
    print(line, flush=True)
    print(f"   largest |i| {max(abs(v) for v in rec['i']):.3f} A, |us| {max(abs(v) for v in rec['us']):.2f} N; JS {max(abs(v) for v in J['i']):.3f} A, {max(abs(v) for v in J['us']):.2f} N")
print("largest relative difference over all:", max(worst.values()))

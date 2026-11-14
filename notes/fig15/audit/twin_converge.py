"""Fig. 15 grid audit, part 2: the twin with the cell-averaged potential (each grid cell holds the mean of V over its width)
converging to the exact continuum answer as the spacing shrinks; and the position of the V0 = 3 resonance (exact 0.877) found from
a sweep of long packets. Uses twin_sources.twin. Writes twin_converge.json."""
import sys, os, json, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import twin_sources as ts
cases = [dict(shape="flat", N=2, V0=3.0, D=1.0, P=2.5, R=0.0, E=0.7827, bias=0.0, sx=12.0, sp=3.0, Nx=512),
         dict(shape="flat", N=2, V0=2.0, D=1.0, P=2.5, R=0.0, E=0.821, bias=0.0, sx=12.0, sp=3.0, Nx=512),
         dict(shape="flat", N=2, V0=2.0, D=1.0, P=2.5, R=0.0, E=0.75, bias=0.0, sx=3.0, sp=3.0, Nx=192)]
out = dict(conv=[], peak={})
for sp in cases:
    ex = ts.exact_bar(sp); row = dict(spec=sp, exact=ex, T={})
    for dx in (0.5, 0.25, 0.125, 0.0625, 0.03125):
        for dt in ((0.01, 0.0025) if dx <= 0.0625 else (0.01,)):
            T = ts.twin(sp, dx=dx, dt=dt, vmode="cell", Nx_stored=sp["Nx"]); row["T"][f"{dx}|{dt}"] = T
            print(f'V0={sp["V0"]} sx={sp["sx"]} E={sp["E"]} dx={dx} dt={dt}  T={T:.5f}  exact={ex:.5f}  diff={T-ex:+.5f}', flush=True)
    out["conv"].append(row)
# resonance position, V0 = 3: long packets (sx = 24 for a narrower energy spread) on a sweep, peak by a parabola through the top 3
base = dict(shape="flat", N=2, V0=3.0, D=1.0, P=2.5, R=0.0, bias=0.0, sx=24.0, sp=3.0, Nx=1024)
Es = np.round(np.arange(0.80, 0.925, 0.0075), 4)
def peak(Ts):
    i = int(np.argmax(Ts)); i = min(max(i, 1), len(Ts) - 2); y0, y1, y2 = Ts[i - 1:i + 2]
    return float(Es[i] + 0.5 * (y0 - y2) / (y0 - 2 * y1 + y2) * (Es[1] - Es[0]))
for name, kw in [("exact", None), ("stored dx0.5 step", dict(dx=0.5)), ("dt0.0025", dict(dx=0.5, dt=0.0025)), ("box x2", dict(dx=0.5, Lmul=2.0)),
                 ("cell dx0.25", dict(dx=0.25, vmode="cell")), ("cell dx0.125", dict(dx=0.125, vmode="cell")), ("cell dx0.0625", dict(dx=0.0625, vmode="cell"))]:
    Ts = [ts.exact_bar(dict(base, E=float(e))) if kw is None else ts.twin(dict(base, E=float(e)), Nx_stored=base["Nx"], **kw) for e in Es]
    out["peak"][name] = dict(E=Es.tolist(), T=Ts, peak=peak(np.array(Ts)))
    print(f"resonance V0=3 {name:20s} peak E = {out['peak'][name]['peak']:.4f}", flush=True)
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "twin_converge.json"), "w"), indent=1)

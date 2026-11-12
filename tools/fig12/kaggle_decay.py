"""Fig. 12 computed on Kaggle: how fast the stored swing dies, and how far the wall lean drifts.

Reads public/data/fig12/<date>/rides.json (default: the newest date folder) and prints, for each ride:
  - the first sloshing mode q(t), the height of mode 1 at the wall, in mm: the cos(theta) part of ring 13 of the stored
    surface (r = 31.8 mm, the outermost ring the notebook built from particles; rings 14-16 are extended from it), scaled
    to the wall by the mode's shape, J1(xi) / J1(xi r/R) (Fig. 12 note, section 4.5);
  - its free decay after the last bump: a direct least-squares fit of q = A exp(-t/tau) cos(w t + phi) + c + s t over 3 s
    from 2 frames after the cart leaves the bump (x > 9.15 m); tau and w by a grid search, the rest linear. The damping
    ratio is zeta = 1/(w tau). --selftest fits made-up decays of known tau first;
  - the drift: the stored lean (front minus back wall) and 2q, averaged over the last 5 s, at steady speed on flat road.
With --modal it also fits fig12_cart_damping.json in the temporary folder (written by node tools/fig12/cart_damping.cjs): the same cart and road with
the site's reduced model, to show how much damping the cart alone gives.

Run: python3 tools/fig12/kaggle_decay.py [--selftest] [--modal] [path/to/rides.json]   (numpy only)
"""
import base64, glob, json, math, os, sys, tempfile, zlib
import numpy as np

F11, XI = 3.421, 1.841184       # Hz; first zero of J1' (note, eq. 16)
RING = 13


def j1(x):
    s, t = 0.0, x / 2
    for k in range(60):
        s += t; t *= -(x * x / 4) / ((k + 1) * (k + 2))
    return s


def fit_decay(t, q):
    """q = exp(-t/tau) (a cos wt + b sin wt) + c + s t: linear in a, b, c, s for given tau, w; grid search, then refine."""
    def best(taus, ws):
        top = (np.inf, None)
        for tau in taus:
            e = np.exp(-t / tau)
            for w in ws:
                M = np.stack([e * np.cos(w * t), e * np.sin(w * t), np.ones_like(t), t], 1)
                coef, res, *_ = np.linalg.lstsq(M, q, rcond=None)
                r = float(np.sum((M @ coef - q) ** 2))
                if r < top[0]: top = (r, (tau, w, coef))
        return top[1]
    tau, w, c = best(np.geomspace(0.05, 300, 240), 2 * np.pi * np.arange(2.5, 4.5001, 0.01))
    tau, w, c = best(tau * np.geomspace(0.9, 1.1, 81), w + 2 * np.pi * np.arange(-0.01, 0.0101, 0.0005))
    return dict(tau=tau, f=w / 2 / np.pi, zeta=1 / (w * tau), A=float(math.hypot(c[0], c[1])))


def free_part(t, q, x):
    i0 = int(np.argmax(x > 9.15)) + 2
    seg = slice(i0, i0 + 90)
    return t[seg] - t[seg][0], q[seg]


def main(path, selftest, modal):
    if selftest:
        rng = np.random.default_rng(1); t = np.arange(0, 3, 1 / 30)
        for tau in (0.32, 0.76, 8.7, 12.9):
            q = 2 * np.exp(-t / tau) * np.cos(2 * np.pi * 3.42 * t + 0.4) + 0.3 + 0.05 * t + rng.normal(0, 0.01, len(t))
            print(f"selftest: made-up tau {tau} s -> fitted {fit_decay(t, q)['tau']:.3f} s")
    D = json.load(open(path))
    nr, nth, fps = D["nr"], D["nth"], D["fps"]
    th = 2 * np.pi * np.arange(nth) / nth
    scale = j1(XI) / j1(XI * RING / nr)
    print(f"{path}\nq from ring {RING} of {nr}, scaled to the wall by J1(xi)/J1(xi {RING}/{nr}) = {scale:.4f}")
    for r in sorted(D["rides"], key=lambda r: r["v0"]):
        b = np.frombuffer(zlib.decompress(base64.b64decode(r["frames"])), np.uint8).reshape(r["n"], nr + 1, nth).astype(float)
        h = (D["fill"] + (b - 128) * D["q"]) * 1000
        q = 2 / nth * (h[:, RING, :] * np.cos(th)).sum(1) * scale
        t = np.arange(r["n"]) / fps; x = np.array(r["x"]); lean = np.array(r["lean"])
        ft = fit_decay(*free_part(t, q, x))
        last = t > t[-1] - 5
        print(f"v0 {r['v0']} m/s: after the last bump q swings {ft['A']:.2f} mm at {ft['f']:.3f} Hz, tau {ft['tau']:.3f} s, damping ratio {ft['zeta']:.4f}; "
              f"last 5 s: wall lean {lean[last].mean():.2f} mm, 2q {2 * q[last].mean():.2f} mm")
    if modal:
        mp = os.path.join(tempfile.gettempdir(), "fig12_cart_damping.json")
        M = json.load(open(mp))
        for k, v in M.items():
            ft = fit_decay(*free_part(np.array(v["t"]), np.array(v["q"]), np.array(v["x"])))
            print(f"reduced model, {k}: tau {ft['tau']:.2f} s, damping ratio {ft['zeta']:.4f} (stout's own {v['zeta_fluid']:.4f}, so the cart adds {ft['zeta'] - v['zeta_fluid']:.4f})")


if __name__ == "__main__":
    a = [x for x in sys.argv[1:] if not x.startswith("--")]
    if a: p = a[0]
    else:
        here = os.path.dirname(os.path.abspath(__file__))
        p = os.path.normpath(sorted(glob.glob(os.path.join(here, "..", "..", "public", "data", "fig12", "*", "rides.json")))[-1])
    main(p, "--selftest" in sys.argv, "--modal" in sys.argv)

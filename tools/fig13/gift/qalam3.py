"""Words written with the reed pen over a master model, one word at a time (no mirror).

Every centre-line path of the model word (skeleton.py) is smoothed and inked with a flat nib at ALPHA; paths whose extent is less
than about a nib are the model's dots, and are stamped as rhombic dots (a short press across the nib). The nib swells with the
model's own half-width so heavy and light parts keep their weight, and tapers at free ends.

    python3 tools/fig13/gift/qalam3.py MODEL.ttf OUT.png
"""
import sys, math
import numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from skeleton import paths
from qalam2 import smooth, quads, ALPHA

WORDS = ['رِيمْ', 'فَرَاشَتُكِ']


def ink(model, text, nib):
    S = []
    for p in paths(model, text):
        q, half = p['pts'], p['half']
        ext = np.ptp(q, axis=0).max(); closed = np.hypot(*(q[0] - q[-1])) < 0.25 * ext and len(q) > 12
        if closed or (ext < 0.9 * nib and np.median(half) < 0.25 * nib and len(q) > 25):   # a ring (sukun, a loop's counter): ink it round
            c = q.mean(0); r = max(0.5 * ext, 0.3 * nib); th = np.linspace(0.3, 2 * np.pi + 0.5, 50)
            if ext < 1.2 * nib:
                S.append(dict(pts=np.stack([c[0] + r * np.cos(th), c[1] + 0.9 * r * np.sin(th)], 1), k=np.full(50, 0.42)))
                continue
        if ext < 0.9 * nib and not closed:                                     # a dot (or a joint fragment): a rhombic press of the nib
            c = q.mean(0); d = 0.30 * nib * np.array([math.cos(ALPHA - math.pi / 2), math.sin(ALPHA - math.pi / 2)])
            S.append(dict(pts=np.linspace(c - d, c + d, 10), k=np.full(10, 0.7)))
            continue
        sp = smooth(q, s=len(q) * 4.0)
        for end in (0, -1):                                     # carry each end a little on along its tangent: strokes overlap at joints
            t = sp[end] - sp[3 if end == 0 else -4]; t = t / (np.hypot(*t) + 1e-9)
            ext_pts = sp[end] + np.outer(np.linspace(0.05, 0.28, 4), t) * nib
            sp = np.vstack([ext_pts[::-1], sp]) if end == 0 else np.vstack([sp, ext_pts])
        half = np.r_[np.full(4, half[0]), half, np.full(4, half[-1])]
        h = np.interp(np.linspace(0, 1, len(sp)), np.linspace(0, 1, len(half)), half)
        k = np.clip(1.15 * 2 * h / nib, 0.25, 1.15)              # the model's weight, through the pen
        S.append(dict(pts=sp, k=k))
    return S


if __name__ == '__main__':
    import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
    from matplotlib.collections import PolyCollection
    model, out = sys.argv[1], sys.argv[2]; NIB = 98.0
    fig, ax = plt.subplots(2, 2, figsize=(14, 10), dpi=110)
    for j, w in enumerate(WORDS):
        Q = [qq for st in ink(model, w, NIB) for qq in quads(st, ALPHA, NIB)]; allp = np.concatenate(Q)
        for i, (bg, c) in enumerate((('#140d10', '#e2a2aa'), ('#f5f1ea', '#7a1f2b'))):
            a = ax[i, j]; a.set_facecolor(bg); a.add_collection(PolyCollection(Q, facecolors=c, edgecolors=c, linewidths=0.5))
            a.set_xlim(allp[:, 0].min() - 100, allp[:, 0].max() + 100); a.set_ylim(allp[:, 1].min() - 100, allp[:, 1].max() + 100)
            a.set_aspect('equal'); a.set_xticks([]); a.set_yticks([])
    fig.subplots_adjust(0, 0, 1, 1, 0.02, 0.02); fig.savefig(out)

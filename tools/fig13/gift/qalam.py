"""A reed pen (qalam) and my own sketch of the name رِيمْ as a mirror composition (muthanna) that opens like a butterfly.

The pen: a flat nib of width W held at a fixed angle ALPHA. Moving its centre along a path leaves ink where the nib sweeps, so a
stroke is thick where it moves across the nib and thin where it moves along it, as with a cut reed. Each stroke may swell or
taper its nib along its length (the calligrapher's pressure and lift), given as a profile k(s), 0 <= s <= 1.

Units: the nib width W = 1 (the rhombic dot of the proportion system is about one nib square). The word is laid out on a baseline
y = 0 with the mirror axis at x = 0, the word to the right of the axis (Arabic runs right to left, so ra is outermost and the mim's
tail runs down the axis). The right half is turned by TILT about the axis foot so the wings rise; the left half is its mirror image
(x -> -x, nib angle -> 180 deg - ALPHA).

    strokes() -> list of dicts: pts (n, 2) centre line, k (n,) nib factor, alpha (rad), kind ('letter' | 'dot' | 'mark')
    python3 tools/fig13/gift/qalam.py PREVIEW.png      draws the composition
"""
import sys, math
import numpy as np

ALPHA = math.radians(62)        # nib edge angle from the horizontal (thuluth-like hold)
TILT = math.radians(0)
WEIGHT = 1.4                    # nib width relative to the letter sizes below (jali: heavy)         # the wings rise


def bez(*P, n=60):
    """Cubic Bezier chain through control points P0 P1 P2 P3 [P4 P5 P6 ...] (shared ends), sampled n per piece."""
    P = np.asarray(P, float); out = []
    for i in range(0, len(P) - 1, 3):
        a, b, c, d = P[i:i + 4]; t = np.linspace(0, 1, n)[:, None]
        seg = (1 - t) ** 3 * a + 3 * (1 - t) ** 2 * t * b + 3 * (1 - t) * t ** 2 * c + t ** 3 * d
        out.append(seg if not out else seg[1:])
    return np.vstack(out)


def prof(n, a=0.15, b=0.25, lo=0.35, hi=1.0, end=0.12):
    """Nib factor along a stroke: enter from lo to hi over the first a, hold, lift to `end` over the last b."""
    s = np.linspace(0, 1, n); k = np.full(n, hi)
    k = np.where(s < a, lo + (hi - lo) * np.sin(0.5 * np.pi * s / a), k)
    k = np.where(s > 1 - b, end + (hi - end) * np.cos(0.5 * np.pi * (s - (1 - b)) / b), k)
    return k


def right_half():
    """The word as it sits right of the axis, in nib widths. Order outward from the axis, as written right to left: ra, ya, mim."""
    S = []
    # mim (final): its head a small knot just off the axis (the nib fills its counter); its tail straight down the axis: the body
    p = bez((3.0, 0.15), (2.4, 0.15), (1.9, 0.95), (1.25, 0.9), (0.6, 0.85), (0.55, 0.0), (1.15, -0.1),
            (1.7, -0.2), (1.55, 0.45), (0.95, 0.4), (0.55, 0.35), (0.42, -0.6), (0.4, -1.8),
            (0.38, -3.6), (0.36, -5.6), (0.18, -7.4))
    S.append(dict(pts=p, k=prof(len(p), a=0.04, b=0.42, lo=0.9, end=0.03), kind='letter'))
    # ya (initial): its tooth (a wedge head, then down), rising like a feeler, then along the line into the mim
    p = bez((4.45, 3.7), (4.3, 2.8), (3.95, 1.3), (3.6, 0.3), (3.45, 0.0), (3.2, 0.12), (3.0, 0.15))
    S.append(dict(pts=p, k=prof(len(p), a=0.10, b=0.06, lo=1.15, hi=0.85, end=0.95), kind='letter'))
    # ra, written large as a jali composition allows: the head high on the outside, a drop down, the belly swelling out,
    # then the long sweep in and down towards the body, thinning to a hair: the edge of the upper wing
    p = bez((8.3, 5.4), (8.75, 5.5), (9.2, 5.1), (9.45, 4.2), (9.9, 2.6), (10.0, 0.6), (8.9, -0.6),
            (7.7, -1.8), (6.0, -2.3), (4.4, -2.05))
    S.append(dict(pts=p, k=prof(len(p), a=0.1, b=0.38, lo=0.55, end=0.03), kind='letter'))
    # the two dots of ya: rhombic, a short press of the nib straight across its edge, below the ya, in the lower wing
    d = 0.33 * np.array([math.cos(ALPHA - math.pi / 2), math.sin(ALPHA - math.pi / 2)])
    for c in ((3.5, -3.3), (5.0, -3.75)):
        c = np.array(c); p = np.linspace(c - d, c + d, 12)
        S.append(dict(pts=p, k=np.full(len(p), 0.68), kind='dot'))
    # kasra under ra: a stroke slanting down to the left, under the belly of the ra
    p = bez((9.2, -2.2), (8.6, -2.65), (8.0, -3.05), (7.3, -3.4), n=28)
    S.append(dict(pts=p, k=prof(len(p), a=0.3, b=0.45, lo=0.5, hi=1.0, end=0.2), kind='mark'))
    # sukun over mim: a small open ring with a thin nib: with its mirror, the two eyes
    th = np.linspace(0.4, 2 * np.pi + 0.2, 44); p = np.stack([1.35 + 0.42 * np.cos(th), 1.95 + 0.38 * np.sin(th)], axis=1)
    S.append(dict(pts=p, k=np.full(len(p), 0.38), kind='mark'))
    return S


def strokes():
    out = []
    c, s = math.cos(TILT), math.sin(TILT)
    R = np.array([[c, -s], [s, c]])
    for st in right_half():
        p = st['pts'] @ R.T
        out.append(dict(pts=p, k=st['k'], alpha=ALPHA, kind=st['kind'], side=1))
    for st in list(out):
        out.append(dict(pts=st['pts'] * [-1, 1], k=st['k'], alpha=math.pi - ALPHA, kind=st['kind'], side=-1))
    return out


def quads(st):
    """The ink of one stroke as quadrilaterals between successive nib positions."""
    p, k, a = st['pts'], st['k'], st['alpha']; e = 0.5 * np.array([math.cos(a), math.sin(a)])
    A, B = p + WEIGHT * k[:, None] * e, p - WEIGHT * k[:, None] * e
    return [np.array([A[i], A[i + 1], B[i + 1], B[i]]) for i in range(len(p) - 1)]


if __name__ == '__main__':
    import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
    from matplotlib.collections import PolyCollection
    fig, axs = plt.subplots(1, 2, figsize=(14, 7), dpi=110)
    for ax, bg, ink in zip(axs, ('#140d10', '#f5f1ea'), ('#e2a2aa', '#7a1f2b')):
        ax.set_facecolor(bg)
        for st in strokes():
            ax.add_collection(PolyCollection(quads(st), facecolors=ink, edgecolors=ink, linewidths=0.6))
        ax.set_aspect('equal'); ax.set_xlim(-12.5, 12.5); ax.set_ylim(-9, 8); ax.set_xticks([]); ax.set_yticks([])
        for sp in ax.spines.values(): sp.set_visible(False)
    fig.patch.set_facecolor('#140d10'); fig.subplots_adjust(0, 0, 1, 1, 0.01)
    fig.savefig(sys.argv[1], facecolor=fig.get_facecolor())

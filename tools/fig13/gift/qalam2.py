"""رِيمْ written with the reed pen of qalam.py over a master model (mashq), then composed as a mirror (muthanna) butterfly.

Model: Amiri (Khaled Hosny, SIL OFL), a Naskh after the Bulaq press, with full vowel marks placed by HarfBuzz. Its centre lines
(skeleton.py) give each stroke's path; each path is smoothed (a smoothing spline) and inked with a flat nib held at ALPHA, so the
thick and thin come from the pen, not from the font. The pen order follows the hand: ra; kasra; ya's tooth and its join; the mim's
head and tail; the dots; the sukun.

    python3 tools/fig13/gift/qalam2.py MODEL.ttf OUT.png      model under the pen strokes, and the mirror composition
"""
import sys, math
import numpy as np
from scipy.interpolate import splprep, splev
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from skeleton import paths

ALPHA = math.radians(62)
NIB = 98.0                       # nib width in font units (the model's thickest strokes are about 90-140 wide)


def smooth(p, s=None, n=None):
    p = np.asarray(p, float)
    keep = np.r_[True, np.hypot(*np.diff(p, axis=0).T) > 1e-6]; p = p[keep]
    tck, _ = splprep([p[:, 0], p[:, 1]], s=len(p) * 6.0 if s is None else s, k=3)
    u = np.linspace(0, 1, n or max(20, len(p)))
    return np.stack(splev(u, tck), 1)


def taper(n, a=0.12, b=0.3, lo=0.5, hi=1.0, end=0.08):
    s = np.linspace(0, 1, n); k = np.full(n, hi)
    k = np.where(s < a, lo + (hi - lo) * np.sin(0.5 * np.pi * s / a), k)
    return np.where(s > 1 - b, end + (hi - end) * np.cos(0.5 * np.pi * (s - (1 - b)) / b), k)


def strokes(model):
    P = [p['pts'] for p in paths(model, 'رِيمْ')]
    S = []
    def add(p, k, kind): S.append(dict(pts=p, k=k, kind=kind))
    ra = smooth(P[9]); add(ra, taper(len(ra), a=0.08, b=0.4, lo=0.6, end=0.04), 'letter')
    kas = smooth(P[10]); add(kas, taper(len(kas), a=0.3, b=0.4, lo=0.45, hi=0.75, end=0.25), 'mark')
    join = smooth(np.vstack([P[6][::-1][:-1], P[3][::-1]]))                      # tooth top, down, and the join into the mim
    add(join, taper(len(join), a=0.15, b=0.05, lo=0.55, hi=0.8, end=0.9), 'letter')
    head = smooth(np.vstack([P[5][::-1], [[150, 100]], P[14]]), s=400)           # the mim's head: round, filled by the nib
    add(head, np.full(len(head), 1.05), 'letter')
    tail = smooth(P[1]); add(tail, taper(len(tail), a=0.05, b=0.45, lo=0.95, hi=0.85, end=0.03), 'letter')
    d = 0.33 * NIB * np.array([math.cos(ALPHA - math.pi / 2), math.sin(ALPHA - math.pi / 2)])
    for c in ((552, -118), (445, -148)):
        c = np.array(c, float); add(np.linspace(c - d, c + d, 12), np.full(12, 0.72), 'dot')
    th = np.linspace(0.5, 2 * np.pi + 0.3, 48); add(np.stack([83 + 46 * np.cos(th), 946 + 42 * np.sin(th)], 1), np.full(48, 0.36), 'mark')
    return S


PIVOT, TILT, RA_SCALE, AXIS, SUKUN_AT = np.array([200.0, 110.0]), math.radians(13), 1.18, 52.0, np.array([118.0, 360.0])
GATHER = np.array([-185.0, 70.0])


def composed(model):
    """The right half of the mirror butterfly. The mim's tail stays as written: with its mirror, the body, tapering downward.
    Everything else turns up by TILT about the mim's head (the thorax), so the ya-mim join rises outward (the leading edge of
    the upper wing) and the ra, enlarged about its head, sweeps down as the wing's outer edge; the kasra and the dots fall in the
    lower wing; the sukun sits over the mim, and with its mirror makes the eyes. Shifted so the axis is x = 0."""
    S = strokes(model); c, s = math.cos(TILT), math.sin(TILT); R = np.array([[c, -s], [s, c]])
    S[0]['pts'] = S[0]['pts'][0] + RA_SCALE * (S[0]['pts'] - S[0]['pts'][0])
    S[1]['pts'] = S[1]['pts'] + [-40, 150]
    for i in (0, 1, 5, 6):                                  # ra, kasra and the dots drawn in towards the body: one closed wing
        S[i]['pts'] = S[i]['pts'] + GATHER
    S[-1]['pts'] = S[-1]['pts'] - S[-1]['pts'].mean(0) + SUKUN_AT
    for i, st in enumerate(S):
        if i != 4 and i != len(S) - 1:                     # all but the tail (index 4) and the sukun turn about the head
            st['pts'] = (st['pts'] - PIVOT) @ R.T + PIVOT
        st['pts'] = st['pts'] - [AXIS, 0]
    return S


def quads(st, alpha=ALPHA, nib=NIB):
    p, k = st['pts'], st['k']; e = 0.5 * nib * np.array([math.cos(alpha), math.sin(alpha)])
    A, B = p + k[:, None] * e, p - k[:, None] * e
    return [np.array([A[i], A[i + 1], B[i + 1], B[i]]) for i in range(len(p) - 1)]


def ink_polys():
    """All the ink of the mirror composition, as quadrilaterals (right half, then its mirror)."""
    out = []
    for st in composed(MODEL):
        for sgn in (1, -1):
            out += quads(dict(st, pts=st['pts'] * [sgn, 1]), ALPHA if sgn > 0 else math.pi - ALPHA)
    return out


MODEL = None
if __name__ == '__main__':
    import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
    from matplotlib.collections import PolyCollection
    MODEL = sys.argv[1]; Q = ink_polys(); allp = np.concatenate(Q)
    fig, ax = plt.subplots(1, 2, figsize=(16, 7), dpi=110)
    for a, bg, ink in zip(ax, ('#140d10', '#f5f1ea'), ('#e2a2aa', '#7a1f2b')):
        a.set_facecolor(bg); a.add_collection(PolyCollection(Q, facecolors=ink, edgecolors=ink, linewidths=0.5))
        a.set_xlim(allp[:, 0].min() - 120, allp[:, 0].max() + 120); a.set_ylim(allp[:, 1].min() - 120, allp[:, 1].max() + 120)
        a.set_aspect('equal'); a.set_xticks([]); a.set_yticks([])
        for sp in a.spines.values(): sp.set_visible(False)
    fig.patch.set_facecolor('#140d10'); fig.subplots_adjust(0, 0, 1, 1, 0.01); fig.savefig(sys.argv[2], facecolor=fig.get_facecolor())

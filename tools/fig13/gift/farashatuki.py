"""فَرَاشَتُكِ written in the hand of the traced رِيمْ (reem_ref.json), for the gift film.

The hand, measured on the traced name (stroke width against stroke direction, 5282 skeleton samples): a flat nib about 60 px wide
(px of the 4x crop of the reference), held at 70 degrees from the horizontal: horizontal strokes 57-60 px thick, strokes at 60-75
degrees about 16 px. Its habits, read from the plate: letters climb on a diagonal from the upper right; the ra sweeps far down and
to the left, under what follows; marks are long and slanted (fatha), a damma with a long tail, a short slanted kasra; dots are
rhombic presses of the nib.

What is taken from the plate unchanged: the ra (contour 7), the fathas (contours 0 and 1), the damma (3), the kasra (13) and the
small hooked mark used inside the kaf (4). What is written new with the same nib: fa (initial: a round head with its counter, the
neck dropping into the ra's head), alif, shin (initial: three teeth) and ta (medial: one tooth) on one baseline that runs on into
the kaf (final: the long base with an upturn, its upright and its top bar), and the dots (one over fa, three over shin, two over ta).

    python3 tools/fig13/gift/farashatuki.py OUT.json [PREVIEW.png]
Coordinates: px, y down, as reem_ref.json; contours oriented alike (the traced outer contours' sense), filled with the nonzero rule.
"""
import sys, json, math
import numpy as np

HERE = __file__.rsplit('/', 1)[0]
REF = json.load(open(HERE + '/reem_ref.json'))
NIB, ALPHA = 60.0, math.radians(70)          # measured on the traced رِيمْ
E = 0.5 * NIB * np.array([math.cos(ALPHA), -math.sin(ALPHA)])   # half the nib edge, in y-down px


def bez(*P, n=40):
    P = np.asarray(P, float); out = []
    for i in range(0, len(P) - 1, 3):
        a, b, c, d = P[i:i + 4]; t = np.linspace(0, 1, n)[:, None]
        seg = (1 - t) ** 3 * a + 3 * (1 - t) ** 2 * t * b + 3 * (1 - t) * t ** 2 * c + t ** 3 * d
        out.append(seg if not out else seg[1:])
    return np.vstack(out)


def prof(n, a=0.12, b=0.3, lo=0.5, hi=1.0, end=0.1):
    s = np.linspace(0, 1, n); k = np.full(n, hi)
    k = np.where(s < a, lo + (hi - lo) * np.sin(0.5 * np.pi * s / a), k)
    return np.where(s > 1 - b, end + (hi - end) * np.cos(0.5 * np.pi * (s - (1 - b)) / b), k)


def area(c):
    return 0.5 * (np.dot(c[:, 0], np.roll(c[:, 1], 1)) - np.dot(c[:, 1], np.roll(c[:, 0], 1)))


SENSE = np.sign(area(np.array(REF['contours'][7])))   # the traced outer contours' sense


def orient(c, outer=True):
    return c if np.sign(area(c)) == (SENSE if outer else -SENSE) else c[::-1]


TWIST = 0.5 * NIB * np.array([math.cos(math.radians(45)), -math.sin(math.radians(45))])   # the reed turned for uprights: 40 px wide, as the plate's uprights


def stroke(p, k, e=None):
    """The envelope of the nib swept along p (one side forward, the other back): one closed contour."""
    e = E if e is None else e
    A, B = p + k[:, None] * e, p - k[:, None] * e
    return orient(np.vstack([A, B[::-1]]))


def dot(c, size=0.85):
    """A rhombic dot: a short press of the nib straight across its edge."""
    d = 0.42 * NIB * np.array([math.sin(ALPHA), math.cos(ALPHA)]) * size
    p = np.linspace(np.array(c) - d, np.array(c) + d, 8)
    return stroke(p, np.full(8, size))


def ref(i, dx=0.0, dy=0.0, s=1.0, about=None):
    c = np.array(REF['contours'][i], float); o = c.mean(0) if about is None else np.array(about, float)
    return orient(o + s * (c - o) + [dx, dy])


def word():
    C = []
    # fa (initial): a round head, high on the right, its counter left open by the nib, then the neck dropping into the ra's head
    head = bez((1760, 300), (1800, 240), (1770, 175), (1712, 182), (1660, 190), (1648, 255), (1690, 285), (1715, 302), (1748, 300), (1760, 300), n=30)
    C.append(stroke(head, np.full(len(head), 0.78)))
    neck = bez((1740, 300), (1690, 330), (1600, 330), (1520, 340), (1480, 345), (1452, 350), (1440, 362), n=40)
    C.append(stroke(neck, prof(len(neck), a=0.1, b=0.12, lo=0.7, end=0.9)))
    C.append(dot((1712, 130)))
    # ra: the plate's own, its head where the fa's neck arrives
    C.append(ref(7, dx=330, dy=-20))
    # alif: tall and slender (it runs nearly along the nib), with a small head at the top
    alif = bez((1265, 150), (1258, 280), (1240, 450), (1222, 610), n=50)
    C.append(stroke(alif, prof(len(alif), a=0.08, b=0.25, lo=1.1, hi=0.95, end=0.6), TWIST))
    # shin (initial) and ta (medial) on one baseline that runs on into the kaf's long base, which turns up at its end
    base = bez((1090, 600), (980, 612), (860, 615), (760, 618), (600, 622), (430, 640), (330, 650), (250, 655), (205, 630), (215, 560), n=60)
    C.append(stroke(base, prof(len(base), a=0.04, b=0.12, lo=0.9, end=0.35)))
    for x, h in ((1085, 470), (1000, 500), (915, 500), (780, 470)):       # three teeth of shin, one of ta
        tooth = bez((x + 6, h), (x + 4, h + 40), (x, h + 90), (x - 4, 612), n=16)
        C.append(stroke(tooth, prof(len(tooth), a=0.25, b=0.1, lo=1.15, hi=0.9, end=0.9), TWIST))
    for c in ((1000, 385), (955, 315), (1045, 315)):                      # shin's three dots
        C.append(dot(c))
    for c in ((745, 390), (810, 390)):                                    # ta's two dots
        C.append(dot(c))
    # kaf (final): the upright rising from the end of the base, and its top bar slanting up to the right
    up = bez((250, 650), (300, 520), (360, 380), (420, 250), n=40)
    C.append(stroke(up, prof(len(up), a=0.06, b=0.1, lo=0.95, end=0.85), TWIST))
    bar = bez((410, 255), (470, 225), (560, 190), (650, 160), n=30)
    C.append(stroke(bar, prof(len(bar), a=0.05, b=0.35, lo=0.95, end=0.2)))
    C.append(ref(4, dx=-1110, dy=260, s=1.0))                             # the small mark inside the kaf
    # the vowels, from the plate: fatha over fa, fatha over ra, fatha over shin, damma over ta, kasra under kaf
    C.append(ref(1, dx=20, dy=-185, s=0.55))
    C.append(ref(1, dx=-30, dy=150, s=0.6))
    C.append(ref(0, dx=-90, dy=-30, s=0.55))
    C.append(ref(3, dx=200, dy=-30, s=0.8))
    C.append(ref(13, dx=-120, dy=-10, s=1.0))
    return C


if __name__ == '__main__':
    C = word()
    allp = np.vstack(C); W, H = int(allp[:, 0].max() + 60), int(allp[:, 1].max() + 60)
    json.dump(dict(width=W, height=H, contours=[c.round(2).tolist() for c in C]), open(sys.argv[1], 'w'), separators=(',', ':'))
    print('%d contours, %d points, box %d x %d px' % (len(C), sum(len(c) for c in C), W, H))
    if len(sys.argv) > 2:
        import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
        from matplotlib.path import Path; from matplotlib.patches import PathPatch
        def patch(cs):
            v, cd = [], []
            for q in cs: v += list(q) + [q[0]]; cd += [Path.MOVETO] + [Path.LINETO] * (len(q) - 1) + [Path.CLOSEPOLY]
            return Path(v, cd)
        fig, ax = plt.subplots(1, 2, figsize=(18, 7), dpi=90); fig.patch.set_facecolor('#f5f1ea')
        for a, cs in zip(ax, ([np.array(c) for c in REF['contours']], C)):
            a.add_patch(PathPatch(patch(cs), fc='#1c1518', ec='none')); a.autoscale_view(); a.invert_yaxis(); a.set_aspect('equal'); a.axis('off')
        ax[0].set_title('رِيمْ (the plate)'); ax[1].set_title('فَرَاشَتُكِ (the same hand)')
        fig.savefig(sys.argv[2], facecolor=fig.get_facecolor())

"""Compositions of فَرَاشَتُكِ that read as one word, in the hand of the traced رِيمْ (pen and marks from farashatuki.py).

The word falls into three pieces, فر · ا · شتك, because ra and alif never join the letter after them. A calligrapher binds such
pieces by stacking and interlocking them, as the plate binds رِيمْ with the ra's sweep under the ya. Three compositions:
  A  ra as the binding sweep: alif stands on it, شتك rides on its tail, the kaf's upright and bar arch back over the word
  B  kaf's bowl as the binding sweep: a deep curve under the word from the ta to an upturned end, as the plate's mim tail
  C  a tight stack: فر on top, ا through the middle, شتك below on a long kashida
    python3 tools/fig13/gift/farashatuki_v2.py A|B|C OUT.json        one composition
    python3 tools/fig13/gift/farashatuki_v2.py sheet OUT.png         all three beside the current one and the plate
"""
import sys, json
import numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from farashatuki import bez as _bez, prof, stroke, dot, ref, TWIST, REF, word as current


def bez(*P, n=40):
    """A chain of cubic pieces; a short last piece is completed by repeating its end point."""
    P = [np.asarray(q, float) for q in P]
    while (len(P) - 1) % 3: P.append(P[-1])
    return _bez(*P, n=n)


def fa(C, cx, cy):
    """Initial fa: a round head (its counter left open by the nib); returns the start of its neck."""
    head = bez((cx + 20, cy + 50), (cx + 60, cy - 10), (cx + 30, cy - 75), (cx - 28, cy - 68), (cx - 80, cy - 60), (cx - 92, cy + 5), (cx - 50, cy + 35),
               (cx - 25, cy + 52), (cx + 8, cy + 50), (cx + 20, cy + 50), n=30)
    C.append(stroke(head, np.full(len(head), 0.78)))
    return np.array([cx, cy + 50])


def neck(C, a, b):
    p = bez(a, a + [-30, 35], b + [40, -25], b, n=30)
    C.append(stroke(p, prof(len(p), a=0.1, b=0.12, lo=0.7, end=0.9)))


def alif(C, top, bottom):
    p = bez(top, top + (bottom - top) * 0.33, top + (bottom - top) * 0.66, bottom, n=50)
    C.append(stroke(p, prof(len(p), a=0.08, b=0.25, lo=1.1, hi=0.95, end=0.6), TWIST))


def shin_ta(C, x0, y, step=68):
    """Teeth of shin (three) and ta (one) on a baseline at y from x0 leftwards; dots; returns the ta's x."""
    xs = [x0, x0 - step, x0 - 2 * step, x0 - 3 * step - 30]
    for x in xs:
        t = bez((x + 6, y - 125), (x + 4, y - 85), (x, y - 35), (x - 4, y + 10), n=16)
        C.append(stroke(t, prof(len(t), a=0.25, b=0.1, lo=1.15, hi=0.9, end=0.9), TWIST))
    mid = xs[1]
    for c in ((mid - 32, y - 215), (mid + 32, y - 215), (mid, y - 280)):
        C.append(dot(c))
    for c in ((xs[3] - 30, y - 210), (xs[3] + 30, y - 210)):
        C.append(dot(c))
    return xs


def compose(kind):
    C = []
    if kind == 'A':
        C.append(ref(7))                                         # the ra, as on the plate: head (1110-1150, 370-440), tail to (820, 860)
        n0 = fa(C, 1235, 215); neck(C, n0, np.array([1128.0, 372.0])); C.append(dot((1222, 88)))
        alif(C, np.array([1012.0, 150.0]), np.array([985.0, 660.0]))
        xs = shin_ta(C, 925, 610)
        base = bez((945, 605), (820, 618), (700, 622), (600, 628), (500, 636), (430, 640), (390, 618), (395, 560), n=50)
        C.append(stroke(base, prof(len(base), a=0.04, b=0.12, lo=0.9, end=0.4)))
        up = bez((430, 640), (470, 520), (520, 400), (565, 285), n=40); C.append(stroke(up, prof(len(up), a=0.06, b=0.1, lo=0.95, end=0.85), TWIST))
        bar = bez((555, 290), (620, 262), (700, 232), (790, 200), n=30); C.append(stroke(bar, prof(len(bar), a=0.05, b=0.35, lo=0.95, end=0.2)))
        C.append(ref(4, dx=575 - 1518, dy=505 - 250))            # the small mark inside the kaf
        C.append(ref(1, dx=1150 - 1460, dy=40 - 169, s=0.5))    # fatha over fa
        C.append(ref(1, dx=1070 - 1460, dy=310 - 169, s=0.42))   # fatha over ra
        C.append(ref(0, dx=860 - 1108, dy=280 - 245, s=0.38))   # fatha over shin
        C.append(ref(3, dx=xs[3] - 580, dy=330 - 255, s=0.62))   # damma over ta
        C.append(ref(13, dx=560 - 542, dy=745 - 818, s=0.95))    # kasra under kaf
    elif kind == 'B':
        n0 = fa(C, 1500, 230); C.append(dot((1488, 100)))
        C.append(ref(7, dx=270, dy=-60, s=0.82, about=(1110, 370)))            # ra, smaller, hanging from the fa
        neck(C, n0, np.array([1380.0, 320.0]))
        alif(C, np.array([1215.0, 120.0]), np.array([1190.0, 600.0]))
        xs = shin_ta(C, 1110, 520)
        bowl = bez((1130, 515), (980, 525), (860, 530), (760, 540), (620, 560), (520, 700), (600, 800), (760, 880), (1080, 860), (1250, 760), (1330, 700), (1380, 640), (1395, 590), n=60)
        C.append(stroke(bowl, prof(len(bowl), a=0.04, b=0.18, lo=0.9, end=0.25)))
        up = bez((620, 560), (650, 440), (690, 330), (735, 225), n=40); C.append(stroke(up, prof(len(up), a=0.06, b=0.1, lo=0.95, end=0.85), TWIST))
        bar = bez((725, 230), (790, 200), (870, 170), (960, 140), n=30); C.append(stroke(bar, prof(len(bar), a=0.05, b=0.35, lo=0.95, end=0.2)))
        C.append(ref(4, dx=760 - 1518, dy=420 - 250))
        C.append(ref(1, dx=1420 - 1460, dy=45 - 169, s=0.5)); C.append(ref(1, dx=1330 - 1460, dy=200 - 169, s=0.4))
        C.append(ref(0, dx=1050 - 1108, dy=200 - 245, s=0.36)); C.append(ref(3, dx=xs[3] - 580, dy=250 - 255, s=0.6))
        C.append(ref(13, dx=880 - 542, dy=760 - 818, s=0.85))
    elif kind == 'C':
        n0 = fa(C, 1100, 140); C.append(dot((1090, 15)))
        C.append(ref(7, dx=-60, dy=-200, s=0.75, about=(1110, 370)))
        neck(C, n0, np.array([1050.0, 175.0]))
        alif(C, np.array([880.0, 60.0]), np.array([860.0, 560.0]))
        xs = shin_ta(C, 1150, 690, step=62)
        base = bez((1170, 685), (1000, 700), (800, 712), (600, 718), (430, 722), (330, 726), (290, 700), (300, 640), n=60)
        C.append(stroke(base, prof(len(base), a=0.04, b=0.12, lo=0.9, end=0.4)))
        up = bez((330, 726), (380, 560), (430, 410), (480, 270), n=40); C.append(stroke(up, prof(len(up), a=0.06, b=0.1, lo=0.95, end=0.85), TWIST))
        bar = bez((470, 275), (540, 245), (620, 215), (710, 185), n=30); C.append(stroke(bar, prof(len(bar), a=0.05, b=0.35, lo=0.95, end=0.2)))
        C.append(ref(4, dx=520 - 1518, dy=560 - 250))
        C.append(ref(1, dx=1000 - 1460, dy=-40 - 169, s=0.5)); C.append(ref(1, dx=990 - 1460, dy=260 - 169, s=0.4))
        C.append(ref(0, dx=1090 - 1108, dy=380 - 245, s=0.36)); C.append(ref(3, dx=xs[3] - 580, dy=420 - 255, s=0.6))
        C.append(ref(13, dx=420 - 542, dy=800 - 818, s=0.95))
    return C


def save(C, path):
    allp = np.vstack(C); W, H = int(allp[:, 0].max() + 60), int(allp[:, 1].max() + 60)
    json.dump(dict(width=W, height=H, contours=[c.round(2).tolist() for c in C]), open(path, 'w'), separators=(',', ':'))


if __name__ == '__main__':
    if sys.argv[1] in 'ABC':
        save(compose(sys.argv[1]), sys.argv[2])
    else:
        import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
        from matplotlib.path import Path; from matplotlib.patches import PathPatch
        def patch(cs):
            v, cd = [], []
            for q in cs: q = np.asarray(q); v += list(q) + [q[0]]; cd += [Path.MOVETO] + [Path.LINETO] * (len(q) - 1) + [Path.CLOSEPOLY]
            return Path(v, cd)
        panels = [('رِيمْ — the plate', REF['contours']), ('current فَرَاشَتُكِ (rejected)', current()), ('A · the ra binds the word', compose('A')),
                  ('B · the kaf’s bowl binds the word', compose('B')), ('C · a tight stack', compose('C'))]
        fig, ax = plt.subplots(1, 5, figsize=(30, 7), dpi=70); fig.patch.set_facecolor('#f5f1ea')
        for a, (t, cs) in zip(ax, panels):
            a.add_patch(PathPatch(patch(cs), fc='#7a1f2b', ec='none')); a.autoscale_view(); a.invert_yaxis(); a.set_aspect('equal'); a.axis('off'); a.margins(0.06)
            a.set_title(t, fontsize=16, color='#1c1518')
        fig.tight_layout(); fig.savefig(sys.argv[2], facecolor=fig.get_facecolor())

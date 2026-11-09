"""Centre lines of a word in a model font (the path the centre of a pen would travel), for re-inking with the reed pen of qalam.py.

The word is shaped and outlined by calligraphy.py, filled into a raster (RES px per font em), thinned to a one-pixel skeleton
(scikit-image), and the skeleton traced into polylines: from each end point, then around any closed loop. Short spurs (shorter
than SPUR px) are dropped; each path is smoothed and resampled every STEP px. The half-width of the ink along each path (from the
distance transform) is kept, so the re-inking can match the model's weight.

    paths(font, text) -> list of dict(pts (n, 2) in font units, y up; half (n,) half-width in font units)
"""
import numpy as np
from matplotlib.path import Path
from skimage.morphology import skeletonize
from scipy.ndimage import distance_transform_edt, gaussian_filter1d
from calligraphy import word_contours

RES, SPUR, STEP = 1.2, 14, 2.0       # px per font unit; spur length (px); resampling step (px)


def raster(contours, pad=40):
    allp = np.concatenate(contours); x0, y0 = allp.min(0) - pad / RES; x1, y1 = allp.max(0) + pad / RES
    W, H = int((x1 - x0) * RES), int((y1 - y0) * RES)
    yy, xx = np.mgrid[0:H, 0:W]; pts = np.stack([x0 + (xx.ravel() + 0.5) / RES, y1 - (yy.ravel() + 0.5) / RES], 1)
    verts, codes = [], []
    for c in contours: verts += list(c) + [c[0]]; codes += [Path.MOVETO] + [Path.LINETO] * (len(c) - 1) + [Path.CLOSEPOLY]
    inside = Path(verts, codes).contains_points(pts).reshape(H, W)   # nonzero winding, as fonts fill
    return inside, (x0, y1)


def trace(sk):
    """Polylines of a skeleton: walk from end points and junctions; then any loops left."""
    H, W = sk.shape; on = set(zip(*np.nonzero(sk)))
    nb = lambda p: [(p[0] + i, p[1] + j) for i in (-1, 0, 1) for j in (-1, 0, 1) if (i or j) and (p[0] + i, p[1] + j) in on]
    deg = {p: len(nb(p)) for p in on}; used = set(); paths = []
    def walk(a, b):
        path = [a, b]; used.add(frozenset((a, b)))
        while deg[path[-1]] == 2:
            nxt = [q for q in nb(path[-1]) if frozenset((path[-1], q)) not in used]
            if not nxt: break
            used.add(frozenset((path[-1], nxt[0]))); path.append(nxt[0])
        return path
    for p in [p for p in on if deg[p] != 2]:
        for q in nb(p):
            if frozenset((p, q)) not in used: paths.append(walk(p, q))
    for p in on:
        for q in nb(p):
            if frozenset((p, q)) not in used: paths.append(walk(p, q))
    return paths


def paths(font, text):
    cs = word_contours(font, text)
    img, (x0, y1) = raster(cs)
    sk = skeletonize(img); dist = distance_transform_edt(img)
    out = []
    for p in trace(sk):
        p = np.array(p, float)
        if len(p) < SPUR: continue
        seg = np.hypot(*np.diff(p, axis=0).T); s = np.concatenate([[0], np.cumsum(seg)])
        t = np.arange(0, s[-1] + 1e-9, STEP)
        r = gaussian_filter1d(np.interp(t, s, p[:, 0]), 2, mode='nearest'); c = gaussian_filter1d(np.interp(t, s, p[:, 1]), 2, mode='nearest')
        half = dist[np.clip(np.round(r).astype(int), 0, img.shape[0] - 1), np.clip(np.round(c).astype(int), 0, img.shape[1] - 1)]
        out.append(dict(pts=np.stack([x0 + (c + 0.5) / RES, y1 - (r + 0.5) / RES], 1), half=half / RES))
    return out

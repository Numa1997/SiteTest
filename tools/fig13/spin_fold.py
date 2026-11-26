"""Fig. 13: the eye in its natural frame, spin and fold.
Usage: spin_fold.py SHEET.npy EYE.npy OUTDIR
SHEET.npy, EYE.npy: fine chaos maps from kaggle_fractal.py (mean capped twin distance d per strike); the sheet covers
p1 in +-35.56, p2 in +-20 kg m^2/s (watch 6.67 s), the eye p1 in +-14.4, p2 in +-8.1 (watch 26.67 s).

The strike (p1, p2) from hanging straight is rewritten as
    X = (p1 + p2) / sqrt(2 Is)            spin: the part that turns the pendulum as one straight stick
    Y = sqrt(mu / 2) * (w2 - w1)          fold: the part that bends the elbow, with no net turning
with Is = A + B + 2C (moment of inertia of the straight stick about the pin), mu = det(M)/Is, w = M^-1 p.
Then the strike's energy is K = X^2 + Y^2 exactly (checked below), so the energy ellipses are circles, and the
separatrix K = (p1+p2)^2 / (2 If), If = A + B - 2C (folded stick), is the pair of lines at angle +-acos(sqrt(If/Is)) from the spin axis.
For two equal uniform rods If/Is = 1/4 and the angle is 60 degrees.
Writes eye_spin_fold.png (the eye in the X, Y plane) and eye_unrolled.png (direction against energy)."""
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy.ndimage import map_coordinates

A, B, C = 4 / 3, 1 / 3, 1 / 2                                  # kg m^2: equal uniform rods, m = 1 kg, l = 1 m
M = np.array([[A, C], [C, B]]); Mi = np.linalg.inv(M)
Is, If, mu = A + B + 2 * C, A + B - 2 * C, np.linalg.det(M) / (A + B + 2 * C)
T = np.vstack([np.array([1, 1]) / np.sqrt(2 * Is), np.sqrt(mu / 2) * (Mi[1] - Mi[0])])   # (X, Y) = T (p1, p2)
Ti = np.linalg.inv(T)
rng = np.random.default_rng(0); p = rng.normal(size=(1000, 2)) * 10
K = 0.5 * np.einsum('ni,ij,nj->n', p, Mi, p); u = p @ T.T
assert np.allclose(K, (u ** 2).sum(1)), 'K is not X^2 + Y^2'
alpha = np.degrees(np.arccos(np.sqrt(If / Is)))
for x in (19 - 4 * np.sqrt(21), 19 + 4 * np.sqrt(21)):         # the note's lines (9)
    v = T @ np.array([x, 1.0]); print('line p1 = %.4f p2 sits at %.3f deg from the spin axis' % (x, np.degrees(np.arctan2(v[1], v[0]))))
print('Is %.4f  If %.4f  mu %.5f  lash angle %.3f deg' % (Is, If, mu, alpha))
print('spin axis on the sheet: p1/p2 = %.3f (%.1f deg); fold axis: p1 = -p2' % ((A + C) / (B + C), np.degrees(np.arctan2(B + C, A + C))))

stops = np.array([[0.00, 20, 13, 16], [0.25, 46, 18, 28], [0.50, 122, 31, 43], [0.72, 196, 96, 112], [0.88, 226, 162, 170], [1.00, 255, 240, 226]])
bright = lambda d: np.clip(np.log(1000 * np.maximum(d, 1e-12)) / np.log(1000), 0, 1)
paint = lambda v: np.stack([np.interp(v, stops[:, 0], stops[:, k]) for k in (1, 2, 3)], -1)
def sample(arr, hx, hy, p1, p2):
    H, W = arr.shape; col = (p1 + hx) / (2 * hx) * W - .5; row = (hy - p2) / (2 * hy) * H - .5
    v = map_coordinates(arr, [row, col], order=1, cval=np.nan); v[(np.abs(p1) > hx) | (np.abs(p2) > hy)] = np.nan; return v
sheet, eye = bright(np.load(sys.argv[1])), bright(np.load(sys.argv[2])); out = sys.argv[3]
font = lambda s: ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', s)
INK = (255, 246, 234)

# 1. the eye in the spin-fold plane
N, R = 2000, 8.8                                               # pixels, half-width in sqrt(J): the disc K <= 77 J lies inside the eye map
X, Y = np.meshgrid((np.arange(N) + .5) / N * 2 * R - R, R - (np.arange(N) + .5) / N * 2 * R)
P = Ti @ np.stack([X.ravel(), Y.ravel()]); v = sample(eye, 14.4, 8.1, P[0], P[1]).reshape(N, N)
im = Image.fromarray(paint(np.nan_to_num(v, nan=0)).astype(np.uint8)); d = ImageDraw.Draw(im); px = lambda x, y: ((x + R) / (2 * R) * N, (R - y) / (2 * R) * N)
for E in (9.8, 29.4, 39.2):
    r = np.sqrt(E); d.ellipse([*px(-r, r), *px(r, -r)], outline=(255, 255, 255), width=3)
    d.text(px(r * np.cos(np.radians(15)) + .1, r * np.sin(np.radians(15))), '%g J' % E, font=font(34), fill=INK)
for sgn in (1, -1):
    c, s = np.cos(np.radians(alpha)), sgn * np.sin(np.radians(alpha)); d.line([px(-12 * c, -12 * s), px(12 * c, 12 * s)], fill=(140, 230, 255), width=3)
d.line([px(-R, 0), px(R, 0)], fill=(160, 150, 150), width=2); d.line([px(0, -R), px(0, R)], fill=(160, 150, 150), width=2)
d.text((40, N / 2 + 14), 'SPIN: both rods turn together', font=font(40), fill=INK); d.text((N / 2 + 20, 30), 'FOLD: the rods turn against each other', font=font(40), fill=INK)
d.text(px(4.6, 8.4), '60°', font=font(40), fill=(140, 230, 255))
im.save(out + '/eye_spin_fold.png')

# 2. unrolled: direction of the strike against its energy
W2, H2 = 2400, 1350; K0, K1 = 1.0, 3000.0
ph, lk = np.meshgrid((np.arange(W2) + .5) / W2 * 180 - 90, np.log(K1) - (np.arange(H2) + .5) / H2 * np.log(K1 / K0))
r = np.sqrt(np.exp(lk)); P = Ti @ np.stack([(r * np.cos(np.radians(ph))).ravel(), (r * np.sin(np.radians(ph))).ravel()])
v = sample(sheet, 20 * 16 / 9, 20.0, P[0], P[1]).reshape(H2, W2); rgb = paint(np.nan_to_num(v, nan=0)); rgb[np.isnan(v)] = (58, 52, 54)
im = Image.fromarray(rgb.astype(np.uint8)); d = ImageDraw.Draw(im); yk = lambda E: (np.log(K1) - np.log(E)) / np.log(K1 / K0) * H2; xa = lambda a: (a + 90) / 180 * W2
for E in (9.8, 29.4, 39.2, 196):
    d.line([(0, yk(E)), (W2, yk(E))], fill=(255, 255, 255), width=2); d.text((14, yk(E) - 44), '%g J' % E, font=font(36), fill=INK)
for a in (-alpha, alpha):
    d.line([(xa(a), 0), (xa(a), H2)], fill=(140, 230, 255), width=2); d.text((xa(a) + 10, 12), '%+.0f°' % a, font=font(36), fill=(140, 230, 255))
d.line([(xa(0), 0), (xa(0), H2)], fill=(160, 150, 150), width=1); d.text((xa(0) + 10, 12), '0°: pure spin', font=font(36), fill=INK); d.text((14, 12), '-90°: pure fold', font=font(36), fill=INK)
d.text((14, H2 - 52), 'up: energy of the strike (each step x10)     across: how the strike is split between spin and fold', font=font(34), fill=INK)
im.save(out + '/eye_unrolled.png')

# is the map mirror-symmetric about the spin axis (fold reversed)?  Compared on the unrolled picture, hard strikes only.
hi = (np.exp(lk) > 196); a, b = v, v[:, ::-1]; ok = hi & np.isfinite(a) & np.isfinite(b)
print('above 196 J: chaotic share at fold > 0: %.4f, at fold < 0: %.4f; same call (chaotic or not) at mirrored strikes: %.4f' % ((a[ok & (ph > 0)] > .5).mean(), (a[ok & (ph < 0)] > .5).mean(), ((a[ok] > .5) == (b[ok] > .5)).mean()))
for lo, hi_ in ((9.8, 39.2), (39.2, 196)):
    ok = (np.exp(lk) > lo) & (np.exp(lk) < hi_) & np.isfinite(a) & np.isfinite(b); print('%g to %g J: same call at mirrored strikes %.3f, chaotic share %.3f' % (lo, hi_, ((a[ok] > .5) == (b[ok] > .5)).mean(), (a[ok] > .5).mean()))

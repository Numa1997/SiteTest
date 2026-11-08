"""Compound double pendulum in momentum space: our own computation.

Physics (same as 2swap's swaptube PendulumHelpers.h, kept with symbols):
two equal uniform rods, mass m, length l, gravity g, angles from the downward vertical.
Hamilton's equations with Delta = th1 - th2, D = 16 - 9 cos^2 Delta:
  th1' = 6/(m l^2) (2 p1 - 3 cos(Delta) p2) / D
  th2' = 6/(m l^2) (8 p2 - 3 cos(Delta) p1) / D
  p1'  = -1/2 m l^2 ( th1' th2' sin(Delta) + 3 (g/l) sin th1)
  p2'  = -1/2 m l^2 (-th1' th2' sin(Delta) +   (g/l) sin th2)
Tip of the lower rod: x = l (sin th1 + sin th2), y = -l (cos th1 + cos th2).
"""
import numpy as np, sys, time

m, l, g = 1.0, 1.0, 9.8
mll = m * l * l


def deriv(s):
    t1, t2, p1, p2 = s
    d = t1 - t2
    c, sn = np.cos(d), np.sin(d)
    k = 6.0 / (mll * (16.0 - 9.0 * c * c))
    w1 = k * (2.0 * p1 - 3.0 * c * p2)
    w2 = k * (8.0 * p2 - 3.0 * c * p1)
    e = w1 * w2 * sn
    return np.array([w1, w2, -0.5 * mll * (e + 3.0 * g / l * np.sin(t1)),
                     -0.5 * mll * (-e + g / l * np.sin(t2))])


def rk4(s, h):
    k1 = deriv(s); k2 = deriv(s + 0.5 * h * k1)
    k3 = deriv(s + 0.5 * h * k2); k4 = deriv(s + h * k3)
    return s + h / 6.0 * (k1 + 2 * k2 + 2 * k3 + k4)


def energy(s):
    t1, t2, p1, p2 = s
    w = deriv(s)
    T = mll / 6 * (4 * w[0] ** 2 + w[1] ** 2 + 3 * w[0] * w[1] * np.cos(t1 - t2))
    V = m * g * l / 2 * (4 - 3 * np.cos(t1) - np.cos(t2))
    return T + V

AR = 16 / 9
P = 20.0  # half-range of p2; p1 half-range is P*AR (as in the video)

# ---- 1. tip paths of the 10 x 10 grid -------------------------------------
N = 10
xs, ys = np.meshgrid((np.arange(N) + .5) / N - .5, (np.arange(N) + .5) / N - .5)
p1 = (xs * 2 * P * AR).ravel(); p2 = (-ys * 2 * P).ravel()
s = np.array([np.zeros_like(p1), np.zeros_like(p1), p1, p2])
E0 = energy(s)
fps, sub = 30, 300
h = 1.0 / fps / sub                   # 1/9000 s, ten times finer than 2swap's step
frames = 12 * fps
tips = np.empty((frames * sub // 10 + 1, 2, N * N))   # keep every 10th step (900 points per second)
tips[0] = [l * (np.sin(s[0]) + np.sin(s[1])), -l * (np.cos(s[0]) + np.cos(s[1]))]
for i in range(frames * sub):
    s = rk4(s, h)
    if (i + 1) % 10 == 0: tips[(i + 1) // 10] = [l * (np.sin(s[0]) + np.sin(s[1])), -l * (np.cos(s[0]) + np.cos(s[1]))]
drift = np.abs(energy(s) - E0) / E0
print('paths done; max relative energy drift', drift.max(), flush=True)
np.savez_compressed(sys.argv[1] + '/paths.npz', tips=tips.astype(np.float32), p1=p1, p2=p2,
                    E0=E0, drift=drift, h=h, sub=sub, fps=fps)

if len(sys.argv) < 3: sys.exit(0)
# ---- 2. momentum-space chaos map (twin-pendulum divergence) ---------------
W, H = int(sys.argv[2]), int(sys.argv[3])
gx = np.linspace(-P * AR, P * AR, W); gy = np.linspace(P, -P, H)
G1, G2 = np.meshgrid(gx, gy)
a = np.array([np.zeros(W * H), np.zeros(W * H), G1.ravel(), G2.ravel()])
b = a.copy(); b[0] += 1e-4             # twin: th1 nudged by 1e-4 rad (as in swaptube)
acc = np.zeros(W * H)
steps, hb = 4000, 0.05 / 30            # 4000 steps of 0.05/30 s, as in the video
t0 = time.time()
for i in range(steps):
    a = rk4(a, hb); b = rk4(b, hb)
    acc += np.sqrt(((a - b) ** 2).sum(0))
    if i % 500 == 0:
        print('map step', i, round(time.time() - t0), 's', flush=True)
np.savez_compressed(sys.argv[1] + '/map.npz', mean_dist=(acc / steps).reshape(H, W),
                    E=energy(np.array([np.zeros(W*H), np.zeros(W*H), G1.ravel(), G2.ravel()])).reshape(H, W),
                    gx=gx, gy=gy)
print('map done', round(time.time() - t0), 's', flush=True)

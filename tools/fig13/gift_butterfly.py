"""A butterfly drawn by a double pendulum: the real motion and the butterfly, linked frame to frame.

The butterfly is the real path of the tip of the lower rod (metres, in the plane of the swing). Four linked panels show how
the swinging rods produce it, each panel driven by the one before through one exact map:

  1  The pendulum      theta1(t), theta2(t) from Hamilton's equations (equal uniform rods, m = 1 kg, l = 1 m, g = 9.8 m/s^2)
  2  Two rods, one arm psi = (theta1 + theta2)/2,  D = theta1 - theta2;  tip = l e^{i theta1} + l e^{i theta2} = 2 l cos(D/2) e^{i psi}
  3  The fold clock    a point turning at the angle D/2 on a circle; its height is cos(D/2), so r = 2 l cos(D/2) (circle -> cosine)
  4  The butterfly     tip = r e^{i psi}; a petal is drawn each time D completes a turn; the petal direction phi_n = theta2(t_n)
                       swings about straight down like a slow pendulum, and the petals pile up at its turning points: the wings

Usage: python3 tools/fig13/gift_butterfly.py OUT.mp4 FONTDIR [p1 p2 N slow]
       defaults: the closed 24-petal butterfly p = (3.557307, 12.211010) kg m^2/s, shown at a quarter of real speed.
"""
import sys, math
import numpy as np
from scipy.integrate import solve_ivp
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.animation import FFMpegWriter
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from chaos_map import coefficients
from hunt import rhs, turns, BASE, RTOL, ATOL

out, fontdir = sys.argv[1], sys.argv[2]
P1, P2, N, SLOW = (float(sys.argv[3]), float(sys.argv[4]), int(sys.argv[5]), float(sys.argv[6])) if len(sys.argv) > 6 \
    else (3.557312977100609, 12.211005483946245, 24, 0.25)   # full precision, from tools/fig13/butterfly.py
FPS, HOLD = 30, 3.0                                       # frames per second; seconds held on the finished butterfly

for f in ('InstrumentSerif.ttf', 'PlexMono.ttf', 'PlexSans.ttf'):
    font_manager.fontManager.addfont(fontdir + '/' + f)
SERIF = font_manager.FontProperties(fname=fontdir + '/InstrumentSerif.ttf')
MONO = font_manager.FontProperties(fname=fontdir + '/PlexMono.ttf')
plt.rcParams['mathtext.fontset'] = 'cm'
NIGHT, CREAM, ROSE, WINE, MUTED, RULE = '#140d10', '#f5f1ea', '#e2a2aa', '#7a1f2b', '#b9a59b', '#3a2a2e'

# ---- the motion: one full period of the closed butterfly ---------------------------------------------------------------
coef = coefficients(dict(BASE, g=9.8))
t_tip, s_tip, sgn = turns(coef, P1, P2, N, 60.0)
T = t_tip[-1]
closure = math.hypot(math.remainder(s_tip[-1, 1], 2 * math.pi), math.hypot(s_tip[-1, 2] - P1, s_tip[-1, 3] - P2))
assert closure < 1e-6, 'this kick does not close after N petals: %.2e' % closure
tt = np.linspace(0, T, 40001)
sol = solve_ivp(rhs(coef), (0, T), [0, 0, P1, P2], method='DOP853', rtol=RTOL, atol=ATOL, t_eval=tt, dense_output=True)
th1, th2 = sol.y[0], sol.y[1]
D, psi = th1 - th2, (th1 + th2) / 2
r = 2 * np.cos(D / 2)                                     # signed reach, metres (l = 1 m)
X, Y = np.sin(th1) + np.sin(th2), np.cos(th1) + np.cos(th2)  # tip, metres, y pointing down
assert np.max(np.abs(r * np.sin(psi) - X)) < 1e-12 and np.max(np.abs(r * np.cos(psi) - Y)) < 1e-12   # map (3)->(4) is exact
phi = np.concatenate([[0.0], s_tip[:, 1]])               # petal tip directions: start, then each alignment
tp = np.concatenate([[0.0], t_tip])
wing = np.degrees(np.max(np.abs([math.remainder(a, 2 * math.pi) for a in phi])))
print('period %.4f s, %d petals, closure %.1e, wings +-%.1f deg' % (T, N, closure, wing))

# ---- the figure ------------------------------------------------------------------------------------------------------------
fig = plt.figure(figsize=(19.2, 10.8), dpi=100, facecolor=NIGHT)
def panel(rect, title, eq):
    ax = fig.add_axes(rect); ax.set_facecolor(NIGHT)
    for sp in ax.spines.values(): sp.set_color(RULE)
    ax.set_xticks([]); ax.set_yticks([])
    fig.text(rect[0], rect[1] + rect[3] + 0.012, title, fontproperties=SERIF, fontsize=25, color=CREAM)
    fig.text(rect[0], rect[1] - 0.034, eq, fontsize=15, color=MUTED)
    return ax
fig.text(0.03, 0.945, 'A butterfly drawn by a double pendulum', fontproperties=SERIF, fontsize=40, color=CREAM)
fig.text(0.03, 0.915, 'two equal rods, 1 kg and 1 m each, hanging still, kicked once: p = (%.3f, %.3f) kg·m²/s.  '
         'The butterfly is the real path of the lower rod\'s tip.' % (P1, P2), fontproperties=MONO, fontsize=13, color=MUTED)
A = panel([0.03, 0.47, 0.17, 0.30], '1 · The pendulum', r'$\theta_1(t),\ \theta_2(t)$')
B = panel([0.225, 0.47, 0.17, 0.30], '2 · Two rods, one arm', r'$\psi=\frac{\theta_1+\theta_2}{2},\ \Delta=\theta_1-\theta_2$')
C = panel([0.03, 0.09, 0.365, 0.25], '3 · The fold clock', r'$r = 2l\cos\frac{\Delta}{2}$   (a turning circle drawn out as a cosine)')
Dp = panel([0.43, 0.09, 0.54, 0.68], '4 · The butterfly', r'$\mathrm{tip} = r\,e^{i\psi}$;  one petal per turn of $\Delta$;  the petals point at $\phi_n=\theta_2(t_n)$, which swings like a slow pendulum')
for ax in (A, B):
    ax.set_xlim(-2.25, 2.25); ax.set_ylim(2.25, -2.25); ax.set_aspect('equal')
    ax.add_patch(plt.Circle((0, 0), 2, fill=False, ls=(0, (2, 4)), color=RULE, lw=1))
Dp.set_xlim(-2.2 * 1.6, 2.2 * 1.6); Dp.set_ylim(2.2, -2.2); Dp.set_aspect('equal')
C.set_xlim(-1.3, 6.0); C.set_ylim(-1.25, 1.25); C.set_aspect('equal')
C.add_patch(plt.Circle((0, 0), 1, fill=False, color=RULE, lw=1)); C.axhline(0, color=RULE, lw=0.8)

# 1: rods and a short fading trail of the tip
rodA, = A.plot([], [], color=CREAM, lw=5, solid_capstyle='round')
jointA, = A.plot([], [], 'o', ms=7, color=WINE, mec=CREAM, mew=1.2)
trailA, = A.plot([], [], color=ROSE, lw=1, alpha=0.7)
A.plot(0, 0, 'o', ms=6, color=CREAM)
# 2: the two rods faint, the one equivalent arm bright
rodB, = B.plot([], [], color=CREAM, lw=3, alpha=0.25, solid_capstyle='round')
armB, = B.plot([], [], color=ROSE, lw=3, solid_capstyle='round')
tipB, = B.plot([], [], 'o', ms=7, color=CREAM)
psiB = B.text(0, 0, '', color=MUTED, fontsize=14)
# 3: circle point at D/2, its height cos(D/2), the cosine trailing to the right
ptC, = C.plot([], [], 'o', ms=8, color=CREAM)
radC, = C.plot([], [], color=CREAM, lw=1.2, alpha=0.6)
linkC, = C.plot([], [], ls=(0, (3, 3)), color=MUTED, lw=1)
waveC, = C.plot([], [], color=ROSE, lw=1.6)
C.text(-1.25, 1.08, r'the angle $\Delta/2$ turns', color=MUTED, fontsize=13)
C.text(1.6, 1.08, r'its height, $r/2l$, over the last %.2f s' % (T / 4), color=MUTED, fontsize=13)
# 4: the growing butterfly, the arm, the swing of the petal direction
traceD, = Dp.plot([], [], color=ROSE, lw=0.9, alpha=0.9)
armD, = Dp.plot([], [], color=CREAM, lw=2.2, alpha=0.9, solid_capstyle='round')
tipD, = Dp.plot([], [], 'o', ms=6, color=CREAM)
handD, = Dp.plot([], [], color=WINE, lw=2.5, alpha=0.95)
petD, = Dp.plot([], [], 'o', ms=4, color=CREAM, alpha=0.8)
Dp.plot(0, 0, 'o', ms=6, color=CREAM)
ang = np.radians(np.linspace(-wing, wing, 200))
Dp.plot(2.12 * np.sin(ang), 2.12 * np.cos(ang), color=WINE, lw=1, alpha=0.6)
Dp.text(2.15 * math.sin(math.radians(wing)) + 0.1, 2.15 * math.cos(math.radians(wing)), '±%.1f°' % wing, color=MUTED, fontsize=13, fontproperties=MONO)
countD = Dp.text(-3.4, -1.95, '', color=MUTED, fontsize=14, fontproperties=MONO)
clock = fig.text(0.97, 0.945, '', ha='right', fontproperties=MONO, fontsize=15, color=MUTED)
# the link across panels: from the tip in panel 1 to the tip in panel 4 (the same point, two frames)
link = matplotlib.lines.Line2D([], [], transform=fig.transFigure, ls=(0, (1, 4)), color=MUTED, lw=1, alpha=0.7)
fig.add_artist(link)

def at(t):
    return min(int(round(t / T * (tt.size - 1))), tt.size - 1)

frames_main = int(round(T / SLOW * FPS)); frames = frames_main + int(HOLD * FPS)
writer = FFMpegWriter(fps=FPS, codec='libx264', bitrate=12000, extra_args=['-pix_fmt', 'yuv420p'])
with writer.saving(fig, out, dpi=100):
    for f in range(frames):
        t = min(f / FPS * SLOW, T); i = at(t)
        x1, y1 = math.sin(th1[i]), math.cos(th1[i]); x, y = X[i], Y[i]
        rodA.set_data([0, x1, x], [0, y1, y]); jointA.set_data([x1], [y1])
        j0 = at(max(0, t - 0.25)); trailA.set_data(X[j0:i + 1], Y[j0:i + 1])
        rodB.set_data([0, x1, x], [0, y1, y]); armB.set_data([0, x], [0, y]); tipB.set_data([x], [y])
        psiB.set_position((0.15, -1.9)); psiB.set_text('r = %+.2f m' % r[i])
        h = math.cos(D[i] / 2); a = D[i] / 2
        ptC.set_data([math.sin(a)], [h]); radC.set_data([0, math.sin(a)], [0, h])
        k0 = at(max(0, t - T / 4)); seg = slice(k0, i + 1)
        xs = 1.6 + (t - tt[seg]) / (T / 4) * 4.3
        waveC.set_data(xs, np.cos(D[seg] / 2)); linkC.set_data([math.sin(a), 1.6], [h, h])
        traceD.set_data(X[:i + 1], Y[:i + 1]); armD.set_data([0, x], [0, y]); tipD.set_data([x], [y])
        n = int(np.searchsorted(tp, t, side='right')) - 1
        ph = phi[n]; handD.set_data([0, 2.12 * math.sin(ph)], [0, 2.12 * math.cos(ph)])
        petD.set_data(np.sin(phi[:n + 1]) * 2, np.cos(phi[:n + 1]) * 2)
        countD.set_text('petal %d of %d' % (n, N) if t < T else 'closed: %d petals in %.3f s' % (N, T))
        clock.set_text('t = %.3f s   (shown at %g× real speed)' % (t, SLOW) if t < T else 't = %.3f s · the butterfly closes' % T)
        pa = fig.transFigure.inverted().transform(A.transData.transform((x, y)))
        pd = fig.transFigure.inverted().transform(Dp.transData.transform((x, y)))
        link.set_data([pa[0], pd[0]], [pa[1], pd[1]])
        writer.grab_frame(facecolor=NIGHT)
        if f in (frames_main // 3, frames - 1):
            fig.savefig(out.replace('.mp4', '_f%04d.png' % f), facecolor=NIGHT)
print('wrote', out, frames, 'frames')

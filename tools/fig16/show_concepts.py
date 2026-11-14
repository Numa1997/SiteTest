"""Fig. 16: one picture of the three concepts. Top: each cart drawn to scale. Bottom: the kerb at 1.5 m/s, the stout's tilt over
time and the head spilled, each concept against Fig. 12's cart, from the design simulator (cart16.py). Writes notes/fig16/concepts.png."""
import os, numpy as np
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, Polygon, FancyBboxPatch
import concepts as CC, cart16 as C, spill as SP, sweep as S

HERE = os.path.dirname(os.path.abspath(__file__)); WINE = "#7a1f2b"
go = CC.SIMS[4.0][0]
runs = {}
for n in ["Fig. 12 cart, speed held", "A tray", "B gimbal", "C muscle"]:
    P = CC.concept(n); o, Pf = go(dict(P, vk=1.5), "one sharp 30 mm bump", 1.5); runs[n] = (o, SP.spill(o, S.WS))


def glass(ax, x0, y0, s=1.0, ang=0.0, px=None, py=None):
    # the tulip from its profile, 1 unit = 1 mm, rotated about (px, py)
    import slosh_model as SM
    z = np.arange(0, len(SM.GLASS_R), 10) * SM.DZP * 1e3; r = SM.GLASS_R[::10] * 1e3
    pts = np.c_[np.r_[r, -r[::-1]], np.r_[z, z[::-1]]] + [0, 14]
    pts = np.r_[[[-32, 0], [32, 0], [32, 14]], pts, [[-32, 14]]]
    beer = np.c_[np.r_[r[z <= 125], -r[z <= 125][::-1]], np.r_[z[z <= 125], z[z <= 125][::-1]]] + [0, 14]
    head = np.array([[-39, 125], [39, 125], [39, 144], [-39, 144]]) + [0, 14]
    for poly, fc, ec in ((beer, "#1a0e0a", "none"), (head, "#f1e6c8", "none"), (pts, "none", "#555")):
        p = poly.copy()
        if px is not None:
            c, s_ = np.cos(ang), np.sin(ang); d = p + [x0, y0] - [px, py]
            p = np.c_[c * d[:, 0] - s_ * d[:, 1], s_ * d[:, 0] + c * d[:, 1]] + [px, py]
        else: p = p + [x0, y0]
        ax.add_patch(Polygon(p, closed=True, fc=fc, ec=ec, lw=1.2))


def wheel(ax, x, r, y=0): ax.add_patch(Circle((x, y + r), r, fc="#333", ec="k")); ax.add_patch(Circle((x, y + r), r * 0.35, fc="#999"))


def body(ax, x, y, w, h, label=None):
    ax.add_patch(FancyBboxPatch((x - w / 2, y), w, h, boxstyle="round,pad=2", fc="#d9d4cc", ec="#555"))


def spring(ax, x, y0, y1, n=6):
    yy = np.linspace(y0, y1, 2 * n + 1); xx = x + 6 * np.array([0] + [(-1) ** k for k in range(2 * n - 1)] + [0]); ax.plot(xx, yy, color="#555", lw=1)


def motor(ax, x, y, big=False):
    ax.add_patch(Rectangle((x - (14 if big else 9), y), 28 if big else 18, 22 if big else 16, fc=WINE, ec="k"))


fig = plt.figure(figsize=(15, 10))
titles = {"A tray": "A · the tray\nglass hangs free from a bail, oil damper at the pivot\nFig. 12's motor (12 V, 3 A), softer tyre",
          "B gimbal": "B · the gimbal\na torque motor tilts the glass, IMU on the holder\n24 V, 10 A drive; load cell at the axle sees the bump",
          "C muscle": "C · the muscle\nglass fixed to the body\n100 mm soft wheel, 24 V, 10 A drive, load-cell preview"}
for k, n in enumerate(["A tray", "B gimbal", "C muscle"]):
    ax = fig.add_axes([0.03 + k * 0.33, 0.47, 0.30, 0.44]); ax.set_aspect("equal"); ax.axis("off"); ax.set_xlim(-160, 160); ax.set_ylim(-10, 470)
    ax.plot([-160, 160], [0, 0], color="k", lw=1)
    Rw = {"A tray": 40, "B gimbal": 60, "C muscle": 100}[n]
    wheel(ax, 0, Rw); spring(ax, -20, 2 * Rw, 2 * Rw + 55); spring(ax, 20, 2 * Rw, 2 * Rw + 55)
    by = 2 * Rw + 55; body(ax, 0, by, 220, 30); motor(ax, 45, Rw - 8, big=n != "A tray")
    ax.text(45, Rw - 20, "motor", ha="center", fontsize=8, family="monospace")
    if n == "C muscle":
        glass(ax, 0, by + 30); ax.text(85, by + 6, "load cell", fontsize=8, family="monospace")
    else:
        zp = 300 if n == "A tray" else 200; py = by + 30 + 14 + zp
        ax.plot([-95, -95, 95, 95], [by + 30, py + 20, py + 20, by + 30], color="#555", lw=3)                  # the frame
        ax.add_patch(Circle((0, py), 6, fc=WINE if n == "B gimbal" else "#999", ec="k", zorder=5))
        ax.plot([0, -45, -45], [py, py - 40, by + 44], color="#777", lw=1.5); ax.plot([0, 45, 45], [py, py - 40, by + 44], color="#777", lw=1.5)
        glass(ax, 0, by + 30, ang=np.radians(-6), px=0, py=py)
        ax.text(12, py + 4, "pivot" + (": torque motor" if n == "B gimbal" else ": damper"), fontsize=8, family="monospace")
        if n == "B gimbal": ax.text(50, py - 60, "IMU", fontsize=8, family="monospace", color=WINE)
    ax.set_title(titles[n], fontsize=10, loc="left")

ax1 = fig.add_axes([0.06, 0.07, 0.55, 0.33]); ax2 = fig.add_axes([0.68, 0.07, 0.29, 0.33])
sty = {"Fig. 12 cart, speed held": ("#999", 2.5), "A tray": ("#3b6ea5", 1.6), "B gimbal": (WINE, 2.2), "C muscle": ("#c08a2b", 1.6)}
for n, (o, V) in runs.items():
    c, lw = sty[n]; ax1.plot(o["t"], o["tilt"] * 1e3, color=c, lw=lw, label=n); ax2.plot(o["t"], V * 1e6, color=c, lw=lw)
ax1.set_xlim(0.5, 2.5); ax1.set_xlabel("time, s"); ax1.set_ylabel("tilt of the stout's surface, mm\n(front wall minus back)")
ax1.axhline(0, color="k", lw=0.5); ax1.legend(fontsize=9); ax1.grid(alpha=0.3)
ax1.set_title("The kerb (30 mm, 1.5 m/s): how far the stout tips in the glass", fontsize=10, loc="left")
ax2.set_xlim(0.5, 2.5); ax2.set_xlabel("time, s"); ax2.set_ylabel("head of foam spilled, mL"); ax2.grid(alpha=0.3)
ax2.set_title("Head spilled", fontsize=10, loc="left")
for n, (o, V) in runs.items(): ax2.text(2.45, V[-1] * 1e6 + 0.04, f"{V[-1] * 1e6:.2f}", ha="right", fontsize=8, color=sty[n][0])
plt.savefig(os.path.join(HERE, "..", "..", "notes", "fig16", "concepts.png"), dpi=90)

"""Fig. 16, spill derived from a stored ride, step 2 (19 Nov 2026): where the stored ride's spilled stout lands on Fig. 16's deck.
Kaggle CPU; nothing runs outside Kaggle. Dataset numakoudsie/fig16-guinness-cart-control attached.  python3 land_on_deck.py OUTDIR

THE PRINCIPLE (review of 19 Nov, notes/spill/FINDINGS-review-19-nov.md, section 6). The stored flight IS computed: a parcel in the air
has atmospheric pressure all round, so the full equation Dv/Dt = -grad p / rho + g reduces to free flight, which is what the old model
integrated. Only its LANDING is wrong for Fig. 16: it froze drops on Fig. 12's body plane (z = -14 mm, 220 x 120 mm) and let the rest
fall to -250 mm. Fig. 16's deck is z = -30 mm, 310 x 124 mm. No velocity is estimated and no formula is fitted; the stored positions
are used as they are.
- Drops frozen on the old body plane: that plane lies wholly inside the deck's outline (110 < 155 mm, 60 < 62 mm), so they would have
  fallen 16 mm more onto the deck. They are put on the deck at their stored (x, y). Error bound: their horizontal drift during a 16 mm
  fall, v_h sqrt(2 * 0.016 / g) = v_h * 57 ms, reported with v_h from the stored cloud.
- Drops that fell past the old body's edge: their crossings of the deck's plane are read from the stored pictures (drops between
  -33 and -27 mm, outside the old body's outline). Each picture's drops stand for ndrops / listed particles (the list is an even
  subsample); the crossing map is scaled to the stored fallen mass. A drop seen in the band in two pictures counts twice; the
  fall speed there (about 1.9 m/s after 177 mm) makes the band's 6 mm about 3 ms, under one picture (17 ms), so this is small.
OUTPUT: REPORT.md, report.json, deck_landing.png."""
import glob, json, os, sys
import numpy as np
OUT = sys.argv[1] if len(sys.argv) > 1 else "/kaggle/working"; os.makedirs(OUT, exist_ok=True)
RIDE = os.environ.get("RIDE", "kerb_off"); SUB = "fig-16-guinness-cart-with-control/v8/output/2026-11-15"
DECK = (0.155, 0.062, -0.030); OLD = (0.11, 0.06, -0.014); BAND = 0.003
MD = []; say = lambda s="": (print(s, flush=True), MD.append(s))
src = glob.glob(f"/kaggle/input/**/{SUB}/{RIDE}.npz", recursive=True)
if not src: say("STOP: stored ride not attached"); open(os.path.join(OUT, "REPORT.md"), "w").write("\n".join(MD)); sys.exit(1)
Z = np.load(src[0]); t = Z["t"]; nf = len(t); mp = float(Z["mp"]); N = int(Z["N"])
D = Z["drops"].astype(np.float64); nd = Z["ndrops"].astype(float); nst = Z["nstuck"].astype(float); nland = Z["nlanded"].astype(float)
say(f"# Fig. 16, ride `{RIDE}`: where the stored spill lands on Fig. 16's deck\n")
say(f"Stored: {(N - Z['nact'][-1]) * mp * 1e3:.1f} g over the rim; at the end {nst[-1] * mp * 1e3:.1f} g frozen on Fig. 12's body plane, {nland[-1] * mp * 1e3:.1f} g fallen past its edge.\n")

# frozen drops: the last picture's list (an even subsample)
L = D[-1]; L = L[np.isfinite(L).all(1)]
fr = L[np.abs(L[:, 2] - OLD[2]) < 4e-4]
in_old = (np.abs(fr[:, 0]) < OLD[0]) & (np.abs(fr[:, 1]) < OLD[1])
m_fr = nst[-1] * mp / max(len(fr), 1)

# falling drops crossing the deck's plane, outside the old body's outline
cx, cy, cw = [], [], []
for k in range(nf):
    Dk = D[k]; ok = np.isfinite(Dk).all(1); Dk = Dk[ok]
    if not len(Dk): continue
    w = nd[k] / len(Dk)                                              # particles each listed drop stands for
    b = (np.abs(Dk[:, 2] - DECK[2]) < BAND) & ~((np.abs(Dk[:, 0]) < OLD[0]) & (np.abs(Dk[:, 1]) < OLD[1]))
    cx.append(Dk[b, 0]); cy.append(Dk[b, 1]); cw.append(np.full(b.sum(), w))
cx, cy, cw = np.concatenate(cx), np.concatenate(cy), np.concatenate(cw)
scale = nland[-1] * mp / max(cw.sum(), 1e-30); mc = cw * scale         # kg per crossing, scaled to the stored fallen mass
on_c = (np.abs(cx) < DECK[0]) & (np.abs(cy) < DECK[1])

m_deck = len(fr) * m_fr + mc[on_c].sum(); m_off = mc[~on_c].sum()
front = lambda x, m: float(m[x > 0].sum() / max(m.sum(), 1e-30))
rep = dict(frozen_on_old_plane_g=nst[-1] * mp * 1e3, frozen_listed=int(len(fr)), frozen_all_inside_old_outline=bool(in_old.all()),
           fell_past_old_edge_g=nland[-1] * mp * 1e3, crossings_listed=int(len(cx)), crossing_weight_scale=float(scale / mp),
           from_fallen_on_deck_g=float(mc[on_c].sum() * 1e3), from_fallen_off_deck_g=float(m_off * 1e3),
           on_deck_g=float(m_deck * 1e3), off_deck_g=float(m_off * 1e3),
           off_front_g=float(mc[~on_c & (cx > DECK[0])].sum() * 1e3), off_back_g=float(mc[~on_c & (cx < -DECK[0])].sum() * 1e3),
           off_sides_g=float(mc[~on_c & (np.abs(cx) <= DECK[0])].sum() * 1e3))
say("| | mass (g) |\n|---|---|")
say(f"| frozen on Fig. 12's plane, put on the deck below it | {rep['frozen_on_old_plane_g']:.1f} |")
say(f"| fell past Fig. 12's edge, crossing Fig. 16's deck plane ON the deck | {rep['from_fallen_on_deck_g']:.1f} |")
say(f"| fell past Fig. 12's edge, crossing Fig. 16's deck plane OFF the deck | {rep['from_fallen_off_deck_g']:.1f} (front {rep['off_front_g']:.1f}, back {rep['off_back_g']:.1f}, sides {rep['off_sides_g']:.1f}) |")
say(f"| **on Fig. 16's deck** | **{rep['on_deck_g']:.1f}** |")
say(f"| **off the deck, to the floor** | **{rep['off_deck_g']:.1f}** |")
say(f"\nChecks: every frozen drop lies inside Fig. 12's outline: {rep['frozen_all_inside_old_outline']}; listed crossings {len(cx):,}.")
json.dump(rep, open(os.path.join(OUT, "report.json"), "w"), indent=1, default=float)
try:
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(8.5, 4))
    ax.scatter(fr[:, 0] * 1e3, fr[:, 1] * 1e3, s=1, c="k", alpha=0.35, label="frozen on Fig. 12's plane -> deck")
    ax.scatter(cx[on_c] * 1e3, cy[on_c] * 1e3, s=2, c="tab:blue", label="falling, crosses the deck's plane on the deck")
    ax.scatter(cx[~on_c] * 1e3, cy[~on_c] * 1e3, s=2, c="tab:red", label="falling, misses the deck")
    ax.add_patch(plt.Rectangle((-DECK[0] * 1e3, -DECK[1] * 1e3), 2e3 * DECK[0], 2e3 * DECK[1], fill=False, lw=1.6, label="Fig. 16 deck"))
    ax.add_patch(plt.Rectangle((-OLD[0] * 1e3, -OLD[1] * 1e3), 2e3 * OLD[0], 2e3 * OLD[1], fill=False, lw=1, ls="--", label="Fig. 12 body"))
    ax.set_aspect("equal"); ax.set_xlim(-400, 400); ax.set_ylim(-180, 180); ax.set_xlabel("x along the road (mm)"); ax.set_ylabel("y (mm)")
    ax.legend(fontsize=7, markerscale=5, loc="upper left"); ax.set_title(f"{RIDE}: where the stored spill comes down on Fig. 16's deck")
    fig.tight_layout(); fig.savefig(os.path.join(OUT, "deck_landing.png"), dpi=130); plt.close(fig)
except Exception as e: say(f"figure failed: {e}")
open(os.path.join(OUT, "REPORT.md"), "w").write("\n".join(MD) + "\n")

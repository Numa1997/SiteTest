"""Fig. 16 on Kaggle's CPU (no GPU quota): the natural modes of the four-wheel cart with its control system OFF, from the cart's own
linear model (cart4.linear_model: cart, deck heave and pitch, two axles, the stout's first sloshing mode with the head, about steady
cruising), at 1.0 and 1.5 m/s. Question (audit item I): is the uncontrolled cart's pitch in resonance with the stout?
Writes /kaggle/working/modes/modes.json: per speed, every oscillating mode's frequency (Hz), damping ratio and the share of the
deck's pitch, heave, the axles and the stout's swing in it (energy-free measure: |component| of the eigenvector scaled so that each
coordinate is in its natural unit: m for heights, rad x 0.11 m (a corner's rise) for the pitch, m at the wall for the swing); and
the wheelbase filter of each road: a road profile that repeats at f lifts the rear axle tau = wb / v after the front, so it drives the
pitch by |2 sin(pi f tau)| and the heave by |2 cos(pi f tau)|, relative to one axle alone."""
import os, json, math
import numpy as np
import cart4 as C4, slosh_model as SM

OUT = "/kaggle/working/modes"; os.makedirs(OUT, exist_ok=True)
P = dict(C4.CART4); ml = SM.liquid_mass(); S = C4.statics(P, ml)
names = ["dv", "xi", "zc", "vzc", "th", "om", "zf", "vzf", "zr", "vzr", "q", "qd"]
scale = dict(zc=1.0, th=P["af"], zf=1.0, zr=1.0, q=1.0)        # pitch as the rise of a corner 0.11 m from the centre
res = dict(ml_kg=ml, J_kgm2=S["J"], Ms_kg=S["Ms"], wheelbase_m=P["af"] + P["ar"], speeds=[])
for v0 in (1.0, 1.5):
    A, B, E = C4.linear_model(P, S, v0)
    lam, V = np.linalg.eig(A); modes = []
    for j in np.argsort(np.abs(lam.imag)):
        l = lam[j]
        if l.imag <= 1e-6: continue                              # one of each complex pair, oscillating modes only
        vec = V[:, j]; amp = {k: abs(vec[names.index(k)]) * s for k, s in scale.items()}; tot = sum(amp.values())
        modes.append(dict(f_hz=round(abs(l.imag) / (2 * math.pi), 3), zeta=round(-l.real / abs(l), 3),
                          share={k: round(a / tot, 3) for k, a in amp.items()}))
    roads = {}
    for name, f in (("five 20 mm bumps (0.29 m apart)", v0 / 0.29), ("stout's swing with the head (2.915 Hz)", C4.PLANT_F0), ("bare stout (3.42 Hz)", 3.42)):
        tau = (P["af"] + P["ar"]) / v0
        roads[name] = dict(f_hz=round(f, 3), pitch_drive=round(abs(2 * math.sin(math.pi * f * tau)), 3), heave_drive=round(abs(2 * math.cos(math.pi * f * tau)), 3))
    res["speeds"].append(dict(v0=v0, modes=modes, wheelbase_filter=roads))
    print(f"v0 = {v0} m/s"); [print("  ", m) for m in modes]; [print("  ", k, r) for k, r in roads.items()]
json.dump(res, open(os.path.join(OUT, "modes.json"), "w"), indent=1)
print("written", os.path.join(OUT, "modes.json"))

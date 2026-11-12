"""Fig. 14: what classical particles would do. An ensemble drawn from the packet's own spreads (positions around
(x0, 0, 0) with standard deviation sigma0 on each axis, wave numbers around (k0, 0, 0) with 1/(2 sigma0)): that is the
Wigner distribution of the starting Gaussian, which is a true probability distribution. Each particle flies straight;
at the sphere's surface the tangential momentum is kept and the energy is kept, so it enters (refracted) if its normal
kinetic energy exceeds V0 and is reflected otherwise; leaving, it speeds up again. Counted at the stored run's end time.
Usage: python3 notes/fig14/classical.py"""
import numpy as np, json, sys
sys.path.insert(0, '/home/user/SiteTest/notes/fig14')
from runs import IDX, find
rng = np.random.default_rng(14)
def t_end(E):
    k0 = np.sqrt(2 * E); steps = int(round(30 / k0 / 0.01)); per = max(1, steps // 47); return per * 47 * 0.01
def hit(p, v, R, inside):
    """time to the sphere surface along p + v t (nan if none ahead)"""
    a = (v * v).sum(1); b = 2 * (p * v).sum(1); c = (p * p).sum(1) - R * R
    disc = b * b - 4 * a * c; ok = disc > 0; sq = np.sqrt(np.where(ok, disc, 0))
    t1 = (-b - sq) / (2 * a); t2 = (-b + sq) / (2 * a)
    t = np.where(inside, t2, t1); t = np.where(ok & (t > 1e-12), t, np.nan); return t
def ensemble(E, V0, R, n=400000, s0=3.0, x0=-14.0):
    k0 = np.sqrt(2 * E); T = t_end(E)
    p = rng.normal(0, s0, (n, 3)); p[:, 0] += x0
    v = rng.normal(0, 1 / (2 * s0), (n, 3)); v[:, 0] += k0
    inside = (p * p).sum(1) < R * R
    tl = np.full(n, T); above = 0.5 * (v * v).sum(1) > V0
    for _ in range(4):
        th = hit(p, v, R, inside); go = ~np.isnan(th) & (th < tl)
        step = np.where(go, th, tl); p = p + v * step[:, None]; tl = tl - step
        if not go.any(): break
        nrm = p[go] / R; vn = (v[go] * nrm).sum(1); vt = v[go] - vn[:, None] * nrm; ins = inside[go]
        # outside going in (vn < 0)
        enter = ~ins & (0.5 * vn * vn > V0); refl = ~ins & ~enter
        vn_new = np.where(enter, -np.sqrt(np.maximum(vn * vn - 2 * V0, 0)), np.where(refl, -vn, np.sqrt(vn * vn + 2 * V0)))
        v[go] = vt + vn_new[:, None] * nrm
        inside_go = inside[go]; inside_go = np.where(enter, True, np.where(refl, False, False)); inside[go] = inside_go
        p[go] = p[go] + v[go] * 1e-9
    x = p[:, 0]; border = (np.abs(p) > 26).any(1)
    return dict(behind=float((x < -R).mean()), ahead=float((x > R).mean()), inside=float((np.abs(x) <= R).mean()),
                past_border=float(border.mean()), above=float(above.mean()), t=T,
                aimed=float(((p[:, 1]**2 + p[:, 2]**2) < R * R).mean()))
out = {}
cases = [(2.5, 3, 4), (2.0, 3, 4), (2.5, 0, 4), (0.5, 8, 6), (4.5, 4, 2), (1.0, 3, 4)] + [(2.5, v, R) for R in (2, 4, 6) for v in IDX['Vs']]
for (E, V, R) in cases:
    c = ensemble(E, V, R); r = find(E, V, R); c['q_behind'] = r['behind']; c['q_ahead'] = r['ahead']; c['q_lost'] = round(1 - r['norm_end'], 6)
    out[f'{E}_{V}_{R}'] = c
    print('E=%g V0=%g R=%g t=%.2f  classical behind %.4f ahead %.4f inside %.4f past border %.4f | above V0 %.4f | quantum behind %.4f ahead %.4f lost %.4f' % (
        E, V, R, c['t'], c['behind'], c['ahead'], c['inside'], c['past_border'], c['above'], r['behind'], r['ahead'], c['q_lost']))
# fraction aimed at the disc (impact parameter b < R) at the start
for R in (2, 4, 6):
    y = rng.normal(0, 3, (400000, 2)); print('aimed at disc R=%g: %.4f (formula %.4f)' % (R, ((y**2).sum(1) < R * R).mean(), 1 - np.exp(-R * R / 18)))
json.dump(out, open('/home/user/SiteTest/notes/fig14/classical.json', 'w'), indent=1)

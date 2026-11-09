"""Parity of physics/ch02.js (browser solver) and ref/ch02.py (NumPy reference): same inputs, relative difference printed.
    python3 notes/electron-beam/ch02/check_parity.py        (needs node on the path)"""
import json, math, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); EB = os.path.abspath(os.path.join(HERE, '..', '..', '..', 'portfolios-src', 'electron-beam'))
sys.path.insert(0, os.path.join(EB, 'ref'))
import ch02 as R
eV = R.eV
CASES = [  # F V/m, phi eV, T K
    (4e9, 4.5, 300), (5e9, 4.5, 300), (3e9, 4.5, 300), (5e8, 2.9, 1800), (8e8, 2.9, 1800), (1e8, 4.5, 2800), (3e9, 4.5, 1500)]
js = r"""
await import(process.argv[1]); const P = globalThis.EB_CH02, eV = P.K.e, out = {};
const cases = JSON.parse(process.argv[2]);
out.model = cases.map(([F, phi, T]) => { const m = P.emissionModel(F, phi * eV, T); return {J: m.J, Jc: m.Jcheck, Br: m.B_r, fwhm: m.fwhm, met: m.meanEt, peak: m.peak, jt0: m.jt0, regime: m.regime}; });
out.v = [0.05, 0.2, 0.284, 0.5, 0.9].map(f => [P.vExact(f), P.vForbes(f), P.tForbes(f)]);
out.fn = cases.map(([F, phi, T]) => P.jFN(F, phi * eV, T));
out.tip = [[1000, 50e-9, 5, 4.5 * eV, 300], [1500, 130e-9, 5, 4.5 * eV, 300]].map(([V, r, k, phi, T]) => P.tipCurrent(V, {r, k, phi, T}));
out.ho = (h => [h.I_e, h.B_r, h.dE, h.d_v])(P.handover({V: 1000, r: 50e-9, k: 5, phi: 4.5 * eV, T: 300}));
out.hk = [P.hkFlux(1e-9, 300, 28), P.hkFlux(1e-8, 300, 2.016)];
const a = P.hkFlux(1e-9, 300, 28) * 1 / 1e19, kd = P.kDes(1.9, 700);
out.cov = [P.coverageStep(0.01, 100, a, kd), P.timeToCoverage(0.1, a, 0), P.kDes(1.9, 300)];
const c = P.cycle({pPa: 1e-8, Tg: 300, mu: 2.016, Ns: 1e19, s: 0.5, kappa: 1, Ed: 1.9, T: 300, Tflash: 900, tflash: 5, thr: 0.7, theta0: 0, rho: 0.0, tmax: 7200, dt: 1});
out.cyc = [c.flashes.length, c.flashes[0], c.theta[c.theta.length - 1]];
console.log(JSON.stringify(out));
"""
res = json.loads(subprocess.check_output(['node', '--input-type=module', '-e', js, '--', os.path.join(EB, 'physics', 'ch02.js'), json.dumps(CASES)], text=True))
worst = 0.0
def cmp(name, a, b):
    global worst
    rel = abs(a - b) / max(abs(b), 1e-300); worst = max(worst, rel)
    print(f'{name:34s} js={a:.10e} py={b:.10e} rel={rel:.1e}')
for (F, phi, T), j in zip(CASES, res['model']):
    m = R.emission_model(F, phi * eV, T); tag = f'F={F:.0e} phi={phi} T={T}'
    for k, a, b in (('J', j['J'], m['J']), ('B_r', j['Br'], m['B_r']), ('FWHM', j['fwhm'], m['fwhm']), ('<Et>', j['met'], m['mean_et']), ('J_check', j['Jc'], m['J_check'])):
        cmp(f'{tag} {k}', a, b)
    assert j['regime'] == m['regime'], (j['regime'], m['regime'])
for f, (ve, vf, tf) in zip((0.05, 0.2, 0.284, 0.5, 0.9), res['v']):
    cmp(f'v_exact({f})', ve, R.v_exact(f)); cmp(f'v_F06({f})', vf, R.v_forbes(f)); cmp(f't_F({f})', tf, R.t_forbes(f))
for (F, phi, T), a in zip(CASES, res['fn']):
    b = R.j_fn(F, phi * eV, T)
    if a is None or not math.isfinite(b): assert a is None and not math.isfinite(b), (a, b); print(f'J_FN F={F:.0e} T={T}: both undefined (outside the regime of the formula)')
    else: cmp(f'J_FN F={F:.0e} T={T}', a, b)
for (V, r, k, phi, T), a in zip([(1000, 50e-9, 5, 4.5 * eV, 300), (1500, 130e-9, 5, 4.5 * eV, 300)], res['tip']):
    cmp(f'tip current V={V}', a, R.tip_current(V, r, k, phi, T))
h = R.handover(1000, 50e-9, 5, 4.5 * eV, 300)
for n, a, b in zip(('I_e', 'B_r', 'dE', 'd_v'), res['ho'], (h['I_e'], h['B_r'], h['dE'], h['d_v'])): cmp('handover ' + n, a, b)
cmp('hk flux CO 1e-9', res['hk'][0], R.hk_flux(1e-9, 300, 28)); cmp('hk flux H2 1e-8', res['hk'][1], R.hk_flux(1e-8, 300, 2.016))
a = R.hk_flux(1e-9, 300, 28) / 1e19; kd = R.k_des(1.9, 700)
cmp('coverage step', res['cov'][0], R.coverage_step(0.01, 100, a, kd)); cmp('time to 10 %', res['cov'][1], R.time_to_coverage(0.1, a, 0.0)); cmp('k_des 300 K', res['cov'][2], R.k_des(1.9, 300))
c = R.cycle(1e-8, 300, 2.016, 1e19, 0.5, 1, 1.9, 300, 900, 5, 0.7, 0, 0.0, 7200, 1)
print('cycle flashes js/py', res['cyc'][0], len(c['flashes']), ' first flash t', res['cyc'][1], c['flashes'][0] if c['flashes'] else None)
assert res['cyc'][0] == len(c['flashes']) and abs(res['cyc'][1] - c['flashes'][0]) < 1e-9
print(f'WORST relative difference: {worst:.2e}'); sys.exit(0 if worst < 1e-8 else 1)

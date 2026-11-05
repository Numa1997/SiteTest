"""Compare the page's controller with the offline reference: gains K (same data, same cost), the closed-loop time constant, and
the bump runs. python3 tools/fig12/gate_ctl3.py out.json [slosh-modes.js]"""
import sys, os, json, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import controller3 as C, plant
pg = json.load(open(sys.argv[1])); mpath = sys.argv[2] if len(sys.argv) > 2 else 'public/scripts/slosh-modes.js'
data = C.load_modes(mpath); fill = [f for f in data['fills'] if f['V_mL'] == pg['V']][0]
rho, sigma, M_f, nu, g = 1007.0, 0.045, 0.15 * 1007.0 * 0.018, 2.06e-3 / 1007.0, 9.81
def gamma_fn(md):
    lam = md['lam']; kappa = M_f * lam / rho; w = np.sqrt((g * lam + sigma * lam ** 3 / rho) / (1 + kappa)); sq = 0.5 * np.sqrt(nu * w / 2)
    return sq * (md['Iw'] + md['Ib']) + sq * md['Is'] + 2 * nu * lam ** 2 + 0.05 + (0.016 / fill['a']) * (1 - np.exp(-lam * 0.018))
modes = plant.modal_params(fill, rho, sigma, M_f, gamma_fn)
for md, raw in zip(modes['x'], [m for m in fill['modes'] if m['m'] == 1 and m['o'] == 'c']): md['rim_front'] = sum(raw['psi'][k][0][-1] for k in raw['psi'])
P = dict(plant.DEFAULT); P['I_max'] = pg['Imax']; P['Bl'] = pg['Bl']
D = C.design(P, fill, modes, rho, Ts=pg['Ts'], s_eta=pg['se'], s_psi=pg['sp'], s_v=pg['sv'], s_u=pg['su'])
K = np.array(pg['K']); ok = True
rel = np.abs(K - D['K_sub']).max() / np.abs(D['K_sub']).max(); print(f'gains: page vs offline, max rel diff {rel:.1e} (n = {pg["n"]}, {pg["iters"]} iterations on the page)')
if rel > 1e-6: ok = False
print(f'tau_cl: page {pg["tau"]:.5f} s, offline {D["tau"]:.5f} s')
if abs(pg['tau'] - D['tau']) > 1e-4 * D['tau']: ok = False
for law in ('passive', 'skyhook', 'lqr'):
    o = C.simulate(D, P, 'bump', v=pg['v'], T=6.0, law=law)
    pk = np.abs(o['eta']).max(); r = pg['runs'][law]
    print(f'  bump, {law:8s}: peak rim wave page {r["peak"]*1e3:6.2f} mm, offline {pk*1e3:6.2f} mm; max |u| page {r["maxU"]:6.1f} N, offline {np.abs(o["u"]).max():6.1f} N')
print('PASS' if ok else 'FAIL'); sys.exit(0 if ok else 1)

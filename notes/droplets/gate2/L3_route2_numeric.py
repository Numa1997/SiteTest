"""Gate 2, level L3 (chapter 4), route 2 (numerical, NumPy): (4.1) by an explicit perfectly-inelastic collision; (4.2) example numbers
with an independently coded surface tension (IAPWS 2014: sigma = 235.8e-3 tau^1.256 (1 - 0.625 tau), tau = 1 - T/647.096 K)."""
import numpy as np, json
rng = np.random.default_rng(3)
print('== (4.1) random masses and 3-D velocities: energy lost in a perfect merger (momentum conservation gives the final velocity)')
worst = 0
for _ in range(100000):
    m1, m2 = rng.uniform(0.1, 10, 2); v1, v2 = rng.normal(size=3) * 5, rng.normal(size=3) * 5
    KE0 = 0.5 * m1 * v1 @ v1 + 0.5 * m2 * v2 @ v2
    vf = (m1 * v1 + m2 * v2) / (m1 + m2)                     # momentum conserved
    lost = KE0 - 0.5 * (m1 + m2) * vf @ vf
    cke = 0.5 * (m1 * m2 / (m1 + m2)) * (v1 - v2) @ (v1 - v2)
    V = (m1 * v1 + m2 * v2) / (m1 + m2)
    split = 0.5 * (m1 + m2) * V @ V + cke
    worst = max(worst, abs(lost - cke) / max(cke, 1e-30), abs(KE0 - split) / KE0)
print('   max relative deviation over 1e5 random cases (merger loss vs mu dv^2/2 ; KE vs M V^2/2 + mu dv^2/2): %.2e' % worst)
# 1-D elastic/inelastic check including a rebound: CKE is the part of KE that can be lost; elastic rebound loses none, merger loses all of it
m1, m2, u1, u2 = 2.0, 3.0, 4.0, -1.0
cke = 0.5 * m1 * m2 / (m1 + m2) * (u1 - u2)**2
vf = (m1 * u1 + m2 * u2) / (m1 + m2)
print('   1-D example m=(2,3), u=(4,-1): CKE = %.4f ; KE before %.4f ; KE after merger %.4f ; lost %.4f' % (cke, 0.5 * m1 * u1**2 + 0.5 * m2 * u2**2, 0.5 * (m1 + m2) * vf**2, 0.5 * m1 * u1**2 + 0.5 * m2 * u2**2 - 0.5 * (m1 + m2) * vf**2))

D = json.load(open('L3_model_dump.json'))
def sigma_iapws(T): tau = 1 - T / 647.096; return 0.2358 * tau**1.256 * (1 - 0.625 * tau)
rho_w = 1000.0
def We_of(a1, a2, dv, sigma):
    m1 = 4 / 3 * np.pi * rho_w * a1**3; m2 = 4 / 3 * np.pi * rho_w * a2**3
    cke = 0.5 * m1 * m2 / (m1 + m2) * dv**2
    dc = ((2 * a1)**3 + (2 * a2)**3)**(1 / 3)
    return cke, cke / (np.pi * sigma * dc**2)
print('== (4.2) example numbers (radii in um; fall speeds from the model: inputs)')
for name in ['cloud', 'std20']:
    d = D[name]; sg = sigma_iapws(d['T']); print('  air %s: T = %.2f K, sigma (own IAPWS) = %.5f N/m, model sigmaWater = %.5f' % (name, d['T'], sg, d['sigma_model']))
    for (a1, a2, lab) in [(40, 8, '8 um on 40 um (text: CKE 3.0e-14 J, We 2.0e-5, E 0.99998)'), (60, 50, 'collectors 60 and 50 um (text We 2.9e-4)'), (500, 250, 'radii 500 and 250 um (text We 0.52, E 0.55, dv 2.1 m/s; Stokes dv 23 m/s, We 61)')]:
        for law in ['B', 'S']:
            dv = abs(d['v'][str(a1)][law] - d['v'][str(a2)][law]); cke, We = We_of(a1 * 1e-6, a2 * 1e-6, dv, sg)
            print('   %-9s %s dv = %9.5f m/s CKE = %.3e J  We = %.3e  E_coal = exp(-1.15 We) = %.6g   [%s]' % (name, 'drag balance' if law == 'B' else 'Stokes      ', dv, cke, We, np.exp(-1.15 * We), lab if law == 'B' else ''))

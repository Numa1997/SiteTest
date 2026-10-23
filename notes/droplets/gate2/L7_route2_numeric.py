"""Gate 2, level L7 (chapter 8), route 2 (numerical, NumPy/SciPy): (8.1) pair counting by simulation; (8.2) own evaluation with the coefficients of
Sotiropoulou et al. (2021) Appendix B (eq. B5, B8), the soft-hit limit, and the table of the text from data/cold.json (model output, read only)."""
import json, numpy as np
rng = np.random.default_rng(8)
print('== (8.1) events per volume and time for two kinds + one self-colliding kind, uniform kernel K, volume V = 1: simulate the pair clocks')
K, V = 0.7, 1.0; N1, N2, N3 = 40, 60, 50
rate_formula = K * N1 * N2 / V + K * N3 * (N3 - 1) / 2 / V
T = 2000.0
# every unordered pair carries an independent Poisson clock of rate K/V: total events in T ~ Poisson(pairs K T/V)
pairs = N1 * N2 + N3 * (N3 - 1) // 2
ev = rng.poisson(pairs * K / V * T, size=20)
print('   pairs = %d ; simulated rate %.2f +- %.2f per unit time ; K n1 n2 + (1/2) K n3^2 (1 - 1/N3) = %.2f ; naive ordered double sum over N3 would give %.2f' % (pairs, ev.mean() / T, ev.std() / T / np.sqrt(20), rate_formula, K * N1 * N2 + K * N3 * (N3 - 1)))
print('   (8.1) is a sum over unordered pairs: for two different kinds K n1 n2, for one kind (1/2) K n^2, as the model code does (i == j gets 1/2).')

print('== (8.2) with the coefficients of Sotiropoulou et al. 2021, Appendix B (graupel-graupel, eq. B8): a0 = 3.78e4 (1 + 0.0079/D^1.5), A = a0/3 + max(2 a0/3 - a0 |T-258|/9, 0), C = 6.3e6 psi (psi = 3.5e-3 or 1), gamma = 0.3, F_max = 100')
def A_of(D, T): a0 = 3.78e4 * (1 + 0.0079 / D**1.5); return a0 / 3 + max(2 * a0 / 3 - a0 * abs(T - 258) / 9, 0)
def Fbr(K0, D, Dclamp, T, C, gamma=0.3):
    alpha = np.pi * D**2; A = A_of(Dclamp, T); x = C * K0 / (alpha * A)
    return min(100.0, alpha * A * (1 - np.exp(-x**gamma))), alpha * A, x
rho_i = 900.0; mass = lambda r: 4 / 3 * np.pi * r**3 * rho_i
m1, m2 = mass(40e-6), mass(8e-6); v1, v2 = 0.1726, 0.0076
K0 = 0.5 * m1 * m2 / (m1 + m2) * (v1 - v2)**2
F, aA, x = Fbr(K0, 16e-6, 5e-4, 263.15, 6.3e6)
print('   worked example: K0 = %.3e J ; alpha A = %.3e ; x = %.3e ; F = %.3e (text 3.4e-4)' % (K0, aA, x, F))
F2, _, _ = Fbr(K0, 16e-6, 5e-4, 263.15, 6.3e6 * 3.5e-3)
print('   psi = 3.5e-3 (C = 2.2e4): F = %.3e ; fragments per collision in the soft limit scale as C^0.3: ratio %.2f (= %.2f)' % (F2, F / F2, (1 / 3.5e-3)**0.3))
print('   soft-hit limit: F / (alpha A x^0.3) for x = 1e-12 ... 1e-2 :', ['%.4f' % (Fbr(1.0 * xx * aA / 6.3e6, 16e-6, 5e-4, 263.15, 6.3e6)[0] / (aA * xx**0.3)) for xx in (1e-12, 1e-8, 1e-5, 1e-3, 1e-2)])
print('   hard-hit limit: F / alpha A for x = 1e2 ... 1e8 (cap F_max = 100 not reached here):', ['%.5f' % (Fbr(xx * aA / 6.3e6, 16e-6, 5e-4, 263.15, 6.3e6)[0] / aA) for xx in (1e2, 1e4, 1e8)])
print('   energy scaling in the soft regime: local exponent d ln F / d ln K0 at K0 = 2.6e-14 J: %.4f (gamma = 0.3)' % ((np.log(Fbr(K0 * 1.001, 16e-6, 5e-4, 263.15, 6.3e6)[0]) - np.log(Fbr(K0 / 1.001, 16e-6, 5e-4, 263.15, 6.3e6)[0])) / (np.log(1.001) - np.log(1 / 1.001))))
print('   with the true diameter in A (D = 16 um, outside the fitted range) at K0 = 2.6e-14: F = %.3e' % Fbr(K0, 16e-6, 16e-6, 263.15, 6.3e6)[0])
print('   Mizuno-type correction used in the source\'s own implementation, dv = (1.7 (u1-u2)^2 + 0.3 u1 u2)^(1/2) instead of u1 - u2: dv = %.4f vs %.4f ; K0 x %.2f ; F x %.2f' % (np.sqrt(1.7 * (v1 - v2)**2 + 0.3 * v1 * v2), v1 - v2, (1.7 * (v1 - v2)**2 + 0.3 * v1 * v2) / (v1 - v2)**2, ((1.7 * (v1 - v2)**2 + 0.3 * v1 * v2) / (v1 - v2)**2)**0.3))

print('== rough energy scale of the collisions the law was fitted to (ice spheres 900 kg/m3, D = 0.5 to 5 mm; fall speeds from a Schiller-Naumann drag balance, own estimate)')
from scipy.optimize import brentq
rho_a, mu_a, g = 0.8, 1.7e-5, 9.81
def vt(D):
    f = lambda v: 4 / 3 * np.pi * (D / 2)**3 * (rho_i - rho_a) * g - 0.5 * rho_a * v**2 * np.pi * (D / 2)**2 * (24 / (rho_a * v * D / mu_a) * (1 + 0.15 * (rho_a * v * D / mu_a)**0.687) if v * D > 0 else 0)
    return brentq(f, 1e-4, 100)
Ks = []
for D1 in (0.5e-3, 1e-3, 2e-3, 5e-3):
    for D2 in (0.5e-3, 1e-3, 2e-3, 5e-3):
        if D2 > D1 * 0.5: continue
        m_a, m_b = mass(D1 / 2), mass(D2 / 2); dv = vt(D1) - vt(D2); Ks.append((0.5 * m_a * m_b / (m_a + m_b) * dv**2, D1, D2, dv))
Ks.sort()
for k0, D1, D2, dv in Ks: print('   D = %.1f and %.1f mm : dv = %.2f m/s, K0 = %.2e J' % (D1 * 1e3, D2 * 1e3, dv, k0))
lo, hi = 1.3e-14, 2.3e-13
print('   cloud collisions 1.3e-14 .. 2.3e-13 J; ratio of these fitted-range energies to the cloud ones: from %.1f to %.1f orders of magnitude (text: "eight to twelve")' % (np.log10(Ks[0][0] / hi), np.log10(Ks[-1][0] / lo)))

print('== the table of 8.3 from data/cold.json (model output, read only)')
C = json.load(open('/home/user/SiteTest/portfolios-src/droplets/data/cold.json')); pm = lambda x: x * 60 / 1e6
print('   liquid %.1f ice %.1f cm^-3 ; ice-ice collisions %.3f ; rime events with liquid >= 25 um radius %.3f (text 2.88 and 2.80, 2.799 of 2.803 with the drop the larger partner)' % (C['liquid'] / 1e6, C['ice'] / 1e6, pm(C['ii']), pm(C['rime25'])))
print('   rime25big %.3f of rime25 %.3f ; shattering 0 .. %.2f (text 0 to 4.8)' % (pm(C['rime25big']), pm(C['rime25']), pm(C['shatter'][1])))
print('   breakup clamped D: %.2e (psi 3.5e-3) .. %.2e (psi 1)  (text 3.0e-4 to 1.6e-3) ; true D: %.3f (text 0.050) ; old rule %.2f (text 2.6)' % (pm(C['fragLo']), pm(C['fragHi']), pm(C['fragTrueD']), pm(C['oldRule'])))
print('   old rule / breakup: %.0f (text 1600) and %.0f (text 52)' % (C['oldRule'] / C['fragHi'], C['oldRule'] / C['fragTrueD']))
print('   collision energies 5/50/95 %%: %s J (text 1.3e-14 to 2.3e-13 for 5 and 95 %%)' % ['%.1e' % q for q in C['K0q']])
print('   mean fragments per ice-ice collision: clamped %.2e (psi 1), %.2e (psi 3.5e-3) ; consistency with F of the worked example 3.4e-4: same order' % (C['fragHi'] / C['ii'], C['fragLo'] / C['ii']))

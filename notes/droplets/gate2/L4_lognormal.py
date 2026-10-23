"""Gate 2, L4 supplementary: the initial water fraction above 40 um (text 5.1: 20.09 %) from the two lognormal modes, analytically (scipy.stats.norm)."""
import numpy as np
from scipy.stats import norm
modes = [dict(N=300e6, rg=8e-6, sg=1.25), dict(N=1e6, rg=40e-6, sg=1.2)]
def mass_above(md, r0):
    ls = np.log(md['sg']); M = md['N'] * 4 / 3 * np.pi * 1000 * md['rg']**3 * np.exp(4.5 * ls**2)      # lognormal third moment
    return M, M * norm.sf((np.log(r0 / md['rg']) - 3 * ls**2) / ls)                                    # mass-weighted lognormal is lognormal with ln r shifted by 3 ln^2 sg
tot = sum(mass_above(m, 40e-6)[0] for m in modes); ab = sum(mass_above(m, 40e-6)[1] for m in modes)
print('analytic: total water = %.4f g/m3 ; above 40 um = %.4f g/m3 ; fraction = %.4f %% (text 20.09 %%)' % (tot * 1e3, ab * 1e3, 100 * ab / tot))
# brute-force check of the closed form by quadrature in ln r
from scipy.integrate import quad
def dm(lnr, md): ls = np.log(md['sg']); r = np.exp(lnr); return md['N'] / (np.sqrt(2 * np.pi) * ls) * np.exp(-(lnr - np.log(md['rg']))**2 / (2 * ls**2)) * 4 / 3 * np.pi * 1000 * r**3
tq = sum(quad(dm, np.log(1e-7), np.log(1e-2), args=(m,), limit=500)[0] for m in modes); aq = sum(quad(dm, np.log(40e-6), np.log(1e-2), args=(m,), limit=500)[0] for m in modes)
print('quadrature in ln r: fraction = %.4f %%' % (100 * aq / tq))

# Golovin test, text 5.3: "mass error -4.58e-7 is exactly the water the exponential puts below the grid's first bin"
mbar = 4 / 3 * np.pi * 1000 * (10e-6)**3; x0 = 4 / 3 * np.pi * 1000 * (1e-6)**3
for s in (2, 4, 8, 16):
    ue = x0 * 2**(-1 / (2 * s)) / mbar           # lower edge of bin 0 if bins are centred on x_k = x0 2^(k/s) (geometric half-width)
    print('mass fraction of exp(-m/mbar) below the lower edge of bin 0, s = %2d bins/doubling: %.3e  (u_edge = %.4e)' % (s, 1 - (1 + ue) * np.exp(-ue), ue))
print('(text: -4.58e-7; matches s = 8, which is the grid of the warm-cloud runs; the text does not say which s the number belongs to)')

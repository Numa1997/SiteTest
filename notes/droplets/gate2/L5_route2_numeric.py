"""Gate 2, level L5 (chapter 6), route 2 (numerical, NumPy/SciPy): Monte Carlo of the Poisson argument, of Gillespie's waiting time and of thinning,
plus the data-level comparison of (6.1) with the exact runs in data/stochastic.json (read only) and the arithmetic of the 6.2/6.3 statements."""
import json, numpy as np
from scipy import stats
rng = np.random.default_rng(2026)

print('== (6.1) Poisson: rare independent drops as a binomial scatter of N candidates, each a "hit" with probability mu/N')
for mu in [0.3, np.log(2), 2.0]:
    N = 2000; trials = 400000
    cnt = rng.binomial(N, mu / N, size=trials)
    print('   mu = %.4f : P(no drop) simulated %.5f +- %.5f ; exp(-mu) = %.5f ; mean %.4f var %.4f (Poisson: both = mu)' % (mu, (cnt == 0).mean(), np.sqrt((cnt == 0).mean() * (1 - (cnt == 0).mean()) / trials), np.exp(-mu), cnt.mean(), cnt.var()))
# drops placed uniformly at random in a unit cube of volume 1, each with probability: Poisson process in space; volume fraction V sampled
print('   spatial Poisson process, density n = 4 per unit volume; probability that a randomly placed box of volume V = ln2/n holds none:')
n_ = 4.0; Vb = np.log(2) / n_; trials = 100000
empty = 0
for _ in range(trials):
    pts = rng.uniform(size=(rng.poisson(n_ * 8), 3)) * 2.0            # 8 unit volumes, density n
    x0 = rng.uniform(0, 2 - Vb ** (1 / 3), 3)
    inside = np.all((pts >= x0) & (pts < x0 + Vb ** (1 / 3)), axis=1).any()
    empty += (not inside)
print('      P(empty) = %.4f (expected 1/2 for V n = ln 2)' % (empty / trials))

print('== Gillespie: tau = -ln(u)/a0 with u uniform on (0,1]; pair chosen in proportion to its rate')
a0 = 3.7; u = 1 - rng.uniform(size=400000)
tau = -np.log(u) / a0
print('   mean tau = %.5f (1/a0 = %.5f) ; KS test against Exp(a0): statistic %.5f, p = %.3f' % (tau.mean(), 1 / a0, *stats.kstest(tau, 'expon', args=(0, 1 / a0))))
rates = np.array([0.5, 1.5, 0.2, 3.0, 1.1]); pr = rates / rates.sum()
ch = rng.choice(len(rates), size=400000, p=pr); freq = np.bincount(ch) / len(ch)
print('   pair choice frequencies', np.round(freq, 4), ' target', np.round(pr, 4), ' chi-square p =', round(stats.chisquare(np.bincount(ch), pr * len(ch)).pvalue, 3))
# the merged process: competing exponential clocks with rates r_i: first event time Exp(sum r_i), index prob r_i/sum r
clocks = rng.exponential(1 / rates, size=(200000, len(rates)))
first = clocks.min(axis=1); who = clocks.argmin(axis=1)
print('   competing clocks: min time mean %.5f (1/sum = %.5f), who-first frequencies %s' % (first.mean(), 1 / rates.sum(), np.round(np.bincount(who) / len(who), 4)))

print('== thinning: Poisson stream at rate lam*, keep with probability q = K/K*; compare with a direct Poisson stream of rate lam* q')
lam_star, qk, T = 12.0, 0.37, 5.0
counts = []
for _ in range(60000):
    Np = rng.poisson(lam_star * T); keep = rng.uniform(size=Np) < qk; counts.append(int(keep.sum()))     # kept points of a Poisson(lam* T) stream
counts = np.array(counts); mu_ = lam_star * qk * T
kk_ = np.arange(0, 80); pmf = stats.poisson.pmf(kk_, mu_) * len(counts); obs_all = np.bincount(counts, minlength=80)[:80].astype(float)
good = np.where(pmf > 5)[0]; lo_, hi_ = good[0], good[-1]
obs = np.concatenate([[obs_all[:lo_ + 1].sum()], obs_all[lo_ + 1:hi_], [obs_all[hi_:].sum()]]); ex = np.concatenate([[pmf[:lo_ + 1].sum()], pmf[lo_ + 1:hi_], [len(counts) * stats.poisson.sf(hi_ - 1, mu_)]])
ex *= obs.sum() / ex.sum()
chi = stats.chisquare(obs, ex)
print('   kept count: mean %.4f var %.4f (Poisson mean %.3f: both equal) ; chi-square against Poisson(%.3f): p = %.3f' % (counts.mean(), counts.var(), mu_, mu_, chi.pvalue))
# time to the first KEPT point of a rate-lam* stream (sequential thinning): must be Exp(lam* q)
first = np.empty(200000)
for k_ in range(len(first)):
    t_ = 0.0
    while True:
        t_ += rng.exponential(1 / lam_star)
        if rng.uniform() < qk: break
    first[k_] = t_
print('   time to first kept event: mean %.5f (1/(lam* q) = %.5f) ; KS against Exp(lam* q): p = %.3f' % (first.mean(), 1 / (lam_star * qk), stats.kstest(first, 'expon', args=(0, 1 / (lam_star * qk))).pvalue))
# class-pair scheme: 3 classes with n_a = 3, 4, 2 members, bound K*_ab >= K_ij, true K_ij random; per-pair accepted rate must be K_ij/V
print('== class-pair scheme (V = 1): per-pair accepted rate must equal K_ij')
members = {0: [0, 1, 2], 1: [3, 4, 5, 6], 2: [7, 8]}; cls_of = {i: c for c, L in members.items() for i in L}
nid = 9; Kt = np.triu(rng.uniform(0.2, 1.0, (nid, nid)), 1); Kt = Kt + Kt.T
Kstar = np.zeros((3, 3))
for a in range(3):
    for b in range(3): Kstar[a, b] = max(Kt[i, j] for i in members[a] for j in members[b] if i != j) * 1.15
prop_rate = np.array([[Kstar[a, b] * len(members[a]) * len(members[b]) / (1 if a != b else 2) for b in range(3)] for a in range(3)])
# class pairs a <= b only
cp = [(a, b) for a in range(3) for b in range(a, 3)]; rate_cp = np.array([prop_rate[a, b] for a, b in cp]); A = rate_cp.sum()
Tsim = 4000.0; Np = rng.poisson(A * Tsim); which = rng.choice(len(cp), size=Np, p=rate_cp / A)
acc = {}
for w in range(len(cp)):
    a, b = cp[w]; m = (which == w).sum()
    I = rng.choice(members[a], m); J = rng.choice(members[b], m)
    ok = I != J
    pr_acc = np.where(ok, Kt[I, J] / Kstar[a, b], 0.0)
    keep = rng.uniform(size=m) < pr_acc
    for i, j in zip(I[keep], J[keep]): acc[(min(i, j), max(i, j))] = acc.get((min(i, j), max(i, j)), 0) + 1
worst = 0
for i in range(nid):
    for j in range(i + 1, nid):
        r_est = acc.get((i, j), 0) / Tsim; worst = max(worst, abs(r_est - Kt[i, j]) / np.sqrt(Kt[i, j] / Tsim))
print('   %d pairs, %d proposals: worst deviation of the accepted rate from K_ij in standard errors: %.2f' % (nid * (nid - 1) // 2, Np, worst))

print('== data-level check of (6.1) against the exact runs (data/stochastic.json) and the mean-field tail (data/bridge.json, 16 bins per doubling)')
base = '/home/user/SiteTest/portfolios-src/droplets/data/'
S = json.load(open(base + 'stochastic.json')); B = json.load(open(base + 'bridge.json'))['s16']          # the text uses the 16-bins-per-doubling tail (checks/check_numbers.cjs line 186)
tb = np.array(B['t'], float); Nmax = np.maximum.accumulate(np.array(B['N100'], float))
for Vcm3 in ['10', '100', '1000']:
    Vm3 = float(Vcm3) * 1e-6
    t100 = np.array([q['t100'] if q['t100'] is not None else np.inf for q in S['V'][Vcm3]])
    med_emp = np.median(t100)
    med_6 = next((tb[i] for i in range(len(tb)) if Vm3 * Nmax[i] >= np.log(2)), None)
    print('   V = %5s cm3 (%3d runs): empirical median %.0f s ; (6.1) median %s ; max V n100 over the hour = %.3f (ln 2 = 0.693)' % (Vcm3, len(t100), med_emp, ('%.0f s' % med_6) if med_6 is not None else 'never reached', Vm3 * Nmax[-1]))
    for tq in [150, 200, 250, 300, 400, 600, 900]:
        pe = (t100 <= tq).mean(); pm = 1 - np.exp(-Vm3 * Nmax[np.searchsorted(tb, tq)])
        if 0.02 < pm < 0.98 or 0.02 < pe < 0.98:
            se = np.sqrt(max(pm * (1 - pm), 1e-4) / len(t100))
            print('        t = %4d s : fraction of runs with a 100 um drop %.3f ; 1 - exp(-V n100) = %.3f ; difference %+.3f (= %.1f binomial standard errors)' % (tq, pe, pm, pe - pm, (pe - pm) / se))
print('   1 m3 (V = 1): first 100 um drop at', next(tb[i] for i in range(len(tb)) if Nmax[i] >= np.log(2)), 's (text about 60 s) ; first 1 mm drop (N1mm = ln 2):', next(tb[i] for i in range(len(tb)) if B['N1mm'][i] >= np.log(2)), 's =', next(tb[i] for i in range(len(tb)) if B['N1mm'][i] >= np.log(2)) / 60, 'min (text about 18 min)')
F = np.array(B['F100']); print('   half the water above 100 um at t = %.1f s (text 585 s, "to the 5 s record")' % np.interp(0.5, F, tb))
print('== water available in a small volume (text: in 1 cm3 no drop ever reaches 100 um; truncated modes at 3 sigma)')
from scipy.stats import norm
def mode_mass(N, rg, sg, trunc):
    ls = np.log(sg); lo, hi = -trunc, trunc                                    # in units of ln sg, centred on ln rg
    Z = norm.cdf(hi) - norm.cdf(lo)                                           # truncation rescales the number to keep N
    m3 = np.exp(4.5 * ls**2) * (norm.cdf(hi - 3 * ls) - norm.cdf(lo - 3 * ls)) / Z
    return N * 4 / 3 * np.pi * 1000 * rg**3 * m3
Wm = mode_mass(300e6, 8e-6, 1.25, 3) + mode_mass(1e6, 40e-6, 1.2, 3)
for Vc in (1, 10):
    m = Wm * Vc * 1e-6; rmax = (3 * m / (4 * np.pi * 1000)) ** (1 / 3)
    print('   V = %2d cm3 holds %.4e kg of water: one drop of all of it has radius %.1f um' % (Vc, m, rmax * 1e6))
print('   no collector starts above rg sg^3 = 40 x 1.2^3 = %.2f um (text 69)' % (40 * 1.2**3))
z100 = np.log(100 / 40) / np.log(1.2)
print('   untruncated lognormal tail: P(r > 100 um) for the 1 cm^-3 mode = %.3e -> %.3f drops per m3 (text 0.25)' % (norm.sf(z100), 1e6 * norm.sf(z100)))

B8 = json.load(open(base + 'bridge.json'))['s8']; t8 = np.array(B8['t'], float); N8 = np.maximum.accumulate(np.array(B8['N100'], float))
print('sensitivity to the grid (8 bins per doubling): medians 100 cm3: %s s, 1000 cm3: %s s, 1 m3: %s s ; half the water above 100 um: %.1f s' % tuple([next(t8[i] for i in range(len(t8)) if V * N8[i] >= np.log(2)) for V in (1e-4, 1e-3, 1.0)] + [np.interp(0.5, B8['F100'], t8)]))
print('== arithmetic quoted in 6.2/6.3 (current text of book-06)')
mass100 = 4 / 3 * np.pi * 1000 * (100e-6)**3; mass1mm = 4 / 3 * np.pi * 1000 * (1e-3)**3
Wm_un = (300e6 * 4 / 3 * np.pi * 1000 * (8e-6)**3 * np.exp(4.5 * np.log(1.25)**2) + 1e6 * 4 / 3 * np.pi * 1000 * (40e-6)**3 * np.exp(4.5 * np.log(1.2)**2))   # untruncated modes, kg/m3
print('   total water of the two modes (untruncated) %.4f g/m3 ; a 100 um drop holds the water of %.2f cm3 (text 3.75) ; a 1 mm drop of %.2f litres (text 3.75)' % (Wm_un * 1e3, mass100 / Wm_un * 1e6, mass1mm / Wm_un * 1e3))
print('   10 cm3 hold the water of one drop of radius %.0f um (text 139)' % (((3 * Wm_un * 1e-5) / (4 * np.pi * 1000)) ** (1 / 3) * 1e6))
print('   captures of 8 um droplets from 69 to 100 um: (100^3 - 69^3)/8^3 = %.0f (text 1312)' % ((100**3 - 69**3) / 8**3))
print('   mean-field share of 10 cm3 volumes that ever hold a 100 um drop: 1 - exp(-V max n100) = %.1f %% (text 32 %%)' % (100 * (1 - np.exp(-1e-5 * Nmax.max()))))

"""The Electron Beam, from Tip to Measurement · text/ch06.py · chapter 6, Scan and hit.

Written by the finisher (9 November 2026). Format: eb_lib.py (the dict CH). Numbers: outputs of physics/ch06.js (checked through ref/ch06.py),
expressions of them, and the values derive/ch06.py writes to data/ch06/derive_results.json and data/ch06/mc_runs.json (stored runs of the
page's own module through Node, 2000 electrons each; rerun derive/ch06.py after changing the model).
"""
import html
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
EB = os.path.abspath(os.path.join(HERE, '..'))
if EB not in sys.path:
    sys.path.insert(0, EB)
from ref import core as RC, ch06 as R6  # noqa: E402

DER = json.load(open(os.path.join(EB, 'data', 'ch06', 'derive_results.json'), encoding='utf-8'))
RUNS = json.load(open(os.path.join(EB, 'data', 'ch06', 'mc_runs.json'), encoding='utf-8'))
DN = DER['numbers']
NUMS = {}


def mod(name, inputs, out, module='ch06', scale=1, sig=3):
    NUMS[name] = {'module': module, 'inputs': inputs, 'out': out, 'scale': scale, 'sig': sig}


def ex(name, expr, of=None, scale=1, sig=3):
    NUMS[name] = {'expr': expr, 'of': dict(of or {}), 'scale': scale, 'sig': sig}


def const(name, value, sig=3):
    ex(name, repr(float(value)), {}, 1, sig)


# ---- the default: silicon at 800 V; and silicon at 30 kV
for tag, inp in (('d', {}), ('k', {'V_land': 30000.0})):
    mod(tag + '_eta', inp, 'eta_BSE', sig=2)
    mod(tag + '_ueta', inp, 'u_eta', sig=1)
    mod(tag + '_delta', inp, 'delta_SE', sig=2)
    mod(tag + '_udelta', inp, 'u_delta', sig=1)
    mod(tag + '_R', inp, 'R', scale=1e9, sig=2)
    mod(tag + '_r90', inp, 'r90', scale=1e9, sig=2)
    mod(tag + '_sig', inp, 'sigma_sig', scale=1e9, sig=2)
mod('k_Rum', {'V_land': 30000.0}, 'R', scale=1e6, sig=2)
mod('k_r90um', {'V_land': 30000.0}, 'r90', scale=1e6, sig=2)
mod('k_sigum', {'V_land': 30000.0}, 'sigma_sig', scale=1e6, sig=2)
ex('d_sum', 'a+b', {'a': 'd_eta', 'b': 'd_delta'}, sig=2)
ex('vol_ratio', '(b/a)**3', {'a': 'd_r90', 'b': 'k_r90'}, sig=1)
ex('sig_ratio', 'b/a', {'a': 'd_sig', 'b': 'k_sig'}, sig=2)
# gold at 800 V
mod('au_eta', {'material': 'Au'}, 'eta_BSE', sig=2)
mod('au_delta', {'material': 'Au'}, 'delta_SE', sig=2)
mod('au_R', {'material': 'Au'}, 'R', scale=1e9, sig=2)
# ---- material constants as the module uses them
for mt in ('Si', 'Au'):
    const('J_' + mt, DN['J_eV'][mt], sig=3)
const('mfp_Si_08', DN['mfp_Si']['0.8'], sig=2)
const('mfp_Si_30', DN['mfp_Si']['30.0'], sig=2)
const('mfp_Si_100', DN['mfp_Si']['100.0'], sig=3)
const('joy_const', DN['joy_const'] * 1e21, sig=3)
const('es_mid_lo', DN['estar_ratio_mid'][0], sig=2)
const('es_mid_hi', DN['estar_ratio_mid'][1], sig=3)
const('es_lo_hi', DN['estar_ratio_lo'][1], sig=2)
const('es_100', DN['estar_ratio_100'][0], sig=2)
const('es_100_beta', DN['estar_ratio_100'][2], sig=2)
B = {mt: {tuple(b['band_keV']): b for b in DN['eta_bands'][mt]} for mt in DN['eta_bands']}
for mt in ('Si', 'Cu', 'Au'):
    for key, tag in (((0.4, 2.0), 'lo'), ((8.0, 31.0), 'hi')):
        const('eb_%s_%s_mc' % (mt, tag), B[mt][key]['eta_mc_mean'], sig=2)
        const('eb_%s_%s_me' % (mt, tag), B[mt][key]['eta_meas_mean'], sig=2)
const('eb_Si_lo_n', B['Si'][(0.4, 2.0)]['n_meas'], sig=1)
DC = DN['delta_cmp']
for mt in ('Si', 'Au'):
    const('dc_%s_mc20' % mt, DC[mt]['mc20'], sig=2)
    const('dc_%s_lj20' % mt, DC[mt]['lj20'], sig=2)
    const('dc_%s_mc2' % mt, DC[mt]['mc2'], sig=2)
    const('dc_%s_lj2' % mt, DC[mt]['lj2'], sig=2)
LJ = DN['lin_joy']


def law(E, mt):
    """Lin and Joy's universal law (their Eq. 12), with their delta_max and E_max for the element."""
    x = E / LJ[mt]['Emax']
    return LJ[mt]['dmax'] * 1.28 * x ** -0.67 * (1 - math.exp(-1.614 * x ** 1.67))


const('law_Si_08', law(0.8, 'Si'), sig=2)
const('si_dmax', LJ['Si']['dmax'], sig=2)
const('si_Emax', LJ['Si']['Emax'] * 1e3, sig=2)

LITERALS = {
    '5, 329, 1991': 'volume, page and year of Joy 1991', '37, 895, 2005': 'volume, page and year of Lin and Joy', '800 eV': 'the default landing energy, a given',
    '30 keV': 'an energy of the comparison, a given', '3.4\\times10^{-3}': 'Bishop\'s screening constant, quoted', '5.21\\times10^{-21}': 'Joy\'s constant, quoted',
    '0.795': 'Joy et al.\'s fitted k for silicon, quoted', '0.832': 'Joy et al.\'s fitted k for gold, quoted', '32-bit': 'the word size of the generator',
    '2.3\\lambda': 'ln 10 = 2.3, the tenth-percentile path', '10^{-9}': 'the measured parity agreement', '0.4 and 2 keV': 'an energy band, a choice',
    '8 and 31 keV': 'an energy band, a choice', 'Eq. 12,': 'equation number of Lin and Joy', '20 keV': 'an energy of Lin and Joy\'s table', '329–337': 'pages of Joy 1991', '–337,': 'last page of Joy 1991', '–900,': 'last page of Lin and Joy',
    '895–900': 'pages of Lin and Joy', 'Eqs. 1 to 3 and 12, Eq. 13,': 'equation numbers of Lin and Joy',
    'Example 6.1': 'the number of a worked example', 'Example 6.2': 'the number of a worked example', 'Example 6.3': 'the number of a worked example',
    '800 V': 'the landing voltage of the default, a given', '30 kV': 'a given of Example 6.2', '2000': 'the number of simulated electrons, a given',
    '50 eV': 'the conventional upper energy of a secondary electron and the end of the Joy–Luo stopping power, quoted', '1991': 'year of Joy\'s paper',
    '2005': 'year of Lin and Joy', '1996': 'year of Joy et al.', '1976': 'year of Bishop', '1972': 'year of Kanaya and Okayama', '2023': 'year of Akbari et al.',
    '5.21': 'Joy\'s constant, quoted', '10^{-21}': 'exponent of that constant', '3.4': 'Bishop\'s screening constant, quoted', '0.67': 'exponent in the screening and the universal law, quoted',
    '78\\,500': 'Joy\'s stopping-power constant, quoted', '1.166': 'the constant in the Bethe logarithm, quoted', '0.85': 'Joy and Luo\'s k as Lin and Joy use it, quoted',
    '9.76': 'Berger–Seltzer constant, quoted', '58.5': 'Berger–Seltzer constant, quoted', '0.19': 'Berger–Seltzer exponent, quoted', '27.6': 'Kanaya–Okayama constant, quoted',
    '1.67': 'Kanaya–Okayama exponent, quoted', '0.89': 'Kanaya–Okayama exponent, quoted', '1.28': 'universal law constant, quoted', '1.614': 'universal law constant, quoted',
    '511': 'm c² in keV', '1024': '2 m c² in keV, as Joy prints it', '90 %': 'the energy fraction that defines r90, a choice', '½': 'the escape factor K = 0.5 of Lin and Joy',
    '0.5': 'the escape factor K of Lin and Joy', '90 eV': 'Lin and Joy\'s ε for silicon, quoted', '2.7 nm': 'Lin and Joy\'s λ for silicon, quoted', '35 eV': 'Lin and Joy\'s ε for gold, quoted',
    '0.5 nm': 'Lin and Joy\'s λ for gold, quoted', '2 and 20 keV': 'the energies of Lin and Joy\'s table', '1 keV': 'Joy\'s stated lower limit, quoted',
    'about 50 eV': 'Joy\'s stated limit of the stopping power, quoted', '7919': 'the seed step between electrons', '40': 'the number of drawn paths',
    '4000': 'histogram bins', '12': 'escape depths beyond which secondary generation is skipped, a choice', '200': 'the cap on parts of one step',
    'Si, Al, Cu, Au': 'the four materials', 'Si 173, Al 166, Cu 322, Au 790 eV': 'ESTAR\'s J values, quoted', '0.4 to 2 keV': 'an energy band, a choice',
    '8 to 31 keV': 'an energy band, a choice', '5 to 30 keV': 'an energy band', '1 to 3 keV': 'an energy band', '100 keV': 'an energy of the comparison',
    'M1': 'check label', 'M10': 'check label', '20 000': 'number of random cases in check M4', '200 000': 'quadrature points of check M5',
    '10.1002/mp.16604': 'DOI of Akbari et al.', '10.5281/zenodo.7810951': 'DOI of the data set', '10.1002/sia.2107': 'DOI of Lin and Joy',
    '5, 329': 'volume and first page of Joy 1991', '37, 895': 'volume and first page of Lin and Joy', '10, 653': 'volume and first page of Joy et al. 1996',
    '5 (1991) 329–337': 'volume, year and pages of Joy 1991', '37 (2005) 895–900': 'volume, year and pages of Lin and Joy', '10 (1996)': 'volume and year of Joy et al.',
    '5 (1972) 43': 'volume, year and page of Kanaya and Okayama', 'CC BY 4.0': 'the licence of the data set', '1–4': 'a range of equation numbers',
    '12 ': 'an equation number of Joy', 'Eqs. 1 to 3': 'equation numbers of Lin and Joy', 'Eq. 13': 'equation number of Lin and Joy', 'Eq. 12': 'equation number',
    'Eqs. 1–4, 6, 7, 11 and 12': 'equation numbers of Joy', 'Table 1': 'table number of Lin and Joy', 'Table 2': 'table number of Joy et al.',
    '50 000': 'the nucleus-to-electron mass ratio of silicon, rounded', '10 000': 'the order of the energy transferred, inverse', '0.0001': 'the order of the energy fraction',
}


def checks_table():
    rows = ''.join('<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (c['id'], html.escape(c['title']), 'pass' if c['ok'] else 'FAIL', html.escape(c['detail']))
                   for c in DER['checks'])
    return '<div class="ptab-wrap"><table class="ptab ptab--checks"><thead><tr><th>check</th><th>what is verified</th><th>result</th><th>detail</th></tr></thead><tbody>%s</tbody></table></div>' % rows


COL = {'Si': '#7a1f2b', 'Al': '#8b8079', 'Cu': '#7a4b12', 'Au': '#3a322e'}
ST = 'font-family:IBM Plex Mono,monospace;font-size:16px;fill:#3a322e'


def _frame(W, H, L, Rr, T, Bt, ylab, yticks, Y):
    out = ['<svg viewBox="0 0 %d %d" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="%s">' % (W, H, html.escape(ylab)),
           '<rect width="%d" height="%d" fill="#fff"/><rect x="%d" y="%d" width="%d" height="%d" fill="none" stroke="#d9d0c2"/>' % (W, H, L, T, Rr - L, Bt - T)]
    X = lambda E: L + (math.log10(E) - math.log10(0.5)) / (math.log10(30) - math.log10(0.5)) * (Rr - L)
    for E, lab in ((0.5, '0.5'), (1, '1'), (2, '2'), (5, '5'), (10, '10'), (20, '20'), (30, '30')):
        out.append('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="#eee7da"/><text x="%.1f" y="%d" text-anchor="middle" style="%s">%s</text>' % (X(E), T, X(E), Bt, X(E), Bt + 17, ST, lab))
    for v, lab in yticks:
        y = Y(v)
        out.append('<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="#eee7da"/><text x="%d" y="%.1f" text-anchor="end" style="%s">%s</text>' % (L, y, Rr, y, L - 6, y + 4, ST, lab))
    out.append('<text x="%d" y="%d" text-anchor="middle" style="%s">landing energy (keV), logarithmic</text>' % ((L + Rr) // 2, Bt + 36, ST))
    out.append('<text x="%d" y="%d" style="%s">%s</text>' % (L, T - 8, ST, html.escape(ylab)))
    return out, X


def fig_eta():
    W, H, L, Rr, T, Bt = 640, 390, 58, 620, 34, 326
    Y = lambda v: Bt - v / 0.7 * (Bt - T)
    out, X = _frame(W, H, L, Rr, T, Bt, 'backscattering coefficient η', [(v, '%.1f' % v) for v in (0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7)], Y)
    for mt in ('Si', 'Al', 'Cu', 'Au'):
        col = COL[mt]
        for E, e in RUNS['database'].get(mt, []):
            if 0.5 <= E <= 30:
                out.append('<circle cx="%.1f" cy="%.1f" r="2.6" fill="none" stroke="%s" stroke-width="1"/>' % (X(E), Y(e), col))
        pts = [(r['E_keV'], r['eta']) for r in RUNS['runs'][mt]]
        out.append('<polyline fill="none" stroke="%s" stroke-width="2.2" points="%s"/>' % (col, ' '.join('%.1f,%.1f' % (X(E), Y(e)) for E, e in pts)))
        E_, e_ = pts[-1]
        out.append('<text x="%.1f" y="%.1f" style="%s;fill:%s">%s</text>' % (X(E_) - 30, Y(e_) + {'Si': -8, 'Al': 20, 'Cu': -8, 'Au': -8}[mt], ST, col, mt))
    out.append('<text x="%d" y="%d" style="%s">lines: this Monte Carlo · circles: measurements</text>' % (L + 8, Bt - 10, ST))
    out.append('</svg>')
    return ''.join(out)


def fig_delta():
    W, H, L, Rr, T, Bt = 640, 390, 58, 620, 34, 326
    lo, hi = math.log10(0.02), math.log10(2.0)
    Y = lambda v: Bt - (math.log10(max(v, 1e-3)) - lo) / (hi - lo) * (Bt - T)
    out, X = _frame(W, H, L, Rr, T, Bt, 'secondary-electron yield δ, logarithmic', [(v, str(v)) for v in (0.02, 0.05, 0.1, 0.2, 0.5, 1, 2)], Y)
    for mt in ('Si', 'Au'):
        col = COL[mt]
        Es = [0.5 * 60 ** (i / 80) for i in range(81)]
        out.append('<polyline fill="none" stroke="%s" stroke-width="1.4" stroke-dasharray="5 4" points="%s"/>' % (col, ' '.join('%.1f,%.1f' % (X(E), Y(law(E, mt))) for E in Es)))
        pts = [(r['E_keV'], r['delta']) for r in RUNS['runs'][mt]]
        out.append('<polyline fill="none" stroke="%s" stroke-width="2.2" points="%s"/>' % (col, ' '.join('%.1f,%.1f' % (X(E), Y(d)) for E, d in pts)))
        for E, key in ((2.0, 'd2'), (20.0, 'd20')):
            v = LJ[mt][key]
            out.append('<rect x="%.1f" y="%.1f" width="7" height="7" fill="none" stroke="%s" stroke-width="1.3"/>' % (X(E) - 3.5, Y(v) - 3.5, col))
        E_, d_ = pts[0]
        out.append('<text x="%.1f" y="%.1f" style="%s;fill:%s">%s</text>' % (X(E_) + 6, Y(d_) - 8, ST, col, mt))
    out.append('<text x="%d" y="%d" style="%s">solid: this Monte Carlo · dashed: universal law</text>' % (L + 8, Bt - 26, ST))
    out.append('<text x="%d" y="%d" style="%s">squares: Lin and Joy’s Monte Carlo</text>' % (L + 8, Bt - 10, ST))
    out.append('</svg>')
    return ''.join(out)


def estar_table():
    rows = []
    for mt in ('Si', 'Au'):
        for T_, Sc, Sj, r in RUNS['estar_cmp'][mt]:
            if T_ in (1, 2, 5, 10, 30, 100):
                rows.append('<tr><td>%s</td><td>%g</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (mt, T_, RC.fmt(Sc, 3), RC.fmt(Sj, 3), RC.fmt(r, 3)))
    return ('<div class="ptab-wrap"><table class="ptab ptab--checks"><thead><tr><th>material</th><th>E (keV)</th><th>ESTAR collision (MeV cm² g⁻¹)</th>'
            '<th>Joy–Luo (MeV cm² g⁻¹)</th><th>ratio</th></tr></thead><tbody>%s</tbody></table></div>') % ''.join(rows)


S = []
S.append({'id': 'picture', 'title': 'Into the wafer', 'html': r'''
<p>Throw a handful of marbles into a box of loosely packed heavier balls. Each marble rattles about, changes direction at every hit, and slows down; some bounce back out of the box, the rest come to rest inside. An electron entering a wafer does the same, with two kinds of collision. It is deflected by the atomic nuclei, which are tens of thousands of times heavier than it is (a silicon nucleus about 50 000 times): such a hit turns it without taking away more than about one part in 10 000 of its energy, an <em>elastic</em> collision. And it loses energy to the electrons of the solid in many small bites, ionising and exciting as it goes, <em>inelastic</em> collisions, which hardly turn it.</p>
<p>What comes back out is the signal of the microscope. Electrons that turn round and leave with most of their energy are <em>backscattered electrons</em> (BSE); their number per incident electron is the backscattering coefficient $\eta$. The energy the beam leaves in the solid frees slow electrons of a few electronvolts, and those born within a few nanometres of the surface can escape: <em>secondary electrons</em> (SE), by convention those leaving with less than 50 eV; their number per incident electron is the yield $\delta$. A secondary electron made by the incoming beam right where it enters carries the sharp information; one made by a backscattered electron on its way out comes from wherever that electron surfaced, which can be far from the beam. How far the electrons wander, and how many come back, is what this chapter computes, for the probe of chapter 5 landing on silicon, aluminium, copper or gold.</p>
<p>No closed formula follows hundreds of random turns. We follow the electrons one by one instead, drawing each turn and each free path from the probability laws of the two collisions: a Monte Carlo simulation, in the form D. C. Joy describes (<em>Scanning Microscopy</em> 5, 329, 1991), with the secondary-electron model of Y. Lin and D. C. Joy (<em>Surf. Interface Anal.</em> 37, 895, 2005).</p>
'''})

S.append({'id': 'elastic', 'title': 'Turning: the screened Rutherford cross-section', 'html': r'''
<p>An electron passing a nucleus of charge $Ze$ is pulled by the Coulomb force and leaves turned by an angle $\varphi$. Rutherford's calculation of this two-body problem gives the probability of a turn into the solid angle $\mathrm d\Omega$ as an effective target area, the differential cross-section. For a fast electron of momentum $p$ and speed $v$ it is</p>
$$ \frac{\mathrm d\sigma}{\mathrm d\Omega}=\left(\frac{Ze^2}{4\pi\varepsilon_0}\right)^2\frac{1}{(pv)^2}\,\frac{1}{(1-\cos\varphi)^2} , \label{ruth6} $$
<p>which in the non-relativistic case, $pv=2E$, is the textbook form with $\sin^4(\varphi/2)$ in the denominator. It diverges at small angles because a bare Coulomb field reaches to infinity. In a solid the atom's own electrons screen the nucleus beyond about an atomic radius, which removes the divergence. Joy, following Bishop (1976), writes the screening as a shift of the denominator to $(1-\cos\varphi+2a)^2$, with the screening parameter</p>
$$ a=3.4\times10^{-3}\,\frac{Z^{0.67}}{E/\mathrm{keV}} , \label{screen6} $$
<p>fitted so that simulated backscattering agrees with experiment. Integrating over all directions (check M1) gives the total elastic cross-section, and with $pv=E(E+2mc^2)/(E+mc^2)$ (check M2) it becomes Joy's Eq. 1,</p>
$$ \sigma_E=\left(\frac{Ze^2}{4\pi\varepsilon_0}\right)^2\frac{\pi}{a(1+a)}\,\frac{1}{E^2}\left(\frac{E+mc^2}{E+2mc^2}\right)^2=5.21\times10^{-21}\,\frac{Z^2}{E^2}\,\frac{4\pi}{a(1+a)}\left(\frac{E+511}{E+1024}\right)^2\ \mathrm{cm}^2 \label{sigma6} $$
<p>with $E$ in keV. The constant follows from $(e^2/4\pi\varepsilon_0)^2/4=$ {{num:joy_const}}×10<sup>−21</sup> keV<sup>2</sup> cm<sup>2</sup>; Joy's 5.21 is half a per cent higher (check M2), and we use his value. A beam crossing a solid with $n=N_A\rho/A$ atoms per volume ($\rho$ the density, $A$ the molar mass, $N_A$ Avogadro's number) meets a nucleus on average once per <em>elastic mean free path</em></p>
$$ \lambda_\mathrm{el}=\frac{A}{N_A\,\rho\,\sigma_E} . \label{mfp6} $$
<p>In silicon it is {{num:mfp_Si_08}} nm at 800 eV, {{num:mfp_Si_30}} nm at 30 keV and {{num:mfp_Si_100}} nm at 100 keV. The angle at each hit is mostly small: for silicon at 800 eV the screening parameter is a few hundredths, and half of the turns are smaller than about $2\sqrt a$ radians.</p>
<p>How good is this cross-section? Rutherford's formula treats the electron as a classical particle in a point-charge field and ignores its spin. For light elements and energies of several keV that is adequate; for heavy elements and low energies it is not, and the proper replacement is the Mott cross-section from the Dirac equation. Joy states plainly that his models "are not, in principle, suitable for incident beam energies below 1 keV". Our default, 800 eV, is below that. We use the model anyway, because it is open and simple, and we measure its error against data in {{sec:ch06-yields}}.</p>
'''})

S.append({'id': 'loss', 'title': 'Slowing down: the stopping power', 'html': r'''
<p>Between the elastic turns the electron loses energy to the electrons of the solid. A single loss is usually tens of electronvolts, small against keV, and there are many of them per mean free path. Joy therefore lets the energy fall continuously along the path, at the rate given by Bethe's stopping power. In the low-energy form of Joy and Luo, which Lin and Joy use (their Eq. 13),</p>
$$ -\frac{\mathrm dE}{\mathrm ds}=78\,500\,\frac{\rho Z}{AE}\,\ln\!\left(\frac{1.166\,(E+kJ)}{J}\right)\ \frac{\mathrm{keV}}{\mathrm{cm}},\qquad k=0.85 , \label{bethe6} $$
<p>with $\rho$ in g cm<sup>−3</sup>, $A$ in g mol<sup>−1</sup> and $E$ in keV. The picture behind Bethe's formula is a fast charge sweeping past the atomic electrons: each feels a short electric pulse and takes up momentum, the more the slower the charge passes, hence the $1/E$. The logarithm counts the range of distances over which the pulse is short enough to excite an electron of typical binding energy $J$, the mean ionisation energy; Joy's Eq. 12 (Berger and Seltzer) gives it as $J=(9.76Z+58.5Z^{-0.19})$ eV, {{num:J_Si}} eV for silicon and {{num:J_Au}} eV for gold, within 3 % of the values NIST uses (check M7). The term $kJ$ is Joy and Luo's empirical change: without it the logarithm turns negative below $E=J/1.166$, which is meaningless; with it the formula stays positive and, by their measurements, fits stopping powers down to about 50 eV (D. C. Joy et al., <em>Scanning Microscopy</em> 10, 1996, Table 2 gives fitted $k$ of 0.795 for silicon and 0.832 for gold; we keep 0.85, the value Lin and Joy used with their secondary-electron constants).</p>
<p>The NIST table ESTAR lists the stopping power computed from the full relativistic Bethe theory. The comparison (table below, check M6): from 5 to 30 keV the two agree to between {{num:es_mid_lo}} and {{num:es_mid_hi}}. Below, Joy–Luo is larger, up to {{num:es_lo_hi}} times for gold at 1 keV, where Bethe's theory itself is no longer valid and neither number is a measurement. Above, Joy–Luo falls behind ({{num:es_100}} at 100 keV) because it is non-relativistic: the true stopping power goes as $1/\beta^2$, not as $1/E$, and $\beta^2/(2E/mc^2)=$ {{num:es_100_beta}} at 100 keV. The chapter's range ends at 30 keV, inside the band of agreement.</p>
''' + estar_table()})

S.append({'id': 'loop', 'title': 'The Monte Carlo loop', 'html': r'''
<p>Each electron starts at the point of impact, heading straight into the wafer with the landing energy $E$. Then the same four steps repeat.</p>
<p><b>1. A free path.</b> The chance of travelling a distance $s$ without an elastic hit falls as $\mathrm e^{-s/\lambda_\mathrm{el}}$, the law of a constant hazard. A path with this distribution is $s=-\lambda_\mathrm{el}\ln R_1$, with $R_1$ a random number uniform between 0 and 1: the fraction of paths longer than $s$ is the fraction of $R_1$ below $\mathrm e^{-s/\lambda_\mathrm{el}}$ (check M3). Ten per cent of the paths are longer than $2.3\lambda_\mathrm{el}$.</p>
<p><b>2. A move and a loss.</b> The electron moves $s$ along its direction and loses $s\,|\mathrm dE/\mathrm ds|$ by {{eq:bethe6}}. If the step would take it above the surface, it is cut there: the electron has left the wafer, and it counts as backscattered if its energy is still above 50 eV. If the loss would take its energy below 50 eV, the step is cut where that happens and the electron stops.</p>
<p><b>3. A turn.</b> The polar angle of the elastic hit comes from the same trick applied to the angular distribution: the fraction of hits that turn by less than $\varphi$ is set equal to a second random number $R_2$, and solving gives Joy's Eq. 6 (check M1),</p>
$$ \cos\varphi=1-\frac{2aR_2}{1+a-R_2} , \label{angle6} $$
<p>while the azimuth about the old direction is uniform, $\psi=2\pi R_3$.</p>
<p><b>4. A new direction.</b> The unit vector of motion is turned by $\varphi$ and $\psi$ about itself. Joy's formulas divide by the direction cosine $c_z$ and fail for an electron moving exactly parallel to the surface; we use the equivalent rotation $c'=c\cos\varphi+\sin\varphi\,(\hat e_1\cos\psi+\hat e_2\sin\psi)$ with two unit vectors $\hat e_{1,2}$ perpendicular to $c$, built from $c$ without that division. Check M4 confirms on 20 000 random cases, including directions parallel to the surface, that the new vector has unit length and makes exactly the angle $\varphi$ with the old one.</p>
<p>The loop runs until the electron leaves or stops. The page runs 2000 electrons for each setting, each with its own stream of pseudo-random numbers (the 32-bit generator mulberry32, seeded per electron), so the same settings always give the same numbers, and the Python reference <code>ref/ch06.py</code> reproduces the browser's numbers from the same streams (parity check: about $10^{-9}$, from last-bit differences of library functions).</p>
<p><b>How sure is a count of 2000?</b> Whether a given electron comes back is a coin with probability $\eta$; for $N$ electrons the count has the binomial standard deviation, so the estimate $\hat\eta$ carries the standard error $u_\eta=\sqrt{\eta(1-\eta)/N}$. For $\delta$ the spread of the individual electrons' contributions gives $u_\delta$ in the same way. Both are readouts of the simulation, and the text quotes them.</p>
<div class="pbox"><span class="pbox__t">Key result · what one simulated electron needs</span><p>Two probability laws and one rate: free paths $s=-\lambda_\mathrm{el}\ln R$ from the screened Rutherford cross-section, turns $\cos\varphi=1-2aR/(1+a-R)$, and a continuous loss $|\mathrm dE/\mathrm ds|$ from the Bethe–Joy–Luo stopping power. The statistical error of every count falls as $1/\sqrt N$.</p></div>
'''})

S.append({'id': 'yields', 'title': 'What comes back: η and δ', 'html': r'''
<p><b>Backscattering.</b> The simulated $\eta$ is compared in {{fig:eta}} with the measurements collected by Akbari et al. (an open database, CC BY 4.0; <code>data/ch06/README.md</code> gives its provenance). For silicon and aluminium the agreement is within the spread of the measurements at all energies, also below 1 keV, where Joy warns that the model is not meant to work: between 0.4 and 2 keV the simulation gives {{num:eb_Si_lo_mc}} for silicon and the {{num:eb_Si_lo_n}} measurements average {{num:eb_Si_lo_me}}. For the heavy elements the model is too generous. Gold backscatters {{num:eb_Au_hi_mc}} in the simulation against {{num:eb_Au_hi_me}} measured between 8 and 31 keV, and {{num:eb_Au_lo_mc}} against {{num:eb_Au_lo_me}} between 0.4 and 2 keV; copper lies between ({{num:eb_Cu_lo_mc}} against {{num:eb_Cu_lo_me}} at low energy). That is the failure Joy predicts: at low energy and high $Z$ the electron feels the nucleus close in, where spin and relativity matter and the Mott cross-section differs from Rutherford's. So the model is honest for silicon and aluminium and overstates the backscattering of copper and gold, most at low energy (check M9 records all bands).</p>
{{figure:eta}}
<p><b>Secondary electrons.</b> Lin and Joy model the secondary yield in two steps (their Eqs. 1 to 3). Energy lost by the beam makes secondaries at the rate $\frac1\varepsilon|\mathrm dE/\mathrm ds|$ per path length, where $\varepsilon$ is the mean energy spent per secondary electron, and a secondary born at depth $z$ escapes with probability $\tfrac12\mathrm e^{-z/\lambda_s}$: half of them start towards the surface, and on the way they are absorbed with the escape depth $\lambda_s$. Lin and Joy fitted $\varepsilon$ and $\lambda_s$ to the measured yield curves of each element with their own Monte Carlo (their Table 1: silicon 90 eV and 2.7 nm, gold 35 eV and 0.5 nm). We add these escape weights along every step of every electron, exactly for each straight piece (check M5), on the way in and on the way out; so $\delta$ counts both the secondaries made by the incoming beam and those made by the backscattered electrons leaving.</p>
<p>{{fig:delta}} compares the result with Lin and Joy's universal law (their Eq. 12, with their $\delta_\mathrm{max}$ and the energy of the maximum) and with the values of their own Monte Carlo at 2 and 20 keV. At 800 eV in silicon the simulation gives $\delta=$ {{num:d_delta}} ± {{num:d_udelta}}, and the universal law {{num:law_Si_08}}: the two agree. At higher energy ours is smaller: at 20 keV {{num:dc_Si_mc20}} against their {{num:dc_Si_lj20}} for silicon, and {{num:dc_Au_mc20}} against {{num:dc_Au_lj20}} for gold (check M10). We use their constants and their stated equations; the difference must lie in parts of their simulation the paper does not give (its elastic cross-section and stopping power for the fast backscattered electrons). We record the gap rather than tune it away.</p>
{{figure:delta}}
<div class="pbox pbox--ex"><span class="pbox__t">Example 6.1 · silicon at 800 V</span>
<p>The default probe lands with 800 eV on silicon. Of 2000 simulated electrons a fraction $\eta=$ {{num:d_eta}} ± {{num:d_ueta}} comes back as backscattered electrons, and each incident electron frees on average $\delta=$ {{num:d_delta}} ± {{num:d_udelta}} secondary electrons. Gold at the same voltage gives $\eta=$ {{num:au_eta}} and $\delta=$ {{num:au_delta}} (the $\eta$ too high, as above). Together $\delta+\eta=$ {{num:d_sum}}: about as many electrons leave as arrive, so at this voltage even an insulating surface would charge little. The model itself has no charging, and a conductive silicon wafer drains any charge to ground.</p></div>
'''})

S.append({'id': 'volume', 'title': 'How far the electrons go', 'html': r'''
<p>The classic estimate of how deep electrons go is the range of K. Kanaya and S. Okayama (<em>J. Phys. D</em> 5 (1972) 43; we use the formula as Goldstein et al. quote it, not the original),</p>
$$ R_\mathrm{KO}=27.6\,\frac{A\,E^{1.67}}{Z^{0.89}\,\rho}\ \mathrm{nm} \label{ko6} $$
<p>with $A$ in g mol<sup>−1</sup>, $\rho$ in g cm<sup>−3</sup> and $E$ in keV. The power 1.67 is the integral of the stopping power: with $|\mathrm dE/\mathrm ds|\propto1/E$ (ignoring the slow logarithm) the path to stop grows as $E^2$, and the logarithm and the scattering bring the exponent down. The range grows almost as the square of the energy. That is the whole case for low-voltage metrology in one line.</p>
<p>From the simulation we take two more measures. The radius $r_{90}$ of the hemisphere about the point of impact that holds 90 % of the energy left in the wafer, and the interaction volume $V_\mathrm{int}=\tfrac23\pi r_{90}^3$ defined by it. And the lateral spread $\sigma_s$ of the secondary-electron signal: the root mean square distance, along one direction across the surface, of the points where escaping secondaries are born, weighted by their escape probability. It is what blurs an edge in the image beyond the size of the probe.</p>
<div class="pbox pbox--ex"><span class="pbox__t">Example 6.2 · 800 V against 30 kV in silicon</span>
<p>At 800 V the Kanaya–Okayama range is {{num:d_R}} nm, 90 % of the energy stays within {{num:d_r90}} nm of the point of impact, and the secondary signal spreads with $\sigma_s=$ {{num:d_sig}} nm, the same order as the probe of chapter 5. At 30 kV the range is {{num:k_Rum}} µm, $r_{90}=$ {{num:k_r90um}} µm, and $\sigma_s=$ {{num:k_sigum}} µm: the interaction volume is about {{num:vol_ratio}} times larger, and the secondary signal spreads {{num:sig_ratio}} times wider. The sharp secondaries made by the incoming beam are still there at 30 kV, but they ride on a broad halo made by backscattered electrons surfacing micrometres away, and the beam deposits its energy deep in the device. At low voltage both the halo and the damage are confined to the top tens of nanometres.</p></div>
<div class="pbox pbox--ex"><span class="pbox__t">Example 6.3 · gold at 800 V</span>
<p>In gold the range at 800 V is only {{num:au_R}} nm: the dense, heavy target stops and turns the electrons quickly. The simulation then sends back {{num:au_eta}} of them, which is too many by the comparison above; a design decision that rests on the backscatter of a heavy metal at low voltage needs the Mott cross-section.</p></div>
'''})

S.append({'id': 'checks', 'title': 'Checks, hand-over and limits', 'html': r'''
<p>The symbolic and numerical checks of this chapter, run by <code>derive/ch06.py</code>, which also stores the simulation runs behind the two figures (the page's own module, through Node, 2000 electrons per point):</p>
''' + checks_table() + r'''
<p><b>What chapter 7 receives.</b> The secondary yield $\delta$, the backscattering coefficient $\eta$ and the lateral spread $\sigma_s$ of the signal, for the material and voltage chosen, with their statistical errors.</p>
<p><b>What the model leaves out.</b> The Mott cross-section, which heavy elements at low energy need (shown above). Discrete energy losses (plasmons, inner-shell ionisation) and the energy spectrum of the backscattered electrons. The transport of the secondary electrons themselves, replaced by Lin and Joy's exponential escape. Charging of insulators, which at low voltage decides the contrast of resist and oxide. Compounds: no resist, no oxide, no layered stack, although the database has resist data. Above all, topography: the wafer here is flat, while a metrology tool looks at lines and edges, where secondaries escape through the side walls and the yield rises at the edge; chapter 7 models the edge as a signal profile instead. And the crystal: channelling in single-crystal silicon changes backscattering with the angle of incidence.</p>
<div class="pbox pbox--ex"><span class="pbox__t">Problems</span><ol>
<li>From {{eq:ruth6}} with the screened denominator, show that half of the elastic turns are smaller than the angle with $1-\cos\varphi=2a$, that is about $2\sqrt a$ for small $a$, and evaluate it for silicon at 800 eV and 30 keV.</li>
<li>Integrate $\mathrm ds=\mathrm dE/|\mathrm dE/\mathrm ds|$ with $|\mathrm dE/\mathrm ds|=c/E$ and a constant logarithm, to show that the path length to stop grows as $E^2$. Compare with the exponent of {{eq:ko6}} and say what makes the difference.</li>
<li>Run the simulation for silicon from 0.5 to 5 kV and plot $\delta+\eta$. At which voltage does it cross one, and what would that mean for an insulating sample?</li>
</ol></div>
<p><b>Sources.</b> D. C. Joy, "An introduction to Monte Carlo simulations", <em>Scanning Microscopy</em> 5 (1991) 329–337, <a href="https://digitalcommons.usu.edu/microscopy/vol5/iss2/4">open copy</a>, read in full: Eqs. 1–4, 6, 7, 11 and 12 and the remarks on validity. Y. Lin, D. C. Joy, "A new examination of secondary electron yield data", <em>Surf. Interface Anal.</em> 37 (2005) 895–900, doi 10.1002/sia.2107, read: Eqs. 1 to 3 and 12, Eq. 13, Table 1. D. C. Joy, S. Luo, R. Gauvin, P. Hovington, N. Evans, "Experimental measurements of electron stopping power at low energies", <em>Scanning Microscopy</em> 10 (1996), <a href="https://digitalcommons.usu.edu/microscopy/vol10/iss3/4">open copy</a>, read: Table 2 and the discussion of $k$. Backscattering data: F. Akbari et al., <em>Medical Physics</em> (2023), doi 10.1002/mp.16604, data doi 10.5281/zenodo.7810951. Stopping powers: NIST ESTAR. Kanaya–Okayama: as quoted by J. I. Goldstein et al., <em>Scanning Electron Microscopy and X-Ray Microanalysis</em>, Springer 2017 (abstract only); the 1972 paper was not opened.</p>
'''})

CH = {
    'title': 'Scan and hit',
    'lead': 'What the electrons of the probe do inside the wafer: they turn at the nuclei and slow down among the electrons, and some come back out. We follow them one by one in a Monte Carlo simulation built on the screened Rutherford cross-section and the Bethe stopping power, count the backscattered and secondary electrons, measure how far the electrons wander, and compare the counts with a database of measurements and with published simulations.',
    'sections': S,
    'figures': {
        'eta': {'svg': fig_eta(), 'caption': 'Backscattering coefficient against landing energy for silicon, aluminium, copper and gold: this chapter\'s Monte Carlo (lines, 2000 electrons per point, stored runs of the page\'s own module) and the measurements of the Akbari et al. database (circles). The simulation overstates the heavy elements, most at low energy.'},
        'delta': {'svg': fig_delta(), 'caption': 'Secondary-electron yield against landing energy for silicon and gold: this chapter\'s Monte Carlo (solid), Lin and Joy\'s universal law with their δ<sub>max</sub> and energy of the maximum (dashed), and the values of their own Monte Carlo at 2 and 20 keV (squares). Both simulations use the same ε and λ<sub>s</sub>.'},
    },
    'numbers': NUMS,
    'literals': LITERALS,
    'sim': {'module': 'ch06', 'title': 'Electrons in the wafer'},
}

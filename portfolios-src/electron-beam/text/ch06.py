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
for tag, inp in (('d', {}), ('k', {'V_land': 30000.0})):
    mod(tag + '_core', inp, 'sig_core', scale=1e9, sig=2)
    mod(tag + '_fcore', inp, 'f_core', scale=100, sig=2)
    mod(tag + '_halo', inp, 'sig_halo', scale=1e9, sig=2)
mod('k_halo_um', {'V_land': 30000.0}, 'sig_halo', scale=1e6, sig=2)
ex('d_sum', 'a+b', {'a': 'd_eta', 'b': 'd_delta'}, sig=2)
ex('au20_over_law', '100*(a/b-1)', {'a': 'dc_Au_mc20', 'b': 'law_Au_20'}, sig=2)
ex('vol_ratio', '(b/a)**3', {'a': 'd_r90', 'b': 'k_r90'}, sig=1)
ex('sig_ratio', 'b/a', {'a': 'd_sig', 'b': 'k_sig'}, sig=2)
# gold at 800 V
mod('au_eta', {'material': 'Au'}, 'eta_BSE', sig=2)
mod('au_delta', {'material': 'Au'}, 'delta_SE', sig=2)
mod('au_R', {'material': 'Au'}, 'R', scale=1e9, sig=2)
ex('au_sum', 'a+b', {'a': 'au_eta', 'b': 'au_delta'}, sig=2)
ex('au_over_law', '100*(a/b-1)', {'a': 'au_delta', 'b': 'law_Au_08'}, sig=2)
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
const('law_Au_08', law(0.8, 'Au'), sig=2)
const('law_Au_20', law(20.0, 'Au'), sig=2)
const('au_dmax', LJ['Au']['dmax'], sig=3)
const('au_Emax', LJ['Au']['Emax'] * 1e3, sig=2)
const('loss_mfp', DN['loss_per_mfp_eV'], sig=2)
const('plasmon', DN['plasmon_eV'], sig=3)
const('zab_Si', DN['zab_Si'], sig=2)
const('zab_Au', DN['zab_Au'], sig=2)
const('mfp_Au_08', DN['mfp_Au_08'], sig=2)
const('spacing_Au', DN['spacing_Au'], sig=2)
const('mr_Si', round(DN['mass_ratio']['Si'], -3), sig=2)
const('mr_Au', round(DN['mass_ratio']['Au'], -4), sig=2)
const('c78500', DN['c78500'], sig=3)
ex('joy1024', '100*(1-(1022/1024)**2)', {}, sig=1)
# a deflector: the field-length product that sweeps a 1 um field at 800 V with the pivot 3 mm above the wafer
mod('p800', {'V_acc': 800.0, 'V_land': 800.0}, 'V_star', module='ch03', sig=6)
ex('defl_theta', '0.5e-6/3e-3*1e3', {}, sig=2)                                                       # mrad, half-field 0.5 um over 3 mm
ex('defl_B', '(0.5e-6/3e-3)*sqrt(2*9.1093837015e-31*1.602176634e-19*v)/1.602176634e-19/5e-3*1e6', {'v': 'p800'}, sig=2)  # uT over 5 mm
const('si_dmax', LJ['Si']['dmax'], sig=2)
const('si_Emax', LJ['Si']['Emax'] * 1e3, sig=2)

LITERALS = {
    '0.67449': 'median of |x| over sigma for a Gaussian', 'three core widths': 'the cut of the core, a choice',
    '10 −21': 'exponent of Joy\'s constant', 'Eq. 13,': 'equation number of Lin and Joy', '2.718': 'Euler\'s number', '10^{-13}': 'the measured parity agreement of the readouts',
    '5, 329, 1991': 'volume, page and year of Joy 1991', '37, 895, 2005': 'volume, page and year of Lin and Joy', '800 eV': 'the default landing energy, a given',
    '30 keV': 'an energy of the comparison, a given', '3.4\\times10^{-3}': 'Bishop\'s screening constant, quoted', '5.21\\times10^{-21}': 'Joy\'s constant, quoted',
    '0.795': 'Joy et al.\'s fitted k for silicon, quoted', '0.832': 'Joy et al.\'s fitted k for gold, quoted', '32-bit': 'the word size of the generator',
    '2.3\\lambda': 'ln 10 = 2.3, the tenth-percentile path', '10^{-9}': 'the measured parity agreement', '0.4 and 2 keV': 'an energy band, a choice',
    '8 and 31 keV': 'an energy band, a choice', 'Eq. 12,': 'equation number of Lin and Joy', '20 keV': 'an energy of Lin and Joy\'s table', '329–337': 'pages of Joy 1991', '–337,': 'last page of Joy 1991', '–900,': 'last page of Lin and Joy',
    '895–900': 'pages of Lin and Joy', 'Eqs. 1 to 3 and 12, Eq. 13,': 'equation numbers of Lin and Joy',
    'Example 6.2': 'the number of a worked example', 'Example 6.3': 'the number of a worked example', 'Example 6.4': 'the number of a worked example', 'Example 6.1': 'the number of a worked example', '1 µm': 'a field of view, a given', '3 mm above': 'pivot height, a given', '5 mm long': 'deflector length, a given', 'tens of microtesla': 'the Earth\'s field, rounded', '1 eV': 'rounded lower end of the logarithm', '6 eV': 'rounded lower end of the logarithm', 'one part in 10 000': 'rounded 4m/M for silicon',
    '800 V': 'the landing voltage of the default, a given', '30 kV': 'a given of Example 6.3', '2000': 'the number of simulated electrons, a given',
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
    rows = ''.join('<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (c['id'], html.escape(c['title']), ('recorded' if c.get('record') else 'pass') if c['ok'] else 'FAIL', html.escape(c['detail']))
                   for c in DER['checks'])
    return '<div class="ptab-wrap"><table class="ptab ptab--checks"><thead><tr><th>check</th><th>what is verified</th><th>result</th><th>detail</th></tr></thead><tbody>%s</tbody></table></div>' % rows


COL = {'Si': '#7a1f2b', 'Al': '#8b8079', 'Cu': '#7a4b12', 'Au': '#3a322e'}
# Label size of the figures: 23 units of the 640-unit width on a phone (11 px on a 360 px screen), 17 on a small tablet, 15 on a wide
# screen (16 to 17 px). Every label is placed for the largest size, so it stays clear of the drawing at all three: the element names
# sit beyond the right end of their curves, the keys below the axis title.
SVGCSS = ('<style>.pfig svg.ebf text{font-family:\'IBM Plex Mono\',monospace;font-size:23px}'
          '@media (min-width:480px){.pfig svg.ebf text{font-size:17px}}@media (min-width:760px){.pfig svg.ebf text{font-size:15px}}</style>')
ST = 'fill:#3a322e'


def _frame(W, H, L, Rr, T, Bt, ylab, yticks, Y):
    out = ['<svg class="ebf" viewBox="0 0 %d %d" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="%s">' % (W, H, html.escape(ylab)), SVGCSS,
           '<rect width="%d" height="%d" fill="#fff"/><rect x="%d" y="%d" width="%d" height="%d" fill="none" stroke="#d9d0c2" data-nocollide=""/>' % (W, H, L, T, Rr - L, Bt - T)]
    X = lambda E: L + (math.log10(E) - math.log10(0.5)) / (math.log10(30) - math.log10(0.5)) * (Rr - L)
    for E, lab in ((0.5, '0.5'), (1, '1'), (2, '2'), (5, '5'), (10, '10'), (20, '20'), (30, '30')):
        out.append('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="#eee7da" data-nocollide=""/><text x="%.1f" y="%d" text-anchor="middle" style="%s">%s</text>' % (X(E), T, X(E), Bt, X(E), Bt + 34, ST, lab))
    for v, lab in yticks:
        y = Y(v)
        out.append('<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="#eee7da" data-nocollide=""/><text x="%d" y="%.1f" text-anchor="end" style="%s">%s</text>' % (L, y, Rr, y, L - 8, y + 7, ST, lab))
    out.append('<text x="%d" y="%d" text-anchor="middle" style="%s">landing energy (keV), logarithmic</text>' % ((L + Rr) // 2, Bt + 68, ST))
    out.append('<text x="%d" y="%d" style="%s">%s</text>' % (16, T - 20, ST, html.escape(ylab)))
    return out, X


def _names(out, ends, Rr, lo, hi):
    """Element names beyond the right end of their curves, pushed apart to 26 units where two ends are close, each with a short leader."""
    ends = sorted(ends, key=lambda e: e[1])
    ys = []
    for _, y, _ in ends:
        ys.append(max(y + 8, ys[-1] + 26) if ys else max(y + 8, lo + 21))
    over = ys[-1] - hi if ys else 0
    if over > 0:
        ys = [v - over for v in ys]
    for (mt, y, col), yl in zip(ends, ys):
        out.append('<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="%s"/><text x="%d" y="%.1f" style="%s;fill:%s">%s</text>' % (Rr + 3, y, Rr + 11, yl - 8, col, Rr + 14, yl, ST, col, mt))


def fig_eta():
    W, H, L, Rr, T, Bt = 640, 458, 72, 590, 52, 338
    Y = lambda v: Bt - v / 0.7 * (Bt - T)
    out, X = _frame(W, H, L, Rr, T, Bt, 'backscattering coefficient η', [(v, '%.1f' % v) for v in (0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7)], Y)
    ends = []
    for mt in ('Si', 'Al', 'Cu', 'Au'):
        col = COL[mt]
        for E, e in RUNS['database'].get(mt, []):
            if 0.5 <= E <= 30:
                out.append('<circle cx="%.1f" cy="%.1f" r="2.6" fill="none" stroke="%s" stroke-width="1"/>' % (X(E), Y(e), col))
        pts = [(r['E_keV'], r['eta']) for r in RUNS['runs'][mt]]
        out.append('<polyline fill="none" stroke="%s" stroke-width="2.2" points="%s"/>' % (col, ' '.join('%.1f,%.1f' % (X(E), Y(e)) for E, e in pts)))
        ends.append((mt, Y(pts[-1][1]), col))
    _names(out, ends, Rr, T, Bt)
    out.append('<text x="%d" y="%d" style="%s">lines: Monte Carlo · circles: measured</text>' % (16, Bt + 108, ST))
    out.append('</svg>')
    return ''.join(out)


def fig_delta():
    W, H, L, Rr, T, Bt = 640, 486, 72, 590, 52, 338
    lo, hi = math.log10(0.02), math.log10(2.0)
    Y = lambda v: Bt - (math.log10(max(v, 1e-3)) - lo) / (hi - lo) * (Bt - T)
    out, X = _frame(W, H, L, Rr, T, Bt, 'secondary-electron yield δ, logarithmic', [(v, str(v)) for v in (0.02, 0.05, 0.1, 0.2, 0.5, 1, 2)], Y)
    ends = []
    for mt in ('Si', 'Au'):
        col = COL[mt]
        Es = [0.5 * 60 ** (i / 80) for i in range(81)]
        out.append('<polyline fill="none" stroke="%s" stroke-width="1.4" stroke-dasharray="5 4" points="%s"/>' % (col, ' '.join('%.1f,%.1f' % (X(E), Y(law(E, mt))) for E in Es)))
        pts = [(r['E_keV'], r['delta']) for r in RUNS['runs'][mt]]
        out.append('<polyline fill="none" stroke="%s" stroke-width="2.2" points="%s"/>' % (col, ' '.join('%.1f,%.1f' % (X(E), Y(d)) for E, d in pts)))
        for E, key in ((2.0, 'd2'), (20.0, 'd20')):
            v = LJ[mt][key]
            out.append('<rect x="%.1f" y="%.1f" width="7" height="7" fill="none" stroke="%s" stroke-width="1.3"/>' % (X(E) - 3.5, Y(v) - 3.5, col))
        ends.append((mt, Y(pts[-1][1]), col))
    _names(out, ends, Rr, T, Bt)
    out.append('<text x="%d" y="%d" style="%s">solid: ours · dashed: universal law</text>' % (16, Bt + 108, ST))
    out.append('<text x="%d" y="%d" style="%s">squares: Lin and Joy’s Monte Carlo</text>' % (16, Bt + 136, ST))
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
<p>Throw a handful of marbles into a box of loosely packed heavier balls. Each marble rattles about, changes direction at every hit, and slows down; some bounce back out of the box, the rest come to rest inside. An electron entering a wafer does the same, with two kinds of collision. It is deflected by the atomic nuclei, which are far heavier than it is ({{num:mr_Si}} times for silicon, {{num:mr_Au}} times for gold). Such a hit turns it while taking away at most four times the mass ratio of its energy, about one part in 10 000 for silicon: an <em>elastic</em> collision. And it loses energy to the electrons of the solid in many small bites, ionising and exciting as it goes, <em>inelastic</em> collisions, which hardly turn it.</p>
<p>What comes back out is the signal of the microscope. Electrons that turn round and leave with most of their energy are <em>backscattered electrons</em> (BSE); their number per incident electron is the backscattering coefficient $\eta$. The energy the beam leaves in the solid frees slow electrons of a few electronvolts, and those born within a few nanometres of the surface can escape. These are the <em>secondary electrons</em> (SE), by convention those leaving with less than 50 eV, and their number per incident electron is the <em>secondary yield</em> $\delta$. A secondary electron made by the incoming beam right where it enters carries the sharp information. One made by a backscattered electron on its way out comes from wherever that electron surfaced, which can be far from the beam. How far the electrons wander, and how many come back, is what this chapter computes, for the probe of chapter 5 landing on silicon, aluminium, copper or gold.</p>
<p>No closed formula follows hundreds of random turns. We follow the electrons one by one instead, drawing each turn and each free path from the probability laws of the two collisions: a Monte Carlo simulation, in the form D. C. Joy describes (<em>Scanning Microscopy</em> 5, 329, 1991), with the secondary-electron model of Y. Lin and D. C. Joy (<em>Surf. Interface Anal.</em> 37, 895, 2005).</p>
'''})

S.append({'id': 'scan', 'title': 'Scanning the probe', 'html': r'''
<p>To make an image the probe is moved over the wafer line by line, as the spot of an old television tube was. A pair of deflection coils above the objective tilts the beam by a small angle, and the lens turns that tilt into a sideways shift on the wafer. The physics is chapter 1's. An electron of momentum $p$ that crosses a transverse magnetic field $B$ over a length $\ell$ leaves turned by the small angle $\theta=eB\ell/p$, because the sideways force $evB$ acts for the time $\ell/v$ and gives the sideways momentum $eB\ell$. With the pivot of the deflection a distance $L$ above the wafer, the spot moves by $L\theta$.</p>
<div class="pbox pbox--ex"><span class="pbox__t">Example 6.1 · how much field a scan needs</span>
<p>To sweep a field of view of 1 µm, half of it on each side, with the pivot 3 mm above the wafer, the beam must turn by {{num:defl_theta}} mrad. At 800 V a deflector 5 mm long does that with $B=\theta p/(e\ell)=$ {{num:defl_B}} µT, a field smaller than the Earth's, which is some tens of microtesla. That is why electron columns are shielded with soft iron and why stray fields from the fab blur images. A field the size of the scan field, varying in time, moves the spot as much as the scan does.</p></div>
<p>Each point of the scan is a <em>pixel</em>, held for the <em>dwell time</em> $t_d$; chapter 7 counts the electrons that a pixel returns. This chapter asks what happens to the beam electrons at one point.</p>
'''})

S.append({'id': 'elastic', 'title': 'Turning: the screened Rutherford cross-section', 'html': r'''
<p>An electron passing a nucleus of charge $Ze$ is pulled by the Coulomb force and leaves turned by an angle $\varphi$. Rutherford's calculation of this two-body problem gives the probability of a turn into the solid angle $\mathrm d\Omega$ as an effective target area, the differential cross-section. For a fast electron of momentum $p$ and speed $v$ it is</p>
$$ \frac{\mathrm d\sigma}{\mathrm d\Omega}=\left(\frac{Ze^2}{4\pi\varepsilon_0}\right)^2\frac{1}{(pv)^2}\,\frac{1}{(1-\cos\varphi)^2} , \label{ruth6} $$
<p>which in the non-relativistic case, $pv=2E$, is the textbook form with $\sin^4(\varphi/2)$ in the denominator. ★ It follows from the orbit. An electron that would pass the nucleus at the distance $b$ (the impact parameter) if it were not deflected is turned by $\varphi$ with $\tan(\varphi/2)=k/(pv\,b)$, $k=Ze^2/4\pi\varepsilon_0$. This is the hyperbola of the Kepler problem. The nucleus attracts the electron as the Sun attracts a passing comet, and the deflection obeys the same formula as for the repelled alpha particles of Rutherford. The electrons that pass through the ring between $b$ and $b+\mathrm db$, of area $2\pi b\,\mathrm db$, leave into the cone between $\varphi$ and $\varphi+\mathrm d\varphi$, of solid angle $2\pi\sin\varphi\,\mathrm d\varphi$. So $\mathrm d\sigma/\mathrm d\Omega=b\,|\mathrm db/\mathrm d\varphi|/\sin\varphi$, which with $b=(k/pv)\cot(\varphi/2)$ is {{eq:ruth6}} (check M2). The formula diverges at small angles because a bare Coulomb field reaches to infinity. In a solid the atom's own electrons screen the nucleus beyond about an atomic radius, which removes the divergence. Joy, following Bishop (1976), writes the screening as a shift of the denominator to $(1-\cos\varphi+2a)^2$, with the screening parameter</p>
$$ a=3.4\times10^{-3}\,\frac{Z^{0.67}}{E/\mathrm{keV}} , \label{screen6} $$
<p>fitted so that simulated backscattering agrees with experiment. Integrating the screened form over all directions (check M1),</p>
$$ \int\frac{\mathrm d\Omega}{(1-\cos\varphi+2a)^2}=2\pi\int_0^2\frac{\mathrm du}{(u+2a)^2}=\frac{\pi}{a(1+a)},\qquad u=1-\cos\varphi , \notag $$
<p>gives the total elastic cross-section, and with $pv=E(E+2mc^2)/(E+mc^2)$ (check M3)</p>
$$ \sigma_E=\left(\frac{Ze^2}{4\pi\varepsilon_0}\right)^2\frac{\pi}{a(1+a)}\,\frac{1}{E^2}\left(\frac{E+mc^2}{E+2mc^2}\right)^2 . \label{sigma6} $$
<p>Joy's Eq. 1 writes the same with numbers, $E$ in keV:</p>
$$ \sigma_E=5.21\times10^{-21}\,\frac{Z^2}{E^2}\,\frac{4\pi}{a(1+a)}\left(\frac{E+511}{E+1024}\right)^2\ \mathrm{cm}^2 . \label{sigmajoy6} $$
<p>The constant follows from $(e^2/4\pi\varepsilon_0)^2/4=$ {{num:joy_const}}×10<sup>−21</sup> keV<sup>2</sup> cm<sup>2</sup>, and the 4 cancels the quarter that $((E+511)/(E+1022))^2$ tends to at low energy. Joy prints 5.21 (half a per cent higher, check M3) and 1024 for $2mc^2=1022$ keV ({{num:joy1024}} % lower in $\sigma_E$ at low energy). The two nearly cancel, and we use his numbers as printed. A beam crossing a solid with $n=N_A\rho/A$ atoms per volume ($\rho$ the density, $A$ the molar mass, $N_A$ Avogadro's number) meets a nucleus on average once per <em>elastic mean free path</em></p>
$$ \lambda_\mathrm{el}=\frac{A}{N_A\,\rho\,\sigma_E} . \label{mfp6} $$
<p>In silicon it is {{num:mfp_Si_08}} nm at 800 eV, {{num:mfp_Si_30}} nm at 30 keV and {{num:mfp_Si_100}} nm at 100 keV. The angle at each hit is mostly small. For silicon at 800 eV the screening parameter is a few hundredths, and half of the turns are smaller than about $2\sqrt a$ radians. In gold at 800 eV the formula gives {{num:mfp_Au_08}} nm, less than the spacing between gold atoms, {{num:spacing_Au}} nm. There the picture of separate collisions with single atoms has lost its meaning, and the model is a parametrisation rather than a description.</p>
<p>The cross-section has known weaknesses. Rutherford's formula treats the electron as a classical particle in a point-charge field and ignores its spin. Bishop's screening parameter was fitted to measured backscattering, so agreement with backscattering data is partly built in. A measure of how strong the nucleus's field is for the passing electron is the Sommerfeld parameter $Z\alpha_\mathrm{fs}/\beta$ ($\alpha_\mathrm{fs}$ the fine-structure constant, $\beta=v/c$). The simple treatments of the screened field need it small. At 800 eV it is {{num:zab_Si}} for silicon and {{num:zab_Au}} for gold. For heavy elements and low energies the proper replacement is the Mott cross-section from the Dirac equation. In Joy's words, "at such low energies the Rutherford cross-section is not accurate and a Mott cross-section must be used". He also states plainly that his models "are not, in principle, suitable for incident beam energies below 1 keV". Our default, 800 eV, is below that. We use the model anyway, because it is open and simple, and we measure its error against data in {{sec:ch06-yields}}.</p>
'''})

S.append({'id': 'loss', 'title': 'Slowing down: the stopping power', 'html': r'''
<p>Between the elastic turns the electron loses energy to the electrons of the solid. A single loss is usually tens of electronvolts, small against keV, and there are many of them per mean free path. Joy therefore lets the energy fall continuously along the path, at the rate given by Bethe's stopping power. In the low-energy form of Joy and Luo, which Lin and Joy use (their Eq. 13, written here per length, with the density),</p>
$$ -\frac{\mathrm dE}{\mathrm ds}=78\,500\,\frac{\rho Z}{AE}\,\ln\!\left(\frac{1.166\,(E+kJ)}{J}\right)\ \frac{\mathrm{keV}}{\mathrm{cm}},\qquad k=0.85 , \label{bethe6} $$
<p>with $\rho$ in g cm<sup>−3</sup>, $A$ in g mol<sup>−1</sup> and $E$ in keV. The picture behind Bethe's formula is a fast charge sweeping past the atomic electrons. Each feels a short electric pulse and takes up momentum, the more the slower the charge passes, hence the $1/E$. The numbers are not arbitrary: $78\,500\approx2\pi(e^2/4\pi\varepsilon_0)^2N_A=$ {{num:c78500}} keV<sup>2</sup> cm<sup>2</sup> mol<sup>−1</sup>, and $1.166=\sqrt{\mathrm e/2}$ with $\mathrm e=2.718\ldots$ (check M8). The logarithm counts the range of distances over which the pulse is short enough to excite an electron of typical binding energy $J$, the <em>mean ionisation energy</em>. Joy's Eq. 12 (Berger and Seltzer) gives it as $J=(9.76Z+58.5Z^{-0.19})$ eV, {{num:J_Si}} eV for silicon and {{num:J_Au}} eV for gold, within 3 % of the values NIST uses (check M7). The term $kJ$ is Joy and Luo's empirical change. Without it the logarithm turns negative below $E=J/1.166$, which is meaningless. With it the logarithm stays positive down to $E=(1/1.166-k)J$, about 1 eV for silicon and 6 eV for gold, far below the 50 eV at which we stop following an electron. By their measurements it fits stopping powers down to about 50 eV (D. C. Joy et al., <em>Scanning Microscopy</em> 10, 1996, Table 2 gives fitted $k$ of 0.795 for silicon and 0.832 for gold. We keep 0.85, the value Lin and Joy used with their secondary-electron constants).</p>
<p>Treating the loss as continuous needs many small losses between two elastic turns. At 800 eV in silicon the loss per elastic mean free path is only {{num:loss_mfp}} eV, about one plasmon (the collective oscillation of the valence electrons, {{num:plasmon}} eV for silicon's four valence electrons per atom in the free-electron model). At the default the continuous loss is therefore an average over a few events, one more approximation of the model at low energy. At 30 keV the elastic steps are long and hold hundreds of losses.</p>
<p>The NIST table ESTAR lists the stopping power computed from the full relativistic Bethe theory. The comparison (table below, check M7; ESTAR gives the stopping power per areal density, so we divide ours by the density). From 5 to 30 keV the two agree to between {{num:es_mid_lo}} and {{num:es_mid_hi}}. Below, Joy–Luo is larger, up to {{num:es_lo_hi}} times for gold at 1 keV, where Bethe's theory itself is no longer valid and neither number is a measurement. Above, Joy–Luo falls behind ({{num:es_100}} at 100 keV) because it is non-relativistic: the true stopping power goes as $1/\beta^2$, not as $1/E$, and $\beta^2/(2E/mc^2)=$ {{num:es_100_beta}} at 100 keV. The chapter's range ends at 30 keV, inside the band of agreement.</p>
''' + estar_table()})

S.append({'id': 'loop', 'title': 'The Monte Carlo loop', 'html': r'''
<p>Each electron starts at the point of impact, heading straight into the wafer with the landing energy $E$. Then the same four steps repeat.</p>
<p><b>1. A free path.</b> The chance of travelling a distance $s$ without an elastic hit falls as $\mathrm e^{-s/\lambda_\mathrm{el}}$, the law of a constant hazard. A path with this distribution is $s=-\lambda_\mathrm{el}\ln\xi_1$, with $\xi_1$ a random number uniform between 0 and 1: the fraction of paths longer than $s$ is the fraction of $\xi_1$ below $\mathrm e^{-s/\lambda_\mathrm{el}}$ (check M4). Ten per cent of the paths are longer than $2.3\lambda_\mathrm{el}$.</p>
<p><b>2. A move and a loss.</b> The electron moves $s$ along its direction and loses $s\,|\mathrm dE/\mathrm ds|$ by {{eq:bethe6}}. If the step would take it above the surface, it is cut there. The electron has left the wafer, and it counts as backscattered if its energy is still above 50 eV. If the loss would take its energy below 50 eV, the step is cut where that happens and the electron stops.</p>
<p><b>3. A turn.</b> The polar angle of the elastic hit comes from the same trick applied to the angular distribution. The fraction of hits that turn by less than $\varphi$ is, from the integral above, $F(\varphi)=(1+a)(1-\cos\varphi)/(1-\cos\varphi+2a)$. Setting it equal to a second random number $\xi_2$ and solving for $\cos\varphi$ gives Joy's Eq. 6 (check M1),</p>
$$ \cos\varphi=1-\frac{2a\xi_2}{1+a-\xi_2} , \label{angle6} $$
<p>while the azimuth about the old direction is uniform, $\psi=2\pi\xi_3$.</p>
<p><b>4. A new direction.</b> The unit vector of motion is turned by $\varphi$ and $\psi$ about itself. Joy's formulas divide by the direction cosine $c_z$ and fail for an electron moving exactly parallel to the surface. We use the equivalent rotation $c'=c\cos\varphi+\sin\varphi\,(\hat e_1\cos\psi+\hat e_2\sin\psi)$ with two unit vectors $\hat e_{1,2}$ perpendicular to $c$, built from $c$ without that division. Check M5 confirms on 20 000 cases, random ones, directions parallel to the surface and directions along and near each axis, that the new vector has unit length and makes exactly the angle $\varphi$ with the old one.</p>
<p>The loop runs until the electron leaves or stops. The page runs 2000 electrons for each setting, each with its own stream of pseudo-random numbers (the 32-bit generator mulberry32, seeded per electron), so the same settings always give the same numbers. The Python reference <code>ref/ch06.py</code> reproduces the browser's numbers from the same streams (parity check: the readouts agree to about $10^{-13}$, the drawn paths to about $10^{-9}$, from last-bit differences of library functions). One setting takes up to a second at 30 kV, so the readouts follow the slider with a delay.</p>
<p><b>The statistical error of a count of 2000.</b> Whether a given electron comes back is a coin with probability $\eta$. For $N$ electrons the count has the binomial standard deviation, so the estimate $\hat\eta$ carries the standard error $u_\eta=\sqrt{\eta(1-\eta)/N}$. For $\delta$ the spread of the individual electrons' contributions gives $u_\delta$ in the same way. Both are readouts of the simulation, and the text quotes them. The lateral spread $\sigma_s$ below has no error estimate of its own. It is set by a few electrons that surface far away, so it fluctuates more than $\eta$ and $\delta$ do.</p>
<div class="pbox"><span class="pbox__t">Key result · what one simulated electron needs</span><p>Two probability laws and one rate: free paths $s=-\lambda_\mathrm{el}\ln\xi$ from the screened Rutherford cross-section, turns $\cos\varphi=1-2a\xi/(1+a-\xi)$, and a continuous loss $|\mathrm dE/\mathrm ds|$ from the Bethe–Joy–Luo stopping power. The statistical error of every count falls as $1/\sqrt N$.</p></div>
'''})

S.append({'id': 'yields', 'title': 'What comes back: η and δ', 'html': r'''
<p><b>Backscattering.</b> The simulated $\eta$ is compared in {{fig:eta}} with the measurements collected by Akbari et al. (an open database, CC BY 4.0; <code>data/ch06/README.md</code> gives its provenance). For silicon and aluminium the agreement is within the spread of the measurements at all energies, also below 1 keV, where Joy warns that the model is not meant to work. That agreement is partly by construction, because the screening parameter was fitted to backscattering data. Between 0.4 and 2 keV the simulation gives {{num:eb_Si_lo_mc}} for silicon and the {{num:eb_Si_lo_n}} measurements average {{num:eb_Si_lo_me}}. For the heavy elements the model is too generous. Gold backscatters {{num:eb_Au_hi_mc}} in the simulation against {{num:eb_Au_hi_me}} measured between 8 and 31 keV, and {{num:eb_Au_lo_mc}} against {{num:eb_Au_lo_me}} between 0.4 and 2 keV. Copper lies between ({{num:eb_Cu_lo_mc}} against {{num:eb_Cu_lo_me}} at low energy). For gold even the trend is wrong: the measured $\eta$ rises with energy, the simulated one falls. That is the failure Joy predicts for low energy and high $Z$, where the Rutherford cross-section is not accurate, and where the Sommerfeld parameter above is large. So the model is fair for silicon and aluminium and overstates the backscattering of copper and gold, most at low energy (check M11 records all bands).</p>
{{figure:eta}}
<p><b>Secondary electrons.</b> Lin and Joy model the secondary yield in two steps (their Eqs. 1 to 3). Energy lost by the beam makes secondaries at the rate $\frac1\varepsilon|\mathrm dE/\mathrm ds|$ per path length, where $\varepsilon$ is the mean energy spent per secondary electron. A secondary born at depth $z$ escapes with probability $\tfrac12\mathrm e^{-z/\lambda_s}$. Half of them start towards the surface, and on the way they are absorbed over the <em>escape depth</em> $\lambda_s$. Lin and Joy fitted $\varepsilon$ and $\lambda_s$ to the measured yield curves of each element with their own Monte Carlo (their Table 1: silicon 90 eV and 2.7 nm, gold 35 eV and 0.5 nm). We add these escape weights along every step of every electron, exactly for each straight piece (check M6), on the way in and on the way out. So $\delta$ counts both the secondaries made by the incoming beam and those made by the backscattered electrons leaving.</p>
<p>Lin and Joy also give a <em>universal law</em> (their Eq. 12) that describes measured yield curves of all elements by two numbers, the largest yield $\delta_\mathrm{max}$ and the energy $E_\mathrm{max}$ at which it occurs:</p>
$$ \frac{\delta}{\delta_\mathrm{max}}=1.28\left(\frac{E}{E_\mathrm{max}}\right)^{-0.67}\left[1-\exp\!\left(-1.614\left(\frac{E}{E_\mathrm{max}}\right)^{1.67}\right)\right] \label{law6} $$
<p>(silicon {{num:si_dmax}} at {{num:si_Emax}} eV, gold {{num:au_dmax}} at {{num:au_Emax}} eV, their Table 1). {{fig:delta}} compares our simulation with this law and with the values of their own Monte Carlo at 2 and 20 keV. At 800 eV in silicon the simulation gives $\delta=$ {{num:d_delta}} ± {{num:d_udelta}} and the law {{num:law_Si_08}}: they agree. For gold at 800 eV ours is {{num:au_over_law}} % above the law, and above their $\delta_\mathrm{max}$. At 20 keV ours is below their Monte Carlo for every element ({{num:dc_Si_mc20}} against {{num:dc_Si_lj20}} for silicon, {{num:dc_Au_mc20}} against {{num:dc_Au_lj20}} for gold, check M12). For gold it is {{num:au20_over_law}} % above their law, which their own Monte Carlo exceeds by more still. The simulations share $\varepsilon$, $\lambda_s$ and the equations the paper states. The paper does not give the rest of their simulation, so we cannot say where the difference comes from, and we record it rather than tune it away.</p>
{{figure:delta}}
<div class="pbox pbox--ex"><span class="pbox__t">Example 6.2 · silicon at 800 V</span>
<p>The default probe lands with 800 eV on silicon. Of 2000 simulated electrons a fraction $\eta=$ {{num:d_eta}} ± {{num:d_ueta}} comes back as backscattered electrons, and each incident electron frees on average $\delta=$ {{num:d_delta}} ± {{num:d_udelta}} secondary electrons. For silicon $\delta+\eta=$ {{num:d_sum}}: in this model 800 V is almost exactly the voltage at which as many electrons leave as arrive, so an insulating surface would hardly charge. Measured crossover voltages depend on the surface and we did not compare them. Gold at the same voltage gives $\eta=$ {{num:au_eta}} and $\delta=$ {{num:au_delta}}, together {{num:au_sum}}, both too high by the comparisons above. The model itself has no charging, and conductive silicon and gold drain any charge to ground.</p></div>
'''})

S.append({'id': 'volume', 'title': 'How far the electrons go', 'html': r'''
<p>The classic estimate of how deep electrons go is the range of K. Kanaya and S. Okayama (<em>J. Phys. D</em> 5 (1972) 43; we use the formula as Goldstein et al. quote it, not the original),</p>
$$ R_\mathrm{KO}=27.6\,\frac{A\,E^{1.67}}{Z^{0.89}\,\rho}\ \mathrm{nm} \label{ko6} $$
<p>with $A$ in g mol<sup>−1</sup>, $\rho$ in g cm<sup>−3</sup> and $E$ in keV. The power 1.67 is the integral of the stopping power. With $|\mathrm dE/\mathrm ds|\propto1/E$ (ignoring the slow logarithm) the path to stop grows as $E^2$, and the logarithm and the scattering bring the exponent down. The range therefore grows faster than the energy, roughly as its five-thirds power (Kanaya–Okayama). That is the whole case for low-voltage metrology in one line.</p>
<p>From the simulation we take two more measures. The radius $r_{90}$ of the hemisphere about the point of impact that holds 90 % of the energy left in the wafer, and the interaction volume $V_\mathrm{int}=\tfrac23\pi r_{90}^3$ defined by it. And the lateral spread $\sigma_s$ of the secondary-electron signal: the root mean square distance, along one direction across the surface, of the points where escaping secondaries are born, weighted by their escape probability. It is what blurs an edge in the image beyond the size of the probe. One root-mean-square number describes a two-part signal poorly: a sharp core of secondaries made where the beam enters, and a broad halo made by backscattered electrons surfacing far away. The halo sets $\sigma_s$, so at high voltage $\sigma_s$ overstates the blur of the sharp part. We therefore also split the signal. From a weighted histogram of where the escaping secondaries are born, the <em>core width</em> $\sigma_\mathrm{core}$ is the median distance divided by 0.67449 (the ratio for a Gaussian). The <em>core fraction</em> $f_\mathrm{core}$ is the share of the signal within three core widths, and the <em>halo width</em> $\sigma_\mathrm{halo}$ is the root-mean-square distance of the rest. The model lets a secondary escape where it is born. Its own sideways travel on the way out, of the order of the escape depth $\lambda_s$, is added to the core width in quadrature, $\sigma_\mathrm{core}^2=(\text{median width})^2+\lambda_s^2$, a rough allowance rather than a transport calculation. Chapter 7 blurs edges with the two parts separately.</p>
<div class="pbox pbox--ex"><span class="pbox__t">Example 6.3 · 800 V against 30 kV in silicon</span>
<p>At 800 V the Kanaya–Okayama range is {{num:d_R}} nm, and 90 % of the energy stays within {{num:d_r90}} nm of the point of impact. The secondary signal spreads with $\sigma_s=$ {{num:d_sig}} nm: {{num:d_fcore}} % of it in a core of {{num:d_core}} nm, the rest in a halo of {{num:d_halo}} nm, all of the order of the probe of chapter 5. At 30 kV the range is {{num:k_Rum}} µm, $r_{90}=$ {{num:k_r90um}} µm, and $\sigma_s=$ {{num:k_sigum}} µm: the interaction volume is about {{num:vol_ratio}} times larger, and the root-mean-square spread {{num:sig_ratio}} times wider. The split shows what that number hides. {{num:k_fcore}} % of the signal is still in a core of {{num:k_core}} nm, set by the escape depth because the incoming beam has not yet scattered sideways in the top nanometres. The rest is a halo of {{num:k_halo_um}} µm, made by backscattered electrons surfacing micrometres away. The halo lowers the contrast; the core keeps the edges sharp. Meanwhile the beam deposits its energy deep in the device. At low voltage both the halo and the damage are confined to the top tens of nanometres.</p></div>
<div class="pbox pbox--ex"><span class="pbox__t">Example 6.4 · gold at 800 V</span>
<p>In gold the range at 800 V is only {{num:au_R}} nm: the dense, heavy target stops and turns the electrons quickly. The simulation then sends back {{num:au_eta}} of them, which is too many by the comparison above. A design decision that rests on the backscattering of a heavy metal at low voltage needs the Mott cross-section.</p></div>
'''})

S.append({'id': 'checks', 'title': 'Checks, hand-over and limits', 'html': r'''
<p>The symbolic and numerical checks of this chapter, run by <code>derive/ch06.py</code>, which also stores the simulation runs behind the two figures (the page's own module, through Node, 2000 electrons per point):</p>
''' + checks_table() + r'''
<p><b>What chapter 7 receives.</b> The secondary yield $\delta$, the backscattering coefficient $\eta$ and the spread of the signal as core width, core fraction and halo width, for the material and voltage chosen, with their statistical errors.</p>
<p><b>What the model leaves out.</b> The Mott cross-section, which heavy elements at low energy need (shown above). Discrete energy losses (plasmons, inner-shell ionisation) and the energy spectrum of the backscattered electrons. The transport of the secondary electrons themselves, replaced by Lin and Joy's exponential escape. Charging of insulators, which at low voltage decides the contrast of resist and oxide. Compounds: no resist, no oxide, no layered stack, although the database has resist data. Above all, topography: the wafer here is flat. A metrology tool looks at lines and edges, where secondaries escape through the side walls and the yield rises at the edge. Chapter 7 models the edge as a signal profile instead. And the crystal: channelling in single-crystal silicon changes backscattering with the angle of incidence.</p>
<div class="pbox pbox--ex"><span class="pbox__t">Problems</span><ol>
<li>From $F(\varphi)$ in {{sec:ch06-loop}}, show that the median turn has $1-\cos\varphi=2a/(1+2a)$, about $2\sqrt a$ radians for small $a$, and evaluate it for silicon at 800 eV and 30 keV.</li>
<li>Integrate $\mathrm ds=\mathrm dE/|\mathrm dE/\mathrm ds|$ with $|\mathrm dE/\mathrm ds|=c/E$ and a constant logarithm, to show that the path length to stop grows as $E^2$. Compare with the exponent of {{eq:ko6}} and say what makes the difference.</li>
<li>Run the simulation for silicon from 0.5 to 5 kV and plot $\delta+\eta$. At which voltage does it cross one, and what would that mean for an insulating sample?</li>
</ol></div>
<p><b>Sources.</b> D. C. Joy, "An introduction to Monte Carlo simulations", <em>Scanning Microscopy</em> 5 (1991) 329–337, <a href="https://digitalcommons.usu.edu/microscopy/vol5/iss2/4">open copy</a>, read in full: Eqs. 1–4, 6, 7, 11 and 12 and the remarks on validity. Y. Lin, D. C. Joy, "A new examination of secondary electron yield data", <em>Surf. Interface Anal.</em> 37 (2005) 895–900, doi 10.1002/sia.2107, read: Eqs. 1 to 3 and 12, Eq. 13, Table 1. D. C. Joy, S. Luo, R. Gauvin, P. Hovington, N. Evans, "Experimental measurements of electron stopping power at low energies", <em>Scanning Microscopy</em> 10 (1996), <a href="https://digitalcommons.usu.edu/microscopy/vol10/iss3/4">open copy</a>, read: Table 2 and the discussion of $k$. Backscattering data: F. Akbari et al., <em>Medical Physics</em> (2023), doi 10.1002/mp.16604, <a href="https://doi.org/10.5281/zenodo.7810951">data set</a>. Stopping powers: <a href="https://physics.nist.gov/PhysRefData/Star/Text/ESTAR.html">NIST ESTAR</a>. Lin and Joy: <a href="https://psec.uchicago.edu/Papers/A_new_examination_of_secondary_electron_yield_data.pdf">open copy</a>. Kanaya–Okayama: as quoted by J. I. Goldstein et al., <em>Scanning Electron Microscopy and X-Ray Microanalysis</em>, Springer 2017 (abstract only); the 1972 paper was not opened.</p>
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

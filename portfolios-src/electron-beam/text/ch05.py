"""The Electron Beam, from Tip to Measurement · text/ch05.py · chapter 5, The spot.

Written by the finisher (9 November 2026). Format: eb_lib.py (the dict CH). Numbers: outputs of physics/ch05.js (checked through ref/ch05.py),
chapter 2 and 4 modules, expressions of them, and the cross-check values derive/ch05.py writes to data/ch05/derive_results.json. The figure
of probe size against current is computed here with ref/ch05.py from the same formulas the page's module uses.
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
from ref import ch05 as R5, core as RC  # noqa: E402

DER = json.load(open(os.path.join(EB, 'data', 'ch05', 'derive_results.json'), encoding='utf-8'))
C = RC.C
EVJ = C['e']
NUMS = {}


def mod(name, inputs, out, module='ch05', scale=1, sig=3):
    NUMS[name] = {'module': module, 'inputs': inputs, 'out': out, 'scale': scale, 'sig': sig}


def ex(name, expr, of=None, scale=1, sig=3):
    NUMS[name] = {'expr': expr, 'of': dict(of or {}), 'scale': scale, 'sig': sig}


def const(name, value, sig=3):
    ex(name, repr(float(value)), {}, 1, sig)


# ---- the default spot: chapter 4's lens, chapter 2's cold source, 800 V, 10 pA, 5 mrad
for o in ('d_p', 'd_I', 'd_A', 'd_S', 'd_C', 'd_p_opt'):
    mod('f_' + o, {}, o, scale=1e9, sig=3)
mod('f_aopt', {}, 'alpha_opt', scale=1e3, sig=3)
for o in ('d_p', 'd_p_opt', 'd_A', 'd_S', 'd_C'):
    mod('r_' + o, {'probe_convention': 'rss'}, o, scale=1e9, sig=3)
mod('r_aopt', {'probe_convention': 'rss'}, 'alpha_opt', scale=1e3, sig=3)
ex('rss_over_fw50', 'a/b', {'a': 'r_d_p_opt', 'b': 'f_d_p_opt'}, sig=2)
# ---- currents: 1 pA and 1 nA at the optimum, fw50
for tag, I in (('1p', 1e-12), ('1n', 1e-9)):
    mod('dopt_' + tag, {'I_p': I}, 'd_p_opt', scale=1e9, sig=2)
    mod('aopt_' + tag, {'I_p': I}, 'alpha_opt', scale=1e3, sig=2)
# ---- an immersion-class lens: C_s = 0.2 mm, C_c = 0.1 mm (the calculated values of Tsuno et al., quoted in data/ch05)
IMM = {'C_s': 2e-4, 'C_c': 1e-4}
mod('imm_dopt', IMM, 'd_p_opt', scale=1e9, sig=2)
mod('imm_aopt', IMM, 'alpha_opt', scale=1e3, sig=2)
# ---- 30 kV with the same lens
mod('k30_dopt', {'V_land': 30000.0}, 'd_p_opt', scale=1e9, sig=2)
mod('k30_aopt', {'V_land': 30000.0}, 'alpha_opt', scale=1e3, sig=2)
# ---- chapter 4's lens and chapter 2's source, for the record
mod('c4_Cs', {}, 'C_s', module='ch04', scale=1e3, sig=3)
mod('c4_Cc', {}, 'C_c', module='ch04', scale=1e3, sig=3)
mod('c2_dE', {}, 'dE', module='ch02', scale=1 / EVJ, sig=3)
mod('c2_Br', {}, 'B_r', module='ch02', sig=3)
mod('c2_dE50', {}, 'dE50', module='ch02', scale=1 / EVJ, sig=3)
mod('c2_dv', {}, 'd_v', module='ch02', scale=1e9, sig=3)
mod('c4_M', {}, 'M', module='ch04', sig=2)
mod('vs800', {'V_acc': 800.0, 'V_land': 800.0}, 'V_star', module='ch03', sig=6)
mod('lam800', {'V_acc': 800.0, 'V_land': 800.0}, 'lambda_e', module='ch03', scale=1e12, sig=3)
ex('Mtot', 'a/b', {'a': 'f_d_I', 'b': 'c2_dv'}, sig=2)                  # total magnification source -> wafer that 10 pA at 5 mrad needs
ex('I_Monly', '(pi**2/4)*(b/log(2))*v*(5e-3)**2*(m*d)**2*1e15', {'b': 'c2_Br', 'v': 'vs800', 'm': 'c4_M', 'd': 'c2_dv'}, sig=2)   # fA
ex('d_Monly', 'm*d*1e9', {'m': 'c4_M', 'd': 'c2_dv'}, sig=2)
# ---- the Schottky preset of chapter 2 (figure and Problem 3)
SCH_IN = {'r_t': 5e-7, 'V_ex': 2000.0, 'k_f': 8.0, 'T': 1800.0, 'phi': 2.9 * EVJ, 't_clean': 0.0}
mod('sch_Br', SCH_IN, 'B_r', module='ch02', sig=3)
mod('sch_dE50', SCH_IN, 'dE50', module='ch02', scale=1 / EVJ, sig=3)
mod('sch_dE', SCH_IN, 'dE', module='ch02', scale=1 / EVJ, sig=3)
# ---- the parts at the optimum (computed with ref/ch05.py, the same formulas as the module), and where the source image takes over
_p = RC.with_defaults(R5.INPUTS)
_t = R5.terms(_p, R5.optimum(_p))
for k in ('dA', 'dS', 'dC', 'dI'):
    const('o_' + k, _t[k] * 1e9, sig=3)
for tag, I in (('1n', 1e-9),):
    _q = dict(_p, I_p=I)
    _tt = R5.terms(_q, R5.optimum(_q))
    const('n_dC', _tt['dC'] * 1e9, sig=3)
    const('n_dI', _tt['dI'] * 1e9, sig=3)


def _gap(I):
    q = dict(_p, I_p=I)
    t = R5.terms(q, R5.optimum(q))
    return t['dI'] - max(t['dA'], t['dS'], t['dC'])


_lo, _hi = 1e-10, 1e-7
for _ in range(60):
    _m = math.sqrt(_lo * _hi)
    _lo, _hi = (_m, _hi) if _gap(_m) < 0 else (_lo, _m)
const('I_cross_nA', _lo * 1e9, sig=2)
ex('ratio_1n_1p', 'b/a', {'a': 'dopt_1p', 'b': 'dopt_1n'}, sig=2)
# ---- derive cross-checks
for k, sg in (('aopt_sph_cf_mrad', 4), ('aopt_chr_cf_mrad', 4), ('fw50_eV', 3), ('fwhm_eV', 3), ('fw50_over_fwhm', 3), ('joy_nm', 3), ('I_AI_coef', 3),
              ('P1_alpha_coef', 3), ('P1_d_coef', 3), ('dA_coef_eq19', 3), ('airy_fw50_coef', 3), ('airy_frac_066', 2), ('sph_fw50_coef', 3), ('joy_aopt_mrad', 3), ('joy_dopt_nm', 3)):
    const('dv_' + k, DER['numbers'][k], sig=sg)
ex('dv_airy_pct', '100*f', {'f': 'dv_airy_frac_066'}, sig=2)

LITERALS = {
    'Example 5.1': 'the number of a worked example', 'Example 5.2': 'the number of a worked example', 'Example 5.3': 'the number of a worked example',
    '1996': 'year of Barth and Kruit', '2008': 'year of Bronsgeest et al.', '2006': 'year of Joy', '1936': 'year of Scherzer', '1995': 'year of Tsuno et al.',
    '101, 101': 'volume and page of Barth and Kruit', '26, 949': 'volume and page of Bronsgeest et al.', '4, 369': 'volume and page of Joy',
    '0.54': 'FW50 diffraction coefficient (Bronsgeest et al. Eq. 19 in units of lambda/alpha)', '0.66\\times10^{-9}': 'Eq. 19 of Bronsgeest et al. as printed',
    '1.226': 'lambda sqrt(V) in nm, the standard constant', '20 nA': 'where Bronsgeest et al. stop their example, quoted', '10 nA': 'the end of the slider and figure range',
    '0.1 pA': 'a current of the figure, a given', '0.4 nm': 'Hitachi resolution claim, quoted', '0.17 to 5 mm': 'range of the published values, quoted',
    'the 2 mm': 'CEOS value, quoted', '5 mm is': 'Joy value, quoted', 'ten published': 'count of lens rows in the data file', '0.1 and 100 mrad': 'the search interval', 'P10': 'check label',
    '\\tfrac38': 'defocus of the FW50 minimum, a fraction', '\\tfrac34': 'defocus of least confusion, a fraction', 'at 4 to 5 mrad': 'Joy\'s stated angle, quoted',
    '10.1116/1.2907780': 'the DOI of Bronsgeest et al.', '10.1380/ejssnt.2006.369': 'the DOI of Joy 2006', 'Eq. 19': 'equation number in Bronsgeest et al.', 'at 100 V': 'the voltage of the parity case', '4, 369 (2006)': 'volume, page and year', '26, 949 (2008)': 'volume, page and year', '101, 101 (1996)': 'volume, page and year',
    '101, 593 (1936)': 'volume, page and year', 'Eqs. 1 to 4': 'equation numbers of Joy', '25–75': 'edge levels', 'SU9600': 'product name', '1.76': 'quoted from Bronsgeest et al., section II', '0.18': 'FW50 spherical coefficient, quoted', '0.6': 'FW50 chromatic coefficient, quoted',
    '1.3': 'exponent of the root-power sum, quoted', '1.22': 'Airy diameter coefficient', '0.61': 'Airy radius coefficient, as Joy prints it',
    '10 pA': 'the asked current of the default, a given', '5 mrad': 'the half-angle of the default, a given', '800 V': 'the landing voltage, a given',
    '0.2 mm': 'C_s of an immersion lens, quoted (Tsuno et al.)', '0.1 mm': 'C_c of an immersion lens, quoted (Tsuno et al.)', '30 kV': 'a given of Example 5.3',
    '1 pA': 'a given current', '1 nA': 'a given current', '5 mm': 'C_s = C_c of Joy\'s example, quoted', '1 keV': 'energy of Joy\'s example, quoted',
    '0.7 eV': 'energy spread of Joy\'s example, quoted', '18 nm': 'Joy\'s result, quoted', '0.17 to 5 mm': 'range of the published values, quoted',
    '1.08': 'Bronsgeest\'s I_AI coefficient, quoted', '10 −18': 'exponent of that coefficient', '10⁻¹⁸': 'exponent of that coefficient', 'ln 2': 'an exact number',
    'holds 84 %': 'fraction of the light in the Airy central disc, 83.8 %, a standard result of diffraction theory', '26, 949, 2008': 'volume, page and year of Bronsgeest et al.',
    'Eqs. 18 to 21': 'equation numbers in Bronsgeest et al.', '1.76 times the 25–75': 'quoted from Bronsgeest et al., section II', '4, 369, 2006': 'volume, page and year of Joy',
    'a 4 mm working': 'Joy\'s working distance, quoted', 'a 3 mm working': 'the working distance of chapter 4, a given',
    'Eqs. 6 and 19': 'equation numbers in Bronsgeest et al.', 'by 100 at': 'a given of a problem', '10^{-15}': 'stated parity agreement', '10^{-12}': 'stated parity agreement',
    'P1': 'check label', 'P8': 'check label', '4001': 'planes scanned in check P3', '20001': 'rays in check P3',
}


def checks_table():
    rows = ''.join('<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (c['id'], html.escape(c['title']), 'pass' if c['ok'] else 'FAIL', html.escape(c['detail']))
                   for c in DER['checks'])
    return '<div class="ptab-wrap"><table class="ptab ptab--checks"><thead><tr><th>check</th><th>what is verified</th><th>result</th><th>detail</th></tr></thead><tbody>%s</tbody></table></div>' % rows


def fig_curve():
    """Smallest FW50 probe against probe current, for the cold and the Schottky source of chapter 2, with chapter 4's lens at 800 V."""
    base = RC.with_defaults(R5.INPUTS)
    # chapter 2's two presets through its reference module (B_r axial, dE FWHM)
    import importlib.util
    sp_ = importlib.util.spec_from_file_location('r2', os.path.join(EB, 'ref', 'ch02.py'))
    r2 = importlib.util.module_from_spec(sp_)
    sp_.loader.exec_module(r2)
    cold = r2.compute(RC.with_defaults(r2.INPUTS, {'t_clean': 0.0}))
    sch = r2.compute(RC.with_defaults(r2.INPUTS, {'r_t': 5e-7, 'V_ex': 2000.0, 'k_f': 8.0, 'T': 1800.0, 'phi': 2.9 * EVJ, 't_clean': 0.0}))
    series = []
    for name, src, col in (('cold field emitter', cold, '#7a1f2b'), ('Schottky preset', sch, '#7a4b12')):
        pts = []
        for i in range(41):
            I = 1e-13 * 10 ** (5 * i / 40)
            q = dict(base, B_r=src['B_r'], dE=src['dE'], dE50=src['dE50'], I_p=I)
            a = R5.optimum(q)
            pts.append((I, R5.terms(q, a)['dp']))
        series.append((name, col, pts))
    W, H, L, Rr, T, B = 640, 330, 70, 620, 20, 280
    X = lambda I: L + (math.log10(I) + 13) / 5 * (Rr - L)
    ylo, yhi = -9.0, -7.3
    Y = lambda d: B - (math.log10(d) - ylo) / (yhi - ylo) * (B - T)
    out = ['<svg viewBox="0 0 %d %d" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Smallest probe diameter against probe current for two sources">' % (W, H),
           '<rect width="%d" height="%d" fill="#fff"/><rect x="%d" y="%d" width="%d" height="%d" fill="none" stroke="#d9d0c2"/>' % (W, H, L, T, Rr - L, B - T)]
    st = 'font-family:IBM Plex Mono,monospace;font-size:11px;fill:#5a504b'
    for k, lab in zip(range(-13, -7), ('0.1 pA', '1 pA', '10 pA', '100 pA', '1 nA', '10 nA')):
        x = X(10 ** k)
        out.append('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="#e6dfd2"/><text x="%.1f" y="%d" text-anchor="middle" style="%s">%s</text>' % (x, T, x, B, x, B + 16, st, lab))
    for d, lab in ((1e-9, '1 nm'), (2e-9, '2 nm'), (5e-9, '5 nm'), (1e-8, '10 nm'), (2e-8, '20 nm'), (4e-8, '40 nm')):
        y = Y(d)
        out.append('<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="#e6dfd2"/><text x="%d" y="%.1f" text-anchor="end" style="%s">%s</text>' % (L, y, Rr, y, L - 6, y + 4, st, lab))
    out.append('<text x="%d" y="%d" text-anchor="middle" style="%s">probe current I_p</text>' % ((L + Rr) // 2, H - 8, st))
    for j, (name, col, pts) in enumerate(series):
        out.append('<polyline fill="none" stroke="%s" stroke-width="2.2" points="%s"/>' % (col, ' '.join('%.1f,%.1f' % (X(I), Y(d)) for I, d in pts)))
        out.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="2.2"/><text x="%d" y="%d" style="%s">%s</text>' % (L + 12, T + 16 + 16 * j, L + 36, T + 16 + 16 * j, col, L + 42, T + 20 + 16 * j, st, name))
    out.append('</svg>')
    return ''.join(out)


S = []
S.append({'id': 'blurs', 'title': 'Four blurs on one spot', 'html': r"""
<p>Sunlight focused by a magnifying glass makes a bright dot, but never a point: the dot has a size because the sun is not a point, because the glass is not perfect, and because light is a wave. The probe of an electron column is the same kind of dot, and it is blurred in the same four ways. Each has a picture.</p>
<p>The <em>source image</em>: the lenses form an image of the virtual source of chapter 2, and that image has a size $d_I$. <em>Diffraction</em>: the electron is a wave of wavelength $\lambda=h/\sqrt{2meV^*}$ (chapter 3; $V^*$ is the relativistically corrected beam voltage, {{num:lam800}} pm at 800 V). A wave that converges in a cone of half-angle $\alpha$ carries sideways momentum only up to about $p\alpha$, and by the uncertainty relation it cannot be squeezed into a region much narrower than $h/(p\alpha)=\lambda/\alpha$. <em>Spherical aberration</em>: rays at large angles are focused too strongly ({{sec:ch04-aberrations}}) and miss the paraxial image by $C_s\alpha^3$. <em>Chromatic aberration</em>: an electron whose energy differs by $\Delta E$ sees a lens of slightly different strength, its focus moves along the axis by $C_c\,\Delta E/(eV^*)$, and a ray at angle $\alpha$ that crosses the axis that far from the image plane misses it sideways by $C_c\alpha\,\Delta E/(eV^*)$.</p>
<p>The angle $\alpha$, set by an aperture, decides the balance. A small angle makes the aberrations negligible and the diffraction large; a large angle the reverse. The angle also decides the current. Brightness, the current per area per solid angle, divided by $V^*$, is the quantity that Liouville's theorem conserves down the column (chapter 3); with the practical brightness $B_\mathrm{pr}=B_r/\ln2$ of chapter 3 ($B_r$ is the reduced brightness of chapter 2) the probe current is</p>
$$ I_p=B_\mathrm{pr}\,V^*\,\frac{\pi d_I^2}{4}\,\pi\alpha^2,\qquad d_I=\sqrt{\frac{4I_p}{\pi^2B_\mathrm{pr}V^*\alpha^2}} . \label{dI5} $$
<p>For a given current, a wider cone needs a smaller source image. The source image is the virtual source times the total magnification of the column, which the condenser lenses set. For chapter 2's cold tip the virtual source is only {{num:c2_dv}} nm across, and 10 pA at 5 mrad needs $d_I=$ {{num:f_d_I}} nm: a total magnification of {{num:Mtot}}, so here the condensers must <em>enlarge</em> the source before the objective's demagnification of {{num:c4_M}} (chapter 4). With the objective alone the source image would be {{num:d_Monly}} nm and the current {{num:I_Monly}} fA. A cold field emitter's tiny source is spent on current. So the asked current is a knob of the problem, the source-image size follows from it, and the spot size is what we pay.</p>
"""})

S.append({'id': 'adding', 'title': 'How the blurs add', 'html': r"""
<p>The four blurs are not independent shapes that could be laid side by side. The probe is the source image convolved with the blur of a point (diffraction and aberrations together), and a convolution does not add widths in any simple way. Two conventions are in use, and the simulation offers both.</p>
<p><b>The classic quadrature sum.</b> Each term is given a diameter and the squares are added, as for independent Gaussian errors:</p>
$$ d_p^2 = \left(1.22\frac\lambda\alpha\right)^2 + \left(\tfrac12C_s\alpha^3\right)^2 + \left(C_c\frac{\Delta E}{eV^*}\alpha\right)^2 + d_I^2 . \label{rss5} $$
<p>The diffraction diameter is the Airy disc out to its first dark ring. The spherical term is the <em>disc of least confusion</em>: the narrowest cross-section of the cone of aberrated rays. At the paraxial image the outermost rays miss by $C_s\alpha^3$, so the blur there is $2C_s\alpha^3$ across; a little before it, at $\Delta z=-\tfrac34C_s\alpha^2$, the bundle is narrowest, $\tfrac12C_s\alpha^3$ across (check P3 finds both numbers by brute force). The chromatic term is the spread of focus across the energy width $\Delta E$, here the FWHM of chapter 2. The convention is simple and widely taught, and its weakness is known: the terms are not Gaussian, and their diameters are not defined alike (an Airy disc to its first zero holds 84 % of the current; a disc of least confusion holds all of it).</p>
<p><b>The FW50 root-power sum.</b> Barth and Kruit (<em>Optik</em> 101, 101, 1996) define every term as the diameter that holds half the current (FW50) and combine them by a rule fitted to full wave-optical calculations of probes. In the form of Bronsgeest, Barth, Swanson and Kruit (<em>J. Vac. Sci. Technol. B</em> 26, 949, 2008, Eqs. 18 to 21; <a href="https://repository.tudelft.nl/file/File_4245540e-e7ce-4173-9608-932300f0db0b">open copy</a>):</p>
$$ d_p = \sqrt{\Big(\big(d_A^4+d_S^4\big)^{1.3/4}+d_I^{1.3}\Big)^{2/1.3}+d_C^2}, \label{rps5} $$
$$ d_A=0.54\,\frac\lambda\alpha,\qquad d_S=0.18\,C_s\alpha^3,\qquad d_C=0.6\,C_c\,\frac{\Delta E_{50}}{eV^*}\,\alpha . \label{rpsc5} $$
<p>Each term is the FW50 the probe would have if that blur acted alone. We checked two coefficients from first principles: the Airy disc holds half its current inside {{num:dv_airy_fw50_coef}} $\lambda/\alpha$ (check P7; the paper prints its Eq. 19 as $0.66\times10^{-9}/(\alpha\sqrt{V})$ in metres and volts, which is the same thing, because $\lambda\sqrt V=1.226$ nm·V<sup>½</sup>), and a spherically aberrated bundle that fills the aperture evenly has its smallest FW50, {{num:dv_sph_fw50_coef}} $C_s\alpha^3$, at $\Delta z=-\tfrac38C_s\alpha^2$ (check P8). The chromatic coefficient 0.6 we take from the paper. The powers have no derivation: in the paper's words, "the powers are simply those that give a good approximation to complete simulations". What they do is easy to see. Whenever one term is much larger than the others, $d_p$ tends to it. Diffraction and spherical aberration are added with the power 4, so the larger of the two dominates sharply: both are parts of one wave aberration of the same point image. The source image joins with the power 1.3, a softer sum than quadrature. The chromatic term is added in quadrature.</p>
<p>The $\Delta E_{50}$ in $d_C$ is the FW50 of the energy distribution, the narrowest energy interval holding half the electrons; for chapter 2's cold source it is {{num:dv_fw50_eV}} eV against a FWHM of {{num:dv_fwhm_eV}} eV (check P9), and the module takes it from chapter 2. The FW50 is also what a knife-edge measurement relates to most directly: for the three probe shapes Bronsgeest et al. compare (Gaussian, Lorentzian, top hat) the FW50 is 1.76 times the 25–75 % edge width.</p>
<div class="pbox"><span class="pbox__t">Key result · probe size</span><p>For an asked current $I_p$, the probe diameter is a function of the beam angle alone: diffraction falls as $1/\alpha$, the source image as $1/\alpha$, chromatic aberration rises as $\alpha$ and spherical aberration as $\alpha^3$. There is one angle at which $d_p$ is smallest, and the column is run near it.</p></div>
"""})

S.append({'id': 'optimum', 'title': 'The best angle', 'html': r"""
<p>For two terms the best angle can be found by hand. Take diffraction $A/\alpha$ and spherical aberration $B\alpha^3$ in quadrature. The derivative of $A^2\alpha^{-2}+B^2\alpha^6$ is $-2A^2\alpha^{-3}+6B^2\alpha^5$; it vanishes at $\alpha^8=A^2/(3B^2)$ (check P1). With the classic $A=1.22\lambda$ and $B=\tfrac12C_s$ this is $\alpha_\mathrm{opt}=$ {{num:dv_P1_alpha_coef}} $(\lambda/C_s)^{1/4}$ and $d_\mathrm{min}=$ {{num:dv_P1_d_coef}} $\lambda^{3/4}C_s^{1/4}$: the optimum angle grows only as the fourth root of $\lambda/C_s$, which is why a lens twice as bad costs so little in angle. With diffraction and chromatic aberration $K\alpha$, $K=C_c\Delta E/(eV^*)$, the derivative of $A^2\alpha^{-2}+K^2\alpha^2$ vanishes at $\alpha=\sqrt{A/K}$, where the diameter is $\sqrt{2AK}$ (check P2): the spot scales as the square root of the chromatic coefficient times the relative energy spread.</p>
<p>With all four terms the solver searches for the minimum numerically (golden-section search on $\ln\alpha$ between 0.1 and 100 mrad). With the chromatic term and the current switched off it reproduces the closed form of P1 to seven digits, {{num:dv_aopt_sph_cf_mrad}} mrad for the default lens, and with the spherical term switched off that of P2, {{num:dv_aopt_chr_cf_mrad}} mrad (checks P4 and P5). The default case is close to the second: at 800 V the optimum is a balance of diffraction against chromatic aberration.</p>
<div class="pbox pbox--ex"><span class="pbox__t">Example 5.1 · the default spot</span>
<p>Chapter 4's objective ($C_s=$ {{num:c4_Cs}} mm, $C_c=$ {{num:c4_Cc}} mm), chapter 2's cold source ($B_r=$ {{num:c2_Br}} A m<sup>−2</sup> sr<sup>−1</sup> V<sup>−1</sup>, $\Delta E_{50}=$ {{num:c2_dE50}} eV, FWHM {{num:c2_dE}} eV), landing at 800 V, asking for 10 pA at 5 mrad. In the FW50 convention the parts are $d_A=$ {{num:f_d_A}} nm, $d_S=$ {{num:f_d_S}} nm, $d_C=$ {{num:f_d_C}} nm and $d_I=$ {{num:f_d_I}} nm, and the probe is $d_p=$ {{num:f_d_p}} nm. Diffraction dominates at this angle. Opening the beam to the optimum, {{num:f_aopt}} mrad, gives {{num:f_d_p_opt}} nm, with diffraction {{num:o_dA}} nm and chromatic blur {{num:o_dC}} nm nearly equal and spherical aberration ({{num:o_dS}} nm) and source image ({{num:o_dI}} nm) minor. The classic quadrature sum gives {{num:r_d_p}} nm at 5 mrad and {{num:r_d_p_opt}} nm at its optimum of {{num:r_aopt}} mrad, {{num:rss_over_fw50}} times the FW50 value: the two conventions measure different things, and a specification must say which it means.</p></div>
<div class="pbox pbox--ex"><span class="pbox__t">Example 5.2 · current against size, and a better lens</span>
<p>At 1 pA the smallest FW50 probe is {{num:dopt_1p}} nm (at {{num:aopt_1p}} mrad); at 1 nA it is {{num:dopt_1n}} nm (at {{num:aopt_1n}} mrad). A thousand times the current costs only a factor {{num:ratio_1n_1p}} in size, because the optimum angle opens and the extra current is collected over a wider cone. At 1 nA the chromatic blur ({{num:n_dC}} nm) is still larger than the source image ({{num:n_dI}} nm); the source image becomes the largest part only above about {{num:I_cross_nA}} nA. An immersion-type objective with $C_s=$ 0.2 mm and $C_c=$ 0.1 mm (calculated values of Tsuno et al., 1995, quoted in this project's data) gives {{num:imm_dopt}} nm at 10 pA, at {{num:imm_aopt}} mrad: at this current the source image is a minor part, so a better lens is what shrinks the spot.</p></div>
<div class="pbox pbox--ex"><span class="pbox__t">Example 5.3 · the same column at 30 kV</span>
<p>Landing at 30 kV with the same lens geometry (excited for the higher voltage, chapter 4) gives {{num:k30_dopt}} nm at {{num:k30_aopt}} mrad for 10 pA. The shorter wavelength and the smaller relative energy spread both help. The price is the deeper and harder hit in the wafer, which chapter 6 measures.</p></div>
{{figure:curve}}
"""})

S.append({'id': 'data', 'title': 'Our lens and spot next to published values', 'html': r"""
<p>Published aberration coefficients of real objectives (collected with their provenance in <code>data/ch05/objective_lens_cs_cc.csv</code>) run from 0.17 to 5 mm in $C_s$. Our bell-field objective, {{num:c4_Cs}} and {{num:c4_Cc}} mm at a 3 mm working distance, is larger than all but one of the ten published lens values there: about twice the 2 mm that the corrector maker CEOS gives for an uncorrected CD-SEM column, and below only Joy's "typical" 5 mm (<em>J. Surf. Sci. Nanotechnol.</em> 4, 369, 2006, for a low-voltage objective at a 4 mm working distance). Magnetic immersion lenses reach a few tenths of a millimetre. The bell field is a teaching model, and its working distance is long by these standards. These are values read from abstracts, excerpts and a manufacturer's table, not measurements we could check. For the spot itself we found no published probe diameter we could compare like for like: manufacturers quote image resolution, a different quantity (Hitachi, for instance, states 0.4 nm at 30 kV for its SU9600 cold-field-emission SEM, <a href="https://hte.hitachi-hightech.com/blog/cold-field-emission-vs-schottky">manufacturer's page</a>), which is the same order as our {{num:k30_dopt}} nm at 30 kV with a lens of several times larger $C_s$.</p>
<p>Joy also gives a worked spot size: $C_s=C_c=$ 5 mm, 1 keV, a Schottky spread of 0.7 eV, his three terms in quadrature, "about 18 nm" at 4 to 5 mrad. His diffraction term is $0.61\lambda/\alpha$, which is the radius of the Airy disc to its first zero, used beside a diameter for the spherical term; we reproduce his formulas as printed. At 5 mrad they give {{num:dv_joy_nm}} nm, which reproduces his number (check P10). Their smallest value, however, is {{num:dv_joy_dopt_nm}} nm at {{num:dv_joy_aopt_mrad}} mrad; the excerpt we read does not say why 4 to 5 mrad was taken. Bronsgeest et al. also give the current at which source image and diffraction disc are equally large, $I_p=$ 1.08×10<sup>−18</sup> $B$; their Eqs. 6 and 19 reproduce it (check P6).</p>
<p>Scherzer's theorem ({{sec:ch04-aberrations}}) is what makes all of this unavoidable: with a round, static lens $C_s$ and $C_c$ cannot be made zero, so the spot always has an optimum and the optimum is always a compromise. Aberration correctors with multipoles break the theorem's assumptions and shift the optimum to larger angles and more current; they are outside this project.</p>
"""})

S.append({'id': 'checks', 'title': 'Checks, hand-over and limits', 'html': r"""
<p>The symbolic and numerical checks of this chapter, run by <code>derive/ch05.py</code>:</p>
""" + checks_table() + r"""
<p>The browser module <code>physics/ch05.js</code> and <code>ref/ch05.py</code> agree to $10^{-15}$ in the closed formulas and to about $10^{-12}$ in the optimum angle at the test cases, where the minimum is flat (parity check; at 100 V the two searches part at the ninth digit).</p>
<p><b>What chapters 7 and 8 receive.</b> The probe diameter $d_p$ (FW50) and the probe current $I_p$, with the angle that produced them.</p>
<p><b>What the model leaves out.</b> A wave-optical calculation of the probe (the root-power sum is a fit to such calculations). The aberrations of the gun and condensers, which the objective demagnifies but does not remove, and which at large current limit how much of the emission can be used at all; Bronsgeest et al. stop their example at 20 nA for that reason. Coma and astigmatism from misalignment. Fifth-order spherical aberration, which matters at angles of tens of milliradians. The overlap of objective and retarding field of a decelerating column (chapter 4). Coulomb interactions between the electrons in the beam, which blur it at large current (the trajectory-displacement effect); the sliders and the figure run to 10 nA without them. Stage vibration, stray fields and the finite scan step. Each adds to the probe of a real column.</p>
<div class="pbox pbox--ex"><span class="pbox__t">Problems</span><ol>
<li>Show that with diffraction and spherical aberration alone the smallest quadrature diameter is $(4/3)^{1/2}3^{1/8}A^{3/4}B^{1/4}$, and evaluate it for the default lens at 800 V.</li>
<li>Using {{eq:dI5}}, find by what factor the source-image size $d_I$ grows when the asked current is multiplied by 100 at a fixed angle, and by what factor the angle must grow to keep $d_I$ unchanged.</li>
<li>Chapter 2's Schottky preset has $B_r=$ {{num:sch_Br}} A m<sup>−2</sup> sr<sup>−1</sup> V<sup>−1</sup> and $\Delta E_{50}=$ {{num:sch_dE50}} eV (FWHM {{num:sch_dE}} eV), against {{num:c2_Br}} and {{num:c2_dE50}} eV for the cold source. In the figure, which of the two differences makes the Schottky spot larger at 0.1 pA, and which at 10 nA? Check your answer with the simulation.</li>
</ol></div>
<p><b>Sources.</b> M. S. Bronsgeest, J. E. Barth, L. W. Swanson, P. Kruit, <em>J. Vac. Sci. Technol. B</em> 26, 949 (2008), doi 10.1116/1.2907780, read in full in the <a href="https://repository.tudelft.nl/file/File_4245540e-e7ce-4173-9608-932300f0db0b">TU Delft copy</a>. J. E. Barth, P. Kruit, <em>Optik</em> 101, 101 (1996), abstract only. D. C. Joy, <em>J. Surf. Sci. Nanotechnol.</em> 4, 369 (2006), doi 10.1380/ejssnt.2006.369, excerpt of its Eqs. 1 to 4. O. Scherzer, <em>Z. Physik</em> 101, 593 (1936), through chapter 4.</p>
"""})

CH = {
    'title': 'The spot',
    'lead': 'The probe on the wafer is the source image, blurred by diffraction and by the spherical and chromatic aberration of the objective. This chapter adds the four blurs in the classic way and in the FW50 way of Barth and Kruit, finds the beam angle that makes the probe smallest for an asked current, derives the optimum in closed form where it exists, and checks the result against a published worked example.',
    'sections': S,
    'figures': {'curve': {'svg': fig_curve(), 'caption': 'The smallest FW50 probe against the probe current, at the best angle for each current, for chapter 2\'s cold field emitter and Schottky preset, each with its own brightness and FW50 energy width (listed in Problem 3), with chapter 4\'s objective at 800 V. Computed with the same formulas as the simulation (<code>ref/ch05.py</code>).'}},
    'numbers': NUMS,
    'literals': LITERALS,
    'sim': {'module': 'ch05', 'title': 'Probe size against beam angle'},
}

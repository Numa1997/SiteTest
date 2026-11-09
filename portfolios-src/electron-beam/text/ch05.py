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
# ---- derive cross-checks
for k, sg in (('aopt_sph_cf_mrad', 4), ('aopt_chr_cf_mrad', 4), ('fw50_eV', 3), ('fwhm_eV', 3), ('fw50_over_fwhm', 3), ('joy_nm', 3), ('I_AI_coef', 3)):
    const('dv_' + k, DER['numbers'][k], sig=sg)

LITERALS = {
    'Example 5.1': 'the number of a worked example', 'Example 5.2': 'the number of a worked example', 'Example 5.3': 'the number of a worked example',
    '1996': 'year of Barth and Kruit', '2008': 'year of Bronsgeest et al.', '2006': 'year of Joy', '1936': 'year of Scherzer', '1995': 'year of Tsuno et al.',
    '101, 101': 'volume and page of Barth and Kruit', '26, 949': 'volume and page of Bronsgeest et al.', '4, 369': 'volume and page of Joy',
    '0.66': 'FW50 diffraction coefficient, quoted from Bronsgeest et al.', '0.18': 'FW50 spherical coefficient, quoted', '0.6': 'FW50 chromatic coefficient, quoted',
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
            q = dict(base, B_r=src['B_r'], dE=src['dE'], I_p=I)
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
S.append({'id': 'blurs', 'title': 'Four blurs on one spot', 'html': r'''
<p>Sunlight focused by a magnifying glass makes a bright dot, but never a point: the dot has a size because the sun is not a point, because the glass is not perfect, and because light is a wave. The probe of an electron column is the same kind of dot, and it is blurred in the same four ways. The <em>source image</em>: the lenses form a reduced image of the virtual source of chapter 2, and that image has a size $d_I$. <em>Diffraction</em>: a beam that converges with half-angle $\alpha$ cannot be focused tighter than about $\lambda/\alpha$. <em>Spherical aberration</em>: rays at large angles are focused too strongly ({{sec:ch04-aberrations}}) and miss by $C_s\alpha^3$. <em>Chromatic aberration</em>: electrons of slightly different energy focus at different places and miss by $C_c\alpha\,\Delta E/(eV^*)$.</p>
<p>The angle $\alpha$, set by an aperture, decides the balance. A small angle makes the aberrations negligible and the diffraction large; a large angle the reverse. And the angle also decides the current, because by chapter 3 the probe current is</p>
$$ I_p=B_\mathrm{pr}\,V^*\,\frac{\pi d_I^2}{4}\,\pi\alpha^2,\qquad d_I=\sqrt{\frac{4I_p}{\pi^2B_\mathrm{pr}V^*\alpha^2}} , \label{dI5} $$
<p>with $B_\mathrm{pr}=B_r/\ln2$ the practical brightness. For a given current, a wider cone needs a smaller source image, which the condenser lenses provide by demagnifying the source more. So the asked current is a knob of the problem, the source-image size follows from it, and the spot size is what we pay.</p>
'''})

S.append({'id': 'adding', 'title': 'How the blurs add', 'html': r'''
<p>The four blurs are not independent shapes that could be laid side by side. The probe is the source image convolved with the blur of a point (diffraction and aberrations together), and a convolution does not add widths in any simple way. Two conventions are in use, and the simulation offers both.</p>
<p><b>The classic quadrature sum.</b> Each term is given a diameter and the squares are added, as for independent Gaussian errors:</p>
$$ d_p^2 = \left(1.22\frac\lambda\alpha\right)^2 + \left(\tfrac12C_s\alpha^3\right)^2 + \left(C_c\frac{\Delta E}{eV^*}\alpha\right)^2 + d_I^2 . \label{rss5} $$
<p>The diffraction diameter is the Airy disc out to its first dark ring. The spherical term is the <em>disc of least confusion</em>: the narrowest cross-section of the cone of aberrated rays, which lies a little before the paraxial image and is half as wide as the miss $C_s\alpha^3$ there (check P3 finds this factor ½ by brute force). The chromatic term is the spread of focus across the energy width. The convention is simple and widely taught, and its weakness is known: the terms are not Gaussian, and their diameters are not defined consistently (an Airy disc to its first zero holds 84 % of the current; a disc of least confusion holds all of it).</p>
<p><b>The FW50 root-power sum.</b> Barth and Kruit (<em>Optik</em> 101, 101, 1996) define every term as the diameter that holds half the current (FW50) and fitted, to full wave-optical calculations, the rule</p>
$$ d_p = \sqrt{\Big(\big(d_A^4+d_S^4\big)^{1.3/4}+d_I^{1.3}\Big)^{2/1.3}+d_C^2},\quad d_A=0.66\frac\lambda\alpha,\ d_S=0.18\,C_s\alpha^3,\ d_C=0.6\,C_c\frac{\Delta E}{eV^*}\alpha \label{rps5} $$
<p>with the coefficients as Bronsgeest et al. (<em>J. Vac. Sci. Technol. B</em> 26, 949, 2008, Eqs. 18 to 21) give them. We read that paper in full; Barth and Kruit we know only from its abstract and from Bronsgeest's use of it. The FW50 is also what a knife-edge measurement relates to most directly (Bronsgeest et al. show that FW50 = 1.76 times the 25–75 % edge width for any of the probe shapes they tried). One more convention to state: their $\Delta E$ is the FW50 of the energy distribution; we feed the FWHM of chapter 2, which for the cold source is wider by a factor {{num:dv_fw50_over_fwhm}}⁻¹ (FW50 {{num:dv_fw50_eV}} eV, FWHM {{num:dv_fwhm_eV}} eV, check P7), so our chromatic term is on the safe side by that much.</p>
<div class="pbox"><span class="pbox__t">Key result · probe size</span><p>For an asked current $I_p$, the probe diameter is a function of the beam angle alone: diffraction falls as $1/\alpha$, the source image as $1/\alpha$, chromatic aberration rises as $\alpha$ and spherical aberration as $\alpha^3$. There is one angle at which $d_p$ is smallest, and the column is run near it.</p></div>
'''})

S.append({'id': 'optimum', 'title': 'The best angle', 'html': r'''
<p>For two terms the best angle can be found by hand. With only diffraction $A/\alpha$ and spherical aberration $B\alpha^3$ in quadrature, setting the derivative of $A^2/\alpha^2+B^2\alpha^6$ to zero gives $\alpha^8=A^2/(3B^2)$ (check P1): the optimum angle grows only as the fourth root of $\lambda/C_s$, which is why a lens twice as bad costs so little in angle. With only diffraction and chromatic aberration, $K\alpha$ with $K=C_c\Delta E/(eV^*)$, the optimum is $\alpha=\sqrt{A/K}$ and the smallest diameter $\sqrt{2AK}$ (check P2): at low voltage, where $\Delta E/(eV^*)$ is large, the spot scales as the square root of the chromatic coefficient times the energy spread.</p>
<p>With all four terms the solver searches for the minimum numerically (golden-section search on $\ln\alpha$). With the chromatic term and the current switched off it reproduces the closed form of P1 to seven digits, {{num:dv_aopt_sph_cf_mrad}} mrad for the default lens, and with the spherical term switched off that of P2, {{num:dv_aopt_chr_cf_mrad}} mrad (checks P4 and P5).</p>
<div class="pbox pbox--ex"><span class="pbox__t">Example 5.1 · the default spot</span>
<p>Chapter 4's objective ($C_s=$ {{num:c4_Cs}} mm, $C_c=$ {{num:c4_Cc}} mm), chapter 2's cold source ($B_r=$ {{num:c2_Br}} A m<sup>−2</sup> sr<sup>−1</sup> V<sup>−1</sup>, $\Delta E=$ {{num:c2_dE}} eV), landing at 800 V, asking for 10 pA at 5 mrad. In the FW50 convention the parts are $d_A=$ {{num:f_d_A}} nm, $d_S=$ {{num:f_d_S}} nm, $d_C=$ {{num:f_d_C}} nm and $d_I=$ {{num:f_d_I}} nm, and the probe is $d_p=$ {{num:f_d_p}} nm. Diffraction dominates at this angle; opening the beam to the optimum {{num:f_aopt}} mrad gives {{num:f_d_p_opt}} nm. The classic quadrature sum gives {{num:r_d_p}} nm at 5 mrad and {{num:r_d_p_opt}} nm at its optimum of {{num:r_aopt}} mrad, {{num:rss_over_fw50}} times the FW50 value: the two conventions measure different things, and a specification must say which it means.</p></div>
<div class="pbox pbox--ex"><span class="pbox__t">Example 5.2 · current against size, and a better lens</span>
<p>At 1 pA the smallest FW50 probe is {{num:dopt_1p}} nm (at {{num:aopt_1p}} mrad); at 1 nA it is {{num:dopt_1n}} nm (at {{num:aopt_1n}} mrad). A thousand times the current costs a factor of a few in size, and at large current the source image takes over. An immersion-type objective with $C_s=$ 0.2 mm and $C_c=$ 0.1 mm (calculated values of Tsuno et al., 1995, quoted in this project's data) gives {{num:imm_dopt}} nm at 10 pA, at {{num:imm_aopt}} mrad: at low voltage the lens, not the source, sets the spot.</p></div>
<div class="pbox pbox--ex"><span class="pbox__t">Example 5.3 · the same column at 30 kV</span>
<p>Landing at 30 kV with the same lens geometry (excited for the higher voltage, chapter 4) gives {{num:k30_dopt}} nm at {{num:k30_aopt}} mrad for 10 pA. The shorter wavelength and the smaller relative energy spread both help. The price is the deeper and harder hit in the wafer, which chapter 6 measures.</p></div>
{{figure:curve}}
'''})

S.append({'id': 'data', 'title': 'Our lens and spot next to published values', 'html': r'''
<p>Published aberration coefficients of real objectives (collected with their provenance in <code>data/ch05/objective_lens_cs_cc.csv</code>) run from 0.17 to 5 mm in $C_s$ and are mostly of the order of the working distance: Joy (<em>J. Surf. Sci. Nanotechnol.</em> 4, 369, 2006) takes 5 mm for both as typical of a low-voltage objective at a 4 mm working distance; magnetic immersion lenses reach a few tenths of a millimetre. Our bell-field objective, {{num:c4_Cs}} and {{num:c4_Cc}} mm at a 3 mm working distance, sits inside that range, at the conventional end. These are values read from abstracts, excerpts and a manufacturer's table, not measurements we could check.</p>
<p>Joy also gives a worked spot size: $C_s=C_c=$ 5 mm, 1 keV, a Schottky spread of 0.7 eV, his three terms (with $0.61\lambda/\alpha$ for diffraction) in quadrature, "about 18 nm" at an optimum of 4 to 5 mrad. Recomputed from his formulas it is {{num:dv_joy_nm}} nm at 5 mrad (check P8), which reproduces his number; at his own optimum, the smaller angle where diffraction and chromatic blur are equal, the sum is smaller, so his 18 nm is a choice of a larger angle for more current. One disagreement we found inside Bronsgeest et al. we record rather than resolve: they quote that source image and diffraction disc are equally large at $I_p=$ 1.08×10<sup>−18</sup> $B$, while their own Eqs. 6 and 19 give a value larger by a factor close to $1/\ln2$ (check P6), as if the quoted number counted only the current inside the FW50 disc. We use Eq. 6 as printed.</p>
<p>Scherzer's theorem ({{sec:ch04-aberrations}}) is what makes all of this unavoidable: with a round, static lens $C_s$ and $C_c$ cannot be made zero, so the spot always has an optimum and the optimum is always a compromise. Aberration correctors with multipoles break the theorem's assumptions and shift the optimum to larger angles and more current; they are outside this project.</p>
'''})

S.append({'id': 'checks', 'title': 'Checks, hand-over and limits', 'html': r'''
<p>The symbolic and numerical checks of this chapter, run by <code>derive/ch05.py</code>:</p>
''' + checks_table() + r'''
<p>The browser module <code>physics/ch05.js</code> and <code>ref/ch05.py</code> agree to $10^{-15}$ in the closed formulas and to about $10^{-12}$ in the optimum angle, where the minimum is flat (parity check).</p>
<p><b>What chapters 7 and 8 receive.</b> The probe diameter $d_p$ (FW50) and the probe current $I_p$, with the angle that produced them.</p>
<p><b>What the model leaves out.</b> A wave-optical calculation of the probe (the root-power sum is a fit to one); the aberrations of the condenser and gun, which the objective demagnifies but does not remove; coma and astigmatism from misalignment; Coulomb interactions in the beam, which blur it at large current (the trajectory-displacement effect); stage vibration, stray fields and the finite size of the scan step. Each adds to the probe of a real column.</p>
<div class="pbox pbox--ex"><span class="pbox__t">Problems</span><ol>
<li>Show that with diffraction and spherical aberration alone the smallest quadrature diameter is $(4/3)^{1/2}3^{1/8}A^{3/4}B^{1/4}$, and evaluate it for the default lens at 800 V.</li>
<li>Using {{eq:dI5}}, find how the source-image size at the optimum angle changes when the asked current is multiplied by 100 at a fixed angle.</li>
<li>Explain why, at the same current, the cold source gives a smaller spot than the Schottky source in the figure even though the chromatic term enters both with similar weight.</li>
</ol></div>
'''})

CH = {
    'title': 'The spot',
    'lead': 'The probe on the wafer is the source image, blurred by diffraction and by the spherical and chromatic aberration of the objective. This chapter adds the four blurs in the classic way and in the FW50 way of Barth and Kruit, finds the beam angle that makes the probe smallest for an asked current, derives the optimum in closed form where it exists, and checks the result against a published worked example.',
    'sections': S,
    'figures': {'curve': {'svg': fig_curve(), 'caption': 'The smallest FW50 probe against the probe current, at the best angle for each current, for chapter 2\'s cold field emitter and Schottky preset, with chapter 4\'s objective at 800 V. Computed with the same formulas as the simulation (<code>ref/ch05.py</code>).'}},
    'numbers': NUMS,
    'literals': LITERALS,
    'sim': {'module': 'ch05', 'title': 'Probe size against beam angle'},
}

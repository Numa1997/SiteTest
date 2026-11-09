"""The Electron Beam, from Tip to Measurement · text/ch03.py · chapter 3, Acceleration, brightness, energy spread.

Written by the finisher (9 November 2026). Format: eb_lib.py (the dict CH). Every number in the prose is a {{num:..}} declared in NUMS:
module outputs of physics/ch03.js and physics/ch02.js (run by the build through the page's JavaScript and by checks/check_numbers.py
through ref/ch03.py and ref/ch02.py), or expressions of them. Quoted source values are named constants with the source in a comment and
listed in LITERALS. The SymPy checks are derive/ch03.py; its table is shown in the last section.
"""
import html
import importlib.util
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
EB = os.path.abspath(os.path.join(HERE, '..'))
if EB not in sys.path:
    sys.path.insert(0, EB)
from ref import core as RC  # noqa: E402

_spec = importlib.util.spec_from_file_location('eb_derive_ch03', os.path.join(EB, 'derive', 'ch03.py'))
DERIVE = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(DERIVE)
C = RC.C
EVJ = C['e']

NUMS = {}


def mod(name, inputs, out, module='ch03', scale=1, sig=3):
    NUMS[name] = {'module': module, 'inputs': inputs, 'out': out, 'scale': scale, 'sig': sig}


def ex(name, expr, of=None, scale=1, sig=3):
    NUMS[name] = {'expr': expr, 'of': dict(of or {}), 'scale': scale, 'sig': sig}


def const(name, value, sig=3):
    ex(name, repr(float(value)), {}, 1, sig)


# ---- constants of nature (CODATA 2018, ref/core.py)
const('mc2_keV', C['m_e'] * C['c'] ** 2 / C['e'] / 1e3, sig=6)
const('hc_', C['h'] * C['c'])
const('e_', C['e'])

# ---- wavelength and the size of the relativistic correction at four voltages
for V in (1000, 30000, 100000, 300000):
    k = '%dk' % (V // 1000)
    mod('lam_' + k, {'V_acc': float(V), 'V_land': float(V)}, 'lambda_e', scale=1e12, sig=4)
    mod('vs_' + k, {'V_acc': float(V), 'V_land': float(V)}, 'V_star', sig=6)
    mod('g_' + k, {'V_acc': float(V), 'V_land': float(V)}, 'gamma', sig=6)
    ex('nrerr_' + k, '100*(sqrt(s/v)-1)', {'s': 'vs_' + k, 'v': 'v_' + k}, sig=2)
    const('v_' + k, V)
ex('vs_ratio_30k', 's/v', {'s': 'vs_30k', 'v': 'v_30k'}, sig=6)
ex('V_1pct_kV', '((1.01**2-1)*2*m)', {'m': 'mc2_keV'}, sig=3)          # sqrt(1 + eV/2mc^2) = 1.01, solved for V, in kV
ex('lam_ur_300k', 'hc/(e*300000)*1e12', {'hc': 'hc_', 'e': 'e_'}, sig=3)  # the ultra-relativistic form hc/eV at 300 kV, pm

# ---- deceleration: the column at 5 kV, landing at 800 V (a given of the example), and the default 1 kV -> 800 V
DEC = {'V_acc': 5000.0, 'V_land': 800.0}
mod('dec_mag', DEC, 'ang_mag', sig=3)
mod('dec_lam_col', DEC, 'lambda_e', scale=1e12, sig=3)
mod('dec_lam_land', DEC, 'lambda_land', scale=1e12, sig=3)
mod('def_mag', {}, 'ang_mag', sig=4)

# ---- the source of chapter 2: cold preset (contract defaults, clean tip) and Schottky preset
COLD = {'t_clean': 0.0}
SCH = {'r_t': 5e-7, 'V_ex': 2000.0, 'k_f': 8.0, 'T': 1800.0, 'phi': 2.9 * EVJ, 't_clean': 0.0}
mod('cold_Bd', COLD, 'B_r', module='ch02')
mod('cold_dE', COLD, 'dE', module='ch02', scale=1 / EVJ, sig=3)
mod('cold_dv', COLD, 'd_v', module='ch02', scale=1e9, sig=2)
mod('cold_Ie', COLD, 'I_e', module='ch02', scale=1e9, sig=2)
mod('sch_Bd', SCH, 'B_r', module='ch02')
mod('sch_dE', SCH, 'dE', module='ch02', scale=1 / EVJ, sig=2)
ex('ln2inv', '1/log(2)', {}, sig=5)
const('lam_const', C['h'] / math.sqrt(2 * C['m_e'] * C['e']) * 1e12, sig=5)
ex('cold_Bp', 'b/log(2)', {'b': 'cold_Bd'})
ex('sch_Bp', 'b/log(2)', {'b': 'sch_Bd'})
ex('cold_over_sch', 'a/b', {'a': 'cold_Bp', 'b': 'sch_Bp'}, sig=2)

# ---- probe current from the practical brightness (Bronsgeest et al. 2008, Eq. 6), example: landing at 800 V, d_I = 1 nm, alpha = 5 mrad
mod('vs_land_def', {}, 'V_star_land', sig=5)
const('d_I_nm', 1.0)
const('alpha_mrad', 5.0)
ex('Ip_pA', 'B*V*(pi*(d*1e-9)**2/4)*(pi*(a*1e-3)**2)*1e12', {'B': 'cold_Bp', 'V': 'vs_land_def', 'd': 'd_I_nm', 'a': 'alpha_mrad'}, sig=2)
ex('Ip_sch_pA', 'B*V*(pi*(d*1e-9)**2/4)*(pi*(a*1e-3)**2)*1e12', {'B': 'sch_Bp', 'V': 'vs_land_def', 'd': 'd_I_nm', 'a': 'alpha_mrad'}, sig=2)
ex('electrons_per_us', 'I*1e-12*1e-6/e', {'I': 'Ip_pA', 'e': 'e_'}, sig=2)

# ---- energy spread, relative to the beam energy
ex('rel_spread_1k', 'd/(e*1000)*1e4', {'d': 'cold_dE', 'e': 'e_'}, sig=2)          # dE is stored in joules; in units of 1e-4
ex('rel_spread_land', 'd/(e*800)*1e4', {'d': 'cold_dE', 'e': 'e_'}, sig=2)

# ---- published values: Williams & Carter, Transmission Electron Microscopy, ch. 5, Table 5.1 (brightness at 100 kV, typical values)
const('wc_B_cold', 1e13)
const('wc_B_sch', 5e12)
const('wc_dE_cold', 0.3)
const('wc_dE_sch', 0.7)
ex('wc_Br_cold', 'b/v', {'b': 'wc_B_cold', 'v': 'vs_100k'})
ex('wc_Br_sch', 'b/v', {'b': 'wc_B_sch', 'v': 'vs_100k'})
ex('ratio_cold', 'a/b', {'a': 'cold_Bp', 'b': 'wc_Br_cold'}, sig=2)
ex('ratio_sch', 'a/b', {'a': 'sch_Bp', 'b': 'wc_Br_sch'}, sig=2)
ex('nrc_pct_100k', '100*(s/v-1)', {'s': 'vs_100k', 'v': 'v_100k'}, sig=2)
const('coulomb_limit', 3e8)          # Bronsgeest et al. 2008, section III, citing van Veen et al. 2001: Schottky interactions matter above this
ex('sch_vs_limit', 'b/l', {'b': 'sch_Bp', 'l': 'coulomb_limit'}, sig=2)

STYLE = 'font-family:IBM Plex Mono,monospace;font-size:11px;fill:#5a504b'
SVG_GUN = ('<svg viewBox="0 0 640 250" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Potential energy of an electron along the column">'
           '<rect x="0" y="0" width="640" height="250" fill="#fff"/>'
           '<line x1="60" y1="30" x2="60" y2="220" stroke="#3a322e"/><line x1="60" y1="220" x2="610" y2="220" stroke="#3a322e"/>'
           '<text x="16" y="40" style="%s">U(z)</text><text x="590" y="240" style="%s">z</text>'
           '<path d="M70 50 L120 50 C140 50 150 70 170 110 C200 170 230 200 280 205 L420 205 C470 205 500 180 530 160 L600 160" fill="none" stroke="#7a1f2b" stroke-width="2.2"/>'
           '<line x1="70" y1="50" x2="600" y2="50" stroke="#8b8079" stroke-dasharray="4 4"/>'
           '<text x="72" y="44" style="%s">tip: U = 0 (Fermi level)</text>'
           '<text x="300" y="198" style="%s">column: U = −eV_acc</text>'
           '<text x="500" y="150" style="%s">wafer: U = −eV_land</text>'
           '<line x1="290" y1="54" x2="290" y2="202" stroke="#1c1518" marker-end="url(#a3)" marker-start="url(#a3)"/>'
           '<text x="296" y="130" style="%s">kinetic energy eV_acc</text>'
           '<line x1="560" y1="54" x2="560" y2="157" stroke="#1c1518" marker-end="url(#a3)" marker-start="url(#a3)"/>'
           '<text x="470" y="100" style="%s">eV_land</text>'
           '<rect x="150" y="30" width="8" height="190" fill="#d9d0c2"/><rect x="230" y="30" width="8" height="190" fill="#d9d0c2"/><rect x="520" y="30" width="8" height="190" fill="#d9d0c2"/>'
           '<text x="130" y="240" style="%s">extractor</text><text x="216" y="240" style="%s">anode</text><text x="500" y="240" style="%s">retarding plate</text>'
           '<defs><marker id="a3" viewBox="0 0 8 8" refX="4" refY="4" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L8 4 L0 8 z" fill="#1c1518"/></marker></defs>'
           '</svg>') % ((STYLE,) * 10)

SVG_PHASE = ('<svg viewBox="0 0 640 230" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="The same beam in phase space at two planes">'
             '<rect x="0" y="0" width="640" height="230" fill="#fff"/>'
             '<line x1="40" y1="115" x2="290" y2="115" stroke="#d9d0c2"/><line x1="165" y1="20" x2="165" y2="210" stroke="#d9d0c2"/>'
             '<line x1="350" y1="115" x2="610" y2="115" stroke="#d9d0c2"/><line x1="480" y1="20" x2="480" y2="210" stroke="#d9d0c2"/>'
             '<ellipse cx="165" cy="115" rx="90" ry="22" fill="#e2a2aa" fill-opacity=".55" stroke="#7a1f2b"/>'
             '<ellipse cx="480" cy="115" rx="22" ry="90" transform="rotate(-25 480 115)" fill="#e2a2aa" fill-opacity=".55" stroke="#7a1f2b"/>'
             '<text x="272" y="108" style="%s">x</text><text x="172" y="30" style="%s">p_x</text>'
             '<text x="592" y="108" style="%s">x</text><text x="487" y="30" style="%s">p_x</text>'
             '<text x="60" y="205" style="%s">plane 1: wide, nearly parallel</text><text x="370" y="205" style="%s">plane 2: a focus, same area</text>'
             '</svg>') % ((STYLE,) * 6)

LITERALS = {
    'Example 3.1': 'the number of a worked example', 'Example 3.2': 'the number of a worked example', 'Example 3.3': 'the number of a worked example',
    'Eq. 6': 'equation number in Bronsgeest et al. 2008', 'Eqs. 15 and 16': 'equation numbers in Bronsgeest et al. 2008',
    'Table 5.1': 'table number in Williams and Carter', '100 kV': 'the voltage at which Williams and Carter state their brightness values',
    '5 kV': 'a given of Example 3.2', '800 V': 'the landing voltage of the examples, a given', '1 kV': 'the column voltage of the default, a given',
    '1 nm': 'a given of Example 3.3', '5 mrad': 'a given of Example 3.3', '2008': 'year of a cited paper', 'D1': 'check label', 'D9': 'check label',
    '2001': 'year of a cited paper', '1/ln 2': 'an exact number', 'ch. 5': 'chapter number in Williams and Carter',
    '1 MV': 'the end of the plotted range', '300 kV': 'the voltage of the last case of Example 3.1, a given',
    '4 V/nm': 'the apex field of chapter 2\'s working point, a given there', '1.44\\,ej': 'the factor as Bronsgeest et al. print it, quoted',
    '15 kV': 'a given of a problem', '500 V': 'a given of a problem', '1 mrad': 'a given of a problem',
    '(32(mc²)²)': 'SymPy output shown in the checks table', '-x**2/32': 'SymPy output shown in the checks table', '= 1.4427 ×': 'the title of check D7, 1/ln 2',
    '= 1.44270': 'SymPy output shown in the checks table', 'πα⁴/12': 'series shown in the checks table', '64-bit': 'the width of a double',
    '10 −14': 'the stated parity tolerance, an exponent', '10 V': 'the start of the plotted range', '61': 'number of plotted voltages',
}


def checks_table():
    rows = ''.join('<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (c['id'], html.escape(c['title']), 'pass' if c['ok'] else 'FAIL', html.escape(c['detail']))
                   for c in DERIVE.checks)
    return ('<div class="ptab-wrap"><table class="ptab"><thead><tr><th>check</th><th>what is verified</th><th>result</th><th>detail</th></tr></thead><tbody>%s</tbody></table></div>' % rows)


S = []
S.append({'id': 'gun', 'title': 'The gun: a step in potential', 'html': r'''
<p>A marble let go at the top of a smooth slide arrives at the bottom with a speed that depends only on how far it has dropped, not on the shape of the slide. An electron in a static electric field is that marble. In {{sec:ch01-nr}} we found that in static fields the energy $\gamma mc^2 + q\varphi$ is conserved, with $q=-e$ the electron's charge and $\varphi$ the electric potential. An electron that leaves the tip at rest (on the scale of what follows) and arrives where the potential is higher by $V$ has therefore gained the kinetic energy</p>
$$ E_0 = (\gamma-1)\,mc^2 = eV, \qquad \gamma = 1+\frac{eV}{mc^2}. \label{e03} $$
<p>Nothing else about the path enters. This is why an electron gun can be built from simple parts: the tip of {{sec:ch02-intro}}, an <em>extractor</em> a fraction of a millimetre away whose voltage $V_\mathrm{ex}$ pulls the electrons out by tunnelling, and an <em>anode</em> whose voltage $V_\mathrm{acc}$ sets their final energy. The two knobs do different jobs. $V_\mathrm{ex}$, together with the tip radius, fixes the field at the apex and therefore the current and its energy spread (chapter 2). $V_\mathrm{acc}$ fixes the energy with which the electrons travel down the column, and with it their wavelength, how stiffly they resist the lenses, and how deep they would go into the wafer. {{fig:gun}} shows the potential energy $U=-e\varphi$ of an electron along the axis: a drop of $eV_\mathrm{acc}$ in the gun, a flat floor in the column, and, if the wafer is held at a less positive potential, a step back up to $-eV_\mathrm{land}$ just before the wafer.</p>
{{figure:gun}}
<p>One correction to "at rest". Electrons leave a cold tip with energies within a few tenths of an electronvolt of the Fermi level (chapter 2 found a width of {{num:cold_dE}} eV at the working point). Measured from the Fermi level, every electron then gains exactly $eV$; the spread is carried along unchanged. We come back to this in {{sec:ch03-spread}}.</p>
'''})

S.append({'id': 'momentum', 'title': 'Momentum and wavelength, exactly', 'html': r'''
<p>The wavelength that decides how small a spot can be (chapter 5) is the de Broglie wavelength $\lambda=h/p$, so we need the momentum $p$ that belongs to the kinetic energy $eV$. For a particle of rest energy $mc^2$, total energy $E$ and momentum $p$, special relativity gives $E^2=(pc)^2+(mc^2)^2$. With $E = mc^2+eV$ from {{eq:e03}},</p>
$$ (pc)^2 = (mc^2+eV)^2-(mc^2)^2 = (eV)^2 + 2\,eV\,mc^2 . \notag $$
<p>We divide by $c^2$ and take $2meV$ out as a factor:</p>
$$ p^2 = 2meV\left(1+\frac{eV}{2mc^2}\right) \equiv 2meV^*, \qquad V^* = V\left(1+\frac{eV}{2mc^2}\right). \label{vstar3} $$
<p>The quantity $V^*$ is the <em>relativistically corrected voltage</em>. Its use is that every non-relativistic formula of electron optics in which $V$ stands for $p^2/(2me)$ becomes exact when $V$ is replaced by $V^*$. The wavelength is then</p>
$$ \lambda = \frac{h}{p} = \frac{h}{\sqrt{2meV^*}} . \label{lam3} $$
<div class="pbox"><span class="pbox__t">Key result · the beam voltage</span><p>After a potential step $V$ the electron has $p^2=2meV^*$ with $V^*=V(1+eV/2mc^2)$, and $\lambda=h/\sqrt{2meV^*}$. In every formula below, the beam voltage means $V^*$.</p></div>
<p>Two limits check {{eq:lam3}}. When $eV\ll mc^2=$ {{num:mc2_keV}} keV, the bracket is 1 and $\lambda\to h/\sqrt{2meV}$, the school formula. When $eV\gg mc^2$, the term $(eV)^2$ dominates, $p\to eV/c$ and $\lambda\to hc/(eV)$, the wavelength of a photon of the same energy: the electron's rest mass no longer matters. Both limits are verified symbolically (check D2 in {{sec:ch03-checks}}).</p>
<p>How large is the correction? The non-relativistic formula overestimates the wavelength by the factor $\sqrt{V^*/V}=\sqrt{1+eV/2mc^2}\approx 1+eV/(4mc^2)$ (check D3), which passes one per cent at {{num:V_1pct_kV}} kV.</p>
<div class="pbox pbox--ex"><span class="pbox__t">Example 3.1 · wavelengths along the range of electron microscopes</span>
<p>At 1 kV, $V^*=$ {{num:vs_1k}} V and $\lambda=$ {{num:lam_1k}} pm; the non-relativistic formula is off by {{num:nrerr_1k}} %. At $V=$ {{num:v_30k}} V, $V^*/V=$ {{num:vs_ratio_30k}}, $\gamma=$ {{num:g_30k}} and $\lambda=$ {{num:lam_30k}} pm, an error of {{num:nrerr_30k}} % without relativity. At 100 kV, $\lambda=$ {{num:lam_100k}} pm (error {{num:nrerr_100k}} %), and at $V=$ {{num:v_300k}} V, $\lambda=$ {{num:lam_300k}} pm, where the photon-like limit $hc/eV$ would give {{num:lam_ur_300k}} pm: at 300 kV the electron is half-way between the two limits. A low-voltage scanning microscope, which works at a few hundred volts to a few kilovolts, can use the school formula to a fraction of a per cent; a transmission microscope cannot.</p></div>
'''})

S.append({'id': 'landing', 'title': 'Landing softly: deceleration before the wafer', 'html': r'''
<p>The energy that is best for the column is often not the energy that is best for the wafer. A fast beam is stiff: it is less disturbed by stray fields and by the repulsion between its own electrons, and the lens aberrations that grow with the relative energy spread $\Delta E/E$ (chapter 5) are smaller. A slow beam is gentle: it deposits its energy in the top few nanometres, charges insulators less and damages fragile resist less (chapter 6). A column can have both by running at $V_\mathrm{acc}$ and slowing the electrons in a <em>retarding field</em> between the last lens and the wafer, which is held at a potential $V_\mathrm{acc}-V_\mathrm{land}$ below the column, so that the electrons land with $eV_\mathrm{land}$ ({{fig:gun}}).</p>
<p>What happens to the beam's angles? Near the axis of a round system the retarding field points along the axis. It changes the axial momentum $p_z$ and leaves the transverse momentum $p_\perp$ alone, as a ball thrown sideways while it rolls up a ramp keeps its sideways push. The angle of a ray to the axis is $\tan\alpha = p_\perp/p_z$, and for small angles $p_z\approx p$, so</p>
$$ \frac{\alpha_\mathrm{land}}{\alpha} = \frac{p_\mathrm{acc}}{p_\mathrm{land}} = \sqrt{\frac{V^*_\mathrm{acc}}{V^*_\mathrm{land}}} . \label{angmag3} $$
<p>(check D4). A beam slowed down opens up. This is not a loss: as {{sec:ch03-brightness}} shows, the brightness per volt is unchanged, so a spot that is smaller in angle at the column energy is simply larger in angle at the wafer, and the current is the same.</p>
<div class="pbox pbox--ex"><span class="pbox__t">Example 3.2 · a column at 5 kV landing at 800 V</span>
<p>The angle grows by {{eq:angmag3}}: $\alpha_\mathrm{land}/\alpha=$ {{num:dec_mag}}. The wavelength grows from {{num:dec_lam_col}} pm in the column to {{num:dec_lam_land}} pm at the wafer, which is what sets the diffraction limit there. The simulation's default (1 kV landing at 800 V) gives a factor {{num:def_mag}}.</p></div>
<p>The model is the paraxial one: a uniform retarding field along the axis, no fringe fields at its edges, and no lens action of the retarding field itself. In a real column the retarding field and the objective lens overlap and form one immersion lens; chapter 4 treats lenses, and the overlap is outside this project.</p>
'''})

S.append({'id': 'brightness', 'title': 'Brightness, and why the column cannot raise it', 'star': True, 'html': r'''
<p>A lens can make a spot smaller only by making its angles larger, as a magnifying glass that concentrates sunlight into a small dot does so by bringing the light in from a wide cone. The quantity that no lens can change is the current per area per solid angle, the <em>brightness</em>,</p>
$$ B = \frac{\mathrm dI}{\mathrm dA\,\mathrm d\Omega}, \label{bright3} $$
<p>in A m<sup>−2</sup> sr<sup>−1</sup>. The reason is Liouville's theorem. Take the distance $z$ along the axis as the "time" and follow the electrons that cross a plane $z$ at transverse position $x$ with transverse momentum $p_x$. In a static field the energy is fixed, and the motion from plane to plane is generated by the Hamiltonian $H(x,p_x;z)=-p_z=-\sqrt{P(x,z)^2-(p_x-qA_x)^2}$, where $P(x,z)$ is the total momentum the potential allows at that point and $A_x$ the vector potential. Hamilton's equations, $\mathrm dx/\mathrm dz=\partial H/\partial p_x$ and $\mathrm dp_x/\mathrm dz=-\partial H/\partial x$, define a flow in the plane $(x,p_x)$ whose divergence is</p>
$$ \frac{\partial}{\partial x}\frac{\partial H}{\partial p_x}-\frac{\partial}{\partial p_x}\frac{\partial H}{\partial x} = 0 , \notag $$
<p>because mixed derivatives commute (check D5, done symbolically for one transverse dimension; the second, $y$, is the same calculation). A flow with no divergence carries a patch of phase space without changing its area, as an incompressible fluid carries a drop of ink: the patch can be stretched into a long thin streak (a focus) but not shrunk ({{fig:phase}}). In two transverse dimensions the conserved quantity is $\mathrm dA\,\mathrm d^2p_\perp$.</p>
{{figure:phase}}
<p>The solid angle of a narrow cone of directions is $\mathrm d\Omega = \mathrm d^2p_\perp/p^2$, since a direction differs from the axis by $p_\perp/p$ in each transverse coordinate. So $\mathrm dA\,\mathrm d\Omega\,p^2$ is conserved, and with it $B/p^2$. With $p^2=2meV^*$ from {{eq:vstar3}} the conserved quantity is the <em>reduced brightness</em></p>
$$ B_r = \frac{B}{V^*} . \label{br3} $$
<div class="pbox"><span class="pbox__t">Key result · reduced brightness is conserved</span><p>Without collisions between the beam's electrons, $B_r=B/V^*$ has the same value at every plane of the column, whatever lenses, apertures (which remove current but do not raise $B_r$) and accelerating or retarding fields lie between (check D6, which only needs D5 and {{eq:vstar3}}). A column can at best keep the brightness its source gives; it can never raise it.</p></div>
<p>This is why chapter 2 spent so long on the tip. Every gain in probe current at a given spot size must come from the source.</p>
'''})

S.append({'id': 'practical', 'title': 'From brightness to probe current', 'html': r'''
<p>Chapter 2 computed the brightness of the emitting patch on the axis, $B_r=e\,j(\varepsilon_t{=}0)/\pi$, which for the exponential distribution of transverse energies there equals $eJ/(\pi\langle\varepsilon_t\rangle)$: the current from an infinitesimal area at the centre of the source into an infinitesimal solid angle. A probe, however, is an image of the <em>whole</em> virtual source, and the virtual source of a field emitter has a Gaussian profile, brightest at the centre. Bronsgeest, Barth, Swanson and Kruit (2008) define the <em>practical brightness</em> as the total angular current density divided by the area of the disk that holds half of the current (the "FW50" diameter $d$), and show that it fixes the probe current (their Eq. 6):</p>
$$ I_p = B_\mathrm{pr}\,V^*\,\frac{\pi d^2}{4}\,\pi\alpha^2 , \label{ip3} $$
<p>with $\alpha$ the half-angle of the beam at the wafer and $d$ the FW50 diameter of the source image there; $\pi\alpha^2$ is the small-angle solid angle of the cone (check D8).</p>
<p>The step from the axial value to the practical one is short. A Gaussian profile $J(r)=J_0e^{-r^2/\sigma^2}$ carries the total current $\pi\sigma^2J_0$; the current inside radius $R$ is $\pi\sigma^2J_0(1-e^{-R^2/\sigma^2})$, which is half the total when $R^2=\sigma^2\ln2$. The total divided by the area $\pi R^2$ of that disk is $J_0/\ln 2$. Hence</p>
$$ B_\mathrm{pr} = \frac{B_r}{\ln 2} = {{numtex:ln2inv}}\,B_r , \label{bpr3} $$
<p>(check D7). Bronsgeest et al. write this as $1.44\,ej/(\pi\langle\varepsilon_t\rangle)$ (their Eqs. 15 and 16) and call the factor "a surprising, new result"; our derivation shows where it comes from. It holds as long as the electrons do not push each other between the tip and the extractor.</p>
<div class="pbox pbox--ex"><span class="pbox__t">Example 3.3 · the probe current of the cold tip</span>
<p>The cold tip of chapter 2 (clean, 4 V/nm) has $B_r=$ {{num:cold_Bd}} A m<sup>−2</sup> sr<sup>−1</sup> V<sup>−1</sup>, so $B_\mathrm{pr}=$ {{num:cold_Bp}}. Land at 800 V ($V^*=$ {{num:vs_land_def}} V), form a source image of $d=$ 1 nm with $\alpha=$ 5 mrad, and {{eq:ip3}} gives $I_p=$ {{num:Ip_pA}} pA, about {{num:electrons_per_us}} electrons per microsecond. The Schottky preset of chapter 2 would give {{num:Ip_sch_pA}} pA in the same spot: its practical brightness is lower by a factor {{num:cold_over_sch}}. Chapter 7 shows that a few thousand electrons per pixel are needed for a clean edge, and this is where the trade-off of chapter 0 bites: half the spot diameter at the same angle means a quarter of the current.</p></div>
'''})

S.append({'id': 'spread', 'title': 'Energy spread through the column', 'html': r'''
<p>Two electrons that leave the tip with energies $E_a$ and $E_b$ each gain $eV$ in a static field, so their difference $E_a-E_b$ is unchanged (check D9). The energy spread $\Delta E$ of the source, {{num:cold_dE}} eV for the cold tip of chapter 2 and {{num:sch_dE}} eV for its Schottky preset, is carried to the wafer as it is. What changes is the <em>relative</em> spread $\Delta E/(eV)$: {{num:rel_spread_1k}}×10<sup>−4</sup> at 1 kV, {{num:rel_spread_land}}×10<sup>−4</sup> at 800 V. Chapter 5 shows that the chromatic blur of the spot is proportional to this ratio, which is why low-voltage columns prize the narrow spread of the cold source.</p>
<p>The statement "unchanged" assumes that the electrons of the beam do not exchange energy with one another. Where the beam is dense, near the source and at crossovers, the random Coulomb pushes between electrons widen the distribution, the Boersch effect, and also blur the spot sideways. Both grow with the current and are the reason why practical brightness stops rising at high emission current. This project does not model them; the numbers here are lower bounds on the spread an operating gun shows.</p>
'''})

S.append({'id': 'data', 'title': 'The model next to published source data', 'html': r'''
<p>How do the brightness and energy spread of chapter 2 compare with what real guns achieve? Williams and Carter (<em>Transmission Electron Microscopy</em>, ch. 5, Table 5.1) list typical values, stated at 100 kV, and the librarian of this project digitised them with their provenance (<code>data/ch02/source_properties_williams_carter.csv</code>). They are round textbook numbers, good to a factor of about two, not measurements with uncertainties. We convert their brightness to reduced brightness with $V^*$ at 100 kV ({{num:vs_100k}} V, a correction of {{num:nrc_pct_100k}} % over dividing by $V$).</p>
<div class="ptab-wrap"><table class="ptab"><thead><tr><th>source</th><th>model $B_\mathrm{pr}$ (A m<sup>−2</sup> sr<sup>−1</sup> V<sup>−1</sup>)</th><th>Williams &amp; Carter $B/V^*$</th><th>model / book</th><th>model $\Delta E$ (eV)</th><th>book $\Delta E$ (eV)</th></tr></thead><tbody>
<tr><td>cold field emission</td><td>{{num:cold_Bp}}</td><td>{{num:wc_Br_cold}}</td><td>{{num:ratio_cold}}</td><td>{{num:cold_dE}}</td><td>{{num:wc_dE_cold}}</td></tr>
<tr><td>Schottky</td><td>{{num:sch_Bp}}</td><td>{{num:wc_Br_sch}}</td><td>{{num:ratio_sch}}</td><td>{{num:sch_dE}}</td><td>{{num:wc_dE_sch}}</td></tr>
</tbody></table></div>
<p>The brightness agrees in order of magnitude for both sources, the model being higher for the cold source and lower for the Schottky preset; both gaps lie within the factor of two the table itself carries. The energy spreads of the model are smaller than the book's, by about a third for both. That is the direction we expect: the model is the intrinsic emission of a clean surface, while the book's values belong to operating guns, which add the Boersch broadening of {{sec:ch03-spread}}. For the Schottky preset the model also assumes a work function and an apex field that chapter 2 states as assumptions. Bronsgeest et al. note that for Schottky sources the interactions become important above a practical brightness of about 3×10<sup>8</sup>; our preset sits at {{num:sch_vs_limit}} of that, so the model's neglect of interactions is consistent for it. The cold source at {{num:cold_Bp}} would sit above that mark, so its predicted brightness is an upper limit for an operating gun.</p>
'''})

S.append({'id': 'checks', 'title': 'Checks, hand-over and limits', 'html': r'''
<p>The symbolic checks of this chapter, run by <code>derive/ch03.py</code> with SymPy; each line states what is verified and how:</p>
''' + checks_table() + r'''
<p>The browser module <code>physics/ch03.js</code> and the Python reference <code>ref/ch03.py</code> evaluate the same closed formulas; they agree to the last bits of a 64-bit number (the parity check states a tolerance of 10<sup>−14</sup>). Every number in this chapter's text is produced by one of them, or by chapter 2's module, and checked against the other.</p>
<p><b>What chapter 4 and chapter 5 receive.</b> The column voltage $V^*_\mathrm{acc}$, the landing voltage $V^*_\mathrm{land}$ and the wavelength there, the angle factor {{eq:angmag3}}, and the rule {{eq:ip3}} with $B_\mathrm{pr}=B_r/\ln2$ for the probe current.</p>
<p><b>What the model leaves out.</b> Electron–electron interactions (Boersch broadening, trajectory displacement, space charge); the gun's own lens action and aberrations, which matter at large emission angles; the overlap of the retarding field with the objective lens; any noise or ripple of the high-voltage supply, which adds to $\Delta E$ directly. The next, more complete model would trace electrons through a computed gun field with their mutual forces (a Monte Carlo of Coulomb interactions), which is how the practical brightness of a real gun is predicted.</p>
<div class="pbox pbox--ex"><span class="pbox__t">Problems</span><ol>
<li>Show from {{eq:lam3}} that $\lambda\,[\mathrm{pm}] \approx {{numtex:lam_const}}/\sqrt{V^*[\mathrm V]}$, and use it to check the wavelengths of Example 3.1.</li>
<li>A column at 15 kV lands its beam at 500 V. By what factor does the beam angle grow? If the aperture gives 1 mrad in the column, what is the half-angle at the wafer?</li>
<li>A Gaussian virtual source is cut by an aperture to a top-hat profile of radius $R$. Show that the practical brightness then tends to the axial value times 2 as $R\to 0$, which is the upper limit Bronsgeest et al. quote.</li>
</ol></div>
'''})

CH = {
    'title': 'Acceleration, brightness, energy spread',
    'lead': r'The gun turns a voltage into kinetic energy; relativity turns that energy into a momentum and a wavelength; Liouville\'s theorem says the column can never make the source brighter. This chapter derives the beam voltage $V^*$, the angle change when the beam is slowed before the wafer, the conservation of reduced brightness, and the probe current that a given brightness allows, and puts the source of chapter 2 next to published values.',
    'sections': S,
    'figures': {
        'gun': {'svg': SVG_GUN, 'caption': 'Potential energy $U=-e\\varphi$ of an electron along the axis (sketch, not to scale). The gun gives it $eV_\\mathrm{acc}$; a retarding plate can take part of it back so that it lands with $eV_\\mathrm{land}$.'},
        'phase': {'svg': SVG_PHASE, 'caption': 'The same beam in the transverse phase space $(x, p_x)$ at two planes (sketch). A lens shears and rotates the patch; it cannot shrink its area. This is Liouville\'s theorem, and it is why brightness is conserved.'},
    },
    'numbers': NUMS,
    'literals': LITERALS,
    'sim': {'module': 'ch03', 'title': 'Acceleration and landing'},
}

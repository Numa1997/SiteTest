"""The Electron Beam, from Tip to Measurement · text/ch04.py · chapter 4, The lens.

Written by the finisher (9 November 2026). Format: eb_lib.py (the dict CH). Numbers: module outputs of physics/ch04.js (built through the
page's JavaScript, checked through ref/ch04.py), expressions of them, and the cross-check values that derive/ch04.py writes to
data/ch04/derive_results.json (run it after changing the lens model; the build reads the file and does not rerun the slow quadrature).
"""
import html
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
EB = os.path.abspath(os.path.join(HERE, '..'))
if EB not in sys.path:
    sys.path.insert(0, EB)
from ref import core as RC  # noqa: E402

DER = json.load(open(os.path.join(EB, 'data', 'ch04', 'derive_results.json'), encoding='utf-8'))
C = RC.C
NUMS = {}


def mod(name, inputs, out, module='ch04', scale=1, sig=3):
    NUMS[name] = {'module': module, 'inputs': inputs, 'out': out, 'scale': scale, 'sig': sig}


def ex(name, expr, of=None, scale=1, sig=3):
    NUMS[name] = {'expr': expr, 'of': dict(of or {}), 'scale': scale, 'sig': sig}


def const(name, value, sig=3):
    ex(name, repr(float(value)), {}, 1, sig)


# ---- the default objective (contract defaults: a = 2 mm, object 0.2 m before the lens, wafer 3 mm behind its centre, 800 V)
for o, sc, sg in (('NI', 1, 3), ('B_0', 1e3, 3), ('M', 1, 3), ('f', 1e3, 4), ('C_s', 1e3, 3), ('C_c', 1e3, 3), ('theta_rot', 1, 3), ('omega_G', 1, 4)):
    mod('d_' + o, {}, o, scale=sc, sig=sg)
ex('d_rot_deg', 't*180/pi', {'t': 'd_theta_rot'}, sig=3)
ex('d_k2', 'w**2-1', {'w': 'd_omega_G'}, sig=3)
ex('d_Mx', '1/m', {'m': 'd_M'}, sig=3)
ex('d_fa', 'f/0.002', {'f': 'd_f'}, sig=3)   # f in units of a; expressions see raw SI values
ex('d_50nm', '50*m', {'m': 'd_M'}, sig=2)                      # f in units of a (a = 2 mm)
# ---- the same lens at 30 kV: the excitation scales with sqrt(V*), the optics do not change
mod('k30_NI', {'V_land': 30000.0}, 'NI', sig=3)
mod('k30_Cs', {'V_land': 30000.0}, 'C_s', scale=1e3, sig=3)
mod('k30_rot', {'V_land': 30000.0}, 'theta_rot', sig=3)
ex('NI_ratio', 'b/a', {'a': 'd_NI', 'b': 'k30_NI'}, sig=4)
mod('vs800', {'V_acc': 800.0, 'V_land': 800.0}, 'V_star', module='ch03', sig=6)
mod('vs30k', {'V_acc': 30000.0, 'V_land': 30000.0}, 'V_star', module='ch03', sig=6)
ex('sqrt_vs_ratio', 'sqrt(b/a)', {'a': 'vs800', 'b': 'vs30k'}, sig=4)
# ---- a longer working distance and a sharper lens
mod('wd5_Cs', {'WD': 5e-3}, 'C_s', scale=1e3, sig=3)
mod('wd5_Cc', {'WD': 5e-3}, 'C_c', scale=1e3, sig=3)
mod('wd5_f', {'WD': 5e-3}, 'f', scale=1e3, sig=3)
mod('a1_Cs', {'a_lens': 1e-3, 'WD': 2e-3}, 'C_s', scale=1e3, sig=3)
mod('a1_Cc', {'a_lens': 1e-3, 'WD': 2e-3}, 'C_c', scale=1e3, sig=3)
mod('a1_NI', {'a_lens': 1e-3, 'WD': 2e-3}, 'NI', sig=3)
# ---- cross-checks written by derive/ch04.py
const('Cs_integral', DER['numbers']['Cs_integral'] * 1e3, sig=6)
const('Cc_integral', DER['numbers']['Cc_integral'] * 1e3, sig=6)
const('f_formula', DER['numbers']['f_formula'] * 1e3, sig=7)
mod('d_Cs6', {}, 'C_s', scale=1e3, sig=6)
mod('d_Cc6', {}, 'C_c', scale=1e3, sig=6)
mod('d_f7', {}, 'f', scale=1e3, sig=7)
const('mu0_', C['mu0'])
ex('B0_check', 'mu*n/(pi*0.002)*1e3', {'mu': 'mu0_', 'n': 'd_NI'}, sig=3)
# disc of the spherical aberration at the default lens for a 5 mrad beam (radius C_s alpha^3)
ex('ds5', 'c*(5e-3)**3*1e9', {'c': 'd_C_s'}, sig=2)
ex('dc5', 'c*5e-3*(0.215/800)*1e9', {'c': 'd_C_c'}, sig=2)   # 0.215 eV spread of chapter 2 at 800 V
mod('lam800', {'V_acc': 800.0, 'V_land': 800.0}, 'lambda_e', module='ch03', sig=4)
ex('dd5', '0.61*l/5e-3*1e9', {'l': 'lam800'}, sig=2)               # Airy radius 0.61 lambda/alpha at 5 mrad
ex('wafer_pct', '100/(1+(0.003/0.002)**2)', {}, sig=2)               # field at the wafer, per cent of B_0 (WD = 3 mm, a = 2 mm)
ex('B_wafer', 'b/(1+(0.003/0.002)**2)*1e3', {'b': 'd_B_0'}, sig=2)  # in mT
mod('k30_B0', {'V_land': 30000.0}, 'B_0', sig=2)

STY = 'font-family:IBM Plex Mono,monospace;font-size:17px;fill:#3a322e'
SVG_LENS = ('<svg viewBox="0 0 640 410" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="A magnetic lens in section: coil inside an iron yoke whose bore wall has a gap; field lines leave the gap and cross the axis; an electron path is bent back to the axis; below, the axial field B(z)">'
            '<rect width="640" height="410" fill="#fff"/>'
            # iron yoke, upper and lower section (the yoke is a ring around the axis); the bore wall facing the axis is open at the gap
            '<path d="M190 18 H450 V128 H342 V106 H428 V40 H212 V106 H298 V128 H190 Z" fill="#d9d0c2" stroke="#1c1518" stroke-width="1.5"/>'
            '<path d="M190 302 H450 V192 H342 V214 H428 V280 H212 V214 H298 V192 H190 Z" fill="#d9d0c2" stroke="#1c1518" stroke-width="1.5"/>'
            '<rect x="226" y="50" width="188" height="44" fill="#efe4c8" stroke="#3a322e"/><rect x="226" y="226" width="188" height="44" fill="#efe4c8" stroke="#3a322e"/>'
            '<text x="236" y="78" style="%s">coil: N turns, I</text><text x="236" y="254" style="%s">coil</text>'
            '<text x="458" y="40" style="%s">iron</text><text x="458" y="60" style="%s">yoke</text>'
            '<line x1="466" y1="116" x2="344" y2="120" stroke="#3a322e"/><text x="470" y="122" style="%s">gap</text>'
            # field lines leaking out of the gap onto the axis region
            '<path d="M298 128 C300 152 340 152 342 128" fill="none" stroke="#3a322e" stroke-width="1.2"/>'
            '<path d="M290 128 C284 176 356 176 350 128" fill="none" stroke="#3a322e" stroke-width="1.2"/>'
            '<path d="M298 192 C300 168 340 168 342 192" fill="none" stroke="#3a322e" stroke-width="1.2"/>'
            '<path d="M290 192 C284 144 356 144 350 192" fill="none" stroke="#3a322e" stroke-width="1.2"/>'
            # axis and an electron path from an axial object point, bent back to the axis
            '<line x1="16" y1="160" x2="624" y2="160" stroke="#8b8079" stroke-dasharray="6 4"/><text x="606" y="184" style="%s">z</text>'
            '<path d="M16 160 L296 141 Q320 139.5 344 142.5 L570 160 L624 164.2" fill="none" stroke="#7a1f2b" stroke-width="2.2"/>'
            '<text x="24" y="138" style="%s">electron</text><line x1="570" y1="146" x2="570" y2="174" stroke="#1c1518" stroke-width="2"/><text x="530" y="198" style="%s">image</text>'
            # the axial field below
            '<line x1="16" y1="392" x2="624" y2="392" stroke="#8b8079"/>'
            '<path d="M16 390.3 C200 388 260 340 320 336 C380 340 440 388 624 390.3" fill="none" stroke="#7a1f2b" stroke-width="2"/>'
            '<text x="20" y="346" style="%s">B(z) on the axis</text><text x="404" y="346" style="%s">peak at the gap</text>'
            '</svg>') % ((STY,) * 10)

LITERALS = {
    'about 2 T': 'saturation of iron, a rounded material fact', 'the 2 T': 'saturation of iron, a rounded material fact', '386, 974, 1926': 'volume, page and year of Busch 1926',
    '10.1002/andp.19263862507': 'the DOI of Busch 1926', '1.5a': 'WD/a = 3 mm / 2 mm, the givens', '0.61': 'coefficient of the Airy radius', '5 kV to 800 V': 'chapter 3\'s case, quoted',
    'Example 4.1': 'the number of a worked example', 'Example 4.2': 'the number of a worked example', 'Example 4.3': 'the number of a worked example',
    '30 kV': 'a given of Example 4.3', '800 V': 'the landing voltage of the default, a given', '2 mm': 'a given of the default lens',
    '3 mm': 'a given of the default lens', '0.2 m': 'a given of the default lens', '5 mm': 'a given of Example 4.2', '1 mm': 'a given of Example 4.2',
    '5 mrad': 'a given of Example 4.2', '0.215 eV': 'chapter 2\'s energy spread, quoted', '1941': 'year of Glaser\'s paper',
    '1936': 'year of Scherzer\'s paper', '10 −4': 'the relative voltage step of the C_c derivative', '±10⁻⁴': 'the relative voltage step of the C_c derivative',
    '2000a': 'the start of the parallel ray, in units of a', '1/2000²': 'the expected gap from that start', 'L1': 'check label', 'N5': 'check label',
    '2 and 4 mrad': 'the two image angles of the C_s fit', '1 to 8 mrad': 'the range of the scaling check', '0.02 %': 'the stated tolerance of check N5',
    '6000': 'the number of RK4 steps', '60': 'the number of bisection steps', '(α⁵)': 'order of the next term',
    '117, 285, 1941': 'volume, page and year of Glaser 1941', '50 nm': 'an example source image, a given', '1 and 8 mrad': 'the range of the scaling check',
    '10^{-9}': 'the angle of the tiny ray', '10^{-11}': 'the stated parity agreement', '101, 593': 'volume and page of Scherzer 1936',
    'r⁴B⁗/64': 'a term of the field expansion', 'B‴/16': 'a term of the field expansion', 'r**4': 'SymPy output', '/64': 'SymPy output',
    '10⁻⁷': 'check tolerance', '10⁻⁶': 'check tolerance', '10⁻⁴)': 'relative voltage step', '2e-3': 'image angle', '1.4×10⁻⁷': 'the measured gap of check N1',
}


def checks_table():
    rows = ''.join('<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (c['id'], html.escape(c['title']), 'pass' if c['ok'] else 'FAIL', html.escape(c['detail']))
                   for c in DER['checks'])
    return '<div class="ptab-wrap"><table class="ptab ptab--checks"><thead><tr><th>check</th><th>what is verified</th><th>result</th><th>detail</th></tr></thead><tbody>%s</tbody></table></div>' % rows


S = []
S.append({'id': 'picture', 'title': 'From the helix to a lens', 'html': r'''
<p>The beam that leaves the gun of chapter 3 must now be focused into a spot, and the first hint of how was in chapter 1. In {{sec:ch01-helix}} an electron in a long uniform magnetic field ran on a helix and came back to the axis after one turn, wherever it had started from on the axis and at whatever small angle. A uniform field images a point onto a point. A long solenoid is an awkward lens, because the image lies a whole turn away and the field fills all the space between. Shorten the field to a few millimetres, as a coil wound inside an iron shell with a narrow gap does ({{fig:lens}}), and the electron gets only a short kick on its way through. The kick is towards the axis and grows in proportion to the distance from it. That is exactly what a convex glass lens does to light, and it is why a short coil focuses.</p>
{{figure:lens}}
<p>The puzzle is how a magnetic field can push an electron towards the axis at all. On the axis the field points along the axis, and an electron moving along the axis feels nothing ($\mathbf v\times\mathbf B=0$). Off the axis the field lines are not parallel to the axis near the gap. On the way into the gap they converge towards it, and on the way out they spread again. So the field has a radial part $B_\mathrm{rad}$ (in this chapter $B_\mathrm{rad}$ is this radial field, not the reduced brightness of chapters 2 and 3). An electron moving along $z$ through $B_\mathrm{rad}$ gets a force $-e\,v_zB_\mathrm{rad}$ in the azimuthal direction: it starts to turn about the axis. Once it turns, its azimuthal velocity $v_\theta$ crosses the axial field $B_z$, and $-e\,v_\theta B_z$ points towards the axis. The twist comes first, and the twist turned by the axial field is the focusing push. The next three sections make this exact.</p>
'''})

S.append({'id': 'field', 'title': 'The field near the axis', 'html': r'''
<p>Between the pole pieces there are no currents and the field is static, so $\nabla\cdot\mathbf B=0$ and $\nabla\times\mathbf B=0$. For a round lens nothing depends on the angle $\theta$ about the axis, and the field has a radial part $B_\mathrm{rad}(r,z)$ and an axial part $B_z(r,z)$. In cylindrical coordinates the two equations are</p>
$$ \frac1r\frac{\partial(rB_\mathrm{rad})}{\partial r}+\frac{\partial B_z}{\partial z}=0,\qquad \frac{\partial B_\mathrm{rad}}{\partial z}-\frac{\partial B_z}{\partial r}=0 . \label{maxw4} $$
<p>Near the axis we expand in powers of $r$. By symmetry $B_z$ is even in $r$ and $B_\mathrm{rad}$ is odd: $B_z=B(z)+b_2(z)r^2+\dots$ and $B_\mathrm{rad}=c_1(z)r+c_3(z)r^3+\dots$, where $B(z)$ is the field on the axis, the one function a lens designer measures or computes. The first equation of {{eq:maxw4}} at order $r^0$ gives $2c_1+B'=0$, so $c_1=-B'/2$. The second at order $r^1$ gives $c_1'-2b_2=0$, so $b_2=-B''/4$. One more order of each gives $c_3=B^{\prime\prime\prime}/16$. Hence</p>
$$ B_z = B(z)-\frac{r^2}{4}B''(z)+\dots,\qquad B_\mathrm{rad}=-\frac r2B'(z)+\frac{r^3}{16}B^{\prime\prime\prime}(z)+\dots \label{expand4} $$
<p>(check L2 verifies that these satisfy both equations up to the next order). The whole field near the axis is fixed by $B(z)$ and its derivatives. The radial part is the bending of the field lines. By {{eq:expand4}} it points inwards where $B$ rises along $z$ (the lines converge into the gap) and outwards where $B$ falls.</p>
<p>For $B(z)$ we take Glaser's bell-shaped field (W. Glaser, <em>Z. Physik</em> 117, 285, 1941),</p>
$$ B(z)=\frac{B_0}{1+(z/a)^2}, \label{glaser4} $$
<p>with its peak $B_0$ at the centre of the gap and half-width $a$ at half maximum. It is a fair description of a real pole-piece lens and has the rare virtue that its rays can be found exactly ({{sec:ch04-glaser}}). The peak follows from Ampère's law. Take a loop that runs along the axis from $-\infty$ to $+\infty$ and closes far away, outside the iron, where the field vanishes. The whole loop is in vacuum, where $\mathbf B=\mu_0\mathbf H$, and it links the current of the $N$ turns once, so $\oint\mathbf H\cdot\mathrm d\mathbf l=NI$ gives $\int B\,\mathrm dz=\mu_0NI$ exactly, whatever the iron does. The iron shapes $B(z)$, it does not change its integral. With {{eq:glaser4}} the integral along the axis is $\pi aB_0$ (check L1), so</p>
$$ B_0=\frac{\mu_0NI}{\pi a} . \label{ampere4} $$
<p>What the iron decides is how concentrated the field is: a narrow gap gives a small $a$ and, for the same $NI$, a high peak. That works only while the pole tips are not saturated; iron saturates at about 2 T, and a lens pushed towards that loses the bell shape that {{eq:glaser4}} assumes.</p>
'''})

S.append({'id': 'busch', 'title': 'Busch’s theorem and the paraxial ray equation', 'html': r'''
<p>The twist of {{sec:ch04-picture}} follows from a conservation law. In chapter 1 the Lagrangian $L=-mc^2/\gamma-q\varphi+q\mathbf v\cdot\mathbf A$ gave the canonical momentum $\mathbf p=\gamma m\mathbf v+q\mathbf A$ ({{sec:ch01-lagrange}}). A round lens has no preferred angle, so $L$ does not depend on $\theta$ and the angular component of canonical momentum is conserved:</p>
$$ p_\theta = \gamma m r^2\dot\theta + q\,rA_\theta = \text{const}. \label{ptheta4} $$
<p>Near the axis the vector potential of a field $B(z)$ is azimuthal, and Stokes' theorem on a circle of radius $r$ gives $2\pi rA_\theta=\pi r^2B$, the flux through the circle. So $A_\theta=rB/2$. Electrons that leave a point on the axis, as in a probe column, start with $p_\theta=0$ (they have $r=0$), so with $q=-e$</p>
$$ \dot\theta = \frac{eB(z)}{2\gamma m} \label{larmor4} $$
<p>(check L4). This is Busch's theorem (H. Busch, <em>Annalen der Physik</em> 386, 974, 1926, doi 10.1002/andp.19263862507; we found its record, not its text). The electron turns about the axis at the Larmor rate, half the cyclotron rate, wherever the field is, and stops turning when it leaves the field. The image is therefore rotated, by $\theta_\mathrm{rot}=\int\dot\theta\,\mathrm dt=\frac{e}{2p}\int B\,\mathrm dz$ along the path.</p>
<p>Now the radial motion. The radial component of the magnetic force $q\,\mathbf v\times\mathbf B$ is $q(v_\theta B_z-v_zB_\theta)=q\,r\dot\theta B$ near the axis, since $B_\theta=0$ for a round lens and $B_z\approx B$. The radial equation of motion in cylindrical coordinates, with $\gamma$ constant in a magnetic field, is</p>
$$ \gamma m\left(\ddot r-r\dot\theta^2\right) = q\,r\dot\theta B = -e\,r\dot\theta B . \notag $$
<p>Insert {{eq:larmor4}}: the right side is $-e^2B^2r/(2\gamma m)$, and the centrifugal term $\gamma mr\dot\theta^2$ is $e^2B^2r/(4\gamma m)$. Their sum gives</p>
$$ \ddot r = -\left(\frac{eB}{2\gamma m}\right)^2 r . \notag $$
<p>The force is towards the axis and proportional to $r$: the lens law. Half of the magnetic push is used up keeping the electron on its turning path; the other half focuses. For paraxial rays $\dot z\approx v$, so $\mathrm d/\mathrm dt=v\,\mathrm d/\mathrm dz$, and with $p=\gamma mv$ and $p^2=2meV^*$ from chapter 3,</p>
$$ r''(z) = -\frac{e^2B^2}{4p^2}\,r = -\eta\,B(z)^2\,r,\qquad \eta=\frac{e}{8mV^*} \label{parax4} $$
<p>(check L5). So far the ray started on the axis: it turns about the axis with the Larmor rate and its distance $r$ from the axis obeys {{eq:parax4}}. A ray that starts off the axis with a sideways velocity (a skew ray) has $p_\theta\ne0$, and the argument must be redone. Write the transverse position as one complex number $w=x+\mathrm iy$. With $B_x=-xB'/2$, $B_y=-yB'/2$ from {{eq:expand4}} the transverse force, written as one complex number, is</p>
$$ q\big[(\mathbf v\times\mathbf B)_x+\mathrm i(\mathbf v\times\mathbf B)_y\big]=-\mathrm iq\,\big[B\dot w+\tfrac12vB'w\big], \notag $$
<p>so with $q=-e$ and $\mathrm d/\mathrm dt=v\,\mathrm d/\mathrm dz$</p>
$$ w''=\mathrm i\kappa\,(2Bw'+B'w),\qquad \kappa=\frac{e}{2p} . \notag $$
<p>Now look at the ray from a frame that turns about the axis by the angle $\theta(z)$ with $\theta'=\kappa B$: put $w=u\,\mathrm e^{\mathrm i\theta}$. The terms in $u'$ and $B'$ cancel, and what remains is $u''=-\kappa^2B^2u$, with $\kappa^2=e/(8mV^*)=\eta$ (check L8). Both components of $u$ obey {{eq:parax4}}, for every paraxial ray, skew or not. In the turning frame the lens acts as a plain radial focusing force; the turning itself is the image rotation.</p>
<p>The equation is linear: any sum of two solutions is a solution. Every ray from an object point at transverse position $u_0$ is $u=u_0\,g(z)+\alpha\,h(z)$, where $g$ starts at height 1 with zero slope and $h$ starts on the axis with unit slope. If the lens makes $h$ return to the axis at some plane, every ray from that object point arrives there at the same place $u_0\,g$, whatever its angle $\alpha$. A point is imaged onto a point. That linearity is what makes a sharp image possible at all.</p>
<div class="pbox"><span class="pbox__t">Key result · the round magnetic lens</span><p>In the frame turning at the Larmor rate $eB/(2\gamma m)$, all paraxial rays obey $r''=-\eta B^2r$ with $\eta=e/(8mV^*)$. The lens strength depends on $B^2/V^*$: the same lens focuses a beam of four times the voltage at twice the current. The image is turned by $\theta_\mathrm{rot}=\sqrt{e/(8mV^*)}\int B\,\mathrm dz$.</p></div>
'''})

S.append({'id': 'glaser', 'title': 'Glaser’s exact solution', 'star': True, 'html': r'''
<p>With the bell field {{eq:glaser4}}, {{eq:parax4}} reads $r''+k^2a^2r/(a^2+z^2)^2=0$ with the dimensionless strength $k^2=\eta B_0^2a^2$. Glaser's substitution $z=a\cot\psi$ maps the axis from $z=-\infty$ to $+\infty$ onto $\psi$ from $\pi$ to 0. Together with the new unknown $y=r\sin\psi$ it turns the equation into $\mathrm d^2y/\mathrm d\psi^2+\omega^2y=0$ with $\omega^2=1+k^2$, an oscillator with constant coefficients. Its solutions are sines of $\omega\psi$, and dividing by $\sin\psi$ gives $r$. Its solution for a ray that arrives parallel to the axis at unit height is</p>
$$ r=\frac{\sin\big(\omega(\pi-\psi)\big)}{\omega\sin\psi},\qquad \omega=\sqrt{1+k^2} \label{glasersol4} $$
<p>(check L6 confirms the equation symbolically). Far before the lens, $\psi\to\pi$ and $r\to1$. Far behind it, $\psi\to0$ with $z\approx a/\psi$, and expanding the sine gives $r\approx\sin(\omega\pi)\,z/(\omega a)-\cos(\omega\pi)$: a straight line of slope $\sin(\omega\pi)/(\omega a)$. A ray that came in parallel at unit height leaves with slope $-1/f$, so the focal length is</p>
$$ f=-\frac{\omega a}{\sin(\omega\pi)} . \label{f4} $$
<p>For $1\lt\omega\lt2$ the sine is negative and $f$ is positive: one crossing of the axis, a converging lens. For a weak lens, $k\to0$, $\sin(\omega\pi)\approx-\pi k^2/2$ and $1/f\to\pi k^2/(2a)$, which is the thin-lens formula $1/f=\eta\int B^2\,\mathrm dz$ (check L7): the lens strength is the integral of the square of the field. The square explains why a lens cannot tell north from south, and why designers concentrate the field in a short gap. The same $NI$ spread over half the length gives twice the $\int B^2$.</p>
'''})

S.append({'id': 'objective', 'title': 'The objective lens, focused on the wafer', 'html': r'''
<p>The last lens of a probe column, the objective, takes a small source image (or a crossover) far above it and forms a much smaller image on the wafer. Its operator focuses by turning the lens current. Our solver does the same. It places the object a distance $u$ before the lens centre, the wafer a working distance $W\!D$ behind it, and starts a paraxial ray from the axis at the object. It then adjusts $B_0$ by bisection until the ray crosses the axis exactly at the wafer. The integration runs in the variable $\tau$ with $z=a\tan\tau$, so that the steps crowd into the lens. It is the RK4 method of chapter 1 with a fixed number of steps.</p>
<p>The magnification follows from the angles. Liouville's theorem of chapter 3 at one voltage says that the product of the image size and the beam angle is fixed (the Lagrange invariant). So $M=\alpha_\mathrm{object}/\alpha_\mathrm{image}$, read off the slopes of the same ray at both ends.</p>
<div class="pbox pbox--ex"><span class="pbox__t">Example 4.1 · the default objective</span>
<p>A gap field of half-width $a=$ 2 mm, the object 0.2 m before it, the wafer 3 mm behind its centre, electrons of 800 V. Focusing needs $NI=$ {{num:d_NI}} A, a peak field $B_0=$ {{num:d_B_0}} mT (by {{eq:ampere4}}, $\mu_0NI/(\pi a)=$ {{num:B0_check}} mT). In terms of the dimensionless strength $k^2=\eta B_0^2a^2$ and $\omega=\sqrt{1+k^2}$ of {{sec:ch04-glaser}} this is $k^2=$ {{num:d_k2}}, $\omega=$ {{num:d_omega_G}}. The focal length {{eq:f4}} is $f=$ {{num:d_f}} mm, {{num:d_fa}} times $a$. It describes the straight lines that rays follow far outside the field, the way focal and principal planes describe a thick glass lens. The wafer is not far outside. At 3 mm $=1.5a$ the field is still {{num:wafer_pct}} % of $B_0$, {{num:B_wafer}} mT. The rays are still bending when they arrive, so the thin-lens equation with $f$ and $u$ would not give the wafer's position. That is why the solver focuses the actual ray on the wafer and reads $M$ from its actual slopes. The lens demagnifies by {{num:d_Mx}} ($M=$ {{num:d_M}}), so a source image of 50 nm becomes {{num:d_50nm}} nm. The image is turned by {{num:d_theta_rot}} rad, {{num:d_rot_deg}}°.</p></div>
<div class="pbox pbox--ex"><span class="pbox__t">Example 4.2 · the same lens at 30 kV</span>
<p>At 30 kV the lens must be excited with $NI=$ {{num:k30_NI}} A, a factor {{num:NI_ratio}} more, which is $\sqrt{V^*_{30\,\mathrm{kV}}/V^*_{800\,\mathrm V}}=$ {{num:sqrt_vs_ratio}}. By {{eq:parax4}} the optics depend only on $B^2/V^*$, so a fixed geometry with $B_0\propto\sqrt{V^*}$ has the same focal length, magnification and aberrations ($C_s=$ {{num:k30_Cs}} mm against {{num:d_C_s}} mm). The rotation is unchanged too, {{num:k30_rot}} rad. The scaling holds for a real lens only while its iron is not saturated. This lens needs a peak of {{num:k30_B0}} T at 30 kV, well below the 2 T at which iron saturates. A shorter, stronger lens at high voltage reaches that limit.</p></div>
'''})

S.append({'id': 'aberrations', 'title': 'Why a round lens is never perfect: spherical and chromatic aberration', 'html': r'''
<p>Equation {{eq:parax4}} is exact only for rays infinitely close to the axis. A real ray at angle $\alpha$ departs from it in two ways. It feels the $r^3$ terms of the field {{eq:expand4}}, and its own motion is not paraxial (its speed along the axis is smaller than $v$ by the part that goes sideways and round the axis, which adds terms in $B^4$). Both are third order in the ray's height and slope, and in a magnetic lens they always focus the outer rays more strongly than the inner ones, as a glass ball does. Rays through the rim cross the axis before the paraxial image. At the image plane they miss the axis by</p>
$$ \Delta r_s = C_s\,\alpha^3 , \label{cs4} $$
<p>the spherical aberration, with $\alpha$ the half-angle of the ray at the image and $C_s$ a length. A ray of a slightly different energy, $eV^*(1+\delta)$, sees a lens of strength $\eta/(1+\delta)$ and focuses at a different place. It misses by $\Delta r_c=C_c\,\alpha\,\delta$, the chromatic aberration. (Here $\Delta r$ is the radius in the Gaussian image plane; chapter 5 turns these into disc diameters.)</p>
<p>Scherzer proved in 1936 (<em>Z. Physik</em> 101, 593) that $C_s$ and $C_c$ are always positive for a lens that is static, round, free of charge on the axis and forms a real image. No arrangement of coils and iron of that kind can cancel them; one has to break one of the assumptions, which is what multipole aberration correctors do. This project does not model correctors.</p>
<p><b>How we measure them.</b> We trace rays without the paraxial approximation. The solver follows the exact equation of motion of an electron in a static magnetic field, with $z$ as the variable and the speed constant, through the field {{eq:expand4}} kept to third order in $r$. It launches rays from the axial object point at image angles of 2 and 4 mrad and measures how far each misses the axis at the paraxial image. It removes the tiny linear part left by the discretisation, which a ray of $10^{-9}$ rad at the object, traced on the same grid, gives (that ray's own cubic miss is negligible). Then it solves $\Delta r=C_s\alpha^3+C_5\alpha^5$ for $C_s$. For $C_c$ it runs the paraxial ray at $V^*(1\pm10^{-4})$ and takes the central difference.</p>
<p><b>How we check them.</b> ★ For $C_c$ there is a short proof. Let $h(z)$ be the paraxial ray from the axial object point at $z_o$, scaled to unit slope at the image plane $z_i$, so $h(z_i)=0$, $h'(z_i)=1$. The ray of image angle $\alpha$ is $\alpha h$. An electron of energy $eV^*(1+\delta)$ sees $\eta/(1+\delta)\approx\eta(1-\delta)$, so its ray $\alpha h+\Delta$ obeys, to first order in $\delta$, $\Delta''+\eta B^2\Delta=\delta\,\eta B^2\alpha h$. Take a second paraxial ray $g$ that is independent of $h$. Their Wronskian $W=gh'-hg'$ is constant along $z$ because neither equation has a first-derivative term, and at the image it equals $g(z_i)$. Variation of constants gives the miss at the image,</p>
$$ \Delta(z_i)=\int_{z_o}^{z_i}\frac{h(z)g(z_i)-g(z)h(z_i)}{W}\,\delta\eta B^2\alpha h\,\mathrm dz=\delta\,\alpha\,\eta\int_{z_o}^{z_i}B^2h^2\,\mathrm dz . \notag $$
<p>So $C_c=\eta\int_{z_o}^{z_i}B^2h^2\,\mathrm dz$, and the solver's central difference agrees with this integral to all printed digits: {{num:d_Cc6}} mm against {{num:Cc_integral}} mm (check N2). For $C_s$ the standard aberration integral, over the same range from object to image, is (P. W. Hawkes and E. Kasper, <em>Principles of Electron Optics</em>, vol. 1, Academic Press 1989; we took the formula as it is quoted in the lens-design literature and did not open the book, so our check of it is the agreement below)</p>
$$ C_s=\frac{e}{128mV^*}\int\left[\frac{3e}{mV^*}B^4h^4+8B'^2h^4-8B^2h^2h'^2\right]\mathrm dz . \label{csint4} $$
<p>Evaluated on a fine grid it gives {{num:Cs_integral}} mm; the traced value is {{num:d_Cs6}} mm (check N3). The two methods have nothing in common but the field, and they agree to about one part in ten million, so each checks the other. The traced miss grows as $\alpha^3$ to 0.02 % between 1 and 8 mrad (check N5). The traced focal length equals Glaser's {{eq:f4}}, {{num:d_f7}} against {{num:f_formula}} mm. They differ only in the eighth digit, because the solver starts its parallel ray at a finite distance (check N1).</p>
<div class="pbox pbox--ex"><span class="pbox__t">Example 4.3 · what the aberrations cost</span>
<p>The default objective has $C_s=$ {{num:d_C_s}} mm and $C_c=$ {{num:d_C_c}} mm, of the order of the focal length, as for most real objectives. For a beam of 5 mrad half-angle the spherical miss is $C_s\alpha^3=$ {{num:ds5}} nm, and with the 0.215 eV spread of chapter 2 at 800 V the chromatic miss is $C_c\alpha\,\Delta E/E=$ {{num:dc5}} nm. At 800 V the chromatic aberration is therefore the larger of the two, which is why low-voltage columns care so much about the energy spread of their source. Diffraction is larger still at this angle: the radius of the Airy disc, $0.61\lambda/\alpha$, is {{num:dd5}} nm. Moving the wafer to 5 mm raises them to {{num:wd5_Cs}} and {{num:wd5_Cc}} mm ($f=$ {{num:wd5_f}} mm). A sharper field of $a=$ 1 mm with the wafer 2 mm from the centre lowers them to {{num:a1_Cs}} and {{num:a1_Cc}} mm and needs {{num:a1_NI}} A. Short working distance and a short, strong field are what make a good objective; chapter 5 shows how the beam angle is then chosen to balance diffraction against these blurs.</p></div>
'''})

S.append({'id': 'electric', 'title': 'Electric lenses, briefly', 'html': r'''
<p>An electric field can focus too. The same expansion as in {{sec:ch04-field}}, applied to Laplace's equation for the potential, gives near the axis $\varphi(r,z)=\phi(z)-\tfrac{r^2}{4}\phi''(z)+\dots$, with $\phi(z)$ the potential on the axis. The radial field $E_r=-\partial\varphi/\partial r=\tfrac r2\phi''$ again grows in proportion to $r$. So a region where $\phi''\ne0$ acts as a lens, converging or diverging depending on the sign and on how the electron's speed changes on the way. The retarding field of chapter 3 is such a lens. Electric lenses are common in the gun and in low-voltage columns, where the retarding field and the objective overlap. Their paraxial equation contains $\phi'$ and $\phi''$ besides $\phi$ and is solved in the same way. This project models only the magnetic objective, and it has no field solver. Both lens fields are analytic models, and a real design starts from a computed field (finite or boundary elements) of the actual pole pieces and electrodes.</p>
'''})

S.append({'id': 'checks', 'title': 'Checks, hand-over and limits', 'html': r'''
<p>The symbolic and numerical checks of this chapter, run by <code>derive/ch04.py</code>:</p>
''' + checks_table() + r'''
<p>The browser module <code>physics/ch04.js</code> and the Python reference <code>ref/ch04.py</code> run the same Runge–Kutta integrals on the same grid of 6000 steps, 60 bisection steps for the focus. They agree to about $10^{-11}$ in every output (parity check).</p>
<p><b>What chapter 5 receives.</b> $C_s$ and $C_c$ referred to the image (the wafer). The magnification $M$ from the object to the wafer is reported but not handed on. In chapter 5 the size of the source image on the wafer follows from the source brightness and the asked current. The lens here is computed at the landing voltage, that is, without a retarding field. In a column that decelerates the beam in front of the wafer, as in chapter 3's 5 kV to 800 V case, the electrons pass the objective at the higher voltage. The overlapping electric and magnetic fields would have to be solved together.</p>
<p><b>What the model leaves out.</b> The field is an analytic bell, not the computed field of real pole pieces; iron losses and saturation; misalignment of the lens with the beam and the off-axis aberrations (coma, astigmatism, field curvature, distortion) that it causes; the overlap with a retarding field; condenser lenses, whose aberrations the objective demagnifies. Each is a known part of real column design. Saturation breaks the $\sqrt{V^*}$ scaling of Example 4.2 for strong lenses; the others change the numbers, not the method.</p>
<div class="pbox pbox--ex"><span class="pbox__t">Problems</span><ol>
<li>From {{eq:glasersol4}}, find the value of $\omega$ for which a parallel ray crosses the axis exactly at the lens centre ($\psi=\pi/2$), and the corresponding $NI$ at 800 V. Show that it does not depend on $a$, and explain why {{eq:f4}} gives an infinite focal length there.</li>
<li>Show from {{eq:parax4}} that the lens strength is unchanged when $B$ is scaled by $\sqrt{V^*}$, and use this to explain Example 4.2.</li>
<li>Using $\Delta r_s=C_s\alpha^3$ and $\Delta r_d\approx\lambda/\alpha$ for diffraction, find the angle at which the two are equal for the default lens at 800 V, and the size of the blur there.</li>
</ol></div>
'''})

CH = {
    'title': 'The lens',
    'lead': r'A short coil in an iron shell focuses electrons as a glass lens focuses light, because the field lines that bulge out of its gap first twist the electron about the axis and then push it inwards, in proportion to its distance from the axis. We derive the field near the axis from Maxwell’s equations, the twist from Busch’s theorem and the paraxial ray equation from the radial force; solve Glaser’s bell-shaped lens exactly; focus it on the wafer; and measure its spherical and chromatic aberration by tracing rays, checked against the aberration integrals.',
    'sections': S,
    'figures': {'lens': {'svg': SVG_LENS, 'caption': 'A magnetic lens in section (sketch, not to scale): the coil inside an iron yoke, the field concentrated at the gap, and the axial field $B(z)$ that the chapter models by Glaser\'s bell curve.'}},
    'numbers': NUMS,
    'literals': LITERALS,
    'sim': {'module': 'ch04', 'title': 'The objective lens, focused on the wafer'},
}

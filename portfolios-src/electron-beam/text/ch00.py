"""The Electron Beam, from Tip to Measurement · text/ch00.py · chapter 0, The goal. Session S3.

The question of the project in plain words, the Abbe limit of light derived, why electrons, what the machine must deliver, and the road
through the chapters. The reading guide for the reviewer that PLAN.md puts at the top of chapter 0 is written by session S11 (file
ownership, PLAN.md section 7); the build places it above the chapters, so this file holds none.

Numbers: the optical limit and the electron wavelength come from the module physics/ch00.js (Abbe, and the relativistic de Broglie
wavelength), run in the page's JavaScript and in the Python reference. The givens of the story (the pitch of 2025 from the IRDS
roadmap, the wavelengths and apertures of the optics, the silicon lattice constant) are named constants with their source in the comment.
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
EB = os.path.abspath(os.path.join(HERE, '..'))
if EB not in sys.path:
    sys.path.insert(0, EB)
from ref import ch00 as R0, core as RC  # noqa: E402

NUMS = {}


def mod(name, inputs, out, scale=1, sig=3):
    NUMS[name] = {'module': 'ch00', 'inputs': inputs, 'out': out, 'scale': scale, 'sig': sig}


def ex(name, expr, of=None, scale=1, sig=3):
    NUMS[name] = {'expr': expr, 'of': dict(of or {}), 'scale': scale, 'sig': sig}


def const(name, value, scale=1, sig=3):
    ex(name, repr(float(value)), {}, scale, sig)


# givens, with their sources
const('pitch', 20e-9, 1e9, 2)          # tightest metal pitch of 2025, G45M20: IRDS 2022 More Moore, Table MM-7 (p. 7)
const('lam_arf', 193e-9, 1e9, 3)       # ArF excimer laser wavelength, the deep-ultraviolet line of immersion lithography
const('na_arf', 1.35, 1, 3)            # a typical immersion numerical aperture: an assumption of the figure (the ceiling is the index of water)
const('lam_euv', 13.5e-9, 1e9, 3)      # EUV wavelength, IRDS 2022 Lithography
const('na_euv1', 0.33, 1, 2)           # IRDS 2022 Lithography: 0.33 NA, the workhorse
const('na_euv2', 0.55, 1, 2)           # IRDS 2022 Lithography: 0.55 NA, high-NA
const('si_a', 5.431020511e-10, 1e9, 3)  # silicon lattice parameter (CODATA 2018, 22.5 degrees C)

mod('abbe_arf', {'lambda_opt': 193e-9, 'NA': 1.35}, 'd_opt', 1e9, 3)
mod('abbe_euv1', {'lambda_opt': 13.5e-9, 'NA': 0.33}, 'd_opt', 1e9, 3)
mod('abbe_euv2', {'lambda_opt': 13.5e-9, 'NA': 0.55}, 'd_opt', 1e9, 3)
mod('lam_1k', {'V_acc': 1000.0}, 'lambda_e', 1e12, 3)
mod('lam_30k', {'V_acc': 30000.0}, 'lambda_e', 1e12, 3)
ex('hp', 'p/2', {'p': 'pitch'}, 1e9, 2)
ex('si_nn', 'a*sqrt(3)/4', {'a': 'si_a'}, 1e9, 3)
ex('si_atoms', 'h/n', {'h': 'hp', 'n': 'si_nn'}, 1, 2)
ex('ratio_arf', 'a/p', {'a': 'abbe_arf', 'p': 'pitch'}, 1, 2)
ex('abbe_hp_euv1', 'a/2', {'a': 'abbe_euv1'}, 1e9, 3)
ex('lamfrac_1k', 'l/a', {'l': 'lam_1k', 'a': 'si_a'}, 1, 2)
ex('pitch_over_lam30k', 'p/l', {'p': 'pitch', 'l': 'lam_30k'}, 1, 4)

_V = {}
_used = set()


def n(key, sig=None):
    """{{num:..}} for a declared number, with its own digits or `sig` significant figures."""
    if sig is None:
        _used.add(key)
        return '{{num:%s}}' % key
    name = '%s_s%d' % (key, sig)
    NUMS.setdefault(name, {'expr': 'x', 'of': {'x': key}, 'scale': NUMS[key]['scale'], 'sig': sig})
    _used.add(name)
    return '{{num:%s}}' % name


def fig_scales():
    """Figure 0.1: the structure pitch, the optical limit lambda/2NA and the electron wavelength on one logarithmic axis, computed with ref/ch00.py."""
    g = {}
    g['arf'] = R0.compute({'V_acc': 1000.0, 'lambda_opt': 193e-9, 'NA': 1.35, 'w_feat': 20e-9})['d_opt']
    g['euv1'] = R0.compute({'V_acc': 1000.0, 'lambda_opt': 13.5e-9, 'NA': 0.33, 'w_feat': 20e-9})['d_opt']
    g['euv2'] = R0.compute({'V_acc': 1000.0, 'lambda_opt': 13.5e-9, 'NA': 0.55, 'w_feat': 20e-9})['d_opt']
    e1 = R0.compute({'V_acc': 1000.0, 'lambda_opt': 193e-9, 'NA': 1.35, 'w_feat': 20e-9})['lambda_e']
    e30 = R0.compute({'V_acc': 30000.0, 'lambda_opt': 193e-9, 'NA': 1.35, 'w_feat': 20e-9})['lambda_e']
    items = [('light', 'ArF immersion, λ/2NA', g['arf'], '#8b8079'), ('light', 'EUV 0.33 NA, λ/2NA', g['euv1'], '#8b8079'),
             ('light', 'EUV 0.55 NA, λ/2NA', g['euv2'], '#8b8079'),
             ('feature', 'tightest metal pitch, 2025', 20e-9, '#7a1f2b'), ('feature', 'silicon crystal cell', 5.431020511e-10, '#7a1f2b'),
             ('electron', 'electron, 1 kV: λ', e1, '#1c1518'), ('electron', 'electron, 30 kV: λ', e30, '#1c1518')]
    x0, w, lo, hi = 40, 680, -12.0, -6.0
    X = lambda v: x0 + (math.log10(v) - lo) / (hi - lo) * w
    s = ['<svg viewBox="0 0 760 400" role="img" aria-label="A logarithmic length axis from one picometre to one micrometre. The feature pitch, the optical limit and the electron wavelength are marked.">',
         '<rect width="760" height="400" fill="#fff"/>']
    for e in range(-12, -5):
        x = X(10.0 ** e)
        s.append('<line x1="%.1f" y1="30" x2="%.1f" y2="372" stroke="#f0ebe3"/>' % (x, x))
        s.append('<text class="tick" x="%.1f" y="392" text-anchor="middle">%s</text>' % (x, {-12: '1 pm', -11: '10 pm', -10: '100 pm', -9: '1 nm', -8: '10 nm', -7: '100 nm', -6: '1 µm'}[e]))
    s.append('<line x1="%d" y1="372" x2="%d" y2="372" stroke="#6f655f"/>' % (x0, x0 + w))
    groups = [('light', 'light: smallest period resolved, λ/2NA', 62), ('feature', 'the structures to be measured', 190), ('electron', 'electrons: wavelength λ', 290)]
    ys = {'light': [92, 120, 148], 'feature': [220, 248], 'electron': [320, 348]}
    for k, lab, y in groups:
        s.append('<text class="lbl" x="%d" y="%d" font-weight="600">%s</text>' % (x0, y, lab))
    cnt = {k: 0 for k in ys}
    for kind, lab, v, col in items:
        y = ys[kind][cnt[kind]]
        cnt[kind] += 1
        s.append('<circle cx="%.1f" cy="%d" r="6" fill="%s"/>' % (X(v), y, col))
        txt = '%s  %s' % (lab, ('%.3g nm' % (v * 1e9)) if v >= 1e-9 else ('%.3g pm' % (v * 1e12)))
        anchor, tx = ('start', X(v) + 12) if X(v) < 500 else ('end', X(v) - 12)
        s.append('<text class="lbl" x="%.1f" y="%d" text-anchor="%s">%s</text>' % (tx, y + 4, anchor, txt))
    s.append('</svg>')
    return ''.join(s)


SECTIONS = [
    {'id': 'question', 'title': 'The question', 'star': False, 'html': '''
<p class="psec__lead">A chip is a few square centimetres of silicon carrying billions of switches. One switch that is the wrong size, or one wire that is cut, can make the whole chip useless, so every manufacturing step is followed by a measurement, and the measuring machine has to look at structures that are only a few nanometres across.</p>
<p>Take the tightest wires of a processor of 2025. The International Roadmap for Devices and Systems (IRDS 2022, <em>More Moore</em>, Table MM-7) lists their pitch, the distance from the middle of one wire to the middle of the next, as %(pitch)s&nbsp;nm: a line about %(hp)s&nbsp;nm wide, then a gap of the same width, and so on. A hydrogen atom is about a tenth of a nanometre across. The cubic cell of the silicon crystal is %(si_a)s&nbsp;nm wide (CODATA 2018) and neighbouring atoms are %(si_nn)s&nbsp;nm apart, so a line %(hp)s&nbsp;nm wide is about %(si_atoms)s atoms across. The task is to say, for a line like that, where its edges are, how tall it is and what it is made of, and to say it for millions of lines on a wafer and within minutes, so that a factory can correct its machines before the next wafer is spoiled.</p>
<p>Think of reading a coin in the dark by running a fingertip over it. A finger tells you the coin is round and has a head on it, but the fine engraving is lost, because the fingertip is wider than the lines. A sharp needle can follow them. An electron beam is that needle: a very thin probe that is scanned across the wafer, one point after another, while a detector counts what comes back from each point. This project builds, chapter by chapter, the physics of that needle and of the machine that holds it, and checks each part against theory and published measurements.</p>
'''},
    {'id': 'light', 'title': 'Why light is not enough', 'star': False, 'html': '''
<p>The obvious probe is light, and light is used for many steps of chip making. It has a limit, and we derive it, because the limit is the reason for the whole project.</p>
<p>Imagine a pattern of lines with period (pitch) $p$, lit by a plane light wave of wavelength $\\lambda$ in a medium of refractive index $n$. The pattern acts as a diffraction grating: the light leaves in directions $\\theta_m$ given by the grating equation $p\\,(\\sin\\theta_m-\\sin\\theta_i)=m\\lambda/n$, where $\\theta_i$ is the angle of incidence and $m=0,\\pm1,\\pm2,\\dots$ counts the diffraction orders. The picture of the grating is carried by the interference of the orders. If a lens collects <em>only</em> the zeroth order, it sees a uniform bright field and no lines at all. To see lines, at least one more order must enter the lens. A lens can accept rays up to an angle $\\alpha$ from its axis; the number $\\mathrm{NA}=n\\sin\\alpha$ is its <em>numerical aperture</em>. Tilt the illumination to the edge of the aperture, $\\theta_i=\\alpha$, so that the zeroth order enters at $+\\alpha$; the order $m=-1$ then leaves at $\\sin\\theta_{-1}=\\sin\\alpha-\\lambda/(np)$, and it still enters the lens when this is at least $-\\sin\\alpha$. That requires $\\lambda/(np)\\le2\\sin\\alpha$:</p>
$$p_{\\min}=\\frac{\\lambda}{2\\,\\mathrm{NA}} . \\label{abbe}$$
<p>This is Abbe's limit (E. Abbe, <em>Arch. mikrosk. Anat.</em> 9, 413, 1873). It is a statement about the <em>period</em>; the smallest line is half of it. Light is therefore limited by two numbers it cannot change much: its wavelength, and the numerical aperture, which cannot exceed the refractive index of the medium. For deep-ultraviolet light of wavelength %(lam_arf)s&nbsp;nm through water (a numerical aperture of %(na_arf)s is a typical value of an immersion tool, and the ceiling is the index of water) $p_{\\min}=$ %(abbe_arf)s&nbsp;nm, %(ratio_arf)s times the pitch of %(pitch)s&nbsp;nm that we want to look at. With extreme ultraviolet (EUV) light of %(lam_euv)s&nbsp;nm, the roadmap's workhorse aperture of %(na_euv1)s gives $p_{\\min}=$ %(abbe_euv1)s&nbsp;nm and its high-NA successor of %(na_euv2)s gives %(abbe_euv2)s&nbsp;nm. The IRDS lithography chapter says that a half-pitch of 12 nm is "optically resolvable by 0.33 NA optics" (a half-pitch of %(abbe_hp_euv1)s&nbsp;nm by {{eq:abbe}}, so the statement is consistent with the limit), but resists limit it in practice. EUV light is made in a hot tin plasma, is absorbed by every material, even air, and has to be reflected from mirrors in vacuum. It prints patterns; it is not a practical way to look at millions of them quickly on every wafer. Optical measurement of finished patterns works on test targets of many lines and infers a shape from what the whole target does to the light; Applied Materials describes this as "optical target-based approximation, statistical sampling, and single-layer control" and says that leading-edge designs need a metrology that goes beyond it.</p>
'''},
    {'id': 'electrons', 'title': 'Why electrons', 'star': False, 'html': '''
<p>An electron is also a wave. Its wavelength is $\\lambda=h/p$, where $h=6.626\\,070\\,15\\times10^{-34}\\ \\mathrm{J\\,s}$ is Planck's constant and $p$ the momentum. An electron that has fallen through a voltage $V$ has the kinetic energy $T=eV$; the relativistic relation between energy and momentum, $(pc)^2=T(T+2mc^2)$, gives, as chapter 1 derives in {{sec:ch01-nr}},</p>
$$\\lambda=\\frac{h}{\\sqrt{2meV\\left(1+\\dfrac{eV}{2mc^2}\\right)}} . \\label{lam0}$$
<p>At $V=1\\ \\mathrm{kV}$ this is $\\lambda=$ %(lam_1k)s&nbsp;pm and at 30 kV it is %(lam_30k)s&nbsp;pm (1 pm is a thousandth of a nanometre). The wavelength is %(lamfrac_1k)s of the silicon lattice constant at 1 kV and %(pitch_over_lam30k)s times smaller than the %(pitch)s&nbsp;nm pitch at 30 kV. This one number settles a question of principle: for electrons the diffraction limit of {{eq:abbe}} is not what stops us. {{fig:scales}} puts the three lengths on one axis.</p>
{{figure:scales}}
<p>An electron microscope does not reach a spot of the size of its wavelength, because the lenses that focus electrons are much worse than glass lenses, as chapters 4 and 5 show. The spot is set by the source size, the aberrations of the lenses and the diffraction at the aperture, and this chain is the subject of the project. What the short wavelength buys is that it is not the first limit, so that a better source and better lenses can still improve the picture.</p>
<p>There are three further reasons, each worked out in a later chapter. An electron has the charge $-e$, so electric and magnetic fields can steer and focus it: chapter 1 describes how, and every lens of chapter 4 is such a field. An X-ray photon has no charge, so no field can steer it; its optics are limited to weak, specialised elements such as zone plates and grazing-incidence mirrors, though its wavelength is short. An ion has the charge and a short wavelength as well, but it is thousands of times heavier (a proton alone is 1836 times the electron mass), and at kilovolt energies it knocks atoms out of the surface it is meant to examine; an electron of the same energy mostly does not (chapter 6). And what comes back is useful: electrons of the surface layer, which carry the shape, and backscattered electrons from deeper layers, which carry the material (chapter 6).</p>
'''},
    {'id': 'demands', 'title': 'What the machine has to deliver', 'star': False, 'html': '''
<p>The probe has to do four things at once, and they pull against each other.</p>
<p>The <em>spot</em> must be thinner than the structure, or every measurement averages over neighbours. The <em>current</em> in the spot must be large enough that the picture is clean: electrons arrive one at a time, so the number counted in a pixel fluctuates by the square root of the number (shot noise), and a clean edge needs thousands of counts. The beam must be <em>gentle enough</em> for fragile resist, which a fast electron damages, and still reach buried layers, which a slow electron cannot, so the landing energy is a compromise. And it must be <em>fast</em>, because a factory measures many wafers an hour. A smaller spot means less current, because the electrons come from a source of finite brightness; less current means longer dwell time per pixel, and so slower measurement. Chapters 2 to 8 follow these dependences quantitatively.</p>
<p>The state of the art can be read off the public statements of one manufacturer. Applied Materials says on the product page of its PROVision 10 system (read on 9 November 2026) that the column uses "cold field emission (CFE) technology", that it reaches "up to 100 million accurate, actionable measurements per hour", that its Elluminator "captures 95% of back-scattered electrons", and that it offers "high-energy modes for rapid measurement, hundreds of nanometers deep, and low-energy modes for damage-free measurement of fragile materials and structures, including EUV and high-NA EUV photoresist". In the press release of 14 December 2022 it contrasts "thermal field emission" sources, operated at "more than 1,500°C", with cold field emission, "a narrower beam with more electrons", "sub-nanometer image resolution and a 10X increase in imaging speed". The price is a vacuum "well below" 10<sup>−11</sup> millibar (the release prints "1×10 – 11"), two to three orders of magnitude better than for thermal sources, because "if a single atom adheres to the eBeam source tip, it can partially block the emission of electrons", and a "cyclical self-cleaning process". We quote these as public claims by the manufacturer. This project is not affiliated with Applied Materials, does not use its data, and models no product of the company; it builds the physics from the first principles that every such column rests on, and the statements above show which behaviour those principles must be able to explain: why a cold tip is bright but fragile, why a vacuum of 10<sup>−9</sup> pascal matters, why a high-energy mode sees deeper.</p>
'''},
    {'id': 'road', 'title': 'The road through the chapters', 'star': False, 'html': '''
<p>Each chapter has one question, a derivation, a simulation with every parameter as a slider, and a hand-over to the next.</p>
<table class="ptab"><thead><tr><th>chapter</th><th>question</th><th>hands over</th></tr></thead><tbody>
<tr><td>1</td><td>Where does one electron go in given fields?</td><td>force law, energy relation, integrator</td></tr>
<tr><td>2</td><td>How does the tip emit, and how does a single atom change it?</td><td>current, brightness, energy spread, source size</td></tr>
<tr><td>3</td><td>What does acceleration do to the beam?</td><td>energy, wavelength, relativistic factor</td></tr>
<tr><td>4</td><td>How can a field focus?</td><td>focal length, aberration coefficients</td></tr>
<tr><td>5</td><td>How small can the spot get?</td><td>probe diameter and current</td></tr>
<tr><td>6</td><td>What happens when the beam hits the wafer?</td><td>yields, range, signal spread</td></tr>
<tr><td>7</td><td>How is a width read from a noisy picture?</td><td>uncertainty, measurements per hour</td></tr>
<tr><td>8</td><td>How do the parts behave as a whole machine?</td><td>sensitivities, tolerances, process window</td></tr>
</tbody></table>
<p>The model leaves out a field solver for arbitrary electrodes beyond what chapter 4 builds, aberration-corrected optics, and every proprietary detail of any real column. Where a number comes from is stated where it first appears. We start with the electron itself.</p>
'''},
]


def _fill(h):
    """Replace %(key)s by {{num:key}} (a declared number, printed with its own digits)."""
    import re
    return re.sub(r'%\((\w+)\)s', lambda m: n(m.group(1)), h)


for _s in SECTIONS:
    _s['html'] = _fill(_s['html'])

_FIG = {'svg': fig_scales(), 'caption': 'Lengths on a logarithmic axis, from one picometre to one micrometre. Red: the pitch to be measured (IRDS 2022) and the cell size of the silicon crystal. Grey: the smallest period that light of the quoted wavelength and numerical aperture can resolve, $\\lambda/2\\mathrm{NA}$; the ArF aperture is an assumption of the figure, the EUV values are those of the roadmap. Black: the wavelength of electrons of 1 kV and 30 kV.'}


def _closure(names):
    seen, stack = set(), list(names)
    while stack:
        k = stack.pop()
        if k not in seen:
            seen.add(k)
            stack.extend(NUMS[k].get('of', {}).values())
    return seen


LITERALS = {
    '1836': 'proton-to-electron mass ratio, CODATA 2018 (1836.15267343), quoted from the source',
    '6.626\\,070\\,15\\times10^{-34}': 'Planck constant in J s, CODATA 2018 (exact)',
    '12 nm': 'IRDS 2022 Lithography: "12-nm half-pitch is optically resolvable by 0.33 NA optics", quoted from the source',
    '0.33 NA': 'IRDS 2022 Lithography, quoted from the source',
    '9, 413, 1873': 'Abbe, Arch. mikrosk. Anat. 9, 413 (1873): volume, first page and year of the paper cited',
    '1 pm is': 'the definition of the picometre, a unit',
    '30 kV': 'the column voltage of the second example, a given of the problem',
    '1 kV': 'the voltage of the first example, a given of the problem',
    '100 million': 'Applied Materials product page, quoted from the source as a public claim',
    '95%': 'Applied Materials product page, quoted from the source as a public claim',
    '1,500°C': 'Applied Materials press release of 14 December 2022, quoted from the source as a public claim',
    '10X': 'Applied Materials press release of 14 December 2022, quoted from the source as a public claim',
    '1×10 – 11': 'the way the press release prints its vacuum figure, quoted from the source',
    '−11': 'the exponent of the vacuum of the press release, well below 1e-11 millibar, read from the source',
    '−9': 'the exponent of the same vacuum in pascal (1 millibar is 100 pascal), derived from the quoted value',
    '14 December': 'date of the Applied Materials press release',
    '10-34': 'exponent of the Planck constant, CODATA 2018',
    '0.33': 'IRDS 2022 Lithography numerical aperture, quoted from the source',
    '1 millibar': 'unit definition',
    '2 to 3': 'chapter numbers',
}

CH = {
    'title': 'The goal',
    'sections': SECTIONS,
    'figures': {'scales': _FIG},
    'numbers': {k: NUMS[k] for k in sorted(_closure(_used))},
    'literals': LITERALS,
}

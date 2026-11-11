"""The Electron Beam, from Tip to Measurement · text/ch07.py · chapter 7, Detect and measure.

Written by the finisher (9 November 2026). Format: eb_lib.py (the dict CH). Numbers: outputs of physics/ch07.js (checked through ref/ch07.py),
expressions of them, and the values derive/ch07.py writes to data/ch07/derive_results.json.
"""
import html
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
EB = os.path.abspath(os.path.join(HERE, '..'))
if EB not in sys.path:
    sys.path.insert(0, EB)

DER = json.load(open(os.path.join(EB, 'data', 'ch07', 'derive_results.json'), encoding='utf-8'))
NUMS = {}


def mod(name, inputs, out, module='ch07', scale=1, sig=3):
    NUMS[name] = {'module': module, 'inputs': inputs, 'out': out, 'scale': scale, 'sig': sig}


def ex(name, expr, of=None, scale=1, sig=3):
    NUMS[name] = {'expr': expr, 'of': dict(of or {}), 'scale': scale, 'sig': sig}


def const(name, value, sig=3):
    ex(name, repr(float(value)), {}, 1, sig)


# ---- the default measurement
mod('d_n', {}, 'n_pe', sig=2)
mod('d_snr', {}, 'SNR', sig=2)
mod('d_cdm', {}, 'CD_meas', scale=1e9, sig=3)
mod('d_sig', {}, 'sigma_CD', scale=1e9, sig=2)
mod('d_sigmc', {}, 'sigma_CD_mc', scale=1e9, sig=2)
mod('d_dose', {}, 'dose', scale=100, sig=2)
mod('d_mph', {}, 'MPH', scale=3600, sig=2)
ex('d_bias', '(a-2e-8)*1e9', {'a': 'd_cdm'}, sig=2)
ex('d_tframe', '512**2*1e-7*1e3', {}, sig=2)              # ms, N_px = 512, t_d = 100 ns
ex('d_mph_noov', '3600/(512**2*1e-7)', {}, sig=2)
ex('d_rows_e', 'n*512', {'n': 'd_n'}, sig=2)
# ten times the dwell
mod('t10_sig', {'t_d': 1e-6}, 'sigma_CD', scale=1e9, sig=2)
mod('t10_snr', {'t_d': 1e-6}, 'SNR', sig=2)
mod('t10_dose', {'t_d': 1e-6}, 'dose', scale=100, sig=2)
mod('t10_mph', {'t_d': 1e-6}, 'MPH', scale=3600, sig=2)
ex('t10_ratio', 'a/b', {'a': 'd_sig', 'b': 't10_sig'}, sig=3)
# a fin-like line: vertical walls, taller, narrower
FIN = {'sidewall': 0.0, 'height': 5e-8, 'cd': 1.5e-8}
mod('fin_snr', FIN, 'SNR', sig=2)
mod('fin_cdm', FIN, 'CD_meas', scale=1e9, sig=3)
mod('fin_sig', FIN, 'sigma_CD', scale=1e9, sig=2)
# a blunt probe
mod('bl_cdm', {'d_p': 1.5e-8}, 'CD_meas', scale=1e9, sig=3)
mod('bl_sig', {'d_p': 1.5e-8}, 'sigma_CD', scale=1e9, sig=2)
mod('c5_dp', {}, 'd_p', module='ch05', scale=1e9, sig=2)
mod('fin_bias_n', FIN, 'CD_meas', scale=1e9, sig=3)
ex('fin_bias', '(a-1.5e-8)*1e9', {'a': 'fin_cdm'}, sig=2)
ex('fin_bias_pct', '100*(a-1.5e-8)/1.5e-8', {'a': 'fin_cdm'}, sig=2)
ex('bl_bias', '(a-2e-8)*1e9', {'a': 'bl_cdm'}, sig=2)
mod('bl_sigmc', {'d_p': 1.5e-8}, 'sigma_CD_mc', scale=1e9, sig=2)
ex('sig_b', 'sqrt((5.3e-9/2.3548)**2+(3.33e-9)**2)*1e9', {}, sig=2)
ex('blur_space', 'sqrt((5.3e-9/2.3548)**2+(3.33e-9)**2)/2e-8', {}, sig=2)
# checks
DN = DER['numbers']
const('cd_sharp', DN['cd_sharp'] * 1e9, sig=4)
const('cd_bottom', DN['bottom'] * 1e9, sig=4)
const('slope_t', DN['slopes']['t_d'], sig=3)
# Applied's public claim, quoted: up to 100 million measurements per hour
ex('amat_us', '3600/1e8*1e6', {}, sig=2)
ex('amat_per_image', '1e8/3600*512**2*1e-7', {}, sig=2)

LITERALS = {
    '30 kV': 'a landing voltage of chapter 6, a given', '0.76': 'chapter 6\'s δ, rounded, the default input', '0.24': 'chapter 6\'s η, rounded, the default input',
    '20 %': 'the agreement level of check C6', '3.3 nm': 'chapter 6\'s core width, rounded, the default input', '86 %': 'chapter 6\'s core fraction, the default input', '8.7 nm': 'chapter 6\'s halo width, the default input', '2.7 nm': 'Lin and Joy\'s escape depth for silicon, quoted', '1.5': 'aspect ratio h/CD = 30/20, givens',
    '5 %': 'the contrast below which the module stops', '4000': 'the number of Monte Carlo repeats', '1 %': 'the statistical error of the Monte Carlo, rounded',
    'two neighbouring periods': 'what the code adds at small blur', 'Example 7.4': 'the number of a worked example', 'four times': 'a factor of a problem',
    '7.1.26': 'formula number in Abramowitz and Stegun', '1964': 'year of Abramowitz and Stegun', '1.3 %': 'the effect of counting backscattered electrons as Poisson, from the derivation review', '0.1 nm': 'a target of a problem, a given', '10^{-10}': 'the measured parity agreement',
    'Example 7.1': 'the number of a worked example', 'Example 7.2': 'the number of a worked example', 'Example 7.3': 'the number of a worked example',
    '20 nm': 'the true CD of the default, a given', '40 nm': 'the pitch of the default, a given', '30 nm': 'the height of the default, a given',
    '2°': 'the sidewall angle of the default, a given', '1 nm': 'the pixel size of the default, a given', '100 ns': 'the dwell time of the default, a given',
    '512': 'pixels per line and lines per image of the default, a given', '10 pA': 'the probe current of the default, a given', '0.5': 'the collection fraction of the default, a given',
    '1 s': 'the assumed overhead per site, a given', '800 V': 'the landing voltage, a given', '1000': 'the number of Monte Carlo repeats', '95%': 'Applied\'s claim, quoted',
    '100 million': 'Applied\'s claim, quoted', '1 µs': 'the dwell time of Example 7.2, a given', '15 nm': 'the CD of the fin-like line, a given', '50 nm': 'the height of the fin-like line, a given',
    '15 nm,': 'the probe of Example 7.1, a given', 'three pixels': 'the peak average of the algorithm', '7.1.26': 'formula number in Abramowitz and Stegun',
    '1.5\\times10^{-7}': 'accuracy of that formula, quoted', '2.355': 'the FWHM of a Gaussian in units of sigma', 'C1': 'check label', 'C8': 'check label', 'ten': 'a given factor',
    '1 C m⁻²': 'unit conversion', '100 µC cm⁻²': 'unit conversion', 'half': 'the threshold level, a choice', '0.1 %': 'the contrast below which the module stops',
}


def checks_table():
    rows = ''.join('<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (c['id'], html.escape(c['title']), 'pass' if c['ok'] else 'FAIL', html.escape(c['detail']))
                   for c in DER['checks'])
    return '<div class="ptab-wrap"><table class="ptab ptab--checks"><thead><tr><th>check</th><th>what is verified</th><th>result</th><th>detail</th></tr></thead><tbody>%s</tbody></table></div>' % rows


# Label size of the figure: 23 units of the 640-unit width on a phone (11 px on a 360 px screen), 17 on a small tablet, 15 on a wide
# screen (16 to 17 px). Every label is placed for the largest size, so it stays clear of the drawing at all three; the words for the
# tilted wall stand below it.
SVGCSS = ('<style>.pfig svg.ebf text{font-family:\'IBM Plex Mono\',monospace;font-size:23px}'
          '@media (min-width:480px){.pfig svg.ebf text{font-size:17px}}@media (min-width:760px){.pfig svg.ebf text{font-size:15px}}</style>')
STY = 'fill:#3a322e'
SVG_EDGE = ('<svg class="ebf" viewBox="0 0 640 440" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Why an edge is bright: the beam crosses the thin escape layer at a slant on a steep wall">'
            + SVGCSS +
            '<rect width="640" height="440" fill="#fff"/>'
            # flat surface with escape layer
            '<rect x="20" y="200" width="280" height="130" fill="#efe4c8" stroke="#3a322e"/><rect x="20" y="200" width="280" height="16" fill="#e2a2aa" opacity="0.6"/>'
            '<line x1="200" y1="60" x2="200" y2="300" stroke="#7a1f2b" stroke-width="2.5"/><text x="210" y="84" style="%s">beam</text>'
            '<line x1="186" y1="200" x2="186" y2="216" stroke="#1c1518" stroke-width="2"/><text x="24" y="186" style="%s">escape layer</text><text x="186" y="252" text-anchor="end" style="%s">path λ_s</text>'
            # tilted wall
            '<path d="M340 330 L340 200 L450 90 L620 90 L620 330 Z" fill="#efe4c8" stroke="#3a322e"/>'
            '<path d="M340 200 L450 90 L461 101 L351 211 Z" fill="#e2a2aa" opacity="0.6"/>'
            '<line x1="400" y1="20" x2="400" y2="300" stroke="#7a1f2b" stroke-width="2.5"/><text x="410" y="44" style="%s">beam</text>'
            '<line x1="394" y1="146" x2="394" y2="168" stroke="#1c1518" stroke-width="2"/>'
            '<text x="340" y="364" style="%s">wall tilted by θ:<tspan x="340" dy="1.25em">path λ_s / cos θ,</tspan><tspan x="340" dy="1.25em">more SE</tspan></text>'
            '</svg>') % ((STY,) * 5)


S = []
S.append({'id': 'picture', 'title': 'Reading a width from an image', 'html': r'''
<p>A metrology tool in a chip factory does one thing over and over: it puts the probe of chapter 5 on a pattern, scans it across in lines, counts the electrons that come back for each point, and reads a width, the critical dimension (CD), from the resulting picture. A good picture needs many electrons per point; a factory needs many measurements per hour; and the wafer must not be damaged by the beam. This chapter turns those three demands into numbers for the simplest pattern there is, a row of parallel lines.</p>
<p>The lines in an electron image look like their own outlines: bright edges on a duller ground. {{fig:edge}} shows why. Secondary electrons escape only from a thin layer under the surface, of thickness about the escape depth $\lambda_s$ of chapter 6. A beam that hits a flat surface crosses that layer on a path of length $\lambda_s$; one that hits a wall tilted by $\theta$ crosses it on the longer path $\lambda_s/\cos\theta$ and frees proportionally more secondaries that can get out. The yield grows as $1/\cos\theta$, the <em>secant law</em>, and on a near-vertical wall it is many times the flat value.</p>
{{figure:edge}}
'''})

S.append({'id': 'signal', 'title': 'The expected profile', 'html': r'''
<p>Across one period $p$ of the pattern, a line of width CD at half its height $h$ stands on the floor; its walls lean by the angle $\beta$ from the vertical, so each wall covers the width $w=h\tan\beta$ seen from above. On the flat top and floor the yield is chapter 6's $\delta$. On a wall the surface is tilted by $\theta=90^\circ-\beta$, and the secant law gives $\delta/\sin\beta$. The excess over the flat value, summed across one wall, is</p>
$$ \delta\left(\frac{1}{\sin\beta}-1\right)h\tan\beta=\delta\,h\left(\frac{1}{\cos\beta}-\tan\beta\right) , \label{excess7} $$
<p>which stays finite for a vertical wall, where it becomes $\delta h$ (check C3): a vertical wall is invisible in projection, yet it adds as much signal as a flat strip of width $h$. Backscattered electrons add a flat $\eta$, because we give them no dependence on the slope.</p>
<p>The detector never sees this sharp map. The probe has a size, and the signal spreads in the solid before it escapes. We treat both as Gaussian blurs. A round Gaussian probe of FW50 diameter $d_p$ has the standard deviation $\sigma_p=d_p/2.355$ along any line (check C2). Chapter 6 splits the escaping secondaries into a core, a fraction $f_\mathrm{core}$ of width $\sigma_\mathrm{core}$ made by the incoming beam, and a halo of width $\sigma_\mathrm{halo}$ made by backscattered electrons. Each part is blurred by its own Gaussian, $\sigma_1^2=\sigma_p^2+\sigma_\mathrm{core}^2$ and $\sigma_2^2=\sigma_p^2+\sigma_\mathrm{halo}^2$. The expected yield at the beam position $x$ is then the flat value plus each wall's excess spread over its width and blurred,</p>
$$ Y(x)=\delta+\eta+\sum_\text{walls}\frac{\delta h(1/\cos\beta-\tan\beta)}{w}\sum_{k=1,2}f_k\left[\Phi\!\left(\frac{x-x_1}{\sigma_k}\right)-\Phi\!\left(\frac{x-x_2}{\sigma_k}\right)\right], \label{profile7} $$
<p>with $f_1=f_\mathrm{core}$, $f_2=1-f_\mathrm{core}$, $x_1$ and $x_2$ the ends of a wall in projection and $\Phi$ the cumulative normal distribution (the error function, approximated to $1.5\times10^{-7}$ by formula 7.1.26 of M. Abramowitz and I. A. Stegun, <em>Handbook of Mathematical Functions</em>, 1964, check C4). The pattern is periodic, so the walls of the neighbouring lines are added too (two neighbouring periods on each side when the blur is small, more when it is wide; a halo wider than twice the pitch is simply a uniform background): at a pitch of 40 nm and a blur of a few nanometres they overlap.</p>
<p>The default numbers are chapter 6's silicon at 800 V, rounded: $\delta=0.76$, $\eta=0.24$, a core of 3.3 nm holding 86 % of the signal and a halo of 8.7 nm (the core includes the escape depth $\lambda_s=2.7$ nm), and chapter 5's probe of {{num:c5_dp}} nm, so $\sigma_1=$ {{num:sig_b}} nm. The line is 20 nm wide and 30 nm high (aspect ratio 1.5), the space 20 nm, and the core blur is {{num:blur_space}} of the space: the edges are sharp enough to find, but the neighbours' edges already lift the floor.</p>
<p>A Gaussian is a fair stand-in for the probe. For each part of the signal it is rougher, and the split into two parts is itself a summary of chapter 6's histogram, not its full shape.</p>
'''})

S.append({'id': 'noise', 'title': 'Counting electrons', 'html': r'''
<p>Electrons arrive one by one. A current of $I_p$ held on a pixel for the dwell time $t_d$ brings on average $\bar n=I_pt_d/e$ electrons, and the actual number fluctuates from pixel to pixel by the Poisson law, with variance equal to the mean. This is <em>shot noise</em>, and it is where the graininess of charge, a quantum fact, enters the measurement. Each beam electron then frees a random number of secondaries, of which a fraction $\eta_c$ reaches the detector. If that number is also Poisson, with mean $m=\eta_cY$, the counts $k$ of one pixel have</p>
$$ \langle k\rangle=\bar n\,m,\qquad \operatorname{Var}k=\bar n\,(m+m^2) \label{var7} $$
<p>by the law of total variance (check C1): the beam's own shot noise is amplified by the random yield. Whether secondaries really follow Poisson statistics we did not verify against a measurement; it is the simplest assumption and is stated as such. (Backscattered electrons are counted the same way, although each beam electron gives at most one; that adds about 1.3 % to the variance at the default.)</p>
<p>A useful single number is the contrast-to-noise ratio of one scan line, $\mathrm{SNR}=(\langle k_\text{edge}\rangle-\langle k_\text{floor}\rangle)/\sqrt{\operatorname{Var}k_\text{floor}}$: how far the bright edge stands out of the noise of the floor, in one line of the raw image.</p>
<div class="pbox pbox--ex"><span class="pbox__t">Example 7.1 · one line of the default image</span>
<p>With 10 pA and 100 ns per pixel, each pixel receives $\bar n=$ {{num:d_n}} electrons. On a 1 nm pixel that is a dose of {{num:d_dose}} µC cm<sup>−2</sup> per image, the order of the dose that exposes an electron-beam resist, which is why resists shrink under a metrology beam. With the collection fraction 0.5, one scan line has $\mathrm{SNR}=$ {{num:d_snr}}: the edges stand out of the noise by only a few standard deviations. The tool averages the 512 lines of the image along the line direction into one profile: {{num:d_rows_e}} beam electrons land on each position across the line, and the detector counts the fraction $\eta_cY$ of them.</p></div>
<p>The collection fraction $\eta_c$ is a property of the detector. Applied Materials states publicly that the Elluminator detector of its PROVision 10 system "captures 95% of back-scattered electrons" (<a href="https://www.appliedmaterials.com/us/en/product-library/provision-10-ebeam-metrology.html">product page</a>, read 9 November 2026). We quote that as the company's claim (the page was re-read on that date); it concerns backscattered, not secondary, electrons, and it is not an input of this model, whose default 0.5 is an assumption.</p>
'''})

S.append({'id': 'edges', 'title': 'Finding the edges', 'html': r'''
<p>The averaged profile is still noisy, and the width must be read from it by a rule. We use a simple and common one, a threshold on the outer flank of each edge peak. The floor level $S_\text{floor}$ is the mean of the pixels in the middle half of the space; the level of each edge peak is the mean of the three pixels around its maximum; the threshold is half-way between them; and the edge is the point where the profile, followed outwards from the peak, first falls below the threshold, interpolated linearly between pixels. The measured width is the distance between the two edges found.</p>
<p>A rule reads a width, but not necessarily the true one. With a vanishingly small probe and no spread of the signal, the outer flanks are the bottom corners of the line, and the rule finds {{num:cd_sharp}} nm against the bottom width {{num:cd_bottom}} nm (check C7). With the default blur the flanks move outwards and the rule reads {{num:d_cdm}} nm for a line whose true CD is 20 nm: a bias of {{num:d_bias}} nm, made of the sidewall's projection (the bottom is wider than the middle) and above all of the blur, which moves the half-height point of each outer flank outwards by about one $\sigma_1$. The fin-like line of Example 7.3 reads {{num:fin_bias}} nm too wide, {{num:fin_bias_pct}} % of its width. Such a bias is not an error of the tool but a property of the method; real tools calibrate it away against a reference measurement (cross-section electron microscopy or atomic force microscopy) for each kind of pattern. What cannot be calibrated away is the scatter from one measurement to the next.</p>
'''})

S.append({'id': 'precision', 'title': 'The precision of a width', 'html': r'''
<p>Each pixel of the averaged profile carries the variance {{eq:var7}} divided by the number of lines averaged, $N$. The measured width is a function of all pixel values, $\mathrm{CD}_m=f(S_1,\dots,S_n)$; to first order in the noise its variance is</p>
$$ \sigma_\mathrm{CD}^2=\sum_i\left(\frac{\partial f}{\partial S_i}\right)^2\frac{\operatorname{Var}N_i}{N} , \label{prop7} $$
<p>where the derivatives tell how much the found width moves when one pixel goes up by one count. Many of them are zero: only the pixels at the two threshold crossings, those that set the peak levels and those of the floor take part. Near a crossing the derivative is $1/|S'|$, the inverse slope of the profile there, so steep edges give precise widths. The module takes the derivatives by perturbing each pixel of the noise-free profile and running the rule again.</p>
<p>Error propagation is only first order. To check it, the module also repeats the whole measurement 4000 times on noisy profiles and takes the standard deviation of the widths found (about 1 % statistical error). At the default the two give {{num:d_sig}} and {{num:d_sigmc}} nm; at five settings where the edges stand well out of the floor they agree within 20 % (check C6). The differences come from steps the linear theory cannot see: noise makes the maximum of a sharp edge peak jump between neighbouring pixels, which moves the threshold, and the crossing can move from one pair of pixels to the next. Where the edge contrast is low the two part more, in either direction: for the blunt probe of Example 7.4 the propagation gives {{num:bl_sig}} nm and the Monte Carlo {{num:bl_sigmc}} nm. Below 5 % contrast the module stops, because the rule then finds no stable edges.</p>
<p>Every term in {{eq:prop7}} scales as $1/(\bar nN)$, so</p>
$$ \sigma_\mathrm{CD}\propto\frac{1}{\sqrt{I_p\,t_d\,N}} , \label{law7} $$
<p>the $1/\sqrt N$ law of counting statistics (check C5 finds the slope {{num:slope_t}} against the dwell time). Precision is bought with electrons, and electrons cost time and dose.</p>
<div class="pbox"><span class="pbox__t">Key result · precision against time and dose</span><p>At a fixed pixel size and pattern, the scatter of a measured width falls as the inverse square root of the number of electrons used, $\sigma_\mathrm{CD}\propto(I_pt_dN)^{-1/2}$. Halving it needs four times the electrons. Through the dwell time or the current that is four times the dose on each pixel; through more lines it is four times the scan time at the same dose, because each line falls on fresh wafer.</p></div>
<div class="pbox pbox--ex"><span class="pbox__t">Example 7.2 · ten times the dwell</span>
<p>At 1 µs per pixel instead of 100 ns, $\sigma_\mathrm{CD}$ falls from {{num:d_sig}} to {{num:t10_sig}} nm, a factor {{num:t10_ratio}}, close to $\sqrt{10}$; one line's SNR rises to {{num:t10_snr}}. The dose rises to {{num:t10_dose}} µC cm<sup>−2</sup> and the measurements per hour fall to {{num:t10_mph}}.</p></div>
<div class="pbox pbox--ex"><span class="pbox__t">Example 7.3 · a fin-like line</span>
<p>A taller, narrower line with vertical walls (15 nm wide, 50 nm high) has brighter edges, by {{eq:excess7}}: one line's SNR is {{num:fin_snr}}, the width reads {{num:fin_cdm}} nm, and $\sigma_\mathrm{CD}=$ {{num:fin_sig}} nm.</p></div>
<div class="pbox pbox--ex"><span class="pbox__t">Example 7.4 · a blunter probe</span>
<p>A probe of 15 nm instead of chapter 5's {{num:c5_dp}} nm, at the same current, softens the edges: the default line then reads {{num:bl_cdm}} nm (a bias of {{num:bl_bias}} nm against {{num:d_bias}} nm) and its scatter grows from {{num:d_sig}} to {{num:bl_sig}} nm. The bias changes little, because the neighbours' edges already set it; the precision suffers most.</p></div>
'''})

S.append({'id': 'throughput', 'title': 'Measurements per hour', 'html': r'''
<p>One image of 512 by 512 pixels at 100 ns per pixel takes {{num:d_tframe}} ms. A measurement site also needs a stage move, focusing and pattern recognition, which we lump into an overhead $t_\mathrm{ov}$; we assume 1 s, not a vendor's number. For a square image of $N$ lines of $N$ pixels each (the lines averaged are the rows of the image), the rate is then</p>
$$ \dot N_m=\frac{1}{N^2t_d+t_\mathrm{ov}} , \label{mph7} $$
<p>{{num:d_mph}} per hour at the default, of which the scan itself would allow {{num:d_mph_noov}}. The overhead dominates, so a faster scan alone gains little; what pays is measuring many features in one image.</p>
<p>Applied Materials states that its PROVision 10 makes "up to 100 million accurate, actionable measurements per hour" with a cold-field-emission column (product page, as above). We cannot check that claim and do not model that tool. As arithmetic only: 100 million per hour is one measurement every {{num:amat_us}} µs. In the time of one default image, {{num:d_tframe}} ms, that is {{num:amat_per_image}} measurements, which is possible only if each image yields hundreds of widths at once, many lines in a large field, read by software in parallel. Our single-line model counts one width per image, so its rate and the claim measure different things.</p>
'''})

S.append({'id': 'checks', 'title': 'Checks, hand-over and limits', 'html': r'''
<p>The checks of this chapter, run by <code>derive/ch07.py</code>:</p>
''' + checks_table() + r'''
<p>The browser module <code>physics/ch07.js</code> and <code>ref/ch07.py</code> run the same profile, rule and Monte Carlo with the same random numbers; they agree to about $10^{-10}$ (parity check).</p>
<p><b>What chapter 8 receives.</b> The precision $\sigma_\mathrm{CD}$, the bias of the rule, the dose and the measurements per hour, as functions of every input of chapters 2 to 7.</p>
<p><b>What the model leaves out.</b> A three-dimensional simulation of the electrons in the actual line (the secant law and two Gaussian blurs replace it). The roughness of real line edges, which makes the width vary along the line; averaging 512 lines then measures the mean width, and the scatter of the width along the line is a property of the sample, not noise. Charging, which at low voltage changes the contrast of insulating lines. Shrinkage of resist under the dose of Example 7.1. Detector physics: energy filtering, the geometry of in-lens and side detectors, the analogue noise of the detector chain, and backscattered-electron contrast that depends on the slope. Edge physics beyond the secant law: the law fails near grazing incidence, secondaries escape through two faces near a corner (the edge effect), the trench walls shadow the detector, and line and substrate of different materials give different yields. Smarter rules (fitting a model profile, as real tools do), which are more precise than a threshold. The Gaussian approximation of the noise in the Monte Carlo, which needs many counts per averaged pixel.</p>
<div class="pbox pbox--ex"><span class="pbox__t">Problems</span><ol>
<li>Show that for a threshold crossing on a straight flank of slope $S'$, with noise $\sigma_S$ at the crossing and a fixed threshold, the edge scatters by $\sigma_S/|S'|$, so a width with two such edges by $\sqrt2\,\sigma_S/|S'|$. The module gives less at the default; explain the two effects that move it, one downwards (interpolation between two pixels averages their noise) and one upwards (the threshold itself is set from noisy pixels).</li>
<li>From {{eq:law7}} and {{eq:mph7}}, show that at a required $\sigma_\mathrm{CD}$ the product $t_dN$ is fixed, so the time per site is $N\cdot(t_dN)+t_\mathrm{ov}$, smallest for the fewest lines with the longest dwell. Name two things that stop a real tool from going to that limit.</li>
<li>With the simulation, find the probe current at which $\sigma_\mathrm{CD}$ reaches 0.1 nm at the default settings with the probe size held fixed, and the dose that costs. Why would the answer be larger in a real column (chapter 5)?</li>
</ol></div>
<p><b>Sources.</b> Applied Materials, PROVision 10 product page, <a href="https://www.appliedmaterials.com/us/en/product-library/provision-10-ebeam-metrology.html">appliedmaterials.com</a>, read 9 November 2026 (claims quoted, nothing modelled on them). M. Abramowitz, I. A. Stegun, <em>Handbook of Mathematical Functions</em> (1964), formula 7.1.26 for the error function. The yields and the escape depth come from chapter 6 and its sources (Joy 1991; Lin and Joy 2005). The secant law and the threshold rule are standard; we did not take them from a particular book, and the model built from them is ours.</p>
'''})

CH = {
    'title': 'Detect and measure',
    'lead': 'The probe is scanned across a pattern of lines, and a width is read from the electrons that come back. We build the expected profile from the secant law and the blurs of chapters 5 and 6, add the shot noise of the beam and the randomness of the secondary yield, read the width with a threshold rule, and find how its scatter depends on current, time and dose, checked by error propagation and by Monte Carlo.',
    'sections': S,
    'figures': {'edge': {'svg': SVG_EDGE, 'caption': 'Why edges are bright (sketch): the beam crosses the thin escape layer (rose) at a slant on a steep wall, on a path longer by 1/cos θ, and frees more secondary electrons that can get out.'}},
    'numbers': NUMS,
    'literals': LITERALS,
    'sim': {'module': 'ch07', 'title': 'Line profile, noise and width'},
}

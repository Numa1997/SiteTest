"""The Electron Beam, from Tip to Measurement · text/ch08.py · chapter 8, The whole machine.

Written by the finisher (9 November 2026). Format: eb_lib.py (the dict CH). Numbers: data/ch08/derive_results.json, written by derive/ch08.py
from the page's own modules run in Node (derive/ch08_probe.cjs). Chapter 8 has no Python twin (PLAN.md section 4); its checks compare the
chain with the separate chapters instead.
"""
import html
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
EB = os.path.abspath(os.path.join(HERE, '..'))
DER = json.load(open(os.path.join(EB, 'data', 'ch08', 'derive_results.json'), encoding='utf-8'))
DN = DER['numbers']
O = DN['o']
NUMS = {}


def ex(name, expr, of=None, scale=1, sig=3):
    NUMS[name] = {'expr': expr, 'of': dict(of or {}), 'scale': scale, 'sig': sig}


def const(name, value, sig=3):
    ex(name, repr(float(value)), {}, 1, sig)


IN = ['r_t', 'V_ex', 'p', 'V_land', 'I_p', 'WD', 'a_lens', 't_d', 'N_px', 'eta_c']
INNAME = ['tip radius', 'extraction voltage', 'gun pressure', 'landing voltage', 'probe current asked', 'working distance',
          'lens half-width', 'dwell time', 'lines averaged', 'collection fraction']
OUT = ['probe d<sub>p</sub>', 'current I', 'precision σ<sub>CD</sub>', 'rate']
S = DN['sens']
sens = lambda o, i: S[o * 10 + i]
for o, on in enumerate(('dp', 'I', 'cd', 'mph')):
    for i, k in enumerate(IN):
        const('s_%s_%s' % (on, k), sens(o, i), sig=2)
const('o_dp', O['d_p'] * 1e9, sig=3)
const('o_aopt', O['alpha_opt'] * 1e3, sig=3)
const('o_cd', O['sigma_CD'] * 1e9, sig=2)
const('o_cdm', O['CD_meas'] * 1e9, sig=3)
const('o_mph', O['MPH'] * 3600, sig=2)
const('o_dose', O['dose'] * 100, sig=2)
const('o_delta', O['delta_SE'], sig=2)
const('o_fcore', O['f_core'] * 100, sig=2)
const('tol_dp', O['tol_dp_sd'] * 1e9, sig=2)
const('tol_p95', O['tol_cd_p95'] * 1e9, sig=2)
const('tol_yield', O['tol_yield'] * 100, sig=2)
TE = DN['tol_each']
const('te_rt_yield', TE['tol_rt']['yield'] * 100, sig=2)
const('te_rt_p95', TE['tol_rt']['cd_p95'] * 1e9, sig=2)
const('te_NI_dp', TE['tol_NI']['dp_sd'] * 1e9, sig=2)
const('te_rt_dp', TE['tol_rt']['dp_sd'] * 1e9, sig=2)
const('te_z_dp', TE['tol_z']['dp_sd'] * 1e9, sig=1)
const('te_NI_p95', TE['tol_NI']['cd_p95'] * 1e9, sig=2)
const('def_dz', DN['defocus'][0]['dz'] * 1e9, sig=3)
# the process window: grid values
PW = DN['pwin']
NPW = 14
V = lambda i: 500 * 10 ** (i / (NPW - 1))
I = lambda j: 1e-12 * 1000 ** (j / (NPW - 1))
pw = lambda i, j: PW[NPW * i + j]
for tag, (i, j) in {'ll': (0, 0), 'lh': (0, 13), 'hl': (13, 0), 'hh': (13, 13)}.items():
    const('pw_' + tag, pw(i, j) * 1e9, sig=2)
import math as _m
const('tol_se', 100 * _m.sqrt(O['tol_yield'] * (1 - O['tol_yield']) / 300), sig=1)
const('I_drop_pct', 100 * (1 - 1.01 ** S[10 + 0]), sig=2)
const('dp_V', DN['sens'][3], sig=3)
ex('I_dose', '3.0*1e-18/1e-7*1e12', {}, sig=2)

LITERALS = {
    '0.25 nm': 'the assumed precision spec', '0.20 nm': 'the default precision, rounded', 'some 20 %': '3 % times the sensitivity, rounded in words', '2 draws in 300': 'from check W4', 'three spreads': 'the grid half-width', 'about 8 V': 'one step of the extraction slider, rounded', '0.757 ± 0.009': 'chapter 6 run fresh at 800 V, from check W2', '32': 'square root of 1000, rounded', '−3/4': 'the exponent of the law', '+1/2': 'an exponent bound', 'one per cent': 'the change of the sensitivities, in words',
    '0.5 and 30 kV': 'the range of chapter 6\'s stored runs', '10^{-5}': 'the assumed drift of the excitation', 'at 1 pA': 'a corner of the map, a given', 'at 1 nA': 'a corner of the map, a given', 'at 5 kV': 'a corner of the map, a given',
    'Example 8.1': 'the number of a worked example', 'Example 8.2': 'the number of a worked example', 'Example 8.3': 'the number of a worked example',
    '1 %': 'the size of the change in the sensitivities, a choice', '±1 %': 'the size of the change in the sensitivities, a choice', '3 %': 'the assumed spread of the tip radius',
    '10⁻⁵': 'the assumed drift of the excitation', '20 nm': 'the assumed wafer height error', '0.15 nm': 'the assumed precision spec', '300 µC cm⁻²': 'the assumed dose limit',
    '300': 'the number of tolerance samples', '14': 'the size of the process-window grid', '0.5 to 5 kV': 'the voltage range of the map', '1 pA to 1 nA': 'the current range of the map',
    '800 V': 'the default landing voltage, a given', '10 pA': 'the default current, a given', '5 × 5': 'the size of the source grid', 'W1': 'check label', 'W5': 'check label',
    'one in a hundred': 'the same 1 % in words', '0.5': 'the ln-pressure spread, a given', 'Fig. 5': 'figure number in Bronsgeest et al.', '20 nA': 'Bronsgeest et al.\'s limit, quoted',
    'ten inputs': 'count of the table columns', 'four outputs': 'count of the table rows', 'fifteen to sixteen times': 'the rounded sensitivities in words', 'some 15 %': 'the rounded sensitivity in words', 'three times': 'the dose limit over the default, rounded', '1 nm pixels': 'the pixel size, a given', '100 ns': 'the dwell time, a given', '512': 'lines, a given',
}


def checks_table():
    rows = ''.join('<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (c['id'], html.escape(c['title']), ('recorded' if c.get('record') else 'pass') if c['ok'] else 'FAIL', html.escape(c['detail']))
                   for c in DER['checks'])
    return '<div class="ptab-wrap"><table class="ptab ptab--checks"><thead><tr><th>check</th><th>what is verified</th><th>result</th><th>detail</th></tr></thead><tbody>%s</tbody></table></div>' % rows


def sens_table():
    head = ''.join('<th>%s</th>' % h for h in OUT)
    rows = ''
    for i, nm in enumerate(INNAME):
        cells = ''.join('<td>{{num:s_%s_%s}}</td>' % (on, IN[i]) for on in ('dp', 'I', 'cd', 'mph'))
        rows += '<tr><td>%s</td>%s</tr>' % (html.escape(nm), cells)
    return '<div class="ptab-wrap"><table class="ptab"><thead><tr><th>a change of 1 %% in</th>%s</tr></thead><tbody>%s</tbody></table></div>' % (head, rows)


S_ = []
S_.append({'id': 'picture', 'title': 'One chain from tip to number', 'html': r'''
<p>Each chapter so far answered one question with the others held fixed. A machine is more like a long train of gears: a small slip at the first gear is passed on, magnified or damped, to the last. A real column is one chain: the tip sets the brightness and the energy spread, the lens sets the aberrations, together they set the probe, the landing voltage sets what the electrons do in the wafer, and all of it decides how precisely a width can be measured and how fast. Turn one knob and everything downstream moves. This chapter connects the chain and asks three questions of it: which inputs matter most, how much the ordinary wobbles of a real machine spread the result, and which settings meet a specification at all.</p>
<p>The simulation at the end of this chapter is the whole machine. Its sliders are the inputs of the earlier chapters, and its numbers come from their own modules, called in a chain: chapter 2 gives the brightness $B_r$, the FW50 energy spread $\Delta E_{50}$ and the virtual source size $d_v$; chapter 4 gives $C_s$ and $C_c$ for the lens geometry; chapter 5 gives the smallest probe and its angle, because the aperture is always set to the best angle $\alpha_\mathrm{opt}$; chapter 6 gives the yields and the spread of the signal; chapter 7 gives the precision $\sigma_\mathrm{CD}$, the dose and the rate. Only chapter 6 is not rerun: its Monte Carlo takes up to a second per setting, so the chain reads the stored runs behind chapter 6's figures (2000 electrons per point between 0.5 and 30 kV) and interpolates between them.</p>
<div class="pbox pbox--ex"><span class="pbox__t">Example 8.1 · the default machine</span>
<p>Chapter 2's cold tip, chapter 4's lens, landing at 800 V on silicon with 10 pA: the best angle is {{num:o_aopt}} mrad and the probe {{num:o_dp}} nm. The secondary yield is {{num:o_delta}}, {{num:o_fcore}} % of it in the sharp core. A 20 nm line, imaged with 100 ns per pixel and averaged over 512 lines, reads {{num:o_cdm}} nm with $\sigma_\mathrm{CD}=$ {{num:o_cd}} nm, at a dose of {{num:o_dose}} µC cm<sup>−2</sup> and {{num:o_mph}} measurements per hour. These numbers equal those of the separate chapters with the same inputs (check W1); the yield comes from the stored runs of chapter 6, {{num:o_delta}} against 0.757 ± 0.009 from a fresh run at 800 V, within the statistics of both (check W2).</p></div>
'''})

S_.append({'id': 'sensitivity', 'title': 'Which inputs matter: the sensitivity table', 'html': r'''
<p>A good way to see what matters is to change one input by one per cent and watch each output. The ratio of the relative changes,</p>
$$ S_{yx}=\frac{x}{y}\frac{\partial y}{\partial x}=\frac{\partial\ln y}{\partial\ln x} , \label{sens8} $$
<p>is the <em>normalised sensitivity</em>. It has no unit, so inputs of different kinds can be compared on one scale: $S=-0.5$ means that one per cent more of the input gives half a per cent less of the output, and $S=16$ means sixteen per cent more. For a power law $y\propto x^n$ it is just the exponent $n$. The module takes it by central differences of $\pm1$ % in each input; the table holds the values at the defaults, ten inputs against four outputs ($d_p$ the probe, $I$ the probe current with the condensers left at their setting, $\sigma_\mathrm{CD}$ the precision, rate the measurements per hour).</p>
''' + sens_table() + r'''
<p>Three things stand out. First, the source. With the optics fixed, the probe current answers the tip radius with {{num:s_I_r_t}} and the extraction voltage with {{num:s_I_V_ex}}: the field at the apex is $V_\mathrm{ex}/(k r_t)$, and field emission rises with the field almost as steeply as an exponential (chapter 2). A tip that blunts by one per cent loses {{num:I_drop_pct}} % of its current. It follows that such a gun is best run with its emission current held constant by adjusting the extraction voltage as the tip changes (an inference from this table; this project has no source describing a particular gun's control), and that the tip's history matters. Through the number of electrons, the same sensitivity reaches the precision: $\sigma_\mathrm{CD}$ answers the tip radius with {{num:s_cd_r_t}}.</p>
<p>Second, the precision follows the counting law of chapter 7 exactly: $-0.5$ for the dwell time and for the number of lines (check W5), {{num:s_cd_I_p}} for the current, slightly above $-0.5$ because a larger current also enlarges the probe a little. The landing voltage enters with {{num:s_cd_V_land}}: a higher voltage widens the core and the halo of the secondary signal and lowers the yield, which together soften the edges, while the probe shrinks and pulls the other way. The probe itself answers the landing voltage with {{num:dp_V}}, which is the $V^{-3/4}$ law of a balance of diffraction against chromatic aberration: the diameter goes as $\sqrt{AK}$ with $A\propto\lambda\propto V^{-1/2}$ and $K\propto\Delta E/V$ (chapter 5; check W6). It answers the working distance with {{num:s_dp_WD}}. The collection fraction enters the precision with {{num:s_cd_eta_c}}, smaller in size than the $-0.5$ of a pure count, because the noise of the counts includes the random yield of secondaries, which collecting more of them does not reduce.</p>
<p>Third, the rate hardly moves at all ({{num:s_mph_t_d}} for the dwell time): the one-second overhead per site dominates, as chapter 7 found. A tool that is to be fast must cut the overhead or measure many features per image, not scan faster.</p>
<div class="pbox"><span class="pbox__t">Key result · what matters most</span><p>At the default settings the probe current is by far the most sensitive quantity of the machine: in per cent it changes fifteen to sixteen times as much as the tip radius or the extraction voltage; through the number of electrons it carries that sensitivity into the precision of every measurement. Everything else follows power laws with modest exponents, between −3/4 (the probe against the landing voltage) and +1/2.</p></div>
'''})

S_.append({'id': 'tolerance', 'title': 'Wobbles of a real machine: the tolerance Monte Carlo', 'html': r'''
<p>No two tips are alike, a lens current drifts, the gun pressure varies, and the wafer surface is never exactly where the focus was set. A tolerance Monte Carlo draws such errors at random, runs the chain for each draw, and looks at the spread of the results. We draw four errors, with spreads that are assumptions of this page, not data of any tool: the tip radius with a relative spread of 3 % (its logarithm normal), the natural logarithm of the gun pressure with a spread of 0.5, the objective excitation with a relative drift $\varepsilon$ of standard deviation $s_I=10^{-5}$, and the wafer height after focusing with 20 nm. They are independent; there are 300 draws with fixed random numbers. The gun is taken without any current control, so a blunter tip gives less current: this shows the raw sensitivity, the worst case. And the aperture stays at the angle that is best for the nominal machine, as a real aperture would, rather than being re-optimised for each draw.</p>
<p>Two of the errors act through the source: the tip radius and the pressure change $B_r$, $\Delta E_{50}$ and $d_v$. The column was set up for the asked current with chapter 2's default tip; with the same acceptance of the column, the current then scales as $B_rd_v^2$ (brightness times source area, which is the angular intensity) and the source image as $d_v$. The same rule makes the current readout move when the tip or extraction sliders move. Chapter 2 is too slow to run 300 times, so the module runs it on a 5 × 5 grid in tip radius and pressure, spanning three spreads each way, and interpolates (check W4: within 1 % of direct runs; the 2 draws in 300 that fall outside the grid are held at its edge). The other two errors defocus the probe. The lens strength goes as $B^2/V^*$, so an excitation off by the fraction $\varepsilon$ acts like a voltage off by $-2\varepsilon$, and since $C_c$ is the focus shift per relative change of $V^*$, the focus moves by</p>
$$ \Delta z=2C_c\,\varepsilon , \label{defocus8} $$
<p>{{num:def_dz}} nm for $\varepsilon=10^{-5}$; chapter 4's own ray tracer confirms it (check W3). A wafer height error adds to $\Delta z$. A beam of half-angle $\alpha$ defocused by $\Delta z$ is a uniform disc of radius $\alpha|\Delta z|$, whose FW50 diameter is $\sqrt2\,\alpha|\Delta z|$; we add it to the probe in quadrature, a simple rule that is exact for neither shape.</p>
<div class="pbox pbox--ex"><span class="pbox__t">Example 8.2 · the default machine, wobbling</span>
<p>Over the 300 draws the probe varies by {{num:tol_dp}} nm (standard deviation), and the precision is worse than {{num:tol_p95}} nm in 5 % of them. With a specification of 0.25 nm, {{num:tol_yield}} % of the draws meet it; with 300 draws that share carries a statistical error of about {{num:tol_se}} percentage points. Switched on one at a time, the tip radius alone lets {{num:te_rt_yield}} % meet it, through the current, and the other three alone let all draws meet it. The lens drift spreads the probe most, by {{num:te_NI_dp}} nm, but costs little precision; the tip spreads it by {{num:te_rt_dp}} nm, the wafer height by {{num:te_z_dp}} nm; the pressure, at 10<sup>−9</sup> Pa an hour after cleaning, does nearly nothing. The result agrees with the sensitivity table: a 3 % spread of the radius times the table's {{num:s_cd_r_t}} spreads the precision by some 20 %, enough to push the upper tail of a 0.20 nm machine past 0.25 nm.</p></div>
<p>Alignment, which the plan of this project listed, is not among the errors: a beam off the lens axis suffers coma, and we have no source for the coma coefficient of this lens, so we leave it out rather than invent one.</p>
'''})

S_.append({'id': 'window', 'title': 'Which settings work: the measurement window', 'html': r'''
<p>Lithographers draw a <em>process window</em>: the region of focus and exposure in which a pattern prints within specification. A metrology tool has the same kind of map. The left panel of the simulation shows $\sigma_\mathrm{CD}$ over landing voltage (0.5 to 5 kV) and probe current (1 pA to 1 nA), 14 by 14 points, each with the aperture at its best angle. The wine region meets the precision specification, and the darker the grey, the further a point misses it; the dashed line is the dose limit, above which one image would put more than the allowed charge on the wafer (we assume 300 µC cm<sup>−2</sup>; resists differ widely in how much they tolerate).</p>
<div class="pbox pbox--ex"><span class="pbox__t">Example 8.3 · reading the window</span>
<p>At 0.5 kV the precision goes from {{num:pw_ll}} nm at 1 pA to {{num:pw_lh}} nm at 1 nA; at 5 kV from {{num:pw_hl}} to {{num:pw_hh}} nm. Over the map, more current always helps, though over a factor of a thousand in current the precision improves by less than the $\sqrt{1000}\approx32$ of pure counting, because the best probe grows with the current. At a given current, low voltage is better: the core and halo of the secondary signal widen and the yield falls as the voltage rises (chapter 6), and the edges soften. The window is bounded above by the dose: at 100 ns per pixel and 1 nm pixels the limit lies at {{num:I_dose}} pA, only three times the default current. So at these settings the window is a strip of low voltage between about the default current and the dose limit. The map leaves out further reasons for low voltage, charging of insulators and damage to resist, and the reason for high voltage, seeing buried layers; chapter 7's flat silicon line contains none of them.</p></div>
'''})

S_.append({'id': 'checks', 'title': 'Checks and limits', 'html': r'''
<p>The checks of this chapter, run by <code>derive/ch08.py</code> through the page's own modules in Node:</p>
''' + checks_table() + r'''
<p>Chapter 8 has no Python twin: it adds no physics of its own beyond {{eq:defocus8}} and the current at fixed condensers, and every module it calls is checked against its twin in its own chapter.</p>
<p><b>What the model leaves out.</b> Everything the earlier chapters leave out, and in addition: the correlations between errors (a blunter tip delivers the same current from a larger area at a lower field, and so with a narrower energy spread), alignment and coma, drift of the gun's own optics, and the coupling of landing voltage and lens (the lens here is computed without a retarding field, chapter 4). The spreads of the tolerance Monte Carlo and the two specifications are assumptions, chosen to show the method; a real tolerance budget starts from measured spreads of a real tool.</p>
<div class="pbox pbox--ex"><span class="pbox__t">Problems</span><ol>
<li>From {{eq:sens8}}, show that for $y=x_1^ax_2^b$ the sensitivities are $a$ and $b$, and that the relative error of $y$ from small independent relative errors $s_1$, $s_2$ is $\sqrt{a^2s_1^2+b^2s_2^2}$. Use the table to estimate the spread of the probe current from a 3 % spread of the tip radius, and compare with what the Monte Carlo would give if the current were the only thing that changed.</li>
<li>Show that a uniform disc of radius $\rho$ holds half its current inside the radius $\rho/\sqrt2$, which is where the factor $\sqrt2$ in the defocus blur comes from.</li>
<li>In the simulation, find the extraction voltage that restores the default current after the tip radius has grown by 5 %, as near as the slider allows (one step is about 8 V), and check your answer against the sensitivity table.</li>
</ol></div>
'''})

CH = {
    'title': 'The whole machine',
    'lead': 'Chapters 2 to 7 connected into one chain, from the tip to the precision of a width and the measurements per hour. We ask which inputs matter most (a table of normalised sensitivities), how much the ordinary wobbles of a real machine spread the result (a tolerance Monte Carlo), and which settings meet a specification (a measurement window), and we check the chain against the separate chapters.',
    'sections': S_,
    'figures': {},
    'numbers': NUMS,
    'literals': LITERALS,
    'sim': {'module': 'ch08', 'title': 'The whole machine'},
    'css': '#sim-ch08 .eb-sim__grid{grid-template-columns:minmax(0,1fr)}#sim-ch08 .eb-sim__ctls{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:12px 20px}',
}

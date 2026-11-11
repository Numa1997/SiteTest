"""Project 07 · The Electron Beam · chapter 2, the source: the lecture note.

    from text import ch02;  ch02.build()  ->  {'id', 'title', 'html', 'css', 'sim_js_files', 'numbers'}

html is the chapter body in the house note format (section.psec, .pfig, .pbox, .ptab, .prefs): mathematics as \\( … \\) and \\[ … \\] with
\\tag{2.n} numbers, for KaTeX (rendered at build time by the page builder). Every number quoted in the text is read from
data/ch02/derive_results.json (derive/ch02.py) or computed here with ref/ch02.py; none is typed in by hand except inputs
(the presets and the published values, each with its source beside it).
"""
import json, math, os, re, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
EB = os.path.abspath(os.path.join(HERE, '..'))
import importlib.util
_spec = importlib.util.spec_from_file_location('eb_ref_ch02', os.path.join(EB, 'ref', 'ch02.py'))   # same stem as this file: load by path
R = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(R)
_fks = importlib.util.spec_from_file_location('eb_figkit', os.path.join(EB, 'figkit.py'))                # figure layout helpers
FK = importlib.util.module_from_spec(_fks); _fks.loader.exec_module(FK)

eV = R.eV
INK, WINE, TAN, MUTED, ROSE = '#1c1518', '#7a1f2b', '#7a4b12', '#8b8079', '#e2a2aa'

# ================================================================================================ numbers
def load_numbers():
    with open(os.path.join(EB, 'data', 'ch02', 'derive_results.json')) as fh:
        D = json.load(fh)
    N = dict(D['numbers'])
    N['_checks'] = D['checks']
    N['_summary'] = D['summary']
    # ---- the example tip of section 2.1 and the working point of the chapter
    r, V, k, phi_eV = 50e-9, 1000.0, 5.0, 4.5
    phi = phi_eV * eV
    F0 = V / (k * r)
    N.update(ex_r_nm=r * 1e9, ex_V=V, ex_k=k, ex_phi=phi_eV, ex_F_Vnm=F0 * 1e-9, ex_F=F0)
    N['wall_nm'] = phi_eV / (F0 * 1e-9)                                  # phi/(eF) in nm, F in V/nm
    N['F_atom'] = R.e / (4 * math.pi * R.eps0 * (0.529177210903e-10) ** 2)   # field of a proton at one Bohr radius, V/m (a0 CODATA 2018)
    N['F_over_atom'] = N['F_atom'] / F0
    N['f_ex'] = R.scaled_field(F0, phi)
    N['F_R_Vnm'] = R.reference_field(phi) * 1e-9
    N['dphi_ex_eV'] = R.schottky_lowering(F0) / eV
    N['top_ex_eV'] = phi_eV - N['dphi_ex_eV']
    s = math.sqrt(1 - N['f_ex'])
    N['x1_nm'] = phi * (1 - s) / (2 * R.e * F0) * 1e9
    N['x2_nm'] = phi * (1 + s) / (2 * R.e * F0) * 1e9
    N['v_ex'] = R.v_exact(N['f_ex']); N['vF_ex'] = R.v_forbes(N['f_ex']); N['t_ex'] = R.t_forbes(N['f_ex'])
    N['G_ex'] = R.barrier_G(F0, phi)
    N['G_tri_ex'] = R.bFN * phi ** 1.5 / F0
    N['D_ex'] = math.exp(-N['G_ex'])
    N['a_FN'] = R.e ** 2 / (8 * math.pi * R.h) * 1e6                  # µA eV V^-2: J = (a/φ[eV]) F^2 with e^3/(8πh φ[J]) = e^2/(8πh) / φ[eV]
    N['b_FN'] = N['b_eV_Vnm']
    N['J_FN0_ex'] = R.j_fn(F0, phi, 0.0)
    N['J_FN300_ex'] = R.j_fn(F0, phi, 300.0)
    mdl = R.emission_model(F0, phi, 300.0)
    N['J_model_ex'] = mdl['J']; N['d_ex_eV'] = mdl['d'] / eV; N['Tcorr_ex'] = N['J_FN300_ex'] / N['J_FN0_ex']
    N['Tcorr_pct'] = (N['Tcorr_ex'] - 1) * 100
    N['G_F_ex'] = R.bFN * phi ** 1.5 * N['vF_ex'] / F0                    # finisher: exponent with Forbes' v, as the formula is evaluated
    N['d_tri_eV'] = R.hbar * R.e * F0 / (2 * math.sqrt(2 * R.me * phi)) / eV   # finisher: triangular-barrier d, no t(f)
    N['top_f08_eV'] = (1 - math.sqrt(0.8)) * phi_eV                        # finisher: barrier top above the Fermi level at f = 0.8
    N['ay_r_k5'] = None                                                    # filled in finish_numbers once the fit is loaded                          # finisher: the size of the correction, computed
    N['t_des_700'] = 1 / R.k_des(1.9, 700.0)                              # finisher: residence time at 700 K with the assumed E_d, nu0
    N['x_ex'] = math.pi * R.kB * 300 / mdl['d']
    N['kT300_eV'] = R.kB * 300 / eV
    N['I_ex'] = R.tip_current(V, r, k, phi, 300.0)
    N['A_eff_ex_nm2'] = N['I_ex'] / N['J_model_ex'] * 1e18
    N['sites_ex'] = N['A_eff_ex_nm2'] * 1e-18 * 1e19
    # ---- sensitivity (elasticities) of the FN current density at the working point
    dl = 1e-4
    N['el_F'] = (math.log(R.j_fn(F0 * (1 + dl), phi, 0)) - math.log(R.j_fn(F0 * (1 - dl), phi, 0))) / (math.log(1 + dl) - math.log(1 - dl))
    N['el_phi'] = (math.log(R.j_fn(F0, phi * (1 + dl), 0)) - math.log(R.j_fn(F0, phi * (1 - dl), 0))) / (math.log(1 + dl) - math.log(1 - dl))
    N['J_ratio_dphi01'] = R.j_fn(F0, phi + 0.1 * eV, 0) / R.j_fn(F0, phi, 0)
    N['J_ratio_dphi10'] = R.j_fn(F0, phi + 1.0 * eV, 0) / R.j_fn(F0, phi, 0)
    N['J_ratio_F10'] = R.j_fn(F0 * 1.1, phi, 0) / R.j_fn(F0, phi, 0)
    # ---- Schottky preset numbers
    S = N['preset_schottky']
    FS = S['V'] / (S['k'] * S['r'])
    N['sch_F_Vnm'] = FS * 1e-9
    N['sch_dphi_eV'] = R.schottky_lowering(FS) / eV
    N['sch_kT_eV'] = R.kB * S['T'] / eV
    N['sch_J_RS'] = R.j_schottky(FS, S['T'], S['phi'])
    N['sch_J_R'] = R.j_richardson(S['T'], S['phi'])
    mS = R.emission_model(FS, S['phi'], S['T'])
    N['sch_J_model'] = mS['J']; N['sch_top_eV'] = mS['top'] / eV; N['sch_peak_eV'] = mS['peak'] / eV
    N['sch_f'] = mS['f']
    # ---- time to a monolayer
    N['Ns'] = 1.0e19
    N['Ns_lattice'] = N['Ns_W_lattice']
    # ---- flux and times
    N['flux_H2_1e-8'] = R.hk_flux(1e-8, 300, 2.016)
    # ---- Cho et al. 2014 compared with the rate equation (theta* = 0.1: a 10 % drop of the probe current)
    th_star = 0.1
    cho = N['cho']
    for c in cho:
        c['Phi'] = R.hk_flux(c['p'], 300, 2.016)
        c['dose'] = c['Phi'] * c['tau90_min'] * 60
        c['s_eff'] = th_star * N['Ns'] / c['dose']
    N['cho_s_mean'] = float(np.mean([c['s_eff'] for c in cho]))
    N['cho_ptau_spread'] = (max(c['p_tau'] for c in cho) - min(c['p_tau'] for c in cho)) / np.mean([c['p_tau'] for c in cho])
    # ---- the default contamination model
    N['model'] = dict(Ns=1e19, s=N['cho_s_mean'], kappa=1.0, Ed=1.9, nu0=1e13, Tflash=1000.0, tflash=5.0, thr=0.7, dphi_ads=1.0)
    M = N['model']
    N['rho_ads'] = R.covered_ratio(F0, phi, M['dphi_ads'])
    N['kd_RT'] = R.k_des(M['Ed'], 300.0)
    N['kd_700'] = R.k_des(M['Ed'], 700.0)
    N['kd_flash'] = R.k_des(M['Ed'], M['Tflash'])
    N['kd_2000'] = R.k_des(M['Ed'], 2000.0)
    # time between flashes against pressure (H2), threshold I/I0 = 0.7 with the patch model, rho = rho_ads
    rows = []
    for pPa in (1e-7, 1e-8, 1e-9, 1e-10, 1e-11):
        a = M['kappa'] * M['s'] * R.hk_flux(pPa, 300, 2.016) / M['Ns']
        # current ratio = (1-th) + th rho < thr  ->  th* = (1-thr)/(1-rho)
        ths = (1 - M['thr']) / (1 - N['rho_ads'])
        rows.append(dict(p=pPa, t_s=R.time_to_coverage(ths, a, N['kd_RT']), th_star=ths))
    N['flash_scan'] = rows
    # ---- hand-over presets, as the page quotes them
    N['ho_cfe'] = N['handover_cfe']; N['ho_sch'] = N['handover_schottky']
    # ---- single-atom estimate: footprint 1/sites
    N['one_atom'] = 1.0 / N['sites_ex']
    # ---- FN slope of Ayari and the zeta that follows from it
    ay = N['ayari']
    f_mid = 0.5 * (ay['fits']['4.5']['f_lo'] + ay['fits']['4.5']['f_hi'])
    N['ay_s_mid'] = 1 - f_mid / 6
    bphi = N['b_eV_Vnm'] * 4.5 ** 1.5                                        # V/nm
    N['ay_bphi'] = bphi
    N['ay_zeta_slope_nm'] = abs(ay['fn_slope_V']) / (bphi * N['ay_s_mid'])
    N['ay_resid_max_pct'] = ay['resid_max'] * 100
    N['ay_resid_rms_pct'] = ay['resid_rms'] * 100
    return N


# ================================================================================================ svg plots (house chart style)
def nice_ticks(lo, hi, n=5):
    span = hi - lo
    raw = span / n
    mag = 10 ** math.floor(math.log10(raw))
    for m in (1, 2, 2.5, 5, 10):
        if raw <= m * mag:
            step = m * mag
            break
    t = math.ceil(lo / step - 1e-9) * step
    out = []
    while t <= hi + 1e-9 * span:
        out.append(round(t, 12))
        t += step
    return out


SUP = str.maketrans('-0123456789', '⁻⁰¹²³⁴⁵⁶⁷⁸⁹')


def fmt_tick(v):
    if v == 0:
        return '0'
    if abs(v) >= 1e5 or abs(v) < 1e-3:
        e = int(math.floor(math.log10(abs(v)) + 1e-9)); m = v / 10 ** e
        return (('' if abs(m - 1) < 1e-9 else f'{m:g}×') + '10' + str(e).translate(SUP))
    return f'{v:g}'


class Plot:
    """The house chart, drawn twice (figkit.dual): wide at W user units, narrow at figkit.NARROW_W. Curves, dots and reference lines are
    kept as data and drawn for each width; the legend sits below the plot, the y label is turned when it fits beside the plot and is
    written above it otherwise; notes go to the free spot nearest to where they are asked (figkit.Layout), with a leader if they move."""
    _n = 0

    def __init__(s, xlim, ylim, xlabel, ylabel, W=640, H=360, xlog=False, ylog=False, ml=64, mr=16, mt=14, mb=48, xticks=None, yticks=None, legend_xy=None):
        Plot._n += 1
        s.id = f'p{Plot._n}'
        s.W, s.H, s.xlim, s.ylim, s.xlog, s.ylog = W, H, xlim, ylim, xlog, ylog
        s.ml, s.mr, s.mt, s.mb = ml, mr, mt, mb
        s.xlabel, s.ylabel = xlabel, ylabel
        s.xt = xticks; s.yt = yticks
        s.items = []; s.notes = []; s.legend = []

    def _fx(s, x, x0, pw):
        a, b = s.xlim
        if s.xlog: x, a, b = math.log10(x), math.log10(a), math.log10(b)
        return x0 + (x - a) / (b - a) * pw

    def _fy(s, y, y0, ph):
        a, b = s.ylim
        if s.ylog: y, a, b = math.log10(y), math.log10(a), math.log10(b)
        return y0 + ph - (y - a) / (b - a) * ph

    def line(s, xs, ys, color=INK, w=2, dash=None, label=None, opacity=1):
        pts = [(x, y) for x, y in zip(xs, ys) if x is not None and y is not None and np.isfinite(x) and np.isfinite(y)
               and (not s.ylog or y > 0) and (not s.xlog or x > 0)]
        if not pts: return
        s.items.append(('line', pts, color, w, dash, opacity))
        if label: s.legend.append((label, color, dash, 'line'))

    def dots(s, xs, ys, color=WINE, r=3.2, label=None, hollow=False):
        s.items.append(('dots', [(x, y) for x, y in zip(xs, ys) if not (s.ylog and y <= 0)], color, r, hollow))
        if label: s.legend.append((label, color, None, 'dot'))

    def vline(s, x, color=MUTED, dash='4 4', label=None, textpos=None):
        s.items.append(('vline', x, color, dash))
        if label: s.notes.append((x, None, label, 'lbl', 'start'))

    def hline(s, y, color=MUTED, dash='4 4'):
        s.items.append(('hline', y, color, dash))

    def text(s, x, y, txt, cls='lbl', raw=False, anchor='start'):
        s.notes.append((x, y, txt, cls, anchor))

    def _ticks(s, given, lim, log):
        if given is not None: return given
        if log: return [10 ** e for e in range(math.ceil(math.log10(lim[0])), math.floor(math.log10(lim[1])) + 1)]
        return nice_ticks(*lim)

    def _draw(s, title, narrow):
        W = FK.NARROW_W if narrow else s.W
        xt, yt = s._ticks(s.xt, s.xlim, s.xlog), s._ticks(s.yt, s.ylim, s.ylog)
        tw = max(FK.width(fmt_tick(v), 'tick') for v in yt)
        ph = 190 if narrow else s.H - s.mt - s.mb
        rot = not narrow and FK.width(s.ylabel) <= ph - 8
        ytop = [] if rot else FK.wrap(s.ylabel, W - 8)
        ml = max(s.ml, tw + 30) if rot else tw + 12
        mt = s.mt if rot else 16 * len(ytop) + 10
        mr = 10 if narrow else s.mr
        pw = W - ml - mr
        X = lambda x: s._fx(x, ml, pw)
        Y = lambda y: s._fy(y, mt, ph)
        bot = mt + ph
        cid = s.id + ('n' if narrow else 'w') + 'c'
        L = FK.Layout(W, bot + 400)
        out = [f'<defs><clipPath id="{cid}"><rect x="{ml}" y="{mt}" width="{pw}" height="{ph}"/></clipPath></defs>']
        # y ticks, thinned until they are 15 units apart
        ys = [v for v in yt]
        while len(ys) > 2 and min(abs(Y(a) - Y(b)) for a, b in zip(ys, ys[1:])) < 15: ys = ys[::2]
        for v in yt:
            y = Y(v)
            out.append(f'<line x1="{ml}" x2="{ml + pw}" y1="{y:.1f}" y2="{y:.1f}" stroke="#ece5d8" stroke-width="1" data-nocollide=""/>')
            if v in ys: out.append(f'<text x="{ml - 7}" y="{y + 4:.1f}" class="tick" text-anchor="end">{fmt_tick(v)}</text>')
        # x ticks, thinned until their labels stand 8 units apart
        xs = list(xt)
        gap = lambda a, b: (X(b) - FK.width(fmt_tick(b), 'tick') / 2) - (X(a) + FK.width(fmt_tick(a), 'tick') / 2)
        while len(xs) > 2 and min(gap(a, b) for a, b in zip(xs, xs[1:])) < 8: xs = xs[::2]
        for v in xt:
            x = X(v)
            out.append(f'<line x1="{x:.1f}" x2="{x:.1f}" y1="{mt}" y2="{bot}" stroke="#ece5d8" stroke-width="1" data-nocollide=""/>')
            if v in xs:
                w2 = FK.width(fmt_tick(v), 'tick') / 2
                an, tx = ('end', W - 2) if x + w2 > W - 2 else ('start', 2) if x - w2 < 2 else ('middle', x)
                out.append(f'<text x="{tx:.1f}" y="{bot + 16}" class="tick" text-anchor="{an}">{fmt_tick(v)}</text>')
        out.append(f'<rect x="{ml}" y="{mt}" width="{pw}" height="{ph}" fill="none" stroke="#cdc1ae" data-nocollide=""/>')
        # the data
        for it in s.items:
            if it[0] == 'line':
                _, pts, color, w, dash, op = it
                P = [(X(x), Y(y)) for x, y in pts]
                L.line([(min(max(px, ml - 5), ml + pw + 5), min(max(py, mt - 5), bot + 5)) for px, py in P], w / 2 + 0.5)
                d = ' '.join(f'{"M" if i == 0 else "L"}{px:.1f} {py:.1f}' for i, (px, py) in enumerate(P))
                out.append(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{w}" stroke-linejoin="round"' + (f' stroke-dasharray="{dash}"' if dash else '') + (f' opacity="{op}"' if op != 1 else '') + f' clip-path="url(#{cid})"/>')
            elif it[0] == 'dots':
                _, pts, color, r, hollow = it
                for x, y in pts:
                    L.circle(X(x), Y(y), r + 0.7)
                    out.append(f'<circle cx="{X(x):.1f}" cy="{Y(y):.1f}" r="{r}" fill="{"#fff" if hollow else color}" stroke="{color}" stroke-width="1.4" clip-path="url(#{cid})"/>')
            elif it[0] == 'vline':
                _, x, color, dash = it
                L.line([(X(x), mt), (X(x), bot)], 0.8)
                out.append(f'<line x1="{X(x):.1f}" x2="{X(x):.1f}" y1="{mt}" y2="{bot}" stroke="{color}" stroke-width="1.2" stroke-dasharray="{dash}"/>')
            elif it[0] == 'hline':
                _, y, color, dash = it
                L.line([(ml, Y(y)), (ml + pw, Y(y))], 0.8)
                out.append(f'<line x1="{ml}" x2="{ml + pw}" y1="{Y(y):.1f}" y2="{Y(y):.1f}" stroke="{color}" stroke-width="1.2" stroke-dasharray="{dash}"/>')
        # notes inside the plot, where no curve passes
        region = (ml + 3, mt + 3, ml + pw - 3, bot - 3)
        for x, y, txt, cls, anchor in s.notes:
            px, py = (X(x) + 4, mt + 15) if y is None else (X(x), Y(y))
            kw = dict(region=region, radius=70 if narrow else 90, anchors=[anchor, 'end' if anchor != 'end' else 'start'])
            got = L.place(txt, px, py, cls, anchor, force=False, **kw)
            if got is None and '<' not in txt:          # no room on one line: two lines
                got = L.place(FK.wrap(txt, max(FK.width(txt) * 0.55, 60)), px, py, cls, anchor, **kw)
            out.append(got or L.place(txt, px, py, cls, anchor, **kw))
        # axis labels and legend below the plot
        yb = bot + 16 + 20
        for ln in FK.wrap(s.xlabel, W - 8):
            out.append(f'<text x="{(ml + W - mr) / 2 if FK.width(ln) < pw else W / 2:.0f}" y="{yb}" class="lbl" text-anchor="middle">{ln}</text>')
            yb += 16
        if rot:
            out.append(f'<text transform="translate(14 {mt + ph / 2:.0f}) rotate(-90)" class="lbl" text-anchor="middle">{s.ylabel}</text>')
        else:
            for i, ln in enumerate(ytop):
                out.append(f'<text x="4" y="{14 + 16 * i}" class="lbl">{ln}</text>')
        lx, ly = (4 if narrow else ml), yb + 6
        for lab, col, dash, kind in s.legend:
            wl = 30 + FK.width(lab)
            if lx + wl > W - 2 and lx > (4 if narrow else ml):
                lx, ly = (4 if narrow else ml), ly + 18
            if kind == 'line':
                out.append(f'<line x1="{lx}" x2="{lx + 22}" y1="{ly - 4}" y2="{ly - 4}" stroke="{col}" stroke-width="2.2"' + (f' stroke-dasharray="{dash}"' if dash else '') + '/>')
            else:
                out.append(f'<circle cx="{lx + 11}" cy="{ly - 4}" r="3.4" fill="{col}"/>')
            out.append(f'<text x="{lx + 28}" y="{ly}" class="lbl">{lab}</text>')
            lx += wl + 16
        H = (ly + 10) if s.legend else (yb - 6)
        return (f'<svg viewBox="0 0 {W} {H:.0f}" role="img" aria-label="{title}" xmlns="http://www.w3.org/2000/svg"><rect width="{W}" height="{H:.0f}" fill="#fff"/>'
                + ''.join(out) + '</svg>')

    def svg(s, title):
        return FK.dual(s._draw(title, False), s._draw(title, True))


# ================================================================================================ numbering, formatting
LABELS = {}
COUNT = {'eq': 0, 'fig': 0, 'ex': 0, 'sec': 0}
_pass = {'n': 0}


def eq(label, tex):
    COUNT['eq'] += 1
    LABELS['eq:' + label] = COUNT['eq']
    return '\\[' + tex.strip() + f' \\tag{{2.{COUNT["eq"]}}}\\]'


def fig(label, inner, caption, wide=False):
    COUNT['fig'] += 1
    LABELS['fig:' + label] = COUNT['fig']
    return (f'<figure class="pfig" id="fig-{label}"><div class="pfig__plate">{inner}</div>'
            f'<figcaption><span class="pfig__n">Figure 2.{COUNT["fig"]}</span>{caption}</figcaption></figure>')


def ex(label, title, body):
    COUNT['ex'] += 1
    LABELS['ex:' + label] = COUNT['ex']
    return f'<div class="pbox pbox--ex" id="ex-{label}"><span class="pbox__t">Example 2.{COUNT["ex"]} · {title}</span>{body}</div>'


def key(title, body):
    return f'<div class="pbox"><span class="pbox__t">Key result · {title}</span>{body}</div>'


def sec(label, title, body):
    COUNT['sec'] += 1
    LABELS['sec:' + label] = COUNT['sec']
    return f'<section class="psec" id="sec-{label}"><h3><span class="psec__n">2.{COUNT["sec"]}</span>{title}</h3>{body}</section>'


STAR = '<span class="star">★</span>'


def _num(v, f_, in_math):
    if f_.startswith('sci') or f_.startswith('tex'):
        d = int(f_[3:] or 2)
        e = int(math.floor(math.log10(abs(v)))); mnt = v / 10 ** e
        if round(mnt, d) >= 10: mnt /= 10; e += 1
        if f_.startswith('tex') or in_math: return f'{mnt:.{d}f}\\times10^{{{e}}}'
        return f'{mnt:.{d}f}×10<sup>{e}</sup>'.replace('-', '−')
    out = format(v, f_)
    return out if in_math else out.replace('-', '−')


def fill(s, N, SPECIAL=None):
    """@key|fmt@ -> number (key path with '/'); @eq:label@ -> (2.n); @fig:label@; @sec:label@; @ex:label@; @NAME@ -> SPECIAL[NAME];
    scientific notation is written as HTML outside \\( \\) and as TeX inside."""
    SPECIAL = SPECIAL or {}
    pieces = re.split(r'(\\\(.*?\\\)|\\\[.*?\\\])', s, flags=re.S)
    res = []
    for idx, seg in enumerate(pieces):
        in_math = idx % 2 == 1
        def rep(m):
            t = m.group(1)
            if t.startswith('eq:'): return f'(2.{LABELS.get(t, "?")})'
            if t.startswith('fig:'): return f'Figure 2.{LABELS.get(t, "?")}'
            if t.startswith('sec:'): return f'section 2.{LABELS.get(t, "?")}'
            if t.startswith('ex:'): return f'Example 2.{LABELS.get(t, "?")}'
            if t in SPECIAL: return SPECIAL[t]
            k, _, f_ = t.partition('|')
            v = N
            for part in k.split('/'):
                v = v[int(part)] if isinstance(v, list) else v[part]
            return str(v) if not f_ else _num(v, f_, in_math)
        res.append(re.sub(r'@([^@\s]+)@', rep, seg))
    return ''.join(res)


# ================================================================================================ figures
def _tip_svg(N, narrow):
    """Figure 2.1 in drawing units of the wide figure (640 x 330), mapped by P(); labels placed by figkit where nothing is drawn."""
    k, ox, oy, W = (0.44, 6, 46, FK.NARROW_W) if narrow else (1.0, 0, 26, 640)
    P = lambda x, y: (ox + k * x, oy + k * y)
    L = FK.Layout(W, 600)
    s = []
    # anode plate with a hole
    for y0 in (20, 192):
        x, y = P(500, y0)
        s.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{14 * k:.1f}" height="{118 * k:.1f}" fill="#d9d0c2" stroke="{INK}" stroke-width="1.2"/>')
        L.rect(x, y, 14 * k, 118 * k)
    # shank and apex
    apex = (330, 165); rad = 22
    cx = apex[0] - rad
    a1, a2, a3 = P(30, 133), P(apex[0] - rad * 0.92, apex[1] - rad * 0.4), P(apex[0] - rad * 0.92, apex[1] + rad * 0.4)
    a4 = P(30, 197)
    s.append(f'<path d="M {a1[0]:.1f} {a1[1]:.1f} L {a2[0]:.1f} {a2[1]:.1f} A {rad * k:.1f} {rad * k:.1f} 0 0 1 {a3[0]:.1f} {a3[1]:.1f} L {a4[0]:.1f} {a4[1]:.1f} Z" fill="#efe4c8" stroke="{INK}" stroke-width="1.6"/>')
    L.line([a1, a2, P(apex[0], apex[1]), a3, a4, a1], 1)
    c = P(cx, apex[1])
    s.append(f'<circle cx="{c[0]:.1f}" cy="{c[1]:.1f}" r="{rad * k:.1f}" fill="none" stroke="{WINE}" stroke-width="1.2" stroke-dasharray="3 3"/>')
    L.circle(c[0], c[1], rad * k)
    e = P(cx - rad * 0.7, apex[1] - rad * 0.7)
    s.append(f'<line x1="{c[0]:.1f}" y1="{c[1]:.1f}" x2="{e[0]:.1f}" y2="{e[1]:.1f}" stroke="{WINE}" stroke-width="1.6"/>')
    s.append(f'<circle cx="{c[0]:.1f}" cy="{c[1]:.1f}" r="2.5" fill="{WINE}"/>')
    L.line([c, e], 1)
    # field lines: from cap to the anode
    for a in (-1.0, -0.6, -0.25, 0.0, 0.25, 0.6, 1.0):
        th = a * 0.9
        x0 = cx + rad * math.cos(th); y0 = apex[1] + rad * math.sin(th)
        x1, y1 = 500, apex[1] + a * 95
        c1 = (x0 + 70 * math.cos(th) + 40, y0 + 70 * math.sin(th)); c2 = (x1 - 90, y1)
        q = [P(*p) for p in ((x0, y0), c1, c2, (x1, y1))]
        s.append(f'<path d="M {q[0][0]:.1f} {q[0][1]:.1f} C {q[1][0]:.1f} {q[1][1]:.1f}, {q[2][0]:.1f} {q[2][1]:.1f}, {q[3][0]:.1f} {q[3][1]:.1f}" fill="none" stroke="#b79aa0" stroke-width="1" stroke-dasharray="5 3"/>')
        L.line([tuple((1 - t) ** 3 * q[0][i] + 3 * (1 - t) ** 2 * t * q[1][i] + 3 * (1 - t) * t * t * q[2][i] + t ** 3 * q[3][i] for i in (0, 1)) for t in [j / 40 for j in range(41)]], 0.8)
    # emitted electrons
    for a, xx in ((-0.1, 372), (0.1, 372), (-0.08, 430), (0.08, 430), (0.0, 470)):
        d = P(xx, apex[1] + a * 100)
        s.append(f'<circle cx="{d[0]:.1f}" cy="{d[1]:.1f}" r="{3.2 if not narrow else 2.6}" fill="{WINE}"/>')
        L.circle(d[0], d[1], 3.5)
    m0, m1 = P(360, 165), P(492, 165)
    mid = 'arn' if narrow else 'arw'
    s.append(f'<path d="M {m0[0]:.1f} {m0[1]:.1f} L {m1[0]:.1f} {m1[1]:.1f}" stroke="{WINE}" stroke-width="1.4" fill="none" marker-end="url(#{mid})"/>')
    s.append(f'<defs><marker id="{mid}" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0 L8 4 L0 8 Z" fill="{WINE}"/></marker></defs>')
    L.line([m0, m1], 1.5)
    # labels: wanted spot, the feature a leader points to
    lab = lambda txt, at, anchor='middle', to=None, **kw: s.append(L.place(txt, *P(*at), 'lbl', anchor, lead_to=P(*to) if to else None, **kw))
    lab('anode, 0 V', (507, -6), 'middle', prefer=(0, -1))
    lab(['electrons', 'leave the', 'apex'] if narrow else ['electrons leave', 'the apex'], (522, 150), 'start', prefer=(1, 0))
    lab('field lines end on the anode', (270, 50), 'middle', (430, 82), prefer=(0, -1))
    lab('shank', (205, 230), 'middle', (205, 176), prefer=(0, 1))
    lab('tip at −V', (30, 230), 'start', (40, 190), prefer=(0, 1))
    lab('apex: sphere of radius <tspan class="m">r</tspan>', (cx, apex[1] + rad + 26), 'middle', (cx, apex[1] + rad), prefer=(0, 1))
    s.append(L.place('<tspan class="m">r</tspan>', e[0] - 4, e[1] - 4, 'lbl', 'end', radius=20, leader=False))
    bottom = max([b[3] for b in L.boxes] + [P(0, 310)[1]]) + 8
    note = f'not to scale: with <tspan class="m">r</tspan> = {N["ex_r_nm"]:.0f} nm the apex is far smaller than the gap'
    if narrow:
        s.append(FK.text(4, bottom + 14, [f'not to scale: with <tspan class="m">r</tspan> = {N["ex_r_nm"]:.0f} nm the apex', 'is far smaller than the gap']))
        H = bottom + 14 + 16 + 10
    else:
        s.append(FK.text(30, bottom + 16, note))
        H = bottom + 26
    return (f'<svg viewBox="0 0 {W} {H:.0f}" role="img" aria-label="A sharp tungsten tip facing an extraction anode with a hole" xmlns="http://www.w3.org/2000/svg">'
            f'<rect width="{W}" height="{H:.0f}" fill="#fff"/>' + ''.join(s) + '</svg>')


def fig_tip(N):
    return FK.dual(_tip_svg(N, False), _tip_svg(N, True))


def fig_barrier(N):
    phi = 4.5 * eV
    P = Plot((0, 1.6), (-1.5, 5.2), 'distance from the surface x (nm)', 'electron potential energy U relative to the Fermi level (eV)', W=640, H=380, legend_xy=(330, 150))
    xs = np.linspace(0.02, 1.6, 320)
    Q0 = R.Q0
    for Fnm, col, dash, lab in ((0, MUTED, '2 3', 'F = 0 (image only)'), (2, TAN, None, 'F = 2 V/nm'), (4, WINE, None, 'F = 4 V/nm'), (6, INK, None, 'F = 6 V/nm')):
        Fv = Fnm * 1e9
        ys = (phi - R.e * Fv * xs * 1e-9 - Q0 / (xs * 1e-9)) / eV
        P.line(xs, ys, col, 2.2, dash, lab)
    P.hline(0, INK, '6 4')
    P.text(1.58, 0.15, 'Fermi level, U = 0', 'lbl', anchor='end')
    P.hline(4.5, MUTED, '2 4')
    P.text(1.58, 4.65, 'φ = 4.5 eV, the zero-field wall', 'lbl', anchor='end')
    # roots and top at 4 V/nm
    P.dots([N['x1_nm'], N['x2_nm']], [0, 0], WINE, 4.5)
    xm = math.sqrt(R.Q0 / (R.e * 4e9)) * 1e9
    P.dots([xm], [N['top_ex_eV']], INK, 4.5, hollow=True)
    P.text(xm + 0.03, N['top_ex_eV'] + 0.28, f'top {N["top_ex_eV"]:.2f} eV', 'lbl')
    P.text(N['x2_nm'] + 0.04, 0.4, f'x₂ = {N["x2_nm"]:.2f} nm', 'lbl')
    return P.svg('Potential energy of an electron outside a tungsten surface for four fields')


def fig_vt(N):
    P = Plot((0, 1), (0, 1.15), 'scaled field f = F/F_R', 'v(f), t(f)', W=640, H=340, yticks=[0, 0.25, 0.5, 0.75, 1.0])
    fs = np.linspace(0.002, 0.999, 300)
    P.line(fs, [R.v_exact(f) for f in fs], INK, 2.4, None, 'v(f), quadrature (exact)')
    P.line(fs, [R.v_forbes(f) for f in fs], WINE, 2, '6 4', 'v(f) ≈ 1 − f + (f/6) ln f')
    P.line(fs, [R.t_forbes(f) for f in fs], TAN, 2, None, 't(f) ≈ 1 + f/9 − (f/18) ln f')
    P.vline(N['f_ex'], MUTED, '3 4')
    P.text(N['f_ex'] + 0.01, 0.07, f'f = {N["f_ex"]:.3f} (F = 4 V/nm, φ = 4.5 eV)', 'lbl')
    return P.svg('v(f) and t(f)')


_cache = {}


def regimes_data():
    if 'reg' in _cache: return _cache['reg']
    Ts = np.array([300, 500, 800, 1100, 1400, 1700, 2000, 2300, 2600, 3000], float)
    out = {}
    for Fnm in (0.5, 2.0, 4.0):
        out[Fnm] = [R.emission_model(Fnm * 1e9, 4.5 * eV, T)['J'] for T in Ts]
    out['T'] = Ts
    out['regime'] = {Fnm: [R.emission_model(Fnm * 1e9, 4.5 * eV, T)['regime'] for T in (300, 1400, 2600)] for Fnm in (0.5, 2.0, 4.0)}
    _cache['reg'] = out
    return out


def fig_regimes(N):
    D = regimes_data()
    P = Plot((300, 3000), (1e-6, 1e11), 'temperature T (K)', 'current density J (A/m²)', W=640, H=380, ylog=True, xticks=[500, 1000, 1500, 2000, 2500, 3000])
    for Fnm, col, dash in ((4.0, WINE, None), (2.0, TAN, None), (0.5, INK, None)):
        P.line(D['T'], D[Fnm], col, 2.3, dash, f'F = {Fnm:g} V/nm')
        P.dots(D['T'], D[Fnm], col, 2.8)
    Ts = np.linspace(1500, 3000, 40)
    P.line(Ts, [R.j_richardson(T, 4.5 * eV) for T in Ts], MUTED, 1.6, '2 4', 'Richardson–Dushman, F = 0')
    return P.svg('Current density against temperature for three fields, work function 4.5 eV')


def fig_energy(N):
    mC = R.emission_model(N['ex_F'], 4.5 * eV, 300.0)
    S = N['preset_schottky']
    mS = R.emission_model(S['V'] / (S['k'] * S['r']), S['phi'], S['T'])
    P = Plot((-1.2, 1.2), (0, 1.08), 'energy relative to the peak (eV)', 'distribution P(ε), peak = 1', W=640, H=340)
    for m, col, lab in ((mC, WINE, f'cold field emission, 300 K: ΔE = {mC["fwhm"] / eV:.2f} eV'), (mS, INK, f'Schottky emission, 1800 K: ΔE = {mS["fwhm"] / eV:.2f} eV')):
        x = (m['w'] - m['peak']) / eV
        P.line(x[::6], (m['P'] / m['P'].max())[::6], col, 2.3, None, lab)
    P.hline(0.5, MUTED, '3 4')
    P.text(1.18, 0.53, 'half maximum', 'lbl', anchor='end')
    return P.svg('Total energy distributions of a cold field emitter and a Schottky emitter')


def fig_data(N):
    ay = N['ayari']; V = np.array(ay['V']); I = np.array(ay['I_nA'])
    f45 = ay['fits']['4.5']; z = f45['zeta_nm'] * 1e-9; A = f45['A_nm2'] * 1e-18
    x = 1000 / V
    y = np.log(I / V ** 2)
    P1 = Plot((0.58, 0.80), (-27, -20), '1000 / V   (1/kV)', 'ln( I / V² )   (I in nA, V in V)', W=340, H=300, ml=56, xticks=[0.6, 0.65, 0.7, 0.75, 0.8], yticks=[-27, -25, -23, -21], legend_xy=(70, 262))
    xs = np.linspace(0.6, 0.78, 60)
    ym = [math.log(A * R.j_fn(1000 / xx / z, 4.5 * eV, 300) * 1e9 / (1000 / xx) ** 2) for xx in xs]
    P1.line(xs, ym, WINE, 2.2, None, 'model, φ = 4.5 eV, 300 K')
    P1.line(xs, [ay['fn_slope_V'] * xx / 1000 + ay['fn_intercept'] for xx in xs], INK, 1.6, '5 4', 'straight line (authors)')
    P1.dots(x, y, INK, 2.9, 'measured, run 4, down')
    res = np.array([r for _, r in ay['resid_vs_V']]) * 100
    P2 = Plot((1280, 1650), (-8, 8), 'voltage V (V)', 'ln I measured − ln I model  (%)', W=340, H=300, ml=56, xticks=[1300, 1400, 1500, 1600], yticks=[-6, -3, 0, 3, 6])
    P2.hline(0, INK, '4 4')
    P2.dots(V, res, WINE, 3)
    return '<div class="pfig__row">' + P1.svg('Fowler-Nordheim plot of the tungsten tip data') + P2.svg('Residuals of the model fit') + '</div>'


def fig_cho(N):
    P = Plot((3e-10, 1e-7), (3, 3000), 'residual pressure p (Pa)', 'time to a 10 % drop of the probe current τ₉₀ (min)', W=640, H=340, xlog=True, ylog=True)
    M = N['model']
    ps = np.logspace(math.log10(3e-10), -7, 40)
    th_star = 0.1
    P.line(ps, [th_star * M['Ns'] / (N['cho_s_mean'] * R.hk_flux(p, 300, 2.016)) / 60 for p in ps], WINE, 2.3, None, f'model: τ = θ* Nₛ /(κs Φ), s = {N["cho_s_mean"]:.2f}')
    P.dots([c['p'] for c in N['cho']], [c['tau90_min'] for c in N['cho']], INK, 5, 'measured, W(310), Cho 2014')
    return P.svg('Time to a ten percent drop of the emission current against pressure')


def fig_cycle(N):
    M = N['model']
    rho = N['rho_ads']
    c = R.cycle(1e-8, 300, 2.016, M['Ns'], M['s'], M['kappa'], M['Ed'], 300.0, M['Tflash'], M['tflash'], M['thr'], 0.0, rho, 6 * 3600.0, 1.0)
    t = np.array(c['t']) / 60
    P = Plot((0, 360), (0, 1.05), 'time (min)', 'coverage θ and current ratio I/I₀', W=640, H=340, xticks=[0, 60, 120, 180, 240, 300, 360], yticks=[0, 0.25, 0.5, 0.75, 1.0], legend_xy=(380, 150))
    ratio = [r_ if np.isfinite(r_) else None for r_ in c['ratio']]
    P.line(t, c['theta'], INK, 2, None, 'coverage θ')
    P.line(t, ratio, WINE, 2.3, None, 'current ratio I/I₀')
    P.hline(M['thr'], MUTED, '3 4')
    for tf in c['flashes']:
        P.vline(tf / 60, ROSE, '2 3')
    N['cycle_nflash'] = len(c['flashes']); N['cycle_first_flash_min'] = c['flashes'][0] / 60
    N['cycle_gap_min'] = (c['flashes'][1] - c['flashes'][0]) / 60 if len(c['flashes']) > 1 else float('nan')
    return P.svg('Coverage and current against time with flashes')


# ================================================================================================ more numbers used by the sections
def more_numbers(N):
    eVv = eV
    for Fnm in (3, 4, 5):
        N[f'fwhm_{Fnm}'] = R.emission_model(Fnm * 1e9, 4.5 * eVv, 300)['fwhm'] / eVv
        N[f'Br_{Fnm}'] = R.emission_model(Fnm * 1e9, 4.5 * eVv, 300)['B_r']
        N[f'J_{Fnm}'] = R.emission_model(Fnm * 1e9, 4.5 * eVv, 300)['J']
    mC = R.emission_model(N['ex_F'], 4.5 * eVv, 300.0)
    N['meanEt_cfe_eV'] = mC['mean_et'] / eVv
    N['peak_cfe_eV'] = mC['peak'] / eVv
    S = N['preset_schottky']; FS = S['V'] / (S['k'] * S['r'])
    mS = R.emission_model(FS, S['phi'], S['T'])
    N['sch_fwhm_eV'] = mS['fwhm'] / eVv; N['sch_meanEt_eV'] = mS['mean_et'] / eVv; N['sch_Br'] = mS['B_r']
    N['sch_d_eV'] = mS['d'] / eVv
    N['sch_gain_RS'] = N['sch_J_RS'] / N['sch_J_R']
    N['sch_ratio_model_RS'] = N['sch_J_model'] / N['sch_J_RS']
    N['sch_peak_above_top_eV'] = (mS['peak'] - mS['top']) / eVv
    N['ho_ratio_Br'] = N['ho_cfe']['B_r'] / N['ho_sch']['B_r']
    N['surface_tip_nm2'] = 2 * math.pi * N['ex_r_nm'] ** 2          # hemisphere
    N['frac_emitting'] = N['A_eff_ex_nm2'] / N['surface_tip_nm2']
    N['sin_lambda'] = None
    # problems
    r, V, k = 30e-9, 800.0, 5.0
    N['p1_F'] = V / (k * r) * 1e-9
    N['p1_f'] = R.scaled_field(V / (k * r), 4.5 * eVv)
    N['p1_v'] = R.v_forbes(N['p1_f'])
    N['p1_J'] = R.j_fn(V / (k * r), 4.5 * eVv, 0)
    N['p3_t_CO'] = N['Ns'] / R.hk_flux(1e-7, 300, 28.0)
    N['p3_t_H2'] = N['Ns'] / R.hk_flux(1e-7, 300, 2.016)
    # electron wavelength is chapter 3; the barrier width for Example
    N['two_kappa'] = 2 * math.sqrt(2 * R.me * eVv) / R.hbar * 1e-9          # nm^-1 eV^-1/2
    N['cS_Vnm'] = R.schottky_lowering(1e9) / eVv
    return N


def dur(s):
    if s < 120: return f'{s:.0f} s'
    if s < 7200: return f'{s / 60:.0f} min'
    if s < 172800: return f'{s / 3600:.1f} h'
    return f'{s / 86400:.1f} days'


# ================================================================================================ the sections (text, in the macro syntax of render())
SECTIONS = [
('intro', 'A needle, a wall and a leak', r'''
<p class="psec__lead">Every electron beam in this project starts at a piece of metal. We want to know what that piece of metal has to look like, what is applied to it, and what comes out, in numbers the next chapters can use.</p>

<p>Anyone who has touched a door handle on a dry winter day has met the main idea. The spark jumps from a fingertip and not from the flat of the hand, and a lightning rod is a pointed rod and not a plate. Charge on a conductor crowds where the surface curves sharply, and the electric field next to the surface grows with that crowding. A needle tip is the extreme case: a few tens of nanometres across, it turns a modest voltage into a field that is enormous on the scale of atoms.</p>

<h4><span class="psub__n">2.1.1</span>Work function and the wall</h4>
<p>Inside a metal the conduction electrons fill states up to an energy called the <em>Fermi level</em>. We take that level as the zero of energy in this chapter. An electron at the Fermi level is not free: to take it to rest just outside the surface costs a definite energy, the <em>work function</em> \(\varphi\). Picture a bowl of water: its surface is the Fermi level, and its rim stands \(\varphi\) higher. For clean tungsten we use \(\varphi = @ex_phi|.1f@\ \mathrm{eV}\), the value Dolan and Dyke called "the accepted average value for clean tungsten" in 1954. The electronvolt of chapter 1 is \(1.602\,176\,634\times10^{-19}\) J. We shall treat \(\varphi\) as a parameter that can be changed, because the whole story of this chapter depends on how sensitive the current is to it.</p>

<p>An electron can get over or through the rim in three ways. Heat the metal until enough electrons have the energy to climb it (thermionic emission). Apply a field that lowers the rim a little (Schottky emission). Or apply a field so strong that the rim becomes a thin wall and the electrons tunnel through it (field emission). The cold source that Applied Materials describes publicly for its electron-beam metrology column is of the third kind; the Schottky source of the second kind is its main competitor. The three are one calculation, and we do it once.</p>

<h4><span class="psub__n">2.1.2</span>The field at the apex</h4>
<p>Take a conducting sphere of radius \(r\) carrying charge \(Q\) and held at potential \(V\) relative to far away. Outside it the potential is that of a point charge, \(Q/(4\pi\varepsilon_0\rho)\) at distance \(\rho\) from the centre, so \(V = Q/(4\pi\varepsilon_0 r)\). The field at the surface is \(Q/(4\pi\varepsilon_0 r^2)\), and eliminating \(Q\) gives \(F = V/r\). A real tip is a sphere sitting on a cone or a wire, with an anode at a finite distance, and the shank takes some of the potential drop. This is folded into one dimensionless factor \(k\), of order unity to several, so that</p>
[[EQ apexfield]]F = \frac{V}{k\,r}[[/EQ]]
<p>with \(k=1\) for the isolated sphere. The value \(k=5\) is used for tungsten tips by Chapman (1971) and by Ayari et al. (2023), whose data we use in section 2.9. We take it as an assumption, and the chapter says where it enters.</p>

[[EX tip|The field at a tip]]<p>A tip of radius \(r=@ex_r_nm|.0f@\ \mathrm{nm}\) at \(V=@ex_V|.0f@\ \mathrm{V}\) with \(k=@ex_k|.0f@\) has \(F = @ex_V|.0f@/(@ex_k|.0f@\times @ex_r_nm|.0f@\times10^{-9}) = @ex_F_Vnm|.2f@\times10^{9}\ \mathrm{V/m} = @ex_F_Vnm|.1f@\ \mathrm{V/nm}\). For scale, the field of a proton at one Bohr radius is \(@F_atom|tex2@\ \mathrm{V/m}\), so this is \(1/@F_over_atom|.0f@\) of the field inside a hydrogen atom. It is a field that changes the energy of an electron by \(@ex_F_Vnm|.1f@\) eV over each nanometre. An electron at the Fermi level, in this field, has to climb a wall of height \(\varphi\) that falls by \(eF\) per unit length, which would reach the Fermi level after \(\varphi/(eF) = @wall_nm|.3f@\) nm. That is the thickness of the wall it must tunnel through, a few atomic diameters.</p>[[/EX]]

[[FIG tip|TIPFIG]]A tungsten tip and its surroundings. The apex is a sphere of radius <i>r</i>; a voltage <i>V</i> between tip and anode produces the field lines drawn dashed, which crowd onto the apex. Electrons leave the apex and pass through the hole in the anode.[[/FIG]]

[[KEY the field of a needle]]<p>\(F = V/(k r)\): halving the radius doubles the field at the same voltage. With \(r\) in nanometres and a kilovolt applied, fields of several volts per nanometre are reached.</p>[[/KEY]]
'''),

('barrier', 'The wall an electron sees', r'''
<p class="psec__lead">Outside the metal, an electron feels two things: the applied field, which pulls it away from the surface, and its own image, which pulls it back. We add the two energies.</p>

<h4><span class="psub__n">2.2.1</span>The image force</h4>
<p>Put an electron at distance \(x\) from the plane surface of a conductor. The conduction electrons rearrange until the field just outside the surface is perpendicular to it. For the region outside the metal this arrangement is exactly what a single positive charge \(+e\) at distance \(x\) <em>inside</em> the metal, the mirror image of the electron, would produce. The force on the electron is therefore that of a charge \(+e\) at distance \(2x\):</p>
[[EQ imageforce]]F_{\mathrm{im}}(x) = -\frac{e^{2}}{4\pi\varepsilon_0\,(2x)^{2}} = -\frac{e^{2}}{16\pi\varepsilon_0\,x^{2}}[[/EQ]]
<p>The potential energy is minus the work needed to take the electron from \(x\) out to infinity against this attraction,</p>
[[EQ imageenergy]]U_{\mathrm{im}}(x) = -\int_x^{\infty}\frac{e^{2}}{16\pi\varepsilon_0\,x'^{2}}\,dx' = -\frac{e^{2}}{16\pi\varepsilon_0\,x}[[/EQ]]
<p>(One might expect \(e^2/(8\pi\varepsilon_0 x)\), the energy of the real pair at separation \(2x\). It is twice as large, because as the electron moves away the induced charge in the metal rearranges. Only half of the pair's energy is stored in the field outside the surface. Integrating the force, as above, takes this into account.)</p>

<h4><span class="psub__n">2.2.2</span>The Schottky–Nordheim barrier</h4>
<p>The applied field \(F\), directed so that it pulls electrons out, contributes \(-eFx\). Measuring all energies from the Fermi level, an electron at the Fermi level sees outside the surface</p>
[[EQ barrier]]U(x) = \varphi - eF\,x - \frac{e^{2}}{16\pi\varepsilon_0\,x}[[/EQ]]
<p>This is the Schottky–Nordheim (SN) barrier. For \(F=0\) it is the work function wall rounded off by the image force. For \(F>0\) it falls linearly and is cut by the image term near the surface. Writing \(Q_0 = e^2/(16\pi\varepsilon_0)\), the energy \(U\) is zero where \(eF\,x^2 - \varphi\,x + Q_0 = 0\), that is at</p>
[[EQ roots]]x_{1,2} = \frac{\varphi}{2eF}\Bigl(1 \mp \sqrt{1-f}\Bigr),\qquad f = \frac{4eFQ_0}{\varphi^{2}} = \frac{e^{3}F}{4\pi\varepsilon_0\,\varphi^{2}}[[/EQ]]
<p>The dimensionless number \(f\) is the <em>scaled field</em>. The barrier exists as long as \(f<1\); at \(f=1\) the two roots merge and the top of the barrier touches the Fermi level. The field at which this happens, \(F_R = 4\pi\varepsilon_0\varphi^{2}/e^{3}\), is \(@F_R_Vnm|.2f@\) V/nm for \(\varphi=4.5\) eV, so \(f = F/F_R\). Setting \(dU/dx=0\) gives the top of the barrier at \(x_m=\sqrt{Q_0/(eF)}\), where \(U_{\max} = \varphi - \Delta\varphi\) with the Schottky lowering</p>
[[EQ schottky]]\Delta\varphi = \sqrt{\frac{e^{3}F}{4\pi\varepsilon_0}} = \varphi\sqrt{f}\,,\qquad \Delta\varphi = @cS_Vnm|.4f@\ \mathrm{eV}\times\sqrt{F/(\mathrm{V/nm})}[[/EQ]]
<p>The derivation of \(x_{1,2}\), of \(f\), and of \(\Delta\varphi\) was checked symbolically (checks C1 and C2 in section 2.13).</p>

[[EX barrier|The barrier at F = @ex_F_Vnm|.0f@ V/nm]]<p>Here \(f=@f_ex|.4f@\), the roots are \(x_1 = @x1_nm|.3f@\) nm and \(x_2 = @x2_nm|.3f@\) nm, and the top of the barrier is \(\Delta\varphi = @dphi_ex_eV|.2f@\) eV below the zero-field rim, at @top_ex_eV|.2f@ eV above the Fermi level. A Fermi-level electron meets a barrier \(x_2-x_1 = @x2_nm|.2f@ - @x1_nm|.3f@\approx @barrier_w|.2f@\) nm wide.</p>[[/EX]]

[[FIG barrier|BARRIERFIG]]The potential energy of an electron outside a tungsten surface, equation @eq:barrier@, for four fields. An electron at the Fermi level (dashed line, <i>U</i> = 0) has to get through the region where the curve is above the line. The dots mark the two roots <i>x</i><sub>1</sub> and <i>x</i><sub>2</sub> for 4 V/nm; the open circle is the top of the barrier.[[/FIG]]

<p><strong>Where the model is not trusted.</strong> The image term diverges at the surface. At \(x_1\) of less than a tenth of a nanometre the picture of a smooth classical image charge is no longer meaningful. The standard treatment, which we follow, simply uses the barrier between its two roots. The result depends only on the region \(x_1<x<x_2\), where the barrier is above the electron, and that hides the problem. It is one of the reasons the current in section 2.9 is predicted only to a factor, not to a percent.</p>
'''),

('wkb', 'Leaking through: the WKB transmission', r'''
<p class="psec__lead">A wave that meets a barrier higher than its energy does not stop at the edge. Inside the barrier it dies away exponentially, and what is left at the far side leaves as an electron. We now compute how much is left.</p>

<p>Let an electron approach the surface with energy \(w\) of motion normal to it. We write the time-independent Schrödinger equation for that motion,</p>
[[EQ schrod]]-\frac{\hbar^{2}}{2m}\,\psi''(x) + U(x)\,\psi(x) = w\,\psi(x)[[/EQ]]
<p>In the barrier, \(U>w\), so \(\psi'' = \kappa^{2}\psi\) with \(\kappa(x) = \sqrt{2m\,(U(x)-w)}/\hbar\). If \(\kappa\) were constant the solution that decays towards larger \(x\) would be \(e^{-\kappa x}\). When \(\kappa\) varies slowly, \(|d\kappa/dx|\ll\kappa^{2}\), the WKB approximation replaces \(\kappa x\) by \(\int\kappa\,dx\):</p>
[[EQ wkbpsi]]\psi(x)\approx\psi(x_1)\,\exp\Bigl(-\int_{x_1}^{x}\kappa(x')\,dx'\Bigr)[[/EQ]]
<p>The probability of finding the electron, \(|\psi|^{2}\), falls by the square of that factor between the two turning points \(x_1\) and \(x_2\). The transmission probability is taken as this ratio:</p>
[[EQ Dwkb]]D(w) \approx e^{-G(w)},\qquad G(w) = \frac{2}{\hbar}\int_{x_1}^{x_2}\sqrt{2m\,\bigl(U(x)-w\bigr)}\;dx[[/EQ]]
<p>The approximation fails close to the turning points, where \(\kappa\to0\), so \(D\) is only reliable when \(G\) is large. The prefactor that belongs to the exact solution is dropped. For the barriers that give currents we care about, \(G\) is of order 10 (the exponent in @ex:G@ is @G_ex|.1f@). The missing prefactor is then a factor of order one, absorbed in the uncertainty named in section 2.9. Allaham et al. (2022) give the same step in their equations (3) and (4), with the constant \(2\kappa_e = @two_kappa|.3f@\ \mathrm{eV^{-1/2}\,nm^{-1}}\) which is \(2\sqrt{2m\,(1\,\mathrm{eV})}/\hbar\); we recomputed it.</p>

<h4><span class="psub__n">2.3.1</span>The triangular barrier</h4>
<p>Without the image term the barrier is \(U=\varphi-eFx\), which meets the Fermi level (\(w=0\)) at \(x=\varphi/(eF)\). Then</p>
[[EQ Gtri]]G_{\triangle} = \frac{2}{\hbar}\int_0^{\varphi/eF}\!\!\sqrt{2m(\varphi-eFx)}\,dx = \frac{4\sqrt{2m}}{3\hbar e}\,\frac{\varphi^{3/2}}{F} \equiv b\,\frac{\varphi^{3/2}}{F}[[/EQ]]
<p>The integral is \(\tfrac{2}{3}\varphi^{3/2}/(eF)\) times \(\sqrt{2m}\) times \(2/\hbar\). The constant \(b = 4\sqrt{2m}/(3\hbar e)\) is the second Fowler–Nordheim constant; it equals \(@b_FN|.4f@\ \mathrm{eV^{-3/2}\,V\,nm^{-1}}\) (Forbes quotes 6.830 890; check C3). In words: \(G\) grows as the wall gets higher (\(\varphi^{3/2}\)) and shrinks as the field gets stronger (\(1/F\)). With the example numbers \(G_\triangle = @G_tri_ex|.2f@\).</p>

<h4><span class="psub__n">2.3.2</span>With the image term: the function \(v(f)\) <span class="star">★</span></h4>
<p>With the image term, \(U-w = eF\,(x-x_1)(x_2-x)/x\) between the roots (the roots depend on the energy through \(\varphi-w\) in place of \(\varphi\)). We put \(x = x_1+(x_2-x_1)\sin^{2}\vartheta\) with \(0\le\vartheta\le\pi/2\), so that \((x-x_1)(x_2-x) = \Delta^{2}\sin^{2}\vartheta\cos^{2}\vartheta\), \(dx = 2\Delta\sin\vartheta\cos\vartheta\,d\vartheta\), \(\Delta=x_2-x_1\):</p>
[[EQ Gimage]]G = \frac{2\sqrt{2m}}{\hbar}\sqrt{eF}\int_0^{\pi/2}\frac{2\Delta^{2}\sin^{2}\vartheta\cos^{2}\vartheta}{\sqrt{x_1+\Delta\sin^{2}\vartheta}}\,d\vartheta \equiv b\,\frac{\varphi^{3/2}}{F}\,v(f)[[/EQ]]
<p>which has no singularity and is evaluated by Gauss–Legendre quadrature in <code>ref/ch02.py</code> and <code>physics/ch02.js</code> (48 points for the exponent at a single energy, 64 for \(v(f)\), 24 inside the energy integral of section 2.4). The right-hand side defines \(v(f)\), a correction factor that depends only on \(f\). It equals 1 for \(f\to0\) (no image term) and falls to 0 at \(f=1\), where the barrier has disappeared. In the older literature it is written with the elliptic integrals of Nordheim; Forbes (2006) found that \(v\approx 1-f+\tfrac{1}{6}f\ln f\) is good to 0.0024 everywhere on \(0\le f\le 1\). Our quadrature agrees: the largest difference on a grid of 199 values is @v_max_abs_err|.5f@ (check C7).</p>
[[EQ vF]]v(f)\approx 1 - f + \frac{f}{6}\ln f[[/EQ]]
<p>For the working point, \(v = @v_ex|.4f@\) by quadrature and @vF_ex|.4f@ from the approximation.</p>

[[FIG vt|VTFIG]]The barrier function <i>v</i>(<i>f</i>) computed by quadrature (solid), Forbes&rsquo; approximation (dashed), and the companion function <i>t</i>(<i>f</i>) of section @sec:fn@. Both functions are 1 at <i>f</i> = 0.[[/FIG]]

[[EX G|The transmission at the working point]]<p>\(G = b\varphi^{3/2}v/F = @G_tri_ex|.2f@\times @v_ex|.4f@ = @G_ex|.2f@\) and \(D=e^{-G} = @D_ex|tex2@\). The image force changes \(G\) from @G_tri_ex|.2f@ to @G_ex|.2f@ and therefore multiplies the transmission by \(e^{@G_tri_ex|.2f@-@G_ex|.2f@}=@DG|.0f@\). Of every \(@D_inv|.0f@\) electrons that arrive at the wall one gets out.</p>[[/EX]]
'''),

('supply', 'Counting the electrons that arrive: the supply function', r'''
<p class="psec__lead">The transmission is a probability per electron. To get a current we need to know how many electrons strike the surface per second, with which normal energy, and that is a count in the metal.</p>

<p>We treat the conduction electrons as a gas of free particles with the Fermi–Dirac occupation \(\mathcal F(E) = [1+e^{(E-\mu)/kT}]^{-1}\), with \(\mu=0\) the Fermi level. A momentum cell of size \(d^{3}p\) holds \(2\,d^{3}p/h^{3}\) electron states (the 2 is the spin). Electrons with velocity component \(v_x\) normal to the surface, directed at it, reach unit area of surface per unit time at the rate \(v_x\) times their density. So the current density of electrons that arrive with the momenta in \(d^{3}p\) is</p>
[[EQ arrive]]dJ_{\mathrm{in}} = e\,\frac{2}{h^{3}}\,\mathcal F(E)\,v_x\,d^{3}p[[/EQ]]
<p>Split \(E = w + \varepsilon_t\) into the normal energy \(w=p_x^{2}/2m\) and the transverse energy \(\varepsilon_t = (p_y^{2}+p_z^{2})/2m\). Then \(v_x\,dp_x = dw\), and the transverse momentum element is \(dp_y\,dp_z = \pi\,d(p_t^{2}) = 2\pi m\,d\varepsilon_t\). A fraction \(D(w)\) of what arrives is transmitted. Adding up,</p>
[[EQ Jint]]J = e\int dw\,D(w)\,\frac{4\pi m}{h^{3}}\int_0^{\infty}\mathcal F(w+\varepsilon_t)\,d\varepsilon_t\;=\;e\int N(w)\,D(w)\,dw[[/EQ]]
<p>(spin 2 times \(2\pi m\) gives \(4\pi m\)). The inner integral is elementary, because \(\int_w^\infty\mathcal F\,dE = kT\ln(1+e^{-w/kT})\). It defines the supply function, the number of electrons per unit area, time and energy that arrive with normal energy \(w\):</p>
[[EQ supply]]N(w) = \frac{4\pi m\,kT}{h^{3}}\,\ln\Bigl(1+e^{-w/kT}\Bigr)[[/EQ]]
<p>The check C4 verifies the derivative that defines it. For \(w\ll-kT\), \(N\to 4\pi m\,(-w)/h^{3}\). At low temperature the number of arriving electrons grows linearly with how far below the Fermi level they sit, and \(N\) drops to zero above it on a scale \(kT\).</p>


[[KEY the master formula of this chapter]]<p>\(J = e\int N(w)\,D(w)\,dw\), with \(N\) from \(@eq:supply@\) and the transmission from \(@eq:Dwkb@\), which the code evaluates as \(D=1/(1+e^{G})\). This is equal to \(e^{-G}\) wherever \(G\) is large, and bounded by 1 near the top. Above the barrier top, where there are no turning points, the code continues \(G\) linearly in energy with the slope it has 0.02 eV below the top (a parabolic-top continuation in the spirit of Kemble). So \(D\) rises smoothly to 1. Fowler–Nordheim, Richardson–Dushman and Schottky emission are three limits of it; the code of this page evaluates it numerically, without limits, wherever it needs to.</p>[[/KEY]]

<p>One assumption is hidden here and we state it: \(D\) depends only on the energy \(w\) of the normal motion, not on \(\varepsilon_t\). That holds for a plane, smooth surface in an isotropic free-electron metal. It fails for a real crystal face, where the band structure and the surface potential differ from face to face (this is why different tungsten planes emit differently).</p>
'''),

('fn', 'The Fowler–Nordheim equation', r'''
<p class="psec__lead">At low temperature the master formula can be done by hand. The result is the equation with which the experimenters of the 1950s read their tips from volts and amperes alone.</p>

<h4><span class="psub__n">2.5.1</span>Linearising the exponent</h4>
<p>At \(T\to0\) only electrons with \(w<0\) exist and \(N=4\pi m(-w)/h^{3}\). Because \(D=e^{-G}\) changes so fast with \(w\), only energies within a fraction of an electronvolt of the Fermi level matter, and we expand \(G\) there to first order:</p>
[[EQ Glin]]G(w)\approx G_F - \frac{w}{d},\qquad \frac{1}{d} = -\frac{dG}{dw}\Big|_{w=0}[[/EQ]]
<p>with \(G_F=G(0)\), the exponent computed in section 2.3. For the slope, note that raising \(w\) by a small amount lowers the barrier height seen from the electron by the same amount. Because the image term does not depend on \(w\), that is the same as lowering \(\varphi\) at fixed \(F\), so \(dG/dw=-\partial G/\partial\varphi\). With \(G = b\varphi^{3/2}v(f)/F\) and \(f\propto\varphi^{-2}\) (so \(d f/d\varphi=-2f/\varphi\)),</p>
[[EQ dGdphi]]\frac{\partial G}{\partial\varphi} = \frac{b}{F}\Bigl[\tfrac32\varphi^{1/2}v - 2f\,\varphi^{3/2}\tfrac{v'}{\varphi}\Bigr] = \frac{3b\sqrt{\varphi}}{2F}\,t(f),\qquad t(f)\equiv v-\tfrac43 f\,v'(f)[[/EQ]]
<p>For the triangular barrier \(v=1\), \(t=1\), and \(d=2F/(3b\sqrt{\varphi}) = \hbar eF/(2\sqrt{2m\varphi})\). This \(d\), the <em>decay width</em>, is an energy: the transmission falls by a factor e for each \(d\) by which the electron's energy lies below the Fermi level. At the working point it is @d_tri_eV|.3f@ eV for the triangular barrier; the image term divides it by \(t(f)\), and it becomes @d_ex_eV|.3f@ eV. Inserting Forbes' \(v\) gives</p>
[[EQ tF]]t(f)\approx 1+\frac{f}{9}-\frac{f}{18}\ln f[[/EQ]]
<p>(check C6 does the algebra symbolically; check C8 confirms \(\partial G/\partial\varphi\) numerically by differencing the quadrature of section 2.3: the formula with the exact \(t\) agrees to \(@t_exact_agree|tex1@\), and Forbes' \(t(f)\) is @t_approx_pct|.2f@ % off).</p>

<h4><span class="psub__n">2.5.2</span>The integral</h4>
<p>At \(T=0\), \(J = e\,\dfrac{4\pi m}{h^{3}}\,e^{-G_F}\displaystyle\int_{-\infty}^{0}(-w)\,e^{w/d}\,dw\), and \(\int_{-\infty}^0(-w)e^{w/d}dw = d^{2}\) (integration by parts, check C5). So</p>
[[EQ J0]]J_0 = \frac{4\pi m e}{h^{3}}\,d^{2}\,e^{-G_F}[[/EQ]]
<p>Inserting \(d=\hbar eF/(2\sqrt{2m\varphi}\,t)\), \(\hbar=h/2\pi\), and \(G_F=b\varphi^{3/2}v/F\), the constants combine (check C5):</p>
[[EQ FN]]J_0 = \frac{e^{3}}{8\pi h}\,\frac{F^{2}}{\varphi\,t^{2}(f)}\,\exp\!\Bigl(-\,v(f)\,\frac{b\,\varphi^{3/2}}{F}\Bigr)[[/EQ]]

[[KEY Fowler–Nordheim equation with the image-charge barrier (Murphy and Good form)]]<p>\(J_0 = \dfrac{a}{\varphi}\,\dfrac{F^{2}}{t^{2}}\,e^{-v\,b\,\varphi^{3/2}/F}\), with \(a=e^{2}/(8\pi h)=@a_FN|.4f@\ \mu\mathrm{A\,eV\,V^{-2}}\) and \(b=@b_FN|.4f@\ \mathrm{eV^{-3/2}\,V\,nm^{-1}}\) when \(\varphi\) is in electronvolt and \(F\) in volt per nanometre. It follows from the model of sections 2.2 to 2.4 at \(T=0\), with \(G\) expanded to first order about the Fermi level, for \(f\) away from 1. On this page it is evaluated with Forbes' approximations for \(v\) and \(t\).</p>[[/KEY]]

<div class="ptab-wrap"><table class="ptab"><thead><tr><th>symbol</th><th>meaning</th><th>value or unit</th><th>where it comes from</th></tr></thead><tbody>
<tr><td>\(J_0\)</td><td>emitted current density, zero temperature</td><td>A/m², here @J_FN0_ex|sci2@ at \(F\)=4 V/nm</td><td>the result</td></tr>
<tr><td>\(e\), \(h\)</td><td>elementary charge, Planck constant</td><td>exact SI values</td><td>2019 SI</td></tr>
<tr><td>\(F\)</td><td>field at the emitting surface</td><td>V/m; \(F=V/(kr)\)</td><td>@eq:apexfield@</td></tr>
<tr><td>\(\varphi\)</td><td>work function</td><td>@ex_phi|.1f@ eV, tungsten (assumed)</td><td>input</td></tr>
<tr><td>\(f\)</td><td>scaled field \(F/F_R\)</td><td>@f_ex|.4f@</td><td>@eq:roots@</td></tr>
<tr><td>\(v(f)\)</td><td>image-charge lowering of the exponent</td><td>@v_ex|.4f@</td><td>@eq:Gimage@, @eq:vF@</td></tr>
<tr><td>\(t(f)\)</td><td>prefactor correction \(v-\frac43fv'\)</td><td>@t_ex|.4f@</td><td>@eq:dGdphi@, @eq:tF@</td></tr>
<tr><td>\(b\)</td><td>second FN constant \(4\sqrt{2m}/(3\hbar e)\)</td><td>@b_FN|.4f@ eV<sup>−3/2</sup> V/nm</td><td>@eq:Gtri@</td></tr>
</tbody></table></div>
<p>Dimensional check: \(e^{2}F^{2}/(h\varphi)\) in the units of the table is \(\mu\mathrm{A\,eV\,V^{-2}}\cdot(\mathrm{V/nm})^{2}/\mathrm{eV} = \mu\mathrm{A/nm^{2}}\), a current density. Limiting cases: for \(F\to0\) (\(f\to0\)) \(v,t\to1\) and the equation becomes the triangular-barrier form of Fowler and Nordheim (1928). For \(f\to1\), \(v\to0\) and the exponent no longer suppresses the current. At about \(f\approx0.8\) the derivation fails, as Allaham et al. (2022) note. The barrier is then so low and thin that the expansion of \(G\) about the Fermi level is poor. Electrons at the Fermi level do not yet fly over it; at \(f=0.8\) its top still lies @top_f08_eV|.3f@ eV above them, and fly-over begins only at \(f=1\).</p>

[[EX FN|Fowler–Nordheim current density at the working point]]<p>At \(F=@ex_F_Vnm|.0f@\) V/nm and \(\varphi=@ex_phi|.1f@\) eV: \(f=@f_ex|.4f@\), Forbes' \(v=@vF_ex|.4f@\) (the quadrature gives @v_ex|.4f@; we use Forbes' value here because the formula is evaluated with it on this page), \(t=@t_ex|.4f@\), \(b\varphi^{3/2}/F=@G_tri_ex|.2f@\). Then \(J_0 = (@a_FN|.4f@\times10^{-6}/@ex_phi|.1f@)\times @ex_F_Vnm|.0f@^{2}/@t_ex|.3f@^{2}\times e^{-@G_F_ex|.2f@}\) A/nm², which is \(@J_FN0_ex|tex2@\ \mathrm{A/m^2}\). The full integral of section 2.4, without any approximation, gives \(@J_model_ex|tex2@\ \mathrm{A/m^2}\), at 300 K.</p>[[/EX]]

<h4><span class="psub__n">2.5.3</span>Finite temperature <span class="star">★</span></h4>
<p>With the linearised \(D\) and the full \(N\), the integral is \(J=e\,(4\pi m kT/h^{3})\,e^{-G_F}\int\ln(1+e^{-w/kT})\,e^{w/d}\,dw\). Integrating by parts (the boundary terms vanish for \(d>kT\)) turns it into \(\tfrac{d}{kT}\int e^{w/d}/(1+e^{w/kT})\,dw\), and \(\int_{-\infty}^{\infty}e^{au}/(1+e^{u})\,du = \pi/\sin\pi a\) for \(0<a<1\), with \(u=w/kT\) and \(a=kT/d\). Hence</p>
[[EQ Tfactor]]J(T) = J_0\,\frac{\pi kT/d}{\sin(\pi kT/d)}[[/EQ]]
<p>(check C9 evaluates both sides numerically at 30 digits). At the working point, 300 K, \(\pi kT/d=@x_ex|.3f@\) and the factor is @Tcorr_ex|.3f@, a @Tcorr_pct|.1f@ % correction. The factor diverges when \(\pi kT/d\to\pi\), that is when \(kT\to d\), and is a poor description well before that. Electrons far above the Fermi level, where the barrier is thinner, then dominate and the linearisation of \(G\) fails. That is the transition to thermal-field emission; there we integrate numerically.</p>

<h4><span class="psub__n">2.5.4</span>The Fowler–Nordheim plot</h4>
<p>Experimenters measure current \(I\) at voltage \(V\), not \(J\) at \(F\). If the emitting area \(A\) is constant and \(F=V/\zeta\) (so \(\zeta=kr\) is the <em>voltage conversion length</em>), \(I=AJ_0\) gives</p>
[[EQ FNplot]]\ln\frac{I}{V^{2}} = \ln\frac{A\,a}{\varphi\,t^{2}\zeta^{2}} - b\,\varphi^{3/2}\,\zeta\;\frac{v(f)}{V}[[/EQ]]
<p>Plotted against \(1/V\), the right-hand side is a straight line to a good approximation. Its slope is \(d[v(f)/V]/d(1/V)\) times \(-b\varphi^{3/2}\zeta\), and because \(f\propto V\) the derivative is \(v-fv'=s(f)\). For Forbes' \(v\) this is exactly \(s(f)=1-f/6\) (check C6b). So</p>
[[EQ FNslope]]S_{\mathrm{FN}} = -\,b\,\varphi^{3/2}\,\zeta\,\Bigl(1-\frac{f}{6}\Bigr)[[/EQ]]
<p>A measured slope gives \(\zeta\) if \(\varphi\) is known, and then \(r=\zeta/k\) if \(k\) is. Section 2.9 does this with real data.</p>
'''),

('thermal', 'Heat helps: Richardson–Dushman and Schottky emission', r'''
<p class="psec__lead">Warm the same metal and the supply of energetic electrons in the tail of the Fermi function takes over from tunnelling. The master formula gives that limit in one line.</p>

<p>For electrons with \(w\) above the top of the barrier, \(D\approx1\), and \(\ln(1+e^{-w/kT})\approx e^{-w/kT}\) when \(w\gg kT\). With no field the top is at \(w=\varphi\):</p>
[[EQ RD]]J = e\int_{\varphi}^{\infty}\frac{4\pi m\,kT}{h^{3}}\,e^{-w/kT}\,dw = \frac{4\pi m e k^{2}}{h^{3}}\,T^{2}e^{-\varphi/kT} \equiv A_R\,T^{2}\,e^{-\varphi/kT}[[/EQ]]
<p>with \(A_R=@A_R|tex5@\ \mathrm{A\,m^{-2}K^{-2}}\) (check C10; the textbook value is \(1.2017\times10^{6}\)). This is the Richardson–Dushman law. A field lowers the top of the barrier by the Schottky lowering \(\Delta\varphi\) of @eq:schottky@ and the emission is that of a work function \(\varphi-\Delta\varphi\):</p>
[[EQ schottkyJ]]J = A_R\,T^{2}\exp\!\Bigl(-\frac{\varphi-\Delta\varphi}{kT}\Bigr)[[/EQ]]
<p>For our Schottky preset we choose \(\varphi=@ps/phi_eV|.1f@\) eV for the zirconium-oxide-coated surface, an assumed value: the Hitachi page cited below says only that the coating lowers the work function. We also choose \(T=@ps/T|.0f@\) K and a field \(F=@sch_F_Vnm|.1f@\) V/nm at the apex, setting \(k\) so that this holds; this is an assumed operating point, not a quoted specification. Then \(kT=@sch_kT_eV|.3f@\) eV and \(\Delta\varphi=@sch_dphi_eV|.3f@\) eV. The field raises the current by a factor \(e^{\Delta\varphi/kT}=@sch_gain_RS|.0f@\) over plain Richardson emission (\(@sch_J_R|sci2@\) to \(@sch_J_RS|sci2@\ \mathrm{A/m^{2}}\)). The full integral gives \(@sch_J_model|sci2@\ \mathrm{A/m^{2}}\), @sch_ratio_pct|.0f@ % above the Schottky formula; the excess is tunnelling through the top of the lowered barrier.</p>

<h4><span class="psub__n">2.6.1</span>One formula, three regimes</h4>
<p>Dolan and Dyke (1954) did the integral of the master formula numerically, for a wide range of temperature, field and work function. They showed that it contains both the Fowler–Nordheim equation (cold, strong field) and the Richardson formula (hot, weak field). Our code does the same calculation (check C11: against the analytic Fowler–Nordheim formula the full integral is within @cfe_dev_pct|.1f@ % at 4 and 5 V/nm; against Richardson–Schottky at 2800 K and 0.1 V/nm it is within @therm_dev_pct|.1f@ %). The regime is read from where the peak of the emitted electrons' energy distribution lies (section 2.7). Below the Fermi level the source is a cold field emitter; between the Fermi level and the top of the barrier it is in the thermal-field regime; at the top, thermionic or Schottky.</p>

[[FIG regimes|REGFIG]]Current density at three fields from the full integral (dots), as a function of temperature, for a work function of 4.5 eV. At 4 V/nm the current is nearly independent of temperature up to about 1000 K (cold field emission); at 0.5 V/nm it rises by orders of magnitude (thermionic regime). The dotted line is the Richardson–Dushman law at zero field.[[/FIG]]
'''),

('energy', 'How wide is the energy: the spread ΔE', r'''
<p class="psec__lead">Lenses bend electrons of different energies by different amounts. The energy spread of the source therefore sets a blur in the probe (chapter 5), and it is the first of the four numbers we hand over.</p>

<p>Take electrons of total energy \(\varepsilon=w+\varepsilon_t\) leaving the surface. For each total energy, any normal energy \(w\le\varepsilon\) is allowed (the transverse part \(\varepsilon-w\) cannot be negative). Using \(\mathcal F(w+\varepsilon_t)=\mathcal F(\varepsilon)\) in the integral @eq:Jint@ and changing variables from \(\varepsilon_t\) to \(\varepsilon\),</p>
[[EQ Peps]]P(\varepsilon) = \mathcal F(\varepsilon)\int_{-\infty}^{\varepsilon}D(w)\,dw,\qquad J=e\,\frac{4\pi m}{h^{3}}\int P(\varepsilon)\,d\varepsilon[[/EQ]]
<p>(the second relation, which the code checks, follows from integrating @eq:Jint@ by parts; check C12: ratio of the two currents \(1+\)@C12_dev|.1e@). With the linearised barrier, \(D\propto e^{w/d}\), the inner integral is \(d\,e^{\varepsilon/d}\) times constants and</p>
[[EQ Pcold]]P(\varepsilon)\;\propto\;\frac{e^{\varepsilon/d}}{1+e^{\varepsilon/kT}}[[/EQ]]
<p>In words: the electrons that leave have energies spread from below the Fermi level (rising as \(e^{\varepsilon/d}\): lower-lying electrons see a thicker barrier) to a cut-off at the Fermi level, smeared by \(kT\). The peak is at \(\varepsilon^{*}=kT\ln[kT/(d-kT)]\), which exists when \(d>kT\) and lies below the Fermi level when \(d>2kT\). The full integral puts it at \(@peak_cfe_eV|.3f@\) eV at the working point, just below the Fermi level. The full width at half maximum \(\Delta E\) follows from the two roots of \(P=\tfrac12P_{\max}\). With \(d=@d_cfe_eV|.3f@\) eV and \(kT=@kT300_eV|.4f@\) eV it is @fwhm_cfe_linear_eV|.3f@ eV from @eq:Pcold@ and @fwhm_cfe_full_eV|.3f@ eV from the full integral (check C13).</p>

<p>Because \(d\propto F/\sqrt\varphi\), the width grows with the field: \(\Delta E=@fwhm_3|.3f@\), @fwhm_4|.3f@ and @fwhm_5|.3f@ eV at 3, 4 and 5 V/nm. A cold source gains in current by running at higher field and pays in energy width. For the Schottky preset the full integral gives \(\Delta E=@sch_fwhm_eV|.2f@\) eV. The distribution is broad because it is a thermal tail above the barrier top, and its peak lies @sch_peak_above_top_eV|.2f@ eV above the top.</p>

[[FIG energy|ENERGYFIG]]Total-energy distributions from the full integral for the cold preset (300 K, 4 V/nm, 4.5 eV) and the Schottky preset (1800 K, 0.5 V/nm, 2.9 eV), each divided by its own maximum and centred on its peak. The widths at half maximum are in the legend.[[/FIG]]

<p><strong>Against published values.</strong> A public Hitachi High-Tech page (8 May 2026), written for buyers of electron microscopes, quotes "around 0.2–0.3 eV" for cold field emission and "around 0.6–1.1 eV" for Schottky sources. Our cold value, @fwhm_cfe_full_eV|.2f@ eV, lies in the first range and was not fitted to it. Our Schottky value, @sch_fwhm_eV|.2f@ eV, lies below the second range. The model contains no electron–electron interaction in the beam and no distribution of fields over the emitting area. Both widen the measured distribution (an inference, not tested here). The vendor page is a marketing source and gives no conditions, so we use it only to show that the model is in the right range for the cold source and incomplete for the Schottky one.</p>
'''),

('bright', 'Brightness and the virtual source', r'''
<p class="psec__lead">A tip that emits a large current into a huge angle is useless for a probe, because only the electrons that go through a small aperture count. The quantity that matters is the current per unit area <em>and</em> per unit solid angle, the brightness.</p>

<p>The <em>brightness</em> \(B\) of a source is the current \(dI\) that comes from the area \(dA\) into the solid angle \(d\Omega\): \(B=dI/(dA\,d\Omega)\). Chapter 3 shows, with Liouville's theorem, that \(B/V\) does not change as the beam is accelerated through \(V\) (non-relativistically). We therefore give the <em>reduced brightness</em> \(B_r=B/V\), in A m<sup>−2</sup> sr<sup>−1</sup> V<sup>−1</sup>.</p>

<h4><span class="psub__n">2.8.1</span>From the energy of the sideways motion to the angle</h4>
<p>An electron with transverse energy \(\varepsilon_t\) that has been accelerated to the energy \(eV\) moves at a small angle \(\alpha\) to the axis with \(\alpha^{2}\approx\varepsilon_t/(eV)\) (ratio of the transverse to the total kinetic energy). Electrons with transverse energy between \(\varepsilon_t\) and \(\varepsilon_t+d\varepsilon_t\) therefore fill the solid angle \(d\Omega=\pi\,d(\alpha^{2})=\pi\,d\varepsilon_t/(eV)\). Counting those electrons as in @eq:Jint@ but without integrating over \(\varepsilon_t\) gives the current density per unit transverse energy,</p>
[[EQ jt]]j(\varepsilon_t)=e\,\frac{4\pi m}{h^{3}}\int D(w)\,\mathcal F(w+\varepsilon_t)\,dw[[/EQ]]
<p>so \(B = j\,\dfrac{eV}{\pi}\) at \(\varepsilon_t\to0\), where the direction is along the axis, and</p>
[[EQ Br]]B_r = \frac{e}{\pi}\,j(\varepsilon_t=0)[[/EQ]]
<p>with \(j\) per joule, so \(e\,j\) is per electronvolt. For the cold limit, \(\mathcal F\) is a step and \(j(\varepsilon_t)=(J/d)\,e^{-\varepsilon_t/d}\) (integrate \(e^{-G_F}e^{w/d}\) up to \(w=-\varepsilon_t\) and compare with @eq:J0@). The mean transverse energy is then \(d\), and</p>
[[EQ Brcold]]B_r = \frac{J}{\pi\,d}\quad(d\ \mathrm{in\ eV})[[/EQ]]
<p>At 4 V/nm this gives \(@Br_cold_formula|sci2@\), the full integral \(@Br_cold_model|sci2@\ \mathrm{A\,m^{-2}\,sr^{-1}\,V^{-1}}\) (check C14). The model's mean transverse energy is \(@meanEt_cfe_eV|.3f@\) eV (cold) and \(@sch_meanEt_eV|.3f@\) eV (Schottky preset). The reduced brightness of the Schottky preset is \(@sch_Br|sci2@\), a factor @ho_ratio_Br|.0f@ below the cold preset. The cold source wins by its current density, \(@J_4|sci2@\) against \(@sch_J_model|sci2@\ \mathrm{A/m^2}\), at similar transverse energy.</p>

<p>These are numbers for the emitting patch itself. A published reduced brightness of an operating source also includes everything between the patch and the measurement. It is dealt with in chapter 3, where we put published values next to ours. The vendor page of section 2.7 gives a brightness "up to about 10<sup>9</sup> A/cm²·sr" for cold field emission and "high, but generally lower" for Schottky, with no voltage. It is not a reduced brightness and we do not compare it with ours.</p>

<h4><span class="psub__n">2.8.2</span>The virtual source</h4>
<p>The electrons do not all seem to come from the same point. Follow the backward extension of the straight path each electron has far away: these lines pass through a small disc, the <em>virtual source</em>, which is the object the lenses image. A first estimate comes from conservation of angular momentum. In a field that points along the radius from the apex centre, an electron leaving the sphere of radius \(r\) with transverse momentum \(p_t=\sqrt{2m\varepsilon_t}\) keeps \(L=p_tr\) for ever. Far away its momentum is \(p_\infty=\sqrt{2m\,eV}\) and the extended path passes the centre at the distance</p>
[[EQ bimp]]b = \frac{L}{p_\infty} = r\sqrt{\frac{\varepsilon_t}{eV}}[[/EQ]]
<p>(check C17: a Runge–Kutta integration of the trajectory in a \(1/r\) potential, to 2 mm, finds @b_asymptote_nm|.5f@ nm against @b_exact_nm|.5f@ nm). We define the virtual source diameter as \(d_v=2r\sqrt{\langle\varepsilon_t\rangle/(eV)}\), with the mean transverse energy of the model. For the cold preset (\(r=@pc/r_nm|.0f@\) nm, \(V=@pc/V|.0f@\) V) it is @dv_cfe_nm|.2f@ nm; for the Schottky preset (\(r=@ps/r_nm|.0f@\) nm, \(V=@ps/V|.0f@\) V) it is @dv_sch_nm|.1f@ nm. The Hitachi page quotes typical virtual source sizes of 2.5 to 5 nm (cold) and 15 to 30 nm (Schottky). Ours are lower for both; the model has a perfectly radial field, no extractor lens and an emitting patch of zero size. All three would increase \(d_v\) (inference). We treat \(d_v\) as a lower bound.</p>
'''),

('data', 'Checking the model against a published tungsten tip', r'''
<p class="psec__lead">A model that has not met a measurement is a story. Here it meets one: the current–voltage curve of a tungsten tip measured by Ayari, Vincent, Perisanu, Poncharal and Purcell in 2023, whose raw numbers are public.</p>

<p><strong>The measurement</strong> (their section III). A \(\langle111\rangle\) tungsten tip, electrochemically etched from a 125 µm wire, initial radius about 15 nm, heated several times for 30 s at 1700 K. Base pressure \(3\times10^{-10}\) Torr (\(4\times10^{-8}\) Pa). The current was collected by a microchannel plate and phosphor screen, in the range from femtoampere to picoampere. The voltage was swept five times up and down between 1300 V and 1630 V in steps of 10 V. We use their sweep "run 4, down" (33 points; data in <code>data/ch02/ayari2023_w111_iv.csv</code>, licence CC BY 4.0, provenance in the README of that folder).</p>

<p><strong>What we did.</strong> (i) A straight line through \(\ln(I/V^{2})\) against \(1/V\) gives slope \(@ayari/fn_slope_V|.0f@\) V and intercept @ayari/fn_intercept|.3f@. That reproduces the authors' own fit (41 339 ± 73 V, 4.57 ± 0.05; check C19) and so confirms that we read the units of the file correctly (current in nanoampere). (ii) With \(\varphi=4.5\) eV, which the authors also assume, @eq:FNslope@ with \(s(f)=@ay_s_mid|.3f@\) at the middle of the range gives \(\zeta=@ay_zeta_slope_nm|.0f@\) nm. (iii) The full fit of \(I=A\,J(V/\zeta)\) to all 33 points, with the temperature factor and 300 K, gives \(\zeta=@ayari/fits/4.5/zeta_nm|.1f@\) nm, an emitting area \(A=@ayari/fits/4.5/A_nm2|.0f@\ \mathrm{nm^2}\), and a root-mean-square deviation of \(\ln I\) of @ay_resid_rms_pct|.1f@ %, largest deviation @ay_resid_max_pct|.1f@ %. With \(k=5\) the radius is \(r=\zeta/k=@ayari/fits/4.5/r_nm|.0f@\) nm. The authors' own analysis with the Murphy–Good model has 653 nm and 131 nm for the same sweep (their file <code>paramIV4d.txt</code>), so the two calculations agree.</p>

[[FIG data|DATAFIG]]First panel: the Fowler–Nordheim plot of run 4 (down) of Ayari et al. (2023): measured points, our model fit (wine, <i>φ</i> = 4.5 eV, 300 K) and the straight line of the authors. Second panel: the difference of ln <i>I</i> between measurement and model, in per cent.[[/FIG]]

<h4><span class="psub__n">2.9.1</span>Where model and data differ</h4>
<p><strong>The data do not fix the work function.</strong> The fit quality is the same, rms \(@ayari/fits/4.5/rms|.4f@\) in \(\ln I\), for any \(\varphi\) between 4.0 and 5.5 eV. Only \(\zeta\) changes, because the slope fixes the product \(\varphi^{3/2}\zeta\). For \(\varphi=\)4.0, 4.5, 5.0 and 5.5 eV the fit gives \(\zeta=\)@ayari/fits/4.0/zeta_nm|.0f@, @ayari/fits/4.5/zeta_nm|.0f@, @ayari/fits/5.0/zeta_nm|.0f@ and @ayari/fits/5.5/zeta_nm|.0f@ nm. The apex radius deduced from a slope inherits the full uncertainty of \(\varphi\) and of \(k\). The authors of the data make this point more strongly in their title and abstract. The model is not wrong here; the measurement is not sensitive enough to test it for \(\varphi\).</p>
<p><strong>The residuals.</strong> The model describes the curve to within @ay_resid_rms_pct|.1f@ % rms over a range in which the current changes by a factor @ay_I_range|.0f@. The deviations look irregular. The authors report that the current at a fixed voltage drifts by about 8 % per hour (their Fig. 4). In the data file the current at 1470 V in the ten sweeps in time order is @ay_I1470@ nA. Our residuals are of the size of that drift and the noise they quote (1.8 % standard deviation about their line). So the model has no deviation to explain that the measurement does not already contain (inference).</p>
<p><strong>The radius.</strong> The fit gives \(\zeta=kr=@ayari/fits/4.5/zeta_nm|.0f@\) nm, a tip of @ay_r_k5|.0f@ nm radius if \(k=5\), against 15 nm initially. The authors expect the radius to increase because of the repeated heating; the field-emission measurement alone cannot say. It does not contradict the model, but it shows what the model cannot do: it does not predict the geometry.</p>
<p><strong>The scaled field.</strong> The fit places the data at \(f=@ayari/fits/4.5/f_lo|.3f@\) to \(@ayari/fits/4.5/f_hi|.3f@\) (\(F=@ayari/fits/4.5/F_lo|.2f@\) to \(@ayari/fits/4.5/F_hi|.2f@\) V/nm). That is at the lower edge of the range that Forbes and co-workers call physically reasonable for a tungsten tip, \(0.15\le f\le0.45\). It is well above the "clearly unreasonable" limit 0.10 (Allaham et al. 2022, their Table 1). The classical tungsten data set of Dyke and Trolan (1953, emitter X89), which Forbes (2013) re-analysed, covers \(0.20<f<0.34\); our working point \(f=@f_ex|.2f@\) lies inside that range. We did not open the paper of Dyke and Trolan (only its abstract is public), so no number from it enters this chapter.</p>
'''),

('vac', 'Vacuum and contamination', r'''
<p class="psec__lead">The current of a cold tip depends on \(\varphi\) so steeply that a few foreign atoms on the apex change it. How fast they arrive, and whether they leave again, is decided by the pressure and the temperature.</p>

<h4><span class="psub__n">2.10.1</span>How many molecules arrive: Hertz–Knudsen</h4>
<p>The residual gas at temperature \(T_g\) and pressure \(p\) has density \(n=p/kT_g\) and Maxwell–Boltzmann velocities, \(f(\mathbf v)=(m_g/2\pi kT_g)^{3/2}e^{-m_g v^{2}/2kT_g}\). The molecules that hit a surface of unit area per second are those moving towards it, weighted by their normal speed:</p>
[[EQ HK]]\Phi = n\int_{v_x>0}v_x\,f(\mathbf v)\,d^{3}v = n\sqrt{\frac{kT_g}{2\pi m_g}} = \frac{p}{\sqrt{2\pi m_g\,kT_g}}[[/EQ]]
<p>(check C15 does the three integrals symbolically). This is the Hertz–Knudsen flux. For hydrogen (\(m_g=2.016\) u) at 300 K and \(10^{-9}\) Pa, \(\Phi=@flux_H2_1e-9Pa|sci2@\ \mathrm{m^{-2}s^{-1}}\); for carbon monoxide (28 u) \(@flux_CO_1e-9Pa|sci2@\ \mathrm{m^{-2}s^{-1}}\). A surface of tungsten carries about \(N_s=1/a^{2}\) atoms per unit area; with the lattice constant \(a=0.3165\) nm this is \(@Ns_W_lattice|sci2@\ \mathrm{m^{-2}}\), and we use \(N_s=10^{19}\ \mathrm{m^{-2}}\). Dividing, the time to deposit one monolayer if every molecule sticks is \(N_s/\Phi\):</p>
<div class="ptab-wrap"><table class="ptab"><thead><tr><th>pressure p (Pa)</th><th>one monolayer of H<sub>2</sub></th><th>one monolayer of CO</th></tr></thead><tbody>
@MLROWS@
</tbody></table></div>
<p>The table shows what the vacuum requirement means. At \(10^{-4}\) Pa a clean surface is covered in about a second by hydrogen and in a few seconds by carbon monoxide. At \(10^{-9}\) Pa it takes @tML_H2_9|.1f@ h for hydrogen at unit sticking. That is the pressure Applied Materials gives for its columns. Its press release of 14 December 2022 states "well below \(1\times10^{-11}\) millibar", that is below \(10^{-9}\) Pa, a public claim we quote and do not test.</p>

<h4><span class="psub__n">2.10.2</span>The rate equation</h4>
<p>Let \(\theta\) be the fraction of the apex sites that carry an adsorbed atom. Molecules arrive at \(\Phi\), a fraction \(s\) of those that hit a free site stick, and an adsorbed atom leaves at the rate \(k_d\) per second. We allow a factor \(\kappa\ge1\) for gas that is collected on the shank and diffuses to the apex (\(\kappa=1\) in the default). Then</p>
[[EQ rate]]\frac{d\theta}{dt} = a\,(1-\theta) - k_d\,\theta,\qquad a=\kappa\,s\,\frac{\Phi}{N_s},\quad k_d = \nu_0\,e^{-E_d/kT}[[/EQ]]
<p>This is first-order Langmuir kinetics: no interaction between adatoms, no precursor state, one adsorbate per site. The desorption rate has the Arrhenius form with an attempt frequency \(\nu_0=10^{13}\ \mathrm{s^{-1}}\) and a desorption energy \(E_d\); both are assumptions, discussed below. The equation has the solution (check C16, SymPy)</p>
[[EQ ratesol]]\theta(t) = \theta_\infty + (\theta_0-\theta_\infty)\,e^{-(a+k_d)\,t},\qquad \theta_\infty = \frac{a}{a+k_d}[[/EQ]]
<p>and the time to reach a coverage \(\theta^{*}<\theta_\infty\) from a clean surface is \(t^{*}=-\ln(1-\theta^{*}/\theta_\infty)/(a+k_d)\). When \(k_d\) is negligible, \(t^{*}\approx\theta^{*}N_s/(\kappa s\Phi)\) and, because \(\Phi\propto p\), \(p\,t^{*}\) is a constant. This is the prediction we test.</p>

<h4><span class="psub__n">2.10.3</span>Emission as a function of coverage (a model assumption)</h4>
<div class="pbox"><span class="pbox__t">Model assumption</span><p>We assume that the emitting surface is a patchwork: the fraction \(1-\theta\) with the clean work function \(\varphi\), the fraction \(\theta\) with \(\varphi+\Delta\varphi_{\mathrm{ads}}\). The current is the sum of the two contributions, \(I/I_0=(1-\theta)+\theta\rho\) with \(\rho=J(\varphi+\Delta\varphi_{\mathrm{ads}})/J(\varphi)\) at the same field. This is a choice made for simplicity; nothing in the derivation forces it. We take \(\Delta\varphi_{\mathrm{ads}}=@model/dphi_ads|.1f@\) eV, which gives \(\rho=@rho_ads|.4f@\) at the working point; it is not a measured value. What is measured (Cho 2014, below) is that adsorption of residual gas, mostly hydrogen, lowers the current and that this is attributed to an increase of the work function.</p></div>
<p>How strongly the current reacts to the work function is a result of the Fowler–Nordheim equation, not of this assumption. The logarithmic derivatives at the working point are \(\partial\ln J/\partial\ln F=@el_F|.1f@\) and \(\partial\ln J/\partial\ln\varphi=@el_phi|.1f@\). A rise of \(\varphi\) by 0.1 eV (2.2 %) cuts the current density by the factor @J_ratio_dphi01|.2f@; a rise by 1 eV cuts it by @J_ratio_dphi10|.4f@. A field higher by 10 % raises it by @J_ratio_F10|.1f@.</p>

<h4><span class="psub__n">2.10.4</span>The rate equation against a measurement</h4>
<p>Cho (2014) measured the probe current of a W(310) tip in an extreme-high-vacuum chamber after flash heating, while he changed the pressure with a getter pump. The residual gas was more than 99 % hydrogen (his Fig. 5). The probe current stays near its initial value for a time \(\tau_{90}\), until it has dropped by 10 %, and then falls quickly. He reports \(\tau_{90}=\)15, 105 and 450 min at \(2\times10^{-8}\), \(2\)–\(3\times10^{-9}\) and \(6\)–\(8\times10^{-10}\) Pa (gauge readings; we take 2.5 and \(7\times10^{-10}\) Pa). He also reports that the damping rate is proportional to the pressure. The products \(p\,\tau_{90}\) are @cho/0/p_tau|sci2@, @cho/1/p_tau|sci2@ and @cho/2/p_tau|sci2@ Pa·min: constant within \(\pm@cho_spread_half_pct|.0f@\) % over a factor 29 in pressure, as @eq:rate@ with the Hertz–Knudsen flux says. Taking \(\theta^{*}=0.1\) for the 10 % drop (patch model with \(\rho\approx0\)) and \(m_g=2.016\) u, each point needs the product \(\kappa s\) of @cho/0/s_eff|.2f@, @cho/1/s_eff|.2f@ and @cho/2/s_eff|.2f@, mean @cho_s_mean|.2f@. The simulation uses this mean as its default. The shape of the curve is a different matter: Cho's current stays flat and then falls quickly, while our patch model falls from the start, linearly in \(\theta\). The model reproduces the \(1/p\) scaling of the time to a 10 % drop, not the shape of the decay. A model with a threshold (a site that matters only once its neighbours are covered) would be needed for that.</p>

[[FIG cho|CHOFIG]]Time to a 10 % drop of the probe current of a W(310) tip against pressure: measured by Cho (2014) (dots) and the Hertz–Knudsen model of equation @eq:rate@ (line), whose one free number is the product <i>κs</i> of sticking and capture.[[/FIG]]

<p><strong>What this does and does not show.</strong> The data confirm the scaling \(\tau\propto1/p\) over one and a half decades. The size of the constant fixes one number, \(\kappa s\approx0.5\), and so does not test the model independently. Any combination of sticking, dissociation of H<sub>2</sub> into two atoms, and \(\theta^{*}\) that multiplies to the same product fits. Cho notes also that the "stable region" is specific to the (310) plane and disappears when gases other than hydrogen are present. The model has no plane dependence and no species dependence beyond the flux. His own constant \(C_{CH}=1.93\times10^{-7}\) Pa·min refers to a 50 % drop of the <em>total</em> emission current and is a different quantity.</p>

<h4><span class="psub__n">2.10.5</span>The flash-cleaning cycle</h4>
<p>At room temperature \(k_d\) is negligible: for \(E_d=@model/Ed|.1f@\) eV, \(k_d=@kd_RT|sci1@\ \mathrm{s^{-1}}\), so adsorbed atoms stay as long as the experiment lasts. This is why a cold tip cannot clean itself. Heating the tip for a few seconds changes the rate by many orders of magnitude: at 700 K, \(k_d=@kd_700|.2f@\ \mathrm{s^{-1}}\); at @model/Tflash|.0f@ K, \(@kd_flash|.0f@\ \mathrm{s^{-1}}\); at 2000 K, \(@kd_2000|sci1@\ \mathrm{s^{-1}}\). A flash of @model/tflash|.0f@ s at @model/Tflash|.0f@ K therefore removes everything (\(e^{-k_dt}\approx0\)). The values \(E_d=@model/Ed|.1f@\) eV and \(\nu_0=10^{13}\ \mathrm{s^{-1}}\) are assumptions, not measurements for this tip. They are chosen so that hydrogen-like adsorbates stay at room temperature and leave a hot tip within seconds near 700 K, where the residence time is \(1/k_d=@t_des_700|.1f@\) s. The cycle is then: run until \(I/I_0\) falls below a threshold, flash, run again. With the threshold \(@model/thr|.1f@\) the model flashes after @fl_gap_min|.0f@ min at \(10^{-8}\) Pa and hydrogen, and for the other pressures (same assumptions) after:</p>
<div class="ptab-wrap"><table class="ptab"><thead><tr><th>pressure (Pa)</th><th>time between flashes</th></tr></thead><tbody>
@FLROWS@
</tbody></table></div>

[[FIG cycle|CYCLEFIG]]Six hours at 10<sup>−8</sup> Pa (hydrogen, 300 K): coverage and current ratio from the rate equation, with a flash (vertical lines, 5 s at 1000 K) each time <i>I</i>/<i>I</i><sub>0</sub> falls below 0.7.[[/FIG]]

<p><strong>One atom.</strong> Applied Materials states publicly that "a single atom" on the tip can partly block the emission. In our patch model an adsorbed atom blocks only its own site. At our working point that is one of \(@sites_ex|.0f@\) sites in the effective emitting area of \(@A_eff_ex_nm2|.0f@\ \mathrm{nm^{2}}\) (current divided by current density). A single atom therefore changes the current by \(@one_atom|sci1@\). The model does not reproduce the claim for a tip of this size. It does for a tip whose emission is concentrated on a few atoms, where one atom is a large fraction of the emitting area. It also does when an adsorbate changes \(\varphi\) over a region larger than its own footprint. The model has neither; this is a limit of the model that we do not hide (see section @sec:hand@).</p>
'''),

('gap', 'Why the cold tip is bright but fragile', r'''
<p class="psec__lead">The two properties come from the same exponent, and it is easier to see them together.</p>

<p>The tip is bright because of two concentrations. The field concentrates: \(F=V/(kr)\) turns a kilovolt into @ex_F_Vnm|.0f@ V/nm. And the current concentrates. \(J\) varies as \(F^{@el_F|.1f@}\) locally, so electrons come out of a tiny patch (our effective emitting area is @A_eff_ex_nm2|.0f@ nm², @frac_emitting_pct|.0f@ % of the hemisphere, \(@surface_tip_nm2|.0f@\ \mathrm{nm^2}\)) with a small transverse energy (@meanEt_cfe_eV|.2f@ eV). Brightness is current density over transverse energy (section 2.8), so a large current density at a small transverse energy is a high brightness. The tiny emitting area does not raise the brightness. It makes the virtual source small, which is what lets a column shrink it to a nanometre spot without throwing current away.</p>
<p>The tip is fragile because of the same exponent seen from the other side. The current depends on the work function with the logarithmic derivative \(@el_phi|.0f@\). One adsorbed atom that raises the local work function by 0.1 eV removes @loss_01_pct|.0f@ % of the current from where it sits, and by 1 eV removes @loss_10_pct|.1f@ %. At \(10^{-9}\) Pa a surface of tungsten receives a monolayer of hydrogen in @tML_H2_9|.1f@ h (all molecules sticking) and the current falls by 10 % in a few hours. A Schottky emitter is hot, the adsorbates leave as fast as they come, and the current is steady; it pays with a lower brightness and a larger energy spread. A cold emitter has to be flashed.</p>
'''),

('sim', 'The source on the screen', r'''
<p class="psec__lead">The figure below solves the model of this chapter in the browser. The numbers beside it are the ones handed to chapter 3.</p>
@SIM@
<p><strong>Equation to screen.</strong></p>
<div class="ptab-wrap"><table class="ptab"><thead><tr><th>what you see</th><th>symbol</th><th>from</th></tr></thead><tbody>
<tr><td>radius of the drawn apex</td><td>\(r\)</td><td>slider; the apex is drawn on a logarithmic scale of the slider, not to scale against the shank or the gap</td></tr>
<tr><td>density of field lines and of electron dots</td><td>\(F,\ I\)</td><td>@eq:apexfield@, current of the cap integral</td></tr>
<tr><td>dark dots on the apex</td><td>\(\theta\)</td><td>number proportional to the coverage of @eq:ratesol@</td></tr>
<tr><td>Fowler–Nordheim plot, with a least-squares straight line through the clean-tip points</td><td>\(\ln(I/V^{2})\) against \(1/V\)</td><td>the full integral of section 2.4 over the apex cap, 13 voltages from 0.70 to 1.15 times the extraction voltage</td></tr>
<tr><td>energy distribution</td><td>\(P(\varepsilon)\)</td><td>@eq:Peps@, clean and covered parts mixed with the weights \(1-\theta,\ \theta\)</td></tr>
<tr><td>coverage and current against time</td><td>\(\theta(t),\ I/I_0\)</td><td>@eq:ratesol@, flashes when \(I/I_0\) falls below the threshold</td></tr>
</tbody></table></div>
<p><strong>Where the drawing differs from the model.</strong> The apex is drawn as a sphere on a cone. The model uses the cosine law \(F(\vartheta)=F_0\cos\vartheta\) of a sphere in a uniform field for the variation of the field over the cap, and integrates \(J\) over the cap of the hemisphere. The shank is not in the model beyond the factor \(k\). The number of adsorbate dots is proportional to \(\theta\), not a count of atoms. The time axis runs at the rate chosen with the speed control. Nothing is integrated while it plays: the whole run is computed at once (the rate equation has an exact solution) and replayed.</p>
'''),

('hand', 'Hand-over, limits and checks', r'''
<h4><span class="psub__n">2.13.1</span>What chapter 3 receives</h4>
<p>The four numbers handed to chapter 3, for the two presets, are computed by <code>handover()</code> in <code>physics/ch02.js</code> and <code>ref/ch02.py</code> (the two agree to a relative difference of \(10^{-9}\); <code>checks/check_parity.py</code>). The simulation changes them when a slider moves or when time passes.</p>
<div class="ptab-wrap"><table class="ptab"><thead><tr><th>quantity</th><th>symbol, unit</th><th>cold preset</th><th>Schottky preset</th></tr></thead><tbody>
<tr><td>settings</td><td></td><td>\(r=@pc/r_nm|.0f@\) nm, \(V=@pc/V|.0f@\) V, \(k=@pc/k|.0f@\), \(\varphi=@pc/phi_eV|.1f@\) eV, 300 K</td><td>\(r=@ps/r_nm|.0f@\) nm, \(V=@ps/V|.0f@\) V, \(k=@ps/k|.0f@\), \(\varphi=@ps/phi_eV|.1f@\) eV, 1800 K</td></tr>
<tr><td>apex field</td><td>\(F\), V/nm</td><td>@ho_cfe/F0_Vnm|.2f@</td><td>@sch_F_Vnm|.2f@</td></tr>
<tr><td>emission current</td><td>\(I_e\), A</td><td>@ho_cfe/I_e|sci2@</td><td>@ho_sch/I_e|sci2@</td></tr>
<tr><td>reduced brightness</td><td>\(B_r\), A m<sup>−2</sup> sr<sup>−1</sup> V<sup>−1</sup></td><td>@ho_cfe/B_r|sci2@</td><td>@ho_sch/B_r|sci2@</td></tr>
<tr><td>energy spread (FWHM)</td><td>\(\Delta E\), eV</td><td>@ho_cfe/dE_eV|.3f@</td><td>@ho_sch/dE_eV|.3f@</td></tr>
<tr><td>virtual source size</td><td>\(d_v\), nm</td><td>@dv_cfe_nm|.2f@</td><td>@dv_sch_nm|.1f@</td></tr>
</tbody></table></div>

<h4><span class="psub__n">2.13.2</span>What the model leaves out</h4>
<p>Free-electron metal, no band structure and no crystal face dependence. A planar barrier with a classical image charge, and the WKB transmission without its prefactor. A hemispherical cap with \(F\propto\cos\vartheta\), and \(k\) as a free number; no field solver (a proper one is outside this project). No Coulomb interaction between electrons, hence no Boersch effect and no space-charge limit on the brightness. A radial-field estimate of the virtual source. Contamination as one species, first-order kinetics, no surface diffusion, with \(E_d\), \(\nu_0\), \(\kappa\) and \(\Delta\varphi_{\mathrm{ads}}\) assumed, and \(s\) obtained from one data set. No tip blunting by the high-temperature flash, no ion bombardment of the tip, no emission-pattern change. Each omission is a place where a real column's source module differs; none is a claim about any particular product.</p>

<h4><span class="psub__n">2.13.3</span>Checks run for this chapter</h4>
<p>Every formula derived above was checked, symbolically with SymPy where it is an identity and numerically against an independent evaluation where it is not. The script is <code>derive/ch02.py</code>; the table is its output (@checks_summary@).</p>
<div class="ptab-wrap"><table class="ptab"><thead><tr><th>check</th><th>statement</th><th>result</th><th>detail</th></tr></thead><tbody>
@CHECKROWS@
</tbody></table></div>

<div class="pbox pbox--ex"><span class="pbox__t">Problems</span>
<p><strong>1.</strong> A tip of radius 30 nm with \(k=5\) is operated at 800 V. Find \(F\), \(f\), \(v\) (Forbes) and \(J_0\) for \(\varphi=4.5\) eV. <em>Answer:</em> \(F=@p1_F|.2f@\) V/nm, \(f=@p1_f|.3f@\), \(v=@p1_v|.3f@\), \(J_0=@p1_J|sci2@\ \mathrm{A/m^2}\).</p>
<p><strong>2.</strong> Show from \(G=b\varphi^{3/2}v(f)/F\) that \(\partial\ln J/\partial\ln\varphi\approx-\tfrac32\,b\varphi^{3/2}t(f)/F\) when the prefactor is neglected, and evaluate it at the working point. <em>Answer:</em> \(-\tfrac32\times@G_tri_ex|.2f@\times@t_ex|.3f@=@el_phi_approx|.1f@\); the complete derivative, with the prefactor, is @el_phi|.1f@.</p>
<p><strong>3.</strong> With \(s=1\), how long does a clean tungsten surface take to receive one monolayer of CO at \(10^{-7}\) Pa, and of H<sub>2</sub>? <em>Answer:</em> @p3_t_CO|.0f@ s and @p3_t_H2|.0f@ s.</p></div>

<h4><span class="psub__n">2.13.4</span>Sources</h4>
<p>Each source below was opened and read for this chapter; what was read is stated.</p>
<ol class="prefs">
<li>M. M. Allaham, R. G. Forbes, A. Knápek, D. Sobola, D. Burda, P. Sedlák, M. S. Mousa, "Interpretation of field emission current–voltage data: background theory and detailed simulation testing of a user-friendly webtool", Materials Today Communications 31 (2022) 103654, <a href="https://arxiv.org/abs/2205.15042">arXiv:2205.15042</a>. Read: section 2 (barrier, \(F_R\), \(f\), equations 2 to 8 and 15, orthodoxy-test table).</li>
<li>R. G. Forbes, "Development of simple quantitative test for lack of field emission orthodoxy", Proc. R. Soc. A 469 (2013) 20130271, <a href="https://arxiv.org/abs/1209.6611">arXiv:1209.6611</a>. Read: sections 3 and 4, tables of constants and of the classical data sets. The approximation of \(v(f)\) is from R. G. Forbes, Appl. Phys. Lett. 89 (2006) 113122, cited here from the two papers above and not opened.</li>
<li>W. W. Dolan and W. P. Dyke, "Temperature-and-Field Emission of Electrons from Metals", Phys. Rev. 95 (1954) 327. Read: abstract, introduction, the section on the work function.</li>
<li>A. Ayari, P. Vincent, S. Perisanu, P. Poncharal, S. T. Purcell, "All field emission experiments are noisy, … are any meaningful ?", <a href="https://arxiv.org/abs/2301.13578">arXiv:2301.13578</a> (2023), with the data set <a href="https://doi.org/10.5281/zenodo.7215660">doi:10.5281/zenodo.7215660</a> (CC BY 4.0). Read: sections II to III and the analysis notebook.</li>
<li>B. Cho, "Pressure Measurement Using Field Electron Emission Phenomena", Applied Science and Convergence Technology 23 (2014) 83–89, <a href="http://dx.doi.org/10.5757/ASCT.2014.23.2.83">doi:10.5757/ASCT.2014.23.2.83</a>. Read in full.</li>
<li>R. A. Chapman, "The use of an energy analyser for the measurement of the total energy distribution of field-emitted electrons from tungsten", M.Sc. thesis, University of Aston in Birmingham, 1971, <a href="https://publications.aston.ac.uk/id/eprint/21852/">Aston repository</a>. Read: the parts that give \(k=5\) and the tip radii.</li>
<li>Hitachi High-Tech, "Cold Field Emission vs Schottky: How to Choose the Right Electron Source for Your SEM", 8 May 2026, <a href="https://hte.hitachi-hightech.com/blog/cold-field-emission-vs-schottky">hte.hitachi-hightech.com</a>. Read in full; a vendor page, used only for the ranges quoted in sections 2.7 and 2.8.</li>
<li>Applied Materials, press release of 14 December 2022 as reproduced by Semiconductor Digest, <a href="https://www.semiconductor-digest.com/applied-materials-breakthrough-in-electron-beam-imaging-technology-accelerates-development-of-the-worlds-most-advanced-computer-chips/">semiconductor-digest.com</a>. Quoted as a public claim; not re-opened for this chapter (the planning session read it on 9 November 2026). No affiliation with Applied Materials is claimed, and nothing here models any of its products.</li>
</ol>
'''),

]


# ================================================================================================ the rest of the numbers
def finish_numbers(N):
    more_numbers(N)
    ho_c, ho_s = N['ho_cfe'], N['ho_sch']
    pc, ps = N['preset_cfe'], N['preset_schottky']
    N['pc'] = dict(r_nm=pc['r'] * 1e9, V=pc['V'], k=pc['k'], phi_eV=pc['phi'] / eV, T=pc['T'])
    N['ps'] = dict(r_nm=ps['r'] * 1e9, V=ps['V'], k=ps['k'], phi_eV=ps['phi'] / eV, T=ps['T'])
    ho_c['F0_Vnm'] = ho_c['F0'] * 1e-9
    N['DG'] = math.exp(N['G_tri_ex'] - N['G_ex']); N['D_inv'] = 1 / N['D_ex']; N['barrier_w'] = N['x2_nm'] - N['x1_nm']
    N['t_approx_pct'] = 100 * N['t_approx_err_284']
    N['sch_ratio_pct'] = 100 * (N['sch_ratio_model_RS'] - 1)
    N['cfe_dev_pct'] = 100 * max(abs(N['cfe_ratio_4'] - 1), abs(N['cfe_ratio_5'] - 1))
    N['therm_dev_pct'] = 100 * abs(N['thermionic_ratio'] - 1)
    N['C12_dev'] = abs(N['C12_ratio'] - 1)
    N['ay_r_k5'] = N['ayari']['fits']['4.5']['zeta_nm'] / 5               # finisher: was typed as 130 nm
    N['cho_spread_half_pct'] = 50 * N['cho_ptau_spread']
    N['dv_cfe_nm'] = ho_c['d_v'] * 1e9; N['dv_sch_nm'] = ho_s['d_v'] * 1e9
    N['el_phi_approx'] = -1.5 * N['G_tri_ex'] * N['t_ex']
    N['loss_01_pct'] = 100 * (1 - N['J_ratio_dphi01']); N['loss_10_pct'] = 100 * (1 - N['J_ratio_dphi10'])
    N['frac_emitting_pct'] = 100 * N['frac_emitting']
    N['fl_gap_min'] = N['flash_scan'][1]['t_s'] / 60
    N['tML_H2_9'] = N['t_ML_H2_1e-9Pa_s'] / 3600
    I = np.array(N['ayari']['V']); Iv = np.array(N['ayari']['I_nA'])
    N['ay_I_range'] = Iv.max() / Iv.min()
    N['ay_I1470'] = ', '.join(f'{x:.3g}' for x in N['ayari']['I1470_nA'])
    N['checks_summary'] = N['_summary']
    return N


def special_tables(N):
    sup = lambda e: str(e).translate(SUP)
    ml = ''.join(f'<tr><td>10{sup(int(round(math.log10(r["p"]))))}</td><td>{dur(r["t_ML_H2"])}</td><td>{dur(r["t_ML_CO"])}</td></tr>' for r in N['ml_scan'])
    fl = ''.join(f'<tr><td>10{sup(int(round(math.log10(r["p"]))))}</td><td>{dur(r["t_s"])}</td></tr>' for r in N['flash_scan'])
    esc = lambda t: t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    ck = ''.join(f'<tr><td>{c["id"]}</td><td>{esc(c["title"])}</td><td>{"pass" if c["ok"] else "FAIL"}</td><td>{esc(c["detail"])}</td></tr>' for c in N['_checks'])
    return dict(MLROWS=ml, FLROWS=fl, CHECKROWS=ck)


# ================================================================================================ the simulation markup and its style
def ctl(id, label, extra=''):
    return (f'<label class="ctl"><span class="ctl__row"><span>{label}</span><output id="eb-{id}-out" for="eb-{id}"></output></span>'
            f'<input type="range" id="eb-{id}" min="0" max="1" step="0.01" value="0.5" {extra}></label>')


def sim_html(n):
    ro = lambda i, lab, wide=False, accent=False: f'<div{" class=wide" if wide else ""}><dt>{lab}</dt><dd id="eb-o-{i}"{" class=is-accent" if accent else ""}></dd></div>'
    return f'''<div class="ebsim" id="ebsim">
<div class="ebsim__plots">
<figure class="stage ebsim__tipfig"><div class="stage__canvas ebsim__c ebsim__c--tip" style="--ar:16/9"><canvas id="eb-tip" role="img" aria-label="Drawing of the tip, its field lines, electrons and adsorbed atoms"></canvas></div>
<figcaption class="stage__cap"><span><b>Figure 2.{n}a</b>the tip: field lines (dashed), emitted electrons (wine dots, number follows the logarithm of the current), adsorbed atoms (dark dots, number follows θ)</span></figcaption></figure>
<div class="ebsim__three">
<figure class="stage"><div class="stage__canvas ebsim__c" style="--ar:4/3"><canvas id="eb-fn" role="img" aria-label="Fowler-Nordheim plot"></canvas></div>
<figcaption class="stage__cap"><span><b>2.{n}b</b>Fowler–Nordheim plot; dashed: straight line through the clean tip; rose: fully covered tip (θ = 1); solid wine: the tip now</span></figcaption></figure>
<figure class="stage"><div class="stage__canvas ebsim__c" style="--ar:4/3"><canvas id="eb-en" role="img" aria-label="Energy distribution of the emitted electrons"></canvas></div>
<figcaption class="stage__cap"><span><b>2.{n}c</b>energy distribution; grey: clean tip</span></figcaption></figure>
<figure class="stage"><div class="stage__canvas ebsim__c" style="--ar:4/3"><canvas id="eb-tm" role="img" aria-label="Coverage and current against time"></canvas></div>
<figcaption class="stage__cap"><span><b>2.{n}d</b>coverage and current against time; rose lines: flashes; black line: now</span></figcaption></figure>
</div></div>
<div class="panel ebsim__panel">
<div class="panel__group"><p class="panel__label">Source</p><div class="actions"><button class="btn btn--ghost" type="button" data-eb-preset="cold">Cold field emitter</button><button class="btn btn--ghost" type="button" data-eb-preset="schottky">Schottky emitter</button></div>
{ctl('r', 'Tip radius <i>r</i>')}{ctl('V', 'Extraction voltage <i>V</i>')}{ctl('k', 'Field factor <i>k</i>')}{ctl('phi', 'Work function <i>φ</i>')}{ctl('T', 'Tip temperature <i>T</i>')}</div>
<div class="panel__group"><p class="panel__label">Vacuum</p>{ctl('p', 'Pressure <i>p</i>')}
<label class="ctl"><span class="ctl__row"><span>Residual gas</span></span><select id="eb-gas"><option value="H2">H₂ (2.016 u)</option><option value="CO">CO (28.01 u)</option><option value="N2">N₂ (28.01 u)</option></select></label></div>
<div class="panel__group"><p class="panel__label">Time</p>
<label class="ctl"><span class="ctl__row"><span>Speed</span></span><select id="eb-speed"><option value="1">1 s per s</option><option value="30">30 s per s</option><option value="300">5 min per s</option><option value="1800" selected>30 min per s</option><option value="14400">4 h per s</option><option value="86400">1 day per s</option></select></label>
<label class="ctl"><span class="ctl__row"><span>Time since the start (clean tip)</span></span><input type="range" id="eb-scrub" min="0" max="1" step="0.001" value="0"></label>
<div class="actions"><button class="btn" type="button" id="eb-play">Pause</button><button class="btn btn--ghost" type="button" id="eb-flash">Restart from a clean tip</button></div>
<label class="switch"><span>Flash automatically below the threshold</span><input type="checkbox" id="eb-auto" checked></label></div>
<details class="ebsim__assume"><summary>Model assumptions (not measured values)</summary>
{ctl('sk', 'Sticking × capture <i>κs</i>')}{ctl('Ed', 'Desorption energy <i>E<sub>d</sub></i>')}{ctl('dads', 'Work function rise per adsorbate Δ<i>φ</i>')}{ctl('thr', 'Flash threshold <i>I</i>/<i>I</i><sub>0</sub>')}{ctl('Tfl', 'Flash temperature')}{ctl('tfl', 'Flash duration')}</details>
<div class="panel__group"><p class="panel__label">Hand-over to chapter 3</p><dl class="readouts">
{ro('I', 'Emission current <i>I<sub>e</sub></i>', accent=True)}{ro('B', 'Reduced brightness <i>B<sub>r</sub></i>', accent=True)}{ro('dE', 'Energy spread Δ<i>E</i>', accent=True)}{ro('dv', 'Virtual source <i>d<sub>v</sub></i>', accent=True)}
{ro('F', 'Apex field', wide=True)}{ro('reg', 'Regime', wide=True)}{ro('th', 'Coverage θ')}{ro('r', '<i>I</i>/<i>I</i><sub>0</sub>')}{ro('t', 'Since last flash')}{ro('n', 'Flashes so far')}{ro('fl', 'Gas flux Φ', wide=True)}{ro('ml', 'One monolayer in (s = 1)', wide=True)}</dl>
<p class="ebsim__status" id="eb-status" role="status" aria-live="polite"></p></div>
</div></div>'''


SIM_CSS = '''
.ebsim { display: grid; grid-template-columns: minmax(0, 1fr); gap: 16px; align-items: start; margin: 1.6em 0 1.8em; font-family: var(--sans); color: var(--ink); }
.ebsim__plots { display: grid; gap: 14px; min-width: 0; }
.ebsim__three { display: grid; grid-template-columns: minmax(0, 1fr); gap: 14px; }
.ebsim__three .ebsim__c { --ar: 16/7 !important; }
.ebsim .stage { margin: 0; }
.ebsim .stage__cap { font-size: 13.5px; line-height: 1.4; padding: 8px 10px; }
.ebsim .stage__cap b { margin-right: 8px; }
.ebsim__c { background-size: 24px 24px; }
.ebsim .ctl { font-size: 13.5px; }
.ebsim select { font: 13.5px var(--sans); color: var(--ink); background: var(--card); border: 1px solid var(--rule); border-radius: 6px; padding: 5px 8px; }
.ebsim .panel { box-shadow: none; }
@media (min-width: 700px) { .ebsim .panel { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); column-gap: 24px; align-items: start; } .ebsim .panel > .panel__group:last-child, .ebsim__assume { grid-column: 1 / -1; } }
.ebsim__assume { border: 1px solid var(--rule-soft); border-radius: 8px; padding: 8px 12px 12px; display: grid; gap: 10px; }
.ebsim__assume summary { cursor: pointer; font: 500 10.5px var(--mono); letter-spacing: .12em; text-transform: uppercase; color: var(--muted); }
.ebsim__assume[open] summary { margin-bottom: 8px; }
.ebsim__status { margin: 0; min-height: 1.2em; font: 11px var(--mono); color: var(--muted); }
.ebsim .readouts dd { white-space: normal; font-size: 12.5px; }
.ebsim .readouts dt i { font-family: var(--tex); text-transform: none; letter-spacing: 0; font-size: 13px; }
.ptab-wrap { overflow-x: auto; max-width: 100%; margin: 1.2em 0 1.4em; }
.ptab-wrap .ptab { display: table; width: 100%; margin: 0; }
.pfig__row svg { min-width: 0; }
@media (max-width: 640px) { .pfig__row { grid-template-columns: minmax(0, 1fr); } }
'''

# ================================================================================================ render
ABSTRACT = ('<b>Abstract.</b> The chapter starts at the metal. It derives the barrier an electron meets outside a tungsten surface (applied field and image charge), '
            'the probability of tunnelling through it (WKB), the supply of electrons from the Fermi–Dirac gas, and from the three the Fowler–Nordheim, Richardson–Dushman '
            'and Schottky formulas, the energy spread and the reduced brightness of each source. It then follows the vacuum physics (Hertz–Knudsen flux, coverage kinetics, '
            'flash cleaning) that makes a cold tip bright and fragile at once. A published tungsten-tip data set and a published measurement of current decay against '
            'pressure are laid over the model and the differences are stated. Four numbers go to chapter 3: emission current, reduced brightness, energy spread, virtual source size. '
            'Assumed, not measured: the field factor <i>k</i>, the work functions, the desorption energy and the effect of an adsorbate; each is a control of the simulation.')

_MACRO = re.compile(r'\[\[(EQ|FIG|EX|KEY) ([^\]]*)\]\](.*?)\[\[/\1\]\]', re.S)


def render_body(body, SPECIAL, N):
    def macro(m):
        kind, arg, text = m.group(1), m.group(2), m.group(3)
        if kind == 'EQ': return eq(arg, text)
        if kind == 'FIG':
            label, _, k = arg.partition('|')
            return fig(label, SPECIAL[k], text)
        if kind == 'EX':
            label, _, title = arg.partition('|')
            return ex(label, fill(title, N, SPECIAL), text)
        return key(arg, text)
    body = _MACRO.sub(macro, body)
    if '@SIM@' in body:
        COUNT['fig'] += 1; LABELS['fig:sim'] = COUNT['fig']
        body = body.replace('@SIM@', sim_html(COUNT['fig']))
    return fill(body, N, SPECIAL)


def build():
    N = finish_numbers(load_numbers())
    SPECIAL = special_tables(N)
    SPECIAL.update(TIPFIG=fig_tip(N), BARRIERFIG=fig_barrier(N), VTFIG=fig_vt(N), REGFIG=fig_regimes(N), ENERGYFIG=fig_energy(N),
                   DATAFIG=fig_data(N), CHOFIG=fig_cho(N), CYCLEFIG=fig_cycle(N))
    # fig_cycle writes numbers used in the text: rebuild the table that depends on them after the figures
    html = None
    for _ in (1, 2):                                   # two passes: forward references to equations and figures need the numbers of the first
        for k in COUNT: COUNT[k] = 0
        parts = [sec(l, fill(t, N, SPECIAL), render_body(b, SPECIAL, N)) for l, t, b in SECTIONS]
        html = ''.join(parts)
    head = ('<header class="paper__head"><p class="paper__kicker">Project 07 · The electron beam, from tip to measurement · chapter 2</p>'
            '<h2 class="paper__title" id="ch02-title">The source</h2>'
            f'<div class="paper__abstract">{ABSTRACT}</div></header>')
    full = f'<article class="paper is-typeset" id="ch02">{head}<div class="paper__body">{html}</div></article>'
    ui = open(os.path.join(EB, 'physics', 'ch02_ui.js'), encoding='utf-8').read()
    ui = fill(ui, N, SPECIAL)
    return dict(id='ch02', title='The source', html=full, css=SIM_CSS, ui_js=ui, physics_js=os.path.join(EB, 'physics', 'ch02.js'), numbers=N)

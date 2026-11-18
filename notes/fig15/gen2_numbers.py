"""Fig. 15, generation 2: every number the lecture note quotes, read from the stored data.

Usage:  python3 notes/fig15/gen2_numbers.py            print every number with the run file (or stored curve) it comes from
        python3 notes/fig15/gen2_numbers.py --write    also rewrite the NUM block of public/scripts/resonant-note.js

Sources, and nothing else (a pure read: no run is computed here):
  public/data/resonant-tunnelling/2026-11-18/kaggle/index.json   the corrected generation (file_corrected.py): per run T_ref (walls
                                                                  exact; discs and shells the (x, rho) run), T_unc, provisional,
                                                                  T_old, error, gate, status, tau; the diode's J(V) from T_ref
  public/data/resonant-tunnelling/2026-11-14/kaggle/index.json   the batch as first computed (run lengths, GPU time, counts)
  notes/fig15/audit/twin_sources.json, twin_converge.json         the grid audit: which numerical source moved the resonances
  public/data/resonant-tunnelling/2026-11-13/derived/exact-1d.json  the exact 1D diode curve (iv.py) the page draws in Fig. 15e
  tools/kaggle/resonant-tunnelling/tm.py, iv.py                   the same exact 1D code that wrote the stored exact curves, used
                                                                  where the stored 0.01 energy grid is too coarse for a narrow peak
                                                                  (resonance energies, widths Gamma, band edges, the level under bias)
A case not in the index prints as "missing".
"""
import json, os, re, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'tools', 'kaggle', 'resonant-tunnelling'))
import tm  # noqa: E402
import iv  # noqa: E402
import exact1d  # noqa: E402

IDX_PATH = os.path.join(ROOT, 'public/data/resonant-tunnelling/2026-11-18/kaggle/index.json')
EX1_PATH = os.path.join(ROOT, 'public/data/resonant-tunnelling/2026-11-13/derived/exact-1d.json')
NOTE = os.path.join(ROOT, 'public/scripts/resonant-note.js')
IDX = json.load(open(IDX_PATH)); EX1 = json.load(open(EX1_PATH))
OLD = json.load(open(os.path.join(ROOT, 'public/data/resonant-tunnelling/2026-11-14/kaggle/index.json')))
AUD = os.path.join(ROOT, 'notes/fig15/audit')
RUNS = IDX['runs']
OUT = {}            # name -> value, for the note's NUM block
SRC = []            # (name, value, source) lines


def put(name, value, source):
    OUT[name] = value; SRC.append((name, value, source))


def r3(x, n=3):
    return None if x is None else float(f'{x:.{n}g}')


# ---------- exact 1D (tm.py) ----------
def bis(f, a, b):
    fa = f(a)
    for _ in range(80):
        m = (a + b) / 2; fm = f(m)
        if (fm > 0) == (fa > 0): a, fa = m, fm
        else: b = m
    return (a + b) / 2


def segs(N, V0, D, P):
    cs = [(k - (N - 1) / 2) * P for k in range(N)]
    return [(c - D / 2, c + D / 2, V0) for c in cs]


def T1(E, sg):
    return abs(tm.solve(E, sg)[0]) ** 2


def peaks(sg, E0=0.05, E1=2.65, n=26000, thr=0.5):
    E = np.linspace(E0, E1, n); T = np.array([T1(e, sg) for e in E])
    return [i for i in range(1, n - 1) if T[i] > thr and T[i] >= T[i - 1] and T[i] >= T[i + 1]], E, T


def width(sg, Er):
    """Full width at half maximum of the peak at Er, by bisection on each side (T is 1 at a symmetric pair's peak)."""
    Tp = T1(Er, sg); h = Tp / 2
    def side(sgn):
        a, step = Er, 1e-4
        while T1(a + sgn * step, sg) > h: a += sgn * step; step *= 1.5
        lo, hi = a, a + sgn * step
        for _ in range(60):
            m = (lo + hi) / 2
            if T1(m, sg) > h: lo = m
            else: hi = m
        return (lo + hi) / 2
    return side(+1) - side(-1)


def refine(sg, E, T, i):
    a, b = E[i - 1], E[i + 1]
    for _ in range(80):
        m1, m2 = a + (b - a) / 3, b - (b - a) / 3
        if T1(m1, sg) < T1(m2, sg): a = m1
        else: b = m2
    return (a + b) / 2


def resonances(N, V0, D, P, Emax=2.65):
    sg = segs(N, V0, D, P); ii, E, T = peaks(sg, E1=Emax)
    return [refine(sg, E, T, i) for i in ii], sg


def finite_well(V0, L):
    """Bound levels of a square well of depth V0 and width L (even: k tan(kL/2) = kappa; odd: -k cot(kL/2) = kappa), by bisection."""
    E = np.linspace(1e-4, V0 - 1e-4, 40000); out = []
    for f in (lambda e: np.sqrt(2*e) * np.tan(np.sqrt(2*e) * L / 2) - np.sqrt(2*(V0-e)),
              lambda e: -np.sqrt(2*e) / np.tan(np.sqrt(2*e) * L / 2) - np.sqrt(2*(V0-e))):
        F = f(E)
        for i in range(len(E) - 1):
            if F[i] < 0 <= F[i + 1] and abs(F[i + 1] - F[i]) < 5: out.append(bis(f, E[i], E[i + 1]))
    return sorted(out)


def xi(E, V0, D, P):
    """Half the trace of one period's transfer matrix (Kronig-Penney): cos(qP) = Re(e^{-ikP} / t), t of one barrier centred at the
    origin in tm.py's convention (transmitted wave t e^{ikx}). Checked: the N - 1 roots of xi = cos(j pi / N) give T_N = 1 exactly."""
    t = tm.solve(E, segs(1, V0, D, P))[0]; k = np.sqrt(2 * E)
    return float(np.real(np.exp(-1j * k * P) / t))


def U(n, x):
    """Chebyshev polynomial of the second kind, U_n(x), by its recursion U_{n+1} = 2x U_n - U_{n-1}."""
    a, b = 1.0, 2 * x
    if n == 0: return a
    for _ in range(n - 1): a, b = b, 2 * x * b - a
    return b


def TN_formula(E, N, V0=2.0, D=1.0, P=2.5):
    T = T1(E, segs(1, V0, D, P)); return 1 / (1 + (1 - T) / T * U(N - 1, xi(E, V0, D, P)) ** 2)


# ---------- runs ----------
def runs(**kw):
    out = []
    for r in RUNS:
        s = r['spec']
        if all(abs(s[k] - v) < 1e-9 if isinstance(v, float) else s[k] == v for k, v in kw.items()): out.append(r)
    return sorted(out, key=lambda r: r['spec']['E'])


def through(r):   # generation 2026-11-18: the reference transmission of every run (walls exact; discs and shells the (x, rho) run)
    return r.get('T_ref')


def nearest(rs, E):
    return min(rs, key=lambda r: abs(r['spec']['E'] - E)) if rs else None


base = dict(N=2, V0=2.0, D=1.0, bias=0.0, sx=3.0)

OR = OLD['runs']
put('n_runs', len(RUNS), 'index.json (2026-11-18): runs filed')
put('n_dup', sum(1 for r in RUNS if len(r.get('groups', [])) > 1), 'index.json: specs computed in two groups, filed once')
put('n_replaced', len(OLD.get('replaced', [])), '2026-11-14 index replaced: runs the fix notebook reran')
put('run_tmin', round(min(r['t_end'] for r in OR)), 'shortest run length t_end, 2026-11-14')
put('run_tmax', round(max(r['t_end'] for r in OR)), 'longest run length t_end, 2026-11-14')
put('start_in_max', float(f"{max(r['start_in_barrier'] for r in OR):.1e}"), 'largest share of a start packet inside a barrier, 2026-11-14')
put('n_planned', 3739, 'rt3d2_run.py jobs(): the whole batch')
put('n_nb', len(OLD['notebooks']), '2026-11-14 index: notebooks filed')
put('gpu_h', round(sum(n.get('sweep_s', 0) for n in OLD['notebooks']) / 3600, 1), '2026-11-14 notebooks: sum of sweep_s (clock hours, two T4 each)')
put('gpu_ns', round(sum(r['wall'] for r in OR) / sum(float(np.prod(r['box'])) * r['steps'] for r in OR) * 1e9, 2), '2026-11-14 runs: sum of wall / sum of grid points x steps')
# ---------- the correction (2026-11-18) ----------
def cnt(**kw): return sum(1 for r in RUNS if all(r.get(k) == v if k != 'shape' else r['spec']['shape'] == v for k, v in kw.items()))
for sh, nm in (('flat', 'w'), ('coin', 'd'), ('shell', 's')):
    put(f'c_{nm}_n', cnt(shape=sh), f'{sh}: runs'); put(f'c_{nm}_kept', cnt(shape=sh, status='kept'), f'{sh}: kept (stored file passes the gate)')
    put(f'c_{nm}_new', cnt(shape=sh, status='rebuilt') + cnt(shape=sh, status='recomputed'), f'{sh}: rebuilt or recomputed')
    put(f'c_{nm}_prov', sum(1 for r in RUNS if r['spec']['shape'] == sh and r.get('provisional')), f'{sh}: provisional (T_unc > 0.005)')
    er = [abs(r['error']) for r in RUNS if r['spec']['shape'] == sh and r.get('error') is not None]
    if er: put(f'c_{nm}_err_med', r3(float(np.median(er)), 2), f'{sh}: median |T_old - T_ref|'); put(f'c_{nm}_err_max', r3(max(er), 2), f'{sh}: largest |T_old - T_ref|')
    un = [r['T_unc'] for r in RUNS if r['spec']['shape'] == sh and r.get('T_unc') is not None]
    if un: put(f'c_{nm}_unc_med', r3(float(np.median(un)), 1), f'{sh}: median T_unc'); put(f'c_{nm}_unc_max', r3(max(un), 2), f'{sh}: largest T_unc')
    dr = [r['drift'] for r in RUNS if r['spec']['shape'] == sh and r.get('drift') is not None]
    if dr: put(f'c_{nm}_drift_max', r3(max(dr), 2), f'{sh}: largest complex64 norm drift of the (x, rho) runs')
put('c_w_closure_max', r3(max(r['closure_max'] for r in RUNS if r.get('closure_max') is not None), 2), 'walls: largest |P_left + P_struct + P_right - 1| of the exact runs')
put('c_n_new', OUT['c_w_new'] + OUT['c_d_new'] + OUT['c_s_new'], 'runs replaced in all'); put('c_n_prov', OUT['c_w_prov'] + OUT['c_d_prov'] + OUT['c_s_prov'], 'provisional in all')
A1 = json.load(open(os.path.join(AUD, 'twin_sources.json'))); A2 = json.load(open(os.path.join(AUD, 'twin_converge.json')))
for i, a in enumerate(A1):
    tg = f'au{i}'
    put(tg + '_E', a['spec']['E'], 'audit case: ' + json.dumps(a['spec'])); put(tg + '_V0', a['spec']['V0'], 'audit case'); put(tg + '_sx', a['spec']['sx'], 'audit case')
    for k in ('exact', 'stored', 'dx0.25', 'dx0.125', 'dt0.0025', 'box x2'):
        put(tg + '_' + k.replace('.', '').replace(' ', ''), r3(a[k]), 'twin_sources.json: the twin at the stored grid (stored), varied one source at a time')
for i, c in enumerate(A2['conv']):
    for k, v in c['T'].items():
        put(f'cv{i}_' + k.replace('.', '').replace('|', '_'), r3(v), 'twin_converge.json: the twin with a cell-averaged potential, dx|dt')
    put(f'cv{i}_exact', r3(c['exact']), 'twin_converge.json: exact packet average')
# method figures of the correction runs, quoted from their records (not in an index): notes/fig15/CORRECTION_LOG.md 3.1-3.3, 7;
# notes/fig15/THEORY_AND_CODE.md 3.2, 3.4, 9.1-9.3
for k, v, src in (('m_slices', 2000, 'THEORY_AND_CODE 3.2: flat slices of the ramp under bias'), ('m_slices2', 8000, 'same, refined'),
                  ('m_slices_dT', 8e-9, 'THEORY_AND_CODE 3.2: change of T from 2,000 to 8,000 slices'), ('m_dk', 5e-4, 'THEORY_AND_CODE 3.4: k step'),
                  ('m_dk_dT', 3e-6, 'THEORY_AND_CODE 3.4: change of T when the k step is halved'), ('m_hx', 0.0625, 'THEORY_AND_CODE 8.2: x cell of the (x, rho) runs'),
                  ('m_conv', 0.0019, 'THEORY_AND_CODE 9.2: largest change of disc T under any refinement tested'),
                  ('m_wl_c64', 0.1965, 'CORRECTION_LOG 7: (x, rho) wall limit, N2 E0.75, complex64 (0.196539)'), ('m_wl_ex', 0.1968, 'same, exact 0.196820'),
                  ('m_c128_d', 6e-4, 'THEORY_AND_CODE 9.1: complex64 against complex128, discs'), ('m_c128_s', 0.0012, 'same, the one shell checked'),
                  ('m_rmax_s', 160, 'THEORY_AND_CODE 8.2: radial range of the shell runs, a'), ('m_rmax_d', 64, 'same, discs')):
    put(k, v, src)
pe, ps = A2['peak']['exact']['peak'], A2['peak']['stored dx0.5 step']['peak']
kap = np.sqrt(2 * (3.0 - pe)); Le = 1.5 + 2 / kap
put('pk_rel', round(100 * (pe - ps) / pe, 1), 'per cent the first grid lowers the V0 = 3 resonance')
put('pk_kap', round(kap, 2), 'kappa at the exact V0 = 3 resonance'); put('pk_Leff', round(Le, 2), 'L_eff = L + 2/kappa, L = 1.5')
put('pk_dL', round((pe - ps) / pe / 2 * Le, 3), 'by (21), dL_eff = (dE/E) L_eff / 2: how much wider the well acts on the first grid')
for k, v in A2['peak'].items():
    put('pk_' + k.replace(' ', '_').replace('.', ''), round(v['peak'], 3), 'twin_converge.json: V0 = 3 resonance from a sweep of long packets (sx 24), peak by a parabola')
put('planned', dict(A=4 * 6 * 47, B=2 * 2 * 47, C=4 * 3 * 47, D=8 * 47, E=3 * 3 * 47, F=2 * 20 * 25, G=60), 'rt3d2_run.py jobs(): A 4 P x 6 shapes x 47 E; B 2 R x 2 P x 47; C 4 x 3 x 47; D 8 x 47; E 3 N x 3 x 47; F 2 x 20 V x 25 E; G 60 (notes/fig15/STATE.md)')

# ---------- 1. spacing ----------
for P in (2.5, 3.5, 4.5, 5.5):
    Es, sg = resonances(2, 2.0, 1.0, P)
    tag = f'P{P:g}'.replace('.', '_')
    put(f'{tag}_n', len([e for e in Es if e < 2.0]), f'tm.py: resonances below V0 = 2, walls P = {P}')
    put(f'{tag}_E1', round(Es[0], 3), f'tm.py: first resonance, walls P = {P}')
    if len(Es) > 1: put(f'{tag}_E2', round(Es[1], 3), f'tm.py: second resonance, walls P = {P}')
    put(f'{tag}_all', [round(e, 3) for e in Es if e < 2.0], f'tm.py: every resonance below V0 = 2, walls P = {P}')
    up = [e for e in Es if e >= 2.0]
    if up: put(f'{tag}_Eup', round(up[0], 3), 'first full-transmission peak above the barrier top'); put(f'{tag}_Gup', r3(width(sg, up[0])), 'its FWHM')
    G = width(sg, Es[0]); put(f'{tag}_G1', r3(G), f'tm.py: FWHM of the first resonance, P = {P}')
    put(f'{tag}_tau1', r3(1 / G), f'1/Gamma, P = {P}')
    L = P - 1.0; k1 = np.sqrt(2 * (2.0 - Es[0]))
    put(f'{tag}_Ebox', round(np.pi ** 2 / (2 * L ** 2), 3), f'pi^2/(2 L^2), L = P - D = {L}')
    fw = finite_well(2.0, L); put(f'{tag}_Efw', [round(e, 3) for e in fw], f'levels of the finite well, depth 2, width {L} (barriers infinitely thick)')
    put(f'{tag}_Eeff', round(np.pi ** 2 / (2 * (L + 2 / k1) ** 2), 3), f'pi^2/(2 (L + 2/kappa)^2), kappa at E1')
    rs = runs(shape='flat', P=P, R=0.0, **base); r = nearest(rs, Es[0])
    if r and abs(r['spec']['E'] - Es[0]) <= 0.05:
        put(f'{tag}_run_E', r['spec']['E'], r['file']); put(f'{tag}_run_tau', r3(r['tau']['tau'] if r.get('tau') else None), r['file'])
        put(f'{tag}_run_status', r['status'], 'kept: the stored 3D file; rebuilt: the exact wall file')
    else:
        put(f'{tag}_run_E', None, f'missing: walls P = {P} near E = {Es[0]:.3f}'); put(f'{tag}_run_tau', None, 'missing')

# ---------- 2. height and thickness ----------
for V0, D, P in ((1.5, 1.0, 2.5), (2.0, 1.0, 2.5), (3.0, 1.0, 2.5), (2.0, 1.5, 3.0), (2.0, 2.0, 3.5)):
    Es, sg = resonances(2, V0, D, P); G = width(sg, Es[0]); tag = f'V{V0:g}D{D:g}'.replace('.', '_')
    kap = np.sqrt(2 * (V0 - Es[0])); Tone = T1(Es[0], segs(1, V0, D, P))
    put(f'{tag}_E1', round(Es[0], 3), f'tm.py: first resonance, V0 = {V0}, D = {D}, P = {P}')
    put(f'{tag}_G1', r3(G), 'tm.py: its FWHM'); put(f'{tag}_tau1', r3(1 / G), '1/Gamma')
    put(f'{tag}_kd', round(kap * D, 2), 'kappa D at E1'); put(f'{tag}_T1', r3(Tone), 'tm.py: one barrier alone at E1')
    Leff = P - D + 2 / kap; v = np.sqrt(2 * Es[0])
    put(f'{tag}_GoT', round(G / Tone, 2), 'Gamma / T1 (the leak model says v / L_eff)'); put(f'{tag}_vL', round(v / Leff, 2), 'v / L_eff, L_eff = P - D + 2/kappa')
    put(f'{tag}_Gest', r3(Tone * v / Leff), 'Gamma estimate T1 v / L_eff')
    put(f'{tag}_Tthick', r3(16 * Es[0] * (V0 - Es[0]) / V0 ** 2 * np.exp(-2 * kap * D)), 'thick-barrier T1 = 16 E (V0 - E)/V0^2 e^{-2 kappa D}')
    sE3, sE12 = np.sqrt(2 * Es[0]) / 6, np.sqrt(2 * Es[0]) / 24
    put(f'{tag}_Tbar3_est', r3(np.sqrt(np.pi / 8) * G / sE3), 'sqrt(pi/8) Gamma / sigma_E, sigma_x = 3 (valid when sigma_E >> Gamma)')
    put(f'{tag}_Tbar12_est', r3(np.sqrt(np.pi / 8) * G / sE12), 'same, sigma_x = 12')
    rs = runs(shape='flat', V0=V0, D=D, P=P, R=0.0, N=2, bias=0.0, sx=3.0); r = nearest(rs, Es[0])
    ok = r and abs(r['spec']['E'] - Es[0]) <= 0.05 and r.get('tau')
    put(f'{tag}_run_E', r['spec']['E'] if ok else None, r['file'] if ok else 'missing')
    put(f'{tag}_run_tau', r3(r['tau']['tau']) if ok else None, r['file'] if ok else 'missing')
    put(f'{tag}_run_tend', r3(r['t_end']) if ok else None, 'run length t_end'); put(f'{tag}_run_t0', r3(r['tau']['t0']) if ok else None, 'start of the fit window')
    put(f'{tag}_run_status', r['status'] if ok else None, 'kept or rebuilt')
    # the long packet (G) across this resonance, if computed
    g = runs(shape='flat', V0=V0, D=D, P=P, R=0.0, N=2, bias=0.0, sx=12.0)
    if g:
        best = max(g, key=lambda r: through(r) or 0)
        put(f'{tag}_long_T', r3(through(best)), best['file']); put(f'{tag}_long_n', len(g), 'G runs filed for this structure')
        put(f'{tag}_long_E', best['spec']['E'], best['file'])
        atE = nearest(g, Es[0]); put(f'{tag}_long_atE_E', atE['spec']['E'], atE['file']); put(f'{tag}_long_atE_T', r3(through(atE)), atE['file'])
        put(f'{tag}_long_status', sorted(set(x['status'] for x in g)), 'statuses of these runs')
        ek = f'2|{V0:g}|{D:g}|{P:g}|12'
        if ek in IDX['exact']:
            exact1d.SIG0 = 12.0; put(f'{tag}_long_exact', r3(exact1d.tbar(best['spec']['E'], segs(2, V0, D, P), nk=2001)), 'exact1d.tbar, sigma_x 12, at the run energy (quadrature)')
            put(f'{tag}_long_atE_exact', r3(exact1d.tbar(atE['spec']['E'], segs(2, V0, D, P), nk=2001)), 'exact1d.tbar, sigma_x 12, at the energy of the run nearest E1')
            put(f'{tag}_long_tend', round(best['t_end']), best['file'])
            dv = [abs(through(x) - exact1d.tbar(x['spec']['E'], segs(2, V0, D, P), nk=4001)) for x in g]
            put(f'{tag}_long_dev', float(f'{max(dv):.1e}'), 'largest |T_ref - exact1d.tbar| over the 15 long-packet runs of this structure')
    s3 = runs(shape='flat', V0=V0, D=D, P=P, R=0.0, N=2, bias=0.0, sx=3.0); r = nearest(s3, Es[0])
    ok = r is not None and abs(r['spec']['E'] - Es[0]) <= 0.05
    put(f'{tag}_short_T', r3(through(r)) if ok else None, r['file'] if ok else 'missing: short packet within 0.05 of E1')
    put(f'{tag}_short_E', r['spec']['E'] if ok else None, r['file'] if ok else 'missing')
    for sx in (3, 12):
        key = f'2|{V0:g}|{D:g}|{P:g}|{sx}'
        if key in IDX['exact']:
            e = IDX['exact'][key]
            exact1d.SIG0 = float(sx); tq = exact1d.tbar(Es[0], segs(2, V0, D, P), nk=2001)
            put(f'{tag}_Tbar{sx}', r3(tq), f'exact1d.tbar: packet average (18) at the unrounded E1 by quadrature (index.json exact[{key}] holds the same curve on a 0.01 grid)')

# ---------- the Fabry-Perot form of the running example ----------
def theta(E, V0=2.0, D=1.0, P=2.5):
    t, r = tm.solve(E, segs(1, V0, D, P))[:2]; return 2 * np.angle(r) + 2 * np.sqrt(2 * E) * P, abs(r) ** 2
Er = resonances(2, 2.0, 1.0, 2.5)[0][0]; th0, Rr = theta(Er); h = 1e-5   # the unrounded resonance
thp = ((theta(Er + h)[0] - theta(Er - h)[0] + np.pi) % (2 * np.pi) - np.pi) / (2 * h)
d0 = float(abs((th0 + np.pi) % (2 * np.pi) - np.pi)); put('FP_theta_mod', float(f'{d0:.1e}'), 'distance of the round-trip phase 2 arg r + 2 k s from a whole number of turns, at the unrounded E_r')
put('FP_tp', round(float(thp), 2), 'hbar d theta / dE at E_r: the round-trip time')
put('FP_2Lv', round(float(2 * (1.5 + 2 / np.sqrt(2 * (2 - Er))) / np.sqrt(2 * Er)), 2), '2 L_eff / v at E_r')
put('FP_R', round(float(Rr), 3), 'R of one barrier at E_r')
put('FP_G', r3(float(2 * (1 - Rr) / (np.sqrt(Rr) * thp))), 'Gamma = 2 T / (sqrt(R) theta prime)')
put('FP_lnR', round(float(-2 * np.log(Rr)), 4), '-2 ln R: exact decay per round trip (probability R^2 left after two reflections)')
put('FP_2TsR', round(float(2 * (1 - Rr) / np.sqrt(Rr)), 4), '2 T / sqrt(R): what the Lorentzian width gives')
put('FP_2T', round(float(2 * (1 - Rr)), 4), '2 T: two leaks per round trip, counted naively')
put('t_arrive', round(14 / np.sqrt(2 * 0.735), 1), 'time for the short packet centre to cover the 14 a from x0 to the first face at E = 0.735')
put('spread_arr', round(3 * np.sqrt(1 + ((14 / np.sqrt(2 * 0.735)) / 18) ** 2), 1), 'sigma_perp at that time')
put('spread_t40', round(3 * np.sqrt(1 + (40 / (2 * 9)) ** 2), 1), 'sigma_perp(t) = sigma_perp sqrt(1 + (t / 2 sigma_perp^2)^2), sigma_perp = 3, t = 40')

# ---------- 3. N barriers ----------
Eg = np.linspace(0.05, 2.65, 5201); X = np.array([xi(e, 2.0, 1.0, 2.5) for e in Eg]); inb = np.abs(X) <= 1
coarse = [Eg[i] for i in range(1, len(Eg)) if inb[i] != inb[i - 1]]
edges = [bis(lambda e: abs(xi(e, 2.0, 1.0, 2.5)) - 1, c - 0.001, c + 0.001) for c in coarse]
put('band1_lo', round(edges[0], 3), 'tm.py: |xi| = 1, bottom of the first band, V0 2, D 1, P 2.5')
put('band1_hi', round(edges[1], 3), 'same, top of the first band')
put('band2_lo', round(edges[2], 3), 'same, bottom of the second band')
put('gap1', round(edges[2] - edges[1], 3), 'width of the first gap')
put('band1_w', round(edges[1] - edges[0], 3), 'width of the first band')
for Nb in (2, 3, 5, 10):
    Es = sorted(bis(lambda e: xi(e, 2.0, 1.0, 2.5) - np.cos(j * np.pi / Nb), edges[0] + 1e-9, edges[1] - 1e-9) for j in range(1, Nb))
    Tm = min(T1(e, segs(Nb, 2.0, 1.0, 2.5)) for e in Es)
    put(f'N{Nb}_npk', len(Es), f'xi = cos(j pi/N), j = 1..N-1, N = {Nb}; tm.py gives T_N >= {Tm:.9f} at each')
    put(f'N{Nb}_pk', [round(e, 3) for e in Es], 'their energies')
dev = max(abs(TN_formula(e, n) - T1(e, segs(n, 2.0, 1.0, 2.5))) for n in (2, 3, 5, 10) for e in np.linspace(0.1, 2.6, 251))
put('TN_check', float(f'{dev:.1e}'), 'max |T_N(formula) - T_N(tm.py)| over N = 2, 3, 5, 10 and 251 energies 0.1 ... 2.6')
FIG = []
W, H0, X0, X1, EA, EB = 720, 300, 64, 700, 0.3, 1.3
def X(e): return X0 + (e - EA) / (EB - EA) * (X1 - X0)
FIG.append(f'<rect x="0" y="0" width="{W}" height="{H0}" fill="#fff"/>')
FIG.append(f'<rect x="{X(edges[0]):.1f}" y="8" width="{X(edges[1]) - X(edges[0]):.1f}" height="256" fill="#a3303f" fill-opacity=".07"/>')
for j, Nb in enumerate((2, 3, 5, 10)):
    y0 = 8 + j * 64; yb = y0 + 56
    FIG.append(f'<line x1="{X0}" y1="{yb}" x2="{X1}" y2="{yb}" stroke="#1c1518" stroke-width="1"/>')
    FIG.append(f'<line x1="{X0}" y1="{y0 + 6}" x2="{X1}" y2="{y0 + 6}" stroke="#d9d2cb" stroke-width="1" stroke-dasharray="3 3"/>')
    pts = ' '.join(f'{X(e):.1f},{yb - 50 * T1(e, segs(Nb, 2.0, 1.0, 2.5)):.1f}' for e in np.linspace(EA, EB, 1001))
    FIG.append(f'<polyline points="{pts}" fill="none" stroke="#a3303f" stroke-width="1.4"/>')
    FIG.append(f'<text class="mu" x="8" y="{y0 + 34}">N = {Nb}</text>')
for e in (0.4, 0.6, 0.8, 1.0, 1.2):
    FIG.append(f'<line x1="{X(e):.1f}" y1="256" x2="{X(e):.1f}" y2="263" stroke="#1c1518" stroke-width="1"/>')
    FIG.append(f'<text class="mu" x="{X(e) - 10:.1f}" y="292">{e:.1f}</text>')
FIG.append(f'<text class="mu" x="{X(edges[0]) + 4:.1f}" y="22" style="fill:#7a1f2b">band</text>')
FIG.append(f'<text class="mu" x="{X(1.1):.1f}" y="22" style="fill:#5a504b">gap</text>')
FIG.append(f'<text class="m" x="{X1 - 14}" y="292">E</text>')
FIGSVG = ''.join(FIG)

for Nb in (3, 5, 10):
    rs = runs(shape='flat', N=Nb, V0=2.0, D=1.0, P=2.5, R=0.0, bias=0.0, sx=3.0)
    ins = [r for r in rs if edges[0] <= r['spec']['E'] <= edges[1]]; gap = [r for r in rs if edges[1] < r['spec']['E'] < (edges[2] if len(edges) > 2 else 9)]
    put(f'N{Nb}_run_band', [(r['spec']['E'], r3(through(r))) for r in ins], 'walls, the 1D twin T, energies inside the first band')
    put(f'N{Nb}_run_gap', [(r['spec']['E'], r3(through(r))) for r in gap], 'walls, energies in the first gap')
    put(f'N{Nb}_files', [r['file'] for r in ins + gap], 'files')
    bi = [through(r) for r in ins]; gi = [through(r) for r in gap if r['spec']['E'] <= 1.6 and r['spec']['E'] >= edges[1] + 0.1]
    put(f'N{Nb}_band_mean', r3(float(np.mean(bi))) if bi else None, f'mean share through over {len(bi)} band energies')
    put(f'N{Nb}_band_n', len(bi), 'band runs averaged'); put(f'N{Nb}_band_lo', min(r['spec']['E'] for r in ins) if ins else None, 'lowest'); put(f'N{Nb}_band_hi', max(r['spec']['E'] for r in ins) if ins else None, 'highest'); put(f'N{Nb}_gap_n', len(gi), 'gap runs averaged')
    put(f'N{Nb}_gap_mean', r3(float(np.mean(gi))) if gi else None, f'mean share through over {len(gi)} energies from band top + 0.1 to 1.6')
    ek = f'{Nb}|2|1|2.5|3'
    if ek in IDX['exact']:
        e = IDX['exact'][ek]
        bE = [r['spec']['E'] for r in ins]; gE = [r['spec']['E'] for r in gap if edges[1] + 0.1 <= r['spec']['E'] <= 1.6]
        put(f'N{Nb}_band_exact', r3(float(np.mean(np.interp(bE, e['E'], e['Tbar'])))) if bE else None, f'exact packet average (18) at the same band energies, index.json exact[{ek}]')
        put(f'N{Nb}_gap_lo', round(min(gE), 2) if gE else None, 'lowest gap energy averaged'); put(f'N{Nb}_gap_hi', round(max(gE), 2) if gE else None, 'highest')
        put(f'N{Nb}_gap_exact', r3(float(np.mean(np.interp(gE, e['E'], e['Tbar'])))) if gE else None, 'same, gap energies')

# ---------- 4. discs and shells ----------
E1 = OUT['P2_5_E1']; wr = runs(shape='flat', P=2.5, R=0.0, **base)
walls = ([r for r in wr if abs(r['spec']['E'] - 0.75) < 1e-9] or [nearest(wr, E1)])[0]   # 0.75: the grid energy nearest E1
put('disc_walls_status', walls['status'], walls['file']); put('disc_E', walls['spec']['E'], 'the energy of the disc comparison: 0.75 (grid energy nearest E_r) once filed, else the nearest filed')
tw = walls['tau']['tau']; put('disc_tau_walls', r3(tw), walls['file']); put('disc_T_walls', r3(through(walls)), walls['file'])
w1 = [x for x in runs(shape='flat', N=1, V0=2.0, D=1.0, P=2.5, R=0.0, bias=0.0, sx=3.0) if abs(x['spec']['E'] - walls['spec']['E']) < 1e-9]
put('disc_T1_walls', r3(through(w1[0])) if w1 else None, w1[0]['file'] if w1 else 'missing: one wall')
for R in (2.0, 4.0, 6.0, 9.0, 12.0):
    tag = f'R{R:g}'
    r = [x for x in runs(shape='coin', P=2.5, R=R, **base) if abs(x['spec']['E'] - walls['spec']['E']) < 1e-9]
    one = [x for x in runs(shape='coin', N=1, V0=2.0, D=1.0, P=2.5, R=R, bias=0.0, sx=3.0) if abs(x['spec']['E'] - walls['spec']['E']) < 1e-9]
    if r and r[0].get('tau'):
        t = r[0]['tau']['tau']; put(f'{tag}_tau', r3(t), r[0]['file']); put(f'{tag}_T', r3(through(r[0])), r[0]['file'])
        put(f'{tag}_status', r[0]['status'], 'kept (stored 3D file) or recomputed ((x, rho) file)'); put(f'{tag}_prov', bool(r[0].get('provisional')), 'T_unc > 0.005')
        put(f'{tag}_unc', r3(r[0].get('T_unc') or 0, 2), 'T_unc of the pair run')
        put(f'{tag}_tau_side', r3(1 / (1 / t - 1 / tw)) if t < tw else None, '1/(1/tau - 1/tau_walls)')
        put(f'{tag}_tau_side_rnd', r3(1 / (1 / r3(t) - 1 / r3(tw))) if r3(t) < r3(tw) else None, 'the same from the rounded lifetimes printed in the table')
    else:
        put(f'{tag}_tau', None, f'missing: discs R {R} at E {walls["spec"]["E"]}'); put(f'{tag}_T', None, 'missing'); put(f'{tag}_tau_side', None, 'missing')
    put(f'{tag}_T1', r3(through(one[0])) if one else None, one[0]['file'] if one else 'missing: one disc')
    put(f'{tag}_T1_status', one[0]['status'] if one else None, 'one disc: kept or recomputed')
    put(f'{tag}_gain', round(through(r[0]) / through(one[0]), 2) if (r and one) else None, 'pair share / one-disc share, unrounded')
for R in (3.0, 5.0):
    for P in (2.5, 3.5):
        rs = [r for r in runs(shape='shell', N=2, R=R, P=P, V0=2.0, D=1.0, bias=0.0, sx=3.0) if r.get('tau')]
        tag = f'sh{R:g}_{P:g}'.replace('.', '_')
        if rs:
            b = max(rs, key=lambda r: r['tau']['tau'])
            put(f'{tag}_taumax', r3(b['tau']['tau']), b['file']); put(f'{tag}_taumax_E', b['spec']['E'], b['file'])
            put(f'{tag}_n', len(rs), 'shell runs with a fitted lifetime')
            put(f'{tag}_cut', bool(b['tau']['t1'] >= b['t_end'] - 2 * b['frame_dt'] and (b['tau']['t1'] - b['tau']['t0']) < b['tau']['tau']), 'True: the fit window ends at the end of the run AND spans less than one lifetime')
            put(f'{tag}_minE', min(r['spec']['E'] for r in rs), 'lowest energy of the runs for this pair')
            put(f'{tag}_T', r3(through(b)), 'T_ref of that run'); put(f'{tag}_unc', r3(b.get('T_unc'), 2), 'its T_unc'); put(f'{tag}_prov', bool(b.get('provisional')), 'provisional')
    one = [r for r in runs(shape='shell', N=1, R=R, V0=2.0, D=1.0, bias=0.0, sx=3.0) if r.get('tau')]
    if one:
        b1 = max(one, key=lambda r: r['tau']['tau'])
        put(f'sh1_{R:g}_taumax', r3(b1['tau']['tau']), b1['file']); put(f'sh1_{R:g}_taumax_E', b1['spec']['E'], b1['file'])
        put(f'sh1_{R:g}_cut', bool(b1['tau']['t1'] >= b1['t_end'] - 2 * b1['frame_dt'] and (b1['tau']['t1'] - b1['tau']['t0']) < b1['tau']['tau']), 'one shell: fit window cut by the run end')
for R in (12.0,):
    g = runs(shape='coin', V0=2.0, D=1.0, P=2.5, R=R, N=2, bias=0.0, sx=12.0)
    if g:
        best = max(g, key=lambda r: through(r) or 0)
        put('R12_long_T', r3(through(best)), best['file']); put('R12_long_E', best['spec']['E'], best['file']); put('R12_long_prov', sum(1 for x in g if x.get('provisional')), 'provisional among them')
for sh, nm in (('flat', 'w'), ('coin', 'd')):
    q = [(r['T_old'] / r['T_ref']) for r in RUNS if r['spec']['shape'] == sh and r['spec']['bias'] == 0 and r['spec']['N'] == 2 and r['spec']['V0'] == 2.0 and r['spec']['D'] == 1.0 and r['spec']['P'] == 2.5 and r['spec']['sx'] == 3.0 and r.get('T_old') and r['T_ref'] > 1e-3 and (sh == 'flat' or r['spec']['R'] == 6.0)]
    put(f'gq_{nm}_lo', round(min(q), 2), f'{sh} running example (discs R 6): smallest T_old / T_ref'); put(f'gq_{nm}_hi', round(max(q), 2), 'largest')
for tg, kw in (('ge_V2D2', dict(V0=2.0, D=2.0, P=3.5)), ('ge_V3D1', dict(V0=3.0, D=1.0, P=2.5)), ('ge_V2D1', dict(V0=2.0, D=1.0, P=2.5))):
    rs = [x for x in runs(shape='flat', N=2, bias=0.0, sx=3.0, R=0.0, **kw) if x.get('T_old') and x['T_ref'] > 1e-3]
    q = [x['T_old'] / x['T_ref'] for x in rs]
    put(tg + '_lo', round(min(q), 2), 'smallest T_old / T_ref (the 2026-11-14 run against the exact wall), stored energies'); put(tg + '_hi', round(max(q), 2), 'largest')
put('gpu_run_h', round(sum(r['wall'] for r in OR) / 3600, 1), '2026-11-14 runs: sum of wall, hours on one GPU each')

# ---------- 5. the diode ----------
iv.V0 = 2.0
Eg = np.linspace(0.02, 1.2, 2400)
for B in (0.0, 0.5, 1.0):
    T = np.array([iv.T_biased(e, 2.5, B, nper=60) for e in Eg]); i = int(np.argmax(T))
    put(f'Er_bias{B:g}'.replace('.', '_'), round(float(Eg[i]), 3), f'iv.py T_biased: transmission peak at bias {B}, walls P 2.5')
    put(f'Tpk_bias{B:g}'.replace('.', '_'), r3(float(T[i])), f'iv.py T_biased: height of that peak (below 1: the tilted barriers differ)')
def supf(E, V, EF=1.0, kT=0.05): return np.log((1 + np.exp((EF - E) / kT)) / (1 + np.exp((EF - E - V) / kT)))
Ef = np.linspace(0.005, 1.3, 2600)
for B in (0.0, 0.875, 1.25):
    T = np.array([iv.T_biased(e, 2.5, B, nper=60) for e in Ef]); i = int(np.argmax(T[:2000])); m = (Ef > Ef[i] - 0.25) & (Ef < Ef[i] + 0.25)
    tg = f'{B:g}'.replace('.', '_')
    put(f'area_b{tg}', round(float(np.trapezoid(T[m], Ef[m])), 3), f'iv.py: area under the transmission peak (+-0.25 around it) at bias {B}')
    put(f'sup_b{tg}', round(float(supf(Ef[i], B)), 1), f'supply function at the peak energy, bias {B}')
    put(f'prod_b{tg}', round(float(np.trapezoid(T[m], Ef[m]) * supf(Ef[i], B)), 2), 'area x supply, from the unrounded values')
    put(f'lev_b{tg}', round(float(Ef[i]), 2), f'iv.py: energy of the transmission peak (the level) at bias {B}')
    put(f'tpk_b{tg}', round(float(T[i]), 2), f'iv.py: height of the transmission peak at bias {B}')
    h_ = T[i] / 2; lo = i
    while T[lo] > h_: lo -= 1
    hi = i
    while T[hi] > h_: hi += 1
    put(f'fw_b{tg}', round(float(Ef[hi] - Ef[lo]), 3) if B else OUT['V2D1_G1'], f'iv.py: full width at half its height of that peak (grid {Ef[1]-Ef[0]:.4f})')
x = EX1['iv']
put('iv_exact_Vp', x['V_peak'], 'exact-1d.json iv'); put('iv_exact_Vv', round(x['V_valley'], 3), 'exact-1d.json iv')
put('iv_exact_pvr', round(x['pvr'], 1), 'exact-1d.json iv')
for c in IDX['iv']:
    tag = 'iv_walls' if c['shape'] == 'flat' else f'iv_disc{c["R"]:g}'
    J = c['J_runs']
    if not J: continue
    Vs = [p[0] for p in J]; Js = [p[1] for p in J]; ip = int(np.argmax(Js[:len(Js) * 3 // 4]))
    iv_ = ip + int(np.argmin(Js[ip:]));
    put(f'{tag}_Vp', Vs[ip], 'index.json iv J_runs: current peak'); put(f'{tag}_Vv', Vs[iv_], 'index.json iv J_runs: valley after it')
    put(f'{tag}_pvr', round(Js[ip] / Js[iv_], 1), 'peak / valley')
    put(f'{tag}_Jp', round(Js[ip], 2), 'index.json iv J_runs: current at the peak'); put(f'{tag}_Jend', round(Js[-1], 2), 'index.json iv J_runs: current at the last voltage')
    put(f'{tag}_valley_at_end', iv_ == len(Js) - 1, 'True: the lowest current after the peak is at the last voltage computed')
    if c['shape'] == 'flat':
        # recomputed here at V0 = 2 and checked against the index's J_exact_single_energy_same_points (refiled at V0 = 2 on 14 Nov 2026)
        assert iv.V0 == 2.0
        Ei = np.round(np.arange(0.10, 1.3001, 0.05), 3); Xs = [float(np.trapezoid(iv.T_biased_vec(Ei, 2.5, V) * iv.supply(Ei, c['EF'], V, c['kT']), Ei)) for V in Vs]
        St = [x for x in OLD['iv'] if x['shape'] == 'flat'][0].get('J_exact_single_energy_same_points'); assert St and max(abs(q[1] - x) for q, x in zip(St, Xs)) < 1e-6, 'same-points curve differs from the 2026-11-14 filing'
        jp = int(np.argmax(Xs[:len(Xs) * 3 // 4])); jv = jp + int(np.argmin(Xs[jp:]))
        put(f'{tag}_xs_Vp', Vs[jp], 'iv.py at V0 = 2: exact single-energy T at the 25 run energies, same trapezoid sum: peak')
        put(f'{tag}_xs_Vv', Vs[jv], 'same: valley after it'); put(f'{tag}_xs_pvr', round(Xs[jp] / Xs[jv], 1), 'same: peak / valley')
    nF = len([r for r in RUNS if r['spec']['shape'] == c['shape'] and r['spec']['R'] == c['R'] and r['spec']['N'] == 2 and r['spec']['V0'] == 2
              and r['spec']['D'] == 1 and r['spec']['P'] == 2.5 and r['spec']['sx'] == 3 and round(r['spec']['E'], 3) in set(np.round(np.arange(0.10, 1.3001, 0.05), 3))])
    put(f'{tag}_prov', sum(1 for r in RUNS if r['spec']['shape'] == c['shape'] and r['spec']['R'] == c['R'] and r['spec']['N'] == 2 and r['spec']['V0'] == 2 and r['spec']['D'] == 1 and r['spec']['P'] == 2.5 and r['spec']['sx'] == 3 and r.get('provisional') and r['spec']['E'] <= 1.3001), 'provisional runs on the diode grid')
    put(f'{tag}_nruns', nF, 'runs on the diode grid (bias 0 ... 2.375 x energies 0.10 ... 1.30) filed so far; 500 planned')
    put(f'{tag}_J', [[p[0], r3(p[1])] for p in J], 'index.json iv J_runs')
    put(f'{tag}_complete', nF >= 500, 'all 20 voltages x 25 energies filed: only then are peak, valley and ratio quoted')

# ---------- 6. long packets ----------
put('dE_short', round(np.sqrt(2 * E1) / (2 * 3), 3), 'k0 / (2 sigma_x), sigma_x = 3, at E1 of the running example')
put('dE_long', round(np.sqrt(2 * E1) / (2 * 12), 3), 'k0 / (2 sigma_x), sigma_x = 12')
put('box_long', round(512 / 192, 2), 'Nx 512 for long packets against 192: the box is this many times longer')
put('dE_long_fwhm', round(2 * np.sqrt(2 * np.log(2)) * np.sqrt(2 * E1) / 24, 3), 'full width at half maximum of the long packet in energy, 2.355 sigma_E')
put('long_rerun_pending', False, 'the running example long-packet runs of shards 1-2 are on rt3d2_run.py FIX1 (ran >15 % short) until the fix notebook is filed')
g = runs(shape='flat', V0=2.0, D=1.0, P=2.5, R=0.0, N=2, bias=0.0, sx=12.0)
put('long_files', [r['file'] for r in g], 'G runs, walls of the running example')

for k, v, s in SRC:
    print(f'{k:22s} {json.dumps(v):40s} {s}')

if '--write' in sys.argv:
    src = open(NOTE).read()
    src, n = re.subn(r"/\* FIG2-BEGIN \*/.*?/\* FIG2-END \*/", lambda m: "/* FIG2-BEGIN */var FIG2 = '" + FIGSVG + "';/* FIG2-END */", src, flags=re.S)
    if n != 1: sys.exit('FIG2 block not found')
    block = 'var NUM = ' + json.dumps(OUT, separators=(',', ':')) + ';'
    new, n = re.subn(r'/\* NUM-BEGIN \*/.*?/\* NUM-END \*/', lambda m: '/* NUM-BEGIN */' + block + '/* NUM-END */', src, flags=re.S)
    if n != 1: sys.exit('NUM block not found in ' + NOTE)
    open(NOTE, 'w').write(new); print('wrote NUM into', NOTE)

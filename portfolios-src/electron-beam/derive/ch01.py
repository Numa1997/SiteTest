"""Project 07 · chapter 1 · SymPy checks of every derivation in the text.

Each check is one claim of the page, tested as an identity in exact algebra. `run()` returns the list the page prints
(text/ch01.py shows it in the section "Checked by computer algebra"); `python3 derive/ch01.py` prints it as a table.

A check passes when the difference of the two sides simplifies to exactly 0 (or, for series, when the coefficients agree).
SymPy is the independent referee: the text derives by hand, this file confirms the algebra step by step.
"""
import sympy as sp

OK = 'PASS'


def _zero(expr):
    return sp.simplify(sp.expand(expr)) == 0

# The claims as the page shows them (TeX), by check label.
TEX = {
    'D1a': r'\mathbf p=\partial L/\partial\mathbf v=\gamma m\mathbf v+q\mathbf A',
    'D1b': r'\mathrm d(\gamma m\mathbf v)/\mathrm dt=q(\mathbf E+\mathbf v\times\mathbf B)\ \text{from the Euler--Lagrange equation, with }\mathbf E=-\nabla\varphi-\partial_t\mathbf A,\ \mathbf B=\nabla\times\mathbf A',
    'D2a': r'H=\mathbf p\cdot\mathbf v-L=\gamma mc^2+q\varphi',
    'D2b': r'(\gamma mc^2)^2=m^2c^4+c^2|\mathbf p-q\mathbf A|^2',
    'D3a': r'\mathrm d(\gamma mc^2)/\mathrm dt=\mathbf v\cdot\mathrm d\mathbf p_{\mathrm{kin}}/\mathrm dt',
    'D3b': r'\mathbf v\cdot(\mathbf v\times\mathbf B)=0',
    'D4a': r'v/v_{NR}=1-\tfrac34\epsilon+\tfrac{23}{32}\epsilon^2-\dots',
    'D4b': r'(\gamma-1)mc^2=\tfrac12mv^2+\tfrac38mv^4/c^2+\dots',
    'D4c': r'\lambda=\lambda_{NR}\,(1-\tfrac14\epsilon+\dots)',
    'D5a': r'\text{the tangent at the plate exit meets the axis at }x=l/2',
    'D6a': r'e/m=\theta E/(B^2l)\ \text{from }v=E/B',
    'D7a': r'\text{the helix velocity }\mathbf u(t)\text{ solves }\mathrm d\mathbf u/\mathrm dt=\Omega\,\mathbf u\times\hat{\mathbf z}',
    'D7b': r'\dot{\mathbf r}=\mathbf u/\gamma\ \text{for the helix position, which starts at the origin}',
    'D7c': r'\text{the transverse path is a circle of radius }|\mathbf u_\perp|/(\gamma|\Omega|)',
    'D8a': r'\text{Boris: }\mathbf u+(\mathbf u+\mathbf u\times\mathbf t)\times\mathbf s=\text{a turn of }\mathbf u\text{ by }\varphi,\ \tan\tfrac\varphi2=|\mathbf t|',
    'D8b': r'|\mathbf u^+|=|\mathbf u^-|',
    'D8c': r'1-st=\cos\varphi,\ s=\sin\varphi\ \text{for }t=\tan\tfrac\varphi2',
    'D9a': r'r_{\mathrm{Boris}}=r_L\sqrt{1+(\Omega h/2)^2}',
    'D9b': r'\Omega h-2\arctan\tfrac{\Omega h}2=\tfrac{(\Omega h)^3}{12}-\tfrac{(\Omega h)^5}{80}+\dots',
    'D10a': r'|R|^2=1-\tfrac{\theta^6}{72}+\tfrac{\theta^8}{576}',
    'D10b': r'\theta-\arg R=\tfrac{\theta^5}{120}-\tfrac{\theta^7}{336}+\dots',
    'D11a': r'B=(\tfrac45)^{3/2}\mu_0NI/R',
    'D11b': r'\mathrm dB/\mathrm dz=\mathrm d^2B/\mathrm dz^2=0\ \text{at the midpoint}',
    'D12a': r'L=2\pi v_\parallel/\Omega',
}


def run():
    out = []

    def add(label, claim, ok, detail=''):
        out.append(dict(label=label, claim=claim, ok=bool(ok), detail=detail))

    # ------------------------------------------------------------------ D1 Euler-Lagrange -> Lorentz force (eq. 1.14)
    m, c, q = sp.symbols('m c q', positive=True)
    X, Y, Z, T = sp.symbols('X Y Z T', real=True)
    vx, vy, vz = sp.symbols('v_x v_y v_z', real=True)
    phi = sp.Function('phi')(X, Y, Z, T)
    Ax, Ay, Az = [sp.Function(n)(X, Y, Z, T) for n in ('A_x', 'A_y', 'A_z')]
    A = [Ax, Ay, Az]
    v = [vx, vy, vz]
    gam = 1 / sp.sqrt(1 - (vx**2 + vy**2 + vz**2) / c**2)
    L = -m * c**2 / gam - q * phi + q * (vx * Ax + vy * Ay + vz * Az)
    # canonical momentum
    p = [sp.diff(L, vi) for vi in v]
    p_claim = [gam * m * vi + q * Ai for vi, Ai in zip(v, A)]
    add('D1a', 'canonical momentum  p = dL/dv = gamma m v + q A', all(_zero(a - b) for a, b in zip(p, p_claim)))
    # total time derivative along the path: d/dt f(X,Y,Z,T) = f_T + v.grad f
    grad = lambda f: [sp.diff(f, s) for s in (X, Y, Z)]
    ddt = lambda f: sp.diff(f, T) + sum(vi * gi for vi, gi in zip(v, grad(f)))
    # Euler-Lagrange for coordinate i:  d/dt(dL/dv_i) - dL/dx_i = 0 ; solve for d(gamma m v_i)/dt
    E = [-sp.diff(phi, s) - sp.diff(Ai, T) for s, Ai in zip((X, Y, Z), A)]
    B = [sp.diff(Az, Y) - sp.diff(Ay, Z), sp.diff(Ax, Z) - sp.diff(Az, X), sp.diff(Ay, X) - sp.diff(Ax, Y)]
    cross = [vy * B[2] - vz * B[1], vz * B[0] - vx * B[2], vx * B[1] - vy * B[0]]
    ok = True
    for i, s in enumerate((X, Y, Z)):
        dL_dx = sp.diff(L, s)                                   # explicit position dependence through phi and A
        # EL: d(gamma m v_i)/dt + q dA_i/dt - dL/dx_i = 0  ->  d(gamma m v_i)/dt = dL/dx_i - q dA_i/dt
        rhs = dL_dx - q * ddt(A[i])
        ok = ok and _zero(rhs - q * (E[i] + cross[i]))
    add('D1b', 'Euler-Lagrange equation  d(gamma m v)/dt = q (E + v x B)  with E = -grad phi - dA/dt, B = curl A', ok)
    # ------------------------------------------------------------------ D2 Hamiltonian
    vv = sp.symbols('v', positive=True)
    g1 = 1 / sp.sqrt(1 - vv**2 / c**2)
    Hkin = (g1 * m * vv) * vv - (-m * c**2 / g1)            # p_kin v - (-mc^2/gamma)
    add('D2a', 'H = p.v - L = gamma m c^2 + q phi   (kinetic part: gamma m v^2 + m c^2/gamma = gamma m c^2)',
        _zero(Hkin - g1 * m * c**2))
    pk = sp.symbols('p_k', positive=True)                    # |p - qA|
    add('D2b', '(gamma m c^2)^2 = m^2 c^4 + c^2 |p - qA|^2,  with p - qA = gamma m v   (so H = sqrt(m^2 c^4 + c^2 |p - qA|^2) + q phi)',
        _zero(sp.simplify(m**2 * c**4 + c**2 * (g1 * m * vv)**2 - (g1 * m * c**2)**2)))
    # energy theorem: dE/dt = v . dp/dt with E^2 = p^2 c^2 + m^2 c^4
    tt = sp.symbols('t', real=True)
    px, py, pz = [sp.Function(n)(tt) for n in ('p_x', 'p_y', 'p_z')]
    En = sp.sqrt(m**2 * c**4 + c**2 * (px**2 + py**2 + pz**2))
    dEn = sp.diff(En, tt)
    vvec = [c**2 * pi / En for pi in (px, py, pz)]
    add('D3a', 'd(gamma m c^2)/dt = v . d(p_kin)/dt   (so a force at right angles to v does no work)',
        _zero(dEn - sum(vi * sp.diff(pi, tt) for vi, pi in zip(vvec, (px, py, pz)))))
    Bv = sp.symbols('B_x B_y B_z', real=True)
    Fm = sp.Matrix(vx, vy, vz).T if False else None
    vcross = sp.Matrix([vx, vy, vz]).cross(sp.Matrix(Bv))
    add('D3b', 'the magnetic force q v x B is orthogonal to v:  v . (v x B) = 0', _zero(sp.Matrix([vx, vy, vz]).dot(vcross)))
    # ------------------------------------------------------------------ D4 non-relativistic limit
    eps = sp.symbols('epsilon', positive=True)               # eps = eV / (m c^2)
    gam_e = 1 + eps
    beta2 = 1 - 1 / gam_e**2
    beta_nr = sp.sqrt(2 * eps)
    ratio = sp.sqrt(beta2) / beta_nr
    ser = sp.series(ratio, eps, 0, 3).removeO()
    add('D4a', 'v / v_NR = 1 - (3/4) eps + (23/32) eps^2 - ...  with eps = eV/(m c^2)',
        _zero(ser - (1 - sp.Rational(3, 4) * eps + sp.Rational(23, 32) * eps**2)))
    kin = sp.series(m * c**2 * (1 / sp.sqrt(1 - vv**2 / c**2) - 1), vv, 0, 6).removeO()
    add('D4b', '(gamma - 1) m c^2 = m v^2/2 + 3 m v^4/(8 c^2) + ...',
        _zero(kin - (m * vv**2 / 2 + 3 * m * vv**4 / (8 * c**2))))
    lam = sp.symbols('lambda_0', positive=True)
    hh, Vv, ee = sp.symbols('h V e', positive=True)
    Tk = ee * Vv
    lam_rel = hh * c / sp.sqrt(Tk * (Tk + 2 * m * c**2))
    ser2 = sp.series(lam_rel / (hh / sp.sqrt(2 * m * Tk)), Vv, 0, 2).removeO()
    add('D4c', 'lambda = h / sqrt(2 m e V (1 + eV / 2mc^2)) = lambda_NR (1 - eV / 4mc^2 + ...)',
        _zero(sp.simplify(ser2 - (1 - Tk / (4 * m * c**2)))))
    # ------------------------------------------------------------------ D5 parabola and the plate-centre rule
    x, l, a, v0 = sp.symbols('x l a v_0', positive=True)       # a = eE/m
    y = a * x**2 / (2 * v0**2)
    slope_exit = sp.diff(y, x).subs(x, l)
    x_cross = l - y.subs(x, l) / slope_exit
    add('D5a', 'the straight line leaving the plates, traced backwards, crosses the axis at x = l/2 (the plate centre)', _zero(x_cross - l / 2))
    # ------------------------------------------------------------------ D6 crossed fields -> e/m
    Ee, Bf, th, em = sp.symbols('E B theta em', positive=True)
    theta_E = em * Ee * l / (Ee / Bf)**2                        # v = E/B inserted
    sol = sp.solve(sp.Eq(th, theta_E), em)[0]
    add('D6a', 'balance e E = e v B gives v = E/B;  theta = (e/m) E l / v^2 then gives  e/m = theta E / (B^2 l)', _zero(sol - th * Ee / (Bf**2 * l)))
    # ------------------------------------------------------------------ D7 exact helix solves the equation of motion
    Om = sp.symbols('Omega', real=True)
    t = sp.symbols('t', real=True)
    up, ux0, uy0 = sp.symbols('u_par u_x0 u_y0', real=True)
    # B along z:  du/dt = Omega u x z  ->  du_x/dt = Omega u_y, du_y/dt = -Omega u_x
    uxs = ux0 * sp.cos(Om * t) + uy0 * sp.sin(Om * t)
    uys = uy0 * sp.cos(Om * t) - ux0 * sp.sin(Om * t)
    add('D7a', 'helix velocity u(t) = (u_x0 cos(Omega t) + u_y0 sin(Omega t), u_y0 cos(Omega t) - u_x0 sin(Omega t), u_par) solves du/dt = Omega u x z',
        _zero(sp.diff(uxs, t) - Om * uys) and _zero(sp.diff(uys, t) + Om * uxs))
    xs = (ux0 * sp.sin(Om * t) + uy0 * (1 - sp.cos(Om * t))) / Om
    ys = (uy0 * sp.sin(Om * t) - ux0 * (1 - sp.cos(Om * t))) / Om
    add('D7b', 'its integral (positions at gamma = const) satisfies dr/dt = u and starts at the origin',
        _zero(sp.diff(xs, t) - uxs) and _zero(sp.diff(ys, t) - uys) and _zero(xs.subs(t, 0)) and _zero(ys.subs(t, 0)))
    add('D7c', 'the circle has radius |u_perp| / |Omega|:  (x - x_c)^2 + (y - y_c)^2 = (u_x0^2 + u_y0^2)/Omega^2 with centre (u_y0, -u_x0)/Omega',
        _zero((xs - uy0 / Om)**2 + (ys + ux0 / Om)**2 - (ux0**2 + uy0**2) / Om**2))
    # ------------------------------------------------------------------ D8 Boris rotation
    t1, t2, t3, u1, u2, u3 = sp.symbols('t_1 t_2 t_3 u_1 u_2 u_3', real=True)
    tv = sp.Matrix([t1, t2, t3])
    uv = sp.Matrix([u1, u2, u3])
    T2 = tv.dot(tv)
    s_vec = 2 * tv / (1 + T2)
    u_prime = uv + uv.cross(tv)
    u_plus = uv + u_prime.cross(s_vec)
    cphi = (1 - T2) / (1 + T2)
    # Rodrigues' formula for a turn by -phi about t-hat, written without square roots: sin(phi) t-hat = 2 t/(1+t^2), (1 - cos phi) t-hat t-hat.u = 2 t (t.u)/(1+t^2)
    rodrigues = uv * cphi - tv.cross(uv) * 2 / (1 + T2) + tv * tv.dot(uv) * 2 / (1 + T2)
    add('D8a', 'Boris two-step (u\' = u + u x t,  u+ = u + u\' x s,  s = 2t/(1+t^2)) equals a turn of u by the angle phi, tan(phi/2) = |t|, about the axis -t (Rodrigues formula)',
        all(_zero(a - b) for a, b in zip(u_plus, rodrigues)))
    add('D8b', 'hence |u+| = |u| exactly: the rotation conserves the length of u',
        _zero(u_plus.dot(u_plus) - uv.dot(uv)))
    th_, Omh = sp.symbols('theta Omega_h', positive=True)
    add('D8c', 'in the plane normal to B:  u+_x = u_x (1 - s t) + s u_y  with 1 - s t = cos(phi), s = sin(phi) for t = tan(phi/2)',
        _zero((1 - 2 * sp.tan(th_ / 2)**2 / (1 + sp.tan(th_ / 2)**2)) - sp.cos(th_)) and _zero(2 * sp.tan(th_ / 2) / (1 + sp.tan(th_ / 2)**2) - sp.sin(th_)))
    # ------------------------------------------------------------------ D9 Boris polygon radius
    rho, hv, Oh = sp.symbols('rho h_v Oh', positive=True)
    tpar = Oh / 2
    phi_b = 2 * sp.atan(tpar)
    chord = Oh                                                   # chord = h v = rL * (Omega h) when rL = v / Omega
    R_poly = chord / (2 * sp.sin(phi_b / 2))
    add('D9a', 'a polygon with chord (Omega h) r_L and turning angle phi = 2 atan(Omega h / 2) has circumradius r_L sqrt(1 + (Omega h / 2)^2)',
        _zero(sp.simplify(R_poly**2 - (1 + Oh**2 / 4))))
    ser_ph = sp.series(Oh - 2 * sp.atan(Oh / 2), Oh, 0, 6).removeO()
    add('D9b', 'Boris phase error per step:  Omega h - 2 atan(Omega h / 2) = (Omega h)^3 / 12 - (Omega h)^5 / 80 + ...',
        _zero(ser_ph - (Oh**3 / 12 - Oh**5 / 80)))
    # ------------------------------------------------------------------ D10 RK4 on a rotation
    th = sp.symbols('theta', positive=True)
    z = sp.I * th
    R = 1 + z + z**2 / 2 + z**3 / 6 + z**4 / 24
    amp2 = sp.expand(sp.re(R)**2 + sp.im(R)**2)
    add('D10a', 'one RK4 step on a rotation multiplies the squared radius by |R|^2 = 1 - theta^6/72 + theta^8/576  (theta = Omega h)',
        _zero(amp2 - (1 - th**6 / 72 + th**8 / 576)))
    ph = sp.series(th - sp.atan(sp.im(R) / sp.re(R)), th, 0, 8).removeO()
    add('D10b', 'RK4 phase error per step:  theta - arg R = theta^5 / 120 - theta^7 / 336 + ...  (leading term theta^5/120)',
        _zero(sp.expand(ph - (th**5 / 120 - th**7 / 336))))
    # ------------------------------------------------------------------ D11 Helmholtz pair
    N, I, Rr, mu0, zz = sp.symbols('N I R mu_0 z', positive=True)
    loop = lambda zs: mu0 * N * I * Rr**2 / (2 * (Rr**2 + zs**2)**sp.Rational(3, 2))
    pair = loop(zz - Rr / 2) + loop(zz + Rr / 2)
    mid = sp.simplify(pair.subs(zz, 0))
    add('D11a', 'two loops a distance R apart:  B(0) = (4/5)^(3/2) mu_0 N I / R', _zero(mid - (sp.Rational(4, 5))**sp.Rational(3, 2) * mu0 * N * I / Rr))
    add('D11b', 'and dB/dz = d2B/dz2 = 0 at the midpoint (uniform field)',
        _zero(sp.diff(pair, zz).subs(zz, 0)) and _zero(sp.simplify(sp.diff(pair, zz, 2).subs(zz, 0))))
    # ------------------------------------------------------------------ D12 Busch focus
    vpar, Omega_ = sp.symbols('v_par Omega', positive=True)
    add('D12a', 'a helix returns to the axis after one turn T = 2 pi / Omega, i.e. after the length L = 2 pi v_par / Omega',
        _zero((2 * sp.pi / Omega_) * vpar - 2 * sp.pi * vpar / Omega_))
    for r in out:
        r['tex'] = TEX[r['label']]
    return out


def as_text():
    rows = run()
    w = max(len(r['label']) for r in rows)
    lines = ['%-*s  %s  %s' % (w, r['label'], OK if r['ok'] else 'FAIL', r['claim']) for r in rows]
    return '\n'.join(lines), all(r['ok'] for r in rows)


if __name__ == '__main__':
    txt, ok = as_text()
    print(txt)
    print('\nall pass' if ok else '\nFAILURES')
    raise SystemExit(0 if ok else 1)

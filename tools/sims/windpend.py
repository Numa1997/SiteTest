"""Paper globes on threads, swinging in a wind that carries a Kármán vortex street: the reference model behind the right-hand
rail of the home page (scene `rails`) and the scene `wind` of scenes.html. It replaces the spring-coupled pendulums
(tools/sims/coupled.py) there, 25 November 2026: the user asked for pendulums swinging in a velocity field of wind, with the
field's lines (not arrows) drawn, guiding their motion next to gravity. The flow and the drag law are the site's own: the
"Kármán vortex street" of the double inverted pendulum page (its function row() and the case 'street' of fieldV()), and its
section 13, equations (33), (34) and (39).

THE SETUP
The right margin of the page is a tall strip of air. A steady wind of speed U blows straight down the strip: a downdraught, as
under a rain cloud. Above the page the wind has passed a post, and behind a post a wind sheds vortices in turn from its two sides:
a Kármán vortex street, two rows of vortices of opposite spin, a distance h apart, each row with the spacing λ, the two rows
staggered by λ/2, the whole pattern drifting down with the speed c = 0.8 U (it lags behind the wind). Beams cross the strip, one
under the other. From each beam hang K threads of length L, each with a closed globe of thin paper at its end (radius R, paper
mass m_s; the air inside it is neither heavy nor light in the air around it). A globe is all surface and no weight, so the air
moves it easily. Without wind each one is a plain pendulum under gravity. With the wind, every passing vortex pushes the globes
sideways, first one way and then the other, and gravity pulls them back.

COORDINATES
η across the strip (m, 0 at its centre line, positive to the right), ξ along the strip (m, positive DOWN the page, the direction
of gravity and of the wind), t in s. A pendulum's angle θ is measured from the downward vertical, positive towards +η, so its globe is at
    r = (η_p + L sin θ, ξ_p + L cos θ),   velocity  v = L θ' t̂,   t̂ = (cos θ, −sin θ)   (the direction of growing θ).

THE WIND FIELD
One row of smoothed vortices of circulation Γ, on the line η = η0, the vortices at ξ = ξ0 + nλ, has the stream function
    ψ_row = −(Γ / 4π) ln( cosh e − cos z + δ² ),   e = k (η − η0),   z = k (ξ − ξ0),   k = 2π / λ,                      (1)
(δ = 0 is the textbook row of point vortices, Lamb §156; δ > 0 rounds each core off, as on the site). The velocity is
    u_ξ = ∂ψ/∂η = −(Γ / 2λ) sinh e / D,     u_η = −∂ψ/∂ξ = (Γ / 2λ) sin z / D,     D = cosh e − cos z + δ².             (2)
Because both components come from one ψ, ∂u_ξ/∂ξ + ∂u_η/∂η = 0: the air is neither made nor lost anywhere (checked numerically).
The street is two such rows, at η = +h/2 with −Γ and ξ0 = c t + λ/2, and at η = −h/2 with +Γ and ξ0 = c t, plus the wind itself:
    u(η, ξ, t) = (0, U) + u_row(+h/2, c t + λ/2, −Γ) + u_row(−h/2, c t, +Γ),   Γ = 0.4 U λ / tanh(π h / λ),  h = 0.281 λ.   (3)
(0.281 is von Kármán's ratio, the one spacing at which the street keeps its shape.) The whole pattern only slides:
    u(η, ξ, t) = u(η, ξ − c t, 0).                                                                                     (4)
Two things follow from (4), and the page uses both. The wind repeats at every point with the period T = λ / c. And a pendulum
hung lower by Δξ feels exactly the wind of the one above it, Δξ / c later: one computed swing per position across the strip serves
every beam down the page, played with that delay.
The field's lines are the streamlines, the curves the air follows at one instant: the lines ψ_tot = const of
    ψ_tot = U η + ψ_rows.                                                                                              (5)
Lines at equal steps of ψ_tot lie close together where the air is fast. They are stored for the page as curves η_l(ξ − c t).

THE FORCES ON A GLOBE (velocity v, the air's velocity there u, w = v − u its velocity through the air)
(a) Weight less buoyancy. The globe is the paper shell (m_s) and the air inside (ρ V, V = 4πR³/3). The air around it carries the
    weight of the air inside (Archimedes), so the net pull is  m_s g  down.
(b) Drag, the site's two terms added, as in its section 13: slow (Stokes) and fast (pressure) drag of a sphere,
        F_d = −6π μ R w − ½ ρ C_D π R² |w| w,   C_D = 0.47.                                                            (6)
(c) The push of the accelerating air, the site's (39). Where the air speeds up, pressure falls along its path; that pressure
    difference pushes on a body as it would on the air it replaces: ρ V Du/Dt, with Du/Dt = ∂u/∂t + (u·∇)u the acceleration of
    the air itself. And to speed up through air, a sphere must speed up half its own volume of air with it (added mass, C_a = ½):
        F_a = ρ V Du/Dt + C_a ρ V (Du/Dt − dv/dt).                                                                     (7)
    For a body much denser than air (7) is nothing; for a paper globe, about as light as the air it displaces, it matters as much as
    the globe's own inertia. (This is the Maxey–Riley equation of a small sphere in a flow, without its history term.)
(d) The thread pulls along itself. It also feels the wind a little: per metre, across itself, the site's (33) and (34),
        f_n = −ξ_⊥ w_n − ½ ρ C_D,t d |w_n| w_n,   ξ_⊥ = 4π μ / ln(L / (d/2)),   C_D,t = 1.2,   along itself f_t = −(ξ_⊥/2) w_t.  (8)

THE EQUATION OF MOTION
Newton's law for the globe, with its mass m_s + ρV: (m_s + ρV) dv/dt = (a) + (b) + (c) + thread. Take the part along t̂, the only
direction the globe can go (the thread's pull is across t̂ and drops out); dv/dt·t̂ = L θ''; ĝ·t̂ = −sin θ:
    (m_s + ρV + C_a ρV) L θ'' = −m_s g sin θ + t̂·[ F_d + (1 + C_a) ρV Du/Dt ] + (thread's own weight, inertia and drag).
Multiplied by L and with the thread (mass m_t = ρ_t π d² L / 4, a thin rod about its end) and the shell's own turning (2 m_s R²/3):
    I θ'' = −(m_s + m_t/2) g L sin θ + L t̂·[ F_d + (1 + C_a) ρV Du/Dt ] + ∫₀ᴸ s f_n(s) ds,                              (9)
    I = (m_s + ρV + C_a ρV) L² + m_t L²/3 + (2/3) m_s R².
The integral over the thread is done with the site's 4-point Gauss–Legendre rule (the thread's tangential drag gives no torque).
Du/Dt: by (4), ∂u/∂t = −c ∂u/∂ξ for the vortex part, so Du/Dt = ((u − c ξ̂)·∇) u, with ∇u from (2) analytically.

WHAT IS COMPUTED
Each of the K pendulums of a beam (at η = −a, 0, +a), from rest, with (9), DOP853 (SciPy), rtol 1e-10, atol 1e-12, one wind
period T after another. A damped pendulum under a periodic push settles onto a swing of the push's period; this is checked, not
assumed: after every period the state (θ, θ') is compared with the one a period earlier, and the run stops when they agree to
1e-9, or fails loudly after N_MAX periods. One settled period is stored at fps frames a second, with the streamlines (5).

CHECKS (in the header)
- settled: periods needed, and the last change of state over a period (the stored loop's residual);
- energy: over the stored period the change of ½ I θ'² − (m_s + m_t/2) g L cos θ must equal the work of the air's forces (drag,
  the push (7), the thread's drag), integrated along with the motion; the residual is given against the total |power| dt;
- the same period at 100 times tighter tolerances (largest difference of angle);
- div u on a grid by central differences against the size of ∇u (the field keeps the air);
- u_ξ > 0 everywhere on the grid (no air flows back up, so every streamline is one curve η(ξ));
- the largest swing of each pendulum; the smallest gap between neighbouring globes over the period (they must not touch: the model
  has no collisions); the Reynolds number of a globe at its largest speed through the air (which drag term rules).

OUTPUT
windpend.bin = b"WPD1", uint32 header length, a JSON header (parameters, derived values, checks), then int16 little-endian:
first the frames (rows: frames over one period, dt in the header; columns θ_1..θ_K in 1e-4 rad), then the streamlines
(N_l rows, one per line; N_s columns, η in mm at ξ − c t = j λ / N_s). The page draws these and computes nothing.
Usage: python3 windpend.py [out_dir]"""
import json, os, struct, sys, time
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

# ---- parameters (SI); the page draws 1 m as `scale` px ----
P = dict(
    g=9.81,          # m/s^2, gravity
    rho=1.184,       # kg/m^3, air at 25 °C (the site's table, section 13.1)
    mu=1.849e-5,     # Pa s, air at 25 °C
    U=1.6,           # m/s, the wind, straight down the strip
    c_over_U=0.8,    # the vortex street drifts at c = 0.8 U (as on the site)
    lam=4.0,         # m, λ: spacing of the vortices in a row; the wind's period is T = λ / c
    h_over_lam=0.281,  # h / λ, von Kármán's ratio
    delta=0.35,      # δ, rounding of each vortex core (the site's ST_D)
    L=1.6,           # m, thread: pivot to the globe's centre
    R=0.15,          # m, radius of a globe
    m_s=0.004,       # kg, the paper shell of a globe (thin paper, about 14 g/m² over 0.28 m²)
    C_D=0.47,        # drag coefficient of a sphere
    C_a=0.5,         # added-mass coefficient of a sphere
    d=0.0005,        # m, diameter of the thread
    rho_t=1140.0,    # kg/m^3, the thread (nylon)
    C_Dt=1.2,        # drag coefficient of a cylinder across the flow (the site's (34))
    K=3,             # pendulums on a beam
    a=1.1,           # m, they hang at η = −a, 0, +a
    WS=8.0,          # m, width of the strip for which streamlines are stored
    N_l=41,          # streamlines stored
    N_s=96,          # points per streamline along one λ
    fps=30,          # stored frames per second (rounded to a whole number per period; the exact dt is in the header)
    N_MAX=400,       # periods to wait for the swing to settle before giving up
    scale=60.0,      # px per m on the page (L = 1.6 m -> 96 px)
)

GL4X = np.array([0.0694318442029737, 0.3300094782075719, 0.6699905217924281, 0.9305681557970263])
GL4W = np.array([0.1739274225687269, 0.3260725774312731, 0.3260725774312731, 0.1739274225687269])


def derived(P):
    D = dict(P); D["c"] = P["c_over_U"] * P["U"]; D["T"] = P["lam"] / D["c"]; D["h"] = P["h_over_lam"] * P["lam"]; D["k"] = 2 * np.pi / P["lam"]
    D["Gam"] = 0.4 * P["U"] * P["lam"] / np.tanh(np.pi * D["h"] / P["lam"])
    D["V"] = 4 / 3 * np.pi * P["R"] ** 3; D["m_t"] = P["rho_t"] * np.pi * P["d"] ** 2 / 4 * P["L"]
    D["I"] = (P["m_s"] + (1 + P["C_a"]) * P["rho"] * D["V"]) * P["L"] ** 2 + D["m_t"] * P["L"] ** 2 / 3 + 2 / 3 * P["m_s"] * P["R"] ** 2
    D["xi_perp"] = 4 * np.pi * P["mu"] / np.log(P["L"] / (P["d"] / 2))
    D["rows"] = [(+D["h"] / 2, P["lam"] / 2, -D["Gam"]), (-D["h"] / 2, 0.0, +D["Gam"])]   # (η0, ξ0 at t = 0, Γ)
    return D


def field(D, eta, s, grad=False):
    """The air's velocity (u_η, u_ξ) at the point (η, ξ) at time t, as a function of η and s = ξ − c t (equation (4)); with
    grad=True also its four derivatives (∂u_η/∂η, ∂u_η/∂ξ, ∂u_ξ/∂η, ∂u_ξ/∂ξ) from (2)."""
    k = D["k"]; ue = 0.0; ux = D["U"] + 0.0 * eta; a = b = cc = dd = 0.0
    for eta0, xi0, G in D["rows"]:
        e = k * (eta - eta0); z = k * (s - xi0); Dn = np.cosh(e) - np.cos(z) + D["delta"] ** 2; A = G / (2 * D["lam"])
        ue = ue + A * np.sin(z) / Dn; ux = ux - A * np.sinh(e) / Dn
        if grad:
            a = a - A * k * np.sin(z) * np.sinh(e) / Dn ** 2                    # ∂u_η/∂η
            b = b + A * k * (np.cos(z) / Dn - np.sin(z) ** 2 / Dn ** 2)          # ∂u_η/∂ξ
            cc = cc - A * k * (np.cosh(e) / Dn - np.sinh(e) ** 2 / Dn ** 2)      # ∂u_ξ/∂η
            dd = dd + A * k * np.sinh(e) * np.sin(z) / Dn ** 2                   # ∂u_ξ/∂ξ
    return (ue, ux, a, b, cc, dd) if grad else (ue, ux)


def psi_tot(D, eta, s):
    """The stream function (5)."""
    p = D["U"] * eta
    for eta0, xi0, G in D["rows"]:
        p = p - G / (4 * np.pi) * np.log(np.cosh(D["k"] * (eta - eta0)) - np.cos(D["k"] * (s - xi0)) + D["delta"] ** 2)
    return p


def torques(D, eta_p, t, th, om):
    """The torque of the air about the pivot, equation (9) without gravity: (drag of the globe, push of the accelerating air,
    drag of the thread). The pivot is at (η_p, ξ = 0): by (4) a beam elsewhere only shifts the time."""
    L, R, rho = D["L"], D["R"], D["rho"]; sn, cs = np.sin(th), np.cos(th); tx, ty = cs, -sn       # t̂ in (η, ξ)
    ue, ux, a, b, cc, dd = field(D, eta_p + L * sn, L * cs - D["c"] * t, grad=True)
    we, wx = L * om * tx - ue, L * om * ty - ux; wm = np.hypot(we, wx)
    kd = 6 * np.pi * D["mu"] * R + 0.5 * rho * D["C_D"] * np.pi * R * R * wm
    tau_d = L * (-(kd * we) * tx - (kd * wx) * ty)
    # Du/Dt = ((u − c ξ̂)·∇) u
    ae = ue * a + (ux - D["c"]) * b; ax = ue * cc + (ux - D["c"]) * dd
    tau_a = L * (1 + D["C_a"]) * rho * D["V"] * (ae * tx + ax * ty)
    tau_t = 0.0
    for gx, gw in zip(GL4X, GL4W):
        sg = gx * L; ue2, ux2 = field(D, eta_p + sg * sn, sg * cs - D["c"] * t)
        wn = (sg * om * tx - ue2) * tx + (sg * om * ty - ux2) * ty                              # across the thread
        tau_t += gw * L * sg * (-D["xi_perp"] * wn - 0.5 * rho * D["C_Dt"] * D["d"] * abs(wn) * wn)
    return tau_d, tau_a, tau_t


def rhs_factory(D, eta_p):
    grav = (D["m_s"] + D["m_t"] / 2) * D["g"] * D["L"]
    def rhs(t, y):
        th, om = y[0], y[1]; td, ta, tt = torques(D, eta_p, t, th, om); tau = td + ta + tt
        return [om, (-grav * np.sin(th) + tau) / D["I"], tau * om, abs(td * om) + abs(ta * om) + abs(tt * om)]   # θ', θ'', power of the air, |power|
    return rhs


def energy(D, th, om):
    return 0.5 * D["I"] * om * om - (D["m_s"] + D["m_t"] / 2) * D["g"] * D["L"] * np.cos(th)


def settle(D, eta_p, opts):
    """Integrate period after period until the state repeats; return the settled start state, the periods used, the history."""
    rhs = rhs_factory(D, eta_p); y = np.array([0.0, 0.0]); hist = []
    for n in range(1, D["N_MAX"] + 1):
        s = solve_ivp(rhs, ((n - 1) * D["T"], n * D["T"]), [y[0], y[1], 0.0, 0.0], **opts); y2 = s.y[:2, -1]
        ch = float(max(abs(y2[0] - y[0]), abs(y2[1] - y[1]))); hist.append(ch); y = y2
        if ch < 1e-9: return y, n, hist
    tail = hist[-8:]; ratio = [tail[i + 1] / tail[i] for i in range(len(tail) - 1) if tail[i] > 0]
    kind = "still converging slowly (raise N_MAX)" if all(r < 1 for r in ratio) else "not settling on the wind's period: a longer period or chaos (changes over the last periods: %s)" % tail
    raise RuntimeError("pendulum at η = %.2f m did not settle in %d periods: %s" % (eta_p, D["N_MAX"], kind))


def run(out_dir="."):
    t0 = time.time(); D = derived(P); T = D["T"]; K = P["K"]
    etas = [0.0] if K == 1 else list(np.linspace(-P["a"], P["a"], K))
    nf = int(round(T * P["fps"])); dt = T / nf
    opts = dict(method="DOP853", rtol=1e-10, atol=1e-12); tight = dict(method="DOP853", rtol=1e-12, atol=1e-14)
    TH = np.zeros((nf, K)); checks = dict(periods_to_settle=[], loop_residual=[], energy_residual=[], tolerance_diff_rad=[], max_swing_rad=[], reynolds_globe=[])
    for j, ep in enumerate(etas):
        y0, n, hist = settle(D, ep, opts); rhs = rhs_factory(D, ep); tt = n * T + np.arange(nf + 1) * dt
        s = solve_ivp(rhs, (n * T, (n + 1) * T), [y0[0], y0[1], 0.0, 0.0], dense_output=True, **opts); Y = s.sol(tt)
        s2 = solve_ivp(rhs, (n * T, (n + 1) * T), [y0[0], y0[1], 0.0, 0.0], dense_output=True, **tight); Y2 = s2.sol(tt)
        TH[:, j] = Y[0, :nf]
        dE = energy(D, Y[0, -1], Y[1, -1]) - energy(D, Y[0, 0], Y[1, 0])
        wmax = 0.0
        for q in range(nf):
            ue, ux = field(D, ep + P["L"] * np.sin(Y[0, q]), P["L"] * np.cos(Y[0, q]) - D["c"] * tt[q])
            wmax = max(wmax, float(np.hypot(P["L"] * Y[1, q] * np.cos(Y[0, q]) - ue, -P["L"] * Y[1, q] * np.sin(Y[0, q]) - ux)))
        checks["periods_to_settle"].append(n); checks["loop_residual"].append(float(max(abs(Y[0, -1] - Y[0, 0]), abs(Y[1, -1] - Y[1, 0]))))
        checks["energy_residual"].append(float(abs(dE - Y[2, -1]) / max(Y[3, -1], 1e-300)))
        checks["tolerance_diff_rad"].append(float(np.max(np.abs(Y2[0] - Y[0])))); checks["max_swing_rad"].append(float(np.max(np.abs(Y[0]))))
        checks["reynolds_globe"].append(float(P["rho"] * wmax * 2 * P["R"] / P["mu"]))
    # neighbours must not touch
    gap = 1e9
    for j in range(K - 1):
        dx = (etas[j + 1] - etas[j]) + P["L"] * (np.sin(TH[:, j + 1]) - np.sin(TH[:, j])); dy = P["L"] * (np.cos(TH[:, j + 1]) - np.cos(TH[:, j]))
        gap = min(gap, float(np.min(np.hypot(dx, dy)) - 2 * P["R"]))
    checks["min_gap_m"] = gap if K > 1 else None
    # the field on a grid: it keeps the air, and never flows back up
    ge, gs = np.meshgrid(np.linspace(-P["WS"] / 2, P["WS"] / 2, 161), np.linspace(0, P["lam"], 97)[:-1]); hh = 1e-5
    ue, ux, a, b, cc, dd = field(D, ge, gs, grad=True)
    div_fd = (field(D, ge + hh, gs)[0] - field(D, ge - hh, gs)[0]) / (2 * hh) + (field(D, ge, gs + hh)[1] - field(D, ge, gs - hh)[1]) / (2 * hh)
    gsz = float(np.max(np.sqrt(a * a + b * b + cc * cc + dd * dd)))
    checks["div_over_grad"] = float(np.max(np.abs(div_fd)) / gsz); checks["div_analytic"] = float(np.max(np.abs(a + dd)) / gsz)
    checks["u_xi_min_over_U"] = float(np.min(ux) / P["U"]); checks["u_eta_max_over_U"] = float(np.max(np.abs(ue)) / P["U"])
    if checks["u_xi_min_over_U"] <= 0: raise RuntimeError("the air flows back up somewhere (u_ξ ≤ 0): streamlines are not single curves η(ξ)")
    # streamlines (5): at equal steps of ψ, from the value ψ has far to the left to the one far to the right
    sg = np.arange(P["N_s"]) * P["lam"] / P["N_s"]; lev = np.linspace(psi_tot(D, -P["WS"] / 2, 0.0), psi_tot(D, P["WS"] / 2, 0.0), P["N_l"])
    LN = np.zeros((P["N_l"], P["N_s"]))
    for li, C in enumerate(lev):
        for si, s_ in enumerate(sg):
            LN[li, si] = brentq(lambda e: psi_tot(D, e, s_) - C, -P["WS"], P["WS"], xtol=1e-9)
    frames = np.round(1e4 * TH).astype("<i2"); lines = np.round(1e3 * LN).astype("<i2")
    hdr = dict(model="windpend", version=1, params=P,
               derived=dict(c=D["c"], T=T, h=D["h"], Gamma=D["Gam"], V=D["V"], m_air_inside=P["rho"] * D["V"], m_t=D["m_t"], I=D["I"], xi_perp=D["xi_perp"], etas=[float(e) for e in etas],
                            swing_period_no_wind=float(2 * np.pi * np.sqrt(D["I"] / ((P["m_s"] + D["m_t"] / 2) * P["g"] * P["L"])))),
               frames=nf, dt=dt, columns=["theta_%d" % (j + 1) for j in range(K)], units=dict(theta="1e-4 rad", lines="1e-3 m"),
               lines=dict(n=P["N_l"], points=P["N_s"], offset_int16=nf * K, note="row l: η of streamline l in mm at ξ − c t = j λ / points"),
               checks=checks, wall_s=time.time() - t0)
    os.makedirs(out_dir, exist_ok=True); hb = json.dumps(hdr, separators=(",", ":")).encode()
    with open(os.path.join(out_dir, "windpend.bin"), "wb") as f:
        f.write(b"WPD1"); f.write(struct.pack("<I", len(hb))); f.write(hb); f.write(frames.tobytes()); f.write(lines.tobytes())
    json.dump(hdr, open(os.path.join(out_dir, "windpend.json"), "w"), indent=1)
    print(json.dumps(dict(derived=hdr["derived"], frames=nf, checks=checks, wall=hdr["wall_s"]), indent=1))
    return hdr


if __name__ == "__main__":
    run(sys.argv[1] if len(sys.argv) > 1 else ".")

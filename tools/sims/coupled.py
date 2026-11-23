"""Two pendulums tied by a weak spring: the reference model behind the right-hand rail of the home page (scene `rails`).
It replaces Barton's pendulums (tools/sims/barton.py) there, 23 November 2026: the user found those fast, thin and creepy, and
they never visibly gave their motion to one another. Here the swing visibly moves from one bob to the other and back.

The setup. A rigid beam holds two pivots a distance d apart. From each hangs a light rod of length L with a heavy bob of mass m at
its end. A weak spring of stiffness k joins the two rods at the distance a below the pivots; its natural length is d, so with both
pendulums hanging straight it is neither stretched nor squeezed. Without the spring each pendulum swings on its own with
ω₁ = √(g / L). With it, a swing of one pendulum stretches and squeezes the spring, which pushes on the other, and the swing
slowly drains across.

Coordinates and energies. θ₁, θ₂ are the angles from the vertical. The spring's ends sit at
    P₁ = (a sin θ₁, −a cos θ₁),   P₂ = (d + a sin θ₂, −a cos θ₂),   ℓ = |P₂ − P₁|.
    T = ½ m L² (θ₁'² + θ₂'²)                                   (kinetic energy of the bobs; the rods are massless)
    V = − m g L (cos θ₁ + cos θ₂) + ½ k (ℓ − d)²               (gravity and the spring)
Lagrange's equations, d/dt ∂T/∂θᵢ' = − ∂V/∂θᵢ, give
    m L² θᵢ'' = − m g L sin θᵢ − k (ℓ − d) ∂ℓ/∂θᵢ                                          (1)
    ∂ℓ/∂θ₁ = (P₁ − P₂)·(a cos θ₁, a sin θ₁) / ℓ,   ∂ℓ/∂θ₂ = (P₂ − P₁)·(a cos θ₂, a sin θ₂) / ℓ.
These full equations are integrated; nothing is linearised in the stored motion.

Why the swing moves across (small angles). Then ℓ − d ≈ a (θ₂ − θ₁) and (1) becomes
    θ₁'' = − ω₁² θ₁ − κ (θ₁ − θ₂),   θ₂'' = − ω₁² θ₂ − κ (θ₂ − θ₁),   κ = k a² / (m L²).
The sum θ₁ + θ₂ (both swinging together, spring idle) oscillates at ω₁; the difference θ₁ − θ₂ (swinging against each other,
spring working) at ω₂ = √(ω₁² + 2κ). Started with θ₁ = θ₀, θ₂ = 0, both at rest:
    θ₁ = θ₀ cos(½(ω₂ − ω₁) t) cos(½(ω₂ + ω₁) t),   θ₂ = θ₀ sin(½(ω₂ − ω₁) t) sin(½(ω₂ + ω₁) t).
Each swings at the mean frequency inside a slow envelope; the swing has fully crossed to pendulum 2 after half a beat,
    T_b / 2 = π / (ω₂ − ω₁),                                                                (2)
and is back in pendulum 1 after the beat period T_b = 2π / (ω₂ − ω₁).

A loop without a seam. The page plays one stored loop over and over, so the motion must repeat exactly. Choose ω₂ / ω₁ = (M + 1) / M:
then in the linear motion pendulum 1 makes M swings while the beat completes, and at t = T_b / 2 both bobs are at rest
(θ₁ = 0, θ₂ = −θ₀). The full equations (1) shift the frequencies a little, so k is corrected by shooting: k and the time t* are
solved so that θ₁'(t*) = θ₂'(t*) = 0. The equations do not change when time runs backwards, and the start is at rest too, so the
motion from t* to 2t* is the motion from 0 to t* played backwards: the loop of length 2t* closes exactly.

Checks (in the header): the energy T + V over the loop (no friction, so it must stay constant), the loop's residual |y(2t*) − y(0)|,
the time at which the swing has fully crossed against (2), the same loop at 100 times tighter tolerances, and the smallest gap between
the two bobs over the loop (the model has no collisions, so the bobs must never meet).
Integration: DOP853 (SciPy), rtol 1e-11, atol 1e-13.
Output: coupled.bin = b"CPL1", uint32 header length, a JSON header (parameters, derived values, checks), then int16 little-endian
frames (rows: frames evenly spaced over one loop, dt in the header; columns: θ₁, θ₂ in 1e-4 rad). The page draws these and computes nothing.
Usage: python3 coupled.py [out_dir]"""
import json, os, struct, sys, time
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import fsolve

# ---- parameters (SI); the page draws 1 m as `scale` px ----
P = dict(
    g=9.81,        # m/s^2, gravity
    L=1.5,         # m, pivot to bob (period 2π√(L/g) = 2.46 s: a calm swing)
    m=1.0,         # kg, each bob (a steel ball about 6 cm across)
    a=0.5,         # m, where the spring meets each rod, measured down from the pivot
    d=0.8,         # m, distance between the pivots = the spring's natural length; wide enough that the bobs never touch (checked)
    rb=0.04,       # m, radius of a bob (drawn; the check min_bob_gap_m must stay positive)
    theta0=0.20,   # rad, the swing pendulum 1 starts with (about 11°); pendulum 2 starts hanging still
    M=11,          # swings of pendulum 1 per beat: ω₂/ω₁ = (M+1)/M, so the beat lasts M periods (about 27 s)
    fps=30,        # stored frames per second (the loop's frame count is rounded, the exact dt is in the header)
    scale=80.0,    # px per m on the page (L = 1.5 m -> 120 px)
)

def rhs_factory(P, k):
    g, L, m, a, d = P["g"], P["L"], P["m"], P["a"], P["d"]
    def rhs(t, y):
        t1, t2, w1, w2 = y
        p1 = np.array([a * np.sin(t1), -a * np.cos(t1)]); p2 = np.array([d + a * np.sin(t2), -a * np.cos(t2)])
        D = p2 - p1; l = np.hypot(*D); f = k * (l - d)
        dl1 = -(D @ np.array([a * np.cos(t1), a * np.sin(t1)])) / l
        dl2 = (D @ np.array([a * np.cos(t2), a * np.sin(t2)])) / l
        return [w1, w2, (-m * g * L * np.sin(t1) - f * dl1) / (m * L * L), (-m * g * L * np.sin(t2) - f * dl2) / (m * L * L)]
    return rhs

def energy(P, k, y):
    g, L, m, a, d = P["g"], P["L"], P["m"], P["a"], P["d"]; t1, t2, w1, w2 = y
    l = np.hypot(d + a * np.sin(t2) - a * np.sin(t1), -a * np.cos(t2) + a * np.cos(t1))
    T = .5 * m * L * L * (w1 * w1 + w2 * w2); V = -m * g * L * (np.cos(t1) + np.cos(t2)) + .5 * k * (l - d) ** 2
    return T, V, .5 * m * L * L * w1 * w1 - m * g * L * np.cos(t1), .5 * m * L * L * w2 * w2 - m * g * L * np.cos(t2)

def run(out_dir="."):
    t0 = time.time(); g, L, m, a = P["g"], P["L"], P["m"], P["a"]
    w1 = np.sqrt(g / L); w2 = w1 * (P["M"] + 1) / P["M"]
    k_lin = (w2 * w2 - w1 * w1) * m * L * L / (2 * a * a)          # from ω₂² = ω₁² + 2 k a² / (m L²)
    ts_lin = np.pi / (w2 - w1)                                       # half a beat, equation (2)
    y0 = [P["theta0"], 0.0, 0.0, 0.0]
    opts = dict(method="DOP853", rtol=1e-11, atol=1e-13)
    def shoot(z):
        k, ts = z; s = solve_ivp(rhs_factory(P, k), (0, ts), y0, **opts); return [s.y[2, -1], s.y[3, -1]]
    k, ts = fsolve(shoot, [k_lin, ts_lin], xtol=1e-13)
    T = 2 * ts; nf = int(round(T * P["fps"])); dt = T / nf; tt = np.arange(nf + 1) * dt
    rhs = rhs_factory(P, k)
    s = solve_ivp(rhs, (0, T), y0, dense_output=True, **opts); Y = s.sol(tt)
    s2 = solve_ivp(rhs, (0, T), y0, dense_output=True, method="DOP853", rtol=1e-13, atol=1e-15); Y2 = s2.sol(tt)
    E = np.array([sum(energy(P, k, Y[:, j])[:2]) for j in range(nf + 1)])
    E1 = np.array([energy(P, k, Y[:, j])[2] for j in range(nf + 1)]) + m * g * L     # pendulum 1's own energy above rest
    E0 = E1[0]
    # when has the swing fully crossed? the minimum of pendulum 1's energy, found on a fine grid near t*
    tf = np.linspace(.8 * ts, 1.2 * ts, 4001); Yf = s.sol(tf)
    Ef = np.array([energy(P, k, Yf[:, j])[2] for j in range(len(tf))]) + m * g * L
    t_cross = float(tf[np.argmin(Ef)])
    w2_eff = np.sqrt(w1 * w1 + 2 * k * a * a / (m * L * L))
    checks = dict(
        energy_rel_drift=float(np.max(np.abs(E - E[0])) / abs(E[0])),
        energy_J=float(E[0]),
        loop_residual_rad=float(np.max(np.abs(Y[:2, -1] - Y[:2, 0]))), loop_residual_rad_s=float(np.max(np.abs(Y[2:, -1] - Y[2:, 0]))),
        velocity_at_half_loop_rad_s=[float(v) for v in Y[2:, nf // 2]] if nf % 2 == 0 else None,
        crossed_at_s=t_cross, half_beat_linear_s=float(np.pi / (w2_eff - w1)),
        crossed_share_of_energy=float(1 - Ef.min() / E0),
        tolerance_diff_rad=float(np.max(np.abs(Y2[:2] - Y[:2]))),
        min_bob_gap_m=float(np.min(np.hypot(P["d"] + L * (np.sin(Y[1]) - np.sin(Y[0])), L * (np.cos(Y[0]) - np.cos(Y[1])))) - 2 * P["rb"]),
        quantisation_rad=0.5e-4, max_angle_rad=[float(np.abs(Y[0]).max()), float(np.abs(Y[1]).max())])
    frames = np.round(1e4 * Y[:2, :nf].T).astype("<i2")
    hdr = dict(model="coupled", version=1, params=P, derived=dict(omega1=float(w1), omega2=float(w2_eff), k_N_per_m=float(k), k_linear=float(k_lin),
               beat_s=T, loop_s=T, half_beat_s=float(ts), period1_s=float(2 * np.pi / w1)),
               frames=nf, dt=dt, columns=["theta_1", "theta_2"], units=dict(theta_1="1e-4 rad", theta_2="1e-4 rad"), checks=checks, wall_s=time.time() - t0)
    os.makedirs(out_dir, exist_ok=True)
    hb = json.dumps(hdr, separators=(",", ":")).encode()
    with open(os.path.join(out_dir, "coupled.bin"), "wb") as f:
        f.write(b"CPL1"); f.write(struct.pack("<I", len(hb))); f.write(hb); f.write(frames.tobytes())
    json.dump(hdr, open(os.path.join(out_dir, "coupled.json"), "w"), indent=1)
    print(json.dumps(dict(k=k, k_lin=k_lin, loop=T, frames=nf, checks=checks, wall=hdr["wall_s"]), indent=1))
    return hdr

if __name__ == "__main__":
    run(sys.argv[1] if len(sys.argv) > 1 else ".")

"""Barton's pendulums, the reference model behind the right-hand rail of the home page (scene `rails`).

The setup. A light horizontal bar hangs from the frame. A heavy pendulum (the driver) and eight light pendulums of different
lengths hang from it. The driver is so much heavier that it swings on its own, θ_d = A sin φ(t), and its swing drags the bar
sideways by x_b = κ θ_d. The light pendulums do not push back (their mass is negligible), so each one is a pendulum on a moving
support, independent of the others:

    θ_i'' = −(g / L_i) sin θ_i − γ θ_i' − (ẍ_b / L_i) cos θ_i                              (1)

The driver's length is slowly drawn up and let down, L_d(t) = Ld_min + (Ld_max − Ld_min)(1 − cos(2π t / T_s)) / 2, so its own
frequency φ' = √(g / L_d) sweeps through the light pendulums' frequencies √(g / L_i), and the one in resonance swings wide.

    ẍ_b = κ A (φ'' cos φ − φ'² sin φ),   φ'' = −½ √g L_d^(−3/2) L_d'                         (2)

Seamless loop. The whole system is periodic in time with period T_s only if the driver's phase gains a whole number of turns
in one sweep, Φ = ∫₀^{T_s} √(g / L_d) dt = 2π N. Φ grows in proportion to T_s, so T_s is rescaled to the nearest whole N. Then
the damped light pendulums settle onto a solution of period T_s, and one stored period plays as an endless loop without a seam.
The script integrates until the cycle repeats and measures the residual |θ(t + T_s) − θ(t)|.

Integration: DOP853 (SciPy), rtol 1e-10, atol 1e-12, on the full nonlinear equations (1) and (2).
Output: barton.bin = b"BRT1", uint32 header length, a JSON header (parameters, checks), then int16 little-endian frames
(rows = frames at FPS; columns: the driver's angle θ_d (1e-4 rad), its length L_d (1e-4 m), the bar's travel x_b (1e-6 m), then
the eight angles (1e-4 rad)). The page draws these numbers and computes nothing.
Usage: python3 barton.py [out_dir]"""
import json, os, struct, sys, time
import numpy as np
from scipy.integrate import solve_ivp, quad

# ---- parameters (SI); the page draws 1 m as SCALE px ----
P = dict(
    g=9.81,            # m/s^2, gravity
    L_min=0.10,        # m, shortest light pendulum and the driver's shortest length
    L_max=0.34,        # m, longest light pendulum
    Ld_min=0.085,      # m, driver's shortest length (a little beyond the shortest pendulum, so no pendulum is held at resonance at a turning point of the sweep)
    Ld_max=0.36,       # m, driver's longest length
    n=8,               # light pendulums
    A=0.32,            # rad, driver amplitude
    kappa=0.0214,      # m/rad, bar travel per radian of driver swing (bar amplitude kappa*A = 6.8 mm)
    gamma=0.35,        # 1/s, damping rate of the light pendulums (air and pivot)
    T_nominal=65.0,    # s, wanted sweep period before rounding to whole driver turns
    fps=30,            # frames stored per second
    scale=420.0,       # px per m on the page (0.10 m -> 42 px)
)

def model(P):
    g = P["g"]; L = np.array([P["L_min"] + (P["L_max"] - P["L_min"]) * i / (P["n"] - 1) for i in range(P["n"])])
    a, b = P["Ld_min"], P["Ld_max"]
    def Ld(t, T): return a + (b - a) * (1 - np.cos(2 * np.pi * t / T)) / 2
    def Ld_dot(t, T): return (b - a) * np.pi / T * np.sin(2 * np.pi * t / T)
    # Phi(T) = T * mean over one sweep of sqrt(g/L_d); rescale T so Phi = 2 pi N
    mean_w = quad(lambda u: np.sqrt(g / (a + (b - a) * (1 - np.cos(2 * np.pi * u)) / 2)), 0, 1, epsabs=1e-13, epsrel=1e-13)[0]
    N = round(P["T_nominal"] * mean_w / (2 * np.pi)); T = 2 * np.pi * N / mean_w
    def rhs(t, y):
        phi, th, om = y[0], y[1:1 + P["n"]], y[1 + P["n"]:]
        L_d = Ld(t, T); w = np.sqrt(g / L_d); wdot = -0.5 * np.sqrt(g) * L_d ** -1.5 * Ld_dot(t, T)
        xbdd = P["kappa"] * P["A"] * (wdot * np.cos(phi) - w * w * np.sin(phi))
        return np.concatenate(([w], om, -(g / L) * np.sin(th) - P["gamma"] * om - xbdd / L * np.cos(th)))
    return L, T, N, rhs, Ld

def run(out_dir="."):
    t0 = time.time(); L, T, N, rhs, Ld = model(P); n = P["n"]
    y0 = np.zeros(1 + 2 * n)
    # settle: the slowest decay is exp(-gamma t / 2) per amplitude, so k sweeps leave exp(-gamma k T / 2) of the start
    k_settle = 3
    sol = solve_ivp(rhs, (0, k_settle * T), y0, method="DOP853", rtol=1e-10, atol=1e-12)
    y1 = sol.y[:, -1]
    nf = int(round(T * P["fps"])); ts = k_settle * T + np.arange(nf + 1) * (T / nf)
    s1 = solve_ivp(rhs, (ts[0], ts[-1] + T), y1, method="DOP853", rtol=1e-10, atol=1e-12, dense_output=True)
    Y = s1.sol(ts[:-1]); Y2 = s1.sol(ts[:-1] + T)
    th = Y[1:1 + n]; resid = float(np.max(np.abs(Y2[1:1 + n] - th)))
    phi_wrap = float(abs(np.angle(np.exp(1j * (Y2[0] - Y[0] - 2 * np.pi * N))).max()))
    # check of the integrator itself: the same span at 10x tighter tolerances
    s2 = solve_ivp(rhs, (ts[0], ts[0] + T), y1, method="DOP853", rtol=1e-12, atol=1e-14, dense_output=True)
    tol_diff = float(np.max(np.abs(s2.sol(ts[:-1])[1:1 + n] - th)))
    amp = np.abs(th).max(axis=1)
    # resonance check: when each pendulum swings widest, the driver's length should be close to its own
    tpk = ts[:-1][np.argmax(np.abs(th), axis=1)] - k_settle * T
    Ld_at_pk = Ld(tpk, T)
    tt = ts[:-1] - k_settle * T; th_d = P["A"] * np.sin(Y[0])
    frames = np.empty((nf, 3 + n), dtype=np.int16)
    frames[:, 0] = np.round(1e4 * th_d); frames[:, 1] = np.round(1e4 * Ld(tt, T)); frames[:, 2] = np.round(1e6 * P["kappa"] * th_d)
    frames[:, 3:] = np.round(1e4 * th.T)
    hdr = dict(model="barton", version=1, params=P, T_sweep=T, driver_turns_per_sweep=N, frames=nf, columns=["theta_d", "L_d", "x_bar"] + ["theta_%d" % i for i in range(n)],
               units=dict(theta_d="1e-4 rad", L_d="1e-4 m", x_bar="1e-6 m", theta_i="1e-4 rad"), L=L.tolist(), L_px=(L * P["scale"]).tolist(),
               checks=dict(periodic_residual_rad=resid, phase_wrap_rad=phi_wrap, tolerance_diff_rad=tol_diff,
                           quantisation_rad=0.5e-4, max_angle_rad=amp.tolist(), peak_time_s=tpk.tolist(),
                           driver_length_at_peak_m=Ld_at_pk.tolist()),
               wall_s=time.time() - t0)
    os.makedirs(out_dir, exist_ok=True)
    hb = json.dumps(hdr, separators=(",", ":")).encode()
    with open(os.path.join(out_dir, "barton.bin"), "wb") as f:
        f.write(b"BRT1"); f.write(struct.pack("<I", len(hb))); f.write(hb); f.write(frames.astype("<i2").tobytes())
    json.dump(hdr, open(os.path.join(out_dir, "barton.json"), "w"), indent=1)
    print(json.dumps(dict(T=T, N=N, frames=nf, resid=resid, tol_diff=tol_diff, amp=[round(a, 3) for a in amp], wall=hdr["wall_s"]), indent=0))
    return hdr

if __name__ == "__main__":
    run(sys.argv[1] if len(sys.argv) > 1 else ".")

"""Spinners locked by a wandering rotating field: the reference model behind the scene `spin` (the band before the Simulations on
the home page) and section S4 of Fig. 17, "Living scenes" (public/simulations/living-scenes.html).

THE SETUP
A flat tray of thick oil holds a square lattice of small three-armed rotors, N_c columns by N_r rows, one lattice spacing a apart.
Each rotor sits on a pin and is driven by its own small, steady torque τ_i (a little motor, or a stream of oil pushing on its arms),
some one way and some the other. The oil is thick, so a rotor has no momentum worth speaking of: the drag ζ θ' balances the torques
at every instant (overdamped motion). Each rotor carries a small magnet along one arm. Above the tray a coil pair makes a magnetic
field B that rotates in the plane of the tray at the steady rate Ω; the coils are small, so the field is strong only within a
distance of about σ of a centre s(t), and that centre wanders slowly over the tray on a closed path. Neighbouring magnets also pull
on each other a little.

THE EQUATION OF MOTION
Torque balance on rotor i (angle θ_i of its magnet arm, from the x axis):
    ζ θ_i' = τ_i + m B(r_i, t) sin(φ(t) − θ_i) + κ' Σ_{j ∈ nb(i)} sin(θ_j − θ_i),                                         (1)
where φ = Ω t is the direction of the field, m B sin(φ − θ) is the torque of a field B on a magnet of moment m (m × B), and the last
term is the simplest pull between neighbouring magnets that turns them towards each other (the lattice's four nearest neighbours;
fewer at the edges). Dividing by ζ:
    θ_i' = ω_i + K(r_i, t) sin(φ − θ_i) + κ Σ_{j ∈ nb(i)} sin(θ_j − θ_i),   ω_i = τ_i / ζ,  K = m B / ζ,  κ = κ' / ζ,     (2)
    K(r, t) = K₀ exp(−|r − s(t)|² / (2σ²)),   s(t) = ( (N_c − 1)/2 + A_x sin(2π n_x t / T),  (N_r − 1)/2 + A_y sin(2π n_y t / T + 1) ).
Each term is a rate, in rad/s. Equation (2) with κ = 0 and K constant is Adler's equation (R. Adler, Proc. IRE 34, 351 (1946)); with
the neighbour term it is a Kuramoto lattice of phase oscillators driven by an outside rhythm (Y. Kuramoto, Chemical Oscillations,
Waves and Turbulence, Springer 1984; S. Strogatz, Nonlinear Dynamics and Chaos, §4.5 and §8.6).

WHY SOME LOCK (κ = 0, K constant). In the frame turning with the field, ψ = θ − φ obeys ψ' = (ω − Ω) − K sin ψ.            (3)
If |ω − Ω| < K, ψ' = 0 has the solution sin ψ* = (ω − Ω)/K: the rotor turns with the field, a fixed angle behind or ahead of it
(locked). If |ω − Ω| > K, ψ keeps turning: the rotor slips a full turn relative to the field every
    T_slip = ∫ dψ / |(ω − Ω) − K sin ψ| = 2π / √((ω − Ω)² − K²),                                                          (4)
so its mean rate is ⟨θ'⟩ = Ω + sign(ω − Ω) √((ω − Ω)² − K²). This is checked numerically (below). As the field's centre passes, K
rises and falls: rotors whose own rate is near Ω lock while the field is over them and slip again behind it.

WHAT IS COMPUTED
For every pair (K₀, κ) of the grid, the same lattice, the same own rates ω_i (drawn once, seed SEED: |ω_i| uniform between W_LO and
W_HI, the sign at random) and the same start angles; DOP853 (SciPy) with rtol 1e-9, atol 1e-9 over T_RUN seconds, sampled at FPS
frames a second. The field's path is closed over T_RUN (n_x and n_y whole turns), so the field returns to its start; the rotors that
slip do not, and the page cross-fades the last second into the first (it says so).

CHECKS (in the header)
- adler: one rotor, κ = 0, K constant, for a list of ω: the measured mean rate against (4); largest relative error;
- tolerance: the run (K₀ = 12, κ = 1) again at rtol 1e-11: largest angle difference;
- locked: in each run, the share of rotors within σ of the field's centre whose rate stays within LOCK_TOL of Ω over the last
  second, against the share predicted by |ω_i − Ω| < K(r_i) with κ = 0 (they differ where the neighbours help or hinder);
- quantisation: angles are stored in steps of 2π/256 (0.7° at most).

OUTPUT, one file per run, spin-K<K0>-k<kappa>.bin: b"SPN1", uint32 header length, a JSON header, then
  uint8 angles (frames × N, θ mod 2π in steps of 2π/256, row-major over the lattice, row by row),
  float32 field data (frames × 4: s_x, s_y in lattice spacings, φ in rad, the share of rotors locked within σ of the centre).
And spinners.json: the grid, the parameters and every check.
Usage: python3 spinners.py [out_dir]"""
import json, os, struct, sys, time
import numpy as np
from scipy.integrate import solve_ivp

P = dict(
    N_c=72, N_r=9,        # rotors across and down the lattice (72 × 9 = 648); the page shows the part its band can hold
    W_LO=1.5, W_HI=5.0,   # rad/s, the range of the rotors' own rates |ω_i| (each turns one way or the other)
    OMEGA=3.0,            # rad/s, Ω, how fast the field turns
    sigma=4.0,            # lattice spacings, σ, the width of the field's footprint
    A_x=0.37 * 72, A_y=0.33 * 9,  # lattice spacings, how far the field's centre swings across and down
    n_x=3, n_y=5,         # whole swings of the centre across and down per run: the path closes after T_RUN
    T_RUN=80.0,           # s, length of one stored run
    FPS=12,               # stored frames per second (the page draws in between by turning each rotor the short way)
    SEED=17,              # seed of the own rates and start angles
    K0_GRID=[0.0, 4.0, 12.0, 32.0],        # rad/s, the field's pull at its centre, K₀ = m B₀ / ζ
    KAPPA_GRID=[0.0, 1.0, 3.0],            # rad/s, the neighbours' pull, κ
    LOCK_TOL=0.3,         # rad/s, a rotor counts as locked when its rate stays within this of Ω
)


def lattice(P):
    jj, ii = np.meshgrid(np.arange(P["N_r"]), np.arange(P["N_c"]), indexing="ij")
    return ii.ravel().astype(float), jj.ravel().astype(float)


def centre(P, t):
    T = P["T_RUN"]; t = np.asarray(t, float)
    return ((P["N_c"] - 1) / 2 + P["A_x"] * np.sin(2 * np.pi * P["n_x"] * t / T), (P["N_r"] - 1) / 2 + P["A_y"] * np.sin(2 * np.pi * P["n_y"] * t / T + 1.0))


def rhs_factory(P, K0, kappa, w, X, Y):
    nc, nr = P["N_c"], P["N_r"]; s2 = 2 * P["sigma"] ** 2; Om = P["OMEGA"]
    def rhs(t, th):
        sx, sy = centre(P, t); K = K0 * np.exp(-((X - sx) ** 2 + (Y - sy) ** 2) / s2)
        g = th.reshape(nr, nc); c = np.zeros_like(g)                       # the neighbours' pull, open edges
        c[:, 1:] += np.sin(g[:, :-1] - g[:, 1:]); c[:, :-1] += np.sin(g[:, 1:] - g[:, :-1])
        c[1:, :] += np.sin(g[:-1, :] - g[1:, :]); c[:-1, :] += np.sin(g[1:, :] - g[:-1, :])
        return w + K * np.sin(Om * t - th) + kappa * c.ravel()
    return rhs


def adler_check(P):
    """One rotor, κ = 0, K constant: the mean rate against equation (4)."""
    Om, K = P["OMEGA"], 4.0; out = []
    for w in [-5.0, -2.0, 0.5, 2.0, 6.0, 7.5, 9.0]:
        f = lambda t, y: [w + K * np.sin(Om * t - y[0])]
        s = solve_ivp(f, (0, 200), [0.0], method="DOP853", rtol=1e-10, atol=1e-10, dense_output=True)
        t0, t1 = 100.0, 200.0; rate = (s.sol(t1)[0] - s.sol(t0)[0]) / (t1 - t0); d = w - Om
        pred = Om if abs(d) < K else Om + np.sign(d) * np.sqrt(d * d - K * K)
        out.append(dict(omega=w, measured=float(rate), predicted=float(pred), rel_err=float(abs(rate - pred) / max(abs(pred), 1e-12))))
    return out


def run(out_dir="."):
    t0 = time.time(); rng = np.random.default_rng(P["SEED"]); X, Y = lattice(P); N = X.size
    w = rng.choice([-1.0, 1.0], N) * rng.uniform(P["W_LO"], P["W_HI"], N); th0 = rng.uniform(0, 2 * np.pi, N)
    nf = int(round(P["T_RUN"] * P["FPS"])); tt = np.arange(nf) / P["FPS"]
    os.makedirs(out_dir, exist_ok=True); runs = []; Om = P["OMEGA"]
    for K0 in P["K0_GRID"]:
        for kap in P["KAPPA_GRID"]:
            rhs = rhs_factory(P, K0, kap, w, X, Y)
            s = solve_ivp(rhs, (0, P["T_RUN"]), th0, method="DOP853", rtol=1e-9, atol=1e-9, dense_output=True)
            TH = s.sol(tt).T                                                   # frames × N
            sx, sy = centre(P, tt); phi = Om * tt
            # the share locked near the centre, frame by frame: rate over the last second within LOCK_TOL of Ω
            lag = P["FPS"]; share = np.zeros(nf)
            for f in range(lag, nf):
                near = (X - sx[f]) ** 2 + (Y - sy[f]) ** 2 < P["sigma"] ** 2
                rate = (TH[f] - TH[f - lag]) * P["FPS"] / lag
                share[f] = float(np.mean(np.abs(rate[near] - Om) < P["LOCK_TOL"])) if near.any() else 0.0
            share[:lag] = share[lag]
            # predicted with κ = 0 at the end of the run
            near = (X - sx[-1]) ** 2 + (Y - sy[-1]) ** 2 < P["sigma"] ** 2; Kc = K0 * np.exp(-((X - sx[-1]) ** 2 + (Y - sy[-1]) ** 2) / (2 * P["sigma"] ** 2))
            pred = float(np.mean(np.abs(w[near] - Om) < Kc[near])) if near.any() else 0.0
            q = np.floor(np.mod(TH, 2 * np.pi) / (2 * np.pi) * 256).astype(np.uint8) % 256
            fd = np.stack([sx, sy, phi, share], 1).astype("<f4")
            name = "spin-K%g-k%g.bin" % (K0, kap)
            hdr = dict(model="spinners", version=1, K0=K0, kappa=kap, frames=nf, fps=P["FPS"], N=N, N_c=P["N_c"], N_r=P["N_r"],
                       columns=["theta"], layout=dict(angles="uint8 frames×N, θ mod 2π in steps of 2π/256, rows of N_c", field="float32 frames×4: s_x, s_y, φ, locked share"),
                       locked_end=dict(measured=float(share[-1]), predicted_kappa0=pred), mean_locked=float(share.mean()), steps=int(s.t.size))
            hb = json.dumps(hdr, separators=(",", ":")).encode()
            with open(os.path.join(out_dir, name), "wb") as fh:
                fh.write(b"SPN1"); fh.write(struct.pack("<I", len(hb))); fh.write(hb); fh.write(q.tobytes()); fh.write(fd.tobytes())
            runs.append(dict(file=name, K0=K0, kappa=kap, mean_locked=hdr["mean_locked"], locked_end=hdr["locked_end"], steps=hdr["steps"]))
            print(name, json.dumps(runs[-1]), flush=True)
    # tolerance check on one run
    rhs = rhs_factory(P, 12.0, 1.0, w, X, Y)
    a = solve_ivp(rhs, (0, P["T_RUN"]), th0, method="DOP853", rtol=1e-9, atol=1e-9, dense_output=True).sol(tt)
    b = solve_ivp(rhs, (0, P["T_RUN"]), th0, method="DOP853", rtol=1e-11, atol=1e-11, dense_output=True).sol(tt)
    ad = adler_check(P)
    checks = dict(adler=ad, adler_max_rel_err=max(r["rel_err"] for r in ad), tolerance_diff_rad=float(np.max(np.abs(a - b))), quantisation_rad=float(np.pi / 256))
    summ = dict(model="spinners", version=1, params=P, omega=w.round(6).tolist(), theta0=th0.round(6).tolist(), runs=runs, checks=checks, wall_s=time.time() - t0)
    json.dump(summ, open(os.path.join(out_dir, "spinners.json"), "w"), indent=1)
    print(json.dumps(dict(checks=checks, wall=summ["wall_s"]), indent=1))
    return summ


if __name__ == "__main__":
    run(sys.argv[1] if len(sys.argv) > 1 else ".")

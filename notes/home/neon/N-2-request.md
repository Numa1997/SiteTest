NEON REQUEST N-2: light pendulums swinging in a wind whose wake is a Kármán vortex street (a reference model, run once on Kaggle)

GOAL (plain words, and why)
The website Phyein Usul (repository Numa1997/SiteTest, branch `sky-and-wind`, from main at commit 5b09422) hangs pendulums in the
right margin of its home page. Today they are pairs tied by a spring (tools/sims/coupled.py, attached for the format). The user finds
them out of place and asks instead for "swinging pendula under a velocity wind field, the field lines (not arrows) present, guiding
their motion next to gravity", a problem the site has solved before: its double inverted pendulum page lets rods swing in named
flows (a breeze, gusts, a rolling eddy, a Kármán vortex street, ...) with the drag law of its lecture note, section 13 (the exact
functions are attached below). The motion is computed once on Kaggle by a reference model and stored; the page only plays it and
computes nothing. Write that model: tools/sims/windpend.py, and its entry in tools/sims/registry.json.

THE PHYSICAL SETUP (the user's rule: start from the setup; every parameter a symbol with a default, tunable)
- The margin is a tall strip of air. A steady wind U blows DOWN the strip (from the top of the page toward the bottom); somewhere
  above the page it has passed a post, and its wake is a Kármán vortex street: two rows of vortices of opposite sign, a distance h
  apart across the strip, spacing λ along it, staggered by λ/2, drifting down with the speed c = 0.8 U (as on the site). h/λ = 0.281,
  von Kármán's stable ratio.
- Coordinates: η across the strip (m, 0 at its centre, positive to the right), ξ along it (m, positive DOWN the page); time t.
  The field is the site's 'street' flow turned so it runs along ξ: the row function of the attached code, with its smoothing δ
  (ST_D), circulation from the same formula (q = 0.4 U λ / tanh(π h / λ)), plus the uniform stream U along +ξ. Give it as a stream
  function ψ(η, ξ − c t) plus the uniform part, so that the velocity is (u_η, u_ξ) from ψ and is divergence-free by construction;
  the code checks div = 0 numerically.
- Because the vortices only drift, the field is a travelling pattern: v(η, ξ, t) = v(η, ξ − c t). So it repeats in time with the
  period T = λ / c, and a pendulum hung lower by Δξ sees exactly the same wind Δξ / c later. One stored orbit per position across the
  strip therefore serves every beam down the page, played with the time shift ξ_beam / c. This is why this flow was chosen.
- The pendulums: each a light rigid rod of length L and diameter d (balsa, density ρ_r), pivoted at its top on a beam across the
  strip, with a light ball at its end (expanded polystyrene, radius R, density ρ_b). Defaults: L = 1.0 m, d = 0.01 m,
  ρ_r = 160 kg/m³, R = 0.04 m, ρ_b = 20 kg/m³: about 13 g of rod and 5 g of ball, so the air's push is a fair part of their weight
  and the swing is about 10–25°. Air at 25 °C as on the site: ρ = 1.184 kg/m³, μ = 1.849e-5 Pa s. g = 9.81 m/s².
- Each pendulum feels gravity and the drag of the air moving past it, nothing else. The pendulums do not change the wind (one-way).
  Angle θ from the downward vertical (positive toward +η). Rod drag per metre: the site's resistive force theory (33) plus the
  quadratic drag across the rod (34), C_D = 1.2, with w = v_body − v_air at each point of the rod, by 4-point Gauss–Legendre along it
  as dragF() does. Ball: Stokes drag 6πμR w plus ½ ρ C_D,b π R² |w| w, C_D,b = 0.47. Equation of motion about the pivot:
  I θ'' = − (m_r L/2 + m_b L) g sin θ + τ_rod + τ_ball, I = m_r L²/3 + m_b (L² + 2R²/5).
  Derive it in the docstring from the setup, step by step (Lagrange or torque balance), every term from where it comes, with the
  sources: the lecture note's (33)–(34) and the references it gives (resistive force theory: Gray and Hancock 1955; quadratic drag of
  a cylinder, C_D 1.0–1.3; sphere C_D 0.47).
- Positions across the strip: K = 3 pendulums per beam at η = −a, 0, +a (default a = 0.55 m, inside the strip's width WS = 2.5 m).
  Compute each one's orbit independently (they do not touch; check that the bobs of neighbours never come within 2R of each other).

WHAT TO COMPUTE
- Integrate each pendulum with DOP853 (SciPy), rtol 1e-10, atol 1e-12, from rest hanging straight, over whole periods T of the wind.
- It is a damped, periodically forced pendulum: after the start it settles onto a periodic motion with the wind's period (check, do
  not assume). After every period compare the state (θ, θ') with the one a period earlier; stop when the change is below 1e-8 rad and
  1e-8 rad/s, or fail loudly after 400 periods with the history of that change (then the motion is not periodic: chaos or a longer
  period; the error must say which it looks like, from the return map).
- Store one period of the settled motion, sampled at fps = 30 frames per second (frame count rounded, the exact dt in the header),
  for each of the K positions; the loop closes by construction; report its residual.
- For the field lines: store ψ on a grid across the strip (η from −WS/2 to WS/2, 64 points) and along one wavelength (ξ from 0 to λ,
  96 points, periodic) at t = 0. The page draws contours of ψ shifted by c t (that is the stored field moved, not recomputed). Store it
  as float32 with its grid in the header.
- Checks in the header: the energy balance of each pendulum over the stored period (kinetic plus potential energy change equals the
  work of the drag, integrated with the same quadrature: report the residual relative to the drag work); the loop residual; the same
  period at 100 times tighter tolerances (largest angle difference); the divergence of the field on the grid (largest |div| over the
  typical |∇v|); the largest swing of each pendulum; the closest approach of neighbouring bobs; the Reynolds number of the rod and of
  the ball at the largest relative speed (to say which drag rules); the number of periods it took to settle.
- Output, as coupled.py does: windpend.bin = b"WPD1", uint32 header length, JSON header (parameters, derived values, grids, checks),
  then the frames as int16 little-endian (rows: frames; columns: θ_1..θ_K in 1e-4 rad), then ψ as float32 little-endian (96 rows of
  64). Also windpend.json (the header, readable). run(out_dir) returns the header and prints a summary, as coupled.py.
- Time it: a few seconds to a minute on Kaggle's CPU (4 cores); use numpy and scipy only.

THE REGISTRY
Add the entry "windpend" to tools/sims/registry.json (attached whole) in the form of "coupled": model tools/sims/windpend.py, files
["windpend.bin"], one page: path "/", width 1600, height 1000, scroll 650, and a probe that reads the rails scene the way coupled's
probe does (the scene will be rewritten in a later request to load 'windpend', 'windpend.bin' and keep s.D, s.Bs, s.err the same).
Keep every other entry exactly as it is.

RULES THAT BIND THE CODE
- Python 3, numpy and scipy only; one file; no plotting; the parameters dictionary P at the top, every entry commented with its unit
  and meaning (as coupled.py); the docstring is the derivation, in plain words first, then the equations, numbered.
- The page will be written later; do not change any other file.

THE TESTS I WILL RUN ON YOUR ANSWER
1. python3 -c "import ast; ast.parse(open('tools/sims/windpend.py').read())" and python3 -c "import json; json.load(open('tools/sims/registry.json'))".
2. The run itself happens on Kaggle, never on my machine (the user's rule): I push the branch and run the notebook
   numakoudsie/phyein-usul-simulations with JOB = "windpend" at the branch commit (the notebook text is tools/sims/kaggle_sims.py,
   attached); it imports windpend and calls run(OUT). I read its log and its header: settled and periodic for all K, energy residual
   below 1e-6 of the drag work, loop residual below 1e-8, tolerance difference below 1e-6 rad, div below 1e-10, swings between 0.15
   and 0.5 rad, no near-collision.

ANSWER FORMAT
For each file, one fenced block whose first line is "FILE: <path>" followed by the complete new file; nothing else inside the blocks.
The files: tools/sims/windpend.py (new), tools/sims/registry.json (whole). After the blocks, a short list of what changed.

THE FILES (whole, as they stand on the branch), and the site's flow and drag code (exact functions, from
public/simulations/double-inverted-pendulum.html)

----- tools/sims/coupled.py -----
```
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
    m=10.0,        # kg, each bob: a steel ball (7850 kg/m³) of radius rb weighs 4/3 π rb³ · 7850 = 9.9 kg
    a=0.5,         # m, where the spring meets each rod, measured down from the pivot
    d=0.8,         # m, distance between the pivots = the spring's natural length; wide enough that the bobs never touch (checked)
    rb=0.067,      # m, radius of a bob (drawn; the check min_bob_gap_m must stay positive)
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

```

----- tools/sims/registry.json -----
```
{
 "about": "Registry of the simulations whose data is computed once on Kaggle: which files each model writes, and which live pages play them. Only names listed here are ever sent to Kaggle. tools/sims/verify_live.py reads it to check the live site after every run (docs/kaggle-sims.md, step 10).",
 "site": "https://phyeinusul.com",
 "sims": {
  "barton": {
   "dataset": "numakoudsie/phyein-usul-barton",
   "dataset_title": "Barton's pendulums: simulation data",
   "model": "tools/sims/barton.py",
   "files": [
    "barton.bin"
   ],
   "pages": [],
   "note": "Replaced on the home page by coupled (23 November 2026); kept until the coupled pendulums are verified live.",
   "figure": "Barton's pendulums (home page)",
   "page_url": "https://phyeinusul.com",
   "dataset_subtitle": "Barton's pendulums on the Phyein Usul home page: every Kaggle run",
   "dataset_about": "A row of pendulums of different lengths driven by one heavy pendulum: resonance, drawn in the margin of the home page."
  },
  "double_pendulum": {
   "model": "tools/sims/double_pendulum.py",
   "files": [
    "double_pendulum.json",
    "dp_11_09.bin"
   ],
   "about_files": "The model writes 108 files dp_<mass><length>_<theta1>.bin and double_pendulum.json; listed here are the two the page loads at its default start (equal masses and rods, 120 and 150 degrees). No page is listed until the page plays the data.",
   "pages": []
  },
  "wave_interference2": {
   "dataset": "numakoudsie/fig1-wave-interference",
   "dataset_title": "Fig. 1 Wave Interference: simulation data",
   "model": "tools/sims/wave_interference2.py",
   "files": [
    "geometry.bin",
    "dist_lo.bin"
   ],
   "files_note": "Generation 2 of Fig. 1: rings at nodes even in k, blended by the page, every table split into a bottom and a top half. The live check lists the two files every wide screen opens with.",
   "pages": [
    {
     "path": "/simulations/Circular%20Wave%20Interference%20Visualization.html",
     "width": 1600,
     "height": 1000,
     "scroll": 0,
     "probe": "(()=>{const s=window.__simData;if(!s)return {error:'no stored-data loader on the page'};if(s.err)return {error:s.err};if(!s.sha_ok||!s.gen)return {waiting:true};const d=Sim.data.ds;return {sha_ok:s.sha_ok,commit:s.gen.commit,date:s.gen.date,files:s.files,lambda:d.get('lambda'),damp:d.get('damp'),builds:d.get('builds'),renders:d.get('renders')};})()"
    }
   ],
   "figure": "Fig. 1 Circular Wave Interference",
   "page_url": "https://phyeinusul.com/simulations/Circular%20Wave%20Interference%20Visualization.html",
   "dataset_subtitle": "Fig. 1 Circular Wave Interference: every Kaggle run behind the page",
   "dataset_about": "Two point sources and the pattern their circular waves make: the field the page draws, computed on Kaggle."
  },
  "double_pendulum_smoke": {
   "dataset": "numakoudsie/fig2-double-pendulum",
   "dataset_title": "Fig. 2 Double Pendulum: simulation data",
   "model": "tools/sims/double_pendulum_smoke.py",
   "gpu": true,
   "timeout_s": 3600,
   "store": "release",
   "release_files": [
    "*.pack"
   ],
   "files": [
    "double_pendulum.json"
   ],
   "about_files": "Engine test for GPU runs with large data: one pack in the GitHub release sims-double_pendulum_smoke-<date>, the summary with every fingerprint committed. No page plays it.",
   "pages": [],
   "figure": "Fig. 2 Double Pendulum",
   "page_url": "https://phyeinusul.com/simulations/Double%20Pendulum.html",
   "dataset_subtitle": "Fig. 2 Double Pendulum: every Kaggle run behind the page, as the site plays it",
   "dataset_about": "Two rods, two masses, chaos: the swing computed on Kaggle's GPU with the page's own RK4 (step 1/600 s, 64-bit) for every start the page offers, 20 s each, stored as packs of int16 frames."
  },
  "double_pendulum_gpu": {
   "dataset": "numakoudsie/fig2-double-pendulum",
   "dataset_title": "Fig. 2 Double Pendulum: simulation data",
   "model": "tools/sims/double_pendulum_gpu.py",
   "gpu": true,
   "timeout_s": 14400,
   "store": "release",
   "release_files": [
    "*.pack"
   ],
   "files": [
    "double_pendulum.json"
   ],
   "about_files": "Fig. 2 in full: 25 packs (one per mass-length cell) in the GitHub release sims-double_pendulum_gpu-<date>; the summary with every runs file's pack, offset, size and SHA-256 is committed. No page is listed until the page plays it.",
   "pages": [],
   "figure": "Fig. 2 Double Pendulum",
   "page_url": "https://phyeinusul.com/simulations/Double%20Pendulum.html",
   "dataset_subtitle": "Fig. 2 Double Pendulum: every Kaggle run behind the page, as the site plays it",
   "dataset_about": "Two rods, two masses, chaos: the swing computed on Kaggle's GPU with the page's own RK4 (step 1/600 s, 64-bit) for every start the page offers, 20 s each, stored as packs of int16 frames."
  },
  "coupled": {
   "model": "tools/sims/coupled.py",
   "files": [
    "coupled.bin"
   ],
   "pages": [
    {
     "path": "/",
     "width": 1600,
     "height": 1000,
     "scroll": 650,
     "probe": "(()=>{const h=document.querySelector('[data-bg=rails]');const s=h&&h.__bgScene;if(!s)return {error:'no rails scene on the page'};if(s.err)return {error:s.err};if(!s.D)return {waiting:true};return {sha_ok:s.D.sha_ok,commit:s.D.gen.commit,date:s.D.gen.date,frames:s.D.hdr.frames,bars:s.Bs.length};})()"
    }
   ],
   "dataset": "numakoudsie/phyein-usul-coupled",
   "dataset_title": "Coupled pendulums: simulation data",
   "figure": "Coupled pendulums (home page)",
   "page_url": "https://phyeinusul.com",
   "dataset_subtitle": "Coupled pendulums on the Phyein Usul home page: every Kaggle run",
   "dataset_about": "Two pendulums joined by a spring trade their swing back and forth: the scene in the margin of the home page."
  }
 }
}

```

----- tools/sims/kaggle_sims.py -----
```
# Kaggle notebook "phyein-usul-simulations" (one notebook for every simulation of the site; one version per run).
# It fetches this repository at a pinned commit, runs the simulation's reference model, and writes its data under
# /kaggle/working/<YYYY-MM-DD>/<sim>/, the date of generation (docs/kaggle-pipeline.md, "Storage").
# CPU only: these models are small, so no GPU quota is spent.
JOB = "barton"                      # which simulation to compute; one model file per simulation in tools/sims/
COMMIT = "__COMMIT__"               # the commit of Numa1997/SiteTest whose tools/sims/ code is run
import subprocess, sys, os, json, time, datetime, hashlib, platform
T0 = time.time()
day = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
OUT = f"/kaggle/working/{day}/{JOB}"; os.makedirs(OUT, exist_ok=True)
print(platform.platform(), sys.version.split()[0], os.cpu_count(), "CPUs")
src = "/kaggle/working/src"
subprocess.run(["git", "clone", "-q", "--filter=blob:none", "--no-checkout", "https://github.com/Numa1997/SiteTest.git", src], check=True)
subprocess.run(["git", "-C", src, "sparse-checkout", "set", "tools/sims"], check=True)
subprocess.run(["git", "-C", src, "checkout", "-q", COMMIT], check=True)
sys.path.insert(0, f"{src}/tools/sims")
import numpy, scipy; print("numpy", numpy.__version__, "scipy", scipy.__version__)
mod = __import__(JOB)
hdr = mod.run(OUT)
files = {}
for f in sorted(os.listdir(OUT)):
    b = open(os.path.join(OUT, f), "rb").read(); files[f] = dict(bytes=len(b), sha256=hashlib.sha256(b).hexdigest())
index = dict(project="sims", job=JOB, date=day, source=dict(repo="Numa1997/SiteTest", commit=COMMIT, path=f"tools/sims/{JOB}.py"),
             machine=dict(platform=platform.platform(), cpus=os.cpu_count(), python=sys.version.split()[0], numpy=numpy.__version__, scipy=scipy.__version__),
             files=files, wall_s=time.time() - T0)
json.dump(index, open(f"{OUT}/index-{JOB}.json", "w"), indent=1)
print(json.dumps(index, indent=1))
subprocess.run(["rm", "-rf", src])

```

----- the site flow and drag functions (public/simulations/double-inverted-pendulum.html) -----
```
// constants of the 'street' flow, as defined on the page (m): ST_L the spacing λ, ST_H the gap h between the rows, ST_D the smoothing δ of each vortex
var ST_L = 1.6, ST_H = 0.281 * 1.6, ST_D = 0.35;


function row(X, Y, x0, y0, Gm) { var e = 2 * Math.PI * (Y - y0) / ST_L, z = 2 * Math.PI * (X - x0) / ST_L, D = Math.cosh(e) - Math.cos(z) + ST_D * ST_D; return [-Gm / (2 * ST_L) * Math.sinh(e) / D, Gm / (2 * ST_L) * Math.sin(z) / D]; }   // a row of vortices, smoothed

function fieldV(k, X, Y, t, U, nu) {   // the fluid's velocity (u, v) in m/s at the point (X, Y), Y above the rail, time t: the flows of section 13.3
            if (DEEP[k] && t < flowT0 + RAMP) { var rs = Math.max(0, (t - flowT0) / RAMP); U *= rs * rs * (3 - 2 * rs); }   // a deep and slow flow comes up over RAMP seconds from the moment it is chosen (or the liquid changed, or Reset), as U r(τ), r = 3τ² − 2τ³, τ = (t − t_on)/RAMP
            var z, e, th, q, c, xc, r2, f, a;
            switch (k) {
                case 'breeze': return [U, 0];
                case 'gusts': return [U * gust(t), 0];
                case 'ground': z = Y - Y_FLOOR; return [z > Z0 ? U * Math.log(z / Z0) / Math.log(-Y_FLOOR / Z0) : 0, 0];
                case 'lorry': return [U * lorry(t), 0];
                case 'fan': z = Math.max(0.5, X + 6); q = U * Math.cbrt(6) / (6 * JA * JA); e = JA * (Y - 0.6) / Math.pow(z, 2 / 3); th = Math.tanh(e);
                    return [6 * q * JA * JA * Math.pow(z, -1 / 3) * (1 - th * th), 2 * q * JA * Math.pow(z, -2 / 3) * (2 * e * (1 - th * th) - th)];
                case 'eddy': c = 0.4 * U; z = t - 20 * Math.floor(t / 20); xc = -6 + c * z; a = ED_RC * ED_RC + 4 * nu * z; r2 = (X - xc) * (X - xc) + (Y - 0.6) * (Y - 0.6);
                    f = r2 > 1e-12 ? ED_RC * U / ED_PK * (1 - Math.exp(-r2 / a)) / r2 : ED_RC * U / ED_PK / a; return [c - f * (Y - 0.6), f * (X - xc)];
                case 'river': z = Y - Y_FLOOR; return [z > 0 ? U * Math.pow(z / WH, 1 / 7) : 0, 0];
                case 'waves': a = U * Math.tanh(WK * WH) / WOM; z = Y - Y_FLOOR; e = WK * X - WOM * t; q = a * WOM / Math.sinh(WK * WH); return [q * Math.cosh(WK * z) * Math.cos(e), q * Math.sinh(WK * z) * Math.sin(e)];
                case 'shear': return [U * Y, 0]; case 'own': return OWN.u ? ownAt(X, Y, t, U) : [0, 0];
                case 'jets': return [U * X, -U * Y];
                case 'cells': e = U * Math.exp(-2 * nu * Math.PI * Math.PI * t); return [e * Math.sin(Math.PI * X) * Math.cos(Math.PI * Y), -e * Math.cos(Math.PI * X) * Math.sin(Math.PI * Y)];
                case 'internal': e = IW_K * X - IW_W * t; return [U * Math.cos(e) * Math.cos(IW_M * Y), U * IW_K / IW_M * Math.sin(e) * Math.sin(IW_M * Y)];   // ψ = (U/m) cos(kx − ωt) sin(my)
                case 'gyre': q = 0.25 * Math.sin(DG_W * t); z = (X + 3) / 3; e = (Y + 1.5) / 3; f = q * z * z + (1 - 2 * q) * z; a = 3 * U / Math.PI;   // ψ = A sin(πf(x′, t)) sin(πy′), Shadden, Lekien and Marsden (2005), on x′ = (x + 3 m)/3 m, y′ = (y + 1.5 m)/3 m
                    return [a * Math.PI / 3 * Math.sin(Math.PI * f) * Math.cos(Math.PI * e), -a * Math.PI / 3 * Math.cos(Math.PI * f) * Math.sin(Math.PI * e) * (2 * q * z + 1 - 2 * q)];
                case 'deepsea': z = 0; e = 0; for (q = 0; q < 6; q++) { var M6 = DS[q], ph = M6[0] * X + M6[1] * Y - M6[2] * t + M6[3], ca = U * Math.cos(ph) / Math.sqrt(6); z += ca * M6[1] / M6[4]; e -= ca * M6[0] / M6[4]; } return [z, e];   // ψ = Σ (U/√6)/|k_j| sin(k_j·r − ω_j t + φ_j)
                case 'tides': e = TB_K * X; c = Math.cos(e - TB_W1 * t) + Math.cos(e - TB_W2 * t + 1); f = Math.sin(e - TB_W1 * t) + Math.sin(e - TB_W2 * t + 1); return [U / 2 * c, U / 2 * TB_K * Y * f];   // ψ = (U/2) y (cos(kx − ω₁t) + cos(kx − ω₂t + 1))
                case 'street': c = 0.8 * U * t; q = 0.4 * U * ST_L / Math.tanh(Math.PI * ST_H / ST_L); f = row(X, Y, c + ST_L / 2, 0.6 + ST_H / 2, -q); a = row(X, Y, c, 0.6 - ST_H / 2, q); return [U + f[0] + a[0], f[1] + a[1]];
            }
            return [0, 0]; }

// the drag of the medium on the rods: resistive force theory (33) plus quadratic drag (34), 4-point Gauss–Legendre
function dragF(p, s, o) {   // the drag of the medium on rods and cart, (33)–(35), by 4-point Gauss–Legendre per rod: cheap enough for the planner. Still medium: v_f = 0.
            /* with a flow the controller is told (13.8): v_f at each point from the field, frozen at the time p.ft, with the cart's frame shifted by p.fx0; the push of the flow's own acceleration (39) is left out */
            var F = p.fl, s1 = Math.sin(s[1]), c1 = Math.cos(s[1]), s2 = Math.sin(s[2]), c2 = Math.cos(s[2]), xd = s[3], ad = s[4], bd = s[5], Q0 = 0, Q1 = 0, Q2 = 0, i, k, fx0 = (p.fx0 || 0) + s[0], fv;
            for (k = 0; k < 2; k++) { var L = k ? p.L2 : p.L1, sn = k ? s2 : s1, cs = k ? c2 : c1, xi = F.xi[k], om = k ? bd : ad;
                for (i = 0; i < 4; i++) { var sg = GL4.x[i] * L, wq = GL4.w[i] * L, vx = xd + (k ? p.L1 * c1 * ad : 0) + sg * cs * om, vy = -(k ? p.L1 * s1 * ad : 0) - sg * sn * om;
                    if (F.acc) { fv = fieldV(F.field, fx0 + (k ? p.L1 * s1 : 0) + sg * sn, (k ? p.L1 * c1 : 0) + sg * cs, p.ft || 0, F.U, F.nu); vx -= fv[0]; vy -= fv[1]; }
                    var wt = vx * sn + vy * cs, wn = vx * cs - vy * sn, fn = -xi * wn - F.cq * Math.abs(wn) * wn, ft = -xi / 2 * wt, fx = ft * sn + fn * cs, fy = ft * cs - fn * sn;
                    Q0 += wq * fx; if (k) { Q1 += wq * p.L1 * (fx * c1 - fy * s1); Q2 += wq * sg * fn; } else Q1 += wq * sg * fn; } }
            var wc = xd - (F.acc ? fieldV(F.field, fx0, -CART_H / 2, p.ft || 0, F.U, F.nu)[0] : 0); o[0] = Q0 - F.cl * wc - F.cc * Math.abs(wc) * wc; o[1] = Q1; o[2] = Q2; }
        var GL4 = { x: [0.0694318442029737, 0.3300094782075719, 0.6699905217924281, 0.9305681557970263], w: [0.1739274225687269, 0.3260725774312731, 0.3260725774312731, 0.1739274225687269] }, dq3 = new Float64Array(3), CLO = 1e-4;   // the certified-level search may start below W = 1: in a liquid c* can be small

```

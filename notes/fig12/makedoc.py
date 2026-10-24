"""Write docs/simulations/fig12-furuta-pendulum.md from the page: the function map and the store's variables, with line links.
Run after any edit of the page: python3 notes/fig12/makedoc.py"""
import re, os, json, subprocess
ROOT = os.path.join(os.path.dirname(__file__), '..', '..')
PAGE = 'public/simulations/furuta-pendulum.html'
src = open(os.path.join(ROOT, PAGE)).read(); lines = src.split('\n')
def L(n, m=None): return f'[L{n}](../../{PAGE}#L{n})' if m is None else f'[L{n}–{m}](../../{PAGE}#L{n}-L{m})'
def find(pat):
    for i, l in enumerate(lines):
        if re.search(pat, l): return i + 1
    raise SystemExit('not found: ' + pat)
walk = open(os.path.join(ROOT, 'public/scripts/walk/furuta.js')).read()
cat = open(os.path.join(ROOT, 'public/scripts/catalog.js')).read().split('\n')
c0 = next(i for i, l in enumerate(cat) if "id: 'furuta-pendulum'" in l); c1 = next(i for i in range(c0, len(cat)) if 'added:' in cat[i])
thumb = os.path.getsize(os.path.join(ROOT, 'public/images/sims/furuta-pendulum.webp'))
FUN = [  # (name, what it does, equation)
 ('rig', 'reads the controls at the moment of solving into one parameter object p', ''),
 ('derive', 'the constants of the energies: J_r, J₀, J_p, h, G, Δ', '(2), (3)'),
 ('accel', 'the equations of motion solved for (φ̈, α̈) by Cramer’s rule, for a given current I', '(7)'),
 ('energy', 'T + U of arm and pendulum', '(2) + (3)'),
 ('penEnergy', 'the pendulum’s own energy E_p as if its hinge stood still', '(12)'),
 ('wrap', 'an angle reduced to (−π, π]', ''),
 ('err', 'the error ỹ = (φ − φ*, α, φ̇, α̇), angles wrapped', ''),
 ('rhs', 'the state’s rate for a voltage V_m, through the motor law', '(6), (7)'),
 ('linearise', 'A and B at the top by central differences of rhs()', '(9)'),
 ('lqr', 'the Riccati equation by the matrix sign function; returns K and P', '(16), (17)'),
 ('eig', 'eigenvalues: Faddeev–LeVerrier and Durand–Kerner', '(10)'),
 ('rankOf', 'rank of [B, AB, A²B, A³B]', '(11)'),
 ('lyap', 'ỹᵀPỹ', '(18)'),
 ('catchVolt', 'the LQR law V_m = −Kỹ, before the clip', ''),
 ('catchOnly', 'the catch alone from one start, scalar RK4: does ỹᵀPỹ fall below 0.05 within T?', ''),
 ('chol', 'Cholesky factor of a symmetric positive matrix', ''),
 ('measureC', 'the largest level c whose sampled surface the catch rescues (240 starts, 12 halvings)', '(19)'),
 ('measureBasin', 'the rescue grid in the slice φ = φ*, φ̇ = 0 (the page measures it in slices in startBasin())', ''),
 ('design', 'linearise, LQR, eigenvalues, rank, and c (cached per design)', '(9)–(19)'),
 ('decide', 'the supervisor: swing-up → catch below c_in, catch → swing-up above c_out', '(19)'),
 ('drive', 'the motor voltage, current and clip flag for one state and mode', '(6), (13), (14)'),
 ('stepRK4', 'one RK4 step of the closed loop, with the three energy integrals', '(20)'),
 ('run', 'the whole run; the mode decided once every TS = 1 ms', ''),
 ('solve', 'design, run, store, the half-step rerun, the books, the times', ''),
 ('settleTime', 'first stored time after which every error stays within 0.01', ''),
 ('startBasin', 'measures the rescue grid in slices after the run is shown', ''),
 ('geom', 'the rig’s oblique projection, scales and chart boxes', ''),
 ('rodPts', 'screen positions of the arm’s tip and the pendulum’s knob', '(1)'),
 ('drawRig', 'motor, rim, flag, goal, arm, pendulum, torque arc, energy bars, mode label', ''),
 ('drawChart', 'the 8 s window of α and φ − φ*, and the whole-run strip', ''),
 ('drawForces', 'the drive profile: V_m, back-emf, and the two Lyapunov functions', ''),
 ('drawPhase', 'the phase portraits with the rescue grid, separatrix and hand-over ellipse', ''),
 ('frame', 'copies the stored sample nearest t_play into the *_now scalars, then draws', ''),
 ('pose', 'the pose the hand asks for: arm bearing, or α in the pendulum’s plane', ''),
 ('holdState', 'while the hand holds: the live state and what the controller would apply', ''),
 ('release', 'on letting go: solve again from the hand’s state', ''),
 ('replay', 'the data panel’s check: the same RK4 and switch rerun to sample n', ''),
]
rows = []
for name, what, eq in FUN:
    n = find(r'function ' + re.escape(name) + r'\(')
    rows.append(f'| `{name}()` | {L(n)} | {what} | {eq} |')
# store variables
vars_ = re.findall(r"ds\.(var|coord)\('([A-Za-z0-9_]+)', (\[[^\]]*\]|'[a-z]+'), ([A-Za-z0-9']+), \{ symbol: '([^']*)'(?:, units: '([^']*)')?, long_name: '([^']*)', computed_in: '([^']*)'", src)
vrows = [f"| `{v[1]}` | {v[4]} | {v[5] or ''} | {v[6]} | {v[7]} |" for v in vars_]
checks = re.findall(r"^\s{16}([A-Za-z0-9_]+): (?:function|constCheck|stateCol)", src[src.index('check: {'):src.index('drawn: {')], re.M)
drawn = re.findall(r"^\s{16}([A-Za-z0-9_]+): function", src[src.index('drawn: {'):src.index('round: {')], re.M)
nlines = len(lines); nbytes = len(src.encode())
steps = walk.count("title: '")
doc = f"""# Fig. 12 · Furuta Pendulum

| | |
|---|---|
| Page | [{PAGE}](../../{PAGE}) ({nlines:,} lines, {nbytes:,} bytes) |
| Walkthrough | [public/scripts/walk/furuta.js](../../public/scripts/walk/furuta.js) ({walk.count(chr(10))} lines, {steps} steps, key `furuta`) |
| Thumbnail | [public/images/sims/furuta-pendulum.webp](../../public/images/sims/furuta-pendulum.webp) (WebP, 800 × 500 px, {thumb/1000:.1f} kB) |
| Catalog entry | [public/scripts/catalog.js#L{c0}](../../public/scripts/catalog.js#L{c0}-L{c1+1}) (`id: 'furuta-pendulum'`, `fig: 12`, `field: 'control'`, `stage: 2`) |
| Working notes | [notes/fig12/](../../notes/fig12/): `derive.py` (SymPy, 21 checks), `physics.py` and `roa.py` (NumPy reference), the browser scripts `smoke.cjs`, `interact.cjs`, `notecheck.cjs`, `shots.cjs`, `dump.cjs`, `thumb.cjs`, and the blind reports `check-L0.md` and `referee.md` |

A pendulum, a uniform rod, hangs from the tip of an arm that a DC motor turns in a horizontal circle. The motor's voltage is
the only input. The reader chooses a controller (Off, Catch only, Swing up), a target angle φ* for the arm (slider or a flag on the
turntable's rim), the LQR weights, the swing gain, the arm length and the supply limit, and can grab the pendulum's knob or the arm,
push it anywhere and let go. As in Figs. 9 and 10 the whole run is solved first with RK4 and stored; each frame draws one stored
sample. Nothing is integrated while the reader watches.

**Review.** The note was checked blind by a derivation checker (`notes/fig12/check-L0.md`: 20 of 20 equations verified, one
statement wrong, fixed) and a referee (`notes/fig12/referee.md`: 10 must-fix and 32 minor findings). All ten must-fix findings
were fixed on 24 October 2026: the swing picture (a key on a string, not a child pumping), the matrix (9), the linearisation steps
and the meaning of eigenvalues, the Riccati equation derived from the cost-to-go and (18) proved, the sign of the arm gains
(non-minimum phase), the sentence on (18) in §10, the Lagrangian of §5, one letter one meaning, Problem 3, and the uniform rod in
Figure 1. Most minor findings were fixed in the same pass.

In this page, a link such as {L(find('function accel'))} points to a line of `furuta-pendulum.html`.

## The physics in one picture

**What you would see.** A broom balanced on a palm: the hand moves under the lean. A key on a string jiggled by the hand: energy fed
in through the moving suspension, in step with the swing. The motor does the second to bring the rod up and the first to hold it there.

**Symbols.** One letter, one meaning (the referee's rule): δt is the RK4 step (h is the coupling), H_R and H_b the heats (bold Q the
cost matrix), w_φ and w_α the LQR weights, 𝒥 the cost, t_end the end of the run, Γ the generalised forces, ϱ a wire's distance
from the axis.

**The mechanism.** Two generalised coordinates (φ, α), α from straight up; the Lagrangian of a rigid arm and a thin rod (2)–(3);
a permanent-magnet DC motor fed from a voltage source, V_m = RI + kφ̇ with the inductance dropped (Λ/R = 0.5 ms against 0.143 s),
τ = kI (4)–(6). The motor reaches the rod only through h cos α φ̈ in the rod's equation (7); near the top the linear model (9) is
controllable through h = ½ m_p r L (11). Swing-up: the arm acceleration u = sat[k_E(E_p − G) α̇ cos α] − k_φ(φ − φ*) − k_ω φ̇ (13),
turned into a voltage by collocated partial feedback linearisation (14); ½(E_p − G)² is its Lyapunov function. Catch: LQR (15)–(17),
V_m = −Kỹ, Lyapunov function ỹᵀPỹ (18). Hand-over (19) when ỹᵀPỹ < c_in = c/2, where c is the largest level whose 240 sampled
starts the catch rescues; back when it exceeds c. Energy book (20): E(0) + W_in − H_R − H_b − E(t_end) = 0.

Numbers at the defaults (from the page's store): K = (−1.41, −34.29, −1.42, −4.46); closed-loop eigenvalues −24.57, −5.44, −3.52,
−2.36 1/s; open loop at the top −10.32, −0.83, 0, +9.48 1/s; c = 9.78, c_in = 4.89; 339 of 1147 grid starts rescued; caught at
2.75 s after 4 half-swings, settled at 5.22 s; δt vs δt/2 difference 5.9 × 10⁻⁵ at 2.61 s; energy book 5.7 × 10⁻¹¹ J;
W_in = 14.15 J, H_R = 13.91 J (13.80 J of it before the catch), H_b = 0.004 J, E rises by 2G = 0.235 J. c, c_in and ỹᵀPỹ are in seconds
(the integrand of the cost 𝒥 is a pure number).

## How the code computes it

1. **Solve** ({L(find('function solve'))}): `rig()` reads the controls, `design()` linearises at the top, solves the Riccati
   equation, finds both sets of eigenvalues and the rank, and measures c once per design (about a second, cached by
   arm length, supply limit and weights). `run()` integrates (7) with the drive by RK4, δt = 1 ms (`H` in the code), 20 s; the supervisor `decide()`
   runs once every TS = 1 ms (every step at δt, every second step at δt/2), so the half-step rerun switches at the same instants.
2. **Store**: every tenth state (10 ms, 2001 samples) with V_m, I, τ, E, E_p, ỹᵀPỹ, the three energy integrals, the mode and the
   clip flag. Then the same run with δt/2 (not stored) gives `err_half`; the book gives `balance`.
3. **Play**: the clock advances `t_play`; `frame()` copies sample round(t_play / 10 ms) into the `*_now` scalars and draws.
   After the first frame, `startBasin()` measures the 37 × 31 rescue grid in slices of four rows (about a second in all).
4. **The hand**: pointer down on the knob (radius about 18 px), on the arm (14 px from its bar), or on the flag. While held the
   clock stops, the pose follows the pointer (`pose()`), speeds are smoothed over 50 ms, nothing is stored. On release, `solve()`
   from that state. The flag sets φ* in steps of 5° and re-solves from the state on screen.
5. **First load**: the page paints, shows "Measuring where the catch can take over…", and solves 30 ms later.

## Function map

| Function | Line | What it does | Equation |
|---|---|---|---|
""" + '\n'.join(rows) + f"""

## Controls

| Control | Range | Default | What it changes |
|---|---|---|---|
| Presets Off / Catch only / Swing up | — | Swing up | `preset`: off disconnects the amplifier (I = 0); catch runs LQR always; swing runs (13)–(14) and hands over by (19) |
| Target arm angle φ* (`#phs`, flag) | −180° … 180°, 5° | 60° | the goal; re-solves on change from the state on screen |
| Pendulum weight w_α (`#qa`) | 2 … 200 | 40 | LQR weight; a new design (c measured again) |
| Arm weight w_φ (`#qp`) | 0.1 … 20 | 2 | LQR weight |
| Effort weight ρ (`#rho`, log₁₀) | 10^−1.5 … 10^1 | 1 | LQR weight on V_m² |
| Swing gain k_E (`#kE`) | 0 … 120 | 40 | the pump's gain in (13) |
| Arm length r (`#ra`) | 0.02 … 0.25 m | 0.16 m | J_r, J₀, h; the drawing scale does not change |
| Supply limit V_max (`#vmax`) | 3 … 24 V | 12 V | the amplifier's clip |
| Solve / Pause / From t = 0, seek, playback speed | | | as on Figs. 9–11 |

Sliders other than φ* mark the run stale; Solve recomputes. Fixed: the speed weights 0.5 and 2, a_max = 30 rad/s², k_φ = 4 s⁻²,
k_ω = 3 s⁻¹, the start nudge 3°, the rescue criterion ỹᵀPỹ < 0.05 after 3 s at a 2 ms step.

## What the page writes into the data store

`Sim.dataset({{ title: 'Furuta pendulum' }})`, dimensions `k` (4), `kk` (16, P row by row), `ia` × `iv` (37 × 31, the rescue grid)
and `n` (2001, the stored run). Every variable, with its symbol, units, meaning and the function that writes it:

| Name | Symbol | Units | Meaning | Written in |
|---|---|---|---|---|
""" + '\n'.join(vrows) + f"""

**Checks** (`Sim.data.check`, {len(checks)} entries plus the `*_now` scalars): every slider value against its control;
every constant against the code; every derived constant by its formula from the stored inputs; K, P, both sets of eigenvalues and the
rank by running `design()` again from the stored parameters; c by running the bisection again; each grid cell by running the catch
again from that start; the four state arrays, W_in, Q_R, Q_b and the mode by rerunning the same RK4 and the same switch from y(0)
to sample n (`replay()`); V_m, I, τ, E, E_p and ỹᵀPỹ at a sample from the stored state by their formulas; the balance, t_catch,
t_settle, t_sat, the half-step error and the drawing positions from their stored inputs.

**Read-backs** (`Sim.data.drawn`): {', '.join('`' + d + '`' for d in drawn)}. Each checks alpha before colour: the knob is burgundy
ink, the arm grey ink half-way along it, the flag burgundy or dark ink, α and φ − φ* on the window chart dark and burgundy ink;
a sample outside the 8 s window, or φ − φ* beyond ±3.6 rad, returns `ok: null` with the reason.

**Round**: two seconds of the stored run, time variable `t_play`, columns φ, α, V_m, E_p, ỹᵀPỹ; blocked in the last two seconds.

## Where the drawing and the store differ

The `about` paragraph of `Sim.data` says it in the page. In short: the oblique view (24°) and the schematic motor can, hub, rim and knob;
the torque arc scaled to the stall torque; α wrapped to (−π, π] on the time chart and in the phase portrait (the stored α is not);
Lyapunov values below 10⁻⁶ drawn at 10⁻⁶; the rescue grid measured with the catch alone at a 2 ms step, not the stored run's 1 ms.

## How to change it safely

- A change to the physics functions changes the run: run `node notes/fig12/smoke.cjs`, `node notes/fig12/interact.cjs`,
  `node notes/fig12/notecheck.cjs` and `node notes/walkcheck.cjs`, then `python3 notes/fig12/makedoc.py` and `python3 tools/inventory.py`.
- Every number in the note is from `node notes/fig12/dump.cjs`; change them together.
- The walkthrough quotes page lines character for character; `node notes/walkcheck.cjs` finds any that drifted.
- After an English edit, `python3 tools/i18n/build.py` and `--check`.
"""
open(os.path.join(ROOT, 'docs/simulations/fig12-furuta-pendulum.md'), 'w').write(doc)
print('wrote', len(doc), 'bytes;', len(rows), 'functions,', len(vrows), 'variables,', len(checks), 'checks,', len(drawn), 'read-backs')

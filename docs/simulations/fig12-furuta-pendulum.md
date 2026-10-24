# Fig. 12 · Furuta Pendulum

| | |
|---|---|
| Page | [public/simulations/furuta-pendulum.html](../../public/simulations/furuta-pendulum.html) (1,481 lines, 178,707 bytes) |
| Walkthrough | [public/scripts/walk/furuta.js](../../public/scripts/walk/furuta.js) (158 lines, 9 steps, key `furuta`) |
| Thumbnail | [public/images/sims/furuta-pendulum.webp](../../public/images/sims/furuta-pendulum.webp) (WebP, 800 × 500 px, 11.3 kB) |
| Catalog entry | [public/scripts/catalog.js#L217](../../public/scripts/catalog.js#L217-L232) (`id: 'furuta-pendulum'`, `fig: 12`, `field: 'control'`, `stage: 2`) |
| Working notes | [notes/fig12/](../../notes/fig12/): `derive.py` (SymPy, 21 checks), `physics.py` and `roa.py` (NumPy reference), the browser scripts `smoke.cjs`, `interact.cjs`, `notecheck.cjs`, `shots.cjs`, `dump.cjs`, `thumb.cjs`, and the blind reports `check-L0.md` and `referee.md` |

A pendulum, a uniform rod, hangs from the tip of an arm that a DC motor turns in a horizontal circle. The motor's voltage is
the only input. The reader chooses a controller (Off, Catch only, Swing up), a target angle φ* for the arm (slider or a flag on the
turntable's rim), the LQR weights, the swing gain, the arm length and the supply limit, and can grab the pendulum's knob or the arm,
push it anywhere and let go. As in Figs. 9 and 10 the whole run is solved first with RK4 and stored; each frame draws one stored
sample. Nothing is integrated while the reader watches.

In this page, a link such as [L597](../../public/simulations/furuta-pendulum.html#L597) points to a line of `furuta-pendulum.html`.

## The physics in one picture

**What you would see.** A broom balanced on a palm: the hand moves under the lean. A child on a swing: energy fed in step with the
motion. The motor does the second to bring the rod up and the first to hold it there.

**The mechanism.** Two generalised coordinates (φ, α), α from straight up; the Lagrangian of a rigid arm and a thin rod (2)–(3);
a permanent-magnet DC motor fed from a voltage source, V_m = RI + kφ̇ with the inductance dropped (Λ/R = 0.5 ms against 0.143 s),
τ = kI (4)–(6). The motor reaches the rod only through h cos α φ̈ in the rod's equation (7); near the top the linear model (9) is
controllable through h = ½ m_p r L (11). Swing-up: the arm acceleration u = sat[k_E(E_p − G) α̇ cos α] − k_φ(φ − φ*) − k_ω φ̇ (13),
turned into a voltage by collocated partial feedback linearisation (14); ½(E_p − G)² is its Lyapunov function. Catch: LQR (15)–(17),
V_m = −Kỹ, Lyapunov function ỹᵀPỹ (18). Hand-over (19) when ỹᵀPỹ < c_in = c/2, where c is the largest level whose 240 sampled
starts the catch rescues; back when it exceeds c. Energy book (20): E(0) + W_in − Q_R − Q_b − E(T) = 0.

Numbers at the defaults (from the page's store): K = (−1.41, −34.29, −1.42, −4.46); closed-loop eigenvalues −24.57, −5.44, −3.52,
−2.36 1/s; open loop at the top −10.32, −0.83, 0, +9.48 1/s; c = 9.78, c_in = 4.89; 339 of 1147 grid starts rescued; caught at
2.75 s after 4 half-swings, settled at 5.22 s; h vs h/2 difference 5.9 × 10⁻⁵ at 2.61 s; energy book 5.7 × 10⁻¹¹ J;
W_in = 14.15 J, Q_R = 13.91 J, Q_b = 0.004 J, E rises by 2G = 0.235 J.

## How the code computes it

1. **Solve** ([L814](../../public/simulations/furuta-pendulum.html#L814)): `rig()` reads the controls, `design()` linearises at the top, solves the Riccati
   equation, finds both sets of eigenvalues and the rank, and measures c once per design (about a second, cached by
   arm length, supply limit and weights). `run()` integrates (7) with the drive by RK4, h = 1 ms, 20 s; the supervisor `decide()`
   runs once every TS = 1 ms (every step at h, every second step at h/2), so the half-step rerun switches at the same instants.
2. **Store**: every tenth state (10 ms, 2001 samples) with V_m, I, τ, E, E_p, ỹᵀPỹ, the three energy integrals, the mode and the
   clip flag. Then the same run with h/2 (not stored) gives `err_half`; the book gives `balance`.
3. **Play**: the clock advances `t_play`; `frame()` copies sample round(t_play / 10 ms) into the `*_now` scalars and draws.
   After the first frame, `startBasin()` measures the 37 × 31 rescue grid in slices of four rows (about a second in all).
4. **The hand**: pointer down on the knob (radius about 18 px), on the arm (14 px from its bar), or on the flag. While held the
   clock stops, the pose follows the pointer (`pose()`), speeds are smoothed over 50 ms, nothing is stored. On release, `solve()`
   from that state. The flag sets φ* in steps of 5° and re-solves from the state on screen.
5. **First load**: the page paints, shows "Measuring where the catch can take over…", and solves 30 ms later.

## Function map

| Function | Line | What it does | Equation |
|---|---|---|---|
| `rig()` | [L587](../../public/simulations/furuta-pendulum.html#L587) | reads the controls at the moment of solving into one parameter object p |  |
| `derive()` | [L592](../../public/simulations/furuta-pendulum.html#L592) | the constants of the energies: J_r, J₀, J_p, h, G, Δ | (2), (3) |
| `accel()` | [L597](../../public/simulations/furuta-pendulum.html#L597) | the equations of motion solved for (φ̈, α̈) by Cramer’s rule, for a given current I | (7) |
| `energy()` | [L606](../../public/simulations/furuta-pendulum.html#L606) | T + U of arm and pendulum | (2) + (3) |
| `penEnergy()` | [L611](../../public/simulations/furuta-pendulum.html#L611) | the pendulum’s own energy E_p as if its hinge stood still | (12) |
| `wrap()` | [L612](../../public/simulations/furuta-pendulum.html#L612) | an angle reduced to (−π, π] |  |
| `err()` | [L613](../../public/simulations/furuta-pendulum.html#L613) | the error ỹ = (φ − φ*, α, φ̇, α̇), angles wrapped |  |
| `rhs()` | [L628](../../public/simulations/furuta-pendulum.html#L628) | the state’s rate for a voltage V_m, through the motor law | (6), (7) |
| `linearise()` | [L629](../../public/simulations/furuta-pendulum.html#L629) | A and B at the top by central differences of rhs() | (9) |
| `lqr()` | [L636](../../public/simulations/furuta-pendulum.html#L636) | the Riccati equation by the matrix sign function; returns K and P | (16), (17) |
| `eig()` | [L659](../../public/simulations/furuta-pendulum.html#L659) | eigenvalues: Faddeev–LeVerrier and Durand–Kerner | (10) |
| `rankOf()` | [L680](../../public/simulations/furuta-pendulum.html#L680) | rank of [B, AB, A²B, A³B] | (11) |
| `lyap()` | [L694](../../public/simulations/furuta-pendulum.html#L694) | ỹᵀPỹ | (18) |
| `catchVolt()` | [L695](../../public/simulations/furuta-pendulum.html#L695) | the LQR law V_m = −Kỹ, before the clip |  |
| `catchOnly()` | [L696](../../public/simulations/furuta-pendulum.html#L696) | the catch alone from one start, scalar RK4: does ỹᵀPỹ fall below 0.05 within T? |  |
| `chol()` | [L720](../../public/simulations/furuta-pendulum.html#L720) | Cholesky factor of a symmetric positive matrix |  |
| `measureC()` | [L726](../../public/simulations/furuta-pendulum.html#L726) | the largest level c whose sampled surface the catch rescues (240 starts, 12 halvings) | (19) |
| `measureBasin()` | [L743](../../public/simulations/furuta-pendulum.html#L743) | the rescue grid in the slice φ = φ*, φ̇ = 0 (the page measures it in slices in startBasin()) |  |
| `design()` | [L753](../../public/simulations/furuta-pendulum.html#L753) | linearise, LQR, eigenvalues, rank, and c (cached per design) | (9)–(19) |
| `decide()` | [L764](../../public/simulations/furuta-pendulum.html#L764) | the supervisor: swing-up → catch below c_in, catch → swing-up above c_out | (19) |
| `drive()` | [L771](../../public/simulations/furuta-pendulum.html#L771) | the motor voltage, current and clip flag for one state and mode | (6), (13), (14) |
| `stepRK4()` | [L788](../../public/simulations/furuta-pendulum.html#L788) | one RK4 step of the closed loop, with the three energy integrals | (20) |
| `run()` | [L802](../../public/simulations/furuta-pendulum.html#L802) | the whole run; the mode decided once every TS = 1 ms |  |
| `solve()` | [L814](../../public/simulations/furuta-pendulum.html#L814) | design, run, store, the half-step rerun, the books, the times |  |
| `settleTime()` | [L863](../../public/simulations/furuta-pendulum.html#L863) | first stored time after which every error stays within 0.01 |  |
| `startBasin()` | [L875](../../public/simulations/furuta-pendulum.html#L875) | measures the rescue grid in slices after the run is shown |  |
| `geom()` | [L945](../../public/simulations/furuta-pendulum.html#L945) | the rig’s oblique projection, scales and chart boxes |  |
| `rodPts()` | [L961](../../public/simulations/furuta-pendulum.html#L961) | screen positions of the arm’s tip and the pendulum’s knob | (1) |
| `drawRig()` | [L967](../../public/simulations/furuta-pendulum.html#L967) | motor, rim, flag, goal, arm, pendulum, torque arc, energy bars, mode label |  |
| `drawChart()` | [L1057](../../public/simulations/furuta-pendulum.html#L1057) | the 8 s window of α and φ − φ*, and the whole-run strip |  |
| `drawForces()` | [L1105](../../public/simulations/furuta-pendulum.html#L1105) | the drive profile: V_m, back-emf, and the two Lyapunov functions |  |
| `drawPhase()` | [L1152](../../public/simulations/furuta-pendulum.html#L1152) | the phase portraits with the rescue grid, separatrix and hand-over ellipse |  |
| `frame()` | [L1223](../../public/simulations/furuta-pendulum.html#L1223) | copies the stored sample nearest t_play into the *_now scalars, then draws |  |
| `pose()` | [L1249](../../public/simulations/furuta-pendulum.html#L1249) | the pose the hand asks for: arm bearing, or α in the pendulum’s plane |  |
| `holdState()` | [L1266](../../public/simulations/furuta-pendulum.html#L1266) | while the hand holds: the live state and what the controller would apply |  |
| `release()` | [L1298](../../public/simulations/furuta-pendulum.html#L1298) | on letting go: solve again from the hand’s state |  |
| `replay()` | [L1319](../../public/simulations/furuta-pendulum.html#L1319) | the data panel’s check: the same RK4 and switch rerun to sample n |  |

## Controls

| Control | Range | Default | What it changes |
|---|---|---|---|
| Presets Off / Catch only / Swing up | — | Swing up | `preset`: off disconnects the amplifier (I = 0); catch runs LQR always; swing runs (13)–(14) and hands over by (19) |
| Target arm angle φ* (`#phs`, flag) | −180° … 180°, 5° | 60° | the goal; re-solves on change from the state on screen |
| Pendulum weight q_α (`#qa`) | 2 … 200 | 40 | LQR weight; a new design (c measured again) |
| Arm weight q_φ (`#qp`) | 0.1 … 20 | 2 | LQR weight |
| Effort weight ρ (`#rho`, log₁₀) | 10^−1.5 … 10^1 | 1 | LQR weight on V_m² |
| Swing gain k_E (`#kE`) | 0 … 120 | 40 | the pump's gain in (13) |
| Arm length r (`#ra`) | 0.02 … 0.25 m | 0.16 m | J_r, J₀, h; the drawing scale does not change |
| Supply limit V_max (`#vmax`) | 3 … 24 V | 12 V | the amplifier's clip |
| Solve / Pause / From t = 0, seek, playback speed | | | as on Figs. 9–11 |

Sliders other than φ* mark the run stale; Solve recomputes. Fixed: the speed weights 0.5 and 2, a_max = 30 rad/s², k_φ = 4 s⁻²,
k_ω = 3 s⁻¹, the start nudge 3°, the rescue criterion ỹᵀPỹ < 0.05 after 3 s at a 2 ms step.

## What the page writes into the data store

`Sim.dataset({ title: 'Furuta pendulum' })`, dimensions `k` (4), `kk` (16, P row by row), `ia` × `iv` (37 × 31, the rescue grid)
and `n` (2001, the stored run). Every variable, with its symbol, units, meaning and the function that writes it:

| Name | Symbol | Units | Meaning | Written in |
|---|---|---|---|---|
| `ma` | m<sub>a</sub> | kg | mass of the arm, a uniform bar | constant MA |
| `Jh` | J<sub>h</sub> | kg m² | moment of inertia of the hub and the motor’s rotor about the axis | constant JH |
| `mp` | m<sub>p</sub> | kg | mass of the pendulum, a uniform rod | constant MP |
| `Lp` | L | m | length of the pendulum | constant LP |
| `g` | g | m/s² | gravitational acceleration | constant G |
| `br` | b<sub>r</sub> | N m s | viscous friction of the arm’s bearing | constant BR |
| `bp` | b<sub>p</sub> | N m s | viscous friction of the pendulum’s hinge | constant BP |
| `km` | k | N m/A | motor constant: torque per ampere, equal to back-emf per rad/s in V s | constant KM |
| `Rm` | R | Ω | resistance of the motor’s winding | constant RM |
| `Lam` | Λ | H | inductance of the winding (dropped from the model: Λ/R is 0.5 ms) | constant LAMBDA |
| `amax` | a<sub>max</sub> | rad/s² | largest arm acceleration the swing-up asks for | constant AMAX |
| `kphi` | k<sub>φ</sub> | 1/s² | spring that pulls the arm towards φ* during the swing-up | constant KPHI |
| `kw` | k<sub>ω</sub> | 1/s | damper on the arm’s speed during the swing-up | constant KW |
| `ra` | r | m | length of the arm, from the axis to the pendulum’s hinge | ra slider |
| `Vmax` | V<sub>max</sub> | V | largest voltage the amplifier can give | vmax slider |
| `phs` | φ* | rad | target angle of the arm | phs slider |
| `mode` | preset |  | the controller: off (amplifier disconnected), catch (LQR always) or swing (swing-up, then LQR) | the preset buttons |
| `qa` | q<sub>α</sub> | 1/rad² | weight of the pendulum’s angle error in the cost J | qa slider |
| `qp` | q<sub>φ</sub> | 1/rad² | weight of the arm’s angle error in J | qp slider |
| `rho` | ρ | 1/V² | weight of the motor voltage in J: larger means gentler | rho slider |
| `kE` | k<sub>E</sub> | 1/(J s) | gain of the swing-up: arm acceleration per joule of missing energy per rad/s of swing | kE slider |
| `Jr` | J<sub>r</sub> | kg m² | moment of inertia of the arm, hub and rotor about the axis | rig() |
| `J0` | J<sub>0</sub> | kg m² | the same with the pendulum’s mass at the arm’s tip | rig() |
| `Jp` | J<sub>p</sub> | kg m² | moment of inertia of the pendulum about its hinge | rig() |
| `hc` | h | kg m² | coupling between arm and pendulum | rig() |
| `Gc` | G | J | gravity scale of the pendulum: its weight times the height of its centre above the hinge when upright | rig() |
| `Dl` | Δ | kg² m⁴ | determinant of the mass matrix at α = 0 | rig() |
| `w_bot` | ω<sub>bot</sub> | rad/s | angular frequency of small swings at the bottom with the arm free | rig() |
| `w_fix` | ω<sub>fix</sub> | rad/s | the same with the arm held still | rig() |
| `Kg` | K |  | LQR gains on (φ − φ*, α, φ̇, α̇): V/rad, V/rad, V s/rad, V s/rad | lqr() |
| `Pm` | P |  | solution of the Riccati equation, row by row: the bowl ỹᵀPỹ of the catch | lqr() |
| `lamo_re` | Re λ<sub>open</sub> | 1/s | eigenvalues of the rig without control at the top, real parts | eig() |
| `lamo_im` | Im λ<sub>open</sub> | rad/s | imaginary parts | eig() |
| `lamc_re` | Re λ<sub>closed</sub> | 1/s | eigenvalues of the caught rig at the top, real parts: the decay rates | eig() |
| `lamc_im` | Im λ<sub>closed</sub> | rad/s | imaginary parts | eig() |
| `rank` | rank 𝒞 |  | rank of the controllability matrix [B, AB, A²B, A³B] at the top; 4 means the motor can reach every motion near the top | rankOf() |
| `grow` | λ<sub>+</sub> | 1/s | fastest growth rate at the top without control: how fast the pendulum falls | design() |
| `slow` | max Re λ<sub>closed</sub> | 1/s | slowest decay rate once caught | design() |
| `c_meas` | c |  | largest level of ỹᵀPỹ whose whole surface the catch rescues, in 240 sampled starts | measureC() |
| `c_in` | c<sub>in</sub> |  | handover level: the swing-up hands over to the catch when ỹᵀPỹ falls below it | design() |
| `c_out` | c<sub>out</sub> |  | drop-out level: the catch hands back to the swing-up when ỹᵀPỹ rises above it | design() |
| `ga` | α<sub>i</sub> | rad | pendulum angles of the rescue grid | measureBasin() |
| `gv` | α̇<sub>j</sub> | rad/s | pendulum speeds of the rescue grid | measureBasin() |
| `basin` | caught<sub>ij</sub> |  | 1 where the catch alone, started at (φ*, α<sub>i</sub>, 0, α̇<sub>j</sub>), brings ỹᵀPỹ below 0.05 within 3 s | measureBasin() |
| `basin_n` | n<sub>caught</sub> |  | starts of the grid the catch rescues | measureBasin() |
| `basin_ms` | measure time | ms | time the browser took to measure c and the rescue grid | design() |
| `y0s` | y(0) |  | start of the run, (φ, α, φ̇, α̇): hanging, nudged 3°, after Solve; where your hand let go after a drag | solve() |
| `released` | from your hand |  | the run starts where a drag let go | solve() |
| `grabbed` | held |  | what your hand holds now (nothing, the pendulum or the arm); the clock is stopped | the drag |
| `h` | h | s | RK4 step | constant H |
| `steps` | steps |  | RK4 steps in one solve | solve() |
| `solve_ms` | solve time | ms | time the browser took to solve the run twice (h and h/2) and store it | solve() |
| `err_half` | max |y<sub>h</sub> − y<sub>h/2</sub>| |  | largest difference between the stored run and the same run solved with half the step, over the stored samples (rad or rad/s) | solve() |
| `err_end` | t<sub>err</sub> | s | time at which that largest difference occurs | solve() |
| `balance` | balance | J | energy book at the end: E(0) + W<sub>in</sub> − Q<sub>R</sub> − Q<sub>b</sub> − E(T) | solve() |
| `t_catch` | t<sub>catch</sub> | s | time at which the catch takes over for good; NaN if it never does | solve() |
| `t_settle` | t<sub>settle</sub> | s | time after which the state stays within 0.01 of the goal (rad, rad/s); NaN if it never does | solve() |
| `t_sat` | t<sub>sat</sub> | s | time the motor spends at its voltage limit | solve() |
| `n_swings` | swings |  | turning points of the pendulum before the catch: how many half-swings the pumping took | solve() |
| `stale` | stale |  | a slider moved since the last solve | markStale() |
| `ts` | t<sub>n</sub> | s | time of each stored sample | solve() |
| `ph` | φ<sub>n</sub> | rad | angle of the arm, RK4 (not wrapped) | solve() |
| `al` | α<sub>n</sub> | rad | angle of the pendulum from straight up, RK4 (not wrapped) | solve() |
| `wp` | φ̇<sub>n</sub> | rad/s | angular speed of the arm | solve() |
| `wa` | α̇<sub>n</sub> | rad/s | angular speed of the pendulum | solve() |
| `Vs` | V<sub>m, n</sub> | V | voltage across the motor (with the amplifier off: the back-emf an open circuit shows) | drive(), in solve() |
| `Is` | I<sub>n</sub> | A | current in the winding | drive(), in solve() |
| `taus` | τ<sub>n</sub> | N m | torque of the motor on the arm | solve() |
| `Es` | E<sub>n</sub> | J | energy of arm and pendulum: kinetic plus gravity, zero with the pendulum’s centre at the hinge’s height | energy(), in solve() |
| `Eps` | E<sub>p, n</sub> | J | energy of the pendulum alone, as if its hinge stood still; G when it rests at the top | penEnergy(), in solve() |
| `Ly` | ỹᵀPỹ<sub>n</sub> |  | the catch’s bowl at each sample, with φ − φ* and α wrapped to (−π, π] | lyap(), in solve() |
| `Win` | W<sub>in, n</sub> | J | electrical work the amplifier has delivered since t = 0 | solve(), integrated with RK4 |
| `QR` | Q<sub>R, n</sub> | J | heat in the winding since t = 0 | solve(), integrated with RK4 |
| `Qb` | Q<sub>b, n</sub> | J | heat in the two bearings since t = 0 | solve(), integrated with RK4 |
| `caught` | caught |  | 1 while the catch (LQR) drives the motor, 0 while the swing-up pumps or the amplifier is off | decide(), in solve() |
| `sat` | at limit |  | 1 where the controller asks for more voltage than the amplifier can give | drive(), in solve() |
| `win_t0` | t<sub>window</sub> | s | left edge of the 8 s window chart | chartGeom() |
| `Escale` | E<sub>bar</sub> | J | energy that fills a bar: the largest of |E − E*|, W<sub>in</sub>, Q<sub>R</sub> and Q<sub>b</sub> over the run | solve() |
| `E_goal` | E* | J | energy of the rig resting at the goal: pendulum upright, arm still | solve() |
| `i_now` | n<sub>now</sub> |  | stored sample shown in this frame | the clock |
| `t_play` | t<sub>play</sub> | s | playback time in the stored run | the clock |
| `ph_now` | φ | rad | arm angle shown now | the clock, or your hand |
| `al_now` | α | rad | pendulum angle shown now | the clock, or your hand |
| `wp_now` | φ̇ | rad/s | arm speed now | the clock, or your hand |
| `wa_now` | α̇ | rad/s | pendulum speed now | the clock, or your hand |
| `V_now` | V<sub>m</sub> | V | motor voltage now (while you hold: what the controller asks for that state) | the clock, or your hand |
| `I_now` | I | A | motor current now | the clock, or your hand |
| `tau_now` | τ | N m | motor torque now | the clock, or your hand |
| `E_now` | E | J | energy now | the clock, or your hand |
| `Ep_now` | E<sub>p</sub> | J | pendulum energy now | the clock, or your hand |
| `Ly_now` | ỹᵀPỹ |  | the catch’s bowl now | the clock, or your hand |
| `Win_now` | W<sub>in</sub> | J | electrical work up to now | the clock |
| `QR_now` | Q<sub>R</sub> | J | winding heat up to now | the clock |
| `Qb_now` | Q<sub>b</sub> | J | bearing heat up to now | the clock |
| `caught_now` | caught |  | 1 while the catch drives the motor now | the clock, or your hand |
| `px_per_m` | px/m | css px | drawing scale of the rig | geom() |
| `elev` | ε | rad | how far the view looks down on the turntable | constant ELEV |
| `hub_px` | x<sub>O</sub> | css px | screen x of the axis at the arm’s height | geom() |
| `hub_py` | y<sub>O</sub> | css px | screen y of the axis at the arm’s height | geom() |
| `tip_px` | x<sub>P</sub> | css px | screen x of the arm’s tip, the pendulum’s hinge | drawRig() |
| `tip_py` | y<sub>P</sub> | css px | screen y of the arm’s tip | drawRig() |
| `end_px` | x<sub>E</sub> | css px | screen x of the pendulum’s free end (the knob) | drawRig() |
| `end_py` | y<sub>E</sub> | css px | screen y of the pendulum’s free end | drawRig() |
| `flag_px` | x<sub>φ*</sub> | css px | screen x of the target flag on the rim | drawRig() |
| `flag_py` | y<sub>φ*</sub> | css px | screen y of the target flag’s foot | drawRig() |
| `box_w` | box.w | css px | canvas width on your screen | draw() |
| `box_h` | box.h | css px | canvas height on your screen | draw() |
| `fps` | frame rate | Hz | smoothed over about ten frames | the clock |
| `playing` | playing |  | the playback runs | Sim.clock |

**Checks** (`Sim.data.check`, 66 entries plus the `*_now` scalars): every slider value against its control;
every constant against the code; every derived constant by its formula from the stored inputs; K, P, both sets of eigenvalues and the
rank by running `design()` again from the stored parameters; c by running the bisection again; each grid cell by running the catch
again from that start; the four state arrays, W_in, Q_R, Q_b and the mode by rerunning the same RK4 and the same switch from y(0)
to sample n (`replay()`); V_m, I, τ, E, E_p and ỹᵀPỹ at a sample from the stored state by their formulas; the balance, t_catch,
t_settle, t_sat, the half-step error and the drawing positions from their stored inputs.

**Read-backs** (`Sim.data.drawn`): `al_now`, `ph_now`, `phs`, `al`, `ph`. Each checks alpha before colour: the knob is burgundy
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

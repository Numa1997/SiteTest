# Fig. 2, Double Pendulum: from live computing to stored runs (study)

**Read state.md first. Status of this study, 23 November 2026, evening:** sections 1 to 3 (the live page, the physics, how the
browser computes) are true of the page that is live on main. Sections 4 to 7 describe a first plan (CPU, SciPy DOP853, 1296 starts
released from rest, 20 MB) that the user rejected the same day because it removed controls; they are kept as the record of what was
measured, not as the plan. Its measurements were made by running the model in a Claude workspace, which the user's rules forbid.

Written 23 November 2026, before building. Branch `kaggelize/double_pendulum`. Every number below was measured here (a cloud
machine with 2 CPUs, Python 3, NumPy 2.5.3, SciPy 1.18.1), not estimated. Words in *italics* are explained in the word list at
the end; each is also explained in plain words where it first appears.

## 1. The page today

Page: [`public/simulations/Double Pendulum.html`](../../../../public/simulations/Double%20Pendulum.html), 932 lines. Its notes for
maintainers: [`docs/simulations/fig02-double-pendulum.md`](../../../../docs/simulations/fig02-double-pendulum.md). Its walkthrough
("From symbols to code"): [`public/scripts/walk/pendulum.js`](../../../../public/scripts/walk/pendulum.js).

Controls (all in the panel beside the figure):

| Control | Line | Range | Step | What it does today |
|---|---|---|---|---|
| Pause / Play | L58 | | | stops and starts the clock |
| Restart | L59 | | | starts the motion again from the sliders |
| Clear trail | L60 | | | wipes the trail of the lower bob |
| Chaos twin (switch) | L62 | off / on | | adds a pale second pendulum started 0.001 rad further in θ₁ |
| Time scale | L65 | 0.25 to 1.5 × | 0.05 | simulated seconds per real second; does not restart |
| Mass ratio m₂/m₁ | L73 | slider −2.3 to 2.3, the ratio is e^slider: 0.100 to 9.97 | 0.05 | restarts |
| Length ratio l₂/l₁ | L77 | slider −1.6 to 1.6, ratio 0.202 to 4.95 | 0.05 | restarts |
| Angle θ₁ | L85 | −180° to 180° | 1° | restarts |
| Angle θ₂ | L89 | −180° to 180° | 1° | restarts |
| Angular velocity ω₁ | L93 | −5 to 5 rad/s | 0.1 | restarts |
| Angular velocity ω₂ | L97 | −5 to 5 rad/s | 0.1 | restarts |
| Parameter curve (curve.js, added at L539) | L539 | a knob that moves by itself: mass ratio (live, "sand pours in") or time scale | | the mass curve changes m₂ while the pendulum swings |

Pictures and readouts:

| What | Line |
|---|---|
| The figure: canvas `#pend` with the pendulum, the twin, the trail of the lower bob, the protractor | L46, drawn by `draw()` L684 |
| Caption: simulated time t | L50, written by `readouts()` L697 |
| Readout Energy E | L102 |
| Readout Energy drift | L103 |
| Readout Twin separation · bob 2 | L104 |
| Lecture note (nine sections, KaTeX) | L115–441 |
| Walkthrough, key `pendulum`, 13 steps | L443 |
| Data panel (`Sim.data`, datalog.js): 7 groups, 60 stored names, checks and pixel read-backs | L829–923 |

## 2. The physical system

Two thin rigid rods, so light that we treat them as massless, and two small heavy balls (*point masses*). The upper rod, of length
l₁ = 1 m, hangs from a fixed *pivot* (a hinge that lets it turn freely) and carries the ball of mass m₁ = 1 kg. The lower rod, of
length l₂ (m), hangs from that ball and carries the ball of mass m₂ (kg). Both swing in one vertical plane; nothing rubs and no
air pushes. Gravity pulls down with g = 9.81 m/s².

Two numbers fix where everything is: the angle θ₁ (rad) of the upper rod and the angle θ₂ (rad) of the lower rod, each measured
from straight down, counter-clockwise positive. Their rates of change are the *angular velocities* ω₁ = dθ₁/dt and ω₂ = dθ₂/dt
(rad/s), and the rates of change of those are the *angular accelerations* α₁, α₂ (rad/s²). The four numbers (θ₁, θ₂, ω₁, ω₂) are
the *state*: knowing them now fixes all of the future.

Positions (m), pivot at the origin, y up: x₁ = l₁ sin θ₁, y₁ = −l₁ cos θ₁, x₂ = x₁ + l₂ sin θ₂, y₂ = y₁ − l₂ cos θ₂.

Energy (J): kinetic T = ½(m₁+m₂) l₁² ω₁² + ½ m₂ l₂² ω₂² + m₂ l₁ l₂ ω₁ ω₂ cos δ, with δ = θ₁ − θ₂ (rad); potential
V = −(m₁+m₂) g l₁ cos θ₁ − m₂ g l₂ cos θ₂, zero at the height of the pivot. E = T + V stays constant, because nothing rubs.

From the energies, *Lagrange's method* (a recipe that turns the two energies into the equations of motion without drawing forces)
gives the two accelerations (the note's equation (9)), with D = 2m₁ + m₂ − m₂ cos 2δ (kg):

    α₁ = [−g(2m₁+m₂) sin θ₁ − m₂ g sin(θ₁ − 2θ₂) − 2 sin δ · m₂ (ω₂² l₂ + ω₁² l₁ cos δ)] / (l₁ D)
    α₂ = 2 sin δ · [ω₁² l₁ (m₁+m₂) + g (m₁+m₂) cos θ₁ + ω₂² l₂ m₂ cos δ] / (l₂ D)

No formula gives θ(t) directly; the equations are *integrated*: stepped forward in time, small piece by small piece.

The system is *chaotic*: two starts that differ by a hair drift apart exponentially, roughly as d₀ e^{λt}; λ (1/s) is the
*Lyapunov exponent*. Measured here for the default start (120°, 150°, equal masses and rods), from the distance of the lower bobs
of the pendulum and its twin between 10⁻³ m and 10⁻¹ m: λ = 1.38 per second (the note quotes 1.46 from a different fit window).

## 3. How the browser computes it now

| What | Function, line | When |
|---|---|---|
| accelerations α₁, α₂ (equation (9)) | `deriv(s)`, L541 | four times per step |
| one *RK4* step, h = 1/600 s | `rk4(s, h)`, L550 | in the clock callback L760: n = floor(real time × time scale / h) steps per picture, at most 600; about 10 per picture at 60 Hz |
| the twin, the same steps | L774–777 | when the switch is on |
| energy | `energy(s)`, L561 | at restart (E₀) and once per picture in `diagnostics()` L712 |
| the trail | `segment()` L612, one segment per RK4 step; `fade()` L622 once per picture | per step / per picture |
| everything the data panel shows (60 names) | `diagnostics(dt)`, L712 | once per picture |
| a slider move | `restart()` L592: m₂, l₂, start state, E₀, layout | on every input event of the six physics sliders |
| the sand curve | `sand(v)` L539: m₂ changes while the motion runs, the energy it brings is booked as E_sand | every picture while the curve runs |

So per picture the browser takes about ten RK4 steps (twenty with the twin), each with four evaluations of `deriv`. Nothing is
stored beyond the current state: a restart computes everything again.

## 4. The raw data the page needs to play without computing

To draw, the page needs at each moment the two angles of the pendulum and of its twin. To keep the readouts and the data panel on
stored numbers it also needs ω₁, ω₂, α₁, α₂ and the twin distance. Axes: controls (mass ratio × length ratio × θ₁ × θ₂) × time.

Per stored frame and run, 9 numbers as *int16* (a whole number from −32768 to 32767, 2 bytes): θ₁, θ₂, ω₁, ω₂, α₁, α₂, θ₁′, θ₂′
(the twin's angles) and log₁₀ d (the twin distance in m, as a power of ten). Angles in steps of 10⁻⁴ rad (at most 0.05 mm of
error at the end of a 1 m rod); ω and α in steps the model picks per file so that the largest value fits (header field `scale`);
log₁₀ d in steps of 2·10⁻⁴. That is 18 bytes a frame.

Frames per second: the page draws between two stored frames a cubic curve through the two angles with the stored angular
velocities as slopes (*Hermite interpolation*), so the frames can be sparse where the motion is slow and must be dense where it
whips. The model picks, per file, the smallest rate of 20, 25, 30, 40, 50, 60, 75, 100 or 120 per second at which (a) no angle
turns by more than 1 rad between frames and (b) the drawn lower bob stays within 0.002 × (l₁ + l₂) of the true path (0.5 px when
the pendulum is 250 px long), checked at 600 points per second; for the twin, whose angular velocities are not stored, the slopes
come from the neighbouring frames and the bound is 0.004 × (l₁ + l₂).

Measured on the full grid (section 5): 108 files, 17 635 750 bytes of frames and headers, plus `double_pendulum.json` (8 100 bytes).
Rates chosen: 20 to 25 per second for equal masses, up to 100 per second for the heavy lower bob on the short rod (ω₂ reaches
about 78 rad/s there). Per cell (all twelve θ₁ files):

| m₂/m₁ | l₂/l₁ | frames per second | bytes |
|---|---|---|---|
| 0.100 | 0.202 | 20–40 | 1 683 945 |
| 0.100 | 1 | 20 | 1 078 759 |
| 0.100 | 4.95 | 20 | 1 078 941 |
| 1 | 0.202 | 20–50 | 1 942 927 |
| 1 | 1 | 20–25 | 1 184 787 |
| 1 | 4.95 | 20 | 1 078 679 |
| 9.97 | 0.202 | 50–100 | 4 168 087 |
| 9.97 | 1 | 50–75 | 3 303 817 |
| 9.97 | 4.95 | 40 | 2 115 808 |

A visitor downloads only the file of the chosen cell and θ₁: 111 336 bytes for the default start, at most 435 539 bytes.

## 5. The plan to generate it once

**The grid.** The page keeps all four physics sliders that set a shape, on a grid:

- mass ratio: ln(m₂/m₁) ∈ {−2.3, 0, 2.3}, i.e. m₂ = 0.100, 1, 9.97 kg (the slider's two ends and its middle);
- length ratio: ln(l₂/l₁) ∈ {−1.6, 0, 1.6}, i.e. l₂ = 0.202, 1, 4.95 m;
- θ₁ and θ₂ every 30°, −150° … 180° (−180° is the same position as 180°): the marks of the page's protractor; 12 × 12 = 144 starts;
- released from rest, ω₁ = ω₂ = 0.

3 × 3 × 144 = 1296 runs, each with its twin (θ₁ + 0.001 rad): 2592 trajectories. The default start (120°, 150°, equal masses and
rods) is on the grid.

**Random starts and seeds.** None. The double pendulum is not random: the reader chooses the start with the sliders and the page
plays the run of exactly that start. Its chaos is shown, as today, by the twin. So no seed is recorded and the page picks no run at
random.

**Method and tolerances.** SciPy's *DOP853* (an eighth-order Runge–Kutta method that chooses its own step size so that the error of
each step stays below a *tolerance*), relative tolerance 10⁻¹⁰, absolute 10⁻¹²; its continuous solution is sampled at the frames.
Each run lasts 20 s; the page plays it and then starts it again from the beginning.

**Run time, measured.** One file of the default cell (24 trajectories): 4.6 s; the slowest file (heavy short lower bob): 21.2 s; the
whole grid with all checks: 253 s on 2 CPUs (4 min 13 s wall time). Kaggle's CPU notebook has 4 CPUs, so about 2 to 3 minutes there,
far inside the line's 30-minute limit.

**Budget 20 MB: the ways weighed.**

| Way | Size, measured or scaled from the measured run | Cost | Risk |
|---|---|---|---|
| A. Keep the six physics sliders on a grid, ω included: ω₁, ω₂ ∈ {−5, 0, 5} on top of the grid below | 9 × the size of C, about 159 MB | far over budget | none in the physics; impossible to store |
| B. Chosen grid, 30 s runs, the twin with its own ω₁′, ω₂′ (11 columns) | 31 703 694 bytes (measured, first full run) | over budget by 58 % | none |
| C. Chosen grid, 20 s runs, 9 columns, twin slopes from neighbouring frames | **17 635 750 bytes (measured)** | runs loop after 20 s; the twin is drawn with slopes estimated from its frames | the twin's drawn path within 0.004 (l₁ + l₂) instead of 0.002 |
| D. As B but drop α₁, α₂ and the twin's ω (7 columns), 30 s | about 20.2 MB (7/11 of B) | the data panel and walkthrough would show accelerations the page computes itself, against the house rule that the display only reads | a second computation in the page, and still just over budget |

**Taken: C.** It fits with 12 % to spare, every number the panel shows comes from the model, and 20 s is twice the time the twin
needs to separate from the default start (the distance passes 0.1 m at 4.1 s and is 2.24 m at 10 s). Moreover the file the page
downloads is small (111 kB at the default start).

## 6. What the page will no longer be able to do

- Start at any angle: only every 30° (the protractor marks); the angle sliders move in steps of 30°.
- Choose any mass or length ratio: only the two ends and the middle of each slider (0.1, 1, 10 and 0.2, 1, 5).
- Start with a push: the ω₁ and ω₂ sliders go; every start is released from rest.
- Run for ever: each run lasts 20 s and then starts again from the beginning (the caption says so).
- Pour sand into the lower bob: the parameter curve can no longer change m₂ while the pendulum swings. The time-scale curve stays,
  because it only changes how fast the stored run is played.
- The exercise of §6 that asks for starts of 10°: the smallest start is now 30°; the exercise is rewritten for the grid.

## 7. The checks the model carries (written into `double_pendulum.json`)

| Check | What it shows | Measured here |
|---|---|---|
| energy of every run | the largest change of E, divided by (m₁+m₂) g l₁ + m₂ g l₂ (the energy needed to lift both bobs from the bottom to the pivot), over all 1296 runs and their twins | 6.2 × 10⁻⁹ (twins 4.2 × 10⁻⁹) |
| known limit: small swings | equal masses and rods released 0.5° out in each *normal-mode* shape (θ₂ = ±√2 θ₁): periods against 2π / √(g/l (2 ∓ √2)) = 2.6211 s and 1.0857 s | 6.3 × 10⁻⁶ and 1.4 × 10⁻⁴ apart; at 0.25° four times smaller (1.6 × 10⁻⁶, 3.5 × 10⁻⁵), as the first nonlinear correction should be |
| tolerance | the 12 runs of the default θ₁ row again at 100 × tighter tolerances: how long the lower bobs agree within 1 mm | 9.4 s to the whole 20 s (12 runs); within 1 μm for the first 5 s |
| today's browser result | the page's own RK4 at h = 1/600 s from the default start against the model | agree within 1 mm until 10.86 s (the note says 10.9 s); RK4's own energy drift up to 5.0 × 10⁻⁸ |
| chaos | growth rate of the twin distance from the default start | λ = 1.38 per second |
| drawing | largest distance of the drawn cubic from the true lower bob, as a share of l₁ + l₂ | 0.0017 (pendulum), 0.0040 (twin) |

## 8. Words used

- **angular velocity, ω**: how fast an angle changes, in radians per second.
- **angular acceleration, α**: how fast the angular velocity changes, rad/s².
- **chaotic, chaos**: exact laws whose outcome depends so strongly on the start that a tiny change soon gives a different motion.
- **Catmull–Rom slopes**: estimating the rate of change at a frame from the frame before and the frame after.
- **cell**: one pair of mass ratio and length ratio on the grid.
- **DOP853**: a method for stepping equations forward in time that looks at the slope 12 times per step and adjusts its step size
  so the error stays below the tolerance; "8" because its error shrinks like the step size to the 8th power.
- **frame**: one stored moment of the motion.
- **grid**: the list of values each control may take.
- **Hermite interpolation**: drawing between two frames a cubic curve that passes through both stored angles with the stored
  angular velocities as its slopes.
- **int16**: a whole number stored in 2 bytes, from −32768 to 32767; a real number is stored as a whole number of small steps.
- **integrate**: find the motion by stepping the equations forward in many small time steps.
- **Lagrange's method**: a recipe that turns the kinetic and potential energy into equations of motion.
- **Lyapunov exponent, λ**: the rate at which two nearby starts drift apart, d ≈ d₀ e^{λt}.
- **normal mode**: a pattern of small swings in which every part moves at one shared frequency.
- **pivot**: the fixed hinge at the top.
- **point mass**: a ball so small that only its mass and position matter.
- **RK4**: the fourth-order Runge–Kutta method: four looks at the slope per fixed time step, averaged.
- **run**: the stored motion from one start.
- **seed**: the number that fixes a sequence of random numbers, so a random run can be repeated; not needed here.
- **SHA-256**: a 64-character fingerprint of a file; any change to the file changes it.
- **state**: the four numbers (θ₁, θ₂, ω₁, ω₂) that fix the future.
- **tolerance**: the error a step-size-choosing method is allowed per step.
- **twin**: a second pendulum started 0.001 rad further in θ₁, to show chaos.

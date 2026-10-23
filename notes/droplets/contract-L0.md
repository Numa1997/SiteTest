# Contract L0: continuous collection with the Stokes speed (round 3, with the round-3 fixes)

Gate 1 of physics-model-loop. Round 1 failed (`skeptic-G1-L0-r1.md`: 1 fatal, 12 must-fix, 9 minor); round 2 failed (`skeptic-G1-L0-r2.md`:
6 new must-fix, round-1 #10 open). Every objection is answered in the tables at the end (sections 10 and 11).
The thesis throughout is N. Koudsie, *Collisional Ice Multiplication Processes in Clouds*, Bachelor thesis, Leipzig 2022
(its equations as quoted in `notes/droplets/baseline/`). Round-3 numbers: `derive/L0_r3.cjs`, `derive/L0_population.py` part (c). Files: `portfolios-src/droplets/derive/L0_sympy.py` (SymPy, route 1), `L0_wolfram.md` (Wolfram, route 2,
input and output saved), `L0_numbers.py` (exact formulas against `solve_ivp`), `L0_r2.py` (the numbers of section 5),
`L0_population.py` (capture-only master equation; lognormal capture-only mean field).

## 1. Question and observables

What rate does one drop collect at when it falls through smaller droplets, and where in its growth is the time spent? This is the
lowest rung: the collision geometry and mass conservation, with the simplest fall-speed law (Stokes) and every contact counted
(E = 1). Two settings, because the question has two observables:

- **Closed box (seed of observable 1).** The thesis cloud with its collectors taken identical: 300 cm⁻³ droplets of r = 8 µm and
  1 cm⁻³ collectors of R₀ = 40 µm, 10 °C, 850 hPa. Observable: F_c(t), the fraction of all water inside the collectors, and the
  times t₅₀, t₉₀ at which it reaches 0.5 and 0.9. Here every collector is at least 40 µm from the start, so F_c equals F₄₀, the
  fraction of the water in drops of radius r ≥ 40 µm (observable 1 of the study).
- **Open cloud with rare collectors (seed of observable 2).** One collector among droplets whose water W does not change; valid
  while the collectors take a small part of the water: N_c ≤ 0.015 cm⁻³ keeps the 40 → 100 µm time within 2.3 % of a closed box with the
  same droplet water (+0.8 % at 0.005, +8.8 % at 0.05, +59 % at 0.15 cm⁻³; `L0_r3.cjs`). This is not the thesis cloud (1 cm⁻³). Observable: the time to grow from 40 µm to 60 µm and to 100 µm.

Sizes named in the study (radius): cloud droplet below 20 µm; collector 40 µm; drizzle drop 100–250 µm; raindrop r ≥ 250 µm
(diameter 0.5 mm); large raindrop r = 1 mm.

**L0's answer to "how does a cloud make rain": not by capture onto identical collectors.** In the thesis cloud every collector stops at
R_m = 60.15 µm when the droplets are used up; the master equation puts P(R ≥ 65 µm) = 4.8 × 10⁻³ and P(R ≥ 68 µm) = 2.2 × 10⁻⁵ after 60 min.
Drops of 100 µm need a spread of collector sizes or collector–collector mergers (L4, L5). Only the open cloud reaches 100 µm.

Why depletion belongs in L0: it adds no law and no closure. Mass conservation alone gives the droplet water left, W(R), and
observable 1 is defined in a closed box. L0 therefore carries one collector and its box, not two physical effects.

## 2. Picture and formal mechanism

Picture: run through drizzle holding a sheet of cardboard in front of you. The sheet sweeps a volume of air per second equal to its
area times your speed, and catches the drops in that volume. A falling collector is such a sheet, with two differences. Every droplet
it catches makes it wider and, because it is heavier, faster: area grows as R², the Stokes speed as R², so the sweep grows as R⁴ while the
mass to add grows as R³. And unlike the sheet, the drop pushes the air aside, and part of the droplets in its path ride round it (only
about a third to a half are hit at 40 µm: section 5); L0 ignores that (E = 1).

Mechanism: mass conservation for the collector, dM/dt = W × (volume swept per second):

  dM/dt = E π (R + r)² [v(R) − v(r)] W,          M = (4π/3) ρ_w R³.                                          (L0.1)

This is the continuous-collection model usually attributed to Langmuir (1948); the dossier read his tables, not his equation numbers, so
the attribution is not checked against the equation in his paper. With E = 1 and v = ka² the swept
rate grows as R²·R² = R⁴ while the mass to add per unit radius grows as R², so dR/dt ∝ R². Doubling time of R falls as 1/R.

## 3. Model

State: the collector radius R(t). Laws: mass conservation (L0.1); weight less buoyancy against Stokes drag 6πμav, so v(a) = k a²,
k = 2(ρ_w − ρ_a) g/(9μ) = 1.2296 × 10⁸ m⁻¹ s⁻¹ at 10 °C, 850 hPa. Air: ideal gas ρ_a = p/(R_d T) = 1.0458 kg/m³, Sutherland's
viscosity with the thesis's constants (Koudsie 2022, eq. 20, as quoted in the baseline), μ = 1.771 × 10⁻⁵ Pa s; check: the same formula
gives 1.8206 × 10⁻⁵ Pa s at 20 °C, against Beard's (1976) reference value 1.818 × 10⁻⁵ (0.14 %). Closure: E = 1, coalescence = 1.

- Open cloud: dR/dt = (E k W/4ρ_w)(R + r)³(R − r)/R²                                                          (L0.2)
  For r ≪ R: dR/dt = c R², c = E k W/(4ρ_w), so R(t) = R₀/(1 − c R₀ t), infinite at t* = 1/(c R₀).                (L0.3)
  For finite r: t(R) = (4ρ_w/E k W)[F(R) − F(R₀)], F(R) = ln[(R − r)/(R + r)]/(8r) − (3R + 2r)/[4(R + r)²].     (L0.4)
- Closed box, N_c identical collectors: W(R) = N_c (4π/3) ρ_w (R_m³ − R³), R_m³ = R₀³ + W₀/[N_c (4π/3) ρ_w].
  For r ≪ R, dR/dt = (π E k N_c/3) R²(R_m³ − R³), with the closed form
  t(R) = [G(R) − G(R₀)]/(π E k N_c/3), G(R) = {R[−2 ln(R_m − R) + ln(R² + R R_m + R_m²) − 2√3 arctan(√3(2R + R_m)/(3R_m))]/6 − R_m}/(R R_m⁴).   (L0.5)
  With finite r the integrand R²/[(R + r)³(R − r)(R_m³ − R³)] is rational, so a closed form exists; SymPy's antiderivative failed its
  own derivative check (2.8 %), so the finite-r box is computed by two numerical routes instead (section 6).

## 4. Rejected alternatives

1. A stochastic collector (Telford 1955, read in `dossier-stochastic.md`): it needs the capture rate this level supplies, and its
   mean equals L0's to 0.01 min here (section 6); its tail is L5.
2. A measured drag law: it removes the blow-up but adds a closure; it is L1, so the reader sees what Stokes' law alone does.
3. A size distribution with all pair interactions (the SCE): it is L4.

## 5. Assumptions, each with its number (10 °C, 850 hPa unless stated)

| Assumption | Number | Consequence and where it fails |
|---|---|---|
| Terminal fall at every instant | τ_p(40 µm) = 20.1 ms; growth time R/Ṙ at 40 µm = 15.2 min (open cloud, finite r); ratio 2.2 × 10⁻⁵ | holds throughout |
| Stokes drag (C_D = 24/Re), no slip | Re of the Stokes speed is 1 at R = 41.0 µm; against Beard (1976) the Stokes speed is too fast by 5 % at 30 µm, 11 % at 40 µm, 27 % at 60 µm, 69 % at 100 µm; molecular slip raises v(8 µm) by 1.2 %; applied to both drops it raises Δv(40/8 µm) by 0.20 % | a tolerance, not an edge: the 40 → 100 µm time is a lower bound; L1 |
| E = 1 | impaction Stokes number τ_p(r)Δv/R of an 8 µm droplet: 3.79 (R = 40 µm), 5.82 (60), 9.81 (100), above the creeping-flow critical 1.212, so droplets do hit, but not all: E(40 µm, 8 µm) = 0.50 in Hall's (1980) compiled table, 0.394 in Langmuir's (1948) Table 4 (785 hPa, 2 °C), 0.344 from this study's trajectory solver (`physics.cjs` pairEfficiency; printed by `derive/L2_numbers.cjs` and recomputed independently in `checks/check_physics.py`) | overstates the rate by 2 to 3 at the start, where the time is spent; L2 |
| Coalescence = 1 | not measured below about 0.4 mm; extrapolations disagree: Straub et al.'s (2010) energy law gives 0.99998 for 40/8 µm (Weber number 2 × 10⁻⁵), Low and List's (1982) gives 0.54 when pushed to these sizes; Beard and Ochs (1995, not read; via Jacobson 2011) tends to 1 below 14 µm droplet diameter (ours is 16 µm) | taken as 1, uncertainty unknown; L3 |
| Continuous growth | 40 → 100 µm takes 1829 captures; the coefficient of variation of the growth time (Poisson waiting times) is 3.68 %; the capture-only master equation gives t₅₀, t₉₀ = 2.926, 9.184 min against L0's 2.927, 9.192 | right for the mean, wrong for the tail: at t₉₀ the master equation puts 12.1 % of collector mass above R_m; L5 |
| Droplets uniform, air still | the collector's own Stokes number τ_p/τ_K = 0.15, 0.49, 1.54 for ε = 10⁻³, 10⁻², 10⁻¹ m²/s³; turbulent shear speed (R + r)(ε/ν)^½ over Δv: 0.002, 0.006, 0.020; differential-inertia speed |τ_R − τ_r| ε^¾ ν^−¼ over Δv: 0.009, 0.050, 0.28; Ayala et al. (2008) give +0.4 %, +5.6 %, +28 % on the 40/8 µm kernel at 10, 100, 400 cm²/s³ (scout's evaluation) | small at ε ≤ 10⁻² m²/s³ for collector–droplet pairs, not for near-equal pairs; L6. The ε range is the one the turbulence sources tabulate |
| No Brownian motion | Péclet number Δv(R + r)/D = 6.2 × 10⁶ for the 8 µm droplet (D = 1.46 × 10⁻¹² m²/s) | holds |
| Closed box: no condensation, no updraft | a saturated parcel rising on the moist adiabat condenses dW/dz = 2.06 g m⁻³ per km (Clausius–Clapeyron with constant L, lapse rate 4.93 K/km), i.e. 0.062, 0.124, 0.247 g m⁻³ min⁻¹ at 0.5, 1, 2 m/s, against a collection drain of 0.053 g m⁻³ min⁻¹ at t = 0 | comparable: the box isolates collection by choice; it is not a model of a real cloud's water budget, and the page says so |
| Well-mixed box | by t₉₀ a collector falls 176.5 m through the air and the collectors sweep the air 1.95 times (`L0_r3.cjs`). In still air nothing would remix the droplets the collectors deplete; weak turbulence (ε = 10⁻⁴–10⁻³ m²/s³) mixes the 1 cm spacing between collectors in (l²/ε)^{1/3} ≈ 0.5–1 s, against a depletion time 1/(N_c K) = 12 min, while it changes the collision rate by under 1 % (row above). So "air still" means: still for the collision, mixed for the bookkeeping | an assumption of every mean-field level; L5 tests finite volumes |
| Dry-air density | the saturated air is 0.55 % lighter (1.0401 kg/m³); k changes by 6 × 10⁻⁶ | negligible |

Scales in one place (10 °C, 850 hPa; closed box): collector response time 20 ms; Stokes Re = 1 at 41 µm; blow-up time of the open cloud
t* = 21.1 min (r ≪ R); depletion time 1/(N_c K₀) = 12 min; R_m = 60.15 µm; 1829 captures from 40 to 100 µm (300 per collector in the
box). The cloud meant is a weakly turbulent layer or young cumulus with ε ≤ 10⁻² m²/s³; in vigorous cumulus (ε up to 6.5 × 10⁻² m²/s³)
the turbulence row above is +6 % to about +30 %, and L6 says so.

**What L0's times are worth.** The study asks "how fast", so here are the L0 times beside the same calculation with the corrections of
L1 and L2 put in (first estimates, `L0_r3.cjs`; open cloud 40 → 60 and 40 → 100 µm, closed box t₅₀ and t₉₀, minutes):

| Kernel | 40 → 60 | 40 → 100 | t₅₀ | t₉₀ |
|---|---|---|---|---|
| L0 (Stokes, E = 1) | 5.31 | 9.96 | 2.93 | 9.19 |
| Beard speeds, E = 1 | 6.29 | 13.02 | 3.35 | 11.03 |
| Beard speeds, Hall's (1980) E | 11.23 | 21.93 | 6.41 | 19.22 |
| Beard speeds, this study's E table (L2) | 15.95 | 29.49 | 9.07 | 27.24 |

Every L0 time is short by a factor of about 2 to 3, most of it from E = 1. So L0's times are lower bounds, and its use is the shape of
the answer (where the time goes, section 7), not the minutes.

## 6. Exact solutions, limits and comparisons it must reproduce

- (L0.4) against `solve_ivp`: 40 → 100 µm at W = 0.643 g/m³, r = 8 µm: 9.9554 min both ways (rtol 10⁻¹¹). (L0.3), the r ≪ R limit,
  gives 12.64 min: the finite droplet radius shortens the time by 21 %.
- Limit r → 0 of (L0.4) equals (L0.3): SymPy (`L0_sympy.py`, printed: (R₁ − R₀)/(R₁R₀)) and Wolfram (`L0_wolfram.md`), independently.
- Closed box: R_m = 60.15 µm. Finite r: t₅₀ = 2.927, t₉₀ = 9.192 min (`solve_ivp`, `L0_numbers.py`), 2.92704, 9.19197 min (`quad`,
  `L0_population.py` part (c)), 2.926, 9.184 min (capture-only master equation, `L0_population.py` part (a)). The r ≪ R limit (L0.5) gives 3.958 and 12.043 min, 35 % and 31 % too slow here (r/R = 0.2).
- The Fermi estimate (`status.md`): at fixed collector size the collectors clear the droplet water on an e-folding time of 17 min;
  L0 with growth gives t₅₀ = 2.9 min, inside the estimate's "a few minutes".
- No measurement of a single collector's growth in a controlled droplet cloud was found in the sources read for this study (two
  scouts, the baseline); later levels are compared with measured fall speeds (L1) and computed efficiencies (L2, Hall 1980), and with
  Langmuir's (1948) computed growth of a 40 µm collector in 1 g/m³ of 8 µm droplets (to 3 mm in 3860 s, his Tables 6 and 7).

## 7. Where the time goes (the bottleneck)

With r ≪ R, t(R) = t*(1 − R₀/R): growing from 40 to 60 µm uses one third of the time to infinity, from 40 to 100 µm 60 % (finite r:
30 % and 56 %). The time is spent at the smallest sizes, where the speed is lowest and, in reality, E is smallest. So the growth rate
is decided at the start, by the collision efficiency and the drag of the small collector, not by the runaway. The blow-up itself is a
property of the model outside its range: it needs dR/dt to grow faster than R (here ∝ R², and ∫dR/R² converges), and by then Stokes'
law has failed. Once v ∝ R (Re of tens) dR/dt ∝ R gives exponential growth, and once v ∝ √R it gives R^{1/2} rising linearly in t;
the droplets also run out (R_m), and millimetre drops break up (outside the study). In the thesis cloud the droplets run out first:
every identical collector stops at 60.15 µm (section 1).

## 8. Predictions that could come out wrong (for later levels, derived here)

1. **Spread of collector sizes, capture only.** The capture-only mean field with the thesis's lognormal modes (droplets 300 cm⁻³, median
   8 µm, σ_g = 1.25; collectors 1 cm⁻³, median 40 µm, σ_g = 1.2; same kernel) gives F₄₀: t₅₀ = 2.50 min, t₉₀ = 6.85 min (`L0_population.py`;
   recorded once a minute, 3 and 7 min: the old study's "continuous GCE, thesis kernel" row; the skeptic's converged discretization gives
   2.53 / 6.82). All collectors share one sweep integral Φ = (Ek/4ρ_w)∫W dt (for r ≪ R), so R(∞) = 1/(1/R₀ − Φ): larger collectors
   outgrow smaller ones, and the collector that starts at 78 µm ends at 164 µm without meeting another collector.
   **Prediction for L4, now stated with its mechanism:** the full SCE with this kernel on every pair (Stokes, E = 1, coalescence = 1) is
   not a slower or faster version of this mean field; it runs away. The kernel grows faster than mass (as m^{4/3} for unequal pairs),
   which is the population form of the (L0.3) blow-up: collectors meet collectors, and within a few minutes nearly all the water is in
   drops beyond the grid. Computed (`L0_r3.cjs`, s = 8, Δt = 1 s, grid to 4 mm, mass leaving the grid kept in an overflow store and
   counted): t₅₀ = 2.27, t₉₀ = 3.65 min; 90.5 % of the water has left the 4 mm grid by 5 min (the skeptic's independent super-droplet
   runs: 2.3 / 4.1 min, 97–99 % in drops ≥ 1 mm by 5 min). Consequence for L4: every run must count the mass that leaves the grid, and
   the page must say that with Stokes speeds and E = 1 the bounds on t₅₀ and t₉₀ are met for a reason that is unphysical. The grid-free value
   is the skeptic's super-droplet 4.0–4.1 min; the bin value depends on the grid (3.51 / 3.65 / 3.72 min at s = 4 / 8 / 16, 3.86 min with a
   2 mm top) because mass parked in the overflow store stops collecting.
   **A known result that L0 explains, not a prediction:** the old study's thesis kernel (Stokes speeds, E = 1, but the coalescence law
   (4.2) evaluated with Stokes speeds) gives 3 / 5 min, and this study's SCE gives 2.27 / 4.51 min with 0.0 % of the water off the grid and
   0.1 % in drops ≥ 1 mm at 10 min; both were computed before this paragraph. L0 says why the thesis kernel does not run away: with
   Stokes speeds the Weber number of pairs above about 200 µm is of order ten, and the coalescence law switches those mergers off.
   L0 therefore holds no open prediction about nature; its falsifiable content is the code test 8.2.
2. **The tail, as a test of the stochastic engine (L5).** A bin scheme cannot test the capture spread: the skeptic showed that the share
   above R_m at t₉₀ depends more on the bin rule and on ±15 s than on the physics. The test that could fail uses a statistic with no grid:
   one 40 µm collector and n identical 8 µm droplets in a volume V, captures only (identical droplets fall at the same speed and never
   meet), is a pure death chain whose distribution of capture counts at any time follows exactly from the chain's rates. Prediction: the
   L5 Gillespie engine, with its class majorants and thinning, reproduces that distribution for n = 20, V = 0.05 cm³, t = 60 s, the
   extended kernel (Beard speeds, the L2 table): 4000 runs (seeds 1–4000); χ² test with neighbouring capture counts pooled until each
   cell expects at least 5 runs, p > 0.01; and the mean within three standard errors. (Outcome, `checks/check_physics.py`: mean 8.246 ±
   0.036 captures against the exact 8.221; χ² = 18.1 on 13 degrees of freedom, p = 0.15: passed.) A failure means the thinning or the class bookkeeping is wrong. The master
   equation's own spread is recorded for comparison: at t₉₀ = 551.1 s the mean collector radius is 58.02 µm with standard deviation
   1.69 µm (`L0_population.py`).

## 9. Derived, cited, chosen, and the price

Derived here: (L0.1)–(L0.5), R_m, the bottleneck shares, the common sweep integral. Cited: the continuous-collection model (Langmuir
1948); Stokes' drag (derived from the stream function in chapter 2 of the lecture notes, `text/book-02.src.html`, checked by `derive/L1_stokes_sympy.py`); Sutherland's viscosity with the constants of Koudsie (2022); the comparison values of
section 5 (Hall 1980, Langmuir 1948, Beard 1976, Ayala et al. 2008 via the dossiers). Chosen: E = 1, coalescence = 1, identical
droplets and identical collectors, a closed box without condensation. The price: E = 1 overstates the early rate by a factor 2 to 3
(section 5), exactly where the time is spent; Stokes overstates the speed by 11–69 % between 40 and 100 µm, so the open-cloud times
are lower bounds; and the closed box ignores a condensation supply of the same size as the collection drain.

## 10. Answers to round 1 (`skeptic-G1-L0-r1.md`)

| # | Objection | Answer |
|---|---|---|
| 1 | Prediction 2 false (mass above 60 µm without mergers) | Accepted; withdrawn. Replaced by prediction 8.2, derived from my own master-equation run (12.1 %), and by 8.1's common-Φ result (164 µm from a 78 µm start). The same error was in `status.md`'s Fermi text; corrected there. |
| 2 | Prediction 1 untestable | Widths, F₄₀ and the reference (the lognormal capture-only mean field, 2.50 / 6.85 min) are now fixed and computed; the band is one-sided and argued. |
| 3 | Snowball is not the mechanism | Replaced by the cardboard sheet: swept volume = area × speed, both growing with R (section 2), matching the R²·R²/R² count. |
| 4 | 40 → 100 µm outside Stokes' range | Stated as a lower bound with the Beard ratios (section 5); 40 → 60 µm added as an observable closer to Stokes' range. |
| 5 | E = 1 and coalescence have no number | Numbers with sources added (Hall 0.50, Langmuir 0.394, own solver 0.344; impaction St 3.79–9.81; coalescence ≥ 0.9996). |
| 6 | Open vs closed cloud | Validity condition N_c ≪ 0.154 cm⁻³ stated; the open-cloud observable belongs to rare collectors, not to the thesis cloud. |
| 7 | Thermal row is decoration; condensation is first order | Replaced by the Brownian Péclet number and by condensation supply against the collection drain (section 5). |
| 8 | Turbulence row checks the wrong particle | Collector's St, shear and inertial ratios over ε = 10⁻³ to 10⁻¹ m²/s³, and Ayala et al.'s numbers. |
| 9 | 0.8 % per catch is not the measure | Replaced by the 3.68 % coefficient of variation and the master-equation check. |
| 10 | "Cited: none" | Langmuir (1948) cited for the model; viscosity source and its check given. Bowen (1950) and textbooks not cited because not read. |
| 11 | r ≪ R called exact | Now "the r ≪ R limit, 35 % and 31 % too slow here"; finite-r numbers lead. |
| 12 | Checks claimed but not in files | Limit added to `L0_sympy.py`; Wolfram input and output saved in `L0_wolfram.md`; the (L0.3) sentence corrected; Fermi number quoted. |
| 13 | Blow-up instead of the bottleneck | Section 7 names the bottleneck with numbers. |
| 14 | "Faster than linear" blows up | Restated with the integral criterion (∫dR/f(R) finite). |
| 15 | Ratio 10⁻⁴ not computed | 2.2 × 10⁻⁵, computed. |
| 16 | ⟨R⁴⟩ vs R̄⁴ | The old argument is gone; prediction 8.1 rests on the computed common-Φ mean field. |
| 17 | Moist air, slip, the edge of Stokes | Dry vs moist density row added (6 × 10⁻⁶ on k); Stokes error given as a tolerance; slip is L1 (+1.2 % on v(8 µm)). |
| 18 | Geometry of the box | Fall distance and the remixing assumption stated. |
| 19 | "No measurement" | Softened to what was searched, with Langmuir's computed growth as a later comparison. |
| 20 | Two effects at L0 | Section 1 says why depletion adds no law or closure. |
| 21 | Closed form not printed | (L0.5) printed; finite-r closed form exists but SymPy's failed its check, so two numerical routes are used. |
| 22 | "Rain-sized" undefined | Size names defined in section 1. |

## 11. Answers to round 2 (`skeptic-G1-L0-r2.md`)

| # | Objection | Answer |
|---|---|---|
| N1 | Prediction 8.1 met for an unnamed reason (runaway) | Accepted and computed: 2.27 / 3.65 min with 90.5 % off the 4 mm grid by 5 min (`L0_r3.cjs`), in line with the skeptic's 2.3 / 4.1 min. 8.1 now states the runaway, requires L4 to count mass leaving the grid, and predicts what the coalescence law does to it. |
| N2 | 8.2's band smaller than its open choices | Accepted. 8.2 is replaced by a grid-free test that can fail: the Gillespie engine against the exact death chain. The master equation's radius spread (s.d. 1.69 µm at t₉₀ = 551.1 s) is recorded. |
| N3 | "2.928, 9.186 (quad)" in no file | Accepted: my earlier quad was not saved and its 9.186 was wrong. Part (c) of `L0_population.py` now runs `quad` and prints 2.92704 and 9.19197 min, equal to `solve_ivp`. |
| N4 | Coalescence row selective | Rewritten as the skeptic proposed: not measured; Straub 0.99998, Low and List 0.54; Beard and Ochs (1995) suggests 1; taken as 1, uncertainty unknown. |
| N5 | Times without their errors | New table in section 5: L0, Beard, Beard + Hall, Beard + own table, all four observables (`L0_r3.cjs`; reproduces the skeptic's 6.29 / 13.0 / 3.35 / 11.0 and 11.2 / 21.9 / 6.41 / 19.2). |
| N6 | L0 stops at 60 µm in the thesis cloud | Said in sections 1 and 7; size names corrected (drizzle drop 100–250 µm). |
| N7 | Picture shows half the mechanism | Section 2 adds the sweep-against-mass count and the air carrying droplets round the drop. |
| N8 | Langmuir's equation not in the cited section | "Usually attributed to Langmuir (1948); not checked against his equation numbers." |
| N9 | 0.344 without a file | Cited: `physics.cjs` pairEfficiency, `derive/L2_numbers.cjs`, and the independent SciPy recomputation in `checks/check_physics.py`. |
| N10 | Still air against well mixed | Scale argument added; 176.5 m and 1.95 sweeps computed (`L0_r3.cjs`). |
| N11 | "≪" not usable | N_c ≤ 0.015 cm⁻³ for ≤ 2.3 % on the 40 → 100 µm time, with the computed series. |
| N12 | Wolfram checks its own antiderivative | Accepted: `L0_wolfram.md` confirms (L0.5) only through its own antiderivative; the printed G is checked by SymPy (`L0_sympy.py`) and by the skeptic's Wolfram rerun. |
| N13 | Scales scattered; cloud type | List of scales and the cloud type added after the table of section 5. |
| r1 #10 | Thesis unnamed; "which textbook" | Named in the header (Koudsie 2022); Stokes' drag points to chapter 2 of these lecture notes and its SymPy check. |

## 12. Answers to round 3 (`skeptic-G1-L0-r3.md`)

| # | Objection | Answer |
|---|---|---|
| R3-1 | 8.1's "prediction" was already known | Accepted: relabelled as a known result that L0 explains; the contract says plainly that L0 holds no open prediction about nature, only the code test 8.2. |
| R3-2 | 3.65 min depends on the grid | The grid dependence (3.51 / 3.65 / 3.72 / 3.86 min) and the grid-free 4.0–4.1 min are stated in 8.1, with the reason (overflow mass stops collecting). |
| R3-3 | Slip on Δv | Corrected to +0.20 % with slip on both drops. |
| R3-4 | Section 10 rows 1, 2, 5, 6 describe replaced text | Section 10 is the record of round 2's answers; sections 11 and 12 supersede it where they differ (prediction 8.2, the coalescence row). |
| R3-5 | 8.2 lacks realisations and pooling rule | Added: 4000 runs, seeds 1–4000, pooling until each cell expects 5; outcome p = 0.15. |
| N12 | `L0_wolfram.md` item 4 overstates | Item 4 corrected in that file. |

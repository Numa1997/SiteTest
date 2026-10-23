# Skeptic review, Gate 1, contract L0, round 2

Reviewed: `notes/droplets/contract-L0.md` (round 2) against `skeptic-G1-L0-r1.md`; the cited files `portfolios-src/droplets/derive/`
`L0_sympy.py`, `L0_wolfram.md`, `L0_numbers.py`, `L0_r2.py`, `L0_population.py`; the three dossiers only to check citations.
Not read (outside my scope): `status.md`, the baseline, the thesis, other contracts. Claims that rest on them are marked "not checked".

All four Python files were run; their output matches the contract wherever the contract quotes them. The Wolfram input in
`L0_wolfram.md` was run again through the Wolfram evaluator and gave the same output. Every number below was then recomputed by a
different route, in scratch scripts outside the repository
(`/tmp/claude-0/-home-user-SiteTest/de75440b-f270-5344-8ae7-923c4f178e24/scratchpad/sk2_*.py`):

- `sk2_basic.py`: my own quadrature of every L0 time; scales; validity of the open cloud.
- `sk2_beard_hall.py`: Beard (1976) regimes 1 and 2 at 10 °C and 850 hPa, and Hall's (1980) E table, both typed from the dossier; the L0 observables with each correction.
- `sk2_master.py`: the capture-only master equation by another route. In the time s = ∫n_d dt the captures are a birth process with fixed rates, so P(s) = exp(Qs)P₀; then t = ∫ds/n_d.
- `sk2_pool.py`: the lognormal capture-only mean field with another discretization (continuous collector classes, exact 40 µm crossing).
- `sk2_sce.py`: my own SCE solver (fixed pivot, conserves number and mass), capture only and all pairs.
- `sk2_sdm.py`: super-droplet Monte Carlo (the Shima et al. 2009 scheme). It has no bin grid, so no numerical diffusion. Capture only and all pairs.
- `sk2_cond.py`: condensation supply from moist static energy with Bolton's e_s; `sk2_cv.py`: Monte Carlo of capture waiting times.

## What holds (checked, not taken on trust)

- (L0.1) → (L0.2), (L0.3), (L0.4), (L0.5): re-derived by hand. The printed F of (L0.4) and the printed G of (L0.5) give back their integrands
  when differentiated: SymPy (file) and my own Wolfram run both give 0. G gives 3.95757 and 12.04263 min; my quadrature gives the same to 6 digits.
- Numbers: k = 1.2296 × 10⁸ m⁻¹ s⁻¹, ρ_a = 1.0458 kg/m³, μ = 1.7711 × 10⁻⁵ Pa s, Re = 1 at 40.99 µm, τ_p(40 µm) = 20.08 ms, growth time 15.24 min,
  ratio 2.20 × 10⁻⁵. Open cloud 40 → 100 µm: 9.9554 min (finite r), 12.640 min (r ≪ R). R_m = 60.148 µm. Closed box: t₅₀ = 2.92704 and t₉₀ = 9.19197 min
  (finite r); 3.95757 and 12.04263 min (r ≪ R). Time shares 0.333 / 0.600 (r ≪ R) and 0.299 / 0.560 (finite r). N_c bound 0.154 cm⁻³; Pe = 6.19 × 10⁶;
  impaction St 3.79 / 5.82 / 9.81. Turbulence ratios: all nine agree. Collection drain 0.0528 g m⁻³ min⁻¹; moist air −0.55 %; 1829 captures;
  coefficient of variation 3.68 % (Monte Carlo: 3.67 %).
- Condensation: moist static energy with Bolton's e_s gives 2.04 g m⁻³ per km (contract 2.06), i.e. 0.061 / 0.122 / 0.244 g m⁻³ min⁻¹.
- Master equation, my route: t₅₀ = 2.9260 min, t₉₀ = 9.1843 min, 12.07 % of collector mass above R_m at t₉₀. This is the same as `L0_population.py`.
- Beard against Stokes: Stokes is too fast by +5.2, +11.1, +27.3 and +69.0 % at 30, 40, 60 and 100 µm.
- Lognormal pool mean field, converged: F₄₀ gives t₅₀ = 2.53 and t₉₀ = 6.82 min. The contract's 2.50 and 6.85 min carry the s = 8 bin-centre error, about 0.03–0.05 min.
- Dossier citations found: Hall E = 0.50 at r/R = 0.2. Langmuir Table 4 gives 0.394 at 785 mb and +2 °C, and his growth to 3 mm takes 3860 s.
  Beard's μ₀ = 1.818 × 10⁻⁵ Pa s. Telford (1955) was read (dossier-stochastic §1). The Ayala numbers +0.4 / +5.6 / +28 % come from the scout's own
  evaluation. Low and List measured drops of 0.395 mm and up. The ε range is the tabulated one.
- The bottleneck in §7 survives the corrections. With Beard speeds and Hall's E, growth from 40 to 60 µm still takes 51 % of the 40 → 100 µm time (L0: 53 %).

## Round-1 objections: answered or not

| # | Round-1 objection | Verdict | My evidence |
|---|---|---|---|
| 1 | Prediction 2 false (mass above 60 µm only by mergers) | **answered** | Withdrawn. The replacement number, 12.1 %, is reproduced by another route (12.07 %). The R(∞) = 1/(1/R₀ − Φ) argument is now in §8.1. But the replacement prediction 8.2 is not well posed (new N2). The claim "corrected in `status.md`" was not checked (outside my scope). |
| 2 | Prediction 1 untestable | **partly** | Widths, F₄₀ and the reference are now fixed and reproducible (my converged 2.53 / 6.82 min). The band is not derived: "±0.5 min" is two-sided, while the argument given says one side. Run as written, the prediction is met for a reason it does not mention, a runaway (new N1). |
| 3 | Snowball is not the mechanism | **partly** | The cardboard sheet gets the swept volume right (area × speed, R²·R²/R²). The size–speed feedback is told, not shown in the picture. The sheet catches every drop, i.e. it builds in E = 1, the factor §7 calls decisive (new N7). |
| 4 | 40 → 100 µm outside Stokes' range | **partly** | "Lower bound" is stated and the Beard ratios are right. But the time factors are not given: with Beard, 40 → 100 µm takes 13.0 min (+31 %), t₅₀ 3.35 min, t₉₀ 11.0 min. The new 40 → 60 µm observable has no number anywhere (mine: 5.31 min; Beard: 6.29 min). See N5. |
| 5 | E = 1 and coalescence = 1 have no number | **partly** | Hall 0.50 and Langmuir 0.394 found in the dossier; impaction St correct. "0.344 own solver" has no file (N9). The coalescence number is selective (N4). The effect of E on the observables is not given (N5). |
| 6 | Open vs closed cloud | **answered** | 0.154 cm⁻³ correct, and the open cloud is now separated from the thesis cloud. The "≪" could be a number (N11). |
| 7 | Thermal row is decoration | **answered** | Pe = 6.19 × 10⁶ correct. Condensation 2.06 g m⁻³ km⁻¹ confirmed by another route (2.04). Drain 0.0528 correct. |
| 8 | Turbulence row checks the wrong particle | **answered** | Collector St and the shear and inertia ratios recomputed; Ayala's numbers match the dossier; the ε range is the tabulated one. The dossier's cumulus range, 1–6.5 × 10⁻² m²/s³, sits above "small" (+28 % at 4 × 10⁻²). The contract does not say which kind of cloud it means (minor, N13). |
| 9 | 0.8 % per capture is not the measure | **answered** | 1829 captures; CV 3.68 % (Monte Carlo 3.67 %); master equation reproduced; "wrong for the tail" stated. |
| 10 | Unsourced model and closures; "whose thesis?" | **partly** | Langmuir is cited, but the dossier section named (§5) does not show his growth equation (N8). Telford is now traceable. **The thesis is still unnamed**, yet the cloud, the lognormal widths, the viscosity constants ("thesis eq. 20, as quoted in the baseline") and the "old study's row" all rest on it. "Stokes' drag (derived again in the textbook)": which textbook? Must fix. |
| 11 | "Exact" on the r ≪ R approximation | **answered** | Now "the r ≪ R limit, 35 % and 31 % too slow" (I get 1.352 and 1.310). |
| 12 | Checks claimed that the files do not contain | **partly** | The limit is now in `L0_sympy.py` (ran it: (R₁ − R₀)/(R₁R₀)). The Wolfram input and output are saved, and my rerun matches. 12.64 min correct. Fermi time 17 min = 1/(N_c πR₀²v) with r ≪ R (mine 16.85 min); `status.md` not checked. **But a new unbacked check appears: "2.928, 9.186 min (quad)"** (N3). |
| 13 | Blow-up instead of the bottleneck | **answered** | §7 gives the shares, and they survive Beard + Hall (51 % against 53 %). |
| 14 | "Faster than linear" blows up | **answered** | Now stated as a necessary condition, with the integral test. |
| 15 | Ratio 10⁻⁴ not computed | **answered** | 2.20 × 10⁻⁵. |
| 16 | ⟨R⁴⟩ against R̄⁴ | **answered** | Argument removed. |
| 17 | Moist air, slip, edge of Stokes | **partly** | Density row and tolerance wording correct. The slip number (+1.2 % on v(8 µm); my effect on Δv: 0.05 %) appears only in §10, not in the §5 table. |
| 18 | Box geometry | **partly** | A fall distance is given only as a bracket, "109–243 m"; computed, it is 176.5 m. "Swept about once by t₉₀": the integral is 1.95 sweeps (14 % of the droplet water is left). "Remixed" sits beside "air still" with no scale argument (N10). |
| 19 | "No measurement" | **answered** | Softened to what was searched. |
| 20 | Two effects at L0 | **answered** | The argument (depletion adds no law, only mass conservation) is acceptable. |
| 21 | (L0.5) closed form not printed | **partly** | Printed and correct. "SymPy's antiderivative failed its own check by 2.8 %" exists only as a comment, with no output. My own SymPy attempt timed out after 15 min, so I can neither confirm nor refute it (minor). |
| 22 | "Rain-sized" undefined | **partly** | Sizes are defined. But "L0 reaches only drizzle embryos (r ≥ 100 µm)" is false for the thesis cloud, which stops at 60.15 µm. The name is also odd: drizzle drops are r ≈ 100–250 µm, and "embryo" usually means the 20–40 µm seed (N6). |

## New objections

| # | Where | What is wrong | Why (estimate or source) | Severity | What would settle it |
|---|---|---|---|---|---|
| N1 | §8.1 | The "full SCE with this kernel" meets the bounds (t₅₀ within ±0.5 min of 2.50, t₉₀ below 6.85) by a wide margin. The reason is one the prediction does not name: with Stokes speeds and E = 1 for every pair, the population runs away (gels). The bounds are not derived and cannot see it. | Super-droplet runs (3 runs; 2¹⁶–2¹⁷ super-droplets; 1 m³; Δt 0.1 and 0.05 s): t₅₀ = 2.27–2.33 min, t₉₀ = 4.03–4.07 min. At 5 min, 97–99 % of all the water is in drops ≥ 1 mm; by 6.85 min the whole cubic metre is one 6.4 mm drop. My bin SCE (s = 4, grid to 2 mm): t₅₀ 2.27, t₉₀ 3.80 min, and 85 % of the mass has left the top of the grid by 5 min. The kernel grows as mass^{4/3}, faster than mass; this is the population form of the (L0.3) blow-up (dossier-stochastic §0(b)2: the SCE loses mass once a gel forms). At t = 0 a collector meets another collector every 8.5 min and a droplet meets another droplet every 13 min, not long against 6.85 min. Consequences: (i) a solver that drops mass leaving its grid (common) never reaches F₄₀ = 0.9, and the contract would blame the solver for what the kernel does; (ii) §7 calls the blow-up "outside the model's range", yet in L4 it sets t₉₀; (iii) "±0.5 min" is two-sided against a one-sided argument; (iv) the SCE adds a third difference, the spread of capture counts (small here: SCE capture-only 2.55 / 6.80, super-droplet 2.50 / 6.78, pool 2.53 / 6.82). | must fix | Run the all-pairs case now (about a minute of super-droplet time). State t₅₀ ≈ 2.3 and t₉₀ ≈ 4.1 min and the runaway. Require L4 to count mass leaving its grid. Or predict for a kernel that stops using Stokes beyond its range, with bands taken from runs. |
| N2 | §8.2 | "12 ± 2 % of collector mass above R_m at t₉₀": the number is right (12.07 %), but the band is smaller than the effect of three choices the prediction leaves open. A correct solver can fail it. | Time: 9.9 % at t₉₀ − 15 s, 14.3 % at t₉₀ + 15 s. Threshold: 21.5 / 14.4 / 8.7 / 5.0 % at 59.5 / 60.0 / 60.5 / 61.0 µm. Grid: put the exact distribution on a mass-doubling grid with s bins per doubling and count bins whose centre is above R_m. That gives 74 / 9.6 / 37.9 / 20.7 / 14.4 % for s = 1 / 2 / 4 / 8 / 16; with the lower-edge rule, 0 / 9.6 / 1.1 / 3.6 / 6.2 %. A perfect solver at s = 16 fails. The spread is only 1.7 µm (s.d. of R at t₉₀). | must fix | Fix the time (551.1 s, the master-equation t₉₀). Ask for s ≥ 32 or a stated sub-bin rule. Or test a statistic that does not depend on the grid: the s.d. of R, 1.70 µm at t₉₀, or the variance of collector mass. |
| N3 | §6 closed box; comment in `L0_sympy.py` | "2.928, 9.186 min (quad)" and "quad in `L0_population.py`": that file has no quad (only `solve_ivp` and the master equation). My quad gives 2.92704 and 9.19197 min, the same as `solve_ivp`; the quoted 9.186 is off by 0.006 min and cannot be traced. | Round-1 #12 again: a check route claimed that the cited files do not contain, quoted as an independent agreement. | must fix | Put the quadrature in a cited file and print its output, or delete the route. |
| N4 | §5 coalescence row | "Energy-based laws give ≥ 0.9996." Only one law gives that: Straub's, extrapolated 20 times below its range. The other energy-based law in the same dossier, extrapolated the same way, gives about half. | Low and List, a(1 + d_S/d_L)⁻² exp(…), with a = 0.778 and an exponential equal to 1 here: 0.54 (40 + 8 µm), 0.61 (60 + 8), 0.23 (50 + 60). Beard and Ochs (1984, abstract, dossier §2.1): for 30 µm droplets, coalescence lowers time-averaged collection 50 % below collision. The only formula built for this range (Beard and Ochs 1995) was not opened; per Jacobson it tends to 1 below d_s = 14 µm, and ours is 16 µm. | must fix | Write: "not measured below about 0.4 mm; extrapolations disagree (Straub 0.99998, Low and List 0.54); BO95 suggests near 1; taken as 1, uncertainty unknown." |
| N5 | §5, §9 | The study asks "how fast". L0 gives the error of the rate, not of the times, and calls only the open-cloud times lower bounds. | From the dossier tables: Beard + Hall give open 40 → 60 µm 11.2 min (L0 5.31), 40 → 100 µm 21.9 (9.96); closed box t₅₀ 6.41 (2.93), t₉₀ 19.2 (9.19). Beard alone: 6.29 / 13.0 / 3.35 / 11.0 min; Hall alone: 9.51 / 16.9 / 5.61 / 16.1 min. Every L0 time is short by about a factor 2, the closed-box times included. | must fix | One line per observable: L0, with Beard, with Beard and Hall, labelled "first estimate before L1/L2". |
| N6 | §1 "L0 reaches only drizzle embryos" | In the thesis cloud the L0 drop stops at R_m = 60.15 µm, below the contract's own 100 µm. So L0's answer to "how does it become rain" is: not by capture onto identical collectors. That needs collector–collector mergers or a spread of collector sizes. This is the main L0 result for the study's question, and it is not said. | Master equation at 60 min: P(R ≥ 65 µm) = 0.5 %, P(R ≥ 68 µm) = 2 × 10⁻⁵. Only the open cloud (N_c ≪ 0.15 cm⁻³, not the thesis cloud) reaches 100 µm. | must fix | Say it in one sentence in §1 and §7. Rename the size classes (drizzle drop r ≈ 100–250 µm). |
| N7 | §2 picture | The picture shows half the mechanism. The sheet catches every drop in its path (E = 1), the factor §7 says decides the speed. A heavier sheet does not make you run faster, so the feedback is told, not shown. Both drops fall, so the sweep uses the difference of speeds. | At 40 µm only half of the droplets in the path are hit (Hall 0.50); the air pushed aside carries the rest round. | minor | Add one sentence: "unlike the sheet, the drop pushes the air aside, and about half of the droplets in its path ride round it." |
| N8 | §2 "Langmuir (1948; read in the scout's dossier, section 5)" | Dossier §5 does not quote Langmuir's growth equation, nor the finite-r form (R + r)²[v(R) − v(r)]. The attribution is probably right, but the cited text does not show it. | — | minor | Give Langmuir's equation number from the PDF, or write "attributed, not checked". |
| N9 | §5 E row | "0.344 from this study's trajectory solver (prototype for L2)": no file is cited, and it is not among the L0 files. | — | minor | Cite the file and its output, or drop the number. |
| N10 | §5 rows "air still" and "well-mixed box" | In still air nothing remixes the droplets: identical droplets have no relative motion, and Pe = 6 × 10⁶. The scale argument that reconciles the two rows is missing. | Weak turbulence (ε ≈ 10⁻⁴–10⁻³ m²/s³) mixes the 1 cm spacing between collectors in (l²/ε)^{1/3} ≈ 0.5–1 s. The depletion time 1/(N_c K) is 12.2 min. Collisions change by < 1 %. | minor | State that scale argument. Replace "about once" by 1.95 sweeps and the bracket by 176.5 m. |
| N11 | §1 open-cloud condition | "N_c ≪ 0.154 cm⁻³" is a scale, not a usable condition. | The closed box with the same droplet water, against the open cloud's 40 → 100 µm time: +67 % at 0.154, +8.8 % at 0.05, +2.3 % at 0.015, +0.8 % at 0.005 cm⁻³. | minor | "N_c ≤ 0.015 cm⁻³ for ≤ 2 % on the 40 → 100 µm time." |
| N12 | `L0_wolfram.md` item 4; §3 | Item 4 says Wolfram confirms (L0.5), but it differentiates Wolfram's own antiderivative, not the printed G. | I re-ran it with the printed G and F: both give back the integrand exactly (0). The substance holds; the claim is too strong. | minor | Add the printed G and F to the saved Wolfram input. |
| N13 | §5 overall; cloud type | No list of scales: t* = 17.77 min, depletion time 12.2 min, R_m, Re, St_imp and the capture count are scattered through the table. The kind of cloud (layer or cumulus) is not stated, but it decides whether the turbulence row is "small". | Dossier cumulus ε 100–650 cm²/s³: the kernel changes by +6 % to about +30 % (more beyond the formula's range). | minor | Add a short list of scales and say which kind of cloud is meant. |

Not checked (outside my read scope): the correction claimed in `status.md`; the Fermi text there; "thesis eq. 20 as quoted in the baseline";
"the old study's 'continuous GCE, thesis kernel' row (3 and 7 min)".

## The six thresholds

| Threshold | Verdict | Reason |
|---|---|---|
| Motivated | **pass (narrow)** | Open and closed settings are separated, the observables are defined, and the bottleneck answers "which ingredient" and survives Beard + Hall. But L0's answers to "how fast" (about ×2 lower bounds) and "into rain?" (stops at 60 µm) are not stated (N5, N6). |
| Honest | **fail** | Again a check route and two numbers that no file contains (quad 2.928 / 9.186, N3, the same fault as round-1 #12). "Energy-based laws ≥ 0.9996" leaves out the law in the same dossier that gives 0.54 (N4). 0.344 and the "SymPy failed by 2.8 %" rest on nothing cited. |
| Derived | **fail** | (L0.1)–(L0.5) are re-derived and correct. Neither prediction band is derived: 8.1 misses the runaway that sets t₉₀ ≈ 4.1 min in its own model (N1), and the ±2 % of 8.2 is smaller than its own open choices of time, threshold and grid (N2). |
| Checked | **pass** | Every equation and every other printed number was reproduced by an independent route (quadrature, Wolfram, the master equation in operational time, Monte Carlo, moist static energy), except the quad pair of N3. |
| Sourced | **fail (narrow)** | Hall, Langmuir, Beard, Ayala and Telford can be traced in the dossiers. But the thesis (the cloud, the widths, the viscosity constants, the comparison row) is still unnamed (round-1 #10), the Langmuir model equation is not in the cited section, and 0.344 has no file. |
| Readable | **pass (narrow)** | Ordered and short, with symbols defined and (L0.5) printed. The picture shows half the mechanism and the scales are scattered, not listed. |

Gate 1 for L0, round 2: **not passed.** No fatal objection. Six new must-fix objections (N1–N6) and one carried over from round 1 (#10, the
unnamed thesis). Of the 22 round-1 objections, 12 are answered and 10 only in part.

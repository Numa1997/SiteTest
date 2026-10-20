# Fig. 10 · derivation check

Checker: derivation-checker agent. Page: `public/simulations/wind-turbine.html`, the note between `<article class="paper" id="paper">` and `</article>`, at HEAD 468c139 (branch `claude/physics-notes-rewrite-cwctkk`).
Against the commit I started from (127a8d2), 468c139 changes only the layout of equations (3) and (10), each now on two lines, with the same content. The page script is byte-identical to the one I ran.
I did not read `notes/fig10/plan.md` or any teacher script or report.

While I was finishing, another agent left uncommitted edits to the page in the working tree. They touch nine lines:
- Figure 1: the tip arrow now points out of the page.
- §2: one clause added ("since power is torque times angular speed, the wind's torque on the rotor is that power divided by ω"). It is correct.
- §4: the sentence "The curve c_p(λ) used here is an empirical fit … slow- and fast-running limits" is removed.
- Figure 3: the subscript labels are reformatted.
- Equation (8) is reflowed onto two lines, with the same content.

None of these edits changes an equation's content, a number, the 7° sentence or the script. Every verdict below is for HEAD 468c139 and holds for this working copy too.

## How the checks were made

- **Equations.** Each one was re-derived in SymPy 1.14 (`derive.py`), with units from `sympy.physics.units` and limiting cases.
- **Numbers.** The site was built with `APPDEPLOY_VITE_OUT_DIR=/tmp/fig10-check-dist npm run build`. The built page is identical to the repository page. It was served by a small Node static server and run in headless Chromium 1194 through Playwright.
- **The eight runs.** All eight controller × wind runs were solved by clicking the page's own buttons. The values were read from the page's store (`Sim.data.ds`) and from the visible readouts.
- **Modified copies.** For checks that need the page's internal functions, I served modified copies from `/tmp/fig10-mod`. There were five, made from the built page. Each copy differs from the original in three places only:
  - one line exposes `cp`, `tauAero`, `wind`, `rates` and the constants as `window.__wt`;
  - one line in `rates()` records the PI command `raw` and the value `K_opt ω²` at every RK4 stage;
  - the constants `H` and `EVERY` are changed for the step-size study (h = 2.5, 5, 10 and 20 ms, always storing one sample every 20 ms).
  The h = 10 ms copy reproduces the original page's stored runs exactly.
- **Rendering.** KaTeX renders all ten numbered equations with no `katex-error`, tagged (1)–(10) in order. Equations (3) and (10) were screenshotted after the reflow: two lines each, with one tag.

## Equations

| # | Where | Claim in the note | Check | Verdict |
|---|---|---|---|---|
| E1 | §2, (1) | P_wind = ½ρAv³ | Mass flux ρAv times ½v² per kilogram. Units: kg m⁻³ · m² · m³ s⁻³ = W. Doubling v gives 8×; v = 0 gives 0. | verified |
| E2 | §2, (2) | P_aero = c_p ½ρAv³, τ_aero = P_aero/ω | A definition. Units N m. The code's `tauAero` is `0.5·RHO·AREA·v³·cp(ωR/v)/ω`, the same thing. | verified |
| E3 | §3, Bernoulli step (changed) | In front: p₀ + ½ρv² = p⁺ + ½ρv²(1−a)². Behind: p⁻ + ½ρv²(1−a)² = p₀ + ½ρv_w². Adding gives Δp = ½ρ(v² − v_w²) | Solving the two equations for p⁺ and p⁻ in SymPy gives p⁺ − p⁻ = ½ρ(v − v_w)(v + v_w). p₀ and the speed at the disc cancel, as stated. Limit: v_w = v gives Δp = 0. | verified |
| E4 | §3, momentum | ΔpA = ρAv(1−a)(v − v_w), so v(1−a) = ½(v + v_w) and v_w = v(1−2a) | SymPy gives two roots, v_w = v (no force: the trivial case excluded by dividing by v − v_w) and v_w = v(1−2a). With that root the disc speed equals the mean of v and v_w exactly. | verified |
| E5 | §3, (3) (reflowed) | P = ρAv(1−a)·2av·v(1−a) = 2ρAv³a(1−a)², c_p = 4a(1−a)² | Thrust ρAv(1−a)(v − v_w) with v − v_w = 2av, times v(1−a): SymPy confirms both lines. Limits: a = 0 gives 0; a = ½ (wake at rest) gives ½. Renders on two lines with one tag (3). | verified |
| E6 | §3 (changed) | dc_p/da = 4(1−a)(1−3a); roots 1/3 and 1; a = 1 stops the air at the disc and takes nothing | SymPy factorises the derivative exactly so. c_p(1) = 0, and the disc speed v(1−a) = 0 at a = 1. | verified |
| E7 | §3, (4), box | c_p,Betz = 16/27 ≈ 0.593; 59.3 %; air slowed to 2/3 at the disc and 1/3 in the wake | c_p(1/3) = 16/27 = 0.592593. The second derivative is −8 < 0, so this is a maximum. 1 − a = 2/3 and 1 − 2a = 1/3. | verified |
| E8 | §4, (5) | Heier fit with c₁ = 0.5176, c₂ = 116, c₄ = 5, c₅ = 21, c₆ = 0.0068, 1/λᵢ = 1/λ − 0.035 | The code's `cp()` uses the same constants and formula, the β = 0 form of 1/λᵢ = 1/(λ+0.08β) − 0.035/(β³+1). The code adds cut-offs that (5) does not show: c_p = 0 for λ ≤ 0.05 and for 1/λ ≤ 0.035, and `max(0, ·)`. None is reached in the eight runs, where λ stays between 5.67 and 11.89. The clipped zero beyond λ = 13.4 is what Figure 2 draws. | verified |
| E9 | §5, (6) | J dω/dt = τ_aero − τ_gen | Newton's second law for rotation. The code's `rates()[0]` is `(a − g)/J`. | verified |
| E10 | §5, (7) | E_aero = E_gen + Δ(½Jω²) | Multiply (6) by ω. SymPy: d/dt(½Jω²) − Jωω̇ = 0. Integrate. The code checks \|E_a − E_g − ΔKE\|/E_a with ΔKE = ½J(ω_end² − ω₀²). | verified |
| E11 | §6.1, (8) | τ_aero at λ_opt = K_opt ω², K_opt = ρπR⁵c_p,max/(2λ_opt³) | SymPy with v = ωR/λ_opt. Units kg m⁻³·m⁵ = kg m² = N m s². The code's `K_opt` uses the same formula. | verified |
| E12 | §6.1 (changed) | ω* = λ_opt v/R; dc_p/dλ = 0 there, so the aero slope is −P_aero/ω*² = −K_opt ω* | SymPy: in general ∂τ_aero/∂ω = πR⁴ρv(λc_p′ − c_p)/(2λ²). With c_p′(λ_opt) = 0 this becomes −πR⁴ρv c_p,max/(2λ_opt²) = −K_opt ω*. And P_aero = K_opt ω*³ there. | verified |
| E13 | §6.1 | The brake's slope is 2K_opt ω*; the net slope is −3K_opt ω* < 0 | SymPy: d(K_opt ω²)/dω = 2K_opt ω*; the difference is −3K_opt ω*. | verified |
| E14 | §6.1 | J δω̇ ≈ −3K_opt ω* δω, relaxation time J/(3K_opt ω*) | Follows from E13. | verified |
| E15 | §6.1 (changed) | With v = ωR/λ in (2), the net torque is ½ρπR⁵ω²[c_p(λ)/λ³ − c_p,max/λ_opt³] | SymPy: identical. | verified |
| E16 | §6.2, (9) | τ_gen = τ₀ + K_p(ω − ω_ref) + K_i∫(ω − ω_ref)dt′ | Matches `tauGen()` (clamped to [0, TMAX]) and the state I of `rates()`. | verified |
| E17 | §6.2 (changed) | τ₀ = τ_aero(ω_ref, v(0)) balances the wind at the start, so the run begins in equilibrium with nothing to remember | The code sets `c.tau0 = tauAero(c.wref, wind(0,c))` and starts with ω = ω_ref and I = 0. Stored at the first sample of every PI run: τ_gen = τ_aero = 480 285.497 N m (steady, gust, step) and 334 296.845 N m (turbulent, v(0) = 7.138 m/s); I = 0. | verified |
| E18 | §6.2 (changed) | J δω̇ = (∂τ_aero/∂ω − K_p)δω − K_i∫δω dt′ | SymPy: substitute (9) and the linearised τ_aero into (6) with τ₀ = τ_aero(ω_ref). The constants cancel and this form remains. | verified |
| E19 | §6.2, (10) (reflowed) | J δω̈ + (K_p − ∂τ_aero/∂ω)δω̇ + K_i δω = 0 ⇔ δω̈ + 2ζ_cω_n δω̇ + ω_n² δω = 0 | SymPy: differentiating E18 gives the first form. Dividing by J gives the second, with 2ζ_cω_n = (K_p − ∂τ/∂ω)/J and ω_n² = K_i/J. Renders on two lines with one tag (10). | verified |
| E20 | §6.2 | K_i = Jω_n², K_p = 2ζ_cω_n J + ∂τ_aero/∂ω | SymPy solve of E19's matching. Units: K_i in N m (per rad of integrated error), K_p in N m s. The same formulas are in `solve()`. | verified |

## Numbers

All values below were computed by the page's own code in headless Chromium, unless the row says otherwise.

| # | Where | Note says | Recomputed | Verdict |
|---|---|---|---|---|
| N1 | §1 | πR² = 5027 m² | 5026.55 m² (`AREA`) | verified |
| N2 | §1 | about 70 % of a football pitch | 5026.5 / (105 × 68 = 7140 m², the IFAB/FIFA recommended size) = 70.4 % | verified |
| N3 | §1 lead | each blade longer than a jumbo jet's wing | 40 m against about 29 m from fuselage to tip for a 747-400 (64.4 m span) | verified |
| N4 | §1 (changed) | 15 rpm is ω = 1.57 rad/s | 1.570796 rad/s | verified |
| N5 | §1 | ωR = 62.8 m/s, over 220 km/h | 62.832 m/s = 226.2 km/h | verified |
| N6 | §2 | 1.58 MW at 8 m/s | 1 576 326 W | verified |
| N7 | §2 | 4.10 MW at 11 m/s | 4 097 831 W | verified |
| N8 | §3 | Betz worked out the limit in 1920 | van Kuik, *Wind Energy* 10, 289 (2007), doi:10.1002/we.218, abstract: "formulated this maximum in 1920" (read with Firecrawl) | verified |
| N9 | §4 (changed) | A blade piece meets the air from an angle with tan = v/(ωr) = (R/r)/λ; at the tip at λ = 8.1, only 7° off the rotor plane | The arithmetic is right: atan(1/8.1) = 7.04°. But that is the angle of the **undisturbed** wind. Section 3 of the same note shows that the air reaches the disc slowed to v(1−a). Blade-element theory (Burton et al., ch. 3) gives tan φ = v(1−a)/(ωr(1+a′)). At the tip with the Betz-optimal a = 1/3 (a′ ≈ 0.003 there), φ = atan((2/3)/8.1) = **4.7°**. | wrong, because the angle the blade meets is set by the slowed air at the disc, not by the free wind. Correct: about 4.7° at the tip at a = 1/3; 7° is the angle of the undisturbed wind. Fix: say "the undisturbed wind comes from 7° off the rotor plane; slowed by the rotor, the air reaches the blade at about 5°". The λ-only argument (N10) is not affected. |
| N10 | §4 (changed) | Keeping λ while changing ω and v keeps every inflow angle, so c_p depends on λ alone | True with the free-stream angle as written. Also true with induction: in blade-element momentum theory the induction factors a and a′ are themselves functions of λ and r/R only. The argument neglects Reynolds- and Mach-number effects, as is standard. | verified |
| N11 | §4 | Scanning in steps of 0.001: c_p,max = 0.4800 at λ_opt = 8.100 | Stored: λ_opt = 8.10000000000095, c_p,max = 0.4800119. An exact-grid rescan gives the same. A golden-section search gives the true maximum 0.48001190 at λ = 8.10012. | verified |
| N12 | §4 | comfortably below the Betz limit | 0.480 against 0.593 | verified |
| N13 | §4 | The c₆λᵢ version peaks at 0.502 at λ = 8.25 and is widely copied | 0.502272 at λ = 8.2449 (8.245 on the 0.001 grid). The variant appears, for example, in Kumar et al. (INASE 2015) and Sayeh et al. (HAL 2024), found by web search. | verified |
| N14 | Fig. 2 | The curve falls back to zero at λ = 13.4; dashed lines at 16/27 and λ_opt = 8.1 | The zero of (5) is at 13.402. I parsed the 1351 path points of the SVG: they lie within 0.10 px of c_p(λ) from the page's formula, reaching 0 at λ ≈ 13.41. The Betz line sits at y = 38.8 (expected 38.84) and the λ_opt line at x = 430.8 (expected 430.81). | verified |
| N15 | Fig. 2 caption | 0.48 × 1.58 MW = 757 kW | 0.4800119 × 1.5763255 MW = 756.66 kW. The rounded factors as printed multiply to 758 kW; 757 is the correct rounding of the exact product. | verified |
| N16 | Fig. 2 caption | reached at 15.5 rpm | λ_opt·8/40 rad/s = 15.470 rpm | verified |
| N17 | §5 | J = 4.0 × 10⁶ kg m² | `J = 4.0e6` | verified |
| N18 | §6.1 | K_opt = 1.78 × 10⁵ N m s² | 177 972.5 | verified |
| N19 | §6.1 | relaxation time ≈ 4.62 s at 8 m/s | J/(3K_opt ω*) with ω* = 1.62 rad/s gives 4.6246 s (4.6247 with the rounded inputs 0.48 and 8.1) | verified |
| N20 | §6.1 | c_p/λ³ is not monotone: it rises between λ = 2.4 and 4.3 | Rising on [2.4397, 4.2805] (step 10⁻⁴). The page's cut-off adds only a one-sample artefact at λ = 0.05. | verified |
| N21 | §6.1 | c_p/λ³ stays above its λ_opt value for every λ below λ_opt and below it above, checked on a 10⁻⁴ grid | With formula (5): no violation on λ ∈ [10⁻⁴, 20], step 10⁻⁴. With the page's `cp()`: 500 violations, all at λ ≤ 0.05, where the code (not the fit) sets c_p = 0. | verified (for the fit, as the note states) |
| N22 | §6.1 | So in steady wind the rotor returns to λ_opt from any start at which it is already turning | True for the fit (5), from N21. In the page's code it holds only for λ > 0.05 (ω > 0.01 rad/s at 8 m/s), because of the cut-off. No run comes near: λ stays at or above 5.67. | verified |
| N23 | §6.1 | "(The fit gives no torque at a standstill, so it says nothing about starting.)" | As λ → 0 the exponential term of (5) vanishes faster than any power, so c_p → c₆λ. Then τ_aero = ½ρAv³c_p/ω → **½ρAv²c₆R = 53.6 kN m at 8 m/s**, a finite starting torque. I evaluated (5) at ω = 10⁻³, 10⁻² and 0.1 rad/s: 53 595 N m each time. The brake K_opt ω² is zero at standstill, so the fit would start the rotor by itself. It is the page's **code** that gives zero torque: `cp()` returns 0 for λ ≤ 0.05, and `tauAero` returns 0 for ω ≤ 10⁻⁶. | wrong, because formula (5) gives a finite torque at standstill, ½ρAv²c₆R = 53.6 kN m at 8 m/s, not zero. Correct: "the code sets c_p = 0 below λ = 0.05, so it gives no torque at a standstill; the fit itself is not meant for such slow running, so the page says nothing about starting". |
| N24 | §6.2 | ω_n = 0.6 rad/s, ζ_c = 0.8 | `WN = 0.6`, `ZC = 0.8` | verified |
| N25 | §6.2 | K_i = 1.44 × 10⁶ N m | 1 440 000 | verified |
| N26 | §6.2 | aerodynamic slope −2.48 × 10⁵ N m s at 15 rpm, 8 m/s | −248 008.0 by the page's central difference (δω = 10⁻⁴). Negative, so the wind damps the rotor; that is 6 % of 2ζ_cω_nJ. | verified |
| N27 | §6.2 | K_p = 3.59 × 10⁶ N m s | 3 591 992 | verified |
| N28 | §6.2 | an error decays within a few seconds | envelope e^(−ζ_cω_n t), time constant 1/0.48 = 2.08 s | verified |
| N29 | §6.2 (changed) | ζ_c a little below 1, so it swings once past zero by only a few per cent | For the linear free response, the second extremum is exp(−πζ/√(1−ζ²)) = 1.5 % of the first. In the Step run, the dip after the peak is 0.0122/0.3947 = 3.1 % of the overshoot. | verified |
| N30 | §6.2 (changed) | after the wind steps up in the Step run, the rotor overshoots the target by **0.40 rpm** | Step run, hold speed: the stored peak is 15.394736 rpm at t = 32.96 s, against a target of 15 rpm. That is an overshoot of 0.3947 rpm, which rounds to 0.39 (the table's "15.0–15.4 rpm" agrees). Samples are 20 ms apart, so the true peak differs by much less than 10⁻⁴ rpm. | wrong, because 0.3947 rpm rounds to 0.39 rpm, not 0.40. Correct: "overshoots the target by 0.39 rpm" (or "about 0.4 rpm"). |
| N31 | §6.2 (changed) | then dips below it by just 0.01 rpm | The minimum after the peak is 14.987847 rpm at t = 40.80 s, a dip of 0.0122 rpm. | verified |
| N32 | §6.2 | torque kept between 0 and 1.2 MN m | `TMAX = 1.2e6`; PI clamps with `max(0, ·)` and `min(TMAX, ·)` | verified |
| N33 | §7 | 16 sine waves between 0.005 and 0.5 Hz, amplitudes ∝ f^(−1/3) | `TF = 0.005·100^(q/15)`, q = 0…15 (0.005…0.5 Hz, log-spaced); `TA = f^(−1/3)` | verified |
| N34 | Fig. 4 caption | σ = 1.5 m/s, but over these 120 s the standard deviation is 1.30 m/s, because the slowest waves take longer than the run | Stored turbulent wind: population sd 1.3030, sample sd 1.3031 (mean 7.952). Normalisation √(Σa²/2)/TNORM × 1.5 = 1.5 exactly for the long-run σ. The slowest wave lasts 200 s, longer than the 120 s run. | verified |
| N35 | Fig. 4 caption | holding speed 14.4–15.7 rpm; following the wind 12.5–19.8 rpm | 14.4108–15.6790; 12.4675–19.8059 | verified |
| N36 | Fig. 4 | curves computed with the page's own algorithm | I parsed the SVG paths (601 points each) and compared them with the stored runs: wind within 0.29 px; rpm within 0.11 px (follow) and 0.10 px (hold); power within 0.15 px and 0.42 px (0.42 px = 3.6 kW). | verified |
| N37 | table | steady, hold: 25.15 kWh, 754 kW, 15.0 rpm, 0.479 | 25.1477 kWh, 754.43 kW, 15.000, 0.478601 | verified |
| N38 | table | steady, follow: 25.22 kWh, 757 kW, 15.5 rpm, 0.480 | 25.2218, 756.66, 15.4699, 0.480012 | verified |
| N39 | table | gust, hold: 25.22 kWh, 757 kW, 14.8–15.3 rpm, 0.478 | 25.2231, 756.69, 14.7721–15.3352, 0.478092 | verified |
| N40 | table | gust, follow: 25.30 kWh, 759 kW, 15.2–16.1 rpm, 0.480 | 25.3000, 759.00, 15.2480–16.0738, 0.479549 | verified |
| N41 | table | step, hold: 34.43 kWh, 1033 kW, 15.0–15.4 rpm, 0.437 | 34.4263, 1032.79, 14.9878–15.3947, 0.436798 | verified |
| N42 | table | step, follow: 37.18 kWh, 1115 kW, 15.5–18.4 rpm, 0.479 | 37.1806, 1115.42, 15.4699–18.3705, 0.479332 | verified |
| N43 | table | turbulent, hold: 24.73 kWh, 742 kW, 14.4–15.7 rpm, 0.443 | 24.7336, 742.01, 14.4108–15.6790, 0.442836 | verified |
| N44 | table | turbulent, follow: 26.18 kWh, 785 kW, 12.5–19.8 rpm, 0.466 | 26.1830, 785.49, 12.4675–19.8059, 0.465646 | verified |
| N45 | §7 | in steady wind 15 rpm is close to the optimum 15.5 rpm | 15.470 rpm; c_p 0.47860 against 0.48001 | verified |
| N46 | §7 (changed) | after the step to 9.5 m/s the rotor stays at 15 rpm and λ falls to 6.6 | v = 9.5 after the ramp. At t = 120 s: rpm = 15.000000, λ = 6.6139. | verified |
| N47 | §7 (changed) | c_p drops from 0.48 to 0.43 | 0.47860 at t = 29.98 s; 0.42744 at t = 120 s; c_p(6.6139) = 0.42744 | verified |
| N48 | §7 (changed) | which pulls the captured share of the whole run down to 0.44 | E_aero/E_wind = 0.436798 | verified |
| N49 | Exercise 7.1 | the rotor speed that puts λ at 8.1 in a 9.5 m/s wind, nearest slider value | 18.37 rpm, so the slider gives 18.5 (step 0.5, range 8–21). The exercise can be done. | verified |
| N50 | §8 | 12 000 steps of h = 10 ms from 0 to 120 s | `TEND/H` = 12000 exactly in JS; status shows "Solved 12,000 RK4 steps" | verified |
| N51 | §8 (changed) | quickest wind wave has a period of 2 s; the controller answers within seconds; each is cut into hundreds of steps | 1/0.5 Hz = 2 s = 200 steps. Controller time constant 2.08 s = 208 steps; damped period 17.5 s. | verified |
| N52 | §8 (changed) | RK4's error shrinks like h⁴ | Against an h = 2.5 ms reference, the maximum stored-rpm differences are 1.27 × 10⁻¹² (5 ms), 2.16 × 10⁻¹¹ (10 ms) and 3.47 × 10⁻¹⁰ (20 ms). The successive ratios are 17.0 and 16.1, close to 2⁴. | verified |
| N53 | §8 (changed) | defaults solved with h = 5 ms change the stored rotor speed by at most 2 × 10⁻¹¹ rpm | max \|rpm(5 ms) − rpm(10 ms)\| = 2.03 × 10⁻¹¹ rpm (at t = 6.02 s), on all 6001 common samples | verified |
| N54 | §8 (changed) | and with h = 20 ms by 16 times as much | max \|rpm(20 ms) − rpm(10 ms)\| = 3.256 × 10⁻¹⁰ rpm; ratio 16.03 | verified |
| N55 | §8 (changed) | none of the eight runs of section 7 reaches a torque limit | Instrumented at every RK4 stage (48 000 evaluations per run). The PI command raw = τ₀ + K_pe + K_iI stays in [32 367, 915 517] N m. K_opt ω² never exceeds 765 599 N m. TMAX is 1.2 × 10⁶, so the anti-windup branch never acts. The turbulent wind never reaches its 0.5 m/s floor (minimum 5.15 m/s). | verified |
| N56 | §8 | 6 001 rows stored | `NS` = 6001 | verified |
| N57 | §8 | with the defaults the energy balance holds to about 10⁻¹² | 8.21 × 10⁻¹³ (readout "8.2e−13") | verified |
| N58 | §9 | disc foreshortened to 50 %; streaks at 5 px per metre of air, 16 px dashes and 22 px gaps; trail of the last three seconds | `K = 0.5`, `AIRPX = 5`, `DASH = [16, 22]`; trail from i − 150 samples × 20 ms = 3 s | verified |
| N59 | §10 | above about 11 m/s nothing limits the power but the torque limit | At 11 m/s, c_p,max × P_wind = 1.97 MW (the page's 2 MW class). The model has no pitch, so only the torque cap acts. With "follow the wind" the cap is reached in steady wind at 12.8 m/s. | verified |
| N60 | §10 | wind varies across 80 m of rotor | 2R = 80 m | verified |
| N61 | Fig. 3 caption | compare Figure 3 of Fig. 9, where no arrow led back | `driven-oscillator.html` Figure 3: "There is no arrow back from x to F" | verified |

## Numerical method: note against code, line by line

| # | Note | Code | Verdict |
|---|---|---|---|
| M1 | RK4 advances ω and the controller's integral; the same steps carry E_gen, E_aero, E_wind, the air distance and θ | `solve()`: k1…k4 from `rates()` update `w` and `I`. `y[0..4]` integrate τ_gen·ω, τ_aero·ω, ½ρAv³, v, ω with the same weights. | verified |
| M2 | Start in balance: optimum speed (follow) or target speed with τ_gen = τ_aero (hold) | `w = lam_opt·wind(0)/R` or `c.wref`; `c.tau0 = tauAero(c.wref, wind(0,c))`; I = 0 | verified |
| M3 | Torque kept in [0, 1.2 MN m]; the integral stops while the torque sits at a limit | `tauGen` clamps; in `rates`, `dI = 0` when raw ≤ 0 with e < 0 or raw ≥ TMAX with e > 0. Integration into the limit stops; recovery is allowed. | verified |
| M4 | PI gains from ω_n, ζ_c and the aero slope at 15 rpm and 8 m/s | `dtd` is a central difference at (ω_ref, v₀) with δω = 10⁻⁴; `Kp = 2·ZC·WN·J + dtd`, `Ki = J·WN²` | verified |
| M5 | Every second state stored; playback shows the nearest stored row; blades at the stored θ | `step % EVERY === 0` stores; `frame()` uses `Math.round(playT/(EVERY·H))`; `drawScene` uses `th[i]` | verified |
| M6 | Energy balance (7) checked after every solve | `balance = \|y1 − y0 − (KE − KE0)\|/y1` | verified |
| M7 | Turbulence: 16 sines, 0.005–0.5 Hz, ∝ f^(−1/3), σ as set | As in N33/N34. The code also normalises by TNORM and clips v ≥ 0.5 m/s (not mentioned; never reached). | verified |
| M8 | Gust: "IEC shape" | `v0 − 0.37·dv·sin(3πs/10.5)(1 − cos(2πs/10.5))` for 0 ≤ s = t − 30 ≤ 10.5. This is eq. (4) of Shirzadeh et al. (2020) with T = 10.5 s, read in the PDF. | verified |
| M9 | Step wind: "step, +1.5 m/s at 30 s"; "after the wind steps up in the Step run" | `v0 + dv·min(1, max(0, (t − 30)/2))`: a **linear ramp from 30 s to 32 s**, not a step. It matters for the quoted response. With a modified copy using a true step at 30 s, the hold-speed overshoot is 0.42 rpm (peak 15.4189 at 31.82 s) instead of 0.39 rpm. The ramp's corners at 30 s and 32 s are also points where RK4 loses order, which section 8 does not mention. That does not affect the step-size study, which uses the smooth turbulent default. | wrong, because the code ramps the wind linearly by 1.5 m/s over 2 s (30 → 32 s) and the note describes an instantaneous step. Correct: "a 2 s ramp of +1.5 m/s starting at 30 s" (in the table row and in §6.2). |
| M10 | Drawing (section 9): foreshortening, burgundy blade at θ, streaks by ∫v dt, arrow length grows with v, strips dark/pale, rose P_aero curve, 3 s trail on the c_p chart | `drawScene`, `drawStrip`, `drawCp` as described (arrow `al = 6 + 3.2v`; ROSE curve of `Pa`; FAINT after i) | verified |

## References (links opened; chapters checked where possible)

| # | Reference | Road taken and result | Verdict |
|---|---|---|---|
| R1 | Burton et al., *Wind Energy Handbook*, 2nd ed., Wiley 2011, doi:10.1002/9781119992714, chapters 3 and 8 | curl: doi.org redirects to onlinelibrary.wiley.com, which answers 403 to curl (bot wall, not a dead link). The doi.org handle API maps the DOI to the Wiley book URL. Firecrawl opened the page (HTTP 200): "Wind Energy Handbook, Second Edition, 2011". Crossref chapter DOIs give ch. 3 "Aerodynamics of Horizontal Axis Wind Turbines", pp. 39–136; its section list on Wiley (via Firecrawl) begins "The actuator disc concept, Rotor disc theory…" and its references include Betz. Ch. 8 is "The Controller", pp. 475–523. | verified |
| R2 | Manwell, McGowan, Rogers, *Wind Energy Explained*, 2nd ed., Wiley 2009, doi:10.1002/9781119994367 | curl: 403 from Wiley, as in R1. Crossref: Wind Energy Explained, Manwell/McGowan/Rogers, issued 2009-12-18. Firecrawl opened the page (200): "This must-have second edition…". | verified |
| R3 | Heier, *Grid Integration of Wind Energy Conversion Systems*, Wiley 1998; LoC description link | curl: HTTP 200. The page is "Publisher description for … Grid integration of wind energy conversion systems / Siegfried Heier", LoC control number 98018157. | verified |
| R3b | Heier (1998) as the "source of the power-coefficient fit (5)" | The 1998 book is not openly accessible, so I could not read the formula in it. Tang et al. (arXiv:1004.0487, read in the PDF) give exactly (5) with c₆λ and these constants (their eqs. 27–28). They say it "is presented in [42]" (Heier 1998) "and also adopted in MATLAB/Simulink R2007a", with a maximum of 0.48 at (λ, β) = (8.1, 0). The MathWorks block page now returns 404. | unverifiable, because the primary source is not accessible; a secondary source supports the attribution |
| R4 | Shirzadeh, Hangan, Crawford, *Wind Energy Science* 5, 1755–1770 (2020), doi:10.5194/wes-5-1755-2020, eq. (4) | curl: 200 via wes.copernicus.org (open access). Crossref confirms the pages 1755–1770 and vol. 5. In the downloaded PDF, eq. (4) is U(t) = U_hub − 0.37U_gust sin(3πt/T)(1 − cos(2πt/T)) for 0 ≤ t ≤ T, with T = 10.5 s: the page's gust. | verified |

## Wrong rows

The four "wrong" rows (N9, N23, N30, M9) are in full in the tables above.

**Summary: 96 rows — 91 verified, 4 wrong (N9, N23, N30, M9), 1 unverifiable (R3b).**

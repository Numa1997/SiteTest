# Readability audit: Droplet Collection and Rotor Pendula

15 October 2026 · for Numa Koudsie

The two research projects now explain the difficult transitions more slowly, while keeping the chapter order, clear existing paragraphs, numbered equations, figures and expandable calculations. Their numerical models, solver code and stored result data were not changed by this revision.

The main route remains **physical picture → stated model → equation → interpretation → limit**. The aim is a reader with a bachelor's degree in physics who can follow mechanics and differential equations but has not studied cloud microphysics or turbine-mounted generators.

## Droplet Collection

The central distinction is between a particle's mass, the number of particles, and the total water held by a population. A merger removes two particles and adds one of their combined mass. Counting and weighing are different operations.

### From geometry to population evolution

The encounter kernel is an effective volume swept out per second, in m³/s. Concentration turns it into a rate:

| Quantity | Units | Physical reading |
|---|---|---|
| \(K\) | m³/s | Effective volume cleared by one collector per second |
| \(K\,n_r\,dr\) | s⁻¹ | Merger rate for one collector with that partner class |
| \(K\,n_R\,dR\,n_r\,dr\) | m⁻³ s⁻¹ | Events per air volume per second |

The new bridge explains why doubling one concentration doubles its event rate, while doubling both concentrations quadruples the number of pair events per volume. The kernel describes pair physics; it does not itself count available particles.

The population equation now has a three-mass example before its integral interpretation. An event \(m_0+2m_0\to3m_0\) changes the class counts by −1, −1 and +1. Number falls by one, while the weighted mass change is zero. The gain and loss integrals repeat that bookkeeping over every possible pair.

The jump expansion is motivated by collectors that catch at different times. The drift follows mean mass gain; the second term describes the spread left out by one smooth growth path.

### Mathematical repairs

1. **Encounter rate versus the whole kernel.** An excessive Stokes speed increases geometric encounters but can also suppress the adopted coalescence efficiency. A speed error is therefore not automatically the same multiplicative error in the full kernel. A larger cross-section alone also does not prove that radius growth is monotone.

2. **Trajectory approximation.** Linear Stokes drag implies the settling speed \(v_t=\tau_p g^*\). Replacing that speed with a fitted terminal speed while retaining the same relaxation time is an additional approximation. This is now stated where the dimensionless trajectory equation appears. The table-generating program is absent, so the revision does not claim to establish which convention produced the stored efficiencies.

3. **Collision closure.** The empirical flow blend is no longer called the only underived ingredient. Particle drag, shape and mutual airflow disturbance still require modelling even if the carrier flow is solved numerically.

4. **Mass-spread example.** With rates frozen at their initial values, one collector's standard deviation is \(\sqrt{Bt}\). The difference of two independent collectors has \(\sqrt{2Bt}\). The previous wording confused those quantities and treated the initial-rate estimate too much like a full growth prediction. The example now identifies both approximations.

5. **Golovin spectrum error.** The normalised absolute mismatch counts the deficit where mass left and the excess where it arrived. For equal total masses, moving a fraction \(f\) between disjoint regions gives \(\varepsilon=2f\). The stored \(\varepsilon=0.0511\) therefore corresponds to about 2.56% relocated mass under that interpretation, not 5.11%. The error values themselves are unchanged.

6. **Floating-point wording.** The large Stokes energy ratios are finite. It is the exponential coalescence factor that underflows to zero. The table now says which quantity loses floating-point resolution.

The threshold discussion also explains why a mass fraction can rise while particle number falls, and why a late decline can come from overflow rather than particle shrinkage.

## Rotor Pendula

The simplest physical picture is a driven oscillator viewed from the blade. Pivot acceleration supplies an outward restoring tendency, gravity supplies a push once per revolution, and the generator brakes the joint's motion relative to its housing.

### Reading the mechanics

The kinetic-energy cross terms now follow directly from squaring the sum of pivot and relative velocities. The Lagrange-equation gloss treats its inertial terms together and does not identify every conjugate momentum with angular momentum about a fixed point.

A horizontal-blade example checks the torque signs before changing frames: a rod tilted above the outward radial line receives a restoring pivot-acceleration torque, gravity pulls it downward, and the brake opposes its relative angular velocity.

The explanation of generator power follows both ends of the generator. Negative net mechanical power means absorption, not the earlier phrase “gives out less than nothing”.

### Mathematical repairs and qualifications

1. **Gravity and the energy ledger.** Returning to the same rotor phase does not require a chaotic bob to return to the same height. Gravity's work is minus the change in gravitational potential energy. That change belongs in the finite-window storage term. Its long-time mean contribution vanishes for bounded heights.

2. **What follows for turbine output.** At vanishing mean storage, the ideal rotor supplies the harvested mechanical power. With fixed aerodynamic input, this reduces what is available to the main generator. The study contains no blade-flow model from which to infer how an attachment changes aerodynamic capture.

3. **Small angle versus weak forcing.** Linearising only in angle leaves
\[
\varphi''+\kappa\varphi'+[R-G\sin\tau]\varphi=-G\cos\tau.
\]
The simpler driven-oscillator formula drops \(G\varphi\sin\tau\) by also treating the response as first order in weak forcing. A small angle alone does not justify that omission for arbitrary \(G\). The existing nonlinear acceptance checks remain the practical test for the studied cases.

4. **Damping optimum and resonance.** Away from \(R=1\), weak braking gives little extraction; strong braking suppresses speed; the optimum balances damping against stiffness minus inertia at the drive frequency. These contributions are in quadrature. At exact resonance the linear formula has no finite positive damping maximum, so the zero-damping steady-response limit must not be described as zero power.

5. **Geometry-only resonance.** The frequency-ratio argument is identified with the leading weak-forcing model. A change of rotor speed also changes dimensionless damping for a fixed physical generator; stronger forcing can change the response picture.

6. **Chaos.** A complicated trace is not the definition. The revised introduction explains exponential separation under the same forcing, and distinguishes it from transient separation or phase drift in regular motion. The sampled double-versus-single comparison is no longer phrased as a universal design theorem.

7. **Sensor range.** The strict guard \(\Gamma<7\) now follows from a strict gravity-only peak condition \(g(\Gamma+1)<8g\). Reaching the range is measurement saturation, not a structural survival test. Vibration needs a further quantified margin.

The shorter web report carries matching explanations of energy and linear response. Its introduction identifies it as a reading edition. The original downloadable PDF, LaTeX source and study archive remain the original study record.

## The ten shorter lecture notes

Their earlier selective audit is also implemented on the main website. The main changes are the distinction between mean-square displacement and string energy, a local rather than global turbine-stability argument, visible small-amplitude caveats, the limits of the bob-separation estimate, stationary pen versus cusp, the period after cancelling equal-frequency terms, and sampled versus continuous Fourier error.

Every simulation script, inline style and inline SVG was compared with the latest live baseline and preserved byte for byte. The latest live fixes already present in four pages were retained when bringing the repository up to date.

## Verification

- Both research apps build; existing dependencies were reused.
- Independent checks cover the absolute-error factor of two, the collector variance scale, finite energy ratios and exponential underflow, the damping optimum on both sides, the small-angle expansion and conservative gravity work.
- Nine droplet physics/data source files and six rotor physics/data source files match their pre-edit versions.
- Both solver worker bundles retain their existing hashes.
- Reading checks pass for both research apps locally and live, and for their rebuilt website copies: 18 route-and-viewport cases per run.
- Checks exercise chapter navigation, keyboard disclosure, maths remaining typeset after interaction, responsive equations, images and simulation presets.
- The main site's 13 pages pass at desktop and phone sizes, including all ten revised notes.

Historical claims about earlier reruns, primary-paper attributions and sensor datasheet specifications remain attributed study evidence. This revision did not repeat every historical experiment or re-audit every cited publication. The missing collision-table generator is an explicit reproducibility limit.

## Card interaction

The existing pattern is an **animated accordion**, also called an **expandable disclosure card**. Motion of neighbouring cards is a **layout transition**. The house layout and fold behaviour are preserved; the earlier isolated motion comparison remains available for choosing a later interaction refinement.

Deployment: both standalone research apps and the main website are ready. The platform reports one advisory about the main site’s existing 17 QA scenarios; review found distinct workflow coverage, which was retained. There are no reported runtime or network errors. The revised main-site files match the tested upload exactly.

## Independent audit of this revision, and its first repairs · 15–16 October 2026

The revision above was checked by three independent reviews: every physics repair re-derived from the apps' own code and
data, the research pages loaded 88 times and the website pages 26 times in headless Chromium at 1440 × 900 and 390 × 844.
Nothing a reader sees was broken, nothing was lost (equations, figures, tables and fold-outs counted before and after), and
every physics repair is correct. Eleven shortfalls were found; the first nine are repaired here, the last two wait for
Numa's reading of the wording.

| # | Where | What was wrong | Done |
|---|---|---|---|
| 1 | Rotor Pendula `#/report` | Two of Sol's sentences were rewritten in place and a paragraph was added without a mark, against the page's own convention of marked notes; `report.tex` still had Sol's words. | Sol's text restored word for word; the additions are three boxes marked *Reading note*, named in the lede and in the closing note (app v5, snapshot `1792108602425`). |
| 2 | Figs. 4, 8, 9 | A new paragraph was placed between a sentence ending in ":" or "," and the equation that completes it. | Moved after the equation ([Fig. 4 L137](../public/simulations/Transverse%20and%20longitudinal%20waves.html#L137), [Fig. 8 L305](../public/simulations/draw-decompose.html#L305), [Fig. 9 L217](../public/simulations/driven-oscillator.html#L217)). |
| 3 | Fig. 10 | "the linearised equation below": (10) is above. | "(10) above" ([L346](../public/simulations/wind-turbine.html#L346)). |
| 4 | Fig. 10 | The note concluded that no global convergence argument exists. The net torque $\tfrac12\rho\pi R^5\omega^2[c_p(\lambda)/\lambda^3 - c_{p,\max}/\lambda_\text{opt}^3]$ is positive for every $\lambda$ below $\lambda_\text{opt}$ and negative above it (grid of step $10^{-4}$ over the fit), although $c_p/\lambda^3$ rises between $\lambda = 2.4$ and $4.3$. | The sign argument replaces the two sentences ([L340](../public/simulations/wind-turbine.html#L340)). |
| 5 | this repository | The branch `codex/minor-issues-20261015` was cut before the audit repairs `32c240c`–`2c6a436`, so it reverted `datalog.js`, `data.css`, `portfolios.html` and the docs. | Three-way merge; the nine docs conflicts resolved by keeping the hash-linked notes and appending the added sections; `fig07-phasor-sums.md` re-based on the one-line shift of the inserted paragraph. |
| 6 | both copies | Built with KaTeX 0.16.11 while the apps use 0.16.47. The visible maths is the same; the hidden MathML differs in 134 formulas (10⁻¹² read as "1, 0⁻¹²") and multi-line equations shift by up to 10 px. | Rebuilt on 0.16.47 ([portfolios.md](portfolios.md)). |
| 7 | Droplet Collection ch. 4 and ch. 9 | "the two effects compete" is false for partners much smaller than the collector ($E_\text{coal}$ stays 0.995 at Stokes speeds); the reading of (56) proved $\varepsilon = 2f$ for disjoint regions only, while the Golovin spectra overlap. | Both sentences made exact: for equal totals the deficit and the excess are each $\varepsilon L/2$ (app v11, snapshot `1792108231309`). |
| 8 | QA scenarios | Rotor: the solver re-run test had lost its sanity flag. Droplet: two scenarios were merged with an ambiguous step order. Neither change was reported. | Flag restored; "Return to Theory" added to the step. |
| 9 | Rotor Pendula ch. 10 | The renamed heading was still a question. | "The accelerometer's range on the blade". |
| 10 | Figs. 3, 5, 9, 10; Rotor ch. 7 and 9 | Everyday pictures replaced by abstract wording: each photon interferes with itself; pressure cannot spin a parcel; a slow rotor lets the air slip between its blades; the leaves in calm water and in rapids. | Fixed on 16 October 2026 (next section). Evidence: [Fig. 3 L491](../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L491) (both slits for every single photon), [Fig. 5 L253](../public/simulations/water-wave.html#L253) (Kelvin), [Fig. 9 L167](../public/simulations/driven-oscillator.html#L167) (Millennium Bridge), [Fig. 10 L235](../public/simulations/wind-turbine.html#L235) ("almost like a solid wall"); Rotor ch. 9 "like money at compound interest" in `index-CsGEKbO8.js`. |
| 11 | Figs. 2, 8, 9; Droplet ch. 5, 7; Rotor ch. 3 | A garbled sentence, a run-on, $\varphi$ used before it is defined, $v_t$ used for the Stokes speed, a symbol clash on $f$. | Fixed on 16 October 2026 with item 10 (next section); for example the Stokes speed is written \(v_t^S\) in `index-DGIxitSc.js`. |

Also in the Rotor Theory: the angle-only linearisation in chapter 3's fold-out is now displayed as equation (18a), because
the inline form wrapped on a phone.

Checks after the repairs: the three Markdown link checks of this repository pass (4174 links, 0 bad; 81.6 % of backticked
identifiers land on their definition); the 13 website pages and the two copies' theory and report routes pass at both sizes
locally; both apps report no runtime or network errors.

## Second repairs: the pictures and the small slips · 16 October 2026

Items 10 and 11 of the table above, applied after Numa chose to have them done without a preview. Each everyday picture
that the revision had replaced is back, with the revision's precision kept beside it:

| Where | Restored | Kept from the revision |
|---|---|---|
| Fig. 3, Section 7 | every single photon needs both slits; closing a slit or recording the path removes the fringes ([L491](../public/simulations/Interactive%20Double-Slit%20Experiment%20Visualization.html#L491); the page does not use the words "interferes with itself") | the probability amplitude is not the classical field; counts per unit angle against per unit length on a flat screen (a factor 3/4 at 30°) |
| Fig. 5, Section 4 | pressure pushes through a parcel's centre and gravity pulls at it, so neither can spin it; Kelvin's circulation theorem by name | the theorem's three conditions: constant density, no viscosity, a force with a potential |
| Fig. 9, Section 1 | the Millennium Bridge, now as the counter-example: the walkers' steps fed back on the sway | the prescribed-force idealisation stated as such |
| Fig. 10, Section 3 | too slow lets the air through, too fast acts like a wall | the angle of attack as the mechanism behind both |
| Rotor Pendula ch. 07 | an arm with an elbow, the classic toy for chaos; "how much less, and why" | power only from the relative speed across a joint; "in the sampled cases" |
| Rotor Pendula ch. 09 | the leaves in a calm stream and in rapids; compound interest | the test under the same forcing; $\Lambda$ in 1/s; transient growth and phase drift in regular motion |

The small slips. Fig. 2's Lyapunov paragraphs: the limit defines the exponent and the rescaling algorithm computes it; the
1.7 s⁻¹ is a finite-time estimate from two of the four coordinates; the energy sentence is back, with why a small drift
proves only the integrator. Fig. 1's opening in plain words, and the $kr \gg 1$ caveat with the size of its first correction
(a phase lag of $1/(8kr)$, 0.01 rad two wavelengths from a source). Fig. 6's sharp corners. The garbled sentence of Fig. 8
and the run-on of Fig. 9. Droplet Collection (v12, `1792111079794`): the Stokes speed written $v_t^S$ as in (10); the
spread example in numbers ($\sqrt2 \times 3.7 \times 10^{-11}$ kg $= 5.3 \times 10^{-11}$ kg, 19 %); the three-mass example after
the one-half paragraph, with the pair counted twice in the gain integral; the $W_E$ column in numbers and the underflow
threshold ($W_E > 648$, collectors from 0.8 mm); pointers to (8), (35) and the top-edge section; the $R^2$ cancellation
behind $\dot R$. Rotor Pendula (v6, `1792111084380`): the sign check placed after the paragraph that names the three
torques and written in $\theta$; plain glosses for the conjugate momentum, $\varphi = O(G)$, quadrature and the
non-uniform limit; the lead-in to (11) naming all four numbers; the ±8 g headroom in numbers (2.0 g to 5.6 g at the six
of the 18 mountings that pass, from `study.json`). Website v64 (`1792111100165`) carries the eight notes and the copies
rebuilt from these pages (`index-DGIxitSc.js`, `index-CsGEKbO8.js`).

Checks: the 13 pages and the copies' theory and report routes clean in Chromium at 1440 × 900 and 390 × 844, locally
and live; both apps without runtime or network errors; the three link checks of this repository pass.

## Lecture notes · 20 October 2026

Numa found the ten lecture notes "not readable or understandable, not theoretically sophisticated or up to standard", then set
the rule for the work: judge first, offer proper derivations and relaxed, Feynman-like explanations only where needed, and
never overload the simulations ([notes/STANDARD.md](../notes/STANDARD.md)). A team of agents did the work
([notes.md](notes.md)): for each note a teacher judged every section and repaired only those judged "needs work"; the lead read
every changed paragraph; then a derivation checker, a blind referee and a walkthrough checker worked independently, and the
lead made a second repair round from their reports. No page code, shared script, style or walkthrough file changed: every page
is byte-identical to `db1a24b` outside `<article id="paper">`. Equation numbers are unchanged (Fig. 9 adds one, tagged (6a)).

In the teachers' verdict tables (sections, their parts and the abstracts, counted in `notes/STATUS.md`), 59 parts were judged clear and left alone and 52 needed work. The common faults were derivation steps asserted
rather than shown, symbols used before their definition, a few wrong claims and numbers, numerical-method descriptions that
did not say what error to expect, and reading lists without a single link (37 references, none linked).

| Fig. | What was wrong (examples) | What the note does now | Verified |
|---|---|---|---|
| 1 | "The pattern moves as one ring does" (§4): true of each ring, not of the summed crests; "the damping factors are all the same" (§6), false for γ > 0 | each ring at v, crests of the sum faster where rings cross (1.55 v up the middle, measured); the row derived at γ = 0, the damping effect bounded (≤ 0.03 at the default γ); 5 references linked | teacher's float64 recomputation and Chromium measurement |
| 2 | Lyapunov rate "1.7 per second" read off no curve; energy "fixed to one part in ten million" with no time limit; pixel formula adding metres to pixels; no word on where RK4 fails | fitted 1.4 and a full calculation of 1.45 per second; the energy claim for the first 20 s, with the slow creep and the heavy-bob failure measured; σ-based pixel formulas; four wide equations reflowed; references linked | teacher's SymPy, Node runs of the page's own `rk4`, Chromium |
| 3 | θ undefined and the cross term never written (§5); "closing one slit gives the sum of two single-slit patterns" (§7); polarisation "changes nothing for small angles" (§10); 67.5 px fringe spacing where the page shows 72 px | θ and the cross term defined; one slit gives one single-slit pattern; polarisation measured (0.9 % residual at the dark fringe); small-angle estimate vs exact 72 px; references linked, Young 1804 added | checker: 119 verified, 0 wrong; blind referee |
| 4 | A_L used before definition; Exercise 3.1 false for the lower row; B = γp and K + 4G/3 asserted; air density 1.2041 for 1.2043; Exercise 5.1 "bars nearly touch" | each derived in a sentence or two; the exercise corrected; the "new medium" point made where the speed doubles; overloaded caveat and ⁴⁄₃G sentence trimmed; references linked | teacher's SymPy and Chromium; blind referee |
| 5 | symbols used before definition in §02; c_g = dω/dk asserted; surface points said to be stored; Stokes-drift picture explained half of (21) | two-wave derivation of the group velocity; storage claim corrected; both halves of the drift picture; references linked | teacher's SymPy and RK4; blind referee |
| 6 | the second-derivative sign; group velocity "describes a narrow envelope"; string energy asserted; "true corners" cost infinite energy (it is the jumps); a sine count | each corrected or derived; the cosine-rule sign explained; the one-term Gibbs overshoot on the table's basis; references linked | checker: 79 verified, 3 wrong, all 3 fixed; blind referee |
| 7 | "gcd" defined after unrelated text; beat "at half the difference rate" next to a full-rate period; petal rule and cosine-law sign unexplained; "not curves any set of phasors would draw" (false) | each fixed in a clause; Record timing as the code does it (58 ms); references linked | teacher's Node runs of `sumAt()`; blind referee |
| 8 | the inverse DFT step skipped; Figure 3 caption gave the wrong reason; §5 relied on the ★ section the abstract says can be skipped | the step written; the caption measured; §5 recalls the two facts it uses; references linked | teacher's Node runs of the page's `resamp`/`dft`; blind referee |
| 9 | amplitude and phase, roots, constants, Ω_r and the ζ ≥ 1/√2 claim asserted; pole real part "1/τ"; Exercise 6.1 wrong; the window chart not described | each derived (Ω_r by completing the square, (6a)); sign and exercise corrected; the per-run drawing scale and the ruler said in words; Figure 3's label fits its box; references linked | teacher's SymPy and Chromium; blind referee |
| 10 | ω, R, ρ undefined; the Bernoulli step of the Betz derivation asserted; why c_p depends on λ alone; ω*, τ₀ and the PI linearisation skipped; "without ringing" false (0.40 rpm overshoot); no RK4 error estimate | each defined or derived; step-size study h = 5 / 20 ms (ratio 16, fourth order); two wide equations reflowed; references linked | teacher's Node runs of the page's `cp()`/`tauAero()`, Chromium |

Checks after the repairs, all passing: [notes/verify.mjs](../notes/verify.mjs) (ten pages at 1440 × 900 and 390 × 844: no
console or KaTeX errors, no sideways scroll, every fold opens, no display equation wider than its box at 1440 px);
[notes/walkcheck.cjs](../notes/walkcheck.cjs) (226 of 226 quoted code lines found verbatim); `tools/inventory.py --check`.

Open on 20 October 2026, 17:00 UTC:
- The derivation checks of Figs. 1, 2, 4, 5, 7, 8, 9, 10 and the blind referees of Figs. 1, 2, 10 stopped when the account's
  usage limit was reached; they resume after it resets. Until then those notes are verified by their teachers' own
  computations only.
- Walkthrough fixes: every walkthrough quotes its page exactly, but several use other symbols than the repaired notes (for
  example Fig. 8's step 3 writes `a + ib` where the note uses a for an angle; Fig. 10's step 4 still says "without ringing").
  The exact old → new text is in `notes/figNN/walk.md`; walkthrough files change only with Numa's permission.
- Code findings, reported and not fixed: Fig. 2 `drift.toExponential(1).replace('-', '−')` replaces only the first hyphen
  (L639, L691, L693); Fig. 5 stores `cg = c/2` also with dispersion off (L663); Fig. 7 Record snapshots come 58 ms apart, not
  50 (`recAcc = 0`, L1189), and replay does not wrap phases (L1205); Fig. 8 `resamp()` samples a closed shape's start point
  twice; Fig. 9 the last time-tick label can overlap "t (s)" (L783); Fig. 10 Play after 120 s does nothing (L962); Figs. 4, 9, 10
  redraw every frame while paused; Fig. 3 "Animate wavelets" starts ticked while the clock may start paused.

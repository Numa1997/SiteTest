# Plan: section 11 of the Kaggle note, "Holding the stout still: the controllers" (13 November 2026)

Page: `public/simulations/guinness-kaggle.html`, only inside `<article class="paper" id="paper">`. Doc: the Kaggle part of
`docs/simulations/fig12-beer-slosh.md` (the section table of the note). Standard: `notes/STANDARD.md`, verdict of 21 October 2026
(Taylor's *Classical Mechanics*: every step shown, symbols defined where they first appear, Key result boxes, numbered worked
examples with the page's numbers, Problems at the end, ★ on the heavy parts with their results restated). Numa said "Please do"
to control in the GPU loop; run 7 (joint control on the three roads of run 6, slosh LQR and preview on the kerb) is computing and
its data are not available: the results part gives its method and one paragraph marked `<!-- RESULTS-RUN7 -->`.

The code is the truth: `tools/fig12/kaggle/stout_jax.py` (`Cart`, `slosh_lqr`, `susp_lqr`, `observer_design`), a line-by-line
port of `Cart.sample`, `Cart.lqrGains`, `Cart.suspGains` and `Observer` in `public/scripts/stout-cart.js` (lines 1438–1785);
`run_b.py` (`PLANT`, `TASKS_CONTROL`). Built on, not copied: the Fig. 12 note §§ 7, 8.1–8.6, 9 and the brief
`notes/fig12/handoff-control-session.md` §§ 4.3, 4.4, 11.

Renumbering: "Limits, and the next model" becomes 12, "Sources" 13; contents list, section 1's road map, section 10's pointer to
the head's inertia, Problems 11.x → 12.x; the "next model" paragraph of the limits now points back to section 11 and names
what comes after it. Abstract: one clause on control. Section 9: one sentence on the two new readings (motor current, active
suspension force) that the other session added to the page.

## The section, part by part

11 lead. A waiter with a full tray: he keeps an even pace, eases into a step he sees coming, moves his hand against the
drink's rocking, bends his knees at the kerb, and still cannot stop a tray from jolting when somebody bumps into him.

11.1 **Four tricks, four controllers.** The picture mapped onto the cart: speed PI (what run 6 used), road preview, slosh LQR on
a Kalman estimate, joint design (slosh LQR + heave cancellation + suspension LQR). Table 5: what each reads, what it commands.

11.2 **How hard the motor can push.** The cart along the road, M_x v' = b i − c_x v + F_d; the current's limits (±3 A; the
supply 12 V less the back-EMF b v over R_a = 2 Ω; the 2 ms lag; the tyre's grip μN). Example: M_x with stout and head, b I_max,
the largest acceleration; at 1.5 m/s the supply allows only 2.25 A forward. The kerb against the motor (cart alone, frozen
pint, PI): the road's push −N z_a′ peaks at 82 N because the tyre load rises to 105 N while the wheel climbs a slope of 0.785;
it brakes for 44 ms; the wheel then leaves the road six times in 0.17 s (92 ms in the air), when the motor can push nothing.
The best the motor could do (forward at its limit through the climb) still loses 0.25 m/s. Figure 4 (inline SVG from the
cart's own series). Key result: what no controller with this motor can prevent.

11.3 **Keeping the pace: the speed loop.** PI law, gains from crossover 8 Hz and a double pole; designed for M_x without the head
(2.505 kg), so with the head the crossover is 7.92 Hz; poles; anti-windup by conditional integration; the sensitivity at the
swing's frequency, |S| = 0.400 (0.409 with the lag and the half-sample delay).

11.4 **Looking ahead: the road preview.** Why one current lag ahead (a first-order lag delays a slow signal by τ_i), why the
static tyre load; the command. Example: on the kerb the preview asks 3.47 A from the static load where the road pushes with
82 N, 16 A worth.

11.5 **Watching the stout: the slosh regulator ★.** State (Δv, q, q′, ξ), A and B derived from (6) and (21); the LQR cost,
Bryson's rule, the Riccati equation, K = Bᵀ P/r; check: the integral gain is exactly √(Q₄₄/r) = 150 A/m (the fourth column of
A is zero); the gains with the full glass; the plant is the solver's own measured mode (3.278 Hz, ζ 0.467, β 1.541): World's
rule in `stout-cart.js`; the poles before (−9.62 ± 18.21j) and after (−12.40 ± 6.49j), against the bare stout (−0.23 → −12.0);
Key result: the head has already done most of the controller's work.

11.6 **Seeing the swing: probes and a Kalman filter ★.** The sensors (encoder every 1 ms, probes' half difference once per
fluid step, the measured current as input; no noise added); the one-number blend; the model (v, q, q′) with the noise
intensities; exact zero-order hold and Van Loan's Q_d; predict and correct with Joseph's form; the settled gains with a probe
every second sample; worked example (a speed surprise read as a swing); the separation principle; the sampled loop as one
system is stable (largest multiplier 0.9949 per 2 ms).

11.7 **The heave, and the joint design ★.** The cancellation current derived from (6) under vertical acceleration; the filter's
stiffness ω²(1 + a_z/g); with the head the parametric threshold is 1.89 g (Floquet), so the heave cannot pump this swing; the
suspension's LQR with the cross term, its weights, gains for the load the rides start with, and poles.

11.8 **Every limit, every clock, and the check of the port.** Table 6. The port check of `tools/fig12/kaggle/portcheck/`
(run again here, same output).

11.9 **What we expect, and how the controlled rides are read.** Predictions of the one-mode model (the controller's own plant
coupled both ways to the cart of the code, the probes read once per 2 ms step as in `make_advance`) under each controller on
each road (Table 7), checked against run 6 under the speed loop; the method of reading run 7; run 6's baseline from its stored
files; one paragraph with `<!-- RESULTS-RUN7 -->`.

Problems added to the Problems box of section 12: the integral gain √(Q₄₄/r); the cancellation current; the preview's lag.

## The numbers, and how each is measured (scratch scripts in the session's scratchpad; nothing added to the repository)

| Number | How |
|---|---|
| load 454.4 g (stout 429.58 g, head 24.83 g) | `Geometry` and `Stout` of `stout_jax.py` at 1.5 mm, `ride_extra`'s formula |
| M_x 2.529 kg (2.505 kg without the head), b = 5 N/A, 15 N, 5.93 m/s², 2.25 A at 1.5 m/s, μN₀ 17.7 N | `CART_COMMON`, `Cart.massX`, `Cart.forces` |
| K_p, K_i, PI poles, crossover with the head, \|S\| at 3.278 Hz | from `CART_COMMON`; `numpy.roots`; S = 1/(1 + L) with and without lag and half-sample delay |
| K, open- and closed-loop poles, the other plants' gains | `slosh_lqr` (SciPy's CARE), `numpy.linalg.eigvals(A − BK)` |
| K_s, its poles, 84 % of the spring | `susp_lqr`, eigenvalues |
| A_d, B_d, Q_d, the settled 2-periodic Kalman gains and standard deviations | `observer_design`, the filter's recursion iterated 20 000 samples |
| the sampled loop's multipliers and poles | the 1 ms map of (plant with lag, integral, filter, held current) composed over 2 ms |
| Floquet threshold of the heave with ζ = 0.467, 0.016, 0.0107 | SciPy `solve_ivp` monodromy, `brentq`, minimum over Ω |
| the kerb: road force, braking time, airborne time, speeds | `Cart` alone (F = 0), 0.1 ms sub-steps, PI; a subclass that commands full forward current one 2τ_i ahead of the climb; the bound with the motor at its limit and no lag |
| preview command on each road | `road_table`, (M_s + m_w) g max z_a′/b |
| one-mode predictions (lean, current, frames at the limit) | `Cart` coupled to the one-mode plant (exact step over 2 ms, F = −d(P_c q′)/dt, P_c = ρπR³/ξ²) |
| port check | `tools/fig12/kaggle/portcheck/cart_jax.py` run from a scratch copy (same output as `portcheck.txt`) |
| run 6's largest current and frames at the limit | the stored `i` and `v` of `public/data/fig12/2026-11-13/ride_*.json` |
| the note in a browser | `npm run build`; headless Chromium (Playwright): KaTeX errors, equation order, sideways scroll, console errors at 390 and 1440 px |

Sources to open and cite: Åström and Murray, *Feedback Systems* (2nd ed., v3.1.5 PDF): §7.4, §7.5, Exercise 7.16, §8.3, §8.4,
§11.4, §12.4; Kalman (1960), Theorem 3; Van Loan (1978), if an open copy can be reached; the Fig. 12 note.

# Rotor Pendula lecture notes: revision of 30 October 2026

Aim: a reader with a bachelor's in physics reads the nine chapters start to finish and finds nothing foreign. Branch
`rotor-notes-revision`. Only `portfolios-src/rotor-pendula/theory/`, the notes' build output, this folder and the docs that
describe the notes change; the simulation and wind pages, stylesheets and every other page stay as they are.

## Fixed constraints
- **Equation numbers stay.** `rotor_sim.html` and `rotor_wind.html` cite (1.2)–(7.1) by number and may not be edited, so no
  existing number moves. New displays are unnumbered.
- **Section and chapter numbers stay** for the same reason (the pages cite sections 1.1, 2.2, 2.3, 4.3; chapters 2, 6).
- **Figures** are numbered at build time in caption order; no page outside the notes cites a figure number, so new figures may be
  inserted. Every new figure is inline SVG in the notes' existing drawing style.
- **Every number** comes from `numbers.json` or is listed in `tools/typed_numbers.py`; `tools/check_numbers.py` enforces it.
- **Every added step of algebra** is checked in `derive/R_revision.py` (SymPy, 47 checks, all PASS).

## Diagnosis, chapter by chapter (where a BSc graduate stops, and the fix)

### 1 · A double pendulum whose first arm the wind turns
Judgment: clear and complete in most places; the Lagrangian derivation is shown term by term.
- 1.2, the brake: "Rayleigh's dissipation function" and the generalized force $Q_q$ arrive with no definition. A BSc course
  often stops at conservative Lagrangians. **Fix:** one paragraph: virtual work of the brake torque, $\delta W = -c\dot\theta\,\delta\theta$,
  so $Q_\theta = -c\dot\theta$, $Q_\varphi = 0$; $\mathcal F$ is the shorthand whose velocity-derivative gives that.
- 1.3, (1.7): "$\sum\dot q\,\partial\mathcal L/\partial\dot q - \mathcal L = E$ and $dE/dt = \dots$" skips the differentiation.
  **Fix:** the one-line differentiation (the $\ddot q$ terms cancel), then Lagrange's equations put in. Checked (1.3 in R_revision).
- 1.4: "the $R - 1$ of chapter 3" is a forward reference with no reason. **Fix:** half a sentence: shaking at once per turn costs
  the inertia one unit of stiffness.

### 2 · Riding at the tip
- 2.2: the acceleration in the turning frame is stated after "differentiating once more"; the reader has to recall Taylor ch. 9.
  **Fix:** the two differentiations written out, with $(d/dt)_{\rm ground} = (d/dt)_{\rm turning} + \boldsymbol\omega\times$.
- 2.2: the torques are listed for the centrifugal, Coriolis and Euler forces but gravity's is only described in words, and the
  text never adds them up to recover (1.6). **Fix:** gravity's torque line, and one display: the hinge is at rest in the turning
  frame, so $I\ddot\theta$ = sum of torques, which is (1.6).
- 2.2: "$\sin|\theta_b|_{\max} = 1/\Gamma$" jumps from $\sin\varphi = 1/\Gamma$. **Fix:** the substitution shown.
- 2.3: the "puzzle" (gravity pays in one frame, the rotor in the other) is argued in words only. **Fix:** the energy balance in the
  turning frame as a display, $\frac{d}{dt}[\tfrac12I\dot\theta^2 - \tfrac{ml}{2}r_p\Omega^2\cos\theta] = -\tfrac{ml}{2}g\cos(\varphi+\theta)\dot\theta - c\dot\theta^2$;
  chapter 9's ceiling (9.1) then rests on it. Checked (2.3).

### 3 · The best brake
Judgment: clear; the triangle-and-Thales argument is a good picture. One gap:
- 3.1: "it gives a push that is partly steady and partly twice per turn" is asserted. **Fix:** the product-to-sum line. Checked (3.1).

### 4 · Big swings, and the bill
- 4.1: "three-stage Radau IIA" is named with no definition; a computational physicist wants to know what the method does and why
  it suits a stiff equation. **Fix:** a short paragraph: implicit Runge–Kutta, three stages at the Radau points, exact quadrature to
  degree 4, order 5, stability function $R(z)$ with $R(z)\to 0$ as $z\to-\infty$ (L-stable: a fast mode is wiped out in one step, not
  reflected). Checked (4.1).
- 4.2: "pulls on the hinge along the line from the hub to its centre of mass … that line misses the hub" is self-contradictory as
  written (a line from the hub passes through the hub). **Fix:** the pull has the direction of the hub-to-centre-of-mass line and acts at
  the hinge; its line of action through the hinge misses the hub by $\approx\tfrac l2\sin\theta$. Checked (4.2).

### 5 · From swing to watts
Judgment: clear; the chain of losses is followed step by step. Missing picture:
- **Fix:** a new figure of the drive chain (second blade, gearhead $N$, $\eta$, friction; motor $k_t = k_e$, $R_c$, $J$; load $R_L$),
  with what each link does to torque, speed and power, before section 5.1's formulas.

### 6 · The wind
- 6.2: the thrust is taken from momentum and the disc speed from an energy argument; the reader is told Bernoulli "gives the same"
  but not shown. Bernoulli is the route most BSc courses teach (Froude's actuator disc). **Fix:** the two Bernoulli lines and the
  pressure jump, giving the same $v(1-a) = (v + v_{\rm w})/2$. Checked (6.2).
- 6.4: "independent complex numbers $\xi_q$ of unit variance" is ambiguous. **Fix:** $\xi = (a + ib)/\sqrt2$, $a$, $b$ standard normal,
  as `L6_wind.py` draws them, and why the factor 2 under the root gives the variance $S\,\Delta f$.
- 6.5: "the rotor settles there by itself" is asserted. **Fix:** $Q_{\rm aero} = \tfrac12\rho\pi r^5(C_p/\lambda^3)\Omega^2$ at fixed
  $\lambda$, and the stability argument: $C_p/\lambda^3$ falls with $\lambda$ near the peak, so a rotor that runs fast meets more generator
  torque than wind torque and slows. Checked (6.5).

### 7 · The air on the second blade
- 7.1: "Reynolds number" used without definition. **Fix:** $Re = \rho W d/\mu$, the ratio of inertial to viscous stresses, with the
  air's viscosity that `L5_air.py` uses.
- 7.2: "the spring becomes $R/\cos\theta_s$" and "$c^2 + s^2$" are asserted. **Fix:** the linearisation about the lean (one line)
  and the reason pushes a quarter turn apart add in quadrature (chapter 3's turning arrows). Checked (7.2).
- 7.2: the letters $c$ and $s$ clash with the brake $c$ and the distance $s$. **Fix:** renamed $A_c$, $A_s$.
- 7.5: "stall" used without definition. **Fix:** a clause.
- **Fix:** a new figure of the forces on the second blade in the rotor's plane (drag back, lift's small forward part, the steady lean
  where the air's torque and the outward pull's balance).

### 8 · A blade that bends and shakes
- 8.1: the tilt of the stator is the crux of the section and is given in two terse sentences. **Fix:** the derivation: with the
  absolute angle $\psi = \theta + \beta$, the brake acting on $\dot\theta$, and $\beta'' = -\beta$, the tilt adds the push $-(R-1)\beta$.
  Checked (8.1). **Fix:** a new figure of the bent tip: the sag $w$, the slope $\beta$, the stator tilted with the section, the
  outward pull's line through the shifted hinge.
- 8.3: "by Cauchy–Schwarz twice": the first equality $b^{\mathsf T}\mathsf M^{-1}b = \max(b\cdot\dot q)^2/(\dot q^{\mathsf T}\mathsf M\dot q)$
  is not obvious. **Fix:** one line: Cauchy–Schwarz in the inner product defined by $\mathsf M$, equality at $\dot q = \mathsf M^{-1}b$. Checked (8.3).

### 9 · The answer
- 9.1: "gravity is the only force that can feed the swing on average" now points to the balance written out in section 2.3.

## What is deliberately not changed
The voice, the structure of every chapter (picture, idea boxes, derivation, "On our blade", remember, problems) and every result.
Sections judged clear are not reworded (Numa's rule of 20 October 2026: no overkill), apart from the fixes above.

## The blind read (30 October 2026)
One independent reader (a subagent given only the built notes as text, with numbers filled in, and the 20 figures as images; never
this plan) read all nine chapters as a BSc graduate and marked 36 places. It re-derived (1.1)–(8.4) and found no algebraic error.
What was done with each (✔ fixed, ○ left, with the reason):

1. Figure numbers in the text off by one or two. ○ An artifact of the text export made for the reader (it counted text references
   as captions). The built page numbers its 20 captions 1–20 in order and every reference matches (checked in `rotor_notes.html`).
2. "bowl", "hilltop", κ* used in 1.4 before 1.5. ✔ Defined where first used, κ* with a pointer to chapter 3.
3. The R − 1 sentence of 1.4. ○ Rewritten in the first pass; it now names the reason (θ'' = −θ) and points to chapter 3.
4. Light brakes forget faster than the best one (Table 1). ✔ One sentence: the best brake is ~5× critical, slow root ≈ −R/κ*.
5. Figure 5 caption "above Γ ≈ 3.6" against 6 m/s (Γ = 3.32). ○ The caption is written by `tools/make_numbers.py`; reported, not changed.
6. Radians to metres in the 14.4 s horizon. ✔ Stated: 1e-9 rad on a 1 m rod is 1e-9 m.
7. Time near the top. ✔ Derived from x = x_min cosh(√A(φ−φ0)); the 0.1 and 0.26 turns named as whole periods.
8. Action to amplitude needs elliptic integrals. ✔ J = (8√A/π)[E(k) − (1−k²)K(k)], k = sin(a/2), with both limits; checked in R_revision.py.
9. Swing picture contradicted experience. ✔ Rewritten: a still palm the swing bounces off (in step with position) against a push that follows it.
10. Why the rocking term is second order. ✔ Rewritten: lean and wobble of size GΘ/R; second pass gives a fraction (G/R)² ≈ Θ² of the swing; the lean named as chapter 4's trail.
11. Symbols with several meanings. ✔ Complex amplitude in (3.2) renamed θ̂; ψ of 8.1 renamed χ; Veers' random numbers X_q, Y_q; the gust
    component v flagged. ○ A (bowl stiffness, disc area), L, a, f stay: each lives in its own chapter and is defined there.
12. Battery analogy against the real generator's wiring. ✔ A note on the mapping (resistance to motion, not R_L).
13. "what remains … rms". ✔ Said what it is.
14. "parts that average to zero". ✔ Points to the exact torque derived above it.
15. j not divided by η in (5.4). ✔ Said why (estimate; j ≪ R − 1; the full (5.8) charges it).
16. Rotor pays more than P* at 6 m/s. ✔ Explained by j lowering the net stiffness, about j/(R−1).
17. "three brakes tried". ✔ Named: half, the formula's, twice (as `L4_check.py` runs them).
18. Dips in Table 4's shares. ○ Left; they come from the discrete catalogue ratios and the torque limit. Reported.
19. "311 times" not in a table; Θ* without its wind. ✔ Named the case (lightest blade, 10 m/s) and the wind.
20. Promise to explain λ* = 7.55. ✔ Promise reworded; the 7.55 and 7.64 peaks reconciled (same flat top, two calculations; 7.48 was already explained).
21. Betz side pressure argument circular. ✔ Stated as the model's assumption, with the condition under which it holds.
22. Figure 17's caption names the 256 s record before the text. ○ Caption from `make_numbers.py`; reported.
23. Which torque law the first wander belongs to. ✔ "Under the turbine's real torque law".
24. Where 205 mW comes from. ✔ The same solver in steady sheared wind.
25. Euler torque estimate. ✔ Measured by solving each run with and without the term.
26. Two dynamic pressures. ✔ Remark added.
27. (7.2) not reproducible. ✔ A_c and A_s written out, gravity's parts included, which air torque is which; verified: the formula
    gives −23.6, −2.0, +43.8 % from `data/L5_air.json`, identical to the script.
28. "its lean on its own would help". ✔ Wrong as written; replaced: a lean alone only turns gravity's arrow.
29. F_t held fixed in the stiffness. ✔ Stated, with the reason.
30. Half a degree of extra lean. ✔ Replaced with the trail's 0.42° accounting for more than half of the difference.
31. Which lift term drives the gust gain. ✔ Both named; the W C_L term (lift turning forward) is the larger for the wing.
32. Sag sign convention. ✔ Stated once, at the first display.
33. Tip slope not given. ✔ The mode's tilt per metre of tip motion quoted where the tilt enters.
34. 8.2's equations not given. ✔ Said where they are (`L3_shake2.py`) and that the notes give model and results only.
35. Equality claim in 8.3 wrong for point masses. ✔ Corrected (a rod never; point masses hanging straight can).
36. (9.1) with a gearbox. ✔ Why it still holds in the turning frame.

After the fixes: `check_numbers.py` PASS, `R_revision.py` 40 checks PASS (47 after the second pass), `check_physics.py` ALL PASS, `check_combined.py` ALL PASS,
headless Chromium at 1440 × 900 and 390 × 844: 20 figures, 97 displays, 0 KaTeX errors, 0 console errors, no sideways scroll.

## Second pass (30 October 2026, later): derive what was only stated
Asked again for a script a BSc graduate reads with nothing foreign to the eye. The first pass filled missing steps; this pass
derives what was still only stated or cited:
- 1.5: the adiabatic invariant derived (★): average dE/dφ over one swing, use ∂H/∂λ = −(∂H/∂p)(∂p/∂λ) on the orbit, get
  d/dφ ∮p dθ = 0; where slowness enters, and why it fails near the hilltop.
- 6.4: Kolmogorov's −5/3 from dimensions (the coffee-cup cascade, ε in W/kg, E(k) = C ε^{2/3} k^{−5/3}), carried to f by
  Taylor's frozen turbulence; why the spectrum is flat below the large eddies.
- 8.2: the vibration model's two linear equations written out (blade mode x, second blade χ, stator tilt β = Φ'x) and read term
  by term; the same two hinge terms as the sag of 8.1; the Coriolis terms cancel at this order; the power integral.
- Items left open by the first blind read: Figure 4's caption now takes its Γ values from the data (the 6 m/s run at Γ = 3.32 and
  the sweep's neighbours), Figure 17's caption no longer leans on later text, Table 4's uneven shares explained (catalogue ratios),
  and `teaching/export_notes.py` numbers figures as the build does.
`derive/R_revision.py` now holds 47 SymPy checks, all PASS (new: Kolmogorov's exponents, the adiabatic identity and the harmonic
action, the 8.2 equations re-derived from `L3_shake2.py`'s Lagrangian with no first-derivative terms).

Coordination: another session works on the animations at the same time. This branch touches the notes' sources, their build output,
the shared generated page `public/portfolios/rotor-pendula/index.html`, `docs/portfolios.md` and `docs/files.md`. Before each push the
branch is checked against `origin/main`; if `main` has moved, the commits are rebased and the generated files are rebuilt with the
study's scripts, never merged by hand.

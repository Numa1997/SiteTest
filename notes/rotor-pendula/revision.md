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
- **Every added step of algebra** is checked in `derive/R_revision.py` (SymPy, 32 checks, all PASS).

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

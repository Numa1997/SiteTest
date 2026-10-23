# Contract L0: single pendulum, uniform rotation, small swing, gravity drive

Gate 1 contract (physics-model-loop 7.1). Derivations: `derive/L0_single.py` (SymPy, 7 PASS), numbers: `derive/L0_table.py`
(6 PASS), scales: `derive/scales.py`. Gravity g = 9.80665 m/s² (standard gravity, as Sol). Round 1, 23 October 2026.

## 1. Question and observable

A bob of mass m = 0.1 kg on a massless rod of length L = 0.2 m hangs from a pivot fixed to a wind-turbine blade at distance
r_p from the hub axis. The rotor plane is vertical and turns at constant angular speed Ω. A generator whose stator is fixed to
the blade brakes the rod's rotation relative to the blade. **Observable:** the mean mechanical power P̄ the generator takes
from the swing in the steady state, averaged over one turn, as a function of the generator constant c; its maximum P* and the
c that gives it. Secondary: the swing amplitude Θ, the peak generator torque, and who pays (the rotor torque).

## 2. Picture and formal mechanism

**Picture.** Sit on the blade and turn with it. You feel a strong pull outwards along the blade (the centrifugal pull,
Ω² r_p per unit mass, 1.4 to 215 times g on the 18 mountings) and a weaker pull of gravity that, seen from the blade, turns
round once per turn. The rod lies along the blade like a weathervane in a steady wind; gravity leans on it, first to one side,
then the other, once per turn: a child on a swing pushed once per pass, by a hand that cannot be refused. The generator is a
spoon in honey at the pivot: it takes energy only while the rod moves relative to the blade.

**Formal mechanism.** Hamilton's principle for the bob with the rotor angle φ(t) imposed (a rheonomic constraint), plus
Rayleigh's dissipation function F = ½ c θ̇² for the generator. With φ as the clock (blade-angle time, ′ = d/dφ):

  θ″ + κ θ′ + R sin θ + G cos(φ + θ) = 0,   R = r_p/L,  G = g/(Ω² L),  κ = c/(m L² Ω)        (L0.3, ε = 0)

R is the centrifugal stiffness (the pendulum's own frequency is √R per turn), G is gravity's push, κ the generator. Small
swings, parametric term dropped: a driven damped oscillator at forcing frequency 1 and natural frequency √R. Its mean power
P̂ = κ⟨θ′²⟩ = κG²/(2[(R−1)² + κ²]) (in units of m L² Ω³) is largest at κ* = |R − 1|, where

  P* = m L g² / (4 Ω |r_p − L|),   Θ* = G/(√2 |R − 1|),   peak torque c* Ω Θ* = m g L/√2 = 0.1387 N m (every mounting)   (L0.6)

**Who pays.** The energy book (SymPy, L0.2): d(T + V)/dt = τ_rot φ̇ − c θ̇². Over a turn the stored energy returns to its value,
so the rotor's mean extra torque times Ω equals the generator's mean power: the rotor pays for every joule.

**Order tuning.** In blade-angle time the equation contains only R, G, κ. R is fixed by the geometry, so the ratio of the
pendulum's own frequency to the push frequency (√R) does not change with Ω: a slow change of rotor speed cannot detune the
pendulum from gravity's push (it changes G and κ, which L2 measures).

## 3. Model

State: θ (rod angle from the outward radial direction, in the rotor plane), θ̇. Laws: Lagrange's equations with the imposed
φ(t) = Ω t; Rayleigh dissipation. Closure: viscous generator torque −c θ̇ (exact for an ideal linear machine on a resistive
load, c = k_t k_e/(R_coil + R_load); L4 replaces it). Point bob, massless rigid rod, rigid blade, no air.

## 4. Alternatives considered and rejected

- **Out-of-plane (flapwise) swing**, hinge axis along the blade's tangent: gravity lies in the vertical rotor plane, so it has no
  component along the swing; at uniform rotation nothing drives it (shaft tilt adds a constant, non-turning component). Rejected:
  zero power at L0.
- **A spring–mass slider** (tangential): any linear oscillator driven at Ω gives the same off-resonance optimum
  P* = m² g² Ω/(4 |k_eff − mΩ²|). Its frequency is fixed by the spring, so it detunes as Ω changes, and the spring must survive
  1.4–215 g. Rejected at L0 for the pendulum's order tuning and spring-free stiffness; kept as the comparator in L3, where a fixed
  frequency could match the fixed blade mode.
- **Keeping the parametric term (linear time-periodic, Hill's method).** Rejected as inconsistent: the parametric term
  −Gθ sin φ is first order in 1/Γ but its effect on the mean power is second order (it moves energy to frequencies 0 and 2, orthogonal
  to the freq-1 response), the same order as the quadratic term G θ² cos φ/2 and the cubic R θ³/6 it leaves out. At Sol's damping it
  overshoots his nonlinear power by up to 11.6 % (8 rpm, 30 %), while the time-invariant closed form stays within 0.68 %
  (`L0_table.py`). The consistent improvement is the full nonlinear equation (L1).
- **The full nonlinear model now.** Deferred to L1 (one effect per level); L0 must give the closed form and the optimum.

## 5. Assumptions, each with its number (18 mountings, `L0_table.py`, `scales.py`)

| # | Assumption | Number | Fails where |
|---|---|---|---|
| A1 | small swing, sin θ ≈ θ | Θ* = 0.004–0.498 rad | 8 rpm 30 % (0.50 rad), 14 rpm 30 % (0.29), 8 rpm 60 % (0.25): L1 |
| A2 | parametric term dropped | 1/Γ = G/R = 0.005–0.697 | same slow mountings; its power effect is second order (section 4) |
| A3 | uniform rotation | ε = Ω̇/Ω² ≈ 0.024 rms (Fermi, NREL-5MW-like) vs G = 53, R = 94 | L2 measures it |
| A4 | rigid blade | edgewise shaking A at the pivot: P_e/P* = 2(A/g)² at κ* | A ≳ 1 m/s² (2 %): L3 |
| A5 | no air on the bob | exposed: drag 0.05–0.49 weights, rotor pays 0.90–24.3 W | always for an exposed bob: it sits inside the shell |
| A6 | frictionless pivot | ball bearing (M_f = ½ μ F d, μ = 0.0015, d = 5 mm, F = m r_p Ω²): Coulomb loss 0.005–0.73 % of P* | 400 rpm 90 % (0.73 %) |
| A7 | point bob, massless rod | a rod of mass m_r changes the moment of inertia by m_r/(3m) | m_r ≳ 0.03 kg for a 10 % change |
| A8 | rotor plane vertical | NREL 5-MW shaft tilt 5°: in-plane gravity × cos 5°, P × 0.9924 (−0.76 %) | Part II states it |
| A9 | ideal viscous generator | coil inductance, resistance, gearbox: L4 | L4 |

## 6. Must reproduce

- Limit Ω → 0 at fixed φ: ordinary pendulum, ω² = g/L about the downward rod (L0.1 with φ̇ = 0).
- Limit G → 0 (Γ → ∞): no drive, P = 0. Limit κ → 0 or κ → ∞: P → 0 (no brake takes nothing; a locked rod does not move).
- Resonance R = 1 (r_p = L, pivot 20 cm from the hub): P* diverges as κ* → 0; no real mounting reaches it.
- The energy book: mean rotor power = mean generator power (L0.2).
- Sol: κ* = |R − 1|, P* = M L g²/(4Ω|r_p − L|); at his damping, his stored linear rows to < 10⁻⁴ % (PASS);
  57.1 mW at 400 rpm 30 % (P* = 57.09 mW); his nonlinear 9.55–57.1 mW within 1 % (worst 0.68 %, PASS); share ≤ 7.20 × 10⁻⁵ (PASS).

## 7. Predictions that could come out wrong

- P1. At L1, the full nonlinear single pendulum at its own best damping gives within 1 % of P* at every one of the 18
  mountings, although Θ* reaches 0.50 rad and 1/Γ 0.70, because the leading corrections are second order and partly cancel.
  Dropped if any mounting differs by more than 1 %.
- P2. At fixed c, P(Ω)/P(Ω₀) = 2/(1 + Ω²/Ω₀²) for c tuned at Ω₀ (from L0.6). L2 tests it under slow rotor-speed changes.

## 8. Derived, cited, chosen

- Derived here: L0.1–L0.6 (SymPy, `L0_single.py`), the torque amplitude m g L/√2, the order of the parametric correction.
- Cited: Sol's study (stored runs in `public/portfolios/rotor-pendula/study/data/summary.csv`); the SKF frictional-moment
  approximation and μ = 0.0015 for deep-groove ball bearings (SKF rolling bearings catalogue; to be opened before it enters the
  text); NREL 5-MW shaft tilt 5° (dossier-turbine, pending).
- Chosen, with price: viscous generator (L4 pays); rotor plane vertical (A8, −0.76 % on the real turbine); point bob (A7).

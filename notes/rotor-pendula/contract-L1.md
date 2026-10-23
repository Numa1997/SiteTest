# Contract L1: nonlinear single and double pendulum, uniform rotation

Gate 1 contract. Derivation `derive/L1_double.py` (7 PASS); engine `derive/engine.py`, checked by
`derive/L1_engine_check.py` (7 PASS). Round 1, 23 October 2026. g = 9.80665 m/s².

## 1. Question and observables

The same blade and rotor as L0, now with swings of any size, and a second pendulum: two equal bobs (0.05 kg each) on two
equal rods (0.1 m each), same total mass M = 0.1 kg and reach L = 0.2 m as the single, with a generator at the pivot and one at
the hinge, both of constant c (Sol's choice). **Observables:** (1) the mean generator power of each at Sol's 18 mountings at
its best damping, and the ratio double/single; (2) where in (R, G, κ) the double pendulum is chaotic: the largest Lyapunov
exponent λ_max (per radian of blade angle) over an ensemble of initial conditions, with its spread and the fraction of
chaotic members; (3) whether any chaotic state delivers more mean power than the best regular state at the same (R, G).

## 2. Picture and formal mechanism

**Picture.** The single pendulum is a weathervane on the blade. The double is a weathervane with a hinge in the middle of its
arm: the outer half can lag behind the inner half, so gravity's once-per-turn push can make the two halves trade energy back
and forth. When the centrifugal pull is strong (large R) both halves are held straight out and move together; when gravity's
push is comparable to the pull and the brakes are light, the exchange can become irregular, like a double pendulum let go from
a large swing. Chaos means two copies started a hair apart drift apart exponentially.

**Formal mechanism.** Lagrange's equations with the rotor angle imposed (L1_double.py, equations L1.1–L1.2, identical to Sol's
dimensionless equations at uniform rotation); Rayleigh dissipation F = ½c₀q̇₁² + ½c₁(q̇₂ − q̇₁)²; energy book
d(T + V)/dt = τ_rot φ̇ − 2F (residual 10⁻¹³). The largest Lyapunov exponent by Benettin's method: integrate a reference and a
perturbed copy (separation d₀ = 10⁻⁸ in (q₁, q₂, q̇₁/Ω, q̇₂/Ω)), renormalise every quarter turn, average log(d/d₀) over the
measured window. Chaotic: λ_max > 0.01 per radian, with the transient discarded; regular orbits give λ_max < 0 (damped).

## 3. Model and numerics

State (q₁, q₂, q̇₁, q̇₂, E_harvest). Three-stage Radau IIA, order 5, L-stable, fixed step, simplified Newton (engine.py). The
generators make the double stiff: its fast relaxation rate is about 47 κ per radian (≈ 12 000 at the large-rotor optimum),
so explicit schemes need tens of thousands of steps per turn; a second-order splitting with exact damping was tried and
rejected (its error was 0.1–1.9 % at 285–1901 steps per turn). Radau reproduces SciPy DOP853 to 6 × 10⁻¹³, shows observed
order 4.90–4.95, and is converged to 10⁻⁶ at 50 steps per turn on Sol's mountings.

## 4. Alternatives considered and rejected

- **Linear time-periodic (Hill) theory:** inconsistent, overshoots the nonlinear power by up to 11.6 % (contract L0, §4).
- **Second-order perturbation theory (harmonic balance in 1/Γ):** gives the leading nonlinear correction for small swings but
  cannot describe chaos; kept only as a cross-check if the 1 % prediction P1 fails.
- **Poincaré sections alone as the chaos test:** qualitative; a smeared section can come from storage precision (Sol's audit
  found exactly this). Used as a picture, not as the test.
- **The 0–1 test for chaos (Gottwald–Melbourne):** a valid binary alternative; rejected in favour of λ_max because λ_max has
  units and a size, so "how chaotic" can be compared with the damping rate and the rotor period.

## 5. Assumptions, each with its number

| # | Assumption | Number | Fails where |
|---|---|---|---|
| A1 | uniform rotation | ε rms 0.0054 on the NREL 5-MW at 8 m/s, class A (`L2_scales.py`) | L2 |
| A2 | rigid blade | gravity bends the blade edgewise ±0.45 m at the tip, adding 3.4 % to gravity's push at 90 % span (`nrel5mw.py`) | L3 |
| A3 | point bobs, massless rods, viscous generators | as L0 A7, A9 | L4 for the generator |
| A4 | equal split m₁ = m₂, l₁ = l₂, c₀ = c₁ | Sol's choice; his geometry scan (R = 1.2, G = 0.01) found all 9 splits below the single | other splits at other (R, G) are not searched |
| A5 | finite-time Lyapunov exponent | 100 turns discarded, 100 measured; threshold 0.01 per radian ≈ 1.6 × 10⁻³ of the swing frequency at R = 1 | weakly chaotic or transient-chaotic states near the threshold: reported as such |
| A6 | best damping searched on c₀ = c₁ only | Sol's rule | a split of the two constants could do better: stated, not claimed |

## 6. Must reproduce

- Sol's 36 nonlinear mapping runs at his damping: **done, every printed digit (worst 0.000 %)**, ratio 0.6351–0.7354.
- Sol's matched chaos group (R = 1, G = 3.0646, μ = 1): regular branch 0.3789 W at c = 0.022 N m s; chaotic 0.244–0.253 W at
  c = 0.030 with λ = 0.130–0.177 s⁻¹; c = 0.015: 0.2625 W, λ = −1.707 s⁻¹; c = 0.045: 0.1181 W, λ = −0.006 s⁻¹.
- The L0 limit: small G, the nonlinear optimum → P* (within 1 %, L0 prediction P1).
- The energy book on every run (mean rotor power = mean harvest + stored-energy change / window).

## 7. Predictions that could come out wrong

- P1 (from L0): at each of the 18 mountings the single's own best damping gives within 1 % of P*.
- P2: at all 18 real mountings, for κ from the double's best damping down to a tenth of it, every initial condition of the
  ensemble lands on a regular orbit (λ_max < 0). Dropped if any member is chaotic.
- P3: at every (R, G) of the map, the best chaotic member delivers less mean power than the best regular member found at the
  same (R, G) over the same κ grid. Dropped if one chaotic state wins by more than its ensemble spread.

## 8. Derived, cited, chosen

Derived: L1.1–L1.2 (two routes: Lagrange in SymPy and Newton in the blade frame; agree to 6 × 10⁻¹⁵ with Ω̇ ≠ 0), the Euler
terms, the energy book. Cited: Sol's stored runs and report (`public/portfolios/rotor-pendula/study/`); Hairer & Wanner,
*Solving ODEs II*, §IV.5, for Radau IIA (coefficients checked by the order conditions in the code); Benettin, Galgani, Giorgilli,
Strelcyn (1980), Meccanica 15:9, for the Lyapunov algorithm (to be opened before it enters the text). Chosen: the equal split
(A4), the threshold (A5), the κ grid of the map.

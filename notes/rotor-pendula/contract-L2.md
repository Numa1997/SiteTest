# Contract L2: rotor speed driven by turbulent wind

Gate 1 contract. Scales: `derive/L2_scales.py` (3 PASS), turbine: `derive/nrel5mw.py`, wind and rotor: `derive/turbulence.py`.
Round 1, 23 October 2026.

## 1. Question and observables

Real wind is gusty, so a real rotor does not turn at constant speed. Does that change what the pendulum delivers?
Reference turbine: the NREL 5-MW (rotor radius 63 m), mean wind 8 m/s at hub height, IEC 61400-1 ed. 3 class A turbulence.
Mountings: single pendulum (0.1 kg, 0.2 m) at 30, 60, 90 % of the rotor radius (r_p = 18.9, 37.8, 56.7 m), generator constant c
fixed at the L0 optimum for the steady 8 m/s rotor speed Ω₀. **Observables**, over an ensemble of 10-minute records (the
IEC averaging time): the 10-minute mean power P̄ (mean and standard error over records), its 5 % quantile, and the
decomposition of its change against steady operation into (a) the shift of the mean rotor speed, (b) the quasi-static
wandering of Ω, (c) the dynamic Euler terms.

## 2. Picture and formal mechanism

**Picture.** A gust takes tens of seconds to speed the rotor up (the rotor weighs as much as a small ship: J = 4.38 × 10⁷ kg m²,
time constant 7.3 s); the pendulum swings √R ≈ 10–17 times per turn. To the pendulum, the rotor's speeding up and slowing
down is as slow as the seasons are to a day. And because both its own frequency and gravity's push are set by the same rotor
speed, the pendulum stays in step, the way a metronome on a slowly accelerating train keeps beating in the same ratio to the
wheels' clatter.

**Formal mechanism.** In blade-angle time the equation of L0/L1 depends on R, G = g/(Ω²L), κ = c/(mL²Ω) and the Euler
parameter ε = Ω̇/Ω² (L0_single.py eq. 3; L1_double.py gives its double-pendulum form). R does not depend on Ω (order tuning);
G and κ follow Ω slowly; ε is small. Hence three separable effects: (a) P depends on the mean speed through P*(Ω) ∝ 1/Ω and, at
fixed c, P(Ω)/P(Ω₀) = 2/(1 + Ω²/Ω₀²); (b) averaging that curve over the wandering Ω gives a quasi-static shift ≈ s²/2 with
s = σ_Ω/Ω̄ (Jensen); (c) the Euler terms force θ ≈ −ε quasi-statically, harvesting ~ c(dε/dt)², tiny.

## 3. Model

- **Wind.** Hub-height longitudinal turbulence, IEC Kaimal spectrum S_u(f) = 4σ₁²(L_u/V)/(1 + 6fL_u/V)^{5/3}, σ₁ = I_ref(0.75V + 5.6)
  = 1.856 m/s (I_ref = 0.16, class A), L_u = 8.1 × 42 = 340.2 m (TurbSim guide 1.50, eqs. 21–23; Table 1 of IEC 61400-1 ed. 3 as
  printed in the windPRO 4.1 manual). Rotor-effective wind: the u-component averaged over the disc, spectrum S_u(f)χ(f) with
  χ(f) = ∫ p(r) Coh(r, f) dr, IEC coherence Coh = exp(−12√((fr/V)² + (0.12r/L_c)²)), p(r) the distance distribution of two random
  points of the disc. Periodic 600 s records by FFT, mean exactly 8 m/s, spectrum scaled so the expected hub-point record
  variance is σ₁² (TurbSim's ScaleIEC intent). Each record is run twice; the second pass is measured (periodic spin-up).
- **Rotor.** J Ω̇ = Q_aero(v, Ω) − Q_gen(Ω); Q_aero = ½ρπR³v²C_p(λ)/λ with C_p(λ) at zero pitch from NREL's ROSCO table
  (peak 0.466 at λ = 7.5); Q_gen the NREL baseline torque law (regions 1, 1.5, 2, 2.5, 3; Jonkman et al. 2009 Table 7-2) cast to
  the low-speed shaft; J = 4.379 × 10⁷ kg m² (rotor 3.876 × 10⁷ from the report's blade tables, generator 97² × 534.116).
  Above rated speed an ideal pitch controller holds Ω at 12.1 rpm.
- **Pendulum.** L1 equations with φ(t), Ω(t), Ω̇(t) from the rotor, co-integrated in the same Radau state. In-plane gravity
  g cos 5° (shaft tilt).

## 4. Alternatives considered and rejected

- **Full turbulence box (TurbSim grid) + blade-element aerodynamics:** gives blade-local wind; for the rotor speed only the
  disc-averaged torque matters, which the rotor-effective wind captures. Price: no blade-local loads (they enter at L3).
- **Ornstein–Uhlenbeck wind:** right integral time, wrong shape (spectral slope −2 instead of −5/3, too little energy at
  0.01–0.1 Hz where the rotor responds). Rejected; the IEC Kaimal model is the standard's own.
- **Prescribed sinusoidal speed variation:** no source for its amplitude or period. Rejected.
- **A pitch-controller model in region 3:** the rotor reaches rated speed 0.17 % of the time at 8 m/s; an ideal speed limit
  is enough. Price: wrong dynamics during those 0.17 %.

## 5. Assumptions, each with its number (`L2_scales.py`, `nrel5mw.py`)

| # | Assumption | Number | Fails where |
|---|---|---|---|
| A1 | rotor-effective wind = disc average | χ(0) = 0.79, χ(0.01 Hz) = 0.45, χ(0.05 Hz) = 0.066; rotor-effective σ 1.16 m/s against 1.82 at the hub | a torque-weighted average (outer annulus counts more) would raise σ somewhat |
| A2 | one-state rigid drivetrain | first drivetrain torsion mode 0.6205 Hz (FAST; Jonkman et al. 2009 Table 9-1), 29 times above the rotor's response corner 1/(2π · 7.34 s) = 0.0217 Hz | not for the rotor speed; it could matter for blade-local vibration (L3) |
| A3 | ideal pitch at rated | active 0.17 % of the time | higher mean wind |
| A4 | pendulum does not load the rotor | its power is 10⁻⁸ of the rotor's | never here |
| A5 | shaft tilt 5° | in-plane gravity × cos 5° = 0.9962, power × 0.9924 | included |
| A6 | precone 2.5° | centrifugal pull along the coned blade × cos 2.5° = 0.9990 | neglected, with this number |
| A7 | 10-minute records with a fixed mean | IEC defines turbulence within 10 minutes; record means 8.000000 m/s | slower weather variation is outside the question |

Scales: σ_Ω/Ω̄ = 0.103 ± 0.019 per record; Ω from 7.19 to 12.10 rpm; mean Ω 9.29 rpm against the steady 9.07 rpm at 8 m/s;
ε = Ω̇/Ω²: rms 0.0054, largest 0.026, against G = 50–55 and R = 94–284.

## 6. Must reproduce

- Turbulence off (σ = 0): the L1 uniform-rotation power at Ω₀ = 0.9494 rad/s, to 10⁻⁶.
- The steady operating point at 8 m/s: Ω₀ = 9.066 rpm, λ = 7.48, C_p = 0.466, 1.82 MW (`nrel5mw.py`).
- The synthesis: hub-point record variance averages σ₁² (PASS, 0.977 over 200 records); χ(f) equals a Monte Carlo over random
  point pairs (PASS).

## 7. Predictions that could come out wrong

- P1 (brief): rotor-speed turbulence changes the single pendulum's mean power by less than 1 %, measured against uniform
  rotation **at the same mean rotor speed** (effects b + c). Dropped if the ensemble mean differs by more than 1 % plus two
  standard errors.
- P2: effect (c), the dynamic Euler part, is below 10⁻³ of P̄.
- P3: against steady operation at the mean wind (a + b + c), the mean power is lower by about the mean-speed shift: the rotor
  turns 2.5 % faster on average, so P̄ falls by ≈ 2 % (P ∝ 2/(1 + Ω²/Ω₀²) at fixed c). Dropped if it falls by less than 1 % or
  more than 3 %.

## 8. Derived, cited, chosen

Derived: Euler terms (L1_double.py), the decomposition (a)–(c), χ(f), J from the report's tables. Cited: Jonkman et al. 2009
(NREL/TP-500-38060, read via OSTI); OpenFAST r-test blade file; NREL ROSCO C_p table; TurbSim user's guide 1.50 (IEC Kaimal and
coherence); windPRO 4.1 manual for IEC Table 1 (secondary reproduction of the standard, which is paywalled; stated as such).
Chosen: disc-average weighting, ideal pitch, record scaling, c fixed at the steady optimum.

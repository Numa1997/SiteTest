# Fig. 16: the reduced slosh model, its derivation and its validation

Working file of the Fig. 16 chat (see STATE.md). Every number here is printed by a script in `tools/fig16/`; the script is named.

## 1. Why a reduced model

Fig. 12 computes the pint with a million particles on a GPU (about 85 ms a step on a Tesla T4, 4,080 steps for an 8 s ride).
Designing a cart means trying hundreds of carts and controllers. The owner's rule: "not a single atom of data if it's not needed";
the stored Fig. 12 rides already hold the pint's measured behaviour. So the pint is replaced, for design only, by the few sloshing
modes that the Fig. 12 note derives, with every number either from that theory or measured in the stored training rides, and the
model is then judged on stored rides it has never seen.

## 2. The equations

**Modes (Fig. 12 note eqs. 10, 11, 25, 26).** For an upright cylinder of radius R filled to depth h, each zero ξ_n of J₁′ gives a
mode with one wave round the glass, η = q_n J₁(k_n r)/J₁(ξ_n) cos θ, k_n = ξ_n/R, with q_n its height at the front wall:

    q_n'' + D_n(q_n') + ω_n² (1 + a_z/g) q_n = −β_n a_x                                         (M1)
    ω_n² = g k_n tanh(k_n h) / (1 + λ_h k_n tanh k_n h),   β_n = 2 ξ_n tanh(k_n h) / ((ξ_n² − 1)(1 + λ_h k_n tanh k_n h))

λ_h = φ_l h_f = 0.27 × 19 mm = 5.13 mm is the head's mass per area over ρ. Sum rule: Σ 2/(ξ_n² − 1) = 1 (the modes' shares of a
tilted plane): 0.837, 0.073, 0.028, 0.015, ... So one mode carries 84 % of a steady tilt; three carry 94 %.

**The stout's push on the cart.** P_x = ρ ∫ u_x dV = ρ ∫ ∂φ/∂x dV = ρ ∮ φ n_x dS (Gauss). Only the wall has n_x ≠ 0 (n_x = cos θ).
With φ_n = Υ_n J₁(k_n r) cos θ cosh(k_n z)/cosh(k_n h):
P_n = ρ Υ_n J₁(ξ_n) π R ∫₀^h cosh(k_n z) dz / cosh(k_n h) = ρ π R Υ_n J₁(ξ_n) tanh(k_n h)/k_n.
The kinematic condition q_n'/J₁(ξ_n) = k_n tanh(k_n h) Υ_n eliminates Υ_n: **P_n = ρ π R q_n' / k_n² = ρ π R³ q_n' / ξ_n²**, and
F_x = −dP/dt = −Σ γ_n q_n'', γ_n = ρ π R³ / ξ_n² (= 55.8 g for the first mode).
Check: the centre of mass of the liquid moves by x_c = (1/V)∫ x η dA = q R/(ξ² h) for the first mode, and m x_c' = ρπR²h · q'R/(ξ²h)
gives the same P. Measured on the stored rides (`tools/fig16/gamma_check.py`): 79.7 g (five bumps) and 71.7 g (one bump), each
with correlation 0.96 between F_x and −q''. The model uses the measured mean, 75.7 g. The cylinder misses about a third; open.

**The friction** (`slosh_model.damping`): D(q') = 2 ζ ω q' (|q'|/(ω q_ref))^(n − 1), q_ref = 5 mm. n = 1 is linear; Cantat's
sliding law for the head's edge on the glass (stout_jax.head_wall_stress, stress ∝ Ca^(2/3)) gives n = 2/3, whose damping ratio
falls as the swing grows: the head brakes a small swing hard and a big one comparatively little.

**What the rides call the tilt** (pack_ride.py): twice the cos θ part of the surface on the ring r_m = R_fill − Δx/2, so
tilt = 2 Σ q_n J₁(k_n r_m)/J₁(ξ_n).

**The cart.** Fig. 12's `Cart` (stout_jax.py), imported unchanged: same masses, motor, back-EMF, current lag, tyre, suspension,
controllers, observer, sub-steps of 0.1 ms in fluid steps of 2 ms; the probes read Σ q_n once per fluid step.

**The head spilled** (`tools/fig16/spill.py`): the solver's own rule (stout_jax.Stout.head_spill) applied round the rim to
η = (Σ q_n) cos θ: the head's top stands e = η + h_f − (z_rim − fill) above the rim; it breaks off whole once
ρ_f (|g + a_z| e/2 + a_out e) ≥ τ_y. At rest: the head's top is 3.50 mm below the rim and breaks when 4.06 mm stands above it,
so the wall must rise about 7.6 mm before foam leaves.

## 3. Training and validation (filled in by validate.py)

Printed by `python3 tools/fig16/validate.py --plot` (numbers in `tools/fig16/validation.json`, picture `notes/fig16/validation.png`).

Fitted on the training records only (`tools/fig16/fit.py`, `fit.json`): three modes; ζ = 0.213 at q_ref = 5 mm, friction power
n = 0.6665 (Cantat's law predicts 2/3; the fit was free), ζ of modes 2 and 3 = 0.365; linear friction
(n = 1) fits 2.4 times worse. Push coefficient γ = 75.7 g. Spill strip w_s = 2.74 mm, from run 8's kerb with the speed held alone.

| ride (first three: training; last five: validation, never fitted) | tilt max stored / model, mm | rms tilt error of rms tilt, mm | largest speed error, m/s | rms current error, A | head spilled stored / model, mL |
|---|---|---|---|---|---|
| run8/ride_resonant | 13.54 / 13.78 | 0.23 of 2.79 | 0.001 | 0.004 | 0.01 / 0.00 |
| run8/ride_bump25 | 7.96 / 8.31 | 0.10 of 1.05 | 0.001 | 0.001 | 0.00 / 0.00 |
| run8/ride_sharp30 | 22.23 / 26.18 | 1.06 of 5.17 | 0.016 | 0.008 | 2.44 / 2.44 |
| run10/ride_resonant_joint | 1.00 / 0.87 | 0.07 of 0.27 | 0.002 | 0.006 | 0.00 / 0.00 |
| run10/ride_bump25_joint | 1.03 / 0.95 | 0.08 of 0.16 | 0.003 | 0.004 | 0.00 / 0.00 |
| run10/ride_sharp30_joint | 24.55 / 27.47 | 1.05 of 4.89 | 0.023 | 0.149 | 2.07 / 2.14 |
| run10/ride_sharp30_slosh | 20.81 / 25.67 | 0.70 of 3.53 | 0.020 | 0.097 | 1.63 / 1.58 |
| run10/ride_sharp30_preview | 23.03 / 24.89 | 1.11 of 5.37 | 0.016 | 0.006 | 2.51 / 2.46 |

The model's largest tilt is taken over every 2 ms step, the stored one over 30 pictures a second, so on the kerb the model's peak
is 2 to 5 mm higher partly because the stored pictures miss the peak. Bands to carry into the design: tilt ±1.1 mm rms on the kerb,
±0.1 mm on gentle roads; head spilled ±0.07 mL (the solver's own run-to-run scatter is ±0.05 mL); current ±0.15 A on the kerb.
What the model does not have: splashing, drops of stout, the surface's roughness, the stout's vertical push on the cart, swirl.

# Skeptic, Gate 1, contract L4 (geared DC generator), round 1

Blind adversarial read of `contract-L4.md`, 23 October 2026. Read: the contract, `contract-L0.md` (for R, G, κ), `dossier-generator.md`,
`derive/L4_full.py`, `L4_generator.py`, `L4_check.py`, `L4_converge.py`, `L4_resonance.py` and the scan logs and JSON files. Not read:
status, referee notes, earlier skeptic notes.

My own runs. The scripts are in the session scratchpad and are not part of the repository:
- `/tmp/claude-0/-home-user-SiteTest/8b34d6df-5462-5589-b418-3710ebaaeab4/scratchpad/sk/stick.py`: the version-3 full equation (`make_rhs`,
  Radau, 2000 steps per turn) at 7 of the scan's chosen settings. It records θ′ over 3 turns after 60 turns of settling, the fraction
  of time the rod is stopped, and the EMF and the load voltage.
- `/tmp/claude-0/-home-user-SiteTest/8b34d6df-5462-5589-b418-3710ebaaeab4/scratchpad/sk/sens.py`: the formula of `L4_generator.py` with
  motor-side friction ×2 and ×3, and with η = 0.5.
- `python3 -I L4_generator.py` was re-run. It reproduces the formula table.

## What checks out (no objection)

- **Brake constant.** At the motor, e = k_e N θ̇, I = e/(R_c + R_L) and the torque is k_t I. Seen at the pendulum the torque is
  N k_t I = N² k_t k_e θ̇/(R_c + R_L). The sign is right and the units are N m s/rad. The limit R_L → 0 gives c_sc. The sheet gives
  k_t = 20.8 mN m/A and k_e = 20.76 mV s/rad. The 0.2 % mismatch makes the electrical and mechanical powers differ by 0.2 %. That is
  negligible, but the code should use one constant for both.
- **Load share.** The load gets I² R_L out of I²(R_c + R_L), so its share is R_L/(R_c + R_L) = 1 − c_e/c_sc. The load power is
  computed from κ_e θ′² on the motor side, before any gear loss. That is correct: the electrical power is generated on the motor side.
- **Gear loss k = η^(−sgn(xθ′)).** The power lost in the gearhead is (k − 1)xθ′. When xθ′ > 0, k = 1/η > 1. When xθ′ < 0, k = η < 1.
  The loss is ≥ 0 in both cases, and stays ≥ 0 with the tanh smoothing, because (k − 1) keeps the sign of u. So it **cannot create
  energy.** The loss is charged once, on the net mesh torque x = jθ″ + friction + brake. It is not charged on the parts separately, so
  nothing is **double-counted**. This is the right physics, because the teeth carry only the net torque. Charging Coulomb mesh
  friction on reactive power (version 3) is also right. The tooth friction loss ∝ |T ω| does not care where the energy goes next.
- **Monotone implicit equation.** The bound d(kx)/dx ≥ 1 − |ln η|·max(u sech²u) = 1 − 0.448|ln η| > 0 holds for η ≥ 0.5, so bisection
  plus Newton is safe.
- **Describing function.** For θ = Θ sin τ, the fundamental of sgn(cos τ) is 4/π, so κ_f = 4f/(πΘ) at unit frequency. The phasor
  equation then gives Θ²(R − 1 − j)² + (κ_eΘ/η + 4f/π)² = G². In the formula code f already contains 1/η. The mean friction power
  is f(2/π)Θ. All of this is correct.
- **Units.** f₀ = N T0/(m L² Ω²), κ_e = c_e/(m L² Ω) and j = J N²/(m L²) are all dimensionless and consistent with G = g/(Ω² L).
- **Who pays.** The mean of k x θ′ over a turn is the total dissipation (the inertial part only averages to zero when k = 1). This is
  consistent with L0's energy book.
- **Version 2 to version 3.** The reason for the change is physical, not cosmetic. The 0.44 W "resonance" was the reflected inertia
  j ≈ R − 1 tuning the rod onto resonance, with the reactive power passed through the teeth at no cost.

## Objections

### M1 (major). The gearhead's own drag is missing from the model and from the assumption table
**Claim.** The only friction is the motor's, T0 = k_t I0 = 0.84 mN m, reaching the pendulum as N T0/η (A2).
**Why it may be wrong.** The dossier calls the gearhead's breakaway / no-load torque "the main open number". Neither maxon sheet gives
it. A 3-stage planetary carrying 0.14 N m against a 6 N m rating runs at about 2 % of rated torque. At that load the load-independent
losses (grease churning, seals, bearings) dominate, and the "max. efficiency 70 %" says nothing about them. The contract does not list
this drag at all; A1 covers only the efficiency. Every L4 output depends on it: the friction share, the best ratio, the swing, and the
jamming ratios of P2.
**Size (my run, `sens.py`, formula).** At 8 rpm 90 %, total friction ×2 gives 0.89 mW at the load, down from 1.77 mW, with the best ratio
moving from 51 to 33. Friction ×3 gives 0.48 mW. Friction ×2 with η = 0.5 gives 0.41 mW (11× the sensor). P1's "≥ 10×" survives at the
mechanical level, barely. P2 does not: a gearhead drag equal to the motor's, referred to the input, puts N = 111 at f/G ≈ 1.35, so 111
jams too.
**Settles it.** Add the gearhead drag to the assumption table as an explicit input with a range. Use a source (ask maxon, or find a
measured no-load torque for a GP 32 class gearhead) or a bench number. Run the formula and the full equation at drag = 0, 1 and 2 × T0
referred to the input. Restate P2 as conditional on it.

### M2 (major). Voltage level and brushes: "enough for the sensor" is not shown
**Claim.** On the large rotors the load receives at least 10 × 37.6 µW (P1). The electronics are left out "before the electronics" (A6).
**Why it may be wrong.** The power arrives at very low voltage, alternating in sign at the rotor frequency, through graphite brushes.
- **Measured** (`stick.py`, full equation, chosen settings): the peak EMF is 0.20 V and the peak load voltage 0.13 V at 20 rpm 90 % and
  at 8 rpm 90 %. At 8 rpm 60 % they are 0.31 V and 0.23 V; at 8 rpm 30 %, 0.67 V and 0.55 V. The polarity reverses every half swing,
  at 0.13–0.33 Hz, and R_L ≈ 3–7 Ω.
- **Formula with friction ×2** (`sens.py`): the peak load voltage falls to 50–60 mV.
- **Brushes.** The RE 25 part 339152 has **graphite brushes**. maxon's own support article ("Properties of brushed DC motor
  commutation systems", support.maxongroup.com article 360004252074, read through the Zendesk API) lists graphite brushes as **"not
  suited for small currents; higher friction, higher no-load current"**. Only precious-metal brushes are credited with a "small and
  constant voltage drop". Here the peak current is about 45 mA against a nominal 1.5 A (3 %), with tenths of a volt of EMF. A graphite
  brush contact drop of order 0.1–0.5 V would take most or all of it. The linear R_c = 1.53 Ω cannot represent that drop.
- **Rectification.** A diode bridge cannot rectify a 0.1 V signal. A bipolar-input boost converter (an LTC3109-class part) works from
  tens of mV, but its efficiency there is tens of per cent.

So the claim that the generator is "still enough for the sensor" is not established. That claim is the stated question of L4.
**Settles it.** Report the load voltage and current next to every load power. Add a brush contact model with a cited drop for the chosen
part, or switch to a precious-metal-brush motor (RE 25 EB, or the Faulhaber 2232 SR from the dossier) and rerun. Either restate P1 as
"mechanical power at the load terminals, before brushes and electronics", or give a converter efficiency at the actual voltage with a
source.

### M3 (major). Backlash (1°) invalidates the fast-rotor rows
**Claim.** A5 ignores the backlash and calls it "a limit" on the fast rotors.
**Why it is wrong there.** The backlash is about 0.0175 rad in total, so the half-play is b/2 = 0.0087 rad. The chosen swings from the
version-3 scans are:

| Mounting | Swing (rad) |
|---|---|
| 400 rpm 60 % | 0.010 |
| 400 rpm 90 % | 0.006 |
| 200 rpm 60 % | 0.014 |
| 200 rpm 90 % | 0.008 |
| 100 rpm 60 % | 0.021 |
| 100 rpm 90 % | 0.014 |
| 400 rpm 30 % | 0.037 |
| 200 rpm 30 % | 0.039 |
| 100 rpm 30 % | 0.050 |

The motor side is held by its friction and moves only after the play is taken up, so the gear acts as a play (dead-zone) operator. The
motor then sees an amplitude of about Θ − b/2.
- At 400 rpm 90 % and 200 rpm 90 %, Θ < b/2. **The gear never engages, and the load power is zero**, not 4.4 mW and 3.2 mW.
- At Θ ≈ 0.01–0.02 rad most of the motion is lost.
- At 0.037 rad (400 rpm 30 %) the motor amplitude is cut by about 24 %, so roughly 40 % of the power is lost.
- On the large rotors (Θ = 0.06–0.46 rad) the correction is 2–15 % in amplitude. That is not negligible at 20 rpm 90 % (0.06 rad).

Because the brake disappears while the play is being crossed, the swing and the best brake also change. Each reversal is an impact,
which adds wear and noise.
**Settles it.** Withdraw the fast-rotor rows, or recompute them with a play operator: the describing function of backlash, or the full
equation with a dead zone on the motor coordinate. Add the correction at 20 rpm 90 % and 14 rpm 90 %.

### M4 (major). "The swing never sticks at the chosen settings" is false
**Claim.** Section 4 rejects exact stick–slip "because the swing never sticks at the chosen settings".
**Measured** (`stick.py`, version 3, band 10⁻³ of the swing scale). The rod is stopped (|θ′| < 1 % of its peak) for **25–29 % of each
turn** on the large rotors (8 rpm 30/60/90 %, 20 rpm 90 %), 19 % at 200 rpm 90 % and 11 % at 100 rpm 30 %.
**Why.** For R − 1 ≫ 1 the rod is nearly quasi-static. At a turning point the torque from stiffness plus gravity is only about
(1 + j)Θ = 0.3–0.8, while the friction is f/η = 21.7 (G = 70, f/G = 0.31). The rod therefore has to wait until gravity's torque has
swung through 2f before it moves again. The describing function assumes a sinusoidal swing, and that assumption does not hold here.
The smoothed model represents the stuck phases as a stiff viscous creep. `L4_check.py` itself says "the smoothing cannot resolve
sticking" (in the jamming context).
**What softens it.** The formula still agrees with the full equation within 0.3–6.5 % on the large rotors (`gap` in the old
`L4_check_2000.json`). The old 2000-step / band 10⁻³ and 4000-step / band 3×10⁻⁴ runs agree within 0.67 %, which suggests the creep
representation has converged. So the numbers may well be right, but the contract's stated reason is wrong.
**Settles it.** Correct the text. Then run one event-driven stick–slip integration at one large-rotor mounting, or show a band sweep down
to 10⁻⁵ with the load power converging within 1 %. Say on the page that the rod stops about a quarter of every turn. A reader looking at
the animation will see it.

### M5 (major, process). The predictions were written after the runs
P1, P3 and P4 were all computed before the contract (the logs are older than the contract). P4 is explicitly informed by version 2, and
P3's 10 % threshold sits next to measured gaps of up to 6.5 %. None of them could have come out wrong when they were written.
**Settles it.** Register at least one new, quantitative prediction now and test it after this round. For example: "an event-driven
stick–slip run at 8 rpm 90 % gives the load power within 2 % of the smoothed model", or "with a 1° play the 20 rpm 90 % load power
drops by between X and Y %".

### Minor
- m1. **P2 is a definition, not a risk.** N T0/η > m g L is the static-friction criterion inside the model. It is "exact" only for uniform
  Ω and a rigid blade. Euler torque (εR/G ≈ 0.04, L0) and edgewise shaking (L3) add dither that can unjam a marginal ratio, and gearhead
  breakaway (M1) moves the threshold. Also, the formula's own jam criterion is 4f/π ≥ G (f ≥ 0.785 G), not f ≥ G. No catalogue ratio
  falls between the two, but say so.
- m2. **A1: backdriven efficiency.** The textbook friction-angle estimate is η_b = 2 − 1/η_f per mesh. For 3 stages at 0.888 each that
  gives 0.67 overall; applied to the overall figure it gives 0.57. The model uses η for both power directions, but motor→pendulum flow
  is forward drive (η_f) and pendulum→motor flow is backdrive (η_b). Allow two values. `sens.py` shows η = 0.5 costs 40 % of the load
  power at 8 rpm 90 %.
- m3. **A2: low-speed friction.** The direction "probably lower: pessimistic" is not established for graphite brushes. maxon lists
  them as "higher friction", and breakaway friction at each reversal (the rod reverses every half turn) is usually above running
  friction.
- m4. **Convergence file mismatch.** `L4_converge.py` as committed crashes (KeyError 'P_load') on the `L4_check_2000.json` and
  `L4_check_4000.json` on disk, which are in an older key format (`P_load_full`). The 1 % claim in section 6 is supported by those old
  files (worst 0.67 %; my comparison), but the cited script cannot reproduce it until the reruns now in progress (started 18:15) finish.
- m5. **Notation.** In section 2, f in "4f/π" is not defined. In the formula it is N T0/(η m L² Ω²); in section 3, f₀ has no η. Define it
  once.
- m6. **The formula's inertia is lossless (version 2 physics).** The formula keeps the reflected inertia lossless while the full model
  charges it. That is fine on the large rotors (j/κ ≈ 1 %), but at 400 rpm 90 % the formula gives 8.2 mW where the full equation gives
  0.21 mW at the same setting. Flag the formula as invalid where j is close to R − 1.
- m7. **g-loading on the motor.** On the fast rotors (Γ up to 215 g) the brushes, the bearings and the gearhead output radial load
  (m r_p Ω² ≈ 200 N at 400 rpm 90 % against the GP 32 C bearing rating) are outside the datasheet. This is irrelevant on the large rotors
  (Γ ≈ 1.4–4.3).
- m8. Graphite brushes are humidity-sensitive (same maxon article), and the grease viscosity rises in a cold blade. State the
  temperature taken for T0 and η.

## Verdict: FAIL

Must be answered: **M1** (gearhead drag absent), **M2** (voltage level and graphite brushes: the sensor claim is not shown), **M3**
(backlash: the fast-rotor rows are void), **M4** (the sticking premise is false; evidence needed) and **M5** (a fresh prediction). No
fatal objection: the generator model's sign and energy bookkeeping are sound, and the large-rotor mechanical numbers will probably
survive within a factor of about 2–4.

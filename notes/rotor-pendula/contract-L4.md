# Contract L4: from swing to watts, with a real geared generator

Gate 1 contract, 23 October 2026. Written after three model versions had been run (the history is part of the contract).
Scripts: `derive/L4_generator.py` (formula, describing function), `derive/L4_full.py` (full equation, version 3),
`derive/L4_scan.py` (settings chosen in the full equation), `derive/L4_check.py` + `derive/L4_converge.py` (2000 against 4000
steps per turn), `derive/L4_resonance.py` (the accidental resonance, versions 2 and 3), `derive/L4_harmonics.py`.
Sources: `dossier-generator.md` (maxon RE 25 catalogue page 153, GP 32 C pages 430–431, read from the PDFs).

## 1. Question and observables

The ideal brake of L0–L3 loses nothing. A real generator is a small motor driven backwards through a gearhead. How much of
the swing's power reaches a load resistor, and is it still enough for the sensor (37.6 µW)? **Observables**, per mounting
(Sol's 18): the power at the load, the power the rotor pays, the friction's share, the best catalogue ratio and load resistor,
and the swing; plus the ratio above which the gearhead jams the pendulum.

## 2. Picture and formal mechanism

**Picture.** A bicycle dynamo is a brake whose strength you set with the lamp: shorted it is hard to turn, open it spins
freely. A gearbox makes a small fast motor look like a strong slow brake, but everything on the fast side is magnified seen
from the slow side: torque by N, inertia by N² (the hand-cranked egg beater).

**Formal mechanism.** Motor: e = k_e ω_m, torque k_t I, I = e/(R_c + R_L); through ratio N the brake at the pendulum is
c_e = N² k_t k_e/(R_c + R_L) ≤ c_sc = N² k_t k_e/R_c; the load keeps the fraction 1 − c_e/c_sc of the electrical power. The motor's
rotor adds j = J N²/(m L²) to the pendulum's inertia, so the net stiffness becomes R − 1 − j. Friction T0 = k_t I0 reaches the
pendulum as N T0 (Coulomb). Gear loss: the pendulum supplies x/η when power flows into the motor side and receives η x when it
flows back (x the motor-side torque referred to the pendulum through an ideal gear), for every power, inertial included.
Formula: describing function of friction, κ_f = 4f/(πΘ), and the swing from Θ²(R − 1 − j)² + (κ_e Θ/η + 4f/π)² = G².

## 3. Model

Full equation (version 3, `L4_full.py`), rotor angle τ as time:
θ'' + R sin θ + G cos(τ + θ) + k x = 0,  x = j θ'' + f₀ sgn θ' + κ_e θ',  k = η^(−sgn(x θ')),
f₀ = N T0/(m L² Ω²), κ_e = c_e/(m L² Ω). Acceleration from the implicit equation by bisection and Newton (h(a) is increasing).
sgn smoothed by tanh over a band of 10⁻³ (10⁻⁴ for the convergence run) of the swing scale. Radau IIA (L1 engine). Settings: for
each mounting, ratios 14, 33, 51, 111 and brakes 0.25–4 times the formula's best, 100 turns to settle, 20 to measure; a setting
counts if steady (halves agree to 1 %), swing ≤ 0.5 rad, motor ≤ 8000 rpm (gearhead input limit).

## 4. Alternatives considered and rejected (the history)

- **Version 1** (commit 3f19ee0): losses subtracted after the swing was computed with the brake alone. Rejected: friction must
  slow the swing; version 1 double-counted it and made the large rotors look five times worse than they are.
- **Version 2**: gear loss on the brake and friction only, inertial torque passed without loss. Rejected: at 400 rpm, 30 %, ratio
  51 (j = 1.0014 against R − 1 = 1.0054) it found an accidental resonance worth 0.44 W at the load, carried by a reactive power of
  tens of watts flowing through the gears for free. Mesh friction does not care whether the power is reactive.
- **Exact stick–slip friction** (event-driven): not needed for the harvesting runs (the swing never sticks at the chosen
  settings); jamming is settled by the static argument below instead.

## 5. Assumptions, each with its number

| # | Assumption | Number | Fails where |
|---|---|---|---|
| A1 | backdriven efficiency = catalogue maximum forward efficiency (70 % at 3 stages) | not on the sheet | optimistic; a bench test settles it |
| A2 | friction T0 = k_t I0 | 0.84 mN m, measured at 10 900 rpm | at the pendulum's 90–480 motor rpm friction is probably lower: pessimistic |
| A3 | inductance neglected | L/R = 0.12 ms against a swing period ≥ 0.15 s | never here |
| A4 | inertia reflected through an ideal gear, loss by power flow | gearhead inertia 0.7–0.8 g cm² against rotor 14.7 g cm² | |
| A5 | backlash 1.0° ignored | 0.017 rad against swings 0.006–0.45 rad | the fast rotors (swing 0.006–0.04 rad): backlash is comparable to the swing there; stated as a limit |
| A6 | rectifier and regulator not modelled | the margin is quoted "before the electronics" | |

## 6. Must reproduce

- Losses off (f = 0, j = 0, η = 1, c_sc → ∞): the formula reduces to (2.2)/(2.3); the full model to the L1 single pendulum.
- Unit tests of `make_rhs`: η = 1 gives the explicit equation to 10⁻¹⁵; the implicit residual is 10⁻¹⁷.
- Convergence: 2000 and 4000 steps per turn agree within 1 % (`L4_converge.py`).

## 7. Predictions that could come out wrong

- P1: on the large rotors (8–20 rpm) the load receives at least 10 times the sensor's 37.6 µW at every mounting.
- P2: ratios with N T0/η > m g L (190, 246, 492) jam the pendulum (static argument, exact for a rod starting at rest on the
  blade's line, where the centrifugal torque vanishes).
- P3: on the large rotors the formula is within 10 % of the full equation (the brake dominates the inertial torque there,
  j/κ ≈ 1 %).
- P4 (informed by version 2, stated as such): once the gear loss is charged on the inertial power, the accidental resonance at
  400 rpm, 30 %, ratio 51 is no longer the best setting.

## 8. Derived, cited, chosen

Derived: the brake constant, the load share, the reflected inertia, the describing function, the implicit full equation.
Cited: maxon catalogue pages 153 (RE 25, part 339152), 430–431 (GP 32 C). Chosen: the RE 25 + GP 32 C pair (a catalogue part
able to resist 0.14 N m at the pivot), the backdriven efficiency, the friction estimate.

## Round 2: answers to skeptic-G1-L4-r1.md

- **M1 (gearhead drag missing).** Accepted. `derive/L4_sensitivity.py` (the skeptic's script, adopted, extended to the nine
  large-rotor mountings): with the friction doubled the load gets 0.89–5.4 mW, tripled 0.48–2.5 mW, with η = 0.5 1.03–5.4 mW, with
  both twice the friction and η = 0.5 0.41–2.0 mW; the worst is about 10 times the sensor's need, so P1 holds across this range.
  The jamming ratio scales as 1/(friction multiple): 164 at the sheet's value, 82 at twice. The note quotes these.
- **M2 (voltage, brushes).** Accepted as a stated limit. The load voltage peaks at 88–326 mV (large rotors) and alternates once
  per turn (0.13–0.33 Hz). The note now says that converting it is an electronics problem these notes do not solve and that the
  brushes at such small, slow currents need a test; all margins are quoted "before the electronics".
- **M3 (backlash).** Accepted. Table 2 marks the two fast mountings whose swing is below the half play (0.0087 rad) with † and the
  seven whose swing is under six times it with ‡; the headline numbers come from the large rotors only (swing ≥ 0.06 rad).
- **M4 (sticking).** Accepted: "the swing never sticks" was false and is withdrawn. `derive/L4_stick.py` (the skeptic's script,
  adopted) measures the time stopped; the 2000/4000-step runs agree within 1 %, so the smoothed model resolves the averages.
- **M5 (predictions after the runs).** Accepted; P1 was nevertheless at risk under M1's sensitivity and survived (worst 10×).
- **Minor.** `L4_converge.py` failed on the old JSON keys; the version-3 check files use the keys it reads.

## Round 3 (minor points of skeptic-G1-L4-r2.md)

The load voltage is now quoted from the full equation (L4_stick.json, large rotors: 130–553 mV peak), not from a sinusoidal
estimate; §7.4 states that the rod stands nearly still for 25–29 % of each turn; the jamming ratios are marked "at the
catalogue's friction"; chapter 0 carries "before the losses of the sensor's own electronics". The maxon support article on
graphite brushes was not read in this session, so the note does not cite it and says only that the brushes need a test.

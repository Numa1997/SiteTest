# Contract L3: the blade bends and shakes

Gate 1 contract, written on 23 October 2026 after the L3 runs (the order is stated, not hidden: the runs came first, under the
time pressure of the lecture note; this contract records the model as run and is sent to a blind skeptic now).
Scripts: `derive/L3_sag.py`, `derive/L3_sag_numbers.py`, `derive/L3_sag_check.py` (→ `L3_sag.json`), `derive/L3_shake2.py`
(→ `L3_shake2.json`); `derive/L3_shake.py` (one-way, superseded, kept for the record). Turbine data: `derive/nrel5mw.py`.

## 1. Question and observables

A real blade is elastic. Gravity bends it edgewise once per turn (the sag), and gusts make its first edgewise mode vibrate.
Both move the pendulum's pivot. Does that change what the pendulum delivers, and can a pendulum tuned to the blade's vibration
take more? Reference: NREL 5-MW blade (61.5 m), 8 m/s, mean rotor speed 0.9494 rad/s (9.07 rpm), pivots at 30, 60, 90 % of the
rotor radius. **Observables:** (a) the change of the single pendulum's mean power from the sag, in per cent of the rigid-blade
value; (b) the mean power taken from random edgewise shaking at tip levels 5, 20 and 100 mm rms, for Sol's pendulum, the
double of equal mass and reach, and a rod tuned to the blade's frequency; (c) the tuned rod's swing, and its gain averaged over
the measured wander of the rotor speed (L2).

## 2. Picture and formal mechanism

**Picture.** A long springy ruler held out sideways and turned slowly sags first one way, then the other: the blade does the
same in its own plane, once per turn, exactly in step with gravity's push on the pendulum. The blade's section also turns with
the slope of the bend, and the generator's stator is fixed in the section. The shaking is a second, faster wobble near 1.08 Hz.

**Formal mechanism.** Pivot displaced along the blade's tangent by u = Φ(x_p)·x_tip(t), section rotated by β = Φ'(x_p)·x_tip(t)
(Φ the edgewise mode shape). In the Lagrangian of L0, the pivot's acceleration and the shift of the centrifugal field add
2Ω²w cos φ to gravity's push (w the pivot's sag amplitude); the generator brakes θ − β, so the section's rotation enters through
the brake, a quarter period out of step with the push. Shaking: modal coordinate x coupled both ways to the pendulum; linear
frequency-domain response to a modal force that is white near ω_e; power c∫S_F ω²|H_rel|² dω.

## 3. Model

- **Sag.** Edgewise static deflection under gravity from the blade's mass and stiffness tables (OpenFAST r-test blade file,
  NREL 5-MW), first edgewise mode at the system frequency 1.08 Hz (Jonkman et al. 2009, Table 9-1), tip amplitude
  x_tip = g_e g cos5°/(m_e ω_e²) / (1 − (Ω/ω_e)²) (quasi-static with the 1P dynamic factor). Pendulum: L0 single at κ*.
- **Shaking.** Two-way coupled linear model: blade modal mass m_e, stiffness k_e = m_e ω_e², damping ζ_e = 0.5 % or 3 %, pendulum
  linearised about the blade's line in the turning frame (centrifugal stiffness, Coriolis/gyroscopic terms from SymPy), rotor
  at uniform Ω, gravity left out of this part (its 1P effect is the sag above). Modal force white near ω_e, scaled so the blade
  without the pendulum has the stated tip rms. Pendulum: Sol's single (0.1 kg, 0.2 m), the double, and a single rod tuned to
  ω_e at the mean Ω. Pivot at 90 %.

## 4. Alternatives considered and rejected

- **One-way forcing (prescribed pivot motion):** `L3_shake.py` gave 94 W for the tuned rod, more than the gusts feed into the
  blade: unphysical, because the pendulum's reaction on a lightly damped blade is not small near resonance. Rejected; two-way.
- **A full aeroelastic code (OpenFAST):** would give the shaking level from first principles; not available here. Price: the
  tip level is a stated range (5–100 mm rms), not a prediction.
- **Ignoring the section's rotation:** gives +1.2 to +14.7 % from the sag; wrong because the stator turns with the section.

## 5. Assumptions, each with its number

| # | Assumption | Number | Fails where |
|---|---|---|---|
| A1 | first edgewise mode only | next edgewise mode far above (FAST: 2nd edgewise ≈ 4.2 Hz, Jonkman 2009 Table 9-1) | high-frequency shaking |
| A2 | linear blade | tip sag 0.47 m on a 61.5 m blade | never here |
| A3 | shaking level | 5, 20, 100 mm rms tip: no source found that states it for this blade | the range brackets it; stated |
| A4 | white modal force near ω_e | band of the blade's resonance (half-power width 2ζω_e) | broad-band coupling to the pendulum's own frequency |
| A5 | linear pendulum for shaking | tuned rod swing 0.21 rad rms at 5 mm | at 20 mm the linear model asks for > 1 m of rod travel: invalid, stated |
| A6 | uniform Ω for the shaking part | σ_Ω/Ω̄ ≈ 10 % (L2) | the tuned rod: its frequency follows Ω, the blade's does not; averaged in (c) |

## 6. Must reproduce

- No sag, no shaking: the L0/L1 power at Ω₀, to 10⁻⁶.
- Energy bound: the generator never takes more than the turbulent power fed into the blade (checked in every case: PASS).
- Sag: the linear theory and the full nonlinear run with the moving, turning pivot agree within 0.3 percentage points (PASS:
  within 0.2).

## 7. Predictions that could come out wrong

- P1: the sag changes the single pendulum's power by less than 2 % once the section's rotation is included (result: −0.3,
  −0.6, +0.7 %).
- P2: at 5 mm tip shaking, Sol's pendulum takes less than 10 % of what gravity gives it.
- P3: the tuned rod is a tuned mass damper: it takes a sizeable share of the blade's shaking power at 5 mm, and its gain falls
  when averaged over the wandering rotor speed.

## 8. Derived, cited, chosen

Derived (SymPy): the moving-pivot Lagrangian, its linearisation, the coupled matrices. Cited: Jonkman et al. 2009
(NREL/TP-500-38060); OpenFAST r-test NREL 5-MW blade file. Chosen: the shaking range, ζ_e = 0.5 % and 3 %, pivot at 90 %.

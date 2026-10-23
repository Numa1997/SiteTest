# Skeptic, Gate 1, contract L3 (elastic blade: gravity sag and edgewise shaking), round 1

Blind adversarial read of `contract-L3.md`, 23 October 2026. Read: the contract, `contract-L0.md`, `derive/L3_sag.py`, `L3_sag_numbers.py`,
`L3_sag_check.py`, `L3_sag.json`, `L3_shake2.py`, `L3_shake2.json` and `nrel5mw.py`. Not read: status, referee notes, earlier skeptic
notes.

My own run (session scratchpad, not in the repository):
`/tmp/claude-0/-home-user-SiteTest/8b34d6df-5462-5589-b418-3710ebaaeab4/scratchpad/sk/sagstatic.py`. It integrates the static gravity
deflection of the cantilever directly from the OpenFAST blade table: shear, then moment, then curvature M/EI, then slope, then
deflection. It applies the same 1P dynamic factor and the same g cos 5°, once with EdgStff alone and once with the in-plane compliance
projected through the structural twist (cos²τ/EI_e + sin²τ/EI_f). It then puts w and w′ into the same linear power formula as
`L3_sag_numbers.py`.

## What checks out (no objection)

- **Moving-pivot Lagrangian.** I re-derived the pivot term by hand. With u = −w cos Ωt along the rotating tangent e_t, the pivot's
  inertial acceleration along e_t is ü − Ω²u = 2Ω²w cos φ. Gravity's tangential component is −g cos φ e_t, and the d'Alembert force
  −m·2Ω²w cos φ e_t points the same way. So the sag adds 2Ω²w to g in the drive, as claimed. The Coriolis part (2u̇ė_t) is radial: it
  modulates the centrifugal stiffness, which is second order. The SymPy script checks the reduction to L0 and the forcing.
- **Section rotation.** For an Euler–Bernoulli section, β = ∂u/∂r. The signs of u and β agree (u = −w cos φ, β = −w′ cos φ). The rod
  is a free body steered by the apparent gravity, which stays almost radial. The stator turns with the section, so the brake sees
  θ − β, and the generator's power is c(θ̇ − β̇)². This is right, and leaving it out would be wrong.
- **One-way pivot for the sag.** 0.1 kg against a 17.7 t blade, so the reaction on the 1P sag is negligible.
- **Two-way shaking model.** The damping matrix C = c r rᵀ with r = (−Φ′_p, 1) puts the generator's reaction torque back onto the blade
  mode. M, G and K are constant at uniform Ω, G is skew and K comes from a Lagrangian. Rejecting the one-way model (94 W, above the
  power fed in) is correct.
- **Flapwise motion (not discussed in the contract, but harmless).** Flap slope tilts the hinge axis. The in-plane field changes only
  by cos ψ (second order), and pivot motion along the hinge axis exerts no torque. Add one sentence saying so.

## Objections

### M1 (major). Sag: the cancellation makes P1 depend on the deflection shape, and a direct static integration puts it at +2.0 %
**Claim.** The sag changes the single pendulum's power by −0.3, −0.6 and +0.7 % (P1: < 2 %).
**Why it may be wrong.** The net figure is the difference of two large terms. At 90 %, the drive term is +14.5 % and the section rotation
takes back about 14 %. The balance depends on the ratio w′r_p/w: the two terms cancel when w′r_p ≈ 2w, which is a local property of the
deflected shape. The contract takes w and w′ from the **single polynomial mode shape** of the first edgewise mode. A static gravity load
is not the mode shape, and polynomial mode fits are least accurate in slope.
**Measured** (`sagstatic.py`): direct static integration of the same blade table.

| Pivot | Modal: w (mm), w′ (mrad), w′r/w | Static, EdgStff: w (mm), w′ (mrad), w′r/w | Net change: modal (contract) | Net change: static, EdgStff | Net change: static, twist-projected |
|---|---|---|---|---|---|
| 30 % | 31.5, 4.24, 2.54 | 37.1, 4.72, 2.40 | −0.3 % | −0.26 % | −0.28 % |
| 60 % | 165, 9.70, 2.22 | 170, 8.94, 1.98 | −0.6 % | +0.09 % | +0.06 % |
| 90 % | 384, 12.97, 1.91 | 362, 10.91, 1.71 | +0.7 % | **+1.99 %** | **+2.06 %** |

So the 90 % result moves by 1.3 percentage points with the shape model. The better model, the static deflection, puts it on or just over
P1's 2 % line. The "must reproduce" test (linear against nonlinear within 0.2 pp) checks the integrator, not this modelling choice, which
dominates the error.
**Settles it.** Use the static deflection under the distributed gravity load, or several modes, for both w and w′. Quote the spread as
the uncertainty. The physical conclusion ("the sag is a couple of per cent at most") probably survives. P1 as stated may not.

### M2 (major). Tuned rod: gravity's 1P stiffness modulation is left out, and it is first order
**Claim.** In the shaking part "gravity [is] left out (its 1P effect is the sag above)". The tuned rod's gain is quoted at fixed Ω and
averaged over speed wander (observable (c), P3).
**Why it is wrong.** The sag part takes care of gravity's **forcing**. It does not take care of gravity's **parametric** term. Linearised
(L0), the rod's stiffness is R − G sin φ, so it is modulated once per turn by G/R = g/(Ω² r_p) = 0.19 at the 90 % pivot. That value does
not depend on the rod length. The tuned rod's own frequency therefore sweeps by **±9.6 % every turn** (period 6.6 s). The bands it is
meant to sit inside are much narrower:

| Band | Half-width |
|---|---|
| Blade mode, ζ_e = 0.5 % | ±0.5 % |
| Blade mode, ζ_e = 3 % | ±3 % |
| The rod's own damping at the optimum (c = 0.0059 N m s) | ζ ≈ 0.35 %, settling time about 40 s |

This is the same mechanism that cut the gain by a factor of 7 (19.1 to 2.75 mW) in the speed-wander average, at a comparable depth
(9.6 % against σ = 10.3 %), and it is present at every instant, not only in gusts. Because the modulation is faster than the absorber
settles, it spreads the response into sidebands at ω_e ± kΩ rather than detuning slowly. The loss can be anything from tens of per cent
to the factor of 7. The contract does not bound it.

In addition, the tuned rod also carries a 1P gravity swing of G/(R − 1) ≈ 0.2 rad (quasi-static, lightly braked) on top of 0.17–0.27 rad
rms of shaking. The amplitude detuning of a pendulum, Θ²/16 ≈ 0.5–1.5 %, is again of the order of both bandwidths. A5 accepts the linear
model at 5 mm, and that acceptance is not safe for a device whose whole value is a narrow resonance.
**Settles it.** Integrate the tuned rod in the time domain, two-way with the blade mode, with gravity (forcing and parametric) and the
full sin θ. Drive it with a band-limited random modal force at 5 mm tip rms, at uniform Ω and then with the L2 wander. Quote the gain
against the linear 19 mW / 2.75 mW. Until then, observable (c) and P3 are not established.

### M3 (major, process). The predictions were written after the runs
The contract says so honestly. P1's thresholds (2 %) and P2's (10 %) sit well above results that were already known (≤ 0.7 %, 0.6 %), and
P3 has no number ("a sizeable share"). None of them could have failed when written.
**Settles it.** Register at least one fresh, numeric prediction before the next run, and test it. Natural candidates: the static-shape
sag at 90 % (M1), or the tuned rod's gain under gravity modulation, as a stated interval (M2).

### Minor
- m1. **A5 does not match the JSON.** A5 says the tuned rod swings 0.21 rad rms at 5 mm. `L3_shake2.json` gives 0.265 rad (ζ_e = 0.5 %)
  and 0.169 rad (3 %). Quote both, with their ζ.
- m2. **A3: the shaking level has a source in reach.** The OpenFAST r-test, already cited for the blade file, also ships regression
  outputs for the NREL 5-MW in turbulent wind (the `5MW_Land_DLL_WTurb` case). The in-plane tip deflection there gives the rms near
  1.08 Hz directly. "No source found" should become that number, or a reason it cannot be used. The conclusions swing on it: at 100 mm,
  Sol's rod takes 23 mW from shaking against 8.9 mW from gravity.
- m3. **The energy bound is a consistency check, not evidence.** A passive, linear, time-invariant system with positive damping
  satisfies P_gen ≤ P_in automatically: G is skew and the Jacobi integral is conserved. Present it as a code check.
- m4. **Speed-wander averaging is quasi-static.** It is valid only if Ω wanders more slowly than the absorber settles (about 40 s).
  Give the L2 wander's correlation time next to it. The integration band 0.7–1.3 ω_e also cuts off the rod's resonance at 3σ of the
  wander (1.31 ω_e).
- m5. **Mode frequency.** 1.0793 Hz is FAST's "1st blade asymmetric edgewise" system mode. That is right for the 1P gravity sag, which
  is cyclic across the three blades. Collective edgewise content of turbulence couples to drivetrain torsion (about 0.6 Hz) instead.
  State that the shaking model covers only the asymmetric part.
- m6. **1P aerodynamic in-plane loads.** Wind shear, tilt and tower shadow are left out. My estimate is about 3 % of the gravity root
  moment at 8 m/s (rotor torque/3 ≈ 0.67 MN m, a 1P swing of order ±15 %, against g·S_root = 3.6 MN m). State it as an assumption.
- m7. **Centrifugal stiffening and in-plane softening of the static sag.** These enter as (K − 1)(Ω/ω_e)² ≈ 2 %. That is negligible
  alone, but it can shift w′/w, which matters because of M1.
- m8. **P2 is not a test.** At 5 mm the shaking harvest is 0.6 % of gravity's, known before the contract.

## Verdict: FAIL

Must be answered: **M1** (the sag shape: P1 sits on its threshold under a better deflection model), **M2** (gravity's 1P parametric
modulation and the amplitude detuning of the tuned rod are left out, so observable (c) and P3 are not established) and **M3** (a fresh
prediction). No fatal objection: the moving-pivot Lagrangian, the section-rotation argument and the two-way coupling are correct.

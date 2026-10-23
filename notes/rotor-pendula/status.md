# Rotor Pendula: status

Read this first every turn. Brief: `brief.md`. Definition of done: `done.md`. Branch: `claude/dazzling-heisenberg-esnqek`.
Loop: `/goal` cannot be set from inside the session (it is typed by Numa); the fallback of brief 1.1 is in force: never end a
turn while the queue has an item I can act on; `send_later` "Resume from notes/rotor-pendula/status.md" if a turn must end.

## Numa's direction (23 Oct 2026, mid-run)

"We are not writing a paper, we are writing a lecture note. Be careful how wacky or far you go; so long as it is readable
and understandable, I am fine." Rule from here: every computation must earn a figure or a sentence a student reads; no
exhaustive scans; the ladder stays, but each level is as small as its question allows.

## Page 1. Fermi estimates of observable 1, before any model (23 October 2026)

Computed by `derive/scales.py` and `derive/fermi.py`; (prov) = provisional turbine value until the scouts' dossiers arrive.
Observable 1 is the mean power the generator takes from the swing (mechanical; electrical after L4).

| Source (brief 4.2) | Estimate | Mechanism | What would make it wrong |
|---|---|---|---|
| E0 gravity, uniform rotation | 9.58–57.1 mW on the 18 mountings (L0 optimum); 26.8 mW on an NREL-5MW-like rotor at 30 % span; hard ceiling m g L Ω = 164–411 mW on the large rotors | gravity turns once per turn in the blade frame and pushes the bob off its centrifugal equilibrium | swings not small where 1/Γ = 0.70 (8 rpm, 30 %): nonlinear correction |
| E1a rotor speed, dynamic Euler terms | ~5 µW = 2 × 10⁻⁴ of E0 | Ω̇ forces θ quasi-statically, θ ≈ −ε with ε = Ω̇/Ω² ≈ 0.024 rms, far below G = 53 and R = 94 | rotor time constant (6.5 s, prov) much shorter than estimated |
| E1b rotor speed, quasi-static operating point | +s²/2 ≈ +1.1 % for s = σ_Ω/Ω̄ = 0.15 (prov) | at fixed generator constant c, P(Ω)/P(Ω₀) = 2/(1 + Ω²/Ω₀²) is convex in Ω; Jensen | rotor-speed limits clip σ_Ω |
| E2 blade edgewise vibration | resonant, at the gravity-optimal damping: P_e = 2(A/g)² P*; 0.02 % at A = 0.1 m/s², 2 % at 1 m/s², 19 % at 3 m/s² | base shaking along the tangent, where a radial rod has the full effective mass | the edgewise acceleration A at the pivot is unknown: scout S2 |
| E3 turbulence on an exposed bob | drag 0.05–0.49 of the bob's weight at 16.8–50.4 m/s; the rotor pays 0.90–24.3 W | quadratic drag on a 14.5 mm steel sphere | none: the bob must sit inside the blade shell, where the air turns with the blade; E3 = 0 |

Observable 3 (the blade): the rotor's share is 10⁻⁸–10⁻⁴ (Sol: ≤ 7.2 × 10⁻⁵). A perfectly tuned, lightly damped bob is a tuned
mass damper of mass ratio μ = mΦ²/m_modal: 6 × 10⁻⁷ at 30 % span, 6 × 10⁻⁵ at 90 % (prov), adding at most √(μ/8) = 0.03–0.3 %
of critical damping against the blade's 0.477 %. At the gravity-optimal damping the bob is nearly locked to the blade: far less.

Expectation (opinion, to be tested, not assumed): gravity dominates; turbulence enters through the blade only if the edgewise
acceleration at the pivot approaches g; chaos spreads the mobility over a wide band and should lose to a tuned single pendulum.

## Queue (first open item first)

1. [running] Power theorem Monte Carlo, full statistics (`derive/power_theorem_mc.py` → `mc_full.log`, ~25 min).
2. [running] L1 engine checks and Sol's 18 mountings (`derive/L1_engine_check.py` → `L1_engine_check.log`).
3. [running] `contract-L0.md` → blind skeptic (opus) → answer every objection in the contract.
3b. L1 Lyapunov maps over (G, R, κ) with ensembles of initial conditions; Sol's chaos group (R = 1, G = 3.065).
4. Gate 2 for L0: checker writes `check-L0.md` (SymPy + Wolfram).
5. L1 contract; nonlinear single and double, uniform rotation (Python reference + JS physics block); reproduce the 18 mountings,
   the ratio 0.64–0.74 and Sol's chaos numbers; Lyapunov maps over (G, R, κ) with spreads.
6. L2 contract; IEC wind (Kaimal) + one-state rotor of the reference turbine; ensembles of 10-minute records.
7. L3 contract; one edgewise modal degree of freedom; single tuned, double regular, double chaotic at best damping; quantiles.
8. L4 contract; generator as an electrical machine (EMF constant, coil resistance, load, gearbox).
9. Site: `portfolios-src/rotor-pendula/` (physics block, textbook, simulation page, worked problems, number script, Python checks,
   browser check, build script keeping Sol's report and `study/`).
10. Gate 3: runner checks; blind skeptic on the rendered pages, six thresholds.
11. Portfolios article, docs, inventory; push; pull request into main, not merged.
12. Numa (23 Oct): when fully done, write a prompt that deploys "astra" (unknown to me; asked what it is) over the relevant parts of the repo to inspect the study, confirm it is physically solid and well written, and explain it to him. He reads nothing before that review passes.

## Done (with evidence)

- `derive/L0_single.py` rerun: 7 PASS, ALL PASS; P* at Sol's best mounting 57.13 mW (Sol 57.1). 23 Oct.
- `derive/scales.py`: brief 4.2 numbers reproduced (R 2.01–300.8; pendulum 1.34–16.35 Hz, large rotors 1.34–3.66 Hz;
  push 0.133–6.667 Hz; ratio 1.42–17.34; Γ 1.43–215.2; ceiling 164–411 mW; pivot speed 16.8–50.4 m/s). 23 Oct.

- Scouts returned 23 Oct: `dossier-turbine.md` (NREL 5-MW from the report via OSTI and the OpenFAST files; TurbSim guide
  for IEC ed. 3), `dossier-edgewise.md` (no sourced edgewise acceleration at 30/60/90 % span; 1P gravity dominates; edgewise
  mode ~25 dB below 1P in tip displacement in an IEA 15-MW simulation; sweep needed), `dossier-harvesting.md` (no source shows
  chaos beating a linear harvester at equal mass and best damping; Halvorsen 2013 PRE bound for white noise, read in full).
- `derive/power_theorem.py`: 12 PASS, ALL PASS (generalised force −a b(q), b = ∇(M e·x_cm); Itô term (S/2) bᵀM⁻¹b also with a
  gyroscopic vector; noise coefficient independent of p so Itô = Stratonovich; M − m_eff as an explicit sum of squares for single
  and double).
- `derive/power_theorem_mc.py --quick` (N = 300, 20 s): 3 of 4 within 3 %; single small swings 4.46 % off at ±1.95 % standard
  error (statistics, not physics); <m_eff>/M = 0.50 (single, large swings), 0.61 (double, chaotic, 66 turn-overs per trajectory).
- `derive/L0_table.py`: 6 PASS (g = 9.80665 as Sol): LTI at Sol's damping = his stored linear rows (< 10⁻⁴ %); his damping is
  κ = R − 1 except at 14 rpm 30 % and 8 rpm 30 %, where his report says he refined it nonlinearly; LTI P* within 0.68 % of his
  nonlinear runs at all 18; span 9.55–57.1 mW; share ≤ 7.20 × 10⁻⁵. Finding: Hill (parametric term alone) overshoots by 11.6 %.
- `derive/L1_double.py`: 7 PASS (energy book 10⁻¹³; Lagrange = Newton in the blade frame 6 × 10⁻¹⁵ with Ω̇ ≠ 0; Sol's two
  dimensionless equations; Euler terms; single limit with c₁ = 0).
- C_p(λ): ROSCO `Cp_Ct_Cq.NREL5MW.txt` (NREL/ROSCO GitHub, written Jan 2022, CCBlade): peak 0.466 at λ = 7.5, β = 0; Jonkman's
  report says 0.482 at 7.55 (FAST). 3.4 % apart; ROSCO used for the curve's shape.

## Found along the way

- **Brief 4.3 corrected:** a double pendulum reaches m_eff = M_total whenever its TOP rod is perpendicular to e, whatever the
  lower rod does (turning ψ₁ at fixed absolute ψ₂ translates both bobs together). Proven in SymPy (`power_theorem.py`).
  On a blade at rest both rods lie radially and e is tangential, so single and double start with the same m_eff = M.
- Sol used g = 9.80665 m/s²; with 9.81 every power is 0.07 % higher.

- Sources: www.nrel.gov refuses the proxy; the NREL 5-MW model files come from github.com/OpenFAST/r-test (blade file read,
  8049 bytes), and the report through osti.gov (reachable).
- Brief 4.2 says "Sol's resonance at r_p = L"; Sol's chaos scan sits at R = 1 (r_p = 0.2 m, Ω = 4 rad/s), not a real mounting.

## Provisional choices (named, with their price)

- P1. Part II uses the NREL 5-MW reference turbine at its own operating point (λ* ≈ 7.55, Ω ≈ 9.2 rpm at 8 m/s), not Sol's
  λ = 7 rotors; Sol's 8 rpm, 66.8 m rotor is the nearest of his. Price: Part II's mountings are not literally Sol's.
- P2. The bob sits inside the blade shell (E3 above). Price: the chord and thickness must hold a ±0.2 m swing; to be checked.

## Decisions for Numa

- D1 (default in force): the portfolio has two parts, Sol's uniform-rotation study (Part I, reproduced and checked) and the
  turbulent-wind study (Part II, new).
